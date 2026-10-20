# Meshy-Glumanda Integration V1 – Prüfbericht

20.10.2026. Aktives Projekt: `/Users/harry/Developer/PokeMonster`.
Ausgangspunkt: `1577134aecb21e2e6f4f5b0e4bbd530b5bd40d2f`, Branch `main`.

## Ergebnis

Das tatsächlich gelieferte Meshy-Glumanda ersetzt Zunderlauf V1 als aktive optionale
3D-Darstellung. Sieben eigene Animationen, Originaltexturen und die originale
Schwanzflammen-Geometrie sind in Unreal eingebunden. Die Art bleibt
`CreatureSpecies:Zunderlauf`; Kampf-, Fang-, Team-, Heil- und Save-Systeme werden
weiterverwendet. Die bisherigen V1-Quellen/Assets bleiben als Fallback erhalten.
Die technische Integration ist geprüft; eine endgültige künstlerische Masterfreigabe
wird damit nicht vorweggenommen.

## 1. Tatsächliche Quelle und Qualität

- Eindeutige Datei: `Art/Characters/Creatures/Incoming/Glumanda.glb`.
- Größe: 6.123.824 Bytes; SHA-256:
  `44a82157d256a1ae4526f13c37aa3fc85d1022f2615f2812a2a8bba04ba4285c`.
- GLB 2, ein ursprüngliches Mesh, 14.600 Vertices, 21.761 Dreiecke,
  ein Material, eine UV-Ebene, drei eingebettete 2048×2048-JPEGs.
- Kein vorhandenes Rig und keine Animationen. Ursprüngliche Höhe
  0,9511719942 m; uniforme Skalierung 0,6308007423 ergibt 0,600 m.
- Front/Profil tatsächlich gerendert und geprüft: Blender −Y vorwärts, +Z oben;
  Unreal-Import richtet das Modell nach dem vorhandenen Präsentationsvertrag aus.
- Originales Gesicht, Körperform, Frisur/Design, Farben, UVs und Normalen erhalten.
  Keine Retopologie, Decimation, globale Glättung, Farb-Neugestaltung oder Rebaking.
- Das Rohmesh hat 234 Inseln und 6.971 offene Kanten, überwiegend UV-Seams.
  Ein nur diagnostisch exakt positionsverschweißter Proxy reduziert 14.600 auf
  10.901 Vertices; 89 offene Kanten bleiben. Es existieren kleine Quelllöcher,
  insbesondere an Körper-/Beinübergängen. Nicht als wasserdichtes Modell ausgegeben.
  Keine vollständige geometrische Selbstüberschneidungsfreiheit nachgewiesen.

### Erhaltene Geometrie und Materialien

Die bereits modellierte Flamme wurde anhand ihrer tatsächlichen Lage nur entlang
vorhandener Dreiecke separiert. Kein zusätzliches Flammenmodell wurde erfunden.
Körper: 12.227 Vertices / 18.198 Dreiecke. Flamme: 2.409 / 3.563.
Summe unverändert 21.761 Dreiecke; 36 Grenzvertices liegen nun in beiden Objekten.
Keine Originalfläche entfernt oder neu trianguliert. Die unveränderte High-Poly-/
Originalreferenz bleibt in einer separaten ausgeblendeten Blendercollection.

Originale drei JPEGs extrahiert und in `.blend` gepackt. BaseColor ist sRGB;
MetallicRoughness linear mit G=Roughness und B=Metallic, ursprüngliche Faktoren 1;
Normalmap OpenGL mit Green-Flip in Unreal. Opaque/TwoSided entspricht der GLB.
Gemalte Highlights der Quelle bleiben erhalten; keine behauptete neue PBR-Rekonstruktion.

## 2. Blender, Rig und Animationen

Quelle: `Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Meshy_V1.blend`.
Exporte: `Art/Characters/Creatures/Zunderlauf/Exports/MeshyV1/`.
Texturen: `Art/Characters/Creatures/Zunderlauf/Textures/MeshyV1/`.
Werkzeuge/Ablauf: `Tools/MeshyGlumandaV1/README.md`.

V1-Rollen und dessen native Präsentationsschnittstelle sind wiederverwendbar;
Restpose, Proportionen und Gewichte sind nicht direkt übertragbar. Daher eigenes
angepasstes 23-Bone-Rig; Unreal enthält zusätzlich den FBX-Wrapper und damit
24 Bones, Root `Glumanda_Meshy_Rig`. Bone Heat nur auf temporär positionsverschweißtem
Proxy, Gewichte auf originales Render-Mesh übertragen; Kopf, Sohlen/Zehen und
Flammengrenze gesondert behandelt. Kein Bone-Hierarchie-Umbau am V1-Rig.

| Clip | Dauer | Bewegungsbezug |
|---|---:|---|
| Idle | 2,0 s | Atmung, dezente Kopf-/Schwanzbewegung |
| Walk | 0,6 s | in place, 22 cm/s |
| Run | 0,4 s | in place, 36 cm/s |
| Attack | 0,8 s | kurze Vorwärts-/Körperreaktion |
| Hit | 0,4667 s | Rückstoß |
| Faint | 1,1 s | seitliches Niedergehen |
| Happy | 1,0 s | kurze positive Körperbewegung |

Sagittale Zweibein-IK hält die Knie nach vorne; T-Pose-Arme in eine passende
Ruhehaltung gebracht. Schrittparameter an die kurzen Beine angepasst statt
V1-Geschwindigkeiten 35/60 cm/s ungeprüft zu kopieren. Analytischer Fehler der
Standphasen-Inkremente unter 7×10⁻⁹ m; importierter Walk zusätzlich durch
Unreal-Bone-Tests geprüft. Das ist keine Garantie absolut gleitfreier Übergänge
oder Richtungswechsel. Größte gemessene Mesh-Bodentoleranz über die Clips unter
0,4 mm; Profil-GroundOffset −0,04 cm kompensiert diese kleine Skintoleranz.

Blenderquelle erneut geöffnet: 7 Actions, 23 Bones, 3 gepackte Bilder,
keine ungewichteten Vertices, keine nichtnormierten Gewichte, keine losen
Vertices/Nullflächen oder nicht-boundary Non-Manifold-Kanten. Die 5.854 offenen
Körperkanten einschließlich UV-Seams/Flammenschnitt bleiben ausdrücklich erhalten.
Walk-FBX erneut importiert: 12.227 Vertices, 18.198 Dreiecke, 23 Bones,
Armature-Skala 1, Walk 0,6 s. Messungen in den vier `MeshyV1_*Audit.json` unter Art.

## 3. Schwanzflamme und tatsächlich behobene Importfehler

Nur `tail_socket` trägt genau einen allgemeinen Effektanker `TailTipFX`.
Legacy-TailFlame ist leer. Die originale texturierte Flammengeometrie bewegt sich
mit dem Schwanz; dezente Emission und kleine an der Basis maskierte WPO-Bewegung
nutzen das vorhandene günstige Verfahren. Keine Körper-/Kopfflammen, kein
zusätzliches Partikelsystem und keine neue Lichtquelle.

Ein erster Unreal-Test zeigte eine massiv vergrößerte Flamme. Ursache tatsächlich
gemessen: FBX-Socket-Skala etwa (100,100,100), obwohl der Körper korrekt 60 cm groß
ist. Der Importer kompensiert die gemessene Referenzskalierung und -rotation im
relativen Effekt-Offset; effektive Welt-Skala jetzt 1. Neuer Automationstest prüft
dies und die originalen Flammenbounds. 74 finale QHD-Aufnahmen: maximaler
Socket-/Komponenten-Positionsfehler 0 cm. Die frühere fehlerhafte Sequenz bleibt
als lokale Diagnose erhalten und ist nicht der erfolgreiche Nachweis.

Frühere Gewichte zogen Bauch-/Sohlenvertices unter den Boden; Proxy-Heat-Transfer
und gezielte Fußgewichte korrigieren die Ursache. Die alten Knieachsen wurden
auf die reale Meshy-Anatomie angepasst. Kein Verbergen durch große Höhenversetzung.

## 4. Unreal-Assets und minimaler Austausch

Namespace: `/Game/Characters/Creatures/Zunderlauf/MeshyV1/` (16 Assets):

- `Meshes/SK_Glumanda_Meshy`, dessen eigenes Skeleton und `SM_GlumandaTailFlame`.
- `Animations/A_Glumanda_Idle`, `_Walk`, `_Run`, `_Attack`, `_Hit`, `_Faint`, `_Happy`.
- `Textures/T_Glumanda_BaseColor`, `_Normal`, `_MetallicRoughness`.
- `Materials/M_Glumanda`, `M_GlumandaTailFlame`.
- `DA_Glumanda_Presentation`.

Einzige persistente Änderung außerhalb des neuen Asset-Namespace:
`/Game/Data/Creatures/DA_Zunderlauf.Visuals.Presentation` verweist auf dieses Profil.
Art-ID, Anzeigename, Prototypnummer, Stat-Werte, Fangrate, Encounter und Save-Version
bleiben erhalten. Keine neuen Kollider oder parallelen Gameplay-Systeme.
Alle elf Mapdateien einschließlich VisualV2 SHA-256-identisch zum Aufgabenstart.
Heilhaus, Landschaft, Licht, Kamera, TAA und Spielfigur unverändert.

Kleine wiederverwendbare C++-Ergänzung: atomar validiertes `SetPresentation` für
reine Kandidatenvorschau in PIE; `SetSpecies` delegiert weiterhin dieselbe Logik.
Strenge V1-Assettests prüfen jetzt explizit den erhaltenen V1-Stand statt die
absichtlich austauschbare aktuelle Referenz. Save-/Spieltests prüfen weiterhin
die echte Spezies. Neue Meshy-Tests sichern 60 cm, eigenes Rig, alle Clips,
Schrittmechanik und Effekt-Skalierung ab; bestehende Verträge nicht aufgeweicht.

## 5. Tatsächlich durchgeführte Prüfungen

| Prüfung | Ergebnis / lokaler Nachweis |
|---|---|
| Mac Development Editor Build | bestanden, Exit 0; `Saved/ProjectRefinement/MeshyGlumandaV1Build04/Result.json` |
| vollständige Projekt-Automation | 56/56, 0 Warnungen/Fehler; `Saved/ProjectRefinement/MeshyGlumandaV1Automation04/Result.json` |
| Python Pipeline / Evidence / Map-Lifecycle | 9/9, 8/8, 5/5 bestanden |
| alle vorhandenen Maps | 11/11 Map Checks, jeweils 0 Fehler/0 Warnungen; `Saved/MeshyGlumandaV1/MapChecksVerified.json` |
| Blenderquelle + Walk-FBX-Roundtrip | bestanden; `MeshyV1_SourceAudit.json` |
| Kandidatenvertrag + bestehender Art-Schutz | bestanden; `Saved/CreaturePipelineV2/CandidateValidation.json` und vorhandener ValidateWorld-Prüfer |
| echte PIE-Animationsprüfung | alle 7 Clips, 8 Richtungen und native Run-Mischung 1,0; `Saved/MeshyGlumandaV1/RuntimeReviewCandidateFinal/Result.json` |
| vollständiger PIE-Fußlauf | bestanden, 290,38 m, 176,33 Spielsekunden; `Saved/MeshyGlumandaV1/Acceptance/Final02/FootTest.json` |
| Originale / Maps / Dev-Save / Backup | SHA-256/Refs bestätigt; `Saved/MeshyGlumandaV1/ScopeValidation.json` |

Der Enhanced-Input-Lauf prüft tatsächlichen Wildfang, Teamzuwachs auf drei,
Wechsel auf gefangenen Zunderlauf im Liora-Kampf, Sieg, Quest/Archiv, Dialoge,
Heilhaus betreten/verlassen, Heilen, Save/Load, Brücke, Baumkronenfreistellung,
Sprite-Fallback, acht Richtungen und Sprint (unverändert maximal 315 cm/s).
Keine Test-Teleports; die vorhandene Innenraum-Relocation ist normales Gameplay.
Der ursprüngliche Dev-Save wurde bytegleich restauriert:
`01dd9ebb263dd7dde672e1a9b70f8ae5780494fb9a5f3c1140ed3f0132ce057a`.

Der erste Fußlauf Final01 blockierte am alten fest verdrahteten Wild-Annäherungspunkt:
Kontaktkampf war bereits aktiv, während das Testskript weiter auf die Kapsel zulief.
Nur die Testannäherung folgt jetzt der tatsächlichen Kreaturenposition mit Abstand;
Kollision und Gameplay wurden nicht deaktiviert/verändert. Final01 ist als
fehlgeschlagener Nachweis erhalten, Final02 bestanden; beide Male Original-Save restauriert.

Editor-Loghinweise bleiben sichtbar: macOS `idevice_id` falsche CPU-Architektur,
Audio-Samplerate, `r.MotionVectorSimulation` RenderThread-Hinweis, bestehender
UE-LLM-Plugin-Lizenzhinweis und Diagnose-`Shot` Console-Lookups. Vor Engine-Initialisierung
enthält das Editorlog außerdem UnifiedError-/Condition-failed-Ausgaben; diese
werden nicht als erfolgreiche Spieltests umgedeutet. Der separate abschließende
PokeMonster-Automationsreport bestätigt alle 56 Tests ohne Warnungen/Fehler.
Der zusätzliche Lauf Automation03 hatte 55 Success + 1 SuccessWithWarnings (DefeatAndSave, 0 Fehler): zeitgleich eingestreute iOS-`idevice_id`-Geräteerkennung. Der strenge Runner stoppte korrekt. Unveränderte Wiederholung Automation04: 56/56 ohne Testwarnungen; nichts gefiltert oder unterdrückt, beide Reports erhalten. Keine Glumanda-Shader-/Materialfehler in den tatsächlichen Endprüfungen beobachtet.

## 6. Echte Aufnahmen – lokal, nicht in Git

Alle folgenden Pfade relativ zum aktiven Projekt, ausschließlich echte Unreal-PIE-
Aufnahmen; keine Konzeptbilder als Umsetzung ausgegeben:

- `Saved/MeshyGlumandaV1/RuntimeReviewCandidateFinal/*.png`: 74 Originalbilder,
  jedes tatsächlich 2560×1440, unveränderte Spielkamera Pitch −50°, Yaw −45°.
- `Saved/MeshyGlumandaV1/Evidence/Glumanda_Spielkamera_Detail.png`: gekennzeichneter
  2×-Ausschnitt des QHD-Bildes, Glumanda neben der 1,40-m-Spielfigur.
- `Saved/MeshyGlumandaV1/Evidence/Sieben_Clips_Unreal.png`: tatsächliche Clipbilder.
- `Saved/MeshyGlumandaV1/Evidence/Glumanda_Unreal_Bildsequenz.gif`: zeitlich geordnete
  Originalaufnahmen, **keine Echtzeit-Videoaufnahme**.
- `Saved/MeshyGlumandaV1/Acceptance/Final02/BattleWorld_*.png`: realer Teamkampf;
  `BattleUI_*` zeigt zusätzlich das Editorfenster und ist kein reiner QHD-Viewport.
- `Evidence/EvidenceAudit.json`, `RuntimeReviewCandidateFinal/Frames.jsonl`:
  Dateidimensionen, Clipzeiten, Kamera, Socket- und Fußdaten.

## 7. Grenzen und nächste Schritte

Originale kleine Mesh-Löcher und leichte LBS-Kompression an den kurzen Beinen
bleiben sichtbar bei starker Vergrößerung. Schnelle Drehungen/Übergänge und
Schwanznaht benötigen weitere manuelle künstlerische Abnahme. Keine neue
Gesichts-/Lidskelettanimation. Kein vollständiger Selbstschnitt-Test, Cook-,
Standalone-, LOD- oder FPS-Nachweis behauptet; diese waren nicht Teil dieses
PIE-Einzelimports. Keine weitere Kreatur automatisch begonnen.

Die tatsächlich gelieferte GLB ist jetzt die maßgebliche Modellreferenz;
das Erscheinungsbild wurde nicht eigenständig umgestaltet. Vor einer endgültigen
Masterfreigabe bitte die echte QHD-Sequenz visuell prüfen. Für weitere Starter
jeweils eigene tatsächliche Meshy-Datei prüfen, Körperform/Rig/Größe abnehmen,
dann denselben bewachten Pipelineablauf pro Art verwenden.

## 8. Git-/LFS-Sicherung

Die ausgewählte unveränderte Incoming-Glumanda-Quelle wird gezielt mit aufgenommen,
keine anderen Incoming-Modelle. Drei JPEGs zusätzlich eng per `.gitattributes`
über Git LFS; Blender, GLB, FBX und Unreal-Assets unter bestehenden LFS-Regeln.
Keine Videos, Screenshots, GIFs, Logs, Test-Saves oder Caches versionieren.
59 zuvor unversionierte Dateien physisch bytegleich; nach Aufnahme der ausgewählten
Glumanda verbleiben 58 davon bewusst unversioniert. Ein aktiver Worktree, beide
Backup-Refs unverändert auf 03492bd; dieser Commit wird nicht Teil der Remote-Historie.
Commit-/Remote-/LFS-Bestätigung wird nach der tatsächlich erfolgten Sicherung ergänzt.

Aktuelle GitHub-Dateigrenzen vor dem Upload geprüft: [normale Git-Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [Pushgröße](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits), [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage). Der konkrete Index wird zusätzlich auf Pointer, SHA-256 und Objektgrößen geprüft. Kein Kauf, keine Budgetänderung; aktuelle kontoabhängige Abrechnung ist dadurch nicht eingesehen.
