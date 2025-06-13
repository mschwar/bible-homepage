#!/usr/bin/env python3
"""
generate_bible_verses.py
------------------------
Create data/quotes_bible.json from Project Gutenberg's pg10.txt
(King James Version). Verses > 75 words are skipped.

Key features
* Re-assembles verses that span multiple physical lines
* Skips Testament divider headings
* Generates canonical "Book C:V" source strings (e.g., John 3:16)
"""
import json, re, ssl
from pathlib import Path
from urllib.request import urlopen, URLError

# ---------- CONFIG --------------------------------------------------------
URL        = "https://www.gutenberg.org/cache/epub/10/pg10.txt"
MAX_WORDS  = 75
AUTHOR     = "King James Version"
TRADITION  = "Christianity/Judaism"
LOCAL_RAW  = Path(__file__).with_name("pg10.txt")     # optional offline file
# --------------------------------------------------------------------------

# ---------- PATHS ---------------------------------------------------------
ROOT      = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "quotes_bible.json"
DATA_FILE.parent.mkdir(exist_ok=True)
# --------------------------------------------------------------------------

BOOK_DIVIDERS = {
    "The Old Testament of the King James Version of the Bible",
    "The New Testament of the King James Version of the Bible",
}

BOOK_RE   = re.compile(r"^\s*(?:(?:The\s+)?[A-Z][A-Za-z\s]+?)\s*$")
VERSE_RE  = re.compile(r"^\s*(\d+):(\d+)\s+(.+?)\s*$")

def canonical_book(name: str) -> str:
    """Strip verbose prefixes -> 'Genesis', 'John', '1 Peter', etc."""
    if ':' in name:
        # "The First Book of Moses: Called Genesis" → "Genesis"
        name = name.split(':')[-1]
    name = name.replace("The Book of ", "")
    name = name.replace("The Epistle of ", "")
    name = name.replace("The Gospel According to ", "")
    name = name.replace("Called ", "")
    return " ".join(name.strip().split())

def fetch_pg10() -> str:
    if LOCAL_RAW.exists():
        return LOCAL_RAW.read_text(encoding="utf-8", errors="ignore")

    ctx = None
    try:                                # secure attempt
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl._create_unverified_context()

    try:
        with urlopen(URL, context=ctx) as r:
            return r.read().decode("utf-8", errors="ignore")
    except URLError as e:
        raise SystemExit(f"Download failed: {e.reason}")

def strip_header(txt: str) -> str:
    s, e = txt.find("*** START OF"), txt.find("*** END OF")
    return txt[s:e] if s != -1 < e else txt

# --------------------------------------------------------------------------
def parse_verses(raw: str):
    """Yield tuples (book, chapter:verse, text)."""
    book_long = None
    verse_text = []
    chap_verse = None

    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1; continue

        # Divider headings? skip.
        if line.strip() in BOOK_DIVIDERS:
            i += 1; continue

        # Book heading?
        if BOOK_RE.match(line) and not ':' in line.strip() and not VERSE_RE.match(lines[i+1].strip()):
            book_long = canonical_book(line.strip())
            i += 1; continue

        # Verse start?
        m = VERSE_RE.match(line)
        if m and book_long:
            # flush previous pending verse
            if verse_text and chap_verse:
                yield book_long, chap_verse, " ".join(verse_text).strip()
            chap_verse = f"{m.group(1)}:{m.group(2)}"
            verse_text = [m.group(3)]
            i += 1
            # collect continuation lines
            while i < len(lines):
                nxt = lines[i].rstrip()
                if not nxt or VERSE_RE.match(nxt) or BOOK_RE.match(nxt):
                    break
                verse_text.append(nxt.strip())
                i += 1
            continue

        i += 1

    # emit last verse
    if verse_text and chap_verse:
        yield book_long, chap_verse, " ".join(verse_text).strip()

# --------------------------------------------------------------------------
def build_records():
    raw = strip_header(fetch_pg10())
    for book, ref, text in parse_verses(raw):
        if len(text.split()) <= MAX_WORDS:
            yield {
                "text": text,
                "source": f"{book} {ref}",
                "author": AUTHOR,
                "tradition": TRADITION,
                "book": book,
                "reference": ref
            }

def main():
    recs = list(build_records())
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(recs, f, ensure_ascii=False, indent=2)
    print(f"✅  {len(recs):,} verses saved → {DATA_FILE.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
