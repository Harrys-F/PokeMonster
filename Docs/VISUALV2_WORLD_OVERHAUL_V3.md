# VisualV2 World Overhaul V3 – Prüfbericht

Stand: 03.11.2026. Ausgangscommit `a136a805b8d0bdbea1fdfdf58b8ea301856def50`, bestehendes `main`. Ausschließlich `/Game/Maps/Dev_TestMap_VisualV2` gestaltet. Technische Prüfung abgeschlossen; **die visuelle Abnahme liegt bei Harry**, keine Übernahme nach Westland. Das gelieferte sechsteilige Referenzbild war eine gestalterische Orientierung, keine vorhandene Spielsituation und kein Prüfnachweis.

## 1. Bestand und vollständige Flächenabdeckung

Vor der Bearbeitung wurden sämtliche gespeicherten Actors/Komponenten, sichtbare Meshes samt tatsächlichen Instanzpositionen, Materialien, Geometriegrößen, LODs und Gebäudezugänge aufgenommen: `SceneBefore.json`, `Inventory.json`, `Buildings.json`, `SectionsBefore.json` unter `/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3`. Die Hauptlandschaft ist ein vorhandenes statisches Mesh, **kein Unreal-Landscape-Actor**: X −6000 bis 3000cm, Y −3250 bis 3250cm, ungefähr 90×65m. Das abgesetzte Heilhausinnere liegt außerhalb dieser Hauptfläche und wurde ebenfalls berücksichtigt.

Tatsächlich vorhanden sind Dorf/Heilhaus/Kräutergarten, Cottage, Wiesen, westlicher/nördlicher/östlicher Wald, Waldränder, nördliche Lichtung, fünf hinterlegte Wegzüge, flacher Bach mit kurzer Abzweigung, getrennter tiefer Teich, kleine Hügel/Felsgruppen und die östliche Archivruine. Verborgene frühere Hütten-Proxys wurden nicht zu neuen Gebäuden gemacht. Keine erfundenen Biome, keine neuen Gebäudegrundrisse oder Maps.

Die neun Arbeitsabschnitte decken die ganze Hauptfläche ab. Die folgende Zusatzinstanzzahl bezeichnet unregelmäßig komponierte Bodenvegetation, nicht neun rechteckige Blumenbeete. Bestandsvegetation, Bäume, Kies, Uferpflanzen und Felsgruppen kommen gesondert hinzu. Bereichsgrenzen sind Arbeitskoordinaten, keine sichtbaren Spiellinien.

| Abschnitt | Tatsächlicher Bereich | Grenzen [Xmin,Ymin,Xmax,Ymax] cm | Zusätzliche Bodenpflanzen |
|---|---|---|---:|
| SW | Südwest: Blumenwiese, Cottageumfeld | [-6000, -3250, -3000, -1100] | 338 |
| SC | Südmitte: Startwiese und Teichzugang | [-3000, -3250, 0, -1100] | 235 |
| SE | Südost: Teichrand und Außenwiese | [0, -3250, 3000, -1100] | 289 |
| MW | Westmitte: Heilhaus und Kräutergarten | [-6000, -1100, -3000, 1100] | 320 |
| MC | Mapmitte: Wege, Bachzugang und Hügel | [-3000, -1100, 0, 1100] | 196 |
| ME | Ostmitte: Bach und Archivruine | [0, -1100, 3000, 1100] | 307 |
| NW | Nordwest: Westwald und Waldrand | [-6000, 1100, -3000, 3250] | 292 |
| NC | Nordmitte: Waldweg und Lichtung | [-3000, 1100, 0, 3250] | 265 |
| NE | Nordost: Ostwald und Felsrand | [0, 1100, 3000, 3250] | 301 |

Alle Bereiche wurden aus der normalen Third-Person-Perspektive aufgenommen, nicht nur die bisherigen sechs Vergleichspunkte. Die 21 Ansichten umfassen auch Rück-/Seitenfassaden und gegenüberliegende Brücken-/Teichufer. 30 geprüfte QHD-Bildpaare einschließlich der separaten Benchmarkpositionen stehen in `Analysis.json`.

## 2. Verwendete vorhandene Assets und Originalschutz

Die bestehenden importierten Pakete und `/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary` wurden erneut geprüft. Es gab gegenüber dem letzten lokalen Bestand keine neue nutzbare Komplettbibliothek. Keine Downloads und keine Wiederherstellung des zurückgenommenen Buchenwaldtests. Materialeltern, vorhandene Texturen, Skalierung und tatsächliche Kollisions-/LOD-Eigenschaften wurden vor Verwendung kontrolliert.

| Quelle | Verwendung und Entscheidung |
|---|---|
| Beech Fern / Lady Fern, bereits importierte `SM_FAT_FernA/B` | Bestehende gültige lokale Ableitungen für Unterholz; 1129/195 Dreiecke, je 1 LOD/Material. Nicht die zurückgenommene Waldinstallation. |
| Matted Pratia, `SM_EP2_PratiaA` | Niedrige Uferpolster, 182 Dreiecke/1 Material. |
| Lokale StyleHex-Foliage / `FAT_FabShrubs` | Die 52 bestehenden Strauchinstanzen sind 20% kleiner und weniger grell. Originalinstanzen nicht gelöscht. Eine private Mastermaterialableitung hält die lizenzierten Originale unverändert. |
| `WestlandAssetLibrary` Birch A/B, OakYoung B, FruitTree A | 12 passende zusätzliche Bäume in ungleichen Gruppen, bestehende Baum-LODs erhalten. Beispielsweise Birch A: 28628 Dreiecke, 3 LODs/4 Slots; alte Ancient Oak: 12068 Dreiecke, 3 LODs/2 Slots. Kein Austausch hochwertiger Originalbäume. |
| Eigene bestehende EQ3-Gräser | Short/Meadow/Woodland: 392/518/434 Dreiecke, je 1 Material; verschiedene Höhen und Längen, keine flächige grüne Ersatztextur allein. |
| Eigene `SM_WLA_Wildflowers_A` | 2160 Dreiecke, 3 LODs/5 Slots; sechs eigene Farbvarianten mit Weiß/Creme, Gelb, Blau, Violett, Rot und Rosa. Vorhandene Mohn-/Dorfpflanzen bleiben. |
| Pack Bonus Wooden Floor 2 / Stone 1 | Vorhandene Farb-/Normaltexturen in eigenen Holz-/Steinmaterialien, passend skaliert. Originaltexturen unverändert und lokal. |
| RockEnv Small Rocks, vorhandene SimpleRocks-Kollisionsableitungen | Maßstäbliche Kiesel 4–12cm und sieben teilweise eingebettete größere Felsen 65–125cm; kein wahlloser großmaßstäblicher Steinbelag. |
| Vorhandene `SM_WLA_Crate_A` | Eigene vorhandene 3D-Holzkiste als reine Darstellung des alten Interaktions-Testmarkers. Keine neue Figur oder Modellgeneration. |
| Weitere Vault-Pakete: Forest Floor/Path, Mossy Floor/Rocks/Embankment/Wall, Hydrangea, Bolete, Gräser | Bestehende sinnvolle Verwendungen beibehalten; kein pauschaler Neuimport oder doppelter Aufbau. Unvollständige Megaplants/PVE-Materialeltern weiterhin nicht als verwendbar ausgegeben. |

Neue Gruppen werden als HISM angelegt, mit 60–80m Ausblendbereich. Niedrige Pflanzen/Kiesel erhalten keine zusätzlichen dynamischen Schatten oder Blockkollisionen; Bäume und große Felsen behalten sinnvolle Schatten. Zwölf separat unsichtbare Stammkollisionen stehen außerhalb der freigehaltenen Wege. Vorhandene LODs und globale Renderqualität wurden nicht reduziert. Keine isolierte Shaderkostenmessung je Pflanzenart durchgeführt; die reale Gesamtlast ist unten gemessen. Die gemessenen Mehrkosten der Überarbeitung werden ausdrücklich akzeptanzoffen ausgewiesen, nicht durch eine Qualitätsreduktion kaschiert.

**Öffentliches Repository:** Fab-Originale bleiben lokal/ignoriert. Auch die aus dem StyleHex-Master abgeleitete `Content/Environment/VisualV2WorldOverhaulV3/Materials/M_WOV_ShrubMaster.uasset` bleibt explizit lokal ignoriert. Eigene Parameterinstanzen referenzieren sie. Keine lizenzierten Rohtexturen/Modelle/Mastergraphen werden öffentlich gepusht. Das Projekt benötigt auf einem neuen Rechner weiterhin die rechtmäßig bezogenen lokalen Fab-Pakete. Kein portables Komplettassetpaket behauptet.

## 3. Boden, Wege und Gelände

`/Game/Environment/VisualV2WorldOverhaulV3` enthält eigene map-spezifische Ableitungen. `SM_WOV_Ground` hat dieselbe Grundtopologie wie das vorhandene geschlossene `SM_FAT_StreamGround` (48658 Dreiecke), mit neu berechneten Normalen und komplexer Bodenkollision. Bachbett, tiefer Teich und äußere Ausdehnung bleiben erhalten.

Die früheren sichtbaren Boxstufen `Hill_Step_Low`, `Hill_Step_Mid`, `Hill_Lookout` werden durch die kontinuierliche Geländeoberfläche ersetzt; nur diese drei alten Oberflächen/Kollisionen sind ausgeblendet/deaktiviert. Die Höhen betragen 20/40/60cm in der mittleren Hügelgruppe und 42/65/38cm an drei äußeren Stellen, bei weichen Radien von 3,5–4,5m. Es handelt sich um kleine natürliche Bodenformen, nicht neue Bergregionen. Betroffener vorhandener Bewuchs wurde einmalig auf die neue Bodenhöhe gesetzt.

`M_WOV_Ground` unterscheidet Wiese, Waldboden, Erde, steinige Stellen und feuchte Ufer per zusammenhängenden Weltkoordinatenmasken und Farbvariation. Die frühere Beschränkung auf sechs Farbinseln entfällt. Die fünf tatsächlichen Wegverläufe sind erhalten und direkt in die einzige Geländeoberfläche integriert. Da kein Landscape existiert, wurden keine künstlichen Landscape-Paint-Layer oder zusätzliche Wegplatten vorgetäuscht.

Eigenes `M_WOV_Cobbles` verfeinert die vorhandenen Vorplatz-/Zugangselemente, mit kleineren warmen, versetzten und abgerundeten Pflasterformen statt des ersten zu hellen Rasters. 15 durch Pflaster/Eingang wachsende bestehende Dekorinstanzen wurden gezielt entfernt. Normale Wege bleiben frei; Kies und Gräser sitzen unregelmäßig an Rändern. Keine neuen übereinanderliegenden normalen Wegmeshes.

## 4. Wiesen, Wälder und Lebensräume

Die neun Bereiche erhielten insgesamt 2643 zusätzliche Bodenpflanzen, mit räumlichen Gruppen, Lücken, unterschiedlichen Höhen und sechs Blütenfarben. Mit Bäumen, Stammkollisionen, Ufer-/Wegkies und Felsen sind es 3030 neue Instanzen in 28 HISM-Gruppen; darin enthalten sind 12 unsichtbare Kollisionsinstanzen, also nicht ebenso viele sichtbare Dekorationen. Insgesamt 36 neue eigene Map-Actors einschließlich der Brückenteile.

Neue Baumgruppen stehen mit großzügigen Wegabständen, Unterholz ist niedrig. Farne konzentrieren sich auf tatsächliche Wälder, Blumen auf Wiesen/Lichtungen, kurze Pflanzen an Säumen. Große uneingeschränkte Strauchflächen wurden nicht über die Wege gelegt. Die bisherige Waldkamera wurde nicht übernommen; Kamera V3 bleibt 1,72m über ebenem Boden, −12°, 3,50m Abstand und horizontale Drehung.

**Pokémon:** Keine zweite KI, keine neuen Arten oder Modelle, keine Änderungen an Spawnlimit, Häufigkeiten, Lebensraumregeln, Tagesprofilen oder Kampf/Fang. Sichtkorridore und niedriger Bewuchs verbessern die Einbettung vorhandener Tiere, ohne sie zur Sammlung aller Arten zu machen. Im endgültigen nativen Lauf wurden Bisasam, Enton, Garados, Habitak, Karpador, Pikachu, Raupy beobachtet; Population maximal 14 bei globalem Limit 14. Die Verhaltensprotokolle enthalten Wandern, Ruhe/Idle, Schlaf, Nahrungssuche, Beobachten, neugierige Annäherung, Sozial-/Gruppenverhalten und Kampfunterbrechung, soweit tatsächlich im jeweiligen Lauf aufgetreten. Kein besonderes Gras-Fress-Rig oder neue Spezialanimation behauptet. Garados V4 und sämtliche Pokémon-Quellen/Animationen bleiben unverändert.

## 5. Gebäude, Dorf, Zäune und Brücke

261 architektonische Materialzuordnungen wurden lokal überarbeitet: 215 Heilhaus, 29 Cottage, 5 Dorfdetails, 5 Zaungruppen, 4 Archivruine, 3 Gartengruppen. Eigene Materialien `M_WOV_Timber`, `Stone`, `Plaster`, `Roof`, `Cobbles` vereinheitlichen warmes Holz, Stein, Putz und erdige Dachflächen. Texturmaßstab und zurückhaltende Normaldetails verbessern die Oberflächen. Vorhandene hochwertige Gebäude-Meshes, Grundrisse, Fenster-/Türöffnungen, Fundamente, Treppen, Eingangstrigger und Innenraumtechnik sind erhalten. Garten, Fässer/Kisten, Fensterpflanzen, Laternen und logisch verbundene Zäune wurden im Zusammenhang kontrolliert, nicht durch zufällig verstreute neue Objekte ersetzt.

Der graue Würfel hinter dem Cottage war **kein Gebäudefehler**, sondern `Dev_InteractionMarker_Separat`. Seine originale Root-Kollision, Transform und Interaktionsklasse bleiben bestehen. Nur die Würfeldarstellung ist unsichtbar, eine vorhandene 3D-Kiste ist als sichtbare, kollisionslose Kindkomponente angehängt. Der ursprüngliche Interaktionszähler und Lichtschalter wurden über echte Spielerinteraktion geprüft. Kein neuer Collider und keine doppelt sichtbare Würfelfläche.

Die Holzbrücke wurde konstruktiv vervollständigt: ursprüngliche Spannweite 210cm, etwa 170cm Deckbreite, sichtbare Deckoberkante 24cm, Wasseroberfläche 4,4cm; Abstand Deckoberkante–Wasser 19,6cm. Die vorhandene exakte Deckkollision bleibt. Ihr zuvor zusätzlich gerenderter Quader ist nun unsichtbar. Zehn Bretter liegen bündig auf der begehbaren Höhe, Endpfosten stecken bis −8cm im Ufer, mittlere Pfosten beginnen auf dem Deck. Zwei Längsträger, vier Diagonalstreben und zwei korrekt zum Deck ansteigende Rampen ergänzen die vorhandenen Geländer. Keine schwebenden Endpfosten und keine frei endenden neuen Streben. Fußlauf über beide Rampen/Deck sowie tatsächliche seitliche Geländerkollision sind bestanden.

## 6. Wasser und Ufer

Die vorhandenen einzelnen Bach-/Teichoberflächen, Ufermasken und Tiefen bleiben unverändert: flacher Bach, getrennter ungefähr 4,2m tiefer Teich, keine doppelte Wasserfläche oder neue Verbindung. Ganze Bachufer und Teichumfang erhalten kleine maßstäbliche Steine und niedrige Pratia-Pflanzen, ohne eine Steinmauer zu bilden oder den Brückenzugang zu blockieren.

`M_WOV_Stream` behält Single Layer Water; `M_WOV_Pond` behält die bestehende transparente beleuchtete Darstellung. Eigene zeitabhängige Normalen und reduzierte, unregelmäßigere Lichtreflexe ersetzen die erste zu deutlich gestreifte Wellenwirkung. Bachbewegung orientiert sich am vorhandenen Ost-West-Verlauf. Keine physikalische Strömungssimulation, kein neues Unterwassersystem und keine Änderung der Wasser-Pokémon-Steuerung. Reflexionen und Tiefe bleiben stilisiert; keine fotorealistische Wasserfreigabe behauptet.

## 7. Gefundene Altprobleme und gezielte Korrekturen

- Die senkrechte grüne Wand im Westwald war die Begrenzung des **zur Laufzeit in PIE erzeugten NPC-Testgeländes**. Das wurde durch echten Vergleich mit neutralem Hauptbodenmaterial und durch die tatsächlichen Laufzeitbounds belegt: alter Testboden X −10000…−5000/Y1100…4900, Begrenzung bei X−5010; er überlappte einen Teil der Hauptlandschaft. Keine unbelegte Lichtdiagnose.
- Der dünne schwebende Balken am Teichhorizont war ein Rand des separaten Pokémon-Modelltestgeländes. Beide Testflächen bleiben vorhanden, aber außerhalb und unterhalb der normalen Welt: NPC-Mitte `(-20000,3000,-20000)`, Pokémon-Mitte `(-7500,-20000,-20000)` cm. Die vorhandene Kill-Z-Grenze bleibt −1048575cm. Nur die bestehenden Center-Konstanten und der entsprechende NPC-Besuchs-Bodenhöhenoffset wurden angepasst. Keine neue Map/Architektur, keine Änderungen an NPC-/Pokémon-Modellen oder ihrer KI.
- `pm.NPCGround.Go 1` / `pm.NPCGround.Return` und `pm.TestGround.Go 1` / `pm.TestGround.Return` sind erhalten und real geprüft, mit stabilem Bodenkontakt und exakter Rückkehr. Die NPC-RAM-Vorschau wird separat getestet, weil sie absichtlich keinen gleichzeitigen isolierten Disk-Save-Testslot zulässt. Die Testskripte respektieren das vorhandene Schutzsystem.
- Fehlende Instancing-Usage-Freigaben an Bibliotheksmaterialien wurden anhand der frischen Game-Logs gefunden. Eigene Birch/LeafBirch/Timber/LeafOak/Apple-Materialinstanzen nutzen das in UE5.8 vorhandene `SetMaterialUsageOverride`/`UpdateMaterialInstance`. Alle VisualV2-Zuordnungen liegen in eigenen Instanzen; Bibliotheksdateien bleiben unverändert. Kein Ersatzmaterial als gültiges Endergebnis akzeptiert.
- Bereits vor Beginn gab es keine sichtbaren reinen Dekor-PaperSpriteActors. Verborgene alte funktionale Sprites wurden erhalten, nicht fälschlich als neu entfernte Platzhalter gezählt.

## 8. Reale Bildvergleiche

Alle Originalbilder: 2560×1440, High/Profil C, 75%, Mittag 12:00/Sonne75°, normale Third-Person-Kamera. Nur echte Unreal-Aufnahmen; `Compare.swift` ordnet diese proportional an und beschriftet sie, keine Bildgenerierung oder Retusche. Die Kamera-/Spielertransforms und Auflösung sind in `Analysis.json` geprüft. Beim Steinplateau folgt die Kamera dem neu geformten Boden; dieser vertikale Unterschied ist ausdrücklich ausgewiesen, keine falsche identische Kamera behauptet. Wasserwellen und lebende Tiere sind nicht pixelidentisch eingefroren.

[Gesamtübersicht aller 21 Endansichten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/WholeMapContactSheet.png).

| Ansicht | Original vorher | Endstand | Nebeneinander |
|---|---|---|---|
| HeilhausFront | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/HeilhausFront.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/HeilhausFront.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/HeilhausFront.png) |
| HeilhausRueck | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/HeilhausRueck.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/HeilhausRueck.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/HeilhausRueck.png) |
| HeilhausNord | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/HeilhausNord.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/HeilhausNord.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/HeilhausNord.png) |
| CottageFront | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/CottageFront.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/CottageFront.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/CottageFront.png) |
| CottageRueck | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/CottageRueck.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/CottageRueck.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/CottageRueck.png) |
| Startwiese | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Startwiese.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Startwiese.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Startwiese.png) |
| Suedwiese | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Suedwiese.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Suedwiese.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Suedwiese.png) |
| Westwald | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Westwald.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Westwald.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Westwald.png) |
| Nordwald | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Nordwald.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Nordwald.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Nordwald.png) |
| Ostwald | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Ostwald.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Ostwald.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Ostwald.png) |
| Nordlichtung | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Nordlichtung.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Nordlichtung.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Nordlichtung.png) |
| Steinplateau | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Steinplateau.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Steinplateau.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Steinplateau.png) |
| Ruine | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Ruine.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Ruine.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Ruine.png) |
| BachWest | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/BachWest.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/BachWest.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/BachWest.png) |
| BachOst | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/BachOst.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/BachOst.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/BachOst.png) |
| BrueckeSued | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/BrueckeSued.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/BrueckeSued.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/BrueckeSued.png) |
| BrueckeNord | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/BrueckeNord.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/BrueckeNord.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/BrueckeNord.png) |
| TeichNord | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/TeichNord.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/TeichNord.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/TeichNord.png) |
| TeichSued | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/TeichSued.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/TeichSued.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/TeichSued.png) |
| Ostwiese | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Ostwiese.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Ostwiese.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Ostwiese.png) |
| Garten | [Vorher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/BeforeAtlas/Garten.png) | [Nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/AfterAtlas03/Garten.png) | [Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/Comparisons/Garten.png) |

Zusätzlich enthalten die endgültigen Gameplay-Ordner echte Aufnahmen beider Innenräume, des Teams und der Tageszeiten 06/12/19/22 Uhr. Die vorhandene Sonnenbahn/120-Minuten-Weltuhr wurde nicht geändert.

## 9. FPS und GPU/CPU – tatsächlich gemessen

Hardware/Engine laut neuem Prozesslog: Apple M4, 16GB gemeinsamer Speicher, macOS27.2 Build26B123, Unreal **5.8.4 CL58902052**, Metal. Das ist die tatsächlich installierte UE5.8-Version. Keine Hardwaredaten geschätzt.

2560×1440 Ausgabe, Profil C/75% (nominal1920×1080 intern), High/alle Scalability-Gruppen2, Software-Lumen+IFG (`r.Lumen.HardwareRayTracing=0`, `r.Lumen.FinalGatherMethod=0`), VSM1/4 Strahlen, Sonne75°, TAAU. Globales `r.AntiAliasingMethod=4` ist kein Beleg für tatsächlich aktives TSR: der unveränderte `PokeMonsterTemporalAABlendable` setzt in der Spielansicht TemporalAA/TemporalUpscale; `r.TemporalAA.Upsampling=1`. Keine Grafik-/Rendering-Konfiguration verändert. `r.VSync=0`, `t.MaxFPS=0` und GPU-CSV-Aufzeichnung gelten nur vorübergehend im Messprozess und werden vor regulärem Prozessende zurückgesetzt.

`NativeBefore01` gegen **`NativeAfter02`**, getrennte frische Development-Spielprozesse, keine Videoaufnahme. Drei CSV-Messfenster à6s nach je4s Beruhigung pro Hauptpunkt, zusätzliche Detailpunkte einmalig. Fotos entstehen erst nach den jeweiligen Messfenstern. Tabellenwerte werden aus Unreal-CSV-Countern berechnet; p95 aus zusammengeführten gültigen Frames der jeweiligen Position, keine geschätzten Einzelkosten.

| Messpunkt | FPS vorher | FPS nachher | GPU vorher ms | GPU nachher ms | Frame-p95 danach ms | Game Thread danach ms | Render Thread danach ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| Blumenwiese | 31.96 | 25.66 | 30.01 | 38.01 | 43.20 | 1.71 | 38.97 |
| Waldrand | 36.17 | 29.01 | 26.30 | 33.53 | 37.24 | 1.79 | 34.46 |
| Flussufer | 34.88 | 27.02 | 27.35 | 36.23 | 44.57 | 2.04 | 37.02 |
| Felsen | 41.66 | 32.87 | 22.43 | 18.77 | 32.45 | 2.18 | 30.40 |
| Dorf | 32.36 | 27.40 | 21.65 | 26.51 | 39.42 | 1.71 | 36.48 |
| Lebensraum | 41.21 | 31.79 | 22.68 | 30.57 | 33.14 | 2.12 | 31.45 |
| Kraeutergarten | 33.43 | 28.43 | 20.86 | 25.19 | 37.48 | 1.66 | 35.17 |
| Bachbett | 36.79 | 30.09 | 25.78 | 32.40 | 35.78 | 1.82 | 33.23 |
| Felsgruppe | 42.80 | 33.55 | 21.89 | 28.82 | 31.51 | 2.29 | 29.75 |

Die Gesamtänderung umfasst neue Materialien, Bewuchs, Terrain und entfernte überlappende Testdarstellung. Es sind keine isoliert gemessenen Kosten jeder einzelnen Gestaltung. Messfenster schwanken, die beiden Serien liegen zeitlich auseinander; thermische Drift ist nicht separat isoliert. Deshalb kleine Unterschiede nicht als gesicherte Einzeloptimierung interpretieren. Die p95-/1%-Low-Werte und verfügbaren Pass-Counter (BasePass, Schatten, Wasser, IFG, TAA) sind vollständig in `Analysis.json`, überlappende GPU-Bereiche werden nicht addiert. Der Zwischenlauf `NativeAfter01` enthielt noch die Material-Usage-Warnungen und dient **nicht** als Endmessung.

**Bewegtes Gameplay:** Der erste ununterbrochene 42-Wegpunkte-Rundgang im endgültigen nativen Prozess wurde separat als CSV gemessen, vor Fotos, Dialogen, Kampf, Testgeländebesuchen und Save/Load. Uhr/Beleuchtung, KI, Begleiter und Kamera laufen dabei normal. 3435 gültige Frames, **35.17 FPS durchschnittlich**, GPU 24.16ms, Game Thread 2.38ms, Render Thread 28.41ms, Frame-p95 **37.25ms**, 1%-Low 20.74FPS, größter Frame 134.71ms. Ein realer vollständiger Durchlauf; keine mehrstündige Stabilitätszusage oder gepaarte dynamische Vorher-Messreihe.

**Stabile 30FPS werden nicht als nachgewiesen ausgegeben.** Ein Durchschnitt um/über30FPS ersetzt keine p95-/Spitzenbewertung. Etwaige Verluste sind in der Tabelle sichtbar; keine eigenmächtige Grafikreduktion, kein Abschalten von Lumen/VSM/Tag-Nacht und keine Bildverdopplung. Die Funktionslauf-Gesamt-FPS enthalten zusätzlich Screenshots, Menüs und Laden und werden nicht als reine Benchmarkwerte verwendet.

## 10. Technische und Gameplay-Prüfungen

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Finaler Editor-Build | Exit0, `/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/EditorBuildFinal/Console.log` |
| Vollständige relevante Automation | 325 bestanden,0 mit Warnungen,0 fehlgeschlagen,0 nicht ausgeführt,0 laufend; Engine-Exit0 |
| Strenger QA-Exportvertrag | Wrapper-Exit0; `/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2WorldOverhaulV3/FullAutomationFinal/Report/index.json`. Kein Exit1 als bestanden ausgegeben. |
| Zwölf Map Checks auf finalem Stand | Alle zwölf vorhandenen Maps0Fehler/0Warnungen, nur gelesen; `MapCheckResults.json` |
| Echte PIE-Regression | `PIEGameplay05/Result.json`: bestanden |
| Separater Gameplayprozess | `NativeGameplay02/Result.json`: bestanden, reguläres Prozessende0 |
| Gesamte hinterlegte Wegstruktur | Alle fünf Wegzüge über42Wegpunkte mit echter Enhanced-Input-Bewegung, keine Positionssprünge innerhalb dieses Rundgangs; zusätzliche echte Gebäudeein-/austritte |
| Brücke | Rampen/Decküberquerung und tatsächlicher seitlicher Geländeranschlag bestanden |
| Gebäude | Cottage-Tür/Cutaway/In-place-Innenraum und Heilhaus-Tür/abgesetzter Innenraum/Rückweg/Kamera bestanden |
| Steuerung/Kamera | Kamerabezogene Bewegung und Sprint über vorhandene InputActions; unveränderte Third-Person-Einstellungen. Kein physischer Gamepadtest behauptet. |
| NPC/Interaktion | Ursprünglicher Wandererdialog, Rückgabe der Steuerung; neue Kistendarstellung mit ursprünglichem Interaktionszähler/Lichttoggle bestanden |
| Pokémon/Kampf/Fang | Echte Habitatkreatur, ClassicBattle-Attacke/AP, reguläre MasterBall-Transaktion in isolierter Testumgebung, eindeutige zusätzliche Teaminstanz und Rückkehr bestanden |
| Team/Begleiter | Sichtbarer regulärer Testbegleiter, Teamsortierung, Teammenü und Begleiter nach Laden/Reise bestanden |
| Save/Load | Ausschließlich eigene isolierte Testslots/UserDir; normales Speichern/Laden im Heilhaus erhält exakte Position, Team/AP, Inventar und Weltzeit |
| Mapwechsel | Tatsächliches OpenLevel nach `Dev_TestMap`, normales Laden zurück zu gespeicherter VisualV2/Position/Team/Begleiter; keine andere Map gespeichert |
| Tageszeiten | 06/12/19/22Uhr tatsächlich geprüft/aufgenommen; 120min/Tag, Mittag75° und bestehende Renderingwerte unverändert |
| Modelltestgelände | Beide alten Konsolenbefehle/Bodenkontakt/Rückkehr bestanden; getrennte normale PIE-RAM-Prüfung, keine Änderung von Modellen/Animationen |
| Stabilität | Mehrere normale PIE-Start-/Stopp-Zyklen und regulär geschlossene eigene Editoren; kein Force Quit oder Projektabsturz beobachtet |

Zwischenprüfungen sind erhalten: Die ersten erweiterten Testskripte scheiterten an einer nach dem langen Rundgang nicht aktualisierten Interaktionsblickrichtung, einem nicht in Python exponierten Hilfsaufruf, der absichtlich unzulässigen Mischung von NPC-RAM-Vorschau und isoliertem Disk-Testslot sowie einem vor dem eigentlichen Besuch zu früh erfassten Rückkehranker. Diese **Testfixturefehler** wurden korrigiert und erfolgreich wiederholt; keine Save-/Interaktionsarchitektur dafür umgebaut. Zwischenbilder deckten den Horizontbalken, den alten Würfel und Material-Usage-Probleme auf; erst der korrigierte Endstand gilt als Lieferstand.

## 11. Warnungen und verbleibende Einschränkungen

Die exportierte Projekt-Automation und ihr strenger Wrapper sind bestanden. Das heißt **nicht**, dass der komplette Engine-Rohlog frei von Meldungen ist. Wie in der Vorher-Basis erscheinen experimentelle Engine-Toolset-Python-Startfehler (AnimationAssistantToolset/zugehörige Initialisierungen), die bestehende Python-Namenskollision `Information/bInformation`, TEDS-/Layout-/MCP-Hinweise sowie17 `LogAutomationTest: Condition failed` vor Beginn der Projekt-Testqueue. Sie sind separat dokumentiert, nicht als325 fehlgeschlagene Projekttests oder als behobene Projektfehler ausgegeben. Quellen: `RawLogReview.json` und die vollständigen Logs. Im endgültigen VisualV2-Benchmark gibt es keine fehlende Material-Usage-Freigabe mehr. Im nativen Kampftest bleibt eine Warnung der vorhandenen ClassicBattle-Dekoration mit `MI_WLA_LeafOak` unmittelbar nach Kampfstart bestehen. Die unveränderte ClassicBattle-Klasse lädt diese Originalinstanz weiterhin; sie ist keine neue V3-Baumbindung. Kampf und Fang sind funktional bestanden, diese bestehende Materialwarnung ist ausdrücklich offen. Das geschützte Kampf-/Bibliotheksmaterial wurde dafür nicht global verändert.

Die bekannte externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` wurde in den hier ausgewerteten neuen Logs nicht beobachtet; keine iOS-/Engine-Installation oder Rosetta-Konfiguration verändert.

Offen für Harrys visuelle Beurteilung: vorhandene stilisierte Bäume/teilweise schlichte Rückfassaden, Testmapränder ohne neue Fernlandschaft, weiterhin stilisiertes Wasser statt physischer Strömung, subjektive Vegetationsdichte und Farbigkeit. Das Referenzbild ist nicht pixelgetreu nachgebaut, keine identische fotografische Qualität behauptet. Kleine entfernte Pokémon können weiterhin Vegetation überlagern; keine neue Kameralogik oder Modelländerung zur Kaschierung. Keine abschließende temporale Video-/Langzeitleistungsfreigabe und kein nachgewiesenes stabiles30FPS-Ziel. Keine neuen Aufgaben nach Abschluss automatisch beginnen.

## 12. Schutzprüfung und Git-Umfang

SHA256 gegen den Taskbeginn: 6359 ursprünglich versionierte/unversionierte Arbeitsdateien geprüft, nur die explizit erlaubten eigenen Änderungen; 1747 zusätzliche lokale Original-/Fab-Assets **unverändert**; alle 715 vorbestehenden `.sav`-Dateien **unverändert**. Keine fehlenden Dateien. Beide Vollbackup-Refs bleiben exakt `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Geschützte Maps, Pokémon-/Blenderquellen, Renderingprofile und Nutzerdateien wurden nicht verändert.

Der schon vorher vorhandene lokale Unterschied in `Config/DefaultEngine.ini` bleibt bytegleich und wird nicht gestaged. Die34 ursprünglichen unversionierten Dateien bleiben erhalten und außerhalb des Commits. Eigene Assets liegen nur unter `/Game/Environment/VisualV2WorldOverhaulV3`; die eine lizenzabhängige Masterableitung bleibt wie beschrieben lokal. Keine neuen Maps, Worktrees, Projektkopien, Vollbackups oder destruktiven Git-Befehle.

Geplanter Git-Umfang nach der Prüfung: Zielmap, eigene zulässige Ableitungen/Parameterinstanzen, Werkzeuge, dieser Bericht, gezielte Entscheidungsergänzung, lokale Fab-Master-Ignore-Regel sowie ausschließlich Testgelände-Position/Bodenhöhenbezug und passende bestehende Testassertionen. Keine Gameplay-Klassenänderungen an Kampf, Fang, Save, KI, Kamera oder Eingabe. Der Commit wird nach dieser Prüfung erstellt; seine Identität und tatsächliche Remote-/LFS-Verifikation stehen im abschließenden Chat und in `GitFinal.json`/`RemoteLFS.json` unter Saved. Kein zukünftiges Testergebnis vorweggenommen.
