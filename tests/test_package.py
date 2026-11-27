from importlib import metadata, resources

import x2md


def test_installed_package() -> None:
    assert metadata.metadata("x2md")["Name"] == x2md.__name__
    assert resources.files(x2md).joinpath("py.typed").is_file()
