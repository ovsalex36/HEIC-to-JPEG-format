from __future__ import annotations

import argparse
from pathlib import Path

from .converter import convert_heic_to_jpeg, discover_heic_files, output_path_for


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heic-to-jpeg",
        description="Convert HEIC/HEIF images to JPEG format",
    )
    parser.add_argument("input", type=Path, help="Input HEIC/HEIF file or directory")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory where converted JPEG files are saved",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=90,
        help="JPEG quality from 1 to 100 (default: 90)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="When input is a directory, scan recursively",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing JPEG files",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.quality < 1 or args.quality > 100:
        parser.error("--quality must be between 1 and 100")

    files = discover_heic_files(args.input, recursive=args.recursive)
    if not files:
        print("No HEIC/HEIF files found.")
        return 1

    converted = 0
    for input_path in files:
        out_path = output_path_for(input_path, args.output_dir)
        try:
            convert_heic_to_jpeg(
                input_path,
                out_path,
                quality=args.quality,
                overwrite=args.overwrite,
            )
            converted += 1
            print(f"Converted: {input_path} -> {out_path}")
        except FileExistsError:
            print(f"Skipped (already exists): {out_path}")
        except Exception as exc:  # pragma: no cover - best effort reporting
            print(f"Failed to convert {input_path}: {exc}")

    print(f"Done. Converted {converted} file(s).")
    return 0 if converted > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
