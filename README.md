[Voynich Forum](https://www.voynich.ninja/)

[Most complete source of Voynich information](https://www.voynich.nu/) (by Rene Zandbergen)
- [Voynich transliteration](https://www.voynich.nu/transcr.html)
- [Page by page overview](http://voynich.nu/q01/index.html)
- Existing Voynich software by Rene
    - [bitrans](http://www.voynich.nu/software/bitrans/Bitrans_manual.pdf) - performs plaintext substitutions
    - [IVTT](http://voynich.nu/software/ivtt/IVTT_manual.pdf) - CLI for filtering and removing metadata from IVTFF files
    - You should not need either of these if you are using this library
[Most detailed Voynich scan](https://collections.library.yale.edu/catalog/2002046)
- [Scan browser](https://www.voynich.ninja/browser/default.cfm?v=1006075&r=1006082)
- [Multispectral imaging](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/) [(direct link)](https://drive.google.com/drive/folders/1mNQGKQDSCR4M_c2M2JrsU5soghvYwMig)

[Naibbe cipher paper](https://www.dropbox.com/scl/fo/2b39zi1f77tr9mc9p80rt/ADwDDHsLNG7WtT6O0sbN5_4?download=true&e=4&from_auth=login&preview=20250724+Naibbe+Cipher+Paper+Latest+Version.pdf&rlkey=5ap828aun23thr9pvznguzgor&st=88np74hd&dl=0)

[IVTFF format explanation](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

[Voynich Unicode](https://www.kreativekorp.com/software/fonts/voynich/)


- Functions to easily calculate, at either letter or word level:
    - n-gram frequency rank (most common letter, word, letter pair, word pair...)
    - n-gram co-occurence (aka, pair attraction for n=2)
    - position distribution in line, page, and manuscript
    - entropy
        - single (Shannon), pair, conditional
    - Plus in-word position for letter, and word type + token length distributions
- Batteries included! comes with:
    - Easily-loadable VMS transliteration (basic Eva or Cuva)
    - Filtering by every available property, at page and line levels (Currier language, illustration type, locus type, etc)
    - Handful of comparison manuscripts in European languages + easily load and chuck em all into the same analysis
    - Naibbe encoder supporting arbitrary encoding tables + decoder implementing algorithm from paper
    - Plotter functions for common data types / amalyses (see examples)

2 complementary goals:
1. Lower the barrier to entry for Voynich statistical analysis
    - There are some tools out there, but they're scattered, relatively basic, and far from user friendly, even for programmers. This library aims to be very capable while not sacrificing any usability.
2. Reproduce all the important statistical results in one place
    - There is a TON of analysis out there, but it's even more scattered, and a lot of it is just results with no reproduction available, which means it's very difficult to tweak and experiment with and build on.

Issues & PRs very welcome!

bits left:
- [x] filtering system
    - by page and line (different properties available)
- [ ] position functions
    - each unique gets a list that is filled with the position numbers, collapse to average for plot
    - absolute and fractional modes
    - get_words, get_lines, get_pages funcs
    - function to identify rank distributions by concentration (for those with entries n > m)
- [ ] couple more comparison manuscripts (german, latin)
- [x] cuva http://www.voynich.nu/software/bitrans/Eva-Cuva.bit
- [x] word length token + type distribution
- [ ] encoding scorer
    - basic: ambiguity, reconstruction
    - advanced: match to VMS properties, simplicity

- Advanced
    - [ ] Automated topic analysis
    - [ ] Clustering of similar words
        - Show that it's much more common in Voynich than plaintext
    - [ ] Levenshtein distance network generation
    - [ ] Reference self-citation algorithm

- [ ] More options for dealing with spaces and newlines in entropy, freq, cooccurence analysis
- [ ] STA alphabet support
- [ ] Glyph and vord pair attraction symmetry scalar
- [ ] Support for recognizing single glyphs in non-basic EVA
- [ ] Measure of encoding ambiguity - if you always pick the most likely option, how likely are you to be right?
- [ ] Voynich font alongside transliteration for plots
- [ ] basic testing sutie

Transliteration issues:
- Rosette page lacking folio number, inconsistent with other headers
- IVTFF source says Currier hands contains X & Z but it actually contains X & Y