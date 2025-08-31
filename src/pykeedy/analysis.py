from pykeedy.crypt import greshko_decrypt, naibbe_encrypt, preprocess
from pykeedy.utils import load_corpus, shannon_entropy, conditional_entropy
from pykeedy.vms import get_processed_vms
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal, Sequence

def test_reconstruction(text: str, n: int = 1000) -> float:
    def levenshtein(a, b):
        if len(a) < len(b):
            return levenshtein(b, a)
        if len(b) == 0:
            return len(a)
        
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a):
            curr = [i + 1]
            for j, cb in enumerate(b):
                curr.append(min(prev[j + 1] + 1,      # deletion
                            curr[j] + 1,           # insertion  
                            prev[j] + (ca != cb))) # substitution
            prev = curr
        return prev[-1] 
    
    avg = 0
    pre = preprocess(text)
    for i in range(n):
        decoded = greshko_decrypt(naibbe_encrypt(text, prngseed=np.random.randint(0, 2**32)))
        correct = len(pre) - levenshtein(decoded, pre)
        # print(decoded)
        # print(pre)
        # print(correct)
        # print(len(pre))
        avg += correct/len(pre)
    
    rec = avg / n
    print(f"Reconstruction accuracy: {rec*100:.2f}% over {n} trials of text length {len(pre)}")
    return rec

def test_entropy(encode_seeds: int = 1, mode: Literal["char", "word"] = "char") -> dict[str, tuple[float, float]]:
    # Load all available texts and encrypt each encode_seeds times
    # Add vms to corpus then calculate shannon & conditional entropy of each and return dict {name: (shannon, conditional)}
    if mode not in ("char", "word"):
        raise ValueError("mode must be 'char' or 'word'")
    plain = load_corpus()
    all: dict = {}
    for name, text in plain.items():
        all[name] = text
        for i in range(encode_seeds):
            all[name + f"_enc{i}"] = naibbe_encrypt(text, prngseed=i)
    all["vms"] = get_processed_vms()
    if mode == "word":
        for name, text in all.items():
            all[name] = text.split(' ')
    results = {}
    for name, text in all.items():
        results[name] = (shannon_entropy(text), conditional_entropy(text))
    
    return results

def add_axlabels(key: Sequence[str]) -> None:
    if not all(isinstance(x, str) for x in key) or len(key) != 2:
        raise ValueError("key must contain only 2 strings representing labels")
    
    plt.xlabel(key[0])
    plt.ylabel(key[1])

def scatterplot(d: dict, key: Sequence[str] | None = None, fname: str = "scatterplot.png") -> None:
    # Expect dict of {name: (x, y)} pairs
    # name: str, x & y: float
    for i, (name, (x, y)) in enumerate(d.items()):
        plt.scatter(x, y, label=name, c=f'C{i}')
        plt.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points')
    if key:
        add_axlabels(key)
    plt.savefig(fname)
    plt.close()

def barplot(d: dict, fname: str = "barplot.png", n_max: int = 20) -> None:
    names, values = zip(*d.items())
    names, values = list(names), list(values)
    if len(names) > n_max:
        names, values = names[:n_max], values[:n_max]
    plt.bar(names, values)
    add_axlabels(["Item", "Count"])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    
def heatmap(labels: list[str], matrix: list[list[int]], fname: str = "heatmap.png", n_max: int = 20) -> None:
    # Convert to numpy array for easier handling
    matrix_array = np.array(matrix)
    
    if len(labels) > n_max:
        labels = labels[:n_max]
        matrix_array = matrix_array[:n_max, :n_max]

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix_array, cmap='plasma', aspect='auto')
    
    # Set the ticks and labels
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    # Add colorbar
    plt.colorbar(im)
    
    # Add text annotations showing the values
    if len(labels) < 10:
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax.text(j, i, matrix_array[i, j], ha="center", va="center", color="black")
    
    # Add axis labels if key is provided and add_axlabels function exists
    add_axlabels(["First element", "Second element"])
    
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()