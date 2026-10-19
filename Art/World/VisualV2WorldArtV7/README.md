# VisualV2 World Art Quality V7

V6-Stil auf die übrigen bestehenden Außenwege und ihre Landschaft übertragen. Keine neue Karte; keine neuen Meshes oder Texturen. Die drei privaten Materialvarianten referenzieren die vorhandenen V4-/V5-Texturen. Die vorhandenen sechs Boden-/Weg-Komponenten erhalten neue Materialbindungen; alle bestehenden Instanzen, Baumpositionen und Gameplay-Akteure bleiben erhalten. Zusätzliche dekorative HISM-Gruppen verwenden vorhandene Modelle und deren Instancing-Materialien.

`RouteField.json` und `RouteField.hlsl` beschreiben die existierenden fünf Weglinien mit 118 vereinfachten Segmenten. Maximaler Abstand zur tatsächlichen 16-Schritt-Catmull-Rom-Mittellinie <4 cm. Nur sichtbare Erd-/Grasdeckung und Farbmischung ändern sich. Die zugrundeliegenden Meshes und Kollisionen ändern sich nicht. Unterschiedliche Breiten, gekrümmte Kanten und Abnutzung verwenden dasselbe Verfahren wie V6. Schutzbereiche: Heilhaus V4, V6-Musterpflanzungen, Türen, Interaktionen, Brücke und Wasser.

`Scope.json` dokumentiert jede hinzugefügte Instanz und die sechs Materialbindungen. Neue Pflanzen sind visuelle, kollisionsfreie Gruppen ohne Tick, zusätzlichen Schattenwurf oder Distanzfeld-/GI-Beitrag, wie die vorhandenen V5-/V6-Details. Originale Bäume, Figuren und Gebäude behalten ihren Schattenwurf.

## Getrennte Schattenuntersuchung

Keine Schattenänderung wird gespeichert. `Photos.py` stellt nur in temporären Spielwelten am vorhandenen Sonnenlicht `shadow_amount` auf 1, 0.5 oder 0. Die unveränderten Licht- und Postprocessing-Einstellungen bleiben Grundlage. Diese Parameterwerte sind Diagnosewerte, keine Übersetzung des visuellen 50-Prozent-Ziels. Vergleichsbilder und technische Prüfung entscheiden über die Wirkung. Eine generelle Tonwertanhebung, Emissive-Aufhellung oder Änderung von Skylight/Lumen/Exposure wird nicht als Schattenlösung eingesetzt.

## Reproduktion und Grenzen

Die Skripte unter `Tools/VisualV2WorldArtV7` öffnen ausschließlich die bestehende zentrale Karte. Erzeugte Aufnahmen, Quellkarten-Sicherung, umfangreiche Szenenprüfungen und Testausgaben liegen unter `Saved/VisualV2WorldArtV7` und im externen Review-Verzeichnis. Sie gehören nicht zum Git-Upload. `BuildRouteField.py` erzeugt einen neuen Vergleichsordner und überschreibt keine Autorenquelle. Material- und Map-Anwendung verweigern einen unerwarteten oder schmutzigen Ausgangszustand.

Die visuellen Ergebnisse benötigen Harrys Abnahme. Der vorhandene Standard der Lichtquellen, Schatten, TAA und Kamera bleibt erhalten. Es gibt keine Runtime-Performancefreigabe oder behaupteten FPS-Gewinn.
