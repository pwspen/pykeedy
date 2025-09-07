from pykeedy.utils import scatterplot
from pykeedy.analysis import shannon_entropy, conditional_entropy
from pykeedy.utils import load_corpus

# Compute and save plots of character and conditional entropy of the VMS vs comparison plaintexts

# Returns all available plaintexts in a {name: text} dict
plain = load_corpus(include_vms=True)

# For word-level entropy, all you have to do is change below to .to_words()
results = {}
for name, text in plain.items():
    # Pair entropy also available
    results[name] = (
        shannon_entropy(text.to_text()),
        conditional_entropy(text.to_text()),
    )
# saves in current folder
scatterplot(
    results,
    ax_names=("character entropy (bits)", "conditional entropy (bits)"),
    fname="entropy_comparison.png",
)
