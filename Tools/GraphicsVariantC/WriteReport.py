"""Render the report from completed measurements; never invent performance values."""
from pathlib import Path
import json,statistics as st
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';rows=[r for r in json.loads((D/'Summary.json').read_text())['rows']if r['batch']in ['PIEMatrix01','NativeMatrix01']];assert len(rows)==24
for label in ['PIEFinalProof','NativeFinalProof']:assert json.loads((D/label/'Result.json').read_text())['passed']
assert json.loads((D/'ProtectionFinal.json').read_text())['changed_or_missing']==[]
def val(mode,site,p):return next(x for x in rows if x['mode']==mode and x['site']==site and x['percentage']==p)
def n(x):return f'{x:.2f}'.replace('.',',')
def table(headers,body):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,r))+' |'for r in body])
sites=['Dorf','Wiese','Wald','Waldweg','Gewaesser','Gruppe'];tables={}
for mode in ['Native','PIE']:
 tables[mode]=table(['Ort','FPS 100 %','FPS C / 75 %','Spanne C (3 Läufe)','GPU 100 → C (ms)','Frame C (ms)','Game C (ms)','Render C (ms)','Frame-p95 C (ms)'],[[s,n(val(mode,s,100)['fps']),n(val(mode,s,75)['fps']),n(val(mode,s,75)['fps_min_run'])+'–'+n(val(mode,s,75)['fps_max_run']),n(val(mode,s,100)['gpu_ms'])+' → '+n(val(mode,s,75)['gpu_ms']),n(val(mode,s,75)['frame_ms']),n(val(mode,s,75)['game_ms']),n(val(mode,s,75)['render_ms']),n(val(mode,s,75)['frame_p95_ms'])]for s in sites])
photo=table(['Szene','100 %','C / 75 %'],[[s,f'[Original QHD](../Saved/ProjectRefinement/GraphicsVariantC/Photos01/{s}_10000000.png)',f'[Original QHD](../Saved/ProjectRefinement/GraphicsVariantC/Photos01/{s}_C00000.png)']for s in sites+['Gruppe22']])
q=json.loads((D/'NativeMatrix01-Thermal.jsonl').read_text().splitlines()[-1]);thermal=sorted(set(json.loads(l)['label']for l in (D/'NativeMatrix01-Thermal.jsonl').read_text().splitlines()))
report=f"""# Grafikstandard Variante C – Prüfbericht

Stand: 27.10.2026. Ausgangscommit `9c362f0321364a96a845c969bda2d84a72376eea`.

## Ergebnis

Variante C ist der neue Standard für neue Spiel-/PIE-Welten: **2560×1440 Ausgabe,
High, 75 %, intern 1920×1080, nativer temporaler Upscale-Pfad TAAU auf VisualV2/Metal**.
Der unveränderte High/100-%-Vergleich bleibt verfügbar. Keine Gameplay-, Map-,
Modell-, Animations- oder Beleuchtungsänderung in diesem Auftrag.

**30 FPS flächendeckend nicht erreicht.** Im separaten Spielprozess liegen die
Szenenmittel bei 23,48–33,39 FPS; nur die offene Wiese erfüllt hier das 30-FPS-Ziel.
Die wiederholte PIE-Serie erreicht 18,35–28,77 FPS; eine abschließende kurze
Dorf-Abnahme nur 14,91 FPS. Im direkten aktuellen A/B-Vergleich gewinnt C im
separaten Prozess je Szene 34,3–40,5 % FPS; GPU-Zeit sinkt um 27,3–30,9 %.
Das ist ausdrücklich ein Vorteil durch reduzierte interne Auflösung, keine
Beschleunigung bei unverändertem nativen QHD/100 %.

## Umsetzung und Bedienung

- `pm.Graphics C`: Standard wieder aktivieren.
- `pm.Graphics 100`: QHD/High/100-%-Vergleich.
- `pm.Graphics status`: angefordertes Profil und effektiven Screen Percentage ausgeben.
- `-PMGraphicsProfile=100`: Vergleich beim Prozessstart.

Die Wahl gilt im laufenden Prozess einschließlich Mapwechsel; Neustart verwendet C.
`pm.DayNight C` bleibt die separate **85°-Lichtoption**; Mittagssonne weiterhin 75°.
Keine Controllerbelegung geändert.

`UPokeMonsterGraphicsProfile` ist eine nicht tickende Rendering-Anbindung an echte
Game-/PIE-Welten, mit vorhandenen `UGameUserSettings`, Scalability und vorhandenen
reversiblen CVar-Scopes. Default-Konfiguration in `DefaultPokeMonsterGraphics.ini`
und `DefaultGameUserSettings.ini`. Kein ApplySettings/SaveSettings und keine
Schreibzugriffe auf Pokémon-Saves. Die öffentliche Scalability-ResolutionQuality
wird direkt gesetzt, damit DesiredScreenWidth/Height des Nutzers erhalten bleiben.
Die übrigen elf Qualitätsgruppen stehen auf High (2); Unreals Gesamtlabel kann wegen
der individuellen ResolutionQuality trotzdem „Custom“ / -1 sein.

Fester Render-Viewport 2560×1440, dynamische Auflösung aus, sekundärer Skalierungsfaktor
1. VisualV2s vorhandene TAA-Anbindung bleibt unverändert. Keine neuen Plugins oder
Upscaler-Abhängigkeiten. Der kleinere eingebettete Editorbereich kann die QHD-Ausgabe
für die Anzeige herunterskalieren; das ist nicht die interne Renderauflösung.
Explizite höherrangige Konsolen-Overrides werden respektiert und können das Profil
überstimmen. Vergleich über die Profilbefehle, nicht über konkurrierende rohe CVars.

Beim Weltende werden die eigenen Overrides und vorherigen Editor-/Nutzereinstellungen
zurückgegeben. Ein zunächst gemessener Fehler (Editor behielt 75 % statt vorher 0)
wurde korrigiert. Nach C → 100 → C und nach vier Gameplay-PIE-Zyklen stimmen alle
geprüften Werte wieder exakt. Abschließend zusätzlich Auflösung, Fenstermodus,
dynamische Auflösung und öffentlich abfragbare gewünschte Display-Skalierung verglichen.
Keine parallele Gameplay- oder Speicherarchitektur.

## Hardware und Messmethode

MacBook Air Mac16,12, Apple M4 (10 CPU-/10 GPU-Kerne), 16 GB gemeinsamer Speicher,
macOS 27.0.1 (26A434), Unreal 5.8.2 CL 56702186, Metal SM6. Internes Display
2560×1664; gemessener Spiel-Render-Target 2560×1440. Hardware entspricht dem
vorigen Performancebericht. Keine Bildschirm-/Videoaufnahme während der Zeitmessung.

Sechs identische Standorte, je drei C/100-Paare, Reihenfolge C/100, 100/C, C/100.
Je Fenster 4 s Warm-up und 6 s Messung. 36 Fenster im normalen PIE, 36 im separaten
Unreal-`-game`-Prozess bei geschlossenem Editor; zusätzlich vier kurze Abnahmefenster
mit dem endgültigen Build. Das ist **kein paketierter Shipping-Build**.

Beide Profile verwenden High, dieselbe Kamera (-50° Pitch, -45° Yaw, 35° FOV),
Weltuhr 12:00 beim Beginn jedes Fensters, normalen dynamischen Zeitverlauf,
unveränderte Mittagssonne und dieselben Habitatinstanzen. Kontaktprofile nur im
isolierten Benchmark deaktiviert, damit keine zufälligen Kämpfe Messfenster überlagern;
KI-Bewegung bleibt aktiv. Stochastische Pokémon-Positionen und Frameausreißer sind
nicht bitgenau synchronisiert. Die Fenster sind kurze reproduzierbare Stichproben,
keine Garantie für die schlechtesten Situationen des vollständigen Spiels.

Der Profiler wird im neuen Modus **GraphicsProfileActive** zum Beobachter: Er erzwingt
weder Prozentwert, Qualitätsgruppen, VSync, FPS-Grenze noch Fensterauflösung.
Vor jeder Messung prüft Python die produktiven Werte, statt sie richtigzusetzen.
Kein `-ForceRes`, `-ResX` oder `-ResY` im separaten Start. Beide gewöhnlichen Starts
wurden vor dem ersten Profilbefehl als High/75 % bestätigt.

Renderer-Nachweis aus realen Frames: Viewport, Render-Target und UnscaledViewRect
2560×1440; feste Treiberfraktion 0,75, sekundär 1, ScreenPercentage-Showflag aktiv,
AA-Methode 2 (TAA), PrimaryScreenPercentageMethod 1 (TemporalUpscale). Daraus ergibt
sich nach UE-Aufrundung 1920×1080; bei 100 % 2560×1440. Die internen Maße sind aus
dem tatsächlich aktiven festen Treiber abgeleitet, **kein Textur-Allocation-Readback**.
Dynamische Auflösung ist aus; der öffentliche Treiber-Bound ist hier die feste Fraktion.
Sämtliche Messframes werden darauf validiert. Die Rohdaten und zusätzliche GPU-Pässe
bleiben unter Saved, nicht in Git.

FPS = 1000 / mittlere echte Framezeit je Fenster; Tabellen zeigen den Mittelwert der
drei Fenster. p95 = Mittel der jeweiligen Frame-p95-Werte. CPU-Render-Zeit ist eine
Wall-Time einschließlich möglichem GPU-Warten, keine reine CPU-Rechenzeit. Der
PIE-CSV-Zähler RenderThreadTime liefert 0; das ist **nicht** als kostenfreier Renderer
zu interpretieren. Game Thread ist deutlich kleiner als die GPU-Zeit, passend zur
weiterhin überwiegenden GPU-Begrenzung. Gemeldete thermische Zustände im separaten
Lauf: {', '.join(thermal)}. Schwankungen belegen keine bestimmte thermische Ursache.

## Aktueller direkter Vergleich: separater Spielprozess

{tables['Native']}

## Aktueller direkter Vergleich: PIE

{tables['PIE']}

Die GPU-Zeit alleine ist nicht die vollständige Framezeit. Auch im Dorf mit knapp
30 FPS sind 33,3 ms nicht zuverlässig eingehalten. Es wird keine globale 30-/60-FPS-
Freigabe behauptet.

## Abschließende kurze Abnahme mit Build07

Die großen Matrizen stammen aus den vorherigen Profil-Builds. Danach wurden nur
Wiederherstellung und der nicht gerenderte DesiredScreenWidth/Height-Cache der
GameUserSettings korrigiert; die geprüften Renderer-Eingaben bleiben gleich.
Mit Build07 wurden beide echten Starts und der Renderpfad erneut geprüft,
zusätzlich folgende kurze Dorf-Fenster (2 s Warm-up, jeweils 3 s Messzeit):

| Betrieb | FPS 100 % → C | GPU 100 % → C |
| --- | --- | --- |
| PIE | 11,74 → 14,91 | 71,65 → 53,40 ms |
| Separater Prozess | 17,42 → 24,36 | 53,68 → 37,75 ms |

Diese kürzeren Einzelproben werden nicht mit den dreifach gemessenen Serien gemischt.
Sie zeigen höhere absolute Kosten als frühere Dorf-Fenster; Aufwärmung, Systemlast,
Speicher-/Cachezustand und Tageszyklus sind mögliche, hier nicht isoliert bewiesene
Einflüsse. Kein garantierter FPS-Wert für jeden Start. In beiden späten Proben
bleibt C schneller; die Ausgabe-/Treiber-/High-Werte sind erneut bestätigt.
Gerade diese Streuung verbietet eine pauschale 30-FPS-Zusage.

## Vergleich mit bisherigen Messungen

Historische Referenz: [Performanceoptimierung V1](VISUALV2_PERFORMANCEOPTIMIERUNG_V1.md).
Damals nativer High/100-%-Lauf nach Bodenoptimierung: Dorf 22,01, Wiese 22,81,
Wald 16,80, Waldweg 18,58, Gewässer 16,93, Gruppe 19,27 FPS. Die aktuellen nativen
100-%-Werte 17,04–23,76 FPS liegen in ähnlicher Größenordnung; Unterschiede sind
keine isoliert bewiesenen Codegewinne. Insbesondere lag Harrys DefaultEngine.ini-WIP
mit aktivierten HardwareRayTracing-/Nanite-Projektoptionen bereits vor diesem Auftrag
vor und wurde für beide aktuellen Profile unverändert erhalten. Andere Sitzung,
Hintergrundlast, Aufwärmung und KI-Zustände begrenzen den historischen Vergleich.

Der frühere einzelne High/75-%-Alternativstandort erreichte 27,41–29,71 FPS bei
30,12–33,19 ms GPU. Seine Position (-2960,1700) ist nicht der aktuelle Waldmesspunkt
(-4300,1550). Medium/75-%-Ergebnisse sind ebenfalls keine High-Ergebnisse.
Maßgeblich für die Wirkung von C ist der oben direkt gepaarte aktuelle Vergleich.

## Bildqualität – echte QHD-Paare

{photo}

Alle 14 PNGs sind 2560×1440. Pro Paar identische Position, Kamera, FOV, Weltzeit und
pausierte Spielsekunde; keine künstlichen Bilder. Normale Viewport-`Shot`-Aufnahme,
kein HighResShot, das den 75-%-Pfad für den Qualitätsvergleich umgehen könnte.
UE ergänzte bei diesem Lauf den Dateisuffix 00000; die nachgewiesenen Originalpfade
stehen in PhotoValidation.json. Das Werkzeug verwendet künftig den korrekten
`-nosuffix`-Parameter.

Sichtprüfung: Wald, Wiese, Weg, Gebäude und Wasser behalten Dichte, Licht und
Schattenstruktur. Figur und kleine Bisasam bleiben in der Nachtaufnahme erkennbar.
Feine Gras-/Blattkanten und Haar-/Kleidungsdetails sind bei C etwas weicher als bei
100 %, ohne bewusst abgesenkte Material-/Texturqualität. Die Bilder sind statische
Qualitätsvergleiche; keine pauschale Aussage über Flimmerfreiheit oder TAA-Ghosting
in jeder Bewegung. Die vorhandene Bewegungssteuerung wurde zusätzlich im echten PIE
geprüft, keine interpolierten Videos oder vervielfachten Frames erzeugt.

## Technische und Gameplay-Prüfungen

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Editor-Build, endgültig Build07 | Exit 0, 9,64 s |
| Vollständige Projekt-Automation04 | 280 funktional erfolgreich, 0 fehlgeschlagen/ausgelassen |
| Strenger unveränderter QA-Wrapper04 | **Exit 1**, 279 ohne und 1 mit Warnungen |
| Warnungsursache | Zwei externe iOS-idevice_id-Warnungen, Bad CPU type (86), im NPC-Test; keine funktionalen Testfehler |
| Voriger Automation03-Wrapper | Exit 0 / 280 ohne Warnungen, vor letzter reiner User-Settings-Cache-Korrektur |
| Zwölf bestehende Maps, MAP CHECK | Je 0 Fehler und 0 Warnungen, keine Map gespeichert |
| Gameplay.py | 18 echte PIE-Prüfpunkte bestanden |
| Travel.py | Vier Prüfpunkte, VisualV2 → Dev_TestMap → VisualV2; Profil C bleibt aktiv |
| Bewegung/Sprint/Menü | Acht Richtungen, L3 Toggle, X, D-Pad, L/R, A; fünf Prüfpunkte bestanden |
| Save/Load-Zyklus | Position, Uhr, Team, Steuerung und Profil C; drei Prüfpunkte bestanden |
| Profil-Smoke und endgültige Renderer-Abnahme | Standard ohne Befehl, 100, C; zusätzliche kurze PIE-/separate C/100-Messfenster |
| Editor-Rückgabe | Exakter Vorher-/Nachher-Abgleich, auch nach vier Gameplay-Zyklen |
| Schutzprüfung | 3979 Originaldateien inklusive 327 vorhandener .sav und 33 initialer unversionierter Dateien unverändert |

Der zusammenhängende Gameplaylauf enthält Weltuhr-Pause/Fortsetzung, 75°/85°-Licht-
option, beschleunigte Morgendämmerung, echten Gebäudeein-/austritt, Nacht-Save/Load
mit Innenraumkamera, Team/KP/AP und unabhängigem Kontrollpunkt, Mitternacht,
ClassicBattle-Sieg mit bestehender B-Bestätigung/A-Lernangebotbehandlung und
Rückkehr der Steuerung. Mapreise erhält Teamidentität, einen Begleiter und acht
konfigurierte Wild-KI-Instanzen. Eingaben sind Softwareprüfungen, kein neuer
physischer Switch-Pro-Test. Fang/Entwicklung/Repertoire zusätzlich durch bestehende
vollständige Automation, hier kein separater neuer manueller Fang-/Entwicklungsfilm.

Einmaliger Editorabsturz in EditorC02 direkt nach PIE-Start:
`pthread_rwlock_init failed with error: 16`, PThreadsSharedMutex.h, anschließendes
SIGSEGV in einer asynchronen Engine-Task während Editor-Ticks. Kein belastbarer
Nachweis für eine bestimmte Projektursache; kein Engine-/Gameplay-Fix auf Verdacht.
Prozess endete selbst, **kein Force Quit**. Danach erfolgreiche Start-/Stopp-/Reise-
und endgültige Profilprüfungen. Ursache bleibt offen; Stabilität nicht als dauerhaft
bewiesen darstellen. Log EditorC02.log erhalten.

Frühe Arbeitsversuche sind keine Abnahme: Build02/03 scheiterten an in dieser UE-
Version nicht öffentlichen Renderer-APIs; korrigiert auf öffentlichen festen Treiber.
Automation01 startete nach unvollständigem Link nicht, daher keine ausgeführten
Funktionstests. Ein EditorState-Zusatz versuchte zunächst eine geschützte UE-Eigenschaft
zu lesen; auf öffentliche GetDefaultResolutionScale-Abfrage korrigiert. Keine
Engine-Dateien geändert. Die Endergebnisse oben sind gesondert belegt.

## Schutz, Git und lokale Nachweise

Alle ursprünglichen Art-/Content-Dateien, Maps, Meshy-Originale, Nutzersaves,
33 initialen unversionierten Eingänge/Werkzeuge, beide Vollbackup-Refs und die
bereits vorhandenen DefaultEngine.ini-Änderungen bleiben erhalten. Letztere sind
**nicht Bestandteil des Commits**. Keine neuen Maps, Worktrees, Projektkopien,
Modellvarianten oder Backups. Nur neue klar benannte isolierte QA-Slots.

Produktiv geändert: zwei neue Default-INI-Dateien und eine kleine Rendering-Klasse.
Dazu ein Automationstest, reine Entwickler-Profilermessung, QA-Werkzeuge und
Dokumentation. Keine neuen LFS-Assets. Prüfdaten/Medien verbleiben lokal unter
`Saved/ProjectRefinement/GraphicsVariantC/`.

Wichtige Nachweise: `Summary.json`, `Measurements.json`, `PhotoValidation.json`,
`DefaultPIEUnforced.json`, `DefaultPIEBuild07.json`, `NativeMatrix01-Default.json`,
`NativeFinalProof-Default.json`, `EditorBuild07Before/After.json`,
`GameplayStops.json`, `MapCheckLogValidation.json`, `ProtectionFinal.json`.
Build und Automation daneben in `GraphicsVariantCBuild07` und
`GraphicsVariantCAutomation04`. Abschließende Commit-/Remote-/LFS-Prüfung in
`GitFinal.json` und der Chat-Abschlussmeldung. Kein LFS-Budget oder Abrechnung
verändert. Exakte Befehle/Prüfwerkzeuge im [Werkzeug-README](../Tools/GraphicsVariantC/README.md).
"""
(R/'Docs/GRAFIKPROFIL_VARIANTE_C_PRUEFBERICHT.md').write_text(report)
print('Report created from completed results')
