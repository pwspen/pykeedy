from pykeedy import VMS
from pykeedy.analysis import seriesplot
from pykeedy.utils import length_distribution
from collections import Counter

# Plot the distribution of word lengths in the VMS

words = VMS.to_words()

results = {
    "token": length_distribution(words),
    "type": length_distribution(list(set(words))) # only the unique words
}

seriesplot(results, key=("Word length", "Count")) # saves "seriesplot.png" in current folder

# You can also do this quite easily without the library, and the library
# uses this exact same code internally:
token_lengths = [len(word) for word in words]

token_length_counts = Counter(token_lengths)

token_length_tuples = tuple(sorted(token_length_counts.items()))

# seriesplot({"token length": token_length_tuples}, key=("Word length", "Count"))