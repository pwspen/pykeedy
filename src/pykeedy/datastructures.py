import re
from enum import Enum
from dataclasses import dataclass, fields
from typing import Callable, Sequence
import importlib.resources as resources
from functools import lru_cache

class LocusPropType:
    pass
class LocusProp:
    class Location(LocusPropType, Enum):
        UnrelatedToPrev = "@"
        BelowPrev = "+"
        BelowAndLeftOfPrev = "*"
        RightOfPrev = "="
        AlongArcFromPrev = "&"
        RightishFromPrev = "~"
        AboveAndRightOfPrev = "/"
        DoesNotExist = "!"

    class Type(LocusPropType, Enum):
        # P: Linear text in paragraphs
        ParagraphLeftJustified = "P0"
        ParagraphNotLeftJustified = "P1"
        ParagraphFreeFloating = "Pb"
        ParagraphCentered = "Pc"
        ParagraphRightJustified = "Pr"
        ParagraphRightJustifiedTitle = "Pt"

        # L: Short piece of text, a word, or a character that is anywhere on the page, mostly labels
        NotDrawingAssociated = "L0"
        AstronomicalLabel = "La"
        PharmaceuticalContainerLabel = "Lc"
        HerbalFragmentLabel = "Lf"
        BiologicalNymphLabel = "Ln"
        HerbalLargePlantLabel = "Lp"
        StarLabel = "Ls"
        BiologicalTubeLabel = "Lt"
        ExtraneousWriting = "Lx"
        ZodiacLabel = "Lz"

        # C: Text along circumference of circle
        CircumferentialClockwise = "Cc"
        CircumferentialCounterClockwise = "Ca"

        # R: Text along radius of circle
        RadialInwards = "Ri"
        RadialOutwards = "Ro"
    
    @classmethod
    def print_props(cls) -> None:
        for cls in [LocusProp.Location, LocusProp.Type]:
            print(f"LocusProp.{cls.__name__}:")
            for item in cls:
                print(f"  {item.name}")

class PagePropType:
    # A way to tell that something is a filterable property
    pass

class PageProp:
    class Illustration(PagePropType, Enum):
        Astronomical = "A"
        Biological = "B"
        Cosmological = "C"
        Herbal = "H"
        Pharmaceutical = "P"
        MarginalStarsOnly = "S"
        TextOnly = "T"
        Zodiac = "Z"
    
    class CurrierLanguage(PagePropType, Enum):
        A = "A"
        B = "B"
    
    class DavisHand(PagePropType, Enum):
        H1 = "1"
        H2 = "2"
        H3 = "3"
        H4 = "4"
        H5 = "5"
        At = "@"
    
    class CurrierHand(PagePropType, Enum):
        C1 = "1"
        C2 = "2"
        C3 = "3"
        C4 = "4"
        C5 = "5"
        X = "X"
        Y = "Y" # IVTFF format pdf and transliteration do not match - pdf claims X + Z, actual transliteration has X + Y
    
    class ExtraneousWriting(PagePropType, Enum):
        ColorAnnotation = "C"
        MonthName = "M"
        Other = "O"
        CharOrNumSequence = "S"
        Various = "V" # This is deprecated but still in the source for some reason.

    @classmethod
    def print_props(cls) -> None:
        for cls in [PageProp.Illustration, PageProp.CurrierLanguage, PageProp.DavisHand, PageProp.CurrierHand, PageProp.ExtraneousWriting]:
            print(f"PageProp.{cls.__name__}:")
            for item in cls:
                print(f"  {item.name}")

class VMSDataclass:
    @classmethod
    def print_fields(cls) -> None:
        print(f"{cls.__name__} fields:")
        for field in fields(cls): # type: ignore
            print(f"Name: {field.name}")

@dataclass
class Locus(VMSDataclass):
    page_name: str
    locus_in_page_num: int
    location: LocusProp.Location
    type: LocusProp.Type
    text: str
    
    @classmethod
    def from_line(cls, line: str) -> "Locus":
        # Expects line to be a single locus, with no page headers or comments as lines
        # Example line: "<f89v1.23,@Lf>    opol.olaiin" (no \n)
        # So we want to extract page name, locus number in page, location & type code (3 characters), and text.
        line = re.sub(r'<[!@%$].*?>', '', line) # Remove inline comments except interruption tags <[-~]>
        match = re.match(r'<([^.]+)\.([^,]+),([^>]+)>\s*([a-zA-Z?].*)', line)
        # Important parts of above line:

        if not match:
            raise ValueError(f"Line does not match expected locus format: {line}")
        page_name = match.group(1)
        locus_in_page_num = int(match.group(2))

        # Extract 3 character code. First character is location, next two are type.
        loctypecode = match.group(3)
        if len(loctypecode) != 3: # Must be 3 characters
            raise ValueError(f"Corrupted IVTFF file: Locus location & type code must be exactly 3 characters: {loctypecode}")
        locus_location = LocusProp.Location(loctypecode[0])
        locus_type = LocusProp.Type(loctypecode[1:])
        text = match.group(4).strip()
        return cls(page_name=page_name, locus_in_page_num=locus_in_page_num, location=locus_location, type=locus_type, text=text)

# Tries to convert strings of form 'letter' or 'numbers' to int.
def to_int(letter: str) -> int: # A -> 1, B -> 2 ...
    if len(letter) != 1:
        raise ValueError("str must be single character")
    try:
        return int(letter)
    except ValueError:
        if not letter.isalpha():
            raise ValueError("letter str must be alphabetic")
        return ord(letter.upper()) - ord("A") + 1

@dataclass
class Page(VMSDataclass):
    quire_num: int
    page_in_quire_num: int
    folio_in_quire_num: int | None
    bifolio_in_quire_num: int
    illustration: PageProp.Illustration
    currier_language: PageProp.CurrierLanguage | None
    davis_hand: PageProp.DavisHand
    currier_hand: PageProp.CurrierHand | None
    extraneous_writing: PageProp.ExtraneousWriting | None
    name: str
    loci: list[Locus]

    @classmethod
    def from_lines(cls, lines: list[str], name: str, header: str) -> "Page":
        # Expects each line to be one locus, with no page headers or comments as lines
        # Header example: "$Q=M $P=R $F=y $B=2 $I=B $L=B $H=2 $C=2"
        # Name example: "f85r1"
        pattern = r'\$([A-Z])=([A-Za-z0-9])'

        # This encodes the order and thing to be called for letter, we'll use it to build a tuple to pass into constructor.
        letters: dict[str, Callable] = {
            # Below 4: we will need to convert from string to int, rest of types are StrEnums so can pass string directly
            'Q': to_int,
            'P': to_int,
            'F': to_int,
            'B': to_int,
            'I': PageProp.Illustration,
            'L': PageProp.CurrierLanguage,
            'H': PageProp.DavisHand,
            'C': PageProp.CurrierHand,
            'X': PageProp.ExtraneousWriting
        }

        # Dict e.g. {'Q': 'M', 'P': 'R', ...}
        props_pairs = dict(re.findall(pattern, header))

        # For each possible property, get its value if it is present in this header, then pass it to that property's callable. if it isn't then use None.
        props = tuple(func(props_pairs[key]) if key in props_pairs else None
                      for key, func in letters.items())

        # This function is sensitive to the order of the above dict matching the order of constructor parameters. Maybe use type introspection?
        return cls(*props, name=name, loci=[Locus.from_line(line) for line in lines]) # type: ignore
    
@dataclass
class Manuscript(VMSDataclass):
    pages: list[Page]
    source_filename: str | None = None

    @classmethod
    @lru_cache(maxsize=1)
    def from_file(cls, text: str, fname: str) -> "Manuscript":
        # Expects text directly from IVTFF file.
        # Split by page and then create Page for each.

        # Delete all comment lines
        text = re.sub(r'#.*?\n', '', text)

        pages: list[Page] = []
        page_lines: list[str] = []

        # Going in reverse order ( [::-1] ) makes process a bit easier because we don't have to "look forward" for headings,
        # just keep piling up lines and when we do see a heading, ship it all off.
        for line in text.splitlines()[::-1]:
            # Does this line contain a page header?
            header_match = re.search(r'<! (.*?)>', line)
            if header_match:
                # Yep!
                name: str = re.match(r'<(f.*?)>', line).group(1) # type: ignore - name is guaranteed to exist alongside header for IVTFF
                header: str = header_match.group(1)
                if len(page_lines) and name and header:
                    # Process previous page, putting lines back in normal order
                    page = Page.from_lines(page_lines[::-1], name, header)
                    pages.append(page)
                    # Get rid of our used up lines
                    page_lines = []
            else:
                # No header in line
                page_lines.append(line)

        if len(page_lines):
            raise ValueError("File ended without final page header. Corrupted file?")
        
        return cls(source_filename=fname, pages=pages[::-1]) # Put pages back in normal order
    
    def to_text(self) -> str:
        text = to_text(self)
        # Default replacement options: remove text tags, replace things indicating gaps with spaces.
        for string, sub in [(r'(<[!@%$].*?>)', ''), (r'(<[-~]>)', '.')]:
            text = re.sub(string, sub, text)
        return text
    
    def to_lines(self) -> list[str]:
        return self.to_text().splitlines()
    
    def to_words(self) -> list[str]:
        words = []
        for line in self.to_lines():
            words.extend(line.split('.'))
        return words

VMSObject = Manuscript | Page | Locus
# We want to be able to easily take any combination and turn it all into text.
def to_text(source: VMSObject | list[VMSObject]) -> str:
    text = ""
    if isinstance(source, list):
        for item in source:
            text += to_text(item)
    else:
        if hasattr(source, "pages"):
            for page in source.pages: # type: ignore
                text += to_text(page)
        elif hasattr(source, "loci"):
            for locus in source.loci: # type: ignore
                text += to_text(locus)
        elif hasattr(source, "text"):
            text += source.text + "\n" # type: ignore
        else:
            raise TypeError("source must be Manuscript, Page, or Locus")
    return text

Filterable = PagePropType | LocusPropType
# Helper class to load from transliteration file and create Manuscript objects, returning it or its text/lines/words/filtered etc.
class VMS:
    @classmethod
    def filter(cls, props: Sequence[Filterable]) -> Manuscript:
        locus_filt_props = [prop for prop in props if issubclass(prop.__class__, LocusPropType)]
        page_filt_props = [prop for prop in props if issubclass(prop.__class__, PagePropType)]

        vms = cls.get()
        pages = []
        # Below are so we can warn user when either no pages or no loci matched filter
        locus_success = False
        for page in vms.pages:
            if all(fprop in page.__dict__.values() for fprop in page_filt_props) or not len(page_filt_props):
                pages.append(page)
                page_success = True
                orig_page_loci = page.loci
                page.loci = []
                for locus in orig_page_loci:
                    if all(fprop in locus.__dict__.values() for fprop in locus_filt_props):
                        page.loci.append(locus)
                        locus_success = True
        
        if not locus_success:
            print(f"Warning: No text loci matched the given filter properties, result is empty.")
            print(f"(page properties: {', '.join(list(f'PageProp.{p.__class__.__name__ + '.' + p.name}' for p in page_filt_props)) if page_filt_props else 'None'} )") # type: ignore
            print(f"(locus properties: {', '.join(list(f'LocusProp.{p.__class__.__name__ + '.' + p.name}' for p in locus_filt_props)) if locus_filt_props else 'None'} )") # type: ignore
            # Don't allow pages with no loci to be included in result
            pages = []
        return Manuscript(source_filename=vms.source_filename, pages=pages)
    
    @classmethod
    def to_words(cls) -> list[str]:
        return cls.get().to_words()

    @classmethod
    def to_lines(cls) -> list[str]:
        return cls.get().to_lines()

    @classmethod
    def to_text(cls) -> str:
        return cls.get().to_text()

    @classmethod
    def get(cls, basic_ver: bool = True) -> Manuscript:
        translit_dir = resources.files("pykeedy.data.transliterations")

        basic = translit_dir / "RF1b-er.txt"
        extended = translit_dir / "RF1b-e.txt"

        path = basic if basic_ver else extended
        with path.open("r", encoding="utf-8") as f:
            raw = f.read()

        vms = Manuscript.from_file(raw, path.name)
        return vms