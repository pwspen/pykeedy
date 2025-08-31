from pykeedy.crypt import naibbe_encrypt, greshko_decrypt

plain = "this is a test of how the naibbe cipher encodes plaintext"

# Some of the characters in the above are not in the encoding alphabet and are removed (see printed warning).
# (The encoding alphabet is classical latin, aka, english minus j, k, w)
# The encoding process also destroys spaces, so the eventual decoding is just one long string.
# The process uses psuedorandom numbers, so a seed is set for reproducibility.
# If no seed is supplied, a seed of 42 is used. If you want true randomness
# (useful for generating a bunch of possible ciphertexts), setting prngseed=None uses a random large number as the seed.
encoded = naibbe_encrypt(plain, prngseed=999)
print('\nEncoded:\n')
print(encoded) # -> resy sheeed shey oto qotody ...

# Decrypting is deterministic, but uses properties of the encoding, so this function is tied to the default
# encoding table (thus the "greshko" in the name), unlike the encoding process.
# Also, it is not successful on every letter - some it gets wrong and some it can't find any match -> outputs '?'.
# (this could be improved but it purposefully uses the exact implementation from the paper)
# Decoding can add or remove characters by guessing wrong, so the output may be a different length than the (spaces-removed) input.
# On average for long texts, reconstruction rate is about 95% (see test_reconstruction function)
decoded = greshko_decrypt(encoded)
print('\nDecoded:\n')
print(decoded)