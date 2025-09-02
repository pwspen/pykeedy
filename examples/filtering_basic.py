from pykeedy import VMS, LocusProp as Prop

Prop.print_props()
# You see and select filterable properties through LocusProp (imported here as Prop)
# They are printed like
# Type:
#   Val1
#   Val2

# Only the pages and loci (aka lines) that match ALL the given properties will be returned (use as many properties as needed)
# All the same to_text, to_lines, to_words methods are available on filtered results
# Notice property syntax is Prop.Type.Val1
voynich_b = VMS.filter(props=[Prop.CurrierLanguage.B]).to_text()

b_herbal = VMS.filter([Prop.CurrierLanguage.B,
                       Prop.IllustrationType.Herbal]).to_lines()

b_herbal_nymphs = VMS.filter([Prop.CurrierLanguage.B,
                              Prop.IllustrationType.Herbal,
                              Prop.Type.BiologicalNymphLabel]).to_words()

print(b_herbal_nymphs) # [] - there are no voynich b herbal nymph labels (see warning also)

# If you need more advanced filtering operations see example filtering_custom.py
