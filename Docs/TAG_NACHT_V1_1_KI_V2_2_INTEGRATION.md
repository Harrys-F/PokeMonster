# Tag-Nacht V1.1 + Pokémon-KI V2.2 – gemeinsamer Prüfstand

Stand 26.10.2026. **Beide Einzelpakete implementiert und separat geprüft; gemeinsame Abschlussprüfung noch nicht vollständig abgeschlossen.** Der eigene Editor hängt nach erfolgreich beendetem Tagesumlauf beim erneuten PIE-Start. Gezielte Force-Quit-Freigabe wurde angefragt und liegt für diesen Prozess noch nicht vor. Deshalb kein vollständig bestandener Gesamtauftrag behauptet.

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
| Schutzprüfung | 85 ursprüngliche Dateiprüfsummen, 31 ursprüngliche unversionierte Dateien und beide Vollbackup-Verweise unverändert |

Vorhandene Automation deckt weiterhin SaveV2, Fang, Team, AP/Repertoire/Erinnerungsmeister, Lernen/Entwicklung, Kampfarten und Controller-Softwarefunktionen ab. Physischer Controller-Test nicht behauptet. Der erneute tatsächliche SaveLoad-/Kampf-/Travel-Durchlauf **mit** V2.2 wurde durch den Editorstillstand noch nicht ausgeführt; nicht mit dem bestandenen A-Durchlauf verwechseln.

Externe iOS-Helferwarnungen (`idevice_id`, Bad CPU type) bleiben vorhanden. Frühe generische Engine-Condition- und HTTP-Portmeldungen sowie die vorgefundene `MI_WLA_LeafOak`-Instancingwarnung getrennt dokumentiert. Wrapper A bleibt Exit 1, obwohl B in seinem tatsächlichen Lauf Exit 0 erreicht. Keine pauschale Warnungsfreiheit.

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

A: GPU-Vorteil gegenüber bewegten Kontrollen im Dorf ca. 2,54–4,41 ms, Wald 1,58–2,65 ms; Restkosten gegenüber gehaltener Sonne ca. 1,47–1,63 ms. Schattenpass entlastet, keine Qualitäts-/Auflösungsreduktion. B: gemessene acht Komponenten 0,2557 ms/Frame gegenüber 0,2858 ohne Rhythmus; zu kurze Einzelstichprobe für einen Beschleunigungsanspruch. Details/Spannen in den Einzelberichten. Geplante zusätzliche GPU-Kontrolle auf dem gemeinsamen Endstand noch offen.

Lokaler Nachweisordner: `Saved/ProjectRefinement/DayNightV11AI22/`.

- `Before01/` / `AfterA01/`: zwölf echte QHD-Bildpaare mit identischer Kamera, Tageszeit und High-Bedingungen. `LightingCompareA.jpg` ist nur beschriftet/verkleinert, nicht umbelichtet.
- `Joint01/Joint0600.png`, `Joint0900.png`, `Joint1200.png`, `Joint1600.png`, `Joint1900.png`, `Joint2200.png`, `Joint0000.png`, `Joint0430.png`: tatsächliche gemeinsame Spielansichten. Ab 12 Uhr wurde der **Spieler** zum Blick auf die bestehende Bisasam-Gruppe bewegt; Pokémon/Habitate blieben unverändert. Diese Bilder sind keine identischen Vorher-/Nachher-Kamerapaare; dafür ausschließlich A-Paare verwenden.
- `Videos/Joint.mp4`: 45 echte präsentierte Frames über 12,05 Sekunden, tatsächlich **3,65 Hz**, Originalzeitstempel/keine Zwischenbilder. Sichtbar laufendes Spiel, aber für endgültige Feinbeurteilung zu geringe Bildrate. Schattenclips A ebenfalls nur 5,3–6 Hz. Keine hohe Bildrate behauptet.
- Zusätzlicher visueller Restpunkt: Bei `Joint1900.png` sind am bestehenden Sichtkreis kantige helle/grüne Kronenflächen sichtbar. Ursache dort nicht abschließend zugeordnet; keine ungeprüfte globale Änderung an gemeinsamen Blättermaterialien oder Kamera vorgenommen. Lesbarkeit ist gegeben, diese Darstellung benötigt gesonderte Sichtprüfung.

Bildprüfsummen und Zustandsübersicht: [Integrationsnachweis](TAG_NACHT_V1_1_KI_V2_2_INTEGRATIONSNACHWEIS.json). Originalmedien bleiben lokal, nicht in Git/LFS hochgeladen.

## Editorstillstand und verbleibende Abnahme

Der eigene Prozess **23485** beendete PIE regulär. Danach blieb der GameThread beim Viewport-Resize an einer Render-Fence stehen; asynchrone Scene-Extension-Freigabe wartete ebenfalls. `ArtControl start_pie` endete nach 120 s mit Timeout. Diagnose-Sample: `Saved/ProjectRefinement/DayNightV11AI22/EditorB_HangSample.txt`, gemeldeter Footprint 41,4 GB bei 16 GB RAM. Ursache nicht abschließend geklärt; nicht als harmlose iOS-Warnung oder bestandene Abschlussprüfung umdeuten.

Fenster regulär zu schließen hatte keine Wirkung. Eine **einmalige** SIGTERM-Anforderung wurde laut lokalem Unreal-Quellcode über `Mac GracefulTerminationHandler` als reguläre Exit-Anforderung angenommen (Log 21:53:01 UTC), Prozess blieb jedoch stehen. Kein zweites Signal, kein SIGKILL, keine andere Prozessbeendigung, keine Änderung der Force-Quit-Sperre. Gezielte Nutzerfreigabe ausschließlich für diesen Prozess angefragt. Kein neuer Editor parallel gestartet.

Nach Freigabe erforderlich: eigener Editor gezielt beenden/Projekt frisch starten; zusätzliche gemeinsame GPU-Stichprobe, Innenraum/SaveLoad/Kampf, Mapwechsel und regulärer Steuerungsrücklauf. Abschließenden Build/Automation nach sauberem Editorende erneut ausführen. Zwölf Map Checks sind auf unverändertem funktionalem B-Quellstand bereits bestanden; bei neuer Quelländerung erneut prüfen. Bis dahin bleibt die gemeinsame Gesamtfreigabe ausdrücklich offen.

Die begonnenen zusätzlichen QA-Skripte bzw. Assertions (`Gameplay.py`, `TravelJoint.py`, `FinishJoint.py`, `SocialProof.py`) bleiben als Arbeitsdateien erhalten. Noch nicht vollständig ausgeführte Teile werden nicht als fertige Gameplayänderungen eingecheckt. Kein Nutzer-Save oder geschützter Inhalt wurde verändert.

## Verwendung und Fortsetzung

Weltuhr wie bisher: `pm.WorldClock set 1 6 0`, `pm.WorldClock set 1 19 0`, `pm.WorldClock set 1 22 0`; `pause`, `resume`, `speed 60`, `reset` (normale Geschwindigkeit/Fortsetzen). Debugzeit bleibt im bestehenden PIE-Testschutz. `pm.DayNight B` regulär 75°, `pm.DayNight C` Debug85, `pm.DayNight off/on` ursprüngliches Licht / dynamischer Zyklus.

Rhythmen im Abschnitt `PokeMonsterCreatureRhythmSettings` von `Config/DefaultGame.ini` ändern, beispielsweise `+SpeciesProfiles=(Species=Myrapla,Profile=(Rhythm=Nocturnal,IndividualOffsetMinutes=30.0))`; bestehende Zeile ersetzen, keine Doppelzeile. Editor neu starten. Noch keine weiteren Arten konfiguriert. Vorhandene Aktivitäten/Präsentation müssen für spätere Arten geeignet sein; keine neuen Rigs/Animationen aus diesem System ableiten.

A und B sind getrennte überprüfbare Commits. Dieser Dokumentationsstand unterscheidet bestandene Einzelprüfungen und Tagesumlauf ausdrücklich von der blockierten Restabnahme. Normaler Push/Remote-/LFS-Abgleich werden nach dem Sicherungsvorgang im lokalen `GitFinal.json` festgehalten; keine kostenpflichtige Nutzung oder Budgetänderung erforderlich.
