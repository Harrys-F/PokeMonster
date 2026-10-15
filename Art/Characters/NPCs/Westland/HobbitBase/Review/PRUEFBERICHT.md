# Hobbit NPC Base V1 – Erstes Mastermodell

Datum: 14.10.2026. Ausgangs-HEAD `3c6dc47`. Nur dieser neue HobbitBase-Arbeitsbereich wurde für das NPC-Modell verändert. Vorhandene Incoming-GLBs wurden nicht verwendet oder verändert. Keine Meshy-/externen Modelle, kein Unreal-Import.

## Datei und Aufbau

`Source/Hobbit_NPC_Base_V1.blend` ist die normale, erneut geöffnete Arbeitsdatei. `Source/Hobbit_NPC_BodyStage_V1.blend` bewahrt die eigene frühere Körperstufe. Meter, METRIC, Unit Scale 1. Beide Sohlen auf Z=0; Körperachse X=0. Vollständige symmetrische T-Pose: zwei gerade Arme auf gleicher Schulterhöhe, zwei Hände, zwei Beine, zwei breite Füße mit je fünf Zehen. Körper einschließlich Kopf, Hals, Nase, Ohren, Händen/Fingern und Füßen/Zehen ist ein zusammenhängendes geschlossenes Mesh.

Collections: HOBBIT_BODY, HOBBIT_CLOTHING, HOBBIT_FACE, HOBBIT_HAIR und separate PREVIEW_STAGE. Leinenhemd, braune Weste, olivfarbene Kniehose und Gürtel sind separate Objekte. Einfache eigene Materialien; keine finalen Texturen. 19 Modellobjekte; Studiokamera, Boden und drei Lichter gehören nur zu den Vorschauen. Kein Rig und keine Actions.

## Erneute Öffnung und Geometrieprüfung

Die gespeicherte Datei wurde in einem neuen Blender-5.2.2-LTS-Prozess erneut geöffnet und vollständig gerendert. `ReopenAudit.json` enthält die tatsächlichen Werte:

- Gesamthöhe einschließlich Haaroberkante: **1,32000005 m**; numerische Abweichung ca. 0,000005 cm.
- Sohlen: **0,000000 m**. Einheitenskala 1.
- Körper: **ein** zusammenhängender Teil, 16.758 Vertices / 33.512 Dreiecke.
- Offene Kanten / nicht-manifold Kanten am Körper: **0 / 0**.
- Maximale bilaterale Körperabweichung: **0 m**.
- Schnittprüfungen: ein Kopf, ein linker/rechter Arm, zwei Beine, zehn getrennte Zehenkonturen.
- Gesamtes Modell mit ausgewerteten Kleidungsmodifikatoren: **88.060 Dreiecke**.
- Armatures / Actions: **0 / 0**.

Sieben echte Blender-Vorschauen: Front, Rückseite, beide Seiten, Dreiviertel, schräge 2.5D-Nahansicht und zusätzliche 2850-cm-/35°-Spielkamera-Komposition. Diese Bilder sind **keine Unreal-Screenshots**. Originale Cube/Camera/Light der vorher offenen Blender-Szene wurden erhalten.

## Sichtprüfung und Grenzen

Front, Seiten und Dreiviertel wurden visuell geprüft: kompakter erwachsener Körper, kurzer Beinanteil, breite Füße, größerer Kopf und ausgestreckte T-Pose. Mund/Brauen wurden an die tatsächliche Hautoberfläche gesetzt; die zunächst zu stark verbundenen vorderen Zehen sind getrennt. Oberarm-/Unterarm-, Hüft-/Knie- und Knöchelringe bereiten Gelenkbereiche vor.

Die Figur ist eine **erste Modellbasis**, kein finaler NPC. Haare sind einfache stilisierte Lockenvolumen; Gesicht und Hände benötigen später weitere künstlerische Arbeit. Boolean-Verbindungen an Fingern/Zehen/Nase/Ohren sind geschlossen, aber dort ist vor anspruchsvoller Animation lokale Retopologie sinnvoll. Ohne Rig wurden keine Verformungsprüfungen vorgenommen. UVs, Hautgewichte, Crowd-LODs und Texturen sind noch nicht Produktionsstand. 88k Dreiecke sind für einen Quellmaster vertretbar, für viele gleichzeitig sichtbare NPCs muss eine leichtere Runtime-Variante erstellt werden. Größenvarianten 1,20–1,45 m sind vorbereitet als Metadaten, noch nicht als zusätzliche Modelle erzeugt.

Keine Projekt-Dokumentation geändert; Freigabe durch Harry ausstehend. Kein Commit und kein Push.
