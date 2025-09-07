# To run this you need to install additional libraries:
# pip install gensim
# pip install umap-learn

import numpy as np
from gensim.models import Word2Vec
import umap
from dataclasses import dataclass
import time

from pykeedy.analysis import frequency_rank, levenshtein_distance
from pykeedy.utils import load_corpus, scatterplot, seriesplot, barplot
from pykeedy.crypt import naibbe_encrypt_to_object


def preprocess_text(text: str) -> list[list[str]]:
    """Convert text to sentences of tokens for Word2Vec training."""
    # Replace periods with spaces and split by newlines to get sentences
    sentences = text.replace(".", " ").split("\n")

    # Tokenize each sentence (split by whitespace and filter empty tokens)
    tokenized_sentences = []
    for sentence in sentences:
        tokens = [token.strip().lower() for token in sentence.split() if token.strip()]
        if tokens:  # Only add non-empty sentences
            tokenized_sentences.append(tokens)

    return tokenized_sentences


def train_embeddings(
    sentences: list[list[str]],
    vecsize: int,
    window: int,
    min_count: int = 5,
    sg: int = 1,
    epochs: int = 500,
) -> Word2Vec:
    """Train Word2Vec model"""
    model = Word2Vec(
        sentences=sentences,
        vector_size=vecsize,  # Small embedding size
        window=window,  # Large context window for small dataset
        min_count=min_count,  # Focus on words with decent frequency
        sg=sg,  # Skip-gram (better for small datasets)
        epochs=epochs,  # More epochs since less data
        workers=16,
    )
    return model


def visualize_embeddings(model: Word2Vec, words: list[str], fname: str) -> None:
    """Extract embeddings, reduce to 2D with UMAP, and plot"""
    # Get embeddings for words that exist in the model
    valid_words = [word for word in words if word in model.wv]
    embeddings = np.array([model.wv[word] for word in valid_words])

    # Reduce to 2D using UMAP
    reducer = umap.UMAP(n_components=2, n_neighbors=min(15, len(valid_words) - 1))
    embedding_2d = reducer.fit_transform(embeddings)

    results = {
        word: (float(embedding_2d[i, 0]), float(embedding_2d[i, 1]))
        for i, word in enumerate(valid_words)
    }  # type: ignore

    scatterplot(results, ax_names=("UMAP Dimension 1", "UMAP Dimension 2"), fname=fname)


@dataclass
class EmbeddingSimilarityResult:
    sim_weighted_avg_edit_distance: float
    sim_scores: list[tuple[str, str, float]]
    # [word1, word2, similarity]
    # no duplicate comparisons


def analyze_embedding_similarities(
    model: Word2Vec, words: list[str]
) -> EmbeddingSimilarityResult:
    """Analyze embedding similarities & correlation between spelling similarity and embedding similarity."""
    # Filter to words that exist in the model
    valid_words = [word for word in words if word in model.wv]

    # Calculate weighted average Levenshtein distance for each word
    results = []

    sim_scores = []
    for i, word in enumerate(valid_words):
        weighted_distances = []
        weights = []

        # Only compare with later words so each word pair is only checked once
        for j in range(i + 1, len(valid_words)):
            other_word = valid_words[j]
            # Get cosine similarity and save
            similarity = model.wv.similarity(word, other_word)
            # similarity = max(0, similarity) # Only where positive
            sim_scores.append((word, other_word, similarity))

            # Calculate Levenshtein distance & normalize by word length
            lev_dist = levenshtein_distance(word, other_word)
            lev_dist /= (len(word) + len(other_word)) / 2

            # Without this things get kinda crazy
            # Maybe dominated by words that are very
            # dissimlar in both embedding and spelling
            if similarity > 0:
                weighted_distances.append(lev_dist * similarity)
                weights.append(similarity)

        # Calculate weighted average
        if sum(weights) > 0:
            weighted_avg_distance = sum(weighted_distances) / sum(weights)
            results.append((word, weighted_avg_distance, sum(weights)))

    sim_scores.sort(key=lambda x: x[2], reverse=True)

    # Sort by weighted average distance
    results.sort(key=lambda x: x[1])

    overall_avg = float(np.mean([r[1] for r in results]))

    return EmbeddingSimilarityResult(overall_avg, sim_scores)


def avg_and_stddev_result(
    results: list[EmbeddingSimilarityResult],
) -> tuple[EmbeddingSimilarityResult, EmbeddingSimilarityResult]:
    weighted_avgs = [r.sim_weighted_avg_edit_distance for r in results]
    sim_scores_arrays = [
        np.array([score for _, _, score in r.sim_scores]) for r in results
    ]

    avg_weighted = np.mean(weighted_avgs)
    std_weighted = np.std(weighted_avgs)

    avg_scores = np.mean(sim_scores_arrays, axis=0)
    std_scores = np.std(sim_scores_arrays, axis=0)

    # Use first result's word pairs for structure
    word_pairs = [(w1, w2) for w1, w2, _ in results[0].sim_scores]

    return (
        EmbeddingSimilarityResult(
            float(avg_weighted),
            [(w1, w2, float(score)) for (w1, w2), score in zip(word_pairs, avg_scores)],
        ),
        EmbeddingSimilarityResult(
            float(std_weighted),
            [(w1, w2, float(score)) for (w1, w2), score in zip(word_pairs, std_scores)],
        ),
    )


# top_n: how many of most/least similar word pairs to show
# most: True to show most similar, False to show least similar
def print_emb_result(
    name: str,
    result: EmbeddingSimilarityResult,
    stddev: EmbeddingSimilarityResult | None = None,
    top_n: int = 10,
    most: bool = True,
) -> None:
    print(f"\n\n{name} results:")
    print(
        f"similarity-weighted avg edit dist: {result.sim_weighted_avg_edit_distance:.2f} {f' ± {stddev.sim_weighted_avg_edit_distance:.2f}' if stddev else ''}"
    )

    print(f"{'Most' if most else 'Least'} similar word pairs:")
    for i, (w1, w2, sim) in enumerate(result.sim_scores[:: 1 if most else -1][:top_n]):
        print(
            f"{w1 + ' <-> ' + w2:15} | sim: {sim:.3f}{f' ± {stddev.sim_scores[i][2]:.3f}' if stddev else ''}"
        )


# Main execution
analyze = load_corpus(include_vms=True, limit_length=50000)
for name in ["naturalis", "inferno"]:
    analyze[name + "_naibbe_enc"] = naibbe_encrypt_to_object(
        analyze[name].to_text(), insert_newlines_every=10
    )

start = time.time()
emb_results = {name: [] for name in analyze.keys()}

# If you just want to analyze one set of hyperparameters, make these lists length 1
num_top_words = 50
min_count_included = (
    10  # Embedding training process omits all words below this frequency
)
# Varying above makes averaging results very annoying
sgs = [1]  # 1: skip-gram algorithm, 0: CBOW

total = len(sgs) * len(analyze)
completed = 0

for name, text in analyze.items():
    for sg in sgs:
        full_text: str = text.to_text()
        top_n_words: list[str] = list(
            frequency_rank(text.to_words(), normalize=False).keys()
        )[:num_top_words]

        # Preprocess text into sentences
        sentences = preprocess_text(full_text)

        # Train embeddings
        model = train_embeddings(
            sentences=sentences,
            vecsize=20,  # doesn't seem to matter much
            window=5,  # doesn't seem to matter much
            min_count=min_count_included,
            sg=sg,
        )

        # Optional - Save embeddings for later use
        # model.save("word_embeddings.model")

        # Save umap viz of top words, only for first loop
        if completed < len(analyze):
            visualize_embeddings(
                model, top_n_words, fname=f"{name}_word_embeddings_umap.png"
            )

        # Save similarity results
        emb_results[name].append(analyze_embedding_similarities(model, top_n_words))
        completed += 1
        print(f"{completed}/{total} after {time.time() - start:.1f} s")

res_per_ms = {}
for name, results in emb_results.items():
    avg, stddev = avg_and_stddev_result(results)
    res_per_ms[name] = (avg, stddev)
    print_emb_result(name, avg, stddev)

barplot(
    {name: val[0].sim_weighted_avg_edit_distance for name, val in res_per_ms.items()},
    ax_names=("Item", "Similarity-weighted avg edit distance"),
    fname="embedding_similarity_barplot.png",
)

seriesplot(
    {
        name: [(i, sim) for i, (_, _, sim) in enumerate(val[0].sim_scores)]
        for name, val in list(res_per_ms.items())[:10]
    },
    ax_names=("Word pair index (sorted)", "Cosine similarity"),
    fname="embedding_similarity_seriesplot.png",
)
