"""Adapt Xberg extraction to the synchronous handler contract."""

import asyncio
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import BinaryIO

import xberg

from .document import ConversionWarning, MarkdownChunk
from .errors import (
    BackendUnavailableError,
    InvalidDocumentError,
    SourceReadError,
    UnsupportedOCRModeError,
)
from .formats import FileFormat, Language, OCRMode


def read_source(source: Path | bytes | BinaryIO, format: FileFormat) -> bytes:
    if isinstance(source, bytes):
        return source
    try:
        data = source.read_bytes() if isinstance(source, Path) else source.read()
    except (OSError, ValueError):
        raise SourceReadError(f"Could not read the {format} source.") from None
    if not isinstance(data, bytes):
        raise SourceReadError(f"Expected a binary source for {format}.")
    return data


def extract(
    data: bytes, format: FileFormat, mime_type: str, config: xberg.ExtractionConfig
) -> xberg.ExtractedDocument:
    source = xberg.ExtractInput(kind="bytes", bytes=data, mime_type=mime_type)

    def run() -> xberg.ExtractionResult:
        return asyncio.run(xberg.extract(source, config))

    try:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            output = run()
        else:
            with ThreadPoolExecutor(max_workers=1) as worker:
                output = worker.submit(run).result()
    except xberg.MissingDependencyError:
        raise BackendUnavailableError(f"Xberg could not load a backend for {format}.") from None
    except xberg.XbergError:
        raise InvalidDocumentError(f"Xberg could not convert the {format} document.") from None

    results = output.results
    if output.errors or len(results) != 1 or results[0].mime_type != mime_type:
        raise InvalidDocumentError(f"Xberg could not convert the {format} document.")
    return results[0]


def extraction_warnings(
    document: xberg.ExtractedDocument, format: FileFormat
) -> tuple[ConversionWarning, ...]:
    if document.processing_warnings:
        return (ConversionWarning("xberg_warning", f"Xberg reported a warning for {format}."),)
    return ()


def convert_document(
    source: Path | bytes | BinaryIO,
    /,
    *,
    ocr: OCRMode,
    ocr_languages: tuple[Language, ...],
    format: FileFormat,
    mime_type: str,
) -> Iterator[MarkdownChunk]:
    if ocr is OCRMode.FORCE:
        raise UnsupportedOCRModeError(format, ocr)
    document = extract(
        read_source(source, format),
        format,
        mime_type,
        xberg.ExtractionConfig(output_format="markdown", use_cache=False, disable_ocr=True),
    )
    yield MarkdownChunk(
        document.content, backends=("xberg",), warnings=extraction_warnings(document, format)
    )
