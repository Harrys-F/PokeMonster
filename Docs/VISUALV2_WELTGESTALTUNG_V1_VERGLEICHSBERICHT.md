# VisualV2 Weltgestaltung V1 – Vergleich und Integrationsplan

Stand: 19.10.2026. **Nur Bestandsaufnahme und Planung. Keine Map oder Grafikasset geändert. Keine neue künstlerische Freigabe erteilt.**

## 1. Ergebnis

**Die wichtigste neuere Weltgestaltung liegt bereits in der zentralen VisualV2.** Heilhaus V4, die V5-Muster mit der V6-Gruppierung sowie die V7-Ausweitung von Boden, Wegen und Ufersäumen sind tatsächlich angebunden. Ein erneutes Kopieren aus älteren Testkarten würde diesen Stand teilweise zurücksetzen oder Details doppelt platzieren.

**Keine eindeutig freigegebene, noch fehlende vollständige Boden-, Gras-, Weg- oder Uferlösung gefunden.** Interessante zusätzliche Formen und Kompositionen existieren, besitzen aber keine nachgewiesene Freigabe als bessere VisualV2-Gestaltung. Das ist keine Aussage, dass außerhalb dieser Untersuchung keinerlei nutzbares Einzelasset existiert.

Empfohlener erster Schritt nach Harrys Freigabe: den **bereits integrierten V7-Stand visuell abnehmen**, daraus konkrete örtliche Korrekturen ableiten und erst danach ausgewählte zusätzliche Bestandsassets einsetzen. Keine pauschale Map-, Material- oder Vegetationsübertragung.

## 2. Tatsächlich geprüfter Stand und Methode

- Einziger Arbeitsort: `/Users/harry/Developer/PokeMonster`; Unreal-Projekt direkt darin: `PokeMonster.uproject`.
- Branch `main`, Ausgangs-HEAD und direkt abgefragtes GitHub-`origin/main`: `9b885388bd966474dc7608e0c173e67e87270c26`.
- Vor Beginn keine versionierten oder vorgemerkten Änderungen, **49 bestehende unversionierte Dateien**. Diese Dateien sind nicht Teil dieses Arbeitspakets.
- Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` unter Branch-/Archivref erhalten; keine Historyänderung oder LFS-Bereinigung.
- AGENTS, GRAFIKSTIL, relevante TECHNIK-/ENTSCHEIDUNGEN-Abschnitte, Spielidee/-regeln und die einschlägigen Art-/Testberichte gelesen. Frühere Freigabegrenzen anhand späterer ausdrücklicher Entscheidungen eingeordnet.
- **Alle 17 vorhandenen Maps frisch in einer eigenen grafischen Unreal-5.8.2-Editorsitzung geladen**, Actors, Mesh-/Materialbindungen, Instanzzahlen, Licht-/Postprocess-Eigenschaften und direkte Asset-Registry-Abhängigkeiten gelesen. Vorher keine fremde Editorsitzung offen. Keine Save-Funktion, kein PIE, kein Reimport und keine Änderung eines Pakets.
- Map Check für alle 17 Maps: **jeweils 0 Fehler / 0 Warnungen**. Am Schluss keine Dirty-Map-/Contentpakete; Editor regulär beendet (Exit 0).
- Sämtliche **3.564 zuvor vorhandenen versionierten und nicht ignorierten unversionierten Dateien** per SHA-256 nach der Untersuchung identisch, darunter alle 17 Mapdateien. Ignorierte Engine-Caches/-Logs sind davon getrennt.
- Visuelle Bewertung durch tatsächlich geöffnete, vorhandene Unreal-Aufnahmen von Heilhaus V4, V7-Ostwald, Südwiese und Ufer, WestlandVillage, WestlandRegion sowie V3-AssetLibrary. **Historische Aufnahmen, keine heute neu gerenderten Vorher-/Nachher-Paare.** Unterschiedliche Kamerastandorte, Aufnahmezeiten und Qualitätsstufen erlauben einen gestalterischen Vergleich, keinen fairen Helligkeits- oder Performance-A/B-Nachweis.

Die Inventarzahlen umfassen gespeicherte Komponenten/Instanzen einschließlich erhaltener verborgener Altobjekte; sie sind **keine pro Frame sichtbaren Instanzen, Draw Calls oder GPU-Kosten**. Actorzahlen enthalten auch editorseitige Verwaltungsakteure und sind deshalb etwas höher als die früheren reinen Szenensignaturen (VisualV2 heute 1.401 statt V7-Bericht 1.397).

Lokale Rohprüfung, nicht zur Versionierung vorgesehen: `Saved/WorldDesignV1_Audit.json`, `WorldDesignV1_Engine.log`, `WorldDesignV1_Result.json`, `WorldDesignV1_Validation.json` und `WorldDesignV1_Baseline.json`.

Der früher erwähnte `Docs/ZENTRALE_REFERENZMAP_V1_PRUEFBERICHT.md` ist im aktiven Projekt **nicht vorhanden**. Er wurde nicht als gelesene Quelle oder Freigabenachweis ausgegeben. Der Regionsstand wurde anhand der aktuellen Map, ihrer Autorenquellen und vorhandener lokaler Nachweise geprüft.

## 3. Vergleich der vorhandenen Karten

Alle genannten Maps liegen tatsächlich unter `/Game/Maps/`; die Dateien unter `/Users/harry/Developer/PokeMonster/Content/Maps/`. Keine Namensähnlichkeit als Beweis gleicher Inhalte verwendet.

| Map | Geladene Actors | Zweck, Zustand und Nutzen |
|---|---:|---|
| `Dev_TestMap_VisualV2` | 1401 | Zentrale Referenz; V4-Heilhaus, V6-Stil/V7-Ausweitung bereits integriert; V7-Abnahme offen. |
| `Dev_WestlandRegion` | 3094 | Große Region (Autorenplan 800 × 600 m), Terrain, regionales Wegnetz, Fluss, Mühle und Brücken. Kompositions-/Technikreferenz, kein pauschaler Art-Ersatz. |
| `Dev_WestlandVillage` | 1536 | Früher Dorfkern, fünf begehbare Kitgebäude, sieben Wegbänder, 605 PaperSpriteActor. Gebäude-/Wegekomposition als Anregung; Oberflächen älter. |
| `Dev_WestlandAssetLibrary` | 85 | Einzelasset-Review V1/V2/V3; keine fertig komponierte Welt. Drei V3-Heldenmodelle bereits in VisualV2. |
| `Dev_HealingHouseTestMap` | 546 | Expanded Interior / Quality V3 / NaturalGroundV1; weitgehend bereits nach VisualV2 übernommen und dort außen durch V4 ergänzt. |
| `Dev_BuildingKitTestMap` | 420 | Architekturmodule und Cutaway-Referenz; keine bessere Boden-/Uferausarbeitung. |
| `Dev_TestMap` | 631 | Historischer Gameplaykern mit älterer Darstellung; kein Grafik-Upgrade. |
| `Dev_BattleTestMap` | 8 | Isolierte Kampfprüfung; keine relevante Landschaftsvariante. |
| `Dev_TestMap_NPCMotionV2` | 1354 | Ranger-Bewegungs-/Rigexperiment; älterer Landschaftsstand, keine Weltartquelle. |
| `Dev_TestMap_NPCMotionV3` | 1356 | Korrigierte Ranger-Beinmechanik; finale NPC-Freigabe laut Bericht offen. Nicht mit Landschaftsübernahme vermischen. |
| `Dev_TestMap_RangerPerfV2` | 1352 | Geometrie-/LOD-Kandidaten; keine automatische Art-/NPC-Freigabe. |
| `Dev_TestMap_EnvironmentPerfV1` | 1353 | Isolierte Render-/Postprocess-Versuche; keine neuere Landschaftsgestaltung. |
| `Dev_TestMap_EnvironmentPerfV2` | 1354 | Alternative Lumen-Auswertung; Helligkeits-/Kontaktabweichungen dokumentiert. |
| `Dev_TestMap_EnvironmentPerfV3` | 1355 | Erneute Vegetations-/Lumenprüfung; keine belastbare neue Optimierung zur Übernahme empfohlen. |
| `Dev_TestMap_TreeShadowProxyV1` | 1358 | Begrenzter Schattenproxy-Versuch, keine allgemeine Freigabe. |
| `Dev_TestMap_VisualV2GPUBottleneckV1` | 1352 | Diagnosebasis für Render-/AA-/Vegetationsvergleiche; ältere Landschaft als aktuelle VisualV2. |
| `Dev_TestMap_VisualV2EnvironmentQualityV1` | 1352 | Bereits vorhandene unversionierte fremde Testmap; nur lesend untersucht, keine Übernahme oder Versionierung. |

Die Performance-/NPC-Karten enthalten den älteren Weltstand. Ihre höhere Versionsnummer bezeichnet den jeweiligen Versuch, keine jüngere oder bessere Landschaft. EnvironmentPerf-Einstellungen und alternative Schatten werden nicht mitübernommen.

## 4. Was in VisualV2 bereits tatsächlich vorhanden ist

### Boden und fünf Wegfamilien

| Actorlabel | Aktuelle Materialbindung |
|---|---|
| `V2_Ground` | `/Game/Environment/VisualV2WorldArtV7/Materials/M_WA7_Ground` |
| `V2_Path_Main`, `V2_Path_Wild`, `V2_Path_Cottage` | `/Game/Environment/VisualV2WorldArtV7/Materials/M_WA7_MainPath` |
| `V2_Path_VillageLoop`, `V2_Path_NorthLoop` | `/Game/Environment/VisualV2WorldArtV7/Materials/M_WA7_NorthPath` |
| `V2_House_Forecourt` | `/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_HealingForecourt` |
| `V2_House_HH_Q2_OrganicApproach` | `/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_LegacyApproach` |

Der gelesene V7-Bodengraph verwendet tatsächlich die V4-Texturen `T_HA4_Meadow` und `T_HA4_Earth`, die V5-Texturen `T_WA5_ForestFloor` und `T_WA5_WetBank` sowie die bisherigen PaintedGrass/PaintedEarth-Quellen. Die älteren Bodenmaterialien sind damit nicht als fehlendes hochwertigeres Texture-Set zu importieren.

Der vorhandene V7-Autorenpass führt regionales Mischen, variierende sichtbare Wegbreiten und unregelmäßige Säume auf den bestehenden Wegkurven fort. Geometrie-/Kollisionsänderungen wären ein anderer Auftrag. Die Erdbänder wirken in Teilen weiterhin recht homogen; Größe und Streuung der Texturdetails benötigen örtliche gestalterische Kontrolle, keine Rückkehr zum weich verwaschenen Village-Wegmaterial.

### Vegetation und Heilhaus

- V5/V6-Muster: **17 instanzierte Gruppen / 407 Instanzen**, einschließlich acht Wurzeln; die aktuelle Menge stimmt mit den Berichten überein. V6 änderte die Gruppierung von 399 dieser Instanzen, nicht die Gesamtmenge.
- V7-Erweiterung: **23 Gruppen / 658 Instanzen** für West-/Ostwald, südliche Wiese und weiteres Ufer. Keine Empfehlung, diese Gruppen erneut zu erzeugen.
- Alle instanzierten Meshkomponenten der ganzen Map zusammen: **92 / 2.315 gespeicherte Instanzen**, einschließlich Architektur und früherer Gruppen. Das ist keine reine Vegetations- oder Sichtbarkeitszahl.
- V3-Eiche bereits **41** gespeicherte Platzierungen; V3-Strauch A **80**, B **47**, Birke A **4**. Die höheren Strauch-A-Zahlen gegenüber alten Performanceberichten erklären sich durch zusätzliche spätere Artgruppen, nicht durch eine hier vorgenommene Veränderung.
- Heilhaus-V4-Materialien, Pflanzen-/Topfvarianten und örtliche Detailgruppen sind bereits integriert. Die bereits übernommenen V3-Innenraummodule werden nicht durch den älteren Dorfkern ersetzt.
- Außen-Postprocess besitzt den vorhandenen maplokalen TAA-Blendable; Außen-MotionBlurAmount 0 und das separate Innenraum-Override 0,5 sind vorhanden. Keine globale AA-/Lichtänderung erforderlich.

### Flussufer

Feuchte V5-Bodenquelle, V6-Ufergruppierung und V7-Ufer-/Teicherweiterung sind vorhanden. Die vorhandene V7-Aufnahme zeigt Kies/Steine, Farne und unterschiedliche Uferbreiten, aber weiterhin ein vergleichsweise einfaches Wasserbild mit deutlich lesbaren, teilweise geraden/geometrischen Abschnitten. Das ist ein verbleibender Artpunkt, keine fehlende Übernahme des bereits vorhandenen Uferpasses.

## 5. Bewertung nach Grafikstil

Bewertungsmaßstab: organische Formsprache, malerische Oberflächen, regionale Materialvariation, botanische Vielfalt, harmonische Farben und Lesbarkeit aus der festen schrägen Spielkamera. Keine Behauptung einer objektiven Gesamtnote oder automatischen Freigabe.

| Bereich | VisualV2 heute | Andere vorhandene Lösung | Schlussfolgerung |
|---|---|---|---|
| Boden/Gras | V4-Motive, V5-Moos/feuchte Erde, V7-Makro-/Regionalmischung; sichtbar strukturierter | Region benutzt PaintedGrass/PaintedEarth mit gedrehten Skalen; Village zeigt deutlich einfachere großflächige Oberfläche | Aktuelle VisualV2-Familie als Grundlage behalten; kein vollständiger Materialtausch |
| Wege/Übergänge | Fünf organische Bänder, regionales Wegfeld, örtliche Aufweitungen; stellenweise bandartig/homogen | Village: sieben kurvige Wege und Grundstücksvorflächen; Region: Terrainanpassung und gemeinsame Pfadbelegungsmaske | Kompositionsprinzipien prüfen; keine fremden Weltkoordinaten oder Wegmeshes kopieren |
| Wald/Unterholz | Echte V3-Kronen, Farne, Moos, Wurzeln, differenzierte Gruppen; starke Dunkelzonen bleiben | Village ältere Sprite-Vegetation; Library V3-Heldenmodelle bereits übernommen | Vorhandene Formen gezielter komponieren; keine pauschale Rückkehr zu Sprites oder alten Kronen |
| Wiese | Größere Grasstruktur, Klee/Kräuter, kleine Blüteninseln; ruhige, teils noch leere Abschnitte | Region hat weitere Ground-Herb-Meshes und räumliche Landschaftsstaffelung | Einzelne botanische Formen sind Kandidaten, keine freigegebene bessere Gesamtwiese |
| Ufer | Neue feuchte Materialmischung und Pflanzen-/Kieselgruppen; Wasser selbst einfacher | Region: eigenes Flussmesh, Holz-/Steinbrücke, Fels-/Uferkomposition | Als Formreferenz brauchbar; Brücke, Wasserlauf und Collision der VisualV2 erhalten |
| Landschaftsdetails | Heilhaus, Ruinen und Wegdetails bereits kombiniert | Library enthält weitere Stümpfe, Stein-/Wurzelvarianten und ländliche Ausstattung | Pro Einzelasset sichtbaren Mehrwert prüfen; nicht alle Varianten in die Map stellen |
| Farb-/Schattenwirkung | Warme Außenwirkung, aber sehr dunkle Kronenbereiche | EnvPerf-Lumen verändert Helligkeit/Kontakt; V8-Boden-Lift ist bildbasierter Versuch | Keine solche Renderlösung als Landschafts-Upgrade übernehmen |

Die betrachtete Village-Aufnahme hat vergleichsweise glatte Flächen, stark weichgezeichnete Wegkanten und flache Pflanzenkarten. Sie bietet gute Anordnungsideen, liegt aber bei Oberflächendetail und 3D-Vegetation hinter VisualV2. Die Region ist wesentlich größer und anders komponiert; ihr Umfang allein ist kein Qualitätsbeleg. Eine ältere Uferweg-Aufnahme enthält sichtbare Oberflächen-/Bandartefakte; diese Aufnahme gilt nicht als Beweis eines heute unverändert vorhandenen Fehlers an jeder Stelle. Die jeweils aktuelle Map lädt fehlerfrei, was künstlerische Defizite nicht ausschließt.

Die V3-Library-Aufnahme zeigt deutlich reichere Strauchsilhouetten, aber einen einfacheren Boden und eine andere Kamerakomposition als die aktuellen V7-Ansichten. Das ältere Aufnahmeset ist kein geeigneter Maßstab für Schattenhelligkeit oder Figurengröße der heutigen Kamera B.

## 6. A / B / C – Freigaben und Grenzen

**A bedeutet nachweislich durch Nutzerauftrag/Entscheidung freigegebene Grundlage. B bedeutet prüfenswert, aber keine automatische Übernahme. C bedeutet für diesen Integrationsschritt überholt oder verworfen, niemals Löschfreigabe.**

| Klasse | Verbesserung / Variante | Nachweis und Status | Konsequenz |
|---|---|---|---|
| A | Heilhaus V4 als Qualitätsreferenz | V5-Auftrag und späterer Entscheidungsabschnitt ersetzen die frühere offene V4-Formulierung ausdrücklich | Bereits integriert, erhalten |
| A | V6-Gestaltungsstil für Wege/Wald/Wiese/Ufer | V7-Auftrag bezeichnet ihn ausdrücklich als freigegeben und erlaubt die Ausweitung | Bereits Grundlage der aktuellen V7-Bindungen; nicht doppelt importieren |
| A | Bestehende TAA-/Originalschatten-Kombination und Außen-MotionBlurOff | Übernahmeaufträge, TECHNIK und tatsächlicher Blendable/Volume-Bestand | Erhalten; keine neue Renderingmaßnahme |
| B | Konkrete V7-Ausweitung (658 zusätzliche Instanzen / weitere Weg- und Uferbereiche) | Technisch integriert, letzter V7-Bericht und Entscheidungen sagen ausdrücklich „visuelle Abnahme offen“ | Jetzt visuell abnehmen; weder automatisch als freigegeben deklarieren noch ungefragt zurücksetzen |
| B | Einzelne bislang ungenutzte Library-Varianten | Assetexistenz und fehlende Meshbindung nachgewiesen, aber kein belastbarer Nachweis einer finalen Einzelasset-Artfreigabe | Erst gezielte Sichtprüfung/Freigabe |
| B | Regions-Uferformen, Bodenpflanzen und Dorfkomposition | Vorhandene Autorenquellen/Maps, keine nachgewiesene Übernahmefreigabe | Form-/Kompositionsideen getrennt prüfen |
| B | V8-Schattenvariante B | Noch Integrations-/Bewegungsgrenzen, keine reine allgemeine Schattenoperation | Nicht Teil dieses Weltartplans; Originalschatten behalten |
| C | Ältere opake/einfache Weg-/Bodenvarianten am Heilhaus und im Testkern | Örtlich bereits durch V4/V6/V7 ersetzt; Altkomponenten können technisch erhalten sein | Nicht wieder sichtbar machen oder darüberlegen |
| C | Alte Eichen-/Strauchvarianten als Ersatz der verwendeten V3-Heldenmodelle | Frühere Qualitätsgrenzen dokumentiert; bloße Verfügbarkeit ist keine Verbesserung | Keine pauschale Rückstufung |
| C | EnvPerf-Lumenalternative, erzwungene LODs, vereinfachte Schatten C/D und V8-C | Helligkeits-/Tiefen-/Maskennachteile bzw. keine Übernahmeempfehlung | Für diesen Artpass ausschließen |

Widersprüchliche historische Formulierungen werden zeitlich eingeordnet: V4-Bericht und älterer TECHNIK-Absatz nennen noch eine offene V4-Freigabe, der nachfolgende V5-Entscheidungsabschnitt bestätigt jedoch die Nutzerreferenz. Für V6 gilt die entsprechende spätere Freigabe im V7-Auftrag. **Eine spätere Freigabe des V7-Gesamtergebnisses wurde nicht gefunden.**

Die Library-JSON `Art/World/WestlandAssetLibrary/ArtQualityV3.json` enthält weiterhin `human_art_approval: false`. Das verhindert keine Nutzung des längst vorhandenen technischen Bestands, erlaubt aber keine erfundene globale Freigabe aller anderen Bibliotheksmodelle.

## 7. Konkrete fehlende Kandidaten und Abhängigkeiten

Die folgenden Beispiele sind **in den untersuchten Quellmaps referenziert, aber nicht als dasselbe Static Mesh auf VisualV2-Komponenten gebunden**. „Fehlt“ bedeutet hier lediglich Inventardifferenz, nicht notwendige Qualitätslücke. Es wurde keine vollständige transitive Runtime-/Blueprint-Abwesenheit behauptet.

| Kandidat | Tatsächlicher Pfad | Möglicher Nutzen / Hindernis | Klasse |
|---|---|---|---|
| Zweite Wurzel, Stümpfe | `/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Root_B`, `SM_WLA_Stump_A`, `SM_WLA_Stump_B` | Wenige glaubwürdige Waldakzente; Alter/Qualität/Größe und Laufkorridor vorher prüfen | B |
| Kleine Steinvarianten | `/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_SmallStones_A`, `SM_WLA_SmallStones_B` | Zusätzliche Formvariation am Weg/Ufer; vorhandene Kieselgruppen nicht doppeln | B |
| Weitere Kräuterformen | `/Game/Environment/WestlandRegion/Meshes/SM_WR_Ground_BroadHerb`, `SM_WR_Ground_NarrowHerb`, `SM_WR_Ground_LeafPlant`, `SM_WR_Ground_FlowerPlant` | Botanische Abwechslung; Materialien und Maßstab gegenüber V4/V5 prüfen | B |
| Dörfliche Details | `/Game/Environment/WestlandAssetLibrary/Meshes/Farm/SM_WLA_Woodpile_A`, `SM_WLA_Woodpile_B`, `SM_WLA_Haybale_A`, `SM_WLA_Haybale_B` | Nur mit glaubwürdiger Nutzung am vorhandenen Ort; keine automatische Landwirtschaftszone | B |
| Region-Brücken | `/Game/Environment/WestlandRegion/Meshes/WR_StoneBridge`, `WR_WoodBridge` | Kompositions-/Formreferenz; **kein geplanter Ersatz** der bestehenden Gameplaybrücke | B, zurückgestellt |
| Dorfpfad-/Regionpfadtechnik | `M_WV_Path`, `M_WR_PathBlend`, `T_WR_PathCoverage` | Village ist texturlos/transluzent, Region benutzt regional gebundene Koordinaten/Belegungsmaske; nicht direkt passend | C für Materialtausch, B als Autorenprinzip |

Der Regions-Pfadshader verwendet dieselben älteren PaintedGrass/PaintedEarth-Quellen plus `T_WR_PathCoverage`; sein Raster wird aus den Koordinaten der 800 × 600-m-Region aufgebaut. Das lässt sich nicht unverändert auf die kompakte VisualV2 legen. Das bestehende VisualV2-V7-Wegfeld bildet bereits die eigenen Kurven ab.

`Tools/ConformWestlandRegionPathsV1.py` schreibt und speichert ausdrücklich Regionsmeshes und die Regionsmap. **Nicht als vermeintlich lesenden Übernahmeschritt ausführen.** Falls künftig eine terrainbedingte lokale Anpassung notwendig wird, nur das zugrunde liegende Prinzip anhand der tatsächlichen VisualV2-Flächen neu prüfen. Aktuell liegt kein nachgewiesener Bedarf für neue Wegkollisionen vor.

Neue Baumfamilien würden außerdem die bestehende mesh-/materialspezifische Kronenfreistellung berühren. Deshalb im ersten Integrationspaket **keine zusätzlichen Baumfamilien** und keine neuen Reveal-Materialien. Gemeinsame Originalmaterialien nicht pauschal überschreiben; funktionierende Instancing-Materialien beibehalten.

## 8. Priorisierter Integrationsplan nach Freigabe

| Paket | Begrenzter Umfang | Vorgehen | Abnahme / Schutz |
|---|---|---|---|
| P0 – zuerst | Bereits integriertes V7, ohne Umbau | Feste QHD-Spielkameraansichten von Heilhaus, Waldweg, Wiese/Kreuzung und Ufer/Brücke gemeinsam abnehmen; bestehende V6-Kontrollorte danebenstellen | Harry benennt konkret beibehaltene und zu korrigierende Stellen; V7 nicht stillschweigend freigeben |
| P1 | Ein vorhandener Weg-/Uferanschluss mit tatsächlich benannter Schwäche | V4-/V5-Texturen und V6-Gestaltungsprinzip im vorhandenen V7-System verwenden; nur lokale Maske/Farbskala und Saumkomposition, keine neuen Wegmeshes | Identische Vorher-/Nachherkamera; Laufkern, Interaktionen und Wasser-/Brückengrenze unverändert |
| P2 – optional | Kleine Wald-/Wiesenstelle | Nach Einzelassetfreigabe höchstens die dort benötigten Wurzel-/Stein-/Kräutervarianten; vorhandene Gruppen gezielt variieren statt einen zweiten Streupass zu stapeln | Maßstab zur 140-cm-Figur, Bodenkontakt, keine Überlagerung von NPCs/Triggern, NoCollision für reine Dekoration |
| P3 – nur nach P1/P2 | Weitere gezielt freigegebene Stellen | Gleiche bestätigte Material-/Assetfamilien wiederverwenden; unveränderte Quellassets aus anderen Maps referenzieren, keine kompletten Quellmaps kopieren | Ortsweise Bildabnahme und technischer Vergleich; keine automatische Vollkarten-Ausweitung |

**Sofort freigabefähiger Integrationsumfang aus A: keine fehlende Übernahme identifiziert.** A wird als bestehende Grundlage geschützt. P1/P2 setzen eine konkrete örtliche Änderungsfreigabe voraus; B-Kandidaten werden nicht durch diesen Bericht zu A.

Für jedes spätere Umsetzungspaket vor Änderungen Actor-/Komponentenbindungen, Transformationen, Instanzzahlen und ursprüngliche Map-Hashes erfassen, ohne neue Vollkopien oder Testmaps anzulegen. Bestehende Autorenquellen und Git dienen der Wiederherstellbarkeit. Kollisionsboden, Wegmittellinien, Brücke, NPC-Identitäten/-Dialoge, Kampf/Fang, Heilhaus-Innenraum und Übergänge, Spielfigur/Animationen und Kamera B bleiben geschützt. Keine neuen Gameplay-Systeme, keine neue Map, kein neuer Worktree, keine zusätzlichen Vollbackups.

**Unverändert lassen:** sämtliche vorhandenen Lichtquellen, Originalschatten, Lumen, Bloom, Belichtung, TAA, Spielermaßstab und Steuerung. Schattenaufhellung oder andere Lumen-/AA-Maßnahmen sind kein versteckter Bestandteil eines Boden-/Vegetationspasses.

Spätere technische Abnahme: erforderlicher Editor-Build, vollständige Projekt-Automation, Map Check und echter Gameplay-Fußlauf (acht Richtungen, Sprint, NPC/Dialog/Quest, Kampf/Fang, Brücke, Heilhaus/Innenkamera/Heilen, Save/Load, Kronenfreistellung). Ausgangsspielstand erhalten. Echte QHD-Bildpaare mit gleicher Kamera, Position, Qualität und Auflösung, außerdem 720p-Lesbarkeit; PIE und Standalone unterscheiden. Keine FPS-Benchmarks im Artpass. Erst nach erfolgreichen Tests nötige Änderungen gezielt committen/pushen; keine Kontrollmedien oder Caches versionieren.

## 9. Prüfstatus dieses Analyseauftrags

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Git/Remote vor Beginn | `main` und GitHub auf `9b885388bd966474dc7608e0c173e67e87270c26`, Index leer |
| Vorhandene Maps/Assets untersuchen | 17/17 Maps frisch geladen, gespeicherte Bindungen und direkte Abhängigkeiten erfasst |
| Map Check | 17/17 mit jeweils 0 Fehlern / 0 Warnungen |
| Paket-/Quellschutz | Keine Pakete gespeichert; keine Dirty-Pakete; 3.564 vorbestehende Dateien SHA-256-identisch |
| Bildprüfung | Acht tatsächlich vorhandene Unreal-Bilder betrachtet; historische Aufnahmen klar gekennzeichnet |
| Neuer Build / neue Projekt-Automation | **Nicht ausgeführt**, da ausschließlich Bericht und lesende Bestandsaufnahme; keine Code-/Asset-/Mapänderung |
| Gameplay-Fußlauf / neue PIE-/Standalone-Aufnahmen | **Nicht ausgeführt**; historische Tests nicht als neue Ergebnisse ausgegeben |
| Performance | Keine Messung oder FPS-Behauptung |
| Berichtprüfung | Abgleich der Mengen, Mapnamen, tatsächlichen Materialpfade und Freigabeklassen mit Inventar/Quellen; Markdown-/Whitespace- und Indexprüfung vor Commit |

Die frische grafische Editorprüfung ersetzt keinen neuen Gameplay-/Animationslauf. Bekannte Engine-Startup-Diagnosen sind von den tatsächlichen Map-Check-Ergebnissen zu trennen; allgemeine Fehlerfreiheit des Engine-Logs wird nicht behauptet. Der vorherige Abschlussbericht belegt separat 49/49 Tests und 95 Blender-Reopens; diese wurden hier nicht erneut ausgeführt.

## 10. Nachvollziehbare Quellen und lokale Bilder

Wichtigste Projektdokumente: `Docs/GRAFIKSTIL.md`, `TECHNIK.md`, `ENTSCHEIDUNGEN.md`, `DEV_TESTMAP_VISUAL_V2_PRUEFBERICHT.md`, `VISUALV2_HEILHAUS_ART_QUALITY_V4_PRUEFBERICHT.md`, `VISUALV2_WORLD_ART_QUALITY_V5_PRUEFBERICHT.md`, `VISUALV2_WORLD_ART_QUALITY_V6_PRUEFBERICHT.md`, `VISUALV2_WORLD_ART_QUALITY_V7_PRUEFBERICHT.md`, `WESTLAND_VILLAGE_CORE_V1_PRUEFBERICHT.md`, `WESTLAND_ASSET_LIBRARY_ART_QUALITY_V2_PRUEFBERICHT.md`, `WESTLAND_ASSET_LIBRARY_ART_QUALITY_V3_PRUEFBERICHT.md`, `HEALING_HOUSE_ART_QUALITY_V3_PRUEFBERICHT.md`, `VISUALV2_ENVIRONMENT_QUALITY_V1_PRUEFBERICHT.md`, `VISUALV2_SHADOW_QUALITY_V8_PRUEFBERICHT.md`, `DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md` und `VISUALV2_VEGETATION_PERFORMANCE_V1_PRUEFBERICHT.md`.

Autorenquellen: `Art/World/VisualV2HealingArtV4`, `VisualV2WorldArtV5`, `VisualV2WorldArtV6`, `VisualV2WorldArtV7`, `WestlandRegion/WestlandRegion_V1.json`, `Westland/WestlandVillage_V1.json`, `WestlandAssetLibrary/ArtQualityV3.json`; zugehörige vorhandene Werkzeuge wurden gelesen, nicht als Änderungen ausgeführt.

Tatsächlich betrachtete lokale Originalbilder, bewusst nicht neu hochladen:

| Historischer Nachweis | Vorhandener Dateipfad |
|---|---|
| Heilhaus V4 | [QHD-Heilhaus](/Users/harry/Developer/PokeMonster/Saved/VisualV2HealingArtV4/Photos/PIE_Q2_AfterFinal_2560_1440/Heilhaus00000.png) |
| V7-Ostwald | [QHD-Ostwald](/Users/harry/Developer/PokeMonster/Saved/VisualV2WorldArtV7/Photos/PIE_Q1_ArtOnly_2560_1440/Ostwald00000.png) |
| V7-Wiese | [QHD-Südwiese](/Users/harry/Developer/PokeMonster/Saved/VisualV2WorldArtV7/Photos/PIE_Q1_ArtOnly_2560_1440/Suedwiese00000.png) |
| V7-Ufer | [QHD-Uferabzweig](/Users/harry/Developer/PokeMonster/Saved/VisualV2WorldArtV7/Photos/PIE_Q1_ArtOnly_2560_1440/Uferabzweig00000.png) |
| WestlandVillage | [Ältere Dorf-/Wegansicht](/Users/harry/Developer/PokeMonster/Saved/WestlandVillage/04_GeschwungenerWeg.png) |
| WestlandRegion | [Ältere Uferwegansicht](/Users/harry/Developer/PokeMonster/Saved/WestlandRegion/PIE_53_Uferweg.png) |
| WestlandRegion | [Spätere Aufnahme der Brücken-Prüfroute](/Users/harry/Developer/PokeMonster/Saved/WestlandRegion/PIE_71_Steinbruecke.png) |
| AssetLibrary V3 | [Vorhandene Waldansicht](/Users/harry/Developer/PokeMonster/Art/World/WestlandAssetLibrary/Review/V3/GameCamera_Forest.png) |

Die Bildnamen sind die ursprünglichen Bezeichnungen; ein Dateiname wie „Steinbruecke“ beweist nicht, dass das Bauwerk im gewählten Ausschnitt vollständig sichtbar ist. Lokale Links sind keine auf GitHub hochgeladenen Bilddateien und keine Buildabhängigkeit.

## 11. Git-Sicherung und Stopp

Ausschließlich dieser neue Vergleichsbericht gehört zum Sicherungsschritt. Keine Map-, Art-, Config-, C++- oder Gameplaydatei wird mitcommitted; alle 49 zuvor unversionierten Pfade bleiben ausgeschlossen. Rohinventar, Skriptausgaben und optionale Bilder bleiben lokal. Vor Commit gezielter Dateipfad, vollständiger Indexabgleich und `git diff --cached --check`; danach regulärer Push auf `origin/main`, direkter Remote-/Upstreamvergleich und Kontrolle der unveränderten Backup-Refs. Für diesen normalen Markdownbericht entstehen keine neuen LFS-Nutzobjekte. Tatsächlicher Commit-/Push-Hash wird nach Durchführung in der Abschlussantwort genannt.

**Stopp nach diesem Bericht. Keine automatische Übernahme und keine weitere Kartenbearbeitung vor Freigabe.**
