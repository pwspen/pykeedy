from pykeedy.utils import load_corpus

# Returns all available plaintexts in a {name: text} dict
plain = load_corpus()
print(list(plain.keys()))
# ['inferno', 'meidekranz', 'naturalis']
# Built in corpus is Dante's Infero (Italian), Der Meide Kranz (German), and (part of) Pliny's Naturalis Historia (Latin)

# You can also point this at any directory containing .txt files,
# and it will process them as manuscripts.
plain = load_corpus(from_dir=".")  # current directory has 'book.txt'
print(plain)
# {'book': 'thisisafile\nused for showing\nthe functionality\nof loadcorpus'}
# original: 'This+is!a^File\nused for Showing\nthe Functionality\nof load_corpus!'
# Extraneous characters stripped, everything lowercased

plain = load_corpus(from_dir=".", give_objects=True)
# This gets us an object with methods .to_text(), .to_words(), .to_lines()

book = plain["book"]
print(book.to_words())
# ['thisisafile', 'used', 'for', 'showing', 'the', 'functionality', 'of', 'loadcorpus']

# You can also only select certain texts by name
print(load_corpus(from_dir=".", names="book"))  # Prints
print(load_corpus(from_dir=".", names="harrypotter"))  # ValueError: No texts found
