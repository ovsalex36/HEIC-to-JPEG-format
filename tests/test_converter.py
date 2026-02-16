from pathlib import Path

import pytest

from heic_to_jpeg.converter import (
    convert_heic_to_jpeg,
    discover_heic_files,
    is_heic_file,
    output_path_for,
)


def test_is_heic_file_detects_supported_extensions(tmp_path: Path) -> None:
    file_path = tmp_path / "photo.HEIC"
    file_path.write_bytes(b"dummy")
    assert is_heic_file(file_path)


def test_output_path_for_uses_output_dir(tmp_path: Path) -> None:
    input_path = tmp_path / "image.heic"
    output_dir = tmp_path / "out"
    assert output_path_for(input_path, output_dir) == output_dir / "image.jpg"


def test_discover_heic_files_directory_non_recursive(tmp_path: Path) -> None:
    (tmp_path / "a.heic").write_bytes(b"x")
    (tmp_path / "b.heif").write_bytes(b"x")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.heic").write_bytes(b"x")

    files = discover_heic_files(tmp_path)
    assert files == [tmp_path / "a.heic", tmp_path / "b.heif"]


class _DummyImage:
    def __init__(self) -> None:
        self.saved = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def convert(self, mode: str):
        assert mode == "RGB"
        return self

    def save(self, output_path, fmt, quality, optimize):
        self.saved = (output_path, fmt, quality, optimize)
        Path(output_path).write_bytes(b"jpeg")


def test_convert_heic_to_jpeg_writes_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    in_file = tmp_path / "sample.heic"
    in_file.write_bytes(b"heic-bytes")
    out_file = tmp_path / "sample.jpg"

    monkeypatch.setattr("heic_to_jpeg.converter._open_image", lambda _: _DummyImage())

    result = convert_heic_to_jpeg(in_file, out_file, quality=85)

    assert result == out_file
    assert out_file.exists()


def test_convert_rejects_non_heic_input(tmp_path: Path) -> None:
    in_file = tmp_path / "sample.jpg"
    in_file.write_bytes(b"jpg")
    with pytest.raises(ValueError):
        convert_heic_to_jpeg(in_file, tmp_path / "out.jpg")
