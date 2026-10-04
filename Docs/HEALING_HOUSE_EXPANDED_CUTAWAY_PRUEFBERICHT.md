# Healing House Expanded Interior – Cutaway-Prüfbericht

Prüfung: 2026-10-04. Ausgangs-HEAD: `8c9965a Add expanded healing house interior`. Anfangs `git status --short` ohne Ausgabe. Der bestehende Prototyp wurde nicht neu gebaut.

## Umfang und Ergebnis

Nur die explizite Occluder-Liste von `HouseCutaway` in `Dev_HealingHouseTestMap` wurde angepasst. **118 → 107 Referenzen**, elf Seitenbauteile entfernt. Die beiden Seitenwände und die Rückwand des Expanded Interior waren bereits nicht registriert; die Änderung bereinigt die zusätzlich geerbte Liste des äußeren Heilhauses. Das ist keine nachträgliche Behauptung, zuvor seien sämtliche Expanded-Seitenwände ausgeblendet gewesen.

Im ausgelagerten Raum bleiben zehn Seitenwandmodule und sechs Rückwandmodule samt jeweils zugehörigen Balken sichtbar. Nur sechs Front-/Türteile verschwinden. Das offene Oberteil des bestehenden Raums wird nicht verändert; die Dachteile der Außenhülle bleiben in der Liste. Die 101 übrigen Referenzen sind äußere Dach-/Frontteile einschließlich Giebel, Tür-/Fensterteilen, Kamin-/Dachanbauten und Frontdeko. Teilweise gehören sie zu weiterhin deaktivierten Blockout-/V1-Versionen. Das Entfernen ihrer Seitenreferenzen reaktiviert diese Altversionen nicht.

## Entfernte Seitenbauteile

Diese elf Referenzen waren vor der Korrektur in der Liste und sind danach keine Occluder mehr:

- `CameraSideWall`
- `HH_Walls_CameraSide`
- `HH_Timber_CameraSide`
- `HH_WindowFrames_CameraSide`
- `HH_Glass_CameraSide`
- `HH_V2_Walls_CameraSide`
- `HH_V2_Glass_CameraSide`
- `HH_V2_Windows_CameraSide`
- `HH_V2_Timber_CameraSide`
- `HH_V2_Stone_CameraSide`
- `HH_V2_InteriorBeams_CameraSide`

## Unveränderte Parameter und Systeme

- Raum 12 × 10 m; alle 337 Actors erhalten.
- Innenkamera 2600 cm, FOV 35°, Pitch −50°, lokaler Yaw 0°; Fokus (19940,0,80) cm.
- Außenkamera 2500 cm, FOV 35°, Pitch −55°, Yaw −45°; Lag unverändert.
- Player 140 cm, 210 cm/s, acht Richtungen, Sprite-Skalierung/Pivots und Interaktionsreichweite unverändert.
- Relocation über parallele Türschwellen mit 19950-cm-Ortsversatz, 0,4-s-Cutaway und bestehender Übergangsmaske unverändert.
- Heilerin, Einrichtung, Healing, RestPoint, Checkpoint, Save, Quest und Battle unverändert.
- Außenheilhaus-Geometrie, Wohnhaus, Gasthaus, Village und `Dev_TestMap` unverändert.

Vorher-/Nachher-Audit aller 337 Actors: Position, Rotation, Skalierung, Mesh, Materialien, Collision, Sichtbarkeit und erfasste Kamera-/Cutaway-Einstellungen gleich; einzig `HouseCutaway.occluding_actors` unterscheidet sich. Zusätzlich werden unveränderte Dateien gegen die SHA-256-Ausgangsliste geprüft.

## PIE-Fußlauf und Sichtprüfung

Normaler PIE mit regulärem PlayerStart, keine Spawn-Overrides und keine Test-Teleports. `TestHealingHouseExpandedCutawayPIE.py` bewegt ausschließlich über die vorhandene Enhanced-Input-Aktion, in acht normalisierten Bewegungssektoren. Die systemeigene Tür-Relocation bleibt natürlich aktiv.

1. Außenstart und gerade durch den Eingang.
2. Vordere, mittlere und hintere Bereiche an der Seitenwand Y=−600 cm, Laufspur ungefähr Y=−540 cm.
3. Rückwand X=20500 cm, Laufspur ungefähr X=20450 cm; bestehendes Kamin-/Sitzeckenmobiliar über vorhandene freie Gänge umgehen.
4. Hinterer, mittlerer und vorderer Bereich an der Seitenwand Y=+600 cm, Laufspur ungefähr Y=+540 cm.
5. Hauptfläche und seitlicher Zugang zur Heilerin; reguläre Interaktion und Dialog.
6. Gerade hinaus, erneut diagonal hinein, diagonal hinaus, Rückkehr zum Vorplatz.

**Bestanden:** 55 Prüfschritte, zwei vollständige Ein-/Austrittsrunden, keine Fehler, Maximalgeschwindigkeit 210 cm/s. 16 Aufnahmen der tatsächlich gerenderten Spielkamera wurden geprüft. Der Player ist in den geprüften Randbereichen erkennbar; Seiten-/Rückwände verdecken ihn nicht störend. Front- und Türteile sind innen vollständig ausgeblendet, außen korrekt wiederhergestellt. Keine falschen Seiten-/Rückwandteile verschwinden. Keine zusätzliche Wand-Ausnahme erforderlich.

Die Kameraposition wechselt gemeinsam mit der Figur unter der bestehenden vollständig schwarzen Maske; kein sichtbarer Flug über die räumliche Trennung. Die instrumentierten Ortswechsel erhalten Seiten-/Bodenoffsets innerhalb des normalen Bewegungswegs, Innenbewegungsbasis 0° und Außenbasis −45°. Kameraparameter bleiben unverändert. Heilerdialog, volle HP/PP, Checkpoint-ID `Dev_HealingHouse` und regulärer Save-Aufruf bestätigt. Dieser Lauf erzeugte keine absichtliche HP/PP-Depletion; Heilung geschädigter Teams und Save-Fehlerpfade werden weiterhin von den Automationstests abgedeckt. Der zuvor vorhandene persönliche Dev-Spielstand wird nach der Prüfung bytegleich wiederhergestellt.

## Build, Automation und Map Check

Erster Lauf: 37/38 erfolgreich. Der alte Layout-Test verlangte `HH_Walls_CameraSide` ausdrücklich als Occluder und widersprach der neuen Vorgabe. Diese Erwartung wurde ersetzt: alte Seitenfassaden sind ausgeschlossen; alle 16 Expanded-Seiten-/Rückwandmodule bleiben sichtbar; sechs Front-/Türteile sind registriert.

Nur `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp` geändert, kein Gameplay-C++. Mac Development Editor-Build erfolgreich (23,56 s, maximal zwei parallele Aktionen). Neuer Editorprozess lädt die aktualisierte Testbibliothek. **38/38 PokeMonster-Automationstests erfolgreich**, einschließlich HealingHouse Layout/Collision/Rest, RelocatedInterior MappingAndTransition, Player Foundation/ScaleCalibration/BuildingInteriorCamera, Inn, Save/Checkpoint, Quest und Battle. Map Check: **0 Fehler / 0 Warnungen**.

Evidence bleibt unversioniert in `Saved/HealingCutaway`: `Occluders.json`, `MapAudit` im bisherigen `Saved/HealingExpanded/MapAudit.json`, `Preservation.json`, `Frames.jsonl`, `PIERoute.json` und 16 Reviewbilder. Editor-/Buildlogs und temporäre Brücke liegen außerhalb des Repositories in `/private/tmp/HealingCutaway`.

## Geänderte/neue Projektdateien

- `Content/Maps/Dev_HealingHouseTestMap.umap`
- `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp`
- `Tools/BuildHealingHouseExpandedInterior.py` – spätere Reproduktion verwendet dieselbe explizite Liste; hier nicht ausgeführt.
- `Tools/ValidateHealingHouseExpandedInterior.py`
- `Tools/ConfigureHealingHouseExpandedCutaway.py` (neu)
- `Tools/TestHealingHouseExpandedCutawayPIE.py` (neu)
- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/HEALING_HOUSE_EXPANDED_CUTAWAY_PRUEFBERICHT.md` (neu)

Keine neuen Kunstassets, Blender-/FBX-Dateien oder Features. Nichts gestaged, kein Commit und kein Push. `git diff --check` erfolgreich, keine Ausgabe. `git status --short`: sechs bestehende Dateien geändert, drei neue Dateien; kein Staging. 667 andere Ausgangsdateien sind SHA-256-bytegleich. Der persönliche Dev-Spielstand wurde bytegleich wiederhergestellt. Sinnvoller Sicherungspunkt nach Harrys Sichtprüfung: ausschließlich diese neun Dateien aufnehmen; die temporären Prüfnachweise bleiben außerhalb von Git.

## Editor-Arbeitsumgebung

Die native MCP-Verbindung war im bereits geöffneten Benutzereditor nicht aktiv. Authoring, PIE und Tests wurden deshalb in einem separaten vollständigen Unreal-Testeditor durchgeführt, der anschließend geschlossen wurde. Der Benutzereditor bleibt geöffnet und enthält noch seine zuvor geladene Map-Kopie; diese vor Weiterarbeit neu laden.

Bei einem erfolglosen Fokusversuch für die Pythonkonsole wurde `Ground` im Benutzereditor vorübergehend in der Editoransicht verborgen. Das wurde nicht gespeichert und betrifft weder die geprüfte Map-Datei noch die PIE-Bodencollision. Der inzwischen gesperrte Mac verhindert die UI-Rückstellung; ein Neuladen von `Dev_HealingHouseTestMap` stellt den gespeicherten sichtbaren Boden und die neue Occluder-Liste her. Harry wurde um Entsperren gebeten.

## Empfohlener späterer Sicherungspunkt

Erst nach Harrys Sichtprüfung; hier wurde der Befehl nicht ausgeführt:

```sh
git add -- Content/Maps/Dev_HealingHouseTestMap.umap Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp Tools/BuildHealingHouseExpandedInterior.py Tools/ValidateHealingHouseExpandedInterior.py Tools/ConfigureHealingHouseExpandedCutaway.py Tools/TestHealingHouseExpandedCutawayPIE.py Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/HEALING_HOUSE_EXPANDED_CUTAWAY_PRUEFBERICHT.md
```

## Vollständige tatsächlich konfigurierte Occluder-Liste nach der Änderung

Die ersten 101 Einträge stammen aus der bestehenden Außen-/Legacy-Liste, die letzten sechs aus der kameraseitigen Front des ausgelagerten Raums:

- `EntranceWall_-310`
- `EntranceWall_310`
- `DoorLintel`
- `DoorPost_-135`
- `DoorPost_135`
- `DoorBeam`
- `Roof_-260`
- `Roof_260`
- `Ridge`
- `FrontWindow_-315`
- `FrontWindowFrame_-315_-57`
- `FrontWindowFrame_-315_57`
- `FrontWindowSill_-315`
- `FrontWindow_315`
- `FrontWindowFrame_315_-57`
- `FrontWindowFrame_315_57`
- `FrontWindowSill_315`
- `HH_Walls_Front`
- `HH_Gable_Front`
- `HH_Roof_Main`
- `HH_Roof_Porch`
- `HH_Timber_Front`
- `HH_DoorFrame`
- `HH_WindowFrames_Front`
- `HH_Glass_Front`
- `HH_Chimney`
- `HH_ChimneyCap`
- `HH_V2_Walls_Front`
- `HH_V2_Gable_Front`
- `HH_V2_Glass_Front`
- `HH_V2_Glass_Loft`
- `HH_V2_Windows_Front`
- `HH_V2_Windows_Loft`
- `HH_V2_Roof_Main`
- `HH_V2_Roof_Trim`
- `HH_V2_Roof_Porch`
- `HH_V2_Roof_Entry`
- `HH_V2_Timber_Front`
- `HH_V2_Timber_Entry`
- `HH_V2_DoorFrame`
- `HH_V2_DoorLeaf`
- `HH_V2_Stone_Front`
- `HH_V2_Chimney`
- `HH_V2_ChimneyCap`
- `HH_V3_SignBracket`
- `HH_V3_GuardianSign`
- `HH_V3_Lantern`
- `HH_V3_WindowBox_-1`
- `HH_V3_WindowBoxSoil_-1`
- `HH_V3_WindowHerb_-1_0_Pot`
- `HH_V3_WindowHerb_-1_0_Leaf0`
- `HH_V3_WindowHerb_-1_0_Leaf1`
- `HH_V3_WindowHerb_-1_0_Leaf2`
- `HH_V3_WindowHerb_-1_0_Flower`
- `HH_V3_WindowHerb_-1_1_Pot`
- `HH_V3_WindowHerb_-1_1_Leaf0`
- `HH_V3_WindowHerb_-1_1_Leaf1`
- `HH_V3_WindowHerb_-1_1_Leaf2`
- `HH_V3_WindowHerb_-1_2_Pot`
- `HH_V3_WindowHerb_-1_2_Leaf0`
- `HH_V3_WindowHerb_-1_2_Leaf1`
- `HH_V3_WindowHerb_-1_2_Leaf2`
- `HH_V3_WindowHerb_-1_2_Flower`
- `HH_V3_WindowHerb_-1_3_Pot`
- `HH_V3_WindowHerb_-1_3_Leaf0`
- `HH_V3_WindowHerb_-1_3_Leaf1`
- `HH_V3_WindowHerb_-1_3_Leaf2`
- `HH_V3_Ivy_-1_0`
- `HH_V3_Ivy_-1_1`
- `HH_V3_Ivy_-1_2`
- `HH_V3_Ivy_-1_3`
- `HH_V3_Ivy_-1_4`
- `HH_V3_Ivy_-1_5`
- `HH_V3_Ivy_-1_6`
- `HH_V3_WindowBox_1`
- `HH_V3_WindowBoxSoil_1`
- `HH_V3_WindowHerb_1_0_Pot`
- `HH_V3_WindowHerb_1_0_Leaf0`
- `HH_V3_WindowHerb_1_0_Leaf1`
- `HH_V3_WindowHerb_1_0_Leaf2`
- `HH_V3_WindowHerb_1_0_Flower`
- `HH_V3_WindowHerb_1_1_Pot`
- `HH_V3_WindowHerb_1_1_Leaf0`
- `HH_V3_WindowHerb_1_1_Leaf1`
- `HH_V3_WindowHerb_1_1_Leaf2`
- `HH_V3_WindowHerb_1_2_Pot`
- `HH_V3_WindowHerb_1_2_Leaf0`
- `HH_V3_WindowHerb_1_2_Leaf1`
- `HH_V3_WindowHerb_1_2_Leaf2`
- `HH_V3_WindowHerb_1_2_Flower`
- `HH_V3_WindowHerb_1_3_Pot`
- `HH_V3_WindowHerb_1_3_Leaf0`
- `HH_V3_WindowHerb_1_3_Leaf1`
- `HH_V3_WindowHerb_1_3_Leaf2`
- `HH_V3_Ivy_1_0`
- `HH_V3_Ivy_1_1`
- `HH_V3_Ivy_1_2`
- `HH_V3_Ivy_1_3`
- `HH_V3_Ivy_1_4`
- `HH_V3_Ivy_1_5`
- `HH_V3_Ivy_1_6`
- `HH_Expanded_FrontWall_-1`
- `HH_Expanded_DoorPost_-1`
- `HH_Expanded_FrontWall_1`
- `HH_Expanded_DoorPost_1`
- `HH_Expanded_DoorLintel`
- `HH_Expanded_DoorBeam`
