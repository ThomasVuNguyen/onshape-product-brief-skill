# Onshape extraction

Read this when the model must be captured or exported through Onshape's UI.

## Confirm the assembly

- Use the exact document and element named by the user. Check the element title, workspace or version, configuration, and assembly tree before writing copy.
- A visible assembly may contain imported commercial parts, simplified models, suppressed components, or hidden instances. Describe the current visible state. Avoid treating every tree entry as a unique physical part or a validated component choice.
- Inspect a few views before selecting a hero. Onshape's default 3D view shortcuts are `Shift+1` front, `Shift+2` back, `Shift+3` left, `Shift+4` right, `Shift+5` top, `Shift+6` bottom, and `Shift+7` isometric. `f` fits the model. Let orientation settle before judging the fit; zoom manually if fit includes distant geometry. See [Onshape keyboard shortcuts](https://cad.onshape.com/help/Content/Home/keyboard_shortcuts_and_hotkeys.htm) and [view navigation](https://cad.onshape.com/help/Content/View/view_navigation_and_the_view_cube.htm).

## Export geometry

- Export the assembly to GLB when colored, tessellated geometry and bounds are sufficient. STEP or Parasolid can serve CAD-native downstream tools. Record export format, visible/hidden choice, and date.
- Large assembly exports can complete asynchronously. Watch Onshape's notification until it says the export completed. If a direct download is missed, "Store file in a new tab" creates a document tab with a Download button. Remove that temporary tab when appropriate and safe.
- glTF/GLB positions are in meters. `scripts/measure_glb.py` converts the resulting envelope to millimeters. Bounds describe the exported visible model, including any stray pins or distant geometry; compare them with orthographic views before printing dimensions.

## Capture views

- Clear selections, hover highlights, temporary measurements, and open dialogs. Position the complete model away from the view cube, side toolbar, and tab bar before taking a screenshot.
- Capture enough margin to retain silhouette and small protrusions. Crop the viewer UI away. Edge tracing can create a rectangular border at the crop edge; clear a few edge pixels and inspect the result.
- A browser screenshot is a reference image. A dimensioned production drawing needs actual tolerances, datums, and verified geometry. Label traced or screenshot-derived drawings as reference views.
