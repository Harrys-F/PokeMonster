# Environment Performance V3 — isolated investigation

Only the new V3 map and new V3 profiling/report files belong to this experiment. Existing files must not be saved or overwritten.

- `AuditInitial.py`, `CompareAndCopy.py`: verify dirty packages; compare live editor data with a safe reload; create a new map only if the target does not exist.
- `PrepareEditor.py`, `Queue.py`, `Control.py`, `MCPClient.py`: explicit local editor control; endpoint stored under Saved/EnvironmentPerfV3/Endpoint.json. Observe the Python console with Slate before using RunInEditor.py. No modal save/discard actions.
- `Plans/DiscoveryQHD.tsv`: 10 separate factors, 3 adjacent control/factor pairs each. Material show-flag is a whole-scene diagnostic, not a vegetation-only measurement.
- `Plans/NativeMatrix1..6.tsv`, `PIEMatrix1..6.tsv`: 3 sites × 3 paired repetitions × 6 configurations for both native Development -game and embedded PIE. A = actual V2 renderer values; B = TreeMinLOD1. Five-second warm-up, six-second sample; screenshots excluded.
- `NativeCulling.tsv`: current culling and one-factor FinalGather 0/1 follow-up. High/QHD100.
- `RunPIEPlans.py`: set quality BEFORE starting embedded PIE. Never switch High to Medium in a running PIE. Never close a floating PIE window.
- `RunStandalone.py`: editor closed; one native process per configuration. Not a packaged Shipping build. Requires successful build first.
- `ContinueMatrix.py`: sequential convenience helper. The first attempt paused safely while the reopened UI was still loading; wait until Slate shows the Python textbox, then resume with RunInEditor/RunPIEPlans. Do not rerun completed labels or overwrite evidence.
- `ValidateMeasurements.py`, `Summarize.py`, `MetricTables.py`: actual renderer extents/fractions, fixed poses, foreground state, complete repetitions and CSV counters. Zero unavailable counters are not valid cost measurements.
- `PersistControl.py`: RETAINS the V2 renderer state in V3. It deliberately does NOT adopt the unsuccessful minimum-LOD experiment. Only a new map-local profile actor is saved.
- `RunBaselineReviews.py`: genuine QHD screenshots from actual saved source maps, no source map saves. Animations paused only during images.
- `FootTest.py`: actual EnhancedInput walking plus existing interaction/presenter APIs; no test teleports. Genuine healing-house relocation is preserved. The guarded dev save backup is mandatory.
- `RestoreDevSave.py`: preserve the test result and restore only the guarded dev slot after a successful own test, with SHA checks.
- `AuditRuntimeMaterials.py`: after timing only; material statistics can finish shader compilation.
- `ProtectFinal.py`, `PackageEvidence.py`: after all timing; initial versionable file hashes must remain unchanged. Keep raw saves/engine startup logs in Saved; do not publish credentials or unrelated work.

The full conclusions and limitations are in Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md. No baseline adoption, commits or push are performed.
