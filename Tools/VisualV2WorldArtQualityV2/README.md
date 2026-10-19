# Heilhaus World Art Quality V2 – begrenzter Vergleich und Authoring

Diese Werkzeuge verwenden ausschließlich `/Game/Maps/Dev_TestMap_VisualV2`;
keine neue Karte. Keine Änderungen an Kamera, Licht, Schatten, Gameplay oder
Bestands-Topfpflanzen. Private Kandidaten liegen unter
`/Game/Environment/VisualV2WorldArtV2`.

## Erforderliche Projektdateien

- `Art/World/VisualV2WorldArtV2/BaselineInstances.json`: sechs V1-HISM-Gruppen,
  ursprüngliche Mesh-/Materialpfade und alle 175 Transformationen.
- `MeshCandidates.json`: drei geprüfte, geometrisch unveränderte Meshvarianten
  mit einem gemeinsamen Vertexfarben-Material.
- `ArtCandidate.json`: vier begrenzte Bodenmaterialvarianten und neue Positionen.
- Bestehende V1-Materialien, Westland- und NaturalGround-Originalmeshes bleiben
  erforderlich und unverändert.

`RuntimeVariants.Variants(world).apply("V1"|"Merged"|"V2")` lädt diese
versionierten Eingaben. V1 rekonstruiert die ursprüngliche Heilhausgestaltung,
Merged ändert nur die drei Materialabschnitt-Zusammenfassungen, V2 ergänzt die
neue Gruppierung und lokale Texturkoordinatenvariation. Die Teststeuerungen
stellen nach Abschluss V1 wieder her; sie speichern keine Karte.

## Reproduzierbare Messung

Unreal 5.8.2 Mac Development Editor bauen; nur eine eigene Unreal-Instanz,
keine fremden ungesicherten Pakete. `LaunchEditor.py <neues-log-label>
Dev_TestMap_VisualV2` richtet eine explizite, lokale Jobqueue ein.
`RunStudy.py PIE 1` / `RunMatrix.py PIE 1` verwenden Embedded PIE; Qualität 2
jeweils in einem eigenen Start. Niemals Qualitätsstufen über aktive
Reveal-Materialinstanzen umschalten. Für Standalone muss der Editor normal
beendet sein: `RunStudy.py Standalone 1` / `RunMatrix.py Standalone 1`.
Jedes Label ist einmalig; vorhandene Ergebnisse werden nicht überschrieben.

Die TSV-Pläne bestimmen Ausgabeauflösung, Medium/High, SP75/100,
Dorf/Wald/Weg und drei interleavte Wiederholungen. Die unveränderte vorhandene
`pm.EnvPerf2.Run`-Probe zeichnet echte Renderer-Ausdehnungen und AA-Methode
mit auf. Präfix `VGB1_` verhindert alte GI-/Schatten-Diagnosevorgaben.
`pm.WorldArt2.Prepare/Mode` ist ein expliziter, Editor-Development-only-Helfer
für 175 transiente Einzelobjekte; keine automatische Gameplay-Aktivierung,
kein Tick, keine zusätzlichen Kollisionen. Die Varianten No175 und erzwungenes
LOD0 sind ausschließlich Messdiagnosen; keine Übernahme in die Karte.

`Aggregate.py` prüft vollständige Reihen, jeweils drei Läufe,
AA2 und tatsächliche Rendergrößen. FPS = 1000 / Median der Wall-Framezeit;
Gruppenwert = Median der drei Laufmediane. P95 ist die Spannweite der drei
Lauf-P95. All-zero Draw-Call-Zähler dieser Metal-Version sind **nicht messbar**,
keine null Draw Calls. GPU und CPU werden separat ausgewiesen, nicht addiert.

## Begrenzte Asset-Erstellung und Übernahme

`BuildGrassCandidate.py` und `PrepareArtCandidate.py` sind einmalige
Authoring-Schritte für noch nicht vorhandene private Zielassets. Sie ersetzen
keine bestehenden Assets. Keine Decimation, kein Blender-/FBX-Umweg;
Trianglepositionen, UVs und Corner-Normalen bleiben erhalten. Die drei
konstanten Farbmaterialfamilien werden in Vertexfarben übertragen.
`ApplyProduction.py` darf ausschließlich nach Sicht- und Messprüfung laufen.
Es prüft exakt elf erlaubte Actor-Deltas (sechs HISM, fünf Bodenbindings),
alle anderen Actors, Weltparameter und die unveränderte Instanzzahl. Vorher
muss die zentrale Map außerhalb des Projekts gesichert sein. Nur diese Karte
wird gespeichert. Wiederholungsaufrufe stoppen.

`ValidateArt.py`, `RunMapCheck.py`, `Build.py`, `RunQA.py Automation` und
`RunAcceptance.py PIE <neues-label> 1280 720 100` prüfen den gespeicherten Stand.
Der Fußlauf nutzt den vorhandenen Enhanced-Input-Rundweg ohne Testteleports
und sichert/restauriert den tatsächlichen Dev-Slot. Feste Fotopositionen und
Messpunkte werden ausdrücklich separat von diesem Fußlauf eingerichtet.

## Lokale, optionale Nachweise

Rohdaten, Fotos, QHD-Aufnahmen, Engine-Logs, Wärmeprotokoll und Save-Kopien
liegen ausschließlich in `Saved/VisualV2WorldArtQualityV2`,
`Saved/EnvironmentPerfV2` und `Saved/Profiling/CSV`.
Fehlen sie in einem frischen Checkout, sind sie **nicht vorhanden**, nicht
bestanden. Sie können durch neue eindeutig benannte Messreihen neu erzeugt
werden. Keine Kontrollbilder, Videos oder Roh-Frame-CSVs in Git aufnehmen.
Der geprüfte verdichtete Messbericht steht in Docs und ist keine
Voraussetzung für Gameplay oder Build.

## Bekannte Grenze des nativen CSV-Endes

Die bestehende Probe beendet Standalone direkt nach dem letzten Segment.
Dessen zusätzliche Profiler-CSV kann vor dem asynchronen Schreiben leer
bleiben. Die eigene Wall-Frame-/Auflösungsdatei ist vollständig. In den vier
nativen Reihen dieses Tests betrifft das jeweils nur das letzte Segment.
Die Auswertung weist deshalb je Zusatzcounter die Zahl gültiger Läufe aus
(`*_runs`); bei den betroffenen Gruppen zwei statt drei GPU-/CPU-Läufe.
Es werden keine fehlenden Zeiten geschätzt oder aus anderen Szenen kopiert.
Drei vollständige FPS-/P95-Läufe bleiben für jede Gruppe vorhanden.
