# VisualV2 Fab Asset Trial V1

Bounded, project-local authoring and QA tools for the existing VisualV2 map.
Production gameplay, camera, rendering profiles and all other maps are untouched.

Licensed inputs stay local. The seven exact Content roots listed in `.gitignore`
are intentionally excluded from the public repository. A fresh checkout needs
Harry's separately licensed imported packages and the cached/imported test inputs.
No automatic asset download, source replacement or placeholder generation occurs.

`Inventory.py` reads package/mesh/LOD/collision/material data. Initial asynchronous
texture sizes can be the engine's 32px placeholder. `Metadata.py` uses imported
`Dimensions` tags instead. `SceneBefore.json` and file hashes under the task's
Saved directory are local evidence, not a second project or asset backup.

Authoring scripts are one-time, ordered operations on the original recorded
map, not runtime initialization. Do not rerun them over the finished map:
`ImportGroundSources`, `Materials`, `ImportPlants`, `AuthorMap`, `Polish`,
`FinalCorrections`, `NormalizeGround`, `ClearWalkway`, `GardenProps`.
The full actual steps, intermediate corrections and final properties are in
`Docs/VISUALV2_FAB_ASSET_TRIAL_V1.md`. Originals are never saved by these tools.

`RunAutomation.py` reuses the existing full automation/strict report contract,
with isolated storage and no timeout kills. `MapChecks.py` checks exactly the
existing twelve project maps, without saving any of them.

`RunNative.py <unique-label> <script.py>` starts the existing project explicitly
on VisualV2 in an isolated Development `-game` process. It refuses to run while
another editor/game is active. `NativeBefore.py` reconstructs recorded original
bindings/positions only in disposable runtime memory. `CaptureBenchmark.py`
measures three fixed samples per main site and records real QHD stills after
sampling. `Analyze.py` reads Unreal's final CSV header and excludes metadata rows.
GPU pass ranges are not added together.

The existing `pm.WorldClock` command is PIE-only. Native controlled comparisons
use `ClockFixture.py`: a fresh task-owned V11 save is captured normally; only its
uniquely tagged SecondsOfDay double is changed, then the existing regular loader
restores it. Existing menu pause holds noon. This tool asserts the isolated path,
GVAS signature, unique tag/value and surrounding structure before every write.
It never handles a user slot. New save layouts fail these guards and require a
review, not an approximate patch. These frozen/menu-paused measurements are not
proof of regular gameplay FPS. `GameplayReview.py` separately tests active AI,
real movement, dialogue, battle/capture, companion, interiors, isolated Save/Load
and map travel.

PIE visits reuse the existing NPCGround RAM save preview and return anchor:

```text
py exec(open(r"/Users/harry/Developer/PokeMonster/Tools/VisualV2FabAssetTrialV1/Visit.py").read(), {"AREA":"Blumenwiese"})
```

Areas: `Blumenwiese`, `Waldrand`, `Flussufer`, `Felsen`, `Dorf`, `Lebensraum`.
Detail views: `Bachbett`, `Felsgruppe`, `Kraeutergarten`.
Return with the same command and `AREA="Zurueck"`. Use ordinary unlocked VisualV2
PIE and the existing Third Person camera. The original camera yaw is restored on
return; no new runtime console commands or C++ systems are introduced.

Control media and measurement data remain under
`Saved/ProjectRefinement/VisualV2FabAssetTrialV1/`; none are pushed.
