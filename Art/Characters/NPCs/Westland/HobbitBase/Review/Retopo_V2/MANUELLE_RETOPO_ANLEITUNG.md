# Hobbit Retopo V2 – manuelle Bearbeitung

## Status und Schutz

Dies ist ein vorbereiteter Arbeitsplatz, **kein fertig retopologisierter Kopf**. Der neue Zielkörper hat derzeit 0 Vertices und 0 Flächen. Es wurden keine QuadriFlow-/Decimate-Ergebnisse übernommen. Highpoly, Originalmaterial und gepackte Texturen sind unverändert in der neuen Datei enthalten.

Arbeitsdatei: `../../Source/Hobbit_NPC_Retopo_V2.blend` (relativ zu diesem Berichtordner).

1. Öffne die neue Arbeitsdatei. Wähle `RTV2_Head_MANUAL_RETOPO_REQUIRED` in `RETOPO_HEAD`. `HIGH_POLY_REFERENCE` enthält das gegen Auswahl gesperrte Original. Es bleibt im Viewport sichtbar. Nicht dessen Geometrie bearbeiten oder Normalen neu berechnen.
2. Die Figur steht in Metern, Fußsohle Z=0; die Vorderseite zeigt nach **−Y**. Numpad 1 = Front, Numpad 3 = rechte Seite, Ctrl+Numpad 3 = linke Seite. Numpad 5 wechselt orthografisch/perspektivisch. Auf Mac ohne Numpad: View → Viewpoint beziehungsweise die gespeicherten Kameras benutzen. Kopfzentrum der Kontrollansichten: Z=1,205 m.
3. Fünf gespeicherte Kontrollkameras befinden sich in `REVIEW`: Front, rechts, links, Dreiviertel und 2,5D-Nahansicht. Sie sind zur Arbeitsplatzübersicht im Viewport verborgen, rendern aber weiterhin. Eine Kamera im Outliner wählen, Ctrl+Numpad 0 = aktive Kamera; Numpad 0 = Kamerasicht. Diese Ansichten verändern keine Unreal-Kamera.
4. `REVIEW_REF_IMAGES` enthält gepackte, gesperrte Image Empties aus den neuen tatsächlichen Highpoly-Renderings. Sie sind standardmäßig verborgen. Bei Bedarf **nur eine** passende Ebene einblenden; Deckkraft 35 %, gleicher orthografischer Kopfmaßstab, kein Turnaround mit erfundenen Gesichtsformen. Sie dienen der Bildkontrolle, nicht als Projektionsziel.

## Startwerkzeuge

- Magnet/Snapping ist aktiviert, **Face Project** (individuelle Oberflächenprojektion) und Closest sind eingestellt. Nicht bearbeitete Objekte dürfen als Ziel dienen, auch die gegen Auswahl gesperrte Highpoly-Referenz; Selbstprojektion ist deaktiviert. Das alte `use_snap_project` gibt es in dieser Blender-Version nicht mehr. Im Snap-Popover kann bei Bedarf vom individuellen Face Project zum einfachen Face-Snapping gewechselt werden. Immer in Front UND Profil kontrollieren.
- Auf dem leeren Ziel sind **Mirror X** mit Clipping/Merge 0,1 mm und **Shrinkwrap / Nearest Surface Point**, Offset **0,5 mm**, eingerichtet. Die Zielgeometrie wird „In Front“ dargestellt. Das Offset ist ein Arbeitsplatzabstand, kein bewiesener Bake-Cage-Wert.
- Mirror nur zum symmetrischen Start benutzen: Haare und Gesicht der Quelle sind nicht perfekt symmetrisch. Für die Endkontrolle später eine unabhängige neue Zwischenversion speichern, Mirror anwenden und lokale Asymmetrien gezielt anpassen; niemals die Quelle symmetrisieren.
- Shrinkwrap kann auf Stirn/Schläfe versehentlich Haare oder am Hals Kleidung treffen. Vor solchen Bereichen Modifier im Viewport vorübergehend deaktivieren. Keine Modifikatoren blind anwenden. Eine separate validierte Projektionsfläche wäre erst nach manuell bestätigter Flächenauswahl anzulegen; derzeit existiert keine automatisch segmentierte Hautfläche.
- Material Preview zeigt die gemalten Augen/Mundgrenzen; Solid/MatCap zeigt deren echte räumliche Form. Beide Ansichten abwechselnd prüfen. X-Ray nicht pauschal aktivieren: „In Front“ für die neue Cage ist übersichtlicher, das Original bleibt lesbar.

## Konkreter Kopfaufbau

1. **Landmarken manuell am Original bestimmen:** innere/äußere Augenwinkel, Lidbögen, Mundwinkel, Lippenmitte, Nasenflügel, Kinnspitze, Kieferwinkel und Halskontur. Haare nicht mit Schädelkontur verwechseln. Der sichtbare Augenfarbbereich ist nicht automatisch eine geometrische Augenöffnung. Vor Beginn Front, Profil und Clay heranziehen.
2. **Augenringe:** im Edit Mode einen Mesh Circle ohne Füllung als rechte Hälfte anlegen, zunächst etwa 12–16 Punkte als Arbeitsvorschlag, nicht als verbindliche Anatomie. Ausrichten, skalieren und jeden Punkt an die Lidkontur des Originals setzen. Aus diesem geschlossenen Ring einen zweiten Ring extrudieren; dadurch entsteht ein bewusst aufgebauter Quad-Streifen. Die inneren und äußeren Augenwinkel dürfen keine sternförmigen Verdichtungen bekommen. Weitere Ringe erst bei sichtbarem Bedarf ergänzen. Die Öffnung nicht mit einem N-Gon schließen.
3. **Mundringe:** einen zweiten geschlossenen Ring an Lippenkante und Mundwinkeln aufbauen; obere/untere Lippe separat lesbar halten. Einen umlaufenden zweiten Ring für den Übergang zur umgebenden Haut extrudieren. Für spätere Mimik eine innere Lippen-/Mundtasche bewusst modellieren. Das Original belegt keine brauchbare offene Mundhöhle. Nicht einfach die dunkle Mundtextur als Loch ausstanzen.
4. **Nase:** vom Nasenrücken zur Spitze und zu beiden Nasenflügeln passende Quad-Streifen legen. Nasenöffnungen und Verlauf zur Oberlippe am Clay prüfen. Poles nicht mitten auf Nasenflügel oder Lidfalte setzen.
5. **Wangen/Stirn:** Augen-, Mund- und Nasenstreifen über möglichst gleichmäßige Quads verbinden. Mit Poly Build, Extrude (E), Füllen einzelner vierpunktiger Lücken (F), Knife (K) und Edge Slide (GG) arbeiten. Kein globales Grid Fill über Augen/Mund und keine pauschale Unterteilung. Zusätzliche Loops dort, wo Krümmung, Ausdruck oder spätere Deformation sie erfordern.
6. **Kinn/Kiefer:** den Lippenbereich zur Kinnwölbung und zur seitlichen Kieferlinie führen. Besonders im Profil Nasenvorsprung, Lippen, Kinn und Hals prüfen. Keine starre horizontale Z-Schnittkante am unteren Gesicht: der vorherige Test schnitt am Kiefer/Hals sichtbar ungünstig.
7. **Ohren/Schädel:** Ohransatz bewusst verbinden, Helix/Concha nicht mit einer beliebigen Dreiecksfächer-Füllung ersetzen. Unter dichtem Haar sind Schädel und Haarwurzel nicht zuverlässig getrennt sichtbar; dort eine plausible neue Kopfgrundfläche manuell festlegen. Diese Ergänzung als rekonstruierte verdeckte Fläche dokumentieren, nicht als exakt übernommene Quelldetailform.
8. **Hals:** Kopf und Hals über umlaufende, gleichmäßig verteilte Ringe verbinden, ohne Kragen/Umhang einzufangen. Halsring und späterer Körperanschluss dürfen im Arbeitsstand offen bleiben; später definierte Anschlusskante oder geschlossene Basis festlegen. Kopfbewegungen brauchen volumenhaltende Übergänge, nicht eine einzelne dünne Halsreihe.
9. **Kontrolle nach jeder Zone:** Front → beide Profile → Dreiviertel → 2,5D. Hautkontur mit und ohne Originaltextur vergleichen. Shape-Abweichungen nicht durch Bake oder Studio-Licht verstecken. Erst den sichtbaren Loop-Verlauf freigeben, dann restliche Zonen schließen.

## Normalen und Mesh-Prüfung

- Viewport Overlays → Face Orientation einschalten. Die Quelle kann originale Restfehler zeigen; sie wird dadurch nicht repariert. Beim neuen Ziel prüfen, ob sichtbare Außenflächen konsistent orientiert sind.
- Nur das **Ziel** wählen, Edit Mode → Select All → Shift+N für äußere Normalen, anschließend visuell prüfen. Bei offenen Augen-/Mundrändern ist „außen“ nicht überall automatisch eindeutig.
- Select → Select All by Trait → Non-Manifold. Offene definierte Arbeitsränder sind erwartbar, innenliegende Mehrfachkanten/isolierte Punkte nicht. Select Loose Geometry und Merge by Distance nur auf überprüfte neue Zielgeometrie anwenden.
- Im Text Editor ist `RTV2_CHECK_TARGET_READ_ONLY.py` vorbereitet. Im Object Mode mit aktivem Ziel ausführen: zählt Vertices, Faces, Quads, Triangulierung, Ränder, nicht-manifold Kanten und lose Punkte, ohne Änderungen. Keine riesige Highpoly-Geometrie mit bmesh neu aufbauen.
- Selbstüberschneidungen und Kontakt zum Haar müssen zusätzlich im Profil/Clay geprüft werden. Quad-Anteil allein beweist keine Deformationseignung. Es wurde noch kein Rig, keine Gewichte und kein Mimik-/Hals-Deformationstest erstellt.

## Spätere Trennung und Bake – jetzt noch nicht ausführen

Collections sind organisatorisch. Die Quelle besitzt ein Material und eine gemeinsame UV-Atlas-Zuordnung. Räumliche Kandidaten in `WorkspaceAudit.json` überlappen sich und sind keine Schnittmasken. Haut/Haar/Kleidungsgrenzen per Material Preview und Clay manuell nachfahren, Auswahl in einer **separaten neuen Helferkopie** bestätigen. Keine automatische Löschung kleiner Inseln.

- Haare: tragende Lockengruppen, Stirnfransen und Außenkontur als Geometrie; feine Innenrillen/Struktur in Normal/Roughness. Verdeckte Locken nicht als überall gleiche glatte Haarkappe ersetzen. Keine Haar-Retopo in V2.
- Kleidung: Hals-/Armausschnitte, Säume, offene Westenkanten und tiefe silhouetteprägende Falten als Geometrie. Stoffkorn, Nahtrelief und flache Falten können gebacken werden. Ein vollständiger unsichtbarer nackter Körper ist in der Quelle nicht nachgewiesen; modulare Kleidung benötigt rekonstruierte Abdeckung und definierte gemeinsame Anschlüsse.
- Umhang: Außenkante, Dicke, tragende Falten und Schulterkontakt geometrisch erhalten; keine Hautflächen mit Umhang verschmelzen. Kein neuer Umhang-/Rig-Aufbau in diesem Auftrag.
- BAKING bleibt leer. Erst nach bestätigter Cage: UVs ohne problematische Überlappung, ausreichende Texeldichte und Randabstand; lokale Ray-Distanzen messen. Base Color ohne Licht, Normal/Roughness separat. Haare/Ohren/Kragen bei falschen Ray-Treffern als explizit geprüfte Bake-Gruppen behandeln. Nicht die gescheiterten V1-UVs/Bakes wiederverwenden.

## Freigabepunkt

Ein animationsfähiger Kopf liegt erst vor, wenn vollständige Oberfläche, kontrollierte Augen-/Mundloops, passende Profilkontur, Haut/Haar-Grenzen, Halsanschluss, UVs und später Deformationsnachweise geprüft sind. Der gespeicherte V2-Arbeitsplatz ist die Vorbereitung darauf. **Hier stoppen; manuelle Modellierung und erneute Qualitätsprüfung sind erforderlich.**
