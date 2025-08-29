from pydantic import BaseModel, model_validator, computed_field
import numpy as np
import re

unigram = {
    "a": ["ol", "or", "qol", "chdy", "chol", "cheol"],
    "b": ["qokchdy", "okchdy", "otchdy", "sheckhy", "qotchdy", "olkchdy"],
    "c": ["chey", "okedy", "lkaiin", "shckhy", "sar", "lchey"],
    "d": ["cheey", "cheedy", "lkain", "chor", "chckhey", "olkedy"],
    "e": ["chedy", "ar", "dar", "dar", "chckhy", "lchedy"],
    "f": ["qokchey", "okchey", "otchey", "shal", "qotchey", "olkchey"],
    "g": ["qokchy", "okchy", "otchy", "shar", "qotchy", "olkchy"],
    "h": ["qokchedy", "okchedy", "otchedy", "shy", "qotchedy", "olkchedy"],
    "i": ["shedy", "qokedy", "shey", "otedy", "raiin", "qotedy"],
    "l": ["qokal", "okal", "otal", "saiin", "qotal", "olkal"],
    "m": ["qokar", "okar", "otar", "sain", "qotar", "olkar"],
    "n": ["daiin", "dal", "dain", "y", "dair", "dam"],
    "o": ["aiin", "al", "ain", "dy", "air", "am"],
    "p": ["qoky", "oky", "oty", "sheody", "qoty", "olky"],
    "q": ["qokol", "okol", "otol", "shody", "qotol", "olkol"],
    "r": ["qokeedy", "okeedy", "oteedy", "sheol", "qoteedy", "olkeedy"],
    "s": ["qokeey", "okeey", "oteey", "shol", "qoteey", "olkeey"],
    "t": ["qokaiin", "okaiin", "otaiin", "sheey", "qotaiin", "olkaiin"],
    "u": ["qokain", "okain", "otain", "sheedy", "qotain", "olkain"],
    "v": ["qokey", "okey", "otey", "shor", "qotey", "olkey"],
    "x": ["qokor", "okor", "otor", "shaiin", "qotor", "olkor"],
    "y": ["qokdy", "okdy", "otdy", "shain", "qotdy", "olkdy"],
    "z": ["qokeeedy", "okeeedy", "oteeedy", "sheeey", "qoteeedy", "olkeeedy"]
}

prefix = {
    "a": ["k", "yt", "olch", "tch", "op", "sor"],
    "b": ["qockh", "qocth", "cph", "ofch", "es", "x"],
    "c": ["qo", "dsh", "sch", "qolk", "q", "olt"],
    "d": ["dch", "ody", "aiir", "dar", "daly", "aly"],
    "e": ["ch", "yk", "opch", "lch", "kch", "chcth"],
    "f": ["ary", "dair", "da", "om", "f", "dk"],
    "g": ["oiin", "ols", "ssh", "dary", "orch", "opsh"],
    "h": ["dor", "qoch", "os", "qokch", "ockh", "soiin"],
    "i": ["sh", "ok", "ol", "ych", "okch", "tsh"],
    "l": ["or", "chckh", "s", "al", "qotch", "dyk"],
    "m": ["lsh", "dol", "p", "otch", "y", "ls"],
    "n": ["t", "od", "ar", "sol", "och", "otsh"],
    "o": ["qok", "pch", "dal", "ksh", "ykch", "lt"],
    "p": ["cth", "sair", "fch", "qor", "qolch", "lpch"],
    "q": ["ypch", "of", "shckh", "psh", "sar", "dyt"],
    "r": ["lk", "olsh", "sal", "ckh", "ytch", "octh"],
    "s": ["ot", "qopch", "oly", "shcth", "dl", "d"],
    "t": ["r", "qot", "olk", "ysh", "qop", "qol"],
    "u": ["l", "o", "lkch", "rch", "qoksh", "qofch"],
    "v": ["aiiin", "solk", "oksh", "chcph", "osh", "ly"],
    "x": ["solch", "qolsh", "rsh", "air", "ory", "lfch"],
    "y": ["qotsh", "sok", "olpch", "daiir", "sk", "ail"],
    "z": ["oiiin", "do", "chcfh", "sy", "ry", "so"]
}

suffix = {
    "a": ["dy", "al", "o", "ed", "edain", "od"],
    "b": ["dor", "oiiin", "g", "eees", "sy", "eda"],
    "c": ["or", "edal", "e", "as", "edor", "ory"],
    "d": ["daiin", "eear", "edair", "oy", "eom", "eaiin"],
    "e": ["edy", "ain", "ody", "eo", "ees", "dar"],
    "f": ["daly", "do", "als", "eeeos", "ealy", "oin"],
    "g": ["a", "aiis", "eeeo", "eesy", "edaiiin", "eedo"],
    "h": ["dol", "ols", "eoy", "esy", "sd", "eeaiin"],
    "i": ["aiin", "eedy", "am", "eeey", "os", "dain"],
    "l": ["eor", "m", "d", "eos", "ee", "daiiin"],
    "m": ["edaiin", "aly", "eeol", "dam", "edam", "eel"],
    "n": ["ar", "edar", "ear", "dal", "dair", "eeal"],
    "o": ["y", "eol", "oiin", "aiiin", "edol", "eedal"],
    "p": ["es", "eedaiin", "eeos", "er", "eedain", "edo"],
    "q": ["aiir", "sdy", "eeod", "iin", "eeoy", "ery"],
    "r": ["ey", "eed", "s", "ary", "eedar", "aim"],
    "s": ["eey", "eeody", "eeor", "oly", "eeed", "eam"],
    "t": ["eody", "air", "l", "eal", "eod", "ail"],
    "u": ["ol", "eeo", "r", "eeedy", "an", "eoly"],
    "v": ["om", "eain", "ais", "eeeody", "eer", "eeam"],
    "x": ["saiin", "sairy", "iiin", "eols", "eedam", "yr"],
    "y": ["ch", "osy", "yl", "dl", "ry", "alsy"],
    "z": ["ady", "ok", "eds", "iir", "in", "eory"]
}

table_odds = [5, 2, 2, 2, 1, 1]

ngram_odds = [1, 1]

class NaibbeEncoding(BaseModel):
    ngram_slot_tables: list[dict[str, list[str]]] # [unigram, bigram_prefix, bigram_suffix, ...] - order extremely important for lists!
    table_odds: list[float] | list[list[float]] # e.g. [5, 2, 2, 2, 1, 1] - order corresponding to lists in ngram_slot_tables
    ngram_odds: list[float] # [1, 1] for equal odds unigram + bigram - order is ascending (first position is unigram, second bigram)
    
    @model_validator(mode='after')
    def check_encoding(self) -> "NaibbeEncoding":
        num_ngrams = len(self.ngram_odds)
        num_tables = num_ngrams * (num_ngrams + 1) // 2
        # one slot per table
        # unigram only -> 1 table
        # unigram + bigram -> 3 tables (Greshko encoding)
        # unigram + bigram + trigram -> 6 tables

        if len(self.ngram_slot_tables) != num_tables:
            raise ValueError("Number of possible ngram lengths and number of tables do not match")

        # Limit to trigram (most of code should work for higher, limit mostly for more clarity in certain areas)
        if len(self.ngram_odds) > 3:
            raise ValueError("Only up to trigrams are supported")

        alphabet = {}
        num_encodings = 0
        for i, tab in enumerate(self.ngram_slot_tables):
            if i == 0:
                alphabet = set(tab.keys())
            else:
                if set(tab.keys()) != alphabet:
                    raise ValueError("All ngram_tables must use the same plaintext alphabet")
                
            lengths = set(len(v) for v in tab.values())
            if len(lengths) != 1:
                raise ValueError(f"Each encoding table must have same number of encodings per character (problem with table: {self.tabname(i)})")
            
            if i == 0:
                num_encodings = len(list(tab.values())[0])
                if isinstance(self.table_odds[0], float): # single common odds list for all slots
                    if len(self.table_odds) != num_encodings:
                        raise ValueError("If table_odds is a single list, it must have the same length as the number of encodings per character")
                elif isinstance(self.table_odds[0], list): # leaving the door open for slots having different numbers of encodings in future (len would be checked)
                    if len(self.table_odds[i]) != len(self.ngram_slot_tables): # type: ignore
                        raise ValueError("If table_odds is a list of lists, it must have the same length as ngram_tables")
            else:
                if len(list(tab.values())[0]) != num_encodings:
                    raise ValueError("All tables must have the same number of encodings per character")
        
        return self

    @computed_field
    def alphabet(self) -> str:
        return ''.join(sorted(self.ngram_slot_tables[0].keys()))

    @computed_field
    def common_table_odds(self) -> bool:
        return isinstance(self.table_odds[0], float)

    @computed_field
    def get_slot_decrypt_tables(self) -> list[dict[str, str]]:
        # return: [slot1decode, slot2decode, slot3decode]
        # slot1decode: {"qokchedy": "h", "okchedy": "h", ...}
        return [{enc: char for char, encs in slot_dict.items() for enc in encs} for slot_dict in self.ngram_slot_tables]

    @computed_field
    def get_slot_lists(self) -> list[list[str]]:
        # return: [slot1list, slot2list, slot3list]
        # slot1list: ["qokchedy", "okchedy", ...]
        return [list(dec.keys()) for dec in self.get_slot_decrypt_tables] # type: ignore
    

    def tabname(self, tab: int) -> str:
        if tab == 0:
            return "unigram"
        elif tab in [1, 2]:
            return f"bigram {'prefix' if tab == 1 else 'suffix'}"
        elif tab in [3, 4, 5]:
            return f"trigram {'prefix' if tab == 3 else 'middle' if tab == 4 else 'suffix'}"
        else:
            raise ValueError("Only up to trigrams are supported")

    def ambiguousity(self):
        # Debug for now, later return a value for exactly how ambiguous encoding is.

        # An encoding is ambiguous if and only if:
        # -For any slot (unigram, bigram prefix, bigram suffix) there is a duplicate (among any character or table)
        # -An encoding from an earlier slot can be built from a combination of later ones
        
        def find_duplicates(lst):
            seen = set()
            duplicates = set()
            
            for item in lst:
                if item in seen:
                    duplicates.add(item)
                else:
                    seen.add(item)
            
            return list(duplicates)

        # Check first case
        for i, chartab in enumerate(self.ngram_slot_tables):
            # Encodings within the same slot and letter don't have to be unique to be unambiguous, so take their set 
            all_encs = [enc for encs in chartab.values() for enc in set(encs)]
            encset = set(all_encs)
            print(f"{self.tabname(i)}: {len(encset)} / {len(all_encs)} (unique/total)")
            # if len(encset) != len(all_encs):
            #     print(f"Duplicate encodings in {self.tabname(i)} table ({find_duplicates(all_encs)})")
            #     return True

        # Check second case
        if len(self.ngram_odds) == 2:
            unigram_encs = set(enc for encs in self.ngram_slot_tables[0].values() for enc in encs)
            bigram_prefix_encs = set(enc for encs in self.ngram_slot_tables[1].values() for enc in encs)
            bigram_suffix_encs = set(enc for encs in self.ngram_slot_tables[2].values() for enc in encs)

            bigrams = []

            for bpre in bigram_prefix_encs:
                for bsuf in bigram_suffix_encs:
                    bigrams.append(bpre + bsuf)
            bigram_set = set(bigrams)
            print(f"bigrams: {len(bigram_set)} / {len(bigrams)} (unique/total)")
            intersection = bigram_set.intersection(unigram_encs)
            if len(intersection) > 0:
                print(f"Unigram-bigram collision: {len(intersection)}")
                return True
            if len(bigram_set) != len(bigrams):
                print(f"Intersection within bigrams")
                return True
            return False

        elif len(self.ngram_odds) == 3:
            raise NotImplementedError

        else:
            raise ValueError("Only up to trigram supported")

def preprocess(text: str) -> str:
    # preprocess text by deleting spaces and punctuation then lowercasing 
    text = re.sub(r'[ .,;:!?\'\"()\[\]{}\-_/\\@#$%^&*+=<>~`|]', '', text)
    text = text.lower()
    return text

def encrypt(text: str, encoding: NaibbeEncoding, prngseed: int = 42) -> str:
    """
    Encrypt text using some Naibbe encoding.
    Note that this is a general implementation for encodings with any number of characters, ngram lengths, probabilities, etc.
    A function for only unigram-bigram encodings would be simpler.
    """
    if not isinstance(encoding, NaibbeEncoding):
        raise ValueError("encoding must be an instance of NaibbeEncoding")
    text = preprocess(text)

    rng = np.random.default_rng(seed=prngseed)

    def odds_to_thresholds(odds: list[float]) -> np.ndarray:
        # process ordered odds lists to make it easy to select option (ngram length, or, table to use) from a randomly generated number
        # normalize sum of list to 1, then cumsum to get thresholds - last element should always be ~1,
        # which is discarded (rolled to first element then replaced with 0)
        # example: [1 1 1] -> [0 0.3333 0.6666]

        oddsarr = np.array(odds)
        thresharr = np.roll(np.cumsum(oddsarr/np.sum(oddsarr)), 1)
        thresharr[0] = 0.0
        return thresharr

    ngram_length_thresholds = odds_to_thresholds(encoding.ngram_odds)

    table_thresholds_array = None
    # make and copy single thresholds table if each has the same odds, otherwise do for each
    # copying means we just assume each table has its own odds instead of branching later
    if encoding.common_table_odds:
        table_thresholds = odds_to_thresholds(encoding.table_odds) # type: ignore
        table_thresholds_array = np.array([table_thresholds for _ in range(len(encoding.ngram_slot_tables))])
    else:
        table_thresholds_array = np.array([odds_to_thresholds(to) for to in encoding.table_odds]) # type: ignore

    def select_option(thresholds: np.ndarray) -> int:
            # using the precomputed threshold table, generate a random number, then see where it falls on the table (the largest index it is larger than)
            # to select how many characters to encode in a word or which table to use for a character
            rand = rng.random() # 0 -> 1
            return np.nonzero(thresholds < rand)[0][-1]

    i = 0
    encoded = ""
    while i < len(text)-1:
        gramsize = select_option(ngram_length_thresholds) + 1 # select ngram size
        start_table_idx = 0 if gramsize == 1 else 1 if gramsize == 2 else 3 # Only support up to trigrams (same as NaibbeEncoding)

        word = ""

        for j in range(gramsize):
            char = text[i + j]
            if char not in str(encoding.alphabet):
                raise ValueError(f"Character '{char}' at position {i+j} not in encoding alphabet")
            table = select_option(table_thresholds_array[start_table_idx + j])
            word += encoding.ngram_slot_tables[start_table_idx + j][char][table]
        i += gramsize
        encoded += word + " "

    return encoded.strip()

def greshko_decrypt(encoded: str, encoding: NaibbeEncoding) -> str:
    # IMPORTANT: If the encoding is ambiguous (Greshko encoding is), some information is lost in the encryption/decryption process. With this decoding algorithm and the current encoding algorithm reconstruction rate is 95%.

    # This uses the algorithm from the paper (Greshko 2025). It makes use of properties of the encoding tables so it will not work for other encodings!
    # Strategy is important because the encoding is not just a little ambiguous - 90% of unigrams are also valid bigrams.
    # Step 1: If word is a valid unigram, decode it as such (it is usually the far more likely option even if it's also a bigram)
    # Step 2: Use "breakpoint" strings: There are prefix- and suffix-unique strings. The rightmost one in a prefix, or leftmost in a suffix, defines the breakpoint, both affixes are then parsed (prefix and suffix tables are unique)
    # Step 3: Refer to a grammar slot table. Check each character against successive slots until there's a match, then decode the prefix as the longest valid string.

    # One can imagine algorithms that do various types of "greedy parsing" to find the likeliest decoding instead of using a hardcoded method and this is a future goal.
    # When doing this it will also be important to focus on the 15th-century-human-doability as the paper does.

    prefix_only_strs = ["ch", "sh", "cfh", "ckh", "cph", "cth", "f", "k", "p", "t", "x"]
    suffix_only_strs = ["a", "e", "g", "i", "m", "n"]

    t1_slots = [["q", "s", "d", "x"],
                ["o", "y"],
                ["d", "r"],
                ["t", "k", "p", "f"],
                ["ch", "sh"],
                ["cth", "ckh", "cph", "cfh"]]

    t2_slots = [["e", "ee", "eee", "g"],
                ["s", "d"],
                ["o", "a"],
                ["i", "ii", "iii"],
                ["d", "l", "r", "m", "n"],
                ["s"],
                ["y"]]

    slot_decrypt_tables: list[dict[str, str]] = encoding.get_slot_decrypt_tables # type: ignore

    slot_lists: list[list[str]] = encoding.get_slot_lists # type: ignore

    def common_prefix_length(s1: str, s2: str) -> int:
        # Finds length of common prefix between two strings
        # "Prefix" used here entirely unrelated to voynich grammar
        i = 0
        min_len = min(len(s1), len(s2))
        
        while i < min_len and s1[i] == s2[i]:
            i += 1
        
        return i

    def slot_hit(glyph: str, vord_remaining: str) -> bool:
        return common_prefix_length(glyph, vord_remaining) == len(glyph)

    def parse_from_breakpoint(vord: str, pt: int) -> str:
        pre = vord[:pt]
        suf = vord[pt:]
        return slot_decrypt_tables[1][pre] + slot_decrypt_tables[2][suf]

    vords = encoded.split(" ")
    decoded = ""
    for vord in vords:
        # Step 1 (see above comment)
        if vord in slot_lists[0]:
            decoded += slot_decrypt_tables[0][vord]
            continue

        # Step 2
        best = None
        for glyph in prefix_only_strs: # Get rightmost prefix glyph
            pos = vord.rfind(glyph)
            if pos != -1:
                if best is None or pos > best:
                    best = pos + len(glyph)
        for glyph in suffix_only_strs: # Get leftmost suffix glyph
            pos = vord.find(glyph)
            if pos != -1:
                if best is None or pos < best:
                    best = pos
        if best and best > 0:
            try:
                # Sometimes the process is just wrong because type 1 affixes can be suffixes and vice versa, 
                # so have to catch it and continue to step. words caught here tend to have no type 1 affix glyphs
                # example: daleor, lsdaiin, oldal, alaiin, aleedal, qodain...
                decoded += parse_from_breakpoint(vord, best)
                continue
            except KeyError:
                pass

        # Step 3
        def get_longest_affix(vord: str, slots: list[list[str]]) -> int:
            i = 0
            for slot_options in slots:
                best = 0
                for glyph in slot_options:
                    if slot_hit(glyph, vord[i:]):
                        best = len(glyph)
                i += best
            return i
        
        t1 = get_longest_affix(vord, t1_slots)
        t2 = get_longest_affix(vord, t2_slots)
        longest_idx = max(t1, t2)
        # print(f"{t1=} {t2=}")
        try:
            decoded += parse_from_breakpoint(vord, longest_idx)
        except:
            print(f"{vord}")
            decoded += "?"

        # Problem grams:
        # qol + o - grammar suggests qo + lo, lo is invalid (same for qolor)
        # o + ry / or + y - is also a valid t2 gram, so greedy parsing leaves no suffix
        # aiir + y - valid t2 gram

    return decoded


enc = NaibbeEncoding(
    ngram_slot_tables=[unigram, prefix, suffix],
    table_odds=table_odds,
    ngram_odds=ngram_odds
)

def test_reconstruction(text: str, encoding: NaibbeEncoding, n: int = 1000):
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
        decoded = greshko_decrypt(encrypt(text, encoding=encoding, prngseed=np.random.randint(0, 2**32)), encoding=encoding)
        correct = len(pre) - levenshtein(decoded, pre)
        # print(decoded)
        # print(pre)
        # print(correct)
        # print(len(pre))
        avg += correct/len(pre)
    print(avg/n)
    return avg / n

lorem = """this is a test of hov english converts i hope i vill be able to read it"""
encod = encrypt(lorem, encoding=enc, prngseed=np.random.randint(0, 2**32))
dec = greshko_decrypt(encod, encoding=enc)
print(encod)
print(dec)

test_reconstruction(lorem, enc, n=100)