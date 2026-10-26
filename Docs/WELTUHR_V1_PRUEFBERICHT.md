# Weltuhr V1 – Prüfbericht

Stand: 26.10.2026. Ausgangsstand `a7199b9f`, zu Beginn mit `origin/main` synchron.
Umgebung: bestehendes PokeMonster-Projekt, UE 5.8.2 / macOS / Metal,
`/Game/Maps/Dev_TestMap_VisualV2`. Keine neuen Maps oder Projektkopien.

## 1. Ergebnis und technische Umsetzung

Eine einzige `UPokeMonsterWorldClock` pro GameInstance verwaltet Tageszähler und
Tagessekunden. Standardtag **120 Echtminuten**, Start **Tag 1 – 09:00 Uhr**.
Konfiguration und vollständige Bedienung: [WELTUHR_V1.md](WELTUHR_V1.md).

Die Umrechnung ist `Echtsekunden × 1440 / Tagesdauer_in_Echtminuten`:
bei Standardkonfiguration 12×. Doppelte Genauigkeit, variable und lange Frames,
Tagesübertrag und einmalige Fortschreibung je Engineframe. Ein voller Tag wird
in der Automation mit 7200 Echtsekunden simuliert; kein zweistündiger Leerlauf.

Fünf lückenlose, halb offene Phasen: 04–05 früher Morgen, 05–07 Morgendämmerung,
07–18 Tag, 18–20 Abenddämmerung, 20–04 Nacht. Alle 1440 Minuten und die exakten
Grenzen wurden geprüft. Zentral konfigurierbare Grenzen und Tagesdauer;
ungültige Konfiguration fällt auf die vollständigen Standardwerte zurück.

## 2. Pause, Mapwechsel und Schnittstellen

Bestehende Zustände für Haupt-/Untermenüs, Dialoge, ClassicBattle,
Entwicklungspräsentation, Laden, Niederlagenrückkehr und ausdrückliche
Unreal-Pause werden kombiniert. Auch WorldBattle pausiert die Uhr; die
bestehende Kampfabwicklung bleibt erhalten. Debugpause ist ein zusätzlicher
Testgrund, der keine andere Pause freigeben kann. Keine zweite Pauseverwaltung.

GetTime/Day/Hour/Minute/Phase, normierter Tagesfortschritt, Pause und Menütext sind
über C++/Blueprint abrufbar. OnPhaseChanged, OnDayChanged und OnTimeSet wurden im
ersten PIE-Lauf tatsächlich beobachtet und protokolliert. Die wiederholbaren
Folgeläufe prüfen die automatischen Übergänge ohne Python-Delegate-Adapter.
Noch keine Verbraucher für Sonnenbewegung, Beleuchtung, Wetter, KI oder Begegnungen.

## 3. Save-/Load-Integration und Kompatibilität

Bestehendes SaveGame additiv auf Schema 10 erweitert: boolescher Gültigkeitsmarker,
Tag und Tagessekunden. Keine weitere Datei. Snapshot-Capture/Restore, reguläre
manuelle und automatische Sicherung sowie bestehender RAM-Testschutz sind angebunden.

Versionen 1–9 sowie ungültige Zeitdaten fallen nur bezüglich der Uhr auf Tag 1,
09:00 zurück. Die Automation prüft native Serialisierung, Tages-/Nachtzeit,
Bruchteile kurz vor Mitternacht, Legacy-Fallback, Instanz-ID, Erfahrung und AP.
Ein ansonsten ungültiger Spielstand wird ohne Änderung der laufenden Uhr verworfen.

Die manuellen Positionsregeln und der unabhängige Kontrollpunkt bleiben erhalten.
Niederlage führt zu keinem zusätzlichen Zeitsprung. Debugmultiplikator und
Pausengründe werden nicht gespeichert. Nach neuem Editorprozess und neuer
GameInstance wurde derselbe isolierte Disk-Stand exakt mit Tag 7, 23:59 geladen;
vorher normale Geschwindigkeit 1×, danach unveränderte gespeicherte Nachtphase.
Keine automatische Neuschreibung alter Nutzersaves.

## 4. Menü und Entwicklerwerkzeuge

Kleine Uhr im Kopf des bestehenden Reisebuchs: `Tag N – HH:MM Uhr`. Bestehender
0,25-s-Refresh und minutengenauer Rendercache, keine große dauerhafte HUD-Anzeige.
B/A/X/L/R/+ und Tastatur bleiben unverändert. Die PIE-Prüfung verwendet echte
Softwareeingaben über das vorhandene System; keine zusätzliche Hardwarebehauptung.

`pm.WorldClock show`, `set <Tag> <Stunde> <Minute>`, `pause`, `resume`,
`speed <Multiplikator>`, `reset`, `end`. Nur Editor-PIE, in regulären Builds nicht
verfügbar. Erste Änderung aktiviert vorhandenen RAM-Schutz, sofern nicht bereits
ein isolierter Testtransport aktiv ist. Reguläres Speichern blieb im Debugtest im
RAM; `end` stellte den Ausgangszustand wieder her. Geprüft: 5×, 10×, 60×, 0,5×,
Reset auf 1×, ungültige Eingaben und unveränderte vorhandene Speicherdateien.

## 5. Build und Automation

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build `WorldClockV1Build03` | Exit 0 |
| Vollständige Automation `WorldClockV1Automation02` | **267 erfolgreich**, 0 fehlgeschlagen, 0 nicht ausgeführt |
| Neue Weltuhr-Tests | 6 erfolgreich; Zeitformel/Drift/Long Frames, alle Minuten/Grenzen, Konfiguration/Invalidität, 64 Pausenkombinationen, Save/Migration/Atomarität, Menürefresh |
| Strenger QA-Wrapper dieses finalen Automationslaufs | **Exit 0**; 0 den Tests zugeordnete Warnungen |
| Bestehende Gameplay-Automation | Bestandteil derselben 267 Tests; u. a. Fortschritt, Repertoire/AP, KI, Fang, Team, Entwicklung, Classic/WorldBattle und Save |

Die bekannten externen `idevice_id`-Meldungen (`posix_spawn`, Bad CPU type) stehen
weiterhin in Editor-/Startprotokollen. Zusätzlich existieren die bereits im
Ausgangsstand dokumentierten unspezifischen `LogAutomationTest: Error: Condition
failed` vor Beginn der eigentlichen Tests. Diese werden nicht als warnungsfreier
Gesamtlog ausgegeben. In der alten `Dev_TestMap` meldet die Laufzeit außerdem
bestehende Material-Usage-Hinweise zu Laub-Instancing. Diese Assets wurden nicht
verändert. Die gezielten Map-Check-Ergebnisse werden davon getrennt erfasst.

## 6. Tatsächliche PIE-Prüfungen

Alle Sessions starten als gewöhnliches Editor-PIE. Technische Startpositionen
und bestehende Party-/Battle-Fixtures sind ausdrücklich Testaufbau, keine
naturbelassenen Spielerfortschritte. Keine Nutzerslots beschrieben.

| Lauf | Inhalt / Ergebnis |
|---|---|
| `PIE01` | 104 Schritte / 19 Checks: normaler Zeitlauf, Menü/Untermenü, überlappende Pause, Dialog mit vorhandenem Wanderer, tatsächlicher Heilhaus-Ein-/Ausgang, Menü-Save, Innenraum-Load, Dämmerung/Mitternacht, echter ClassicBattle-Sieg und Lernangebote, Nacht-Load; bestanden |
| `PIE02` | Derselbe Ablauf ohne Python-Ereignisadapter; bestanden; gemessen 11,9993 Spielsekunden/Echtsekunde |
| `PIE03` | Wiederholung in frischem Editor; bestanden; gemessen 12,0011 Spielsekunden/Echtsekunde |
| `PIE04` + `Travel06` | Abschließender vollständiger Lauf mit ausdrücklich freigegebenen Python-Testkontexten, danach echter Mapwechsel und Rückweg; beide bestanden |
| `Restart01` | Neuer Editorprozess / frische GameInstance, isolierter Stand aus vorheriger Session: Tag 7, 23:59 exakt wiederhergestellt; bestanden |
| `Defeat01` | Tatsächlicher WorldBattle, Niederlage, bestehende Rückkehr und separater automatischer Testslot; keine Zeitstrafe, manueller Slot bytegleich, Uhr läuft danach weiter; bestanden |
| `Debug01` | Zehn Checks: Befehle, ungültige Zeit, alle Multiplikatoren, RAM-Save und Rücknahme; alle vorhandenen Save-Dateien bytegleich; bestanden |
| `Travel02` | Tatsächlicher OpenLevel-Hin-/Rückwechsel VisualV2 ↔ vorhandene Dev_TestMap; gleiche GI/Uhr, Tag 11 / 18:30 und 5× erhalten, danach reguläres Fortsetzen; bestanden |
| `Cleanup01` + `Travel05` | Minimales Menü, echte QHD-Aufnahme, Speicherbereinigung und anschließender OpenLevel-Hin-/Rückweg; bestanden |

Die reale Zeitmessung verwendet mehrere Sekunden normalen Framefortschritts;
kleine Abweichungen zur Sollrate liegen innerhalb eines Bildintervalls. Der
unabhängige Langzeittest prüft die Formel und variable Framezerlegung auf unter
einer Mikrosekunde Drift. Keine doppelte Fortschreibung wurde beobachtet.

## 7. Echte QHD-Bilder

Lokal unter `Saved/GlumandaV11/LiveUI/WorldClockPIE04.../`:

| Nachweis | Bild |
|---|---|
| Tag 1 – 09:00 | [Start0900](../Saved/GlumandaV11/LiveUI/WorldClockPIE04Start0900/LivePIEViewportQHD.png) |
| Spätere Tageszeit Tag 3 – 16:42 | [Later1642](../Saved/GlumandaV11/LiveUI/WorldClockPIE04Later1642/LivePIEViewportQHD.png) |
| Wiederhergestellter Innenraum | [InteriorLoaded](../Saved/GlumandaV11/LiveUI/WorldClockPIE04InteriorLoaded/LivePIEViewportQHD.png) |
| Automatisch überschrittene Morgendämmerung | [DawnBoundary](../Saved/GlumandaV11/LiveUI/WorldClockPIE04DawnBoundary/LivePIEViewportQHD.png) |
| Tatsächlicher Tageswechsel | [DayRollover](../Saved/GlumandaV11/LiveUI/WorldClockPIE04DayRollover/LivePIEViewportQHD.png) |
| Nachtstand nach Save/Load | [NightLoaded](../Saved/GlumandaV11/LiveUI/WorldClockPIE04NightLoaded/LivePIEViewportQHD.png) |

Jeweils echte laufende Unreal-PIE-/UMG-Darstellung nativ mit 2560×1440 gerendert,
keine Bildskalierung oder Konzeptgrafik. Die unveränderte tatsächliche
Slate-Viewportaufnahme liegt zusätzlich als `ActualSlateViewport.png` daneben;
die QHD-Datei ist separat als Offscreen-Render des laufenden Viewports bezeichnet.
Medien und Rohprotokolle bleiben gemäß Projektregel lokal unter `Saved`.

## 8. Frühere Fehler und Abschluss der Bereinigungsprüfung

- Build01: falscher Headerpfad im neuen Debugwerkzeug; korrigiert.
- Automation01: falsche Array-Syntax ergab nur eine Phasengrenze; Grenztest griff
  ungeschützt auf die zweite zu und brach ab. Array-Konfiguration korrigiert und
  Test gegen ungültige Konfiguration abgesichert. Lauf **nicht bestanden**.
- Editor01/02/03: Weltwechsel nach einem umfangreichen abgeschlossenen
  Python-Prüflauf stürzte in `PreCollectGarbage` ab. Die frühere Vermutung eines
  reinen Python-Delegate-Problems wurde durch PIE03/Travel04 widerlegt. Eine
  einzelne Menü-/QHD-Aufnahme samt GC und anschließendem Weltwechsel funktioniert.
  Abgeschlossene Python-Testkontexte und deren alte Actor-Referenzen werden nun
  vor dem Weltwechsel ausdrücklich freigegeben (`route.clear`, Referenzfreigabe
  und `gc.collect` vor OpenLevel). Der zuvor reproduzierbar fehlgeschlagene
  Gesamtaufbau wurde damit als PIE04 + Travel06 erfolgreich wiederholt. Die
  genaue interne Engine-Fehlerstelle ist nicht vollständig symbolisiert; die
  ersten drei GC-Abstürze bleiben ausdrücklich als fehlgeschlagene Nachweise
  erhalten. Keine Weltuhr-/Gameplayänderung war für diese Werkzeugkorrektur nötig.

## 9. Grenzen und Dateischutz

Noch keine Tag-Nacht-Beleuchtung, Wetter- oder KI-Tagesrhythmen; die APIs sind
vorbereitet. Keine Offline-Zeitfortschreibung. Reale Controllerhardware wurde in
diesem Auftrag nicht erneut geprüft. Starten einer neuen PIE-Session ist weiterhin
kein ungefragtes Auto-Laden eines Nutzersaves; Fortsetzen geschieht über Laden.

Die Abschlussprüfung vergleicht alle 78 ursprünglichen geschützten Dateien
(zwölf Maps, 31 bereits unversionierte Original-/Werkzeugdateien und bestehende
Save-Dateien) per SHA-256 sowie beide Vollbackup-Refs. Kontrollmedien, Testslots und
Rohprotokolle werden nicht versioniert. Kein Modell, keine Animation, keine
Beleuchtung, kein KI-Profil und keine Controllerbelegung geändert.

Abschlussnachweis `Saved/ProjectRefinement/WorldClockV1/FinalVerification.json`:
alle **78** ursprünglichen Dateien unverändert, **31** ursprüngliche unversionierte
Dateien erhalten, beide Vollbackup-Refs unverändert. Zwölf finale Map Checks
jeweils **0 Fehler / 0 Warnungen**. Editor-Szeneninventur identisch, keine dirty
Map-/Content-Pakete; finale Editorsitzung ohne die geprüften kritischen Fehlermuster.
Der eigene Editor wurde regulär geschlossen.

## 10. Git-Abschluss

Implementierungscommit: **`bf83a4bdcd9c544da0f8f18d99fa608733a08813`**,
`feat(time): add persistent world clock and protected PIE controls`.
26 gezielt geprüfte Konfigurations-, Quell-, Werkzeug- und Dokumentationsdateien.
Keine Content-/Art-Dateien oder Testmedien im Commit.

Normaler Push auf `origin/main` erfolgreich. Danach Fetch und serverseitiges
`ls-remote`: exakt derselbe Commit, `main...origin/main` = **0 / 0**. LFS-Status
und Push-Dry-Run zeigen keine ausstehenden Objekte. Es gibt keine neuen oder
geänderten LFS-Assets; historische Assets wurden nicht vollständig neu geladen.
Kein Force-Push, keine Historyänderung und keine Budgetänderung.

Dieser abschließende Berichtsnachtrag wird separat als Dokumentationscommit
normal gesichert; dessen exakter Abschluss-Hash steht im Git-Verlauf und im
lokalen `Saved/ProjectRefinement/WorldClockV1/GitFinal.json`. Danach werden Remote,
Dateischutz, ursprüngliche unversionierte Dateien und Backup-Refs erneut geprüft.
