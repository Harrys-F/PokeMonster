# Environment Performance V1

Explicit, local development tools. No automatic gameplay changes. Original map and Ranger files are preserved. Evidence is written to ignored `Saved/EnvironmentPerfV1`; the final report is in `Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md`.

`PokeMonsterEnvironmentPerformanceProbe.cpp` registers `pm.EnvPerf.Run <absolute TSV>` and `pm.EnvPerf.Stop`. A plan header is `label<TAB>PIE|Standalone<TAB>warmup_seconds<TAB>measurement_seconds`. Each row is `site<TAB>condition<TAB>repeat<TAB>width<TAB>height<TAB>quality<TAB>percentage`. Quality 1=Medium, 2=High. The six required configurations and three repetitions are in `Plans/BaselinePIE.tsv`. Scoped factors restore component, volume and CVar values/priorities; no quality setting is persisted by the probe.

Sites (player capsule centre, cm): Dorf `(-4100,450,50.15)` is the actual healing-house forecourt; Wald `(-4300,1550,50.15)` is the dense north forest; Weg `(-36.6,-47.1,50.15)` is the open way. `NPCWald` is the original NPC forecourt `(-760,-1410,50.15)` and is not presented as the village. Camera settings are untouched.

Native wall-clock frame intervals are paired with engine CSV counters. `FSceneViewport::SetFixedViewportSize` forces the actual game output; window extent, viewport and render target are logged separately. A render-thread observer reads the percentage driver's upper bound with dynamic resolution disabled. The internal image dimensions are **derived** with UE 5.8's ceil rule; they are not a direct SceneColor allocation readback. Allocation padding and individual pass resolutions are not measured. `Summarize.py` reads the final dynamic CSV header and keeps per-run values, P95, camera and extent validation. Zero DrawCall/RHI/PIE RenderThread values are not treated as reliable zero costs. GPU pass times can overlap.

Local editor commands use the existing MCP server and Slate's observed Python console. `PrepareEditor.py` installs a bounded-path job queue; `Control.py job <script>` dispatches only scripts in this directory. Use embedded PIE only. Never close a floating PIE window. No `SaveAll` and no automatic cleanup of foreign dirty packages.

Profiling positions are controlled placements, not a walking test. `FootTest.py` separately uses actual Enhanced Input locomotion and the existing building relocation. Back up the real dev save before running and restore it byte-for-byte afterward.

Do not run Blender renders, builds, hashing or other heavy processes concurrently with benchmarks. Monitor time drift and macOS thermal state; a nominal/fair label does not measure actual clock frequency or degrees Celsius. Use adjacent control/variant pairs with reversed order, not distant before/after blocks as sole causal evidence.
