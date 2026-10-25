# NPC-Ausbau mit vorhandenen Meshy-Modellen – Prüfbericht

Stand: 25.10.2026. Ausgangspunkt `e804343beadb9761143399c9bc878cb094acb0f2`, Branch `main`.
Ausschließlich `/Users/harry/Developer/PokeMonster`; bestehende VisualV2.

## Ergebnis

Elf vorhandene NPC-Quellen als wiederverwendbare, validierte 3D-Präsentationen
aufbereitet: zehn Modelle aus NPCs/Incoming sowie die bestehende Hobbitquelle.
Kein Modell generiert, keine Ersatzfigur gebaut. **Neun Figuren können gehen,
sechs zusätzlich laufen. SilverLady und TreeBeing bleiben bewusst stationär.**
70 Rollenclips: Idle, Talk, Greet, jeweils zwei Drehrollen sowie vorhandene passende
Walk-/Run-Rollen. Keine Behauptung, dass jeder lange Mantel bereits ein fertiges
physikalisches Stoffrig besitzt. Die verbindliche Originaloptik bleibt erhalten.

Vorhandener Wanderer = technische Ranger-Darstellung; das sind keine zwei neuen
Geschichtsrollen. Seine neue Präsentation und die Heilerin sind direkt an ihre
bisherigen Source-Actors gebunden. Identitäten, Transform, Dialog und Heilfunktion
bleiben bestehen. Keine endgültigen Rollen, Berufe, Namen oder Standorte neu festgelegt.
Archivarin und Liora bleiben funktional erhalten; für sie wurde ohne eindeutige
Modellzuordnung kein beliebiges männliches Modell beziehungsweise eine zweite
Heilerinnenkopie als neue endgültige Darstellung eingesetzt.

## Gefundene Quellen und tatsächlicher Animationsstand

Alle elf GLBs besitzen ursprünglich **kein Skeleton und keine Animationen**.
Geometrie und eingebettete Texturen wurden anhand der Dateien und vorhandener
Arbeitsquellen geprüft; die Abbildungen bestätigen die Dateizuordnung. Die zehn
allgemeinen Meshy-Quellen haben je einen Mesh, ein Material und drei eingebettete
2048er JPEGs. Die Hobbitquelle besitzt ihren älteren eigenen 4K-Intake;
verwendet wird ihre vorhandene geprüfte Arbeitsfassung mit 2048er Texturen.

Höhen sind die bisherigen sichtbaren Gesamtmaße einschließlich Hut/Ausrüstung/
Reitern, keine neu festgelegten anatomischen Größen aller Völker. Spieler: 1,40 m.
Die bestehende Heilerin behält zusätzlich ihren bisherigen Actor-Maßstab.

| Station | Technische ID | Unveränderte Incoming-Quelle | Bibliothekshöhe | Blender-Knochen | Tatsächliche Rollen | Integration |
|---|---|---|---:|---:|---|---|
| 1 | Ranger | `Art/Characters/NPCs/Incoming/Aragorn_V1.glb` | 1.80 m | 26 | Stand, Gespräch, Begrüßung, Gehen, Laufen | eigenes benötigtes Skelettmesh |
| 2 | SilverLady | `Art/Characters/NPCs/Incoming/Arwen_V1.glb` | 1.90 m | 3 | Stand, Gespräch, Begrüßung | bestehendes Mesh/Skeleton |
| 3 | TreeBeing | `Art/Characters/NPCs/Incoming/Baumbart_V1.glb` | 3.80 m | 23 | Stand, Gespräch, Begrüßung | eigenes benötigtes Skelettmesh |
| 4 | ElvenScholar | `Art/Characters/NPCs/Incoming/Elrond_V1.glb` | 1.95 m | 27 | Stand, Gespräch, Begrüßung, Gehen | eigenes benötigtes Skelettmesh |
| 5 | Wizard | `Art/Characters/NPCs/Incoming/Gandalf_V1.glb` | 2.05 m | 24 | Stand, Gespräch, Begrüßung, Gehen | eigenes benötigtes Skelettmesh |
| 6 | WhiteHairedWarrior | `Art/Characters/NPCs/Incoming/Geralt_V1.glb` | 1.85 m | 24 | Stand, Gespräch, Begrüßung, Gehen, Laufen | bestehendes Mesh/Skeleton |
| 7 | DwarfWarrior | `Art/Characters/NPCs/Incoming/Gimli_V1.glb` | 1.32 m | 25 | Stand, Gespräch, Begrüßung, Gehen, Laufen | bestehendes Mesh/Skeleton |
| 8 | CrouchedCreature | `Art/Characters/NPCs/Incoming/Gollum_V1.glb` | 1.10 m | 23 | Stand, Gespräch, Begrüßung, Gehen, Laufen | eigenes benötigtes Skelettmesh |
| 9 | ElvenArcher | `Art/Characters/NPCs/Incoming/Legolas_V1.glb` | 1.95 m | 24 | Stand, Gespräch, Begrüßung, Gehen, Laufen | bestehendes Mesh/Skeleton |
| 10 | DarkArmored | `Art/Characters/NPCs/Incoming/Sauron_V1.glb` | 2.25 m | 23 | Stand, Gespräch, Begrüßung, Gehen | eigenes benötigtes Skelettmesh |
| 11 | HobbitBase | `Art/Characters/NPCs/Westland/HobbitBase/Incoming/4K_Base_V1/Meshy_Hobbit.glb` | 1.40 m | 25 | Stand, Gespräch, Begrüßung, Gehen, Laufen | eigenes benötigtes Skelettmesh |

### Gezielte Korrekturen

- Ranger: ursprüngliche detailreichere 90.000-Dreiecke-Arbeitsgeometrie erhalten;
  vorwärts gerichteten Knielöser aus der früheren V3 weiterverwendet, die übermäßig
  abgesenkte 7,8-cm-Beckenhaltung reduziert. Geschwindigkeit und Schrittlänge werden
  gekoppelt; Kontaktstabilisierung und weichere Gang-/Lauf-/Stoppübergänge ergänzt.
- Eigene Gelenkmarken und Referenzgeschwindigkeiten je Körperform; kurze Zwergen-
  und Hobbitbeine werden nicht aus dem 1,80-m-Ranger nur proportional abgeleitet.
- DarkArmored: konkret gemessenen Bodendurchtritt der vorderen Rüstungsbahn
  behoben. Diese Fläche war an Schienbeine gebunden; Saum und Stoffbahn sind jetzt
  vom Beinschwung getrennt. Kein Laufclip für schwere bodenlange Rüstung erzwungen.
- SilverLady: Vollrig-Ärmelversuch wegen deutlicher Faltungen/Dehnungen verworfen.
  Das bestehende geprüfte Dreiknochen-Mesh mit Originalmaterial wird weitergenutzt.
  Atmung, dezente Kopf-/Gesprächsbewegung, Begrüßungsnicken; **kein Gehen/Laufen
  und kein vorgetäuschtes Handwinken**. Gesicht, Haare, Körper und Kleidung nicht
  neu gestaltet. Innenraum-Schattenfreiheit bleibt gesetzt.
- TreeBeing: verwachsene Bodenwurzeln und fest ins Mesh integrierte Reiter erhalten.
  Stamm-/Astbewegung und Astbegrüßung; **kein unsicherer Gehzyklus** übernommen.
- Drei schon geeignete Humanoidenmeshes (WhiteHairedWarrior, DwarfWarrior,
  ElvenArcher) samt Skeleton wiederverwendet. Geometrie, UVs, Gewichte,
  Ruhe-Skelett und Objektmatrix im Blendervergleich exakt identisch. Ihre neuen
  Clips verwenden die alten Skeletons, keine unnötigen Modell-Doppelimporte.
- Alte statische FBX-Materialgraphen verloren teilweise Roughness/Metallic.
  Neue Blender-Arbeitsquellen verwenden wieder die Originalkanäle und gepackte
  Texturen. Unreal verwendet bestehende Materialinstanzen; nur für die bisher
  nicht vorhandene Hobbit-3D-Darstellung waren eigene Importassets nötig.

## Wiederverwendbare Architektur

`UPokeMonsterNPCPresentationData` enthält ausschließlich Präsentation: Mesh,
Materialüberschreibungen, Clips, Höhenmetadaten und Geschwindigkeitsreferenzen.
Validierung prüft Mesh/Skeleton, exakte Clip-Skeleton-Zuordnung, Dauer, Root-Motion,
Materialslots, Geschwindigkeiten und benötigte Kontaktknochen. Ungültige Profile
ersetzen keine funktionierende Darstellung.

Bestehender `PokeMonsterNPC`/RestPoint, DialogSubsystem, Interact-Aktion und
`PokeMonsterNPCVisualActor` bleiben maßgeblich. Gespräch/Begrüßung betrifft den
Oberkörper; die Fußkette wird nicht vom Gesprächsclip überschrieben. Gait-Phase
bleibt zwischen Walk/Run erhalten, Tempo folgt tatsächlicher Bewegung. Optionale
Fußstabilisierung arbeitet auf flachem Boden und verwirft unerreichbare alte Pins.
Kein neuer Dialog-, Quest-, Speicher- oder produktiver NPC-KI-Unterbau.

Profile: `/Game/Characters/NPCs/Library/Profiles/DA_NPC_<ID>`.
Neue Blenderquellen: `Art/Characters/NPCs/<ID>/Source/<ID>_NPCLibrary.blend`,
Hobbit unter seinem vorhandenen Westland/HobbitBase-Quellordner. Die Dateiorganisation
platziert keinen NPC in der Westland-Map. Alle ursprünglichen Quellen bleiben bestehen.

Animations-FBX enthält nur Knochen/Kurven; Geometrie wird einmal im benötigten
Mesh-FBX gehalten. **70 tatsächlich importierte Clips / 28.441 Knochenposen**
vorher/nachher verglichen: maximale Positions-, Skalierungs- und Quaternion-
Komponentendifferenz jeweils **0**. Bei drei wiederverwendeten Skeletons wurde
nur der ursprüngliche Armature-Wrappername wiederhergestellt; deformierende
Knochen und Posewerte bleiben identisch. Vorläufige, ausschließlich in diesem
Auftrag erzeugte Doppelimporte wurden nach Referenz-/Git-Prüfung verworfen;
keine vorher vorhandene Datei wurde dafür entfernt.

## Normaler PIE-Testbereich

Bei jedem gewöhnlichen PIE-Start in VisualV2 verfügbar, nicht nur während Automation.
Mittelpunkt **(-7500, 3000, 0) cm**, elf getrennte Stationen. NPCs sind ausdrücklich
mit TEST gekennzeichnet; ihre Dialoge enthalten keine Quest-/Weltfolgeaktionen.

```text
pm.NPCGround.Go           # Mitte besuchen
pm.NPCGround.Go 1         # Station 1; 1..11 nach obiger Tabelle
pm.NPCGround.Mode idle    # weitere Werte: auto, walk, run
pm.NPCGround.Greet
pm.NPCGround.Return
```

Zum NPC schauen, mit der bestehenden B-/E-Interaktion ansprechen. Dialog regulär
bestätigen. Besuch nur außerhalb Kampf/gesperrter Innenraumzustände. Rückkehranker
bleibt erhalten. Während des Besuchs nutzt Speichern den vorhandenen RAM-Transport;
Rückkehr stellt den ursprünglichen Sitzungsstand her. Keine Save-Kopie oder neue
Save-Datei. Bei anderem bereits aktivem RAM-Test übernimmt der Bereich dessen Schutz
nicht eigenmächtig. Entwicklungskommandos nur Editor-PIE, nicht regulärer Game-/Shipping-
Betrieb. Westland und Biom-Testmap erhalten keinen Testbereich.

Individuelle Ziele/Pausen, Beschleunigung, sanfte Drehungen und Capsule-Sweeps im
freien Testfeld; bei Blockade abbremsen und neues Ziel wählen. Niedrige Randbegrenzung
schützt vor versehentlichem Verlassen. Dies ist **kein vollständiger produktiver
NavMesh-NPC-Pfadplaner für komplexe Gebäude/Treppen**.

## Echte Unreal-Nachweise

33 QHD-Ansichten (2560×1440) aus unveränderter Spielkamera, je vorn/seitlich/hinten,
mit Spieler als Größenreferenz. [Übersicht echter Aufnahmen](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/NPC_Bibliothek_QHD_Uebersicht.jpg)
ist eine ausdrücklich beschriftete Montage, kein einzelner Spiel-Screenshot.
[Wanderer vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Wanderer_Before_QHD.png) /
[nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Wanderer_After_QHD.png): gleiche XY-Position und Rotation;
Boden-Settling-Abweichung in Z kleiner als 0,00001 cm. Keine geänderte Kamera.
[Heilerin – tatsächliche Interaktion](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Heilerin_Interaction_QHD.png).

Finale elf Videos: zusammen 106,96 Spielsekunden, **24,62–27,03 echte Bilder je
Spielsekunde**. Keine erfundenen/interpolierten Zwischenbilder. Nativer QHD-Spielrender;
aufgezeichneter tatsächlicher Slate-Ausschnitt **2331×1311**, nicht als 2560er
Videodatei ausgegeben. Für dichte Bewegungsprüfung wurde PIE bei der Aufnahme auf
0,25-fache Spielzeit verlangsamt und mit echten Spielzeitstempeln normal schnell
encodiert. Das ist keine Echtzeit-FPS-Messung. Die ersten dünneren Framebufferfolgen
PIE02 (ca. 13 Hz, einschließlich Dialogzuständen) sind ergänzende Diagnosen.

| Figur | QHD-Spielkamera | Vollständiger kurzer Bewegungsclip | Dauer / Bilder / Spielzeit-Abtastung |
|---|---|---|---|
| Ranger | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Ranger_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Ranger_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Ranger_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/Ranger_Gameplay.mp4) | 11.65 s / 314 / 26.87 Hz |
| SilverLady | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/SilverLady_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/SilverLady_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/SilverLady_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/SilverLady_Gameplay.mp4) | 4.70 s / 128 / 27.03 Hz |
| TreeBeing | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/TreeBeing_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/TreeBeing_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/TreeBeing_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/TreeBeing_Gameplay.mp4) | 4.76 s / 129 / 26.87 Hz |
| ElvenScholar | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenScholar_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenScholar_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenScholar_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/ElvenScholar_Gameplay.mp4) | 9.16 s / 239 / 25.97 Hz |
| Wizard | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Wizard_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Wizard_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/Wizard_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/Wizard_Gameplay.mp4) | 9.19 s / 241 / 26.10 Hz |
| WhiteHairedWarrior | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/WhiteHairedWarrior_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/WhiteHairedWarrior_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/WhiteHairedWarrior_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/WhiteHairedWarrior_Gameplay.mp4) | 11.74 s / 292 / 24.78 Hz |
| DwarfWarrior | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DwarfWarrior_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DwarfWarrior_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DwarfWarrior_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/DwarfWarrior_Gameplay.mp4) | 11.70 s / 289 / 24.62 Hz |
| CrouchedCreature | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/CrouchedCreature_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/CrouchedCreature_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/CrouchedCreature_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/CrouchedCreature_Gameplay.mp4) | 11.63 s / 297 / 25.44 Hz |
| ElvenArcher | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenArcher_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenArcher_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/ElvenArcher_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/ElvenArcher_Gameplay.mp4) | 11.70 s / 317 / 27.01 Hz |
| DarkArmored | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DarkArmored_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DarkArmored_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/DarkArmored_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/DarkArmored_Gameplay.mp4) | 9.09 s / 236 / 25.86 Hz |
| HobbitBase | [Vorn](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/HobbitBase_Front.png), [Seite](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/HobbitBase_Side.png), [Hinten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/PIE02/HobbitBase_Rear.png) | [Video](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/NPCExpansion/Motion02/HobbitBase_Gameplay.mp4) | 11.63 s / 323 / 27.68 Hz |

Alle Medien bleiben lokal in `Saved`; keine Kontrollbilder oder Videos auf GitHub.

## Prüfungen

- Editor-Build: `NPCExpansionBuild07`, erfolgreich.
- Elf Blender-Arbeitsquellen erneut geöffnet; genau ein Laufzeitmesh und ein Rig,
  benötigte Rollen vorhanden, wirksame Gewichte normalisiert, verwendete
  Originaltexturen gepackt. Historische unbenutzte Posegruppen zählen nicht als
  zusätzliche deformierende Gewichte.
- Vollständige relevante Automation: **210 Tests, 209 Success, 1 SuccessWithWarnings,
  0 Fehler, 0 nicht ausgeführt**. Engine Exit 0; strenger Wrapper **Exit 1** wegen
  zweier externer idevice_id-Warnungen in PokeMonster.BiomeV11.SpeciesPersistence.Garados.
  Kein Projektfehler, keine Warnungsunterdrückung. Alle sechs NPC-Tests erfolgreich,
  einschließlich echter Kapselkollision an der Randbegrenzung und Originalmesh-Wiederverwendung.
- Zwölf vorhandene Maps geprüft, jeweils 0 Fehler / 0 Map-Check-Warnungen. Keine
  neue Map. Ein Map-Check-Ergebnis ist kein allgemeines warnungsfreies Engine-Log.
- Abschließender normaler PIE nach finalem Build: alle neun Gehfiguren tatsächlich
  bewegt, zwei bewusst stationär, drei Originalmeshes kontrolliert, echter Spieler-
  Eingabetest gegen Randkollision, Rückkehr und RAM-Save/Load bestanden.
- Normaler PIE: elf echte NPCs ohne QA-Spawner verfügbar, elf passende B-Ziele,
  Gesprächszustände, Gang-/Lauf-/Begrüßungsfolgen, Richtungen, freie Spielerbewegung.
  B war eine **softwareseitige Slate-Simulation**, kein neuer physischer Hardwaretest.
- Ursprünglicher Wanderer und Heilerin: ursprüngliche Dialogquelle, Blickwendung/
  Präsentationsreaktion, vollständige Heilung und bestehender Save/Load-Rundlauf bestätigt.
- Vorhandene Save-Datei über alle aufgezeichneten Durchläufe SHA-256-identisch:
  `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`.

## Offene Qualitätsgrenzen und Fehlversuche

SilverLady benötigt für überzeugendes Gehen weiterhin gezielte Gewand-/Ärmelarbeit;
TreeBeing eine separate Lösung für verbundene Wurzeln/Reiter. Keine falsche
Vollständigkeitsbehauptung für diese zwei Figuren. Weitere Roben/Rüstungen nutzen
bewusst zurückhaltendes Gehen. Keine Finger-, Gesichtslippen-, Cloth-Simulation,
Terrain-IK oder handanimierten Extrem-Pivots. Subtile Durchdringungen können bei
Nahsicht/Extremposen weitere lokale Arbeit erfordern; Spielkamera und diese Clips
ersetzen keine beliebige Rundum-Animationsfreigabe.

Der erste NPC-Isolationstest rief Engine-BeginPlay unzulässig zweimal auf und
verursachte einen Ensure; Testaufbau korrigiert, nicht der Fehler unterdrückt.
Ein erster PIE-Versuch nach Import/Automation stürzte mit
`pthread_rwlock_init failed with error: 16` ab. Frischer Editor, vollständiger
Funktionslauf, alle elf Bewegungsclips und erneuter PIE-Start nach den korrigierten
NPC-Tests liefen stabil. Die genaue native Ursache des einmaligen Absturzes ist
nicht abschließend bewiesen; frühere Logs bleiben lokal erhalten.

Bekannte externe iOS-Helfer-Warnungen (`idevice_id`, Bad CPU type 86), gegebenenfalls
CoreAudio-Gerätewarnung und belegter Plugin-HTTP-Port werden separat protokolliert.
Keine funktionierenden Controller-Eingaben oder Kamera-/Landschaftssysteme verändert.
Ein strenger QA-Wrapper mit Exit 1 wird nicht als warnungsfrei bestanden dargestellt.

## Git / Schutz

Nur NPC-Quellen, notwendige Bibliotheksassets, gezielte VisualV2-Bindung, Code,
Werkzeuge und Dokumentation. Keine Änderung der Biom-/Westland-Maps, Pokémon-
Assets/Animationen, Incoming-Originale oder vorher vorhandenen 31 unversionierten
Dateien. Lokales Vollbackup `03492bd` und Git-Historie bleiben erhalten.

Commit-/Remote-/LFS-Abschluss wird nach finaler QA ergänzt. Normales `origin/main`,
kein Force-Push; bestätigtes Git-LFS-Budget 0 USD, keine Budget-/Zahlungsänderung.
