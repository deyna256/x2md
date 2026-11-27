import asyncio
from pathlib import Path

import pytest

from x2md import FileFormat, InvalidDocumentError, MarkdownDocument, SourceReadError, convert

DOCX = Path(__file__).with_name("fixtures") / "structure.docx"


def test_convert_docx_preserves_structure_in_order() -> None:
    document = convert(DOCX, format=FileFormat.DOCX)

    assert document.source_format is FileFormat.DOCX
    positions = [
        document.markdown.index(fragment)
        for fragment in (
            "# Project heading",
            "- First item",
            "[Reference](https://example.invalid/docx)",
            "| Name | Value |",
        )
    ]
    assert positions == sorted(positions)


def test_convert_docx_from_a_running_event_loop() -> None:
    async def convert_in_loop() -> MarkdownDocument:
        return convert(DOCX.read_bytes(), format=FileFormat.DOCX)

    assert "# Project heading" in asyncio.run(convert_in_loop()).markdown


def test_docx_errors_distinguish_reading_and_parsing(tmp_path: Path) -> None:
    with pytest.raises(SourceReadError, match="read the docx source"):
        convert(tmp_path / "missing.docx", format=FileFormat.DOCX)
    with pytest.raises(InvalidDocumentError, match="convert the docx document"):
        convert(b"Not a DOCX file", format=FileFormat.DOCX)
