# PokeMonster – Wanderer / Ranger Animation Quality V2

Stand: 16.10.2026. **Funktionsfähiger, geprüfter Arbeitskandidat. Noch keine Freigabe als fertig ausgearbeiteter Referenz-NPC und keine Übernahme in VisualV2.**

Neue Arbeitskarte: **`/Game/Maps/Dev_TestMap_NPCMotionV2`**. Sie enthält den bisherigen Wanderer mit seiner bisherigen Identität, Position und Dialog-/Questanbindung, neuer visueller Darstellung und einen standardmäßig deaktivierten, eindeutig markierten Bewegungsprüfling. Der Story-Wanderer patrouilliert nicht.

## 1. Ausgangslage und Schutz

`351a3ef Add YoungTrainer sprint V1 and in-place run animation`. Arbeitsbaum bereits geändert; Ausgangsstatus: [GitBefore.txt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/RangerAnimationV2/GitBefore.txt). AGENTS, relevante Technik-/Stil-/Spielidee-/Spielregeln-/Entscheidungsabschnitte sowie NPC-, Ranger- und Environment-V1/V2/V3-Prüfberichte gelesen. Tatsächliche Dateien und Runtime geprüft; ältere Chatangaben sind keine Freigabe.

Beim ersten Editorcheck: EnvironmentPerfV3 geöffnet, kein PIE, keine dirty Map-/Content-Pakete. Keine Save-All-/Discard-All-Aktion. Die sichtbare Speicherdruckbenachrichtigung wurde nicht zum Verwerfen von Paketen benutzt. Die offene Blender-Sitzung enthielt ungesicherte Hobbit-Retopo-Arbeit und blieb unverändert. Modellarbeit erfolgte in separaten Blender-5.2.2-LTS-Hintergrundprozessen. Unreal 5.8.2/Mac Development Editor.

Von 3.208 anfangs erfassten Projektdateien bleiben **3.204 bytegleich**. Ausschließlich vier bestehende, bereits unversionierte NPC-Präsentationsdateien sind gezielt erweitert. Keine Ausgangsdatei fehlt. Alle Incoming-GLBs, bisherigen Ranger-/Hobbit-/Player-Blenderquellen, V1-/Spieleranimationen, bisherigen Unreal-Assets und Karten sowie TECHNIK/ENTSCHEIDUNGEN bleiben gegenüber Auftragsbeginn bytegleich. Nachweis: [ScopeAndFiles.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/ScopeAndFiles.json); vollständiger ursprünglicher Hashbestand: [ProtectedBefore.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/ProtectedBefore.json). Ignorierte Build-/Cache-/Logdateien zählen nicht zu dieser Aussage.

Der Dev-Slot wurde vor Tests kopiert und nach dem Fußlauf unter Hashkontrolle wiederhergestellt. SHA-256 vorher/nachher: `626d58c2f512b3c63f90a18537fd646f611adecb76d52827428a67f578bbd21e`. Der zusätzlich erzeugte Testspielstand liegt separat in Saved; die spätere Kollisions-/Dialogprüfung änderte den Slot nicht.

## 2. Neue Karte und bestehendes Gameplay

Kopie über `EditorLoadingAndSavingUtils.save_map` auf einen neuen Paketpfad und anschließendes Laden dieses Pakets. Keine Originalkarte gespeichert. Finaler Actor-/Komponentenvergleich gegen VisualV2: **keine fehlenden Actors und keine Unterschiede vorhandener Actor-Transforms, Static-Mesh-Geometrie, Materialien, HISM-Instanzen, Collision, Lichter oder Postprocess-Einstellungen**. Zwei zusätzliche Actors ausschließlich für explizite Preview: kollisionsloser Source-Halter und deaktivierter Visualactor. [FinalMapAudit.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/FinalMapAudit.json).

Wanderer-Source bleibt `Slice_Wanderer_Hinweis`, Name „Wanderer“, `DA_SliceGuideDialogue`, Position **−920 / −1080 / 65 cm**. Visualbasis weiterhin Z=3 cm. Kein Austausch des Gameplay-Actors, keine neue NPC-Identität, kein Dialog-/Quest-/Save-Schema, keine AI-Patrouille. Quelle/Anbindung: [MapBefore.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/MapBefore.json), [MapConfigured.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/MapConfigured.json).

Außenkamera bleibt **2850 cm / Pitch −50° / Yaw −45° / FOV 35°**. Player 140 cm, normale Bewegung 210 cm/s, Sprint 315 cm/s, Capsule, Input, Interaktionen und Playeranimationen unverändert. Die bestehenden Innenkamera-/Relocation-Übergänge bleiben bestehen. Viewportgrößen wurden nur für explizite Mess-/Bildsitzungen gesetzt; keine Zoom-, FOV- oder Follow-Änderung gespeichert.

## 3. Blenderquelle, Geometrie und Rig

Ausgangspunkt: `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V2_Protected.blend`, mit der erhaltenen 90k-Geometrie und den geschützten 55k-/24k-Kandidaten. Ursprünglicher GLB-Ursprung: `Art/Characters/NPCs/Incoming/Aragorn_V1.glb`; dieser wurde weder verändert noch neu generiert.

Neue selbständige Quelle: [Ranger_NPC_AnimationQuality_V2.blend](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Source/Ranger_NPC_AnimationQuality_V2.blend). Erneut erfolgreich geöffnet. Drei gepackte **2048×2048**-Texturen, ein Materialslot, ursprüngliche UVMap. Keine neuen Texturen oder Gesichts-/Material-Neugestaltung. High-Poly-Referenz mit 2.337.180 Dreiecken bleibt im neuen File erhalten. Alle bestehenden Quelldateien bleiben unberührt.

| Arbeitsgeometrie | Vertices Blender | Dreiecke | Zweck |
|---|---:|---:|---|
| 90k | 44.390 | 90.000 | Vergleichsgeometrie im neuen Arbeitsfile; ebenfalls auf neues Arbeitsrig gewichtet |
| LOD0 | 26.890 | 55.000 | Neuer Runtime-Kandidat |
| LOD1 | 11.390 | 24.000 | Neuer Runtime-Kandidat |

Die Geometriekoordinaten der drei Arbeitsmeshes sind vor/nach diesem Pass hashgleich. Keine neue Decimation oder Retopologie; die vorhandenen Kandidaten wurden in Blender und Unreal verglichen. Der alte verworfene 10k-Versuch bleibt als versteckte Referenz im geladenen Arbeitsbestand, wird **nicht** als Runtime-LOD exportiert/importiert.

Rest-Bounds-Höhe LOD0 **1,800297 m**, LOD1 **1,800949 m**. Das sind gemessene Mesh-Bounds, keine neue Skalierung des Rangers auf Playerhöhe. Körper-/Ausrüstungsproportionen und Objektmaßstab bleiben erhalten.

Rig: **24 → 26 Blender-Bones**, in Unreal **25 → 27** einschließlich importiertem Armature-Root. Neue seitliche Mantel-Bones `cape_l`/`cape_r`. Fuß-/Kniegelenke des neuen Arbeitsrigs an die tatsächlich breitere Stiefelstellung angepasst; eigenständiges neues Skeleton statt Überschreiben der V1-Bindepose. Ketten: root → pelvis → spine → chest → neck → head; clavicle/upperarm/lowerarm/hand je Seite; thigh/shin/foot je Seite; cape_upper → cape_lower/cape_l/cape_r; bag an pelvis; back_sword an chest. Vollständige Hierarchie und Restpositionen stehen im [BlenderAnimationAudit.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/BlenderAnimationAudit.json). Keine Finger-/Zehen-/IK-Steuerbones hinzugefügt.

Diagnose: alte Becken- und Taschen-Bones besaßen praktisch keine Gewichte. Ärmelregionen erfassten auch hintere Mantelflächen; dies erzeugte bereits in V1 verzogene Schulter-/Mantelstücke. Neue Masken unterscheiden vordere Ärmel und hinteren Mantel. Becken-/Knie-/Knöchelübergänge, Mantelzonen und begrenzte Hüfttaschenregion neu gewichtet, Schwertbefestigung ausgenommen. Beim 55k-Mesh 26.566 Vertices neu zugeordnet, darunter 9.187 Mantel- und 240 Taschen-Regionsvertices. Die räumliche Einteilung ist **keine saubere modulare Trennung** des fusionierten Meshy-Modells.

Blender „Preserve Volume“ für Arbeitsmeshes deaktiviert, damit die Prüfposen dem linearen Unreal-Skinning entsprechen. Gewichtsummen ungefähr 0,99999996–1,00000005, keine nicht-endlichen Koordinaten. **515 Aktionsframes pro LOD** erneut ausgewertet. LOD0-Minimum über sämtliche Clips ca. +0,5 mm; LOD1-Minimum ca. −0,64 mm relativ zur Blender-Ebene. Kein mathematischer Nullpenetrationsnachweis für LOD1, keine Terrain-IK. Die bestehende World-Fußbasis wurde nicht verschoben. [BlenderReopened.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/BlenderReopened.json).

## 4. Animationen und Sekundärbewegung

| Clip | Dauer | Frames bei 60 Hz | Inhalt |
|---|---:|---:|---|
| Idle | 3,0 s | 181 | Dezente Atmung, ruhiger Kopf |
| Walk | 0,9 s | 55 | Abwechselnde Schritte, analytisch gelöste Knie-/Fußziele, Armschwung, Becken-/Rumpfgegenbewegung |
| Talk | 3,0 s | 181 | Dezente linke Armgestik und Kopfbewegung |
| TurnLeft / TurnRight | je 0,8 s | je 49 | Neutrale Schrittbasis für Actor-Drehungen |

Alle Clips in-place, Root Motion aus. AuthoredWalkSpeed **150 cm/s**; nominales Schrittpaar **1,35 m**. Dies ist Animations-/Previewmaß, keine Änderung der Gameplaygeschwindigkeit eines bestehenden NPCs. Die Spieler-210-cm/s wurden nicht übernommen. Die beiden Turn-Dateien enthalten derzeit dieselbe neutrale Schrittbasis; die Drehrichtung kommt aus dem Actor-Yaw. Sie sind **keine handanimierten eigenständigen Links-/Rechts-Pivotclips**.

Walk enthält etwa 9° Armschwung, leichte Becken-/Rumpfrotation und geringe zyklische Höhenbewegung. Sohlen werden an tatsächlich deformierter Blendergeometrie kontrolliert. Start/Stop werden über **0,22 s** geblendet, Talk über **0,18 s**; keine separaten handanimierten Start-/Stop-Clips. Walkphase bleibt beim Anhalten erhalten, Wiedergabe skaliert mit tatsächlicher Geschwindigkeit. Richtungssteuerung dreht ausschließlich die Darstellung, begrenzt auf 180°/s; im Stillstand bleibt die letzte Richtung.

Kleine gebackene Mantel-/Taschenbewegung plus gedämpfte, begrenzte native Bone-Federn für Geschwindigkeit, Beschleunigung und Yaw-Geschwindigkeit. Maximal 6° Cape-Pitch, 5° Cape-Swing und 4° Bag-Swing, begrenzte Substeps bei Hitches. Kein Echtzeit-Cloth, kein neuer Physics Asset oder Gameplay-Collider. Hintere Taschen, Riemen und Mantelfalten sind geometrisch verbunden; ihre Gewichtung ist noch nicht überall ausreichend getrennt.

## 5. Unreal-Integration und Wiederverwendbarkeit

Neue Assets ausschließlich unter **`/Game/Characters/NPCs/RangerMotionV2/`**: `Meshes/SK_Ranger_AQV2`, `Meshes/SK_Ranger_AQV2_Skeleton` und `Animations/A_Ranger_{Idle,Walk,Talk,TurnLeft,TurnRight}_AQV2`. Bestehendes `MI_Ranger_V1` und dessen Texturen geteilt. Keine doppelten Materialien/Texturen. Mesh-/LOD-Erstimport und tatsächlicher Custom-LOD-Reimport konsistent über Legacy FBX; `Interchange.FeatureFlags.Import.FBX` danach zurückgestellt. Keine neuen Ranger-Tangenten-/Bindepose-Warnungen im finalen Import festgestellt. [UnrealImport.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/UnrealImport.json).

Vorhandene `PokeMonsterNPCVisualActor`-/`PokeMonsterNPCAnimInstance`-Darstellung erweitert: konfigurierbare Clips, AuthoredWalkSpeed, Facing-Offset, Blendzeit und Zubehör-Bonenamen. Bewegung wird nur gelesen, niemals am Gameplay-Source erzeugt. Source-Velocity hat Vorrang; Transform-Fallback nutzt Spielzeit statt ungeprüfter Animations-Delta-Zeit. Relocation-/Hitch-Sprünge werden nicht als normales Gehen behandelt. Unterschiedliche Skeletons benötigen passend importierte eigene Clips; kein automatisches Retargeting allein aufgrund gleicher Namen.

Legacy-Darstellungen ohne Motion-Opt-in behalten Idle/Talk und Sprite-Fallback. OnlyTickPoseWhenRendered und Update-Rate-Optimierung bleiben erhalten. Kein permanenter neuer Actor-Tick für stationäre NPCs; die bestehende kurze Gesprächsdrehung verwendet weiterhin ihren bisherigen Tick. Kein neuer Animation Blueprint nötig: vorhandener nativer Animationsproxy bleibt zuständig.

Der zusätzliche Preview-Source ist ein Development-Prüfwerkzeug ohne AI, Dialog, Quest, Collision oder Tick. Seine explizite Bewegung ist auf NPCMotionV2 begrenzt. Er meldet wie ein Movement-Controller die zur Trajektorie passende Geschwindigkeit. Das war nötig, weil Slate-Screenshot-Hänger eine rein nachträglich aus Transform/Delta errechnete Geschwindigkeit verfälschten. **Preview ist keine Navigation-/AI-Abnahme.** Frühere Fehlversuche sind als Diagnose erhalten und nicht als erfolgreiche Läufe gezählt.

## 6. Bewegungs- und Sichtprüfung

Finaler Lauf mit Screenshots plus zusätzlicher vollständiger Lauf **ohne Screenshot-Stalls**. Acht Weltbewegungsrichtungen, gerade/diagonal, Start, abruptes Stoppen, Richtungswechsel, 90°-/180°-Drehung und Idle danach. In allen acht stationären Laufabschnitten meldet die finale Controller-Probe **150,0 cm/s**. Langsame Drehung aktiviert Turn-Blend; bei 45°/s etwa 0,5, bei 90°/s etwa 1,0. Nach Stillstand wieder Idle. [MotionValidation.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/MotionValidation.json).

Automatischer LOD-Wechsel tatsächlich während Bewegung und bei gerenderter Figur beobachtet: LOD0 → LOD1 bei **34,74 m**, zurück bei **32,70 m** Kamera-NPC-Abstand. ScreenSize **1,0 / 0,22**, Hysterese **0,01**. Keine verbindlichen Metergrenzen: Pose, Bounds, Ansicht und Engine-LOD-Berechnung beeinflussen sie. Frühere 0,18-Versuche erreichten keinen Wechsel; 0,26 war am Ausgangspunkt schon LOD1. Finale Wahl nach tatsächlicher Kontrolle, kein ungeprüftes Übernehmen des früheren 0,12-Werts.

Native Renderdaten: LOD0 **55.000 Dreiecke / 52.476 Rendervertices**, LOD1 **24.000 / 27.390**, jeweils 27 Skeleton-Bones. Split-Rendervertices sind nicht die Blender-Vertexzahl. In der Messmatrix verwendete V2 bei Standard-PIE LOD1, in den übrigen protokollierten Konfigurationen überwiegend LOD0; exakte Segmentwerte im BenchmarkSettings-Audit. Kein identisches LOD-Verhalten zwischen PIE und Standalone behauptet.

Echte QHD-Spielkamera-Bilder: Idle front/seitlich, acht Laufrichtungen, Waldstandort, Gespräch und Mantel-/Ausrüstungssicht. Zusätzlich 16 pausierte Walk-Kontrollposen beider LODs ohne Änderung der Renderqualität. Statische Vergleiche verwenden identische Kamera und eingefrorene Idle-Zeit 0,25 s. Pausierte Walk-Bilder sind keine Laufaufnahme.

### Echte Unreal-Bildnachweise

Die folgenden Layouts sind ausschließlich beschriftete Ausschnitte echter 2560×1440-Unreal-PNGs. Keine generierten Konzeptbilder, keine Farb-/Materialretusche. Originale und Kamerametadaten bleiben erhalten.

![Unreal – scharfe Walk-Kontrollposen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Unreal/SharpWalk_Positions.jpg)

![Unreal – V1 / V2 LOD0 / V2 LOD1](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Unreal/V1_V2_LODs_Comparison.jpg)

![Unreal – Bewegungsbildfolge](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Unreal/GameplayMotion_Sequence.gif)

Die Bildfolge enthält **37 tatsächliche Screenshots** über ungefähr 15 s Spielzeit. Angezeigte Zeitabstände stammen aus der Spielzeit; der Ausschnitt folgt zur Beurteilung der Figur. Kamera selbst unverändert. Screenshot-Readback und vorhandenes Motion Blur begrenzen die zeitliche Schärfe. **Keine flüssige 30-/60-fps-Videoabnahme behauptet.** Der zusätzliche ungestörte Bewegungsprüflauf ist im JSON protokolliert.

Weitere Nachweise: [EightDirections_ContactSheet.jpg](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Unreal/EightDirections_ContactSheet.jpg), [CaptureResolvedPaths.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/CaptureResolvedPaths.json), [SharpPoses.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/SharpPoses.json). Vollständige PNGs in `Unreal/FinalMotion`, `Unreal/FinalSequence`, `Unreal/SharpPoses` und `UnrealComparison`. Blender-Nahaufnahmen in `Blender/` sind nur ergänzend und kein Ersatz für Unreal-Bilder.

## 7. Gameplay, Build und Tests

**Vollständiger Fußlauf bestanden: 266.21 m, 104 protokollierte Schritte, 179.75 s Spielzeit.** Bestehendes Enhanced Input, keine Test-Teleports. Heilhaustransfers sind reale bestehende Relocation, Save/Load ist reales Laden; nicht als manuelle Wegpositionierung ausgegeben.

- Wanderer → Gespräch/Queststart/Talk-Blend → Wild-Abzweigung/Kampf/Fangen → Liora/Sieg → Archivstein/Save-Load/Abschlussflag → Wanderer-Abschlussdialog.
- Dorf → Heilhaus gerade hinein → Heilerin/HP-/PP-Heilung/Checkpoint/Save → hinaus → diagonal hinein/hinaus → Wald und Kronenfreistellung → Rückweg.
- Acht Playerbewegungsrichtungen, Menü/Dialogsperren, normale 210 cm/s und Sprint-Hold über vorhandene Enhanced-Input-Action mit **315 cm/s**, nach Loslassen wieder 210. Kein physischer Controller geprüft.
- Save/Load kontrolliert innerhalb derselben PIE-Sitzung: Trainerstatus temporär zurückgesetzt und durch echten Load wiederhergestellt, HP/PP erhalten. **Kein zusätzlicher Prozessneustart-Save-Test.** Dev-Slot danach bytegleich restauriert.
- Zusätzlich gezieltes Anlaufen der NPC-Capsule: Stopp bei **62,116 cm** gegenüber Radius-Summe **62,0 cm**. Dialog sperrt tatsächlichen Bewegungsinput; TalkAlpha 1,0; Rückkehr zu Idle. Sprite-Fallback sichtbar, 3D ausgeblendet, ursprüngliche Collision blockiert weiter bei 62,114 cm; anschließend 3D wiederhergestellt. Source-Transform und Dev-Save unverändert. [NPCInteractionRegression.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/NPCInteractionRegression.json).

**Mac Development Editor Build erfolgreich** (final `Build_PreviewSource.log`, 15,23 s). Ein früher Buildfehler wegen Float/Double-Mehrdeutigkeit im neuen Test wurde korrigiert; nicht als erfolgreicher Build gezählt. [Build.log](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/Build.log).

**Vollständige Projekt-Automation: 47/47 erfolgreich**, 0 fehlgeschlagen, 0 nicht ausgeführt, 0 mit zugeordneten Warnungen. Vorher 46, neu `PokeMonster.NPC.MotionV2.IsolationSpeedAndSkeleton`: Source-Isolation, acht Richtungen/150 cm/s, Stop/letzte Richtung, Relocation-Ausschluss, Clip-/Skeleton-Kompatibilität, Root-Motion aus und Fallback. [AutomationSummary.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/AutomationSummary.json).

**Map Check: 0 Fehler / 0 Warnungen**, vor und nach finaler Bildprüfung. Editor abschließend ohne dirty Map-/Content-Pakete auf NPCMotionV2, keine laufende PIE oder Prüfwarteschlange. [FinalEditorState.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/FinalEditorState.json).

Engine-Sitzungen sind nicht warnungsfrei: 17 generische `LogAutomationTest: Error: Condition failed` bei Frame 0 vor den Projektprüfungen, bekannte `idevice_id`/Bad-CPU-type-Startwarnungen, MCP-Lizenzhinweis und ein nicht gebundener MCP-Port 8000 im Automationprozess. Der eigentliche Editor nutzt 8005. Diese Meldungen wurden nicht unterdrückt; alle 47 strukturierten Projekttests stehen auf Success. Vollständige Warning-/Error-Zeilen pro Sitzung: [Warnings.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/Warnings.json).

## 8. Performance – Methode und Grenzen

Gleicher NPC-Vorplatz/Wegrand in derselben VisualV2-Kopie: Player **−760 / −1410 / 50,15 cm**, Kamera **−2055,3805 / −114,6195 / 2268,3767 cm**, −50°/−45°/35°. Das ist kein allgemeiner Dorf-/Wald-/Wegvergleich der ganzen Karte. Beide Zustände im selben Build: V1-Mesh/Idle/Talk versus V2-Mesh/neue Idle/Talk plus Zubehörfunktion. Normaler Idle ohne Gespräch/Patrouille, über mehrere Zyklen laufend; keine exakte Phasenfixierung während Timing. Der separate Lauf-/Drehprüfling ist beim Benchmark deaktiviert.

In jedem der zwei Modi sechs Konfigurationen, je **drei benachbarte AB/BA/AB-Paare**, 5 s Warm-up + 8 s Messfenster. Insgesamt **72 vollständig validierte Segmente**, alle zugehörigen Unreal-CSV-Dateien vorhanden. Keine Blender-Renders, Builds oder Bildverarbeitung gleichzeitig mit Timing. Native Standalone ist Development `UnrealEditor -game`, kein paketierter Shipping-Build; der Editor war dabei geschlossen. PIE ausschließlich eingebettet.

Ausgabe/RenderTarget/Renderer-ViewRect, tatsächliche Primary-/Secondary-Faktoren, Fenster/DPI/Fokus und Kamera pro Frame geprüft. Alle ausgewählten Samples mit korrekten Extents/Faktoren und aktivem Fenster. Interne Größen über den tatsächlichen Renderer-Driver und Ceil-Regel, **keine GPU-Allocation-Rücklesung**: 960×555, 1280×740, 1920×1080, 2560×1440. Historische 2331×1346-Werte sind nicht als 1280×740 ausgegeben. [MeasurementValidation.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/MeasurementValidation.json).

Identische ursprüngliche VisualV2-Rendererwerte für beide NPCs, keine EnvironmentPerf-V2/V3-Optimierungen eingeschmuggelt: IntegrateDownsample 1, gerichtete SMRT-RayCount 8, FinalGatherMethod 1, HWRT-CVar 1. Letzteres ist ein CVar-Zustand, kein gesonderter Nachweis des tatsächlich genutzten Hardware-RT-Pfads. Medium/High als vollständige Scalability-Stufen; kein Qualitätswechsel im laufenden PIE.

r.VSync=0, t.MaxFPS=0, Dynamic Resolution aus, Secondary 100 während Timing. rhi.SyncInterval=1; native Fensterpräsentation/Display-Pacing nicht separat per Present-Telemetrie gemessen. FPS unten = 1000/Median der realen Frame-Loop-Zeit, **keine Monitor-Hz-Messung**. Medianbasierte native Werte über 60 sind kein Beweis einer entsprechend hohen Präsentationsfrequenz. RenderThread in PIE nahezu Null/nicht belastbar; native RenderThread-Zeit enthält Wartezeit. RHI-/DrawCall-Zähler lieferten Null und sind n/v, nicht „0 Draw Calls“. GPU-Pässe sind weltweite, teils überlappende Werte und keine isolierten NPC-Materialkosten.

Thermik/Energie: 133 Abfragen, Zustände {'fair': 128, 'nominal': 5}, durchgehend Netzbetrieb. Klassifizierung, keine Temperatur-/Taktmessung. Die offene, ungesicherte Blender-Sitzung und fremde Anwendungen wurden nicht beendet. Hintergrundlast/thermische Drift nicht vollständig isolierbar; benachbarte Paare und vertauschte Reihenfolge sind deshalb wichtiger als isolierte Tabellenmediane.

Tabellen: Median der drei Laufmediane, P95 = Median der drei Lauf-P95. Die letzte Spalte ist der Median der **drei gepaarten Differenzen**, nicht zwingend die Differenz der separat gebildeten Mediane. Keine Signifikanz- oder FPS-Garantie.

| Modus | Ausgabe / Qualität / SP | FPS V1 → V2 | Median ms V1 → V2 | P95 ms V1 → V2 | GPU ms V1 → V2 | Game ms V1 → V2 | Render ms V1 → V2 | Median Paar-Δ ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| PIE | 1280×740 / Medium / 75 % | 45.48 → 45.11 | 21.99 → 22.17 | 24.29 → 24.33 | 21.54 → 21.59 | 8.12 → 8.05 | n/v | -0.392 |
| PIE | 1280×740 / Medium / 100 % | 35.16 → 35.13 | 28.44 → 28.46 | 30.69 → 30.90 | 27.77 → 27.74 | 6.27 → 6.25 | n/v | -0.050 |
| PIE | 2560×1440 / Medium / 75 % | 21.36 → 21.58 | 46.81 → 46.34 | 49.24 → 48.91 | 46.07 → 45.71 | 6.60 → 6.66 | n/v | -0.545 |
| PIE | 2560×1440 / Medium / 100 % | 14.71 → 14.83 | 67.98 → 67.44 | 70.54 → 71.67 | 67.24 → 66.78 | 7.67 → 7.90 | n/v | -0.486 |
| PIE | 2560×1440 / High / 75 % | 21.88 → 22.03 | 45.70 → 45.39 | 48.20 → 51.04 | 44.33 → 44.37 | 6.95 → 6.89 | n/v | +0.140 |
| PIE | 2560×1440 / High / 100 % | 15.59 → 15.80 | 64.14 → 63.29 | 68.10 → 65.69 | 61.87 → 61.50 | 7.87 → 7.82 | n/v | -0.848 |
| Standalone | 1280×740 / Medium / 75 % | 64.44 → 67.35 | 15.52 → 14.85 | 16.82 → 16.20 | 14.75 → 14.14 | 1.15 → 1.07 | 15.52 → 14.86 | +0.019 |
| Standalone | 1280×740 / Medium / 100 % | 41.57 → 42.43 | 24.06 → 23.57 | 26.34 → 25.54 | 23.26 → 22.80 | 1.34 → 1.27 | 24.04 → 23.56 | -0.357 |
| Standalone | 2560×1440 / Medium / 75 % | 24.11 → 24.24 | 41.47 → 41.26 | 43.73 → 44.54 | 40.73 → 40.71 | 1.56 → 1.56 | 41.46 → 41.29 | -0.406 |
| Standalone | 2560×1440 / Medium / 100 % | 15.76 → 15.87 | 63.46 → 63.02 | 70.63 → 68.22 | 62.65 → 62.12 | 2.00 → 1.98 | 63.45 → 62.99 | -0.441 |
| Standalone | 2560×1440 / High / 75 % | 25.35 → 25.65 | 39.45 → 38.99 | 42.04 → 41.54 | 37.67 → 37.38 | 1.76 → 1.73 | 39.40 → 38.98 | -0.544 |
| Standalone | 2560×1440 / High / 100 % | 16.81 → 16.77 | 59.48 → 59.64 | 63.95 → 66.64 | 57.27 → 57.80 | 2.18 → 2.12 | 59.49 → 59.85 | -0.087 |

**Bewertung:** Die NPC-Änderung liefert keinen großen QHD-FPS-Sprung. Die meisten gepaarten Median-Differenzen liegen im Bereich weniger Zehntelmillisekunden; einzelne Paare und Konfigurationen werden langsamer, P95 verbessert sich nicht durchgehend. Selbst High/QHD/100 bleibt nativ ungefähr bei 16,8 medianbasierten FPS. GPU-/Renderzeit deutlich höher als Game-Thread; die umfassende Weltlast bleibt bestehen. Aus dem Geometrieabbau wird kein pauschaler Animations-/Materialgewinn abgeleitet. Keine isolierte quantitative Aussage zu Walk-/Talk-CPU-Kosten vieler NPCs: diese Matrix misst einen animierten Idle-NPC.

Alle Einzelmediane, P95, Streuungen, GPU-Pässe und Auflösungen: [Measurements.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/Measurements.json). Gepaarte Differenzen: [PerformanceTable.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/PerformanceTable.json). Vollständige native Frame-/Profiler-CSV plus Pläneinstellungen: [RawMeasurements.zip](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/RawMeasurements.zip). Material: weiterhin ein Slot und drei geteilte 2K-Texturen, keine neue Shaderfamilie; pro Material isolierte GPU-/VRAM-Kosten nicht zuverlässig gemessen.

## 9. Künstlerische Bewertung und offene Punkte

Sichtbarer Fortschritt: echte alternierende Bein-/Fußposen statt stationärer Darstellung; ruhigere, besser zusammenhängende Schulter-/Mantelpartie; Becken-/Armschwung und konfigurierbare Sekundärbewegung. Beide importierten LODs behalten aus der normalen Spielkamera eine weitgehend vergleichbare Silhouette. Keine großen Importfehlposen oder fehlenden Gliedmaßen in den kontrollierten Ansichten.

**Noch nicht als fertiger Referenz-NPC freigeben:**

1. Mantel, hintere Taschen, Gurte und Ausrüstung bleiben fusioniert. Die neue Gewichtung vermindert grobe Fehlzuordnungen, garantiert aber keine Durchdringungsfreiheit; einzelne Gurte/Flächen benötigen manuelles Weight Painting und gegebenenfalls lokale Trennung. Kein Körper-/Mantel-Kollisionssystem.
2. Turn-Clips sind gemeinsame prozedurale Schrittbasis. Handgesetzte Pivotkontakte fehlen. Die bestehende Gesprächsdrehung dreht den Actor mit vollem Talk-Poseblend; Füße sind dabei nicht verriegelt. Hier kann weiterhin Rutschen auftreten.
3. Start/Stop nutzt Blends statt speziell animierter Kontaktphasen. Kein vollständiges Foot-Locking, keine Terrain-/Slope-IK. Fußrollen nur über den bestehenden Fußbone; keine zusätzliche Ballen-/Zehenartikulation.
4. Keine Finger-/Lippenanimation. Talk verbessert Kopf/Arm, macht das vorhandene Scan-Rig aber nicht zum vollständigen Gesten-/Gesichtsrig.
5. Vorhandenes Motion Blur verschmiert schnell bewegte Konturen. 37 Screenshotframes ersetzen keine flüssige Echtzeit-Videoabnahme; zeitliche Kleinstfehler bleiben offen. Die scharfen angehaltenen Posensheets prüfen Form/Import, nicht kontinuierliche Fußkontakte.
6. In tiefem Waldschatten bleibt die dunkle Kleidung teilweise schwer lesbar. Das bestehende Kronen-Reveal zielt auf den Player, nicht pauschal auf NPCs; ein NPC außerhalb dieses Sichtkegels kann weiterhin verdeckt sein. Kein Eingriff in Kamera, Baumfamilien oder Materialien.
7. LOD-Wechsel einmal hin/zurück plus erzwungene Posevergleiche tatsächlich geprüft. Keine pauschale Garantie gegen jedes temporale Schatten-/LOD-Popping in allen Spielsituationen.

Die größtmögliche Verbesserung durch kontrolliertes automatisches Rigging ist nicht gleichbedeutend mit fertig handanimierter Qualität. Keine Umgestaltung des Originals durch zusätzliche Primitive, keine neue Frisur/Retopologie und keine pauschale Materialaufhellung zum Kaschieren der Grenzen.

## 10. Wiederverwendbarer Workflow

### Ablauf

Dieser Ablauf beschreibt einen Prüfprozess, keine automatische Art-Freigabe.

1. **GLB erfassen:** genaue Eingangsdatei und SHA sichern; Maße, UVs, Materialslots, Texturauflösungen, Inseln, Normalen und Defekte ermitteln. Original nicht bearbeiten.
2. **High-Poly erhalten:** separate Referenzcollection und unabhängige Blenderdatei, Texturen packen. Änderungen ausschließlich an Arbeitskopien.
3. **Runtime vorbereiten:** vorhandene reduzierte Kandidaten aus Nah- und Spielkamera prüfen. Kopf/Hände/Silhouette schützen. Keine globale Reduktion als Retopologie oder Animationsnachweis ausgeben. Mehrere LODs nur nach Prüfung der jeweiligen Schäden.
4. **Rig anpassen:** eigene anatomische Gelenkmarken. Humaner Ranger ist ca. 1,80 m; Spieler 1,40 m ist keine Rig-Schablone für sämtliche Wesen. Zwerge benötigen kürzere Beine/breiteren Rumpf und andere Gelenkpositionen, Elben längere Proportionen. Namen/Hauptketten können kompatibel bleiben, Bindepose und Knochenlängen nicht ungeprüft übernehmen. Eigenes Skeleton bei veränderter Bindepose verwenden; Retargeting gesondert prüfen.
5. **Gewichte korrigieren:** volle Ärmelquerschnitte, Schulter-/Ellbogenübergänge, Becken/Schritt/Knie und Fußsohlen. Mantel nicht als Arme oder Beine klassifizieren. Bei verbundenen Meshy-Flächen sind räumliche Masken nur ein kontrollierter Anfang; Nahaufnahmen, Rückseite und vollständige Bewegungszyklen entscheiden. Ausrüstung und Riemen getrennt beurteilen.
6. **Idle/Walk/Talk:** eigene in-place Aktionen. Geschwindigkeit und Zyklusdauer dokumentieren. Ranger-Kandidat: 150 cm/s, 0,9-s-Zyklus, 1,35-m-Schrittpaar; nominale Standphase 0,45 s/Bein. IK-berechnete Zielposen in Blender backen; tatsächliche deformierte Sohlen zusätzlich prüfen. Kein Root Motion. Dezente Atmung und Gesprächsgeste, Handgeste ohne Finger-Rig bleibt eingeschränkt.
7. **Sekundärbewegung:** wenige Mantel-/Taschen-Bones mit sanftem Gewichtsübergang. Kleine gebackene Gangbewegung plus begrenzte gedämpfte Runtime-Federn aus Geschwindigkeit, Beschleunigung und Yaw-Geschwindigkeit. Riemen und Schwertbefestigung stabil halten. Keine teure Cloth-Simulation als Standard.
8. **FBX:** Mesh und LODs mit identischer Armature/Bindepose exportieren. Meter→cm über FBX Scene Units, keine zusätzliche hundertfache Skalierung. Animationsclips getrennt, 60 Hz, keine zusätzlichen Leaf-Bones. Nur ausgewählte Arbeitsmeshes/Rig exportieren.
9. **Unreal importieren:** getrennte Assetpfade; bestehende Materialien/Texturen wiederverwenden. Für diesen geprüften UE-5.8-Workflow Legacy FBX für Erstimport, Custom LOD und Reimport konsistent verwenden; Importer-CVar scoped zurückstellen. Skeleton-/Bindepose-Warnungen ernst nehmen. Keine neuen Gameplay-Collider.
10. **Präsentation verbinden:** SourceActor behält Identität, Dialog, Quest, Collision und Bewegung. Visualactor erhält eigene Idle/Walk/Talk/Turn-Clips, AuthoredWalkSpeed und konfigurierte Zubehör-Bonenamen. Geschwindigkeit aus Source-Velocity bzw. tatsächlicher Transformänderung pro Spielzeit; letzte Blickrichtung im Stillstand erhalten. Bewegung bleibt beim bestehenden Gameplay-/Testcontroller. Legacy-NPCs behalten ohne Opt-in ihren bisherigen Idle/Talk-Ablauf.
11. **LOD/Performance:** tatsächliche Renderdreiecke/Bones und automatische LOD-Umschaltungen messen. Erzwungene LOD-Bilder ersetzen keinen natürlichen Wechsel. OnlyTickPoseWhenRendered/URO weiterverwenden; keine zusätzlichen permanenten Actor-Ticks. Benchmarks getrennt PIE/Standalone, gleiche Auflösung/ScreenPercentage/Licht/Kamera, drei AB/BA-Paare. CPU-/GPU-Zähler und Messgrenzen offenlegen.
12. **Abnahme:** komplette Zyklen, Start/Stop, acht Richtungen, 90°/180°, Gespräche, Mantel/Schwert/Riemen, Schatten, Fallback und Gameplay mit echtem Input prüfen. Spielstand vorher sichern und nach Tests unter Hash-Kontrolle restaurieren. Künstlerische Freigabe durch Harry bleibt gesondert.

Nicht humanoide Figuren wie Ents benötigen eigene Stamm-/Ast-/Wurzel-Rigs und einen separaten Qualitätsnachweis. Fusionierte Reiter, Kleider und lange Bärte dürfen nicht pauschal nach einem Menschen-Rig gewichtet werden.


## 11. Dateien und Reproduzierbarkeit

Wesentliche neue Produktions-/Testdateien:

- `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_AnimationQuality_V2.blend`
- `Art/Characters/NPCs/Ranger/Exports/AnimationV2/`: zwei Mesh-/LOD-FBX und fünf Animations-FBX.
- `Content/Characters/NPCs/RangerMotionV2/`: ein Skeletal Mesh, ein Skeleton, fünf Animation Sequences.
- `Content/Maps/Dev_TestMap_NPCMotionV2.umap`.
- `Source/PokeMonster/Development/PokeMonsterNPCMotionPerformanceProbe.cpp`.
- `Source/PokeMonster/Development/PokeMonsterNPCMotionPreviewSource.h` und `.cpp`.
- `Source/PokeMonster/Tests/PokeMonsterNPCMotionV2Test.cpp`.
- `Tools/RangerAnimationV2/`: reproduzierbare Blender-/Import-/Prüf-/Messskripte, Pläne und Workflow.
- Dieser Bericht und `Art/Characters/NPCs/Ranger/Review/AnimationV2/` mit tatsächlichen Bildern und Prüf-/Messdaten.

Gezielt erweiterte bestehende Dateien (alle waren schon unversioniert): `Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h/.cpp`, `PokeMonsterNPCAnimInstance.h/.cpp`. Präziser Vorher-/Nachher-Patch gegen den offenen Anfangsstand: [NPCPresentationChanges.patch](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/NPCPresentationChanges.patch).

Die **vollständige, exakte Dateiliste** aller neuen auftragsbezogenen Dateien und sämtlicher bestehenden Änderungen steht in [ScopeAndFiles.json](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/ScopeAndFiles.json). Review-/Diagnosebilder sind Arbeitsnachweise, keine zusätzlichen Gameplay-Assets. Unvollständige erste Capture-/Weight-Versuche bleiben als Diagnose erhalten und sind nicht die finale Freigabegrundlage. Temporäre Original-/Test-Save-Kopien, Build-/Editorlogs und Rohdateien verbleiben unter `Saved/RangerAnimationV2/`.

## 12. Empfehlung und Git-Abschluss

**V2 im separaten NPCMotionV2 prüfen; noch nicht automatisch nach VisualV2 übernehmen.** Nächste sinnvolle Qualitätsschritte sind manuelle Mantel-/Gurt-/Taschengewichte und gezielte Start-/Stop-/Drehkontakte einschließlich Gesprächsdrehung, danach flüssige Spielkamera-Aufnahme. Der technische Wiederverwendungsrahmen und die Regressionstests stehen; die noch sichtbaren Animationsgrenzen werden nicht durch 47 grüne Tests aufgehoben.

Kein Staging, kein Commit, kein Push; keine Löschung/Reset/Restore bestehender Projektdateien. `git diff --check` und Abschlussstatus werden nach dem Schreiben dieses Berichts im separaten Git-Abschlussnachweis erfasst: [GitFinal.txt](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/GitFinal.txt).

### Vollständiger abschließender Status

```text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Dialogue/PokeMonsterDialogueSubsystem.h
 M Source/PokeMonster/PokeMonster.Build.cs
?? Art/Characters/MiniHobbit/
?? Art/Characters/NPCs/CrouchedCreature/
?? Art/Characters/NPCs/DarkArmored/
?? Art/Characters/NPCs/DwarfWarrior/
?? Art/Characters/NPCs/ElvenArcher/
?? Art/Characters/NPCs/ElvenScholar/
?? Art/Characters/NPCs/Incoming/
?? Art/Characters/NPCs/IntegrationV1/
?? Art/Characters/NPCs/Ranger/
?? Art/Characters/NPCs/SilverLady/
?? Art/Characters/NPCs/TreeBeing/
?? Art/Characters/NPCs/WhiteHairedWarrior/
?? Art/Characters/NPCs/Wizard/
?? Art/World/EnvironmentPerfV1/
?? Art/World/EnvironmentPerfV2/
?? Art/World/EnvironmentPerfV3/
?? Art/World/TreeShadowProxyV1/
?? Content/Characters/NPCs/
?? Content/Environment/TreeShadowProxyV1/
?? Content/Maps/Dev_TestMap_EnvironmentPerfV1.umap
?? Content/Maps/Dev_TestMap_EnvironmentPerfV2.umap
?? Content/Maps/Dev_TestMap_EnvironmentPerfV3.umap
?? Content/Maps/Dev_TestMap_NPCMotionV2.umap
?? Content/Maps/Dev_TestMap_RangerPerfV2.umap
?? Content/Maps/Dev_TestMap_TreeShadowProxyV1.umap
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V1_PRUEFBERICHT.md
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V2_PRUEFBERICHT.md
?? Docs/DEV_TESTMAP_ENVIRONMENT_PERFORMANCE_V3_PRUEFBERICHT.md
?? Docs/MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md
?? Docs/MESHY_RANGER_ANIMATION_QUALITY_V2_PRUEFBERICHT.md
?? Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCAnimInstance.h
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.cpp
?? Source/PokeMonster/Characters/PokeMonsterNPCVisualActor.h
?? Source/PokeMonster/Development/
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV2Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentProfileV3Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterEnvironmentRenderProfileTest.cpp
?? Source/PokeMonster/Tests/PokeMonsterNPCMotionV2Test.cpp
?? Source/PokeMonster/Tests/PokeMonsterNPCPresentationTest.cpp
?? Tools/EnvironmentPerfV1/
?? Tools/EnvironmentPerfV2/
?? Tools/EnvironmentPerfV3/
?? Tools/MeshyNPCIntegrationV1/
?? Tools/PerformanceRangerV2/
?? Tools/RangerAnimationV2/
?? Tools/TreeShadowProxyV1/
```
