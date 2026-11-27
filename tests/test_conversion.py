from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

import pytest

from x2md import (
    ConversionWarning,
    FileFormat,
    Language,
    MarkdownChunk,
    MarkdownDocument,
    OCRMode,
    UnsupportedFormatError,
    conversion,
    convert,
    convert_many,
    iter_markdown,
)


def test_missing_handler(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(conversion._HANDLERS, FileFormat.PDF, raising=False)
    with pytest.raises(UnsupportedFormatError, match="No handler for pdf"):
        convert("missing-file", format=FileFormat.PDF)


def test_format_is_required() -> None:
    with pytest.raises(TypeError, match="required keyword-only argument: 'format'"):
        convert(b"data")  # ty: ignore[missing-argument]


def test_unsupported_format() -> None:
    with pytest.raises(UnsupportedFormatError, match="Unsupported file format"):
        convert(b"data", format="unknown")  # ty: ignore[invalid-argument-type]


def test_conversion_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    chunks = (
        MarkdownChunk("# Chapter", backends=("reader",)),
        MarkdownChunk("\nBody", backends=("reader", "ocr")),
        MarkdownChunk("", warnings=(ConversionWarning("partial", "Missing text", page=3),)),
    )
    seen = []

    def handler(
        source: Path | bytes | BinaryIO, /, *, ocr: OCRMode, ocr_languages: tuple[Language, ...]
    ) -> Iterator[MarkdownChunk]:
        seen.append((source, ocr, ocr_languages))
        yield from chunks

    monkeypatch.setitem(conversion._HANDLERS, FileFormat.PDF, handler)
    assert tuple(iter_markdown(b"input", format=FileFormat.PDF)) == chunks

    jobs = [("first.pdf", FileFormat.PDF), ("second.pdf", FileFormat.PDF)]
    results = convert_many(jobs, ocr=OCRMode.FORCE, ocr_languages=(Language.RUSSIAN,))
    assert seen == [(b"input", OCRMode.AUTO, ())]
    doc = next(results)
    assert seen[-1] == (Path("first.pdf"), OCRMode.FORCE, (Language.RUSSIAN,))
    assert len(seen) == 2
    assert doc == MarkdownDocument(
        markdown="# Chapter\nBody",
        source_format=FileFormat.PDF,
        backends=("reader", "ocr"),
        warnings=chunks[-1].warnings,
    )
    assert list(results) == [doc]
    assert seen[-1][0] == Path("second.pdf")
