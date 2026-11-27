from pathlib import Path

import pytest

from x2md import FileFormat, Language, OCRMode, iter_markdown

PDF = Path(__file__).with_name("fixtures") / "mixed-pages.pdf"


@pytest.mark.parametrize(
    ("ocr", "ocr_pages"),
    [(OCRMode.OFF, []), (OCRMode.AUTO, [3]), (OCRMode.FORCE, [1, 3, 4])],
)
def test_pdf_converts_pages_in_order_with_selective_ocr(ocr: OCRMode, ocr_pages: list[int]) -> None:
    chunks = list(
        iter_markdown(PDF, format=FileFormat.PDF, ocr=ocr, ocr_languages=(Language.ENGLISH,))
    )

    assert [chunk.page for chunk in chunks] == [1, 2, 3, 4]
    assert [chunk.page for chunk in chunks if "tesseract" in chunk.backends] == ocr_pages
    assert "NATIVE PAGE" in chunks[0].markdown
    if ocr is not OCRMode.FORCE:
        assert chunks[0].markdown == "NATIVE PAGE TEXT"
    assert chunks[1].markdown == ""
    assert ("SCANNED PAGE TEXT" in chunks[2].markdown) is (ocr is not OCRMode.OFF)
    if ocr is not OCRMode.OFF:
        assert chunks[2].markdown.startswith("\n\n")
    skipped = [
        warning.page
        for chunk in chunks
        for warning in chunk.warnings
        if warning.code == "ocr_disabled"
    ]
    assert skipped == ([3] if ocr is OCRMode.OFF else [])
