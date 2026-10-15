# V4 – Manuelle Kopf-Sculpt-Sitzung

## Ausgangspunkt und Sicherheit

`Hobbit_NPC_V4_HeadSculpt.blend` ist eine separate V3-Ableitung. Im Sculpt Mode ist ausschließlich `HNV4_Body` aktiv; der aktive Shape Key heißt `V4_LimitedHeadFormPass`. Seine Stärke 1 zeigt den begrenzten Formpass, 0 den lokal verdichteten unveränderten V3-Kopf. Keine finale Art-Freigabe.

Körper, Hände und Füße sind über `.sculpt_mask` vollständig maskiert; der Halsübergang besitzt eine 10-mm-Überblendung. X-Symmetrie an, Y/Z aus. Dyntopo, Voxel Remesh und globale Subdivision **nicht einschalten**. Keine weiteren Meshes auswählen. Vor einer Sitzung unter einem neuen Namen im Ordner SculptV4 speichern. V1–V3 nicht speichern.

## Referenzen und Ansicht

Die Collection `HNV4_REFERENCE_IMAGES_TECHNICAL_V3` enthält vier gepackte, gesperrte Image Empties: Front-Kopf, rechtes Kopfprofil, linkes Ganzkörperprofil und Dreiviertel-Kopf. Transparenz 35 %. Standardmäßig verborgen; im Outliner bei Bedarf jeweils nur die passende Ansicht sichtbar schalten. Diese Bilder dokumentieren die V3-Ausgangsform, **kein gewünschtes erwachsenes Gesichtsdesign**.

Numpad 1: Front; Numpad 3 und Ctrl+Numpad 3: beide Profile; Numpad 5: orthografisch/perspektivisch. Für die benannten Review-Kameras im Outliner Kamera auswählen und als aktive Kamera setzen. Im normalen Sculpt-Vergleich orthografisch bleiben. Nach jeder Formänderung Front, beide Profile und Dreiviertel prüfen. Nicht aus einer einzigen Ansicht fertigstellen.

Die während der Arbeit nachgereichte Datei `AdultHobbit_ArtTarget.jpg` ist als fünftes, gepacktes Image Empty `REF_V4_AdultHobbit_ArtTarget` vorbereitet. Sie zeigt den gewünschten erwachsenen, freundlichen Fantasykopf. Gegenüber V4 benötigt das Gesicht deutlich klarere Jochbein-/Wangen-/Kieferebenen, anatomisch getragene Lider, eine plastische Nase mit unauffälligen Öffnungen und natürliche schmalere Lippen. Das leicht perspektivische Porträt dient als künstlerische Zielvorlage, nicht zum maßhaltigen Nachzeichnen. Exakte Front-/Profilansichten dieses erwachsenen Entwurfs liegen weiterhin nicht vor. Die jugendlichen Trainerbilder sind keine Ersatz-Anatomiereferenz.

## Native Blender-5.2-Werkzeuge

Die mitgelieferten Brushes sind lokal vorhanden: Grab, Clay Strips, Draw Sharp, Smooth, Inflate/Deflate, Crease Polish und Mask. Grab ist im gespeicherten Arbeitsplatz aktiviert. Die übrigen Werkzeuge über die Sculpt-Asset-Shelf auswählen. Front Faces Only einschalten; X-Symmetrie vor jedem Schritt kontrollieren. Die folgenden Werte sind **Startempfehlungen für eine manuelle Sitzung, keine bereits ausgeführten Brush-Strokes**. Radius in Bildpixeln hängt vom Zoom ab.

1. **Gesamtkopf / Kiefer:** Grab, Radius 70–110 px, Strength 0,15–0,20. Den seitlichen Übergang von Wange zu Kiefer runden, den flachen Unterkieferabschluss durch kleinere versetzte Züge auflösen. Kopfoberkante Z=1,282 m und Halsansatz nicht verschieben. Am Profil prüfen, dass Kinn, Mund und Nase keine gemeinsame schiefe Keilfläche bilden.
2. **Wangen / Schläfen:** Clay Strips, Radius 35–60 px, Strength 0,08–0,12. Wenige kurze Züge entlang der Wangenmasse; unter dem Jochbein weniger Volumen als auf der Wange. Smooth mit Shift nur punktuell und schwach (0,08–0,12). Nicht die Anatomie wegpolieren.
3. **Augenpartie:** zuerst beide separaten Augäpfel belassen. Grab 20–35 px / 0,10 zur Lid-/Augenwinkelkorrektur. Clay Strips 15–25 px / 0,08 für Oberlid und unteren orbitalen Übergang. Oberlid soll die Kugel etwas überdecken, Unterlid sie tragen. Blickrichtung im Frontbild kontrollieren. Kein tiefes Crease rund um das ganze Auge; das verstärkt Puppenoptik. Nicht durch die dünne Sockelwand ziehen.
4. **Nase / Nasenflügel:** Grab 20–35 px / 0,10, dann Clay Strips 15–25 px / 0,08. Nasenrücken, Spitze und Alarvolumen als zusammenhängende Formen bearbeiten. Die bestehenden Öffnungen zeigen noch frontal und besitzen eckige Übergänge: Randgeometrie gezielt im Edit Mode verschieben, statt sie mit schwarzer Farbe oder weiteren Löchern zu kaschieren. Öffnungen mehr nach unten ausrichten und innen geschlossen halten. Profil und Ansicht von unten prüfen.
5. **Lippen / Mundwinkel:** Grab 15–25 px / 0,08 für ruhige Mundwinkel und weniger schnabelförmige Projektion. Clay Strips 12–20 px / 0,06 für dünnes, natürliches Lippenvolumen. Draw Sharp bzw. Crease Polish nur 8–14 px / 0,04–0,07 an der kurzen Mundspalte; nicht eine breite Rille ziehen. Ein neutrales Gesicht braucht keinen permanent hochgezogenen Mundwinkel.
6. **Kinn / Unterlippe:** Clay Strips 25–40 px / 0,08 für Kinnvolumen; Grab 35–50 px / 0,10 für Übergang. Die Vertiefung unter der Lippe weich ausformen, nicht als horizontale Furche.
7. **Ohren:** Grab 20–35 px / 0,10 für Helix und Lobulus. Clay Strips 15–25 px / 0,08 für Antihelix/Tragus; Draw Sharp 10–15 px / 0,05 nur zur Trennung klarer Formen. Die vorhandene Ohrmuschel ist noch zu oval und schematisch. Den Ohransatz im Profil kontrollieren, keine separate aufgeklebte Form erzeugen.

## Kontrollpunkte und Abbruchkriterien

Nach jedem Bereich neues lokales Zwischenfile speichern und identisch beleuchtete Front-/Profil-/Dreiviertelbilder prüfen. Augen dürfen nicht verschwinden, Randflächen dürfen nicht umklappen. Bei gekreuzten Flächen, geschlossenen Augenöffnungen oder gerissenem Halsübergang Undo bzw. eigene V4-Sicherung benutzen. Keine älteren Quellen überschreiben.

Die 96 N-Gons der lokalen Auflösungsgrenze am unteren Kopf sind für dieses Sculpt-Zwischenstadium dokumentiert. Vor späterer Retopologie/Rigging benötigen insbesondere Lid-, Lippen-, Nasen- und Ohrschleifen eine gezielte Neuordnung. Geschlossene Topologie beweist keine Verformungsqualität.

Stoppen, sobald die Kopfqualität geprüft werden kann. Keine Haare, Kleidung, Körper-Sculpting, Retopologie, Rigging oder Unreal-Integration ohne nächsten ausdrücklichen Auftrag.
