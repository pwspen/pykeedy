from pykeedy import VMS
from pykeedy.analysis import scatterplot, load_corpus
from pykeedy.utils import shannon_entropy, conditional_entropy

# Compute and save plots of character and conditional entropy of the VMS vs comparison plaintexts

# Returns all available plaintexts in a {name: text} dict
plain = load_corpus()

# For word-level entropy, all you have to do is change below to .to_words()
plain["vms"] = VMS.to_text()
results = {}
for name, text in plain.items():
    # Pair entropy also available
    results[name] = (shannon_entropy(text), conditional_entropy(text))
# saves in current folder
scatterplot(results, key=(f"character entropy (bits)", "conditional entropy (bits)"), fname="entropy_comparison.png")