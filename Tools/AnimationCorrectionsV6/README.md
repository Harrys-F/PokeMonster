# Animations- und Modellkorrekturen V6

Nur das aktive Projekt und die vorhandene VisualV2 verwenden. Das native permanente Testgelände ist Voraussetzung; kein Showcase-Spawner und keine neue Map. Medien bleiben ausschließlich unter `Saved/AnimationCorrectionsV6` und `Saved/VisualV2TAAIntegrationV1/Recordings`.

## Quellen und einmalige Migration

`InspectSources.py`, `MaterialDiagnostics.py` und `AuditPlayerAxes.py` lesen die erhaltenen Quellen. `BuildPlayer.py` und `BuildCreature.py` erstellen getrennte bearbeitbare V6-Quellen. `ExportSources.py` exportiert nur diese Quellen; `ValidateSources.py` öffnet alle gepackten Quellen und importiert jede FBX wirklich zurück. Blender mit `--background --python-exit-code 1 --python ...` starten.

Die explizite Option `--refine-unreleased` war ausschließlich für die während der Abnahme korrigierten eigenen Kandidaten vorgesehen. Sie verweigert bereits versionierte Ziele. Nach Veröffentlichung vorhandene Quellen gezielt bearbeiten; historische Erstaufbau-/Importwerkzeuge nicht automatisch erneut ausführen.

`AuditUnreal.py` erzeugt eine geschützte einmalige Ausgangsaufnahme. `ImportCandidates.py` verweigert bestehende V6-Assetverzeichnisse. `RefreshUnreleased.py`, `RefreshOwnPlayerClips.py` und `CorrectOwnGlurakSampler.py` sind dokumentierte Korrekturschritte ausschließlich für eigene unversionierte V6-Assets. `AcceptCandidates.py` erwartet sämtliche ursprünglichen Referenzen und Null-Geschwindigkeitsüberschreibungen, bevor es vier Präsentationen und zwei Arten ändert. Keine Wiederholungsmultiplikation, keine Original-Skeleton-Speicherung und kein Save-/Mapformatwechsel.

## Wiederholbare echte Spielprüfung

Eine saubere vorhandene `ArtSession.py`-Editorsitzung und einen gewöhnlichen PIE-Lauf benutzen. Unmittelbar nach PIE-Start `Review.py` über `ArtControl.py` aufrufen; natürliche Wildkämpfe können den Testgeländezugang später berechtigterweise sperren. Einen gesperrten Zugang niemals als gültige Aufnahme ausgeben.

Zuvor unter `Saved/AnimationCorrectionsV6/ReviewRequest.json` beispielsweise ablegen:

```json
{"label":"NeueEindeutigePruefung","integrated":true,"targets":["Machomei","Myrapla","Nebulak","Glurak","Pikachu","Schiggy"],"eight_views":true,"glurak_seconds":40}
```

`label` muss neu und alphanumerisch sein. `integrated` prüft die tatsächlich aktiven Player-Standardreferenzen. `candidates` dient nur der ausdrücklich bezeichneten PIE-Vorschau, nicht dem Nachweis dauerhaft aktivierter Daten. Benannte Rotator-Komponenten verhindern die nachgewiesene abweichende Python-Positionsreihenfolge. Acht statische Ausrichtungen, echte native Habitatbewegung und die Player-Eingabesequenz sind getrennte Prüfungen; sie beweisen keine lückenlose kontinuierliche Fußkontaktabnahme jedes Pokémon in acht Laufrichtungen.

`AlignedComparison.py` zeigt erhaltene alte und aktuelle Profile im selben gewöhnlichen PIE bei identischer Kamera. Es verweigert ein bestehendes eigenes Ausgabeziel. Auch hier handelt es sich um kontrollierte Darstellungsvergleiche, keine natürlich entstandene Habitatbegegnung.

`EncodeReviews.py` verwendet den bereits vorhandenen lokalen AVFoundation-Encoder aus `Saved/MotionRefinementV5/EncodeSequence`. Fehlt dieser optionale lokale Encoder, endet die Videostufe mit Code 2; echte Frames mit Zeitstempeln bleiben verfügbar. Keine erfolgreiche Videoabnahme behaupten. Unterkapitel nutzen Symlinks auf Originalframes und deren ursprüngliche Zeiten; keine Zwischenbildberechnung. Der Encoder-Quellcode bleibt in `Tools/MotionRefinementV5/EncodeSequence.swift`. Ein Neuübersetzungsversuch blieb in dieser Umgebung in der Swift-Typauswertung hängen; daraus wird kein reproduzierbarer Compilererfolg abgeleitet.

`RunFullGameplay.py <neuerName>` verwendet die bestehende 103-Schritte-Route mit echten Enhanced-Input-Bewegungen. `StartFullGameplay.py` pausiert ausschließlich deren Wegblockade-Zeitüberwachung während zusätzlicher realer Wildkämpfe. `HandleAmbientBattles.py` verwendet nur die vorhandene legale Flucht und bei Bedarf den regulären erzwungenen Teamwechsel; keine Trainer-/Storysperre umgehen. Speicherprüfungen schützen und restaurieren den ursprünglichen Dev-Slot bytegenau. Ein vollständiger Fußlauf mit dem alten Test-Water-Spielstand ist kein positiver 3D-Begleiternachweis; dafür die vorhandenen artspezifischen `RunActiveBattle.py`-Prüfungen ausführen.

`MapChecks.py` lädt und prüft alle vorhandenen Karten, ohne zu speichern. Build und vollständige Automation über `Tools/ProjectMaintenance/ProjectQA.py` ausführen. Physische Controllerprüfung bleibt separat.

Ergebnis und künstlerische Grenzen: `Docs/ANIMATIONS_UND_MODELLKORREKTUREN_V6_PRUEFBERICHT.md`. Ein grüner technischer Test ersetzt keine visuelle Freigabe.
