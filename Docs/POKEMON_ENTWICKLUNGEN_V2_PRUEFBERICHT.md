# Glutexo und Pokémon-Entwicklungen V2 – Abschlussprüfung

Stand: 23.10.2026. Aktives Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, bestehende VisualV2. **Glutexo und die vollständige Kette Glumanda → Glutexo → Glurak sind spielbar.** Keine neue Map, kein Worktree, keine Projektkopie und kein weiteres Pokémon angelegt. Die finale strenge QA ist wegen einer externen Engine-Warnung ausdrücklich **nicht vollständig bestanden**, obwohl sämtliche 187 fachlichen Tests bestanden sind.

## Meilenstein A – Glutexo

Gesichert auf GitHub: `bbed74619423f0dad25942bcc8b815946b4e510b`. 55 gezielt geprüfte Commitpfade; 26 LFS-Objekte mit 31.868.617 Bytes nach Upload vollständig heruntergeladen und per SHA-256 verifiziert. Ausführlicher Art-/Modellbericht: `GLUTEXO_INTEGRATION_V1_PRUEFBERICHT.md`.

Verwendete Originaldatei: `Art/Characters/Creatures/Incoming/Glutexo.glb`, SHA-256 `718f9eb037832228f25bdbce299671db0972a9c3c271d23724e39743476c6efe`. Tatsächlich Glutexo, ohne ursprüngliches Rig oder Animationen, 21.001 Dreiecke und drei 2048²-Originalbilder. Originaldatei, Geometrie, UVs und Bilddaten erhalten. Eigene gepackte Blenderquelle unter `Art/Characters/Creatures/Glutexo/Source/Glutexo_Meshy_V1.blend`, eigenes 20-Bone-Rig plus Unreal-FBX-Wurzel, Schwanz-/Flammenkette, sieben Rollen Idle/Walk/Run/Attack/Hit/Faint/Happy. Ausschließlich die ursprüngliche modellierte Schwanzspitzenflamme; kein doppelter Effekt, kein Feuer am Körper.

Neue stabile Art `CreatureSpecies:Glutexo`, national 005, Feuer, 110 cm. Eigener Unreal-Namensraum `/Game/Characters/Creatures/Glutexo/MeshyV1`; verifizierte Gen-2-Artwerte und Lernliste nutzen vorhandene produktive V4-Attacken. Originaldatenquellen mit fester Revision und Prüfsummen: `Tools/GlutexoEvolutionV2/ReferenceSources.json`. Kein Umbau anderer Modelle, Rigs oder Animationen.

Normales VisualV2-PIE-Testgelände enthält elf isolierte Exemplare. Zugang per Entwicklungskonsole `pm.TestGround.Go 11`, zurück mit `pm.TestGround.Return`. Die bisherigen zehn Stationspositionen bleiben gleich. Testexemplare sind keine fangbaren Wildinstanzen und besitzen keine Save-Identität. Glutexos vorhandene Systemunterstützung für Wildprofile/Begleiter ist geprüft; kein zusätzliches dauerhaftes Wildhabitat in der Map platziert.

## Meilenstein B – tatsächlich implementierte Entwicklung

| Ausgang | Bedingung | Ziel | Darstellung |
|---|---|---|---|
| Glumanda, stabile historische ID `Zunderlauf` | Level ≥16 | `Glutexo`, Dex 005 | Neues geprüftes Meshy-Modell |
| Glutexo | Level ≥36 | `Glurak`, Dex 006 | Unverändertes vorhandenes Glurak-Modell |

Nur eine tatsächlich an der Ausgangsart hinterlegte Route kann ausgeführt werden. Direkte Glumanda→Glurak-Anwendung wird abgewiesen. Bei mehreren Leveln entstehen nötigenfalls zwei getrennte Angebote und zwei Bestätigungen; keine übersprungene Zwischenform und keine zweite individuelle Instanz.

Die vorhandene `CreatureProgression` prüft Zielart, alle sieben Rollen, exaktes Mesh/Skeleton und die vorhandene Präsentationsvalidierung. `CreatureInstance` bleibt Träger individueller Daten; `EncounterSubsystem` verwaltet weiterhin dasselbe Team. Neue Angebote werden nur außerhalb eines laufenden Kampfes, einer Niederlagenrückkehr, eines Dialogs und anderer gesperrter Eingabekontexte geöffnet. Laufende Attackenlernangebote werden zuvor entschieden. Fehlende/ungültige Zielmodelle führen zu keiner Mutation oder Platzhalterentwicklung; die Berechtigung bleibt aus Art und Level ableitbar.

## Ablauf und Bedienung

Die neue Entwicklungsansicht verwendet die vorhandene **capture-only 3D-Bühne derselben Welt** mit zentral eingepasster Kreatur, Originalgrößen, warmem Leuchten und dezenten Lichtpunkten. Keine separate Arena-/Entwicklungsmap, keine Änderung der Weltkamera und keine Neugestaltung von ClassicBattle. Originalform → Leuchten → Vorschau der neuen Form → Ausklang → atomare Übernahme und Bestätigung. Bis zum Abschluss der fünf Sekunden kann abgebrochen werden, auch nachdem die neue Form bereits als Vorschau sichtbar war.

B bestätigt, A bricht ab; Tastatur Enter/Esc und Steuerkreuz/Pfeile für Lernslots. Vorhandener macOS/Nintendo-Tastenhelfer bleibt maßgeblich; keine neue Grundbelegung. X, L/R und Plus der bestehenden Menüs wurden nicht umgebunden. Nach Abschluss kehren Fokus und Eingabefreigabe in die Oberwelt zurück.

Abbruch verändert weder Art noch individuelle Kampf-/Attackendaten. Das Angebot wird als abgebrochen gespeichert; es erscheint nicht sofort erneut im selben Zustand. Ein späterer Levelaufstieg **oder ein anderer gewonnener Kampf** erlaubt einen erneuten Versuch. Die zweite Bedingung verhindert eine dauerhafte Sperre nach Abbruch auf Level 100. Offene Angebote überleben Save/Load und werden nicht doppelt angelegt.

## Daten, AP und Save-Kompatibilität

- Bestehende Instanz-ID, Teamplatz, Level, numerische Erfahrung, Statusproblem und Schlafzähler bleiben erhalten. Andere Instanzen derselben Art bleiben unberührt.
- Neue Basiswerte werden mit der vorhandenen Wertberechnung bestimmt. Fehlende KP bleiben erhalten; K.O. wird nicht durch eine Entwicklung geheilt. Das System besitzt weiterhin keine neue IV-/EV-/Wesenarchitektur.
- Aktive vier Slots, gesamtes persönliches Repertoire und sämtliche verbrauchten AP werden kopiert, nicht neu aus der Zielart erzeugt. Keine AP-Regeneration durch Entwicklung.
- Nur eine zum aktuellen Level passende neue Lernattacke wird als echtes Angebot vorbereitet. Bei Glurak auf Level 36 ist dies Flügelschlag. Ersetzen, freier Slot und Ablehnen laufen durch die bestehende `ResolveMoveLearning`-Verarbeitung; vorherige Attacken samt AP bleiben im Repertoire. Kein freier nachträglicher Attackentausch im Teammenü.
- Begleiter erkennt dieselbe Instanz mit neuer Art und aktualisiert Mesh, eigenes Skeleton, Clips, Maße, Bodenkapselplanung und Effektanbindung über den vorhandenen Pfad.
- Die vorhandene Feldchronik-/Quest-Speziesregistrierung erhält die neue Art. Scheitert das Speichern, werden Kreatur, Chronik, Questfortschritt und Abschlussflags gemeinsam zurückgenommen. Das vorhandene atomare macOS-Speichern bleibt zuständig.

Save-Schema **8** ergänzt Ziel/Level des Entwicklungsangebots und einen optionalen individuellen Erfahrungskurven-Verweis. Alte Schemata **1–7** bleiben lesbar; es werden keine erlernten Attacken oder Entwicklungen erfunden. Hintergrund der Kurvenangabe: Das historische Glumanda benutzt eine andere Wachstumskurve als die kanonischen Glutexo-Daten. Ein bloßer Artwechsel würde unveränderte XP bei unverändertem Level ungültig machen. Deshalb behält dieses individuelle Pokémon bei der Entwicklung seine tatsächlich verwendete Kurve; neue eigenständige Glutexo verwenden korrekt Medium Slow. Numerische XP und Level werden nicht heimlich umgerechnet, keine alte Artdefinition wird umgeschrieben.

## Weitere Entwicklungsarten

Die vorhandenen Trigger und UND-Bedingungen für Gegenstand, Freundschaft, Ort und besondere Handlung bleiben erhalten. Der neue spielbare Dienst führt jetzt Levelrouten aus; vollständige Gegenstandsverbrauchs-, Freundschaftsökonomie- und Prüfungsabläufe werden nicht behauptet. Kadabra/Gelehrter, Maschock/Kraftprüfung, Georok/Höhle und Alpollo/Ruine werden nicht zu einfachen Levelrouten umgewandelt. Ihre endgültigen Bedingungen, Modelle und Weltintegration bleiben späteren Aufträgen vorbehalten.

## Tatsächliche Qualitätsprüfungen

| Prüfung | Ergebnis / tatsächlicher Kontext |
|---|---|
| Finaler Editor-Build `EvolutionV2_Build07` | Exit 0 |
| Vollständige finale Automation `EvolutionV2_Automation03` | 186 Success, 1 SuccessWithWarnings, 0 Failed, 0 NotRun; **187 fachlich bestanden** |
| Strenger finaler QA-Wrapper | **Exit 1, nicht bestanden**, ausschließlich externe Warnungen im Test `PokeMonster.CrystalMoves.Edges.FrozenTurnEndThawAndFireCure` |
| Warnung | `idevice_id`: `posix_spawn failed (86, Bad CPU type in executable)`, anschließend `Failed to launch Tool` |
| Vorheriger vollständiger Lauf `EvolutionV2_Automation02` | 186/186, keine Testwarnungen, Wrapper Exit 0; dieser Lauf lag vor der zusätzlichen Rücknahmeprüfung und ersetzt nicht den finalen Lauf |
| Finale elf Map Checks, `Editor06.log` | Je 0 Fehler / 0 Warnungen, keine Speicherung |
| Finale reale PIE-Folge `EvolutionReview04` | 18 Prüfungen bestanden: unter/ab Levelgrenzen, späte Stornierung, späterer Versuch, beide Formen, Identität/XP/KP/AP, Reserve-Glurak, Entwicklungslernmenü, Teamplatzsortierung, Save/Load und reale Softwareeingaben |
| Randfälle `EvolutionEdges01` | 12 Prüfungen bestanden: mehrere Level, zwei getrennte Entwicklungsbestätigungen, echter ClassicBattle-Sieg als Auslöser, Wiederholung auf Level 100, fehlendes Zielmodell, Save/Load |
| Vollständiger Gameplay-Fußlauf `EvolutionV2FullFoot01` | 103 Schritte, 289,30 m, maximale bestehende Sprintgeschwindigkeit 315 cm/s; Kampf/Fang, NPC/Dialog, Brücke, Heilhaus/Heilen, Innen-/Außenkamera und Speichern/Laden bestanden |
| Begleiterüberwachung im Fußlauf | 636 Stichproben, keine gemeldeten Probleme; 36 Kampf-Ausblendungs- und 44 Innenraum-Schattenprüfungen |
| Ursprüngliche geschützte Assets | 761 Dateien / 1.665.509.661 Bytes gegen Ausgangscommit `18c397d2` geprüft, **0 Abweichungen**: ursprüngliche Maps, Charakter-/Pokémonassets und -quellen, ursprüngliche Artdefinitionen und Konfigurationen |
| Entwickler-Save | Nach den Prüfläufen wieder SHA-256 `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df` |

Der vollständige Fußlauf erfolgte mit Build06. Die danach ergänzte, isolierte Rücknahme bei fehlgeschlagenem Speichern und strengere Angebotsvalidierung wurden durch Build07, finale volle Automation und finale PIE-Folge geprüft. Im ausdrücklich kanonischen Fußlauf-Testteam war die automatische Entwicklungsansicht pausiert; die normale automatische Anbindung und echte Kampf-/Levelauslöser wurden separat in den Entwicklungsfolgen mit Standardfunktion geprüft. Kein physischer Switch-Pro-Test behauptet.

## Echte Bilder und Videos – nur lokal

Keine Konzeptbilder und keine nachträgliche Bildskalierung als Nachweis. Dateien bleiben im ignorierten Saved und werden nicht hochgeladen.

- Glutexo/Spieler/Testgelände: `Saved/GlutexoEvolutionV2/ReviewA02/Glutexo_World_4_QHD00000.png`, echter Spielkamera-Framebuffer 2560×1440.
- Glutexo in beiden ClassicBattle-Perspektiven: `ReviewA02/Glutexo_Battle_0.png` / `_1.png`, native 2560×1080-Kampfziele; nicht als QHD-Vollbild bezeichnet.
- Finale Entwicklungsangebote, Abbruch, Glutexo, Glurak und Flügelschlag: `Saved/GlumandaV11/LiveUI/EvolutionEvolutionReview04*/ActualSlateViewport.png`, **tatsächlicher Slate-Viewport 2331×1311**. Die Fensterbegrenzung des Mac wird nicht als QHD ausgegeben.
- Zusätzlich: `Saved/GlutexoEvolutionV2/QHDCaptures/EvolutionEvolutionReview04*.png`, echte native Renderings desselben laufenden UMG-/3D-Zustands mit 2560×1440. Technisch separat gerendert mit eigener Layout-/DPI-Skalierung, ausdrücklich keine 1:1-Screenshots des kleineren Slate-Fensters. Farbraum des finalen Renderers geprüft; frühe hellere/dunklere Debugexporte nicht als finale Qualitätsreferenz verwenden.
- Unveränderte echte Bildsequenzen mit Originalzeitstempeln als MP4: `Saved/GlutexoEvolutionV2/Videos/Glumanda_Glutexo.mp4` (5,90 s), `Glutexo_Glurak.mp4` (5,90 s), `Abbruch.mp4` (5,73 s), jeweils native 2331×1311. Grundlage ist die final gestaltete reale Viewportfolge Review03. Keine Zwischenbildgenerierung und keine Aussage über die volle Spiel-Bildrate.

## Gefundene Fehler und verbleibende Grenzen

Der erste Entwicklungs-Widget-Aufbau existierte zwar als Objekt, wurde aber nicht sichtbar gezeichnet. In `RebuildWidget` korrigiert und anschließend real sichtbar mit vollständigen Eingaben erneut geprüft. Frühe unsichtbare Aufnahmen werden nicht als Erfolge gezählt. Der erste neue Save-Automationstest verwendete einen ungültigen Unreal-Outer; korrigiert, keine Engine-Fehler als externe Warnungen umetikettiert.

Während des ersten UI-Fehlversuchs schrieb die noch laufende eigene Sequenz kurz nach dem Testabbruch ein weiteres Test-Save. Der Schutzguard stoppte dessen automatische Rücksetzung. Vor Wiederherstellung wurden Instanz-IDs, Level und XP dieses eigenen Testteams über den vorhandenen Loader nachgewiesen; erst danach wurden die bereits vorhandenen, SHA-verifizierten Originalbytes restauriert. Finaler Runner bricht eine noch laufende Sequenz beim Fehler ab, bevor er den Abschluss-Hash erfasst. Originalspielstand und alle Incoming-Originale sind wieder vollständig unverändert; kein fremder Save wurde blind überschrieben.

Die externe iOS-Helferwarnung bleibt offen; der finale strenge Wrapper bleibt deswegen Exit 1. Keine Änderung an Engine-Helfern, weltweiten Renderwerten oder QA-Schwellwerten vorgenommen. Glutexos Animationsfeinschliff bleibt visuell abnahmefähig, keine perfekte Oberfläche/Bodenkontaktqualität in jeder Extrempose garantiert. Es gibt jetzt keine zusätzlichen endgültigen Pokémon, keine vollständigen Gegenstands-/Freundschafts-/Sonderprüfungsentwicklungen und keinen weiteren Landschafts-/Heilhaus-Art-Pass.

## GitHub und Schutz

Meilenstein A wurde regulär gepusht und seine 26 LFS-Objekte vollständig verifiziert. Meilenstein B umfasst ausschließlich benötigte C++-/Werkzeug-/Dokumentationsdateien, Glutexos neue Entwicklungsroute und ein kleines gemeinsames Präsentationsmaterial. Sein exakter Commit-Hash sowie Remote-/LFS-Endstand werden nach dem regulären Push im Abschluss genannt; es wird kein Hash vorab erfunden. Keine Kontrollmedien, Caches, Builds oder temporären Save-Dateien im Commit. Originale der übrigen 24 unversionierten Incoming-Modelle bleiben unversioniert und bytegleich. Vollbackup `03492bd` bleibt unverändert lokal und außerhalb der main-Historie. Kein Force-Push, keine Käufe oder Budgetänderungen.

Maschinenlesbare Ergebnisse: `POKEMON_ENTWICKLUNGEN_V2_TESTERGEBNISSE.json`. Wiederholbarer Ablauf und Grenzen: `Tools/GlutexoEvolutionV2/README.md`.
