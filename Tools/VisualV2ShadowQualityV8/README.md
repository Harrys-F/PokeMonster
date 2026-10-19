# Shadow Quality V8 – isolated investigation

No tool in this folder creates or saves a map. `PrepareMaterial.py` creates one unused experimental postprocess material. `RuntimeVariant.py` attaches a dynamic instance only to the current play-world copy of the existing outdoor volume. The existing map-specific TAA blendable remains. `StopPIE.py` cleans up temporary observers and material references before ending embedded PIE. No engine shader files are modified.

Parameters: `Art/World/VisualV2ShadowQualityV8/Variants.json`. A bypasses the experiment. B/C are visually calibrated targets, not VSM opacity settings. The scalar gain is not a claimed percentage. Masks use post-tonemap color/albedo ratio, world normal/height, exterior position, nearby contact points and known building footprints. AO was investigated but is not a reliable exclusive small-contact discriminator here; it is not part of the final mask.

Limitations: this is image-space floor shading, not access to the real VSM shadow factor. It cannot perfectly separate indirect-light variation or dark painted surfaces from cast shadows. Vertical walls and character skin are deliberately excluded. Up to 16 nearest contact points are protected, plus two existing building footprints. No claim of universal arbitrary-world contact protection. Interior is explicitly excluded. No automatic adoption or performance claim.

`Initialize.py` generates the local baseline and external map backup directly from the project; archived screenshots are never required for build or automation. Start the guarded editor with `LaunchEditor.py <new-label>` and prepare the separate asset only if it does not already exist.

`RunABC.py`: same QHD positions in embedded PIE; verifies the original scene afterward. `RunNativeABC.py`: same existing map in native -game mode, not cooked Shipping. `RunAcceptance.py PIE CandidateC 2560 1440 100`: existing complete input-driven route with dev-save protection. `RunMapCheck.py`, `RunQA.py Automation Automation`, `Build.py Build` require editor closed. `ValidateOriginal.py` verifies scene and all map hashes. Repeated evidence output names are refused to preserve earlier results.

`ComposeReview.py` requires Pillow/NumPy (bundled Codex Python). It only labels, equally resizes and crops real captures, and records the originals with SHA-256. ROI luminance measurements refer to output code values; they do not measure physical shadow occlusion or human perception exactly. All screenshots/logs stay in Saved or the external review directory and are excluded from Git.

See the final project report for actual results and decisions. The saved VisualV2 remains A until explicit visual approval.
