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
