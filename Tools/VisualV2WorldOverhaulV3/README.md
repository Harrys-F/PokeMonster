# VisualV2 World Overhaul V3

Only `/Game/Maps/Dev_TestMap_VisualV2` is authored. No gameplay/rendering profile edits. The two existing development presentation grounds are repositioned through their existing `Center()` constants; console registration, specimens and return logic stay intact.

## Authoring records

`Inventory.py` and `FinalAudit.py` are read-only. `Materials.py`, `Environment.py`, `Vegetation.py`, `Reground.py`, `FinalPolish.py`, `InstancingMaterials.py` and `WaterPolish.py` document the one-time authoring passes. **Do not rerun them on the completed map.** Their guards intentionally reject completed passes. `Reground.py` additionally requires the task-start evidence. Do not delete evidence to bypass guards. The saved map and own assets are the delivered state.

`Common.py` holds composition exclusions, the existing five path polylines, and six low smooth mounds. There is no new Landscape actor: the existing main ground is a static mesh, so the terrain is one project-owned derivative with integrated world-space surface masks, rather than overlaid normal path planes.

Fab sources remain local and unchanged. In particular, `M_WOV_ShrubMaster` contains a derivative of the imported StyleHex master and is intentionally ignored. The public repository receives only own map bindings, parameter instances, original project-made graphs/ground, tools and documentation, never the licensed master or raw Fab sources. A fresh checkout still needs the licensed local packages listed in the report.

## Reproduce checks

Use the existing guarded `Tools/ProjectMaintenance/ArtControl.py` only with an identified clean owned editor. `start_pie`, `script <path>`, `stop_pie`, `close` retain their existing behavior. Never close another user's session or discard dirty packages.

- `TestGroundCommands.py`: ordinary PIE console visits/returns. Its existing RAM preview intentionally cannot coexist with an isolated disk-save test slot; run it in its own fresh PIE session.
- `GameplayReview.py`: real Enhanced Input through all five existing path polylines (42 waypoints), bridge rail, cottage/healing-house entry/exit, dialogue, real wild encounter/action/capture, companion/team, isolated save/load, day/night and native map travel. Set `GameplayRequest.json` with a new label first. Do not claim physical controller testing.
- `Atlas.py`: 21 actual QHD camera views, matching `AtlasSites.json`. Set `Request.json` with a new label first. The slope viewpoint follows the modified ground; document its vertical camera delta.
- `RunNative.py <new_label> CaptureBenchmark.py`: fresh separate Development process, three 6s CSV samples at each of six positions plus three detail samples; pictures happen after samples, never video during timing. It refuses an existing editor/game and never kills on timeout.
- `RunNative.py <new_label> GameplayReview.py`: independent native real gameplay with isolated storage and actual map travel.
- `MapChecks.py`: all twelve existing maps read-only; returns to the initial map without saving others.
- `RunAutomation.py <new_label>`: all PokeMonster tests and strict exported-report contract (minimum 325, zero failures/warnings/not-run/in-process, engine exit0). Raw startup log issues are separately documented; report exit0 does not claim a warning-free engine log.
- Existing `Tools/ProjectMaintenance/ProjectQA.py VisualV2WorldOverhaulV3/<new_label> Build`: editor-closed build.
- `Analyze.py`, `VerifyProtection.py`: actual CSV/picture pairing and SHA256 protection checks against the initial evidence. Large media and raw data remain under Saved.
- `Compare.swift`: proportionate labelled layouts of real before/after screenshots, not synthesized images.

All native/editor launches use explicit VisualV2, task-specific UserDir, `-nowrite` and `-NoAssetRegistryCacheWrite`. No user saves are loaded/overwritten. Leave protected user configuration differences untouched.
