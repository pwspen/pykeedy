from pykeedy.vms import get_processed_vms
from pykeedy.analysis import barplot
from pykeedy.utils import frequency_rank

for mode in ["char", "word"]:
    # gets EVA transliteration of vms as string
    text = get_processed_vms()
    if mode == "word":
        # frequency_rank function can handle strings or lists, so it works for both character and word level analysis
        text = text.split(' ')
    for i in range(1, 4):
        # saves results in current folder as pngs
        barplot(frequency_rank(text, n=i), fname=f"vms_{mode}_{i}-gram_freq.png")