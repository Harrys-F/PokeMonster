# VisualV2 V7 – Pokémon-Testbereich, Heilhaus und Karpador

Stand: 03.11.2026. Ausgangscommit `41ecb104c1bd77b388eeb8b8dc4194532fd44b95`, Branch `main`. Bestehendes Projekt, Unreal 5.8.4, Mac16,12 / Apple M4 / 16 GB, macOS 27.2, Metal. Keine neue Map oder Worktree.

## Ergebnis und Abgrenzung

**68 integrierte Modelle: 19 spielbereite Pokémon und 49 statische Prüfkandidaten.** Alle besitzen eigene tatsächliche Plätze in der vorhandenen TestGround-Struktur. Beim ersten Besuch wird die ganze Sammlung schrittweise geladen; anschließend bleiben alle 68 Darsteller bis zum Ende dieser Spielwelt physisch bestehen, auch nach Return. Keine wechselnde Einzelmodellvorschau mehr.

Heilhaus: ausschließlich private Oberflächenbindungen und Materialgraphen; Architektur, vier Wände, Lichtquellen, Möbelpositionen, Heiler, Tür und Kollision unverändert. Karpador: explizites VisualV2-Wasserprofil innerhalb der bestehenden KI. Keine Änderung der Originalmodelle/Animationen, Garados V4, Kamera V3, Grafikprofile, anderen Arten oder geschützten Maps.

## 1. Registrierung und Bedienung

Die 19 spielbereiten Arten kommen weiterhin aus `UPokeMonsterCreatureSpeciesData::GetRegisteredPlayableSpecies()`. Weitere vollständig validierte spielbare Arten wurden nicht gefunden. Statische Unreal-Importe werden aus dem bisherigen `/Game/Characters/Creatures/ModelIntakeV6/<Modell>/...`-Pfad über die Asset Registry gelesen. Keine zweite handgepflegte Artenliste. Reine Incoming-Quelldateien ohne Unreal-Integration wurden nicht neu importiert.

Neue Arten im bestehenden Register beziehungsweise neue statische Unreal-Importe im bestehenden Importpfad erscheinen nach Neustart der PIE-/Spielsitzung automatisch mit neu berechneter Fläche. Ein manueller Umbau einzelner Plätze ist nicht erforderlich. Der Bereich bleibt Development-/PIE- und VisualV2-spezifisch.

```text
pm.TestGround.List
pm.TestGround.Go Pikachu
pm.TestGround.Go Karpador
pm.TestGround.Go Garados
pm.TestGround.Go Aquana
pm.TestGround.Go Modell:Nidoran_m
pm.TestGround.Go 1
pm.TestGround.Return
pm.TestGround.Mode auto|idle|walk|run|turn|directions|reset
pm.TestGround.Reset
pm.TestGround.React attack|hit|faint|happy
```

Zahlen 1–19 und der interne Legacy-Alias `Zunderlauf` für Glumanda bleiben erhalten. Unbekannte Ziele werden abgelehnt. Statische Kandidaten akzeptieren nur `idle`, Inspektionsdrehen und `reset`; Gehen/Laufen/Reaktionen werden ausdrücklich verweigert. Eine Inspektionsdrehung ist keine Körperanimation.

Der erste vollständige Ladevorgang benötigte im warmen Prüfzustand etwa 1.41 s; das ist keine Garantie für einen kalten SSD-/Shaderstart. Die schrittweise Initialisierung kann einzelne Ladehänger verursachen. Normales Erkunden lädt die 49 großen Importpakete erst bei ausdrücklicher Prüfanforderung.

## 2. Flächen, Bewegung und Sicherheit

Gleicher vorhandener TestGround-Mittelpunkt `(-7500, -20000, -20000)` cm. Die alte einheitliche 18-m-Aufteilung ist durch kompakte, nach Größe sortierte Reihen ersetzt. Maßgeblich sind tatsächliche Mesh-Bounds einschließlich Versatz, Wasserhülle und Sicherheitsreserve, Körper-/Bewegungsradius und benötigte Besucherfläche. Rohmodelle behalten den importierten Zentimetermaßstab statt einer gemeinsamen 200-cm-Normalisierung. Das ist ausdrücklich keine Freigabe ihrer kanonischen Artgröße.

Freie Land-Verbindungsstreifen: 1,40 m. Getrennte Wasserbecken mit echtem geprüftem Boden-/Wasservolumen, umlaufenden Stegen und Queranschluss an die Landfläche. Karpador: etwa 8,07 × 8,07 m; Garados: etwa 25,19 × 25,19 m einschließlich Stegen. Zusätzliche Reserve hält auch gedrehte vollständige Bounds innerhalb der Wasseröffnung. Niedrige Außenbarrieren verhindern versehentliches Herunterlaufen; definierte Anschlüsse bleiben offen. Die Wasser-Besuchspunkte liegen an den offenen Nordanschlüssen, damit die Sicherheitsränder nicht vor der Kamera stehen. Keine Decke über Flug-/Schwebeprüfungen.

Alle statischen Darsteller haben weder KI- noch Actor-/Komponententicks oder Spielkollision. Die spielbereiten Darsteller nutzen vorhandene kontrollierte Bewegungsziele, keine natürliche Wild-KI. Entfernte Skelett-/Bewegungsupdates ruhen; die Modelle werden dabei nicht entfernt. Nach abgeschlossener Sammlung endet die Importsuche. Vorhandene Idle-/Geh-/Lauf-/Schwimmrollen und weiche Drehung werden verwendet. Kleine ortsfeste Hinweistexte und die detaillierte List-Ausgabe ersetzen große schwebende Namensschilder.

Teleportziele liegen auf begehbarem Land beziehungsweise Stegen, nicht auf der tieferen Schwimm-Wurzelhöhe. Ursprüngliche Position, Blickrichtung, Orbit, Abstand und Kameramodus werden beim Return wiederhergestellt. Die bestehende Begleiterkorrektur bleibt unverändert. Gegen Menü/Kampf/Innenraum/ungültige Welt geschützte Reisen bleiben erhalten.

### Vollständige spielbereite Zielliste

| Nr. | Name | Fläche m | Bewegungsradius cm | vorhandene Rollen | Rig |
|---:|---|---:|---:|---|---|
| 1 | Bisasam | 5.44 × 5.44 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 2 | Glutexo | 6.74 × 6.74 | 126.5 | Idle / Gehen / Laufen | vorhanden |
| 3 | Glurak | 11.22 × 11.22 | 195.5 | Idle / Gehen / Laufen | vorhanden |
| 4 | Schiggy | 5.06 × 5.06 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 5 | Raupy | 4.72 × 4.72 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 6 | Smettbo | 6.89 × 6.89 | 126.5 | Idle / Gehen / Laufen | vorhanden |
| 7 | Hornliu | 4.66 × 4.66 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 8 | Bibor | 6.03 × 6.03 | 115.0 | Idle / Gehen / Laufen | vorhanden |
| 9 | Habitak | 4.90 × 4.90 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 10 | Pikachu | 5.08 × 5.08 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 11 | Raichu | 5.91 × 5.91 | 92.0 | Idle / Gehen / Laufen | vorhanden |
| 12 | Myrapla | 5.10 × 5.10 | 90.0 | Idle / Gehen / Laufen | vorhanden |
| 13 | Enton | 5.77 × 5.77 | 92.0 | Idle / Gehen / Laufen | vorhanden |
| 14 | Machomei | 8.63 × 8.63 | 184.0 | Idle / Gehen / Laufen | vorhanden |
| 15 | Nebulak | 7.21 × 7.21 | 149.5 | Idle / Gehen / Laufen | vorhanden |
| 16 | Gengar | 9.04 × 9.04 | 172.5 | Idle / Gehen / Laufen | vorhanden |
| 17 | Karpador | 8.07 × 8.07 | 103.5 | Idle / Gehen / Laufen / Schwimmen | vorhanden |
| 18 | Garados | 25.19 × 25.19 | 450.0 | Idle / Gehen / Laufen / Schwimmen | vorhanden |
| 19 | Glumanda | 5.20 × 5.20 | 90.0 | Idle / Gehen / Laufen | vorhanden |

Die Referenzgrößen und vollständigen Mesh-/Skelett-/Clip-Pfade stehen in `RegisteredSpecies.json`; Flächenmittelpunkte und Radien in `NativeGameplay01/GalleryResult.json`. Größen sind keine Humanoidenhöhe: Garados Referenz 650 cm beschreibt seine große Körperausdehnung. Vorhandene Flug-/Schwebe- und Wasserrollen bleiben artspezifisch.

### Vollständige statische Zielliste

Alle folgenden 49 Kandidaten: statisch, Rig/Animationen/Spielintegration fehlen. XYZ sind gerundete ursprüngliche Import-Bounds in cm; die spätere Artgröße bleibt offen. Beide Schreibweisen `Go <Name>` und `Go Modell:<Name>` funktionieren.

| Ziel | Import-Bounds XYZ cm | Fläche m |
|---|---|---:|
| Aquana | 93 × 67 × 104 | 2.90 × 2.90 |
| Arbok | 98 × 78 × 100 | 2.95 × 2.95 |
| Arkani | 97 × 74 × 84 | 2.92 × 2.92 |
| Blitza | 43 × 89 × 99 | 2.90 × 2.90 |
| Digda | 96 × 92 × 82 | 3.03 × 3.03 |
| Digdri | 97 × 94 × 83 | 3.05 × 3.05 |
| Duflor | 97 × 69 × 77 | 2.90 × 2.90 |
| Entoron | 99 × 64 × 82 | 2.90 × 2.90 |
| Flamara | 40 × 98 × 63 | 2.90 × 2.90 |
| Fukano | 88 × 76 × 98 | 2.90 × 2.90 |
| Giflor | 100 × 101 × 82 | 3.12 × 3.12 |
| Golbat | 97 × 21 × 59 | 2.90 × 2.90 |
| Ibitak | 95 × 88 × 87 | 2.99 × 2.99 |
| Kicklee | 99 × 28 × 66 | 2.90 × 2.90 |
| Knofensa | 79 × 39 × 98 | 2.90 × 2.90 |
| Knogga | 97 × 87 × 80 | 3.00 × 3.00 |
| Knudeluff | 99 × 64 × 98 | 2.90 × 2.90 |
| Magmar | 97 × 51 × 84 | 2.90 × 2.90 |
| Nidoking | 85 × 100 × 52 | 3.01 × 3.01 |
| Nidoqueen | 95 × 83 × 98 | 2.96 × 2.96 |
| Nidoran_m | 58 × 100 × 82 | 2.90 × 2.90 |
| Nidoran_w | 67 × 99 × 88 | 2.90 × 2.90 |
| Nidorina | 83 × 63 × 98 | 2.90 × 2.90 |
| Nidorino | 73 × 99 × 92 | 2.93 × 2.93 |
| Nockchan | 98 × 23 × 88 | 2.90 × 2.90 |
| Omot | 97 × 37 × 55 | 2.90 × 2.90 |
| Onyx | 54 × 97 × 101 | 2.90 × 2.90 |
| Paras | 95 × 100 × 62 | 3.08 × 3.08 |
| Parasek | 86 × 97 × 81 | 3.00 × 3.00 |
| Piepi | 98 × 77 × 104 | 2.95 × 2.95 |
| Pixi | 106 × 86 × 80 | 3.06 × 3.06 |
| Pummeluff | 100 × 76 × 89 | 2.96 × 2.96 |
| Rattfratz | 97 × 98 × 79 | 3.08 × 3.08 |
| Rattikarl | 73 × 102 × 81 | 2.95 × 2.95 |
| Rettan | 33 × 96 × 39 | 2.90 × 2.90 |
| Sandamer | 114 × 77 × 65 | 3.08 × 3.08 |
| Sandan | 97 × 91 × 94 | 3.03 × 3.03 |
| Sarzenia | 98 × 71 × 89 | 2.91 × 2.91 |
| Schlurp | 75 × 100 × 65 | 2.95 × 2.95 |
| Sichlor | 96 × 48 × 61 | 2.90 × 2.90 |
| Tangela | 185 × 169 × 171 | 4.21 × 4.21 |
| Tauboga | 96 × 40 × 53 | 2.90 × 2.90 |
| Tauboss | 192 × 97 × 100 | 3.85 × 3.85 |
| Taubsi | 55 × 103 × 79 | 2.90 × 2.90 |
| Tragosso | 101 × 92 × 96 | 3.07 × 3.07 |
| Ultrigaria | 96 × 72 × 59 | 2.90 × 2.90 |
| Vulnona | 86 × 101 × 76 | 3.03 × 3.03 |
| Vulpix | 88 × 101 × 95 | 3.04 × 3.04 |
| Zubat | 96 × 20 × 81 | 2.90 × 2.90 |

## 3. Heilhausmaterialien

168 Materialbindungen an 137 vorhandenen Raum-Actors wurden umgebunden. Der vollständige Vergleich der 1380 gespeicherten Scene-Actors bestätigt: außerhalb dieser Materialslots identische Actor-/Komponentenwerte, Instanzen, Transformationen, Kollisionen und Postprocess-Daten. Keine neue Raumgeometrie und keine Lichtänderung.

| Material | Umsetzung |
|---|---|
| M_V7_LimePlaster | warmer matter Kalkputz, unregelmäßige eigene Mikro-Normale, 84-cm-Weltprojektion, Roughness 0,94 |
| M_V7_SageLimewash | zurückhaltende salbeifarbene Kalkfassung mit derselben unregelmäßigen Körnung |
| M_V7_OakFloor | vorhandene lokale Fab-Texturen Cracked Wooden Planks: BaseColor, Normal, eigene Roughness-Textur; 200-cm-Wiederholung, matte warme Farbkorrektur |
| M_V7_OakJoinery | dieselben vorhandenen PBR-Quellen bei 180-cm-Wiederholung und dunklerer Farbgebung für Fachwerk, Decke/Möbel |
| M_V7_ReviewWater | ausschließlich einfache dynamische Prüfbeckenoberfläche; Hauptteich/Bach unverändert |

Weltbasierte Projektion vermeidet gestreckte Standardwürfel-UVs. Holzroughness wird auf 0,68–0,94 begrenzt; Normalkarten sind korrekt als solche abgetastet. Vorhandene Fab-Wall-Texturen wurden exportiert und geprüft, aber als Mauerwerk nicht fälschlich als Putz verwendet. Eine zunächst sichtbare regelmäßige Mikrostruktur wurde nach echter Bildprüfung durch eine eigene nahtlose numerische 512²-Normale ersetzt. Keine KI-generierte Nachweisaufnahme.

Neue eigene Dateien liegen unter `/Game/Environment/VisualV2InteriorV7/`; reproduzierbare Normalkartenquelle unter `Art/World/VisualV2InteriorV7/Generated/PlasterGrainNormal.png`. Fab-Quellen bleiben unverändert lokal. Unverbundene Knoten aus Werkzeugwiederholungen wurden ausschließlich aus den eigenen Graphen entfernt: final 6/6/9/9/4 Ausdrücke, Shaderprüfung jeweils 0 Fehler. `MaterialAuditFinal.json` bestätigt die tatsächlichen endgültigen Texturbindungen.

## 4. Karpador: Ursache und gezielte Änderung

Der tatsächliche Teich liegt bei `(720, -1800)` mit Halbachsen 860/610 cm und Wasserhöhe 4,2 cm. Der Habitat-Override war bereits rund 2.109 cm; der nominelle Art-Radius 750 cm allein war daher nicht die Ursache. Ausschlaggebend waren feste Reisepunkte, längere Ruhe-/Schlafgewichtung und die nachträgliche Kürzung neuer Ziele auf 1.000 cm. Der allgemeine Umwegplaner hat zusätzlich seine unveränderte 1.250-cm-Suchgrenze.

Ein einziges neues Opt-in der bestehenden Karpador-Regel wird nur auf VisualV2 und nur im Wasser gesetzt. Andere Maps/Arten/Garados/Begleiter behalten ihre bisherigen Werte und Pfadregeln. Ganze erodierte Teichellipse statt weniger Reisepunkte, bestehende Sektor-/Zielhistorie gegen Wiederholungen. Bei langen geraden Wasserstrecken wird nur dann das volle Ziel behalten, wenn die vorhandene durchgehende 25-cm-Tiefen-, Boden-, Körper- und Sweepprüfung die gesamte Strecke freigibt. Keine vergrößerte A*-Suche, kein neuer Controller und keine Positionssprünge.

Nur im Opt-in: Gehgewicht 12, Beobachten 1,05, Ruhe 0,36, Schlaf 0,025; Mindest-/Maximalaktivität 3/24 s, Ruhe 4 s, Schlaf 6 s, Bewegungspause 0,6–1,8 s. Das sind Gewichtungen, keine festen Quoten. Laufende gültige Wanderpfade enden vor dem Aktivitätswechsel. Geschwindigkeit/Schwimmclips/Referenzschritt bleiben unverändert: 56 cm/s normales Schwimmen, vorhandene 35-cm/s-Referenz und begrenzte Abspielrate. Kampf-/Aufmerksamkeits-/Fluchtprioritäten und Weltuhrpausen bleiben erhalten.

### Tatsächlich beobachtete Bewegung

| Lauf | Zeitraum | beobachtete Strecke m | Samples mit Bewegung | Planungen | blockierte Schritte |
|---|---:|---:|---:|---:|---:|
| V6-Ausgangsstand | 240 s | 50.0 | 38.7 % | 10 | 0 |
| Ziel-/Aktivitätskorrektur, gleicher Uferstandpunkt | 240 s | 101.5 | 77.5 % | 13 | 0 |
| finale Langstreckenfassung, entfernter Uferstandpunkt | 360 s | 168.1 | 85.2 % | 19 | 0 |

Die finalen 1363 Positionsstichproben (etwa alle 0,25 Spielsekunden) erreichten alle acht normalisierten Richtungssektoren, X = -62.3…1436.0 cm und Y = -2286.1…-1308.6 cm. Das erfolgreich geprüfte 80-cm-Raster erstreckt sich ungefähr von X −60 bis 1.460 und Y −2.330 bis −1.290 cm. Die westlichen/östlichen nutzbaren Randbereiche wurden damit tatsächlich erreicht; keine Behauptung, jede einzelne Wasserzelle durchschwommen zu haben.

Das finale Raster benutzt die echte aktuelle `ProjectWalkable`-Prüfung einschließlich Wassertiefe, Abstand zum Ufer, Hindernissen und Körpermaß. Endpunkte allein ersetzen keine Streckenprüfung; jeder wirkliche Bewegungsschritt bleibt geprüft. Der 14-m-Automationstest beweist separat das zulässige lange direkte Ziel bei unverändert abgelehnter generischer Planung und ungültigem Uferziel. Die längste im Naturlauf beobachtete neue Zielebene betrug rund 11,7 m.

CPU-Messung nur dieses Karpador-Komponentenfensters: im Mittel 90.7 µs je gemessenem Tick, insgesamt 2.84 ms erfasste Planung. Keine globale KI-Performancebehauptung. Die sechsminütige Datenerfassung erfolgte ohne Video/erzwungene Ziele/Uhrpause. Erst anschließend kurze Aufnahme und regulärer Kampf/Fang mit erneut verfügbarem Begleiter.

Die Strecken sind aus den tatsächlich aufgezeichneten Positionen berechnet. Der alte interne Gesamtzähler enthielt auch Startbewegung vor dem Beobachtungsfenster; deshalb sind die anfangs genannten 106,4/172,2 m nicht die bereinigten Vergleichsstrecken. Der finale Zähler wird zusätzlich am Anfang/Ende differenziert. Kleine Abtastfehler der Linienlänge sind möglich. Der entfernte Standpunkt des Zusatztests vermindert Spielereinfluss und ist kein identischer Vorher-Vergleich.

Routendaten und klar beschriftete Datengrafik: `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/KarpadorRoute.svg` (keine Unrealaufnahme).

## 5. Performance

Unverändertes Profil C, QHD 2560×1440, 75 % Screen Percentage (nominell 1920×1080 intern), High (alle untersuchten Scalability-Qualitäten 2), bestehender TAAU-Anschluss, Software-Lumen + IFG, VSM mit vier Strahlen. Weltuhr weiterhin 120 Minuten, Mittagssonne 75°. CVars und vorhandene Postprocess-Konfiguration werden unterschieden: der globale AA-CVar 4 wird weiterhin vom vorhandenen TAA-only-Anschluss der Spielansicht überlagert. Keine Rendering-/Device-Profile-Änderung.

Separate Development-Spielprozesse; zwölf Uhr gehalten, gleiche Kamerastellen, je drei 6-s-CSV-Messfenster nach mindestens 4 s Einlauf, keine Videoaufnahme. FPS = 1000 / mittlere Framezeit. GPU-/Threadwerte sind getrennte Zähler mit möglichen Überlappungen und werden nicht addiert. Nicht verfügbare Einzelzähler werden nicht als Nullkosten ausgegeben.

| Stelle | vorher FPS | erster Nachlauf FPS | frische Wiederholung FPS | final: alle 68 geladen FPS |
|---|---:|---:|---:|---:|
| Dorf | 31.67 | 26.60 | 31.46 | 30.79 |
| Wald | 33.21 | 26.25 | 33.17 | 32.85 |
| Heilhaus | 38.09 | 28.52 | 37.74 | 37.64 |

Die ersten drei Spalten verwenden die normale Bibliotheksbelegung vor einem Modellbesuch. Die letzte ist eine zusätzliche Belastungsbedingung mit bestätigten 68 geladenen Darstellern während jedes Samples; deshalb keine identische Objektbelegung zum Ausgangszustand.

| Stelle | GPU vorher ms | GPU Wiederholung ms | GPU alle 68 ms | Frame-p95 vorher / Wiederholung / alle 68 ms | Game / Render alle 68 ms |
|---|---:|---:|---:|---|---|
| Dorf | 22.38 | 22.41 | 23.27 | 32.73 / 33.23 / 33.67 | 1.69 / 32.49 |
| Wald | 29.07 | 28.92 | 29.44 | 31.47 / 31.48 / 31.59 | 1.77 / 30.44 |
| Heilhaus | 24.98 | 25.13 | 25.32 | 27.78 / 28.11 / 28.16 | 1.53 / 26.57 |

Der erste Nachlauf war deutlich langsamer und verschlechterte sich innerhalb der Sitzung. Er bleibt ausdrücklich dokumentiert. Gepaarte Läufe mit alten Raum-Materialbindungen beziehungsweise vorübergehend ausgeblendeten entfernten Modellmeshes in wechselnder Reihenfolge zeigten keinen konsistenten Kostenvorteil; keine entsprechende Produktionsänderung übernommen. Frische Wiederholung wieder nahe Ausgangsstand. Die Ursache der zeitlichen Drift ist nicht bewiesen. Lesend festgestellt: Netzbetrieb, Low-Power-Modus 0, keine pmset-Thermikwarnung, rund 7,5 GB belegter Swap nach vielen Prüfsitzungen. Das ist kein Beleg für eine bestimmte thermische oder Speicherursache.

Zusammenhängender normaler Eingaberundgang ohne Video, mit aktiver Weltuhr/KI/Begleiter: **33.93 FPS im Mittel**, GPU 25.16 ms, Game 2.59 ms, Render 29.45 ms, Frame-p95 36.98 ms, 1-%-Low 21.04 FPS, Maximum 111.14 ms bei 3314 Frames. Die Tour erfolgte vor dem Galerie-/Aufnahmeteil. **Stabile 30 FPS sind damit nicht nachgewiesen.** Kein direkter Leistungsgewinn gegenüber einem exakt gleichen historischen V6-Tourzustand behauptet.

## 6. Tatsächlich durchgeführte QA

| Prüfung | Ergebnis |
|---|---|
| letzter Editor-Build | EditorBuild13, Exit 0 |
| vollständige Automation / strenger Wrapper | Automation11: 336 bestanden, 0 Testwarnungen, 0 fehlgeschlagen, 0 ausgelassen/in Bearbeitung; Engine 0, Wrapper 0 |
| bestehende Tests | alle 333 erhalten; ursprünglicher Trockenboden-Test auf tatsächliche Wasserprojektion angepasst |
| neue Tests | vollständige dauerhafte Sammlung/gedrehte Wasserhüllen/Spielerkapsel an allen 68 Zielen; Whole-Water-Sampling und ausschließlich Karpador-Regel; lange direkte Wasserroute bei unverändertem Legacy-Limit |
| zwölf Map Checks | MapCheckResultsFinal.json aus EditorRailsFinal02/Engine.log, zwölfmal 0 Fehler / 0 Warnungen, keine Maps gespeichert |
| PIE | PIEInterior01: komplette Raumfunktion; PIEGalleryFinal01: komplette Sammlung/alle Ziele/Editor-Konsole/Bewegung/Rückkehr; PIEWaterViewFinal03 + NativeWaterViewFinal01: endgültige offene Geländer, Wasserbesuche, Kamera, Rückkehr |
| separater Gameplayprozess | NativeGameplay01: durchgehender Rundgang, Sprint/Kamera, Brücke, Cottage, alle 68 Ziele im selben Prozess, danach Dialog/Kampf/Fang/Team/Begleiter/Heilhaus/SaveLoad/Mapwechsel |
| Heilhaus | NativeInterior01 + PIEInterior01: alle vier Wandgruppen/18 Wandactors sichtbar, acht Ansichten, Heiler heilt echte verbrauchte AP/KP, Tür Tempo 1/2/3, isolierter SaveLoad |
| finale natürliche Wasserfassung | NativePondFinal01: 360 s, vollständige Routen-/Tiefenprüfung, anschließend regulärer Kampf/Fang/Begleiter erfolgreich |
| Rückkehr / Steuerbarkeit | ursprüngliche Position/Facing/Orbit/Abstand und Team erhalten; alle 19 + 49 Ziele tatsächlich angesteuert, Begleiter nah und oberhalb des Bodens |
| Originale / Spielstände | SHA-Prüfungen gegen tatsächlich vor Arbeitsbeginn erfasste Dateien; siehe ProtectionFinal.json |

Zeitliche Einordnung: Der zusammenhängende Eingaberundgang und Save/Load-/Mapwechselablauf wurden vor der letzten, ausschließlich Karpador betreffenden Langstreckenkorrektur ausgeführt. Diese wurde danach mit dem vollständigen 336-Test-Lauf, dem eigenen sechsminütigen nativen Teich-/Kampf-/Fang-/Begleitertest und der endgültigen PIE-Serie geprüft. Schutzränder und alle 68 Kapselziele sind im letzten Build/Testlauf enthalten. Die letzte reine Sichtkorrektur stellt die unveränderten durchgehenden Kollisionssperren als offene schmale Geländer dar; sie und die Nord-Besuchspunkte wurden nochmals in PIE geprüft. Die normalen Welt-Messkameras liegen außerhalb der Galerie; eine neue Performanceverbesserung durch diese Sichtkorrektur wird nicht behauptet.

Frühe Prüfwerkzeugfehler (Diagnose-Kamera-API, zu strenger Materialausdruckszähler) und ein alter Trockenhöhen-Test wurden korrigiert; die entsprechenden fehlgeschlagenen Zwischenläufe sind keine bestandenen Prüfungen. Compile-Zwischenläufe scheiterten an einem falschen Getter im neuen Test beziehungsweise einer lokalen Variablen der Plaquenausrichtung und einem privaten Testzugriff; korrigiert und erfolgreich neu gebaut. Ein Buildstart mit falschem Prüfpfad wurde nicht ausgeführt; die darauf folgende alte Binär-Testserie zählt nicht als Nachweis der letzten Geländerkorrektur. Finale erfolgreiche Labels stehen oben.

Engine-/Infrastrukturmeldungen werden getrennt von den funktionalen Testergebnissen behandelt. Bekannte ExperimentalToolsets-Pythonstartmeldungen und frühe Condition-Meldungen vor der Testqueue sind keine als bestanden umetikettierten funktionalen Tests. Der vorhandene LeafOak-Instancing-Hinweis in der Kampfkulisse ist eine bestehende fremde Materialwarnung, kein Anlass zum Ändern geschützter Originale. Keine neuen unbehandelten Projekt-Tracebacks oder Abstürze in den freigegebenen finalen Abläufen. In den abschließend ausgewerteten Logs wurden keine idevice_id-/Bad-CPU-/libimobiledevice-Meldungen gefunden; LogOverview.json hält dies getrennt fest. Kein Force Quit; eigene Sitzungen regulär beendet. Physische Controllerbedienung wurde nicht als neuer Hardwaretest zertifiziert.

## 7. Echte visuelle Nachweise

Alle Originalbilder sind echte Unreal-QHD-Aufnahmen. Diagnoseübersichten sind ausdrücklich zusätzliche Ansichten, keine neue Spielkamera. Die übrigen Modell-/Innenraumaufnahmen stammen aus der bestätigten Third-Person-Kamera. Vorher-/Nachhermontagen enthalten nur beschriftete Skalierungen echter Bilder; Originale bleiben separat erhalten.

| Zweck | Datei unter dem Nachweisordner |
|---|---|
| komplette finale Galerie | PIEWaterViewFinal03/TestGround_DiagnosticOverview.png |
| kleine Modelle | PIEGalleryFinal01/TestGround_Raupy.png, TestGround_Pikachu.png |
| große Modelle | PIEGalleryFinal01/TestGround_Glurak.png, TestGround_Machomei.png |
| Wasser | PIEWaterViewFinal03/TestGround_Karpador.png, TestGround_Garados.png |
| statische Kandidaten | PIEGalleryFinal01/Static_Aquana.png, Static_Entoron.png, Static_Onyx.png, Static_Tauboss.png, Static_Tangela.png, Static_Zubat.png |
| Heilhaus vorher | EditorRoomBefore01/After_Heilhaus_0…315.png – historischer Werkzeugname, der Ordner ist ausdrücklich der VORHER-Lauf |
| Heilhaus final | PIEInterior01/After_Heilhaus_0…315.png; NativeAfterFinal01/Heilhaus.png |
| gleiche Messkamera vorher/nachher | NativeBefore01 und NativeAfter02: Dorf.png, Wald.png, Heilhaus.png |
| natürlicher Karpador | NativePondFinal01/Karpador_Observed.png, KarpadorRoute.svg |

Kurze Filme, jeweils wirklich dekodiert und gegen Originalzeitstempel geprüft:

- `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/Videos/Motion_Pikachu.mp4` – 80 echte Frames, Intervallrate 8.079086415544571 FPS.
- `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/Videos/Motion_Karpador.mp4` – 80 echte Frames, Intervallrate 7.937039517749498 FPS.
- `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/Videos/Motion_Garados.mp4` – 76 echte Frames, Intervallrate 7.574482410368624 FPS.
- `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/Videos/NaturalKarpadorMotion.mp4` – 121 echte Frames, Intervallrate 7.547169811320755 FPS.

Die Aufnahme belastet das Spiel und ist kein Gameplay-Benchmark. Keine Vervielfachung/Interpolation, keine pauschale 30-FPS-Aufnahmebehauptung. Eine vollständige neue temporale Renderingfreigabe folgt daraus nicht.

## 8. Geschützte Inhalte und offene Punkte

Schutzprüfung: 6.869 Ausgangsdateien geprüft; 1.757 Originalquellen/Assets und 758 vorgefundene Save-Dateien (einschließlich früherer isolierter QA-Stände) unverändert und vollständig vorhanden. Bestehende Originalquellen/Assets, Nutzersaves, lokale unversionierte Nutzerdateien, alle anderen Maps und Nutzerkonfiguration unverändert. `Config/DefaultEngine.ini` bleibt exakt beim vorgefundenen SHA `f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523`. Beide Vollbackup-Refs bleiben bei `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Das beweist den Referenzerhalt, behauptet keine zusätzliche aktuelle Vollsicherung. Keine Übernahme nach Westland.

Die vier V5-Begegnungsfelder bleiben bei ihren vorhandenen Wahrscheinlichkeits-/Trigger-/Cooldown-/Vegetations-/Habitatwerten. Als **nicht implementierter späterer Vorschlag**: unregelmäßige kleine Buschgruppen, sichtbar sichere Wege und große Begrenzungsbüsche außerhalb dieser Wege. Keine Änderung ohne spätere Freigabe.

Offen bleiben die 49 Kandidaten-Rigs, Gewichte, Animationssätze, Artmaßstäbe und spätere Gameplaydaten; insbesondere hochpolygone Importkandidaten sind noch keine optimierten spielbaren Assets. Die Galerie kann bei kalter Erstinitialisierung und dichter Sicht teuer sein; weit entfernte Animationen sind reduziert, Originalqualität bleibt erhalten. Performancedrift und einzelne Frametimespitzen sind nicht abschließend erklärt. Eine vollständige Langzeit-/Temporalfreigabe wird nicht behauptet. Harry beurteilt die Gestaltung anschließend selbst.

## 9. Git-Abschluss

Nur eigene V7-Quellen, Werkzeuge, kleine benötigte Materialquellen, private Unreal-Ableitungen, VisualV2-Materialbindungen und Dokumentation sichern. Keine Kontrollmedien, Fab-Originale oder geschützten Incoming-Dateien hochladen. Commit und Synchronisationsnachweis werden im Abschlusschat genannt; der Bericht ist im gleichen Umsetzungscommit enthalten (`git log -1 -- Docs/VISUALV2_POKEMON_TESTGROUND_HEALHOUSE_V7.md`). Nach geprüftem Push keine weitere Bearbeitung bis Harrys Beurteilung.
