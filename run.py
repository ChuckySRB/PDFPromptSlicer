# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pypdf>=4.0",
#     "pyperclip>=1.8",
# ]
# ///
"""Local dev entry point.

For normal use, install the tool with:
    uv tool install git+https://github.com/ChuckySRB/PDFPromptSlicer
and then run `pdfslice ...` from anywhere.

For running without installing, from the repo root:
    uv run --script run.py <pdf> "[1, 3-5]"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from pdf_prompt_slicer.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
