# HEIC to JPEG Converter

A lightweight command-line application to convert Apple HEIC/HEIF images into JPEG format.

## Features

- Convert a single `.heic`/`.heif` file to `.jpg`
- Convert all HEIC files in a directory
- Optional recursive directory scanning
- Configurable JPEG quality
- Optional overwrite behavior

## Installation

Using `uv` (recommended):

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Usage

Convert a single file:

```bash
heic-to-jpeg ./photos/image.heic
```

Convert a directory:

```bash
heic-to-jpeg ./photos
```

Convert recursively and output to a separate directory:

```bash
heic-to-jpeg ./photos --recursive --output-dir ./converted
```

Set JPEG quality and overwrite existing files:

```bash
heic-to-jpeg ./photos -q 95 --overwrite
```

## Notes

This tool uses `pillow-heif` to read HEIC/HEIF files and `Pillow` to write JPEG output.
