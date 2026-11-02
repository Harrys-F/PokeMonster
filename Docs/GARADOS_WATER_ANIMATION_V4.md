# Garados Water Animation V4

Stand 02.11.2026. Ausgangscommit `8a87765b54aae8c9b0ab460e2c6ba26138260638`, bestehendes Projekt `/Users/harry/Developer/PokeMonster`, VisualV2. Stärkere seitliche S-Welle und deutlich höhere Beobachtungspose auf Grundlage von V3. Die künstlerische Beurteilung erfolgt anschließend durch Harry. Keine Änderungen an KI, Gameplay, Weltgestaltung, Kamera oder Renderingprofilen.

## Quelle und bestehende Architektur

Harrys ursprüngliches `Art/Characters/Creatures/Incoming/Garados.glb` bleibt unverändert (SHA256 `ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9`). Alle ursprünglichen Meshy-/WaterV2-/WaterV3-Arbeitsquellen und Assets bleiben erhalten. Die neue Arbeitsquelle `Art/Characters/Creatures/Garados/Source/Garados_Water_V4.blend` basiert auf der vorhandenen V3-Quelle (SHA256 `13fe45be6c9c68a91bfa892e0c43542cc89f85c208fe2f15d1e59007b4ecae92`).

Dasselbe WaterV2-Mesh und dasselbe 22-Bone-Skeleton (Root, Kopf, 20 Körpersegmente). 24.049 Vertices, 26.298 Dreiecke. Kein neues Modell, keine Änderungen an Topologie, Ruhepose, Skinning, UVs, Materialien oder Normalen. Der Mesh-/Rig-/Skin-/UV-/Material-Fingerabdruck bleibt identisch: `e2fcccbba88c3553d8a3ff771d635b675b35af3bfdc4584307adc5cb6dfa7ff7`. Kein Mesh-/Skeleton-Reimport.

Die vorhandene einzelne SkeletalMeshComponent und der bestehende Animationsproxy bleiben zuständig. V3-Phasensynchronisation, 0,55-s-Bewegungsdämpfung, 0,40-s-Slow/Fast-Mischung, 1,1-s-Körpernachlauf, 32° begrenzte Kurvenkorrektur und die 3,2-s-Smoothstep-Haltungsübergänge bleiben unverändert. Keine zusätzliche Animations-Zustandsmaschine.

## Tatsächlich geänderte Animationen

Sechs zusätzliche reine Animations-FBXs unter `Garados/Exports/WaterV4` und sechs AnimSequence-Assets unter `/Game/Characters/Creatures/Garados/WaterV4/Animations`: **SwimSlow, SwimNormal, SwimFast, SwimTurnLeft, SwimTurnRight, SwimObserve**. Nur diese sechs Bindungen im bestehenden `MeshyV1/DA_Garados_Presentation` ersetzt. Der ruhige V3-SwimIdle bleibt unverändert; ebenso alle sieben Land-/Kampfclips und die vier WaterV2-Reaktionen Attack/Hit/Faint/Happy.

Alle sechs neuen Schleifen: 2,8 s, 60-Hz-Sampling, 169 Schlüsselbilder einschließlich exakt gleicher Anfangs-/Endpose. 1.014 Offline-Frames auf endliche Geometrie und Grenzen geprüft.

### Stärkere S-Welle

Die seitliche Tangentenwelle läuft weiterhin vom Vorderkörper zum Schwanz über 1,15 Phasenzyklen entlang des Körpers. Die nach hinten zunehmende Amplitude wurde deutlich verstärkt. Relative Stärke langsam/normal/schnell: 0,70 / 1,00 / 1,18; seitliche Tangentenhülle 0,060 bis 0,780 rad. Ruhiger Kopf, größere verzögerte Schwanzbewegung. Die Turn-Clips verwenden dieselbe normale Welle mit der bestehenden dezenten Kurvenlage. Die V3-Richtungshistorie verbindet beide Bewegungen; keine starre Ganzkörperrotation.

Die vorhandenen 35/70/125 cm/s und das vorhandene Ratenmapping bleiben erhalten: bei normaler Rate 2,8 s pro Zyklus, schnell höchstens 1,35-fache Abspielrate. Keine Veränderung der Bewegungs-/Kampfwerte.

| Ausgewertete Größe | V3 | V4 |
|---|---:|---:|
| Normale Schwanzbewegung, gegenüberliegende Phasen | 36,57 cm | ca.101,83 cm |
| Normale Körpermitte, gegenüberliegende Phasen | 28,36 cm | ca.71,33 cm |
| Kopf seitlich, normal | ca.3,2 cm | ca.4,0 cm |
| Kopf-Anhebung gegenüber flacher Wasserpose | 106,04 cm | ca.265,97 cm |

Die Angaben sind Bone-/Pose-Auswertungen, keine gemessene Geschwindigkeit der Schwanzspitze im realen Wasser. Die vollständigen Blender-Schleifen ergeben am Schwanzende langsam/normal/schnell ca.74,11 / 100,74 / 114,33 cm seitliche Spitze-zu-Spitze-Bewegung. Die leicht abweichende Unreal-Messung verwendet den letzten Bone-Anker, 32 Phasen und importierte Animationen.

### Höheres Aufrichten nach Kampfpose

Die **tatsächlich vorhandene unveränderte Kampfpose** wurde im echten ClassicBattle geprüft: ursprüngliches Meshy-Rig, Kopf 301,28 cm über dem Actor-Fußpunkt, Root unverändert. Echter Bildnachweis: `Saved/ProjectRefinement/GaradosWaterV4/BattlePoseReferenceFinal.png` (Editor-/PIE-Aufnahme einschließlich UI), technische Messung `BattlePoseReference.json`. Wasser- und Kampfskeleton unterscheiden sich; die Kampfanimation wird deshalb nicht unzulässig direkt auf das Wasserskeleton geblendet. Die Silhouette dient als Referenz für eine entsprechende Pose im vorhandenen Wasserrig.

Die vorderen 14 Körpersegmente krümmen sich mit einem weich auslaufenden Profil auf (vorn bis 75°, Exponent 1,10). Der Kopf wird leicht nach oben orientiert. Die hinteren Höhenanker bleiben unverändert auf der bisherigen Wasserhöhe; Root bleibt an derselben Stelle. Garados wird nicht als Ganzes vertikal verschoben. Die vorhandene Beobachtungserkennung, Verlangsamung vor dem Aufrichten, Haltezeit, Absenkung und der Wiederanlauf bleiben zuständig.

Ein erster Kandidat mit 82°/Exponent0,70 hob den Kopf ca.330 cm an. Er war technisch auswertbar, wurde aber visuell verworfen: in der festen niedrigen Kamera wurde der Kopf an mehreren nahen Uferpositionen abgeschnitten. Die endgültige Krümmung hebt ca.266 cm an (etwa 2,5× V3), wirkt weiterhin imposant und passt besser zur unveränderten Kamera. Kein Absenken der Kamera-Testanforderung und keine Änderung des Weltmaßstabs.

## Sichtbarkeitshülle und Grenzen

Der hohe Kandidat zeigte eine tatsächlich zu kleine Render-/Culling-Hülle: Kopf über alter Bounds-Oberkante. Ein neues optionales Präsentationsfeld `SwimBoundsScale` (Standard1, validiert1–2) verwendet bei Garados im Wasser **1,2**, auf Land/im Kampf wieder **1,0**. Es erweitert ausschließlich die visuelle Sichtbarkeitshülle. Kein verändertes Mesh, keine Kollision, kein größerer Navigationsradius und keine globale Rendering-/Qualitätseinstellung. Der Wert folgt aus der alten Bounds-Oberkante von etwa321 cm, der neuen vollständigen Silhouette bis etwa334 cm und einer Sicherheitsreserve.

Die vollständige Offline-Skin-Hülle bleibt innerhalb **368,03 cm** horizontalem Radius; vorhandener konservativer Gelände-Freiraum unverändert **400 cm**. Die Automation prüft zusätzlich die tatsächlich kombinierte Unreal-Skin-Auswertung samt enthaltenen Render-Bounds und die Rücksetzung auf Land. Die finale kombinierte Unreal-Skin-Auswertung erreicht 370,02 cm Radius und bleibt ebenfalls innerhalb400 cm; der importierte Kopf hebt 265,97 cm an. Auch Tiefgang180 cm, Ufer-/Bodenprüfung und Fischkontakt bleiben unverändert. Es ist ein endlicher geprüfter Poseumfang, kein mathematischer Beweis sämtlicher möglicher Kombinationen.

## Visuelle Prüfung und Rig-Grenzen

Echte QHD-Spielaufnahmen aus der bestätigten Third-Person-Kamera: Höhe ca.1,72 m, Pitch−12°, Arm350 cm; horizontales Umsehen. Kamera und FOV bleiben unverändert. Zusätzliche seitliche/diagonale Schwimmblicke sowie Beobachtung von drei Ufern und aus etwas größerem Spielerabstand. Der zusätzliche Abstand entsteht nur durch die Spielerposition im Test, nicht durch eine geänderte Kamera.

Finale Standbilder `PIE04/03_Normal.png`, `05_DelayedTurn.png`, `13_SwimSide.png`, `14_SwimDiagonal.png`, `07_Raising.png`, `08_Observe.png`, `16_ObserveWide.png`, `09_ObserveSide.png`, `10_ObserveSouth.png`, `11_Lowering.png`, `12_ReturnToSwim.png`. Die finale Pose wurde frontal und seitlich angesehen. Der Spieltest nutzt den real natürlich erschienenen Garados im bestehenden Teich; keine ersetzende Testfigur. Vorübergehend wird nur in der eigenen QA-Party der bestehende kleine Enton als Begleiter gewählt, damit das erhaltene große Garados-Landmodell die Wasserprüfung nicht verdeckt; ursprüngliche Reihenfolge wird wiederhergestellt. Der Garados-Landbegleiter wird getrennt geprüft.

Die vorhandene Wasseroberfläche verdeckt Unterwasserteile; kein neues Unterwassersystem oder transparenteres Material zur besseren Darstellung. Die S-Welle ist je nach Blickrichtung unterschiedlich stark projiziert, deshalb mehrere Richtungen. Bäume und der Vordergrundspieler können Sichtbereiche verdecken. Keine endgültige künstlerische Freigabe oder Behauptung vollkommen unverformter Oberfläche.

Zusätzliche Skin-Kontrolle: Vergleich von Kanten über1 mm mit V3 an vier Phasen pro Normal/Fast/Observe. Median der Längenverhältnisse jeweils ungefähr1. Normal p95≤1,027/p99≤1,113; schnell p95≤1,028/p99≤1,125; endgültiges Beobachten p95≤1,021/p99≤1,059. Einzelne kurze Übergangskanten erreichen dennoch größere Verhältnisse (Maximum ca.4,43 bei schnellem Schwimmen, ca.1,93 beim Beobachten); einige werden stärker gestaucht. Das sind verbleibende Grenzen der unveränderten Meshy-/V2-Hautgewichte, kein Nachweis vollständig verzerrungsfreier Oberfläche. Kein ungeprüftes neues Rig oder Weight Painting. Nachweis `DeformationComparison.json`.

## Technische Prüfungen

- **Build01:** Exit0,17,17 s. **Build02:** Exit0,35,15 s; letzter Produktions-C++-Stand einschließlich visueller Bounds. Danach nur eigene Animationsdaten, Präsentationswert und QA-Helfer verfeinert; keine weitere C++-Änderung. Bestehende Installation meldet Unreal **5.8.4/CL58902052**, Blender **5.2.2 LTS**. Keine Engineänderung; keine Prüfung unter5.8.2 behauptet.
- **Automation01:** 321/321 erfolgreich, keine Warnungstests/Fehler/Skips, Engine0/strenger Wrapper0,54,92 s; noch auf dem ersten Posekandidaten. Die bisherige320er-Serie wurde um einen echten V3/V4-Formvergleich ergänzt. **AutomationFinal:** endgültige Pose/Bounds, **321/321 bestanden**, 0 fehlgeschlagen/übersprungen/Warnungstests, Engine-Exit0 und **strenger QA-Wrapper Exit0**, 32,42 s. Nachweise `AutomationFinal/Result.json` und vollständiger Unreal-Automationreport im selben Prüfverzeichnis.
- Neuer Formtest: reale importierte Bone-Pose über32 Phasen, deutlich größere Körper-/Schwanzwelle, ruhiger Kopf, wesentlich höhere Beobachtung, gleicher Root/hinterer Höhenanker, exaktes vorhandenes Skeleton. Der bestehende V3-Test behält Übergangs-, Framerate-, Pause-, Yaw-Wrap-, Skin- und Land-Isolationsprüfungen; seine Bindungsprüfung berücksichtigt die nun ausdrücklich aktiven V4-Clips und den V3-Idle. Zusätzlich tatsächliche Skinoberfläche in Render-Bounds und BoundsScale1 nach Landwechsel.
- **Zwölf finale Map Checks** im eigenen Editor03 nach endgültiger Pose: jeweils **0 Fehler, 0 Warnungen** aus den begrenzten `GARADOS_WATER_V4_MAPCHECK_BEGIN/END`-Abschnitten, keine Map gespeichert. Nachweis `MapCheckResultsFinal.json`.
- **PIE04 bestanden:** 108,79 s, alle Geschwindigkeits-/Kurven-/Aufricht-/Absenk-/Wiederanlaufphasen, finale Pose und visuelle Bounds, mehrere Blickrichtungen, Menü-Save/Load sowie ursprünglicher Landbegleiter. Vollständige Teamfelder inklusive Identitäten, Level/EP, Attacken/AP, Position und pausierter Weltzeit exakt wiederhergestellt. Ausschließlich eigener expliziter PIE-Testslot.
- **PIEBattleFinal bestanden:** 13,33 s; normaler Ufer-Kampfstart, ursprüngliches Garados-Meshy-Kampfrig, BoundsScale1, normaler MasterBall-Fang mit eigenständiger neuer Instanz, bestehende Teamidentitäten erhalten, Menü-Save/Load. Drei unterschiedliche Prüfungen; wiederholte Logeinträge während der Bildaufnahme sind keine zusätzlichen Tests. Die vollständige Automation enthält weiterhin die vorhandenen V2-Angriff/Treffer/Ohnmacht-Auswertungen beider Rigs.

### Fehlversuche und Prüfskripte

PIE01 scheiterte am nicht erreichten schnellen Schwimmen; tatsächliche Geschwindigkeit während dieser Phase0, kein bestandener Gesamtlauf. Der eigene Vorschau-Test fordert bei längerem Stillstand innerhalb einer begrenzten45-s-Phase ein anderes vom **vorhandenen** Planer geprüftes Ziel an und protokolliert Tick, Sperren und Planungszähler. PIE02 bestand anschließend92,13 s, wies aber die zu kleine Bounds-Hülle nach. PIE03 bestand126,20 s nach deren Korrektur auf dem noch zu hohen Kandidaten; diese Bilder sind keine finale Posefreigabe. Der finale Nachweis ist PIE04. Keine Produktions-KI-/Kontaktänderung, kein abgeschalteter Fisch und keine abgeschwächte Geschwindigkeits-/Blend-Schwelle.

Bei Standbildern wurde zusätzlich der Zeitpunkt korrigiert: Unreals Shot-Anforderung muss abgeschlossen sein, bevor der Prüfspieler zur nächsten Uferansicht wechselt. Sonst zeigt das Foto den folgenden Kameraübergang. Das betrifft ausschließlich QA, keine Spielkamera. Native/PIE-Helfer und strenger Reportvertrag werden aus V3 weiterverwendet; siehe `Tools/GaradosWaterV4/README.md`.

## Separater Spielprozess und geprüfte Medien

**Motion01 bestanden:** eigener Development-Spielprozess, 239,61 s Prüfablauf, Prozess-Exit0 (258,36 s einschließlich Start/Ende). Alle 15 qualifizierten Aufnahmephasen einschließlich langsamen/normalen/schnellen Schwimmens, verzögertem Richtungswechsel, Aufrichten, Verweilen, Absenken und Wiederanlauf wurden erreicht. Render-Bounds enthalten die finale Pose. Keine Produktions-KI-, Kamera- oder Renderingänderung. Save/Load und ursprünglicher Garados-Landbegleiter wurden im normalen PIE04 und im echten Kampf getrennt geprüft; der Filmlauf wird nicht als zusätzlicher Save/Load-Nachweis ausgegeben.

Alle folgenden Pfade relativ zu `Saved/ProjectRefinement/GaradosWaterV4/`:

| Medium | Umfang und Prüfung |
|---|---|
| **`Garados_Water_V4_Motion.mp4`** | Vollständiger V4-Film, QHD2560×1440, H.264, **69,33 s / 1.040 echte Frames / 15 Bilder je Spielsekunde**. Alle 1.040 Frames dekodiert, Zeitstempel geprüft (max.3,62 µs Abweichung), tatsächliche Bildinhalte zusätzlich in jedem Frame auf leere/flache Frames geprüft. Alle qualifizierten Posen vor Filmende enthalten. |
| **`Garados_V3_V4_Vergleich_Beschriftet.mp4`** | Beschriftete V3/V4-Ausschnitte: Normal, schnell/Kurve, Aufrichten/Beobachten, Absenken; zusätzlich V4-Seitenblick und Wiederanlauf. **38,00 s / 570 Frames / 15 fps**, alle Frames dekodiert und auf Bildinhalt geprüft, exakte Zeitstempel, keine mehrfach verwendeten Quellframes. Sichtbare Beschriftung anhand dekodierter QHD-Bilder kontrolliert. |
| `PIE04/*.png` | Echte finale QHD-Standbilder aus normalem PIE. Obige Dateinamen bezeichnen die einzelnen Phasen/Blickrichtungen. |
| `BattlePoseReferenceFinal.png` | Tatsächliche ursprüngliche Kampfpose im ClassicBattle einschließlich UI, ohne Bearbeitung von Kampfrig oder -animation. |

Die Aufnahme benutzt ausschließlich für den Film feste30-Hz-Simulationsschritte und echte Aufnahmen jedes zweiten Simulationsbildes. Die Erfassung der1.040 Frames dauerte **152,22 s Echtzeit**, entsprechend **6,83 erfassten Bildern pro Echtzeitsekunde**. Die15-fps-Wiedergabe ist daher eine zeitlich korrekt zusammengesetzte Offline-Animationsaufnahme, **kein Nachweis von15 oder30 live aufgenommenen Gameplay-FPS**. Keine Interpolation oder künstlich vervielfachten Ersatzbilder. Die normale macOS-Fensteraufnahme war zuvor durch TCC blockiert; keine Aufnahmeberechtigung verändert oder neue Freigabe behauptet. Feine schnelle Bewegungen bleiben durch15 Stichproben pro Spielsekunde begrenzt beurteilbar.

Der historische V3-Film stammt aus dem vorherigen echten V3-Test. Der Vergleich zeigt zwei reale Testläufe mit gleicher Kamerakonfiguration; Pokémon-/KI-Verlauf und genaue Welt-/Lichtsituation sind kein pixelidentischer deterministischer Replay. Bildbeschriftung und Ausschnittwahl verändern keine Animation oder Modellform. Der vollständige ungeschnittene V4-Film bleibt separat verfügbar. Ein erster Vergleichsentwurf mit überlappenden Quellframes und ein weiterer mit fehlender Schrift wurden verworfen; nur die oben ausdrücklich **Beschriftet** genannte Fassung ist der finale Vergleich. Nachweise: `VideoVerification.json`, `VideoPixelCheck_Raw.json`, `ComparisonVerificationLabelled.json`, `VideoPixelCheck_Labelled.json`, `ComparisonExpectedPTS.csv` und `ComparisonSegmentsFinal.json`.

## Warnungen und verbleibende Einschränkungen

Die strenge finale Automation hat Exit0; das bedeutet keine globale Warnungsfreiheit sämtlicher Editorlogs. Getrennte Einordnung in `LogClassification.json`: bekannte17 Startup-„Condition failed“-Diagnosen im Automation-/Editorlauf, vorhandene Westland-Material-Usage-Warnung `MI_WLA_LeafOak` im Map-Check-Editor und fehlender Toolset-Python-`PythonTestRunner` beim nativen Start. Keine fatalen Engine-Assertions und keine `idevice_id: Bad CPU type`-Meldungen in diesen finalen Läufen. Die externen iOS-Helferwarnungen bleiben eine getrennte bekannte Infrastrukturfrage; ihr Auftreten wird hier nicht erfunden. Der Offline-Videoeditor meldete zusätzlich veraltete AVFoundation-Schnittstellen; Exporte und anschließende vollständige Dekodierung waren erfolgreich. Keine Unreal-Abstürze oder erneuter Editorstillstand in den finalen Prüfungen.

Die unveränderte niedrige Third-Person-Kamera kann bei sehr geringem Spielerabstand oder engerem Zoom ein so großes aufgerichtetes Pokémon weiterhin anschneiden. Die finale Pose wurde aus mehreren begehbaren Uferansichten vollständig sichtbar geprüft. Verdeckungen durch Spielfigur, Wasser und Vegetation bleiben möglich. Die oben dokumentierten lokalen Skin-Grenzen bleiben bestehen. Kein physischer Gamepad-Test und keine endgültige künstlerische Freigabe behauptet; Steuerung unverändert. Harry beurteilt die stärkere S-Welle und höhere Haltung anschließend selbst.

## Projektschutz

Ausgangs- und Abschlussprüfung: **6.045** zuvor versionierte Dateien, **351** geschützte/unversionierte Dateien einschließlich lokaler Fab-Quellen und **672** vorhandene Save-Dateien per SHA256 verglichen. Ausschließlich die sieben vorgesehenen bestehenden Produktions-/Test-/Werkzeug-/Dokumentationsdateien unterscheiden sich vom Ausgangsstand; alle351 geschützten Dateien und672 alten Saves unverändert und vollständig vorhanden. Neue eigene V4-Dateien werden separat gezielt hinzugefügt. Nachweis `ProtectionCheck_Final.json`. Vorhandene lokale vier Zeilen in `Config/DefaultEngine.ini` bleiben unverändert und außerhalb des Commits. Originalmodelle, WaterV2-/V3-Mesh/Skeleton/Clips, Land-/Kampfanimationen und alle Maps bleiben unverändert. VisualV2-SHA256 `ae9ed79aa91fc2b83d6c328010aa6a7d176d12c6a6f84140ed07ee0389c98a34`; die Buchenwald-Rücknahme `f10dc77f` bleibt erhalten. Keine neuen Maps/Worktrees/Projektkopien, keine Backup-Ref-Änderung und kein LFS-Prune.

Harry hat ausschließlich den vorhandenen Nutzereditor PID32039 regulär zum Schließen freigegeben. Er zeigte kein PIE und „Alle gespeichert“; normal über Cmd-Q geschlossen. Alle späteren Editoren/Spielprozesse sind eigene isolierte Prüfprozesse und werden regulär beendet; kein Force Quit oder Verwerfen ungespeicherter Nutzeränderungen. Eigene QA-Saves und Kontrollmedien bleiben nur unter Saved.

Nur eigene erfolgreich geprüfte Animationsquellen/FBXs/Assets, notwendige Präsentations-Boundskorrektur, Tests/Werkzeuge und Dokumentation werden gezielt committed. Der Commit dieses Berichts ist über `git log -1 -- Docs/GARADOS_WATER_ANIMATION_V4.md` eindeutig auffindbar; konkreter Hash sowie nach dem normalen Push verifizierter Remote-/LFS-Status werden im Chat mitgeteilt. Danach keine weiteren Änderungen bis zu Harrys Beurteilung.
