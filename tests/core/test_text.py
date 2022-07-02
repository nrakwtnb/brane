import pytest
from pathlib import Path

from brane import ExtendedIO as xio
from utils import TextModule

TEXT_CONTENT = "Hello Universe !!"
TEXT_FILENAME = "test.text"

@pytest.fixture
def test_asset_path(tmpdir):
    path = Path(tmpdir) / TEXT_FILENAME
    with open(path, "w") as f:
        f.write(TEXT_CONTENT)
    yield path
    path.unlink(missing_ok=True)


def test_module_load(tmpdir, monkeypatch, test_asset_path: Path):
    monkeypatch.chdir(tmpdir)
    obj = TextModule.read(path=test_asset_path)
    assert obj == TEXT_CONTENT


def test_module_save(tmpdir, monkeypatch, test_asset_path: Path):
    monkeypatch.chdir(tmpdir)
    test_asset_path.unlink(missing_ok=True)
    TextModule.write(obj=TEXT_CONTENT, path=test_asset_path)
    assert test_asset_path.exists()
    # [TODO]: check whether it can be reloaded and matched with the original object


def test_xio_load(tmpdir, monkeypatch, test_asset_path: Path):
    monkeypatch.chdir(tmpdir)
    obj = xio.read(TEXT_FILENAME)
    assert obj == TEXT_CONTENT


def test_xio_save(tmpdir, monkeypatch, test_asset_path: Path):
    monkeypatch.chdir(tmpdir)
    test_asset_path.unlink(missing_ok=True)
    xio.write(obj=TEXT_CONTENT, path=TEXT_FILENAME)
    assert test_asset_path.exists()
