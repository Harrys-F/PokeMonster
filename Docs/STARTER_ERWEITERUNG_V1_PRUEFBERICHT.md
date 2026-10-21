# Starter-Erweiterung V1 – Prüfbericht

Stand 21.10.2026. Ausgangspunkt main `2a1db9165f37866745a6641619e6d2658bde4216`. Keine neue Map, kein Worktree. Vorhandene 58 unversionierte Dateien im Schutzinventar `Saved/StarterExpansionV1/Initial.json` erfasst. Vollbackup 03492bd bleibt unverändert.

## Arbeitspaket 1: sichere Niederlagen-Speicherung

Rückkehr prüft nun die tatsächlich erfolgreiche Teleportierung; bei blockiertem Ziel ist nur ein ebenfalls kollisionsgeprüfter PlayerStart zulässig. Erst nach erfolgreicher Platzierung und vollständiger Teamheilung wird der abgeschlossene Zustand gespeichert. Der tatsächliche Rückkehrpunkt ist Teil desselben bestehenden SaveGame-Snapshots. Während Kampf und laufender Rückkehr bleiben Snapshots gesperrt.

Der macOS-Speichertransport schreibt die unveränderte SaveGame-Version 4 in eine eindeutige temporäre Nachbardatei, liest und deserialisiert diese zur Kontrolle und ersetzt den Slot über das atomare native `rename` der Apple-Plattformdateischnittstelle. Ein Fehlschlag entfernt nur die eigene temporäre Datei; der vorherige Slot wird nicht vorab gelöscht. Kein zusätzlicher dauerhafter Backupslot. Dies garantiert keinen Schutz vor sämtlichen Hardware-/Stromausfällen. Ladevalidierung und Migrationen 1–3 bleiben erhalten. Ein fehlgeschlagenes Autosave wird im Rückkehrhinweis angezeigt; die erfolgreiche Heilung bleibt erhalten.

Prüfungen:

- Mac Development Editor Build erfolgreich: `Saved/ProjectRefinement/StarterSaveBuild02/Result.json`.
- Vollständige Projekt-Automation: **70/70**, keine Testwarnungen oder Testfehler (`StarterSaveAutomation01`). Neue Prüfungen für die Rückkehrsperre und den geprüften atomaren Austausch einschließlich fehlgeschlagener Dateipromotion.
- Echter ClassicBattle-PIE-Niederlagenablauf mit vorhandener Kamera/UI: **bestanden**, `Saved/StarterExpansionV1/DefeatSave04/Result.json`. Speichern im Kampf abgewiesen; Rückkehr, volle KP, Autosave und identisches Reload von GUID/KP/XP/Rückkehrpunkt nachgewiesen. Die ersten Harness-Läufe benötigten eine Korrektur des Python-Checkpoint-Zugriffs und des GUID-Vergleichs; sie sind nicht als erfolgreiche Abnahmen gezählt.
- Ursprünglicher Dev-Spielstand nach jedem Lauf bytegenau wiederhergestellt: SHA-256 `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.
- ClassicBattle-Darstellung, Kampflogik, Maps, Originalmodelle und bisherige Animationen unverändert.

## Weitere beauftragte Arbeitspakete

Die Modell- und Speziesintegration ist unten als zweites Arbeitspaket dokumentiert. Freie Oberweltbewegung und gemeinsame Gameplay-Abnahme sind noch in Bearbeitung. Die Gesamtprüfung mit Map Checks und vollständigem Gameplay-Fußlauf folgt nach deren Integration. Kontrollmedien und lokale Prüfdaten bleiben unter Saved und werden nicht hochgeladen. Physischer Switch-Pro-Test ist ausdrücklich kein Abschlusskriterium.


## Arbeitspaket 2: Schiggy und Bisasam

| Modell | Originaldatei | Vertices / Dreiecke | Rig | Höhe | Materialien / Texturen |
|---|---|---:|---|---:|---|
| Schiggy | `Art/Characters/Creatures/Incoming/Shiggy.glb` | 14.162 / 21.273 | eigenes Biped, 20 Bones | 0,50 m | 1 / 3 × 2048² |
| Bisasam | `Art/Characters/Creatures/Incoming/Bisasam.glb` | 13.885 / 21.545 | eigenes Quadruped, 18 Bones | 0,70 m | 1 / 3 × 2048² |

Original-SHA-256:

- Schiggy: `8353b766fc36d90d3c7a8905e82ae9c407a974959dcab6cac629c5127446a127`.
- Bisasam: `01ee8bc064635aeaaed2b356e1c87e0a9d0ab819fa6285d86cfbe0460466306d`.

Beide Eingaben haben kein Rig und keine Animationen. Keine Retopologie, keine Polygonreduktion, keine neuen Flächen, keine Änderung von Kopf/Körper/Design. Unveränderte GLB-Geometrie als getrennte versteckte Referenz in jeder Blenderquelle, drei gepackte Bilder. Rohmessungen der offenen Kanten (6.599/5.863) enthalten viele UV-Seams und sind kein Beweis für echte Löcher oder Wasserdichtheit. Schiggy zeigt im Original kleine dunkle Oberflächenstellen nahe dem Auge; diese sind nicht als behobene Geometriefehler ausgegeben.

Frühe regionale Gewichtskandidaten zeigten starke Hautauszüge und wurden verworfen. Die endgültigen Gelenke wurden anhand tatsächlicher Hand-/Sohlenpositionen korrigiert. Blender Bone Heat auf einer temporär bei 1 µm positionsverschweißten Hilfskopie lieferte vollständige, anschließend normalisierte Gewichte. Nur Gewichte wurden auf das ursprüngliche Mesh übertragen. Rigidere Sohlen und analytische Zweibone-Standphasen verhindern die zuvor sichtbaren Fußverformungen. Haut-/Gelenkfeinschliff bei extremen Posen bleibt eine spätere manuelle Qualitätsaufgabe; kein pauschaler Produktionsreifeanspruch.

Jeweils Idle, Walk, Run, Attack, Hit, Faint und Happy bei 30 Hz. Schiggy: Walk 26 cm/s, Run 50 cm/s; Bisasam: 32/72 cm/s. Bisasam nutzt einen Viertakt-Walk und diagonale Laufpaarung. Standphasen werden mit gemessener konstanter Fußgegenbewegung gelöst; die maximalen Schrittinkrementfehler und minimale Oberflächenhöhe stehen in den jeweiligen `MeshyV1_AnimationAudit.json`. Das ersetzt keine komplette Ingame-Deformationsabnahme.

Neue bearbeitbare Quellen und Exporte:

- `Art/Characters/Creatures/Schiggy/Source/Schiggy_Meshy_V1.blend` und `Bisasam/Source/Bisasam_Meshy_V1.blend`.
- Je Spezies sieben FBX-Dateien in `Exports/MeshyV1/`, drei unveränderte extrahierte Original-JPEGs in `Textures/MeshyV1/`, Modell- und Animationsaudit.
- Unreal: `/Game/Characters/Creatures/{Schiggy,Bisasam}/MeshyV1/` mit jeweils eigenem Mesh, Skeleton, sieben AnimSequences, Material, drei Texturen und Präsentationsprofil. Keine zusätzlichen Feueranker.
- Spezies `/Game/Data/Creatures/DA_Schiggy`, `DA_Bisasam`; Wildprofile `/Game/Data/Encounters/DA_Schiggy_Wild`, `DA_Bisasam_Wild`. Stabile IDs ändern keine Glumanda-/Save-Identität. Keine neuen Evolutionsmodelle oder ungesicherten Evolutionsreferenzen.

Gen-2-Daten anhand [Serebii Schiggy](https://www.serebii.net/pokedex-gs/007.shtml), [Serebii Bisasam](https://www.serebii.net/pokedex-gs/001.shtml), [Schiggy-Lernliste](https://pokemondb.net/pokedex/squirtle/moves/2) und [Bisasam-Lernliste](https://pokemondb.net/pokedex/bulbasaur/moves/2) geprüft. Fangrate jeweils 45, Wachstum Medium Slow, weiblicher Anteil 12,5 %. Basis-Ertrag 66 für Gen-2-Schiggy ([Generationsänderung](https://pokemondb.net/pokedex/squirtle)), 64 für [Bisasam](https://pokemondb.net/pokedex/bulbasaur). Tackle: 35 Stärke, 95 Genauigkeit, 35 AP. Rankenhieb: Gen-2-Spezialattacke, 35/100/10. Aquaknarre: 40/100/25, ab Level 13. Bisasam nutzt außerdem das unveränderte bestehende Heuler-Asset. Nicht unterstützte Originalwirkungen Rutenschlag/Blubber/Panzerschutz/Egelsamen sind bewusst offen; freie Slots bleiben leer.

Unreal-Abnahme:

- Build `StarterModelBuild02`: bestanden; der erste neue Testbuild benötigte eine Korrektur an die vorhandene MoveSlot-Schnittstelle.
- Automation `StarterModelAutomation01`: **72/72**, 0 Testwarnungen/Fehler. Belegt eigenes Skeleton, sieben kompatible Clips, tatsächliche Meshhöhe, stabile Spezies-IDs, Wildroll, Heilung und Save/Load mit beiden Spezies.
- Beide gespeicherten Blenderquellen erneut geöffnet; alle 14 FBX-Dateien wirklich reimportiert. Gleiche Dreieckzahlen, eigene Bones/Actions, identische UVs und normalisierte Gewichte (`Saved/StarterExpansionV1/BlenderValidation04/Result.json`).
- `ModelReview02`: vier echte PIE-Kämpfe, je beide Perspektiven in ClassicBattle und WorldBattle; Angriff, Flucht und tatsächliches Speichern/Laden bestanden. Ursprünglicher Dev-Spielstand danach bytegenau restauriert.
- Alle **11 vorhandenen Maps**, einschließlich der geschützten unversionierten Testmap: Map Check **0 Fehler / 0 Warnungen**, Editorlog `Saved/StarterExpansionV1/EditorModels01.log`. Keine Map gespeichert/geändert.
- Vorhandene Engine-Start-/Audio-/idevice-Warnungen und eine bestehende `MI_WLA_LeafOak`-Warnung zur Instancing-Nutzung wurden beobachtet. Keine Änderung an diesem welt-/kampfumgebungsbezogenen Altmaterial. Keine Fehler stillschweigend als bestanden umgedeutet.

Texturdiagnose: Schiggys Mip-Atlas erzeugte helle Flecken (`ModelReview01`). Isolierte Änderung ausschließlich seiner neuen BaseColor-Mip-Einstellung beseitigt sie (`ModelReview02`). Originalfarben und Original-JPEG unverändert. Diese Lösung behält volle 2K-Abtastung und kann bei großer Entfernung mehr Abtastungsunruhe verursachen; Bewegungsprüfung folgt. Normals: OpenGL nach Unreal mit invertiertem Grünkanal; MR: G=Roughness, B=Metallic.

Echte Unreal-Aufnahmen, lokal, **tatsächlich 2331 × 1346**, kein behauptetes QHD:

- `Saved/GlumandaV11/LiveUI/Starter_ModelReview02_0_Commands/ActualSlateViewport.png`: Schiggy vorne links, Bisasam gegenüber.
- `Saved/GlumandaV11/LiveUI/Starter_ModelReview02_1_Commands/ActualSlateViewport.png`: umgekehrte Perspektiven.
- Weitere Moves-/Attack-/WorldBattle-Aufnahmen in derselben lokalen Gruppe. WorldBattle am unveränderten Spawnpunkt zeigt teilweise vorhandene Weltdeckung; es wurde kein Weltobjekt für einen schöneren Test entfernt.

Die zentrale Kampfansicht, deren Code/UI/Kameras/Platzierungsregeln und bisherige Modelle/Animationen bleiben unverändert. Dauerhafte Wildplatzierung und Begleiterbewegung folgen separat.
