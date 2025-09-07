from pykeedy.naibbe import ConstructNaibbeEncoding, get_default_encoding

# Recommended to look at example naibbe_custom.py before this one

# The same example encoding from there:
simple_encoding = ConstructNaibbeEncoding(
    ngram_slot_tables=[{"a": ["x", "y"], "b": ["j", "la"], "c": ["loong", "c"]}],
    table_odds=[3, 1],
)
# This encoding will encode stuff, but it's not yet the same type of encoding as the default one ("greshko_2507").
# To get there we need to add some complication: "unigrams" and "bigrams".
# Unigrams are single letters that map to an encoding. Bigrams are letter pairs where each letter maps to an encoding.
# And importantly, for a single letter, the things it can map to as a unigram, first part of a bigram (bigram prefix), or second part, are 3 different sets of encodings.
# This system also defines the number of tables we need: 3.
# Here is what that looks like with a system that can only encode 2 letters:
encoding = ConstructNaibbeEncoding(
    ngram_slot_tables=[
        # Unigram table
        {"a": ["x", "y"], "b": ["j", "daiin"]},
        # Bigram prefix table
        {"a": ["qo", "da"], "b": ["dai", "ch"]},
        # Bigram suffix table
        {"a": ["keedy", "in"], "b": ["iin", "edy"]},
    ],
    table_odds=[3, 1],  # Order is same order as in ngram_slot_tables
    ngram_odds=[2, 1],  # Order is [unigram, bigram]
)
# We also have to introduce another odds list for picking unigrams and bigrams: ngram_odds.
# [2, 1] means that unigrams will be chosen 2/3 of the time and bigrams 1/3.
# So there are two levels of dice rolling: we roll once for the ngram size, then once again per letter for which option to use from that slot.
# This is now the same structure as the full encoding, just smaller.
# The encoding system from the Naibbe paper, named "greshko_2507" (default used by this library) has this structure:
# - alphabet: 23 original latin letters (english minus j, k, w)
# - 3 ngram slots: unigram, bigram prefix, bigram suffix
# - 6 encodings per letter in each slot, for a total of 23*3*6 = 414 different letter encodings (less unique ones)
# - table odds list of [5, 2, 2, 2, 1, 1]
# - ngram odds list of [1, 1] or optionally [47.2, 52.8]
# - many ambiguous encodings: more than 90% of unigram encodings are also valid bigrams
# (aka, for 90% of unigrams, bigram_prefix + bigram_suffix = unigram)
# There are also bigrams that can be composed in multiple ways
# Example: in the above encoding, daiin can be made like:
# "b" -> daiin (unigram)
# "ab" -> da + iin (bigram)
# "ba" -> dai + in (bigram)
# And there is no way to tell if all you have is "daiin".
# (see note at bottom for more info)

# We can directly access the default encoding system using pykeedy.naibbe.get_default_encoding.
# Run this file to see it printed.
get_default_encoding().print()

# Notes:
# This library supports unigram, unigram + bigram, and unigram + bigram + trigram systems. (1, 3, and 6 slot tables required respectively)
# The whole encoding system might seem pretty random. I highly recommend reading the paper it came from to understand the motivation:
# https://www.dropbox.com/scl/fo/2b39zi1f77tr9mc9p80rt/ADwDDHsLNG7WtT6O0sbN5_4?rlkey=5ap828aun23thr9pvznguzgor&st=88np74hd&dl=0
# It is ambiguous by design and was carefully sculpted to match VMS statistical properties, and is a breakthrough even if it looks ugly.
