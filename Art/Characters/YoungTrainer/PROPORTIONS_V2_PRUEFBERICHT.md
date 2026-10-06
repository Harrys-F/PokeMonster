# Young Trainer – Proportions- und Silhouettenpass V2

## Ergebnis und Grenzen

Die bestehende Figur wurde ausschließlich an ihren Formen, Volumen und Positionen korrigiert. Die Gesamtproportionen liegen näher am Turnaround: kürzerer Oberkörper oberhalb des Gürtels, schmalere Schulteransätze, stärker betonte Knievolumen, größere Stiefel und Hände sowie ein größerer, flacherer und tiefer sitzender Rucksack. Die Figur ist weiterhin 1,40 m hoch, steht im Ursprung und hat ihre Sohlen auf Z = 0.

Front, beide Seiten, Rückseite, vier Dreiviertelansichten und zwei erhöhte Blickwinkel wurden überprüft. Die Formen funktionieren als dreidimensionaler Blockout. Das ist **keine vollständige visuelle Übereinstimmung und keine Freigabe für die Detailphase**: Die Haare bleiben zu gleichmäßig und wellenartig, Kleidung und Rucksack zu konstruktiv/kantig und das Gesicht nur ein vorhandener Platzhalter.

Ausgangs-HEAD: `eafab5b Complete healing house art quality V3`. Zu Beginn war `Art/Characters/` bereits untracked; die vorhandenen 21 Charakterdateien wurden erhalten. Keine Änderungen an getrackten Projektdateien, Unreal, Gameplay oder anderen Bereichen. Kein Commit, kein Push, nichts gestaged.

## Quellen und Sicherung

- Korrigierte Quelle: `Source/YoungTrainer_Proportions_V2.blend`
- Unveränderte bisherige Quelle: `Source/YoungTrainer_Reference_V1.blend`
- Zusätzliche bytegleiche Sicherung: `Source/Stages/06_PreProportions.blend`
- Ausgangsdatei und Sicherung: SHA-256 `985784203c7e346b4b6a4a0e1053bbc955b1dd0c5764d47cb3eb49def819b22b`

Die neue Blenderdatei wurde gespeichert und erfolgreich wieder geöffnet. Alle acht Referenzen sind gepackt; die neuen PNG-Dateien bleiben zusätzlich als nachvollziehbare Quellen erhalten. Die vorletzte automatisch angelegte `.blend1` liegt unter dem ignorierten `Saved/YoungTrainerProportions/Backups/`, nicht zwischen den versionierungswürdigen Quellen. Es wurde keine bestehende Nutzerdatei gelöscht.

## Referenzen direkt in Blender

`REF_CHARACTER` enthält acht Image Empties: Front, FrontRight, Right, BackRight, Back, BackLeft, Left und FrontLeft. Es sind unveränderte rechteckige Ausschnitte des gelieferten Sheets, ohne Neuzeichnung, Spiegelung oder unterschiedliche Breiten-/Höhenskalierung.

Gemeinsame Kalibrierung: Vorderansicht Haarspitze Y = 103 px, Bodenlinie Y = 494 px; 391 px entsprechen 1,40 m. Daraus folgen **0,00358056266 m/px**. Alle Ausschnitte verwenden diesen einen Maßstab. Die dargestellten Ansichten sind Illustrationen, keine exakt vermessenen CAD-Projektionen; anatomische Punkte unter Kleidung wurden geschätzt. Die Unsicherheit einzelner Landmarken liegt ungefähr bei 3–8 px bzw. 1,1–2,9 cm.

Die Referenzen stehen vertikal, sind auf derselben Bodenlinie ausgerichtet und mit 40 % Deckkraft über dem Modell sichtbar. Position, Rotation und Skalierung sind gesperrt; Auswahl ist deaktiviert. Sie erscheinen nur orthografisch und entlang der jeweiligen Referenzachse. Die schwarze Umrandung nicht frontal betrachteter Empties ist eine Blender-Hilfsdarstellung und keine Modellgeometrie.

Die Figur blickt nach −Y. Deshalb sieht Blender **Right Orthographic** von +X die anatomisch linke Seite und verwendet die mit „LINKS“ bezeichnete Sheet-Ansicht. Die anatomisch rechte Referenz wird von −X betrachtet. Der Rucksack und die Ausrüstung wurden nicht durch Spiegeln der Bilder auf die falsche Seite gebracht.

## Festgestellte Abweichungen und Korrekturen

Der alte Kopf war nicht pauschal zu klein. Seine untere Kontur saß zu tief; die Augen lagen zu hoch und das Seitenprofil war zu kugelig/tief. Eine blinde Kopfvergrößerung hätte diese Fehler verstärkt. Der Kopf wurde deshalb in seiner Form korrigiert: Kinn angehoben, Augen nach unten versetzt, Schädelprofil abgeflacht, Kopfbreite leicht reduziert. Das große stilisierte Kopf-/Haar-Verhältnis bleibt erhalten. Es wurden keine neuen Gesichtsdetails gebaut.

Die Haarhülle war besonders seitlich zu tief, mit weit abstehenden Stirnspitzen. Das vorhandene Volumen wurde abgeflacht, die Hülle leicht unregelmäßiger gemacht und die vorderen Enden näher an die Gesamthülle gebracht. Keine zusätzlichen Strähnen oder Locken wurden erzeugt. Die vorhandene glatte/wellenartige Grundform bleibt eine erkennbare Abweichung zur lockigen Referenz.

Der Bereich zwischen Schultern und Gürtel war zu lang und breit. Schulteransätze wurden nach innen verlegt; Brustkorb und Rückentiefe reduziert, die Taille höher platziert. Die Weste behält ihre längeren unteren Schöße. Ärmel und Unterarme folgen der kompakteren A-Pose; Hände sind 10 % größer und tiefer positioniert. Knochen und Knochenpose bleiben unverändert.

Die Hose wirkte in allen Hauptansichten zu gleichmäßig röhrenförmig. Ihre Hülle wurde an Hüfte/Oberschenkel verschmälert und am Knie aufgebauscht; seitlich variiert die Tiefe und die Kniezone tritt etwas vor. Der Saum sitzt höher. Es wurde keine zusätzliche Faltengeometrie erzeugt. Die Stiefel wurden breiter, länger, höher und leicht nach außen gedreht, bei unverändertem Sohlenkontakt.

Der Rucksack wirkte seitlich zu tief und insgesamt wie ein kurzer Kasten. Er ist nun breiter, höher, flacher und tiefer am Rücken. Eine gemeinsame Hüllkorrektur hält vorhandene Taschen und Riemen zusammen. Die Bettrolle sitzt tiefer. Die verbleibende kantige Konstruktion wurde nicht durch zusätzliche Details kaschiert.

## Vermessung

Alle folgenden Bounds sind tatsächliche Grenzen der Mesh-Koordinaten der aktiven Formkeys. Kopfwerte schließen Haare aus; Rucksackwerte schließen vorhandene Seitentaschen und den Griff ein. Bei beiden Stiefeln umfasst die gemeinsame Breite auch den Abstand der Füße.

| Merkmal | V1 | V2 |
|---|---:|---:|
| Gesamthöhe | 140,00 cm / 1,400 m | 140,00 cm / 1,400 m |
| Kinn, niedrigster Kopfpunkt | 103,19 cm / 1,032 m | 107,11 cm / 1,071 m |
| Höchster Schädelpunkt | 133,10 cm / 1,331 m | 132,02 cm / 1,320 m |
| Kopfbreite | 30,54 cm / 0,305 m | 29,38 cm / 0,294 m |
| Kopftiefe | 28,52 cm / 0,285 m | 23,39 cm / 0,234 m |
| Haarbreite | 41,67 cm / 0,417 m | 40,02 cm / 0,400 m |
| Haartiefe | 38,09 cm / 0,381 m | 31,47 cm / 0,315 m |
| Augenbereich, Mitte der gemeinsamen Z-Bounds | 120,74 cm / 1,207 m | 117,97 cm / 1,180 m |
| Tiefste Fingerspitze | 57,73 cm / 0,577 m | 52,90 cm / 0,529 m |
| Handsilhouette, gemeinsame vertikale Ausdehnung | 12,46 cm / 0,125 m | 13,71 cm / 0,137 m |
| Hosensaum, tiefster Punkt | 22,67 cm / 0,227 m | 27,37 cm / 0,274 m |
| Gemeinsame Hosenbreite | 41,79 cm / 0,418 m | 46,87 cm / 0,469 m |
| Stiefelhöhe | 17,45 cm / 0,175 m | 20,70 cm / 0,207 m |
| Gemeinsame Stiefelbreite | 36,40 cm / 0,364 m | 45,52 cm / 0,455 m |
| Stiefelausdehnung in Y | 22,90 cm / 0,229 m | 25,59 cm / 0,256 m |
| Vorderste Stiefelkante relativ zur Körperachse | 15,10 cm / 0,151 m | 16,86 cm / 0,169 m |
| Rucksackbreite | 37,20 cm / 0,372 m | 44,29 cm / 0,443 m |
| Rucksacktiefe | 25,15 cm / 0,252 m | 15,68 cm / 0,157 m |
| Rucksackhöhe | 38,73 cm / 0,387 m | 43,76 cm / 0,438 m |
| Unterkante Rucksack | 66,70 cm / 0,667 m | 60,11 cm / 0,601 m |

Die Formkorrektur nutzt Schulteransätze bei Z = 102 cm, Ellenbogen bei 80,3 cm, Handgelenke bei 65 cm und eine Gürtelausrichtung um 73,5 cm. Die Kniehülle wird um Z = 41,2 cm betont. Diese Werte beschreiben die korrigierten Mesh-Formen und ihre Deformationsanker, **nicht verschobene Rig-Gelenke**.

Zusätzlich wurden Halsansatz, Brustkorb, Taille, Hüfte, Schritt, Knöchel und Sohlen in den registrierten Vorder-/Seitenüberlagerungen kontrolliert. Hüfte und Schritt sind unter der Kleidung nicht exakt messbar; hier wurde die sichtbare Hülle verglichen, ohne unveränderte Rig-Knochen als neue anatomische Messwerte auszugeben.

Die Referenz liefert ungefähr 106,7 cm Kinnhöhe, 117,4 cm Augenhöhe, 100,6 cm Schulterhöhe, 75,2 cm Taille, 39,7 cm Kniehöhe und 20,4 cm Knöchelhöhe. Die neutral gespreizten Arme des Modells entsprechen absichtlich nicht der entspannten Armhaltung des Sheets; Ellenbogen-/Handpositionen lassen sich deshalb nicht deckungsgleich beurteilen. Die Illustrationen wechseln außerdem einzelne Ausrüstungsdetails zwischen den Ansichten.

## Mehransichten- und Silhouettenkontrolle

- Front: Taille und Handhöhe liegen näher an der Referenz, Knievolumen und größere Stiefel sind besser erkennbar. Der Kopf bleibt groß, ohne pauschale Vergrößerung. Ärmel/Kleidung wirken weiterhin einfacher und kantiger als die Illustration.
- Beide Seiten: geringere Kopf-/Haartiefe und deutlich flacherer Rucksack; keine extreme seitliche Ausladung wie vorher. Gesichtsvorsprung und Haarabschluss bleiben vereinfacht.
- Rückseite: größere, tiefer liegende Rucksackfläche sowie ausgeprägtere Knie-/Stiefelsilhouette. Die Hülle ist plausibler, bleibt jedoch zu kastenförmig.
- Vier Dreiviertelansichten: die Korrekturen funktionieren zusammen, keine auf eine einzelne Ansicht beschränkte flache Verformung. Einzelne vorhandene Haarenden und Riemen bleiben konstruktiv sichtbar.
- Erhöhte Spielansicht: zusätzlich bei 30° und 40° Elevation geprüft. Großer Kopf, kompakter Rumpf, Knievolumen, große Stiefel und großer Rucksack lesen sich deutlich. Die Kontrolle wurde am gelieferten Abschnitt „PERSPEKTIVE (WIE IM SPIEL)“ verglichen. Das ist eine Blender-Formprüfung, keine Änderung oder exakt kalibrierte Reproduktion einer Unreal-Spielkamera.

Reviewbilder liegen unter dem ignorierten `Saved/YoungTrainerProportions/Review/`: `FrontSide_Comparison.jpg`, `BackLeft_Comparison.jpg`, `V2_Reference_8Directions.jpg`, `V2_Silhouette_8Directions.jpg`, `V2_ThreeQuarter_Game.jpg`, `GamePerspective_Comparison.jpg` sowie vier registrierte Überlagerungen. Links/Referenz, Mitte/V1 und rechts/V2 in den Hauptvergleichsbildern verwenden denselben Pixel-/Weltmaßstab. Die Bilder sind aus nativen Blender-Renderings und unveränderten Referenzausschnitten zusammengesetzt.

## Nicht destruktive Umsetzung und Prüfungen

Alle 20 Meshes besitzen `Basis` und `Proportions_Silhouette_V2`. `Basis` entspricht weiterhin exakt der alten Geometrie; die Korrektur ist auf 1 aktiv. Materialverbindungen, Shaderwerte, UV-Koordinaten, Gewichte, Topologie, Objekttransformationen, Parent-Beziehungen, 32 Knochen einschließlich Restmatrizen und Pose sowie vorhandene Actions sind gegenüber V1 gleich geblieben. Es wurden keine Keyframes oder Animationen hinzugefügt. Die ursprüngliche Szene mit Cube, Camera und Light ist unverändert.

Das bestehende Rig wurde ausdrücklich **nicht angepasst**. Nach den Formänderungen liegen seine Gelenke teilweise nicht mehr an den passenden neuen Positionen. Animationsfähigkeit wurde in diesem Pass deshalb nicht bestätigt; ein später ausdrücklich freigegebener Rig-Abgleich wäre vor weiteren Animationstests nötig.

`Authoring/ValidateProportions.py` öffnet V1 und V2 ausschließlich lesend und vergleicht die geschützten Daten. Ergebnis: **PASS**. Alle 20 Meshes: keine flächenlosen Polygone, keine offenen oder nicht-manifold Kanten; endliche Koordinaten. Alle acht Referenzen: gepackt, vertikal, einheitlicher Maßstab, gesperrt, 40 % Deckkraft. Die 20 vom bisherigen Manifest erfassten Dateien sind weiterhin bytegleich; dessen eigene Datei wurde ebenfalls nicht bearbeitet. V1 und die zusätzliche Sicherung sind bytegleich. Die neue Quelle wurde sowohl im laufenden Blender als auch im unabhängigen Prüfprozess wieder geöffnet.

`git diff --check` ohne Ausgabe; zusätzliche Prüfung der neuen Markdown-/Python-/JSON-Dateien auf Syntax und überflüssige Leerzeichen durchgeführt. Unreal-Build, PIE und Unreal-Automation wurden nicht ausgeführt, da keinerlei Unreal-Dateien verändert oder importiert wurden. Rig-/FK-Tests wurden bewusst nicht ausgeführt, damit das bestehende Rig nicht verändert wird.

## Neue Dateien dieses Passes

- `Source/YoungTrainer_Proportions_V2.blend`
- `Source/Stages/06_PreProportions.blend`
- `Reference/Orthographic/Alignment.json`
- `Reference/Orthographic/Front.png`
- `Reference/Orthographic/FrontRight.png`
- `Reference/Orthographic/Right.png`
- `Reference/Orthographic/BackRight.png`
- `Reference/Orthographic/Back.png`
- `Reference/Orthographic/BackLeft.png`
- `Reference/Orthographic/Left.png`
- `Reference/Orthographic/FrontLeft.png`
- `Authoring/ProportionLandmarks.json`
- `Authoring/CorrectProportions.py`
- `Authoring/RenderProportions.py`
- `Authoring/CompareProportions.py`
- `Authoring/ValidateProportions.py`
- `PROPORTIONS_V2_PRUEFBERICHT.md`
- `PROPORTIONS_V2.json`

Abschließender Kurzstatus: `?? Art/Characters/`. Keine getrackten Änderungen, keine gestagten Dateien. Die genannten 18 neuen Dateien kommen zu den bereits vorhandenen 21 untracked Charakterdateien hinzu.

## Stoppunkt

Der Proportions-/Silhouettenpass endet hier. Kein finales Gesicht, keine finale Haarmodellierung, keine weiteren Accessoires, keine UV- oder Materialarbeit, kein Rigging, keine Animation, kein Export und kein Unreal-Import. Die verbliebenen Formabweichungen wurden nicht durch Details kompensiert.

Nach einer visuellen Freigabe wäre die neue Quelle ein sinnvoller Git-Sicherungspunkt. Folgender Befehl würde ausschließlich die 18 Dateien dieses Passes stagen; er wurde **nicht ausgeführt**. Die bereits vorhandenen 21 untracked Ausgangsdateien sind darin nicht enthalten und müssten für einen eigenständig reproduzierbaren späteren Commit ebenfalls bewusst geprüft und aufgenommen werden.

```sh
git add -- \
  Art/Characters/YoungTrainer/Source/YoungTrainer_Proportions_V2.blend \
  Art/Characters/YoungTrainer/Source/Stages/06_PreProportions.blend \
  Art/Characters/YoungTrainer/Reference/Orthographic \
  Art/Characters/YoungTrainer/Authoring/ProportionLandmarks.json \
  Art/Characters/YoungTrainer/Authoring/CorrectProportions.py \
  Art/Characters/YoungTrainer/Authoring/RenderProportions.py \
  Art/Characters/YoungTrainer/Authoring/CompareProportions.py \
  Art/Characters/YoungTrainer/Authoring/ValidateProportions.py \
  Art/Characters/YoungTrainer/PROPORTIONS_V2_PRUEFBERICHT.md \
  Art/Characters/YoungTrainer/PROPORTIONS_V2.json
```
