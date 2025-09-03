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

scatterplot(
    results, ax_names=("Coverage", "Efficiency"), fname="slot_grammar_scores.png"
)
