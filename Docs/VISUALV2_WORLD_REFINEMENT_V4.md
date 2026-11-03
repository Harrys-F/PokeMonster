# VisualV2 World Refinement V4 – Prüfbericht

Stand: 03.11.2026. Basis `38c6d87e7f8cfe349f3f7aafee5f30e598a4d54f`, bestehendes `main`. Ausschließlich VisualV2 und eigene V4-Derivate bearbeitet. **Technische Prüfungen bestanden; die visuelle Abnahme bleibt Harry vorbehalten. Keine Übernahme nach Westland.** Die echten Leistungswerte samt Verlusten stehen unten; ein stabiles FPS-Ziel wird nicht behauptet.

## 1. Vorher-Bestand und Wiederherstellungspunkt

Die ganze bestehende 90×65m-Hauptfläche wurde untersucht: X −6000…3000, Y −3250…3250cm. Das Gelände ist ein statisches Mesh, **kein Unreal-Landscape-Actor**. Deshalb wurden keine Landscape-Layer, Heightmap-Systeme oder parallelen Landschaftsarchitekturen eingeführt. Vorhanden sind zwei funktionale Häuser, Garten, fünf Wegzüge, drei Waldlagen/Waldränder, Lichtung, Hügel/Felsen, Ruine, Bach mit kurzer Abzweigung und ein getrennter tiefer Teich. Alte unsichtbare Gebäudeproxies wurden nicht zu weiteren Häusern gemacht; das abgesetzte Heilhausinnere blieb erhalten.

Vorher: [SceneBefore.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/SceneBefore.json), [Inventory.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Inventory.json), [Buildings.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Buildings.json). Alle 21 V3-Vergleichspunkte wurden frisch aufgenommen, ergänzt um die vierte Heilhausseite. Die tatsächliche Mapdatei entsprach dem committed LFS-Objekt und dem verifizierten Remote-main: SHA256 `9b203407a8bbaff26dd4de0971fd121faabc4c8145a6db9407dd88ac987f5f44`, 5.546.920Bytes. [MapRecoveryBaseline.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/MapRecoveryBaseline.json) belegt Commit, Pointer und überprüftes unveränderliches lokales LFS-Objekt. Keine zusätzliche Map-/Projektkopie, kein neues Vollbackup behauptet.

## 2. Alle neun Arbeitsabschnitte

| Abschnitt | Tatsächlich geändert / geprüft | Bewusst erhalten |
|---|---|---|
| SW | Niedrige asymmetrische Südwesthügel, reale Gras-/Erdmaterialien, Cottage-Fassaden, Rückfenster und Dach, vorhandene Vegetation neu auf Boden gesetzt | Blumenanzahl, Cottagegrundriss, Zugang und Gartenobjekte |
| SC | Bodenvariation, organischer Teichzugang und Ufermaterial, Geländeübergänge | Startposition, bestehende Wege und Spielobjekte |
| SE | Neue flache östliche Formen, nichtkreisrunde Teichoberfläche, abgestuftes Bett und gedämpftes Wasser, Fernkulisse | Tiefe im Kern, Wasserhabitat und Garados |
| MW | Sämtliche Heilhausfassaden/Materialien, zusätzliche rückwärtige Fenster/Schlagläden und Holzverbände, Pflaster/Grundsockel | Heilpunkt, Eingänge, Innenraum, Interaktionen und Kräutergartenaufteilung |
| MC | Neue Bodenübergänge und Hügel abseits der Wege, vollständige sichtbare Brückenkonstruktion, Bachmaterial | Steinplateau-/Wegkollision, Brückenfunktion und Spawnanker |
| ME | Ruhigere fließende Wasseroberfläche, erdige Ufer, reale Stein-/Bodenmaterialien, östliche Hügel | Ruinenlayout, Bachabzweigung und vorhandene Begehbarkeit |
| NW | Hügel und Wald-/Wiesenübergänge, moosiger Waldboden, Regrounding und geschlossene Fernterrainnaht | Baumarten/-anzahl, lichte Wegschneisen und vorhandene Tierwelt |
| NC | Organischere Bodenformen und Waldboden an Lichtung und nördlichem Waldweg | Lichtung und Hauptwegradius, keine neuen Pflanzenteppiche |
| NE | Unregelmäßige Hänge, Waldboden, eingebettete vorhandene Steine/Pflanzen und Fernhorizont | Bestehende Waldgruppen, Felsen und Lebensraumregeln |

Bestehende Vegetationsdichte und Kräutergartenanordnung wurden nicht pauschal weiter erhöht: die Vorher-Diagnose rechtfertigte das weder gestalterisch noch leistungsmäßig. Keine Rückkehr zum verworfenen European-Beech-Test. Die zwei schon unterirdisch abgesetzten Modelltestbereiche bleiben unabhängig und unverändert; ihre Besuchs-/Rückkehrbefehle wurden geprüft.

## 3. Gelände, Kartenrand und Höhenkontrolle

Eigenes `SM_WR4_Ground`, gleiche XY-Ausdehnung/Topologie und geschlossene Unterseite. 23711 vermessene Oberflächenstützpunkte; niedrige asymmetrische Formen statt regelmäßiger Berge. Sieben breite Hügelgewichte plus kleinräumige Variation, mit weichen Schutzmasken um Wege, Gebäude, Wasser und funktionale Actors. 2060 Wegstützpunkte: **maximale Höhenänderung 0.00cm**. Außerhalb des Teichs größte gemessene Achsensteigung 34.22°, p95 10.02°. Das sind Raster-Achsenwerte, keine Garantie für jeden beliebigen Diagonalschritt.

Vorhandene Bäume, Steine, Bodenpflanzen und zugehörige alte statische Kollisionsproxies wurden anhand tatsächlicher Instanz-Weltpositionen auf die neue Oberfläche gesetzt; keine Einstufung allein nach HISM-Actorursprung. 11466 Instanz-/Komponentenpositionen wurden neu aufgesetzt. Funktionale Actors und Spawnanker blieben unverändert. [GeometryAudit.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/GeometryAudit.json) enthält reale Kollisionsstrahlen auf Hügel, Wege, Gebäudepads und Teichbett; [FinalAudit.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/FinalAudit.json) bestätigt ursprüngliche funktionale Actors und WorldSettings.

Ein eigenes zusammenhängendes Fernterrain verdeckt den bisherigen flachen Abbruchhorizont. Es besitzt **keine Kollision, keinen Schattenwurf und keinen Distance-Field-Beitrag**: keine Erweiterung des spielbaren Gebiets, keine Baumwand. Eine zunächst sichtbare dünne Anschlussnaht wurde durch passende 50cm-Randpunkte und zunehmend gröbere Außenringe geschlossen: 6.240Vertices/11.160Dreiecke, [BackdropStitch.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/BackdropStitch.json). Keine zusätzliche überlappende Bodenfläche. Ein wirkungsloser5cm-Unterlappungsversuch wurde verworfen. Die endgültige Oberseite besitzt getrennte Normalen zur senkrechten Außenwand (50°-Glättungsgrenze). Direkte Normalenabfrage zeigt am alten geschlossenen Rand Z≈0,06–0,09, am korrigierten Rand Z≈0,999. Schatten-/Materialabschaltung in RAM beseitigten die dunkle Naht nicht; die Normalenkorrektur beseitigte sie in echten Vergleichsbildern. Die zunächst falsch orientierten Fernterrainflächen der Zwischenserie06 wurden ebenfalls korrigiert; nurSerie07 gilt als Schlussnachweis. Siehe `SurfaceNormalsVerified.json`, `TerrainNormals.json`, `HorizonProof03` und `SeamDiagnose01`. Die Fernhügel bleiben eine einfache visuelle Testmapkulisse; keine vollständige neue Fernlandschaft mit eigenständigem Gameplay oder neuem Randblockiersystem behauptet.

## 4. Materialien und verfügbare Fab-Quellen

Alle Originalmaterialien/-texturen unverändert. Eigene mapbezogene V4-Graphs unter `/Game/Environment/VisualV2WorldRefinementV4`: Boden, Holz, Stein, Putz, Pflaster, Dach, Glas, grüne Holzläden, Eisen, Brückenholz, Bach, Teich, Fernterrain. Eigene numerische Bodengewichtskarte und feine Putz-Normalmap liegen reproduzierbar unter `Art/World/VisualV2WorldRefinementV4/Generated`; sie sind Materialdaten, keine künstlichen Vergleichsaufnahmen.

| Bereits lokal vorhandene Quelle | Verwendung |
|---|---|
| Fab Uncut Grass `oeeb70` | Reales Wiesengrün und Normalmap, 165cm Wiederholung mit großflächiger Farbvariation |
| Fab Mossy Forest Floor `vfylbge` | Erdiger/moosiger Waldanteil, gedrehte 210cm-Abbildung |
| Fab Cracked Wooden Planks `ui2leaxlw` | Maserung und Normalstruktur der eigenen Holz-/Dachmaterialien |
| Bestehendes Fab `pjwey0` | Erd-/Kiesweg und gedämpfter Teichgrund |
| Bestehendes Pack_Bonus Stone_1 / Tile_1 | Sockel/Stein und Dorfpflaster mit Normal Maps |
| Bestehende eigene Architekturmodule | Fenster, Holzbalken, Brückenteile statt unpassend verkleinerter Komplettbrücke |

Genauer lokaler Quell-/Importpfad je Textur: [ImportedSurfaces.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/ImportedSurfaces.json). Keine Downloads. Neun neu lokal importierte Fab-Texturen unter `/Game/Fab/VisualV2RefinementLocal/Textures` bleiben durch die eng gefasste `.gitignore`-Ergänzung lokal, entsprechend der ausdrücklichen früheren Entscheidung für das öffentliche Repository. Keine Fab-Pixel/Originaldateien werden gepusht; eigene Graphs referenzieren diese lokalen Abhängigkeiten. Die Map benötigt weiterhin die vorhandene lokale Fab-Bibliothek. Roughness ist pro Material/Feuchtbereich gewählt, keine globale Grafikabsenkung.

Die bestehende Weggeometrie ist über eine einmalig berechnete RGBA-Maske in den Boden integriert: Weg, Waldboden, Feuchtigkeit und Makrovariation. Kein pro Pixel wiederholtes Ablaufen aller Wegsegmente und keine zweite flächige Weglage. Farb-/Normaltexturen bleiben erhalten; deutlich regelmäßiger alter Putz wurde nach echter Sichtprüfung durch eigenen zurückhaltenden Kalkputz ersetzt. Dachreihen folgen den tatsächlichen Dachschrägen. Sichtbare Materialwiederholung und die stilisierte Form bestehender Bäume sind nicht vollständig beseitigt.

## 5. Gebäude und Brücke

Heilhaus vorne/hinten/beidseitig und Cottage vorne/hinten geprüft. Außenmaterialien einschließlich Dach, Sockel, Holzrahmen, verputzten Flächen, Fenster und Eingangspflaster verfeinert. Vier vorhandene geformte Fenster-/Steinbankmodule, acht gedämpft grüne Schlagläden und rückseitige Holzverbände ergänzen die vormals schlichten Rückseiten. Positionen wurden gegen echte Mesh-/Wandbegrenzungen geprüft; keine Fenster in erfundene Öffnungen geschnitten. Das bestehende Wand-/Cutaway-Prinzip und die Innenräume bleiben unverändert. Kein neuer Hausgrundriss, keine neue Tür/Quest.

Die vorhandene Brücke bleibt 170cm breit und etwa210cm überspannend; Deckoberkante24cm, Wasser4,4cm. Statt der bisherigen sichtbaren Würfelbretter: vorhandene profilierte Holzbalken mit passend laufender Maserung, durchgehender oberer/unterer Handlauf, sechs Pfosten mit Abdeckung, diagonale Verbände, zwei längs laufende Träger und zwei eingelassene Steinauflager. Auflageroberkante und Trägerunterkante schließen bei5cm an. Keine schwebenden Auflager. Zehn Deckbretter und weitere Teile sind nach Material/Mesh in sechs HISM-Gruppen organisiert; 24 alte sichtbare Einzel-/V3-Teile ausgeblendet, **ihre bewährten Deck-/Geländerkollisionen bleiben erhalten**. Das ist eine strukturelle Bündelung, kein als gemessen ausgegebener Draw-Call-Zähler.

[Bridge.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Bridge.json) und [Architecture.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Architecture.json) enthalten tatsächliche Maße, Module und Bindungen. Brücke im echten Rundgang und separat in beide Richtungen mit `pm.Speed 1`, `2`, `3` bestanden; seitlicher Spieler-Kollisionsversuch gegen Geländer blockiert. Neue untere visuelle Geländerteile erzeugen keine zusätzliche unsichtbare Kleintierbarriere. Keine vollständige Umschließung jedes denkbaren kleinen Pokémon durch diese rein dekorativen Querbalken behauptet.

## 6. Bach, Teich und Lebensräume

Genau zwei vorhandene Wasseroberflächen, keine doppelte Wasserlage. Bach: dezente wandernde Mikro-Normalen mit18cm/s-Materialadvektion entlang der vorhandenen Hauptachse, geringfügig variierende sichtbare Breite; physische Hydrodynamik und komplexe Strömung um Hindernisse werden nicht behauptet. Wasserhöhe, kurzer Nebenarm, Brücke und Wasser-Blocker erhalten. Keine übergroßen neuen Uferfelsen.

Teich: leicht unregelmäßiger Rand statt perfekter Ellipse, angepasste einzelne Oberfläche und passende Bett-/Uferform, erdig gedämpfte Unterwasserstruktur, flache Ränder und erhaltenes tiefes Zentrum. Realer Kollisionsstrahl im Kern: -420.00cm. Bestehende Garados-Tiefe, Habitatparameter und Spieler-Wasserbarrieren unverändert. Beide neuen lokalen Wassergraphs verwenden SingleLayerWater mit zurückhaltender Streuung/Absorption; die anfänglich zu regelmäßigen starken Brechungswellen wurden in der Bildprüfung verworfen und deutlich reduziert. Wasserflächen bleiben aus der Spielkamera eher ruhig; keine fotorealistische Flusssimulation behauptet.

Die wilde Population bleibt maximal14, bestehende Zonen/Regeln/KI und Modelle unverändert. Der echte PIE-Durchlauf beobachtete unter anderem Karpador im `PondWater` und Enton am `PondShore`, dazu Bisasam/Pikachu/Raupy/Habitak in den bestehenden Landzonen. Land-/Wasserprüfung läuft weiterhin über vorhandene Habitat-Fußpunktprojektion und Kollisions-Sweeps, kein zweites Navigationssystem. Alle ursprünglichen funktionalen Map-Actors sind im Signaturvergleich unverändert.

## 7. Echte Bildvergleiche

22 primäre QHD-Vorher-/Nachher-Paare: `BeforeAtlas` → **`AfterAtlas07`**, vierte Heilhausseite `BeforeExtra`→`AfterExtra02`. Zwischenserien01–06 enthalten verworfene Material-/Fixturestände und sind **nicht** der endgültige Nachweis. 21 finale Ansichten stammen aus PIE, die ergänzende vierte Heilhausseite aus dem separaten Development-Spielprozess mit gleicher Kamera/Noon-Konfiguration. Alle Bilder stammen direkt aus Unreal, 2560×1440, gleicher Mittag12:00/75°-Sonne, C75/TAAU/High, normaler Third-Person-Kamera. Kein ImageGen, keine erfundenen Szenen, keine nachträgliche Aufhübschung. Tafeln ordnen nur die echten Bilder mit Beschriftung an.

Wichtig zur Vergleichbarkeit: XY-Position, Blickrichtung, −12°-Neigung und350cm-Abstand wurden übernommen. Wo das tatsächliche Gelände höher ist, folgt die Kamera physikalisch mit. Diese Aufnahmen besitzen deshalb **nicht alle dieselbe absolute Welt-Z-Kameraposition**; Kollisionsverkürzung kann ebenfalls abweichen. Einzelabweichungen stehen in [Analysis.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Analysis.json). Keine heimliche Kamerakorrektur, um eine exakte Gleichheit vorzutäuschen. Die zwei anfänglich unter neue Waldhügel gesetzten alten Fotofixierungen wurden durch oberflächenbezogenes Platzieren korrigiert und neu aufgenommen; dies war ein Testwerkzeugfehler, kein beim normalen Rundgang beobachteter Bodensturz.

[Gesamte finale Bildübersicht](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/WholeMapContactSheet.png)

- [HeilhausFront](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/HeilhausFront.png)

- [HeilhausRueck](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/HeilhausRueck.png)

- [HeilhausNord](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/HeilhausNord.png)

- [CottageFront](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/CottageFront.png)

- [CottageRueck](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/CottageRueck.png)

- [Startwiese](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Startwiese.png)

- [Suedwiese](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Suedwiese.png)

- [Westwald](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Westwald.png)

- [Nordwald](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Nordwald.png)

- [Ostwald](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Ostwald.png)

- [Nordlichtung](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Nordlichtung.png)

- [Steinplateau](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Steinplateau.png)

- [Ruine](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Ruine.png)

- [BachWest](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/BachWest.png)

- [BachOst](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/BachOst.png)

- [BrueckeSued](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/BrueckeSued.png)

- [BrueckeNord](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/BrueckeNord.png)

- [TeichNord](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/TeichNord.png)

- [TeichSued](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/TeichSued.png)

- [Ostwiese](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Ostwiese.png)

- [Garten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/Garten.png)

- [HeilhausSued](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/Comparisons/HeilhausSued.png)

## 8. Performance – neue Messungen, keine alten Werte als neue ausgegeben

Hardware: Mac16,12 / Apple M4 / 16GiB, macOS27.2 Build26B123; UE5.8.4 CL58902052, Metal. Entwicklungsspielprozess mit `-nosound` wie die Vergleichsbasis, explizite VisualV2, isolierter UserDir; kein gepackter Shipping-Test. 2560×1440-Ausgabe,75% Screen Percentage (nominal1920×1080 intern), High-Gruppen2, TAAU, Software-Lumen+IFG, VSM/4Strahlen, Mittag75°. `r.AntiAliasingMethod=4` ist der globale Fallback, kein Beleg für TSR in der Spielansicht: der unveränderte projektinterne TemporalAA-Blendable setzt TAA/TemporalUpscale. `r.TemporalAA.Upsampling=1`, HardwareRayTracing0, FinalGatherMethod0, Shadow.Virtual1 wurden im tatsächlichen Prozess gelesen. Keine Renderingprofile geändert.

`NativeBefore01`/`NativeAfter02`: frisch gestartete separate Prozesse, je drei6s-CSV-Messfenster pro sechs Hauptpunkten nach4s Beruhigung; Startwartezeit/Shaderladen vor der Messung; keine garantierte vollständige PSO-Vorwärmung behauptet. Drei Detailpunkte je ein Fenster. Keine Videoaufnahme, Fotos erst außerhalb der jeweiligen Messfenster. VSync0/FPS-Limit0 nur vorübergehend und vor normalem Ende zurückgesetzt. Statische Messungen halten die Weltzeit bei12Uhr; der separat erfasste echte Bewegungslauf lässt Uhr/KI/Begleiter normal arbeiten. Keine thermische Ursache ohne Sensorbeleg behauptet; zeitabhängige Drift bleibt möglich.

| Messpunkt | FPS vorher | FPS nachher | GPU vorher/nachher ms | Frame-p95 danach ms | Game/Render danach ms |
|---|---:|---:|---:|---:|---:|
| Blumenwiese | 31.47 | 28.88 | 30.72 / 33.66 | 41.58 | 1.77 / 34.63 |
| Waldrand | 34.84 | 30.87 | 27.66 / 31.33 | 41.59 | 1.87 / 32.39 |
| Flussufer | 34.12 | 30.56 | 28.22 / 31.77 | 38.22 | 1.95 / 32.71 |
| Felsen | 39.97 | 34.67 | 15.27 / 17.74 | 32.88 | 2.19 / 28.83 |
| Dorf | 32.83 | 28.77 | 21.52 / 25.03 | 39.63 | 1.72 / 34.76 |
| Lebensraum | 38.97 | 32.76 | 24.57 / 29.39 | 34.26 | 2.16 / 30.51 |
| Kraeutergarten (ein Fenster) | 32.86 | 27.33 | 21.52 / 26.44 | 38.68 | 1.77 / 36.58 |
| Bachbett (ein Fenster) | 36.13 | 29.23 | 26.67 / 33.33 | 35.86 | 1.98 / 34.22 |
| Felsgruppe (ein Fenster) | 40.50 | 32.23 | 23.58 / 29.94 | 32.68 | 2.37 / 30.99 |

Die Leistungsrückgänge der frischen Serien werden ausdrücklich ausgewiesen, nicht mit früheren günstigeren Werten verrechnet. Historischer V3-Bericht: Dorf27,40FPS, Rundgang35,17FPS; die **frische V4-Vorherbasis** lag im selben V3-Stand bereits beiDorf32,83FPS. Diese Streuung verhindert eine saubere Ursachenzuschreibung allein aus unterschiedlichen Starts. Der Render-Thread-Zähler enthält Warte-/Synchronisationsanteile und beweist für sich keinen reinen CPU-Rechenengpass; der Game Thread liegt wesentlich darunter.

### GPU-Durchläufe

| Standort/Stand | Base Pass ms | ShadowDepths ms | IFG ms | LumenSceneLighting ms | Wasser ms | TAA ms |
|---|---:|---:|---:|---:|---:|---:|
| Dorf/V3 | 7.66 | 1.90 | 2.14 | 0.59 | nicht verfügbar | 1.21 |
| Dorf/V4 | 8.74 | 2.20 | 2.28 | 0.72 | nicht verfügbar | 1.38 |
| Blumenwiese/V3 | 7.52 | 1.76 | 2.82 | 0.63 | 0.25 | 1.18 |
| Blumenwiese/V4 | 8.17 | 1.90 | 2.09 | 0.71 | 0.30 | 1.39 |
| Flussufer/V3 | 5.34 | 1.88 | 2.79 | 0.61 | 0.76 | 1.23 |
| Flussufer/V4 | 5.99 | 2.10 | 2.37 | 0.75 | 0.84 | 1.44 |

GPU-Bereiche können sich überschneiden; **nicht zur Gesamtzeit addieren**. Metal lieferte für die ausgewählten RHI-/Basepass-Draw-Call-CSV-Zähler nur0, deshalb sind tatsächliche Draw Calls hier **nicht zuverlässig messbar**, nicht angeblich0. Shader-Instruktionsstatistik war über den vorhandenen Python-Export nicht verfügbar; Materialgraph-Abfragen und Mesh-/Slot-/LOD-Inspektion ersetzen keine gemessene Einzelmaterial-GPU-Zeit. Nanite/LOD/AA/Schattengüte wurden nicht global reduziert.

### Eingrenzung und einzelne Maßnahmen

Die frische Vorher-Diagnose `CostIsolation01` setzte nur in RAM Boden neutral oder blendete ausschließlich zusätzliche V3-Pflanzen aus: Dorf Basepass7,53→7,15ms bei neutralem Boden, Wiese7,62→7,27ms; alle zusätzlichen Pflanzen aus spart in dieser kurzen Diagnose ungefähr0,8–1,0ms Framezeit. Das erklärt nicht pauschal alte größere Verlustangaben und rechtfertigt keine pauschale Ausdünnung. Unattraktiver Neutralboden und kahle Vegetation wurden **nicht übernommen**.

Vorfinale Zusatzdiagnose (noch vor korrigierten Randnormalen/Fernterrain-Vorderseiten, kein endgültiger Standardbenchmark): gepaart nur alter/neuer Boden auf identischer finaler Geometrie, drei Wiederholungen/Standort mit wechselnder Reihenfolge, keine Videos:

| Material/Standort | FPS | GPU ms | Base Pass ms | Frame-p95 ms |
|---|---:|---:|---:|---:|
| V3_Dorf | 22.79 | 28.95 | 9.23 | 82.99 |
| V4_Dorf | 25.91 | 27.72 | 9.72 | 42.94 |
| V3_Wiese | 25.53 | 38.23 | 9.44 | 42.85 |
| V4_Wiese | 25.34 | 38.51 | 9.62 | 42.71 |

Die realen PBR-Texturen verursachen hier einen kleinen zusätzlichen Basepass-Aufwand; die statisch vorab berechnete Maske allein ist **kein nachgewiesener Netto-GPU-Gewinn des neuen gesamten Bodenmaterials**. Ein früher V3_Dorf-Ausreißer verfälscht dessen FPS-Mittel; keine pauschale FPS-Gewinnbehauptung daraus. Beibehalten werden die sichtbare Materialverbesserung, sechs instanzierte Brückengruppen statt verstreuter sichtbarer Einzelteile und eine einzelne Oberfläche je Gewässer. Keine beliebige weitere Pflanzen-/Texturreduktion.

Vorfinaler gepaarter RAM-Szenerievergleich `SceneCostPair02` (vor der abschließenden Normalen-/Flächenkorrektur, daher nur Eingrenzung, keine Performancefreigabe des finalen Standes) (alle gespeicherten statischen V3/V4-Bindungen/Transforms, keine funktionalen Actors, gleiche Renderparameter):

| Szene/Standort | FPS | GPU ms | Base Pass ms | p95 ms |
|---|---:|---:|---:|---:|
| V3_Dorf | 32.98 | 21.41 | 7.59 | 33.70 |
| V4_Dorf | 32.31 | 21.87 | 7.90 | 35.75 |
| V3_Wiese | 30.17 | 32.15 | 8.06 | 37.94 |
| V4_Wiese | 30.39 | 31.94 | 8.12 | 38.83 |

In dieser vorfinalen Zusatzdiagnose betragen die gepaarten GPU-Differenzen Dorf **+0,46ms** und Wiese **−0,21ms** für V4; damit ist kein allgemeiner Netto-Leistungsgewinn nachgewiesen. Der deutlich größere Verlust zwischen den frischen Starts lässt sich daraus nicht vollständig der Mapänderung zuschreiben; eine System-/Messdrift ist möglich, ihre Ursache nicht bewiesen. Diese Zusatzdiagnose rekonstruiert gespeicherte statische Szenerie im RAM des aktuellen Spiels; sie ist kein separat gebooteter vollständiger alter V3-Spielstand. Re-Registrierung statischer Komponenten/Cache-Aufbau und laufende Pokémon bleiben methodische Grenzen. Beide Zustände werden alternierend dreimal je Standort geprüft, jeweils6s-Warm-/6s-Messphase; V4 wird vor Ende wiederhergestellt. Transforms und Instanzzahlen werden geprüft. Werte nicht als Langzeitfreigabe oder sicherer Beleg für thermische Drosselung ausgeben. Der erste Versuch01 scheiterte an editorinternem Billboard und statischer Mobilität, erzeugte keine gültigen Messfenster und wurde regulär über das eigene Spielfenster beendet. Er ist ausdrücklich verworfen, kein bestandener Performance-Test und kein neuer nachgewiesener Engine-Hänger.

**Echter Bewegungslauf:** 2696Frames, 27.60FPS im Mittel, GPU31.20ms, Game2.62ms, Render36.20ms, p9545.18ms,1%-Low16.95FPS, Maximum106.35ms. Ausschließlich der42-Wegpunkte-Lauf vor Screenshots/Menüs/Kampf/Laden, keine Videoaufnahme. Ein vollständiger Lauf, keine mehrstündige oder wiederholt identische Stabilitätsprüfung.

**Stabile30FPS sind nicht nachgewiesen.** Auch durchschnittlich günstige Einzelpunkte reichen dafür nicht; p95/Spitzen und die Verluste der frischen Nachherreihe bleiben offen. Keine eigenmächtige Grafikreduzierung zur Kaschierung. Empfehlungen: längere gegenbalancierte Messreihen unter kontrolliertem Systemzustand, Metal-/Insights-Aufzeichnung für verbleibende Render-/GPU-Wartezeiten und isolierte Materialtests; keine unbelegten weiteren Globalmaßnahmen.

## 9. Technische und Gameplay-Prüfung

| Prüfung | Tatsächlich erreicht |
|---|---|
| Editor-Build | Exit0, bestehendes PokeMonsterEditor Mac Development, keine C++-Änderung |
| Vollständige Automation vor/final | Mehrfach325 bestanden,0mitWarnungen,0fehlgeschlagen/nichtausgeführt/laufend; EngineExit0 |
| Strenger bestehender QA-Exportvertrag | Finaler WrapperExit0; `FullAutomationRelease/Report/index.json` |
| Zwölf vorhandene Map Checks | Alle0Fehler/0Warnungen, nach finaler Nahtkorrektur erneut; keine geschützte Map gespeichert |
| Echter PIE-Rundgang | Bestanden,42Wegpunkte und Gameplayfolge vor der letzten reinen Flächen-/Normalenkorrektur; danach finale21PIE-Ansichten plus erneute unveränderte Kollisionsprüfung |
| Separater Development-Spielprozess | Bestanden, aktive Uhr/KI/Begleiter, echter Rundgang und nachfolgende Interaktionen |
| Brücke | Tour, seitliche Geländerkollision, beidseitig pm.Speed1/2/3, danach Faktor1 |
| Kamera | Bestehende ThirdPersonV3; nativer360°-Orbit in45°-Schritten, Neigung−12°, bestehende Springarmkollision aktiv |
| Gebäude | Cottage tatsächlicher Türdurchgang/Cutaway und zurück; abgesetztes Heilhausinneres betreten/verlassen |
| Kampf/Fang | Natürliche Landbegegnung, ClassicBattle-Attacke/AP-Aktion, normaler MasterBall-Transaktionsweg mit isoliertem Testgegenstand, Team+1 und Rückkehr |
| NPC/Begleiter/Team | Wandererdialog, Steuerung frei; sichtbarer Begleiter, Teamsortierung und Teammenü |
| Save/Load | Taskisolierter Menü-Save/Load innen, exaktes Team/AP/Inventar/Position/Uhr; kein Nutzerslot verwendet |
| Mapwechsel | Echter nativer Wechsel Dev_TestMap und Rückkehr durch normalen Loader zur gespeicherten VisualV2/Team/Position/Kamera/Begleiter |
| Tageszeiten | Echte Gameplayprüfungen/Fotos06/12/19/22; Tageslänge120Minuten und Mittag75° unverändert |
| Lebensräume | ≤14, reale Population in Land- und Wasserzonen, vorhandene KI/Projektion; keine neuen Spawnprofile |
| Modelltestbereiche | NPC-/Pokémon-Konsolenbesuch und genaue Rückkehr in separatem normalen PIE bestanden |
| Controller | Vorhandene Enhanced-Input-Sprintaktion und Bewegung getestet; **kein physischer Gamepadtest behauptet** |
| Stabilität | Mehrere normale PIE-Start-/Stopzyklen/Bilderreihen und normale Prozessenden, kein ForceQuit |

Nachweise: [EditorBuild/Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/EditorBuild/Result.json), [FullAutomationRelease/Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/FullAutomationRelease/Result.json), [MapCheckResults.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/MapCheckResults.json), [PIEGameplay01/Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/PIEGameplay01/Result.json), [NativeGameplay02/Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/NativeGameplay02/Result.json), [TestGroundCommands.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/TestGroundCommands.json). Die Funktionslauf-Gesamt-FPS schließen Fotos/Menüs/Laden ein und sind deshalb nicht als normale Gameplay-Benchmarkwerte verwendet.

Rohlogs sind trotz sauberer Projekt-Testberichte nicht meldungsfrei. Bestehende experimentelle Engine-Toolset-Python-Startfehler, Python-Namenskollision Information/bInformation, TEDS-/Layout-/MCP-Hinweise und vor der Projektqueue auftretende Condition-Meldungen werden separat erfasst: [RawLogReview.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/RawLogReview.json). Die bestehende ClassicBattle-Dekoration kann weiterhin `MI_WLA_LeafOak`-Usagewarnungen erzeugen; Originalmaterial/Kampfsystem wurden dafür nicht verändert. In den geprüften finalen Logs wurden0 iOS-Helfer-/Bad-CPU-Zeilen gefunden; bekannte frühere externe Warnungen sind damit nicht pauschal als behoben erklärt. Im gemeinsamen Editor01-Autorlog stehen auch die verworfenen früheren Shader-Versuche; sie sind keine erneuten finalen PIE-Materialfehler. Fehler des verworfenen Zusatzdiagnoselaufs01 stehen getrennt vom finalen Projekt-QA-Ergebnis.

## 10. Projektschutz, Einschränkungen und Git

Hashprüfung: 6410 vorhandene Arbeitsdateien, 1748 zusätzliche lokale Originalassets und 722 bestehende Save-Dateien; keine unerwartete Änderung/Entfernung. [ProtectionFinal.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/ProtectionFinal.json). Die vorbestehende lokale Änderung in `Config/DefaultEngine.ini` und alle ursprünglichen geschützten unversionierten Nutzerdateien bleiben erhalten und ungestaged. Westland, Biom-Testmap und andere Maps, Grafikprofile, ThirdPersonV3, GaradosV4, Original-Pokémon, Animationen, C++-Gameplay, Quest-/NPC-Systeme und Nutzerspielstände nicht bearbeitet. Vorhandene Backup-Refs erhalten, kein LFS-Prune.

Offen: visuelle Beurteilung durch Harry; die vorhandenen stilisierten Baum-/Grasmodelle bleiben erkennbar, kein fotografischer Realismus behauptet. Fernhügel kaschieren den Rand, sind aber einfache nichtbegehbare Kulisse. Tiefes Garados-Becken setzt der sanften Unterwasserböschung Grenzen. Wasserbewegung ist Materialadvektion, keine physische Strömung. Nicht sämtliche Fotos haben identische absolute Kamerahöhe, weil tatsächlich neue Bodenformen entstanden. Keine abschließende temporale Video-/Langzeitfreigabe, kein stabiler30FPS-Nachweis, mögliche System-/Messdrift und sichtbare Leistungseinbußen bleiben transparent. Kein neuer Download, keine zusätzliche Map/Worktree, keine Weiterarbeit oder Westlandübernahme nach Abschluss.

Git-Sicherung: nur eigene `.gitignore`-Ergänzung, VisualV2, V4-Material-/Mesh-/numerische Quellen, V4-Werkzeuge, Entscheidungseintrag und dieser Bericht. Der tatsächliche Commit sowie Remote-/LFS-Verifikation sind im Abschluss, im Commitverlauf dieses Dokuments und in [GitFinal.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldRefinementV4/GitFinal.json) festgehalten. Keine Messmedien, isolierten Saves, Fab-Texturen oder Nutzerdateien im Commit. Der bestehende V3-Commit bleibt als nachvollziehbarer Wiederherstellungspunkt erhalten.
