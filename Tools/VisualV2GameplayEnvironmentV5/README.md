# VisualV2 Gameplay & Environment V5

Only the existing VisualV2 map opts into the new features. No source models, original materials, rendering profiles or user saves are authoring targets.

- `Author.py`: apply once to the clean V4 map; existing NPC presentation profiles, route footprints, meadow groups, large barrier capsules, four existing EncounterZone actors and the local healer options. The script refuses an existing `GEV5_` actor rather than duplicating content.
- `EntranceClearance.py`: supplemental final pass over the old ground-level healing-house grass only, preserving window plants/garden props. Run after Author and StonePolish, before Audit and final captures.
- `StonePolish.py`: required final refinement; slender existing runestones fit inside the unchanged functional collision footprints. Does not move checkpoint/quest anchors.
- `Audit.py`: all original actors, world settings, five route footprints, four existing habitats, collision policy and asset references. Functional runestones intentionally retain their existing service positions; their new visual footprints are smaller than the original collision capsules.
- `FeatureReview.py`: actual local-player input, unchanged random chance, pause/dialogue suppression, normal capture, cooldown/travel budget, large shrub collision, all room walls, healing, speed 1/2/3 and isolated Save/Load. The healer is approached around the existing counter, not through it.
- `TrainerReview.py`: Liora's unchanged trainer profile through normal battle actions. `GameplayReview.py`: continuous 42-waypoint physical route plus battle/capture, companion, camera, cottage, bridge, save/load and real map travel.
- `Atlas.py`, `DetailViews.py`, `CaptureBenchmark.py`: real QHD captures and separately timed CSV samples. `Compare.swift` only arranges real images. `Analyze.py` reads recorded CSV counters; missing counters are never estimated.
- `LaunchEditor.py`, `RunNative.py`, `RunAutomation.py`: existing UE editor/development-game test methods with isolated storage; no automatic forced process termination. `MapChecks.py` reads all twelve existing maps and returns to VisualV2 without saving them.
- `VerifyProtection.py`: compare task-start tracked/untracked sources, local original assets, pre-existing saves and protected backup references. `FreshVerify.py`: freshly disk-loaded map and unchanged rendering/camera defaults.

Evidence goes to `Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/`. Use fresh unique run labels. `ArtControl.py start_pie` / `script <tool>` only addresses the already-owned clean editor queue. Never overwrite a user session or a previous test directory. PIE file-save tests opt into an isolated test slot before use; native runs use an isolated UserDir.

The central bush config is `Config/DefaultPokeMonsterBushEncounters.ini`. Per field, only enable `DistanceBasedBushEncounters` and reference a valid existing land `HabitatZoneId`; the existing habitat rule/profile and world clock select species/level/weight. `pm.BushEncounters.Enable -1` uses config, `0` disables and `1` enables for the session. `pm.BushEncounters.Debug 1` logs distance rolls and starts; restore `0` after diagnosis. No random encounter ID is persisted and no additional visible wild actor is spawned.

For reproduction: Editor Build via `Tools/ProjectMaintenance/ProjectQA.py <V5 label> Build`; full strict export via `RunAutomation.py <label> PokeMonster`. The existing strict contract requires engine exit 0, sufficient executed tests, no failed/notRun/inProcess tests and no succeededWithWarnings. Raw engine-startup/iOS messages are reviewed separately and are not described as a clean raw log.
