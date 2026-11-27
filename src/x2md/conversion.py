"""Dispatch conversion requests to built-in format handlers."""

from collections.abc import Generator, Iterable, Iterator
from functools import partial
from os import PathLike
from pathlib import Path
from typing import BinaryIO

from ._handlers import Handler
from ._xberg import convert_document
from .document import MarkdownChunk, MarkdownDocument
from .errors import UnsupportedFormatError
from .formats import FileFormat, Language, OCRMode

_HANDLERS: dict[FileFormat, Handler] = {
    FileFormat.ODT: partial(
        convert_document, format=FileFormat.ODT, mime_type="application/vnd.oasis.opendocument.text"
    ),
}


type _Source = str | PathLike[str] | bytes | BinaryIO


def _format(value: FileFormat) -> FileFormat:
    if isinstance(value, FileFormat):
        return value
    if not isinstance(value, str):
        raise UnsupportedFormatError("Expected a FileFormat for format.")
    key = value.lower().removeprefix(".")
    key = {"markdown": "md", "djv": "djvu"}.get(key, key)
    try:
        return FileFormat(key)
    except ValueError as exc:
        raise UnsupportedFormatError(f"Unsupported file format: {key}.") from exc


def iter_markdown(
    source: _Source,
    *,
    format: FileFormat,
    ocr: OCRMode = OCRMode.AUTO,
    ocr_languages: tuple[Language, ...] = (),
) -> Generator[MarkdownChunk, None, None]:
    """Yield appendable Markdown fragments from a path, bytes or binary stream."""
    resolved = _format(format)
    data = Path(source) if isinstance(source, (str, PathLike)) else source
    if not isinstance(ocr, OCRMode):
        raise TypeError("ocr must be an OCRMode.")
    if not all(isinstance(language, Language) for language in ocr_languages):
        raise TypeError("ocr_languages must contain Language members.")
    handler = _HANDLERS.get(resolved)
    if handler is None:
        raise UnsupportedFormatError(f"No handler for {resolved.value}.")
    yield from handler(data, ocr=ocr, ocr_languages=ocr_languages)


def convert(
    source: _Source,
    *,
    format: FileFormat,
    ocr: OCRMode = OCRMode.AUTO,
    ocr_languages: tuple[Language, ...] = (),
) -> MarkdownDocument:
    """Collect Markdown and diagnostics for one input."""
    resolved = _format(format)
    parts = []
    backends: dict[str, None] = {}
    warnings = []
    for chunk in iter_markdown(source, format=resolved, ocr=ocr, ocr_languages=ocr_languages):
        parts.append(chunk.markdown)
        backends.update(dict.fromkeys(chunk.backends))
        warnings.extend(chunk.warnings)
    return MarkdownDocument("".join(parts), resolved, tuple(backends), tuple(warnings))


def convert_many(
    inputs: Iterable[tuple[_Source, FileFormat]],
    *,
    ocr: OCRMode = OCRMode.AUTO,
    ocr_languages: tuple[Language, ...] = (),
) -> Iterator[MarkdownDocument]:
    """Convert inputs lazily in caller order. An error stops iteration."""
    for source, format in inputs:
        yield convert(source, format=format, ocr=ocr, ocr_languages=ocr_languages)
