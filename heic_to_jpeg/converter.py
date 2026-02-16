from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = {".heic", ".heif"}
_HEIF_REGISTERED = False


def _open_image(path: Path):
    global _HEIF_REGISTERED
    from PIL import Image
    from pillow_heif import register_heif_opener

    if not _HEIF_REGISTERED:
        register_heif_opener()
        _HEIF_REGISTERED = True

    return Image.open(path)


def is_heic_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def output_path_for(input_path: Path, output_dir: Path | None = None) -> Path:
    target_dir = output_dir if output_dir is not None else input_path.parent
    return target_dir / f"{input_path.stem}.jpg"


def convert_heic_to_jpeg(
    input_path: Path,
    output_path: Path,
    *,
    quality: int = 90,
    overwrite: bool = False,
) -> Path:
    if not is_heic_file(input_path):
        raise ValueError(f"Not a HEIC/HEIF file: {input_path}")

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with _open_image(input_path) as img:
        rgb_img = img.convert("RGB")
        rgb_img.save(output_path, "JPEG", quality=quality, optimize=True)

    return output_path


def discover_heic_files(path: Path, recursive: bool = False) -> list[Path]:
    if is_heic_file(path):
        return [path]

    if path.is_dir():
        pattern = "**/*" if recursive else "*"
        return sorted(p for p in path.glob(pattern) if is_heic_file(p))

    return []
