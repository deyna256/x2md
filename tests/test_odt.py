from io import BytesIO
from pathlib import Path

from x2md import FileFormat, convert

ODT = Path(__file__).with_name("fixtures") / "structure.odt"


def test_convert_odt_preserves_structure_in_order() -> None:
    with BytesIO(ODT.read_bytes()) as source:
        document = convert(source, format=FileFormat.ODT)
        assert not source.closed

    assert document.source_format is FileFormat.ODT
    positions = [
        document.markdown.index(fragment)
        for fragment in (
            "# Project heading",
            "- First item",
            "[Reference](https://example.invalid/odt)",
            "| Name | Value |",
            "| --- | --- |",
            "| Size | Small |",
        )
    ]
    assert positions == sorted(positions)
