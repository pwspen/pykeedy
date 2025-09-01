from pykeedy import VMS, PageProp, LocusProp
from pykeedy.datastructures import Manuscript, Page, Locus

# If you want to do more complex filtering / analysis, you can get the full Manuscript object
vms = VMS.get()

# 'VMS' is mostly just a wrapper for a Manuscript object, so you can do vms.to_text(), vms.to_lines(), etc

# There are three main data storing objects: Manuscript (what's returned above), Page, and Locus
# Manuscript contains pages which is a list of Page objects, and each Page contains loci which is a list of Locus objects
# To check the properties available on any object:

vms.print_fields() # Only source_filename and pages
print('-----')
vms.pages[0].print_fields() # All page level properties
print('-----')
vms.pages[0].loci[0].print_fields() # All locus level properties
print('-----')

# Directly accessing the properties lets you do whatever filtering / analysis operations you can think of
b_and_herbal = len(list(page.name for page in vms.pages if page.currier_language == PageProp.CurrierLanguage.B
                                                        and page.illustration == PageProp.Illustration.Herbal))

b_or_herbal = len(list(page.name for page in vms.pages if page.currier_language == PageProp.CurrierLanguage.B
                                                       or page.illustration == PageProp.Illustration.Herbal))
print(f'B and Herbal: {b_and_herbal}, B or Herbal: {b_or_herbal}') # B and Herbal: 32, B or Herbal: 180

# You can swap out pieces of individual objects:
page = vms.pages[0]
print(len(page.loci)) # 28

page.loci = [locus for locus in page.loci if locus.location != LocusProp.Location.BelowPrev]
print(len(page.loci)) # 8

# You shouldn't need to create new objects from scratch, but you can do it:
nothing = Manuscript(pages=[])
print(nothing.to_words()) # []