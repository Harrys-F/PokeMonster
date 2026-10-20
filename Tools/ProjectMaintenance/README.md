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
