# VisualV2 Beleuchtung und Schatten V3.1

Die produktive Änderung betrifft genau zwei Einstellungen des vorhandenen Actors
`VS_SoftSkyFill` auf `/Game/Maps/Dev_TestMap_VisualV2`: Yaw 140 → −45 Grad,
Intensität 1,12 → 1,8. `Settings.json` enthält beide Zustände. Kein neues Licht,
kein neues Asset, keine globalen Renderer-/Materialänderungen. Hauptsonne und
Innenraum bleiben erhalten. Das Fülllicht ist eine vorhandene schattenlose
künstlerische Lichtquelle, keine Änderung des physikalischen Schattenfaktors.

Der vollständige Prüfbericht liegt in
`Docs/VISUALV2_BELEUCHTUNG_SCHATTEN_V3_1_PRUEFBERICHT.md`.
Alle Originalbilder, Videos und umfangreichen Messdaten bleiben unter
`Saved/ProjectRefinement/LightingV31`, nicht im Git-Commit.

## Werkzeuge

- `Baseline.py`: einmalige Hash-Inventur von Originaldateien und Backup-Verweisen;
  erstellt keine Kopien und überschreibt keine vorhandene Baseline.
- `Inspect.py`: ursprüngliche vollständige Szenen-/Lichtinventur. Nur vor neuen
  Studien in einem frischen Nachweisziel benutzen, nicht historische Belege ersetzen.
- `Study.py`: temporäre Varianten aus `Saved/.../LightingV31/Request.json` im
  normalen PIE; RAM-Save-Schutz, feste QHD-Spielkamera. Keine Map-Speicherung.
  Fotografische Aufstellung ist ausdrücklich kein Gameplay-Fußlauf. Bewegte
  Pokémon und Animationsposen sind zwischen Aufnahmen nicht identisch.
- `Apply.py`: gesicherte einmalige Übernahme der zwei Einstellungen bei exakt
  passender Ausgangsszene. Verweigert eine erneute oder unerwartete Übernahme.
- `Validate.py`: volle Szenen-/Lichtprüfung gegen den Ausgangsstand mit nur zwei
  zulässigen Unterschieden. Liest die aktuelle Editorwelt, speichert keine Map.
- `Compare.py`: zehn echte QHD-Paare, Kameramatch und deklarierte Bildausschnitte.
  Keine Retusche; Codewerthelligkeit ist keine physikalische Lichtmessung.
- `Footrun.py`: bestehender vollständiger Eingabe-/Physik-Parcours mit eigenem
  Nachweisziel und RAM-Save-Schutz. Keine Teleports entlang der Route.
- `Motion.py` / `EncodeMotion.py`: vorhandene native Aufnahme-/Codierfunktionen,
  nur neue Orte und Nachweisziele. Tatsächliche präsentierte Frames, kontrollierte
  Spielzeitverlangsamung und Originalzeitstempel; kein Echtzeit-FPS-Nachweis.
- `MapChecks.py`: alle zwölf bestehenden Karten rein lesend, Rückkehr zur
  Ausgangsmap. Scoped Marker `LIGHT31_MAPCHECK_BEGIN/END` im Editorlog.
- `Package.py`: prüft alle früheren Kerndateien, geschützten Dateien, anderen
  Maps, Save und Backup-Verweise; aktualisiert nur die explizite Paketliste und
  Kerndatei-Prüfsummen. Staged, committed oder löscht selbst nichts.

Editor-Skripte über die bestehende geschützte `ArtSession.py`/`ArtControl.py`-
Warteschlange ausführen. Keine zweite Editorinstanz oder neue Map nötig.
Historische Bilder und Resultatdateien nicht überschreiben. Das Anwenden und
Rücknehmen ist im Editor an genau einem vorhandenen Licht möglich; niemals
pauschal ganze Maps auf ältere Git-Stände zurücksetzen.
