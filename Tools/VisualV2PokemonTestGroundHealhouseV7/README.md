# VisualV2 Pokémon-Testbereich, Heilhaus und Karpador V7

Nur das bestehende Projekt verwenden. Originale und Nutzersaves erhalten. Große Nachweise ausschließlich unter `Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7/`; keine Kontrollbilder/Videos in Git.

- `EditorAudit.py`, `RegistryReport.py`, `SceneAfter.py`, `MaterialAudit.py`: tatsächliche Arten-/Importmetadaten, Modelle, Skelette, Animationen und Szenenbindungen lesen. `SceneBefore.json` niemals überschreiben.
- `AuthorRoom.py`: einmalige private V7-PBR-Graphen und ausschließlich Materialbindungen des bestehenden versetzten Heilhauses; keine Raum-/Licht-/Kollisionsänderungen. Bewachter Autorierungslauf, kein allgemeines Reparaturwerkzeug.
- `GeneratePlasterGrain.py`, `PolishPlaster.py`: kleine eigene nahtlose numerische Putz-Normale und private Graphanbindung. Keine Originaltexturen bearbeiten. `PruneOwnMaterials.py` entfernt unverbundene Knoten ausschließlich aus den fünf eigenen Materialien; `SaveOwnMaterials.py` verweigert fremde Pakete.
- `GalleryReview.py`: alle 19 spielbereiten und 49 statischen Ziele, tatsächliche gleichzeitige Präsenz, Begleiter, Rückkehr/Facing/Kamera, vorhandene Modi und echte QHD-Aufnahmen. Die separate senkrechte Diagnoseübersicht stellt ihren temporären Blickgeber wieder her. Normale Third-Person-Kamera unverändert.
- `GameplayReview.py`: zusammenhängender realer Eingaberundgang ohne Video, danach vollständiger Modellbesuch im selben Prozess, normale Dialoge/Kampf/Fang/Team, Innenraum, isolierter Save/Load und echter Kartenwechsel. Die Galerie kann als Generator ohne zusätzliche Tick-Schleife eingebunden werden.
- `InteriorReview.py`: Kampf/AP-Verbrauch, Fang, vier sichtbare Wände, acht Kamerablicke, tatsächliche Heileransprache und vollständige HP/AP-Wiederherstellung, Türgänge bei Tempo 1/2/3, isolierter Save/Load.
- `ObservePond.py`: vier Minuten natürliche Beobachtung; keine erzwungenen Ziele, Uhrpause oder Video im Messfenster. `PondCoverageReview.py`: sechs Minuten und tatsächliches Tiefen-/Kollisionsraster. `PondFinalReview.py`: endgültige Langstreckenkorrektur, sechs Minuten, kurzes echtes Video und anschließender regulärer Kampf/Fang/Begleiter.
- `CaptureBenchmark.py`: drei vorhandene QHD-/C75-/High-Stellen, dreimal sechs Sekunden nach vier Sekunden Einlauf, Fotos getrennt; zusätzliche Einzelstellen klar getrennt. `AllModelsBenchmark.py`: zusätzliche Belastung mit allen 68 geladenen Darstellern; kein identischer Ausgangszustand zur ursprünglichen Bibliotheksbelegung.
- `PairedCost.py`: rein temporäre Diagnose alter Raum-Materialien und entfernter Darsteller, wechselnde Reihenfolge. Keine Produktionsänderung daraus ableiten, wenn der Nutzen nicht konsistent messbar ist. Für reale Abläufe ist die jeweilige `RuntimeUsed.py` maßgeblich.
- `LaunchEditor.py`, `RunNative.py`, `RunAutomation.py`, `MapChecks.py`: eigene isolierte Prozesse; keine automatische gewaltsame Beendigung. Nie eine vorhandene Nutzer-Editorsitzung schließen. Für Wiederholungen neue Labels verwenden. Der strenge Wrapper bewertet die tatsächlich exportierte funktionale Testserie, einschließlich Warnungen/Auslassungen; Engine-Startmeldungen separat prüfen.
- `ReviewCapture.py`, `EncodeReviews.py`: begrenzte echte Unreal-JPEG-Folgen und vorhandener AVFoundation-Encoder, Original-Spielzeitstempel und Dekodierprüfung. Aufnahme-FPS niemals als normale Gameplay-FPS ausgeben. Keine Framevervielfachung/Interpolation.
- `Analyze.py`, `VerifyProtection.py`: echte CSV-/Positionsdaten, Szenenvergleich und Start-SHA-Prüfungen. Beobachtete Strecken aus Positionsstichproben von Gesamtzählern seit Spawn unterscheiden.

## Bedienung und Erweiterung

`pm.TestGround.List`, `pm.TestGround.Go <Name|1..19>`, `pm.TestGround.Go Modell:<Name>`, `pm.TestGround.Return`, `pm.TestGround.Mode auto|idle|walk|run|turn|directions|reset`, `pm.TestGround.Reset`, `pm.TestGround.React attack|hit|faint|happy`.

Beim ersten Besuch wird die ganze Sammlung schrittweise einmalig geladen. Anschließend bleiben alle Darsteller bis zum Ende dieser Spielwelt physisch bestehen, auch nach Return. Statische Kandidaten haben keine KI, kein Rig und keine Bewegungsanimation; nur Idle/Inspektionsdrehen/Reset. Importmaßstab ist kein freigegebener Artmaßstab.

Neue spielbereite Arten über das bestehende Artenregister integrieren. Neue statische Unreal-Importe im bisherigen `ModelIntakeV6/<Modell>/...`-Pfad werden anhand der Asset-Registry und tatsächlicher Größenmetadaten erkannt. Neue PIE-/Spielsitzung startet den dokumentierten Aktualisierungsvorgang. Kein manuell gepflegter zweiter Artenkatalog und kein Umbau jedes einzelnen Testfelds.
