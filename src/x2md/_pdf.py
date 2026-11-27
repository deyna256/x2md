"""Convert PDF pages with selective OCR."""

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path
from typing import BinaryIO

import xberg

from ._xberg import extract, extraction_warnings, read_source
from .document import ConversionWarning, MarkdownChunk
from .errors import InvalidDocumentError
from .formats import FileFormat, Language, OCRMode


def convert_pdf(
    source: Path | bytes | BinaryIO,
    /,
    *,
    ocr: OCRMode,
    ocr_languages: tuple[Language, ...],
) -> Iterator[MarkdownChunk]:
    data = read_source(source, FileFormat.PDF)
    mime_type = "application/pdf"
    config = xberg.ExtractionConfig(
        output_format="markdown",
        use_cache=False,
        disable_ocr=True,
        pages=xberg.PageConfig(extract_pages=True),
        content_filter=xberg.ContentFilterConfig(
            include_headers=True, include_footers=True, strip_repeating_text=False
        ),
        pdf_options=xberg.PdfConfig(extract_images=True, extract_vector_geometry=True)
        if ocr is OCRMode.FORCE
        else None,
    )
    native = extract(data, FileFormat.PDF, mime_type, config)
    pages = native.pages
    if pages is None:
        raise InvalidDocumentError("Xberg did not return pages for the PDF document.")

    metadata = native.metadata.format
    pdf = metadata.pdf if metadata is not None else None
    scans = set(pdf.scanned_pages or ()) if pdf is not None else set()
    scans_without_text = {
        page.page_number for page in pages if page.page_number in scans and not page.content.strip()
    }
    targets: set[int] = set()
    if ocr is OCRMode.AUTO:
        targets = scans_without_text
    elif ocr is OCRMode.FORCE:
        targets = {
            page.page_number
            for page in pages
            if page.page_number in scans
            or page.content.strip()
            or page.is_blank is False
            or page.geometry is not None
        }

    recognized: dict[int, tuple[str, bool]] = {}
    failures: set[int] = set()
    warnings = extraction_warnings(native, FileFormat.PDF)
    if targets:
        codes = {Language.ENGLISH: "eng", Language.RUSSIAN: "rus"}
        document = extract(
            data,
            FileFormat.PDF,
            mime_type,
            replace(
                config,
                disable_ocr=False,
                pdf_options=None,
                force_ocr_pages=sorted(targets),
                ocr=xberg.OcrConfig(
                    backend="tesseract", language=[codes[lang] for lang in ocr_languages] or ["eng"]
                ),
            ),
        )
        recognized = {
            page.page_number: (page.content, page.ocr_confidence is not None)
            for page in document.pages or ()
        }
        failures = {
            failed.page for failed in document.ocr_page_failures or () if not failed.recovered
        }
        warnings = warnings or extraction_warnings(document, FileFormat.PDF)

    has_markdown = False
    for page in sorted(pages, key=lambda item: item.page_number):
        number = page.page_number
        page_warnings = warnings
        warnings = ()
        backends = ("xberg",)
        content = page.content
        if ocr is OCRMode.OFF and number in scans_without_text:
            page_warnings += (
                ConversionWarning("ocr_disabled", "OCR is disabled for this scan.", number),
            )
        elif number in targets:
            ocr_text, used_ocr = recognized.get(number, ("", False))
            if used_ocr:
                backends += ("tesseract",)
            if used_ocr and number not in failures and ocr_text.strip():
                content = ocr_text
            else:
                page_warnings += (
                    ConversionWarning("ocr_no_text", "OCR did not return text.", number),
                )

        markdown = content.strip("\n") if content.strip() else ""
        if markdown:
            if has_markdown:
                markdown = "\n\n" + markdown
            has_markdown = True
        yield MarkdownChunk(markdown, page=number, backends=backends, warnings=page_warnings)
