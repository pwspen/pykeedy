from pykeedy.crypt import naibbe_encrypt, greshko_decrypt
from pykeedy.naibbe import ConstructNaibbeEncoding

# It's very easy to make your own encoding tables:
simple_encoding = ConstructNaibbeEncoding(
    ngram_slot_tables=[  # Letters can map to any string (only letters allowed as keys)
        {"a": ["x", "y"], "b": ["j", "la"], "c": ["loong", "c"]}
    ],
    table_odds=[
        3,
        1,
    ],  # For each letter, 3/4 chance of using first table, 1/4 chance of using second table
    ngram_odds=[1],
)
# (see example naibbe_advanced.py for more information)

plain = "abc 123 xyz"  # Only "abc" will be encoded (see warning about characters removed from input)
encoded = naibbe_encrypt(plain, encoding=simple_encoding)  # Supply encoding as argument
print("\nEncoded:\n")
print(encoded)  # -> x j c

# Doesn't work (see error) because decoding process is specific to the default encoding tables
decoded = greshko_decrypt(encoded, encoding=simple_encoding)
