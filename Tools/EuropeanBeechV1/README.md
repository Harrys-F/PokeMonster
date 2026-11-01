# European Beech Forest V1 – own map authoring

The forest is already saved in `/Game/Maps/Dev_TestMap_VisualV2`.
Enter it from the existing northern path around X=-3300/Y=2350 cm, then walk north.
The new area spans X=-7500..4500/Y=3000..15000 cm. No new map or gameplay system.

## Local licensed prerequisite

Import the owner's Fab European Beech pack at `/Game/Fab/EuropeanBeech` with its
`/Game/MSPresets/MS_Foliage_Material` dependencies. These original third-party files
are deliberately absent from this public repository. `AssetReferences.json` lists
actual required mesh paths. Never substitute unrelated assets or commit the Fab sources.
A fresh checkout alone cannot display these trees.

## Composition

`Layout.py` generates the owner's deterministic `Layout.json` and the owner's numeric
`Art/World/EuropeanBeechV1/PathMask.png`. It creates no tree/plant meshes. Existing
project assets supplement the imported trees with ferns, grass, moss, branches and stumps.

`Build.py` is a guarded one-time authoring operation for the clean baseline map before
this forest was added. It refuses an existing EBF1 group, PIE, unexpected dirty packages
or missing meshes. Do not run it again against the delivered map. It adds only EBF1
actors and three owned ground/path assets, checks all pre-existing actors, and saves
only its own assets and the target map. `Snapshot.py` audits transforms, mesh/material
references and instance transforms without exporting original mesh geometry.

For later manual changes, use the grouped HISM actors in the editor folder
`VisualV2/EuropeanBeechV1`: Edge, West, Inner and Deadwood. Keep the 280 cm path clear.
Do not modify the original Fab meshes/materials, old landscape or global camera/rendering.

Actual acceptance evidence and limitations: `Docs/EUROPEAN_BEECH_FOREST_V1.md`.
Heavy inventories, screenshots, test saves and logs stay under the ignored
`Saved/ProjectRefinement/EuropeanBeechV1/` directory.
