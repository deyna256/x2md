"""Document and ebook conversion to Markdown."""

from .conversion import convert, convert_many, iter_markdown
from .document import ConversionWarning, MarkdownChunk, MarkdownDocument
from .errors import (
    BackendUnavailableError,
    ConversionError,
    InvalidDocumentError,
    SourceReadError,
    UnsupportedFormatError,
    UnsupportedOCRModeError,
)
from .formats import FileFormat, Language, OCRMode

__all__ = [
    "BackendUnavailableError",
    "ConversionError",
    "ConversionWarning",
    "FileFormat",
    "InvalidDocumentError",
    "Language",
    "MarkdownChunk",
    "MarkdownDocument",
    "OCRMode",
    "SourceReadError",
    "UnsupportedFormatError",
    "UnsupportedOCRModeError",
    "convert",
    "convert_many",
    "iter_markdown",
]
