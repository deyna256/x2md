"""Input formats and OCR settings."""

from enum import StrEnum


class FileFormat(StrEnum):
    TEXT = "txt"
    EPUB = "epub"
    DOCX = "docx"
    PDF = "pdf"
    DJVU = "djvu"
    MARKDOWN = "md"


class Language(StrEnum):
    RUSSIAN = "ru"
    ENGLISH = "en"


class OCRMode(StrEnum):
    OFF = "off"
    AUTO = "auto"
    FORCE = "force"
