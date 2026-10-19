# VisualV2 World Art Quality V1 – Heilhaus-Vorplatz und Wegsäume

Stand: 19.10.2026. **Erster begrenzter Art-Stand technisch geprüft und zur visuellen Abnahme vorgelegt. Keine automatische Freigabe für die restliche Welt.**

## Ergebnis und Umfang

Bearbeitet wurde ausschließlich `/Game/Maps/Dev_TestMap_VisualV2`, gespeichert unter `Content/Maps/Dev_TestMap_VisualV2.umap`. Keine neue Map. Der zusammenhängende Bereich liegt ungefähr bei X −4620 bis −3560 und Y −720 bis 1190 cm, also rund 10,6 × 19,1 m um Heilhauszugang, Vorplatz und unmittelbare Wegsäume. Grundlegende Performanceoptimierungen wurden nicht fortgesetzt.

Die Ausgangsansicht zeigte einen gleichmäßigen gemalten Grasgrund, wenig niedrigen Bewuchs, eine gleichförmige Wegkante und einen Vorplatz mit übernommenem Materialzentrum aus einer anderen Szene. Die vorhandene Hausarchitektur, Fensterkästen und Kräutertöpfe waren bereits ausreichend bestückt. Weitere dekorative Gebäudeteile wurden deshalb nicht ergänzt.

- Gras erhält nur lokal ruhig verteilte Farb-/Helligkeitsvariation im Material, ohne Lichtwerte zu verändern.
- Vorhandene Erde bleibt die Bildquelle; lokal variierte, etwas entsättigte Erdnuancen und begrenzte unregelmäßige Wegsäume lösen die Gleichförmigkeit auf.
- Der Vorplatz erhält eine organische, mit dem Zugangsweg verbundene Erdfläche. Keine neue Collision oder Änderung der Bodenhöhe.
- 175 kleine Gras-, Kräuter-, Blüten-, Farn- und Steininstanzen bilden ungleichmäßige Pflanzentaschen statt eines Rasters. Blüten bleiben Akzente; ein großzügiger Korridor und der Türvorbereich bleiben frei.
- Kleine flache Steincluster geben sichtbares Bodenrelief. Das eigentliche begehbare Gelände wird nicht ummodelliert; keine künstlichen Stolperkanten.

## Nachgewiesene Überlagerung und sichtbare Nacharbeit

Die erste Nachher-Prüfung zeigte einen grünen Bogen zwischen Weg und neuer Vorplatzfläche. Zunächst wurde die neue Vorplatzvariante auf eine nur Erde zeichnende maskierte Umrandung umgestellt und die Wegkantenauslenkung beruhigt. Eine zusätzliche Verbindung des lokalen Vorplatzmusters mit dem vorhandenen Weg schloss eine kleine Restlücke.

Die anschließende Bounds-/Materialprüfung fand die eigentliche darüberliegende Altfläche: `V2_House_HH_Q2_OrganicApproach` liegt bei **Z=1,4 cm**, über der Vorplatzoberfläche bei **Z=1 cm**. Ihr altes opakes `M_WL_NG_PathBlend` malte Gras an die Ränder und deckte die neue Erdfläche teilweise ab. Eine eigene lokale Variante `M_WAQ1_LegacyApproach` zeichnet dort Erde mit maskierter Kante; außerhalb des begrenzten Einflussbereichs bleibt die ursprüngliche Farb-/Deckkraftfunktion erhalten. Originalmesh, Originalmaterial und Actor-Transformation bleiben unverändert. Die finalen Aufnahmen zeigen die durchgehende Erdfläche ohne diesen grünen Streifen. Frühere Iterationen bleiben als lokale Nachweise erhalten und werden nicht als Endstand ausgegeben.

## Verwendete Assets und technische Organisation

**Keine neuen Meshes, Blenderquellen, Texturen, Gebäude oder Plugins.** Es werden vorhandene NaturalGroundV1-, Westland- und Healing-House-Materialfamilien verwendet. Zwölf neue private Material-/Instance-Assets verhindern Änderungen an gemeinsamen Originalen. Vier sind lokal begrenzte Boden-/Wegvarianten; zwei sind instancingfähige Kopien vorhandener Materialeltern, sechs übernehmen die bisherigen Blatt-/Blütenparameter und Texturen. Bei der Vorbereitung hatten die ursprünglichen WLA-Eltern keine persistente InstancedStaticMeshes-Nutzung; diese wurde nur an den eigenen Elternkopien aktiviert. Keine Rückkehr zum nativen grauen Ersatzmaterial durch ungeprüfte HISM-Nutzung.

| Neue HISM-Gruppe | Instanzen | Dreiecke je Mesh LOD0 / LOD1 / LOD2 | Materialslots |
|---|---:|---|---:|
| WAQ1_GrassSmall | 54 | 45 | 3 |
| WAQ1_GrassMedium | 36 | 90 | 3 |
| WAQ1_MeadowHerbs | 28 | 100 | 4 |
| WAQ1_Flowers | 18 | 2160 / 1188 / 540 | 5 |
| WAQ1_Fern | 12 | 8030 / 4818 / 2409 | 3 |
| WAQ1_Pebbles | 27 | 80 | 1 |

Alle sechs Gruppen: **NoCollision, kein Schattenwurf**, kein Distance-Field-/dynamischer Indirect-Lighting-Beitrag, Culling 4500–6500 cm. Die vorhandenen LODs wurden unverändert übernommen. Rechnerische Obergrenze bei sämtlichen zusätzlichen Instanzen auf LOD0: **145.870 Dreiecke**. Dies ist kein gemessener sichtbarer GPU-Dreieckswert; tatsächlich können bestehende LODs greifen. Materialslots sind keine gemessenen Draw Calls.

Neue Assets:
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_FlowerBlue_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_FlowerCream_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_LeafDark_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_LeafFern_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_LeafLight_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/MI_WLA_Leaf_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_HealingForecourt.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_HealingMeadow.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_HealingPath.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_LegacyApproach.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WLA_PaintedLeaf_Instanced.uasset`
- `Content/Environment/VisualV2WorldArtV1/Materials/M_WLA_Painted_Instanced.uasset`

Maßgebliche Autoren-/Wiederherstellungsdaten: `Art/World/VisualV2WorldArtV1/HealingHouseDressing.json`, inklusive aller Positionen, Größen, ursprünglichen und neuen Materialzuweisungen. Werkzeugfolge und Hinweise: `Tools/VisualV2WorldArtQualityV1/README.md`. Die Werkzeuge sind optional für spätere Bearbeitung, keine neue Laufzeitarchitektur und keine Pflicht-Abhängigkeit zu Kontrollmedien.

## Erhaltene Inhalte

Der vollständige Szenenvergleich der erfassten **1348 → 1354 Actors** bestätigt: genau sechs zusätzliche Darstellungsactors und **fünf bestehende Actors mit ausschließlich geänderten Materialzuweisungen** (`V2_Ground`, `V2_House_Forecourt`, `V2_Path_VillageLoop`, `V2_Path_NorthLoop`, `V2_House_HH_Q2_OrganicApproach`). Sämtliche übrigen erfassten Actor-/Komponenten-/Instanzwerte und vollständigen Postprocess-Settings sind identisch.

Keine Änderung an Lichtquellen, deren Positionen/Intensitäten/Farben, Originalschatten, Lumen, Bloom, Belichtung, TAA, Kamera B, Spielergröße, Bewegung, Sprint, NPC-Identitäten oder Gameplay. Keine Materialänderung an den bisherigen Baumkronen oder der Sichtfreistellung. Bestehende Gebäude und Pflanzen wurden nicht verschoben oder entfernt. Neue kleine Dekoration wirft keine zusätzlichen Schatten. Die Kamera bleibt 2850 cm / −50° / −45° / FOV35°. Der tatsächliche gerenderte View bleibt TAA/Methode2 bei globalem AA-CVar4.

182 vorab erfasste Map-/Source-/Config-Dateien wurden per SHA-256 verglichen: nur die beauftragte zentrale Map ist verändert. Alle anderen Maps, Source- und Config-Dateien bleiben bytegleich, einschließlich des vorbestehenden unversionierten EnvironmentQualityV1-Kartenstands. Original-Arbeitsbaum und Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleiben unverändert. Der Ausgangsstand der zentralen Map liegt zusätzlich außerhalb des Projekts unter `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Dev_TestMap_VisualV2_Before.umap`, SHA-256 `441e9dc5592db4b7e551e861099dd3e82bbb146c4df5be90f498e0ad62256140`.

## Echte Vergleichsaufnahmen

Drei identische feste Spielkamerapositionen, Medium, 100 %, tatsächliche Ausgabe **2560×1440**. Pro Aufnahme wurde die echte Spielkamera nach dem Setzen der Vergleichsposition eingeschwungen; Winkel/FOV/Auflösung und Positionen sind protokolliert. Diese fotografischen Positionierungen sind **nicht** Teil des separat durchgeführten Fußlaufs. Kopien der sechs Original-PNGs wurden per SHA-256 geprüft. Beschriftete Paare sind nur verkleinert/nebeneinander angeordnet, nicht retuschiert und nicht synthetisch erzeugt.

- **Heilhaus**: [Vorher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Heilhaus_Vorher.png), [Nachher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Heilhaus_Nachher.png), [beschrifteter Vergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Heilhaus_Vergleich.png); Kameradifferenz 0.00000000 cm.
- **Vorplatz**: [Vorher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Vorplatz_Vorher.png), [Nachher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Vorplatz_Nachher.png), [beschrifteter Vergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Vorplatz_Vergleich.png); Kameradifferenz 0.00000000 cm.
- **Wegsaum**: [Vorher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Wegsaum_Vorher.png), [Nachher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Wegsaum_Nachher.png), [beschrifteter Vergleich](/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/Vergleich/Wegsaum_Vergleich.png); Kameradifferenz 0.00000000 cm.

Metadaten: `/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19/MatchedPhotoProof.json`. Rohbilder und Zwischenstände bleiben lokal unter `Saved/VisualV2WorldArtQualityV1/Photos`; keine Kontrollmedien werden nach GitHub übertragen. Der normale Fußlauf erzeugte weitere echte Bilder sowie eine 290-Frame-Tür-/Innenraumsequenz unter `Saved/VisualV2TAAIntegrationV1/Recordings/WorldArtV1_Door_ArtFinalFoot`. Keine Behauptung einer gesonderten Videoabnahme.

## Grundlegende Performancekontrolle – keine Optimierungsanalyse

Eine feste Heilhausposition (Player ungefähr −4100/450; Kamera −5395,3805 / 1745,3805 / 2268,3767 cm), Embedded PIE, Medium. Je Ausgabe drei Wiederholungen mit fünf Sekunden Warm-up und fünf Sekunden Messung. 720p/75 %: verifizierte Ausgabe/Target/View 1280×720, interne Treibergröße 960×540. QHD/100 %: sämtliche Größen 2560×1440. Interne Größen stammen vom unabhängigen vorhandenen Renderer-Probe; Screenshots bestätigen die echte Ausgabe. VSync-CVar0, MaxFPS0, dynamische Auflösung aus, keine absichtliche Qualitätsabsenkung. Eine nahe 60-FPS-Plattformbegrenzung der kleinen Ausgabe kann trotzdem nicht ausgeschlossen werden.

Aggregiert wird der Median der drei Laufmediane; P95 ist als Spannweite der drei Läufe angegeben. Zeiten in ms.

| Stand | Ausgabe / SP | FPS | Frame | P95 je Lauf | GPU | Game Thread |
|---|---|---:|---:|---:|---:|---:|
| Before | 1280×720 / 75 % | 60.01 | 16.66 | 16.91–16.92 | 14.84 | 4.54 |
| Before | 2560×1440 / 100 % | 29.71 | 33.66 | 35.03–35.35 | 32.76 | 5.70 |
| AfterFinal | 1280×720 / 75 % | 59.01 | 16.95 | 19.13–20.19 | 15.67 | 7.13 |
| AfterFinal | 2560×1440 / 100 % | 26.89 | 37.18 | 41.60–58.08 | 36.12 | 5.68 |

**Kein Performancegewinn.** In dieser sequenziellen Kurzreihe steigt die QHD-Framezeit von 33,66 auf 37,18 ms, die GPU-Zeit von 32,76 auf 36,12 ms; 720p liegt bei ungefähr 59 statt 60 FPS. Ein QHD-Lauf enthält einen deutlicheren Ausreißer. Thermische und zeitliche Drift wurden hier nicht in einem langen interleavten Versuch isoliert; deshalb ist die gesamte Differenz kein exakt bewiesener kausaler Preis der Dekoration. Der Bildqualitätsgewinn hat gemessene Mehrkosten als offene Abnahmefrage. RenderThreadTime war nahe null und wird nicht als verlässliche CPU-Kostenmessung ausgegeben. Keine neuen Overdraw-/Schattenpass- oder Draw-Call-Behauptungen.

Daten: `Saved/VisualV2WorldArtQualityV1/BasicPerformanceSummary.json`, `Measurements.json` und die Original-Frames-/Segments-/CSV-Dateien mit Präfix `VGB1_WorldArt_`. Die Zwischenmessung `After` gehört zum inzwischen ersetzten ersten Materialstand; **nur `AfterFinal` ist der endgültige Vergleich**. Entsprechend dem ausdrücklichen Pause-Auftrag kein vollständiges High-/Standalone-/Dauertestprofil und keine weitere Performanceoptimierung. Keine 60-FPS-Garantie.

## Technische und Gameplay-Abnahme

- **Mac Development Editor Build erfolgreich**, Exit0; kein Gameplay-/Rendering-C++ geändert. Log `Saved/VisualV2WorldArtQualityV1/Build/Build.log`.
- **49/49 Projekt-Automationstests erfolgreich**, 0 Warnungstests, 0 Fehler, 0 nicht ausgeführte Tests. Originalbericht `Saved/VisualV2WorldArtQualityV1/Automation/Report/index.json`.
- **Frische Map-Ladeprüfung und Map Check 0 Fehler / 0 Warnungen**, keine schmutzigen Map-/Contentpakete. Finale Ergebnisse `Saved/VisualV2WorldArtQualityV1/MapChecks_Verified/`.
- Der erste exakte Ladevergleich war wegen der Komponenten-Aufzählungsreihenfolge der sechs neuen Actors formal fehlgeschlagen. Eine Zuordnung nach eindeutigen Komponentennamen ergibt **vollständige exakte Gleichheit**, einschließlich aller 175 Instanztransformationen; keine numerische Toleranz und keine ausgelassenen Inhaltsfelder. Ein nachfolgender Prüfprogrammaufruf suchte seine JSON-Datei im falschen Ergebnisordner. Beide Werkzeugbefunde sind behoben und ihre Logs erhalten; der finale frische Lauf ist bestanden. Keine Assetfehler wurden dafür kaschiert.
- **Echter Enhanced-Input-PIE-Fußlauf bestanden: 102 Schritte, 276.01 m**, ohne Testteleports. Acht Richtungen, Anhalten, Sprint bis 315.00 cm/s, Kamera, Kollisions-/Begehbarkeitskontrolle, Wanderer-Dialog/Queststart/-abschluss, Wildkampf und Fang, Liora-Trainerkampf, Brücke/Archivziel, Inventarmenü, Save/Load, Heilhauszugang, HP/PP-Heilung, Checkpoint/Save, Aus-/Wiedereintritt einschließlich Diagonalen, Wald/Kronenfreistellung und NPC-Sprite-Fallback bestanden. Keine neuen Blocker auf der Route.
- Der ursprüngliche Dev-Slot war nicht vorhanden. Die Testdatei wurde als Nachweis gesichert; die ursprüngliche Abwesenheit ist wiederhergestellt. `SaveRestored.json` bestätigt dies.

Bekannte allgemeine Engine-Startmeldungen (unter anderem macOS-`idevice_id`-Architektur-/Audio-/MCP-Lizenzhinweise und Engine-Selbsttestausgaben) sind von Map-/Projektfehlern getrennt. Keine neuen Material- oder Shaderkompilierfehler im finalen Prüflauf. Keine Standalone-/Shipping-Abnahme dieses begrenzten Art-Auftrags behauptet.

## Selbstkritische visuelle Bewertung und offene Punkte

Erreicht: Der Heilhauszugang wirkt mit den niedrigen Pflanzentaschen zusammenhängender; die Erde besitzt ruhigere Nuancen, die Säume sind weniger gleichförmig und kleine Steine/Blüten gliedern die Ränder. Die endgültige Vorplatz-/Wegverbindung hat keinen grünen Überlagerungsstreifen mehr. Figuren und Eingang bleiben erkennbar; der freie Bewegungsraum ist erhalten.

Weiterhin sichtbar: Die vorhandenen großen Topfpflanzen besitzen vergleichsweise einfache, flächige Blattformen. Gras-/Erdtexturen können in ruhigen größeren Flächen weiterhin repetitiv erscheinen; der Boden bleibt geometrisch weitgehend flach. Das bestehende Hausmodell, die gelblich-warme Beleuchtung und harte Originalschatten wurden bewusst nicht umgestaltet. Ein vorhandener brauner Testwürfel neben dem Haus wurde nicht entfernt oder umgedeutet. Feines temporales Blatt-/Dither-Flimmern ist durch diesen Auftrag nicht gelöst. Keine neue Wind- oder Kronenanimation. Die Pflanzeninseln sind aus der echten Spielkamera geprüft, aber ihre künstlerische Endabnahme liegt bei Harry.

**Empfehlung:** Diesen begrenzten Bereich visuell prüfen, bevor die Gestaltung auf weitere Wege oder die restliche Karte ausgeweitet wird. Keine automatische Art-Freigabe aus bestandenen Tests. QHD-Mehrkosten und die einfachen bestehenden Topfpflanzen bei der nächsten Priorisierung berücksichtigen; keine versteckte Grafikabsenkung.

## Git-Sicherung und verbleibender Zustand

Ausgangsbranch `codex/slim-backup-v5`, Ausgangs-HEAD und direkt überprüftes origin/main: `d521351e117bd574c3d2930835c6b55db3c74dd0`. Bestehende unversionierte Dateien bleiben ausgeschlossen: `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`, `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.

Die genehmigte Sicherung umfasst ausschließlich private Art-Assets, zentrale Map, Wiederherstellungsdaten, erfolgreiche Werkzeuge und Dokumentation. Keine PNGs, Videos, Roh-CSV, Saved-/Cachedateien oder alte Vollbackup-Historie. `git diff --check` vor Sicherung ohne Befund. Der Art-/Werkzeug-Commit `d7471b4beae5e1abdd9a360c98e248ca41f52ddc` (43 Pfade) wurde regulär auf `origin/main` gepusht und per direktem Remote-Hash bestätigt. 13 LFS-Objekte mit insgesamt **3.530.592 Bytes** wurden übertragen; anschließender LFS-Dry-run ohne Restupload. Unabhängiger Remote-Download aller 13 Objekte bestätigt Größe und SHA-256. Keine Quota-/Kostenfehler; ein aktueller kontoübergreifender Abrechnungsverbrauch ist daraus nicht ablesbar. Normale Git-Dateiinhalte im geprüften Index: 307.111 Bytes, kein großer normaler Blob. Der Bericht wird separat als Dokumentations-Commit gesichert; dessen endgültiger Hash steht im äußeren `GIT_ABSCHLUSS.json` und in der Antwort. Vollbackup `03492bd` ist kein Vorfahr der neuen Remote-Historie. Keine weiteren Flächen werden bearbeitet, bevor Harry den Bereich geprüft hat.
