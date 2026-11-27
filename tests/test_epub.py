from pathlib import Path

from x2md import FileFormat, convert

EPUB = Path(__file__).with_name("fixtures") / "reading-order.epub"


def test_convert_epub_follows_the_book_reading_order() -> None:
    document = convert(EPUB.read_bytes(), format=FileFormat.EPUB)

    assert document.source_format is FileFormat.EPUB
    positions = [
        document.markdown.index(fragment)
        for fragment in ("# First chapter", "The first piece.", "# Second chapter", "The sequel.")
    ]
    assert positions == sorted(positions)
