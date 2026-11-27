"""Internal contract for built-in format handlers."""

from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO, Protocol

from .document import MarkdownChunk
from .formats import Language, OCRMode


class Handler(Protocol):
    def __call__(
        self,
        source: Path | bytes | BinaryIO,
        /,
        *,
        ocr: OCRMode,
        ocr_languages: tuple[Language, ...],
    ) -> Iterator[MarkdownChunk]: ...
