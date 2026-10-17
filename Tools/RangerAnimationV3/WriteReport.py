# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
# -*- coding: utf-8 -*-
"""Final report from measured evidence. Never fills missing tests with success."""
import json,hashlib,subprocess,statistics,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV3';O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3';D=O/'Data'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
assert (S/'PerformanceComplete.txt').exists()
perf=read(D/'PerformanceTable.json');validation=read(D/'MeasurementValidation.json');assert not validation['issues']
foot=read(S/'FootTest/FootTest.json');interaction=read(D/'NPCInteractionRegression.json');assert foot['passed'] and interaction['passed']
reopen=read(D/'BlenderReopened.json');capture=read(D/'RecordingClearAudit.json');motion=read(D/'RecordedMotionClear.json')
automation=read(S/'AutomationFinal/index.json');assert automation['failed']==0 and automation['notRun']==0
protection=read(D/'ScopeAndFiles.json');assert not protection['modified_existing'] and not protection['missing_existing']
head=(S/'Head.txt').read_text().strip();git=(S/'GitFinal.txt').read_text();mapaudit=read(S/'FinalMapAudit.json')
def link(p,label=None):return '['+(label or p.name)+']('+str(p)+')'
lines=[
'# PokeMonster – Wanderer Animation Quality V3',
'',
'Stand: 16.10.2026. **Beinmechanik korrigiert, isolierter V3-Arbeitskandidat getestet. Noch keine Freigabe als vollständig ausgearbeiteter Referenz-NPC. Keine Übernahme in VisualV2.**',
'',
'## 1. Ausgangslage und Schutz',
'',
f'HEAD: `{head}`. Bereits umfangreich veränderter Arbeitsbaum. Alle vorhandenen Arbeiten wurden als Ausgangsbestand behandelt; kein Staging, Commit, Push, Reset, Restore oder Löschen.',
'AGENTS sowie relevante Abschnitte aus TECHNIK, ENTSCHEIDUNGEN, GRAFIKSTIL, SPIELIDEE, SPIELREGELN und den NPC-/Ranger-/Environment-Prüfberichten gelesen. Offener Editor: NPCMotionV2, kein PIE, keine ungespeicherten Map-/Content-Pakete. Kein Save All oder Discard All. Die vorhandene Blender-Sitzung wurde nicht ersetzt; Modellarbeit in separaten Blender-Hintergrundprozessen.',
f"{protection['protected_count']} bestehende versionierte/unversionierte Dateien abschließend bytegleich; keine fehlt. Dazu gehören V2-Blenderquelle und -Animationen, Incoming, Spieler, sämtliche vorherigen Karten und die bereits offenen C++-/Dokumentationsänderungen. Hashnachweis: {link(D/'ScopeAndFiles.json')}. Ignorierte Build-/Log-/Cachedateien sind kein Bestandteil dieser Projektquellenprüfung.",
'',
'## 2. Ursache der fehlerhaften Beine – zuerst untersucht',
'',
'Die FrontQuarter-Pose bei 0,225 s wurde in Blender und Unreal ausgewertet. Hauptfehler im V2-Knielöser: Der verwendete Polvektor zeigt nach **+Y**, obwohl die Figur in Blender nach **−Y** schaut. Die Knie beugen dadurch nach hinten. Zusätzlich hält V2 die Knöchel beim Gehen bei X=±22,5 cm: 45 cm Spurweite. Die geneigte Bindepose verstärkt den breitbeinigen Eindruck.',
'Bei 0,225 s liegt das linke V2-Knie bei Blender Y=+12,71 cm, Hüfte/Fuß dagegen ungefähr −3 cm. V3: linkes Knie Y=−19,38 cm, Hüfte −3,18 cm, Fuß +0,25 cm. Der Unterschied ist eine korrigierte anatomische Beugeebene, nicht nur eine verkürzte Schrittweite.',
'Der FBX-Import ist nicht die Ursache einer Vorwärts-/Seitwärtsvertauschung. Gemessene Abbildung: Unreal (X,Y,Z)=(-Blender Y,-Blender X,Blender Z), mit cm/m-Umrechnung. Blender −Y wird korrekt Unreal +X. Größte Positionsabweichung der verglichenen Gelenke bei 0,225 s: V2 ca. 0,138 cm, V3 ca. 0,073 cm (Sampling/Importkompression eingeschlossen).',
'Restpositionen und Bone-Hierarchie gegenüber V2 unverändert. Lokale Rotationsbasis wird beim Setzen der gelösten Gelenkmatrizen berücksichtigt. Keine pauschale 90°-Korrektur oder willkürliche Fuß-Außenrotation.',
'',
'Belege: '+', '.join(link(D/n) for n in ['V2_AxisDiagnosis.json','V3_AxisDiagnosis.json','V2_Unreal_Axes.json','V3_Unreal_Axes.json'])+'.',
'',
'![Identischer 0,225-s-Vergleich]('+str(O/'Unreal/V2_V3_0225_Comparison.jpg')+')',
'',
'Identische absolute Clipzeit, Spielkamera, NPC-Position, Actor-Yaw und LOD0. Wegen unterschiedlicher Zyklusdauer ist das nicht exakt dieselbe normalisierte Gangphase. Zusätzlich wurden vier Kontrollzeiten beider LODs vorne/hinten aufgenommen; Originalbilder und Kameraaufzeichnungen bleiben erhalten.',
'',
'## 3. Blender, Rig und Animationen',
'',
'Neue, erneut geöffnete Quelle: '+link(R/'Art/Characters/NPCs/Ranger/Source/Ranger_NPC_AnimationQuality_V3.blend')+'. Basis ist die geschützte V2-Animationsquelle. Keine neue Geometrie, Retopologie, Material-, UV- oder Texturänderung.',
'26 Blender-Bones / 27 Unreal-Bones einschließlich Armature-Root; keine Finger- oder Ballen-/Zehenbones. Gepackte drei 2048×2048-Texturen, ein Materialslot. High-Poly-Referenz und frühere Arbeitsmeshes bleiben im unabhängigen File erhalten.',
'',
'| Mesh | Blender-Vertices | Dreiecke | Resthöhe |',
'|---|---:|---:|---:|']
for m in reopen['meshes']:lines.append(f"| {m['name']} | {m['vertices']} | {m['triangles']} | {m['height_m']:.6f} m |")
lines += ['',
'Die Höhen sind Rest-Mesh-Bounds, keine neue Playergröße. V3 senkt das Becken in den gebackenen Posen um etwa 7,8 cm; die Figur wirkt dadurch noch etwas gebeugt. Das ist eine offene künstlerische Schwäche, keine Änderung der Bindepose oder Weltgröße.',
'',
'| Clip | Dauer | Frames 60 Hz | Änderung |',
'|---|---:|---:|---|',
'| Idle | 3 s | 181 | Ruhige Atmung, engerer anatomischer Stand |',
'| Walk | 0,8 s | 49 | Vorderer Kniepol, 29-cm-Knöchelspur, alternierende Stand-/Schwungphasen |',
'| Talk | 3 s | 181 | Zurückhaltende Arm-/Kopfgestik; Lauf-/Drehkontakte bleiben in Unreal erhalten |',
'| TurnLeft / TurnRight | je 1 s | je 61 | Richtungsabhängige kleine Schrittarcs statt identischer V2-Clips |',
'',
'Alle Clips in-place, Root Motion aus. AuthoredWalkSpeed bleibt 150 cm/s: 1,20 m Schrittpaar / 0,8 s. V2: 1,35 m / 0,9 s. Player-210-cm/s und Sprint-315-cm/s wurden nicht übernommen oder verändert. Die Schrittfrequenz ist noch recht zügig; keine handanimierte finale Gangabnahme allein aufgrund des Geschwindigkeitsquotienten.',
'Die erreichbaren Fußziele werden geprüft. Ein erster Versuch wurde wegen eines unerreichbaren Knöchelziels abgefangen und nicht gespeichert; der erzeugte Kandidat verwendet erreichbare Gelenkpositionen. Sohlenkorrektur löst die gesamte Beinkette erneut, statt den Fuß separat vom Schienbein zu verschieben.',
'Tatsächlich erneut geprüft wurden '+str(sum(x['frames_evaluated'] for x in reopen['clips']))+' Frames pro LOD über alle fünf V3-Clips. LOD0-Minimum ca. +0,50 mm; LOD1-Minimum ca. −0,23 mm relativ zur Blender-Ebene. Keine Nullpenetrationsgarantie, keine Gelände-IK. Gewichte normalisiert, keine nicht-endlichen Vertexkoordinaten. '+link(D/'BlenderReopened.json')+'.',
'',
'## 4. V3-spezifische Unreal-Darstellung',
'',
'Neue Karte **/Game/Maps/Dev_TestMap_NPCMotionV3**, über die Editor-SaveMap/LoadMap-API aus NPCMotionV2 kopiert. Nur dort wurde der Darstellungsactor des Wanderers ersetzt. Gameplay-Source, Identität, Dialog, Quest, Position, Capsule und Interaktion sind erhalten. Zwei geerbte deaktivierte V2-Previewactors bleiben bestehen; zwei neue V3-Previewactors sind ebenfalls standardmäßig deaktiviert.',
'Neue Assets unter **/Game/Characters/NPCs/RangerMotionV3/**: eigenes SK_Ranger_AQV3, Skeleton und fünf Animationsclips. Vorhandenes MI_Ranger_V1 und dessen Texturen geteilt. Legacy-FBX konsistent für Mesh, Custom LOD und Reimport; temporäres Importer-Flag anschließend restauriert. Kein neues Gameplay-Collider/Physics Asset.',
'Neue V3-AnimInstance und VisualActor-Unterklasse; bestehende V2-C++-Dateien unverändert. Poseauswertung hält Standfüße in Weltkoordinaten und löst die Beinkette mit einem vorwärts gerichteten Kniepol. Gesprächsblend betrifft den Oberkörper, damit Talk die Beinkontakte nicht überschreibt. Drehschritte können auch während eines Gesprächs aktiv bleiben.',
'Kontaktstabilisierung ist auf flachen Boden begrenzt. Kein Trace pro Frame und keine Änderung des Gameplay-Source. Bei unerreichbaren/starken Änderungen (>25 cm Korrektur) wird ein veralteter Pin verworfen. Diese Schutzgrenze kann sichtbare Kontaktwechsel erzeugen; sie ersetzt keine fertig handanimierten Start-/Stop-/Pivotclips oder Motion Warping.',
'OnlyTickPoseWhenRendered/URO bleiben erhalten. Die vorhandenen kleinen Zubehörfedern sind wiederverwendet; keine Cloth-Simulation. Baked Cape-/Bag-Amplituden reduziert, damit die Bewegung ruhiger bleibt.',
'',
'**Nicht vollständig umgesetzt:** keine neue manuelle Weight-Paint-Bereinigung. Die Gewichte bleiben bewusst V2-identisch; die fusionierten hinteren Taschen, Gurte und Mantelflächen lassen sich nicht zuverlässig allein aus räumlichen Masken trennen. Deshalb keine falsche Behauptung, diese Stellen seien manuell repariert oder durchdringungsfrei. Dies bleibt konkrete Nacharbeit vor Referenzfreigabe.',
'',
'LOD0 55.000 Dreiecke / 52.476 Rendervertices; LOD1 24.000 / 27.390, je 27 Bones. ScreenSize 1 / 0,22, Hysterese 0,01. Automatische Umschaltung im echten gerenderten Bewegungsablauf beobachtet, ungefähr bei 34,69 m hinaus / 32,73 m zurück. Keine allgemeine Garantie gegen jedes LOD-/Schatten-Popping.',
'',
'## 5. Echte Bewegungsaufnahme und visuelle Bewertung',
'',
f"Finale freie Prüfstrecke: **{capture['seconds']:.2f} s, {capture['frame_count']} echte Unreal-Framebufferframes**, durchschnittlich {capture['average_capture_fps']:.2f} erfasste Bilder/s; medianer Abstand {capture['median_interval_s']*1000:.2f} ms, größter Abstand {capture['maximum_interval_s']*1000:.2f} ms. Ausgabe 1280×740. Kein behauptetes 20-/30-/60-FPS-Video. Die tatsächlichen Zeitstempel wurden in H.264/MP4 übernommen; keine künstlich interpolierten Zwischenbilder.",
'Framebuffer-Aufnahme aus eingebettetem PIE, nicht Blender und nicht ein generiertes Konzeptbild. Die macOS-Bildschirmaufnahme war nicht erlaubt; daher eigenes, explizit aktiviertes Unreal-ReadPixels-Werkzeug mit asynchroner Bildkompression. Capture-Readback/Encoding beeinflusst den Ablauf und zählt nicht als Performance-Messung.',
'Enthalten: 10 s Idle, über 15 s Gehen / mehrere vollständige Zyklen, acht Richtungen, wiederholte Wechsel, abrupte Stopps, 90°-/180°-Drehungen, echter Wanderer-Dialog und Talk→Idle. Nur Previewactor wird für Bewegungen gesteuert. Für den Dialog wechselt die Player-Prüfposition zurück zum bestehenden Wanderer; Kameraparameter bleiben unverändert. Dieser Aufnahmeablauf ist keine Navigation-/AI-Prüfung und kein teleportfreier Gameplay-Fußlauf.',
'',
'Die erste PNG-Aufnahme war zu dünn (ca. 5 Hz); weitere frühe Strecken berührten Felsen/Kronen. Diese bleiben als Diagnose erhalten und gelten nicht als freie finale Bewegungsabnahme. Der finale Bereich wurde anhand vorhandener Hindernispositionen gewählt; keine Vegetation oder Weltgeometrie verschoben.',
'',
'| Nachweis | Datei |',
'|---|---|']
for tag,label in [('Gameplay','Vollständiger Ablauf'),('Feet','Fuß-/Unterkörperausschnitt'),('Cape','Mantel-/Ausrüstungsausschnitt')]:lines.append('| '+label+' | '+link(O/('Unreal/Wanderer_V3_Clear_'+tag+'.mp4'))+' |')
lines += ['',
'Ausschnitte vergrößern nur vorhandene Bildpixel; Kamera und Renderperspektive wurden nicht näher gestellt. Motion Blur und geringe Figur-Pixelhöhe begrenzen feine Fuß-/Stoffbeurteilung. Die lossless QHD-Standposen ergänzen die Videoaufnahme, ersetzen aber keine kontinuierliche Bewegung.',
'Sichtbarer Fortschritt: kein rückwärts gerichteter Knielöser und kein seitlicher Ausfallschritt mehr im identischen 0,225-s-Vergleich. Engere Fußspur, voneinander unterscheidbare Schritte und Gegenbewegung. Restschwächen: gebeugte Grundhaltung, Übergangs-/Pivotkontakte bei harten Wechseln, steifer/fusionierter Ausrüstungsbereich und fehlende Zehenartikulation. Keine Garantie gegen subtile Durchdringungen in allen Blickrichtungen.',
'',
'## 6. Gameplay, Build und Automation',
'',
f"Vollständiger echter Enhanced-Input-Fußlauf bestanden: {foot['distance_m']:.2f} m in {foot['game_seconds']:.2f} Spielsekunden. **Keine Test-Teleports in diesem separaten Gameplaytest.** Dialog/Input-Lock, Queststart, Wildkampf/Fangen, Liora, Speichern vor Archiv, kontrolliertes Runtime-Reset/Load, Archivabschluss, geänderter Wandererdialog, Heilhaus/Expanded-Interior, Heilerin/HP/PP/Checkpoint/Save, gerader und diagonaler Ein-/Austritt, Wald/Kronen-Reveal, acht Player-Richtungen, Menü und Sprint geprüft.",
'Save/Load war ein kontrollierter Runtime-Test innerhalb derselben PIE-Sitzung, kein Prozessneustart-Test. Der vorherige Dev-Spielstand wurde vorab kopiert, das Testresultat separat aufbewahrt und das Original hashgesichert bytegleich restauriert. Keine außerhalb des Tests neu entstandenen Spielstände blind überschrieben.',
'Zusätzlicher NPC-Regressionstest: reale Annäherung, Capsule blockiert weiterhin bei ca. 62 cm Radius-Summe, Talk/Input-Lock, Talk→Idle, Sprite-Fallback, Rückkehr zu 3D; Source-Transform und Dev-Save dabei unverändert. Kein physischer Controller getestet.',
f"Mac Development Editor Build regulär mit geschlossenem Editor, kein Live Coding: erfolgreich. Vollständiger Projektbestand nach dem letzten Build: **{automation['succeeded']}/{len(automation['tests'])} erfolgreich**, {automation['failed']} Fehler, {automation['succeededWithWarnings']} Test-Warnungen, {automation['notRun']} nicht ausgeführt. Neuer Test PokeMonster.NPC.MotionV3.AnatomicalLegAxes prüft importierte Gelenke über den vollständigen Walkzyklus, korrekten Kniepol, Fußspur, eigenes Skeleton, In-place und isolierte V3-Darstellung.",
'Map Check der neuen Karte: siehe gesicherte Logauszüge; final 0 Fehler / 0 Warnungen. Keine Warnungen still unterdrückt. Engine-Bootstrap meldet bereits vor Projekt-Tests generische Condition-failed-Ausgaben, außerdem die bekannte nicht startbare idevice_id-Hilfsdatei (Bad CPU type). Diese stehen separat in Warnings.json; sie sind nicht als erfolgreiche Projektassertionen umgedeutet.',
'',
'## 7. V2/V3-Performance unter identischen Bedingungen',
'',
'Fünf verpflichtende Profile, jeweils drei zeitlich verschachtelte AB/BA-Paare, getrennt embedded PIE und native Development-`-game`-Prozesse. Standalone ist kein paketierter Shipping-Build. Pro Segment 5 s Warm-up und 8 s Messfenster; Qualitätswechsel vor PIE, nicht während eines laufenden PIE. Keine Video-/Blender-/Buildlast während der Messfenster. Keine Environment-Optimierung.',
'Gemessen wurde derselbe vorhandene Wanderer im Idle am festen Wald-/Dialog-Prüfpunkt; beide Zustände sichtbar und mit ihrer jeweiligen AnimInstance. Keine pauschale Hochrechnung auf viele laufende NPCs; CPU-Kosten eines vollständigen bewegten NPC-Schwarms nicht gemessen. Der Probe filtert explizit den Gameplay-NPC und keine deaktivierte Previewfigur.',
'Kamera, Playerposition, Licht, VSM-/Lumen-Konfiguration und Materialien identisch. VSync/FPS-Limit ausgeschaltet, rhi.SyncInterval protokolliert; kein Beweis einer bestimmten Display-Präsentationsrate allein aus der Engine-Framezeit. Ausgabe-/Viewport-/Targetgrößen und Renderer-Fractions pro Frame geprüft. Interne Größe aus Renderer-Auflösungsfraktion bei deaktivierter dynamischer Auflösung abgeleitet (ceil), kein GPU-Allocation-Readback.',
'',
'| Modus | Ausgabe / Qualität / SP | V2 FPS | V3 FPS | V2 / V3 Frame ms | V2 / V3 P95 ms | V2 / V3 GPU ms | V2 / V3 Game ms |',
'|---|---|---:|---:|---|---|---|---|']
for x in perf:
 w,h,q,sp=x['config'];f=lambda n:'n/v' if x.get(n) is None else f"{x[n]:.2f}"
 lines.append(f"| {x['mode']} | {w}×{h} / {'Medium' if q==1 else 'High'} / {sp}% | {f('V2_fps')} | {f('V3_fps')} | {f('V2_ms')} / {f('V3_ms')} | {f('V2_p95')} / {f('V3_p95')} | {f('V2_gpu')} / {f('V3_gpu')} | {f('V2_game')} / {f('V3_game')} |")
lines += ['',
'Tabellenwerte sind Mediane der drei Laufmediane; P95 ist der Median der einzelnen Lauf-P95. Einzelwerte, paarweise Deltas, Render-Thread-Werte, Kamerabereiche und alle Rohdaten in PerformanceTable/Measurements/RawMeasurements. Null-/fehlende RHI-/Draw-Counter sind nicht als null Draw Calls gewertet. Render-Thread-Zeit kann Wartezeit enthalten.',
f"Auflösungsprüfung: {validation['segments']} Segmente, keine Abweichungen im finalen Validator. Netz-/Thermikzustände und zeitliche Schwankungen separat protokolliert; keine harte thermische Isolation des MacBook Air oder Garantie einer festen FPS-Zahl. Kleine oder wechselnde Differenzen sind kein belastbarer allgemeiner Optimierungsgewinn.",
'',
'## 8. Empfehlung und offene Arbeiten',
'',
'**V3 noch nicht als fertigen Referenz-NPC freigeben.** Die konkrete Beinachsen-Ursache ist korrigiert und anhand echter Blender-/Unreal-Posen belegt. Build/Automation/Gameplay funktionieren, aber das ersetzt keine finale Animationsqualität.',
'',
'1. Beckenhöhe und Knie-Streckung künstlerisch nachbearbeiten; die Grundhaltung wirkt noch zu gebeugt. Nicht bloß Schrittweite weiter reduzieren.',
'2. Handgesetzte Start-/Stop-/Pivotkontakte ergänzen und 180°-Wechsel ohne Pin-Neusetzen abnehmen; vorhandene 25-cm-Sicherheitsgrenze ist keine finale Lösung für alle Übergänge.',
'3. Fusionierte Mantel-/Taschen-/Riemenbereiche gezielt manuell auswählen und gewichten beziehungsweise lokal sauber trennen. Bestehende V2-Gewichte wurden nicht als manuell korrigiert ausgegeben.',
'4. Ballen-/Zehenrollbewegung und gegebenenfalls Terrain-IK als eigene, vorher abgestimmte Folgearbeit; aktuelles Rig hat nur einen Fußbone je Seite.',
'5. Die echten Videos durch Harry visuell prüfen. Die begrenzte Frame-/Pixelauflösung lässt keine vollständige Mikro-Kontakt-/Stoffabnahme zu. Keine automatische Übernahme in VisualV2.',
'',
'## 9. Dateien und Git',
'',
'Neue Bereiche: Ranger Source/Exports/Review AnimationV3, Content/Characters/NPCs/RangerMotionV3, die neue NPCMotionV3-Karte, V3-spezifische VisualActor/AnimInstance, PreviewSource, Profiling-/Capturewerkzeug, ein Regressionstest und Tools/RangerAnimationV3. Sämtliche bestehenden V2-Dateien und anderen offenen Arbeiten erhalten.',
'Vollständige Dateiliste: '+link(D/'ScopeAndFiles.json')+'. Rohlogs, Save-Backups, SDK-/Capture-Fehlversuche und volatile Jobs unter Saved/RangerAnimationV3. Frühere Diagnoseaufnahmen sind keine finalen Freigabenachweise.',
'`git diff --check`: '+read(D/'GitChecks.json')['tracked_diff_check']+'. Neue Textdateien zusätzlich separat auf Whitespace geprüft. Kein Staging, Commit oder Push.',
'',
'```text',git.rstrip(),'```','']
dest=R/'Docs/MESHY_RANGER_ANIMATION_QUALITY_V3_PRUEFBERICHT.md';assert not dest.exists();dest.write_text('\n'.join(lines))
print('REPORT_WRITTEN',dest)
