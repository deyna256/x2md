"""Markdown output and its conversion diagnostics."""

from dataclasses import dataclass

from .formats import FileFormat


@dataclass(frozen=True, slots=True)
class ConversionWarning:
    code: str
    message: str
    page: int | None = None


@dataclass(frozen=True, slots=True)
class MarkdownChunk:
    """Append markdown verbatim to the output. A warning may have no text."""

    markdown: str
    page: int | None = None
    backends: tuple[str, ...] = ()
    warnings: tuple[ConversionWarning, ...] = ()


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    """Converted Markdown, its input format and any extraction diagnostics."""

    markdown: str
    source_format: FileFormat
    backends: tuple[str, ...] = ()
    warnings: tuple[ConversionWarning, ...] = ()

    def __str__(self) -> str:
        return self.markdown
