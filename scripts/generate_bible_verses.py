#!/usr/bin/env python3
"""
generate_bible_verses.py
------------------------
Download Project Gutenberg’s KJV, extract ≤75-word verses, save to
data/quotes_kjv.json (unified schema).

Handles SSL-cert issues by first trying certifi, then falling back to
a non-verifying context.

Usage:
    python generate_bible_verses.py
"""
import json, re, ssl, textwrap
from pathlib import Path
from urllib.request import urlopen, URLError

SOURCE_URL = "https://www.gutenberg.org/cache/epub/10/pg10.txt"
LOCAL_FALLBACK = Path("scripts/pg10.txt")        # optional manual download
OUT_PATH  = Path("data/quotes_kjv.json")
MAX_WORDS = 75
AUTHOR    = "Various (King James Version)"
TRADITION = "Christianity/Judaism"

_book_re  = re.compile(r"^\s*The\s+([A-Z][\w\s]+?)\s*$")
_verse_re = re.compile(r"^\s*(\d+):(\d+)\s+(.+?)\s*$")

# ---------------------------------------------------------------------------

def fetch_text() -> str:
    """Return pg10.txt, trying certifi first, then unverified SSL as fallback."""
    if LOCAL_FALLBACK.exists():
        print("📄 Using local pg10.txt …")
        return LOCAL_FALLBACK.read_text(encoding="utf-8", errors="ignore")

    print(f"⬇️  Downloading KJV from {SOURCE_URL} …")

    # 1) secure attempt
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        with urlopen(SOURCE_URL, context=ctx) as r:
            return r.read().decode("utf-8", errors="ignore")
    except (ModuleNotFoundError, URLError, ssl.SSLError) as e:
        print("⚠️  Secure download failed:", e)

    # 2) fallback (no verify)
    print("🔓 Retrying with insecure SSL context…")
    ctx = ssl._create_unverified_context()
    with urlopen(SOURCE_URL, context=ctx) as r:
        return r.read().decode("utf-8", errors="ignore")

def strip_header(txt: str) -> str:
    start = txt.find("*** START OF")
    end   = txt.find("*** END OF")
    return txt[start:end] if start != -1 < end else txt

def parse_verses(raw: str):
    book = None
    for line in raw.splitlines():
        if m := _book_re.match(line):
            book = f"The {m.group(1).strip()}"
            continue
        if m := _verse_re.match(line.strip()) and book:
            chap, verse, text = _verse_re.match(line.strip()).groups()
            yield book, f"{chap}:{verse}", text

def build_records():
    raw = strip_header(fetch_text())
    for book, ref, verse in parse_verses(raw):
        if len(verse.split()) > MAX_WORDS:
            continue
        yield {
            "text": verse,
            "source": f"{book}, {ref}",
            "author": AUTHOR,
            "tradition": TRADITION,
            "book": book,
            "reference": ref,
        }

def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    records = list(build_records())
    print(f"✅  Extracted {len(records):,} verses ≤ {MAX_WORDS} words.")
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"💾  Saved → {OUT_PATH}")

if __name__ == "__main__":
    main()
