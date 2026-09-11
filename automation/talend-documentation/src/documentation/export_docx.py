#!/usr/bin/env python3
"""
Markdown to Word (.docx) Exporter
==================================
Converts every .md file under a documentation directory into a mirrored
.docx tree under <docs_dir>/docx/. Hand-rolled Markdown parsing (no new
dependency) — headings, paragraphs, inline bold/code, lists, blockquotes,
GFM tables, and fenced code blocks (Mermaid blocks are rendered to PNG and
embedded as pictures). No network access, no AI calls, no source-JSON
access — operates only on the Markdown tree.

Usage:
    python export_docx.py documentation/
"""

import argparse
import io
import logging
import os
import re
import sys
from pathlib import Path

import mermaidx
from docx import Document
from docx.shared import Inches
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Inline formatting
# ---------------------------------------------------------------------------

INLINE_PATTERN = re.compile(r"(\*\*.+?\*\*|`[^`]+`)")


def add_inline_runs(paragraph, text: str) -> None:
    """Split text on **bold** and `code` spans and add each as a separate run."""
    for token in INLINE_PATTERN.split(text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("`") and token.endswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Courier New"
        else:
            paragraph.add_run(token)


# ---------------------------------------------------------------------------
# Markdown -> docx
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
ORDERED_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def parse_table_row(line: str) -> list[str]:
    """Split a GFM pipe-table row into its cell texts."""
    line = line.strip()
    line = line.removeprefix("|")
    line = line.removesuffix("|")
    return [cell.strip() for cell in line.split("|")]


FENCE_RE = re.compile(r"^```\s*(\S*)\s*$")


def embed_mermaid_diagram(doc: Document, source: str) -> None:
    """Render Mermaid source to PNG and embed it; falls back to monospace text on render failure."""
    try:
        png_bytes = mermaidx.render(source).png(width=1200)
    except Exception as e:  # noqa: BLE001 -- mermaidx has no narrow exception
        # type for malformed diagram source; catch broadly and degrade to
        # raw text rather than aborting the whole file's conversion.
        logger.warning(f"Failed to render Mermaid diagram, embedding raw source instead: {e}")
        for line in source.splitlines():
            code_para = doc.add_paragraph(line if line else " ")
            if code_para.runs:
                code_para.runs[0].font.name = "Courier New"
        return
    doc.add_picture(io.BytesIO(png_bytes), width=Inches(6.0))


def markdown_to_docx(text: str) -> Document:
    """Convert Markdown text into a python-docx Document."""
    doc = Document()
    lines = text.splitlines()
    i = 0
    n = len(lines)
    paragraph_buffer: list[str] = []

    def flush_paragraph():
        if paragraph_buffer:
            para = doc.add_paragraph()
            add_inline_runs(para, " ".join(paragraph_buffer))
            paragraph_buffer.clear()

    while i < n:
        fence_match = FENCE_RE.match(lines[i])
        if fence_match:
            flush_paragraph()
            lang = fence_match.group(1).lower()
            i += 1
            block_lines = []
            while i < n and not lines[i].startswith("```"):
                block_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            source = "\n".join(block_lines)
            if lang == "mermaid":
                embed_mermaid_diagram(doc, source)
            else:
                for bl in block_lines:
                    code_para = doc.add_paragraph(bl if bl else " ")
                    if code_para.runs:
                        code_para.runs[0].font.name = "Courier New"
            continue

        stripped = lines[i].rstrip()

        if not stripped.strip():
            flush_paragraph()
            i += 1
            continue

        if stripped.strip() == "---":
            flush_paragraph()
            i += 1
            continue

        if "|" in stripped and i + 1 < n and TABLE_SEPARATOR.match(lines[i + 1]):
            flush_paragraph()
            header_cells = parse_table_row(stripped)
            i += 2  # skip header + separator
            data_rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                data_rows.append(parse_table_row(lines[i]))
                i += 1
            table = doc.add_table(rows=1 + len(data_rows), cols=len(header_cells))
            table.style = "Light Grid Accent 1"
            for col, cell_text in enumerate(header_cells):
                cell = table.rows[0].cells[col]
                cell.text = ""
                add_inline_runs(cell.paragraphs[0], cell_text)
                for run in cell.paragraphs[0].runs:
                    run.bold = True
            for row_idx, row_cells in enumerate(data_rows, start=1):
                for col, cell_text in enumerate(row_cells):
                    if col < len(header_cells):
                        cell = table.rows[row_idx].cells[col]
                        cell.text = ""
                        add_inline_runs(cell.paragraphs[0], cell_text)
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            doc.add_heading(heading_match.group(2).strip(), level=level)
            i += 1
            continue

        bullet_match = BULLET_RE.match(stripped)
        if bullet_match:
            flush_paragraph()
            para = doc.add_paragraph(style="List Bullet")
            add_inline_runs(para, bullet_match.group(1))
            i += 1
            continue

        ordered_match = ORDERED_RE.match(stripped)
        if ordered_match:
            flush_paragraph()
            para = doc.add_paragraph(style="List Number")
            add_inline_runs(para, ordered_match.group(1))
            i += 1
            continue

        blockquote_match = BLOCKQUOTE_RE.match(stripped)
        if blockquote_match:
            flush_paragraph()
            para = doc.add_paragraph()
            run = para.add_run(blockquote_match.group(1))
            run.italic = True
            i += 1
            continue

        paragraph_buffer.append(stripped.strip())
        i += 1

    flush_paragraph()
    return doc


# ---------------------------------------------------------------------------
# File conversion and tree walk
# ---------------------------------------------------------------------------


def convert_file(md_path: Path, docx_path: Path) -> None:
    """Convert one Markdown file to .docx, creating parent directories as needed."""
    text = md_path.read_text(encoding="utf-8")
    doc = markdown_to_docx(text)
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))


def export_documentation(docs_dir: Path) -> list[Path]:
    """Convert every .md file under docs_dir to .docx under docs_dir/docx/, mirroring the source tree."""
    output_root = docs_dir / "docx"
    written = []
    for md_path in sorted(docs_dir.rglob("*.md")):
        if output_root in md_path.parents:
            continue  # never reprocess this script's own prior output
        rel = md_path.relative_to(docs_dir)
        docx_path = output_root / rel.with_suffix(".docx")
        try:
            convert_file(md_path, docx_path)
            written.append(docx_path)
        except Exception as e:  # noqa: BLE001 -- one bad file must not abort the run
            logger.warning(f"Failed to convert {md_path}: {e}")
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Convert generated Markdown documentation to Word (.docx)",
    )
    parser.add_argument(
        "docs_dir",
        nargs="?",
        default=os.environ.get("OUTPUT_DOCUMENTATION_PATH", "./documentation"),
        help="Directory containing generated Markdown files "
        "(default: ./documentation/, or set OUTPUT_DOCUMENTATION_PATH env var)",
    )
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.is_dir():
        logger.error(f"Documentation directory does not exist: {docs_dir}")
        sys.exit(1)

    written = export_documentation(docs_dir)
    if not written:
        logger.warning(f"No .md files found under {docs_dir}")
        sys.exit(0)

    logger.info(f"Converted {len(written)} file(s) to .docx under {docs_dir / 'docx'}")


if __name__ == "__main__":
    main()
