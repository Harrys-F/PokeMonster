# Starter-Feinschliff V2

Nur im bestehenden PokeMonster-Projekt verwenden. Keine Map-Erzeugung, keine globalen Grafikänderungen. Alle Kontrollmedien/Logs nach ignoriertem `Saved/`; nicht mit Git aufnehmen. `ArtSession.py` ist eine ausdrücklich gestartete, saubere Editorsitzung, keine allgemeine Remote-Ausführung.

- `InspectAnimations.py`: öffnet die drei bisherigen Quellen nur lesend, misst 17 Posen je Clip und rendert diagnostische Extremposen. Ausgabeordner muss neu sein. Blenderbilder sind kein Unreal-Spielnachweis.
- `DiagnoseDeformation.py`: konkrete ursprüngliche Vertex-/Bone-Zuordnung prüfen.
- `CorrectAnimationSources.py`: nur neue, versionierte V2-Quellen/FBX und zugehörige Audits. Originalquellen werden per SHA-256 geschützt. `-- --revise-generated` ist ausschließlich die ausdrückliche Wiederholung auf den eigenen generierten Korrekturdateien; niemals auf Nutzeränderungen anwenden.
- `ValidateCorrections.py`: FBX wirklich reimportieren, Bone-Anzahl aus ursprünglicher Quelle vergleichen, 61 Posen je korrigiertem Clip messen. Bisasams Vertexpositionen, Dreiecke und UVs mit der Originalquelle exakt vergleichen.
- `ImportCorrections.py`: einmaliger Unreal-Import in neue `PolishV2`-Namespaces. Originalskelette/-materialien wiederverwenden. Nur die Spezies-Präsentationsbindung ändern; keine Map speichern. Bestehende Zielassets führen zum Stopp.
- `CreateMoveData.py`: einmalig vier verifizierte Datenassets und die zwei Spezies-Lernlisten ergänzen. Kein Aufruf auf gespeicherten Individuen, keine Save-Migration.
- `InspectLive.py`: aktuelle Profile, sieben Clips, LOD-Anzahl und tatsächlich geladene Texturgrößen lesen. Texturgrößen erst nach abgeschlossenem asynchronem Laden als endgültig werten; vorübergehend kann Unreal 32×32-Platzhalter melden.
- `RunMovement.py <frische alphanumerische Kennung>`: echter PIE-Test über den vorhandenen Runner. Dessen Test-Save wird außerhalb jeder Spieländerung per SHA-256 wiederhergestellt. `ReviewMovement.py` dosiert Enhanced-Input-Testeingaben an Wegpunkten analog, um frameabhängiges Überschießen zu verhindern. Keine Änderung der Spielersteuerung.
- `SetQHD.py`: bestehendes Viewportwerkzeug, 2560×1440/100 %. `CheckQHD.py`/`StopQHD.py`: Framebuffergröße und kurze bestehende native Aufnahme prüfen. Keine hochskalierten Bilder als QHD ausgeben.
- `ReviewVisuals.py` / `ReviewVisualsAfter.py`: echte Oberweltbewegung mit ausdrücklich gekennzeichneter temporärer Party-Prüfkonfiguration, unveränderte Kamera und Map. Vor erneutem Lauf frische Ausgabekennung setzen. Nachherprüfung behandelt auch zufällig ausgelöste echte Wildbegegnungen. Dies sind keine identischen Animationsposen vor/nachher; Zufallsziele und Bewegungszeitpunkte unterscheiden sich.
- `ReviewEffects.py`: tatsächliche ClassicBattle-Aktionen mit markierten Runtime-Prüfindividuen. Kein persistenter Map-/Save-Eingriff. Aufnahmen mit bewusst verletztem Testindividuum prüfen Egelsamen-Heilung. Keine erfundenen Effekterfolge: Ereignisse im Result.json überprüfen.

Gemeinsame bestehende Tests: `Tools/StarterExpansionV1/RunModels.py`, `RunCapture.py`, `RunDefeatSave.py`, `RunFullGameplay.py`, `CheckMaps.py`. Jeweils neue Laufkennung; niemals einen vorhandenen Nutzer-Spielstand durch einen fremden Prüfstand ersetzen. Fehlgeschlagene Resultate bleiben als Fehlschläge erhalten. Build/Automation über `Tools/ProjectMaintenance/ProjectQA.py` nur bei geschlossenem Editor.

Gen-2-Datenquellen und Messergebnisse stehen im Prüfbericht. Physischer Controller-Test ist nicht Teil der automatischen Abnahme. Keine universelle Gelände-, Fuß-IK- oder beliebige Distanzfreigabe aus diesen begrenzten Tests ableiten.
