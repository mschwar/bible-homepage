#!/usr/bin/env python3
"""
scrape_kjv_bible_pg.py
----------------------
Download Project Gutenberg’s public-domain KJV Bible and export a JSON list of
verses with ≤ 75 words in the unified quote schema.

Usage:
    python scrape_kjv_bible_pg.py
"""
import json
import re
import textwrap
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------------------------------
SOURCE_URL   = "https://www.gutenberg.org/cache/epub/10/pg10.txt"
OUT_PATH     = Path("data/quotes_kjv.json")
MAX_WORDS    = 75
AUTHOR_STR   = "Various (King James Version)"
TRADITION    = "Christianity/Judaism"
# ---------------------------------------------------------------------------

def fetch_text() -> str:
    print(f"⬇️  Downloading KJV from {SOURCE_URL} …")
    with urlopen(SOURCE_URL) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def strip_gutenberg_header(txt: str) -> str:
    start = txt.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end   = txt.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return txt[start:end] if start != -1 and end != -1 else txt

_book_re = re.compile(r"^\s*The\s+([A-Z][\w\s]+?)\s*$")
_verse_re = re.compile(r"^\s*(\d+):(\d+)\s+(.+?)\s*$")

def parse_verses(raw: str):
    """Yield (book, chapter:verse, text) tuples."""
    book = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Book heading line?
        m_book = _book_re.match(line)
        if m_book:
            book = f"The {m_book.group(1).strip()}"
            continue
        # Verse line?
        m_verse = _verse_re.match(line)
        if m_verse and book:
            chapter, verse, verse_text = m_verse.groups()
            ref = f"{chapter}:{verse}"
            yield book, ref, verse_text

def build_records():
    raw = fetch_text()
    raw = strip_gutenberg_header(raw)
    for book, ref, verse_text in parse_verses(raw):
        if len(verse_text.split()) > MAX_WORDS:
            continue            # skip long verses
        yield {
            "text"      : verse_text,
            "source"    : f"{book}, {ref}",
            "author"    : AUTHOR_STR,
            "tradition" : TRADITION,
            "book"      : book,
            "reference" : ref
        }

def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    records = list(build_records())
    print(f"✅  {len(records):,} verses ≤ {MAX_WORDS} words extracted.")
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"💾  Saved to {OUT_PATH.relative_to(Path.cwd())}")

if __name__ == "__main__":
    main()
