# QHD Performance Investigation V2

Independent experiment for `/Game/Maps/Dev_TestMap_EnvironmentPerfV2`. Original maps, assets and gameplay are inputs, never saved by these tools. No automatic adoption into VisualV2.

## Measurement

`pm.EnvPerf2.Run <absolute TSV>` is an explicitly invoked Development-only native probe. Plans declare warm-up, sample duration, sites, real renderer viewport size, scalability level and screen percentage. Each frame records renderer view extents, screen-percentage driver fractions, window extent/DPI/activation and camera pose. Internal pixel extents are calculated from the renderer fraction; they are not a GPU texture-allocation readback.

Baseline means EnvironmentPerfV1: integration downsample 2 and directional SMRT ray count 2. The chosen V2 candidate additionally sets `r.Lumen.FinalGatherMethod=0` and `r.Lumen.HardwareRayTracing=0`. Medium already uses final-gather 0 in this engine scalability configuration. Only the independent V2 map owns the persistent renderer scope; it restores its values on EndPlay.

`FinalPairedPIE.tsv` has 108 segments. `StandalonePair1` through `6` repeat the same paired matrix with the editor closed. Each configuration has Dorf/Wald/Weg and three adjacent Control/candidate pairs, with order reversed in repetition 2. Five seconds warm-up, six seconds measurement per segment. No screenshots, builds, concurrent Unreal instances or heavy postprocessing during timing.

`RunStandalone.py` uses the preserved V1 world in a native Development `-game` process, with the exact candidate selected transiently by the probe. This prevents a V2 map profile from contaminating the Control rows. This is not a packaged Shipping build. The engine records `-ResX/-ResY`, requested window mode, actual viewport, window size, fractions and frame-limit settings. Window extent and renderer extent may differ on macOS; do not describe a larger window as a measured larger renderer workload.

`PacingWindowed` and `PacingFullscreen` are separate pacing diagnostics, not optimization comparisons. macOS Metal may synchronize a windowed swap chain even with r.VSync=0. Do not count removal of a cap as a renderer gain.

`SustainedQHD` runs one native process continuously for about twelve minutes: nine segments, five seconds warm-up plus seventy-five seconds measurement, three rounds of the three sites. Compare rounds at the same site, not different sites. `ThermalMonitor.py` records NSProcessInfo thermal states; it does not measure temperature, clock speed or prove a throttling cause.

Use `Summarize.py`, `WriteTables.py` and `StrictValidation.py` after all graphics timing completes. Zero-valued RHI counters are unavailable, not zero draw calls. PIE RenderThread counters on this Mac are not reliable; report them unavailable. GPU event timings use coarse Metal stage counters, so a long leaf marker is not automatically a shader bottleneck.

## Editor and gameplay

Use the existing local Unreal MCP server. `RunInEditor.py <script> <observed Python textbox ref>` installs the guarded own-directory file queue via `PrepareEditor.py`. Use embedded PIE only. Never close a floating PIE window. `Control.py job <script>` sends a guarded script; `Control.py plans <label>` runs an existing plan. Never replay old jobs after editor restart.

`PersistCandidate.py` saves only the new map and refuses existing dirty packages or an existing V2 profile. `FootTest.py` drives Enhanced Input along the complete route; controlled benchmark/screenshot positioning is separate and is never counted as walking. Real building relocation and Save/Load are retained. Before touching the dev save, compare its SHA256 with the backed-up original. `RestoreDevSave.py` restores only the slot written by this completed test and preserves its result.

`FinalMapAudit.py` compares all pre-existing actor transforms/static meshes/materials/collision/instances against V1, expects only one new non-ticking, non-colliding profile actor, and invokes Map Check.

Close the editor cleanly before native measurements or full project automation. Reopen it with the explicit project and V2 map, not LaunchServices or the project browser. `FinalEditorCleanup.py` restores session-only editor settings, removes only this task’s callbacks and restores the original MCP port. No SaveAll, reset, restore, clean or commit operations.

## Rejected runs and complete replacements

The strict validation found foreground loss in the original QHD PIE block, changing native window sizes in StandalonePair1/2 and foreground loss in one High/100 Dorf row. These raw measurements are retained. Do not use the original `FinalPairedPIE` file alone as an approved foreground matrix.

The Development probe prepares a native game window’s requested size and brings it forward **before warm-up**, never during measurement. The editor main window is raised explicitly through the native UI before the repeat. `RepairPIEQHD` repeats all four QHD PIE configurations. `RepairNative1/2` repeat both full standard configurations. `RepairNativeHighDorf` repeats all three Dorf pairs for QHD High/100. No selection of individual favourable frames.

`ResolveMeasurements.py` writes `MeasurementsResolved.json` with explicit origin labels/segments and a `MeasurementSelection.json` exclusion record; the complete original `Measurements.json` remains available. `StrictValidation.py` validates the resolved 108+108 segments, three complete pairs per site/configuration, constant renderer extents/fractions/poses, an active window for every sample, and equal window extents in each pair. The twelve-minute sustained run has its own complete validation.
