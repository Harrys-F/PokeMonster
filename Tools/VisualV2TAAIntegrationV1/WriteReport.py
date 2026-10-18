"""Write final report only after actual matrix, motion, gameplay and QA pass."""
from pathlib import Path
import json,statistics,subprocess
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18')
audit=json.loads((S/'MapChangeAudit.json').read_text());assert audit['reopened'] and audit['reopened_scene_equal']
validation=json.loads((S/'Validation.json').read_text());assert validation['segments']==216 and validation['photos']==32
rows=json.loads((S/'Summary.json').read_text());assert len(rows)==72
qa=json.loads((S/'Automation/Result.json').read_text());assert qa['exit']==0 and qa['summary']['succeeded']>=49 and all(qa['summary'][n]==0 for n in ['failed','notRun','inProcess','succeededWithWarnings'])
for name in ['Dev_TestMap_VisualV2','Dev_TestMap_VisualV2GPUBottleneckV1','Dev_WestlandAssetLibrary']:
 d=json.loads((S/'MapChecks'/(name+'.json')).read_text());assert not d['dirty_maps'] and not d['dirty_content']
foot=[]
for p in sorted((S/'Acceptance').glob('*/FootTest.json')):
 d=json.loads(p.read_text());assert d['passed'];rest=json.loads((p.parent/'SaveRestored.json').read_text());assert rest['restored'];foot.append((p.parent.name,d,rest))
assert len(foot)>=3
motion=json.loads((S/'MotionInventory.json').read_text());assert len(motion)>=18
protection=json.loads((O/'ProtectionAudit.json').read_text());assert not protection['unexpected_changes'] and not protection['missing_original_files']
assess=json.loads((O/'MotionReviewAssessment.json').read_text());assert assess['reviewed_actual_consecutive_frames']
lookup={(r['mode'],r['width'],r['quality'],r['percentage'],r['site'],r['condition']):r for r in rows}
thermal=[json.loads(x) for x in (S/'Thermal.jsonl').read_text().splitlines()];states={n:sum(x['thermal_label']==n for x in thermal) for n in sorted({x['thermal_label'] for x in thermal})}
text=f'''# VisualV2 TAA Integration V1 – Prüfbericht

## Ergebnis

Die zentrale `/Game/Maps/Dev_TestMap_VisualV2` verwendet jetzt für ihre tatsächliche Spielansicht **TAA mit unveränderten Originalschatten**. Keine neue Map erstellt. Die zuvor getrennt geprüften Shadow-Blob-Varianten sind nicht aktiviert. Globaler Projektstandard und alle anderen bestehenden Maps bleiben unverändert.

Der begrenzte Bewegungsvergleich auf der vorhandenen `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` ergab keinen auffälligen zusätzlichen dauerhaften Figuren-Nachzieheffekt, der eine Übernahme blockiert hätte. TAA ist bei 75 % sichtbar weicher. Feines Blattwerk und die bestehenden Dither-Revealkanten sind auch damit nicht vollständig ruhig. Keine Behauptung einer artefaktfreien oder menschlich freigegebenen 60-FPS-Videoabnahme. Anschließend wurde die gespeicherte Wahl ohne AA-Konsolenoverride erneut bewegt und unter echten Renderbedingungen geprüft.

## Ausgangsstand und Schutz

Slim-Worktree `{R}`, Branch `codex/slim-backup-v5`. Anfangs-HEAD und direkt geprüfter origin/main `a0d6109cb3f2154f3de81bec3082319174f5de39`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt auf altem lokalem main und Archiv-Ref unverändert und außerhalb der neuen Remote-Historie.

2999 vorbestehende versionierte/unversionierte Dateien inventarisiert. Vorhandene unversionierte `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap` und `Tools/VisualV2EnvironmentQualityV1/` weder verändert noch aufgenommen. Unreal war zu Beginn geschlossen; keine fremde unsichere Sitzung verworfen. VisualV2 vor Änderungen extern bytegleich gesichert: [Originalmap]({O}/Dev_TestMap_VisualV2_Before.umap), [Dateiinventar]({O}/BeforeFiles.json). Keine Originalquelle, Animation, Vegetation oder Gameplaydatei zurückgesetzt/gelöscht.

Vorher-SHA `{audit['before_sha256']}`; nachher `{audit['after_sha256']}`. Vollständiger erfasster Szenen-/PP-Vergleich bei {audit['actors']} Actors: genau ein neuer AA-Eintrag am vorhandenen `V2_OutdoorExposure`; alle anderen Einstellungen identisch. Frisch erneut geöffnete Datei gegen dieselbe Nachher-Signatur geprüft. [Änderungsaudit]({O}/Evidence/MapChangeAudit.json).

## Technische Integration

UE 5.8.2 bietet die AA-Methode nicht als Feld des `PostProcessSettings`-Structs an. Deshalb ein kleines natives `UPokeMonsterTemporalAABlendable` über die vorhandene Engine-Schnittstelle `IBlendableInterface`, als map-eigenes Objekt am vorhandenen ungebundenen Volume, Gewicht 1. Keine neue Actor-/Gameplay-Architektur und kein zusätzlicher Postprocess-Materialpass.

Es setzt ausschließlich `FSceneView::AntiAliasingMethod` auf TAA und den zugehörigen vorhandenen Screen-Percentage-Modus passend zu `r.TemporalAA.Upsampling`. Editoransichten, Scene Captures und bewusst deaktiviertes AA bleiben unberührt. Keine globale CVar-/Projektconfig-Änderung; `r.AntiAliasingMethod` bleibt 4. Der unabhängige Renderthread-Beobachter bestätigt die tatsächlich gerenderte Methode **2** bei integrierter Wahl und **4** bei der TSR-Gegenprobe. Der globale CVar-Wert allein wäre deshalb kein Nachweis.

Lichtquellen einschließlich Skylight, Positionen, Farben, Intensitäten, Lumen-GI/Reflexionen, Bloom, Belichtung, Nebel, alle ursprünglichen Schatten, Vegetationsdichte/-geometrie, Kamera B 2850/−50/−45/35, Player 140 cm, Gehen 210 cm/s, Sprint 315 cm/s und Gameplay bleiben erhalten. Außen-MotionBlurAmount 0 und Innenwert 0,5 bleiben unverändert. Das Blendable wird auch im Innenraum geerbt; dessen Beleuchtung wird nicht umgestellt.

Zur gezielten Deaktivierung genügt später das Entfernen bzw. Gewicht 0 dieses einen Eintrags; es gibt keinen weltweiten Quality-Schalter. Das ist keine zusätzliche automatische Rückfallregel im Spiel.

## Bewegungsprüfung und echte Aufnahmen

Vorausgehend zwölf reale Eingabesequenzen auf der bestehenden GPU-Testmap: 720p Medium 75/100 %, QHD Medium/High 75/100 %, jeweils TSR/TAA mit Originalschatten. Tatsächliche Spielkamera, Gehen, Sprinten, Stop, diagonale Umkehr, Kamera-Lag, NPC-Idle und Gespräch. Zwei explizite Anfangspositionierungen pro Kurzsequenz, deshalb keine Behauptung eines teleportfreien Fußlaufs für diese Aufnahmen. Separate vollständige Gameplay-Fußläufe unten.

Danach sechs Kurzsequenzen mit der gespeicherten integrierten Wahl ohne AA-Konsolenoverride. Der Originalrecorder für Ranger V3 wurde nicht verändert; neues explizites Development-Aufnahmewerkzeug liest ausschließlich den tatsächlichen Spiel-Framebuffer. JPEG-Frames mit tatsächlichen Spiel-/Wandzeitstempeln; Videos ohne erfundene Zwischenbilder. Aufnahme-/Encodingkosten sind von den Leistungsmessungen ausgeschlossen. Die veröffentlichten Waldvideos enden vor der expliziten Standortpositionierung zum NPC; sie zeigen keine als Fortbewegung ausgegebene Test-Teleportation. Zusätzliche echte Tür-/Innenraumsequenzen aus dem teleportfreien Gameplay-Rundweg liegen separat vor. Insgesamt {len(motion)} auf Vollständigkeit geprüfte Bildfolgen mit {sum(m['frames'] for m in motion)} tatsächlichen Frames. Auflösung und Zeitabstände in [MotionInventory]({O}/Evidence/MotionInventory.json).

{assess['decision']}

Kein auffälliger neuer lang anhaltender Ghost-Trail im geprüften Bereich. Kleine temporale Kantenunruhe/Ditherreste sind weiterhin sichtbar, speziell an feinen Blättern, Haaren und Schattenkanten. 75 % verliert etwas Detail gegenüber 100 %. Es wird keine Perfektion behauptet. Diese Entscheidung gilt für die geprüfte feste Kamera und vorliegenden Figuren/Materialien; spätere neue Materialien oder Windanimationen benötigen eigene Prüfung. Niedrige QHD-Bildrate und ReadPixels-Aufwand begrenzen die Aufnahmefrequenz. Die Videos enthalten keine künstliche Bewegungsglättung.

## Messmethode

Integrierte zentrale VisualV2, kein Ersatzlevel als Ergebnis ausgegeben. 1280×720 Medium 75/100 %, 2560×1440 Medium und High jeweils 75/100 %. PIE und eigenständiges UnrealEditor Development `-game` bei geschlossenem Editor getrennt, kein paketierter Shipping-Build.

Drei feste Orte: Dorf/Heilhaus (−4100,450,50,15), Wald (−4300,1550,50,15), Weg (−36,6,−47,1,50,15) cm. Je drei interleavte Paare, mittlere Wiederholung in umgekehrter Reihenfolge. 5 s Aufwärmen + 5 s Messung pro Abschnitt; 240 reguläre Abschnitte aufgezeichnet; 216 vollständig ausgewertete Abschnitte und 72 Drei-Lauf-Gruppen. Vierundzwanzig alte Wegabschnitte aus vier Gruppen werden durch vierundzwanzig vollständige Nachmessungen ersetzt (Begründung unten). Die Gegenprobe deaktiviert vorübergehend ausschließlich das gespeicherte AA-Blendable und nutzt TSR, anschließend vollständige ursprüngliche PP-Einstellungen restauriert. Keine Beleuchtung-/Schatten-/Material-/Vegetationsdiagnose gleichzeitig.

Renderer-Methode, Viewport, RenderTarget, ViewRect und fortlaufende Renderer-Fractions in jedem regulären Abschnitt verifiziert. 75 % intern 960×540 bzw. 1920×1080, 100 % volle Ausgabegröße. Interne Maße aus beobachteten Treiber-Fractions abgeleitet, kein direkter SceneColor-Pufferreadback. Fenster/DPI/aktive Präsentation gesondert protokolliert.

VSync=0, t.MaxFPS=0, Dynamic Resolution=0; `rhi.SyncInterval` unverändert. Werte nahe 60 FPS können durch Metal-Fensterpräsentation begrenzt sein. Originale Scalability-Profile vor frischem PIE; kein Live-High→Medium-Wechsel. Zwischen Profilen ändern sich deren normale Qualitätsvorgaben, innerhalb jedes AA-Vergleichs sind alle Nicht-AA-Werte gleich.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95, kein gepooltes P95. Kurze Messfenster begrenzen kleine Unterschiede und garantieren keinen Dauerbetrieb. Game-/Renderthreadzähler enthalten teils Wartezeit/Nullwerte; GPU-Scopes sind verschachtelt und werden nicht summiert. Null-Draw-Call-Zähler nicht als kostenlose Renderarbeit interpretiert. Thermische Stichproben {states}, Energiezustand im Rohprotokoll. Keine unabhängigen Celsius-/Taktwerte; kleine Steuer-/Auswertungsprozesse und Zeitdrift begrenzen die Genauigkeit.

## Vorher/Gegenprobe und integrierte TAA – gemessene Werte

Alle Zeiten ms, jeweils Median aus drei Läufen. TSR-Gegenprobe derselben integrierten Map, keine historischen, abweichend gemessenen FPS als kausaler Vergleich.

| Modus | Ausgabe / Profil / SP | Ort | FPS TSR → TAA | Bildzeit TSR → TAA | P95 TSR → TAA | GPU TSR → TAA |
|---|---|---|---:|---:|---:|---:|
'''
for a in rows:
 if a['condition']!='MapTAA:TSR':continue
 b=lookup[(a['mode'],a['width'],a['quality'],a['percentage'],a['site'],'MapTAA:Native')]
 text+=f"| {a['mode']} | {a['width']}×{a['height']} / {'Medium' if a['quality']==1 else 'High'} / {a['percentage']} % | {a['site']} | {a['fps']:.2f} → {b['fps']:.2f} | {a['median_ms']:.2f} → {b['median_ms']:.2f} | {a['p95_ms']:.2f} → {b['p95_ms']:.2f} | {a['csv']['GPUTime']:.2f} → {b['csv']['GPUTime']:.2f} |\n"
selected=lookup[('Standalone',2560,2,100,'Wald','MapTAA:Native')]
text+='\n## Aktuelle Restkosten im nativen QHD/High/100-Wald\n\n'
text+='| Zähler | ms |\n|---|---:|\n'
for name in ['GPUTime','GameThreadTime','RenderThreadTime','GPU/LumenScreenProbeGather','GPU/LumenSceneLighting','GPU/ShadowProjection','GPU/ShadowDepths','GPU/Basepass','GPU/TAA']:
 if name in selected['csv']:text+=f"| {name} | {selected['csv'][name]:.3f} |\n"
text+='\nRenderThreadTime ist hier eine Wallzeit einschließlich GPU-/Present-Warten, kein reines CPU-Budget. GPU-Scopes überlappen bzw. sind verschachtelt und werden nicht addiert. Alle ausgewerteten Fenster waren laut Telemetrie aktiv (Anteil 1,0). Die hohen 720p-Unreal-Framezahlen sind Engine-Durchsatzmessungen, keine separat gemessene physische Monitor-Präsentationsrate.\n'
text+='''
## Verbleibender Performancebedarf

TAA ersetzt keinen vollständigen QHD-Optimierungsdurchgang. Insbesondere native QHD/High/100 erreicht im geprüften Wald noch keine garantierten 30/60 FPS. Lumen-GI, Originalschatten und Material-/Auflösungsarbeit bleiben erhebliche Budgets. Verfügbare GPU-/Game-/Render-/Schatten-/GI-Zähler je Gruppe und einzelne Laufwerte im vollständigen JSON; keine verschachtelten Scopes addieren. Keine weitere Environment-Optimierung in diesem Auftrag. Zuerst visuelle Nutzerprüfung der TAA-Darstellung, danach getrennte gezielte Untersuchungen mit unveränderter Beleuchtung und fairen Paarvergleichen.

## Gameplay und technische Prüfung

'''
for name,d,restore in foot:text+=f"- {name}: vollständiger Enhanced-Input-Fußlauf **{d['distance_m']:.2f} m**, {d['wall_seconds']:.1f} s, maximal {d['max_speed_cm_s']:.2f} cm/s; bestanden, kein Testteleport. Dev-Slot nach Prüfung auf ursprünglichen Zustand zurückgegeben (anfangs vorhanden: {restore['initial']['existed']}).\n"
text+=f'''
Vorhandener Wanderer-Dialog/Quest, Liora, Wildkampf/Fang, Team-/Menülogik, Archivabschluss, Heilhaus gerade und diagonal, Innenraum und Heilerin/HP/PP/Checkpoint, Save/Load, Bewegung in acht Richtungen, Sprint, Collision und Sprite-Fallback über den bestehenden Prüfablauf. Keine manuelle Controllerprüfung behauptet.

Mac Development Editor Build1 (Aufnahmehilfsmittel) und Build2 (AA-/Probe-Fassung) und Build3 (ausschließlich korrigierter Test-Zeitstempel) erfolgreich. Vollständige Automation: **{qa['summary']}**. Der neue Test prüft den echten AA-Callback einschließlich Gewicht 0, Editor-/Capture-Ausschluss, unveränderter globaler AA-Einstellung sowie Kamera/Bloom/Exposure. Drei Map Checks: zentrale VisualV2, bestehende GPU-Testmap und WestlandAssetLibrary; jeweils 0 Fehler/0 Warnungen. Frisch erneut geladene VisualV2 stimmt mit der gespeicherten Nachher-Signatur überein.

## Fehlversuche und Grenzen

Der erste Automationslauf hatte 48 bestehende Erfolge und einen fehlgeschlagenen neuen Test: In dessen künstlicher View-Family fehlte der von Unreal verlangte explizite Zeitstempel (CVS.bTimesSet). Testaufbau korrigiert, produktive AA-/Probe-Funktionen unverändert, danach vollständiger Lauf wiederholt. Der fehlgeschlagene Lauf bleibt separat unter Automation_InitialFixtureFailure erhalten.

Die erste Videokodierung konnte im sandboxbeschränkten Prozess den nativen AVFoundation-Encoder nicht starten (OSStatus −12903); Quelldaten und fehlgeschlagener Ausgang blieben erhalten. Derselbe Encoder arbeitete im autorisierten Prozess erfolgreich. Keine Unreal- oder Modellkorrektur dafür.

Zwei terminale native CSV-Zählerdateien (C4/C5, jeweils Abschnitt 17 auf dem Weg) blieben leer; zwei weitere aus C2/C3 (Abschnitt 17) waren unvollständig und ohne auswertbaren finalen Zählerheader. Die vorhandenen Bildzeit-/Auflösungs-/AA-Telemetrien wurden nicht um erfundene GPU-Werte ergänzt. Stattdessen vollständige drei Paarvergleiche der vier Weggruppen unter identischen Konfigurationen mit Auslaufzeile erneut gemessen. Alle vierundzwanzig ursprünglichen Wegabschnitte dieser vier Gruppen aus der finalen Auswertung ausgeschlossen und durch vierundzwanzig vollständig geprüfte Nachmessungen ersetzt. Exakter I/O-/Exitgrund nicht weiter bewiesen; Rohdateien unverändert erhalten.

Die ersten C1-Fotos waren ungültig: Das Foto-Inventar bearbeitete einen Python-Struct-Proxy und entfernte zur Textauswertung temporär den AA-Eintrag. Die unabhängige tatsächliche Renderer-Methode erkannte 4 statt 2. Die regulären Abschnitte 0–17 davor sind korrekt bestätigt und bleiben getrennt gültig. Foto-Inventar korrigiert: neues unabhängiges Struct per Textimport. CPhotoC1 in frischer Sitzung erneut aufgenommen und mit Methode 2/4 geprüft. Keine ungültigen Bilder in finalen Vergleichen, keine Änderung der gespeicherten Map durch das Foto-Inventar. Fehlversuche lokal erhalten. Ein anfänglicher Analyse-Indentationsfehler wurde ohne Projekt-/Messdatenänderung korrigiert. System-Python ohne Pillow; vorhandene gebündelte Python-Laufzeit genutzt, nichts installiert.

Aufnahmevideos beruhen auf tatsächlichen Bildern, nicht auf Blender oder Konzeptbildern. Keine 60-FPS- oder menschliche Videoabnahme. Kein Shipping-/Cook-Performancebeleg, keine Hardware-Kernelanalyse, keine exakte Temperaturmessung. Standalone protokolliert bei jedem Start 58 Python-Fehlerzeilen aus experimentellen Engine-Toolsets: ToolsetDefinition/AgentSkill sind im -game-Prozess nicht exponiert. Der vollständige Meldungs-Fingerprint ist exakt identisch zu einer bereits vor dieser Aufgabe vorhandenen nativen AA-Studien-Baseline. Keine zusätzlichen Fehler unseres Python-Werkzeugs oder Material-/Shader-/Instancing-Fehler in den finalen Läufen. Diese vorhandenen Startfehler wurden weder behoben noch unterdrückt; sie bleiben ein offener Engine-/Toolset-Punkt und sind keine fehlerfreie Shipping-Abnahme. Allgemeine weitere Engine-/MCP-/Audio-/idevice-Meldungen bleiben ebenfalls in den Logs und im externen WarningAudit erhalten. Fehler nicht unterdrückt.

## Dateien, Bilder und Git

- Map: `Content/Maps/Dev_TestMap_VisualV2.umap` (Git LFS).
- AA: `Source/PokeMonster/Rendering/PokeMonsterTemporalAABlendable.h/.cpp`.
- Development: eigener AA-Review-Recorder, eng begrenzte Erweiterung des vorhandenen Performance-Probes um tatsächliche Renderer-AA und isolierte Blendable-Gegenprobe.
- Test: `Source/PokeMonster/Tests/PokeMonsterTemporalAATest.cpp`.
- Reproduzierbare Werkzeuge/Pläne: `Tools/VisualV2TAAIntegrationV1/`.
- Bestätigte technische Entscheidung in `Docs/TECHNIK.md` und `Docs/ENTSCHEIDUNGEN.md`.

'''
for name,target in [('Vollständige Messergebnisse','Evidence/Summary.json'),('Unabhängige Validierung','Evidence/Validation.json'),('Echte Vergleichsfotos','Evidence/Photos.json'),('Bewegungsinventar','Evidence/MotionInventory.json'),('Alle lokalen Nachweise','Evidence'),('Git-Abschluss','GIT_ABSCHLUSS.md')]:text+=f'- [{name}]({O}/{target})\n'
text+='\n## Direkt zugängliche Bildvergleiche und echte Videos\n\n'
for title,name in [('Standalone QHD/High/100: links TSR, rechts integriertes TAA','Standalone_QHD_High100_AB.png'),('Gespeicherte TAA-Wahl gegenüber geprüftem B bei Bewegung','Integrated_2560_1440_Q2_SP100.png')]:
 text+=f'**{title}**\n\n![{title}]({O}/ImageReview/{name})\n\n'
for title,name in [('TSR, QHD/High/100, echte Waldsequenz','TSR_QHD_High100.mp4'),('Integriertes TAA, QHD/High/100, echte Waldsequenz','TAA_Integrated_QHD_High100.mp4'),('Integriertes TAA, 720p/Medium/75','TAA_Integrated_720p_Medium75.mp4'),('Echter Standalone-Heilhausübergang, QHD','Door_Integrated_Standalone_QHD_Medium100.mp4')]:text+=f'- [{title}]({O}/Videos/{name})\n'
text+=f'\nAlle neun erfolgreich encodierten Videos und deren Quellen: [Videomanifest]({O}/Videos/Manifest.json). Keine Zwischenbildsynthese. Aufnahmelast nicht für FPS-Angaben verwendet. Drei zusätzliche Türsequenzen aus den vollständigen Fußläufen sind neben den 18 Kurzsequenzen separat vorhanden.\n'
text+='\nKontrollbilder, Videos, Rohdaten und Caches werden nicht hochgeladen. Ausschließlich geprüfte benötigte Dateien gezielt committen; reguläre Pushes und Remote/LFS-Prüfung. Der Vollbackup bleibt unverändert. Endgültige Commit-Hashes im verlinkten Git-Abschluss und in der Abschlussantwort.\n\nGit-Status vor Sicherung:\n\n```text\n'+subprocess.check_output(['git','status','--short'],cwd=R,text=True)+'```\n'
p=R/'Docs/VISUALV2_TAA_INTEGRATION_V1_PRUEFBERICHT.md';p.write_text(text);print('REPORT',p,len(text.encode()))
