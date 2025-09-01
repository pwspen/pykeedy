from pykeedy import VMS
from pykeedy.analysis import barplot
from pykeedy.utils import frequency_rank

for mode in ["char", "word"]:
    # gets EVA transliteration of vms as string
    text = VMS.to_text() if mode == "char" else VMS.to_words()
    for i in range(1, 4):
        # saves results in current folder as pngs
        barplot(frequency_rank(text, n=i), fname=f"vms_{mode}_{i}-gram_freq.png")