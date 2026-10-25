#!/usr/bin/env python3
"""Report the overall envelope of an exported glTF/GLB scene in millimeters."""

import argparse
import json
from pathlib import Path

import trimesh


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Onshape GLB or glTF export")
    parser.add_argument("--output", type=Path, help="Optional JSON file")
    args = parser.parse_args()

    if not args.model.is_file():
        parser.error(f"model not found: {args.model}")
    if args.model.suffix.lower() not in {".glb", ".gltf"}:
        parser.error("expected a GLB or glTF file")

    scene = trimesh.load(args.model, force="scene")
    if not scene.geometry:
        parser.error("the exported scene contains no mesh geometry")

    bounds = scene.bounds * 1000.0  # glTF positions are meters.
    extent = bounds[1] - bounds[0]
    result = {
        "source": args.model.name,
        "unit_basis": "glTF meters converted to millimeters",
        "bounds_mm": [[round(float(v), 3) for v in row] for row in bounds],
        "envelope_mm": [round(float(v), 3) for v in extent],
        "note": "Overall exported-scene bounds, not a tolerance-controlled drawing.",
    }
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
