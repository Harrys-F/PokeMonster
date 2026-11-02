# VisualV2 Environment Polish V2

Bounded target-map tools, no runtime/gameplay architecture. Licensed originals
and imported Fab data remain in the already ignored local Fab root. Fresh clones
require the owner's licensed imports. No downloads or originals are distributed.

`Audit.py` records actual geometry and UTF-16 T3D actor references. `ImportFab.py`
imports only identified existing cache inputs, with custom project-owned material
graphs. The glTF mushroom collections contain multiple actual mesh variants.
Hydrangea A is the upright plant; B is a flat component and is not scaled as a shrub.

One-time authoring: `GeneratePathMask.py`, `ImportFab.py`, `Author.py`,
`RefinePaths.py`, `ClearBankView.py`. Do not replay authoring on the finished map.
The actual interrupted authoring/resume is retained under Saved; no user state
was reverted. `AuditFinal.py` verifies exact approved actor changes.

`RunNative.py` starts an owned isolated existing-map Development game, refuses
other active editors/games and never automatically kills them. `CaptureBenchmark`
uses the prior tested three-window noon methodology; it is a static paused-world
comparison, not a promise of moving 30 FPS. `GameplayReview` separately drives
real player input, AI, battle/capture, companion, isolated save/load and travel.
Existing V11 clock fixture only handles newly created isolated test slots.

`MapChecks.py` never saves maps. `RunAutomation.py` uses the full existing
PokeMonster Automation/strict zero-failure/warning report contract (325 minimum).
Media and raw results stay under Saved/ProjectRefinement/VisualV2EnvironmentPolishV2.
No physical controller test is claimed.

For visiting the six sites in ordinary VisualV2 PIE, retain the existing
`Tools/VisualV2FabAssetTrialV1/Visit.py` with AREA Blumenwiese, Waldrand, Flussufer,
Felsen, Dorf, Lebensraum, Bachbett, Kraeutergarten or Felsgruppe; Zurueck returns
to the original player/team anchor using the existing guarded preview service.

`RuntimeReference.py` and `PairedBenchmark.py` perform only disposable native
runtime reconstruction, not map authoring. Static references must be completed
before mesh assignment; assign explicitly visible components, verify transforms
and swap hidden states. `PairedSmoke.py` is a short visual preflight, never a
performance sample. Only NativePaired06 is the final paired comparison, parsed
by `AnalyzePaired.py`. Earlier incomplete fixtures remain evidence under Saved.
The paired test still shows drift and a measurable frame-cost increase; no
stable moving 30 FPS claim.
