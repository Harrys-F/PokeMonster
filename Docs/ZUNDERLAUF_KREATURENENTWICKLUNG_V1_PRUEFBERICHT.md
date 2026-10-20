# Zunderlauf – Kreaturenentwicklung V1

Stand: 20.10.2026. Projekt: `/Users/harry/Developer/PokeMonster`. Unreal Engine 5.8.2, Blender 5.2.2 LTS, macOS.

## Ergebnis und Freigabegrenze

Zunderlauf ist als neue, geriggte 3D-Kreatur in die bestehende VisualV2 und deren vorhandenen Kampf-, Fang-, Team-, Heil- und Speicherablauf integriert. Es gibt sieben Animationen und ausschließlich an der Schwanzspitze Feuer. Der finale Editor-Build, 52/52 Automationstests, elf Map Checks sowie der vollständige reale PIE-Fußlauf sind erfolgreich. Die Implementierung ist auf GitHub gesichert; sämtliche 33 neuen LFS-Objekte wurden danach vom Server heruntergeladen und vollständig gehasht.

Das ist eine technisch geprüfte V1, keine automatische künstlerische Endfreigabe. Das selbst in Blender aufgebaute Modell folgt der bestätigten Referenz, erreicht deren ausgearbeitete Haut-, Augen- und Gesichtsqualität noch nicht vollständig. Die abschließende visuelle Abnahme erfolgt durch Harry. Exakt gleitfreie Kontakte beim Übergang und Drehen sind noch nicht messtechnisch bestätigt. Es wurden keine weiteren Kreaturen begonnen.

## 1. Bestand, Referenz und Schutz

Ein verwendbarer vorhandener Zunderlauf-Modellstand wurde nicht gefunden. Die Nutzerentscheidung lautet ausdrücklich: **„Foto 1 maßgeblich, Foto 2 ergänzend“**. Foto 1 bestimmt Kopf, Augen, Körper, Bauch und kurze Gliedmaßen. Foto 2 ergänzt Seiten-/Rückenform und Schwanzflamme. Die Bilder wurden unverändert übernommen:

| Referenz | Dauerhafter Projektpfad | SHA-256 |
|---|---|---|
| Foto 1 | `Art/Characters/Creatures/Zunderlauf/References/Primary_Design.jpg` | `1ee17479e0dd2130621cf24a10da3a6e128bcfe9289858557275ea07f1c40412` |
| Foto 2 | `Art/Characters/Creatures/Zunderlauf/References/Supplemental_Views.jpg` | `42759223ee9bfe5d5f2a075ff35a1fb958ea8c0e3d6059def5d1829f2b2775c5` |

Die Entscheidung und die vorläufige Größenannahme stehen in `References/ReferenceDecision.json`. Die Beschriftung des ergänzenden Bildes wurde nicht als neue Artdefinition oder kanonische Größenangabe übernommen. Bestehende unversionierte Incoming-Modelle wurden weder verwendet noch verändert.

Ausgangscommit: `cf51c55995797ce9df66bea3e20d07d813f61875`. Alle **53 bereits vorhandenen unversionierten Dateien** wurden einzeln anhand ihrer Anfangs-SHA-256 erhalten und vom Commit ausgeschlossen. Alle anderen zehn vorhandenen Maps blieben bytegleich. An der VisualV2 wurden ausschließlich die unten beschriebenen Einstellungen des bestehenden Wildkreaturen-Actors gespeichert. Kein neuer gespeicherter Map-Actor, keine neue Map, kein Worktree, keine Projektkopie und kein Vollbackup wurden angelegt.

Der V5-Art-Vertrag und der detaillierte Vergleich der bestehenden Szene bestehen weiterhin: Heilhausgestaltung, Landschaft, Spieler, NPCs, Kamera, Lichtquellen, Schatten, TAA und Kollisionen wurden erhalten. Beide lokalen Backup-Refs zeigen unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; dieser Commit ist kein Vorfahr des hochgeladenen main.

## 2. Blender-Modell und Materialien

Bearbeitbare Quelle: `Art/Characters/Creatures/Zunderlauf/Source/Zunderlauf_V1.blend`.

Das Modell wurde neu mit Blender-Python aufgebaut. Körper, Kopf, Hals, Arme, Beine und Schwanz bilden eine zusammenhängende Haut. Augen und Klauen sind modellierte Teile desselben Mesh-Objekts; die Flamme ist ein separates Objekt. Keine extern erzeugten 3D-Modelle oder bezahlten Dienste wurden eingesetzt.

| Messung | Tatsächlicher Wert |
|---|---:|
| Körper-/Detailmesh Vertices | 25.044 |
| Polygone | 24.872 |
| Körper-/Detailmesh Dreiecke | 49.904 |
| Flamme Dreiecke | 288 |
| Gesamte Dreiecke | 50.192 |
| Körperhöhe ohne Flamme | 0,652449686 m |
| Vorläufiger Größenentwurf | rund 0,66 m; Spieler unverändert 1,40 m |
| Blender-Rig | 23 Bones |
| Unreal-Skeleton | 24 Bones einschließlich FBX-Armature-Wurzelknoten |
| Quell-Materialslots | 5 |
| Gepackte Texturen | 3 × 2048 × 2048 |

Es gibt keine losen Vertices, Nullflächen, ungewichteten Vertices oder nicht normierten Gewichte. **96 beabsichtigte offene Randkanten gehören zu den zwei Augenscheiben.** Andere nicht-manifold Kanten wurden nicht gefunden. Deshalb wird das Gesamtmesh ausdrücklich nicht als wasserdicht bezeichnet. Ein umfassender mathematischer Selbstüberschneidungsnachweis ist damit nicht erbracht; die sichtbaren Bewegungen wurden zusätzlich geprüft.

Base Color, Tangent-Normal und Roughness wurden auf das vorhandene UV-Layout gebacken und in die Blenderdatei gepackt. Die Base Color enthält keine gebackene Studiobeleuchtung. Die Normal Map ist OpenGL; Unreal verwendet die passende Grünkanalumkehr. Roughness wird linear gelesen. Die fünf Körper-Slots verwenden in Unreal dasselbe gebackene Material. Die Originalreferenzen bleiben separat erhalten.

Die Blenderquelle und ein Walk-FBX wurden tatsächlich erneut geöffnet: 25.044 Vertices, 49.904 Dreiecke, 23 Bones, Scale 1/1/1 und 0,6 Sekunden Walk bleiben im Roundtrip erhalten. Nachweise: `ModelAudit.json`, `SourceAudit.json`, `AnimationAudit.json`, `BakeAudit.json` im Art-Verzeichnis.

## 3. Rig und sieben Animationen

Eigenes Kurzbein-Rig mit Becken, Wirbelsäule, Kopf, beidseitigen Arm-/Beinketten und sechs Schwanz-/Socket-Bones. Keine ungeprüfte Übertragung des humanoiden Spielerrigs. Offline erstellte Fußziele und Bone-Matrizen bestimmen die Beinmechanik; die Laufzeit benötigt keine aufwendige IK-Simulation.

| Clip | Dauer | Einsatz |
|---|---:|---|
| Idle | 2,00 s | Atmung, geringe Gewichts- und Schwanzbewegung |
| Walk | 0,60 s | In-place; 35 cm/s, 21 cm Weg pro Zyklus |
| Run | 0,40 s | In-place; 60 cm/s, 24 cm Weg pro Zyklus |
| Attack | 0,80 s | Kurze vorbereitete Vorwärtsbewegung des Körpers |
| Hit | 0,4667 s | Trefferreaktion |
| Faint | 1,10 s | Seitliches Niedergehen, Endpose bleibt stehen |
| Happy | 1,00 s | Kurze positive Reaktion |

FBX-Dateien: `Art/Characters/Creatures/Zunderlauf/Exports/Zunderlauf_<Clip>.fbx`; Flamme: `Zunderlauf_TailFlame.fbx`. Der native Animationsproxy mischt Idle/Walk/Run anhand gemessener Bewegungsgeschwindigkeit und skaliert die Zyklusphase nach zurückgelegtem Weg. Die Kreatur übernimmt nicht die Spielergeschwindigkeit von 210 cm/s.

Der importierte Walk wurde zusätzlich direkt an Unreal-Bone-Posen geprüft: Knievorwärtsrichtung, sagittale Beinspur und Fußhöhe; die Standphase kompensiert 35 cm/s innerhalb der Testtoleranz. Das beweist den importierten Clip, nicht sämtliche Weltkontakte auf beliebigem Gelände. Die zusätzliche Weltkontaktprobe lieferte unter ihren strengen Filtern keine ausreichenden aufeinanderfolgenden flachen Standphasenpaare. Deren Ergebnis ist **inconclusive**, nicht „kein Foot Sliding“. Start/Stop und Drehungen benötigen weitere visuelle Feinabnahme. Es gibt noch keinen eigenen Turn-Clip, kein Blinzeln und keine Mundanimation.

## 4. Schwanzfeuer

`SM_TailFlame` folgt ausschließlich `tail_socket`. Der protokollierte maximale Positionsfehler zum Socket beträgt **0,0 cm** in den aufgezeichneten Frames, auch während Run, Faint und Richtungswechseln. In frontaler Projektion kann die hintere Schwanzspitze oberhalb des Kopfes erscheinen; sie ist nicht am Kopf befestigt.

Die etwa 10,5 cm hohe Flamme ist ein kleines, opakes, emissives 3D-Mesh mit sanfter Vertexbewegung. Kein Feuer an Kopf, Rücken oder Körper, keine neue Lichtquelle, kein großes Partikelsystem. Die bestehende Beleuchtung wird nicht zur besseren Präsentation verändert. Die Flamme ist deutlich einfacher als das halbtransparente Feuer der Referenz; ein volumetrischer oder fotografischer Feuereffekt wird nicht behauptet.

## 5. Unreal-Assets und vorhandenes Gameplay

Neue Assets unter `/Game/Characters/Creatures/Zunderlauf/`:

- `Meshes/SK_Zunderlauf`, `SK_Zunderlauf_Skeleton`, `SM_TailFlame`.
- `Animations/A_Zunderlauf_Idle`, `Walk`, `Run`, `Attack`, `Hit`, `Faint`, `Happy`.
- `Materials/M_Zunderlauf`, `M_TailFlame`.
- `Textures/T_Zunderlauf_DIFFUSE`, `NORMAL`, `ROUGHNESS`.
- `DA_Zunderlauf_Presentation`.

Art-/Encounter-Daten: `/Game/Data/Creatures/DA_Zunderlauf` und `/Game/Data/Encounters/DA_Zunderlauf_Wild`. Die vorhandene Test-Feuerart wurde als technische Datenvorlage dupliziert. Ihre bisherigen Werte und Anfangsattacken bleiben Prototypwerte, keine neue freigegebene Starter-Balance. Die Art besitzt eine eigene AssetManager-Identität `CreatureSpecies:Zunderlauf` und wurde im Speicherablauf geprüft.

In VisualV2 wurde der bestehende `Slice_Wildkreatur_Optional` konfiguriert: Ausgangsposition **(-1040, -1450, 60) cm**, Encounter-ID **Dev_VisibleWild**, Seed **3817**, Kollisionskapsel und Interaktionsbereich unverändert. Neu sind Art, eigenes Encounter-Profil und die ausdrücklich optionale kleine Umgebungsbewegung. Sie pausiert nahe dem Spieler und während des Kampfes; Bewegungsziele prüfen Boden und Hindernisse. Die Bodenanpassung betrifft die Darstellung. Es wurden keine zusätzlichen Gameplay-Kollider oder Physics Assets hinzugefügt.

`PokeMonsterCreaturePresentation` ist eine optionale Darstellungsschicht auf dem bestehenden Art-/Encounter-System. Das vorhandene BattleSession-System führt weiterhin Regeln, Zufall, Fang, Team und Persistenz aus. Der BattleWidget-Phasenablauf löst Attack/Hit/Faint/Happy aus; Fehlschläge und Immunität erzeugen keine falsche Trefferreaktion. Ein längerer Abschluss für die 3D-Darstellung lässt Reaktionsclips auslaufen.

Weltkämpfe bleiben auf der geladenen Karte sichtbar. Temporäre kollisionsfreie 3D-Darstellungen stehen auf geprüften freien Bodenpositionen nahe dem Spieler. Die bestehende Kamera bleibt unverändert. Bei keinem sicheren Aufstellpunkt bleibt die vorhandene UI-Darstellung als Fallback verfügbar. Andere Arten ohne 3D-Profil behalten ihre 2D-Darstellung. Teamswitch, Fang und Deaktivierung räumen die entsprechenden Visuals auf. Kein neues Kampf-, Team-, Heil-, Speicher- oder Begleiter-System wurde aufgebaut.

Zunderlauf ist als Wildkreatur und als aktive Teamkreatur im Kampf darstellbar. Ein frei mitlaufender Team-Begleiter gehört nicht zu dieser Implementierung. Bereits abgeschlossene `Dev_VisibleWild`-Begegnungen bleiben in alten Spielständen abgeschlossen; ein Update setzt den Spielstand nicht zurück. Der Editor zeigt außerhalb PIE möglicherweise die bisherige Editor-Sprite-Vorschau, da das neue Visual zur Laufzeit erzeugt wird.

## 6. Durchgeführte Prüfungen

| Prüfung | Finales Ergebnis | Lokaler Nachweis |
|---|---|---|
| Mac Development Editor Build | Exit 0 | `Saved/ProjectRefinement/ZunderlaufV1Build11/Result.json` |
| Vollständige Projekt-Automation | **52/52**, 0 Warnungen, 0 Fehler | `Saved/ProjectRefinement/ZunderlaufV1Automation08/Result.json` |
| Neue Zunderlauf-Tests | Asset-/Skeleton-/Clip-/Persistenzvertrag und importierte Beinmechanik bestanden | `Source/PokeMonster/Tests/PokeMonsterZunderlaufTest.cpp` |
| Bestehende Python-Prüfungen | 8 DevelopmentEvidence- und 5 MapLifecycle-Tests bestanden | Unittest-Läufe der vorhandenen Werkzeuge |
| Alle elf vorhandenen Maps | **0 Fehler, 0 Warnungen** | `Saved/ZunderlaufV1/MapCheckResults.json` |
| Bestehender V5-Art-Vertrag / Szenenschutz | bestanden; 53 unversionierte Dateien unverändert | `Saved/ZunderlaufV1/WorldValidation.json` |
| Vollständiger realer PIE-Fußlauf | **291,153 m**, bestanden, keine Testteleports | `Saved/ZunderlaufV1/Acceptance/Final11/FootTest.json` |
| Zusätzlicher finaler Kampf-Fußlauf | **17,815 m**, bestanden | `Saved/ZunderlaufV1/Acceptance/BattleFinal11/FootTest.json` |
| Sieben Clips, acht Richtungen, native Run-Mischung | durchlaufen; Run-Blend erreicht 1,0 | `Saved/ZunderlaufV1/RuntimeReviewGrounded/Result.json` |
| Blender-Speichern/Öffnen und FBX-Roundtrip | bestanden | `Art/Characters/Creatures/Zunderlauf/SourceAudit.json` |

Der vollständige Fußlauf verwendet echte Enhanced-Input-Eingaben. Er enthält Wanderer-Dialog/Quest, Zunderlauf-Fang, Wechsel der gefangenen Kreatur ins Team, Teamkampf gegen Liora, Attack/Hit/Faint, Archivabschluss, Heilhaus betreten/verlassen, Heilung von HP/PP, Speichern/Laden, Gebäudeübergänge, acht Spielerrichtungen, Waldsichtbarkeit und Sprint. Walk 210 cm/s und Sprint 315 cm/s des Spielers bleiben erhalten. Ein Beobachter bestätigte Zunderlauf im Team und das Verbergen des gefangenen Wild-Visuals. Happy wurde in der Clipprüfung gezeigt; ein tatsächlicher siegreicher Zunderlauf-Teamkampf wurde damit nicht zusätzlich nachgewiesen.

Der vorhandene Dev-Spielstand wurde nach den Tests bytegenau wiederhergestellt: SHA-256 **`a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a`**. Die zwischenzeitliche Test-Save-Datei ist kein Ersatz für den ursprünglichen Nutzerstand.

Während der Entwicklung wurden unter anderem falsche lokale Beinachsen, ungeeignete Augen-Flächenorientierung, anfänglich maskierte Laufmischung, lange Frameintervalle in der Geschwindigkeitsmessung sowie nach Fang noch sichtbare Child-Visuals gefunden und korrigiert. Die oben genannten finalen Prüfungen erfolgten danach auf Build11. Keine fehlgeschlagenen Zwischenläufe werden als finale Erfolge gezählt. Die bekannte macOS-Startmeldung zum nicht ausführbaren alten `idevice_id`-Hilfsprogramm blieb unverändert; der finale Build und die Automation sind dennoch erfolgreich. Keine neuen Material-/Shaderfehler wurden in der finalen Editorsitzung festgestellt.

Nicht durchgeführt: Shipping/Cook, Standalone-Abnahme, GPU-Profiling oder FPS-Benchmarks. Die dokumentierte Laufzeitprüfung ist Editor-PIE. Daraus folgt keine Performance- oder plattformübergreifende Releasefreigabe.

## 7. Echte Unreal-Bilder und Bewegungsnachweise

Alle Bilder stammen aus der tatsächlichen bestehenden Unreal-Spielkamera, keine generierte Konzeptgrafik. Die Quelle enthält **67 verifizierte 2560 × 1440-Aufnahmen**. Eine erste Warm-up-Aufnahme hatte wegen asynchroner Fensteranpassung nur 2331 × 1346 und wurde ausdrücklich aus den QHD-Nachweisen ausgeschlossen. Die beschrifteten Ausschnitte sind jeweils zweifach vergrößerte Bereiche der echten QHD-Aufnahmen; sie erfinden keine höhere Originalauflösung.

![Zunderlauf neben der 1,40-m-Spielfigur, echter Unreal-Ausschnitt](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/Evidence/Zunderlauf_Spielkamera_Detail.png)

![Sieben Animationen, echte Unreal-Spielkameraausschnitte](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/Evidence/Sieben_Clips_Unreal.png)

- [Unbeschnittene QHD-Spielkamera](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/RuntimeReviewGrounded/Idle_00100000.png).
- [Zeitlich geordnete echte Bildsequenz als GIF](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/Evidence/Zunderlauf_Unreal_Bildsequenz.gif). **Keine Echtzeitvideoaufnahme**; aus zeitlich erfassten Spielbildern zusammengesetzt.
- [Finale Kampf-Weltaufnahme, QHD](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/Acceptance/BattleFinal11/BattleWorld_00000000.png).
- [Finaler Kampf mit UI und Editorrahmen](/Users/harry/Developer/PokeMonster/Saved/ZunderlaufV1/Acceptance/BattleFinal11/BattleUI_00100000.png). Dieses UI-Bild hat **2940 × 1696** und wird nicht als saubere QHD-Spielausgabe ausgegeben.
- Bild-/Socketprüfung: `Saved/ZunderlaufV1/Evidence/EvidenceAudit.json`.

Pillow für die reine Montage: `/Users/harry/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. Alle Kontrollmedien und Laufzeitlogs bleiben lokal im ignorierten `Saved/` und werden nicht hochgeladen. Die Links dieses Berichts benötigen deshalb den lokalen Nachweisordner; ein GitHub-Clone enthält die Kontrollbilder absichtlich nicht.

## 8. GitHub-Sicherung

Technik-/Assetcommit: **`137efa259092f7457bcdc33e5bc9599d942e5163`**, `feat: integrate animated Zunderlauf into existing creature flow`.

Vor dem Commit wurden genau 70 beabsichtigte Pfade, deren Indexinhalt und `git diff --cached --check` geprüft. Der neue normale Git-Blobumfang beträgt rund 1,13 MB (nicht die gemessene Netzwerk-Packgröße); größte normale Datei ist das Core-Manifest mit 682.279 Bytes. **33 einzigartige LFS-Objekte, zusammen 30.304.318 Bytes**, umfassen unter anderem Quelle, Exporte, Texturen, Referenzen und Unreal-Assets. Alle lokalen Pointer und Nutzdaten wurden vorab gehasht.

Der reguläre Push auf `origin/main` war erfolgreich. `git ls-remote` bestätigte den vollständigen technischen Commit. Danach wurden alle 33 LFS-Nutzdaten serverseitig abgerufen und ihre tatsächliche Größe und SHA-256 geprüft: `Saved/ZunderlaufV1/RemoteLFS_Technical.json`, `verified: true`. Die zusätzlichen Kontingent-/Abrechnungssummen des GitHub-Kontos wurden nicht abgefragt; es gab keine Quota-Fehler, Käufe oder Budgetänderungen. Die genannten Bytes bezeichnen diese geprüften Objekte, nicht die gesamte Kontonutzung.

Dieser Bericht und sein gezielt ergänzter Core-Manifest-Eintrag werden separat als Dokumentationscommit gesichert. Dessen endgültiger Hash wird im Abschluss genannt. Keine Kontrollvideos, Vergleichsbilder oder temporären Renderings sind Bestandteil der Sicherung. Der versionierte Arbeitsstand ist sauber; die 53 geschützten unversionierten Dateien bleiben weiterhin bewusst unversioniert. Kein Reset, Clean, Force-Push oder LFS-Prune wurde ausgeführt.

## 9. Verbleibende Qualität und nächste Starter

- Gesicht, Augeneinbettung und feine Schuppen sind gegenüber Foto 1 vereinfacht. Besonders bei vergrößerten Ausschnitten ist der Unterschied sichtbar; die aktuelle Form ist nicht als fotorealistischer Master freigegeben.
- Die Schwanzflamme ist ein kleiner stilisierter Mesh-Effekt. Sie erreicht nicht die feinen transparenten Flammenzungen der Vorlage.
- Kein Gesichtsausdrucksrig; keine Blink-/Mundanimation. Turn/Start/Stop nutzen vorhandene Mischung und Ausrichtung, keinen gesondert ausgearbeiteten Drehclip.
- Feine Welt-Fußkontakte, Richtungswechsel und steilere Geländeübergänge erfordern weitere manuelle Bewegungsabnahme. Der numerische Weltkontaktversuch ist unzureichend, nicht bestanden mit Nullabweichung.
- Die bestehenden Weltschatten wurden erhalten. Sie können in einzelnen Blickrichtungen Hautdetails verdecken; die Beleuchtung wurde nicht für einen schöneren Nachweis manipuliert.
- Prototypwerte, Starterhöhe und endgültige Balance sind noch festzulegen. Alte abgeschlossene Encounter bleiben abgeschlossen.

Empfehlung: **V1 als funktionsfähige, technisch geprüfte Integrationsgrundlage verwenden und jetzt visuell abnehmen.** Eine uneingeschränkte Freigabe als endgültiger Kreaturen-Master ist noch nicht gerechtfertigt.

Für die übrigen Starter kann derselbe optionale Präsentationsvertrag verwendet werden: bestätigte Referenz und Größe, erhaltene Blenderquelle, anatomisch geeignetes eigenes Rig, sieben Clips mit Geschwindigkeitsvertrag, Schwanz-/Effekt-Sockets nur nach Design, FBX-Roundtrip, Art-/Encounter-Daten im bestehenden System, reale Kampf-/Fang-/Heil-/Save-Prüfung, Spielkameraabnahme und gezielte Git-/LFS-Sicherung. Unterschiedliche Anatomien erhalten passende Rigs; die Zunderlauf-Beinkette ist kein ungeprüfter Standard für alle Kreaturen. Hier endet die Arbeit; keine weitere Kreatur oder Landschaftsüberarbeitung wurde begonnen.
