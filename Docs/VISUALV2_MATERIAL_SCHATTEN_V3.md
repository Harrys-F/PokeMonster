# VisualV2 – Material- und Schattenoptimierung V3

Stand: 27.10.2026. Messungen, abgeschlossene Regression und Git-Abschluss sind getrennt ausgewiesen.

## Ergebnis und Leistungsziel

Übernommen wird ausschließlich das gerichtete VSM-SMRT-Sampling von acht auf vier Strahlen für VisualV2 im Standard-Grafikprofil C. Vier Samples pro Strahl, Schattenauflösung, Reichweite, Baumkronen, Vegetationsdichte, Lumen-HWRT, Distance Fields, TAAU, High, Weltuhr und Sonnenbahn bleiben erhalten. Andere Maps, Editor-Vorschau und das bisherige 100-%-Vergleichsprofil werden nicht angepasst.

**Stabile 30 FPS mit Reserve sind nicht erreicht.** Die längere gepaarte Vergleichsreihe liegt in Dorf und Wald unter 30 FPS. Eine kurze frische Produktionskontrolle überschreitet im Mittel 30 FPS, hat aber Frame-p95 über 33,3 ms. Diese Ergebnisse werden getrennt berichtet.

## Messbasis und Schutz

- Projektbasis `01ae3fd36c17f181dfb49956ee4a8b7eb4aa3151`; zu Beginn main = origin/main.
- Apple M4, Mac16,12, zehn GPU-/zehn CPU-Kerne, 16 GiB gemeinsamer Speicher, macOS 27.0.1; UE 5.8.2 CL 56702186, Metal SM6.
- Separater ungepackter Development-Spielprozess (`UnrealEditor -game`), nicht Shipping und nicht PIE; MacEditor-Device-Profil.
- Ausgabe 2560×1440, intern 1920×1080, Primärfaktor 0,75, Sekundärfaktor 1, tatsächliches AA=2/TAA und temporales Upscaling=1. Sämtliche elf Nicht-Auflösungs-Scalabilitygruppen High=2.
- Lumen-HWRT/Inline=1, VSM=1, DistanceFieldShadowing=1 bleiben aktiv. Kein Wechsel zu Software-Lumen, SSGI oder gebackenem Licht.
- Vorhandene Nutzeränderungen an `Config/DefaultEngine.ini` (HWRT, Nanite-Projektfreigabe und Sichtbarkeitswarnung) bleiben unverändert und werden nicht mitcommittet. Die Messung beschreibt ausdrücklich diesen lokalen Ausgangszustand.
- Je 4 s Aufwärmen und 5 s Messung, drei Wiederholungen je Ort/Uhrzeit/Konfiguration, wechselnde A/B-Reihenfolge. 120 Fenster und 17730 tatsächlich validierte Frames. Keine Videoaufnahme während der Messung.
- Jeder Frame wurde auf Ausgabe-/interne Auflösung, TAA-Upscale, High/75 % und aktives Fenster geprüft. FPS = 1000 / mittlere Framezeit je Lauf; Tabellen mitteln diese Laufwerte. Frame-p95 wird aus den zusammengeführten Frames der drei Läufe berechnet.
- Normal laufende Weltuhr, Start jedes Fensters zur bezeichneten Stunde; 120 Echtminuten/Tag. Kontaktprofile der zwölf Wildinstanzen nur im RAM des Benchmarks deaktiviert, vorhandene Bewegung bleibt aktiv. 1495 Welt-Actors im Inventar; diese Anzahl ist keine Anzahl gleichzeitig sichtbarer Figuren.
- Ausschließlich kopierter QA-Spielstand in frischem eigenem `-UserDir`; keine Schreibzugriffe auf normale Nutzer-Slots.

Die längere Reihe umfasst viele Orts-/Zeitsprünge und zunehmende Laufzeit. Globale GPU-Zeiten schwankten; NSProcessInfo meldete nominal/fair (0/1). Ein früher Versuch driftete sogar bei Originalkontrollen von etwa 31 auf 67 ms GPU. Dieser Versuch begründet keine Optimierungsentscheidung. AC-Betrieb, Akku 100 %, Low-Power-Modus 0 wurden lesend bestätigt. Thermik, Cachezustand und Hintergrundlast sind mögliche Einflüsse; eine isolierte GPU-Takt-/Temperaturursache ist nicht nachgewiesen. Kurze und längere Messungen dürfen nicht direkt als Versionsgewinn verglichen werden.

## Materialanalyse

Unveränderte Szene: 106 Umwelt-Materialmaster inventarisiert, Graphverbindungen, Custom-HLSL, Texturen, Maskierung, Two-Sided-Flags, WPO, Mesh-/LOD-/Instanz- und Schattenflags geprüft. Editorstatistiken sind keine Metal-ISA-Instruktionsmessung; eingebettete HLSL-Texture.Load-Zugriffe werden dort nicht vollständig als Texture Samples sichtbar.

| Gruppe | belegte Eingrenzung | Bewertung |
|---|---|---|
| Fünf Wege / zwei Master | Dorf Base Pass 7,86→4,13 ms, Wald 7,79→3,72 ms beim vorübergehenden Ausblenden | stärkster belegter Ansatz; prozedurale Farb-/Maskenberechnung, je 118 Segmentabstände in Custom-HLSL |
| Gras/Bodenpflanzen | Dorf 7,86→6,86 ms, Wald 7,79→5,97 ms | messbarer Gruppenbeitrag; viele Instanzen/Überlagerungen, bereits ohne eigene Schatten |
| Gebäude | Dorf 7,86→6,99 ms; im Wald praktisch keine Base-Pass-Ersparnis | lokaler Beitrag, kein allgemeiner Spitzenreiter |
| kleinere Dekoration | Dorf 7,86→7,62 ms, Wald 7,79→7,42 ms | kleinerer Beitrag |
| Boden | Dorf 7,86→7,56 ms, Wald 7,79→7,72 ms | vorhandener statischer Farbbake bereits aktiv; Gesamtszenen-GPU ändert sich zusätzlich durch GI/Schattenempfänger |
| Baumkronen | Ausblenden erhöht Base Pass auf 9,48/8,69 ms, reduziert aber Shadow Projection | Materialkosten nicht separat isolierbar: freigelegte Hintergrundflächen verfälschen die Differenz |
| Sträucher | etwa 0,1 ms Base-Pass-Differenz | kein vorrangiger Engpass |

Diese 54 Fenster mit je drei Wiederholungen sind Sichtbarkeits-Ablationen, keine vorgeschlagene Entfernung von Objekten. Sie verändern auch Verdeckung, GI und Schattenempfänger. Fünf präzise Einzelmaterial-Kosten lassen sich daraus nicht seriös angeben. Masked Overdraw ist ein plausibler Anteil bei dichter Vegetation, wurde aber nicht separat in ms isoliert.

Inventar: 41 Baumkomponenten mit Schatten/Distance-Field-Beitrag, 129 Komponenten/6228 Instanzen in der Sammelgruppe kleiner Pflanzen, 50 Komponenten/150 Instanzen Sträucher. Kleine Pflanzen und Sträucher werfen bereits keine eigenen Schatten. LOD0-Dreieckssummen sind Inventarobergrenzen und keine gemessenen sichtbaren Dreiecke. Teilweise erfasst die Pflanzennamensgruppe auch innen liegende Kräutermöbel; deren unsichtbarer Beitrag wird nicht als Pflanzenkosten ausgegeben.

Kronen: masked/two-sided, Editorwert 208 Pixelshader-Instruktionen, kein verbundener WPO-Ausgang. Zwei Texture Samples im Editorwert. Der Auto-VSM-Invalidierungsmodus bleibt erhalten; es gibt hier keinen belegten windbedingten WPO-Invalidierungsfehler.

## Verworfen: Materialvarianten

| Versuch | Editorwert Main/North | Nachweis / Entscheidung |
|---|---:|---|
| Original | 1647 / 1735 | erhalten |
| expliziter Branch vor Routensuche | 1647 / 1735 | dreifach gemessen; kein belastbarer Vorteil |
| konservative räumliche Segmentvorauswahl | 2478 / 2566 | mehr Shaderaufwand; kein belastbarer Vorteil |
| Vorauswahl mit spätem Rückfall nur bei relevanten Breiten-Grenzfällen | 2485 / 2573 | 18 Kontroll-/Versuchsfenster; kein belastbarer Vorteil |

Die Vorauswahl speicherte nur Kandidaten-IDs; Originalsegmentdaten und Distanzformel blieben erhalten. CPU-Gegenprüfung mit 36641 Punkten sowie eine echte 1024²-Metal-GPU-Gegenprüfung mit Positivkontrolle: Breiten identisch, Distanzabweichung unter 0,001 cm im geprüften Raster. Das beweist keine Beschleunigung. Keine Variante wird eingebunden. Sieben neu erzeugte, unreferenzierte Versuchsassets und ihre ausschließlich eigenen Erzeugungsquellen wurden nach Registry-Prüfung entfernt; kein Originalmaterial wurde überschrieben.

## Schattenanalyse und Änderung

VSM-Caching ist aktiv. Sonnenrotationen invalidieren Richtungslicht-Cacheeinträge; der Engine-Code beschreibt diesen Übergang ausdrücklich. Die bestehende 0,1-s-Auswertung mit 0,025°-Rotationsschwelle erzeugt tagsüber etwa 1,8 tatsächliche Rotationsanwendungen/s. Eine temporäre 0,05°-Schwelle reduzierte diese etwa auf die Hälfte, lieferte aber keinen ausreichend klaren Gesamtvorteil. Keine dauerhafte Änderung der Tag-Nacht-Steuerung.

Baum-Distance-Field-Beteiligung separat aus-/eingeschaltet, globale Verfahren erhalten: kein ausreichend klarer Gewinn. Der ergänzende DF-Schattenpass liegt in der Diagnose bei etwa 0,26–0,35 ms. Die Baumänderung beseitigt diesen Pass nicht; daraus folgt keine belegte vollständig redundante Berechnung. Nicht übernommen.

In der finalen Mittagsreihe bleibt Lumen Screen Probe Gather praktisch unverändert: Dorf 6,50→6,44 ms, Wald 6,72→6,68 ms; ergänzende DF-Schatten etwa 0,29–0,38 ms. Die ursprünglich genannten 5,5–5,7 ms sind damit kein neu gemessener Wert dieses längeren Laufs. Keine besondere neue Lumen-Kostenursache durch das reduzierte VSM-Sampling belegt.

Vier VSM-Strahlen reduzieren den gerichteten Samplinganteil, nicht die Schattenauflösung oder die Geometrie. 4 Samples/Strahl bleiben erhalten. Der gemessene gesamte Shadow-Projection-Pass sinkt in Außenbereichen typischerweise um etwa 0,2–0,8 ms. Daraus darf keine Halbierung der gesamten Schatten- oder Framekosten abgeleitet werden.

Implementierung: ausschließlich `UPokeMonsterGraphicsProfile::SelectProfile`, vorhandene `FPokeMonsterEnvironmentCVarOverride`-Verwaltung. Exakter World-Paketname nach PIE-Präfixentfernung und Profil C erforderlich. Beim Verlassen/Ende wird der vorherige Wert einschließlich Priorität wiederhergestellt, sofern kein Nutzer-Override übernommen hat. Keine neuen Actors, Timer, Gameplay- oder Speicherfelder.

## Vollständige längere Vergleichsreihe

SD = ShadowDepths, SP = ShadowProjection, BP = Basepass. GPU-Pässe sind CSV-Scopes; sie werden nicht ungeprüft zu einer Framezeit addiert. Draw/RenderThreadTime enthält Warte-/Synchronisationsanteile und ist keine reine CPU-Arbeitszeit. Game Thread liegt deutlich unter der GPU-Zeit.

| Ort | Uhr | Strahlen | FPS | GPU ms | BP ms | SD ms | SP ms | Frame-p95 ms | Game ms | Draw ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dorf | 6:00 | 8 | 26.92 | 34.16 | 7.81 | 2.42 | 3.40 | 42.53 | 2.25 | 37.47 |
| Dorf | 6:00 | 4 | 27.39 | 33.47 | 7.79 | 2.43 | 2.66 | 42.15 | 2.16 | 36.85 |
| Dorf | 12:00 | 8 | 25.25 | 35.97 | 7.92 | 2.42 | 3.43 | 42.65 | 2.21 | 39.61 |
| Dorf | 12:00 | 4 | 25.92 | 35.03 | 7.93 | 2.40 | 2.83 | 42.32 | 2.09 | 38.62 |
| Dorf | 19:00 | 8 | 25.34 | 36.27 | 8.00 | 2.60 | 3.39 | 42.34 | 2.30 | 39.48 |
| Dorf | 19:00 | 4 | 25.52 | 36.01 | 8.03 | 2.60 | 2.83 | 42.11 | 2.24 | 39.20 |
| Dorf | 22:00 | 8 | 25.85 | 35.53 | 7.95 | 1.99 | 3.44 | 40.58 | 2.14 | 38.67 |
| Dorf | 22:00 | 4 | 26.44 | 34.67 | 7.95 | 1.98 | 2.83 | 39.80 | 2.16 | 37.80 |
| Wiese | 6:00 | 8 | 35.76 | 25.47 | 1.75 | 2.32 | 2.58 | 32.86 | 2.40 | 28.30 |
| Wiese | 6:00 | 4 | 35.93 | 25.32 | 1.79 | 2.30 | 2.37 | 32.89 | 2.37 | 28.16 |
| Wiese | 12:00 | 8 | 32.57 | 27.61 | 1.86 | 2.32 | 2.90 | 33.05 | 2.33 | 30.70 |
| Wiese | 12:00 | 4 | 32.83 | 27.38 | 1.87 | 2.33 | 2.66 | 32.90 | 2.41 | 30.47 |
| Wiese | 19:00 | 8 | 31.39 | 28.90 | 1.83 | 3.43 | 3.27 | 35.64 | 2.41 | 31.86 |
| Wiese | 19:00 | 4 | 31.79 | 28.46 | 1.83 | 3.43 | 2.73 | 35.14 | 2.38 | 31.45 |
| Wiese | 22:00 | 8 | 32.84 | 26.99 | 1.83 | 2.05 | 2.88 | 32.28 | 2.20 | 30.44 |
| Wiese | 22:00 | 4 | 33.14 | 26.72 | 1.82 | 2.11 | 2.60 | 31.81 | 2.20 | 30.18 |
| Waldweg | 6:00 | 8 | 28.64 | 31.57 | 4.68 | 3.21 | 3.43 | 42.11 | 2.14 | 35.25 |
| Waldweg | 6:00 | 4 | 28.89 | 31.30 | 4.74 | 3.25 | 2.76 | 42.05 | 2.13 | 35.04 |
| Waldweg | 12:00 | 8 | 25.85 | 34.60 | 4.99 | 3.12 | 3.85 | 42.52 | 2.21 | 38.73 |
| Waldweg | 12:00 | 4 | 26.60 | 33.50 | 4.94 | 3.04 | 3.06 | 41.50 | 2.11 | 37.62 |
| Waldweg | 19:00 | 8 | 26.79 | 33.45 | 4.79 | 3.39 | 3.51 | 40.93 | 2.11 | 37.32 |
| Waldweg | 19:00 | 4 | 27.04 | 33.12 | 4.89 | 3.49 | 2.84 | 40.79 | 2.17 | 36.99 |
| Waldweg | 22:00 | 8 | 27.15 | 32.95 | 4.91 | 2.66 | 3.48 | 38.85 | 2.10 | 36.83 |
| Waldweg | 22:00 | 4 | 27.84 | 32.05 | 4.88 | 2.65 | 2.82 | 37.54 | 2.06 | 35.91 |
| Wald | 6:00 | 8 | 26.77 | 34.52 | 8.01 | 2.47 | 3.25 | 42.80 | 2.18 | 37.63 |
| Wald | 6:00 | 4 | 27.38 | 33.71 | 7.95 | 2.47 | 2.56 | 41.94 | 2.15 | 36.82 |
| Wald | 12:00 | 8 | 24.35 | 37.65 | 8.31 | 2.46 | 3.92 | 45.53 | 2.22 | 41.10 |
| Wald | 12:00 | 4 | 24.89 | 36.77 | 8.28 | 2.45 | 3.13 | 44.65 | 2.23 | 40.22 |
| Wald | 19:00 | 8 | 25.90 | 35.71 | 8.18 | 2.35 | 3.05 | 40.75 | 2.07 | 38.60 |
| Wald | 19:00 | 4 | 26.27 | 35.18 | 8.17 | 2.36 | 2.61 | 40.44 | 2.14 | 38.05 |
| Wald | 22:00 | 8 | 25.49 | 36.32 | 8.22 | 2.01 | 3.89 | 41.16 | 2.10 | 39.23 |
| Wald | 22:00 | 4 | 25.99 | 35.58 | 8.25 | 2.00 | 3.09 | 40.67 | 2.09 | 38.46 |
| Innenraum | 6:00 | 8 | 36.91 | 25.10 | 2.40 | 0.73 | 1.87 | 29.69 | 2.22 | 27.27 |
| Innenraum | 6:00 | 4 | 36.65 | 26.33 | 2.39 | 0.72 | 1.91 | 29.13 | 2.23 | 27.36 |
| Innenraum | 12:00 | 8 | 34.31 | 28.10 | 2.46 | 0.81 | 2.30 | 30.78 | 2.26 | 29.15 |
| Innenraum | 12:00 | 4 | 33.93 | 27.18 | 2.50 | 0.81 | 2.32 | 31.02 | 2.37 | 29.46 |
| Innenraum | 19:00 | 8 | 34.54 | 27.07 | 2.46 | 0.85 | 2.17 | 30.13 | 2.20 | 28.95 |
| Innenraum | 19:00 | 4 | 35.07 | 27.46 | 2.44 | 0.83 | 2.14 | 29.36 | 2.25 | 28.51 |
| Innenraum | 22:00 | 8 | 34.81 | 27.69 | 2.44 | 0.80 | 2.22 | 29.69 | 2.23 | 28.72 |
| Innenraum | 22:00 | 4 | 34.52 | 27.12 | 2.47 | 0.82 | 2.23 | 30.09 | 2.29 | 28.97 |

## Frische produktive Kontrolle nach dem Build

Hier wurde der Schattenwert **nicht im Test gesetzt**: Das gebaute Standardprofil musste selbst vier Strahlen liefern. Drei Fenster pro Ort, gleiche QHD/75-%-/High-/TAAU-Validierung.

| Ort | FPS | GPU ms | Frame-p95 ms |
|---|---:|---:|---:|
| Dorf | 31.69 | 29.03 | 33.62 |
| Wald | 31.59 | 29.32 | 33.95 |

Diese kurze Kontrolle ist kein gepaarter Beweis für einen Sprung von 25 auf 31 FPS: anderer Lauf-/Warmzustand und weniger Orts-/Zeitwechsel. Der belastbare Versionsvergleich steht in der längeren A/B-Tabelle.

## Bildqualität und Nachweise

20 echte VSM-Vorher-/Nachher-Paare, insgesamt 40 PNG, 2560×1440. Uhrzeit, Spielerposition, Kamera, FOV und Innenraumbasis sind pro Paar maschinell identisch geprüft. Welt/Animation während des Paares eingefroren, keine künstlichen Bilder und kein Lichtbake.

Bilder: `Saved/ProjectRefinement/MaterialShadowV3/Photos02/<Ort>H<6|12|19|22><Control|VSM4>.png`. Orte: Dorf, Wiese, Waldweg, Wald, Innenraum.

- Baumkronen/Silhouetten, Dichte, Gebäude-/Wegkanten, Bodendetails und Schattenreichweite bleiben erhalten.
- Morgen/Abend/Nacht behalten ihre Lichtstimmung. Kein offensichtlicher deutlicher Verlust in den betrachteten Normaldistanz-Aufnahmen. Geringeres stochastisches Sampling kann grundsätzlich mehr zeitliches Rauschen erzeugen. Die kurzen PIE-Bewegungsabläufe und stichprobenweise UI-Aufnahmen ersetzen keine quantitative Flimmermessung oder langfristige visuelle Nutzerabnahme. Kein neues Video und keine behauptete vollständige zeitliche Rauschfreiheit.
- Keine behauptete finale Nutzerfreigabe oder absolute Pixelidentität der Schatten.
- Zusätzliche 40 Bilder der verworfenen Materialvariante: `Photos01`, nicht als produktive Nachher-Version ausgeben.
- Rohdaten: `FinalMatrix01/Measurements.json`, `Production01/Measurements.json`, Renderer-Frames/CSV in deren eigenen UserData-Verzeichnissen.

Direkt zugängliche QHD-Vergleiche um 12:00 Uhr (lokal, nicht in Git):

| Szene | vorher: 8 Strahlen | nachher: 4 Strahlen |
|---|---|---|
| Dorf | [Original](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/DorfH12Control.png) | [Optimiert](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/DorfH12VSM4.png) |
| Wiese | [Original](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WieseH12Control.png) | [Optimiert](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WieseH12VSM4.png) |
| Waldweg | [Original](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WaldwegH12Control.png) | [Optimiert](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WaldwegH12VSM4.png) |
| Wald | [Original](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WaldH12Control.png) | [Optimiert](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/WaldH12VSM4.png) |
| Innenraum | [Original](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/InnenraumH12Control.png) | [Optimiert](../Saved/ProjectRefinement/MaterialShadowV3/Photos02/InnenraumH12VSM4.png) |


## Technische Prüfungen

- Editor-Build: **Exit 0**, 17,98 s, `Saved/ProjectRefinement/MSV3Build01/Result.json`.
- Vollständige relevante Automation: **280 bestanden, 0 mit Testwarnungen, 0 fehlgeschlagen, 0 übersprungen**.
- Strenger QA-Wrapper: **Exit 0**, 33,28 s; `Saved/ProjectRefinement/MSV3Automation01/Result.json`. Das gesamte Engine-Log ist dadurch nicht automatisch warnungsfrei.
- Zwölf Map Checks: **je 0 Fehler / 0 Warnungen**, `MapCheckResults.json`; alle zwölf vorhandenen Maps geprüft und VisualV2 wieder geladen. Kein Speichern von Maps.
- Separater Gameplaytest `NativeGameplay03`: **bestanden**. Acht Bewegungsrichtungen, L3, X/L/R/Steuerkreuz/A, Plus-Menü mit Weltzeitpause, echtes Speichern/Laden auf Platte einschließlich Position, Team, KP/AP, Repertoire und Kontrollpunkt. Kampf-Teamwechsel, Fang, Heilung, Teamreihenfolge und genau ein Begleiter zusätzlich bestanden. Fang verwendet ausdrücklich den vorhandenen geskripteten QA-Wildkampf mit einem KP, nicht einen natürlichen Begegnungs-/Balancetest.
- Zusammenhängender gewöhnlicher VisualV2-PIE-Start `PIE01`: **21 Prüfungen bestanden**, 72 Routenaktionen. C75 mit vier Strahlen, Reference100 mit acht Strahlen, Wechsel zurück, Start 09:00, Mittag75°/Debug85°, Pause/Fortsetzen, Morgendämmerung, tatsächlicher Weg ins bestehende Heilhaus, Nacht-Save/Load mit Raumkamera und unabhängigem Kontrollpunkt, Rückweg, Mitternacht, ClassicBattle-Sieg und freigegebene soziale Reservierungen.
- Echter Mapwechsel `Travel01`: VisualV2→vorhandene Dev_TestMap→VisualV2 **bestanden**. Weltuhr/individuelles Team erhalten; außerhalb acht, nach Rückkehr vier Strahlen; kein zusätzliches Tag-Nacht-System auf der anderen Map, genau ein Begleiter nach Rückkehr.
- Bewegung `Motion01` und frischer Wiederholungslauf `Motion04`: **bestanden**, einschließlich Sprint-Toggle und Menürückkehr. Zwei reguläre PIE-Start-/Endzyklen abgeschlossen; beide eigenen Prüfeditoren regulär geschlossen, keine gewaltsame Beendigung. Nach PIE wieder acht Strahlen, keine schmutzigen Assets/Maps; Szenensignatur vollständig identisch (`PostPIE.json`, `EditorCheckAfterProof.json`).
- Ein zusätzlicher Wiederholungsversuch `Motion02` nach manuellem UI-Fokuswechsel scheiterte am Sprint-Schritt; die acht vorherigen Richtungsimpulse hatten alle exakt unveränderte Positionen. Mit normalem Öffnen/Schließen des bestehenden Menüs vor dem Test und dadurch wiederhergestelltem Spielfokus bestand der frische Lauf. Kein Eingabe- oder Gameplay-Code geändert. `Motion03` startete wegen einer nicht als Python-Klasse exponierten Widget-Hilfsbibliothek im Adapter nicht; der verwendete bestehende Controller-Menüweg benötigt sie nicht.
- KI-/Tagesrhythmen unverändert: vollständige zugehörige Automation, Save/Load-Zeitereignisse, gültige gegenseitige Reservierungen, Auflösung bei Kampf und acht konfigurierte Instanzen nach Maprückkehr geprüft. Keine neue statistische Tagesrhythmus-/Langzeitabnahme durchgeführt.
- Physischer Switch-Pro-Controller: keine neue Hardwareabnahme; bestehende Belegung unverändert.

## Externe Meldungen und eigene Diagnosefehler

- Lokaler Port 8000 wird vom bereits vor Auftrag vorhandenen CrashReportClient PID 58163 gehalten. Ein lesender Registry-Commandlet prüfte sieben Versuchsassets ohne externe Referenz erfolgreich, endete aber wegen `LogHttpListener: unable to bind` mit **Exit 1**. Dies ist kein erfolgreicher warnungsfreier Commandletlauf. Prozess unangetastet.
- Native `-game`-Starts können zusätzlich Python-Toolset-Startupfehler aus Engine-Plugins melden (`ToolsetDefinition`/`PythonTestRunner` fehlen im Game-Kontext). Getrennt von Projekt-Testfehlern bewerten.
- Automation-Rohlog: **27 Warning-/Error-Zeilen** trotz Wrapper 0 und 280 erfolgreichen Tests. Darunter drei `idevice_id`-Startfehler mit jeweils zwei Zeilen (Bad CPU type/Failed to launch), ein MCP-Lizenzhinweis, ein Port-8000-Fehler, eine bestehende Projekt-Python-Namenswarnung (`bInformation`/`Information`) und eine alte Layoutversionswarnung. Diese Zeilen werden nicht unterdrückt.
- Zu diesen 27 Zeilen gehören auch 17 `LogAutomationTest: Error: Condition failed` stehen bereits beim Engine-Start unmittelbar nach `UE::UnifiedErrorTest`, vor `Initializing Engine`. Der exportierte PokeMonster-Testreport enthält keinen fehlgeschlagenen Test; diese Startmeldungen werden deshalb nicht als 17 fehlgeschlagene Projektfälle ausgegeben. Ihre vollständige interne Engine-Ursache wurde nicht behoben oder abschließend bewiesen.
- Der echte PIE-Editor meldet zusätzlich einmal einen Audio-Samplerate-Abfragefehler; der zweite Editor einen `r.MotionVectorSimulation`-Thread-Safety-Hinweis. Keine daraus belegte Rendering-Regression; upstream/offen. Die vom Nutzer vor Auftrag aktivierte Sichtbarkeitswarnung erzeugt weiterhin „Keine vorberechnete Sichtbarkeit“ im Bild. Sie wurde nicht zur kosmetischen Bereinigung abgeschaltet.
- Erste native QA-Adapterversuche scheiterten an unbeantworteten Lernangeboten beziehungsweise einem veränderbaren GUID-Struct-Vergleich. Korrektur nur im Diagnoseadapter; die anschließend vollständige native Wiederholung bestand.
- Ein eigener früher temporärer Material-Asset-Löschversuch löste ein behandeltes ObjectTools-Unload-Ensure aus. Die Originalszene blieb unverändert; der Editor blieb tastaturbedienbar und wurde nach konkreter Freigabe regulär geschlossen. Danach nur echte transiente UObject-Prüfmaterialien, keine ForceDelete-Operation.
- Beim UI-Zugriff auf einen bereits endenden separaten Spielprozess entstand ein leerer Projektbrowser ohne Projekt. Regulär geschlossen, keine Projektkopie/Map und kein Force Quit.

## Grenzen und Empfehlungen

1. Vier VSM-Strahlen sind eine kleine, belegte Optimierung; kein 30-/60-FPS-Versprechen.
2. Base Pass/komplexe Wegberechnung und Lumen Screen Probe Gather bleiben große Kostenblöcke. Keine ungeprüften Materialvereinfachungen oder GI-Abschaltungen übernehmen.
3. Ein späterer separater Versuch kann statische Wegfarb-/Maskenanteile pro Mesh oder mit exakter UV-/Nahtkontrolle vorberechnen. Die hier getestete dynamische Segmentindexierung rechtfertigt keine produktive Übernahme. Erwartete Einsparungen sind dafür noch nicht gemessen.
4. Quantitative Overdraw-/Metal-ISA- und GPU-Taktanalysen bleiben begrenzt; keine geschätzten Einzelkosten als Messungen ausgegeben.
5. Keine Änderungen an Westland/Biom, Modellen, Animationen, Controller, Gameplay, Save-Schema, Weltuhr oder dynamischem Licht.

## Git und Integrität

SHA-256-Endkontrolle gegen 6302 Ausgangsdateien: **alle 33 ursprünglich unversionierten geschützten Dateien und alle 335 vorhandenen .sav-Dateien unverändert**. Sämtliche Content-/Art-Originale und Maps unverändert, ebenso die bestehende Nutzeränderung an DefaultEngine.ini. Beide Vollbackup-Verweise weiterhin `03492bd96b4dba44692f675c19d5f11abfa86b4b`.

Die gesamte Arbeitsumgebung ist nicht bitidentisch: Neben den zwei beabsichtigten versionierten Änderungen änderte sich die erzeugte `Saved/Config/MacEditor/EditorPerProjectUserSettings.ini` während der Editorsitzungen. Die gezielt geänderten Hintergrund-Throttle-/Evolution-Auto-Voreinstellungen wurden vor regulärem Schließen restauriert; mangels Originalinhalt wird keine exakte Rücksetzung aller Editor-Historien behauptet. Sieben ursprünglich erfasste CrashReportClient-Konfigurationsdateien fehlen bei der abschließenden Hashprüfung; es gab keinen Löschbefehl dafür. Automatische Engine-/CrashReporter-Verwaltung ist eine Möglichkeit, die Ursache ist nicht bewiesen. Die genauen Pfade stehen in `Saved/ProjectRefinement/MaterialShadowV3/ProtectionFinal.json`.

Gezielt gesichert werden ausschließlich der fünfzeilige Rendering-Zusatz, die vorhandene Entscheidungsliste, dieser Bericht und drei reproduzierbare Prüfskripte mit README. Screenshot-/CSV-/Testsave-Dateien bleiben lokal in Saved und werden nicht hochgeladen. Keine neuen LFS-Assets erforderlich.

- Implementierungscommit: `b81eb11c39dcf8aa3a3632b3822d40b8a9f1e911` – `Reduce VisualV2 directional shadow sampling after measured validation`.
- Dieser Prüfbericht wird anschließend separat dokumentiert; seinen eindeutigen Commit liefert `git log -1 --format=%H -- Docs/VISUALV2_MATERIAL_SCHATTEN_V3.md`.
- Live-Remote-/LFS-Endprüfung: [lokales maschinelles Git-Protokoll](../Saved/ProjectRefinement/MaterialShadowV3/GitFinal.json). Enthält lokale/Remote-Hashes, ausstehende LFS-Objekte und den tatsächlichen Endstatus, ohne Nutzeränderungen zu übernehmen.
- Keine Historienänderung, kein Force Push, keine Budget-/Abrechnungsänderung und kein LFS-Prune.
