# Nintendo Switch Pro Controller V1 (macOS)

Uses the existing Enhanced Input actions, player controller, Reisebuch, dialogue and battle widgets. No new map, pawn, input subsystem or combat logic.

## Physical labels and backend

| Physical Switch control | Current Apple GameController backend UE key | Action |
|---|---|---|
| B | Gamepad_FaceButton_Right | Confirm / existing InteractAction |
| A | Gamepad_FaceButton_Bottom | Back / cancel |
| X | Gamepad_FaceButton_Left | Existing quick menu (Team / Bag) |
| L / R | Gamepad_LeftShoulder / Gamepad_RightShoulder | Previous / next of the two existing categories |
| + | Gamepad_Special_Right | Main page / resume |
| L3 | Gamepad_LeftThumbstick | Persistent sprint mode |
| Dpad | Gamepad_DPad_* | Selection and six-slot team sorting |
| Left stick | Existing Gamepad_Left2D radial mapping | Existing movement and optional Slate menu navigation |

B in battle was confirmed physically by Harry before this task. The running editor was read as `Slate.MacControllerPreferGCImpl=1`; local Unreal 5.8.2 AppleControllerInterface.cpp maps framework buttonB/buttonA/buttonX to Right/Bottom/Left. The legacy HID implementation maps physical B/A/X differently; the shared helper reads the existing backend CVar and follows that explicit mapping. No engine/backend setting is changed. macOS remapping/firmware and the other physical buttons still need user verification; software simulation is not that proof.

`pm.Input.Trace 1` shows/logs raw gamepad key-down events even when UMG owns focus. Disable with `pm.Input.Trace 0`. The observer never consumes events or assigns actions. `pm.Input.Key <UEKey> down|up|tap [repeat]` and `pm.Input.Axis <UEAxis> <value>` are development-only explicit simulations. Their log entries say `PM_INPUT_SIMULATED`; never count them as hardware evidence. For world actions hold down over at least one game tick, then release; a same-tick tap is useful only for immediate UI routing.

## Context and behaviour

- Existing world Enhanced Input: B interacts/challenges the selected valid target; X/Tab opens Team/Bag; +/Escape opens the Main page. No menu during battle/dialogue/defeat lock.
- Existing UMG owns focus while open. Preview handling consumes confirm/cancel before a focused Slate button can apply its generic accept layout. Repeated B/A/X/+ and shoulder events cannot perform repeated context changes. Dpad repeats remain available for navigation.
- B picks a team source and then any target slot; A first cancels that selection. Slot one remains the only companion source. Inventory B selects an existing usable healing item, then a team target; A cancels without consumption. The existing encounter/inventory APIs enforce valid targets, quantities and healing rules.
- + opens the Main page of the same Reisebuch widget: Team, Bag, Save, Resume. Save calls the existing save subsystem; no new schema or slot.
- L3 selects a mode even at rest. The mode survives stops, obstacles, menus, dialogue, battles and indoor pauses. Actual sprint requires movement, grounded state, outdoors and no lock. Walking/sprint speeds and Shift hold remain unchanged. The next L3 switches it off. The mode is transient, not written to the save schema.
- Keyboard/mouse bindings remain. Hints follow the most recent keyboard/gamepad input; battle text now correctly says B confirm / A back.

## Tests

Two C++ regressions under `PokeMonster.Input.SwitchPro`: mappings/persistent sprint and UMG contexts/repeat guards/item cancellation. Existing sprint/mapping-count assumptions are updated explicitly to the approved semantics. Existing inventory, party, save, wild encounter and battle tests remain required.

After a clean editor startup using the existing `Tools/ProjectMaintenance/ArtSession.py`:

```sh
python3 Tools/SwitchProControllerV1/RunProbe.py UniqueRunLabel
```

This runs **simulated Slate events in real PIE**. It uses the existing BattleV3 injured-party/item fixture and a separate StarterReview three-species fixture for the companion checks. These temporary parties are explicitly not the real saved team. It temporarily holds the actual developer save, then restores its exact bytes; do not save manually in parallel. On initialization failure it stops its own PIE and returns an untouched held original when no conflicting save exists. On timeout or unknown concurrent save it preserves the original for inspection instead of overwriting. Review the per-label result and restoration JSON under ignored `Saved/ProjectRefinement/`. The isolated NPC/wild cases use explicitly recorded diagnostic positioning; they are not a footrun. Run the separate existing complete walking route for that proof.

`MapChecks.py` loads/checks every existing map without saving. Evidence and screenshots stay under ignored Saved; only the sources and report belong in Git. See `Docs/NINTENDO_SWITCH_PRO_CONTROLLER_V1_PRUEFBERICHT.md` for actual results and open hardware checks.
