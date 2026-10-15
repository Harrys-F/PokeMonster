# Modulares Hobbit-NPC-System – Vorschlag, noch nicht umgesetzt

Die bestehende Form und Textur bleiben die künstlerische Grundlage. Keine vollständige Neumodellierung, keine Primitive als Ersatz und keine automatische Aufteilung der 3.324 verbliebenen Geometrieinseln.

| Modul | Gemeinsame Rig-Anbindung | Konkrete Vorbereitung / Grenze |
| --- | --- | --- |
| Kopf | head, neck | Gesicht zunächst erhalten. Halsanschluss mit definiertem gemeinsamen Ring; keine aktuellen Face-/Augenbones. |
| Haare | head | Separates Scalp-/Haarmodul nach semantischer Prüfung. Haarinseln nicht pauschal entfernen oder zu Haut verschweißen. |
| Körper | pelvis, spine, chest, neck und bestehende Gliedmaßenbones | Zuerst gezielt Risse reparieren. Verdeckte Haut unter Kleidungsflächen ist noch nicht als vollständiger Basiskörper nachgewiesen. Nur nötige lokale Flächen ergänzen, nicht das ganze Modell neu generieren. |
| Leinenhemd | chest, clavicle, upperarm, lowerarm | Ärmel und Schulteranschlüsse gezielt prüfen; gemeinsame Hautgewichte an Anschlussringen. Aktueller Atlas enthält Haut und Stoff gemeinsam. |
| Weste | spine, chest, pelvis | Eigenes Kleidungsmodul mit sauberen Säumen; Riemenbefestigung gesondert behandeln. |
| Hose | pelvis, thigh, shin | Knie-Faltungen und Saum priorisieren. Keine automatische Trennung durch Z-Höhen, die Beine oder Umhang mitschneidet. |
| Umhang | cape_upper, cape_lower, cape_left, cape_right | Bestehende vier Bones wiederverwenden. Risse lokal reparieren; keine Voll-Cloth-Simulation nötig. NPCs ohne Umhang können dasselbe Skelett behalten. |
| Tasche / Gürtel | bag sowie pelvis/spine/chest für Gürtel und Riemen | Tasche separat, Riemen körpergebunden. Nicht den gesamten Trageriemen auf bag gewichten. |
| Füße | foot_l, foot_r, shin_l, shin_r | Barfußform erhalten, Knöchelanschluss definieren. Zehen-/Foot-Roll-Bones fehlen; eine Erweiterung ist freigabepflichtig. |

## Gemeinsamer Animationsvertrag

25 Bone-Namen, Elternhierarchie, Achsen und Restpose vorerst unverändert halten. Keine zusätzlichen IK-, Finger-, Gesichts- oder Steuerbones in diesem Pass. Grobe Gesprächsgesten sind durch Kopf-, Schulter-, Arm- und Handrotationen möglich; artikulierte Finger-/Gesichtsgesten benötigen später eine gesonderte Skelettentscheidung.

Unreal-Vorschlag nach Modellfreigabe: ein gemeinsames NPC-Skeleton, ein Haupt-SkeletalMesh mit Animationsinstanz und passende modulare SkeletalMesh-Komponenten mit derselben Pose. Kleine rigid gebundene Accessoires können geeignete Bone-/Socket-Anbindungen verwenden. Bestehenden Player-Skeleton-/AnimInstance-Code dafür nicht verändern. Kein solches System wurde hier implementiert oder getestet.

Idle/Walk weiterverwenden, Run optional. Bei uniformer Skalierung die Abspielrate an tatsächliches NPC-Tempo und skalierte Schrittlänge koppeln. Nichtuniforme Körpervarianten brauchen erneut geprüfte Gewichte/Restposen und gegebenenfalls Retargeting; bloß gleiche Bone-Namen reichen nicht.

## Materialien und Performance

Vorhandene 2048²-Farb-, ORM- und Normaltexturen erhalten. Eine spätere Modultrennung soll möglichst gemeinsame Materialfamilien und wenige Draw Calls bewahren. Variantenfarben benötigen gezielte Masken oder passende Texturvarianten; globales Tinting würde Haut, Kleidung und Haare gleichzeitig verfärben. Keine neuen Materialfamilien oder Textursets in dieser V2 erstellt.

Runtime-LODs erst nach Sichtfreigabe und gezielter Reparatur untersuchen. Aktuell 47.744 Dreiecke; eine erneute aggressive globale Reduktion wäre kein geeigneter Ersatz für saubere lokale Reparatur.

## Empfohlener nächster eng begrenzter Reparaturschritt

Eine einzelne gut sichtbare Unterarm-/Ärmelstelle oder ein kleines Umhangfeld manuell reparieren und unter identischen Kameras sowie allen vorhandenen Posen gegenprüfen. Die ursprüngliche hochauflösende Meshy-Quelle kann nach Maßstabs-/Ausrichtungsprüfung als lokale Formreferenz dienen. Nicht einfach die gesamte reduzierte Kopie durch ein anderes Mesh ersetzen. Erst ein nachweislich gutes kleines Reparaturmuster auf ähnliche Stellen übertragen.
