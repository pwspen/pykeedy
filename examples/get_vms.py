from pykeedy import VMS

# There are a number of formats you can get the VMS text in:
# (note: the outputs from to_text and to_pages contain newlines \n)
text = VMS.to_text()      # Full text as single string
pages = VMS.to_pages()    # List of strings, each is a page
lines = VMS.to_lines()    # List of strings, each is a line
words = VMS.to_words()    # List of strings, each is a word

# For each of these, you can choose the transliteration alphabet (EVA or CUVA) as an argument
# and whether or not to normalize all gaps to spaces (represented by '.')
# The default is alphabet="eva" and normalize_gaps=True
text_cuva = VMS.to_text(alphabet="cuva", normalize_gaps=False)

# See filtering_basic.py and filtering_custom.py for how to filter to certain parts of the text