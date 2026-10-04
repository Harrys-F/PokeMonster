# Healing House Expanded Interior – Art & Dressing V1

Stand: 2026-10-04. **Technisch geprüft; visuelle Freigabe durch Harry ausstehend.**

## 1. Ausgangs-HEAD und Status

`78c5e35 Refine expanded interior cutaway`; `git status --short` war vor Beginn leer. Der bereits funktionierende Expanded Interior wurde ergänzt, nicht erneut aufgebaut. Keine Commits, Pushes, Staging- oder Restore-Aktionen.

Alle 676 ursprünglich versionierten Dateien wurden vor Beginn direkt mit SHA-256 erfasst. Am Ende sind davon genau vier verändert: die Heilhaus-Testmap, zwei Dokumentationen und der lesende Expanded-Interior-Auditor. Die übrigen 672 sind bytegleich, darunter sämtliche C++-Dateien, Player-/Sprite-/Gameplayassets, bestehende Blenderquellen, V3-/Kit-Assets und alle anderen Maps.

## 2. Analyse der Bildreferenz

Primär ist die untere große Innenraumdarstellung des beigefügten Bildes. Der Empfang liegt hinten mittig unter einem grünen Symbolbanner, eingerahmt von Regalen mit Flaschen, Büchern, Pflanzen und Heilmaterial. Links liegen Kamin und gemütliche Sitzgruppe, rechts verschieden große Liegen. Heller Putz, dunkle Balken, niedrige Natursteineinfassungen und Holzfußboden rahmen die Einrichtung ein. Warmes Feuer-/Laternenlicht bildet einzelne Lichtinseln. Die höhere Dichte sitzt vor allem an Wänden und Arbeitsflächen; der Weg vom Eingang zum Empfang und zu den Liegen bleibt klar.

Die kleinen Maßstabsfelder geben ca. 45 cm Sitzhöhe, 75 cm Tischhöhe, 80/105 cm Tresen, 60–70 cm Liegen und erreichbare Regalbereiche vor. Sie sind Gestaltungsrichtwerte; die verbindliche 140-cm-Figur und bestehende Technik haben Vorrang. Die in der Bildreferenz größere Tür wurde ausdrücklich nicht auf die vorhandene Tür übertragen.

Vor Umbau wurden V3-Quellen, Props und die bestehende Szene aus der tatsächlichen 2600/35/−50/0-Spielkamera geprüft. Der konkrete Übertragungsplan steht in `Art/HealingHouse/ExpandedArtV1/Design.md`.

## 3. Erreichte Übereinstimmung

Konkret übernommen wurden Empfang hinten mittig, gestufter Holztresen, grüne Stoff-/Symbolflächen, linke Warte-/Kaminzone, rechte Kreaturenliegen, gegliederte Putz-/Stein-/Balkenwände, Fenster, gefüllte Regale, Kräuter, Keramik, Teppiche und warme Lichtinseln. Die Aufnahme `02_Interior00000.png` zeigt diese Anordnung aus der verbindlichen Spielkamera.

**Die Qualität der gemalten Referenz ist noch nicht erreicht.** Die Props und Oberflächen wirken weiterhin einfacher und geometrischer. Raumaufteilung, Materialfamilien und Funktionsbereiche sind näher an der Referenz; deren dichte, unregelmäßige, malerische Detailwirkung wird nicht als fertig behauptet. Harry entscheidet anhand der lokalen Aufnahmen über die weitere Richtung.

## 4. Endgültige Raumaufteilung

Der Raum bleibt 12 m breit entlang Y und 10 m tief entlang X, mit 3-m-Wänden. Weltzentrum bleibt (20000,0,150) cm. Eingang liegt bei X=19500, Rückwand bei X=20500, Seiten bei Y=±600 cm. Die feste Innenkamera blickt entlang +X.

| Bereich | Anordnung im Spielbild |
| --- | --- |
| Eingang/Hauptweg | unten mittig; grüner Läufer und freie seitliche Passage |
| Empfang | hinten mittig; unveränderte Heilerinposition und Interaktion |
| Warten | links vorne; zwei Bänke, Tisch, Teppich und Pflanzen |
| Kamin | linke Seitenwand; abseits des Hauptwegs |
| Behandlung | rechts; vorhandener Kräutertisch und unterschiedlich große Liegen |
| Vorräte | Seiten- und Rückwände; Bücher, Kräuter, Flaschen und Keramik |

Die Heilerin steht weiterhin bei (20330,−80,62) cm. Der Zugang rechts um den Tresen bleibt frei. Einrichtung steht in Gruppen statt gleichmäßig über der Bodenfläche verteilt.

## 5. Empfang und Heilerin

Ein neuer wiederverwendbarer Holztresen mit Panelgliederung, gedecktem Grün und dünnen Metallakzenten ersetzt die einfache visuelle Frontwirkung. Hauptfläche 105 cm, niedrige Stufe 80 cm. Der bestehende Kollisions-Fußabdruck bleibt erhalten; das neue sichtbare Mesh hat keine zusätzliche Collision.

Kleine Flaschen, Keramik, Buch, Bandage, Schale, Korb und Pflanze sitzen auf passenden Arbeitsflächen. Die unterschiedliche Tresenhöhe erforderte eine reine Positionskorrektur einzelner vorhandener Heilutensilien, keine Änderung ihrer Assets oder Funktion. Heilerin, Dialog, Heal, RestPoint, Checkpoint und Save bleiben bei ihren vorhandenen Klassen und Daten.

## 6. Kamin und Sitzbereich

Neuer Steinkamin an der linken Wand, mit heller Steinstruktur, dunkler Feueröffnung, Holzeinfassung und warmem Feuerlicht. Der alte verkürzte Schornstein-Platzhalter bleibt als vorhandener Actor erhalten, ist im Innenraum verborgen und nicht kollidierend.

Zwei gepolsterte Holzbänke, ein kleiner Tisch, Keramik, Pflanzen, Korb und grüner Teppich bilden die Wartezone. Eine frühere Testroute lief versehentlich durch die zweite Bank; die Route wurde um die Bank geführt. Ihre funktionale Collision wurde dafür nicht entfernt. Der Umweg bleibt offen und diagonal nutzbar.

## 7. Heil- und Kreaturenbereich

Die beiden unterschiedlichen V3-Liegen werden wiederverwendet: kleinere/mittlere und größere Ruheposition. Holz-/Stoffmaterialien, zusätzliche Kissen, Kräutertisch und kleine Heilutensilien verdeutlichen den Zweck. Beide Liegen und der Weg dazwischen sind im Fußlauf erreichbar. Kein drittes Bett, keine Kreaturen-KI, kein neues Heilsystem.

## 8. Sichtbare Wandgestaltung und Cutaway

Beide Seiten und die Rückwand bleiben sichtbar: insgesamt zehn Seiten- und sechs Rückwandfelder. Warmer Putz, Steinuntersockel, Balken/Pfosten, sechs echte Fensteröffnungen, Wandkräuter, Laternen und Rückwandbanner ersetzen die Wirkung eines leeren Testkastens.

Sechs Fensterfelder verwenden neue sichtbare Fensterwandmodule. Die bisherigen Kollisionskörper dieser Felder bleiben als sechs verborgene Kopien erhalten. Die neuen sichtbaren Wandmeshes sind `NoCollision`; eine Fensteröffnung ist deshalb kein zusätzlicher begehbarer Ausgang.

**Vorher und nachher genau 107 Occluder, gleiche Referenzen und gleiche Reihenfolge.** Im ausgelagerten Raum bleiben ausschließlich die beiden Frontwände, zwei Türpfosten, Lintel und Türbalken ausblendbar; die übrigen 101 vorhandenen Außen-Dach-/Frontreferenzen bleiben ebenfalls unverändert. Die ursprünglichen maskierten Frontmaterialien sind erhalten. Kein neues Detail und kein Seiten-/Rückwandteil wurde als Occluder ergänzt. Fade weiterhin 0,4 s.

## 9. Wiederverwendete Assets

Wiederverwendet werden beide V3-Liegen, Kräutertisch, Kräuterregal samt Inhalt, bestehendes Bücherregal, Bücher, Flaschen, Heilmaterial, Nischenmöbel sowie vorhandene V3-Laternen. Zwei weitere Regalinstanzen an der Rückwand verwenden das bestehende V3-Bücherregalmesh. Die ursprünglichen Assetdateien und Blenderquellen bleiben bytegleich; die neuen Farben sind lokale Materialzuweisungen auf Innenraum-Instanzen.

## 10. Neue Assets

17 wiederverwendbare Meshes: `FloorTile2m`, `WindowWall2m`, `StoneWainscot2m`, `CounterStepped`, `Fireplace`, `Bench`, `Table`, `CeramicJar`, `Vial`, `Basket`, `HerbPot`, `DriedHerbs`, `Banner`, `Rug`, `WallPost`, `ShelfStock`, `Pillow`.

18 eigene Materialien und eine 512 × 512-Oberflächentextur ergeben zusammen mit den Meshes **36 neue Unreal-Assets** unter `/Game/Environment/HealingHouse/ExpandedArtV1`. Keine externen Downloads, Marketplace-Assets, Meshy-Generierung oder neuen Plugins.

Die Map erhält 141 neue Actors: 136 StaticMeshActors einschließlich der sechs erhaltenen Wandblocker, vier kleine Lichtquellen und ein begrenztes PostProcessVolume. Sechs vorhandene Wandactors werden auf die neuen Fensterwandmeshes umgestellt. Quelle: 42.412 Dreiecke für alle 17 Props. Neue Propinstanzen ohne die sechs ersetzten Fensterfelder: 275.462 Dreiecke; einschließlich dieser Fensterfelder 283.238. Bestehende V3-Geometrie ist in dieser Art-Pass-Zahl nicht enthalten. Nur eine kleine neue Textur; kein Anspruch auf ein vollständiges Performanceprofil.

## 11. Blenderänderungen und Sicherung

Eigenständige Quelle ausdrücklich gespeichert unter:

`/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/HealingHouse/Source/HealingHouse_ExpandedArt_V1.blend`

Die Datei wurde in einem neuen Blender-Prozess erneut geöffnet. Alle 17 Props wurden auf Maße, Materialslots, UVs und nicht degenerierte Geometrie geprüft und aus zwei Richtungen gerendert. **Erst nach dieser Sichtprüfung wurden die 17 FBX-Dateien exportiert.** Originalquellen und die vorhandene interaktive Blender-Szene mit Cube/Camera/Light wurden nicht überschrieben. Die separate Quelle enthält die Props als editierbare Einzelobjekte; kein monolithisches Interior-Mesh.

Die Blender-Review verwendet hellere Arbeitsbeleuchtung/prozedurale Oberflächen. Die entscheidende Farb-/Materialbewertung erfolgt in Unreal, dessen eigene Materialgraphen die Projekttextur nutzen. Source-Audit und Blender-Reviewbilder bleiben unter ignoriertem `Saved/HealingArt/Blender`.

## 12. Materialien

Warmes braunes Holz, dunkleres Fachwerk, heller warmer Putz, graubrauner Stein, gedecktes Kräutergrün, grüne Stoffe, Creme/Leinen, zurückhaltende Keramik-/Blütenakzente. Matte Oberflächen mit leichter eigener Variation; Fenster und Feuer bekommen nur kleine Emissive-Anteile.

Ein Import-/Samplerproblem zeigte zunächst graue Defaultflächen und wurde korrigiert: die lineare Oberflächentextur verwendet passende lineare Color-Sampler. Der endgültige Materialaudit prüft die tatsächlich am jeweiligen Material angeschlossenen Expressions; keine fehlenden Materialien oder Assets. Echte Front-Fade-Materialien werden nicht durch neue opake Art-Materialien ersetzt.

## 13. Beleuchtung

Vier neue kleine schattenlose PointLights für Kamin, Warten, Empfang und Behandlung ergänzen die zwei bestehenden Innenlichter. Fenster-/Laternenflächen unterstützen die Lesbarkeit. Ein räumlich begrenztes PostProcessVolume liefert dezente Belichtungs-/Farb-/AO-Abstimmung ausschließlich im ausgelagerten Innenraum. Es ist nicht ungebunden und überlappt die Außenwelt nicht. Kein neues finales Lichtsystem, kein Schatten-/VFX-Ausbau, keine Kameraänderung.

Die Referenz besitzt stärkere Lichtstaffelung und reichere malerische Schatten. Der aktuelle Raum bleibt bewusst gut lesbar, wirkt aber noch flächiger als das Bild.

## 14. Pflanzen und Kräuter

Zehn neue Topfpflanzen, sieben hängende/trocknende Kräuterbündel, Fensterpflanzen und vorhandene V3-Regalkräuter. Flaschen/Bücher/Keramik sitzen gruppiert in zwölf Vorratsgruppen und auf Arbeitsflächen. Pflanzen konzentrieren sich auf Wände, Fenster, Regale und Raumzonen, nicht auf den Hauptweg. Kleine Dekoration hat keine Collision.

## 15. Maßstab und verbindliche Technik

| Parameter | Endstand |
| --- | --- |
| Player sichtbare Körperhöhe | unverändert 140 cm / 1,40 m |
| Bewegung | unverändert 210 cm/s |
| Innenraum | unverändert 1200 × 1000 cm / 12 × 10 m |
| Außenheilhaus | unverändert 900 × 930 cm / 9 × 9,3 m |
| Türpassage | unverändert 150 × 215 cm / 1,50 × 2,15 m |
| Sitzhöhe | ca. 45 cm / 0,45 m; Rückenlehnen-Bounds sind keine Sitzhöhe |
| Tischoberkante | ca. 75 cm / 0,75 m |
| Tresenoberkanten | 80 / 105 cm, entsprechend 0,80 / 1,05 m |
| Liegen | weiterhin ca. 70 cm / 0,70 m |
| Innenkamera | unverändert 2600 cm, FOV 35°, Pitch −50°, lokaler Yaw 0° |
| Außenkamera | unverändert 2500 cm, FOV 35°, Pitch −55°, Yaw −45°, vorhandener Lag |
| Übergang/Steuerung | unverändert 0,4 s / 0,18-s-Bewegungsbasis-Blend |

Input, acht Richtungen, Playeranimationen, Pivot, Collision und Interaktionsreichweite sind unverändert. Keine neue allgemeine Skalierungsentscheidung.

## 16. Laufwege und Collision

Vorhandene Boden-, Tür-, Tresen- und Liegen-Collision bleibt erhalten. Neue große Möbel blockieren sinnvoll; neue Dekoration, Teppiche, Dielen und Fensterdarstellung verwenden dauerhaft `NoCollision`. Sechs verborgene ursprüngliche Wandkörper behalten die Gebäudebegrenzung. Neue Möbel ignorieren den Visibility-/Interaktionskanal.

Ein Re-Load-Audit fand zunächst Default-`BlockAll`-Profile auf Dekoration trotz temporär deaktivierter Collision. Die gespeicherten Profile wurden korrigiert, die Map erneut geladen und anschließend der vollständige Fußlauf wiederholt. Der Player kann Empfang, Sitzgruppe, Kamin, Behandlung, beide Liegen und alle drei Wandseiten erreichen. Kein Test-Teleport oder Deaktivieren tragender Collision zur Testabkürzung.

## 17. Vollständiger PIE-Fußtest

**Bestanden auf dem final gespeicherten und erneut geladenen Stand:** Außen → gerader Eintritt → Empfang/Heilerin → Sitzbereich → Kamin → Behandlung → kleine Liege → große Liege → beide Seitenwände → Rückwand → Ausgang → diagonaler Wiedereintritt → diagonaler Austritt → Vorplatz.

Zwei Eintritte und zwei Austritte; 18 echte Spielkamera-Aufnahmen. Enhanced Input steuert sämtliche Laufbewegungen. Die normale maskierte Building-Relocation bleibt die einzige räumliche Versetzung; der Test enthält keine Pawn-Transformsetter oder Spawn-Overrides. Gemessene Maximalgeschwindigkeit 210,00000000004 cm/s, entsprechend unverändert 210 cm/s. Übergangsmaske, Raum-/Außenbasis und Kameraendpunkte wurden während des Laufs protokolliert.

Player bleibt auf den geprüften begehbaren Routen sichtbar. Kleine punktuelle Überdeckung durch Topfpflanzen ist möglich; keine Wand verdeckt ganze Laufzonen, keine neue Occluder-Ausnahme erforderlich. Der hintere Zugang zur Heilerin ist begehbar. Die Einrichtung macht natürliche Umwege notwendig, erzeugt aber keine Sackgasse.

## 18. Heal, Checkpoint und Save

Vor dem Fußlauf wurde das vorhandene Testkampf-/Presenter-System verwendet, um reale Teamzustände zu verbrauchen: erste Kreatur 0/52 HP, zweite 15/47 HP, teilweise verringerte PP (27 beziehungsweise 31 statt 35 im ersten Slot). Keine neue Kampfmechanik.

Über die normale Heilerin-Interaktion/Dialogfolge wurden anschließend beide Kreaturen vollständig geheilt und sämtliche bekannten PP aufgefüllt. Checkpoint-ID `Dev_HealingHouse` und tatsächliche Innenposition wurden registriert. Der echte Dev-Spielstand wurde geschrieben und seine gespeicherte Position geprüft. Heil-/Checkpoint-/Save-Code wurde nicht verändert.

Der vorhandene persönliche Dev-Spielstand wurde vor den Tests gesichert und nach allen Tests bytegleich wiederhergestellt. Die Testkopie bleibt ausschließlich im ignorierten `Saved/HealingArt`; keine Save-Datei wird versioniert.

## 19. Automation, Map Check und Audits

**Finaler vollständiger Lauf in einer frischen eigenen Unreal-Instanz: 38/38 erfolgreich** (2026-10-04, 17:45 UTC). Enthalten sind Player Foundation/ScaleCalibration/BuildingInteriorCamera, HealingHouse Layout/CollisionAndCutaway/RestCheckpointSaveAndDefeat, RelocatedInterior MappingAndTransition, Inn CameraAndFootprint sowie sämtliche vorhandenen Battle-, Encounter-, Capture-, Inventory-, Save-, Dialogue-, Quest- und UI-Tests. Testliste: `Saved/HealingArt/AutomationFresh.json`.

Der erste vollständige Lauf war ebenfalls 38/38 erfolgreich. Eine zusätzliche Wiederholung nach mehreren PIE-/Testwelt-Ladevorgängen war 37/38: `Battle.Session.ValidationAndReplay` löste bei seiner expliziten Garbage Collection ein Engine-Ensure über ein noch initialisiertes `LandscapeSubsystem` der zuvor geladenen `Dev_BuildingKitTestMap` aus. Die Battle-Assertions meldeten keinen abweichenden Kampfzustand. Die frische Instanz hat genau diesen Test und alle übrigen erfolgreich ausgeführt; kein Unterdrücken von Fehlern, kein Ändern von Test-/Gameplay-C++ und keine Behauptung, der fehlerhafte Zwischenlauf sei grün gewesen.

Nach finalem Fußtest: Map Check **0 Fehler / 0 Warnungen**. Expanded-Interior-, Material-/Missing-Asset-, Geometrie- und Collision-Audit bestanden. Sämtliche neuen Props sind aufrecht; keine versehentlich gepitchten Möbel oder Fenster. Unterstützungshöhen kleiner Tisch-/Regalobjekte wurden korrigiert. Die sechs Fensterwandorientierungen werden im bestehenden lesenden Audit gezielt geprüft, einschließlich Null-Pitch/Null-Roll.

Kein C++ verändert, daher **kein Build erforderlich oder ausgeführt**. Der formale Paketvalidator des verwendeten Room-Skills erwartete einen anderen Meshy-/Room-Paketvertrag und ist für diese ausdrücklich beauftragte eigene Blender-/Unreal-Arbeit nicht als Projekt-Test verwendet worden. Es wird kein bestandenes Skill-Paket-Gate behauptet. Die Projektprüfungen oben liefern die tatsächliche Validierung.

## 20. Unterschiede zur Referenz und Gründe

Die Referenz ist eine stark malerische Konzeptdarstellung; dieser Pass verwendet eigene echte, wiederverwendbare 3D-Props im bestehenden 2.5D-/Paper2D-Spielraum. Möbelkonturen, Maserung, textile Falten, feine Kräuter-/Blumenvariation, weichere Schatten und unregelmäßige Detailstaffelung sind noch deutlich einfacher. Das ist eine offene visuelle Qualitätsgrenze, keine Behauptung gleichwertiger Bildqualität.

Der vorhandene Raum ist größer und der Hauptlaufbereich breiter/freier als im Bild, damit 8-Wege-Bewegung und alle Funktionsstellen komfortabel bleiben. Die feste frontalere Innenkamera und offenen Cutaway-Kanten entsprechen der vorhandenen Technik; kein Anpassen der Kamera für einen schöneren Einzel-Render. Heilerin und Player bleiben ihre vorhandenen Sprite-Platzhalter. Der Kamin wird aus dieser Kamera stärker seitlich gelesen als in der Referenz. Der vorhandene Eingang bleibt 150 × 215 cm trotz abweichender universeller Tür im Konzeptbild.

Für eine noch stärkere Annäherung fehlen vor allem malerischere Oberflächen, weniger regelmäßige Möbel-/Regaldetails, reichere Stoff-/Kräuterformen und differenziertere Licht-/Schattenwirkung. Diese Arbeit ist **nicht** automatisch angeschlossen. Nach diesem Bericht keine weiteren Änderungen bis Harrys Sichtprüfung.

## 21. Vollständige Dateiliste und Schutz des Ausgangsstands

Vier bestehende Dateien verändert, 65 neue Dateien. Keine Dateien gelöscht. Die 200 ursprünglichen Actors außerhalb des ausgelagerten Raums sind im semantischen Transform-/Asset-/Material-/Collision-Vergleich unverändert; Heilerin und gesamte Cutaway-Konfiguration ebenfalls. Pointer-Adressen in Unreal-Struct-Textausgaben wurden bei diesem Vergleich ignoriert. Alle anderen Maps und Originalquellen sind zusätzlich bytegleich gesichert.

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Tools/ValidateHealingHouseExpandedInterior.py
?? Art/HealingHouse/ExpandedArtV1/Design.md
?? Art/HealingHouse/ExpandedArtV1/Props.json
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Banner.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Basket.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Bench.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_CeramicJar.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_CounterStepped.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_DriedHerbs.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Fireplace.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_FloorTile2m.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_HerbPot.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Pillow.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Rug.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_ShelfStock.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_StoneWainscot2m.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Table.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_Vial.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_WallPost.fbx
?? Art/HealingHouse/Exports/ExpandedArtV1/SM_HH_Art_WindowWall2m.fbx
?? Art/HealingHouse/Source/HealingHouse_ExpandedArt_V1.blend
?? Art/HealingHouse/Textures/ExpandedArtV1/T_HH_Art_Surface.png
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Book.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Ceramic.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Fire.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Flower.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Glass.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Gold.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Leaf.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_LeafLight.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Linen.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Metal.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Mortar.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Paper.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Plaster.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Sage.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Stone.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Timber.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Window.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_Wood.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Banner.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Basket.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Bench.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_CeramicJar.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_CounterStepped.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_DriedHerbs.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Fireplace.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_FloorTile2m.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_HerbPot.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Pillow.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Rug.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_ShelfStock.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_StoneWainscot2m.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Table.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_Vial.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_WallPost.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Meshes/SM_HH_Art_WindowWall2m.uasset
?? Content/Environment/HealingHouse/ExpandedArtV1/Textures/T_HH_Art_Surface.uasset
?? Docs/HEALING_HOUSE_EXPANDED_ART_V1_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseExpandedArtV1.py
?? Tools/Blender/ExportHealingHouseExpandedArtV1.py
?? Tools/Blender/ReviewHealingHouseExpandedArtV1.py
?? Tools/DressHealingHouseExpandedArtV1.py
?? Tools/ImportHealingHouseExpandedArtV1.py
?? Tools/TestHealingHouseExpandedArtV1PIE.py
?? Tools/ValidateHealingHouseExpandedArtV1.py
```

Für einen späteren Sicherungspunkt **nach Sichtfreigabe** können ausschließlich diese Projektdateien vorgemerkt werden; der folgende Befehl wurde nicht ausgeführt:

```sh
git add -- Content/Maps/Dev_HealingHouseTestMap.umap Docs/TECHNIK.md Docs/ENTSCHEIDUNGEN.md Docs/HEALING_HOUSE_EXPANDED_ART_V1_PRUEFBERICHT.md Tools/ValidateHealingHouseExpandedInterior.py Art/HealingHouse/ExpandedArtV1 Art/HealingHouse/Exports/ExpandedArtV1 Art/HealingHouse/Source/HealingHouse_ExpandedArt_V1.blend Art/HealingHouse/Textures/ExpandedArtV1 Content/Environment/HealingHouse/ExpandedArtV1 Tools/Blender/BuildHealingHouseExpandedArtV1.py Tools/Blender/ReviewHealingHouseExpandedArtV1.py Tools/Blender/ExportHealingHouseExpandedArtV1.py Tools/ImportHealingHouseExpandedArtV1.py Tools/DressHealingHouseExpandedArtV1.py Tools/TestHealingHouseExpandedArtV1PIE.py Tools/ValidateHealingHouseExpandedArtV1.py
git diff --cached --stat
```

## 22. Lokale Reviewdateien

Alle Screenshots/Logs/Audits bleiben ignoriert und gehören nicht ins Repository. Hauptvergleich aus der echten Spielkamera:

`Saved/HealingArt/FootFinal/Review/02_Interior00000.png`

```text
Saved/HealingArt/FootFinal/Review/01_Exterior00000.png
Saved/HealingArt/FootFinal/Review/02_Interior00000.png
Saved/HealingArt/FootFinal/Review/03_Reception00000.png
Saved/HealingArt/FootFinal/Review/04_Waiting00000.png
Saved/HealingArt/FootFinal/Review/05_Fireplace00000.png
Saved/HealingArt/FootFinal/Review/06_Treatment00000.png
Saved/HealingArt/FootFinal/Review/07_SmallBed00000.png
Saved/HealingArt/FootFinal/Review/08_LargeBed00000.png
Saved/HealingArt/FootFinal/Review/09_SidePlusRear00000.png
Saved/HealingArt/FootFinal/Review/10_SidePlusFront00000.png
Saved/HealingArt/FootFinal/Review/11_SideMinusFront00000.png
Saved/HealingArt/FootFinal/Review/12_SideMinusMiddle00000.png
Saved/HealingArt/FootFinal/Review/13_SideMinusRear00000.png
Saved/HealingArt/FootFinal/Review/14_RearMinus00000.png
Saved/HealingArt/FootFinal/Review/15_RearMiddle00000.png
Saved/HealingArt/FootFinal/Review/16_OutsideAgain00000.png
Saved/HealingArt/FootFinal/Review/17_DiagonalInside00000.png
Saved/HealingArt/FootFinal/Review/18_FinalOutside00000.png
```

Fußlaufprotokoll `Saved/HealingArt/FootFinal/PIERoute.json`, frameweises Übergangsprotokoll `Frames.jsonl`, finaler Mapaudit `Saved/HealingArt/FinalAudit.json`, Erhaltungsnachweis `Preservation.json`, Blenderprüfung `Saved/HealingArt/Blender/SourceAudit.json` und zwei Prop-Reviewbilder. Frühere Versuchsläufe bleiben als solche separat erhalten. Die Reviewauflösung beträgt 3093 × 1730; für die Qualität zählen die echten Spielbilder, nicht freie Editoransichten.

## 23. Markdown und git diff --check

Markdown auf ausgewogene Codeblöcke, Überschriften-/Listenabstände und nachlaufende Leerzeichen geprüft. Alle neuen Python-Werkzeuge bestehen die Syntaxprüfung. **`git diff --check`: Exit 0, keine Ausgabe.**

## 24. Endgültiges git status --short

```text
 M Content/Maps/Dev_HealingHouseTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Tools/ValidateHealingHouseExpandedInterior.py
?? Art/HealingHouse/ExpandedArtV1/
?? Art/HealingHouse/Exports/ExpandedArtV1/
?? Art/HealingHouse/Source/HealingHouse_ExpandedArt_V1.blend
?? Art/HealingHouse/Textures/ExpandedArtV1/
?? Content/Environment/HealingHouse/ExpandedArtV1/
?? Docs/HEALING_HOUSE_EXPANDED_ART_V1_PRUEFBERICHT.md
?? Tools/Blender/BuildHealingHouseExpandedArtV1.py
?? Tools/Blender/ExportHealingHouseExpandedArtV1.py
?? Tools/Blender/ReviewHealingHouseExpandedArtV1.py
?? Tools/DressHealingHouseExpandedArtV1.py
?? Tools/ImportHealingHouseExpandedArtV1.py
?? Tools/TestHealingHouseExpandedArtV1PIE.py
?? Tools/ValidateHealingHouseExpandedArtV1.py
```

Nichts gestaged, kein Commit und kein Push. Für Harrys Sichtprüfung die gespeicherte `Dev_HealingHouseTestMap` neu laden; der bereits geöffnete Benutzer-Editor wurde nicht zur Testinstanz umgebaut.
