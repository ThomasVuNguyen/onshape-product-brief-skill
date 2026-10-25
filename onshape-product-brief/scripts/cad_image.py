#!/usr/bin/env python3
"""Create a transparent CAD cutout and/or line trace from a clean screenshot."""

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


def bounds(value):
    try:
        result = tuple(int(part) for part in value.split(","))
        if len(result) != 4 or result[0] >= result[2] or result[1] >= result[3]:
            raise ValueError
        return result
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use x0,y0,x1,y1 with increasing bounds") from exc


def hex_color(value):
    if len(value) != 7 or not value.startswith("#"):
        raise argparse.ArgumentTypeError("use a six-digit hex color, such as #FFFFFF")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid hex color") from exc


def save_cutout(image, output):
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, _ = pixels[x, y]
            difference = 255 - min(r, g, b)
            alpha = max(0, min(255, (difference - 8) * 6))
            pixels[x, y] = (r, g, b, alpha)
    output.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(output)


def save_trace(image, output, color, scale, threshold, clear_border):
    enlarged = image.resize(
        (image.width * scale, image.height * scale), Image.Resampling.LANCZOS
    )
    edge = enlarged.convert("L").filter(ImageFilter.FIND_EDGES)
    edge = edge.filter(ImageFilter.GaussianBlur(0.35))
    alpha = edge.point(lambda value: min(255, max(0, (value - threshold) * 9)))
    if clear_border:
        p = alpha.load()
        border = clear_border * scale
        for y in range(alpha.height):
            for x in range(alpha.width):
                if x < border or y < border or x >= alpha.width - border or y >= alpha.height - border:
                    p[x, y] = 0
    trace = Image.new("RGBA", edge.size, color + (0,))
    trace.putalpha(alpha)
    output.parent.mkdir(parents=True, exist_ok=True)
    trace.save(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Screenshot with a white CAD background")
    parser.add_argument("--crop", type=bounds, required=True, help="x0,y0,x1,y1")
    parser.add_argument("--erase", type=bounds, action="append", default=[], help="UI rectangle relative to the crop; repeat as needed")
    parser.add_argument("--color-output", type=Path, help="Transparent shaded cutout PNG")
    parser.add_argument("--line-output", type=Path, help="Transparent line drawing PNG")
    parser.add_argument("--line-color", type=hex_color, default=(34, 39, 46))
    parser.add_argument("--scale", type=int, default=3, help="Line drawing enlargement, default 3")
    parser.add_argument("--edge-threshold", type=int, default=15)
    parser.add_argument("--clear-border", type=int, default=7, help="Crop-edge pixels to clear, default 7")
    args = parser.parse_args()

    if not args.color_output and not args.line_output:
        parser.error("request --color-output, --line-output, or both")
    if args.scale < 1 or args.clear_border < 0 or not 0 <= args.edge_threshold <= 255:
        parser.error("scale must be positive; border and threshold must be valid")
    if not args.input.is_file():
        parser.error(f"image not found: {args.input}")

    source = Image.open(args.input).convert("RGB")
    x0, y0, x1, y1 = args.crop
    if x0 < 0 or y0 < 0 or x1 > source.width or y1 > source.height:
        parser.error("crop extends beyond the image")
    image = source.crop(args.crop)
    for rectangle in args.erase:
        image.paste("white", rectangle)

    if args.color_output:
        save_cutout(image, args.color_output)
        print(args.color_output)
    if args.line_output:
        save_trace(image, args.line_output, args.line_color, args.scale, args.edge_threshold, args.clear_border)
        print(args.line_output)


if __name__ == "__main__":
    main()
