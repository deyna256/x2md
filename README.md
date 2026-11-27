# x2md

A Python library in development for converting documents and ebooks to Markdown.
The current checkout contains the package and its development tools. The first converter is pending.

## Development

From this checkout, create the virtual environment and run the checks.

```sh
uv sync --locked
just ci
```

The development interpreter is Python 3.12. CI tests Python 3.12 through 3.14.
Use `just format` to format changes and `just test` to run the tests.
`uv build` produces a source distribution and a wheel in `dist/`.
