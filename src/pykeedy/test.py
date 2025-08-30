from pykeedy.crypt import greshko_decrypt, encrypt, preprocess
from pykeedy.utils import load_text, shannon, conditional
from pykeedy.analysis import get_processed_vms
import numpy as np

def test_reconstruction(text: str, n: int = 1000) -> float:
    
    def levenshtein(a, b):
        if len(a) < len(b):
            return levenshtein(b, a)
        if len(b) == 0:
            return len(a)
        
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a):
            curr = [i + 1]
            for j, cb in enumerate(b):
                curr.append(min(prev[j + 1] + 1,      # deletion
                            curr[j] + 1,           # insertion  
                            prev[j] + (ca != cb))) # substitution
            prev = curr
        return prev[-1] 
    
    avg = 0
    pre = preprocess(text)
    for i in range(n):
        decoded = greshko_decrypt(encrypt(text, prngseed=np.random.randint(0, 2**32)))
        correct = len(pre) - levenshtein(decoded, pre)
        # print(decoded)
        # print(pre)
        # print(correct)
        # print(len(pre))
        avg += correct/len(pre)
    
    rec = avg / n
    print(f"Reconstruction accuracy: {rec*100:.2f}% over {n} trials of text length {len(pre)}")
    return rec

inferno = load_text("inferno").replace(' ', '')
vms = get_processed_vms().replace('.', '')
for text in (inferno, vms):
    print(shannon(text))
    print(conditional(text))