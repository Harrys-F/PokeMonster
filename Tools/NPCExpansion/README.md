# NPC-Bibliothek

Alle Arbeiten verwenden das bestehende Projekt, Originalquellen und NPC-System.
`Library.json` enthält technische IDs und individuell gesetzte Gelenkmarken. Die
historischen Gesamthöhen (einschließlich Hüten/Ausrüstung/Reitern) bleiben erhalten;
sie sind keine neu beschlossene allgemeine Größenordnung der Völker.

## Verwendung in Unreal

Profile: `/Game/Characters/NPCs/Library/Profiles/DA_NPC_<ID>`.
Einen vorhandenen `PokeMonsterNPC` mit geeignetem Dialog verwenden, einen
`PokeMonsterNPCVisualActor` zuordnen und `ApplyPresentation(Profile)` aufrufen.
An den Source-NPC anhängen, den visuellen Fußpunkt an den Capsule-Fuß setzen.
Profile enthalten keine Berufe, Geschichten, Quests oder neuen Save-Identitäten.
Materialüberschreibungen gelten nur am Präsentationscomponent. Drei bereits geeignete humanoide Modelle nutzen ihre vorhandenen Meshes und
Skeletons weiter; nur neue Rollenclips liegen in `Animations/SharedSkeleton`.
Die Heilerin nutzt ihr vorhandenes Dreiknochen-Mesh und das Originalmaterial, keine erneute Meshkopie.
Animationen werden nur bei exakt passendem Skeleton angenommen. Ein ungültiges
Profil ersetzt keine funktionierende Darstellung.

Die Präsentation misst die wirkliche Bewegung des Source-Actors. Ein Weg-/KI-System
bleibt für dessen Bewegung verantwortlich. Geschwindigkeiten sind individuelle
Referenzen für die Clips, keine Änderung der Spielerbewegung. Die optionale
Fußstabilisierung ist für flachen Testboden ausgelegt, keine universelle Gelände-IK.
Gespräch und Begrüßung betreffen den Oberkörper; die laufende Beinkette bleibt
bestehen. Keine Finger-/Lippensynchronisation oder physikalische Stoffsimulation.

## Normaler PIE-Zugang in VisualV2

Die Vorführung entsteht bei jedem gewöhnlichen PIE-Start, ohne QA-Aufruf.
Kein Betrieb in Westland, Biom-Karte, eigenständigem Game oder Shipping.

```text
pm.NPCGround.Go          # Mitte bei (-7500, 3000, 0) cm
pm.NPCGround.Go 1        # aktueller Standort des ersten NPCs
pm.NPCGround.Mode idle   # stehen; weitere Werte auto, walk, run
pm.NPCGround.Greet       # vorhandene Begrüßung zeigen
pm.NPCGround.Return     # zum ursprünglichen Ort zurück
```

Stationen 1..11: Ranger, SilverLady, TreeBeing, ElvenScholar, Wizard,
WhiteHairedWarrior, DwarfWarrior, CrouchedCreature, ElvenArcher, DarkArmored,
HobbitBase. Mit B beziehungsweise E normal ansprechen; zuerst zur Figur schauen.
Laufmodus fällt bei Figuren ohne geeigneten Laufclip auf Gehen zurück.
SilverLady und TreeBeing sind bewusst stationär. Bei SilverLady ist die Begrüßung
nur ein Nicken; der unsichere Vollrig-Versuch wurde verworfen. Das Baumwesen besitzt
fest verbundene Bodenwurzeln und Reiter; kein vorgetäuschter menschlicher Gang.

Die Vorführung nutzt normale NPC-Interaktionen mit einem rein technischen Dialog
und ohne Folgeaktionen. Beim Besuch wird der vorhandene RAM-Save-Transport
aktiviert. Rückkehr stellt den Sitzungsstand wieder her; normale Save-Dateien werden
nicht kopiert oder überschrieben. Laufversuche verwenden Capsule-Sweeps, begrenzte
Testziele und Abbremsen; kein neuer produktiver NPC-Pfadplaner.

## Quellen / Werkzeuge

`Inventory.py` prüft GLB-Metadaten/SHA-256 und legt nur lokale Schutzmanifeste in
`Saved/ProjectRefinement/NPCExpansion` an. `InspectBlender.py` prüft vorhandene
Laufzeitexporte, nicht blind die Millionenpolygone der Originale.
`BuildLibrary.py -- <ID>` wird im Blender-Hintergrund aufgerufen; vorhandene
Bibliotheksquelldateien werden nicht automatisch überschrieben. Beispiel:
`/Applications/Blender.app/Contents/MacOS/Blender --background --threads 3 --python-exit-code 1 --python Tools/NPCExpansion/BuildLibrary.py -- Ranger`. Quellen liegen
neben den ursprünglichen Quellen unter `Source/*_NPCLibrary.blend`.
Für DarkArmored folgt `FixArmorHem.py`: Die vordere Rüstungsbahn gehört nicht an
die Schienbeine. Der Fix prüft reale verformte Geometrie über alle Cliprollen.
`ReopenSources.py` validiert erneut gespeicherte Rigs, Gewichte und gepackte Texturen.
`ImportLibrary.py` legt nur fehlende Bibliotheksassets an und verwendet bestehende
Materialien. Importer-Flag wird anschließend zurückgestellt. Nicht pauschal alle
historischen Tools ausführen.

`ReviewPIE.py` erzeugt echte Spielkamera-Bilder und native Bewegungsaufnahmen.
Die technische Positionierung für Einzelaufnahmen ist keine behauptete Fußreise.
Die abschließenden Videos (`ReviewMotionPIE.py`) erfassen echte präsentierte
Slate-Frames bei 0,25-facher Spielzeit und werden mit den echten
Spielzeitstempeln normal schnell encodiert. Die dünneren ersten
Framebufferfolgen dienen nur der Diagnose. `EncodeReview.py <PIE-Label>` prüft Bildfolge und
Abtastdichte. Keine Performance-Messung oder physische Controller-Abnahme.
Anim-FBX enthält nur Knochen/Kurven; Geometrie steht einmal im Mesh-FBX.
`ReimportAnimationOnly.py` prüft die tatsächlich importierbare Knochenquelle
gegenüber dem existierenden Skeleton und der unveränderten Clipdauer.
Kontrollmedien und Fehlversuche bleiben ausschließlich in `Saved`, außerhalb Git.
