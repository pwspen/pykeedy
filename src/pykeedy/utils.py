from functools import lru_cache
import yaml
from importlib import resources
import re
import numpy as np

@lru_cache(maxsize=1)
def _load_encodings() -> dict[str, str]: # [enc_name: filename]
    enc_dir = resources.files("pykeedy.data.encodings")
    result = {}
    for entry in enc_dir.iterdir():
        if entry.is_file() and entry.name.endswith(".yaml"):
            with entry.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            try:
                result[data["encoding"]["name"]] = entry.name
            except KeyError:
                print(f'Warning: Encoding file {entry.name} does not contain "encoding"->"name" key and cannot be parsed, skipping')
    return result

def load_encodings(force_update: bool = False) -> dict[str, str]:
    if force_update:
        _load_encodings.cache_clear()
    return _load_encodings()

def preprocess(text: str) -> str:
    # preprocess text by deleting spaces and punctuation then lowercasing 
    text = re.sub(r'[ .,;:!?\'\"()\[\]{}\-_/\\@#$%^&*+=<>~`|]', '', text)
    text = text.lower()
    return text

def shannon(text: str | list[str]) -> float:
    # Accept either a string and return character entropy,
    # Or a list of words and return word entropy.
    seq = np.array(list(text)) if isinstance(text, str) else np.array(text)
    unique_chars, counts = np.unique(seq, return_counts=True)
    probabilities = counts / len(text)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return entropy

def joint(text: str | list[str], n: int = 2) -> float:
    seq = np.array(list(text)) if isinstance(text, str) else np.array(text)
    
    if len(seq) < n:
        return 0.0
    
    # Get each ngram from sequence
    ngrams = [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]
    unique_ngrams, counts = np.unique(ngrams, axis=0, return_counts=True)
    probabilities = counts / len(ngrams)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return entropy

def conditional(text: str | list[str], n: int = 2) -> float:
    return joint(text, n) - shannon(text)

def load_text(name: str) -> str:
    if not name.endswith(".txt"):
        name += ".txt"
    text_dir = resources.files("pykeedy.data.plaintexts")
    path = text_dir / name
    with path.open("r", encoding="utf-8") as f:
        return f.read()