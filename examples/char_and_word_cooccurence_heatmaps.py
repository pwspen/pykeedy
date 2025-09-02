from pykeedy import VMS
from pykeedy.analysis import heatmap
from pykeedy.utils import cooccurence_matrix

# Compute and save heatmap plots of co-occurence / pair-attraction at character and word level in VMS

for mode in ["char", "word"]:
    # gets EVA transliteration of vms as string
    if mode == "word":
        text = VMS.to_words()
    else:
        text = VMS.to_text()
    # concurrence_matrix function can handle strings or lists, so it works for both character and word level analysis
    res = cooccurence_matrix(text, n=2)
    # saves results in current folder as pngs
    heatmap(*res, fname=f"vms_{mode}_cooccurence_heatmap.png")