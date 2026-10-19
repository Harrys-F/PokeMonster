# VisualV2 World Art Quality V1 – begrenzter Heilhausbereich

Dies ist ein Autoren-/Reviewwerkzeug, kein Gameplay- oder Buildsystem. Die gespeicherte zentrale Karte und die privaten Materialien sind das Ergebnis. Keine neue Map. Keine Änderungen an Lighting, Originalschatten, TAA, Kamera, Collision oder NPC-Identitäten.

## Schutz und einmalige Erstellung

Nur im schlanken Worktree verwenden. Vor einem Autorenlauf den Git-Status prüfen, sämtliche Editoränderungen klären und die zentrale Map außerhalb des Projekts per SHA-256-gesicherter Bytekopie sichern. `LaunchEditor.py` öffnet ausschließlich eine bestehende, explizit gewählte Karte in einem frischen Editor; `Startup.py` erfasst die Ausgangssignatur. Niemals eine bestehende Arbeitsinstanz schließen oder ungesicherte Pakete verwerfen. Die feste externe Beweisablage gilt für diesen Auftrag, nicht für beliebige spätere Wiederholungen.

Die Autorenfolge war `ApplyArt.py`, `PolishForecourt.py`, `JoinForecourt.py`, `FixLegacyApproach.py`. Sie dokumentiert die tatsächlichen Sichtprüfungsiterationen. **Nicht auf den fertigen Stand erneut anwenden.** Fertigmarker und neue Assetpfade verhindern eine versehentliche Stapelung; bei Teilfehlern ausschließlich die eigenen neu angelegten Pakete prüfen. Keine Lösch-/Reset-Fallbacks. `HealingHouseDressing.json` unter `Art/World/VisualV2WorldArtV1` enthält die Platzierungen und alten/neuen Materialzuweisungen zur Wiederherstellung.

## Prüfungen und lokale Nachweise

`ValidateArt.py` prüft die Autorenkonfiguration und die 175 NoCollision-/NoShadow-Instanzen. `Build.py`, `RunQA.py Automation` und `RunMapCheck.py <neues_Label>` laufen nur bei geschlossenem Editor. Die frische Ladeprüfung ordnet Komponenten nach ihrem eindeutigen Namen zu; sämtliche Werte bleiben exakt verglichen, ohne numerische Toleranz oder Feldentfernung. Die Reihenfolge von Unreal-Komponentenlisten ist kein persistenter Inhalt.

`RunAcceptance.py PIE <neues_Label> 1280 720 75` verwendet unverändert die bestehende vollständige Enhanced-Input-Route aus `Tools/VisualV2QualityV2/FootTest.py`. Nur eigene Ausgabepfade und eine Tür-Bildfolge werden angebunden. Der Dev-Spielstand wird vor dem Test gesichert und sein ursprünglicher Inhalt bzw. seine ursprüngliche Abwesenheit danach wiederhergestellt. Kein Testteleport auf dieser Route. Die optionale native Aufnahme bleibt innerhalb des unveränderten sicheren Ausgabeordners der bestehenden TAA-Capture-Komponente.

`Photos.py` verwendet für Vergleichsstillbilder ausdrücklich feste Pawn-Startpositionen, wartet auf die echte Spielkamera und den tatsächlich geschriebenen Screenshot. Das ist unabhängig vom Fußlauf. `ComposeReview.py` kopiert die echten 2560×1440-Originale SHA-verifiziert und beschriftet verkleinerte Paare; keine generierten Bilder, kein Bild-Retouching.

`BasicPerformance.py`/`Plans` erfassen lediglich eine kurze Heilhaus-Kontrolle, drei Wiederholungen pro Ausgabeprofil mit je fünf Sekunden Warm-up und Messung. Keine umfassende GPU-Analyse und keine Optimierung. `Summarize.py` übernimmt den vorhandenen CSV-Auswerter. Null-/ungenügende Zähler dürfen nicht als Messung behauptet werden. Auflösung und tatsächliches View-AA kommen vom vorhandenen Probe. `VGB1_`-Labels verhindern die alten Environment-Licht-/Schattenprofile.

Fehlende lokale Kontrollbilder/CSV-Dateien sind keine fehlenden Spielassets und keine Buildfehler. Bei erneuter Abnahme neue Labels/Ausgabeordner verwenden; vorhandene Nachweise nicht überschreiben. Rohmedien bleiben außerhalb der Git-Sicherung. Details und Einschränkungen im Prüfbericht.
