"""Self-check for export_docx.py. Run directly: uv run src/documentation/test_export_docx.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from export_docx import embed_mermaid_diagram, export_documentation, markdown_to_docx


def test_headings_and_paragraphs() -> None:
    doc = markdown_to_docx("# Title\n\nSome plain paragraph text.\n\n## Subheading\n")
    texts = [p.text for p in doc.paragraphs if p.text]
    styles = [p.style.name for p in doc.paragraphs if p.text]
    assert "Title" in texts
    assert "Some plain paragraph text." in texts
    assert "Subheading" in texts
    assert "Heading 1" in styles
    assert "Heading 2" in styles


def test_bullet_and_ordered_lists() -> None:
    doc = markdown_to_docx("- first bullet\n- second bullet\n\n1. step one\n2. step two\n")
    bullets = [p for p in doc.paragraphs if p.style.name == "List Bullet"]
    numbers = [p for p in doc.paragraphs if p.style.name == "List Number"]
    assert [p.text for p in bullets] == ["first bullet", "second bullet"]
    assert [p.text for p in numbers] == ["step one", "step two"]


def test_blockquote_is_italic() -> None:
    doc = markdown_to_docx("> Implementation status: this is a note.\n")
    quote_para = next(p for p in doc.paragraphs if "Implementation status" in p.text)
    assert all(run.italic for run in quote_para.runs if run.text.strip())


def test_inline_bold_and_code() -> None:
    doc = markdown_to_docx("- **Project**: `STUDIO_TEST_PROJECT`\n")
    para = next(p for p in doc.paragraphs if "Project" in p.text)
    bold_runs = [r for r in para.runs if r.bold]
    code_runs = [r for r in para.runs if r.font.name == "Courier New"]
    assert any(r.text == "Project" for r in bold_runs)
    assert any(r.text == "STUDIO_TEST_PROJECT" for r in code_runs)


def test_horizontal_rule_produces_no_extra_paragraph() -> None:
    doc = markdown_to_docx("Para one.\n\n---\n\nPara two.\n")
    texts = [p.text for p in doc.paragraphs if p.text]
    assert texts == ["Para one.", "Para two."]


def test_gfm_table() -> None:
    md = (
        "| Column | Type |\n"
        "|--------|------|\n"
        "| CustomerID | Whole number |\n"
        "| Email | Text |\n"
    )
    doc = markdown_to_docx(md)
    assert len(doc.tables) == 1
    table = doc.tables[0]
    assert len(table.rows) == 3
    assert table.rows[0].cells[0].text == "Column"
    assert table.rows[0].cells[1].text == "Type"
    assert table.rows[1].cells[0].text == "CustomerID"
    assert table.rows[2].cells[1].text == "Text"
    header_run = table.rows[0].cells[0].paragraphs[0].runs[0]
    assert header_run.bold


def test_fenced_code_block_monospace() -> None:
    md = "```text\nplain code line\n```\n"
    doc = markdown_to_docx(md)
    code_para = next(p for p in doc.paragraphs if p.text == "plain code line")
    assert code_para.runs[0].font.name == "Courier New"


def test_mermaid_block_embeds_picture() -> None:
    md = "```mermaid\nflowchart LR\n  A --> B\n```\n"
    doc = markdown_to_docx(md)
    assert len(doc.inline_shapes) == 1


def test_mermaid_render_failure_falls_back_to_text() -> None:
    from unittest.mock import patch

    from docx import Document

    doc = Document()
    with patch("export_docx.mermaidx.render", side_effect=RuntimeError("boom")):
        embed_mermaid_diagram(doc, "not real mermaid source")
    assert len(doc.inline_shapes) == 0
    assert any("not real mermaid source" in p.text for p in doc.paragraphs)


def test_export_documentation_against_real_docs() -> None:
    import zipfile

    repo_root = Path(__file__).parent.parent.parent
    docs_dir = repo_root / "documentation"
    job_doc = docs_dir / "talend" / "STUDIO_TEST_PROJECT" / "job_OnBoardingDemoJob.md"
    arch_doc = docs_dir / "01_system_architecture.md"
    assert job_doc.is_file(), f"expected fixture missing: {job_doc}"
    assert arch_doc.is_file(), f"expected fixture missing: {arch_doc}"
    assert "|" in job_doc.read_text(encoding="utf-8"), "fixture should contain a table"
    assert "```mermaid" in arch_doc.read_text(encoding="utf-8"), "fixture should contain a Mermaid block"

    written = export_documentation(docs_dir)
    assert written, "expected at least one .docx to be written"

    job_docx = docs_dir / "docx" / "talend" / "STUDIO_TEST_PROJECT" / "job_OnBoardingDemoJob.docx"
    arch_docx = docs_dir / "docx" / "01_system_architecture.docx"
    assert job_docx in written
    assert arch_docx in written

    with zipfile.ZipFile(job_docx) as zf:
        assert "word/document.xml" in zf.namelist()

    with zipfile.ZipFile(arch_docx) as zf:
        assert any(n.startswith("word/media/") for n in zf.namelist()), (
            "expected the Mermaid diagram to be embedded as an image"
        )

    # Re-running must not reprocess this script's own prior docx/ output.
    first_run_count = len(written)
    second_written = export_documentation(docs_dir)
    assert len(second_written) == first_run_count


def main() -> None:
    test_headings_and_paragraphs()
    test_bullet_and_ordered_lists()
    test_blockquote_is_italic()
    test_inline_bold_and_code()
    test_horizontal_rule_produces_no_extra_paragraph()
    test_gfm_table()
    test_fenced_code_block_monospace()
    test_mermaid_block_embeds_picture()
    test_mermaid_render_failure_falls_back_to_text()
    test_export_documentation_against_real_docs()
    print("All export_docx.py checks passed.")


if __name__ == "__main__":
    main()
