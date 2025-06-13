#!/usr/bin/env python3
"""
generate_bible_verses.py
------------------------
Download / parse Project Gutenberg KJV and write a filtered JSON file
to  <repo root>/data/quotes_bible.json  (≤ 75-word verses).

Run from anywhere:  python scripts/generate_bible_verses.py
"""

import json, re, ssl
from pathlib import Path
from urllib.request import urlopen, URLError

# ---------- CONFIG --------------------------------------------------------
SOURCE_URL  = "https://www.gutenberg.org/cache/epub/10/pg10.txt"
MAX_WORDS   = 75
AUTHOR      = "Various (King James Version)"
TRADITION   = "Christianity/Judaism"
LOCAL_RAW   = Path(__file__).with_name("pg10.txt")        # optional offline copy
# --------------------------------------------------------------------------

# ---------- Paths relative to repo root -----------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR  = REPO_ROOT / "data"
OUT_FILE  = DATA_DIR / "quotes_bible.json"
# --------------------------------------------------------------------------

_book_re  = re.compile(r"^\s*The\s+([A-Z][\w\s]+?)\s*$")
_verse_re = re.compile(r"^\s*(\d+):(\d+)\s+(.+?)\s*$")

def fetch_text() -> str:
    """Return raw pg10 text, handling SSL issues & offline fallback."""
    if LOCAL_RAW.exists():
        print("📄 Using local pg10.txt …")
        return LOCAL_RAW.read_text(encoding="utf-8", errors="ignore")

    print("⬇️  Downloading KJV from Project Gutenberg …")
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        return urlopen(SOURCE_URL, context=ctx).read().decode("utf-8", "ignore")
    except (ImportError, URLError, ssl.SSLError):
        ctx = ssl._create_unverified_context()
        return urlopen(SOURCE_URL, context=ctx).read().decode("utf-8", "ignore")

def strip_header(txt: str) -> str:
    s, e = txt.find("*** START OF"), txt.find("*** END OF")
    return txt[s:e] if s != -1 < e else txt

def parse_verses(raw: str):
    book = None
    for line in raw.splitlines():
        if m := _book_re.match(line):
            book = f"The {m.group(1).strip()}"
            continue
        if book and (v := _verse_re.match(line.strip())):
            chap, verse, text = v.groups()
            yield book, f"{chap}:{verse}", text

def build_records():
    raw = strip_header(fetch_text())
    for book, ref, text in parse_verses(raw):
        if len(text.split()) <= MAX_WORDS:
            yield {
                "text": text,
                "source": f"{book}, {ref}",
                "author": AUTHOR,
                "tradition": TRADITION,
                "book": book,
                "reference": ref,
            }

def main():
    DATA_DIR.mkdir(exist_ok=True)
    records = list(build_records())
    print(f"✅  {len(records):,} verses ≤ {MAX_WORDS} words extracted.")
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"💾  Saved to {OUT_FILE.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
