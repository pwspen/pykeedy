from pykeedy import VMS, PageProp, LocusProp

# There are many different ways to work with the VMS text.
text = VMS.to_text()  # returns EVA transliteration as a string
lines = VMS.to_lines()  # EVA in a list of lines
words = VMS.to_words()  # EVA in a list of words

# There is a simple function to filter by most of the properties you could ever want
# (everything in IVTFF - Currier language, scribe hands, illustration types, etc.)
# Some properties are at page level and some are at locus level
# You access properties through PageProp and LocusProp

PageProp.print_props()
LocusProp.print_props()

# Only the pages and loci that match ALL the given properties will be returned (use as many properties as needed)
# All the same to_text, to_lines, to_words methods are available on filtered results
voynich_b = VMS.filter(props=[PageProp.CurrierLanguage.B]).to_text()

b_herbal = VMS.filter([PageProp.CurrierLanguage.B, PageProp.Illustration.Herbal]).to_lines()

b_herbal_nymphs = VMS.filter([PageProp.CurrierLanguage.B, PageProp.Illustration.Herbal, LocusProp.Type.BiologicalNymphLabel]).to_words()

print(b_herbal_nymphs) # [] - there are no voynich b herbal nymphs (see warning also)

