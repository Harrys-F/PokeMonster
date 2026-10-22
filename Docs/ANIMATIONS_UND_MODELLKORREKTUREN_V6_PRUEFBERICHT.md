# PokeMonster – Animations- und Modellkorrekturen V6

Stand: 22.10.2026. Ausschließlich `/Users/harry/Developer/PokeMonster`, bestehende VisualV2 und ihr natives permanentes Pokémon-Testgelände. Ausgangspunkt `ee6dcaf9921cd387a55e3add66539734e45444d5`.

**Ergebnis:** Änderungen sind tatsächlich in Blender/Unreal umgesetzt und aktiv. Build, 99/99 Automationstests, elf Map Checks und vollständiger PIE-Fußlauf bestehen. Eine vollständige künstlerische Freigabe wird nicht behauptet: Gluraks dunkle Flügelwurzelfelder, enge Fußwendungen und die Mantel-/Hosen-Silhouette bleiben Abnahmepunkte.

Umsetzungscommit: `3407e609a1a5c2bdc8baf813be9612c0861f98cb` – `fix: refine player gait and Pokemon animation presentation`. Der GitHub-Push ist wegen nicht einsehbarer aktueller kostenloser LFS-Kapazität noch nicht ausgeführt; Einzelheiten unten.

## 1. Befunde und tatsächliche Korrekturen

| Gegenstand | Nachgewiesener Ausgangsbefund | V6 und verbleibende Grenze |
|---|---|---|
| Player-Beine | Feste Fußmitten bei ±16 cm im vorhandenen Gang; Weltachsen-IK bereits vorhanden | ±12 cm, also 24 statt 32 cm Abstand. Körpergeometrie, Gewichte, Rest-Rig und Größe unverändert. Source-Sohlenminimum ca. 0,05 cm; Knie-/Sprunggelenk-Anschlussabweichung unter 0,00024 cm. Das ist ein Source-Wert, kein vollständiger World-Space-Fußkontaktbeweis. |
| Player-Arme | Tatsächlicher Ellbogenwinkel in den vorherigen Idle/Walk/Run-Clips praktisch konstant bei 15,18°. Eine Drehung nur durch die Restbasis kann nach Absenken des Oberarms überwiegend zum Verdrehen des Unterarms führen. | Beugung durch die tatsächliche Posenbasis: Walk ca. 16,11–24,24°, Run 13,66–26,93°. Lockererer Oberarm-/Schulterschwung, bestehende Gegenrotation erhalten. Kein Face-/Haar-/Kleidungsredesign. |
| Mantel/Hose | Ein gemeinsames Mesh mit eng benachbarten Kleidungsflächen. Keine Mantelgewichte >0,1 im eindeutig abgegrenzten vorderen Beinbereich; zwölf Randvertices sind geometrisch nicht eindeutig als Hose statt Mantel klassifizierbar. | Bestehende separate Mantel-Bones erhalten stärkere rückwärtige Führung und phasenversetzte Bewegung; vorhandene Turn-/Stop-Springs bleiben. Keine unbelegte Regewichtung, kein Geometrieschnitt und keine neue Cloth-Simulation. Eine vollständige Beseitigung der seitlichen Verbindungswirkung ist **nicht nachgewiesen**. |
| Glurak-Farbe | Bisherige Rückseitenmaske hing von Texturfarbton und einem zu engen Normalenschwellwert ab; große dunkle Randreste sind im echten Vorherbild sichtbar. | Tatsächliche Front-/Rücksicht über BVH-Strahlen und anatomische Flügelgewichte; 25.092 Rückflächen klassifiziert. Neues lokales Material, Originaltexturen/UVs bleiben. Die großen dunklen Randbereiche verschwinden. **Zwei dunkle Felder nahe den gefalteten Flügelwurzeln bleiben sichtbar: das Ziel einer restlos orange erscheinenden Rückansicht ist noch nicht vollständig erreicht.** Innenseiten werden nicht pauschal orange übermalt. |
| Glurak-Bewegung | Geringe Spitzenbewegung und gleichförmiger Flügelschlag; steife Vorderarme | Unterschiedliche Basis-/Spitzenphasen, verzögerte Spitzen, zusätzliche Schlagharmonik, entspannter geführte Bodenflügel und Vorderarme. Alle sieben Rollen sowie Takeoff/Hover/Land neu gebacken. Bestehender 90-cm-Hover, Bodennavigation und Schwanzflamme erhalten. |
| Nebulak-Kern | Gasmaterial-Zuordnung anhand peripherer Bone-Einflüsse schneidet in die deckende Kernoberfläche. Nach virtuellem UV-Naht-Schweißen zeigen die getrennten Materialflächen 310/319 offene Grenzkanten; diese sind nicht gleichbedeutend mit ebenso vielen echten Geometriefehlern. | 766 Kernflächen wieder deckend. Zusätzliche geschlossene innere Oberfläche mit 1.840 Dreiecken verhindert Durchsicht durch verbleibende Öffnungen. Originale Außenflächen, Gesicht, Augen, UVs und Texturen erhalten; keine Neumodellierung des Gesichts. In den geprüften Front-/Seiten-/Rückansichten kein durchsichtiger schwarzer Kern mehr. |
| Nebulak-Schweben/Gas | Bisherige zusätzliche Oberwelt-Liftamplitude null; violette Außenströmung relativ schwach | Zusätzlicher langsamer visueller Lift gemessen 2,10–14,10 cm, kleine Neigung/Yaw, ausschließlich mit Oberwelt-Roaming-Kontext. Logische Bodenposition/Kollision unverändert. Kräftigere transparente violette Abstufungen und bestehende verschieden schnelle Strömungen. Originale skulptierte Gasformen bleiben teilweise erkennbar; kein volumetrischer Rauch. |
| Machomei | Restfüße und alte Ziele bereits 60 cm auseinander; die Ursache ist nicht erst ein FBX-Achsentausch | 46 cm animierter Fußmittenabstand, anatomische Weltachsen-IK, Gewichtsverlagerung, ruhigere Fußrückführung. Keine Änderung der muskulösen Geometrie oder 160-cm-Größe. Vier Arme mit verschiedenen Phasen und Schulter-/Ellbogenbewegung; Attacken zeitlich versetzt. Zu stark abgesenkte erste Armvariante vor Übernahme korrigiert. |
| Myrapla | Fünf vorhandene Blatt-Bones, geringe nahezu einförmige Bewegung | Unterschiedliche Phasen, zusätzliche langsame Bewegungskomponente, stärkere Walk-/Run-Auslenkung, stabile Bone-Ansätze. Vorhandene Bewegungsblends glätten Start/Stop; kein neuer separater physikalischer Blatt-Stopp-Spring. Originalform/-farben unverändert. |

Walk/Sprint des Players bleiben **210/315 cm/s**, Clipzyklen 0,55/0,45 s, Referenzgröße 140 cm. Ein allgemeines vollständiges Foot-Locking bei abrupten engen Wendungen ist nicht implementiert. Keine pauschale Aussage, dass jedes Fußgleiten oder jede mögliche Selbstüberschneidung beseitigt sei.

## 2. Pikachu und Schiggy: tatsächliche Oberweltgeschwindigkeit

Nur `Species.Overworld.WalkSpeedOverride` und `RunSpeedOverride` geändert. Kampfwerte, rundenbasierte Initiative, Referenzgrößen und die authored Clipgeschwindigkeiten bleiben erhalten; der vorhandene Animator taktet nach tatsächlich gemessener Bewegung.

| Art | Vorher Walk/Run | V6 Walk/Run | Im normalen Testgelände tatsächlich erreichte Werte |
|---|---:|---:|---:|
| Pikachu, 40 cm | 13 / 28 cm/s | 14,95 / 32,2 cm/s | 14,9499998 / 32,2000008 cm/s |
| Schiggy, 50 cm | 26 / 50 cm/s | 29,9 / 57,5 cm/s | 29,8999996 / 57,5 cm/s |

Das permanente Testgelände hatte seine Bewegung bisher stets auf die Präsentationsreferenzgeschwindigkeiten gesetzt. Es respektiert nun dieselben individuellen Artenüberschreibungen wie Wild- und Begleiterbewegung. Der Vergleich zeigt deshalb reale Bewegung und keine bloß geänderten Datenanzeigen. Kein globaler Geschwindigkeitsmultiplikator und kein FPS-Benchmark.

## 3. Dateien, Rig und Integration

Fünf getrennte gepackte Blenderquellen unter den bestehenden Art-Verzeichnissen:

- `Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationCorrections_V6.blend`
- `Art/Characters/Creatures/{Glurak,Nebulak,Machomei,Myrapla}/Source/{Name}_AnimationCorrections_V6.blend`

Jeweils `AnimationCorrectionsV6_Audit.json` mit Quell-/Exportprüfsummen und gezielten Änderungsdaten; zusammen 34 neue FBX unter `Exports/AnimationV6`. Alle fünf Dateien erneut geöffnet, Bilder eingebettet und **jede der 34 FBX tatsächlich nach Blender zurückimportiert**.

| Quelle | Bisherige Body-Dreiecke | Blender-Bones | V6-Geometrieänderung |
|---|---:|---:|---|
| Player | 47.744 | 25 | Keine |
| Glurak | 246.066 | 24 | Keine; nur Farbattribute/Animationen |
| Nebulak | 21.687 | 12 | Geschlossene innere Kernoberfläche, +1.840 Dreiecke |
| Machomei | 21.708 | 22 | Keine |
| Myrapla | 224.602 | 15 | Keine |

Neue Unreal-Pakete unter `/Game/Characters/Creatures/{Glurak,Nebulak,Machomei,Myrapla}/AnimationV6` und drei Player-Clips unter `/Game/Characters/YoungTrainer/AnimationV6`. Insgesamt 50 neue Unreal-Assets. Player verwendet sein ursprüngliches V2-Mesh/Skeleton; die vier Kreaturen erhalten eigene Skeleton-Assets mit exakt gleichen Referenz-Bones/Eltern/Resttransformationen. Alte Quellen, Meshes, Materialien und Clips bleiben erhalten.

Nur vier Spezies-Präsentationsverweise und die zwei genannten Oberweltgeschwindigkeitskonfigurationen geändert. Alle zehn Spezies-IDs, Größen, Team-/Save-Strukturen, Kampfregeln und bestehenden Karten bleiben erhalten. Nebulaks Float-Parameter ist opt-in für Floating-Rigs und benötigt einen Oberwelt-Bewegungskontext. Separate ClassicBattle-Visuals erhalten keinen Lift; WorldBattle gibt seiner bestehenden Kampfpose weiterhin die Kontrolle.

Werkzeuge und Schutzbedingungen: [README](/Users/harry/Developer/PokeMonster/Tools/AnimationCorrectionsV6/README.md). Kompakte geprüfte Rohdaten-/Medienquittung: [Acceptance.json](/Users/harry/Developer/PokeMonster/Tools/AnimationCorrectionsV6/Acceptance.json).

## 4. Echte QHD-Bildvergleiche und Bewegungsnachweise

Alle Bilder stammen aus Unreal, alle hier verwendeten Spielkameraaufnahmen sind tatsächlich 2560 × 1440 mit 100 % Screen Percentage. Kein Konzeptbild, Blender-Rendering oder synthetisches Zwischenbild als Umsetzungsnachweis.

Für die fünf folgenden A/B-Paare wurden erhaltene alte und aktive neue Unreal-Assets innerhalb desselben gewöhnlichen PIE-Laufs auf dem nativen Testgelände verglichen. Keine zusätzlichen Modelle gespawnt. Die protokollierte Kamerapositions- und Rotationsdifferenz beträgt für **jedes Paar exakt null**. Das sind kontrollierte Darstellungsvergleiche; unabhängige natürliche Bewegungs-/Gameplaytests stehen unten.

| Ansicht | Vorher | Nachher |
|---|---|---|
| Player | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/PlayerBefore00000.png) | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/PlayerAfter00000.png) |
| Glurak hinten | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/GlurakBefore00000.png) | [QHD; Wurzelfelder noch offen](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/GlurakAfter00000.png) |
| Nebulak | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/NebulakBefore00000.png) | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/NebulakAfter00000.png) |
| Machomei | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/MachomeiBefore00000.png) | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/MachomeiAfter00000.png) |
| Myrapla | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/MyraplaBefore00000.png) | [QHD](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/MyraplaAfter00000.png) |

Nebulak im identischen Bildausschnitt:

![Vorher – Nebulak](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/NebulakBefore00000.png)

![Nachher – Nebulak](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/AlignedAB07/NebulakAfter00000.png)

**Bewegung – echte zeitlich geordnete Unreal-Frames als lokale MP4:**

| Motiv | Vorher | Nachher |
|---|---|---|
| Player: Idle, Walk, Sprint, Stop, acht Richtungen | [167 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforePlayer/Motion.mp4) | [158 Frames, ca. 25 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterPlayer/Motion.mp4) |
| Glurak: Ansichten, Gehen, Abheben/Schweben/Landen | [222 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforeGlurak/Motion.mp4) | [402 Frames, ca. 55 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterGlurak/Motion.mp4) |
| Machomei: Stand, vier Arme, Gang/Run/Attack | [147 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforeMachomei/Motion.mp4) | [220 Frames, ca. 31 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterMachomei/Motion.mp4) |
| Myrapla-Blätter | [142 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforeMyrapla/Motion.mp4) | [132 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterMyrapla/Motion.mp4) |
| Nebulak: Front/Seite/Rücken und Bewegung | [143 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforeNebulak/Motion.mp4) | [138 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterNebulak/Motion.mp4) |
| Pikachu | [143 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforePikachu/Motion.mp4) | [120 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterPikachu/Motion.mp4) |
| Schiggy | [142 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/BeforeSchiggy/Motion.mp4) | [119 Frames](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV6/Media/AfterSchiggy/Motion.mp4) |

Die Originalzeitabstände sind erhalten. Framebuffer-Readback und einzelne PNG-Aufnahmen verursachen sichtbare Aufnahmeabstände; diese Videos beweisen keine ungestörte flüssige Live-Wiedergabe und sind kein FPS-Benchmark. Bewegte A/B-Läufe verwenden gleiche Eingabefolgen und Spielkamera, ihre Posenzeitpunkte sind nicht pixelidentisch. Player: alle acht Geh-/Sprintrichtungen geerdet. Glurak/Machomei zusätzlich acht feste Ausrichtungen. Eine vollständige kontinuierliche Fußkontakt-/Selbstüberschneidungsabnahme jedes Pokémon in allen acht Laufrichtungen bleibt künstlerisch offen.

Medien sind absichtlich nur lokal vorhanden. Git enthält ihre Prüfsummen/Quittung, keine Kontrollbilder, Videos oder temporären Renderings. Nach frischem Clone neue Aufnahmen erzeugen; fehlende alte Medien sind kein Testpass.

## 5. Technische und Gameplay-Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Mac Development Editor Build | `AnimationV6Build02`: Prozesscode 0, ca. 26,5 s |
| Vollständige Automation nach letzter Clipkorrektur | `AnimationV6Automation02`: **99 Success, 0 SuccessWithWarnings, 0 Failed, 0 NotRun, 0 InProcess** |
| Neuer Regressionstest | Derselbe Floating-Datensatz hebt ein echtes Oberweltvisual, ein separates Battlevisual bleibt bei Z=0. Logische Position/Kollision unverändert; kein Rest-Lift/Rest-Tilt nach Profilwechsel; ungültige Amplitude/Rig-Familie abgelehnt. |
| Elf Map Checks, abschließende Wiederholung | Alle 11 vorhandenen Maps: 0 Fehler, 0 Warnungen; keine Map gespeichert |
| Endgültiger vollständiger PIE-Fußlauf | `AnimationV6FullFoot03`: **103 Schritte, 289,11 m, maximal 315 cm/s**; echter Enhanced Input, keine Testteleports |
| Fußlauf-Funktionen | Wanderer/Dialog/Quest, Liora-Trainerkampf, Fang, acht Richtungen/Sprint, Brücke/Wald/Wege, Heilhaus gerade/diagonal betreten/verlassen, Heilen, Menüfokus, Save/Load bestanden |
| Weitere natürliche Wildkämpfe im Fußlauf | Glurak und Gengar regulär geflohen; erforderlicher Teamwechsel gegen Gengar über die vorhandene Spiellogik. Keine Sperre oder Kampfregel umgangen. |
| Sechs artspezifische 3D-Prüfungen | Glurak, Nebulak, Machomei, Myrapla, Pikachu, Schiggy: echter Begleiter/Walk/Sprint, beide ClassicBattle-Perspektiven, Attack/Hit/Happy/Faint, Attackenauflösung und Rückkehr bestanden |
| Kampfbild | Unveränderte bestehende 2560×1080-Battle-RenderTargets; vollständige LiveUI gesondert. Keine Behauptung, diese Targets seien selbst QHD-Spielkamerabilder. Nebulak/Glurak im Kampf ohne autonome zusätzliche Schwebehöhe. |
| Fang/Team/Heilung/Save | `AnimationV6Capture`: sieben Fangfälle bestanden, ursprünglicher Dev-Save exakt restauriert |
| WorldBattle | `AnimationV6WorldOutcome` bestanden; besondere Ausgangsregeln erhalten |
| Niederlagen-Autosave | `AnimationV6Defeat` bestanden, Rückkehr/erneutes Laden geprüft, ursprünglicher Dev-Save restauriert |
| Glurak-Hover | Grounded → Takeoff → Hover → Landing → Grounded tatsächlich protokolliert; Maximum 94 cm |
| Permanente Verfügbarkeit | Normale PIE-Starts verwenden den nativen WorldSubsystem-Testbereich, keine Automation als Spawnvoraussetzung |
| Quellen | Fünf gepackte Quellen und 34 echte FBX-Rückimporte bestanden |
| Physischer Switch Pro Controller | Offen; simulierte Eingaben und Softwaretests sind kein Hardwaretest |

Der vollständige Fußlauf benutzt den erhaltenen alten Test-Water-Spielstand ohne 3D-Begleiter. Seine null 3D-Begleiterstichproben werden **nicht** als positiver Begleiternachweis gewertet; dafür dienen ausdrücklich die sechs artspezifischen Prüfungen.

Der ursprüngliche Dev-Slot hat nach allen schreibenden Tests wieder exakt SHA-256 `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`. 1.556 ursprüngliche Art-/Map-/Config-Dateien sind per SHA-256 unverändert. Die während der Arbeit neu hinzugekommenen 25 Incoming-GLB bleiben ebenfalls unverändert und unversioniert. Keine neue Map, kein Worktree, keine Projektkopie, keine zusätzliche Vollsicherung und kein Original-Asset-Reimport. Landschaft, Heilhaus, Kamera, Beleuchtung, Schatten und TAA bleiben unverändert.

## 6. Fehler, verworfene Stufen und Warnungen

- Der erste Aufnahmezugang war durch einen natürlichen Wildkampf gesperrt. Aufnahmen der falschen Szene verworfen; der Prüftreiber kontrolliert jetzt jeden Zugang.
- Positionsargumente von Unreals Python-`Rotator` entsprachen nicht der angenommenen Achsenreihenfolge. Die betroffenen frühen Vorführungen sind ungültig; feste Ansichten benutzen ausdrücklich `pitch=`, `yaw=`, `roll=`. Keine gespeicherten Assets wurden dadurch gekippt.
- Gluraks erstes neues Material hatte einen bestätigten `Linear Color`-/`Masks`-Samplerfehler für die MetallicRoughness-Textur. Vor Übernahme korrigiert. Der graue Glurak-Teil von `V6Refinements03` ist kein Abnahmebeleg; der separate Machomei-Videoausschnitt daraus ist gültig. Endgültiger Glurak-Nachweis: `V6GlurakFinal04` und `AlignedAB07`.
- Erster voller Fußlauf meldete beim zusätzlichen Gengar-Kampf eine Wegblockade; der historische Prüfhelfer behandelte einen nötigen Teamwechsel nicht. Nur Testtreiber korrigiert: legale Flucht/erzwungener Wechsel und pausierter Geh-Watchdog während realer Kämpfe. Zweiter Lauf bestanden; nach letzter Player-Korrektur nochmals vollständig bestanden.
- Ein neuer Swift-Compilerlauf blieb in der Typauswertung hängen. Nur eigene Compilerprozesse beendet; vorhandenen lokalen AVFoundation-Encoder erfolgreich wiederverwendet. 14 echte kurze Vergleichsvideos erstellt. Kein Erfolg einer portablen Neuübersetzung behauptet.
- Python-Skeletonzugriff beim eigenen unpublizierten Player-Reimport korrigiert; ausschließlich die betroffene eigene Animationsdatei fertig gespeichert, ursprüngliches Skeleton nicht gespeichert.
- Externe Engine-Warnungen: ARM-Startfehler 86 des installierten `idevice_id`-Hilfsprogramms sowie bekannte frühe Engine-Automation-Startmeldungen. Getrennt von der ausdrücklich gestarteten Projekt-Suite; beide vollständigen Projekt-Automationläufe enden 99/99 ohne Testwarnungen.
- Vorhandene Umweltmaterial-Usage-Warnungen, soweit im Battleaufbau ausgegeben, werden nicht durch ungefragte Änderungen an Weltmaterialien versteckt. Kein neuer verbleibender V6-Shader-Kompilierungsfehler in der abschließenden Sitzung.

## 7. Git-Sicherung und Abnahme

Umsetzungscommit `3407e609a1a5c2bdc8baf813be9612c0861f98cb`: 133 gezielt geprüfte Pfade. Index vollständig gegen Plan und Arbeitsdateien geprüft, `git diff --cached --check` bestanden. 95 eindeutige LFS-Objekte mit **201.023.205 Bytes** (ca. 0,187 GiB), alle lokalen Objektprüfsummen korrekt. Größte neue Datei 35.929.780 Bytes. Normales Git-Paket als obere Schranke gemessen: **457.712 Bytes**, deutlich unter 1 GiB. Keine Medien/Caches/Builds/Incoming-Neuzugänge im Commit.

Der LFS-Dry-Run nennt genau diese 95 Pfade. **Es fand bisher kein Push und kein LFS-Upload statt.** `origin/main` bleibt auf `ee6dcaf9921cd387a55e3add66539734e45444d5`. Die lokale schlanke main-Historie enthält vor V6 etwa 7,25 GiB eindeutige erreichbare LFS-Objekte; daraus folgt keine zuverlässige Aussage zur gesamten aktuellen Kontonutzung oder verbliebenen Bandbreite.

GitHub nennt für Free 10 GiB eingeschlossenen LFS-Speicher/Downloadbandbreite; Überziehungen können abhängig vom Kontobudget kostenpflichtig sein. Die aktuelle Kontoseite ist in der verfügbaren Browseroberfläche nicht angemeldet, `gh` ist nicht installiert. Die bereits erteilte Push-Freigabe fehlt nicht; erforderlich ist die angefragte aktuelle kostenlose Kapazitätsangabe. Keine Käufe oder Budgetänderungen vorgenommen. Quellen: [GitHub LFS-Abrechnung](https://docs.github.com/en/billing/concepts/product-billing/git-lfs), [Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

Das Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unverändert über beide bisherigen lokalen Verweise erreichbar und ist kein Vorfahr der schlanken main-Historie. Keine History-Rewrites, Resets, Bereinigung oder neuen Backup-Verweise.

**Empfehlung:** Technisch brauchbarer Verbesserungsstand; zur visuellen Abnahme insbesondere Player-Seitenprofil, Glurak-Flügelwurzeln, enge Wendungen und Gaswirkung anhand der Videos prüfen. Keine uneingeschränkte Freigabe als endgültiger Animationsreferenzstand. Keine weiteren Pokémon oder Landschafts-Art-Pässe begonnen.

Zugang zur eigenen Prüfung: gewöhnliches Play in VisualV2, Output Log auf **Cmd**, `pm.TestGround.Go`, optional Nummer 1–10, `pm.TestGround.Mode idle|walk|run|auto`, Rückkehr `pm.TestGround.Return`. Bestehende Controllerbelegung wird nicht überschrieben.
