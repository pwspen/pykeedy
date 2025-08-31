from pykeedy.vms import get_processed_vms
from pykeedy.analysis import scatterplot, load_corpus
from pykeedy.utils import shannon_entropy, conditional_entropy

# Returns all available plaintexts in a {name: text} dict
plain = load_corpus()
plain["vms"] = get_processed_vms()
results = {}
for name, text in plain.items():
    # Pair entropy also available
    # For word-level entropy, the only change is adding the below line
    # text = text.split(' ')
    results[name] = (shannon_entropy(text), conditional_entropy(text))
scatterplot(results, key=(f"character entropy (bits)", "conditional entropy (bits)"), fname="entropy_comparison.png")