from pykeedy import VMS
from pykeedy.utils import load_corpus, scatterplot
from pykeedy.analysis import shannon_entropy, conditional_entropy
from pykeedy.crypt import naibbe_encrypt

# Compute and save plots of character and conditional entropy of the VMS, comparison plaintexts, and the Naibbe encryptions of those plaintexts
# builds on entropy_comparisons.py

# Returns all available plaintexts in a {name: text} dict
plain = load_corpus()

analyze = {}
for name, text in plain.items():
    analyze[name] = text
    analyze[name + "_naibbe_encoded"] = naibbe_encrypt(
        text
    )  # Uses Greshko encoding as default

# For word-level entropy, all you have to do is change below to .to_words()
analyze["vms"] = VMS.to_text()

results = {}
for name, text in analyze.items():
    print(name, len(text))  # Notice encoded length is about 4x plaintext length
    results[name] = (shannon_entropy(text), conditional_entropy(text))
# saves in current folder
scatterplot(
    results,
    ax_names=("character entropy (bits)", "conditional entropy (bits)"),
    fname="encrypted_entropy.png",
)
