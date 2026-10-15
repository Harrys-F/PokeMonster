# Meshy Player Sprint V1 – Implementierung und Prüfung

14.10.2026, Ausgangs-HEAD `3c6dc47`. Der Nutzer hat ausdrücklich Sprint für den bestehenden Meshy-Player und eine getrennte, ungeriggte Hobbit-NPC-Basis bestätigt. Projekt-Dokumentation in Docs bleibt bis zur visuellen Prüfung unverändert.

## Verhalten

- Normales Gehen bleibt **210 cm/s**, Sprint **315 cm/s**. Der Code speichert beim Aktivieren den tatsächlich eingestellten Gehwert und multipliziert ihn mit 1,5; beim Deaktivieren wird genau dieser Wert wiederhergestellt.
- **Linke/rechte Shift-Taste halten**; **L3** während Bewegung schaltet den Sprintwunsch um. Stillstand beziehungsweise ein tatsächlicher Kollisionsstopp löscht die L3-Vormerkung.
- Acht Richtungen nutzen dieselbe normalisierte Kamera-Bewegungsbasis; Diagonalen überschreiten 315 cm/s nicht.
- Bestehende Menü-/Dialog-/Encounter-Eingabesperre verhindert Sprint. Sie löscht alte Sprintwünsche; nach dem Schließen von UI/Dialog eine frische Shift-Betätigung verwenden. Kein unerwarteter Sprint durch ein in UI verbliebenes Signal.
- Bestehende BuildingCutaway-Innenraumgrenzen verhindern Sprint auch ohne Innenkamera. Der vorhandene Innenkamera-Übergang sperrt Sprint zusätzlich. Gehaltenes Shift kann nach normalem Hinauslaufen wieder Sprint aktivieren.
- Keine Ausdauer, kein zusätzlicher Player-Tick, kein Eingriff in Kamerawerte, Capsule oder Gameplay-Regeln. Das vorhandene CharacterMovement-Update prüft die Sperren.

## Animation und Quellen

Neue Datei: `Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend`. Neues FBX: `Art/Characters/YoungTrainer/Exports/SprintV1/A_Player_Meshy_Run_V1.fbx`. Neue Animation: `/Game/Characters/YoungTrainer/MeshyV2/Animations/A_Player_Meshy_Run_V1`.

Bestehendes V2-Rig mit **25 Knochen** und unveränderten Gewichten. Referenzkörper **1,39999998 m**; drei 2048²-Texturen gepackt. Quelldatei in neuem Blender-Prozess erneut geöffnet. Original `Player_Meshy_V1.blend`, GameReady V1 und AnimationQuality V2 unverändert.

Eigener **0,45-s-Rennzyklus**, 28 gespeicherte Frames bei 60 Hz. Bei 315 cm/s entspricht ein vollständiger Zyklus 1,4175 m Fortbewegung; die Stützphase benutzt eine entgegen der Bewegung laufende Fußbahn mit 3,15 m/s. Gegengleiche Arme, etwas kräftigere Knieerholung, kleine Becken-/Schulterbewegung, begrenzte Körperneigung und vorhandene Umhang-/Taschenbewegung. Kein Root Motion. Tatsächliche verformte Sohlengeometrie an allen 28 Frames geprüft: nicht unter dem Boden; Root bleibt am Ursprung.

Bestehende Animationsinstanz mischt Idle/Walk/Run über **0,18 s**, koppelt die Rate an die tatsächliche Geschwindigkeit und synchronisiert die Links-/Rechts-Zyklusphase. Bestehende Zubehörfedern bleiben erhalten. Ohne neuen Run-Clip bleibt Walk als robuste Darstellung erhalten; Paper2D-Rückfall unverändert erreichbar.

## Tatsächlich ausgeführte Prüfungen

- Unreal-5.8.2-Editorbuild Mac Development: **Succeeded**, 24,47 s, maximal zwei parallele Aktionen.
- Aktueller Testumfang **42/42 Success**, einschließlich neuem `PokeMonster.Player.Sprint`, erweitertem MeshyPresentation-Test und allen bisherigen Tests. Keine Fehler im Ergebnisdatensatz.
- Eingebetteter PIE in `/Game/Maps/Dev_TestMap_VisualV2`, keine schwebenden PIE-Fenster.
- 324 protokollierte Frames / rund 20 s Bewegungstest: alle acht Sprintbewegungen erreichen 315; Shift-Aktionsfreigabe und L3-Aus kehren zu 210 zurück, Stop löscht L3, letzte Blickrichtung bleibt, Menü sperrt, Paper2D-Fallback funktioniert.
- Bestehenden Wanderer durch die echte Interaktionssuche angesprochen: Dialogstart, Bewegungs-/Sprintsperre und Wiederaufnahme nach Schließen bestanden. Existierender Testkampf gestartet und eine Runde aufgelöst: Battle-UI und Sprint-/Bewegungssperre bestanden. Kein vollständiger Sieg-/Niederlagendurchlauf in diesem Sprint-Test; die entsprechenden bisherigen Automationstests bleiben grün.
- Heilhaus außen → Tür → unveränderte Relocation → innen gerade/diagonal → Tür → außen **zu Fuß** geprüft. Kein Test-Teleport während der Bewegung; nur PIE-Startposition vor der Tür. Innen 210, nach Austritt wieder 315. Bestehende Heil-/Save-Funktionen hier nicht erneut bedient.
- Kamera **2850 / −50 / −45 / 35**, Capsule Radius28/Halbhöhe48 während des Bewegungstests unverändert geprüft.
- Map Check: **0 Fehler / 0 Warnungen**. Keine dirty Maps/Content-Pakete.
- `git diff --check`: keine Ausgabe.

Die Bewegungstests benutzen Enhanced-Input-Aktionsinjektion im echten PIE, nicht einen simulierten CharacterMovement-Ersatz. **Physischer Controller nicht getestet.** L3-Mapping und Zustandslogik sind automatisiert geprüft. Ein zusätzlicher UI-Tastaturversuch lieferte W bis 210 cm/s, aber der UI-Automationsdienst übergab Shift nur als Modifier und unterstützt keinen isolierten gehaltenen Modifier. Daher ist eine vollständige Prüfung der realen Shift-Tastaturbetätigung durch Harry noch offen; sie wird nicht als bestanden ausgegeben.

## Sichtprüfung und offene Qualitätsgrenzen

22 echte Gameplay-Screenshotdateien unter `Saved/Sprint_20261014/PIE/`; vollständige tatsächliche Pfade in `Saved/Sprint_20261014/ActualScreenshots.json`. Unter anderem `Run_Up_3400000.png`, `Run_Down_3200000.png`, `HealingHouse_Inside00000.png`. Blender-Datei/Sohlenprüfung und Gameplay-Bilder wurden geprüft. Keine synthetischen Konzeptbilder und keine angebliche Videoaufnahme.

Der neue Clip funktioniert und hat abwechselnde Schritte, eine schnelle Phase und weiche Übergänge. Das vorhandene Meshy-Mesh und seine früheren Skinning-Grenzen bleiben erhalten: Umhang/Beine können in extremen Zwischenposen noch lokale Überschneidungen zeigen; perfekte Fußhaftung während Beschleunigung und Richtungswechsel ist nicht garantiert. Kein neuer Cloth-Solver, kein neues Rig, kein Retopologiepass. Visuelle Freigabe des Rennbilds steht aus.

Der erste Prüflauf zählte noch den Eingabe-/Abbrems-Übergangsframe als „Gehen“ und meldete dadurch zwei falsche Geschwindigkeitsüberschreitungen. Der finale Test berücksichtigt 0,25 s Einschwingzeit; es wurde dafür keine Gameplay-Beschleunigung geändert. Temporäre Python-Testbeobachter wurden vor der weiteren Prüfung durch einen sauberen Editorneustart entfernt.

## Dateien und Sicherung

Geändert:

- `Source/PokeMonster/Characters/PokeMonsterPlayerCharacter.h` und `.cpp`
- `Source/PokeMonster/Characters/PokeMonsterMeshyVisualComponent.h` und `.cpp`
- `Source/PokeMonster/Characters/PokeMonsterMeshyAnimInstance.h` und `.cpp`
- `Source/PokeMonster/Tests/PokeMonsterPlayerFoundationTest.cpp`
- `Source/PokeMonster/Tests/PokeMonsterMeshyPlayerTest.cpp`

Neu: Sprint-Blenderquelle, Run-FBX, Run-uasset, `Source/PokeMonster/Tests/PokeMonsterPlayerSprintTest.cpp`, `Tools/Blender/CreateMeshySprintV1.py`, `Tools/ImportMeshySprintV1.py`, dieser Reviewbericht. Zusätzlich die getrennte NPC-Basis im neuen HobbitBase-Arbeitsbereich mit eigenem Prüfbericht und sieben Vorschauen.

Von **1461** vor Sprint erfassten Projekt-/Incoming-Dateien sind **1453 bytegleich**, nur die acht oben genannten C++-/Testdateien geändert. Alle bestehenden Maps, Blender-Quellen, Meshes, Texturen, Materialien und zehn bereits untracked vorhandenen Incoming-GLBs erhalten. Kein Commit, kein Push, nichts gestaged.

Detailbelege: `Saved/Sprint_20261014/Build.log`, `AutomationResults.json`, `BlenderRunAudit.json`, `ReopenSprint.json`, `MovementPIE.json`, `DialogueBattlePIE.json`, `InteriorPIE.json`, `BaselineComparison.json` und `FinalEditorAudit.json`. Saved enthält lokale Prüfarbeitsdaten, keine verbindliche Projektdokumentation.
