from pykeedy.crypt import encrypt, greshko_decrypt
import numpy as np
from pykeedy.test import test_reconstruction

lorem = """this is a test of hov english converts i hope i vill be able to read it"""
encod = encrypt(lorem, prngseed=np.random.randint(0, 2**32))
dec = greshko_decrypt(encod)
print(encod)
print(dec)

test_reconstruction(lorem, n=100)