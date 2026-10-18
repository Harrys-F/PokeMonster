"""Assemble measured tables after validation/QA. Visual judgement must be supplied separately."""
from pathlib import Path
import json,statistics,csv,subprocess
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2AASoftShadowsV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18')
rows=json.loads((S/'Summary.json').read_text());validation=json.loads((S/'Validation.json').read_text());assert len(rows)==192 and validation['regular_segments']==576
cost=json.loads((S/'CostSummary.json').read_text());assert len(cost)==2
visual=json.loads((O/'VisualAssessment.json').read_text());assert visual['reviewed_by_agent']
qa=json.loads((S/'Automation/Result.json').read_text());assert qa['exit']==0 and qa['summary']['succeeded']>=48
foot={}
for v in ['A','B','C','D']:
 d=json.loads((S/'Acceptance'/('Variant'+v)/'FootTest.json').read_text());assert d['passed'];restored=json.loads((S/'Acceptance'/('Variant'+v)/'SaveRestored.json').read_text());assert restored['restored'];foot[v]=d
invariants=json.loads((S/'RuntimeInvariant.json').read_text());assert invariants['passed']
protection=json.loads((O/'ProtectionAudit.json').read_text());assert not protection['unexpected_changes'] and not protection['missing_original_files']
thermal=[json.loads(x) for x in (S/'Thermal.jsonl').read_text().splitlines()];states={v:sum(x['thermal_label']==v for x in thermal) for v in sorted({x['thermal_label'] for x in thermal})}
feature_hash=(O/'FeatureCommit.txt').read_text().strip() if (O/'FeatureCommit.txt').exists() else 'Noch nicht erstellt; erst nach abgeschlossener Prüfung.'
label={'A':'TSR / Originalschatten','B':'TAA / Originalschatten','C':'TSR / weiche Bodenprojektionen','D':'TAA / weiche Bodenprojektionen'}
text=f'''# VisualV2 TAA/TSR & Soft Shadows V1 – Prüfbericht

## Ergebnis und Freigabegrenze

{visual['recommendation']}

Es wurde **keine neue Map erstellt und keine vorhandene Map gespeichert**. Versuche ausschließlich zur Laufzeit in `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1`. Die zentrale VisualV2 bleibt unverändert auf TSR und Originalschatten. Keine automatische Übernahme. Sonnen-/Skylight-Werte, Belichtung, Lumen, Bloom, Nebel und Innenraumbeleuchtung wurden nicht als Optimierung geändert.

## Ausgangslage und Schutz

Slim-Worktree: `{R}`. Ausgangs-HEAD und direkt geprüfter origin/main: `a87b7b07111f6b13fe68d6e1e1fe7588067685e3`. Branch `codex/slim-backup-v5`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt auf altem main und Archiv-Ref erhalten und wird nicht in die Remote-Historie aufgenommen.

Vorgefundene unversionierte Arbeiten `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap` und `Tools/VisualV2EnvironmentQualityV1/` bleiben unangetastet und ausgeschlossen. Vorher-SHA-Inventar: {len(json.loads((O/'BeforeFiles.json').read_text()))} Dateien. Vollständige Schutzprüfung: [ProtectionAudit]({O}/ProtectionAudit.json).

Vorhandene Karten wurden geprüft; die gespeicherte GPU-Diagnosekarte entspricht nach Normalisierung des Paketnamens der aktuellen VisualV2-Szene. EnvironmentPerf-Varianten enthalten andere Versuchsbedingungen und wurden nicht als vermeintlich gleichwertige Ausgangsbasis übernommen. TreeShadowProxyV1 bleibt ein begrenztes, nicht allgemein freigegebenes früheres Experiment. Die aktuelle Strauch-Instancing-Materialkorrektur ist enthalten.

## Varianten und technische Umsetzung

| Variante | AA | Schatten |
|---|---|---|
| A | TSR, Methode 4 | Original |
| B | TAA, Methode 2 | Original |
| C | TSR | weiche Bodenprojektionen |
| D | TAA | weiche Bodenprojektionen |

Neue Assets ausschließlich unter `/Game/Development/VisualV2AASoftShadowsV1`: `M_SoftGroundBlob`, `MI_TreeBlob`, `MI_FigureBlob`. Gemeinsamer texturloser Deferred-Decal-Master, schwarze Base Color mit weich fallender, leicht gelappter Deckkraft. Dichte 0,45 für Bäume und 0,50 für Figuren. Keine Blatt-/Astkonturen. Nur Color/Opacity angeschlossen; keine Normal-/Roughness-/Specular-/Metallic-Eingänge. Der lokale Renderer `DecalRenderingCommon.cpp` leitet die tatsächlich geschriebenen Kanäle aus angeschlossenen Materialeigenschaften ab. Bestehende Empfängermaterialien werden nicht geändert.

45 sichtbare Eichen-/Birkenkomponenten und fünf Figuren ergeben im aktuellen Versuch 50 Projektoren, nicht 50 zwingend gleichzeitig sichtbare Draw Calls. Frustum-/Screen-Size-Culling bleibt wirksam. 46 Strauch- und vier kleine Pflanzenkomponenten erhalten keine zusätzlichen Flecken; ihre Einzelschatten werden in C/D deaktiviert, soweit vorher vorhanden. Dynamische Schatten bleiben an Gebäuden und nicht ausgewählten Objekten erhalten. Keine pauschale DirectionalLight-Abschaltung.

Der opt-in Development-Befehl `pm.SoftShadows.Test` ist auf diese vorhandene Testwelt begrenzt. Er speichert ursprüngliche CastShadow-Werte, erzeugt nur Runtime-Helfer ohne Kollision und stellt alle Werte beim Stop wieder her. Kein Start beim Laden einer Map. Figuren folgen pro Frame; WorldStatic-Bodenabfrage höchstens alle 0,05 s und unmittelbare Neuabfrage bei großem Ortswechsel. Zwischen Abfragen lokale Bodenebene. Verdeckte/deaktivierte aktuelle Quellfiguren werden berücksichtigt. Später neu gespawnte Figuren werden in diesem begrenzten Prototyp noch nicht automatisch registriert.

Rückgabeprüfung: {len(invariants['changed_shadow_components'])} tatsächlich umgeschaltete Schattenkomponenten; {invariants['unchanged_light_components']} Lichtkomponenten und {invariants['unchanged_postprocess_volumes']} vollständige Postprocess-Volumes unverändert. Originale Komponenten-/Material-/Transform-/Collision-Zustände nach Stop exakt zurückgegeben. [Runtime-Invarianten]({O}/Evidence/RuntimeInvariant.json).

Kamera B 2850 cm / −50° / −45° / FOV 35°, Playerhöhe 140 cm, Gehen 210 und Sprint 315 cm/s sowie Eingaben, Kollisionen, NPC-/Quest-/Kampflogik bleiben unverändert.

## Messmethode und Auflösungen

1280×720 und 2560×1440, jeweils Medium/High und 75/100 %, PIE und Standalone getrennt. Acht feste Konfigurationen pro Modus. Drei Orte: Dorf/Heilhaus (-4100,450,50,15), Wald (-4300,1550,50,15), Weg (-36,6,-47,1,50,15) cm. Drei Wiederholungen; A/B/D/C beziehungsweise umgekehrte Reihenfolge interleavt. Pro Segment 3 s Warm-up + 3 s Messung. 576 reguläre Segmente, 192 Drei-Lauf-Zusammenfassungen. Fotos und Drainzeilen außerhalb der Timingwertung.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95, kein gepooltes Gesamt-P95. Kurze Fenster begrenzen kleine Unterschiede und sind keine Dauer-FPS-Garantie. Alle bislang verlangten Auflösungskombinationen wurden anhand von Viewport, Target, ViewRect und fortlaufenden Renderer-Beobachtungen geprüft. Interne Größen: 960×540/1280×720 beziehungsweise 1920×1080/2560×1440. Interne Maße sind aus dem Renderer-Screen-Percentage-Treiber abgeleitet, kein direkter Pufferreadback. Fenster-/DPI-Daten separat im Rohdatensatz; Renderausgabe nicht mit logischer macOS-Fenstergröße verwechseln.

Scalability vor frischem PIE gesetzt; keine High→Medium-Umschaltung mit lebenden Reveal-MIDs. Zwischen Qualitätsprofilen gelten die originalen Scalability-Vorgaben, innerhalb eines Profils sind Lumen/Reflections/VSM/Bloom identisch für A–D. VSync=0, t.MaxFPS=0, Dynamic Resolution=0. `rhi.SyncInterval=1` blieb bestehen; Fälle nahe 60 FPS können präsentationsbegrenzt sein. Keine künstliche FPS-Verbesserung aus unterschiedlichen Renderauflösungen.

Standalone ist UnrealEditor Development `-game` bei geschlossenem Editor, kein paketierter Shipping-Build. GPU-Zeit aus verfügbaren Unreal-CSV-Zählern. Game-/Renderthread-Scopes enthalten Wartezeiten beziehungsweise teils Nullwerte; Null-Draw-Call-Zähler sind keine Messung kostenloser Arbeit. Verschachtelte GPU-Scopes nicht addieren. Begleitende thermische Stichproben: {states}; Netzbetrieb laut Energieprotokoll. Kein Temperatur-/Takt-Sensorbeweis. Leichte Auswertungs-/Steuerprozesse und mögliche Zeitdrift begrenzen kleine Submillisekunden-Schlüsse.

## Vollständige Ergebnistabelle

Zeiten in ms. GPU/ShadowProjection und GPU/ShadowDepths sind verfügbare CSV-Scopes; keine vollständige Summe aller Schattenarbeit.

| Modus | Ausgabe | Profil/SP | Ort | Variante | FPS | Median | P95 | GPU | Game | Render | Schattenprojektion | Schattentiefe |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for r in sorted(rows,key=lambda x:(x['mode'],x['width'],x['quality'],x['percentage'],x['site'],x['variant'])):
 c=r['csv'];fmt=lambda n:f'{c[n]:.2f}' if n in c else 'n. v.'
 text+=f"| {r['mode']} | {r['width']}×{r['height']} | {'Medium' if int(r['quality'])==1 else 'High'}/{r['percentage']} % | {r['site']} | {r['variant']} | {r['fps']:.2f} | {r['median_ms']:.2f} | {r['p95_ms']:.2f} | {fmt('GPUTime')} | {fmt('GameThreadTime')} | {fmt('RenderThreadTime')} | {fmt('GPU/ShadowProjection')} | {fmt('GPU/ShadowDepths')} |\n"
text+='''
## Isolierte Kosten der Bodenprojektionen

Zusatzvergleich QHD/High/100 %, drei Paare: exakt dieselben deaktivierten Objektschatten und dieselbe AA-Methode, nur sichtbare gegenüber unsichtbaren Decal-Helfern. Registrierungs-/Nachführungsaufwand bleibt in beiden Fällen bestehen; Differenz umfasst Raster-/Compositing-Effekte und Messrauschen, keinen isolierten Hardware-Kernel.

| Modus | GPU sichtbar | GPU unsichtbar | Differenz | Bildzeit sichtbar | Bildzeit unsichtbar | Differenz |
|---|---:|---:|---:|---:|---:|---:|
'''
for c in cost:text+=f"| {c['mode']} | {c['visible_gpu_ms']:.3f} | {c['hidden_gpu_ms']:.3f} | {c['gpu_difference_ms']:+.3f} | {c['visible_frame_ms']:.3f} | {c['hidden_frame_ms']:.3f} | {c['frame_difference_ms']:+.3f} |\n"
text+='\n'+visual['cost_assessment']+'\n\n## Visuelle Prüfung und Bewegung\n\n'+visual['details']+'\n'
text+='\n## Tatsächliche Gameplay- und technische Tests\n\n'
for v,d in foot.items():text+=f"- Variante {v}: Enhanced-Input-Fußlauf **{d['distance_m']:.2f} m**, {d['wall_seconds']:.1f} s, Maximalgeschwindigkeit {d['max_speed_cm_s']:.2f} cm/s. Bestanden; kein Testteleport.\n"
text+=f"\n{visual['test_details']}\n\nMac Development Editor Build erfolgreich (Logs Build1–5; letzte Fassung Build5). Vollständige Projekt-Automation: {qa['summary']}. Map Checks: zentrale VisualV2, bestehende GPU-Testkarte und WestlandAssetLibrary, Ergebnisse in den verlinkten Logs. Ein gezielter Cook der neuen Materialien wird getrennt dokumentiert; kein Shipping-Spieltest behauptet.\n"
text+='\n## Fehlversuche und Grenzen\n\n'+visual['failures_and_limits']+'\n'
text+='\n## Dateien und lokale Nachweise\n\n'
text+=f"- Neuer Code: `Source/PokeMonster/Development/PokeMonsterSoftShadowTest.h/.cpp`; eng begrenzte Erweiterung des vorhandenen Performance-Probes.\n- Neue Materialien: die drei oben genannten Development-Assets. Keine vorhandene Material-/Textur-/Meshdatei geändert.\n- Werkzeuge und 16 reproduzierbare Messpläne: `Tools/VisualV2AASoftShadowsV1/`.\n- [Alle Drei-Lauf-Ergebnisse]({O}/Evidence/Summary.json), [alle A/B/C/D-Vergleiche]({O}/Evidence/Comparison.csv), [Auflösungs-/Kamera-/Lichtprüfung]({O}/Evidence/Validation.json), [isolierte Kosten]({O}/Evidence/CostSummary.json).\n- [Fotoverzeichnis]({O}/Evidence/Screenshots), [Rohdatenarchiv]({O}/RawMeasurements.zip), [SHA-geprüftes Nachweismanifest]({O}/EvidenceManifest.json).\n- [Automation]({O}/Evidence/Automation/Result.json), [Map Checks]({O}/Evidence/MapChecks), [Fußläufe und Bildfolgen]({O}/Evidence/Acceptance).\n"
for name,path in visual['images']:
 text+=f'\n**{name}**\n\n![{name}]({path})\n'
text+=f"\n## Git-Sicherung\n\nFeature-/Werkzeug-Commit: `{feature_hash}`. Benötigte Projektdateien gezielt aufnehmen, keine Videos, Kontrollbilder, Rohmessungen, Cachedateien oder verworfenen Prototypskripte. Bericht separat sichern. Vollbackup bleibt unverändert. Remote/LFS-Abschluss im [Git-Nachweis]({O}/GIT_ABSCHLUSS.md) und in der Abschlussantwort. Keine automatische Übernahme in VisualV2.\n\nGit-Status vor Sicherung:\n\n```text\n"+subprocess.check_output(['git','status','--short'],cwd=R,text=True)+"```\n"
path=R/'Docs/VISUALV2_TAA_TSR_SOFT_SHADOWS_V1_PRUEFBERICHT.md';path.write_text(text);print(path,len(text.encode()))
