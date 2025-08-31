from pykeedy.vms import get_processed_vms
from pykeedy.analysis import heatmap
from pykeedy.utils import cooccurence_matrix

for mode in ["char", "word"]:
    # gets EVA transliteration of vms as string
    text = get_processed_vms()
    if mode == "word":
        text = text.split(' ')
    # concurrence_matrix function can handle strings or lists, so it works for both character and word level analysis
    res = cooccurence_matrix(text, n=2)
    # saves results in current folder as pngs
    heatmap(*res, fname=f"vms_{mode}_cooccurence_heatmap.png")