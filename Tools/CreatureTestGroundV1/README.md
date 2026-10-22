# Dauerhaftes Pokémon-Testgelände V1

Das native `PokeMonsterCreatureTestGround`-WorldSubsystem startet **automatisch bei
jedem gewöhnlichen PIE-Start der bestehenden VisualV2**. Kein Python-Showcase,
Automationstest, zusätzlicher Startparameter oder Map-Speichern erforderlich.
Die reproduzierbare Entwicklungsfunktion ist versioniert; die Laufzeitobjekte
selbst sind bewusst transient. In anderen Maps, Standalone und ausgelieferten
Spielen wird das Gelände nicht erzeugt.

## Zugang für Harry

1. `/Game/Maps/Dev_TestMap_VisualV2` öffnen und normal **Spielen / Play** drücken.
2. Falls schon ein Kampf, Dialog oder Menü läuft: regulär beenden/schließen.
   Teleports sind außerdem im Innenraum und während Niederlagenrückkehr gesperrt.
3. Unreal-Konsole öffnen und `pm.TestGround.Go` eingeben. Alternativ **Shift+F1**,
   unten im Output-Log die Eingabeart **Cmd** (nicht Python) wählen, den Befehl
   ausführen und wieder in den Spielviewport klicken.
4. Mit der normalen Steuerung frei umherlaufen. Die niedrig eingefasste Fläche
   ist 56 × 36 m groß, jeder Testbereich hat 4,30 m Radius. Die vorhandene
   Spielkamera bleibt unverändert; nicht alle zehn weit auseinander stehenden
   Tiere passen gleichzeitig in ein normales Kamerabild.
5. Optional `pm.TestGround.Go 1` bis `pm.TestGround.Go 10` für einzelne Stationen.
6. `pm.TestGround.Return` bringt die Figur zur ursprünglichen Position vor dem
   **ersten** Besuch zurück. Weitere Stationswechsel überschreiben den Anker
   nicht. Bei blockiertem Rückkehrziel bleibt der Anker erhalten. Er gilt nur
   für den aktuellen PIE-Lauf und dieselbe Spielfigur.

Keine neue Tastatur- oder Controllerbelegung. Konsole/Output-Log sind vorhandene
Unreal-Entwicklungswerkzeuge, keine neue Spielinteraktion.

## Positionen (Unreal-Weltkoordinaten in cm)

Mitte: **X −7500, Y −4000, Boden Z 0**. Boden reicht von X −10300 bis −4700 und
Y −5800 bis −2200. Kein bestehender platzierter Actor überschneidet diese Fläche
laut Bestandsprüfung; die normalen Wildhabitate werden nicht verändert.

| Station | Art | Bereichsmitte X / Y | Originalgröße |
|---|---|---|---|
| 1 | Glumanda (`Zunderlauf`) | −9500 / −4700 | 60 cm |
| 2 | Schiggy | −8500 / −4700 | 50 cm |
| 3 | Bisasam | −7500 / −4700 | 70 cm |
| 4 | Pikachu | −6500 / −4700 | 40 cm |
| 5 | Myrapla | −5500 / −4700 | 50 cm |
| 6 | Enton | −9500 / −3300 | 80 cm |
| 7 | Machomei | −8500 / −3300 | 160 cm |
| 8 | Nebulak | −7500 / −3300 | 130 cm |
| 9 | Gengar | −6500 / −3300 | 150 cm |
| 10 | Glurak | −5500 / −3300 | 170 cm |

Die tatsächlichen Positionen variieren durch freies Wandern. GroundOffset,
Nebulaks Schweben und Gluraks bestehendes bodennahes Schweben bleiben erhalten.

## Animationen beobachten

- `pm.TestGround.Mode auto`: Standard; zeitversetzt Ruhe, Wandern und schnelleres
  Laufen, mit vorhandenen artspezifischen Geschwindigkeiten und Bodenprüfungen.
- `pm.TestGround.Mode idle`, `walk` oder `run`: gewünschte vorhandene Rolle.
  Walk/Run lassen weiterhin natürliche Pausen und sicheres Drehen zu; sie
  erzwingen kein Gleiten und überschreiben keine Animationsassets.
- `pm.TestGround.React attack`, `hit`, `faint` oder `happy`: vorhandene Reaktion
  aller zehn Visuals. Kein Schaden, Kampf, Fang oder dauerhafter K.O.-Zustand.
- Glurak kann im Auto-/Walk-Modus seine bestehende Abheben-/Schweben-/Landenfolge
  zeigen. Idle pausiert die Wanderkomponente; dadurch wird kein Abheben erzwungen.
- Außerhalb 35 m Abstand zur Spielfigur pausiert die Wanderbewegung. Keine
  zusätzlichen Landschaften, Lichter oder Pokémon-Modelle.

Die Testtiere sind **reine VisualActors**, tragen `PokemonDevelopmentSpecimen`
und sichtbare TEST-Nummern. Kein WildActor, Interactable, Begegnungs- oder
Instanz-ID; keine Änderungen an Team, Inventar, Checkpoints oder Saveformat.
Ein vorhandener regulärer Begleiter bleibt unabhängig und kann mitkommen.

## Wiederholbare Prüfungen

`Observe.py` liest ein **schon laufendes normales PIE**, ohne Actors zu erzeugen.
`Acceptance.py` beobachtet dieselben zehn nativen Exemplare, führt die
Konsolenbefehle und simulierte Enhanced-Input-Bewegung aus. Es schreibt keine
Assets oder Spielstände. Vorher unter `Saved/ProjectRefinement/TestGroundV1/`
`AcceptanceRequest.json` mit einem neuen alphanumerischen `label` anlegen und
`Observe.py` einmal ausführen. Für weitere Beobachtungen `ObserveRequest.json`
mit einem neuen alphanumerischen `label` setzen und dieses als `observation` in
`AcceptanceRequest.json` angeben. Vorhandene Nachweise werden nicht überschrieben.
`MapChecks.py` prüft alle bestehenden Karten lesend und kehrt zur VisualV2 zurück.
`CompanionProbe.py` ist ausdrücklich eine zusätzliche **ungespeicherte Party-Fixture**
mit drei vorhandenen Startern, um einen echten 3D-Begleiter neben den zehn
Testtieren zu prüfen. Nur in frischem PIE starten und danach PIE beenden;
sie ist kein unveränderter Normalspiel-Nachweis.
Diese Prüfscripte sind **nicht erforderlich**, um das Gelände im normalen PIE
zu besuchen. Eingabesimulation ist kein physischer Controller-Nachweis.

Rohprotokolle, QHD-Screenshots und Prüfspielstände bleiben ausschließlich unter
`Saved`. Sie werden nicht nach GitHub hochgeladen.


Für die vollständige bestehende Fußroute im ersten Terminal
`python3 Tools/WildEncountersV2/RunFullGameplay.py EIN_NEUES_LABEL` starten.
Nach Start der Route im zweiten Terminal optional über `ArtControl.py script`
`Tools/CreatureTestGroundV1/HandleAmbientBattles.py` und `WatchFoot.py` anhängen.
Der erste Helfer beendet zusätzliche echte Wildkämpfe im späten Waldabschnitt
regulär über die vorhandene Fluchtaktion; Trainer-/Story-Fluchtverbote bleiben
wirksam. Er verändert weder Routenpunkte noch Habitate, Spielfunktionen oder
Spielstände. Der zweite Helfer sammelt nur Blockadebeobachtungen. Beide sind
Prüftreiber, niemals für die Verfügbarkeit des Geländes erforderlich. Der
bestehende Runner schützt und restauriert die ursprüngliche Dev-Save-Datei.
