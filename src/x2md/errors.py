"""Exceptions shared by all x2md format handlers."""

from .formats import FileFormat, OCRMode


class ConversionError(Exception):
    """The input could not be converted to Markdown."""


class BackendUnavailableError(ConversionError):
    """A required engine or language resource is unavailable."""


class UnsupportedFormatError(ConversionError):
    """No built-in handler can convert the supplied input format."""


class SourceReadError(ConversionError):
    """The input could not be read."""


class InvalidDocumentError(ConversionError):
    """The contents could not be decoded or parsed in the requested format."""


class UnsupportedOCRModeError(ConversionError):
    """The selected format handler cannot honor the requested OCR mode."""

    def __init__(self, format: FileFormat, mode: OCRMode) -> None:
        super().__init__(format, mode)
        self.format = format
        self.mode = mode

    def __str__(self) -> str:
        return f"Format '{self.format}' does not support OCR mode '{self.mode}'."
