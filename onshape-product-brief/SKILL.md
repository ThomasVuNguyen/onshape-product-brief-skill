---
name: onshape-product-brief
description: Create a polished, concise product brief PDF from an Onshape assembly or part studio. Use when the user wants CAD-derived product storytelling, specifications, and drawings in a designed document.
---

# Onshape product brief

Turn the selected Onshape model into a short, credible PDF that can be reviewed as both a product story and a visual artifact. Adapt the page count and style to the product and the user's reference. A sample brief may help calibrate quality, but it is not a fixed template.

## Workflow

1. **Establish the source.** Open the exact document and element the user names. Record the document URL, workspace or version, configuration, capture date, visible/hidden state, and assembly status. Inspect the model in isometric and orthographic views, its tree and properties. If the intended product is unclear, make progress from visible geometry and ask one focused question about use or audience.

2. **Collect evidence.** Capture clean hero, top, front, and side views that show the complete model. Export the selected visible assembly when geometry is needed. Prefer an existing authenticated Onshape session; use new API credentials only when necessary and authorized. Read [Onshape extraction](references/onshape-extraction.md) for export, view, and capture details. `scripts/measure_glb.py` reports the exported model's overall envelope in millimeters. Treat that envelope as a CAD measurement, not a manufacturing dimension.

3. **Write a claim ledger.** For each proposed statement, identify whether it is directly shown in the model, derived from exported geometry, an interpretation, or unverified. Use direct and derived facts in the specification with their basis. Label interpretive language as a concept description. Omit performance, material, compatibility, safety, production, and tolerance claims without source evidence. An imported instance count is not a bill of materials.

4. **Set the visual direction.** If the user provides a reference PDF, study its page rhythm, amount of copy, drawing style, typography, and opening/closing treatment. Build a distinct identity from the product's physical colors and form; reuse the reference's design principles without copying its branding. Plan only pages supported by the evidence. A cover, concise overview, compact specification, drawing-led middle, and quiet closing page are a useful starting rhythm.

5. **Make the artifact.** Create clean cutouts or line drawings from CAD views; `scripts/cad_image.py` can remove a white viewer background and trace edges. Keep viewer controls and crop borders out of the artwork. Set a deliberate type scale, margins, and limited palette. Use the strongest view as a hero, keep prose short, and give drawings enough size to read. Include the Onshape source and date. Put a reference-only note beside CAD-derived dimensions when no tolerances are verified.

6. **Review the rendered PDF.** Render every page to images and inspect at normal reading size. Check spacing, typography, contrast, alignment, page fit, and repetition, then fix each visible defect. Check that every dimension and component claim still matches the source, that no UI artifact or clipped geometry remains, and that the opening and closing pages feel intentional. Deliver the PDF and briefly state the provenance and remaining unknowns.

The source document and any requested external publication have separate authorization boundaries. Before publishing a brief or repository, review the exact files for credentials, private CAD exports, third-party reference PDFs, and other material the user did not intend to share.

## Helpers

Install `Pillow` and `trimesh` when using the helpers. The scripts accept explicit input and output paths; use `--help` for arguments. When this skill is used from its source repository, the example's `build_brief.py` is a complete ReportLab source file for studying layout choices and reproducing its PDF.
