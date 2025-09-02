from pykeedy import VMS, LocusProp
from pykeedy.analysis import barplot
from pykeedy.utils import frequency_rank

# Compute and save plots of most frequent words in Currier A vs Currier B

for lang in ("A", "B"):
    # Convert to property using IVTFF codes, "A" or "B" for currier language
    text = VMS.filter([LocusProp.CurrierLanguage(lang)]).to_words() # Get words list (for char level: .to_text())
    barplot(frequency_rank(text, n=1), fname=f"vms_{lang}_word_freq.png")

