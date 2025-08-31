import importlib.resources as resources
from functools import lru_cache
import re

@lru_cache(maxsize=1)
def get_vms(basic_ver: bool = True) -> str:
    translit_dir = resources.files("pykeedy.data.transliterations")

    basic = translit_dir / "RF1b-er.txt"
    extended = translit_dir / "RF1b-e.txt"

    path = basic if basic_ver else extended
    with path.open("r", encoding="utf-8") as f:
        return f.read()
    
def process_ivtt(text: str, verbose: bool = True, save_to_fpath: str | None = None) -> str:
    # match based line ops: skip, select
    # group based line op: remove
    skip = [r'<!.*?>', r'#'] # Skip page identifiers and comments
    sub = [(r'(<f.*?>)', ''), (r'(<@.*?>)', ''), (r'(<->)', '.'), (r'\.', ' ')] # Delete locus identifier, delete text tags, replace gaps with periods (spaces), replace periods with spaces
    ops = [lambda line: line.strip(), lambda line: '' if len(line) < 10 else line]

    lines = text.splitlines()

    def avglen():
        return sum(len(line) for line in lines) / len(lines)

    info = []

    def report(s: str) -> None:
        info.append(f"After {s}: {len(lines)}, avg len {avglen():.1f}")

    report("start")
    for pattern in skip:
        results = []
        for line in lines:
            if re.search(pattern, line):
                continue
            results.append(line)
        lines = results
        report(f"skip '{pattern}'")

    for pattern, repl in sub:
        results = []
        for line in lines:
            newline = re.sub(pattern, repl, line)
            if newline:
                results.append(newline)
        lines = results
        report(f"sub '{pattern}' -> '{repl}'")

    for i, op in enumerate(ops):
        results = []
        for line in lines:
            newline = op(line)
            if newline:
                results.append(newline)
        lines = results
        report(f"op {i}")
    text = '\n'.join(lines)
    if verbose:
        print(text)
        print('\n'.join(info))
    if save_to_fpath:
        with open(save_to_fpath, 'w', encoding='utf-8') as f:
            f.write(text)
    return text

@lru_cache(maxsize=1)
def get_processed_vms(basic_ver: bool = True) -> str:
    return process_ivtt(get_vms(basic_ver=basic_ver), verbose=False)

