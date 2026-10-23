# Animationsfeinschliff V6.1 – Prüfbericht

Stand: 23.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, vorhandene `/Game/Maps/Dev_TestMap_VisualV2`.

**Ergebnis:** Der große Verbindungsstreifen zwischen Hosenrückseite und Mantelsaum ist behoben. Gluraks äußere Flügelwurzeln erscheinen in der finalen Unreal-Rückansicht orange. Eine kleine Laufzeitkorrektur verbessert die Standkontakte des Players. Der Stand ist ein technisch geprüfter Zwischenstand mit ausdrücklich verbleibenden Grenzen bei verdeckten Meshy-Nähten, Extremposen und Aufnahmehitches.

## 1. Nachgewiesene Ursachen und Änderungen

### Player: Mantel und Hose

Der frühere pauschale Koordinatenfilter für den hinteren Mantelbereich hatte zusammenhängende **braune Hosenflächen** an `cape_*`-Bones gebunden. Benachbarte Hosenvertices folgten dagegen Schienbein beziehungsweise Oberschenkel. Beim Beugen wurde dadurch die Hosenrückseite bis zum Mantelsaum gespannt. Die Prüfung erfolgte in Ruhe-/Idle-, Walk- und Run-Posen, anhand echter Kanten, Texturfarben, zusammenhängender Flächen und früherer Quellen. Kein pauschaler Schluss allein aus UV-Naht-/Boundary-Zahlen.

1.142 betroffene Vertices werden wieder den passenden Bein-/Beckenbereichen zugeordnet. Zusätzlich glätten 132 Einträge den abrupten Links-/Rechtswechsel im echten Hosenschritt; wegen einer Überschneidung sind insgesamt **1.273 unterschiedliche Vertices** geändert. Flächenweise Medianfarben statt einzelner Atlas-Randpixel verhindern die Spitzen der verworfenen ersten Gewichtsvariante.

An der zuvor auffälligsten gemessenen Kante, Vertices 3501/3272, beträgt die Längenvergrößerung gegenüber der Ruhegeometrie:

| Diagnosepose | V6 | V6.1 |
|---|---:|---:|
| Idle | 17,66× | 1,007× |
| Walk | 62,99× | 1,028× |
| Run | 90,36× | 1,032× |

Das ist eine örtliche Dehnungsmessung dieser nachgewiesenen Fehlstelle, keine Perfektionsaussage über das gesamte Mesh. Geometrie, UVs, Materialzuordnung, Gesicht, Haare, Kleidungsgestaltung, Rest-Rig und alle V6-Animationskurven bleiben unverändert. Die vorhandenen Mantel-Bones, gebackene Walk-/Run-Bewegung und verzögerten Turn-/Stop-Springs bleiben erhalten und bewegen nun die richtigen Kleidungsflächen. Keine Cloth-Simulation und keine Neumodellierung.

### Player: Fußkontakte

Im vorhandenen Drei-Clip-Animator wird nach dem bestehenden Blend eine begrenzte Zweibein-IK über die Engine-Funktion `AnimationCore::SolveTwoBoneIK` angewendet. Keine neue Animationsgraph- oder Bewegungsarchitektur. Zwei einfache Bodenabfragen erfolgen im Game-Thread; die Poseauswertung verwendet nur vorbereitete Daten. Standfüße behalten begrenzt ihre Weltposition/-ausrichtung. Enge Drehungen, fehlender Boden, Teleports und lange Frameabstände lösen die Bindung, bevor Beine stark verdreht oder gestreckt würden. Korrektur höchstens 12 cm, lokale Bodenhöhenanpassung höchstens ±8 cm; kein Limb-Stretching.

Zusätzlich wird der tatsächliche CharacterMovement-Abstand der Kollisionskapsel zum Boden ausschließlich am visuellen Mesh ausgeglichen: auf dem ebenen Testboden ungefähr **2,15 cm**. Kapsel, Actorposition, Kamera, Steuerung und Geschwindigkeiten **210/315 cm/s** bleiben unverändert. `pm.PlayerFootIK 0|1` dient nur der reversiblen Diagnose, Standard 1.

Eine eigene räumliche Prüfung ohne Screenshot-Readbacks verwendete dieselbe reale Enhanced-Input-Folge mit acht Geh-/Sprintrichtungen, Start/Stop und engen Wechseln. Die folgende Kennzahl umfasst ausschließlich stabile, annähernd gerade Standphasen mit begrenztem Frameabstand; Übergänge und enge Wendungen sind ausdrücklich ausgeschlossen:

| Messung der Fuß-Bone-Bewegung | V6-Verhalten | V6.1 |
|---|---:|---:|
| Auswertbare Standintervalle | 197 | 203 |
| Median horizontales Rutschen | 1,449 cm/s | <0,001 cm/s |
| P95 horizontales Rutschen | 5,587 cm/s | <0,001 cm/s |
| Median Knöchelhöhe über ebenem Boden | 10,790 cm | 8,661 cm |

Knöchelhöhe ist keine Messung jedes Sohlenvertices. Keine Behauptung vollständigen Foot-Lockings in allen Übergängen und Geländeformen. Dies ist eine räumliche Animationsprüfung, **kein FPS-Benchmark**. Rohdaten: `Saved/AnimationCorrectionsV61/FootContactComparison.json`.

### Glurak: äußere Flügelwurzeln

Die dunklen Stellen waren ursprüngliche blaue Texturbereiche, die von der vorhandenen Rückseiten-Farbmaske ausgelassen wurden. Der V6-Filter verlangte einen Flügel-Bone-Einfluss; dieser liegt am Ansatz teilweise bei null. Ein zu enger Orts-/Farbfilter ließ danach noch eine schmale Restkante übrig. Diese wurde gesondert geprüft: weitere **312 echte Außenflächen**, nicht die geschützte Innenseite.

Die finale Maske ergänzt insgesamt **1.871 äußere Wurzelflächen**, geprüft über UV-Farbe, Flächenorientierung sowie tatsächliche Front-/Rück-/Rückaufsicht mit BVH-Strahlen. Keine blickabhängige Materialumschaltung und keine globale Orangefärbung. Originaltexturen, UVs, Normalen, Materialslots, Körper, Schwanz und die dunklen inneren Membranflächen bleiben erhalten. Das vorhandene V6-Material wird wiederverwendet; geändert wird ausschließlich seine lokale Vertexfarbenmaske im neuen Mesh.

Alle sieben normalen Clips sowie Takeoff/Hover/Land bleiben **dieselben Unreal-Assets**, auf exakt demselben Skeleton. Tatsächlich aufgezeichnet: Grounded → Takeoff → Hover → Landing → Grounded, maximal 94 cm Lift. Schwanzflamme erhalten.

## 2. Quellen, Assets und Integration

| | Player | Glurak |
|---|---|---|
| Bearbeitbare Quelle | `Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationCorrections_V61.blend` | `Art/Characters/Creatures/Glurak/Source/Glurak_AnimationCorrections_V61.blend` |
| Meshtransport-FBX | `Art/Characters/YoungTrainer/Exports/AnimationV61/Player_Idle.fbx` | `Art/Characters/Creatures/Glurak/Exports/AnimationV61/Glurak_Idle.fbx` |
| Unveränderte Geometrie | 52.699 Vertices / 47.744 Dreiecke | 135.600 Vertices / 246.066 Dreiecke |
| Blender-Rig | 25 Bones, unverändert | 24 Bones, unverändert; Unreal-Importroot wie V6 |
| Referenzhöhe | 140 cm | 170 cm |
| Neues Unreal-Mesh | `/Game/Characters/YoungTrainer/AnimationV61/SK_Player_V61` | `/Game/Characters/Creatures/Glurak/AnimationV61/SK_Glurak_V61` |

Beide Quellen erneut geöffnet und beide FBX tatsächlich nach Blender zurückimportiert. Alle dateibasierten Texturen gepackt. Originalgeometrie, UVs, Material-Flächenzuordnung, Rest-Bones und sämtliche bisherigen Aktionskurven gegen V6 verglichen. Gluraks Gewichte sind ebenfalls unverändert. Die Höhe einer animierten Idle-Pose ist von der unveränderten Referenzhöhe zu unterscheiden.

Player erhält ausschließlich den neuen Meshverweis im bestehenden nativen VisualComponent; V2-Skeleton und V6-Idle/Walk/Run bleiben. Glurak verwendet `/Game/Characters/Creatures/Glurak/AnimationV61/DA_Glurak_Presentation_V61`; nur der Präsentationsverweis in `DA_Glurak` wird gewechselt. Keine neuen Spezies-IDs, kein Saveformatwechsel, keine neuen Clips und keine Mapänderung.

Benötigte Werkzeuge: [README](/Users/harry/Developer/PokeMonster/Tools/AnimationCorrectionsV61/README.md). Kompakte Rohdaten-/Medienquittung: [Acceptance.json](/Users/harry/Developer/PokeMonster/Tools/AnimationCorrectionsV61/Acceptance.json). Einmalige Aufbau-/Importwerkzeuge verweigern vorhandene veröffentlichte Ziele; keine Originalassets erneut importieren.

## 3. Echte Unreal-Vergleiche und Videos

Alle verlinkten Originalbilder sind echte **2560 × 1440**-Unreal-Framebuffers mit angeforderten 100 % Screen Percentage, aus der vorhandenen Spielkamera. Kein Konzeptbild und kein Blender-Rendering als Umsetzungsnachweis.

Sechs finale A/B-Paare in `Saved/AnimationCorrectionsV61/AlignedAB05`: Player Idle/Walk/Run sowie Glurak Front/Seite/Rücken. Für jedes Paar protokollierte Kamera- und Rotationsdifferenz **exakt null**. Player mit festen identischen V6-Clipzeiten, Glurak mit derselben Idle-Rolle. Die Standbilder isolieren Gewichts-/Farbänderungen; die Laufzeit-Fußkorrektur wird in Bewegung und der gesonderten räumlichen Prüfung beurteilt.

Die folgenden Bilder sind ausdrücklich nur identische Ausschnitte dieser QHD-Originale, zweifach mit Nearest Neighbor vergrößert, ohne Retusche oder erzeugte Details:

![Player Walk: V6 links, V6.1 rechts](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/DetailsFinal/PlayerWalkComparison.png)

![Player Sprint: V6 links, V6.1 rechts](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/DetailsFinal/PlayerRunComparison.png)

![Glurak außen: V6 links, V6.1 rechts](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/DetailsFinal/GlurakRearComparison.png)

**Echte kurze Bewegungsvideos, Originalzeiten und keine synthetischen Zwischenbilder:**

| Motiv | Vorher | Nachher |
|---|---|---|
| Player: Idle, acht Richtungen, Walk/Sprint, enge Wechsel, Start/Stop | [228 Frames, ca. 31 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/Media/BeforePlayer/Motion.mp4) | [229 Frames, ca. 31 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/Media/AfterPlayer/Motion.mp4) |
| Glurak: Ansichten, Flügelschläge, Bodenbewegung, Takeoff/Hover/Land | [466 Frames, ca. 53 s](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/Media/BeforeGlurak/Motion.mp4) | [427 Frames, ca. 53 s, finale 1.871-Flächen-Korrektur](/Users/harry/Developer/PokeMonster/Saved/AnimationCorrectionsV61/Media/AfterGlurak/Motion.mp4) |

Alle vier Videos selbst 2560 × 1440. Native Spielkamera, tatsächliche Enhanced-Input-/Testgeländebewegungen. Bewegte A/B-Läufe verwenden dieselbe Eingabefolge, sind aber nicht frame- oder phasengenau pixelidentisch. Readback-/Aufnahmehitches und ungleichmäßige Frameabstände bleiben sichtbar; dies ist kein Nachweis ungestörter 60-Hz-Wiedergabe. Standbilder allein werden nicht als endgültige Bewegungsabnahme gewertet.

Finale Player-Folge: `V61After01`; finale Glurak-Folge: `V61AfterGlurak02`. Die früheren Glurak-Bilder innerhalb `V61After01` sind durch die gesonderte abschließende Wurzelkorrektur ersetzt und kein finaler Glurak-Abnahmebeleg. Die Medienquittung enthält zur Nachvollziehbarkeit auch echte Zwischenaufnahmen. Rohbilder/-videos bleiben nur lokal unter Saved; nach frischem Clone neu erzeugen.

## 4. Kurze Prüfung aller zehn Pokémon

Gewöhnlicher PIE-Beginn mit dem bestehenden nativen dauerhaften Testgelände, kein Automation-Spawner und keine neue Map. Alle zehn Modelle in Front-/Seiten-/Rückansicht, mit Idle/Walk/Run und Übergängen erfasst: Glumanda, Schiggy, Bisasam, Pikachu, Myrapla, Enton, Machomei, Nebulak, Gengar, Glurak. 50 QHD-Bilder in `V61TenPokemon01`, Glurak danach mit finaler Maske gesondert vollständig nachgeprüft.

Aus der normalen Kamera kein weiterer neu belegter grober Fehler, der in diesem begrenzten Auftrag zuverlässig zusätzlich repariert werden musste. Keine erneute Gesamtanimation aller Arten. Nebulaks teilweise erkennbare skulptierte/facettierte Gashülle und begrenzte Extremposenabnahme bleiben bestehende Qualitätsgrenzen. Keine Behauptung, alle sieben Rollen aller zehn Arten seien vollständig künstlerisch freigegeben. Die übrigen neun Pokémon-Quellen und Präsentationen bleiben unverändert.

## 5. Technische und Gameplay-Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Finaler Mac Development Editor Build | `AnimationV61BuildFinal`, Exit 0, 11,1 s |
| Finale vollständige Automation | **101 Testzustände Success**, 0 Failed/NotRun/InProcess; davon 100 ohne Warnung, 1 mit den bekannten externen `idevice_id`-Warnungen |
| Strenger QA-Treiber | Verlangt null Testwarnungen und endet deshalb im letzten Lauf mit Exit 1. Nicht als warnungsfreier Gesamtlauf umgedeutet. Beide Meldungen betreffen das installierte ARM-inkompatible iOS-Hilfsprogramm, keine Projektassertion. |
| Vorheriger vollständiger sauberer Lauf | `AnimationV61Automation02`: 101/101, 0 Warnungen; vor der letzten vertikalen IK-Reihenfolgekorrektur. Finale Daten nicht allein damit abgenommen. |
| Neue Regressionen | Begrenzter Weltkontakt, sichere Freigabe bei Drehung/Hitch/fehlendem Boden, neue Schritte, exakte Skeleton-/Material-/Clip-Wiederverwendung |
| Alle elf Map Checks | 0 Fehler, 0 Warnungen; keine Karte gespeichert |
| Vollständiger PIE-Fußlauf | `AnimationV61FullFoot01`: **103 Schritte, 288,74 m, maximal 315 cm/s**, reale Enhanced-Input-Bewegungen, keine Testteleports |
| Fußlauf-Funktionen | Bewegung/Sprint, Wanderer/Dialog/Quest, Trainerkampf, Wildfang, Brücke/Wald/Wege, Heilhaus gerade/diagonal hinein/hinaus, Heilen, Speichern/Laden, Menüfokus bestanden |
| Glurak Begleiter/Kampf | `AnimationV61GlurakBattle`: echter 3D-Begleiter mit Walk/Sprint, beide ClassicBattle-Perspektiven, vorhandene Attack/Hit/Faint/Happy-Reaktionen und Rückkehr bestanden |
| Battle-Aufnahmen | Bestehende RenderTargets 2560 × 1080; LiveUI gesondert. Nicht als QHD-RenderTargets ausgegeben. Keine Änderung der Kampfkameras/-regeln. |
| Controller-Software im PIE | `AnimationV61SwitchPro`: **46 Checks** bestanden, darunter B/A, L3, X, L/R, Plus, Dpad, Tastatur, Dialog/Herausforderung, Beutel, Teamwechsel, Begleiterpause/-rückkehr und Save/Load |
| Physischer Controller | Bestehende bestätigte Grundbelegung unverändert; in dieser Aufgabe nicht erneut physisch geprüft. Simulation ist kein Hardwarebeweis. |
| Quellenprüfung | Beide finalen Blenderquellen und zwei echte FBX-Rückimporte bestanden; alle alten Kurven/UVs/Rest-Rigs erhalten |
| Editorübergabe | VisualV2 geladen, kein PIE, keine schmutzigen Karten-/Inhaltspakete; aktive V6.1-Meshes, alle zehn Originalhöhen und bestehendes map-eigenes TAA-Blendable überprüft |

Die Begleiterstatistik des vollständigen alten Test-Water-Fußlaufspielstands ist kein positiver 3D-Begleiternachweis. Dafür dienen ausdrücklich die Glurak-Präsentationsfixture und die Controller-Prüfung mit klar benanntem Dreistarter-Testteam. Diese isolierten Fixtures sind wiederum keine natürlich entstandene Habitatbegegnung.

Der erste Build wurde durch einen Unity-Build-Bezeichnerkonflikt zweier vorhandener `Names`-Variablen gestoppt. Ausschließlich die Konstante des Testgeländes in `DevelopmentSpecimenNames` umbenannt, keine Funktionsänderung. Bekannte externe Engine-Start-/iOS-Warnungen und die strenge QA-Auswertung bleiben in den Rohlogs erhalten. Keine Warnungsfilter oder Änderungen am Engine-Installationsverzeichnis.

## 6. Verbleibende Grenzen und Schutz

- Die großen sichtbaren Hosenstreifen sind beseitigt. Kurze verdeckte Hüftnaht-Kanten bleiben in der analytischen Extremposenprüfung auffällig, bis ungefähr 26× an millimetergroßen Ausgangskanten. Keine vollständige topologische Trennung sämtlicher Meshy-Kleidungsnähte behauptet. Eine weitere manuelle Naht-/Topologiereparatur wäre gesonderte Arbeit.
- Bei engen Pivots, abrupten Wechseln und unebenem Gelände sind kleine Restbewegungen möglich. Die begrenzte IK gibt Kontakte absichtlich frei, statt Knie zu verdrehen. Keine vollständige Sohlen-/Geländerotation und keine Mantel-Körper-Kollisionssimulation.
- Vier echte Videos liegen vor; Aufnahmehitches begrenzen die endgültige Beurteilung flüssiger Bewegung. Die visuelle Abnahme soll zusätzlich beim normalen PIE-Laufen erfolgen.
- Keine erneute umfassende Abnahme aller Extremposen aller zehn Arten. Keine neuen Pokémon, Modelleingänge oder Landschafts-/Heilhausänderungen.

**Unverändert:** 1.848 ursprüngliche Art-/Map-/Config-Dateien per SHA-256, sämtliche Original-Meshy-Dateien, alle bisherigen Blender-/V6-Stände, alle elf Maps, Weltbeleuchtung, Kamera, Controllerzuordnung und Gameplay. Alle 25 aktuellen unversionierten Incoming-GLB sind unverändert und vom Commit ausgeschlossen.

Nach allen schreibenden Tests der ursprüngliche Dev-Slot bytegenau restauriert: SHA-256 `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt über beide bestehenden lokalen Verweise unverändert erreichbar und ist kein Vorfahr der schlanken main-Historie. Keine neuen Maps, Worktrees, Projektkopien oder Vollbackups; keine Lösch-/Reset-/Prune-Aktion.

## 7. GitHub-Sicherung

Ausgangspunkt: `b2c6a990de7ebefda81cea69292f42812a4fad47`, direkt auf GitHub bestätigt; auch `3407e60` ist damit enthalten. Der historische V6-Bericht mit seinem damaligen ungepushten Stand wird nicht rückwirkend umgeschrieben.

Umsetzungscommit **`3200a16c20186a79e8267a156a577b8beb3a4cdb`**, `fix: decouple player clothing and complete Glurak wing roots`: 43 exakt gegen den Plan geprüfte Pfade. Acht LFS-Objekte mit **105.541.747 Bytes**, lokale Pointer-/Objekt-SHA-256 geprüft. Normales Git-Paket als obere Schranke **622.784 Bytes**. Keine Kontrollmedien, Caches, Builds oder Incoming-Neuzugänge im Commit. `git diff --cached --check` und erforderliches Kernmanifest bestanden.

Regulärer Push erfolgreich, ein Uploadversuch. `origin/main` direkt auf `3200a16c20186a79e8267a156a577b8beb3a4cdb` bestätigt; danach alle **acht Remote-LFS-Objekte tatsächlich heruntergeladen und ihre SHA-256-Prüfsummen verifiziert**, zusammen 105.541.747 Bytes. Nach diesem Push `main...origin/main = 0/0`. Kein Quota-/Kostenfehler gemeldet, keine Käufe oder Budgetänderungen. Ein Kontorechnungszähler wurde nicht ausgelesen; die Bytezahl ist der nachgewiesene Objektumfang.

Dieser Abschlussbericht und sein Kernmanifest-Eintrag werden anschließend als eigener kleiner Dokumentationscommit regulär gesichert. Der abschließende Hash steht in der Abschlussantwort beziehungsweise in `git log -1`; er kann nicht sinnvoll im selben Dokument als eigener Inhalts-Hash vorweggenommen werden. Versionierte Dateien sollen danach sauber bleiben; die 25 geschützten Incoming-Dateien bleiben unversioniert.

## 8. Visuelle Abnahme

Empfehlung: als verbesserten, technisch geprüften Zwischenstand visuell abnehmen; keine uneingeschränkte Perfektionsfreigabe aller Animationen. Besonders enge Wendungen, verdeckte Mantelnähte und Sprint aus der Seite im normalen Spiel ansehen.

Zugang: gewöhnliches Play in VisualV2, Output Log auf **Cmd**, `pm.TestGround.Go`, optional Station `10` für Glurak. `pm.TestGround.Mode idle|walk|run|auto`, zurück mit `pm.TestGround.Return`. Keine Controller-Tasten überschrieben.
