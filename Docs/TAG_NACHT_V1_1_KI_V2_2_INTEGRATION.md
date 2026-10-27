# Tag-Nacht V1.1 + Pokémon-KI V2.2 – gemeinsamer Prüfstand

Stand **27.10.2026**. **Beide Einzelpakete und die gemeinsame technische Restabnahme sind geprüft.** Der frühere Blocker ist mit der ausdrücklich auf PID 23485 beschränkten Nutzerfreigabe aufgehoben. Nach frischem Start wurden Build, alle 279 Automationstests, tatsächliches Save/Load im Innenraum, Kampf, Mapwechsel, Begleiter-Rückkehr, GPU-Stichprobe und zwölf Map Checks abgeschlossen. Bekannte visuelle Grenzen, geringe Clip-Bildrate und der nicht abschließend geklärte frühere Editorstillstand bleiben unten ausdrücklich dokumentiert. Der Zwischenstatus aus `5a82a2c0` wird damit ersetzt.
## Gesicherte Meilensteine

- **`230ff51e` – Paket A:** wärmere/hellere Morgendämmerung, sichtbarer Sonnenuntergang um 19 Uhr, zurückhaltend besser lesbare Nacht, 75° regulär/85° Debug. [Einzelbericht mit GPU-Tabelle und Originalbildpfaden](TAG_NACHT_V1_1_PRUEFBERICHT.md).
- **`5ae1380d` – Paket B:** vorhandene KI über zentrale Weltuhr gewichtet, sechs konfigurierbare Rhythmen, individuelle Zeitversätze, Ruhe/Schlaf/Nahrung/Sozialkontakte, Pause und Unterbrechungen. [Einzelbericht mit Artentabelle, CPU-Werten und Grenzen](POKEMON_KI_V2_2_PRUEFBERICHT.md).
- Basis **`f712b662`**, einschließlich `e1fc3517`. Keine zweite Uhr, unverändert 120 Echtminuten je Tag, keine Spawn-/Fang-/Kampf-/EP-/Entwicklungsänderungen. Keine neuen Models/Maps oder neuen LFS-Nutzdaten.

## Tatsächlich bestandene Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Editor-Build A | `DayNightV11A_Build02`, Exit 0 |
| Automation A | 273 funktional bestanden; 272 sauber + 1 Warnung, Engine 0, **strenger Wrapper 1** |
| Editor-Build B | `DayRhythmV22_Build02`, Exit 0 |
| Automation B, gesamter Projektfilter | **279 bestanden, 0 fehlgeschlagen/übersprungen/Testwarnungen**, Engine/Wrapper 0 |
| Map Checks A und B | Je alle zwölf bestehenden Maps, jeweils **0 Fehler / 0 Warnungen** |
| Echter PIE-Fußlauf A | Menüpause, B/C, Morgendämmerung/Mitternacht, Heilhaus-Ein-/Ausgang, isoliertes Innenraum-SaveLoad mit exakter Uhr/Team/Kontrollpunkt, ClassicBattle-Sieg und Steuerungsrückkehr bestanden |
| Echter Mapwechsel A | VisualV2 → Dev_TestMap → VisualV2, identische zentrale Weltzeit, korrekte Nacht nach Rückkehr bestanden |
| Unabhängige KI-PIE-Prüfung B | 94 Sekunden, ursprüngliche Habitate, keine erzwungenen Aktivitäten, echte Besuche, Zeitsprünge und Ambient-Pausenhalt bestanden |
| Gemeinsamer Tagesumlauf | `Joint01`, **354,15 Sekunden**, 516 Zustandsstichproben für acht bestehende Instanzen aus sechs Arten, alle Assertions bestanden |
| Abschließender Editor-Build | `DayNightV11AI22_FinalBuild01`, Exit 0 |
| Abschließende volle Automation | `DayNightV11AI22_FinalAutomation01`: **279 bestanden, 0 fehlgeschlagen/übersprungen/Testwarnungen**, Engine/strenger Wrapper Exit 0 |
| Gemeinsamer echter Gameplay-Fußlauf | `GameplayJoint01`, 67,38 s, **18 Prüfungen bestanden**: Innenraum/SaveLoad mit exakter Uhr und KI-Gewichten, ClassicBattle, Pausen und Steuerungsrückkehr |
| Gemeinsamer echter Mapwechsel | `TravelJoint04`, gleiche GameInstance/Uhr, korrektes Nachtlicht, Team-Identitäten/KP/AP unverändert, genau ein sichtbarer Begleiter außerhalb der Wildrhythmen, acht zeitgesteuerte Wildinstanzen |
| Zusätzliche GPU-Stichprobe | `GPUJoint01`, QHD/High, 3 Wiederholungen × 2 Orte, normale tatsächlich laufende 1×-Uhr, bestanden |
| Abschließende Map Checks | Im frischen Editor erneut **alle zwölf Maps mit jeweils 0 Fehlern / 0 Warnungen**, keine Map gespeichert |
| Schutzprüfung | 85 ursprüngliche Dateiprüfsummen, 31 ursprüngliche unversionierte Dateien und beide Vollbackup-Verweise unverändert; Editor-Szene identisch, keine schmutzigen Pakete |

Vorhandene Automation deckt weiterhin SaveV2, Fang, Team, AP/Repertoire/Erinnerungsmeister, Lernen/Entwicklung, Kampfarten und Controller-Softwarefunktionen ab. Physischer Controller-Test nicht behauptet. Der erneute tatsächliche SaveLoad-/Kampf-/Travel-Durchlauf **mit** V2.2 wurde am 27.10.2026 erfolgreich nachgeholt. Native Befehle und Softwareeingaben nutzen die bestehende Steuerung; kein Hardwaretest behauptet.

Externe iOS-Helferwarnungen (`idevice_id`, Bad CPU type) bleiben vorhanden. Frühe generische Engine-Condition- und HTTP-Portmeldungen sowie die vorgefundene `MI_WLA_LeafOak`-Instancingwarnung getrennt dokumentiert. Wrapper A bleibt Exit 1, obwohl B in seinem tatsächlichen Lauf Exit 0 erreicht. Keine pauschale Warnungsfreiheit. In der frischen Sitzung kam bei einem langen Map-Ladeframe zusätzlich die Engine-Meldung `GetSimulationTimeStep – Max iterations` vor; die anschließende Platzierung/Steuerung wurde erfolgreich geprüft. Frühe generische Startup-Condition-/HTTP-Bind-Meldungen und externe HTTP-Shutdown-Warnungen sind weiterhin Logbefunde, keine neu behauptete Warnungsfreiheit.

## Gemeinsame Tagesbeobachtung

Reale Zeitpunkte 06:00, 09:00, 12:00, 16:00, 19:00, 22:00, 00:00 und 04:30 geprüft, anschließend vorhandene Uhr mit Debuggeschwindigkeit 60× über einen vollständigen Tag. Erste/letzte Umlaufstichprobe: Tag 8, 04:36:48 → Tag 9, 04:56:17 in 121,66 Echtsekunden. Beobachtete Umrechnung ca. 719,79 Ingame-Sekunden je Echtsekunde, erwartet 12 × 60 = 720; Stichproben an Framegrenzen, keine zweite Zeitfortschreibung. Alle fünf zentralen Tagesphasen beobachtet.

- Bisasam: Nahrung, Bewegung, Ruhe, Schlaf und soziale Annäherung; Spielerbeobachtung/-annäherung erhält Vorrang, wenn der Beobachter näher steht.
- Pikachu: überwiegend Bewegung, zeitweise Idle/Ruhe. Eine einzelne Beobachtung garantiert keine lange Schlafphase.
- Glumanda: auch nachts aktiv, mehrere abgeschlossene Nahrungssuchen.
- Myrapla: im gemeinsamen Lauf nachts tatsächlich Wanderung beobachtet, außerdem Nahrungssuche, Ruhe und Schlaf. Kurze unabhängige Nachtstichprobe war zuvor überwiegend ruhig; beides bleibt im Nachweis sichtbar.
- Enton: unter anderem Nahrungssuche um 19 Uhr, Ruhe und Schlaf außerhalb der Dämmerung, tatsächliche Abschlüsse beobachtet.
- Nebulak: nachts Wanderung/Schweben, tagsüber häufiger ruhig; auch Schlafzustand beobachtet. Keine Geh-Animation hinzugefügt.

Alle Stichproben prüfen Habitatgrenzen, gegenseitig eindeutige Partnerreservierungen sowie keine Bewegung/Sozialpartner im Schlaf. Kein unerwünschter Kampf. Spontane Besuche wurden unabhängig B vollständig abgeschlossen; im gemeinsamen Lauf gab es soziale Annäherungen, aber keinen vollständig abgeschlossenen Besuch. Zusätzlicher rein lesender Fotobeobachter fand in seinem Zeitfenster keinen ruhenden Sozialkontakt; kein entsprechendes Bild erfunden. Keine Populationsstatistik aus diesem kurzen Einzelumlauf ableiten.

## Leistung und Bilder

A: GPU-Vorteil gegenüber bewegten Kontrollen im Dorf ca. 2,54–4,41 ms, Wald 1,58–2,65 ms; Restkosten gegenüber gehaltener Sonne ca. 1,47–1,63 ms. Schattenpass entlastet, keine Qualitäts-/Auflösungsreduktion. B: gemessene acht Komponenten 0,2557 ms/Frame gegenüber 0,2858 ohne Rhythmus; zu kurze Einzelstichprobe für einen Beschleunigungsanspruch. Details/Spannen in den Einzelberichten. Die zusätzliche GPU-Kontrolle auf dem gemeinsamen Endstand ist nachgeholt:

| Frische Sitzung, begrenzte Aktualisierung | GPU-Median | GPU-Spanne der 3 Einzelmediane | Frame-Median | ShadowDepths-Median |
|---|---:|---:|---:|---:|
| Dorf | 66,30 ms | 64,18–66,78 ms | 76,15 ms | 3,32 ms |
| Wald | 71,43 ms | 68,51–75,32 ms | 81,30 ms | 2,21 ms |

QHD 2560×1440, High=2, 100%, gleiche Kamerapunkte/Sonne wie A. 456 Lichtauswertungen führten zu 85 Rotationsanwendungen; kein Kampf und keine unerwartete Uhrpause. Diese frische Sitzung an einem anderen Zeitpunkt hat andere Speicher-/Lastbedingungen als die vorherige lange Sitzung. **Der niedrigere absolute Wert ist kein kausaler KI- oder zusätzlicher Optimierungsgewinn.** Der belastbare Optimierungsvergleich bleibt die direkt kontrollierte A-Messreihe.

Lokaler Nachweisordner: `Saved/ProjectRefinement/DayNightV11AI22/`.

- `Before01/` / `AfterA01/`: zwölf echte QHD-Bildpaare mit identischer Kamera, Tageszeit und High-Bedingungen. `LightingCompareA.jpg` ist nur beschriftet/verkleinert, nicht umbelichtet.
- `Joint01/Joint0600.png`, `Joint0900.png`, `Joint1200.png`, `Joint1600.png`, `Joint1900.png`, `Joint2200.png`, `Joint0000.png`, `Joint0430.png`: tatsächliche gemeinsame Spielansichten. Ab 12 Uhr wurde der **Spieler** zum Blick auf die bestehende Bisasam-Gruppe bewegt; Pokémon/Habitate blieben unverändert. Diese Bilder sind keine identischen Vorher-/Nachher-Kamerapaare; dafür ausschließlich A-Paare verwenden.
- `Videos/Joint.mp4`: 45 echte präsentierte Frames über 12,05 Sekunden, tatsächlich **3,65 Hz**, Originalzeitstempel/keine Zwischenbilder. Sichtbar laufendes Spiel, aber für endgültige Feinbeurteilung zu geringe Bildrate. Schattenclips A ebenfalls nur 5,3–6 Hz. Keine hohe Bildrate behauptet.
- `GameplayJoint01/InteriorDay.png`, `InteriorNight.png`, `InteriorLoaded.png`: echte zusätzliche QHD-Aufnahmen des Innenraum- und SaveLoad-Durchlaufs.
- Zusätzlicher visueller Restpunkt: Bei `Joint1900.png` sind am bestehenden Sichtkreis kantige helle/grüne Kronenflächen sichtbar. Ursache dort nicht abschließend zugeordnet; keine ungeprüfte globale Änderung an gemeinsamen Blättermaterialien oder Kamera vorgenommen. Lesbarkeit ist gegeben, diese Darstellung benötigt gesonderte Sichtprüfung.

Bildprüfsummen und Zustandsübersicht: [Integrationsnachweis](TAG_NACHT_V1_1_KI_V2_2_INTEGRATIONSNACHWEIS.json). Originalmedien bleiben lokal, nicht in Git/LFS hochgeladen.

## Editorstillstand, gezielte Freigabe und Nachprüfung

Der eigene Prozess **23485** beendete PIE am 26.10. regulär. Danach blieb der GameThread beim Viewport-Resize an einer Render-Fence stehen; asynchrone Scene-Extension-Freigabe wartete ebenfalls. `ArtControl start_pie` endete nach 120 s mit Timeout. Diagnose-Sample: `Saved/ProjectRefinement/DayNightV11AI22/EditorB_HangSample.txt`, gemeldeter Footprint 41,4 GB bei 16 GB RAM. Dies war ein tatsächlicher Stabilitätsbefund, keine harmlose iOS-Warnung.

Reguläre Fensterbeendigung und eine einmalige SIGTERM-Anforderung hatten den Prozess nicht beendet. Am **27.10.2026** genehmigte der Nutzer ausdrücklich: „Ja, nur PID 23485 beenden und fortsetzen“. Identität, Projektargumente und Startzeit wurden erneut geprüft. **Ausschließlich PID 23485** wurde gezielt per SIGKILL beendet; Protokoll `AuthorizedForceClose.json`. Die allgemeine Force-Quit-Sperre wurde nicht geändert. Keine anderen Prozesse zwangsbeendet.

Zwei danach frisch gestartete kurze Editor-Sitzungen führten die offenen Prüfungen erfolgreich durch und wurden **regulär geschlossen** (`EditorRecoveryGameplay.log`, `EditorRecoveryGPU.log`). Der frühere Stillstand trat darin nicht erneut auf. Seine Ursache ist nicht abschließend geklärt; dies bleibt ein dokumentiertes Stabilitätsrisiko bei langen, speicherintensiven Editor-/Aufnahmesitzungen. Keine neue allgemeine Engine-/Rendering-Implementierung zur Kaschierung vorgenommen.

### Tatsächliche Korrekturen am QA-Aufbau

- Eine verspätete Begleiter-Zusatzprüfung lief bereits während eines neu gestarteten normalen Wildkampfes; Ausblenden des Begleiters war dort korrekt. Kein Produktionsfehler daraus abgeleitet.
- Die frische GPU-Sitzung nutzte zunächst `DA_TestWater` ohne 3D-Modell. Dafür ist kein Begleiter vorgesehen; die Testannahme „immer ein Begleiter“ war falsch.
- Für die gezielte Begleiterprüfung wird deshalb der **vorhandene** RAM-Debugaufbau `pm.EvolutionReview.Party Zunderlauf 15` mit Glumanda und unabhängigem Glurak verwendet, im zuvor ausgewählten isolierten QA-Slot. Keine Nutzerdaten/Saves überschrieben. Rückkehr zu einem sicheren Beobachtungspunkt verhindert einen unbeabsichtigten Folgekontakt während der Prüfung.
- `Actor.is_hidden()` ist nicht in Unreal-Python exponiert. Die Abfrage wurde gegen die tatsächlich vorhandene reflektierte Eigenschaft `bHidden` geprüft und korrigiert.
- Erst **`TravelJoint04`** ist der vollständig bestandene erweiterte Rundlauf. Alle vorherigen fehlgeschlagenen Diagnoseversuche bleiben als solche erhalten; keine Ergebnisse überschrieben oder nachträglich als bestanden ausgegeben. Der erste reine Uhr-/Lichtrundlauf `TravelJoint01` war bereits bestanden.

In dieser Fortsetzung wurden keine produktiven C++-, Map-, Material-, Pokémon- oder Save-Strukturen geändert. Nur QA-Werkzeuge und Bericht wurden vervollständigt. `Gameplay.py`, `TravelJoint.py` und der vollständig ausgeführte Abschlussablauf `FinishJoint.py` werden gezielt versioniert. Ältere optionale/fehlgeschlagene Diagnose-Arbeitsdateien `CheckReturn.py` und `SocialProof.py` bleiben lokal unversioniert erhalten; sie sind kein notwendiger Laufzeitbestandteil.

## Verwendung und Fortsetzung

Weltuhr wie bisher: `pm.WorldClock set 1 6 0`, `pm.WorldClock set 1 19 0`, `pm.WorldClock set 1 22 0`; `pause`, `resume`, `speed 60`, `reset` (normale Geschwindigkeit/Fortsetzen). Debugzeit bleibt im bestehenden PIE-Testschutz. `pm.DayNight B` regulär 75°, `pm.DayNight C` Debug85, `pm.DayNight off/on` ursprüngliches Licht / dynamischer Zyklus.

Rhythmen im Abschnitt `PokeMonsterCreatureRhythmSettings` von `Config/DefaultGame.ini` ändern, beispielsweise `+SpeciesProfiles=(Species=Myrapla,Profile=(Rhythm=Nocturnal,IndividualOffsetMinutes=30.0))`; bestehende Zeile ersetzen, keine Doppelzeile. Editor neu starten. Noch keine weiteren Arten konfiguriert. Vorhandene Aktivitäten/Präsentation müssen für spätere Arten geeignet sein; keine neuen Rigs/Animationen aus diesem System ableiten.

A und B bleiben getrennte überprüfbare Commits (`230ff51e`, `5ae1380d`); `5a82a2c0` dokumentiert den früheren Blocker. Der anschließende reine QA-/Dokumentationsabschluss ist über `git log -1 -- Docs/TAG_NACHT_V1_1_KI_V2_2_INTEGRATION.md` nachvollziehbar. Normaler Push/Remote-/LFS-Abgleich werden nach dem Sicherungsvorgang im lokalen `GitFinal.json` festgehalten. Keine neuen LFS-Nutzdaten, keine Budgetänderung oder kostenpflichtige Nutzung.

**Verbleibend:** Sichtkreis-Kronenartefakt separat visuell untersuchen; echte Aufnahmen mit höherer Bildrate für endgültige Bewegungsfeinabnahme wünschenswert; früherer Editorstillstand bleibt als nicht abschließend geklärtes Stabilitätsrisiko dokumentiert. Keine der offenen Restdarstellungen wurde durch neue Modelle, Landschafts-/Kameraänderungen oder pauschale Qualitätsreduktion verdeckt.
