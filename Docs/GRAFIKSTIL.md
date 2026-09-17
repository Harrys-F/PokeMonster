# Grafikstil – PokeMonster

## Verbindliche Stilrichtung

PokeMonster verwendet einen modernen, handgezeichneten und hochauflösenden 2D-Stil mit einer leicht schrägen 3/4-Top-Down-Perspektive.

Die Hauptreferenz ist die bereitgestellte Szene mit dem freundlichen Hügelland, den Erdhäusern, Gärten, Steinbrücken und dem Bachlauf.

Besonders verbindlich sind:

- Kameraperspektive der ersten Referenz
- Figurengröße der ersten Referenz
- sichtbare Gebäudefassaden
- räumliche Tiefenwirkung
- übersichtliche Wege und begehbare Flächen
- handgezeichnete, detailreiche Umgebung
- hochauflösende Sprites statt grober Pixelgrafik
- klare Trennung zwischen Figuren und Hintergrund

Die technische Umsetzung der Kamera wird erst in einer Testszene festgelegt. Entscheidend ist zunächst die visuelle Wirkung. Eine orthografische oder nahezu orthografische Kamera soll geprüft werden.

## Kameraperspektive

- leicht schräger Blick von oben
- keine streng senkrechte 90-Grad-Draufsicht
- Gebäude, Mauern, Brücken und Felsen zeigen sichtbare Vorderseiten
- Höhenunterschiede müssen klar erkennbar sein
- Spielfigur und wichtige Wege müssen trotz vieler Details gut lesbar bleiben
- die Kamera folgt der Figur weich und ohne hektische Bewegungen
- Zoom und sichtbarer Kartenausschnitt orientieren sich an der ersten Referenz

## Figurengröße

Die Spielfigur soll im Bild ungefähr dieselbe relative Größe wie in der ersten Referenz besitzen.

Vorläufige Gestaltungsregeln:

- Figur ungefähr 7 Prozent der sichtbaren Bildhöhe
- Türen ungefähr 1,5 bis 2 Figuren hoch
- normale Wege mindestens 2 bis 3 Figuren breit
- Bäume und größere Landschaftselemente deutlich größer als die Figur
- Kreaturen dürfen abhängig von ihrer Art stark unterschiedliche Größen besitzen
- Figuren und Kreaturen erhalten klare Silhouetten und etwas weniger Hintergrunddetails

Die exakten Pixelgrößen werden erst nach einem Test mit der endgültigen Kamera und Zielauflösung festgelegt.

## Darstellung und Tiefenwirkung

Die Welt bleibt technisch und gestalterisch eindeutig 2D, soll aber mehr Tiefe als klassische frühe Pokémon-Spiele vermitteln.

Dafür vorgesehen:

- mehrere sichtbare Höhenebenen
- Vordergrund-, Spielebene- und Hintergrundelemente
- Überlagerung von Figuren durch Bäume, Mauern und Gebäude
- weiche Kontaktschatten
- zurückhaltende dynamische Beleuchtung
- Wasser, Wasserfälle, Nebel, Lichtstrahlen und Lava als animierte Elemente
- leichte Parallaxenwirkung, wenn sie die Lesbarkeit nicht beeinträchtigt

## Regionale Bildsprache

### Hügelland und Startregion

- freundliche warme Farben
- Erdhäuser und kleine Gärten
- Blumenwiesen
- natürliche Wege
- Bachläufe und Steinbrücken
- einladende, friedliche Atmosphäre

### Uralter Wald

- große alte Bäume
- dichter Pflanzenbewuchs
- Ruinen und verwitterte Steinbauten
- Nebel und Lichtstrahlen
- Wasserläufe und Holzbrücken
- geheimnisvolle, aber nicht dauerhaft düstere Stimmung

### Monumentale helle Stadt

- heller Stein
- Terrassen und große Treppen
- Bögen, Brücken und Wasserkanäle
- Brunnen und Wasserfälle
- gepflegte Pflanzen
- blaue und goldene Akzente
- großzügige, elegante Architektur

### Dunkles Endgebiet

- dunkler Fels und schwarze Architektur
- Lavaflüsse und Abgründe
- Ruinen, Statuen und große Brücken
- orangefarbene Lavabeleuchtung
- vereinzelte grüne magische Lichtquellen
- bedrohliche und monumentale Atmosphäre

Alle Regionen müssen trotz unterschiedlicher Farbwelten wie Bestandteile desselben Spiels wirken.

## Modularer Aufbau

Die Spielwelt soll nicht aus einzelnen riesigen Hintergrundbildern bestehen.

Bevorzugt werden wiederverwendbare Module:

- Bäume und Pflanzen
- Felsen und Klippen
- Wege und Bodenflächen
- Mauern und Zäune
- Bögen und Säulen
- Treppen
- Brücken
- Gebäudeteile
- Vordergrundelemente
- Wasser- und Lavaelemente
- Dekorationen
- Licht-, Nebel- und Partikeleffekte

Module dürfen in mehreren Varianten erstellt werden, damit Wiederholungen nicht auffallen.

## Höhen und Begehbarkeit

Nicht jede dargestellte Höhe muss eine echte begehbare Ebene sein.

Bei jeder Szene muss eindeutig festgelegt werden:

- welche Flächen begehbar sind,
- welche Treppen tatsächlich benutzt werden können,
- unter welchen Brücken die Figur hindurchgehen darf,
- welche Höhen nur optisch dargestellt werden,
- wo Kollisionen und Ebenenwechsel liegen.

Komplexe Höhenwechsel werden zuerst in einer kleinen Testszene geprüft.

## Lesbarkeit

Optische Details dürfen die Spielbarkeit nicht beeinträchtigen.

Deshalb:

- begehbare Wege bleiben erkennbar,
- Ausgänge und Übergänge sind visuell verständlich,
- interaktive Objekte heben sich dezent ab,
- Figuren verschwinden nicht dauerhaft hinter Dekorationen,
- wichtige Kreaturen und NPCs sind leicht zu erkennen,
- Vordergrundelemente können bei Bedarf transparent werden.

## Stil-Testszene

Vor der Produktion größerer Mengen an Grafiken wird eine kleine Testszene erstellt.

Sie soll enthalten:

- Spielfigur in der beschlossenen Größe
- Hütte oder Erdhaus
- Weg
- Bäume und Büsche
- Felsen und Mauern
- Bach oder kleiner Fluss
- Steinbrücke
- unterschiedliche Höhen
- Vordergrundüberlagerung
- Beleuchtung und Schatten
- animiertes Wasser

Mit dieser Szene werden Perspektive, Figurengröße, Kamera, Kollisionen, Tiefenwirkung, Lesbarkeit und Leistung geprüft.

Erst nach Freigabe dieser Testszene werden größere Mengen an Weltgrafiken produziert.

## Umgang mit Referenzbildern

Referenzbilder dienen zur Beschreibung von:

- Perspektive
- Größenverhältnissen
- Farbwirkung
- Beleuchtung
- Atmosphäre
- Architektur
- Detailgrad

Sie werden nicht unverändert als Spielkarten übernommen. Geschützte Motive, Figuren, Logos und konkrete Designs werden nicht einfach kopiert.
