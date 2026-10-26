# Pokémon-KI V2 – Prüfung

Die sechs Arten verwenden ihre Aktivitäten beim normalen PIE-Start auf VisualV2 automatisch. Es ist kein Testbefehl zur Freischaltung erforderlich. Andere Maps und Begleiter bleiben ausgeschlossen.

Die folgenden Werkzeuge setzen eine saubere, regulär gestartete Editor-Sitzung mit der vorhandenen `Tools/ProjectMaintenance/ArtSession.py`-Warteschlange voraus. Keine zweite Editorinstanz parallel starten. Keine Nutzersaves kopieren oder umbenennen.

```sh
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/PokemonAIV2/Prepare.py
python3 Tools/PokemonAIV2/Run.py connected NeuesEindeutigesLabel
python3 Tools/PokemonAIV2/Run.py visual WeiteresEindeutigesLabel
python3 Tools/PokemonAIV2/Run.py performance NochEinEindeutigesLabel
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/PokemonAIV2/MapChecks.py
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/PokemonAIV2/Restore.py
```

Jeder Lauf nutzt eine neue Evidenzablage und einen eigenen `PokeMonster_SaveV2_Test_…`-Slot. `Run.py` beendet PIE regulär und kontrolliert die Original-Save-Prüfsumme. Die beiden verbundenen Tests enthalten protokollierte diagnostische Spielerpositionierungen; der Fußlaufabschnitt verwendet echte Spieleingaben. Ein physischer Controller-Test wird nicht behauptet.

`Visual.py` zeichnet echte QHD-Spielkamerabilder auf. Sein Sozialabschnitt gewichtet die bestehende Bisasam-Gruppe vorübergehend stärker sozial und hält sie ruhig; das ist ein technischer Testaufbau, keine Behauptung über die spontane Häufigkeit im normalen Spiel. `SocialClearing.py` ist ein zusätzlicher, ausdrücklich temporärer Sichtaufbau mit zwei vorhandenen Bisasam auf einer vorhandenen Wiese. Die ursprüngliche Map wird nie gespeichert. Fehlgeschlagene Aufbauten sind im Prüfbericht separat aufgeführt.

`Performance.py` misst sieben kurze Fälle (1/3/8 vorhandene Instanzen, Aktivitätsmodus aus/an, acht entfernte Instanzen). Die Messflagge ist im normalen Spiel aus. Keine Renderqualität wird verändert; schwankende Gesamtbildzeiten sind kein isolierter GPU-Kostennachweis.

Build/Automation erfolgen bei regulär geschlossenem Editor über `ProjectQA.py` mit neuen Labels. Der strenge Wrapper weist Testwarnungen als Fehler aus. Engine-Startwarnungen und Testergebnis müssen getrennt gelesen werden.

Alle Medien und Rohdaten bleiben unter dem ignorierten `Saved/`-Ordner. `Encode.py` verwendet den bestehenden nativen macOS-Encoder und die tatsächlichen Frame-Zeitstempel, ohne Zwischenbilder zu erzeugen. Seine Eingabeliste bezieht sich auf die im Prüfbericht genannten lokalen Nachweise.
