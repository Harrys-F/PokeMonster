# Gameplay- und Controller-Praxistest V1

Prüfadapter für den vorhandenen Stand `45068771`, keine neue Gameplayarchitektur.
Nur VisualV2. Normale PIE-Sitzungen, vorhandene Encounter-, UI-, Animations-,
Save- und Testdienste. Kein physischer Controller-Hardwaretest.

## Schutz und Ausführung

`Baseline.py` erstellt nur Hashes von Nutzerdateien, allen zwölf Maps, Save und
Backup-Verweisen. Keine Kopien. Im sauberen bestehenden ArtSession-Editor:

```sh
python3 Tools/GameplayPraxisV1/Run.py controller EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py battle EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py progression EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py themes EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py evolution EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py wild EINDEUTIGERLABEL Zunderlauf TERRITORIAL Victory
python3 Tools/GameplayPraxisV1/Run.py group EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py repertoire EINDEUTIGERLABEL
python3 Tools/GameplayPraxisV1/Run.py follower EINDEUTIGERLABEL
```

Jeder Label wird nur einmal verwendet; bestehende Nachweise werden abgewiesen.
Nicht während eines eigenen Nutzer-PIE oder parallel aufrufen. Keine manuellen
Saveaktionen während automatischer Sitzungen. `Prepare.py` verlangt eine saubere
VisualV2. `Guard.py` nutzt den **vorhandenen** RAM-Transport von NPCTestGround.Visit
und stellt die Spielertransform sofort zurück. Die dortigen NPCs stammen bereits
aus dem normalen PIE-Weltstart; der Adapter erzeugt keine neuen NPC-Quellen.
Erst danach dürfen vorhandene explizite Team-/Level-/Itemfixtures laufen.
`Teardown.py` stellt temporäre CVars/Editor-Drosselung zurück. Normaler PIE-Stopp
verwirft die isolierten Daten. User-Saves werden weder umbenannt noch kopiert,
restauriert oder überschrieben. Änderungen am Originalhash stoppen die Prüfung.

`Legacy.py` führt die referenzierten bestehenden Prüfskripte aus; nur Nachweisziele
und ausdrücklich dokumentierte zusätzliche Eingabefälle werden angepasst.
Es ist kein Ersatz für Encounter-, Interaktions- oder Save-Verarbeitung.

`EndToEnd.py` erweitert den bestehenden Eingabe-/Physik-Parcours. Ein vorhandenes
Glumanda15-/Glurak36-Testteam wird vorbereitet, Glumanda steht ein XP vor Level16.
Der erste Gegner ist der **unveränderte tatsächliche wilde Mapactor**; kein 1-KP-
Gegner und keine Profiländerung im zusammenhängenden Lauf. Zusätzliche Wildkämpfe
werden regulär per Flucht behandelt. Seitliche Stickeingaben umgehen echte
Hindernisse; keine In-route-Testteleports oder Änderungen der Kollisionen.

`Collision.py` und `Follower.py` verwenden getrennte klar bezeichnete Startpositions-
fixtures. Wildbegegnungen werden nur in diesen isolierten Tests ausgesetzt;
bestehende Landschaftskollisionen bleiben aktiv. `Repertoire.py` verwendet den
vorhandenen XP-Dienst für ein echtes offenes Lernangebot und prüft den RAM-Roundtrip.

`Suite.py` und `RunRemaining.py` dokumentieren den einmaligen seriellen Ablauf
mit festen historischen Labels dieses Auftrags. Nicht blind erneut ausführen;
für neue Durchläufe frische Labels/Ziele wählen. `Movement.py`/`EncodeMovement.py`
haben absichtlich das feste, einmalige Nachweisziel Movement01. Native tatsächlich
präsentierte Frames und Originalzeitstempel; keine Interpolation, kein FPS-Test.

`Restart.py` prüft einen normalen frischen PIE und **explizites** vorhandenes
Laden ohne Speicheraufruf. PIE erzeugt bisher zunächst sein Dev-Team; kein Autoload.
Das bestehende Schema speichert einen Checkpoint, keine beliebige aktuelle
Pawntransform. Ein stationärer RAM-Roundtrip beweist diese Positionspersistenz nicht.

`Inspect.py`, `CollisionInventory.py`, `TraceAPI.py` und `RestartState.py` sind
rein lesende Diagnoseadapter. `MapChecks.py` prüft alle zwölf Maps ohne Speicherung;
`VerifyEditor.py` vergleicht die gesamte Editorszene. `Media.py` benötigt vorhandenes
Pillow und indexiert nur frische echte Bilder. `Summarize.py` schreibt tatsächliche
Ergebnisse einschließlich Wrapper-Exit 1; kein Warnungsfilter und kein Fake-Pass.
`Package.py` prüft alle ursprünglichen Kerndateien und schützt alle Originale.

## Dokumentation und Medien

`Docs/GAMEPLAY_CONTROLLER_PRAXISTEST_V1_PRUEFBERICHT.md`, strukturierte Fakten in
`Acceptance.json`. Vollständige Logs und Originalmedien nur unter
`Saved/ProjectRefinement/GameplayPraxisV1` bzw. den bestehenden nativen Capture-
Verzeichnissen. Keine Medien, Caches, Saves oder Builds committen.
