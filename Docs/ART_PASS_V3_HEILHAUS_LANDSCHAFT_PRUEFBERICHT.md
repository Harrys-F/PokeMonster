# Art-Pass V3 – Heilhaus und Landschaft

Stand: 20.10.2026. Aktives Projekt ausschließlich `/Users/harry/Developer/PokeMonster`; Unreal Engine 5.8.2, Blender 5.2.2 LTS. Zielkarte `/Game/Maps/Dev_TestMap_VisualV2`.

## Ergebnis und Abnahmegrenzen

Die VisualV2 enthält einen schlagschattenfreien, weiterhin räumlich schattierten Heilraum mit freier Raummitte, eine unabhängige SilverLady-Standpose am bestehenden Heilpunkt, räumlich gefaltete Farne und zurückhaltend unregelmäßigere Wege. Außenlichter, Außenschatten, Kamera, TAA und Gameplay bleiben erhalten. Technische Prüfung und Sicherung sind erfolgreich. **Keine pauschale künstlerische Endfreigabe.**

**Offen:** Das sporadische Fensterflackern wurde nicht zuverlässig reproduziert; es gibt keinen bestätigten Ursachenfix. SilverLady ist statisch und besitzt noch kein geprüftes Animationsrig oder Idle-/Talk-Clips. Die äußeren Sonnenkontraste werden nicht als gelöst oder um 50 % aufgehellt ausgegeben.

## Ausgangszustand und Schutz

Ausgangs-HEAD/main/origin/main: `41bcfefe44c939d1fe6b4c73b293ff0c5ed9b71a`. Zunächst keine getrackten Änderungen; 53 bestehende unversionierte Dateien, einschließlich vier Kreaturen-GLBs, Cleanup-Unterlagen, historischen Werkzeugen und einer EnvironmentQuality-Map. Alle 53 Dateien am Ende anhand ihres ursprünglichen SHA-256 verifiziert und nicht aufgenommen. Keine neuen Maps, Worktrees, Projektkopien, Vollbackups, Löschungen oder destruktiven Git-Befehle. Zehn andere Mapdateien bytegleich erhalten.

Beide lokalen Vollbackup-Refs bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Der vorgefundene Editor war nicht geöffnet; eigene Sitzungen wurden über die bestehende kontrollierte Warteschlange normal beendet. Kein Save All, Discard All oder Force Quit.

## 1. Innenraumschatten

Ursache der bisherigen direkten Schlagschatten: Der räumlich versetzte Heilraum und seine Playerdarstellung wurden vom allgemeinen direkten Außenlicht mitbeleuchtet. Im vorhandenen System lässt sich direkte Beleuchtung über Lichtkanäle trennen; Lumen-GI ist dadurch nicht vollständig isoliert.

- Nur vorhandene Raumkomponenten und Raumlichter erhalten Kanal 1; ihr Schattenwurf wird deaktiviert. Materialien bleiben räumlich beleuchtet und behalten Rauheit/Normalen.
- `bUseShadowlessInteriorLighting` ist nur am bestehenden Heilhaus-Cutaway aktiviert. Player-Komponenten werden beim tatsächlichen Raumaufenthalt zugeordnet; ursprüngliche Kanalbits und Schattenflags werden beim Verlassen, opt-out und EndPlay restauriert.
- Eine einzige breite, bewegliche RectLight auf Kanal 1 ergänzt 550 lm, 5000 K, Quellfläche 650 × 500 cm, Reichweite 1250 cm. Kein Schattenwurf, indirekte Intensität 0, volumetrischer Beitrag 0. Keine direkte Beleuchtung von Kanal-0-Außenobjekten.
- Ein erster 2000-lm-Entwurf war sichtbar zu hell und wurde auf 550 lm korrigiert. Er wurde nicht als finaler Stand übernommen.
- Sonne, Skylight, bestehender Außenfüllanteil, Außenfensterlichter, Lumen, Bloom, Exposure und Kameras bleiben unverändert. Die gespeicherten Außen-Actor-/Postprocess-Signaturen stimmen mit dem Ausgangsstand überein.

Echte QHD-Innenaufnahmen zeigen keine sichtbaren harten Schlagschatten von Player, Möbeln, Raumteilen oder Heilerin. Indirekte Formschattierung und Materialkontraste bleiben sichtbar; dies ist keine Abschaltung aller Beleuchtungswirkung.

## 2. Fensterflackern: untersucht, nicht als behoben gemeldet

Die tatsächlichen sichtbaren Scheiben verwenden `M_HH_Art_Window` unter `/Game/Environment/HealingHouse/ExpandedArtV1/Materials`. Dieses Material ist **Opaque**, nicht transparent/alpha-geclippt, nicht zweiseitig; vier einfache Ausdrücke, schwache Emission, keine Time-/Ditheranimation. Teile der äußeren Holzrahmen besitzen das vorhandene HouseCutaway-Material; das ist nicht das Scheibenmaterial.

Geometrie, Materialgraphen, Raumlichter und überlappende Bounding Boxes wurden geprüft. Rahmen-/Wandüberschneidungen allein belegen kein Z-Fighting. Eine zweite versehentlich sichtbare Scheibeninstanz wurde nicht nachgewiesen. Weder eine konkurrierende animierte Lichtquelle noch TAA oder Lumen wurden als Ursache bewiesen.

Vorher und nachher je 80 echte 1280×720-Aufnahmen in vier zeitlich geordneten Folgen: Innenraum still, Innenraumgehen, Außenannäherung und Außenrückweg. Etwa zwei Sekunden Einpendeln, dann je 20 Aufnahmen in Abständen von mindestens 0,30 s. Außenbewegung verändert die tatsächliche Spielkamera, Innenraumkamera bleibt absichtlich fest. Manche späten Rückwegframes verlassen den interessierenden Fensterbereich; sie sind kein Beleg für eine durchgängige Fensterprüfung.

Stationäre Scheibenausschnitte schwanken zeitlich gering: mittlere Pixelstandardabweichung vor/nach links 0,603/0,393, rechts 0,427/0,446 auf einer 8-Bit-Skala. Putzreferenz 0,387/0,452. Das sind Stichproben, **kein Nachweis einer Fehlerursache oder Reparatur**; zudem unterscheidet sich die beauftragte Raumbeleuchtung. Kein hypothetischer Materialumbau, kein AA-/Lumen-Workaround. Für einen bestätigten Fix wird weiterhin eine reproduzierbare konkrete Flackersituation benötigt.

## 3. Möbelanordnung und Laufwege

Bestehende hochwertige Möbel werden wiederverwendet. Keine neue Innenraum-Map und keine neue Möbelserie.

| Element | Vorher cm | Nachher cm | Zweck |
|---|---|---|---|
| Zusätzliche Bank | 16825 / 200 / 0 | 16520 / 190 / 0 | Wartesitz an Eingangsseite, freie Mitte |
| Wartetisch | 16670 / 215 / 0 | 16635 / 215 / 0 | Kompakte Sitzgruppe links |
| Eingangsläufer | 16785 / 505 / 3 | 16665 / 505 / 3 | Kürzer/schmaler; Skalierung 1,25 / 0,86 / 1 |

Bei Bank und Tisch bewegen sich sichtbares Q3-Mesh und der vorhandene maßgebliche Kollisionsblocker gemeinsam. Kollisionstypen bleiben erhalten. Tischdekoration und Mörser folgen dem Tisch um 35 cm. Ein überlappender zusätzlicher Empfangsteppich ist unsichtbar erhalten. Schränke/Regale bleiben an den Wänden, Empfang hinten, Behandlung rechts; Türen und Heilansprache bleiben frei. Alle neun konkreten Bewegungen stehen in `Art/HealingHouse/ArtPassV3_Interior.json`.

Der echte Rundweg erreicht Empfang, verlässt den Raum und wiederholt diagonale Ein-/Ausgänge ohne Blockierung. Dies ist keine Exhaustivprüfung jeder denkbaren Möbelkante.

## 4. SilverLady am bestehenden Heilpunkt

Gefundenes Original: `Art/Characters/NPCs/SilverLady/Source/SilverLady_NPC_Source_V1.blend`; bestehender statischer 149.999-Dreiecke-Export `SM_SilverLady_Reference_V1.fbx`, drei vorhandene Texturen und `MI_SilverLady_V1`. Die ursprüngliche Blenderquelle ist erheblich dichter; sie wurde nicht überschrieben. Der vorhandene Unreal-Export ist eine T-Pose ohne geeignetes Animationsskelett.

Eine unabhängige Blenderdatei übernimmt genau den bestehenden Export. Eine begrenzte 9-Bone-Pose-Studie senkt die Arme und hält die weiten Ärmel eher der Schwerkraft folgend. Sie ist **kein geprüftes NPC-Animationsrig**. Gesicht, Kleid, ursprüngliche Texturen und High-Poly-Quelle werden nicht neu erzeugt. Eine unveränderte Geometriereferenz bleibt innerhalb der neuen Arbeitsdatei erhalten.

Neue Quelle `Art/Characters/NPCs/SilverLady/Source/SilverLady_HealerPose.blend`; neuer statisch gebackener Export `Exports/SM_SilverLady_HealerPose.fbx`; neues Unreal-Mesh `/Game/Characters/NPCs/SilverLady/Meshes/SM_SilverLady_HealerPose`. 177.228 indizierte Exportvertices, 149.999 Dreiecke, ein Materialslot, keine einfache Meshkollision. Maßstab 0,905 ergibt rund 172,24 cm einschließlich Haaren; Fußpunkt ungefähr auf dem Boden. Der Player bleibt 140 cm.

Die vorhandene NPC-Präsentationsklasse erhält eine ausdrücklich optionale statische Komponente, nur bei gesetztem Asset. Vorhandene Skeletal-NPCs erhalten keine leere zusätzliche Komponente. Das neue Präsentationsobjekt verweist auf denselben `V2_House_HouseHealer` bei unverändert 17230 / 420 / 62 cm. Identität, ursprüngliche Kapsel, Dialog, Heilen, Checkpoint und Save-Funktion bleiben am Quellactor. Kein neuer Gameplay-Collider. Der ursprüngliche Sprite bleibt als geprüfter Fallback verfügbar.

Mesh-Vorwärtsachse +Y: Anfangsyaw 90°, Forward-Offset −90°. Der bestehende Offset wird jetzt auch bei Gesprächsdrehungen angewendet; Standardwert 0 verändert andere NPCs nicht. Blickwendung und Sprite-Fallback wurden im gerenderten PIE geprüft.

Nach unabhängiger Wiederöffnung wurden zwei historische FBX-Texturpfade der mitgeführten Referenz gefunden. Nur die neue Arbeitsdatei erhielt die vorhandenen aktuellen Texturen gepackt; Geometrieprüfsummen blieben identisch. Abschließend fünf gepackte Bilddatenblöcke, keine fehlenden Bildquellen oder externen Bibliotheken. Noch vorhandene Ärmel-/Haaroberflächen wirken in Nahsicht teilweise grob; die offene Standhaltung ist nur eine Zwischenlösung. Kein Idle, Talk, Walk oder hochwertiges Kleid-Skinning wird behauptet.

## 5. Landschaft und Wege

Die bestehende V7-/jüngere Gestaltung einschließlich Bäumen, Detailgruppen und Pflanzpositionen bleibt Grundlage. Keine Flächen werden ausgedünnt.

- Vorhandenes Wegfeld bleibt einschließlich aller Mittellinien und Brückenschutzmasken erhalten. Zusätzliche langsame Breitenvariation bis ±8 und ±4 cm, zusätzliche kleine Randabweichung bis ±3 cm. Farb- und Deckkraftgraph verwenden dieselbe Korrektur. Keine neue Weggeometrie, Kollision oder Navigation.
- Erdpalette wird um 8,5 % zum eigenen Luminanzwert entsättigt. Das beruhigt warme Spitzentöne geringfügig, ohne Emissive-Aufhellung oder globales Licht-/Schatten-Tuning. Es wird keine messbare Schattenaufhellung behauptet. Harte Außenschattengrenzen bleiben.
- Zwei neue räumlich gefaltete Farnwedelvarianten aus Blender: A mit sieben Wedeln/168 Fiedern, 3.017 Vertices und 3.990 Dreiecken; B mit neun Wedeln/216 Fiedern, 3.879 Vertices und 5.130 Dreiecken. Blattflächen sind gezielt offene gefaltete Flächen, kein wasserdichtes Charaktermesh. Keine Alpha-Karten.
- Ersetzt werden ausschließlich die Mesh-/Materialbindungen von **224 bestehenden Instanzen in zwölf Gruppen**. Transformationen, Anzahl, Schattenflags und Kollisionstypen bleiben gleich. Vorherige Farnmeshes mit je 8.030 Dreiecken und alle anderen Maps bleiben unverändert. Ein vorhandenes instancingfähiges Vertexfarbenmaterial wird wiederverwendet; ein Slot je Variante.

Quellen: `Art/World/VisualV2WorldArtV7/Source/Westland_Ferns.blend`, zwei FBXs unter `Exports/`, `FernRefinement.json`, `ArtPassV3_Landscape.json`, `ArtPassV3_PathGraphs.json`. Private Unreal-Meshes unter `/Game/Environment/VisualV2WorldArtV7/Meshes/`. Drei bisherige private VisualV2-Heilhaus-Landschaftsmaterialien werden gezielt angepasst; ursprüngliche V7-Materialien bleiben erhalten. `Art/HealingHouse/RefinedGraphs.json` enthält die tatsächlichen aktuellen Graphen.

## 6. Tatsächlich durchgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | Erfolgreich, 28,76 s |
| Gesamte Projekt-Automation | 50/50 erfolgreich, 0 Warnungsfälle/Fehler/übersprungene Tests, 31,76 s |
| Zusätzliche Python-Map-Lifecycle-Tests | 5/5 erfolgreich |
| Laden/Map Check aller vorhandenen Maps | 11/11, jeweils 0 Fehler und 0 Warnungen |
| NPCMotionV3-Regressionsaudit | Bestanden, alte Actor-Signaturen und Ranger-Quellidentität unverändert |
| Strenger VisualV2-Scope-Audit | Bestanden: 1.421 erfasste Actor, nur zwei neue Actor; vorhandene Gameplay-/Kameradaten, Außenlicht und PP erhalten |
| Vollständiger gerenderter PIE-Fußlauf | 102 Schritte, 286,33 m, 179,37 s Spielzeit, 212,49 s reale Zeit; ohne Testteleports |
| Gezielte Tür-/Heilhauswiederholung | 33 Schritte, 84,20 m; 298 Innenraum-, 385 Außenraum- und 37 Heiler-Gesprächsframes im zusätzlichen Audit |
| Beide neuen Blenderquellen erneut geöffnet | Bestanden; keine fehlenden Texturen, keine Änderung durch Prüfung |
| QHD-Bildpaare | Neun Paare, echte 2560×1440-Ausgabe, High, 100 %, eingebettetes PIE; identische Kameradaten auf <0,001 verifiziert |
| Kontrollmedien auf GitHub | Keine |

Der Fußlauf verwendet tatsächliche Enhanced-Input-Bewegung im gerenderten Spiel, nicht reine Actor-Teleports. Er prüft Wanderer-Dialog/Quest, Liora, Wildkampf/Fang, Archiv, Menüs, Save/Load, Brücke, Sprint mit 315 cm/s, normalen Gang mit 210 cm/s, acht Richtungen, Heilhausübergänge/Diagonalen, vollständige Heilung und Checkpoints. Zwei NPC-Sprite-Fallbacks und die SilverLady-Interaktion sind geprüft. Die Fotowerkzeuge positionieren den Player dagegen absichtlich zu Diagnosezwecken; sie werden nicht als Fußlauf ausgegeben.

Ursprünglicher Dev-Save in beiden Läufen exakt restauriert: SHA-256 `a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a`. Keine manuelle Controllerabnahme, kein Standalone-Durchlauf und keine FPS-/GPU-Benchmarks in diesem Auftrag.

### Abgebrochene bzw. korrigierte Prüfungen

Eine zusätzliche erste Laufzeitprobe benutzte irrtümlich einen breiten X-Bereich als Raumdefinition. Sie meldete am Türvorraum einen Schattenfehler, obwohl dort die Außenflags bereits korrekt restauriert waren. Dieser fehlgeschlagene Nachweis bleibt lokal erhalten. Die Wiederholung verwendet exakt `IsViewerInRelocatedRoom`, wie der Produktcode; der 84,20-m-Lauf und sämtliche Innen-/Außen-/Gesprächsproben sind bestanden. Der Produktcode wurde deshalb nicht kaschierend verändert.

Frühe Werkzeugläufe wurden wegen unpassender Python-Property-Zugriffe abgebrochen und nach Korrektur wiederholt. Die erste separate Quellenprüfung fand die oben genannten fehlenden Referenztexturen; nach ausschließlich lokal begrenzter Reparatur bestanden beide unabhängigen Wiederöffnungen. Ein früher 50-Test-Lauf hatte einen Warnungsfall durch den vorhandenen Unreal-iOS-Gerätedetektor (`idevice_id`: Bad CPU type). Der endgültige Build und neue vollständige Lauf haben 50 reine Erfolge ohne Warnungsfälle. Engine-Startmeldungen wie `UnifiedErrorTest`/`Condition failed` stehen vor der Projekt-Testqueue im Editorlog und wurden nicht unterdrückt; sie sind nicht die 50 ausgewerteten Projekttests. Im abschließenden Art-Editorlog wurde kein Material-/Shaderkompilierfehler gefunden.

## 7. Echte Bilder und Rohdaten

Alle Kontrollmedien bleiben ausschließlich lokal und optional, nicht auf GitHub. Basispfad `/Users/harry/Developer/PokeMonster/Saved/ArtPassV3/`. Die Originale liegen unter `Before/` und `After/`, jeweils `<Ansicht>00000.png`. `PhotoValidation.json` enthält die exakten Kamera-/Auflösungsprüfungen. Die folgenden JPEG-Tafeln kombinieren nur echte Spielscreenshots; links vorher, rechts nachher, für die Darstellung verkleinert.

| Ansicht | Vergleichstafel relativ zum Basispfad |
|---|---|
| Innenraum / Möbel / Player | `Comparisons/Innenraum.jpg` |
| Empfang und Heilerin | `Comparisons/Empfang.jpg` |
| Heilbereich | `Comparisons/Heilbereich.jpg` |
| Heilhaus außen | `Comparisons/Heilhaus.jpg` |
| Fassade / Außenschatten | `Comparisons/Fassade.jpg` |
| Wald / neue Farne | `Comparisons/Wald.jpg` |
| Wiese / Weg | `Comparisons/Wiese.jpg` |
| Flussufer | `Comparisons/Flussufer.jpg` |
| Uferabzweig | `Comparisons/Uferabzweig.jpg` |

Dialognachweis mit sichtbarer Spieloberfläche: `Acceptance/RoomBoundary/SilverLady_Healing_000000.png` und drei Folgeaufnahmen. Diese UI-Aufnahmen enthalten das Editorfenster und sind nicht als reine 2560×1440-Renderausgabe deklariert. Fensterfolgen: `WindowBefore/`, `WindowAfter/`, jeweils tatsächliche Dateien in `Result.json`; Übersichten `WindowBeforeSequence.jpg` und `WindowAfterSequence.jpg`. Keine Videoabnahme behauptet.

Lokale maschinenlesbare Nachweise: `ScopeValidation.json`, `MapCheckResults.json`, `FinalMapAudit.json`, `BlenderReopen.json`, `PackedReferenceFix.json`, `WindowTemporalFinal.json`, `Acceptance/Final/FootTest.json`, `Acceptance/Final/SaveRestored.json`, `Acceptance/RoomBoundary/RuntimeAudit.json`, `ArtRemoteLFS.json`. Build-/Automationprotokolle unter `Saved/ProjectRefinement/ArtV3FinalBuild/` und `ArtV3FinalAutomation/`. Zusammenfassung ohne notwendige Medienabhängigkeit: `Tools/ProjectMaintenance/ArtV3Acceptance.json`.

## 8. GitHub-Sicherung

1. `f785fd1ff5d8485a17c1f967e735d8b5a28769da` – opt-in Innenraumbeleuchtung, optionale statische NPC-Präsentation und Regressionstests. Regulär auf origin/main gepusht und Remote geprüft.
2. `0bf877efa22869d703d12c0ad9f22d9d004aebf2` – geprüfter Art-Pass mit 34 exakt ausgewählten Projektpfaden. Zwölf LFS-Objekte, **61.042.873 Bytes**, vollständig übertragen und anschließend serverseitig heruntergeladen/gegen SHA-256 geprüft. Normale Indexdateien zusammen 1.217.995 Bytes. Keine Kontrollbilder, Videos, Caches oder Builds aufgenommen.
3. Dieser Abschlussbericht, technische Dokumentation und die kleine maschinenlesbare Abnahme werden separat gesichert; den zugehörigen Hash nennt die Abschlussantwort bzw. `git log`.

Vor den Commits exakter Indexvergleich, LFS-Pointer-/lokale Payloadprüfung und `git diff --cached --check`; zusätzlich `git diff --check` und erforderliche Core-Fingerprints geprüft. Alle neuen binären Quellen/Assets laufen über die vorhandenen LFS-Regeln. Keine Konto-/Budgetänderung, kein Force-Push, kein Prune.

## 9. Empfehlung und nächste Entscheidung

Innenraumlayout, Schattenfreiheit und die neuen Farnsilhouetten anhand der echten QHD-Paare visuell abnehmen. Die technische Sicherung ersetzt diese Abnahme nicht. Für SilverLady sind als gesonderter nächster Schritt ein belastbares Kleid-/Ärmelrig und dezente Idle-/Talk-Animationen sinnvoll; die vorliegende Standpose bleibt ein begrenzter Zwischenstand. Für das Fensterflackern zuerst eine konkrete reproduzierbare Spielsituation aufnehmen und erst danach die bestätigte Ursache beheben. Keine weiteren Schatten-, Licht- oder Landschaftsexperimente automatisch übernehmen.
