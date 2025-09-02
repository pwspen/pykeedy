from pykeedy import VMS
from pykeedy.analysis import barplot
from pykeedy.utils import frequency_rank

# Compare the n-gram frequency ranks for n=1,2,3 at both character and word levels
# Save 6 plots in current folder

for mode in ["char", "word"]:
    # gets EVA transliteration of vms as string
    text = VMS.to_text() if mode == "char" else VMS.to_words()
    for i in range(3):
        # saves results in current folder as pngs
        gramsize = i + 1
        barplot(frequency_rank(text, n=gramsize), fname=f"vms_{mode}_{gramsize}-gram_freq.png")