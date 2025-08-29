from functools import lru_cache
import yaml
from importlib import resources
import re

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