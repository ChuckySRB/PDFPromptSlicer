# pdf-prompt-slicer

A tiny CLI that slices specific pages out of a PDF **and** copies the extracted text to your clipboard — so you can feed an LLM a focused subset of a document instead of uploading the whole thing.

- Pick pages individually or by range: `"[1, 2, 3-6]"`
- Get a new, shorter PDF saved next to the original
- Get the raw text of those pages on your clipboard, ready to paste
- Optional clipboard-only mode when you don't need a new PDF

## Install (simplest)

Requires [uv](https://docs.astral.sh/uv/). If you don't have it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install this tool in one line:

```bash
uv tool install pdf-prompt-slicer
```

That puts a `pdfslice` command on your PATH. You can now run it from anywhere.

> Prefer pip? `pipx install pdf-prompt-slicer` works the same way.

To upgrade later: `uv tool upgrade pdf-prompt-slicer`
To uninstall: `uv tool uninstall pdf-prompt-slicer`

## Usage

```bash
pdfslice <path_to_pdf> "<pages>" [-c]
```

### Arguments

- `<path_to_pdf>` — path to the source PDF.
- `<pages>` — a list of pages or ranges. Brackets are optional; whitespace is fine.
  Examples: `"[1, 2, 3-6]"`, `"1,2,3-6"`, `"4-4"`, `"7"`.
- `-c`, `--clipboard-only` — copy text to the clipboard only; do **not** write a sliced PDF.

### Examples

Slice pages 1, 2, and 3 through 6 into a new PDF **and** copy their text:

```bash
pdfslice paper.pdf "[1, 2, 3-6]"
```

Just copy the text (no new PDF):

```bash
pdfslice paper.pdf "[1, 2, 3-6]" -c
```

### Output

- The sliced PDF is saved **next to the original** with `_sliced_<n>` appended to the filename.
  `paper.pdf` → `paper_sliced_1.pdf`. Running again produces `paper_sliced_2.pdf`, etc. — existing files are never overwritten.
- The combined text of all selected pages (separated by blank lines) is placed on the system clipboard.

## Running without installing

From a clone of the repo:

```bash
uv run --script run.py <pdf> "[1, 3-5]"
```

`uv` reads the inline script metadata at the top of `run.py` and sets up a temporary env with the right dependencies — no manual install step.

## Development

```bash
git clone https://github.com/ChuckySRB/PDFPromptSlicer
cd PDFPromptSlicer
uv sync
uv run pdfslice test_data/your.pdf "[1-3]"
```

The project layout:

```
PDFPromptSlicer/
├── pyproject.toml
├── run.py                    # inline-deps entry point (no install needed)
├── src/pdf_prompt_slicer/
│   ├── __init__.py
│   ├── __main__.py           # enables `python -m pdf_prompt_slicer`
│   └── cli.py                # real implementation + `main()`
└── test_data/                # gitignored; for local testing
```

## Dependencies

- [`pypdf`](https://pypi.org/project/pypdf/) — PDF read/write
- [`pyperclip`](https://pypi.org/project/pyperclip/) — cross-platform clipboard

On Linux, `pyperclip` needs either `xclip` or `xsel` installed for clipboard access. macOS and Windows work out of the box.
