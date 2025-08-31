from importlib import resources
import regex
import numpy as np

def preprocess(text: str) -> str:
    # preprocess text by deleting spaces and punctuation then lowercasing
    # \p{C} - Control characters (includes things like null bytes, tabs, newlines)
    # \p{M} - Mark characters (combining marks, accents, diacritics)
    # \p{P} - Punctuation characters (periods, commas, quotes, etc.)
    # \p{S} - Symbol characters (mathematical symbols, currency symbols, etc.)
    # \p{Z} - Separator characters including spaces, tabs, etc
    # regex is imported because standard re does not this type of syntax
    remove = regex.compile(r'[\p{C}|\p{P}|\p{S} ]+', regex.UNICODE) # space at end of pattern is important!
    text = remove.sub('', text)
    text = text.lower()
    return text

def frequency_rank(text: str | list[str], n: int = 1) -> dict[str, int]:
    # Accept either a string and return character frequency rank,
    # Or a list of words and return word frequency rank.
    # Return sorted descending
    char_level = isinstance(text, str)
    
    seq = np.array(list(text)) if char_level else np.array(text)

    if len(seq) < n:
        return {}

    # could be optimized but whatever
    ngrams = [seq[i:i+n] for i in range(len(seq)-n+1)]
    unique, counts = np.unique(ngrams, axis=0, return_counts=True)
    
    sorted_indices = np.argsort(counts)[::-1]
    joiner = '' if char_level else ' '

    result: dict[str, int] = {}
    for idx in sorted_indices:
        key = joiner.join(unique[idx])  # works for all n, including n==1
        if ' ' in key:
            key = f"'{key}'"
        result[key] = int(counts[idx])
    
    return result

def cooccurence_matrix(text: str | list[str], n: int = 2) -> tuple[list[str], list[list[int]]]:
    char_level = isinstance(text, str)
    seq = np.array(list(text)) if char_level else np.array(text)
    
    if len(seq) < n:
        return [], []
    
    # Generate n-grams, excluding any containing spaces
    # TODO add option that includes spaces to calculate most common first and last letters
    ngrams = []
    exclude = [' ', '\n']
    for i in range(len(seq)-n+1):
        ngram = tuple(seq[i:i+n])
        if any(elem in exclude for elem in ngram):
            continue
        ngrams.append(ngram)
    
    # Get unique n-grams and their counts
    unique_ngrams, counts = np.unique(ngrams, axis=0, return_counts=True)
    
    # Counting the gram occurences in all ngram occurences
    # Note this duplicates anything not at the start or end of a sequence
    # We want that in this case
    element_counts = {}
    for ngram_array, count in zip(unique_ngrams, counts):
        for element in ngram_array:
            element_counts[element] = element_counts.get(element, 0) + count

    # Generate sorted-descending list of elements by their counts
    sorted_elements = sorted(element_counts.keys(), key=lambda x: element_counts[x], reverse=True)
    
    # Create element to index mapping
    element_to_idx = {elem: i for i, elem in enumerate(sorted_elements)}
    
    # Initialize matrix
    matrix = np.zeros(tuple(len(sorted_elements) for _ in range(n)), dtype=int)
    
    # Fill matrix using unique n-grams and their counts
    # This works for any n
    for i, ngram_array in enumerate(unique_ngrams):
        ngram_count = counts[i]
        # Reverseing elements to make columns first element and rows second
        idx = tuple(element_to_idx[elem] for elem in ngram_array)[::-1]
        matrix[idx] += ngram_count
    return sorted_elements, matrix.tolist()

def shannon_entropy(text: str | list[str]) -> float:
    # Accept either a string and return character entropy,
    # Or a list of words and return word entropy.
    seq = np.array(list(text)) if isinstance(text, str) else np.array(text)
    unique_chars, counts = np.unique(seq, return_counts=True)
    probabilities = counts / len(text)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return float(entropy)

def joint_entropy(text: str | list[str], n: int = 2) -> float:
    seq = np.array(list(text)) if isinstance(text, str) else np.array(text)
    
    if len(seq) < n:
        return 0.0
    
    # Get each ngram from sequence
    ngrams = [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]
    unique_ngrams, counts = np.unique(ngrams, axis=0, return_counts=True)
    probabilities = counts / len(ngrams)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return float(entropy)

def conditional_entropy(text: str | list[str], n: int = 2) -> float:
    return joint_entropy(text, n) - shannon_entropy(text)

def load_corpus(names: str | list[str] | None = None, prep: bool = True) -> dict[str, str]:
    """
    Load plaintext(s) and return dict[name: text]
    Accepts single name, list of names, or None for all available texts
    """
    text_dir = resources.files("pykeedy.data.plaintexts")
    result = {}
    for entry in text_dir.iterdir():
        if entry.is_file() and entry.name.endswith(".txt"):
            name = entry.name.strip(".txt")
            if names is not None:
                if isinstance(names, str):
                    if name != names.strip(".txt"):
                        continue
                elif isinstance(names, list):
                    if name not in [n.strip(".txt") for n in names]:
                        continue
            with entry.open("r", encoding="utf-8") as f:
                text = f.read()
            if prep:
                text = preprocess(text)
            result[name] = text
    return result