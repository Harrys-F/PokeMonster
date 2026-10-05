# Healing House – Art Quality V3 / Reference Polish

## Ergebnis und Ausgangsstand

Stand 2026-10-05. Ausgangs-HEAD: `26428cf Improve healing house art and natural ground`. `git status --short` war vor Beginn leer. Der technische V2-Raum wurde weiterverwendet; keine neue Raum-, Quest-, Kampf- oder Heiltechnik. Kein Commit, Push oder Staging. Die Umsetzung ist technisch geprüft; Harrys visuelle Freigabe steht ausdrücklich noch aus.

Der Pass verbessert Möbelkonstruktion, botanische Silhouetten, Heilhaus-Ornamente, lokale Lichtwirkung, Schindel-/Fassadendetails und Bodenmischung. Das Referenzbild bleibt die gestalterische Richtung, ist noch nicht in allen sichtbaren Punkten erreicht. Originale Blenderquellen und gemeinsam genutzte Gebäudeassets bleiben erhalten.

## Vergleich mit der Referenz

Die Referenz verbindet ausgearbeitete Möbelsilhouetten, warme Holzrahmen, unterschiedlich geformte Heilpflanzen, überlappende Terrakottadächer, tiefe Fenster, handwerkliches Fachwerk/Naturstein, markanten Eingang und ein Schutz-/Heilsymbol. Innen schaffen Kamin, Fenster und Laternen mehrere Lichtzonen; außen gruppieren sich Blumen/Kräuter an Fenstern und Eingang. Formen und Oberflächen wirken gepflegt, nicht verfallen.

| Merkmal | V3-Annäherung | Sichtbarer Abstand zur Referenz |
| --- | --- | --- |
| Empfang | Zusammenhängender 80/105-cm-Tresen, Rahmen, Unterbau, geformte Kanten, Beschläge, Blattornament | Schnitzerei, Gefäßvielfalt und feine malerische Verschattung bleiben einfacher |
| Möbel | Bretter, gestützte Beine, Zierleisten, abgerundete Kanten, kleine handwerkliche Unregelmäßigkeit | Silhouetten weiterhin ruhiger/rechteckiger; Polster und Gefäße noch Platzhalter |
| Pflanzen | Breite/schmale/gekrümmte/hängende/blühende Familien und geformte Töpfe | Weniger botanische Dichte, einfachere Blattoberflächen und Blüten als im Bild |
| Licht | Kamininsel mit Schatten, kleine Laternenbereiche, schwache Fensterfüllung | Referenz hat reichere weiche Licht-/Schattenstaffelung; Außenlicht bleibt deutlich heller/flacher |
| Dach | Flach überlappende Schindelkurse, neue gemalte Terrakotta, klarere Kanten | Große Dachform bleibt technisch unverändert und geradliniger; Kurse noch regelmäßiger |
| Fassade | Stärkere/leicht unregelmäßige Balken, differenzierte Steine, Fensterrahmen/-kästen, Eingang und Kamin | Weniger florale Verflechtung, weniger architektonische Vielfalt und Atmosphärentiefe |
| Identität | Bestehendes Guardian-Blatt-/Schutzmotiv in Schild, Tresen und Stoff erhalten | Referenz besitzt reichere heraldische und handgeschnitzte Details |
| Boden | Gemischte Texturmaßstäbe/Rotationen/Offsets und Macro-Variation | Feine ähnliche Grasflecken bleiben bei längerem Vergleich erkennbar; keine mathematische Aperiodizität |

Die normale Spielkamera zeigt keine dominanten regelmäßigen V2-Texturquadrate mehr. Die Referenz ist eine dicht inszenierte Illustration; V3 bleibt ein funktionaler, begehbarer 3D-Spielraum mit sichtbaren Vereinfachungen. Keine Umdeutung der dokumentierten 2D/2.5D-Richtung. Vor allem Außenbeleuchtung, botanische Dichte, Feuerdarstellung und feinere malerische Oberflächen sind verbleibende Qualitätsabstände. Der vorhandene kleine Testwürfel außerhalb des Gebäudes wurde nicht nebenbei entfernt.

## Möbel, Pflanzen und Ornamente

- Empfang: ein Möbelstück mit gemeinsamem Rahmen/Unterbau, niedriger 80-cm- und normaler 105-cm-Arbeitsfläche; keine zwei zusammengestellten Würfel. Bestehende Heilerin- und Interaktionsposition unverändert.
- Regale: stärkere Stützen, Sockel-/Kopfprofile, sichtbare Rahmen und Holzverbindungen; vorhandene Bücher/Gefäße weiterverwendet.
- Bänke/Tische: Bretter mit kleinen Unregelmäßigkeiten, konstruktive Träger/Beine, gefaste Kanten; vorhandene Sitzpolster bleiben. Tisch-/Sitzmaßstab ca. 75/45 cm.
- Behandlung/Liegen: geformte Rahmen, Pfosten, Beschläge, vorhandene zwei Größen und Q2-Decken; ursprüngliche Blocker und Laufwege erhalten.
- Sieben Pflanzenfamilien: BroadHerb, NarrowHerb, LeafPlant, FlowerPlant, TrailingHerb, HangingHerb und HerbBundle. Unterschiedliche Blattbreite, Neigung, Krümmung, Blüten und gebundene Bündel; gedrehte/skalierte Gruppen statt einer identischen Standardsilhouette.
- Geformte Töpfe, sechs Fensterkästen mit 18 Pflanzen, vier Eingangspflanzen, vier neue Vorplatzgruppen und drei Kräuterbündel; Platzierung nach Fenster-, Regal-, Eingang- und Behandlungskontext. Vorhandene Pflanzstandorte bevorzugt erhalten.
- Guardian-Schild: bestehendes Schutz-/Blattmotiv mit Holzrahmen und Beschlägen. Schmiedehaken, Fensterkästen und dezente Holzdetails ergänzen die Identität; keine Pokéball- oder Krankenhausästhetik.

Im ersten Sicht-/Fußreview störten zwei Bodenpflanzen und zu große Hängepflanzen die wandnahe Player-Silhouette. Nur Dekoration wurde korrigiert: `HH_Art_FloorHerb_1` um 40 cm versetzt, Skalierung 1,25 → 0,85; `HH_Art_FloorHerb_2` um 100 cm versetzt. Drei Hängetöpfe auf 0,55 skaliert, Haken auf Y 0,85 und näher an ihre Wand gesetzt. Die korrigierten vorderen/hinteren Seitenlaufzonen wurden im vollständigen finalen Fußlauf erneut geprüft. Keine Möbel- oder Wandcollision verändert.

## Außenhaus

Grundmaß ca. 9 × 9,3 m, Höhenwirkung und 150 × 215-cm-Passage unverändert. Dachhauptfläche, Vorbau und Eingang erhalten zusammenhängende überlappende Schindelreihen und gemalte Terrakotta; keine Tausende einzelner Actors. Dachkanten, Balken und Türrahmen klarer ausgeformt. Fenster mit Rahmen/Tiefe, Fensterbank und eigenen Kräuter-/Blumenkästen. Steine behalten warme Grau-/Brauntöne mit Form-/Fugenvariation. Putz verwendet weiterhin die gepflegte V2-Oberfläche; keine unnötige neue Putztextur. Kaminform und Schichten stärker ausgearbeitet.

Die feste playerbezogene Außenkamera schneidet unmittelbar am Gebäude weiterhin Teile des hohen Dachs ab. Eingang, Front, Dachkante und seitliche Fassade wurden in tatsächlicher PIE-Kamera beim Gehen geprüft; die Aufnahmen sind keine vollständige Gebäudefreistellung. Kamera oder Hausgröße wurden dafür nicht geändert. Die komplette Quellgeometrie wurde zusätzlich in Blender geprüft.

## Räumliche Lichtmodellierung und Materialabstimmung

Lokale Lichtquellen verwenden physikalischen Abfall, begrenzte Reichweiten und moderate Quellradien. Der Kamin ist die einzige schattenwerfende lokale Innenlichtquelle. Keine neue globale Außenlichtstimmung.

| Quelle | Candela | Reichweite cm | Quellradius cm | Temperatur K |
| --- | ---: | ---: | ---: | ---: |
| Kamin | 20 | 270 | 18 | 2450 |
| Warten | 3,8 | 245 | 12 | 2850 |
| Empfang | 5,5 | 260 | 15 | 3100 |
| Behandlung | 3,5 | 260 | 16 | 3400 |
| Tresen | 1,8 | 210 | 16 | 3050 |
| Ruhe | 1,5 | 210 | 16 | 3200 |
| Je Fenster, sechs Spots | 5 | 440 | 24 | 5800 |

Fenster-Spots ohne Schatten, Kegel 12/48°. Räumlich begrenzter Innen-Postprocess: Exposure Compensation −0,55 → −0,63, AO 0,8/60 → 0,95/65. Kamin beleuchtet seine unmittelbare Umgebung; der übrige Raum bleibt spielbar lesbar. Holz, Stein, Putz, Stoff und Pflanzen unter echter PIE-Kamera abgestimmt. Helle botanische Albedos wurden dort zu ruhigeren Oliv-/Kräutertönen korrigiert; neutrale Blender-Prüffarben sind nicht die finale Unreal-Farbabstimmung. Die vorhandene helle Feuer-Platzhalterform bleibt erkennbar vereinfacht.

## Boden-Anti-Tiling und Vegetation

Ursache: je Gras/Erde nur eine identische Welt-XY-Texturprobe mit einem Maßstab; die Wiederholung setzte sich auf Grundfläche und Blends fort.

V3 verwendet dieselben vorhandenen zwei Bodenbilder: drei Grasproben bei 190/271/413 cm, zwei Erdproben bei 220/337 cm, mit unterschiedlichen Rotationen und Offsets. Dezente großflächige Farbvariation bricht gleiche lokale Kontraste zusätzlich auf. Maximal fünf Farbproben; keine neue Bodenbitmap, kein teurer mehrlagiger Noise-/PBR-Stack, keine extreme Texturvergrößerung. Der gemeinsame Quellshader liegt in `Art/HealingHouse/QualityV3/GroundBlend.hlsl`.

Vier bestehende Materialien geändert: Grass, Earth, PathBlend, ForecourtBlend. Weg-/Vorplatzmasken und Parameter bleiben kompatibel, einschließlich Center −850/0 cm und HalfSize 325/340 cm. Weltkoordinaten halten Anschlüsse konsistent.

Die 321 räumlichen Gras-/Kräuter-/Steindetails in sechs HISM-Komponenten bleiben mit vorhandenen Gruppen, Lücken, freien Wegmitten und Culling 3200–4300 cm erhalten. Keine Player-Collision oder dynamischen Grasschatten. Keine gleichmäßige Vollflächenbegrünung. Im tatsächlichen Mapbestand werden diese vier Bodenmaterialien derzeit ausschließlich von `Dev_HealingHouseTestMap` referenziert. `Dev_WestlandVillage` und alle anderen Maps sind bytegleich. Übernahme ins Dorf und regionale Dichteprofile sind nicht Teil dieses Passes.

## Blender, Export, Import und Wiederverwendung

Quelle ausdrücklich gespeichert:
`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/HealingHouse/Source/HealingHouse_QualityV3.blend`

Erneut in Blender geöffnet, 34 Meshes/Materialbelegung/Bounds geprüft und Formübersicht visuell angesehen; erst danach endgültige 34 FBX-Exporte. Originale V1/V2/V3/QualityV2-Blenderdateien nicht überschrieben. Keine Marketplace-Assets oder externen Downloads. Eine selbst erzeugte gemalte Terrakottatextur; Herkunft/Prompt neben der Quelle dokumentiert.

34 neue Meshes: acht Möbel, sieben botanische Formen, Fensterkasten/Schild/Haken sowie 16 Dach-/Fassadenvarianten. 16 eigene Materialien, ein Texture-Asset; insgesamt 51 Unreal-Assets unter `/Game/Environment/HealingHouse/QualityV3`. Reused: V2-Holz/Timber/Stein/Putz/Sage/Linen und vorhandene Buch-, Papier-, Glas-, Gefäß-, Metall-, Symbol-/Fenster- und Feuerbestandteile. Neue Fade-Varianten statt Änderung gemeinsamer ursprünglicher Gebäudematerialien.

Alle 34 importierten LOD0-Dreieckzahlen entsprechen exakt der gespeicherten Blenderbibliothek; Bounding-Box-Größen stimmen innerhalb 0,02 cm überein. Keine fehlenden Meshes, Materialslots oder Texture-Referenzen. Neue Textur zur Laufzeit maximal 1024, Mips und Streaming; keine zusätzlichen Mikro-PBR-Bilder.

## Collision, Cutaway und eingefrorene Technik

Zehn vorhandene Möbelactors behalten Mesh, Transformation und Collisionprofil exakt. Nur ihre alte Darstellung ist verborgen; passende sichtbare Quality-V3-Actors liegen ohne Collision an denselben Transformationen. Sämtliche neuen Pflanzen/Dekorationen sind NoCollision. Die neue Formsprache verändert die ursprünglichen Blocker nicht.

Die ursprünglichen 107 geordneten Occluder bleiben erhalten; zehn neue frontseitige Fensterkasten-/Pflanzenactors folgen demselben Fade, insgesamt 117. Keine neue Seiten-/Rückwand als Occluder. Zusätze: WindowBox 0/1, jeweils drei WindowHerb sowie EntranceHerb 0/1. Dach und kameraseitige Front verschwinden innen, beide Seiten- und Rückwand bleiben sichtbar.

| Größe/System | Finaler Stand |
| --- | --- |
| Expanded Interior | 12 × 10 m, unverändert |
| Außenkamera | 2500 cm / FOV 35° / Pitch −55° / Yaw −45° |
| Innenkamera | 2600 cm / FOV 35° / Pitch −50° / lokaler Yaw 0° |
| Player | 1,40 m sichtbare Höhe, Sprite-Skalierung unverändert |
| Bewegung | 210 cm/s; acht Richtungen/Animationen unverändert |
| Control Blend | 0,18 s |
| Cutaway | 0,4 s, bestehende Logik |
| Relocation/Übergangsmaske/Lag | Unverändert |
| Heilerin/Heal/Checkpoint/Save/Quest/Battle | Gameplay-Code und Konfiguration unverändert |

## Vollständiger finaler PIE-Fußlauf

Auf dem gespeicherten, erneut geprüften Endstand über Enhanced-Input-Bewegung, ohne Pawn-Testteleports oder Kamera-Verstellung: Außenfläche → Weg → gerade durch Eingang → Empfang/Heilerin → Sitzbereich/Kamin → Behandlung → kleine und große Liege → beide Seitenwände → Rückwand → erneut die korrigierten Pflanzenzonen → Ausgang → diagonaler Wiedereintritt → diagonaler Ausgang → Außenweg/Bodenvergleich.

Bestanden: 96 Weg-/Prüfschritte, 26 lokale Kamera-Aufnahmen, zwei Eintritte und zwei Austritte. Keine blockierende Dekoration, keine neue Sackgasse, keine neuen Map-Lücken auf der Route. Player an allen geprüften Stationen sichtbar. Wände korrekt erhalten, Front/Dach korrekt verborgen; Endkamera und Steuerungsbasis innen/außen korrekt. Höchste gemessene Laufgeschwindigkeit 210,0000000000473 cm/s (numerische Rundung).

Die vorgesehenen Relocation-Sprünge des bestehenden Systems erfolgen vollständig hinter der Übergangsmaske; dies sind keine Testteleports. Kameraübergang/Control-Blend bleiben erhalten. Kurze temporale Dither-/TAA-Historie direkt nach dem Cut kann in einer unmittelbaren Aufnahme sichtbar sein; die ruhenden finalen Raumaufnahmen zeigen keine dauerhafte Ghost-Geometrie. Keine neue Übergangslogik.

Team vor Heilung tatsächlich über bestehende Battle-Runden geschädigt: erste Kreatur 0/52 HP, zweite 15/47 HP, PP teilweise verbraucht. Normale Heilerin-Interaktion/Dialog vollständig ausgeführt: alle HP/PP voll, Checkpoint `Dev_HealingHouse` gesetzt und vorhandener Save-Aufruf erfolgreich. Gespeicherte Checkpoint-ID sowie exakte double-Position im Save-Payload geprüft; Deserialisierung zusätzlich durch die bestehenden Checkpoint-/Save-Tests. Ursprünglichen Nutzer-Dev-Spielstand nach allen Tests bytegleich zurückkopiert: 7458 Bytes, SHA-256 `3374b7719cbf462a1fec993a5e80b29c94be61591cc06121d291c130f05cc1f4`.

Ein früherer Reviewlauf wurde durch eine nachträgliche Verschiebung der Prüfroute im Testwerkzeug abgebrochen, nicht durch eine Gameplay-Kollision. Dieser Zwischenlauf bleibt lokal als `FootFirstReview`; ausschließlich der neu gestartete, vollständige `FootFinal` ist der Abschlussnachweis.

## Build und Tests

Der erste Automationlauf bestand 37/38 Tests. Die Layoutprüfung erwartete die sichtbare Darstellung auf dem alten Kollisionsprimitive; die neue, absichtlich getrennte Art-/Collision-Lösung erfüllte diese alte Annahme nicht. Nur `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp` erweitert: ein verborgener Originalblocker muss eine passende sichtbare Darstellung mit identischer Transformation und NoCollision besitzen, während seine eigene Player-Collision aktiviert bleibt. Keine Änderung an Gameplay-C++, keine Testdeaktivierung und keine pauschale Abschwächung der Visibilityprüfung.

Build `PokeMonsterEditor Mac Development` unter UE 5.8.2 erfolgreich, ohne Compile-/Linkfehler. Danach neue Prüfinstanz mit frisch gebautem Modul: **38/38 Automationstests bestanden**. Einschließlich Player Foundation/ScaleCalibration/InteriorCamera, HealingHouse Layout/CollisionAndCutaway/RestCheckpointSaveAndDefeat, RelocatedInterior sowie kompletter vorhandener Battle-/Capture-/Inventory-/Quest-/Save-Testbestand.

Map Check **0 Fehler / 0 Warnungen**. Materialgraph-/Missing-Asset-/Collision-/Bounds-/Importaudit bestanden. Alle sieben neuen Pythonwerkzeuge syntaktisch geprüft. `git diff --check` ohne Ausgabe; Markdown-Fences/Dateiverweise/JSON ebenfalls geprüft. Keine Behauptung, das gesamte Unreal-Startlog sei warnungsfrei: die Engine meldet auf diesem Mac weiterhin ihren vorhandenen iOS-Gerätetool-Startfehler; dieser betrifft die erfolgreichen Projektprüfungen nicht.

## Performance und Grenzen

34 Bibliotheksmeshes zusammen **96144 Dreiecke**. Hochgerechnete sichtbare Q3-Instanzen in der Editor-Map **214596 Dreiecke**; Innen- und Außenraum zusammen, kein gleichzeitiger PIE-GPU-Messwert. Die Schindelgeometrie wurde vor finalem Export deutlich vereinfacht; Hauptdach 9624 Dreiecke, Vorbau 656, Eingang 232. Kamin 17228, Empfang 12772; diese vergleichsweise aufwendigeren Formen bleiben Profiling-Kandidaten.

Actorbestand 482 → 539: 57 zusätzliche Actors, davon sechs Fenster-Spots, übrige visuelle Meshes. Keine neue Tick-/Gameplayklasse. Bestehende 321 HISM-Details ca. 28608 Dreiecke und unverändertes Culling. Materialien mit mehreren Sektionen benötigen weiterhin mehrere Render-Batches. Maskierte Blatt-/Fadeflächen verursachen etwas zusätzliche Überzeichnung; keine transparenten Komplettgebäudeschichten. Lokale Lichtreichweiten begrenzt, ein schattenwerfendes Innenlicht; sechs neue Spots ohne Schatten.

Neue FBX zusammen ca. 3,6 MB, Unreal-QualityV3-Assets ca. 8,2 MB, Blenderquelle ca. 15 MB. Boden maximal fünf Samples statt einfacher V2-Probe; keine neue Bodenbitmap. Das ist ein dokumentierter Kostenanstieg, kein belastbarer FPS-/M4-/Village-Benchmark. Große Dorfübernahme benötigt gesondertes Profiling und ggf. LOD-/Batchoptimierung.

## Lokale Reviewnachweise

Alle Bilder/Logs/Prüfkopien ausschließlich unter ignoriertem `Saved/HealingQualityV3`, nicht in Git. Native PIE-Screenshots, keine nachträglich erzeugten/retuschierten Spielbilder. Innen 2600/35/−50/0, außen 2500/35/−55/−45.

- [Innenraum gesamt, nach diagonalem Eintritt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/17_DiagonalInside00000.png)
- [Empfang/Heilerin](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/03_Reception00000.png)
- [Sitzbereich](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/04_Waiting00000.png)
- [Kamin/Lichtinsel](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/05_Fireplace00000.png)
- [Behandlung/Kräutertisch](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/06_Treatment00000.png)
- [Kleine Kreaturenliege](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/07_SmallBed00000.png)
- [Große Kreaturenliege](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/08_LargeBed00000.png)
- [Pflanzen-/Regalbereich an linker Seite](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/13_SideMinusRear00000.png)
- [Korrigierte hintere Pflanzenzone](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/19_CorrectedRearPlant00000.png)
- [Korrigierte vordere Pflanzenzone](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/20_CorrectedFrontPlant00000.png)
- [Außenfassade/Eingang/Dach, schräg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/16_OutsideAgain00000.png)
- [Seitlicher Außenvergleich; Gebäude nicht vollständig im Bild](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/21_ExteriorWhole00000.png)
- [Weg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/00B_Path00000.png)
- [Gras-/Wegrand](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/00C_GrassEdge00000.png)
- [Große Bodenfläche, Anti-Tiling](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/FootFinal/Review/22_GroundWideFinal00000.png)

Blender-Formreview: [/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/Blender/SourceReview.png](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/HealingQualityV3/Blender/SourceReview.png). Prüfprotokolle: `Saved/HealingQualityV3/QualityAudit.json`, `ImportAudit.json`, `Blender/SourceAudit.json`, `FootFinal/PIERoute.json`, `FinalTests.json`, `Build.log`, `AutomationEditor.log` und `BaselineComparison.json`.

## Vollständige Dateiliste

Projektroot: `/Users/harry/Developer/PokeMonster/Game/PokeMonster`. Die folgenden Pfade sind relativ zu diesem Root. **8 bestehende Dateien geändert, 100 neue Dateien**. Von 808 bestehenden versionierten Dateien sind die übrigen **800 bytegleich**; alle Gameplay-C++-Dateien, anderen Maps und ursprünglichen Artquellen sind unverändert. Nur der genannte Automationstest ist die zusätzliche C++-Änderung.

### Bestehende Dateien geändert

- `Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Earth.uasset`
- `Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_ForecourtBlend.uasset`
- `Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass.uasset`
- `Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend.uasset`
- `Content/Maps/Dev_HealingHouseTestMap.umap`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`
- `Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp`

### Neue Dateien

- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Bench.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Bookcase.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_BroadHerb.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Chimney.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_CounterStepped.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_DoorFrame.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_FlowerPlant.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_GuardianSign.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_HangingHerb.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_HerbBundle.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_HerbShelf.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_HerbTable.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_LanternHook.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_LeafPlant.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_NarrowHerb.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Roof_Entry.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Roof_Main.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Roof_Porch.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Roof_Trim.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Stone_CameraSide.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Stone_Far.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Stone_Front.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Table.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Timber_CameraSide.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Timber_Entry.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Timber_Far.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Timber_Front.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_TrailingHerb.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_TreatmentBedLarge.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_TreatmentBedSmall.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_WindowPlanter.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Windows_CameraSide.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Windows_Far.fbx`
- `Art/HealingHouse/Exports/QualityV3/SM_HH_Q3_Windows_Front.fbx`
- `Art/HealingHouse/QualityV3/Design.md`
- `Art/HealingHouse/QualityV3/GroundBlend.hlsl`
- `Art/HealingHouse/QualityV3/Placement.json`
- `Art/HealingHouse/QualityV3/Props.json`
- `Art/HealingHouse/Source/HealingHouse_QualityV3.blend`
- `Art/HealingHouse/Textures/QualityV3/T_HH_PaintedTerracotta.png`
- `Art/HealingHouse/Textures/QualityV3/T_HH_PaintedTerracotta.prompt.json`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Ceramic.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Cream.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Glass.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Metal.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Plaster.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Roof.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Sage.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Stone.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Timber.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Fade_Wood.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Flower.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_FlowerCream.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Leaf.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_LeafDark.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_LeafLight.uasset`
- `Content/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Metal.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Bench.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Bookcase.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_BroadHerb.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Chimney.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_CounterStepped.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_DoorFrame.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_FlowerPlant.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_GuardianSign.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_HangingHerb.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_HerbBundle.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_HerbShelf.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_HerbTable.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_LanternHook.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_LeafPlant.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_NarrowHerb.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Roof_Entry.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Roof_Main.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Roof_Porch.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Roof_Trim.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Stone_CameraSide.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Stone_Far.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Stone_Front.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Table.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Timber_CameraSide.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Timber_Entry.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Timber_Far.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Timber_Front.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_TrailingHerb.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_TreatmentBedLarge.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_TreatmentBedSmall.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_WindowPlanter.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Windows_CameraSide.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Windows_Far.uasset`
- `Content/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_Windows_Front.uasset`
- `Content/Environment/HealingHouse/QualityV3/Textures/T_HH_PaintedTerracotta.uasset`
- `Docs/HEALING_HOUSE_ART_QUALITY_V3_PRUEFBERICHT.md`
- `Tools/Blender/BuildHealingHouseQualityV3.py`
- `Tools/Blender/ReviewExportHealingHouseQualityV3.py`
- `Tools/DressHealingHouseQualityV3.py`
- `Tools/ImportHealingHouseQualityV3.py`
- `Tools/RefineHealingHouseQualityV3.py`
- `Tools/TestHealingHouseQualityV3PIE.py`
- `Tools/ValidateHealingHouseQualityV3.py`

## Git-Abschluss und nächster Sicherungspunkt

`git diff --check`: bestanden, keine Ausgabe. `git status --short`:

```text
 M Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Earth.uasset
 M Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_ForecourtBlend.uasset
 M Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass.uasset
 M Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend.uasset
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp
?? Art/HealingHouse/Exports/QualityV3/
?? Art/HealingHouse/QualityV3/
?? Art/HealingHouse/Source/HealingHouse_QualityV3.blend
?? Art/HealingHouse/Textures/QualityV3/
?? Content/Environment/HealingHouse/QualityV3/
?? Docs/HEALING_HOUSE_ART_QUALITY_V3_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseQualityV3.py
?? Tools/Blender/ReviewExportHealingHouseQualityV3.py
?? Tools/DressHealingHouseQualityV3.py
?? Tools/ImportHealingHouseQualityV3.py
?? Tools/RefineHealingHouseQualityV3.py
?? Tools/TestHealingHouseQualityV3PIE.py
?? Tools/ValidateHealingHouseQualityV3.py
```

Nichts gestaged, kein Commit, kein Push. Ein sinnvoller Sicherungspunkt ist nach Harrys visueller Prüfung. Nur dann bei weiterhin unverändertem Dateiumfang gezielt stagen:

```sh
git add -- \
  Content/Maps/Dev_HealingHouseTestMap.umap \
  Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass.uasset \
  Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Earth.uasset \
  Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend.uasset \
  Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_ForecourtBlend.uasset \
  Content/Environment/HealingHouse/QualityV3 \
  Art/HealingHouse/Exports/QualityV3 \
  Art/HealingHouse/QualityV3 \
  Art/HealingHouse/Source/HealingHouse_QualityV3.blend \
  Art/HealingHouse/Textures/QualityV3 \
  Source/PokeMonster/Tests/PokeMonsterHealingHouseTest.cpp \
  Tools/Blender/BuildHealingHouseQualityV3.py \
  Tools/Blender/ReviewExportHealingHouseQualityV3.py \
  Tools/ImportHealingHouseQualityV3.py \
  Tools/DressHealingHouseQualityV3.py \
  Tools/RefineHealingHouseQualityV3.py \
  Tools/ValidateHealingHouseQualityV3.py \
  Tools/TestHealingHouseQualityV3PIE.py \
  Docs/TECHNIK.md \
  Docs/ENTSCHEIDUNGEN.md \
  Docs/HEALING_HOUSE_ART_QUALITY_V3_PRUEFBERICHT.md
git diff --cached --stat
```

Diese Befehle wurden nicht ausgeführt. Lokale Saved-Reviews und Testspielstände gehören nicht in den Commit. Nach diesem Bericht keine weitere Gestaltung; auf Harrys Sichtprüfung warten.
