"""Slice specific pages out of a PDF and copy their text to the clipboard."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pyperclip
from pypdf import PdfReader, PdfWriter


def parse_pages(spec: str, total_pages: int) -> list[int]:
    """Parse "[1, 2, 3-6]" / "1,2,3-6" into an ordered, deduped 1-based page list."""
    cleaned = spec.strip().strip("[]")
    if not cleaned:
        raise ValueError("no pages specified")

    result: list[int] = []
    for raw in cleaned.split(","):
        part = raw.strip()
        if not part:
            continue
        if "-" in part:
            lo_str, hi_str = part.split("-", 1)
            lo, hi = int(lo_str.strip()), int(hi_str.strip())
            if lo > hi:
                lo, hi = hi, lo
            result.extend(range(lo, hi + 1))
        else:
            result.append(int(part))

    for p in result:
        if p < 1 or p > total_pages:
            raise ValueError(f"page {p} out of range (PDF has {total_pages} pages)")

    seen: set[int] = set()
    ordered: list[int] = []
    for p in result:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered


def next_sliced_path(original: Path) -> Path:
    """Return `<stem>_sliced_<n>.pdf` next to the original, n chosen to not overwrite."""
    n = 1
    while True:
        candidate = original.with_name(f"{original.stem}_sliced_{n}{original.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="pdfslice",
        description="Slice specific pages from a PDF and copy their text to clipboard.",
    )
    parser.add_argument("pdf", help="path to the input PDF")
    parser.add_argument(
        "pages",
        help='pages to keep, e.g. "[1, 2, 3-6]" or "1,2,3-6"',
    )
    parser.add_argument(
        "-c",
        "--clipboard-only",
        action="store_true",
        help="only copy text to clipboard; skip writing a sliced PDF",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.is_file():
        print(f"error: file not found: {pdf_path}", file=sys.stderr)
        return 1

    reader = PdfReader(str(pdf_path))
    total = len(reader.pages)

    try:
        page_numbers = parse_pages(args.pages, total)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    text_blocks = [reader.pages[p - 1].extract_text() or "" for p in page_numbers]
    pyperclip.copy("\n\n".join(text_blocks))
    print(f"copied text from {len(page_numbers)} page(s) to clipboard")

    if not args.clipboard_only:
        writer = PdfWriter()
        for p in page_numbers:
            writer.add_page(reader.pages[p - 1])
        out_path = next_sliced_path(pdf_path)
        with open(out_path, "wb") as f:
            writer.write(f)
        print(f"wrote sliced PDF: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
