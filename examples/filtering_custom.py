from pykeedy import VMS, LocusProp as Prop
from pykeedy.datastructures import IVTFFManuscript

# If you want to do more complex filtering / analysis, you can get the full Manuscript object
vms = VMS.get()

# 'VMS' is mostly just a wrapper for a Manuscript object, so you can do all the same stuff
vms.to_lines(normalize_gaps=False)
vms.to_words(alphabet="cuva")

# The main data-storing class this library uses is Locus
# Each one is one line from the IVTFF file
# Manuscript is mostly just a list of locuses / loci

vms.print_fields()  # Only source_filename and loci
print("-----")
vms.loci[0].print_fields()  # All locus level properties
print("-----")

# Directly accessing the properties lets you do whatever filtering / analysis operations you can think of
b_and_herbal = [
    locus for locus in vms.loci if locus.currier_language == Prop.CurrierLanguage.B
]

b_or_herbal = [
    locus
    for locus in vms.loci
    if locus.currier_language == Prop.CurrierLanguage.B
    or locus.illustration == Prop.IllustrationType.Herbal
]

print(
    f"B and Herbal: {len(b_and_herbal)}, B or Herbal: {len(b_or_herbal)}"
)  # B and Herbal: 2809, B or Herbal: 4071
print(
    f"Names of all b+herbal pages: {set([loc.page_name for loc in b_and_herbal])}"
)  # Get unique page names


# Create new Manuscript objects with list of Locus
voynich_b = IVTFFManuscript(
    loci=[loc for loc in vms.loci if loc.currier_language == Prop.CurrierLanguage.B]
)

# All of these methods are available for any Manuscript object
text, lines, words = voynich_b.to_text(), voynich_b.to_lines(), voynich_b.to_words()


# Locus has methods .is_label(), .is_paragraph(), and .is_below_prev() (all returning booleans)
# to easily filter by commonly grouped categories
labels = [loc for loc in vms.loci if loc.is_label()]  # Labels only


# Complex filtering operation:
# Get all loci that are Currier Lang A and on pages with Herbal illustrations,
# but exclude any of them in Davis hands H2 or H3,
# and exclude any below a certain line length in characters
include = [Prop.CurrierLanguage.A, Prop.IllustrationType.Herbal]
exclude = [Prop.DavisHand.H2, Prop.DavisHand.H3]
min_length = 20

# Calling VMS.get() ensures you always get the full unmodified list of loci
# Locus objects have .props() that returns a list of all their LocusProps
match_loci = []
for locus in VMS.get().loci:
    # Locus has all props we want to include
    has_all_include = all(inc_prop in locus.props() for inc_prop in include)
    # Or any of the ones we want to exclude
    has_any_exclude = any(ex_prop in locus.props() for ex_prop in exclude)
    long_enough = len(locus.text) >= min_length
    if has_all_include and not has_any_exclude and long_enough:
        match_loci.append(locus)

text = IVTFFManuscript(loci=match_loci).to_text()


# The IVTFF string code for a given property can be turned into the property itself:
prop = Prop.CurrierLanguage("B")
print(prop == Prop.CurrierLanguage.B)  # True

# However, note that for convenience, for many properties the codes are not the same as the property name
prop2 = Prop.Type("L0")
print(prop2 == Prop.Type.NotDrawingAssociated)  # True

# Note also that Locus objects have other information that isn't part of the special property system:
loc = vms.loci[0]
print(loc.page_name)  # f1r
print(loc.locus_in_page_num)  # 1
print(loc.id_str)  # f1r.1
print(loc.text)  # fachys.ykal.ar ...

# Complete list of Locus properties:

# At page level:

# quire_num: int
# page_in_quire_num: int
# folio_in_quire_num: int | None
# bifolio_in_quire_num: int
# illustration: LocusProp.IllustrationType
# currier_language: LocusProp.CurrierLanguage | None
# davis_hand: LocusProp.DavisHand
# currier_hand: LocusProp.CurrierHand | None
# extraneous_writing: LocusProp.ExtraneousWriting | None
# page_name: str

# At locus level:

# id_str: str
# locus_in_page_num: int
# location: LocusProp.Location
# type: LocusProp.Type
# text: str
