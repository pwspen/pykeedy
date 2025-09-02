from pykeedy import VMS

# There are a number of formats you can get the VMS text in:
text = VMS.to_text()       # Full text as single string (including newline characters \n)
lines = VMS.to_lines()     # List of lines (locuses)
words = VMS.to_words()     # List of words

# For each of these, you can choose the transliteration alphabet (EVA or CUVA) as an argument
# and whether or not to normalize all gaps to spaces (represented by '.')
# The default is alphabet="eva" and normalize_gaps=True
text_cuva = VMS.to_text(alphabet="cuva", normalize_spaces=False)

# See filtering_basic.py and filtering_custom.py for how to filter to certain parts of the text