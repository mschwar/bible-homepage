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

BOOK_RE   = re.compile(r"^\s*(?:The\s+First|The\s+Second|The\s+Third)?\s*(?:[A-Z][A-Za-z\s]+?)\s*$")
VERSE_RE  = re.compile(r"^\s*(\d+):(\d+)\s+(.+?)\s*$")

def canonical_book(name: str) -> str:
    """Strip verbose prefixes -> 'Genesis', 'John', '1 Peter', etc."""
    if ':' in name:
        name = name.split(':')[-1]
    name = name.replace("The Book of ", "")
    name = name.replace("The Epistle of Paul the Apostle to the ", "")
    name = name.replace("The General Epistle of ", "")
    name = name.replace("The Epistle of ", "")
    name = name.replace("The Gospel According to ", "")
    name = name.replace("Called ", "")
    return " ".join(name.strip().split())

def fetch_pg10() -> str:
    if LOCAL_RAW.exists():
        print(f"Using local cache file: {LOCAL_RAW}")
        return LOCAL_RAW.read_text(encoding="utf-8", errors="ignore")

    print(f"Fetching KJV text from {URL}...")
    ctx = None
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl._create_unverified_context()

    try:
        with urlopen(URL, context=ctx) as r:
            content = r.read().decode("utf-8", errors="ignore")
            # Cache it locally for next time
            LOCAL_RAW.write_text(content, encoding="utf-8")
            return content
    except URLError as e:
        raise SystemExit(f"Download failed: {e.reason}")

def strip_gutenberg_header_footer(txt: str) -> str:
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE KING JAMES BIBLE ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES BIBLE ***"
    s_idx = txt.find(start_marker)
    e_idx = txt.find(end_marker)
    if s_idx != -1:
        txt = txt[s_idx + len(start_marker):]
    if e_idx != -1:
        txt = txt[:e_idx]
    return txt

def parse_verses(raw: str):
    book_long = None
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line in BOOK_DIVIDERS:
            continue

        m = VERSE_RE.match(line)
        if m and book_long:
            chap_verse = f"{m.group(1)}:{m.group(2)}"
            verse_text = [m.group(3).strip()]

            # Look ahead for continuation lines
            while i < len(lines) and lines[i].strip() and not VERSE_RE.match(lines[i]) and not BOOK_RE.match(lines[i]):
                verse_text.append(lines[i].strip())
                i += 1

            yield book_long, chap_verse, " ".join(verse_text)
        elif BOOK_RE.match(line):
             # Check if the next line is a verse to avoid misinterpreting text as a book title
            if i < len(lines) and VERSE_RE.match(lines[i]):
                book_long = canonical_book(line)

def build_records():
    raw = strip_gutenberg_header_footer(fetch_pg10())
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
    print(f"✅  {len(recs):,} verses (max {MAX_WORDS} words) saved to {DATA_FILE.relative_to(ROOT)}")

if __name__ == "__main__":
    main()