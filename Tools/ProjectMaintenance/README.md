# Projektpflege am festen Projektpfad

Aktives Projekt: `/Users/harry/Developer/PokeMonster/PokeMonster.uproject`.
`main` folgt dem vorhandenen `origin/main`. Das Vollbackup bleibt unter
`backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` lokal erhalten.
Diese Verweise nicht nach GitHub pushen und keine Git-/LFS-Bereinigung ausführen.

`EditorSession.py` lädt bestehende Karten, führt Map Check aus, liest tatsächliche
Importquellen und öffnet eine lokale, auf wenige Aktionen begrenzte Prüfwarteschlange.
Es speichert keine Karte und importiert keine Modelle neu. Aufruf über den vorhandenen
Unreal-Editor mit `-ExecCmds="py /Users/harry/Developer/PokeMonster/Tools/ProjectMaintenance/EditorSession.py"`.
Ergebnisse bleiben unter `Saved/ProjectMigration`, außerhalb von Git.

`RunGameplay.py` verwendet den unveränderten vollständigen Enhanced-Input-Fußlauf
aus `Tools/VisualV2QualityV2/FootTest.py`. Der originale Dev-Spielstand wird nur
vorübergehend umbenannt und nach Ende von PIE bytegleich zurückgelegt. Es entsteht
keine zusätzliche Sicherungskopie. Bei einem Prozessabbruch die gehaltene Originaldatei
`Saved/ProjectMigration/PokeMonster_Dev.migration-held.sav` vor weiteren Spieltests prüfen.
Keine parallelen manuellen Spielstände während dieser Prüfung speichern.

Keine neuen Maps, keine Änderungen an Gameplay, Kamera, Licht oder Animationen.
Historische Berichte behalten ihre damaligen Pfadbezeichnungen. Alte Review-Replays
können weiterhin lokale Nachweise benötigen; sie sind kein Teil des normalen Builds.


`BlenderSources.py` prüft Quelldateien ausschließlich lesend in einem eigenen
Blender-Hintergrundprozess. Mit `--python-exit-code 23` starten. Nach `--` können
`--only <relative Blendpfade>` und `--report <Dateiname.json>` übergeben werden.
Bibliotheksdateien ohne eigene Szene bleiben Datenbibliotheken; das ist keine
künstlerische Freigabe. Der Bericht und die Quellen-SHA müssen geprüft werden.

`FixMovedTexturePaths.py` ist die enge, einmalige Korrektur der zwei bei dieser
Umstellung gefundenen Blatttexturverweise. Vorher/Nachher-Fingerprints prüfen
Meshes, Topologie, UV-/Farbattribute, Materialien und Objekttransformationen.
Vorhandene unbenutzte Mesh-/Materialdaten werden nötigenfalls mit Fake User
vor unbeabsichtigtem Wegfallen beim Speichern geschützt. Kein Remesh, Export,
Rigging, Materialumbau oder zusätzliche `.blend1`-Sicherung. Alte Quellen bleiben
in Git/LFS erreichbar. Nicht pauschal auf andere Quelldateien anwenden.

## Art-Pass V3

`ValidateArtPassV3.py` prüft die aktuelle VisualV2 streng gegen erforderliche Actor-Signaturen und die gezielten Innenraum-/Farn-/Wegmanifeste. Falls die lokale ursprüngliche Szene noch vorhanden ist, prüft es zusätzlich den genauen Vorher-/Nachher-Umfang. `ValidateRefinedArt.py` delegiert bei vorhandenem V3-Signaturvertrag hierher; der ältere Audit bleibt für seinen alten Stand erhalten. Fehlende optionale Kontrollbilder ersetzen keine Geometrie- oder Gameplayprüfung.

`ArtV3Interior.py`, `ArtV3RoomFill.py` und `ArtV3Landscape.py` sind einmalige, gegen erneutes Überschreiben gesicherte Umsetzungsskripte. Nicht blind auf einen schon umgesetzten Stand anwenden. `PoseSilverLady.py` und `BuildWestlandFerns.py` erzeugen nur eigene neue Quellen und Exporte; vorhandene Originale werden nicht überschrieben. Die SilverLady-Armature ist ausschließlich eine statische Pose-Studie.

`RunArtV3Gameplay.py` führt den vorhandenen echten Enhanced-Input-Rundweg aus; `RoomBoundary` ist eine begrenzte Wiederholung für Ein-/Ausgang, Heilen und die exakten Raumgrenzen. Der echte Dev-Spielstand wird für diesen Test unter ignoriertem Saved gehalten und danach bytegleich restauriert. Nicht parallel manuell speichern. `ArtV3RuntimeAudit.py` verwendet dieselbe tatsächliche Raumgrenze wie BuildingCutaway. `ArtV3Photos.py` und `ArtV3WindowMotion.py` erzeugen optionale echte Spielkameraaufnahmen unter `Saved/ArtPassV3`. Foto-Positionierungen sind Diagnose-Teleports und kein Ersatz für den separat durchgeführten Fußlauf. Keine Medien in Git aufnehmen.

`ArtV3MapChecks.py` lädt ausschließlich vorhandene Karten, führt Map Check und die unveränderte Ranger-V3-Regression aus. Ergebnisse und verbleibende Grenzen: `ArtV3Acceptance.json` und `Docs/ART_PASS_V3_HEILHAUS_LANDSCHAFT_PRUEFBERICHT.md`.

## Grafikpass V4

`ValidateArtPassV4.py` und `ArtV4Signatures.json` prüfen den gespeicherten V4-Stand einschließlich exakter Actor-Signaturen, bestehender Kollisionen/Instanzen, Gameplay-Anker, Innenraum-/Außenlichtgrenzen und der neuen Objekte. `ValidateRefinedArt.py` wählt bei vorhandenem V4-Vertrag diesen aktuellen Prüfer; V3 bleibt als historische Referenz erhalten. Zahlen-Nullen werden nur für identisches `-0.0`/`0.0` kanonisiert; unbenutzte transiente `NPCStaticVisual`-Komponenten ohne Mesh sind kein persistentes Asset. Aktive Darstellungen werden weiter geprüft.

Neue Blenderquellen sind `Art/HealingHouse/Source/HealingHouse_ArtV4.blend` und `Art/Characters/NPCs/SilverLady/Source/Westland_Healer_ArtV4.blend`. Die zugehörigen Builder/Exporte sind eigene Varianten; keine Originalquelle ersetzen. Umsetzungsskripte sind einmalige, zustandsabhängige Arbeitsschritte und ausdrücklich keine bedenkenlos erneut ausführbare Migration: BuildHealingArtV4 → BuildHealingRug → FixHealingRugUV → BuildHealerV4; anschließend ArtV4Interior → ArtV4Healer → CorrectHealingArtV4 → FinishHealingArtV4 → ReimportHealingRug → ArtV4ComposeFinish → ArtV4Landscape → ArtV4FinalComposition → ArtV4FireFinish. Den Ablauf zuerst anhand der Manifeste prüfen; auf bereits umgesetzten V4 nicht wiederholen. ArtV4FinalLayout und ArtV4_HearthPlacement enthalten die finale Kaminposition.

`ArtV4MaterialFingerprint.py` vergleicht Live- und Disk-Materialeigenschaften. `ArtV4SaveStoneUsage.py` darf ausschließlich den nachgewiesenen Instancing-Usage-Unterschied sichern; keine Pakete verwerfen oder neu laden. Der tatsächliche Nachweis liegt in `Art/HealingHouse/ArtV4_StoneUsageProof.json`.

`RunArtV4Gameplay.py` verwendet den bestehenden Enhanced-Input-Rundweg und identifiziert Ranger/Heilerin über ihre tatsächlichen Source-Actors. Er hält den originalen Dev-Spielstand nur während des Tests und restauriert ihn bytegenau. `ArtV4RuntimeAudit.py` prüft echte Raumgrenzen, Schatten, Sichtbarkeit und Gesprächsdrehung. `ArtV4FurnitureCollision.py` verwendet getrennte Diagnose-Startpositionen und echte Bewegung gegen die zwei neuen Möbelkollisionen. Diese Probe ersetzt keinen vollständigen Fußlauf.

`ArtV4Photos.py`, `ArtV4IdleReview.py` und `ArtV4WindowMotion.py` erzeugen optionale echte Aufnahmen ausschließlich unter Saved/ArtPassV4. Die Fenster-Bildfolge ist 720p, die statischen Vergleiche sind echtes QHD/100 %. Kein Videoerfolg behauptet. `ArtV4MapChecks.py` lädt die elf bestehenden Karten ohne Speichern und prüft die Ranger-V3-Regression. Kompakte Ergebnisse: `ArtV4Acceptance.json`. Kontrollmedien sind keine erforderlichen Build-Dateien und werden nicht hochgeladen.

## Grafikpass V5

`ArtV5Interior.py` entfernt ausschließlich die freigegebene V4-Steinbodeninstanz, ersetzt die bisherigen kollisionsfreien Boden-Visuals durch nahtloses Holz, bindet SilverLadys originales Material und ergänzt eigenes Raum-Dressing. `BuildHealingArtV5.py` benutzt die erhaltenen V4-Autorenhelfer für neue eigene Polster-/Sessel-/Buchmeshes; keine alte Blenderdatei überschreiben. `VerifySilverLadyV5.py` vergleicht die Original-Heilpose lesend mit der riggbaren Kopie. `VerifyHealingV5.py` öffnet die neue noch nicht gestagte Quelle lesend und prüft ihre Geometrie-/UV-/Texturabhängigkeiten. Der historische BlenderSources-Prüfer bleibt auf bereits versionierte Quellen beschränkt.

Umsetzungsfolge: BuildHealingArtV5 → ArtV5Interior → ArtV5Landscape → ArtV5ReviewFinish → ValidateArtPassV5 (erster Vertrag) → ArtV5ContactFinish → ValidateArtPassV5. Einmalige, zustandsabhängige Arbeitsschritte; auf dem fertigen V5 nicht blind wiederholen. Die Kontaktkorrektur prüft explizit nur die vier eigenen geänderten Actor-Signaturen, bevor sie deren neuen Stand schreibt. Keine allgemeine Lockerung des Signaturvergleichs. Der aktuelle Vertrag schützt alle übrigen Actor-/Gameplay-/Kollisions-/Licht-/Postprocesswerte.

`ArtV5Photos.py`, `ArtV5IdleReview.py`, `ArtV5WindowMotion.py`, `ArtV5FurnitureCollision.py`, `ArtV5RuntimeAudit.py`, `RunArtV5Gameplay.py` und `ArtV5MapChecks.py` folgen den erhaltenen V4-Prüfungen. Tatsächlicher vollständiger Fußlauf und separate Diagnose-Teleports werden unterschieden. Der Dev-Spielstand wird nur für den Gameplaytest gesichert und danach bytegleich zurückgegeben; keine parallelen manuellen Save-Vorgänge. Kontrollmedien ausschließlich unter ignoriertem Saved/ArtPassV5, keine Git-Pflicht für Bilder/Videos. Bericht: `Docs/GRAFIKPASS_V5_PRUEFBERICHT.md`; kompakte Ergebnisse: `ArtV5Acceptance.json`.
