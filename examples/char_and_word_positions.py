from pykeedy import VMS
from pykeedy.analysis import position_distribution, frequency_rank
from pykeedy.utils import barplot

text = VMS.to_text()
word_tokens = VMS.to_words()
word_types = set(word_tokens)
lines = VMS.to_lines()
letters = set(text)
# ? means unknown character which we don't care about
letters.remove("?")
pages = VMS.to_pages()

# See warnings for characters that we passed but don't appear in words - these are omitted from results
position_distribution(letters, word_tokens, normalize=True, average=True)
# {'a': 0.45, 'b': 1.0, 'c': 0.18 ...
# This means that 'a' appears on average 45% through a word, 'b' appears only at the end of words, etc

position_distribution(letters, word_tokens, normalize=False, average=True)
# {'a': 2.14, 'b': 5.29, 'c': 1.07 ...
# When not normalizing, the number means characters, so 'a' is on average the second character

# Clearly due to b=1.0 from first example, we might want to filter things with few occurences
all_pos = position_distribution(letters, word_tokens, normalize=True, average=False)
# This now returns all positions: {'a': [0.1, 0.3, 0.2 ...], 'b': [1.0, 1.0] ...}

# Which we can easily turn back into an average but remove things with less than 20 occurences
many_occurs = {k: sum(v) / len(v) for k, v in all_pos.items() if len(v) > 200}

barplot(
    many_occurs,
    key=("Letter", "Avg pos in word"),
    fname="vms_letter_positions_in_words.png",
    n_max=len(many_occurs),
)
# Plot shows that m and n are virtually always at the end, and q virtually always at the start

# You can easily do the analysis at other levels
position_distribution(letters, lines)  # default is normalize=True, average=False
position_distribution(word_types, [text])  # 0 means start of manuscript, 1.0 means end

# Checking where the 20 most common words appear in lines, pages, manuscript
top_words = [k for k, v in frequency_rank(word_tokens).items()][:20]

# Word mode only counts occurences that are bounded by . or \n on both sides (otherwise e.g. there's 3 'a' words in '.aaa.')
barplot(
    position_distribution(top_words, lines, word_mode=True, average=True),
    key=("Word (most common on left)", "Avg pos in line"),
    fname="vms_top_words_pos_in_lines.png",
)

# As expected for a randomish distribution, they are mostly grouped around 0.5 (middle of page)
barplot(
    position_distribution(top_words, pages, word_mode=True, average=True),
    key=("Word (most common on left)", "Avg pos in page"),
    fname="vms_top_words_pos_in_page.png",
)

# However, they are not so evenly distributed in the manuscript as a whole
barplot(
    position_distribution(top_words, [text], word_mode=True, average=True),
    key=("Word (most common on left)", "Avg pos in VMS"),
    fname="vms_top_words_pos_in_manuscript.png",
)
