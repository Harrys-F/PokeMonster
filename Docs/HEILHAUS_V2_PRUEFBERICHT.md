# Healing House V2 – Architectural Art Pass

Dieser Bericht dokumentiert den Architekturstand **vor** dem anschließenden Proportions-Pass. Aktuelle Tür-/Hausmaße, Map-Anpassungen und Tests stehen in [HEILHAUS_V2_PROPORTIONEN.md](HEILHAUS_V2_PROPORTIONEN.md).

Stand: 2026-10-02. Ausgangs-HEAD: `8705b16 Refine camera and healing house cutaway`.
Der Arbeitsbaum war vor Beginn sauber. Kein Commit, kein Push.

## Quelle, Export und Maße

- Neue eigenständige Quelle: `Art/HealingHouse/Source/HealingHouse_V2.blend`.
- Gebäudeexport: `Art/HealingHouse/Exports/HealingHouse_V2.fbx`.
- Fensterbibliothek: `Art/HealingHouse/Exports/HealingHouse_V2_WindowModules.fbx`.
- V1-Quelle und V1-FBX bleiben bytegleich zum HEAD erhalten.
- Hauptkörper weiterhin **10,30 × 9,30 m**; Wandmittellinien Unreal X ±4,50 m / Y ±5,00 m.
- Dachfirst weiterhin **6,40 m**; Kaminoberkante **7,02 m**; Fußbodenoberkante **0,00 m**.
- Freie Hauptpassage weiterhin **2,40 × 2,30 m**, ohne Türschwellenstufe.
- Tatsächlicher Gesamtmesh-Umfang einschließlich kräftiger Dachkanten, offenem Türblatt und Vorbaustützen: **12,35 × 10,625 m** (Breite × Tiefe). Die größere Tiefe entsteht hauptsächlich durch das nach außen geöffnete Türblatt; der begehbare Grundkörper und seine Collision ändern sich nicht.
- Gebäude: **39 Module, 15.256 Dreiecke**. Zusätzliche, nicht in der Map platzierte Fensterbibliothek: **3 Module, 2.308 Dreiecke**. Zusammen exportiert: **17.564 Dreiecke**.
- Positive Volumina. Die V2-Quelle enthält bei den zwei Innenbalkenmodulen jeweils **8 bereits vorhandene nicht-manifold Kanten**; die frühere pauschale Aussage „0“ war falsch. Der anschließende Proportions-Pass erhält die Topologie unverändert. Die übrigen Module und die Fensterbibliothek haben 0 nicht-manifold Kanten. Gemeinsamer angewandter Gebäudeursprung, Metermaßstab, Unreal-Importfaktor 1.

## Architektur

| Bereich | V2-Ausführung |
| --- | --- |
| Dach | Gebrochene, leicht ausgeschweifte Fantasy-Dachprofile; 18 cm dicke Hauptdach-Solids; kräftige 27–30 cm Trauf-/Ortgangbalken und Überstände. Hauptdach, Dachrand, Eingangsdach und Vorbaudach bleiben getrennt ausblendbar. Schindeln sind eine selbst erzeugte Textur, keine einzeln modellierten Ziegel. |
| Fachwerk | 24–28 cm Eck-/Rahmenbalken, klare horizontale Riegel, ausgewählte 20–22 cm Diagonalstreben und Giebelpfosten. Das runde Giebelfenster wird vom Pfosten ausgespart. |
| Putz / Stein | Heller warmer Putz, unregelmäßiger zweireihiger Feldsteinsockel mit abgeschwächten Kanten, Steinsolbank und punktueller Innen-Steinsockel. |
| Eingang | Steineinfassung, Holzrahmen, eigenes kleines Giebeldach mit sichtbaren Balken; fest offen dargestelltes Holz-Türblatt mit zwei dezenten Metallbändern. Türblatt liegt außerhalb der freien Passage. Platz für spätere Laterne und eigenes Hüter-Symbol bleibt frei; kein neues Türsystem und kein finales Schild. |
| Fenster | Drei Formen: Bogenfenster, abgeschrägtes Doppelfenster, rundes Giebelfenster. Kräftige Holzrahmen, breite Sohlbänke und warmes Glas mit zurückhaltender Emission. Zwei Bogen-, vier Doppel- und ein Rundfenster sind in echten Wandöffnungen eingesetzt. |
| Fensterbibliothek | `SM_HH_V2_WindowModule_Arch`, `_Twin`, `_Round`: jeweils Rahmen und Glas, eigener lokaler Pivot an Wandebene / horizontaler Mitte / Sohlbank, lokale Außenseite −X. Eigenständig wiederverwendbar; die Bibliotheks-Collection in Blender ist ausgeblendet und wird nicht zusätzlich in der Map platziert. |
| Kamin | Naturstein-Schaft mit kräftigerem Mauerabschluss und dunkler Deckplatte; in das Dach eingebunden. Kein Rauch oder VFX. |
| Vorbau | Angeschlossenes eigenes Dach, dickere Holzstützen auf Steinsockeln, Kopfbänder und Querträger. Fläche für spätere Kräuter-/Versorgungsnutzung frei von neuen Props. |
| Innenarchitektur | Texturierter Holzfußboden, Wand-/Randbalken, Kopfbänder und punktueller Naturstein. Kameraseitiger Innenbalken ist ein eigener Cutaway-Teil. Zentraler Weg und diagonale Wege bleiben frei. Behandlungs-, Warte- und Versorgungsbereiche sind im Geometrie-Audit reserviert. Vorhandene V1-Möbel bleiben erhalten; keine neuen Detail-Liegen, Regale oder Dekorationssets. |
| Tresen | Holzflächen mit ruhigem Rahmen-/Paneelaufbau und leicht abgeschwächten Kanten. Weiterhin 92 cm Oberkante und 173 cm vorderste X-Kante; identischer vorhandener Blocker. Player und Hüterin sind in der Spielansicht sichtbar. Die Höhe ist auch als niedriger Versorgungstresen für größere Humanoide plausibel. |

## Materialien und Unreal-Integration

Sieben neue Material-/Texturpaare: **Plaster, Wood, Timber, Stone, Roof, Metal, Glass**.
Eigenständig erzeugte, reproduzierbare Farb-/Strukturtexturen ohne Downloads; Dach 1024²,
übrige Texturen 512². Keine photorealistischen Normal-/PBR-Sets. Hohe Roughness,
reduzierter Specular-Anteil und zurückhaltende Glas-Emission.

Alle V2-Assets liegen in der vorhandenen Struktur:

- `/Game/Environment/HealingHouse/Meshes/SM_HH_V2_*` – **42 Meshes**, davon 39 Gebäudeteile und 3 Bibliotheksfenster.
- `/Game/Environment/HealingHouse/Materials/M_HH_V2_*` – **7 Materialien**.
- `/Game/Environment/HealingHouse/Textures/T_HH_V2_*` – **7 Texturen**.

Damit **56 neue Unreal-Assets**. Die V1-Assets werden nicht überschrieben.
Die 24 V1-Mesh-Actors bleiben als unsichtbare Rückfallhülle erhalten.
Nur `Dev_HealingHouseTestMap` wird gespeichert; `Dev_TestMap` ist bytegleich zum HEAD.
Import-Bounds wurden gegen Blender in Zentimetern geprüft (Toleranz 0,3 cm).
Alle neuen Gebäude-Actors verwenden `NoCollision`; bestehende Actor-Platzierungen,
Skalierungen, Rotationen und Pawn-/Visibility-Collision wurden numerisch vor/nach dem Import verglichen.

## Cutaway und unveränderte Systeme

**23 neue V2-Module** wurden der vorhandenen Occluder-Liste hinzugefügt:
Dächer/Dachrand, vorderer Giebel, Front- und kameraseitige Wand-, Stein-, Fachwerk-,
Fenster-/Glasteile, Eingang, Kamin sowie der kameraseitige Innenbalken.
Boden, Rückwände, rückseitige Innenbalken, Tresen und Hüterin bleiben sichtbar.

Unverändert: Türschwelle **40 × 240 × 230 cm** bei **(−450, 0, 115) cm**,
Hysterese **4 cm**, Fade **0,4 s**, maskierter `DitherTemporalAA`,
**Custom Primitive Data Index 0** und Collision. Neue Materialien verwenden denselben
`HouseCutaway`-Parameter mit Standardwert 0.

Unverändert: Kamera **2500 cm**, FOV **35°**, Rotation **(−55°, −45°, 0°)**,
Camera Lag **6 / maximal 180 cm**, Player-Körperhöhe **140 cm**, Bewegung **210 cm/s**,
Collision, Input, 8-Richtungsdarstellung, Playeranimationen, Healing, RestPoint,
Checkpoint, Save, Quest und Battle. **Kein C++ geändert**, kein neuer Build erforderlich.

## PIE: vollständiger Fußweg

Im separat gestarteten lokalen Testeditor, regulärer PlayerStart, **keine Test-Teleports**
und kein Spawn-Override. Alle Bewegungen erfolgen durch normale WASD-Eingaben.
Der ursprüngliche Benutzereditor wird nicht geschlossen.

| Schritt | Nachweis / Ergebnis |
| --- | --- |
| Außenstart | Player bei (−1000, 0, 50) cm, Dach/Fassade vollständig eingeblendet. |
| Vorplatz | Zu Fuß bis (−679, −17) cm. Balken, Fenster, Eingang und Dachdeckung klar lesbarer; Player gut erkennbar. |
| Vor der Tür | Bei X −579 cm und nochmals X −479 cm: Cutaway **aus**, Fade **0**. Kein vorzeitiges Ausblenden auf dem Vorplatz. |
| Tür / Innenraum | Durch die vorhandene freie Passage. Bei (−379, −28) cm: Cutaway **an**, Fade **1**; Innenraum sichtbar. Keine Blockade oder Stufe. |
| Diagonalwege | Verschiedene normale W-/D-/S-/A-Eingaben führen ohne Feststecken durch den zentralen Innenraum. |
| Tresen | Bei X 151,62 cm stoppt der unveränderte Blocker sinnvoll vor dem Tresen. Playerkopf/Körper und Hüterin bleiben sichtbar. |
| Hüterin | Regulär mit **E** angesprochen. Begrüßungsdialog erscheint. Nach **Enter**: „Dein Team wurde vollständig geheilt. Der Spielstand wurde gespeichert. Dieser Ruhepunkt ist jetzt dein Rückkehrort.“ |
| Rückweg | Nach Dialogende normale Bewegung wieder möglich; freier Innenraumweg zurück durch die Tür. |
| Wieder außen | Bei (−589, −74) cm: Cutaway **aus**, Fade **0**, V2-Dach und Fassade vollständig wieder eingeblendet. |

Der vorhandene `PokeMonster_Dev`-Slot wurde vor der Bestätigung gesichert und nach StopPIE
**bytegleich wiederhergestellt**. SHA-256:
`56e72576d928353a557a58a4653e58e9613a566dc1b77e3e166135d63f38facf`.
Der zusätzliche, vollständig gespeicherte Testeditor wurde anschließend geschlossen,
um auf dem 16-GB-Mac RAM freizugeben. Der ursprüngliche Benutzereditor bleibt offen.

### Wirkung der festen Spielkamera

Fensterformen, dicke Holzrahmen, Dachdeckung und Eingangsgiebel sind bei 2500 cm lesbar.
Die 140-cm-Figur passt weiterhin zur 240 × 230-cm-Passage und zum 92-cm-Tresen.
Innen bleiben zentrale Laufwege, Versorgungstresen und Hüterin klar erkennbar.
**Direkt am Eingang/Vorplatz bleibt der obere Dachbereich im Bild angeschnitten**,
wie bereits beim bestätigten V1-Kamerastand. Das wurde nicht durch Kamera-/FOV-Änderungen kaschiert.
Blender-Übersichtsbilder zeigen zusätzlich die komplette Silhouette; sie sind keine PIE-Beweise.
Keine Vegetations-/Dekorationsphase und keine finale Lichtinszenierung begonnen.

### Bilder

- `Art/HealingHouse/Review/V2/Blender_Exterior.png`, `Blender_Porch.png`, `Blender_Interior.png` – Architekturübersichten.
- `Art/HealingHouse/Review/V2/PIE_V2_Exterior_2500.png` – normaler Spawn.
- `Art/HealingHouse/Review/V2/PIE_V2_Forecourt_2500.png`, `PIE_V2_BeforeThreshold_2500.png` – Fassade vor Cutaway.
- `Art/HealingHouse/Review/V2/PIE_V2_InteriorWalk_2500.png`, `PIE_V2_AtCounter_2500.png` – tatsächlich spielbarer Innenraum.
- `Art/HealingHouse/Review/V2/PIE_V2_HealerDialogue_2500.png`, `PIE_V2_HealingConfirmed_2500.png` – reguläre Interaktion und Funktionsbestätigung.
- `Art/HealingHouse/Review/V2/PIE_V2_OutsideAfterReturn_2500.png` – Rückweg; dieses Bild enthält eine rein editorseitige Speicherdruck-Benachrichtigung.
- `Art/HealingHouse/Review/V2/PIE_V1_PreviousExterior_2500.png` – unverändert kopiertes Bild aus dem vorherigen bestätigten V1-PIE-Test bei 2500 cm; kein neu durchgeführter V1-Test.

## Tests und Prüfung

- Vorhandener gesamter PokeMonster-Automationstestbestand: **35 erfolgreich, 0 fehlgeschlagen, 0 Warnungen**; einschließlich Player Foundation, Scale Calibration und aller drei HealingHouse-Tests.
- HealingHouse: `Layout`, `CollisionAndCutaway`, `RestCheckpointSaveAndDefeat`.
- **Map Check: 0 Fehler, 0 Warnungen** nach V2-Integration.
- Blender-Geometrie-, Fensterbibliotheks- und Unreal-Import-Audits erfolgreich.
- Prüfdateien: `GeometryAudit.json`, `WindowLibraryAudit.json`, `UnrealImportAudit.json`, `WindowLibraryImport.json`, `ValidationResults.json` unter `Art/HealingHouse/Review/V2/`.
- Keine C++-Änderung; kein neuer Build erforderlich.
- `git diff --check`: **erfolgreich, keine Whitespace-Fehler**. Markdown-Codeblöcke, Dateiende und Tabellenformat geprüft.

## Neue/geänderte Dateien

```text
Art/HealingHouse/Exports/HealingHouse_V2.fbx
Art/HealingHouse/Exports/HealingHouse_V2_WindowModules.fbx
Art/HealingHouse/Review/V2/Blender_Exterior.png
Art/HealingHouse/Review/V2/Blender_Interior.png
Art/HealingHouse/Review/V2/Blender_Porch.png
Art/HealingHouse/Review/V2/GeometryAudit.json
Art/HealingHouse/Review/V2/PIE_V1_PreviousExterior_2500.png
Art/HealingHouse/Review/V2/PIE_V2_AtCounter_2500.png
Art/HealingHouse/Review/V2/PIE_V2_BeforeThreshold_2500.png
Art/HealingHouse/Review/V2/PIE_V2_Exterior_2500.png
Art/HealingHouse/Review/V2/PIE_V2_Forecourt_2500.png
Art/HealingHouse/Review/V2/PIE_V2_HealerDialogue_2500.png
Art/HealingHouse/Review/V2/PIE_V2_HealingConfirmed_2500.png
Art/HealingHouse/Review/V2/PIE_V2_InteriorWalk_2500.png
Art/HealingHouse/Review/V2/PIE_V2_OutsideAfterReturn_2500.png
Art/HealingHouse/Review/V2/UnrealImportAudit.json
Art/HealingHouse/Review/V2/ValidationResults.json
Art/HealingHouse/Review/V2/WindowLibraryAudit.json
Art/HealingHouse/Review/V2/WindowLibraryImport.json
Art/HealingHouse/Source/HealingHouse_V2.blend
Art/HealingHouse/Textures/V2/T_HH_V2_Glass.png
Art/HealingHouse/Textures/V2/T_HH_V2_Metal.png
Art/HealingHouse/Textures/V2/T_HH_V2_Plaster.png
Art/HealingHouse/Textures/V2/T_HH_V2_Roof.png
Art/HealingHouse/Textures/V2/T_HH_V2_Stone.png
Art/HealingHouse/Textures/V2/T_HH_V2_Timber.png
Art/HealingHouse/Textures/V2/T_HH_V2_Wood.png
Content/Environment/HealingHouse/Materials/M_HH_V2_Glass.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Metal.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Plaster.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Roof.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Stone.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Timber.uasset
Content/Environment/HealingHouse/Materials/M_HH_V2_Wood.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Chimney.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_ChimneyCap.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Counter.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Floor.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Foundation.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Far.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorStone.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_PorchFloor.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Entry.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Porch.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Far.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Rear.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Entry.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Far.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Porch.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Far.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Rear.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Arch.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Round.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Twin.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_CameraSide.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Far.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Front.uasset
Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Glass.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Metal.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Plaster.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Roof.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Stone.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Timber.uasset
Content/Environment/HealingHouse/Textures/T_HH_V2_Wood.uasset
Content/Maps/Dev_HealingHouseTestMap.umap
Docs/ENTSCHEIDUNGEN.md
Docs/HEILHAUS_V2_PRUEFBERICHT.md
Tools/Blender/BuildHealingHouseV2.py
Tools/Blender/BuildHealingHouseV2WindowLibrary.py
Tools/Blender/ReviewHealingHouseV2.py
Tools/GenerateHealingHouseV2Textures.py
Tools/ImportHealingHouseV2.py
Tools/ImportHealingHouseV2WindowLibrary.py
```

## Git-Status

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
?? Art/HealingHouse/Exports/HealingHouse_V2.fbx
?? Art/HealingHouse/Exports/HealingHouse_V2_WindowModules.fbx
?? Art/HealingHouse/Review/V2/
?? Art/HealingHouse/Source/HealingHouse_V2.blend
?? Art/HealingHouse/Textures/
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Glass.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Metal.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Plaster.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Roof.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Stone.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Timber.uasset
?? Content/Environment/HealingHouse/Materials/M_HH_V2_Wood.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Chimney.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_ChimneyCap.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Counter.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorFrame.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_DoorLeaf.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Floor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Foundation.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Gable_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Glass_Loft.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorBeams_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_InteriorStone.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_PorchFloor.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Entry.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Main.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Roof_Trim.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Stone_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Entry.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Porch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Timber_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Walls_Rear.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Arch.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Round.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_WindowModule_Twin.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_CameraSide.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Far.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Front.uasset
?? Content/Environment/HealingHouse/Meshes/SM_HH_V2_Windows_Loft.uasset
?? Content/Environment/HealingHouse/Textures/
?? Docs/HEILHAUS_V2_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseV2.py
?? Tools/Blender/BuildHealingHouseV2WindowLibrary.py
?? Tools/Blender/ReviewHealingHouseV2.py
?? Tools/GenerateHealingHouseV2Textures.py
?? Tools/ImportHealingHouseV2.py
?? Tools/ImportHealingHouseV2WindowLibrary.py
```
