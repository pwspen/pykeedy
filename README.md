[Voynich Unicode](https://www.kreativekorp.com/software/fonts/voynich/)

[Voynich Forum](https://www.voynich.ninja/)

[Best all-around source of Voynich information](https://www.voynich.nu/) (by Rene Zandbergen)
- All around great. However, it's somewhat of a spiderweb and has outdated information in parts, overwritten elsewhere. Software is also not user friendly.
- [Voynich transliteration](https://www.voynich.nu/transcr.html)
- [Page by page overview](http://voynich.nu/q01/index.html)

[Most detailed Voynich scan](https://collections.library.yale.edu/catalog/2002046)
- [Multispectral imaging](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/) [(direct link)](https://drive.google.com/drive/folders/1mNQGKQDSCR4M_c2M2JrsU5soghvYwMig)

[Naibbe cipher paper](https://www.dropbox.com/scl/fo/2b39zi1f77tr9mc9p80rt/ADwDDHsLNG7WtT6O0sbN5_4?download=true&e=4&from_auth=login&preview=20250724+Naibbe+Cipher+Paper+Latest+Version.pdf&rlkey=5ap828aun23thr9pvznguzgor&st=88np74hd&dl=0)

[IVTFF format explanation](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)
- Page header (pg 20):
    - Q: Quire number, 1->20 (A->T) excluding P/16 and R/18
    - P: Page within quire, 1->24 (A->X)
    - F: Folio within quire, a-f, u-z
    - B: Bifolio within quire, 1-6
    - I: Illustration type on page
        - A: Astronomical
        - B: Biological
        - C: Cosmological
        - H: Herbal
        - P: Pharmaceutical
        - S: Marginal stars only
        - T: Text only
        - Z: Zodiac
    - L: Currier language (A, B)
    - H: Fagin Davis scribe hand (1-5 + @)
    - C: Currier scribe hand (1-5 + X + Z)
    - X: Has extraneous writing
        - C: Color annotation
        - M: Month name
        - S: Sequence of characters or numbers

- Locus identifiers (start of each line)
    - < page . num , code >
    - page: page name matching most recent page header
    - num: sequence number within page
    - code: 3 character code consisting of 1-char 'locator' and 2-char 'locus type'
        - locator & locus type values defined in pdf page 21

- Functions to easily calculate, at either letter or word level:
    - n-gram frequency rank (most common letter, word, letter pair, word pair...)
    - n-gram co-occurence (aka, pair attraction for n=2)
    - position distribution in line, page, and manuscript
    - entropy
        - single (Shannon), pair, conditional
    - Plus in-word position for letter, and word type + token length distributions
- Batteries included, comes with:
    - Easily-loadable VMS transliteration (basic Eva or Cuva)
    - Filtering by every available property (Currier language, illustration type, locus type, etc)
    - Handful of comparison manuscripts in European languages + easily load and chuck em all into the same analysis
    - Naibbe encoder supporting arbitrary encoding tables + decoder implementing algorithm from paper
    - Plotter functions for common data types (see examples)

- Glyph
    - [x] Glyph frequency rank
    - [x] Glyph pair frequency rank
    - [x] Glyph pair attraction (matrix)
    - [ ] Glyph position in vord
    - [ ] Glyph position in line (horiz)
    - [ ] Glyph position in paragraph (vert)
    - [ ] Glyph position in manuscript
- Vord
    - [x] Vord token frequency rank
    - [x] Vord token pair frequency rank
    - [x] Vord token pair attraction (matrix)
    - [ ] Vord token position in line (horiz)
    - [ ] Vord token position in paragraph (vert)
    - [ ] Vord token position in manuscript
    - [ ] Vord & vord token length distribution
- Entropy
    - [x] Glyph entropy
    - [x] Glyph pair entropy
    - [x] Conditional entropy
    - [x] Vord entropy
    - [x] Vord pair entropy
    - [x] Conditional vord entropy
- [ ] Filters by every property available in the transliteration
- [ ] Comparison plaintexts
    - Focus on European, especially Latin, Italian, German, but wide ranging
- [x] Naibbe encrypt & decrypt with arbitrary table (Gresko is default)
- Advanced
    - [ ] Automated topic analysis
    - [ ] Levenshtein & Hamming distance network generation
    - [ ] Measure of vord clustering
    - [ ] Self-citation algorithm

- [ ] More options for dealing with spaces in entropy, freq, cooccurence analysis
- [ ] Cuva alphabet support (conversion table: http://www.voynich.nu/software/bitrans/Eva-Cuva.bit)
- [ ] STA alphabet support (later)
- [ ] Glyph and vord pair attraction symmetry scalar
- [ ] Support for recognizing single glyphs in non-basic EVA