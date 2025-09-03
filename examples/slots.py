from pykeedy import VMS
from pykeedy.slots import BASIC13, BASIC11, COMPACT7, EXTENDED12, score_slot_grammar
from pykeedy.utils import scatterplot
# Use these for custom stuff

print(BASIC13)
# List of list of strings, one sub-list per slot
# [['ch', 'sh', 'q', 'y'], ['e', 'o', 'a'], ...

words = VMS.to_words()
results = {}  # Save results to plot them
for name, slots in [
    ("BASIC13", BASIC13),
    ("BASIC11", BASIC11),
    ("COMPACT7", COMPACT7),
    ("EXTENDED12", EXTENDED12),
]:
    score_dict = score_slot_grammar(words, slots)
    sigfigs = 3  # This line and below just for prettier printing
    print(name, {key: float(f"{val:.{3}g}") for key, val in score_dict.items()})
    results[name] = (score_dict["coverage"], score_dict["efficiency"])

# BASIC13 {'coverage': 0.489, 'efficiency': 0.000834, 'f1': 0.00166}
# BASIC11 {'coverage': 0.469, 'efficiency': 0.0016, 'f1': 0.00319}
# COMPACT7 {'coverage': 0.444, 'efficiency': 0.00623, 'f1': 0.0123}
# EXTENDED12 {'coverage': 0.812, 'efficiency': 4.17e-06, 'f1': 8.33e-06}

scatterplot(
    results, ax_names=("Coverage", "Efficiency"), fname="slot_grammar_scores.png"
)
