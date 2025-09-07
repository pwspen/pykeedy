from pykeedy import VMS
from pykeedy.utils import barplot
from pykeedy.analysis import frequency_rank

# Compare the n-gram frequency ranks for n=1,2,3 at both character and word levels
# Save 6 plots in current folder

for mode in ["word", "char"]:
    # gets EVA transliteration of vms as string
    text = VMS.to_text() if mode == "char" else VMS.to_words()
    for i in range(0, 5):
        # saves results in current folder as pngs
        gramsize = i + 1
        barplot(
            frequency_rank(text, n=gramsize, normalize=False),
            ax_names=(f"{mode} {gramsize}-gram", "Frequency"),
            fname=f"vms_{mode}_{gramsize}-gram_freq.png",
        )
