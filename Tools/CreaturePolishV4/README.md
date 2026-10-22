# Pokémon-Animationsfeinschliff V4

Nur im vorhandenen Projekt und in VisualV2. Keine neue Map, keine Projektkopie.

## Wiederverwendbares Vorführgelände

Mit sauberem Editor die vorhandene `Tools/ProjectMaintenance/ArtSession.py`-Queue
starten. Dann beispielsweise:

```
python3 Tools/CreaturePolishV4/RunShowcase.py MyIdleReview --seconds=10
python3 Tools/CreaturePolishV4/RunShowcase.py MyDirectionReview
python3 Tools/CreaturePolishV4/RunShowcase.py MyReactionReview --reactions --seconds=23
```

Jedes Label muss neu sein. Nur PIE, bestehende VisualV2, zehn bekannte Spezies.
Das Werkzeug erzeugt eine neutrale Vorführfläche am baumfreien westlichen Rand
um −5200/−2300 cm. Floor und zehn Visuals sind transient; keine Begegnungs-IDs,
keine Änderungen an Team, Habitaten oder Karte. Die Spielfigur wird für die
Vorführung vorübergehend versetzt und gesperrt, anschließend zurückgesetzt.
Der native Spawnhelfer erlaubt nur PIE in VisualV2; außerhalb gibt es keinen Spawn.

Native AnimInstance, echte Positionsänderungen bei artspezifischen Referenzspeeds,
alle acht Richtungen in Walk und Run. Zwischen Takes werden Modelle ausdrücklich
zurückgesetzt; diese Schnitte sind **keine** natürlichen Bewegungsvorgänge. Die
Kameraparameter bleiben erhalten. QHD-Framebuffer und 100 % Screen Percentage
werden geprüft. Die normale Figur bleibt für diese reine Modellübersicht verborgen.
Aufnahmen und tatsächliche Aufnahmezeiten liegen ausschließlich unter `Saved`.
Es wird keine erfolgreiche Videoabnahme behauptet.

`--focus=Nebulak` oder `--focus=Glurak --yaw=-45` verschiebt nur den Standort der
bestehenden Spielkamera. `--candidate` ist eine explizite Vorschau anhand der lokalen
Importquittung, kein Spezies- oder Save-Austausch. Im regulären Spiel existiert das
Gelände nicht. Der Spielstand wird ohne Schreiben per SHA vor/nach kontrolliert.

## Technische Prüfung

- `RunTeam.py LABEL`: echte Team-UI/Slate-Eingaben, Begleiter, Save/Load, Kampfsperre.
- `RunActiveBattle.py SPECIES LABEL`: aktive Profile in Welt und beiden Battle-
  Perspektiven. Die ursprüngliche ClassicBattle-Fläche bleibt 2560 × 1080,
  die Weltaufnahmen sind 2560 × 1440. UI-Screenshots haben ihre tatsächlich
  protokollierte Slate-Größe; nicht pauschal als QHD ausgeben.
- `RunRegressionOutcomes.py`: bestehende Enton-/Nebulak-Niederlagenflucht,
  Niederlagen-Autosave und WorldBattle. Stoppt am ersten Fehler.
- `AuditAllSources.py`, `ValidateCandidates.py`: Quellen lesend öffnen,
  alle Animationsframes prüfen und neue FBXs wirklich reimportieren.
- `VerifyAccepted.py`: normalisierter Mapvergleich ohne Tuple-/Listen- oder
  Speicheradressen-Scheinabweichungen. Nur die dokumentierte Außen-Fülllichtänderung
  darf gegenüber dem Ausgangszustand bestehen.

Die beschriebenen Gameplaytests enthalten explizite Laufzeitfixtures. Die natürliche
Produktionsroute wird separat mit `Tools/CreatureExpansionV3/RunFullGameplay.py`
getestet; isolierte Modellaufnahmen sind kein Ersatz dafür.

## Einmalige Quellen- und Importarbeit

`PolishSources.py`, die `Refine*`-/`Limit*`-/`Finalize*`-Werkzeuge und Importskripte
sind **keine** allgemein auszuführende Batchpipeline. Sie dokumentieren die geprüften
Einzelschritte dieses Arbeitsgangs und besitzen SHA-/Namensraum-/Git-Schutzprüfungen.
Bereits versionierte Quellen bzw. freigegebene V4-Assets dürfen sie nicht überschreiben.
Keine automatische Wiederholung auf bearbeiteten Quellen.

Enton: 899 Schwanz- und 173 zentrale Bauchvertices korrigiert, Sohlen gesperrt
beibehalten. Nebulak: Originalgesicht geschützt, äußere Gasbones plus langsamer
Material-WPO, innere Farbvariation und begrenztes TAA-Dithering am Rand. Keine
Volumensimulation. Glurak: ursprüngliche Gewichtung, Original-Skeleton und alle sieben
Originalclips als sichere Rückfalllösung. Nur die dunkle Flügelrückseite wird umgefärbt;
Originaltextur schützt orange Körperbereiche. Große zusätzliche Flügelschläge und der
Glurak-Run-Bauchversuch wurden **nicht** freigegeben. Die verworfenen Gewichtungs-
versuche gehören zur Diagnose und sind keine erfolgreichen Korrekturen.

Vor Rückbindung eines visuellen Meshs prüft der native Helfer Bone-Namen, Eltern
und alle Resttransformationen. Eine absichtlich falsche Spezies muss scheitern.

## Beleuchtung

SkyLight +15 % nicht übernommen. Bestehendes schattenloses Außen-Fülllicht
`VS_SoftSkyFill`: 0,65 → 1,0 nach sechs QHD-Vergleichen. Keine Änderung an Sonne,
SkyLight, Lumen, TAA, Bloom, Belichtung oder privaten Spieler-Fülllichtparametern.
`CompareShadows.py` und `CompareFillLight.py` sind ausschließlich reversible
Laufzeitdiagnosen; sie stellen ihre Ausgangswerte wieder her.

Screenshots, Videos, Testspielstände und Rohlogs niemals stagen.

Die Einmal-Importer dokumentieren den historischen Arbeitsgang und setzen lokale
Prüfquittungen aus `Saved` voraus. Sie sind kein Clean-Clone-Rebuildbefehl. Für
einen späteren Neuimport der endgültigen Blenderquelle ist die bestehende
`Docs/KREATUREN_PIPELINE_V2.md` maßgeblich. Bei Glurak nur den finalen Idle-Mesh-FBX
und das exakt geprüfte Original-Skeleton/die Originalclips verwenden; die sechs
verworfenen Zusatzexports und acht ungenutzten UE-Zwischenassets sind ausschließlich
lokal unter `Saved/CreaturePolishV4/RejectedInputs` erhalten.


## Ergänzung: gewöhnliches PIE-Testgelände (22.10.2026)

Die obige Aussage „Im regulären Spiel existiert das Gelände nicht“ beschreibt
das historische explizite Showcase. Für gewöhnliches VisualV2-PIE gibt es jetzt
einen getrennten, automatisch verfügbaren nativen Entwicklungsbereich. Zugang:
`pm.TestGround.Go`, Rückkehr: `pm.TestGround.Return`. Kein Showcase ausführen.
Details: `Tools/CreatureTestGroundV1/README.md`. Kein Shipping-/Standalone-Inhalt.
