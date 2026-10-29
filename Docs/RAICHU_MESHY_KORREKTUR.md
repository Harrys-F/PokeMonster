# Raichu – verbindliche Meshy-Korrektur

Stand: 29.10.2026. Ausgangspunkt `3b2e1baa84dc88bf2c202014ba7748c406cc27d8`, einschließlich `67476bc2` und `5840ee63`. Die frühere Modellentscheidung ist ersetzt. **Das aktive Raichu stammt jetzt ausschließlich aus Harrys Meshy-Original. Das selbst erstellte Modell und seine exklusiven Quellen/Assets wurden tatsächlich aus dem Arbeitsstand entfernt.**

## Anlass und verbindliche Quelle

Der frühere Commit `67476bc2` enthielt laut eigener README ausdrücklich einen in Blender selbst modellierten Kandidaten (`BuildRaichu.py`, anschließend sieben Animationen und sechs Materialien). Das erklärt die nachweisbare Herkunft; es war kein importiertes Meshy-Raichu. Diese Verwendung entspricht Harrys nun ausdrücklich verbindlicher Meshy-Regel nicht. `AGENTS.md`, `Docs/GRAFIKSTIL.md` und `Docs/ENTSCHEIDUNGEN.md` halten die Regel dauerhaft fest. Es gibt keine Prototyp-Ausnahme für selbst erzeugte Pokémon.

Zu Beginn lag keine eindeutig identifizierte Raichu-Quelle in Incoming. Nach der Rückfrage stellte Harry `Art/Characters/Creatures/Incoming/Raichu.glb` bereit. Name, tatsächliche Front-/Seiten-/Rückansichten und Geometrie wurden geprüft; kein anderes Modell dient als Ersatz.

- Quelle: `Art/Characters/Creatures/Incoming/Raichu.glb`, 5.478.044 Byte.
- SHA-256: `e41d212e1fd8500275067f3953a9709a4a2eaa07dc4c4e006954768dca6c5b64`.
- Ein Mesh, 17.144 importierte Vertices, 21.351 Dreiecke, ein ursprüngliches Material, drei eingebettete JPEGs (BaseColor, Metallic/Roughness, Normal), eine UV-Ebene. Keine gelieferten Bones oder Animationen.
- Das GLB bleibt bytegleich. Arbeitsquelle: `Art/Characters/Creatures/Raichu/Source/Raichu_Meshy_V1.blend`; darin zusätzlich die unveränderte, ausgeblendete GLB-Referenz. Keine neue Körpergeometrie, kein Remesh, keine Dezimierung, keine neue Modellgestalt.

## Technische Integration

Bestehende CreatureExpansionV3-Pipeline um Raichu-Parameter erweitert. Andere Arten behalten ihre bisherigen Standardwerte und unveränderten Arbeitsquellen/Exports/Assets. 27 anatomisch angepasste Blender-Bones mit Beinen, Armen, Ohren und neun Schwanzsegmenten. Meshy-Geometrie, UVs und Originaltexturen bleiben erhalten; normalisierte Gewichte mit maximal vier Einflüssen. Harte lokale Skinninggrenzen an Pfoten und Blitzansatz wurden anhand deformierter Kanten nachgewiesen und durch kontinuierliche Übergänge sowie virtuelle Gewichtsglättung korrigiert. Die virtuelle Schweißung verändert keine Geometrie.

Neutralhöhe einschließlich Ohren 80 cm gegenüber 140 cm Spielfigur; Actor-Skalierung bleibt 1. Lauf-/Gehreferenz 55/28 cm/s. Die T-Pose-Arme werden im Animationssystem abgesenkt, nicht neu modelliert. Sieben in-place Rollen: Idle, Walk, Run, Attack, Hit, Faint, Happy. Der vorhandene Vorwärtssturz hält die tiefste deformierte Oberfläche am Boden. Die gelieferten Schwanzschlaufe und flache Blitzform bleiben erhalten.

Aktive Pfade:

- Art: `/Game/Data/Creatures/DA_Raichu.DA_Raichu` (ID Raichu, Dex 026 unverändert).
- Präsentation: `/Game/Characters/Creatures/Raichu/MeshyV1/DA_Raichu_Meshy_Presentation`.
- Mesh: `/Game/Characters/Creatures/Raichu/MeshyV1/Meshes/SK_Raichu_Meshy`.
- Eigenes Skeleton im selben Meshes-Verzeichnis; sieben `Animations/A_Raichu_*`.
- Ein `Materials/M_Raichu_Meshy`, drei `Textures/T_Raichu_*`; BaseColor sRGB, Normal mit Unreal-Normalkartenimport, G/B des MR-Originals für Roughness/Metallic. Keine Änderungen an gemeinsam verwendeten Materialien.
- Quellexporte `Art/Characters/Creatures/Raichu/Exports/MeshyV1/Raichu_*.fbx`, Original-JPEG-Extrakte unter `Textures/MeshyV1`.

Nur das Visuals-Feld des stabilen Artenassets wurde ersetzt. Vergleich vor/nach Import bestätigt unveränderte Art-ID, Name, Dex, Typen, Geschlecht, Startlevel, Gen-2-Werte (60/90/55/90/80/100), Fangrate, Wachstum, EP-Ertrag, Lernliste, Entwicklungsregeln und Oberweltparameter. Kein neues Saveformat und keine neue Entwicklungs-, Kampf-, Begleiter- oder Registrierungslogik. Save-Schema bleibt 11.

## Tatsächlich entfernte Dateien

32 zuvor versionierte exklusive Dateien und zwei eindeutig exklusive lokale Saved-Hilfsskripte, insgesamt 34. Vor dem Entfernen wurden Referenzen ersetzt, der genaue Dateisatz und seine SHA-256-Werte festgehalten. Die 16 Unreal-Pakete wurden über die Assetverwaltung nach Prüfung externer Referenzen gelöscht; anschließend wurden die exakt abgeglichenen übrigen Dateien entfernt. Keine bloße Deaktivierung.

| Ursprüngliche Datei | Maßnahme | Ergebnis |
|---|---|---|
| `Art/Characters/Creatures/Raichu/AnimationAudit.json` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Attack.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Faint.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Happy.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Hit.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Idle.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Run.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Exports/V4/Raichu_Walk.fbx` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/ModelAudit.json` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Art/Characters/Creatures/Raichu/Source/Raichu_V4.blend` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Attack.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Faint.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Happy.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Hit.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Idle.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Run.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Animations/A_Raichu_Walk.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/DA_Raichu_Presentation.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Brown.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Coat.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Cream.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Eyes.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Gold.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Materials/M_Raichu_Highlight.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Meshes/SK_Raichu_V4.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Content/Characters/Creatures/Raichu/V4/Meshes/SK_Raichu_V4_Skeleton.uasset` | Gelöscht | Dateisystem: nicht vorhanden; AssetRegistry: nicht vorhanden, keine Referenz |
| `Tools/ModelsV4/BuildRaichu.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Tools/ModelsV4/AnimateRaichu.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Tools/ModelsV4/ImportRaichu.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Tools/ModelsV4/RenderSource.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Tools/ModelsV4/RenderMotionSource.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Tools/ModelsV4/ValidateSource.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Saved/ProjectRefinement/ModelsV4/ReviseFaint.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |
| `Saved/ProjectRefinement/ModelsV4/RefreshOwnFaint.py` | Gelöscht | Dateisystem: nicht vorhanden; SHA-256 vor Entfernung abgeglichen |

Gemeinsam verwendete Bestands-/Gameplaywerkzeuge bleiben erhalten. Der allgemeine historische `Saved/ProjectRefinement/ModelsV4/WriteReport.py` wurde nach separater Inhaltsprüfung nicht in die exklusive Löschliste aufgenommen. Er ist kein Modellgenerator, aber als alter Berichtschreiber wegen entfernter Quellen nicht mehr verwendbar. Frühere Screenshots/Prüfmedien können die alte Darstellung zeigen; sie sind weder Modellquellen noch aktive Spielassets. Keine anderen Pokémon, gemeinsamen Skelette oder Materialien gelöscht.

## Abschließende Referenz- und Dateiprüfung

- Tatsächliche AssetRegistry vollständig eingelesen, darunter in einem frisch gestarteten separaten Spielprozess. Alter Namensraum `/Game/Characters/Creatures/Raichu/V4`: **0 Assets**.
- Alle 16 alten Paketnamen ausdrücklich auf Referenten geprüft, auch nachdem die Pakete fehlen: **keine harten, weichen, Such- oder Verwaltungsreferenzen**. Aktive Art zeigt auf SK_Raichu_Meshy. Keine Redirector-/Altmodell-Pakete im alten Verzeichnis. Ergänzende Dateinamensuche über den Arbeitsbaum: keine Raichu_V4-Modell-/Assetdateien.
- Modelltestgelände, Entwicklungsenthüllung, Kampf und Begleiter verwenden die bestehende Artregistrierung und deshalb die neue Meshy-Präsentation; tatsächlich im Spiel und durch Assetpfade geprüft.
- Alle 34 entfernten Pfade nochmals geprüft: nicht vorhanden. Zusätzlicher Scan von 51567 Arbeitsdateien: 39 gleich große Kandidaten gegen die ursprünglichen Datei-Hashes geprüft, **keine umbenannte Kopie**.
- `.git`, historische Commit-/LFS-Objekte und die geschützten Vollbackup-Refs wurden ausdrücklich nicht bereinigt. Historische Wiederherstellbarkeit in Git bedeutet keine verbliebene aktive Projektdatei. Keine Historie umgeschrieben, kein LFS-Prune.

## Erneut ausgeführte Qualitätssicherung

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor Mac Development Build | Exit 0, 26.42 s |
| Vollständige relevante Automation / strenger ProjectQA-Wrapper | 309 bestanden; 0 mit Testwarnung, 0 fehlgeschlagen, 0 nicht ausgeführt; Exit 0 |
| Map Checks | Alle 12 bestehenden Maps, jeweils 0 Fehler / 0 Warnungen; keine Map gespeichert |
| PIE01 | 94 Schritte, 22 bestätigte Prüfungen, bestanden; 139.98 s |
| Native01 | 94 Schritte, 22 bestätigte Prüfungen, bestanden; 138.66 s |
| Restart01 | 5 Schritte, 3 bestätigte Prüfungen, bestanden; 20.16 s |
| Functional04 | 71 Schritte, 21 bestätigte Prüfungen, bestanden; 155.76 s |
| Travel01 | 2 Schritte, 3 bestätigte Prüfungen, bestanden; 27.09 s |
| Appearance08 | 16 Schritte, 5 bestätigte Prüfungen, bestanden; 50.17 s |

PIE01 und Native01 durchlaufen jeweils 94 Schritte mit 22 Prüfungen: reguläres Level-11-Pikachu aus einer bestehenden QA-Fixture, echte Beutel-/Team-Auswahl des Donnersteins, Angebot ohne frühen Verbrauch, Abbruch in der Sequenz, erneuter Versuch, absichtlich nicht beschreibbarer ausschließlich isolierter Test-Speicherordner, echte Rücknahme von Instanz und Stein, erfolgreiche Wiederholung mit genau einem verbrauchten Stein, vollständige Originalfarben-Enthüllung, AP-/Status-/Erfahrungs-/Instanzprüfung, andere Teammitglieder unverändert, identischer bestehender Begleiter-Actor mit neuem Modell, Teamsortierung, Save/Load, echte Bewegung in acht Richtungen, alle Testgeländemodi und sichere Rückkehr. Anschließend echte Habitatbegegnung, Raichu-Attacke mit genau einem AP-Verbrauch, regulärer Fang mit ausgewähltem MasterBall, aktualisiertes Team und Rückkehr des Begleiters. Keine behauptete Fangwahrscheinlichkeit aus diesem gezielt gesicherten MasterBall-Test.

Restart01 lädt den im vorherigen separaten Prozess gespeicherten weiterentwickelten individuellen Pokémon-/Inventarzustand in einem neuen Prozess exakt und stellt den Raichu-Begleiter wieder her. Appearance08 lädt zusätzlich eine bereits vor der Korrektur existierende Raichu-QA-Fixture: neue Meshy-Darstellung ohne Save-Migration. Functional04 prüft vorhandene NPC-Interaktion, bestehende Habitatgrenzen, Modelltest, tatsächlichen Heilhaus-Ein-/Austritt, Innenraum-Save/Load, Menüpause, sechs Tagesgrenzen einschließlich Mitternacht, Wildkampf mit Attacke/Flucht, Fang, Team-/Begleiterwechsel und vollständige Wiederherstellung der QA-Fixture. Travel01 führt reale Mapwechsel VisualV2 → Dev_TestMap → VisualV2 aus, mit identischem Team/AP und derselben zentralen Weltuhr.

Neue siebte ModelsV4-Automationsgruppe schützt Meshy-Provenienz und tatsächliche Entfernung. Vorhandene sechs Gruppen prüfen weiterhin Daten/Registrierung, Rig/Clips/80 cm, Donnerstein/GUID/AP, Save-Schema, echten Kampfschaden und Wiederverwendung des Visual-Actors. Alle anderen Projektgruppen wurden mit ausgeführt. Blender prüfte die tatsächlich erneut geöffneten sieben FBX-Dateien, Bones/Dreiecke, originale UVs, gepackte Bilder und Gewichtsnormalisierung.

### Getrennte Warnungen und Prüfgrenzen

Einige eigene frühe Aufnahmehilfen scheiterten an Python-API-Unterschieden (fehlende Referenten liefern None; Blueprint-interne Spawnfunktion ist nicht Python-exponiert; relative Rotation ist eine Eigenschaft). Diese Hilfsläufe sind **nicht bestanden** und bleiben unter Appearance01–03 nachvollziehbar. Appearance04 war technisch bestanden, aber für die endgültigen Bilder zu eng eingerahmt; der entfernte ursprüngliche Pikachu-Testplatz führte außerdem zur regulären Distanz-Ausblendung. Appearance05 bestätigte die unzureichende gemeinsame Sichtbarkeit der entfernten Originaltestplätze und ist nicht bestanden. Appearance06 war noch ohne ausreichende Beruhigungszeit des Begleiters nach dem Plattform-Teleport und erreichte den Bildsichtbarkeitsnachweis nicht. Die abschließende Aufstellung verwendet deshalb den regulären Raichu-Begleiter neben dem tatsächlich besuchten zentral registrierten Pikachu-Testexemplar; danach wird der originale Raichu-Testplatz besucht. Functional01 scheiterte bei der zweiten Begegnung am erneut ausgewählten Bisasam mit regulärem Cooldown nach Flucht; Functional04 verwendet einen anderen aktiven Gegner, ohne Begegnungsregeln zu umgehen. Functional02 erreichte den zweiten Kampf, stürzte dann bei einer Screenshot-Anforderung im Metal/Slate-Readback mit SIGSEGV ab (RHIReadSurfaceData, zuvor Drawable-/Viewport-Größenabweichung). Diese Ausführung ist nicht bestanden; die genaue Ursache bleibt offen. Functional03 scheiterte zusätzlich an der pauschalen Schwimmstreckenannahme (Garados 0 cm); diese nicht deterministische Zusatzprüfung wird nicht als bestanden gewertet und bleibt außerhalb der Raichu-Funktionsabnahme offen. Die Proben zeigen Garados im Zustand Rest/Idle ohne Bewegungsplan, innerhalb des Wasserlebensraums; daraus allein lässt sich kein Defekt oder dessen Ursache beweisen. Functional04 wiederholt die für Raichu relevanten funktionalen Schritte ohne diese artfremde Schwimmstreckenvorgabe und ohne Bildlesevorgänge, ohne Spiel- oder Renderinglogik zu ändern. Die eigentlichen Bildnachweise stammen aus den getrennten Aufnahmeläufen. Eine Behebung des Metal-Aufnahmeabsturzes wird ausdrücklich nicht behauptet. Korrigierte Aufnahmehilfe verwendet vorhandene Laufzeitkamera und vorhandene Exemplare; Appearance08 separat nachgeprüft. Keine Gameplay-/Engineänderung als Umgehung.

Der strenge Wrapper bewertet die exportierte PokeMonster-Testwarteschlange. Frühere Testzahlen wurden nicht übernommen. Engine-/Plugin-Startmeldungen außerhalb dieser Warteschlange sind davon getrennt: bekannte Condition-failed-Registrierungsmeldungen, experimentelle Python-Testtypen/Toolset-Definitionen, Plugin-/Layout- bzw. Python-Namenswarnungen und eine lange Startframe-Bewegungswarnung können im Rohlog stehen. Der absichtlich erzeugte isolierte Speicherfehler ist Teil der erfolgreichen Rücknahmeprüfung. Keine pauschale Behauptung eines völlig warnungsfreien Editorlogs. Externe iOS-Helferwarnungen gesondert geprüft; in den abschließenden Logdateien wurden keine idevice_id-/Bad-CPU-Meldungen gefunden. Die gesonderte Zählung steht in Saved/ProjectRefinement/RaichuMeshyCorrection/LogSummary.json.

Zusätzliche unveränderte Projektwarnung bei der Kampfkulisse: `MI_WLA_LeafOak` meldet ein fehlendes InstancedStaticMeshes-Usage-Flag und möglichen Default-Material-Ersatz. Das gemeinsame Material wurde in diesem Auftrag nicht geändert oder neu gespeichert. Die erfolgreichen Funktionsprüfungen sind keine Freigabe dieser bestehenden Materialwarnung.

## Echte Unreal-Bilder und visuelle Grenzen

Alle nachstehenden Aufnahmen stammen aus dem realen Metal-Spiel/PIE, 2560 × 1440, Profil C. Keine generierten Nachweisbilder.

| Nachweis | Lokaler Pfad unter Saved/ProjectRefinement/RaichuMeshyCorrection |
|---|---|
| Vorderansicht | `Appearance08/Meshy_Front.png` |
| Seitenansicht | `Appearance08/Meshy_Side.png` |
| Rückansicht | `Appearance08/Meshy_Back.png` |
| Normale Spielkamera / Begleiter | `Appearance08/Meshy_InGame_Buddy.png`, `Native01/Buddy_Village.png`, `Native01/Buddy_Forest.png` |
| Raichu neben echtem Pikachu-Exemplar | `Appearance08/Meshy_TestGround_Raichu_Pikachu.png` |
| Entwicklung / Abbruch / Team | `Native01/Stone_Complete.png`, `Stone_Cancelled.png`, `Team_Raichu.png` |
| ClassicBattle | `Native01/Raichu_ClassicBattle.png` |
| Neustart | `Restart01/Restart_Raichu.png` |

Nahansichten verwenden ausschließlich eine temporär eingerichtete Laufzeitkamera; die Standard-Spielkamera und Modellgrößen bleiben unverändert. Die Vergleichsaufstellung verwendet das vorhandene registrierte Pikachu-Testexemplar und den regulären Raichu-Begleiter aus der QA-Party. Nur für dieses Bild wird seine Bewegung pausiert und seine Position gesetzt; anschließend werden Bewegung und Kamera wiederhergestellt. Keine zusätzliche Map, keine neue permanente Figur. Kontrolle von Idle/Walk/Run/Turn/Directions/Auto/Reset und den vier Reaktionen im tatsächlichen Testgelände. In sehr nahen Unreal-Ansichten bleiben kleine Oberflächenfacetten und einzelne Dreiecks-/UV-Chart-Nähte sichtbar; eine vollständige Retopologie oder Textur-Neugestaltung wurde nicht vorgenommen. Originale Meshy-Oberflächenfacetten, UV-Chart-Nähte und die asymmetrisch modellierte Schwanzschlaufe sind erhalten. Eine abschließende künstlerische Bewegungs-/Materialfreigabe durch Harry und ein physischer Controller-Test werden nicht behauptet; Stillbilder ersetzen keine vollständige temporale Abnahme. Keine hochwertige 30-FPS-Videoabnahme oder allgemeine neue Performancemessreihe behauptet.

## Projektschutz, Rendering und Erweiterbarkeit

Hash-Baseline von 5.999 zuvor vorhandenen versionierten/geschützten Dateien und 595 vorhandenen .sav-Dateien. Alle 595 vorbestehenden Saves und alle 34 zuvor geschützten unversionierten Dateien sind bytegleich. Incoming-Raichu ebenfalls bytegleich seit Bereitstellung. Andere Pokémon-Modelle/Animationen, alle bestehenden Maps, Backups und Rendering-/Gameplayquellen bleiben unverändert. Die bereits vor Beginn lokal geänderte `Config/DefaultEngine.ini` bleibt exakt erhalten und wird nicht mitcommittet.

Kontrollierte Laufzeitwerte unverändert: Software-Lumen `r.Lumen.HardwareRayTracing=0`, IFG `r.Lumen.FinalGatherMethod=0`, TAAU=1, Screen Percentage=75, VSM-Richtungsstrahlen=4, 120 reale Minuten/Spieltag. Es wurden keine neuen Wildspawnregeln, Arten oder Controllerbelegungen eingeführt. 19 Modelle bleiben zentral registriert; Raichu erscheint automatisch im vorhandenen Testgelände.

Bestehende Bedienung: `pm.TestGround.Go Raichu`, `pm.TestGround.Mode idle|walk|run|turn|directions|auto`, `pm.TestGround.React attack|hit|faint|happy`, `pm.TestGround.Reset`, `pm.TestGround.Return`. Im normalen Spiel Pikachu im vorhandenen Beutel mit Donnerstein auswählen; B/Enter bestätigen, A/Escape zum vorgesehenen Zeitpunkt abbrechen. Keine zweite Entwicklungslogik.

## Nachweisdateien und Git-Abschluss

Unter `Saved/ProjectRefinement/RaichuMeshyCorrection`: SourceDiscovery/SourceIntake, Replacement, RemovalPlanFinal, RemovalResults, AssetDeletion, ReferencesBefore/After, FilesystemFinal, Protection, MapCheckResults und jeweilige Result-/Engine-Logs. Blender-Endprüfung unter `Saved/CreatureExpansionV3/RaichuMeshyCorrection04/Result.json`. Build/Automation unter `Saved/ProjectRefinement/RaichuMeshyBuild01` und `RaichuMeshyAutomation02`. Große Prüfmedien bleiben lokal und werden nicht hochgeladen.

Dieses Dokument gehört zum gezielten Korrekturcommit. Commit-ID und abschließender Remote-/LFS-Nachweis werden nach dem normalen Push im Chat und lokal in `Saved/ProjectRefinement/RaichuMeshyCorrection/GitFinal.json`/`RemoteLFS.json` festgehalten. Die vorhandene Nutzer-INI und 34 unbeteiligten unversionierten Dateien sind ausdrücklich nicht Teil des Commits. Keine Backup-Refs gepusht, keine Budgets/Zahlungen verändert.
