# Biom-Testmap V1 – Prüf- und Sicherungsbericht

Technische Prüfung: 23.10.2026. Gezielte Git-Sicherungsprüfung: 24.10.2026.
Projekt: `/Users/harry/Developer/PokeMonster`, UE 5.8.2, macOS / Apple M4.
Ausgangsstand: `4a530610121981a558fcaf9efe2c7cf0b75d281e` auf `main` und dem am 24.10. abgefragten `origin/main`.

## Umfang und Einstieg

Die ausdrücklich beauftragte neue, separate Karte `/Game/Maps/Dev_BiomeTestMap_V1` ist dauerhaft gespeichert und mit gewöhnlichem **Play / Selected Viewport** begehbar. Keine Automation oder Konsolenaktivierung zum Start erforderlich. Vorhandenes Projekt öffnen, Karte im Content Browser laden, Play drücken. Zugang und Werkzeuge: `Tools/BiomeTestV1/README.md`.

Die Karte umfasst vier ungefähr 44 m große Bereiche auf einer 104 × 104 m großen Geländequelle. Das beschriftete Zentrum verbindet die Gebiete; Richtungen beziehen sich auf die Spielkamera.

| Bereich | Lage | Inhalt |
|---|---|---|
| Wiese / Waldrand | links oben | Bisasam 0,70 m, Pikachu 0,40 m; eigene freie Glurak-Lichtung, 1,70 m |
| Bach / Teich | rechts oben | Schiggy 0,50 m und Enton 0,80 m am kontinuierlich abgesenkten Ufer; Holzbrücke; grüner Wasser-Prüfkörper |
| Felsen / Höhlenschnitt | links unten | tatsächlich 3 m hohe begehbare Plattform mit Machomei 1,60 m; offener Höhlenschnitt mit Glutexo 1,10 m |
| Wald / Ruine | rechts unten | Nebulak 1,30 m im Wald; begehbare offene Ruine mit Gengar 1,50 m |

Neun echte Pokémon plus ein ausdrücklich beschrifteter technischer Marker; der Marker ist **kein Goldini**. Keine neuen Pokémon-Modelle erstellt. 103 Bäume und 2.441 instanzierte Pflanzen-/Bodendetails verwenden vorhandene Grafikquellen. Kamera und 1,40-m-Spielfigur stammen aus dem vorhandenen Character; FOV 35, Spring Arm 2.850 cm, Pitch −50°, Yaw −45°.

## Umsetzung und Isolierung

- Neue native Klassen `APokeMonsterBiomeHabitat` und `APokeMonsterBiomeTestGameMode` speichern die Habitatkonfiguration in dieser Karte. Bei normalem PIE erzeugte Testexemplare sind transient, ohne persönliche Team-/Save-Identität und ohne Fang-/Kampfinteraktionen.
- Das vorhandene Roaming und seine Weg-/Kollisionsprüfung werden wiederverwendet. Der zusätzliche Habitatverweis ist auf bisherigen Karten null; die dortige Bewegung bleibt unverändert.
- Explizite Medien Land, Amphibisch, Nur Wasser und Schwebend. Übergänge und Ziele berücksichtigen tatsächliche Bodenkollision und Wassertiefe. Spieler können die Brücke nutzen; tieferes Wasser ist ohne Spieler-Schwimmsystem gesperrt.
- Test-GameMode deaktiviert Begleiter, reguläre UI, Begegnungen und normalen Save/Load/Delete. Der neue Opt-out ist auf bisherigen GameModes standardmäßig nicht aktiv. Normale Spielstände werden weder geladen noch überschrieben.
- Neue Gelände-/Wasserquelle unter `Art/World/BiomeTestV1`, zwei exportierte FBX und zwei Unreal-Meshes. Eigene Boden-/Wassermaterialien verwenden vorhandene Texturen. Private Instancing-Materialkopien verhindern Änderungen an Originalmaterialien. Bäume verwenden die vorhandenen Kamera-Freistellungsmaterialien.
- Nachgewiesene Korrekturen innerhalb der neuen Karte: FBX-Y-Achse, aufwärts gerichtete Wasserflächen, physische Höhlenwandkollision statt blockierender dekorativer AABB sowie Beobachtungslichtung für Nebulak. Neun ausschließlich neue Kartenbäume wurden umgestellt; alle 103 bleiben vorhanden.
- Bestehende Maps einschließlich VisualV2, Heilhaus, ursprüngliche Beleuchtung, Modelle, Animationen und Save-Dateien wurden nicht verändert. Die neue Karte hat eine eigene Licht-/Post-Process-Konfiguration auf Grundlage der bestehenden Außenlichtwerte und TAA.

## Tatsächliche Prüfungen

Die folgenden Ergebnisse stammen aus den vorhandenen Prüfungen vom 23.10.; für die reine Sicherung wurden Build und Gameplay nicht unnötig erneut ausgeführt. Am 24.10. erfolgten erneut Dateizuordnung, Original-Prüfsummenvergleich und Abhängigkeitsabgleich.

| Prüfung | Ergebnis / Grenze |
|---|---|
| Editor-Build `BiomeV1_Build02` | Exit 0, 19,65 s; aktueller nativer Biom-Code gebaut |
| Vollständige PokeMonster-Automation | 190 fachlich bestanden: 189 ohne und 1 mit Warnungen; 0 Fehler, 0 nicht ausgeführt |
| Strenger QA-Wrapper | **Exit 1**; ausdrücklich nicht warnungsfrei bestanden. Engine-Prozess Exit 0; zwei externe iOS-Helfer-Warnungen im Test `PokeMonster.CrystalMoves.Edges.SunSolarBeamAndWeatherHealContext` |
| Neue native Biome-Tests | `ExplicitMediaAndContinuousShore` und `ExistingPathRespectsWaterAndWalls` jeweils bestanden, keine Warnungen |
| Map Checks | Alle 12 Karten (11 vorhandene plus neue Biom-Karte), jeweils 0 Fehler / 0 Warnungen |
| Asset-Audit | 290 Projektpackages einschließlich Map; keine fehlenden harten/weichen Projektabhängigkeiten; verwendete Präsentationsdaten ohne Validierungsfehler |
| Gewöhnlicher grafischer PIE-Start, `Walk07` | 92/92 Schritte, 11 Prüfungen bestanden; 473,13 m ohne Spielerteleport durch echte Enhanced-Input-Bewegung gelaufen |
| Medien und Bewegung | Alle zehn Testactoren bewegten sich; keine Habitatüberschreitung. Schiggy und Enton auf Land und im Wasser beobachtet; Nur-Wasser-Marker durch tatsächliche Bodentiefenprüfung abgesichert |
| Glurak | Grounded, Takeoff, Hover und Landing tatsächlich erfasst |
| Spieler und Laufwege | Acht Richtungen, bestehender Sprint 315 cm/s, Brücke, 3-m-Plattform, Höhle und Ruine begehbar; feste Spielkamera unverändert |
| Zusätzlicher PIE-Lauf `Details01` | 25/25 Schritte, 4 Prüfungen bestanden, 167,91 m; zusätzliche QHD-Spielkameraaufnahmen von Glutexo und Nebulak |
| Original-/Save-Schutz | Alle 2.938 erfassten Originaldateien unverändert; Dev-Save vor/nach PIE und am 24.10. identisch |
| Controller | Software-Eingaben geprüft; kein neuer physischer Controller-Hardwaretest behauptet |

Externe Warnung: Engine-Helfer `libimobiledevice/Mac/idevice_id` lässt sich mit `posix_spawn` nicht starten (86, „Bad CPU type in executable“). Die zwei Warnungen sind von Projektfehlern getrennt. Sie werden nicht durch Abschwächen des strengen Wrappers verborgen.

Dev-Save SHA-256: `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`.

Die 290 Abhängigkeiten sind vollständig bereits versioniert oder Bestandteil dieses Sicherungspakets. Alle 24 geschützten unversionierten Incoming-GLBs bleiben unverändert und werden nicht mit aufgenommen. Beide Vollbackup-Referenzen bleiben bei `03492bd96b4dba44692f675c19d5f11abfa86b4b`.

## Lokale visuelle und technische Nachweise

Diese Nachweise bleiben absichtlich im ignorierten `Saved` und werden nicht auf GitHub geladen:

- `Saved/BiomeTestV1/PRUEFBERICHT.md`: vollständiger ursprünglicher lokaler Bericht mit Bild-/Videolinks; dessen damalige Vorgabe „kein Commit/Push“ bezog sich auf die Erstellung und ist durch den ausdrücklichen Sicherungsauftrag vom 24.10. ersetzt.
- `Saved/BiomeTestV1/Walk07/`: echte QHD-Spielkameraaufnahmen aller Bereiche, `Result.json`, Telemetrie und Wegfortschritt.
- `Saved/BiomeTestV1/Details01/`: zusätzliche echte QHD-Spielkameraansichten in Höhle und Wald, `Result.json`.
- `Saved/BiomeTestV1/Walk06/Sequences.json`: echte, zeitgestempelte sparse Bildsequenzen (Flug 90 Bilder / 60 s, Wasser 60 Bilder / 40 s; keine Echtzeitvideo-Framerate behauptet).
- `Saved/BiomeTestV1/Overview_Unreal_sRGB.png`: tatsächliche temporäre Unreal-SceneCapture-Übersicht, ausdrücklich **keine normale Spielkameraaufnahme** und kein Konzeptbild.
- `Saved/BiomeTestV1/AssetAudit.json`, `MapCheckResults.json`, `FinalIntegrity.json` und `Before.json`: lokale Audits und Original-Prüfsummen.
- `Saved/ProjectRefinement/BiomeV1_Build02/Result.json` und `BiomeV1_Automation01/Report/index.json`: Build-/Automationsergebnisse.

Nach einem GitHub-Clone sind diese optionalen Kontrollmedien nicht vorhanden. Die Karte, benötigten Originalquellen, Abhängigkeiten und versionierten Prüfwerkzeuge sind davon unabhängig nutzbar.

## Grenzen und offene Abnahme

1. Schwimmen ist ein **Idle-/Auftriebsprototyp**, keine eigens erstellte Schwimmanimation. Kein Unterwassersystem.
2. Goldini fehlt; der technische Marker belegt ausschließlich die Nur-Wasser-Beschränkung. Kein Ersatzmodell wird als fertig integriertes Pokémon ausgegeben.
3. Glurak nutzt vorhandenes bodennahes Schweben in 0,5–1,5 m über sicheren Bodenpunkten; kein freier dreidimensionaler Flug oder Reiten.
4. Kein geeigneter fliegender Höhlenbewohner vorhanden. Höhle und Ruine sind absichtlich oben und zur Kamera offen.
5. Die Karte prüft Bewegung/Darstellung. Reguläres Kampf-, Fang- und Save-Gameplay ist dort bewusst gesperrt; die gemeinsame Automation deckt bestehende Systeme ab, ohne einen neuen vollständigen manuellen Kampfdurchlauf auf dieser Testkarte zu behaupten.
6. Die visuelle Abnahme bleibt beim Nutzer. Git-Sicherung bedeutet keine neue Stilfreigabe und keine Übernahme in VisualV2.

## Gezielter Git-Umfang

Versioniert werden ausschließlich:

- `Content/Maps/Dev_BiomeTestMap_V1.umap` und 20 eigene Assets unter `Content/Environment/BiomeTestV1`.
- Vier Gelände-Original-/Exportdateien unter `Art/World/BiomeTestV1`.
- Die neue Habitat-/Test-GameMode-Klasse, zwei Biome-Automationstests und die acht bereits getesteten gemeinsamen Quelltextanpassungen.
- 16 ausgewählte Dateien unter `Tools/BiomeTestV1` für Erstellung, Isolation, Terrainprüfung, Asset-Audit, Map Checks und echte PIE-Begehung sowie deren Anleitung.
- Dieser Bericht und eine eng begrenzte Fortschreibung von `Tools/DevelopmentEvidence/CoreFiles.json` um genau diese geprüften Dateien. Keine alten Manifesteinträge werden entfernt; unveränderte Pflichtdateien müssen weiterhin stimmen. Der Validator bleibt unverändert.

24 neue LFS-Dateien (Map, Assets, Blender und FBX), zusammen **7.771.845 Bytes** / ca. 7,41 MiB. Bestehende LFS-Objekte werden nicht bereinigt.

Nicht versioniert und nicht gelöscht werden die Incoming-Unikate, sämtliche Kontrollmedien, Caches und elf einmalige lokale Diagnose-/Sitzungshelfer (`CancelFailedReview`, `EncodeSequences`, `FinalEditorState`, `InspectMap`, `InspectPIE`, `InspectScenery`, `MaterialAPI`, `RepairGroundAndLabels`, `SaveNewMap`, `SmokePIE`, `WriteReport`, jeweils `.py`). Sie sind für normales Play und die ausgewählten versionierten Werkzeuge nicht erforderlich. Das dauerhafte textbasierte Ergebnis steht in diesem Bericht; der alte Berichtsgenerator bleibt ein lokaler Sitzungshelfer.

Die erneute Sicherungsprüfung umfasst explizite Index-Dateiliste, LFS-Zeiger mit lokalen SHA-256-Werten, Python-Syntaxprüfung ohne Cache-Erzeugung, `git diff --cached --check` und den unveränderten Core-Validator. Regulärer Push ausschließlich nach `origin/main`; Remote-Commit und LFS-Download-Prüfsummen werden anschließend separat verifiziert und im Abschluss an den Nutzer gemeldet. Kein Force-Push, keine Budgetänderung, kein Push der lokalen Vollbackup-Referenzen.
