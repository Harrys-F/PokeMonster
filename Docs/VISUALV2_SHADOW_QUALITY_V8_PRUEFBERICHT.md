# VisualV2 Shadow Quality V8 – Prüfbericht

19.10.2026. **A bleibt aktiv. B und C sind echte, reversible Vergleichsversuche; keine Schattenvariante wurde in die gespeicherte Karte übernommen.** B ist der vorsichtigere visuelle Kandidat, aber noch keine vorbehaltlos übernehmbare Lösung.

## 1. Ausgangszustand und Sicherheit

Worktree `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`, Ausgangs-HEAD/Remote `16f19044489c17833d8d494c2e317a094002fa87`. AGENTS sowie Grafikstil, Technik, Spielidee, Spielregeln, Entscheidungen und V7-Befund berücksichtigt. Zu Beginn kein offener Unreal-Editor; keine fremden ungespeicherten Pakete verworfen.

Einzige untersuchte Karte: `/Game/Maps/Dev_TestMap_VisualV2`. **Keine neue Karte, kein Speichern oder Überschreiben einer bestehenden Map.** Alle 17 Map-Dateien sind nach Abschluss bytegenau unverändert. Die vollständige Editor-Szene mit 1.397 Akteuren stimmt mit dem Ausgangszustand überein; keine schmutzigen Map- oder Content-Pakete verbleiben.

Originalkarten-SHA-256: `e06d3edcbb6bc6c8844f1734f22650f55454e8aa87507c8ee0422e37bafc6713`. Zusätzliche Kopie außerhalb des Projekts: `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/VisualV2_Original.umap`. Lokales `main` und Archiv-Ref für das Vollbackup bleiben bei `03492bd96b4dba44692f675c19d5f11abfa86b4b`; nicht Teil der schlanken Remote-Historie.

Vorhandene fremde Dateien bleiben unangetastet und uncommittet:

```
Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
Tools/VisualV2EnvironmentQualityV1/
Tools/VisualV2QualityV2/__pycache__/
```

## 2. Technische Untersuchung

Das vorhandene Setup verwendet Virtual Shadow Maps. Der in V7 geprüfte Directional-Light-Regler `ShadowAmount` erzielte dort keine geeignete Wirkung; V8 setzt diese wirkungslose Methode nicht als B/C fort. Der lokale Engine-Code zeigt den echten VSM-Schattenfaktor innerhalb der Renderer-Projektion (`VirtualShadowMapProjection.usf` / `VirtualShadowMapProjectionCommon.ush`). Die üblichen Postprocess-Materialeingänge liefern Scene Color, Albedo, Normale, Tiefe usw., aber keinen frei nutzbaren getrennten VSM-Direktschattenfaktor. Die untersuchten öffentlichen View-Extension-Hooks erlauben hier keinen einfachen unveränderten Zugriff auf diesen internen Projektionsschritt.

An der installierten Engine wurde nichts verändert. Auch Lichtstärke, Farben, Richtung, Schattenbias, Belichtung, Kamera, TAA, Gameplay und Vegetation wurden nicht geändert. Erfasste Directional-/Point-/Spot-/Skylight-Werte einschließlich Schattenparametern sowie die gespeicherten Postprocess-Einstellungen sind unverändert. Für alle Varianten gelten dieselben Medium-Einstellungen; keine Qualitäts- oder Lumen-Umschaltung zwischen A/B/C. Keine persistente Projekt-Renderkonfiguration geändert.

**Getestete Alternative:** Ein separates Material nach dem Tonemapping schätzt dunkle Bodenbeschattung anhand des Verhältnisses von Bildfarbe zu diffuser Materialfarbe. Normale und Höhe begrenzen den Effekt auf bodennahe Flächen. Eine Ortsmaske schließt den ausgelagerten Heilhaus-Innenraum aus. Das Material wird nur als dynamische Instanz an die temporäre Spielwelt-Kopie des bestehenden Außen-Postprocess-Volumens angehängt. Der vorhandene TAA-Blendable bleibt erhalten. A umgeht den Versuch vollständig. Die gespeicherte Materialquelle besitzt neutralen Gain 0 und ist in keiner Map verbunden.

Eine anfängliche RGBA-Anschlusskorrektur am neuen Material wurde vor der finalen Prüfung behoben. AO wurde als Kontaktmerkmal untersucht, erwies sich aber nicht als verlässliche ausschließlich kleinräumige Abgrenzung und ist nicht Bestandteil der finalen Aufhellungsmaske. Verwerfliche Kalibrierungsstände bleiben nur in lokalen Nachweisen. Frische finale native Prüfung: keine Shader-Kompilierfehler oder Default-Material-Fallbacks.

## 3. A/B/C und Kontaktschutz

| Variante | Umsetzung | Bewertung |
|---|---|---|
| A | unverändertes Original, Zusatzmaterial umgangen | weiterhin aktiver Standard |
| B | moderater, bildbasiert kalibrierter Boden-Lift, Ziel ungefähr 25 % heller | zurückhaltender visueller Kandidat; weitere Integration/Abnahme erforderlich |
| C | stärkere gleiche Methode, Ziel ungefähr 50 % heller | Bodenstruktur deutlicher, aber Masken-/Materialgrenzen stärker sichtbar; derzeit nicht zur Übernahme empfohlen |

Die tatsächlichen Testparameter stehen in `Art/World/VisualV2ShadowQualityV8/Variants.json`: Gain B 0,45 / C 0,90, Klassifikationsschwellen 0,40 / 1,20. **Diese Werte sind keine VSM-Deckungsgrade und nicht die Prozentangaben.** Sie wurden anhand gerenderter Bildausschnitte kalibriert. Die Masken gelten für alle Schattenwerfer gemeinsam; Baum-, Gebäude- und Figurenschatten werden nicht über Änderungen ihrer Assets vereinfacht oder abgeschaltet.

Kontaktbereiche: Player-Fußpunkt mit 35-cm-Kern und weichem 24-cm-Auslauf; bis zu 15 weitere nächstgelegene NPC-/Baum-/Gegenstandskontakte sowie schmale Sockelbereiche an den zwei vorhandenen Gebäuden. Sichtbare Baum-/Instanzpositionen und tatsächliche Gegenstandsbounds werden benutzt. Das schützt lokale Bodennähe, während breitere Schattenbereiche angehoben werden. Es ist kein universeller Ersatz für die korrekte Kontakttrennung beliebiger künftiger Objekte.

## 4. Echte Bildvergleiche und Abgleich

**42 finale Unreal-Aufnahmen:** je A/B/C an sieben Positionen, jeweils eingebettetes PIE und nativer `-game`-Standalone-Betrieb. Kein gecookter Shipping-Build. Ansichten: Wald, Wiese, Heilhaus, Gebäudeschatten, Spielfigur, Flussufer und separater Innenraum.

Alle Original-PNGs und tatsächlichen Viewports: **2560 × 1440**, Medium, primärer/sekundärer Screen Percentage 100, Dynamic Resolution 0. Gleiche Kamerapositionen, Rotation, FOV und Spielerpositionen innerhalb 0,02 cm/Grad. Bestehende Außenkamera 2850 cm / −50° / −45° / FOV 35°; Innenraum nutzt seine unveränderte eigene Kamera. Fotopositionierung ist von dem tatsächlich gelaufenen Gameplaytest getrennt. Für die Bilder ist die Player-Pose eingefroren; dies gilt nicht für den Fußlauf. Wasser, Feuer, NPCs und temporale Verarbeitung können kleine Restunterschiede verursachen.

| Ausgewählter Kontrollausschnitt | B gegenüber A | C gegenüber A |
|---|---:|---:|
| Wald-Boden, PIE | +25,12 % | +50,80 % |
| derselbe Wald-Boden, Standalone | +25,40 % | +51,12 % |
| sonniger Weg, PIE | +0,005 % | +0,004 % |
| Fußkontakt im Wald, PIE | −0,054 % | +0,089 % |
| Innenraumboden, PIE | +0,023 % | +0,056 % |

Dies sind relative Mittelwerte gewichteter **Bild-Codewerte** in offen dokumentierten Pixelrechtecken, keine physikalischen Schattenfaktoren und keine exakten psychophysischen Wahrnehmungsprozente. Das Ziel wird im kalibrierten Wald-Boden erreicht, **nicht als einheitliche Prozentwirkung auf jede Schattenart zugesichert**. Die Innenraumabweichung ist sehr klein; der Shader schließt diesen Raum ausdrücklich aus. Statische Kontaktbereiche bleiben dort kräftiger als die angehobenen umgebenden Bodenschatten.

Lokale Tafeln (links A, Mitte B, rechts C):

- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Wald_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Wiese_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Heilhaus_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Gebaeudeschatten_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Spielfigur_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Flussufer_ABC.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/PIE_Innenraum_ABC.jpg`
- entsprechende `Standalone_*`-Tafeln sowie Details `PIE_BodenUndFigur_Detail_ABC.jpg`, `PIE_Figurenkontakt_Detail_ABC.jpg` und `PIE_FassadeUndBoden_Detail_ABC.jpg`.

Originale mit SHA-256 und vollständiger Zuordnung: `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/Comparisons/Manifest.json`; Zahlen und Pixelrechtecke: `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/ImageMeasurements.json`. Unveränderte Originalbilder unter `Saved/VisualV2ShadowQualityV8/Photos/PIE_A` bis `Standalone_C`. Tafeln sind nur beschriftete, gleich skalierte bzw. gleich zugeschnittene echte Bilder – keine Retusche oder synthetische Aufhellung von Vergleichsbildern.

## 5. Visuelle Grenzen und technischer Zielkonflikt

Der Boden unter großen Kronen wird in B/C lesbarer; die Sonne bleibt im Kontrollausschnitt nahezu unverändert. Die RGB-Anhebung bewahrt weitgehend die lokale Farbrichtung. Original-VSM-Schattenform, Blattsilhouetten und geometrische Penumbra werden nicht ersetzt oder absichtlich verbreitert. Änderungen des wahrgenommenen Kantenkontrasts entstehen dennoch durch die Klassifikation.

**Keine reine Schattenoperation:** Geringe indirekte Beleuchtung, Oberflächenfarbe und echter Schlagschatten sind im fertigen Bild nicht eindeutig trennbar. Die Albedo-Normalisierung reduziert Verwechslungen, beseitigt sie aber nicht. C hebt stellenweise Boden-/Materialstruktur und die Grenzen der Erkennung deutlicher hervor. Vertikale Fassadenbeschattung und Eigenbeschattung von Haut/Kleidung sind bewusst ausgeschlossen; deren vollständige Aufhellung wäre mit diesem begrenzten Verfahren nicht sauber abgesichert. Eine durchgehend gleiche Wirkung auf Baum-, Gebäude- und Figurenschatten kann deshalb nicht bestätigt werden.

Der Innenraum bleibt durch die Ortsmaske geschützt. Das ist eine gezielte Lösung für diese konkrete bestehende Map, keine allgemeine Raumklassifikation. Bodenniveau-/Normalenmasken sind ebenfalls keine universelle Lösung für spätere hohe Terrassen oder beliebiges Gelände.

**Bewegter Kontakt:** 24 zeitlich geordnete QHD-Bilder während des C-Fußlaufs, mit gleichzeitig ausgelesenen Pawn-/Materialkontakt-Koordinaten. Median der Positionsdifferenz 14,34 cm, Maximum 41,76 cm; bei den meisten Aufnahmen wenige bis etwa 17 cm. Das ist ein Parameter-Snapshot am Python-/Slate-Testcallback, keine render-synchrone GPU-Kontaktmessung. Daraus wird kein fehlerfreier bewegter Kontakt abgeleitet. Die Testmaske kann zeitlich versetzt sein; vor Übernahme wäre eine zum finalen Renderframe synchronisierte Aktualisierung nötig. Kontakt-/Halo-Wirkung muss anschließend erneut in Bewegung abgenommen werden. Keine erfolgreiche Videoabnahme behauptet; bereitgestellt sind Bildfolgen.

**Empfehlung:** A als Standard behalten. B kann anhand der Bilder visuell weiterdiskutiert werden, aber noch keine technische Gesamtfreigabe. C derzeit nicht übernehmen. Für eine streng vom übrigen Beleuchtungsbild getrennte, allgemeine Abschwächung wäre ein kontrollierter Eingriff am echten VSM-/Lichtattenuationsfaktor samt separatem Kontaktpfad erforderlich. Das wäre ein eigener Renderer-Auftrag. Eine Aufhellung von Skylight, Lichtintensität oder Belichtung wäre eine andere Beleuchtungsentscheidung und wurde nicht durchgeführt.

## 6. Tatsächliche Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | bestanden, Exit 0 |
| vollständige Projekt-Automation | **49/49**, 0 Warnungen/Fehler/nicht ausgeführt |
| frischer Map Check | **0 Fehler, 0 Warnungen**, ursprüngliche gespeicherte Szene exakt |
| kompletter eingebetteter PIE-Fußlauf mit C | **102 Schritte**, 291,53 m gemessene Strecke, bestanden |
| Gameplay | Dialog/Quest, Liora, Wildkampf/Fang, Archiv, Menü, Heilhaus, Schwellen, Heilung/Checkpoint, Save/Load, acht Richtungen, Sprint, Kollision, Kronenfreistellung und NPC-Sprite-Fallback geprüft |
| Spielstandschutz | ursprüngliche Abwesenheit des Dev-Slots wiederhergestellt; keine Nutzerdaten ersetzt |
| nativer A/B/C-Spielbetrieb | Exit 0, alle 21 Aufnahmen vorhanden; keine neuen Material-Shaderfehler |
| alle 17 Maps / gesamte Editor-Szene / Lichtwerte | unverändert |
| FPS-/GPU-Benchmark | nicht durchgeführt |

Der Fußlauf benutzt tatsächliche Enhanced-Input-Eingaben und bestehende Physik; keine Test-Teleports. Die bestehenden Weltübergänge und Save/Load-Funktionen sind Teil des Tests. Normales Gehen 210 cm/s und Sprint 315 cm/s bleiben bestehen. Der Weg wird durch Testtiming abgetastet; die gemessene Strecke ist kein Performancevergleich.

Die nativen Engine-Logs enthalten weiterhin die aus V7 bekannten 58 experimentellen Python-Toolset-Fehlerzeilen mit denselben 47 normalisierten Fingerprints, u. a. ToolsetDefinition/PythonTestRunner. Keine neuen Fingerprints; diese Engine-Probleme wurden nicht behoben oder unterdrückt. Projekt-Automation und Map Check sind gesonderte Ergebnisse. Kein Shipping-Cook, kein High-/75-%-Matrixvergleich und keine vollständige universelle Kontaktprüfung durchgeführt.

## 7. Gespeicherte Dateien und GitHub

Benötigte neue Dateien: `Art/World/VisualV2ShadowQualityV8/ShadowLift.hlsl`, `Variants.json`; `Content/Environment/VisualV2ShadowQualityV8/Materials/M_SV8_ShadowLift_Experimental.uasset`; Werkzeuge unter `Tools/VisualV2ShadowQualityV8/`; dieser Bericht. **Keine bestehende Map, kein Originalmaterial, kein Gameplay-/Player-/Vegetationsasset geändert.** `Initialize.py` erzeugt lokale Sicherheitsdaten aus dem Projekt selbst; keine archivierten Kontrollmedien als Build-/Testfixture notwendig.

Zwei gezielte kleine Sicherungsschritte: getestete Quellen/Testmaterial und danach Bericht. Quellencommit `38c54acfd2053898c7e714ddcd423f31151c3fd2`; abschließender Berichtscommit und tatsächliche Remote-/LFS-Nachweise in `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/GIT_ABSCHLUSS.json` und der Codex-Abschlussantwort. Das Testmaterial umfasst **26.863 Bytes LFS**; keine Maprevision und keine Kontrollmedien hochladen. Vollständige Indexprüfung und `git diff --cached --check` vor den Commits; Remote und LFS nach den Pushes prüfen. Keine Käufe, Budgetänderungen, Force-Pushes, Löschungen, Resets oder LFS-Bereinigungen.

Lokale vollständige Prüfdaten: `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/FinalEvidence.json`, `/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19/QA/` und `Saved/VisualV2ShadowQualityV8/`. Die drei bereits vorher fremden unversionierten Pfade bleiben offen. Keine Schattenübernahme vor Harrys visueller Freigabe; nach Bericht und Bildern stoppen.
