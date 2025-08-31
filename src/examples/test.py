from pykeedy.crypt import encrypt, greshko_decrypt
import numpy as np
from pykeedy.analysis import test_reconstruction, test_entropy, scatterplot, barplot, load_corpus, heatmap
from pykeedy.vms import get_processed_vms
from pykeedy.utils import shannon_entropy, conditional_entropy, frequency_rank, cooccurence_matrix


plain = load_corpus()
plain["vms"] = get_processed_vms()

results = {}
for name, text in plain.items():
    results[name] = (shannon_entropy(text), conditional_entropy(text))

scatterplot(results, key=(f"character entropy (bits)", "conditional entropy (bits)"), fname="entropy_comparison.png")