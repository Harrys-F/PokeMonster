# Kreaturen-Pipeline V2 – Meshy → Blender → Unreal

Aktives Projekt ausschließlich `/Users/harry/Developer/PokeMonster`. Dieser Vertrag bereitet den schrittweisen Import von bis zu 251 Arten vor. Er erzeugt keine Modelle, keinen Pokédex-Katalog und keinen automatischen Massenimport. Aktueller Stand nach Meshy-Glumanda Integration V1: Die Nutzerdatei liegt jetzt vor und ersetzt über ein eigenes Profil die aktive Darstellung; Zunderlauf V1 bleibt unverändert als Rückfallquelle erhalten. Details und tatsächliche Prüfungen: `Docs/MESHY_GLUMANDA_INTEGRATION_V1_PRUEFBERICHT.md`. Der unten beschriebene V2-Pending-Plan bleibt eine historische Vorlage, nicht der aktuelle Importstatus.

## Bestehende Architektur und stabile Identität

`UPokeMonsterCreatureSpeciesData` enthält gemeinsame Art-/Kampfdaten. `FPokeMonsterCreatureInstance` enthält Instanz-ID, Level, XP, HP und eigene Moveslots/PP. Encounter-, BattleSession-, Capture-, Team-, Heil- und Save-Systeme bleiben zuständig. Das optionale `Visuals.Presentation` zeigt auf ein `UPokeMonsterCreaturePresentationData`; ohne 3D-Profil bleibt der bestehende 2D-Fallback verfügbar.

Der Save speichert `CreatureSpecies:<InternalId>` und individuelle Zustände, **keinen Mesh-, Skeleton- oder Präsentationspfad**. Deshalb wird beim späteren Glumanda-Austausch **`CreatureSpecies:Zunderlauf` und `/Game/Data/Creatures/DA_Zunderlauf` erhalten**. Kein Umbenennen, keine neue Art-ID und keine Save-Versionänderung nur wegen eines Modells. Encounter-ID, Profil, Seed, Kampfwerte und vorhandene Fortschrittsflags bleiben gleich. Ein später gewünschter Anzeigenamenwechsel oder die Bereinigung der Prototyp-Pokédexnummer ist eine getrennte Datenentscheidung.

Die Inventur enthält derzeit nur TestGrass (1001), TestWater (1003), TestFire (1002) und Zunderlauf (1002). Die doppelte Prototypnummer wird nicht als nationaler Pokédex ausgegeben und hier nicht korrigiert. Es gibt keinen vollständigen 251er-Größenkatalog und keine Kreaturen-Blueprint-Assets. Die zentrale Funktionalität ist nativ in C++ und datengetrieben.

## 1. Eingang und Quellen

1. Vom Nutzer gelieferte Original-GLB unter den bestehenden Kreaturenquellen erhalten. Herkunft und SHA-256 dokumentieren. Nicht aus einem Dateinamen auf Art, Freigabe, Maßstab oder Rig schließen.
2. Nur diese Art bearbeiten. Originaldatei nicht remeshen, vereinfachen oder überschreiben. Keine anderen Incoming-Dateien automatisch integrieren.
3. Mit Blender 5.2.2 im isolierten Hintergrundprozess oder einer kontrollierten Sitzung lesen. Ein vorhandenes Live-Dokument nicht ersetzen.
4. Quellbestand und Arbeitsquelle trennen: Original-GLB unverändert; bearbeitbare `.blend`, tatsächliche Texturen, nötige FBX-Exporte im bestehenden Art-Verzeichnis. Keine zusätzlichen Projektkopien, Worktrees oder Maps.
5. Bestehenden Quelldateien niemals still neue Inhalte unterschieben. Git schützt geprüfte Entwicklungsmeilensteine; keine pauschalen Backups oder Blender-Quelle löschen.

Lesende Inspektion, ohne Blenderdatei zu speichern:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/CreaturePipelineV2/InspectBlender.py -- Art/Characters/Creatures/Zunderlauf/Source/Zunderlauf_V1.blend Saved/CreaturePipelineV2/NeueQuellpruefung.json
```

Der Ausgabepfad muss neu und unter `Saved/` liegen. `.glb` kann ebenfalls gelesen werden. Das Werkzeug meldet tatsächliche Meshes, Vertices/Dreiecke, UVs, Materialslots, Texturen, Rigs, Actions, Maße und negative Transformationen. Es repariert oder exportiert nichts. Seine Objekt-Bounds sind keine automatische Artgröße; Effekte, Pose, lange Schwänze und falsche Achsen müssen fachlich eingeordnet werden.

## 2. Originalgröße und Ausrichtung

- Eine Blender-Einheit entspricht beim vorbereiteten Export einem Meter; `Unit Scale` 1. Unreal verwendet Zentimeter. Keine doppelte Hundertfach-Skalierung. Ein Meter muss im FBX-Roundtrip 100 cm in Unreal ergeben; am echten Import messen.
- Blender-Autorenkonvention: **vorne −Y, oben +Z**, symmetrische Mitte X=0. Der bisherige FBX-Import konvertiert mit `convert_scene=True`, `convert_scene_unit=True`, `force_front_x_axis=True`, `import_uniform_scale=1` auf **Unreal +X vorne, +Z oben**. Die Transformation am tatsächlichen Kandidaten im Profil und mit Knie-/Fußbewegung nachweisen; keinen unbekannten Meshy-Rest-Pose-Roll blind übernehmen.
- Keine negativen Skalen, keine unterschiedlichen Korrekturskalen an Mesh und Armature. Originalkopie erhalten; Arbeitsrig, Skin und Animationsweg gemeinsam kontrolliert skalieren. Danach Transformationen, Bind Pose und Animationen erneut prüfen. Geometrie bei Bedarf im Bearbeitungsmodus korrigieren, ohne ein fertiges Rig blind anzuwenden.
- Die Größe kommt aus vorhandenen bestätigten Artdaten oder einer belegten Originalquelle. Wenn keine Größe vorhanden ist, Quelle und Messdefinition vor Integration ergänzen; keine der 251 Größen erfinden. Die bestehende Spielerhöhe bleibt 140 cm.
- Stehhöhe ist nicht Körperlänge: schlangenförmige oder liegende Arten können eine Längenangabe benötigen. Flügelspannweite, Schwanzflamme, Partikel und Spitzen einer Animationspose sind nicht automatisch die maßgebliche Größe. Der Intake verlangt deshalb `standing_height` oder `body_length` und eine bestätigte Messung. Gekrümmte Körperlänge muss ausdrücklich gemessen werden; eine Achsen-Boundingbox genügt dort nicht.
- Einheitlicher Skalierungsfaktor: `Originalgröße_cm / (gemessenes Bezugsmaß_m × 100)`. Er wird nur vorgeschlagen, nie automatisch angewandt. `ReferenceSizeCm`/`SizeSource` im Darstellungsprofil sind Dokumentation, keine automatische Laufzeitskalierung.

**Glumanda:** offizielle Größe **0,60 m**, [offizieller Pokédex](https://ph.portal-pokemon.com/pokedex/0004/), geprüft 20.10.2026. Die aktuelle Zunderlauf-V1-Höhe von ca. 65,2 cm bleibt bis zum echten Austausch unverändert. Die nationale Nummer 4 im Intake ist kein Auftrag, die bestehende technische Nummer 1002 oder Save-ID zu verändern.

## 3. Geometrie, UVs und Materialien

Vor jeder Reparatur tatsächliche Mesh-Inseln, offene/non-manifold Kanten, Normalen, degenerierte Flächen, Überschneidungen, UVs, Materialien, Alpha und Texturauflösungen untersuchen. Keine globale Decimation/Remesh als Standard. Bei Bedarf kontrollierte Retopologie und Baking gegen das erhaltene High-Poly, mit sichtbarer Abnahme aus der Spielkamera. 4K bezeichnet eine Texturauflösung, keine Geometrie- oder Animationsqualität.

Das aktuelle Laufzeitprofil verwendet **ein Skeletal Mesh** mit eigenen Materialslots und beliebigem geeigneten Skeleton. Mehrteilige Modelle müssen für diesen Pfad kontrolliert auf dasselbe Rig vorbereitet/zusammengeführt werden; eine beliebige Mehrkomponenten-/Morph-/Gesichts-Architektur ist nicht implementiert. Allgemeine Effekt-Meshes sind separat angebunden.

Base Color: sRGB, ohne eingebranntes Studiolicht. Normal: Normalmap-Kompression, kein sRGB; Grünkanal passend zur tatsächlichen Blender/OpenGL- oder DirectX-Quelle prüfen. Roughness/Metallic/AO: linear; keine ungeprüfte ORM-Kanalbelegung. Alpha nur bei echter Notwendigkeit; Masked/Translucent und doppelseitige Flächen jeweils beurteilen. Materialslots nicht nur nach Namen ersetzen. Augen, Haut, Fell, Federn oder harte Schalen benötigen unterschiedliche, belegte Eigenschaften. Keine Beleuchtung, Lumen-, TAA- oder Kamerawerte zum Kaschieren von Materialfehlern ändern.

Die Zunderlauf-V1-Materialien, Texturen und Meshes werden nicht als endgültige Meshy-Quelle behandelt. Benötigte Texturen in die neue Blenderquelle packen und externe Originalbilder ebenfalls nachvollziehbar erhalten. Importpfade dürfen nur auf das aktive Projekt zeigen, nicht auf alte Worktrees oder temporäre Downloads.

## 4. Rigs und Animationen

`RigFamily` klassifiziert Custom, Biped, Quadruped, Serpentine, Winged, Aquatic oder Floating. Diese Angabe wählt **kein** humanoides Rig, keine Knochenhierarchie und kein Retarget automatisch. Jede Art erhält ihre eigene geeignete Anatomie und Bone-Rest-Pose. Ein gemeinsames Skeleton ist nur nach realer Kompatibilitätsprüfung sinnvoll.

- Zweibeiner: Hüfte/Knie/Fuß und Gegenbewegung prüfen.
- Vierbeiner: Schulterblatt, Vorder-/Hinterläufe, Wirbelsäule und Gangphase separat ausarbeiten.
- Schlangen/Langkörper: kontrollierte Körperkette und Längenmaß; keine Beinannahmen.
- Fliegende, schwimmende und schwebende Arten: eigene Körper-/Flügel-/Flossenbewegung, passende Höhenreferenz. Die Pipeline erzeugt keine Flug-/Schwimm-KI oder neue Wasser-Kollisionen.
- Eigenständiges Rig nicht durch ein ungeprüftes 23-/25-Bone-Schema ersetzen. Effekt-Anker haben semantische Namen, keine fest vorgeschriebenen anatomischen Bones.

Für die vollständige Integration sieben Rollen: **Idle, Walk, Run, Attack, Hit, Faint, Happy**. Walk/Run können artspezifisch langsames/schnelles Schwimmen oder Fliegen bedeuten. Keine menschliche Laufbewegung erzwingen. Einzelne Idle-Vorschauen sind zulässig, gelten aber nicht als vollständige Kreatur.

Alle Clips im bestehenden nativen Präsentationspfad verwenden das **exakte Skeleton des Zielmeshes**. Gleiche Namen reichen nicht. Fremde Clips zuerst gezielt retargeten, in echte Sequenzen für das Ziel-Skeleton backen und Verformung prüfen. Der Validator verweigert sonst die Bindung. Animationen sind in-place; Root-Motion-Extraktion muss ausgeschaltet sein. Zusätzlich Root-/Armature-Trajektorie tatsächlich prüfen: ein ausgeschaltetes Flag allein beweist keine ortsfeste Animation.

Geschwindigkeit je Profil in cm/s messen, nicht Spielerwerte kopieren. Zyklusstrecke = Geschwindigkeit × Clipdauer. Standphasen, Fußspur, Abrollen, Körperkontakt und Übergänge in Blender sowie im Unreal-Import nachweisen. Die vorhandene native Mischung steuert Idle/Walk/Run und Reaktionen, keine universelle Boden-IK, Gesichtsmimik oder fortgeschrittene Animationszustandsmaschine.

## 5. Effekt-Anker

`EffectAnchors` bindet pro Profil optionale einfache Static-Mesh-Effekte mit eindeutiger ID, Bone/Socket, lokalem Offset und optionaler weltaufrechter Rotation. Beispiele für Bedeutungen: `TailTipFX`, `MouthFX`, `BodyCenterFX`. Die tatsächlichen Socketnamen dürfen pro Rig verschieden sein. Position und Rotation in allen relevanten Clips prüfen. Eine leere Liste ist gültig; nicht jede Kreatur benötigt Feuer oder einen Schwanz.

Der bestehende Zunderlauf-V1-Pfad `TailFlame`/`FlameBone` bleibt unverändert unterstützt. Ein neues Profil nutzt entweder diesen Pfad oder den allgemeinen Anker für denselben Effekt; keine doppelte Flamme. Neue Komponenten haben keine Kollision und werfen keine zusätzlichen Schatten. Alte Effektkomponenten werden beim gültigen Darstellungswechsel entfernt. Ein ungültiger Kandidat verändert die bisherige funktionierende Darstellung nicht.

Die Erweiterung implementiert einfache Mesh-Effekte, **keinen** universellen Niagara-/Audio-/Licht-Importer. Solche Effekte wären eine spätere separate Erweiterung. Für Glumanda bleibt verbindlich: **Feuer ausschließlich an der Schwanzspitze**.

## 6. Vorprüfung und Unreal-Import

`Tools/CreaturePipelineV2/Glumanda_Pending.json` enthält einen absichtlich unvollständigen Plan. Fehlende Quelldateien bleiben `null`; keine Ersatzdatei wird ausgewählt.

```sh
python3 Tools/CreaturePipelineV2/preflight.py Tools/CreaturePipelineV2/Glumanda_Pending.json
```

Solange das Modell fehlt, ist **Exit 2 / `ready_for_manual_import: false` korrekt**. Später im Plan Original-GLB, deren SHA-256, vorbereitete Blenderquelle samt SHA-256, lesenden Blender-Audit und die sieben tatsächlichen FBX-Exportpfade mit SHA-256 eintragen. Messbasis, gemessenes Bezugsmaß und Vorwärtsrichtung nach visueller Prüfung im Audit bestätigen. Alle Quellpfade bleiben relativ zum aktiven Projekt. Pfadflucht/Symlinkflucht, veränderte Quellen und bereits existierende Zielassets werden abgewiesen. Ein positives Ergebnis ist nur die Zulässigkeit des manuellen Imports, keine künstlerische oder Rigging-Freigabe.

Danach **ein Modell einzeln** in einen neuen Kandidaten-Namespace innerhalb der vorhandenen Kreaturenstruktur importieren. Der Plan sieht `/Game/Characters/Creatures/Zunderlauf/MeshyCandidate` vor, legt ihn hier aber nicht an. Vorhandene V1-Assets nicht reimportieren. Mesh mit eigenem Skeleton, Materialien kontrolliert zuweisen, keine automatischen zusätzlichen Gameplay-Kollider/Physics Assets. Sieben Sequenzen auf genau dieses Skeleton importieren. Für andere Modelle keine Zunderlauf-spezifischen Generatoren/Importer als generische Batchskripte verwenden.

Der bestehende FBX-Pfad ist die technische Vorlage: Mesh/Animationen getrennt, Szenen-/Einheitenkonvertierung wie oben, importierte Normalen, keine automatische Material-/Textur-Ersetzung, 30-Hz-Abtastung als geprüfter Anfang, exportierter Clipbereich, Import Scale 1. Wenn dafür das Legacy-FBX-Featureflag temporär umgestellt wird, vorherigen Wert im `finally` wiederherstellen. Auflösungen, Kanäle, Clipdauer, Anzahl/Orientierung der Bones und tatsächliche Größe nach dem Import neu messen. Quelle und FBX tatsächlich erneut öffnen.

`GetValidationErrors()` ist im Blueprint/Editor aufrufbar und prüft Mesh/Skeleton, zugewiesene Materialslots, Idle, sämtliche vorhandenen Clips, exakte Skeletonzuordnung, positive Clipdauer, deaktivierte Root-Motion-Extraktion, Geschwindigkeiten, Bodenoffset, Größenquelle und Effekt-Anker. Eine funktionierende Darstellung wird erst nach erfolgreicher Prüfung verändert. Normale Bewegung und sichtbare Animationen müssen zusätzlich künstlerisch geprüft werden.

Für die lesende Prüfung eines importierten Kandidaten `Saved/CreaturePipelineV2/CandidateRequest.json` mit `species_asset`, `presentation_asset`, `expected_primary_asset_id`, `require_all_seven: true` schreiben. Dann in der vorhandenen sauberen Editorsitzung:

```sh
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/CreaturePipelineV2/CheckCandidate.py
```

Dieses Werkzeug validiert nur; es bindet keine Spezies um und speichert keine Assets. Es wurde hier gegen Zunderlauf V1 ausgeführt. Die neue allgemeine Intake-Vorprüfung ist kein bereits abgenommener automatischer 251er-Importer.

## 7. Konkreter späterer Austausch Zunderlauf → Meshy-Glumanda

1. Nutzerdatei tatsächlich entgegennehmen; Dateiname und SHA-256 bestätigen. Fehlender Anhang bleibt ein Stoppgrund für modellabhängige Schritte.
2. Original visuell mit der bestätigten Referenz vergleichen; keine neue Gestaltung erfinden. In Blender vorbereiten und am belegten Größenmaß von 60 cm ausrichten. Aktuelles V1 nicht verändern.
3. Geeignetes eigenes Rig, Gewichte und sieben Clips erstellen. Kein V1-Retarget ohne Kompatibilitätsnachweis. Schwanzspitzen-Anker und ausschließlich dort Feuer prüfen.
4. Intake-Plan vervollständigen, Vorprüfung, FBX-Roundtrip und tatsächlichen Unreal-Import in unabhängige Kandidatenassets durchführen. Das neue Skeleton kann von V1 vollständig abweichen; alle eigenen Clips müssen zu ihm passen.
5. Neues Präsentations-Data-Asset mit Mesh/Clips, gemessenen Geschwindigkeiten, Bodenoffset und Effekt konfigurieren. `ReferenceSizeCm=60`, belegte `SizeSource`, passende `RigFamily`. Keine globale oder geheime Actor-Skalierung.
6. Kandidatenprüfer und Spielkameraabnahme ausführen. Vorder-/Seiten-/Rückenansicht, acht Richtungen, Bewegung, Schwanzfeuer, Attack/Hit/Faint/Happy und Bodenkontakt prüfen. Keine neue Map.
7. **Erst nach erfolgreicher Prüfung ausschließlich `DA_Zunderlauf.Visuals.Presentation` auf das neue Profil setzen.** Keine Änderung an InternalId, Art-Assetpfad, Encounter-Profil, Seed, Kampfwerten, Attacken, Instanz-IDs oder Saveformat. V1-Quelle und Assets behalten. Rücknahme: dieselbe eine Präsentationsreferenz wieder auf V1 setzen; kein Git-Reset nötig.
8. Vorher erstellten Save mit gefangenem Zunderlauf nach dem Austausch laden. ID, Level, XP, HP, PP, Team, Fang-/Questflags, Heilung und Speichern vergleichen. Dasselbe Wild-Encounter nicht neu erzeugen, wenn es im Spielstand abgeschlossen war.
9. Bestehenden Kampf/Fang und Teamwechsel testen, einschließlich 2D-Fallback und sicherer Darstellung bei fehlendem/ungültigem Kandidaten. Danach Build, vollständige Automation, Map Checks und echten Gameplay-Lauf. Erst geprüfte benötigte Quellen/Assets/Dokumentation gezielt committen und regulär pushen; Remote/LFS verifizieren. Kontrollmedien bleiben im ignorierten Saved.

## 8. Grenzen für große und besondere Arten

Das bestehende Weltkampf-Placement prüft kleine freie Bodenpositionen und das vorhandene Wild-Encounter hat einen prototypischen Kollider. Es ist **keine** Freigabe für 251 beliebig große Körper, lange Schlangen oder fliegende Gruppen. Für jede spätere Art Größe, Platzbedarf, Terrainkontakt, Sichtbarkeit und Gameplay-Kollision explizit abnehmen. Nicht heimlich Modelle kleiner skalieren, um eine feste Aufstellprobe zu bestehen. Bei unpassendem Platz den vorhandenen Fallback verwenden und die konkrete Erweiterung planen.

Die neuen Rig-Typen sind Metadaten; sie ersetzen keine artspezifische Animation, Navigation, Flug-/Schwimmbewegung oder Performanceprüfung. Skinning, Silhouette, Materialqualität, Transparenz, vollständige Selbstüberschneidung, Root-Trajektorie und feine Fußkontakte benötigen reale Kandidaten und Bild-/Bewegungsabnahme. Ein erfolgreicher Dateivalidator kann diese nicht ersetzen.

## Ergänzung aus dem realen Meshy-Import

Eine FBX-Armature kann trotz korrekter 60-cm-Meshbounds eine Socket-Skalierung von 100 enthalten. Für separat exportierte Effektmeshes die tatsächliche Socket-Referenztransformation auslesen und deren Skalierung im relativen Effekt-Offset kompensieren; keine feste 0,01 ohne Messung anwenden. Die reine Darstellungs-API `SetPresentation` erlaubt eine validierte Vorschau in PIE ohne Änderungen an Speziesdaten. Quellenorientierung darf durch dokumentierte Front-/Profil-Renderprüfung bestätigt werden; das Werkzeug behauptet dabei keine menschliche Freigabe.

## 10. Wiederverwendbare Landbewegung und Begleiter (Starter-Erweiterung V1)

`Species.Overworld` enthält Habitat-/Geschwindigkeits-/Pausen-/Rückrufwerte. `UPokeMonsterCreatureRoamingComponent` ist die gemeinsame Grundlage für bewusst platzierte Wildbegegnungen und eine reine Begleiterdarstellung. Bestehende Encounter-IDs bleiben die persistente Identität; die Zufallsbewegung wird nicht als separater Kreaturenzustand gespeichert.

- Wilde Instanzen: vorhandene `APokeMonsterVisibleWildCreatureActor`, eigenes `Profile` + `VisualSpecies`, `bAmbientMotion=true`, stabile eindeutige EncounterId/Seed. Radius pro Art, optional `HabitatRadiusOverride` und `HabitatHalfExtent` pro Instanz. Keine Platzierung nur nach XY-Nähe: tatsächlichen Boden, Kapsel, Gebäude und Zugänge prüfen.
- Planung: begrenzte lokale A*-Suche mit realen Boden-/Kapselabfragen; Steigung, Stufen, feste Hindernisse, vorhandene Wasserblocker und geschlossene/versetzte Gebäuderäume respektieren. Tags `Water` und `CreatureNoWalk` ergänzen die Geometrieprüfung. Keine automatische semantische Erkennung beliebiger Wassermaterialien. Keine Schwimm-/Flug-KI, kein universeller Ersatz für langfristige Navigation einer großen Welt.
- Lange Wege mit Pausen und Umschauen; vor großen Richtungswechseln erst drehen. Bei Annäherung des Spielers wird eine Wildbegegnung ruhig und ansprechbar. Während Kampf/Rückkehr pausiert die Oberweltbewegung.
- Der WorldSubsystem-Begleiter zeigt ausschließlich Teamplatz 1 mit gültiger, kampffähiger 3D-Darstellung. Ist Platz 1 ungültig, kampfunfähig oder ohne 3D-Profil, erscheint kein Ersatz aus späteren Slots. Kein neues Team-/Inventar-/Save-System, keine zusätzliche Kollisionskapsel und kein eigener UI-Auswahldialog. Lose Bewegung, Rückruf mit Hysterese, höhere Geschwindigkeit beim tatsächlichen Sprint. Der maximale aktive Abstand ist konfigurierbar; echte Raum-/Save-Teleportierungen und eine außerhalb des Bildes liegende Wiederanknüpfung sind abgesicherte Ausnahmefälle, kein normaler sichtbarer Laufschritt.
- Optionaler `SprintAnimation` + `SprintReferenceSpeed` gehört nur zur Begleiterdarstellung. Exaktes vorhandenes Skeleton, in-place, gemessene Zyklusstrecke, echter FBX-Roundtrip. Nur ein temporäres Profil des Begleiters ersetzt dessen Run-Clip; die sieben Originalclips und Kampfprofile bleiben unverändert. Kleine Kreaturen benötigen bei 315 cm/s Spielersprint eine eigene längere Laufbewegung statt zehnfach beschleunigter kurzer Schritte.
- Bestehende Innenraum-Lichtkanäle und Schattenfreiheit vom Spieler nur auf den eigenen Begleiter übernehmen; keine Licht-/Raumassets ändern.

Prüfen: `Tools/StarterExpansionV1/RunMovement.py`, `RunCapture.py`, `RunFullGameplay.py`, alle Projekt-Automationstests und alle vorhandenen Map Checks. QA-Fixtures sind explizit und dürfen nicht als natürlicher Gameplay-Fußlauf ausgegeben werden. Der vollständige Fußlauf nutzt Enhanced Input ohne Testteleports. Original-Dev-Slot vor gezielten Speicherprüfungen sichern und ausschließlich bei nachgewiesen unverändertem Testendstand restaurieren. Kontrollmedien bleiben unter Saved.

## 11. Starter-Feinschliff V2

- `Acceleration`, `BrakingDeceleration`, `CompanionAcceleration`, `CompanionBrakingDeceleration` und `TurnAcceleration` ergänzen die bestehenden Speziesparameter. Pfadenden bremsen aus; kollisionsgeprüfte Zwischenpunkte stoppen nicht künstlich. Beschleunigung ersetzt keine Fuß-IK.
- Lokale Ziele vermeiden vier jüngste Ziele und bevorzugen seltener besuchte Habitatsektoren. Der A*-Planer kann den exakten begehbaren Zielpunkt aus einer Nachbarzelle erreichen. Pfadglättung führt jeden Kandidaten erneut durch die vorhandene Hindernis-/Bodenprüfung. Fehlgeschlagene Rückrufversuche bleiben zeitlich begrenzt.
- `Glumanda_Faint_PolishV2.blend` ist eine kleine bearbeitbare Rig-/Actionquelle. Unverändertes Referenzmesh aus `Glumanda_Meshy_V11.blend` zur Bearbeitung hinzuladen. Die Ohnmacht dreht die geerbte Idle-Pose gemeinsam um die geprüfte Weltachse; Schwanz und Rumpf erhalten keine widersprechenden unabhängig ausgerichteten Posen.
- `Bisasam_Meshy_PolishV2.blend` enthält unveränderte Geometrie/UVs/Materialien und die bestehenden sieben Actions mit 135 gezielt korrigierten Bauchgewichten. Keine erneute automatische Retopologie oder Neugestaltung. Neue Unreal-Assets liegen unter den jeweiligen `PolishV2`-Verzeichnissen. Die bestehenden Skeletons und bisherigen Quellen bleiben erhalten.
- Vier begrenzt ergänzte Gen-2-Attacken: Rutenschlag, Blubber, Panzerschutz, Egelsamen. Neue Individuen verwenden weiterhin die letzten vier chronologisch erlernten Attacken. Bereits gespeicherte Slots/PP bleiben unverändert; `AssignSpeciesMoves` ist ausdrücklich eine administrative Neuzuweisung und darf bei vorhandenen Spielständen nicht zur ungefragten Aktualisierung aufgerufen werden. Verteidigung/Initiative und Egelsamen bleiben kampflokale Zustände; keine neue Save-Version.
- Aktuelle Prüfungen: `Tools/StarterPolishV2/README.md` und `STARTER_FEINSCHLIFF_V2_PRUEFBERICHT.md`. Optionaler Bild-/Videonachweis gehört nach `Saved/`, nicht in Git.


## Kreaturen-Erweiterung V3 – aktueller zusätzlicher Bestand (21.10.2026)

Die sieben gelieferten Arten Pikachu (40 cm), Myrapla (50 cm), Enton (80 cm), Machomei (160 cm), Nebulak (130 cm), Gengar (150 cm) und Glurak (170 cm) sind eigenständig unter `Art/Characters/Creatures/{Name}` und `/Game/Characters/Creatures/{Name}/MeshyV1` vorbereitet. Originale in Incoming unverändert, eigene Skeletons/alle sieben Rollen, gepackte editierbare Quellen und echter FBX-Roundtrip. Kein pauschales Humanoid-Retargeting: vier Arme, Blätter, Gashülle und Flügel/Schwanz benötigen eigene Landmarken und Gewichte. Material-/Topologieerhalt anhand der tatsächlichen Modelle prüfen. Körpermitte nicht blind aus einer Box mit seitlichem Schwanz ableiten.

Neuer Ablauf und eng geschützte einmalige Import-/Habitatmigrationen: `Tools/CreatureExpansionV3/README.md`. Wiederholbare native Präsentations-, Fang-/Heil-/Save- und echte Habitatprüfungen separat ausweisen. Mathematische IK-Fehler sind kein Ersatz für die Minimumhöhe der deformierten Haut. Original-LOD0 und unvollständige unterstützte Gen-2-Lernlisten sind bewusst dokumentierte Grenzen. Keine abschließende Behauptung einer lückenlosen 8-Richtungs-Animationsabnahme. Ergebnisse: `KREATUREN_ERWEITERUNG_V3_PRUEFBERICHT.md`. Die älteren Abschnitte beschreiben ihren damaligen Entwicklungsstand.


## Glutexo und Entwicklungen V2

Elfte integrierte Art: Glutexo/005, 110 cm. Unveränderte Incoming-GLB, eigene gepackte Blenderquelle, eigenes anatomisch eingepasstes Rig und sieben Clips unter `Art/Characters/Creatures/Glutexo`; keine Wiederverwendung inkompatibler Skeletons. Die modellierte Originalflamme bleibt ausschließlich am Schwanz. Eigenständige Artidentität und eigenes Präsentationsprofil; Glumanda/Zunderlauf und Glurak unverändert. `Tools/GlutexoEvolutionV2` enthält Einzelimport, Quellenprüfung und reale PIE-Nachweise.

Entwicklung wechselt die Art derselben individuellen Instanz, nicht die globalen Präsentationsdaten einer anderen Art. Begleiter und Kämpfe laden dadurch das neue eigene Skeleton/Profil über die bestehende Darstellung. Unveränderte persönliche XP-Kurve kann bei historischen Daten vom neuen Artstandard abweichen und wird mit Schema 8 gespeichert. Vollständiger Bericht: `POKEMON_ENTWICKLUNGEN_V2_PRUEFBERICHT.md`.
