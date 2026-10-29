# Pokémon-Modelle V4

Nur im aktiven PokeMonster-Projekt. Neue Art `Raichu`/Dex 026, keine Änderungen an Originalmodellen, Maps oder Rendering. **Technisch integriert – visuelle Freigabe ausstehend.** Das Modell ist ein eigenständig in Blender modellierter Kandidat, kein umgefärbtes Pikachu, kein externer Download.

## Bestand und Quellen

`Inventory.py` liest AssetRegistry, die zentrale spielbare Artenregistrierung, Präsentationen/Clips und Modellquelldateien; keine Assets werden gespeichert. `InspectSources.py` öffnet sämtliche Pokémon-Blenderdateien ohne Speichern. `InspectIncoming.py` liest alle 38 Pokémon-GLBs, prüft UVs/Topologie/Bilder und rendert kleine Diagnoseansichten. Alle Nachweise unter `Saved/ProjectRefinement/ModelsV4`; keine dieser Originalquellen wird verändert. UV-getrennte Randkanten sind kein alleiniger Nachweis von Löchern.

## Neue eigene Raichu-Quelle

Blender 5.2.2 im Hintergrund, keine laufende Sitzung überschreiben:

1. `BuildRaichu.py`: verweigert vorhandene Quelle ohne ausdrückliches `-- --revise`; erzeugt ausschließlich `Art/Characters/Creatures/Raichu/Source/Raichu_V4.blend`. `--revise` würde eigene Handbearbeitung ersetzen und ist kein allgemeiner Reimportbefehl.
2. `AnimateRaichu.py`: benötigt eine Quelle ohne Actions, erstellt sieben eigene in-place Rollen, Fußkontakt-IK und FBX. Bestehende handbearbeitete Actions werden nicht stillschweigend ersetzt. Körperhöhe ca. 80,9 cm, Referenz 80 cm, keine Actor-Skalierung. Der Vorwärtssturz richtet die tiefste deformierte Oberfläche in jedem Sample am Boden aus.
3. `ValidateSource.py`: Quelle und alle sieben FBX tatsächlich erneut öffnen; normalisierte deformierende Gewichte, UVs, Maßstab, Bones und Schleifenschluss prüfen. Numerische Fußdaten ersetzen keine optische Bewegungsabnahme.
4. `RenderSource.py`, `RenderMotionSource.py`: tatsächliche Blenderbilder. Letzteres mit `-- --faint` für den Ohnmachtsclip. Stillbilder sind kein Echtzeitvideo.
5. `ImportRaichu.py`: ausschließlich Erstimport in den neuen Raichu-Namensraum. Abgeschlossenen Import nicht erneut ausführen. Begrenzte Wiederaufnahme der eigenen unterbrochenen Erstoperation verlangt den lokalen Baseline-Nachweis; kein Überschreiben vorhandener Originalassets. Neues Skeleton, sechs einfache Materialien und sieben AnimSequences verwenden den bestehenden nativen Visual-Proxy.

Artendaten und Quellen: `ReferenceSources.json`; Gen-2-Initiative 100, keine spätere Erhöhung auf 110. Kein neuer Wildspawn, keine neuen Lebensraumprofile. Die schon vorhandene Pikachu-Regel und der bereits vorhandene Donnerstein werden durch die neue gültige Zielart nutzbar. Keine Änderung am Save-Schema 11.

## Wiederholbare Gameplayprüfung

`Run.py <absoluter Saved/ProjectRefinement/ModelsV4/Request.json>` akzeptiert nur einen neuen eindeutigen Labelnamen und eine bestehende QA-Fixture unter Saved. Beispiel: `{"label":"Native03","fixture":"/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2PokemonWaterTeamV1/Functional05/InitialTeam.sav","timeout":850}`.

Verwendet einen eigenen UserDir, normale Beutel-/Teamwahl und bestehende Entwicklung V3/V2.1, echtes Level-11-Pikachu, Abbruch, Schreibfehler im ausschließlich eigenen Testordner, Wiederholung, erfolgreichen Verbrauch, Begleiter, Teamsortierung, Save/Load, acht Richtungen und Modelltestbefehle. Temporäre Standortwechsel sind explizite Testaufstellung; keine Behauptung eines durchgehenden Fußlaufs. Wildkämpfe verwenden echte Habitatakteure und deren normale Interaktionsprüfung. Keine Freigabe eines physischen Controllers durch Softwaretests behaupten.

Der Launcher beendet keinen hängenden Prozess. Reguläres Spielende erfolgt über Unreal. Vor PIE den bestehenden Save-Dienst auf einen isolierten `PokeMonster_SaveV2_Test_...`-Slot im eigenen Editor-UserDir setzen. Nicht mit einem RAM-Preview kombinieren.

Bestehende Befehle: `pm.TestGround.List`, `pm.TestGround.Go Pikachu`, `pm.TestGround.Go Raichu`, `pm.TestGround.Mode idle|walk|run|turn|directions|auto`, `pm.TestGround.React attack|hit|faint|happy`, `pm.TestGround.Reset`, `pm.TestGround.Return`. Neue Modelle erscheinen über den vorhandenen AssetManager, ohne zweite Liste oder Mapänderung.
