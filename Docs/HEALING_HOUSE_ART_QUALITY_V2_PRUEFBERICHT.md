# Healing House – Art Quality V2 + Natural Ground Pass

Stand: 2026-10-05. Visueller Qualitäts-Prototyp; Harrys Sichtfreigabe steht aus.

## 1. Ausgangsstand und Umfang

Sauberer Ausgangs-HEAD: `0d656cf Add healing house expanded interior art V1`. Art V1 war committed. Ausschließlich eigene V2-Artassets, unmittelbarer Boden/Vorplatz und Einrichtung in `Dev_HealingHouseTestMap` sowie zugehörige Autorenwerkzeuge/Dokumentation. Kein C++, kein Build erforderlich, keine neue Gameplayfunktion, keine Staging-/Commit-/Push-Aktion.

Raum 12 × 10 m, Außenheilhaus 9 × 9,3 m, Heilerinposition, Relocation, Türschwellen und Maske bleiben erhalten. Außenkamera 2500 cm / FOV 35° / Pitch −55° / Yaw −45°, innen 2600 cm / 35° / −50° / lokaler Yaw 0°. Lag, 140-cm-Player, Sprites/Pivots, acht Richtungen, 210 cm/s und Interaktionsreichweite bleiben unverändert. Die bestehenden 107 Occluder bleiben in derselben Reihenfolge; nur Dach/Front verschwinden, beide Seiten und Rückwand bleiben sichtbar.

## 2. Möbelüberschneidungen

Drei Regale wurden zusammen mit ihrem vollständigen Bestand versetzt; keine Regale oder Originalassets gelöscht. Insgesamt 48 bestehende Möbel-/Stock-Actors verschoben. Weltkoordinaten in cm:

| Regal | Vorher | Nachher | Korrektur |
|---|---|---|---|
| `HH_V3_HerbShelf` | (20395, −505, 0) | (20290, −450, 0) | vom linken Fensterbereich in eine freie Wandzone |
| `HH_Art_RearApothecary_0` | (20460, −350, 0) | (20400, −290, 0) | vor die rückwärtige Wand-/Balkenebene |
| `HH_Art_RearApothecary_1` | (20460, 420, 0) | (20400, 295, 0) | aus dem rückwärtigen Fenster-/Balkenbereich |

Die drei gesamten Regal-Bounds überschneiden sich nachher mit keinem der Seiten-/Rückwandmodule oder zugehörigen Balken. Beide hinteren Regale enden bei X ≈ 20423 cm; die vorderste relevante Rückwand-Bay beginnt bei X ≈ 20463 cm. Die Rückenabstände sind Möbelabstände, keine vorgesehenen Durchgänge. Freier Umgang vor den Regalen wurde tatsächlich zu Fuß geprüft. Weitere vergleichbare störende Überschneidungen wurden in den Rundgang-Aufnahmen nicht gefunden. Dekoration auf Möbeln, Teppichmotive und architektonische Anschlüsse sind beabsichtigte Überlagerungen.

## 3. Verbesserung gegenüber Art V1 und Referenzvergleich

Die Referenz bleibt das stilistische Ziel: gepflegter warmer Putz, kräftige Holzmaserung, unregelmäßiger Naturstein, weiche grün-/erdige Stoffe, Pflanzen in Gruppen, weiche Lichtinseln und natürlich eingewachsener Weg. Keine Fotos, Pixel-Art oder fotorealistische Mikro-PBR-Struktur.

V1 hatte überwiegend einfache Farbflächen mit einer gemeinsamen kleinen Oberflächentextur. V2 verwendet sechs eigene gemalt wirkende Texturen, eigene Materialtöne, fein überarbeitete vorhandene Formen und echte kleine Grascluster. Empfang, Kamin/Sitzgruppe, Kreaturenliegen, Behandlung und Laufzonen bleiben am selben Ort.

**Sichtbare Qualitätsgrenzen gegenüber der Referenz:** Architektur und Möbel bleiben geradliniger; Pflanzen und Gefäße sind weiterhin einfacher modellierte Props. Die Referenz besitzt wesentlich reichere handgezeichnete Ornamente, subtilere Kontakt-/Lichtmodellierung, mehr unterschiedlich gestaltete Kräuter und räumliche Einzelheiten. Die äußere Fassaden-/Dachgestaltung bleibt V3; dieser Pass konzentriert sich außen auf Boden und Nahumgebung. Bodentexturen können auf großen freien Flächen noch als Wiederholung erkannt werden. Der Testboden endet weiterhin an der vorhandenen Mapgrenze. V2 ist eine deutliche Oberflächenverbesserung, noch keine finale Referenzqualität.

## 4. Holz

Eigene gemalte Maserung mit breiten Strichen, Knoten, dunkleren Vertiefungen und warmer Farbvariation. Gemeinsame Textur für Holz, helle/dunkle Holztöne und Fachwerk; keine identische flache braune Fläche mehr. Die Tonabstände des Bodens wurden aus der echten Spielkamera reduziert, um große Schachbrettfelder zu vermeiden. Die bestehenden Bodendielen erhalten passende Maserungs-UVs und kleine Kantenunregelmäßigkeiten. Tresen, Bank und Kaminholz werden als Ableitungen der vorhandenen V1-Formen verfeinert; Regale/Tische behalten ihre bestehenden Meshes und profitieren von Materialüberschreibungen.

## 5. Naturstein

Warme Grau-/Brauntöne mit gemalten Strukturflächen. Kamin und Innensockel erhalten moderat unregelmäßige einzelne Steinformen; Größenvariation bis ungefähr 1,8 %, kleine Positionsabweichungen und bestehende dunkle Mörtelfugen. Silhouetten und Funktion bleiben erhalten. Kleine Außensteine verwenden denselben Steincharakter.

## 6. Putz

Eigenes helles warmes Putzbild mit dezenter gemalter Fleckigkeit und Strichstruktur. Gepflegter Eindruck; keine schmutzige Ruinenwand. Materialüberschreibungen bleiben auf den sichtbaren Seiten-/Rückwandbereichen des Expanded-Raums. Die bestehenden maskierten Dach-/Frontmaterialien werden nicht ersetzt.

## 7. Möbelqualität

Sechs geänderte Formvarianten auf Basis vorhandener Meshes: Dielenmodul, Empfangstresen, Kamin, Bank, Steinsockel und Kissen. Vorhandene Bevels bleiben; kleine Formabweichungen vermeiden völlig gleiche Kanten. Bestehende Tische, Regale, Liegenrahmen und Behandlungsutensilien werden weiterverwendet. Kein neues Raumlayout und keine automatische komplette Möbelersetzung. Alte Quellen/FBX-/Unreal-Assetdateien bleiben bytegleich.

## 8. Stoffe und Liegen

Gedämpfter Salbeigrün-Stoff, warme helle Kissen, dezente breite Falten. Ein zunächst zu starkes wiederholtes Stoffmuster wurde aus der Spielkamera zurückgenommen: 1× UV-Wiederholung und nur 22 % Texturanteil gegenüber der ruhigen Grundfarbe. Zwei zusätzliche wiederverwendbare Deckengeometrien auf den vorhandenen Liegen erzeugen eine weich gewölbte Oberfläche und leicht fallende Seiten. Kein neuer Liegenblocker; bestehende Nutzungsmaße bleiben erhalten.

## 9. Innenbeleuchtung

Die vier vorhandenen lokalen Art-V1-Lichter werden fein abgestimmt: Kamin 9 → 11, Warten 3,5 → 3, Empfang 4 unverändert, Behandlung 3,5 → 3. Quellradius 65 cm. Weiterhin schattenlos; keine neuen teuren Schattenlichter. Die beiden ursprünglichen Innenlichtquellen und Außenbeleuchtung bleiben unverändert. Der vorhandene räumlich begrenzte Innen-Postprocess erhält Belichtungsbias −0,7 → −0,55 und Kontakt-AO 0,5/90 → 0,8/60. Keine Änderung an CameraComponent, FOV oder globaler Beleuchtung. Kamin und Laternen bilden warme Inseln; Fenster-/Grundlicht bleibt dezent.

## 10. Grasboden

Eigene gemalte Grass-/Erdtextur statt homogener grüner Fläche. Grüntöne mit trockenen/erdigen Flecken, mittlere Strukturmaßstäbe von 190 cm; leichte Entsättigung und ruhigere Tönung nach Spielkamera-Review. Weltkoordinaten halten dieselbe Grasprobe auf Grundfläche, Wegkanten und Vorplatz zusammen. Originale Ground-Geometrie und Kollision unverändert.

## 11. Natürlicher Weg und Vorplatz

14,3 m langes flaches Wegband, 73 Konturstationen und 9 Querproben, 1152 Dreiecke, Breite ungefähr 184–263 cm. Leichte Kurve und wechselnde Breite, weiche unregelmäßige Übergänge von Erde zu identischem Gras; Mitte etwas stärker abgetreten. Opaker Materialblend statt Transparenzflächen. Der alte gerade `ApproachPath` bleibt verborgen als nicht kollidierender Fallback erhalten. Der bestehende Vorplatz behält seine Geometrie, erhält aber einen erdig gerundeten, zum Gras auslaufenden Materialbereich.

## 12. 3D-Grassystem

Ein generischer Actor mit sechs nativen HISM-Komponenten, keine neue C++-/Gameplayklasse. 321 persistente Instanzen:

| Modul | Instanzen | Dreiecke je Mesh |
|---|---:|---:|
| GrassSmall | 120 | 54 |
| GrassMedium | 116 | 108 |
| GrassLarge | 14 | 168 |
| MeadowHerbs | 49 | 112 |
| PebbleSmall | 14 | 80 |
| PebbleCluster | 8 | 80 |

Echte leicht gebogene, zugespitzte Blattflächen; Rotation, Skalierung und drei Grünvarianten. Gruppen entlang der Wegkante, bei bestehenden Pflanzen/Steinen und am Hausrand. Türpassage und Wegmitte bleiben frei. Keine flächendeckende Halmsimulation.

## 13. Bodendetails

49 Kräuter-/Blumengruppen sowie 22 kleine Stein-/Steingruppen-Instanzen ergänzen Gras in unregelmäßigen Gruppen. Bestehende Pflanzen bleiben erhalten. Keine zufällige Dekoflut und keine Kollision auf diesen Details.

## 14. Wiederverwendbarkeit für Westland

Gemeinsame Assets unter `/Game/Environment/Westland/NaturalGroundV1`: Gras/Erde, Gras-/Kräuter-/Steinmodule sowie Weg- und Vorplatzblend. Die sechs Cluster sind getrennte FBX-Dateien. Das Instanzlayout liegt als cm-/Seed-JSON vor. Wegmaterial erwartet ein UV-Band 0–1 und Welt-XY für Bodenstruktur; ein anderer Weg kann seine eigene Kontur verwenden. Der Vorplatz bietet `CourtCenter_cm` und `CourtHalfSize_cm` zur Anpassung per Materialinstanz. Keine Abhängigkeit von einem Healing-/Encounter-Actor. Die Steine teilen bewusst das eigene V2-Steinmaterial; diese Content-Abhängigkeit ist beim Wiederverwenden mitzunehmen. Westland Village wurde nicht verändert.

## 15. Performance und Quellen

Sechs HISM-Komponenten statt 321 einzelne Actors; keine Ticklogik oder Player-Collision auf Vegetation. Insgesamt 28608 instanzierte Detaildreiecke, dazu 1152 Wegdreiecke. Gras opak/zweiseitig, ohne dynamische Schatten oder Alpha-Overdraw. Distanz-Culling 3200–4300 cm. Mehrere Materialsektionen pro Cluster bedeuten, dass sechs Komponenten nicht pauschal sechs Draw Calls entsprechen. Keine Behauptung einer vollständigen M4-Performance-Zertifizierung; ein großes Village-Szenario wurde nicht profiliert.

Sechs source PNGs mit 1254² Pixeln; in Unreal maximal 1024, Power-of-Two-Stretch, Mips und Streaming. Keine 4K-Texturen oder zusätzliche Normal-/Height-Maps. Eigene Texturen mit eingebautem Imagegen erzeugt; Prompts/Destinationen sind in `Art/HealingHouse/QualityV2/TexturePrompts.json` dokumentiert. Keine externen Downloads/Marketplace-Assets oder Plugins.

Blenderquelle gespeichert, erneut geöffnet, UVs/Materialslots/Flächen und Maße geprüft, SourceReview visuell geprüft und **erst danach** 13 FBX-Dateien exportiert:

`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/HealingHouse/Source/HealingHouse_QualityV2.blend`

## 16. Vollständiger Fußtest

Bestanden: über den neuen Weg und Vorplatz hinein → Empfang/Heilerin → Sitz-/Kaminbereich → Behandlung und beide Liegen → entlang beider Seitenwände und der Rückwand → hinaus → diagonal erneut hinein und hinaus. 2 Eintritte, 2 Austritte, keine Fehler im finalen Routenprotokoll, 21 echte Spielkamera-Aufnahmen. Bewegung ausschließlich über normale Enhanced-Input-Richtungen; keine Test-Teleports. Die bestehende reguläre Relocation beim Türübertritt bleibt aktiv.

Player blieb bei allen geprüften Wand-/Möbelzonen sichtbar; freie Wege und diagonale Passage ohne neue Blockade. Dach/Front verschwinden, Seiten-/Rückwände bleiben. Übergangsmaske und Innensteuerung unverändert; gemessene maximale Geschwindigkeit 210 cm/s. Frühere Probeläufe hatten ungeeignete Wegpunkte zu nahe an vorhandenen Möbeln; korrigiert wurde die Prüfroutenführung, nicht die Gameplay-Collision.

Für die Heilerinprobe wurden die beiden Testteammitglieder vorübergehend auf 0/52 und 15/47 HP sowie verringerte PP gesetzt. Danach vollständig geheilt, alle bekannten PP voll, Checkpoint `Dev_HealingHouse` bei (20328,997; −3,627; 50,150) cm aktiviert und Dev-Speichern erfolgreich. Der zuvor gesicherte ursprüngliche Nutzer-Dev-Spielstand wurde nach allen Prüfungen bytegleich wiederhergestellt; das lokale Testsave bleibt nur als Nachweis unter `Saved/HealingQualityV2/TestDevSave.sav`. Healing-/Save-Code wurde nicht geändert.

## 17. Tests / Map Check

- Vollständiger vorhandener `PokeMonster`-Automationbestand in einer frisch gestarteten separaten Editorinstanz: **38/38 erfolgreich**, kein fehlgeschlagener Test. Darunter Player-Foundation, HealingHouse, Expanded Interior/Cutaway, Battle, Creature, Encounter, Items, Save, Quest und Overworld-UI. Ergebnisliste: `Saved/HealingQualityV2/AutomationResults.json`.
- Finaler Map Check: **0 Fehler / 0 Warnungen**.
- Geometrie-/Material-/Missing-Asset-/Collision-Audit bestanden: 482 Mapactors, 36 eigene neue Unrealassets, keine fehlenden Assets; alle ursprünglichen Collision-Profile/Enabled-Werte erhalten. Originale Occluder-Liste weiterhin 107 in identischer Reihenfolge. Drei Regal-Bounds ohne Überschneidung mit Seiten-/Rückwandarchitektur. Nach Speichern und Wiederöffnung HISM-Instanzen, UVs und Materialgraphen vorhanden.
- Blenderquelle erneut geöffnet: 13 Meshobjekte, Geometrie, UVs, Materialslots und Dimensionen geprüft. Eigene Modelle exportiert und importiert; Originale unverändert.
- Sieben neue Python-Autoren-/Prüfwerkzeuge syntaktisch geprüft. Kein C++ geändert, deshalb kein Build erforderlich.

Während der visuellen Iteration gefundene Fehler wurden vor dem finalen Durchgang korrigiert: Wegnormalen aufwärts, tatsächlicher Sample-Pin `UVs`, korrekter Desaturation-Eingang sowie beide Custom-Blend-Eingänge. Der zunächst harte Vorplatz und zu unruhige Stoff wurden entsprechend verfeinert. Der finale Lauf und die frisch geladene Map sind die maßgeblichen Nachweise.

Der frische Editorlog enthält 17 `Condition failed`-Meldungen vor Beginn des Projekt-Testlaufs sowie SDK-Hinweise für nicht verwendete Plattformen; die Projekt-Testauswertung weist dennoch eindeutig alle 38 Tests als erfolgreich aus. Deshalb wird kein insgesamt fehlerfreier Engine-Startlog behauptet. Logs bleiben zur Nachprüfung lokal. Es wurde nur die eigene Prüfeditorinstanz gestartet und sauber geschlossen.

## 18. Vollständige neue/geänderte Dateien

Neue Dateien: **67** (23 Art-/Quell-/Exportdateien, 36 Unrealassets, 7 Werkzeuge, 1 Prüfbericht). Bestehende geändert: **3**. Nichts gelöscht. Alle weiteren 738 der 741 Ausgangsdateien sind SHA-256-bytegleich, einschließlich Gameplay/C++, Originalquellen/-Assets und aller anderen Maps.

Geänderte bestehende Dateien:

```text
Content/Maps/Dev_HealingHouseTestMap.umap
Docs/ENTSCHEIDUNGEN.md
Docs/TECHNIK.md
```

Sämtliche neuen Dateien:

```text
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_GrassLarge.fbx
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_GrassMedium.fbx
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_GrassSmall.fbx
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_MeadowHerbs.fbx
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_PebbleCluster.fbx
Art/Environment/Westland/NaturalGroundV1/Exports/SM_WL_NG_PebbleSmall.fbx
Art/Environment/Westland/NaturalGroundV1/HealingApproachLayout.json
Art/Environment/Westland/NaturalGroundV1/Textures/T_WL_PaintedEarth.png
Art/Environment/Westland/NaturalGroundV1/Textures/T_WL_PaintedGrass.png
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_Bench.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_CounterStepped.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_Coverlet.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_Fireplace.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_FloorTile2m.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_Pillow.fbx
Art/HealingHouse/Exports/QualityV2/SM_HH_Q2_StoneWainscot2m.fbx
Art/HealingHouse/QualityV2/Props.json
Art/HealingHouse/QualityV2/TexturePrompts.json
Art/HealingHouse/Source/HealingHouse_QualityV2.blend
Art/HealingHouse/Textures/QualityV2/T_HH_PaintedCloth.png
Art/HealingHouse/Textures/QualityV2/T_HH_PaintedPlaster.png
Art/HealingHouse/Textures/QualityV2/T_HH_PaintedStone.png
Art/HealingHouse/Textures/QualityV2/T_HH_PaintedWood.png
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Linen.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Plaster.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Sage.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Stone.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Timber.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Wood.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_WoodDark.uasset
Content/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_WoodLight.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_Bench.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_CounterStepped.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_Coverlet.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_Fireplace.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_FloorTile2m.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_Pillow.uasset
Content/Environment/HealingHouse/QualityV2/Meshes/SM_HH_Q2_StoneWainscot2m.uasset
Content/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedCloth.uasset
Content/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedPlaster.uasset
Content/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedStone.uasset
Content/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedWood.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Earth.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_FlowerCream.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_ForecourtBlend.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_Grass.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_GrassLeaf0.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_GrassLeaf1.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_GrassLeaf2.uasset
Content/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_GrassLarge.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_GrassMedium.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_GrassSmall.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_HealingApproach.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_MeadowHerbs.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_PebbleCluster.uasset
Content/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_PebbleSmall.uasset
Content/Environment/Westland/NaturalGroundV1/Textures/T_WL_PaintedEarth.uasset
Content/Environment/Westland/NaturalGroundV1/Textures/T_WL_PaintedGrass.uasset
Docs/HEALING_HOUSE_ART_QUALITY_V2_PRUEFBERICHT.md
Tools/Blender/BuildHealingHouseQualityV2.py
Tools/Blender/ReviewExportHealingHouseQualityV2.py
Tools/DressHealingHouseQualityV2.py
Tools/ImportHealingHouseQualityV2.py
Tools/RefineHealingHouseQualityV2.py
Tools/TestHealingHouseQualityV2PIE.py
Tools/ValidateHealingHouseQualityV2.py
```

## 19. Lokale Reviewdateien

Alle Reviewbilder/Protokolle liegen ausschließlich im ignorierten `Saved/HealingQualityV2`. Keine Screenshots oder Logs im Git-Dateisatz. Finale Spielkamera-Aufnahmen unter `FootFinal/Review`:

- `02_Interior00000.png`: Innenraum gesamt, direkt mit Art-V1-`Saved/HealingArt/FootFinal/Review/02_Interior00000.png` vergleichbar.
- `03_Reception00000.png`: Empfang/Heilerin.
- `04_Waiting00000.png`, `05_Fireplace00000.png`: Kamin und Sitzecke.
- `06_Treatment00000.png`, `07_SmallBed00000.png`, `08_LargeBed00000.png`: Behandlung und Kreaturenliegen.
- `09_SidePlusRear00000.png` bis `15_RearMiddle00000.png`: Wand-/Regalzonen und erhaltene Seiten/Rückwand.
- `00A_ExteriorFar00000.png`, `01_Exterior00000.png`: Heilhaus außen.
- `00B_Path00000.png`: neuer Weg.
- `00C_GrassEdge00000.png`: Gras-/Weg-Übergang.
- `16_OutsideAgain00000.png`, `17_DiagonalInside00000.png`, `18_FinalOutside00000.png`: erneuter Ein-/Austritt.

Weitere Nachweise: `Blender/SourceReview.png`, `Blender/SourceAudit.json`, `QualityAudit.json`, `Placement.json`, `CameraRefinement.json`, `FootFinal/PIERoute.json`, `FootFinal/Frames.jsonl` sowie finaler Automation-/Editorlog. Frühe Review-/Prüfversuche bleiben getrennt lokal erhalten und sind nicht die finale Freigabegrundlage.

## 20. Git-/Markdown-Prüfung und Sicherungspunkt

`git diff --check`: erfolgreich, keine Ausgabe. Zusätzlich Markdown und Syntax der sieben neuen Python-Dateien geprüft; alle weiteren Ausgangsdateien bytegleich. Der originale Dev-Spielstand ist bytegleich wiederhergestellt. Git-Index leer; nichts gestaged.

Sinnvoller Sicherungspunkt **nach Harrys visueller Prüfung**, nicht ausgeführt:

```bash
git add -- Art/HealingHouse/QualityV2 Art/HealingHouse/Textures/QualityV2 Art/HealingHouse/Exports/QualityV2 Art/HealingHouse/Source/HealingHouse_QualityV2.blend Art/Environment/Westland/NaturalGroundV1 Content/Environment/HealingHouse/QualityV2 Content/Environment/Westland/NaturalGroundV1 Content/Maps/Dev_HealingHouseTestMap.umap Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/HEALING_HOUSE_ART_QUALITY_V2_PRUEFBERICHT.md Tools/Blender/BuildHealingHouseQualityV2.py Tools/Blender/ReviewExportHealingHouseQualityV2.py Tools/ImportHealingHouseQualityV2.py Tools/DressHealingHouseQualityV2.py Tools/RefineHealingHouseQualityV2.py Tools/ValidateHealingHouseQualityV2.py Tools/TestHealingHouseQualityV2PIE.py
```

Keine automatische visuelle Freigabe, kein Commit oder Push. Weitere Gestaltung erst nach Harrys Sichtprüfung.

## 21. Abschließendes git status --short

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
?? Art/Environment/
?? Art/HealingHouse/Exports/QualityV2/
?? Art/HealingHouse/QualityV2/
?? Art/HealingHouse/Source/HealingHouse_QualityV2.blend
?? Art/HealingHouse/Textures/QualityV2/
?? Content/Environment/HealingHouse/QualityV2/
?? Content/Environment/Westland/
?? Docs/HEALING_HOUSE_ART_QUALITY_V2_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseQualityV2.py
?? Tools/Blender/ReviewExportHealingHouseQualityV2.py
?? Tools/DressHealingHouseQualityV2.py
?? Tools/ImportHealingHouseQualityV2.py
?? Tools/RefineHealingHouseQualityV2.py
?? Tools/TestHealingHouseQualityV2PIE.py
?? Tools/ValidateHealingHouseQualityV2.py
```
