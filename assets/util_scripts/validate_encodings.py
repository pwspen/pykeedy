import csv
from pykeedy.naibbe import NaibbeEncoding

with open(
    "../Downloads/Python versions of the Naibbe cipher and Voynichesque/references/naibbe_tables.csv",
    "r",
) as f:
    from_csv = {row[0]: row[1] for row in csv.reader(f) if len(row) >= 2}

letters = set([name[-1] for name in from_csv.keys()])
letters = sorted(list(letters))

ngram_slot_tables: list[dict[str, list[str]]]

slotnames = {0: "unigram", 1: "prefix", 2: "suffix"}
tables: list[dict[str, list[str]]] = [{}, {}, {}]
tabnames = {0: "alpha", 1: "beta1", 2: "beta2", 3: "beta3", 4: "gamma1", 5: "gamma2"}

mismatches = 0
for i, slotname in slotnames.items():
    for letter in letters:
        tables[i][letter] = []
        for j, tabname in tabnames.items():
            entryname = f"{slotname}_{tabname}_{letter}"
            tables[i][letter].append(from_csv[entryname])
NaibbeEncoding(
    name="test",
    ngram_slot_tables=tables,
    table_odds=[5, 2, 2, 2, 1, 1],
    ngram_odds=[1, 1],
).save()
