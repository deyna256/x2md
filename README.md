# x2md

Python library for converting documents and ebooks to Markdown. The public API
is in development. This checkout has no built-in format handlers yet.

## Python API

- `convert(source, *, format, ocr, ocr_languages)` collects Markdown and diagnostics
  in a `MarkdownDocument`. Its `source_format` records the input format.
- `iter_markdown(...)` yields `MarkdownChunk` objects. Each handler determines
  how much Markdown it can emit at once.
- `convert_many(inputs, *, ocr, ocr_languages)` consumes pairs of source and
  format lazily, in order. An error stops the batch.

Pass a path, bytes or a binary stream as the source. Supply the input format
explicitly with `FileFormat`. The OCR options are optional and default to
`ocr=OCRMode.AUTO` and `ocr_languages=()`. A format without a handler raises
`UnsupportedFormatError` when conversion starts.

## Development

The project targets Python 3.12 and later. From the checkout, run:

```sh
uv sync --locked
just ci
```
