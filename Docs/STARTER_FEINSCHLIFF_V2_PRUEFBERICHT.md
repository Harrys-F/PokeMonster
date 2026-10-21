# Starter-Feinschliff V2 – Prüfbericht

21.10.2026. Projekt `/Users/harry/Developer/PokeMonster`, Ausgangscommit `d1c9deef87ac542f845ddb4f201ed4711ea6e794`, Branch `main`. Umsetzung in der vorhandenen VisualV2 ohne Map-Speicherung, neue Map, Worktree, Projektkopie oder vollständiges Backup. Keine Heilhaus-/Landschafts-, Licht-, Kamera-, Player- oder Kampfoberflächengestaltung verändert.

## 1. Bestandsaufnahme und Änderungen

Vorhanden waren drei separate, anatomisch unterschiedliche Skeletons, sieben Clips je Starter, die gemeinsame CreaturePresentation mit 0,14-s-Lokomotionsüberblendung, landgebundene lokale Wegsuche sowie ein rein visueller Begleiter. Spezies-IDs und Höhen bleiben: `Zunderlauf`/Glumanda 60 cm, `Schiggy` 50 cm, `Bisasam` 70 cm. Keine künstliche Größenanpassung.

Bereits korrekt: genau ein kollisionsloser Begleiter, Kampfstart-Ausblendung, bewegungsabhängiges Animationstempo, tatsächliche Sprintgeschwindigkeit, Gebäude-/Wasserprüfung, Rückkehr nach Kampf, bestehende Party-/Save-Verknüpfungen. Diese Systeme wurden weiterverwendet.

Korrigiert:

- Die Auswahl suchte das erste *geeignete* Mitglied. Jetzt kann ausschließlich Teamplatz 1 erscheinen. Bei K.O., ungültigen Daten oder fehlendem gültigen 3D-Profil erscheint kein ersatzweises späteres Mitglied. Kein automatischer Teamtausch.
- Beschleunigung/Bremsen und begrenzte Winkelbeschleunigung ersetzen abrupte Start-/Stoppgeschwindigkeit. Eigene Parameter für freie Wanderung und Begleiter im bestehenden `Species.Overworld`. Große Richtungsänderungen werden zunächst im Stand ausgeführt. Die vorhandene Idle-/Walk-/Run-Überblendung bleibt erhalten.
- Vier jüngste Ziele und Besuchszähler für acht Habitatsektoren vermindern wiederholte Zielwahl. Zufällige Pausenzeiten und langsames Umschauen bleiben erhalten. Keine komplexe neue KI.
- Kollisionsgeprüfte Pfadglättung entfernt unnötige Rasterknicke. Der exakte begehbare Zielpunkt kann aus einer Nachbarzelle erreicht werden; eine blockierte gerundete Zielzelle verhindert nicht mehr automatisch das Erreichen des tatsächlichen Ziels. Wasser, Gelände, Hindernisse und Habitatgrenzen werden weiterhin geprüft.
- Bei leerem Rückrufpfad wurde die Wegsuche trotz Wartezeit jeden Frame erneut gestartet. Erneute Versuche sind jetzt zeitlich begrenzt. Blockierte Schritte führen weiterhin zu neuer Ziel-/Routenwahl.

Echter PIE-Test `Saved/StarterExpansionV1/PolishMovement02/Result.json`: 17 Prüfschritte bestanden, einschließlich Sprint/Brücke, Rückruf, ClassicBattle-Pause, Rückkehr, genau einem Begleiter und explizitem Wechsel aller drei Begleiterspezies. Keine Testteleports.

| Spezies | Größte gemessene Auslenkung im Test | Pläne nach 65 s Beobachtung | Blockierte Schritte in dieser Stichprobe |
|---|---:|---:|---:|
| Glumanda | 603,96 cm | 2 | 0 |
| Schiggy | 514,27 cm | 3 | 0 |
| Bisasam | 581,69 cm | 3 | 0 |

Alle innerhalb ihrer bestehenden Habitate. Maximaler Begleiterabstand im Sprint-/Brückenlauf 830,48 cm, maximale Bewegungsgeschwindigkeit 385,00 cm/s; anschließender Rückruf unter 300 cm bestanden. Das sind Verhaltensmessungen, keine FPS-Benchmarks und keine Garantie für beliebiges Terrain. Zusätzlich echte Boden-/Wasser-/Hindernistests und ein Test mit blockierter gerundeter Zielzelle.

## 2. Animation und Modellqualität

Alle 21 ursprünglichen Clips wurden in Blender mit je 17 zeitlich verteilten Posen untersucht; Extremposen separat gerendert. Erst nach konkreter Gewichtungs-/Bone-Analyse erfolgten zwei begrenzte Korrekturen. Keine Retopologie oder optische Neugestaltung.

**Glumanda:** Die größte Ohnmachtsverformung lag am Schwanzansatz (benachbarte Vertices 7444/11754, `tail_01` gegenüber `pelvis`). Die bisherige Pose richtete den Schwanz unabhängig von der bereits gedrehten Körperpose aus. Neue Faint-Action dreht die geerbte Idle-Pose gemeinsam um die geprüfte Weltachse und passt nur die Bodenhöhe an. Eine erste interne Fassung verwendete die lokale statt der Weltachse und wurde vor Import korrigiert. Das Original-V11-Mesh, seine Gewichte, Materialien und die sechs anderen Clips bleiben unverändert.

**Bisasam:** Die frühere Sohlenmaske band zentrale Bauchvertices vollständig an Vorder-/Hinterfüße. Beim Lauf zog dies die Bauchfläche auseinander. 135 gezielt abgegrenzte Bauchvertices wurden wieder dem Rumpf zugeordnet. Vertexpositionen, Dreiecke, UVs, Materialien, Skeleton und alle sieben Actions bleiben erhalten. Keine pauschale neue automatische Gewichtung.

| Diagnose, identische 33 Abtastzeitpunkte | Größtes Wachstum einer einzelnen Meshkante vorher | Nachher |
|---|---:|---:|
| Glumanda Faint | 144,99 mm | 5,45 mm |
| Bisasam Run | 104,30 mm | 57,05 mm |

Dies ist absolute Kantenlängenänderung, kein Fußgleiten und kein allgemeiner Qualitätsprozentsatz. Anschließende dichtere Prüfung mit 61 Posen: Glumanda Faint maximal 5,45 mm, Bisasam Run maximal 60,04 mm. Verbleibende Verformung an Gelenk-/Übergangsbereichen ist damit nicht als fehlerfrei zertifiziert. Bisasams tiefste Oberfläche unterschreitet im Run die lokale Bodenebene maximal um rund 0,90 mm; Glumandas neue Faint liegt mindestens etwa 0,95 mm darüber, jeweils vor dem unveränderten Präsentationsoffset.

Neue Quellen und Exporte:

- `Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Faint_PolishV2.blend` – kleine Rig-/Actionquelle mit Verweis auf das unveränderte Referenzmodell.
- `Art/Characters/Creatures/Zunderlauf/Exports/PolishV2/Glumanda_Faint.fbx`.
- `Art/Characters/Creatures/Bisasam/Source/Bisasam_Meshy_PolishV2.blend` – vollständige bearbeitbare Quelle, bestehende Bilder/Materialien/Actions.
- `Art/Characters/Creatures/Bisasam/Exports/PolishV2/Bisasam_Skin.fbx`.
- Jeweils `PolishV2_AnimationAudit.json` mit Quelldigest, Messwerten und konkret geänderten Gewichten.

Beide Quellen gespeichert und erneut geöffnet, beide FBX tatsächlich reimportiert. Gemessene Reimporthöhen 0,59999995 m und 0,69999993 m, 23 bzw. 18 Bones. Bisasams Geometrie-/UV-/Dreiecksgleichheit mit der Originalquelle exakt geprüft. Neue Unreal-Assets unter `/Game/Characters/Creatures/Zunderlauf/PolishV2/` und `/Game/Characters/Creatures/Bisasam/PolishV2/`. Bestehende Skeletons und Materialien wiederverwendet; originale Präsentationsprofile erhalten. Nur aktuelle Spezies-Präsentationsbindungen angepasst.

Schiggys sieben Animationen unverändert. Originale kleine Oberflächenfehler nahe dem Auge bleiben erhalten. Keine allgemeine Fuß-IK, keine Garantie vollständig fixierter Standfüße bei allen Drehungen/Extremposen. Verbesserte Beschleunigung und Überblendung ersetzen keine manuelle Endabnahme dieser Fälle.

## 3. Schiggy: Entfernung, Mips und Vergleich

Alle drei Modelle besitzen aktuell eine Mesh-LOD-Stufe und jeweils drei 2048×2048-Texturen. Schiggys BaseColor nutzt weiterhin die im V1-Bericht belegte `TMGS_NO_MIPMAPS`-Umgehung für weiße Atlasflecken; Normal und MR sowie die anderen Starter nutzen die vorhandenen Mips. LOD-Bias 0, kein erzwungenes höheres Texturmaximum. Originaltexturen und Materialparameter unverändert.

Echte QHD-Oberweltaufnahmen: 2560×1440, Screen Percentage 100 %, bestehende Kamera Pitch −50°, Yaw −45°, FOV 35°. Gemessene Kameradistanzen in der Nachherreihe: Schiggy 26,91–31,90 m, Bisasam 26,62–31,58 m, Glumanda 26,98–31,37 m. Dies sind tatsächliche Entfernungen zur erhöhten 2,5D-Kamera, keine Entfernung zum Spieler. Vergleich unter derselben Kamera und denselben Grafikbedingungen; zufällige Begleiterziele und Posen unterscheiden sich.

Keine neuen weißen Atlasflecken in dieser begrenzten Reihe bestätigt. Keine unbelegte Textur-/Mip-Änderung übernommen. No-Mip-Aliasing in anderen Entfernungen und bei anderen Kameras bleibt offen; eine umfassende LOD-/Mip-Freigabe wird nicht behauptet. Die erste Inventur unmittelbar beim Laden meldete 32×32-Platzhalter; nach abgeschlossenem Laden erneut tatsächliche 2048×2048 gelesen. Kein belegter Quelltexturverlust.

## 4. Vier fehlende Attackenwirkungen

Gezielte Ergänzung im vorhandenen BattleSession-/Event-/HP-Präsentationssystem, keine neue Kampflogik oder Attackendatenbank. Neue Assets `/Game/Data/Moves/DA_TailWhip`, `DA_Bubble`, `DA_Withdraw`, `DA_LeechSeed`.

| Attacke | Typ/Kategorie in Gen 2 | Stärke | Genauigkeit | AP | Implementierte Wirkung |
|---|---|---:|---:|---:|---|
| Rutenschlag | Normal/Status | 0 | 100 | 30 | Ziel-Verteidigung −1 |
| Blubber | Wasser/Spezial | 20 | 100 | 30 | 10 % Ziel-Initiative −1 |
| Panzerschutz | Wasser/Status | 0 | 100 | 40 | Eigene Verteidigung +1 |
| Egelsamen | Pflanze/Status | 0 | 90 | 10 | Einmal je Rundenende 1/8 Ziel-Max-KP, mindestens 1; tatsächlichen Entzug beim aktiven Gegenüber heilen |

Stufen auf −6…+6 begrenzt, physische Verteidigung verändert keinen Spezialschaden. Initiative beeinflusst die Zugreihenfolge. Gras-Pokémon sind gegen Egelsamen immun, erneutes Bepflanzen ohne zusätzliche Wirkung. Samen und Stufen enden beim Auswechseln des betroffenen Pokémon; kein persistenter Status und keine Save-Version geändert. Fehlversuche, AP und eigene Statusattacken bleiben im vorhandenen Rundensystem. KP-Entzug und Heilung erhalten eigene animierte HP-Schritte, ohne die klassische Oberfläche neu zu gestalten.

Schiggy lernt neu erzeugt Tackle 1, Rutenschlag 4, Blubber 7, Panzerschutz 10, Aquaknarre 13. Das vorhandene Schema verwendet bei mehr als vier Attacken die letzten vier: auf Level 13 also Rutenschlag/Blubber/Panzerschutz/Aquaknarre. Bisasam: Tackle 1, Heuler 4, Egelsamen 7, Rankenhieb 10. **Bestehende gespeicherte Attackenslots und verbrauchte AP werden nicht ungefragt neu belegt.** `AssignSpeciesMoves` bleibt eine administrative Neuzuweisung für neue Individuen, keine Save-Migration.

Quellen: [Schiggy Gen 2](https://www.serebii.net/pokedex-gs/007.shtml), [Bisasam Gen 2](https://www.serebii.net/pokedex-gs/001.shtml), [Blubber Gen 2](https://www.serebii.net/attackdex-gs/bubble.shtml), [Egelsamen Gen 2](https://www.serebii.net/attackdex-gs/leechseed.shtml), [Egelsamen-Wirkung](https://pokemondb.net/move/leech-seed), [Panzerschutz](https://pokemondb.net/move/withdraw), [Rutenschlag](https://pokemondb.net/move/tail-whip). Abruf/Abgleich 21.10.2026. Die bestehende vereinfachte Schadensformel, Fluchtregel und bereits vorhandene Verbrennungsabwicklung bleiben Grundlage; keine vollständige Gen-2-Emulation zugesagt.

Echter PIE-Test `Saved/StarterPolishV2/EffectsPIE/Result.json`: fünf ausgeführte Aktionen, einschließlich Egelsamen-Entzug, Heilung und erfolgloser Doppelanwendung. Blubbers Initiative-Zusatzeffekt ist in diesem kurzen Sichtlauf nicht ausgelöst; der unverändert konfigurierte 10-%-Effekt wurde zusätzlich über 100 deterministische Seeds im Automationstest geprüft.

## 5. Echte Aufnahmen und ihre Grenzen

Kontrollmedien bleiben lokal im ignorierten `Saved/`. Keine generierten Bilder oder hochskalierten Screenshots als Nachweis.

- `Saved/StarterPolishV2/VisualBefore/`: zwölf originale QHD-Oberweltbilder.
- `Saved/StarterPolishV2/VisualAfter02/`: zwölf originale QHD-Oberweltbilder, jeweils mit Größenreferenz, realen Positionen, Kameradistanz und Geschwindigkeit in `Result.json`.
- `Saved/VisualV2TAAIntegrationV1/Recordings/PolishBefore_*` und `PolishAfter02_*`: echte Framebuffer-JPEG-Sequenzen mit Zeitstempeln, etwa 10 s je Bisasam/Glumanda-Reihe. Die Nachheraufnahme Schiggys wurde durch eine echte Wildbegegnung nach etwa 1,22 s unterbrochen; nicht als zehnsekündige Aufnahme ausgeben. Vorher-Schiggy-Reihe etwa 9,88 s.
- `Saved/GlumandaV11/LiveUI/Starter_PolishModels01_*`: echte ClassicBattle-/WorldBattle-Spieloberflächenaufnahmen. Tatsächliche Slate-Größe 2331×1346; nicht als QHD deklarieren.
- `Saved/StarterPolishV2/FinalReactions*/`: echte ausgeführte Siege/K.O. für alle drei Starter anhand ausdrücklich markierter Runtime-Gegner mit 1 KP. Keine neue Map, keine erzwungenen Animationsposen. BattleEvents sind kein Ersatz für eine visuelle Aufnahme.
- Normales `Shot` und der bestehende reine Framebuffer-Rekorder enthalten die separat gezeichnete ClassicBattle-UI nicht. Ihre `FinalReactions`-/`EffectsPIE`-Weltbilder sind **kein** visueller Kampfanimationsnachweis. Deshalb zusätzliche echte Slate-Spieloberflächen-Bildfolge über `pm.CreatureReview.CaptureLiveUI`; 19 echte Slate-Aufnahmen unter `Saved/GlumandaV11/LiveUI/PolishReactionsUI_*`, tatsächlich **2331×1311**, keine QHD-UI-Abnahme. Die Reihe zeigt unter anderem die korrigierte Glumanda-Ohnmacht im laufenden realen Kampf. `FinalReactionsUI/Result.json` bestanden.
- `Saved/StarterPolishV2/AnimationCorrections/`: identische Blender-Diagnosekameras vorher/nachher für die konkreten Verformungen. Diese Bilder sind ausschließlich technische Blenderdiagnostik, ausdrücklich kein Unreal-Spielkameraersatz.

Zufallsbewegung verhindert identische Oberweltposen vorher/nachher; dies wird nicht als pixelgenauer A/B-Test ausgegeben. Vegetation kann Begleiter weiterhin teilweise verdecken. Die bestehende Playerfreistellung und Weltgestaltung wurden nicht verändert.

## 6. Technische Prüfung

| Prüfung | Ergebnis / lokaler Nachweis |
|---|---|
| Mac Development Editor Build | Erfolgreich, zuletzt `StarterPolishBuild04` |
| Vollständige Projekt-Automation | **80/80**, 0 Testwarnungen, 0 Fehler, `StarterPolishAutomation02` |
| Map Check | **11/11**, jeweils 0 Fehler/0 Warnungen, `Saved/StarterPolishV2/MapChecks.json` |
| Wildhabitate, Brücke, Sprint-Rückruf, Kampfpausen | `PolishMovement02`, bestanden |
| ClassicBattle und WorldBattle, beide Starterperspektiven | `PolishModels01`, vier Fälle bestanden, Save/Load je Fall |
| Fang, Wechsel, Heilung, Inventarverbrauch und Save/Load | `PolishCapture01`, beide Spezies bestanden |
| Niederlage → Rückkehr → Heilung → atomarer Autosave → Reload | `PolishDefeat01`, bestanden |
| Vollständiger echter Enhanced-Input-Fußlauf | **102 Schritte, 289,03 m, Sprint 315 cm/s**, `Saved/GlumandaV11/Acceptance/PolishFull01/` |
| KO-/Siegesabläufe aller drei Starter | `FinalReactions/Result.json`, drei Fälle bestanden; UI-Sichtnachweis separat |
| Quellen und Originalassets | Referenzdigests, FBX-Roundtrip und exakter Bisasam-Geometrie-/UV-Vergleich bestanden |
| Save-Schutz | ursprünglicher Dev-Slot SHA-256 `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b` restauriert |
| Dateischutz | alle 58 vorbestehenden unversionierten Dateien unverändert; 185/187 geschützte Dateien byte-identisch, nur zwei bewusst erweiterte Kampfereignis-Adapter aus dieser Schutzmenge geändert |

Der vollständige Fußlauf prüft Liora/Quest-/Archivfluss, Fang, Party, Menü, Heilen/Speichern, Ein-/Austritt und diagonale Türen sowie acht Laufrichtungen/Sprint. Seine 675 Begleiter-Beobachtungen sahen wegen des nicht 3D-konfigurierten ersten Prototyp-Teammitglieds keinen Begleiter. Daraus wird ausdrücklich keine zusätzliche Innenraum-Begleiterabnahme abgeleitet; der dedizierte Starterlauf prüft die echten Begleiter und Kampfpausen separat.

Fehlgeschlagene Zwischenprüfungen bleiben erhalten: erster Bewegungslauf durch überschießende Testeingabe; erste Nachherreihe durch unerwartete Wildbegegnung; erste Automation 79/80 durch veraltete aktive Profilpfad-Erwartung. Teststeuerung bzw. veraltete Erwartung gezielt korrigiert, erfolgreiche Wiederholungen separat dokumentiert. Keine Fehlerunterdrückung.

Unabhängige Engine-/Editor-Meldungen bleiben offen: 17 `LogAutomationTest: Error: Condition failed` beim Engine-Start vor der eigentlichen Testsuite, in beiden geöffneten Editorständen gleich; Ursache nicht abschließend ermittelt. Zusätzlich iOS-Hilfsprogramm `idevice_id` falsche CPU-Architektur, CoreAudio-Sample-Rate-Warnung, bestehende Python-Namenskollision `bInformation`/`Information`, Renderthread-Warnung zu `r.MotionVectorSimulation`, sowie `MI_WLA_LeafOak` mit fehlendem `InstancedStaticMeshes`-Usageflag beim Laden. Nicht als fehlerfreies Gesamt-Engine-Log ausgeben und keine auftragsfremde Welt-/Materialänderung vornehmen. Projekt-Automation und Map-Check-Ergebnisse oben sind davon getrennt ausgewertet.

Physischer Switch-Pro-Controller-Test bleibt ausdrücklich offen. Keine neuen Hardwaretests oder umfangreichen Performance-Reihen durchgeführt.

## 7. GitHub und Schutz

Geprüfter Bewegungsmeilenstein: `54f6b7d3e98cb39f97c6e9419acf675f51786cad`, regulär nach `origin/main` gepusht und Remote verifiziert. Weitere Abschlussdateien werden erst nach abschließender Index-/Diff-/Quellen-/LFS-Prüfung gezielt committed und gepusht. Vollbackup `03492bd` bleibt unter beiden bestehenden lokalen Verweisen unverändert und ist kein Vorfahr von `main`. Keine History-Umschreibung, Bereinigung oder neuen Backups. Abschluss-Hash und verifizierte LFS-Übertragung im abschließenden Git-Nachweis ergänzen.

## 8. Empfehlung

Technisch nutzbarer Starter-Feinschliff für die vorhandene VisualV2: natürliche Beschleunigung, bessere Habitatnutzung, eindeutige Begleiterwahl, zwei nachgewiesene Animationsfehler begrenzt korrigiert und vier dokumentierte Attackenwirkungen ergänzt. Keine pauschale künstlerische Endfreigabe aller Extremposen, beliebiger Distanzen oder aller Geländesituationen. Schiggys ursprüngliche Oberflächenfehler/No-Mip-Grenzen, Fußkontakte beim Drehen und die teilweise Vegetationsverdeckung bleiben sichtbar zu beurteilen. Keine weiteren Kreaturen oder Welt-Art-Passes automatisch begonnen.

## Lokale Bildauswahl zur visuellen Abnahme

Die folgenden Dateien werden nicht auf GitHub geladen. QHD-Oberweltbilder zeigen reale Bewegung mit der ausdrücklich bezeichneten Runtime-Prüfparty; keine identischen Zufallsposen.

- [Schiggy vorher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualBefore/Schiggy_8_QHD00000.png) / [nachher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualAfter02/Schiggy_8_QHD00000.png). Keine Materialänderung.
- [Bisasam vorher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualBefore/Bisasam_18_QHD00000.png) / [nachher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualAfter02/Bisasam_18_QHD00000.png). Vegetationsverdeckung im Nachherbild sichtbar, keine Behauptung einer vollständigen Sichtbarkeitskorrektur.
- [Glumanda vorher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualBefore/Zunderlauf_3_QHD00000.png) / [nachher, QHD](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualAfter02/Zunderlauf_3_QHD00000.png). Originaloptik erhalten.
- [Dichte echte Glumanda-KO-Bildfolge, tatsächliche UI-Auflösung 2331×1311](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/PolishReactionsUI_Zunderlauf_004/ActualSlateViewport.png).
- [Bisasam-Bauchgewichtung vorher, Blenderdiagnostik](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/AnimationCorrections/Bisasam_Before.png) / [nachher, Blenderdiagnostik](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/AnimationCorrections/Bisasam_After.png).
- [Glumanda-Faint vorher, Blenderdiagnostik](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/AnimationCorrections/Zunderlauf_Before.png) / [nachher, Blenderdiagnostik](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/AnimationCorrections/Zunderlauf_After.png).

![Echte QHD-Oberweltaufnahme mit Schiggy](/Users/harry/Developer/PokeMonster/Saved/StarterPolishV2/VisualAfter02/Schiggy_8_QHD00000.png)

![Echte korrigierte Glumanda-Ohnmacht, Slate 2331×1311, markierter 1-KP-Kampfprüffall](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/LiveUI/PolishReactionsUI_Zunderlauf_004/ActualSlateViewport.png)
