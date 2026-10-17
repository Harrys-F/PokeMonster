# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
from pathlib import Path
import json,subprocess,shutil,hashlib
R=Path(__file__).resolve().parents[2];O=R/'Saved/TreeShadowProxyV1';A=R/'Art/World/TreeShadowProxyV1';D=A/'Review';E=D/'Evidence'
for n in ['FinalEditorState.json','GitAfter.txt']:
 if (O/n).exists():shutil.copy2(O/n,E/n)
data=json.loads((D/'Measurements.json').read_text());rows=data['summary'];walk=json.loads((D/'WalkTest.json').read_text());pres=json.loads((O/'Preservation.json').read_text());tests=json.loads((O/'AutomationSummary.json').read_text());assert pres['changed']==pres['missing']==[];assert walk['passed'] and tests['succeeded']==45 and tests['failed']==0
for p in (R/'Tools/TreeShadowProxyV1').glob('*.py'):compile(p.read_text(),str(p),'exec')
table='| Ausgabe / Qualität / SP | Bildzeit A → B (ms) | FPS A → B | P95 A → B (ms) | GPU A → B (ms) |\n|---|---:|---:|---:|---:|\n'
shadow='| Ausgabe / Qualität / SP | ShadowDepths A → B (ms) | ShadowProjection A → B (ms) | Game Thread A → B (ms) |\n|---|---:|---:|---:|\n'
for r in rows:
 name=f"{r['width']} × {r['height']} / {'Medium' if r['quality']==1 else 'High'} / {r['percentage']} %";a,b=r['A'],r['B'];fmt=lambda key:f"{a[key]:.3f} → {b[key]:.3f}"
 table+=f"| {name} | {fmt('median_frame_ms')} | {fmt('median_fps')} | {fmt('p95_frame_ms')} | {fmt('GPUTime')} |\n"
 shadow+=f"| {name} | {fmt('GPU/ShadowDepths')} | {fmt('GPU/ShadowProjection')} | {fmt('GameThreadTime')} |\n"
files=sorted(p for folder in [A,R/'Content/Environment/TreeShadowProxyV1',R/'Tools/TreeShadowProxyV1'] for p in folder.rglob('*') if p.is_file() and '__pycache__' not in str(p));files+=[R/'Content/Maps/Dev_TestMap_TreeShadowProxyV1.umap'];paths='\n'.join('- `'+str(p.relative_to(R))+'`' for p in files)
report=f'''# Baumschatten – begrenzter Proxy-Test V1

Stand: 15.10.2026. Experiment, keine Freigabe oder Übernahme ins übrige Gebiet.

## Ergebnis

Drei bestehende V3-Eichen besitzen in einer separaten Karte eine geschlossene, undurchsichtige Kronen-Schattenschale mit je drei großen unregelmäßigen Öffnungen. Einzelblätter dieser drei Bäume werfen keine zusätzlichen VSM-Schatten. Stamm und Äste werfen über eine geometrisch erhaltene Kopie weiter Schatten. Keine Transparenztextur und kein zusätzlicher Weichzeichner.

Die Schattenform ist sichtbar vereinfacht. Ein großer allgemeiner Performancegewinn ist **nicht** nachgewiesen. Die GPU-Schattenprojektion wird günstiger; die ShadowDepths-Kosten bleiben nahezu gleich. QHD/High/100 % verbessert sich in den drei zeitlich verschachtelten Paaren um 0,869 / 1,204 / 2,721 ms, während andere Konfigurationen teilweise durch Zeitdrift überlagert werden. Kein Rückschluss auf die ganze Region oder Standalone.

## Ausgangsstand und Schutz

- HEAD: `351a3ef Add YoungTrainer sprint V1 and in-place run animation`.
- Arbeitsbaum war bereits verändert. Status vor Beginn: `Evidence/GitBefore.txt`, nach Abschluss: `Evidence/GitAfter.txt`.
- {pres['files_checked']} vorhandene versionierte und unversionierte Projektdateien per SHA256 verglichen: **0 verändert, 0 fehlend**. Alle vorherigen Entwicklungsarbeiten bleiben erhalten, einschließlich VisualV2, EnvironmentPerf V1/V2, Ranger, Player und Incoming.
- Keine Änderungen an bestehenden Maps, Materialien, Meshes, Blenderquellen, C++, Konfiguration, Gameplay oder verbindlichen Docs. Kein Commit, kein Push, nichts gestaged.

## Karte, Gruppe und Kamera

- Quelle: `/Game/Maps/Dev_TestMap_VisualV2` (unveränderte visuelle Referenz, nicht EnvironmentPerfV2 mit dessen abweichendem Laufzeitprofil).
- Neue Karte: `/Game/Maps/Dev_TestMap_TreeShadowProxyV1`.
- Datei: `Content/Maps/Dev_TestMap_TreeShadowProxyV1.umap`.
- Kopie über `EditorLoadingAndSavingUtils.save_map`, anschließend von eigener Datei geladen. Kein Dateisystem-Kopieren externer Levelreferenzen.
- Gruppe: `V2_ForestOak_0` (−4650/900/0 cm, Faktor 0,62), `_1` (−3880/1580/0, Faktor 0,60), `_2` (−2640/1670/0, Faktor 0,52).
- Player-Messpunkt: −4300 / 1550 / 50,15 cm. Feste echte Spielkamera: −5595,3805 / 2845,3805 / 2268,3767 cm, Pitch −50°, Yaw −45°, FOV 35°, Arm 2850 cm. Keine Kameraänderung.
- Sichtbare Bäume behalten Mesh, Materialien, Transformation und Kollision. Der lesende Actorvergleich bestätigt genau drei Änderungen bestehender Actors: `CastShadow=False`. Genau sechs neue Proxy-Actors. Keine versetzten Bäume.
- Andere Bäume einschließlich der Birke im Vordergrund behalten bewusst ihre bisherigen Schatten.

## Tatsächlich verwendetes Rendering

Virtual Shadow Maps (`r.Shadow.Virtual.Enable=1`), Lumen (`r.DynamicGlobalIlluminationMethod=1`), statische Beleuchtung projektseitig deaktiviert. Bewegliches Haupt-DirectionalLight: Pitch −48°, Yaw −100°, Intensität 7,5, Source Angle 3,5°. Fülllicht wirft keine Schatten. Licht, Source Angle, Postprocessing und Schattenauflösung wurden für den Proxy nicht geändert.

Sichtbare Eiche: `/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3`, LODs 12.068 / 7.240 / 3.621 Dreiecke, zwei Materialslots. Verwendet die vorhandenen maskierten Bark-/Crown-Reveal-Materialien. Diese bleiben identisch; die Spielerfreistellung bleibt am Originalmesh aktiv.

Die vorhandene native Messhilfe setzt intern zunächst ihr V1-Profil. Dieses wurde **in jeder einzelnen A- und B-Zeile identisch** auf die auditierte VisualV2-Konfiguration überschrieben: IntegrateDownsampleFactor 1, SMRT RayCountDirectional 8, FinalGatherMethod 1, HardwareRayTracing 1. Medium/High sind die angegebenen Scalability-Gruppen mit diesen vier expliziten gemeinsamen Overrides. Die Hardware-Raytracing-CVar allein ist kein Beweis für jeden tatsächlich unterstützten Metal-Renderpfad. Kein Leistungsgewinn wird durch eine Änderung dieser Werte erzeugt.

Nach dem Test wurde der Editor neu geöffnet: OverridePIEScreenPercentage 1, SecondaryScreenPercentage 0, ScreenPercentage 0 (automatisch), Renderer 1/8/1/1 wie bei der ersten Bestandsaufnahme. Siehe `Evidence/FinalEditorState.json`. Kein dauerhaftes globales Renderprofil hinzugefügt.

## Proxy-Geometrie und Import

- Neue Blenderquelle: `Art/World/TreeShadowProxyV1/Source/OakAncient_ShadowProxy_V1.blend`.
- Separater Blender-5.2.2-Hintergrundprozess; die laufende Blender-Arbeitssitzung wurde nicht verwendet.
- Stamm/Äste: 4.412 Dreiecke, 2.293 Blender-Vertices, keine Non-Manifold-Kanten. Aus Materialbereich 0 des existierenden V3-Quellmeshes übernommen. Unreal-Vertexvergleich: maximale nächste-Punkt-Abweichung 0,00003412 cm; kein Achsen-/Spiegelungsfehler.
- Krone: 376 Dreiecke, 184 Vertices, drei echte Durchgänge, 0 Non-Manifold-Kanten. Irregulärer Umriss ohne einzelne Blattformen. Kein Alpha-Material.
- Ein einfaches neues Opaque-Material, je Mesh ein Slot, keine neuen Texturen, keine Mesh-Kollision. Beide Assets ohne Distance-Field-Auflösung.
- Je Baum zwei versteckte Komponenten mit `CastHiddenShadow=True`, `HiddenInGame=True`, `CastShadow=True`, Profil `NoCollision`, keine Overlaps, keine Raytracing-Sichtbarkeit und kein Einfluss auf Distance-Field-Lighting. Die Originalkomponenten werfen keine VSM-Schatten mehr. Kein Doppelwurf beider Darstellungen.
- Unreal-Ordner: `/Game/Environment/TreeShadowProxyV1/` mit `M_TSP_OpaqueShadow`, `SM_TSP_OakAncient_Bark`, `SM_TSP_OakAncient_Crown`.
- Im normalen Editor sind die Proxies als bearbeitbare Hilfsobjekte sichtbar; **im Spiel sind sie unsichtbar**. Sie stehen im Ordner `TreeShadowProxyV1_ShadowOnly`.
- Erneutes Öffnen der gespeicherten Blenderdatei bestanden, beide Meshes geschlossen; auch die gespeicherte Unreal-Testkarte erneut geladen, sechs Proxies korrekt, keine temporäre Neigungsfläche, keine dirty Packages.

Der erste dicke Proxy beschattete die sichtbare Krone störend selbst und schloss Lichtlücken im schrägen Einfall. Dieser Stand wurde verworfen. Die finale dünne Schale liegt unter den Blattflächen; ihr horizontaler Versatz entlang der Lichtprojektion erhält die mittlere Bodenschattenposition. Dadurch ist der Versuch auf die **vorhandene feste Sonnenrichtung** abgestimmt. Ein späterer Tageszeitenwechsel benötigt eine Nachführung beziehungsweise andere Proxyform. Das ist noch keine universelle Baumlösung.

## Messmethode

MacBook Air M4, 16 GB, Netzbetrieb 100 %. Eingebetteter Editor-PIE, keine schwebenden PIE-Fenster. Sechs Konfigurationen, jeweils drei A/B-Paare mit Reihenfolge AB / BA / AB. 20 Sekunden Vorlauf nach der Qualitätseinstellung außerhalb von PIE, anschließend je Segment 10 Sekunden Warm-up und 10 Sekunden Messung. Nachgeladenes Material und Shader waren vor der Messung bereit; keine parallelen Builds, Blender-Generierung, Bildverarbeitung oder Aufnahmen während der Zeitmessung.

A = Originalschatten der drei Bäume, sechs Proxies ohne Schatten. B = Originalschatten aus, sechs versteckte Proxies werfen Schatten. Baumdarstellung, Geometrie, Kamera, NPC-Zustände (Animationen für den Vergleich pausiert), Beleuchtung und Einstellungen bleiben innerhalb jedes Paars identisch. Beim Fußlauf wurden Animationen wieder freigegeben.

36 Segmente validiert, drei Wiederholungen je Zustand/Konfiguration, alle gemessenen Frames im aktiven Unreal-Fenster, konstante Kamerapose. Native Messhilfe überprüft Viewport, Render-Target und unskaliertes Renderer-ViewRect, nicht nur `r.SetRes`. Editorfenster: 2940 × 1696 Backing-Pixel bei DPI 2; dies ist **nicht** die Spiel-Renderauflösung. Ausgabe 1280 × 740 beziehungsweise 2560 × 1440. Interne Größen aus den nativen Renderer-Fractions abgeleitet, keine Buffer-Allokations-Rücklesung: 960 × 555 / 1280 × 740 / 1920 × 1080 / 2560 × 1440. Dynamische Auflösung aus, VSync aus, `t.MaxFPS=0`, Secondary Fraction 1.

Die Tabellen zeigen den Median der drei Laufmediane; P95 ist der Median der drei einzelnen P95-Werte. Die vollständigen Einzelwerte und Streuungen stehen in `Measurements.json`; sämtliche Frame- und GPU-CSV-Dateien, Settings, Pläne und Steuerprotokolle in `Evidence/RawMeasurements.zip`.

{table}

## GPU-Schattenkosten

{shadow}

GPU/ShadowDepths und GPU/ShadowProjection sind die verfügbaren CSV-Zähler für die **gesamte Szene**, nicht ausschließlich für diese drei Bäume. Überlappende GPU-Pässe werden nicht addiert. Die großen RenderThread-Nullzähler in diesem Editorpfad sind nicht auswertbar und bedeuten keine kostenlose Renderarbeit. GPUTime enthält auch Editor-/Slate-Anteile; die Fensterbedingungen sind gepaart identisch. ProfileGPU wurde zusätzlich außerhalb der Messungen aufgenommen; Metal-Statistikmarker und konstante Null-Draw-Zähler werden nicht als belastbarer Bottleneck-Beweis behandelt.

127 thermische Stichproben im Begleitprotokoll sämtlich `nominal`. Keine verlässliche Temperatur-/Frequenzmessung; `nominal` schließt jeden Drift nicht aus. Insbesondere Standard/75 % schwankt zwischen den Wiederholungen deutlich. ShadowProjection sinkt in allen sechs Zusammenfassungen, die gesamte Bildzeit jedoch nicht konsistent. Daher **kleiner beziehungsweise teilweise nicht zuverlässig isolierbarer Gesamtnutzen**. Keine stabile-60-FPS-Zusage.

Messungen beschränken sich bewusst auf die gewählte Baumgruppe. Kein zusätzlicher vollständiger Dorf-/Weg-/Regions-Benchmark und kein Standalone-Vergleich; dafür keine Ergebnisse behauptet.

## Visuelle und funktionale Prüfung

- Echte identische QHD-Spielkamera: `GameCamera_A_QHD00000.png` (vorher), `GameCamera_B_QHD00000.png` (nachher). Keine Konzeptbilder.
- Grobe Kronenumrisse mit wenigen größeren Lichtlücken. Die Öffnungen wirken teilweise noch relativ oval; die künstlerische Abnahme steht aus.
- Blattformen, Baumpositionen, Texturen und Reveal-Materialien unverändert. Durch den Austausch des Schattenwerfers ändert sich die **Selbstbeschattung** teilweise; keine Behauptung pixelidentischer Beleuchtung.
- Fußlauf: {walk['distance_m']:.2f} m in {walk['seconds']:.2f} s, reale Enhanced-Input-Steuerung, keine Test-Teleports, maximal 210 cm/s, keine Blockade oder Stürze, feste Kamera unverändert. Zum Wald hin, an und unter den drei Kronen vorbei, diagonal sowie zurück. Schritt-/Frameprotokoll: `WalkTest.json`.
- In den geprüften Aufnahmen keine sichtbaren Hilfsflächen, keine auffälligen Doppel-/Umschaltschatten, Stamm-/Wurzelkontakt plausibel. Abgetastete echte Bildfolge: `WalkSequence.gif`, Übersicht `WalkContact.jpg`, sechs volle `WalkReview_*.png`.
- Diese Bildfolge ist eine Aufnahme alle etwa 2 Sekunden, **kein kontinuierliches Video und kein vollständiger hochfrequenter Flicker-Nachweis**.
- Geneigte Fläche: echter PIE-Test auf einem temporären kollisionsfreien 4 × 3-m-Empfänger mit 8° Neigung, 60 cm Höhe; Schatten und große Lichtlücke projizieren plausibel darauf. `SlopeReceiver8deg_QHD00000.png`, `SlopeTest.json`. Anschließend ausschließlich dieser neu erzeugte temporäre Actor entfernt, nicht in der Testkarte behalten. Kein natürlicher Hang in der ausgewählten Gruppe vorhanden; kein ausgedehnter Geländetest behauptet.
- Wind: WPO an beiden tatsächlich verwendeten Eichenmaterialien nicht angeschlossen. Deshalb keine bestehende Windbewegung zu synchronisieren. Test mit animiertem Wind bleibt **offen**, insbesondere für spätere windbewegte Kronen.
- Keine erneuten Kampf-/Save-/Quest-End-to-End-Tests durchgeführt; diese Systeme wurden nicht verändert. Vorhandene automatisierte Tests wurden tatsächlich ausgeführt.

## Tests und aufgetretene Probleme

- Map Check der fertigen Testkarte: **0 Fehler, 0 Warnungen**, 15.10.2026 17:42:01 UTC. Rohlog `Evidence/MapCheck.txt`.
- **45/45 PokeMonster-Automationstests erfolgreich**, 0 fehlgeschlagen, 0 Testwarnungen, Prozess-Exit 0. `Evidence/Automation_index.json`, `Evidence/AutomationSummary.json`.
- Separat vorhanden: 17 generische `Condition failed`-Meldungen beim Engine-Start vor der PokeMonster-Testwarteschlange und die vorhandene `idevice_id`-Warnung (Bad CPU type). Nicht unterdrückt; vollständiges Log im Raw-Archiv. Die Aussage 45/45 bezieht sich auf den exportierten PokeMonster-Testbestand, nicht auf ein fehlerfreies komplettes Engine-Startlog.
- Ein früher Messstart ist beim Wechsel High → Medium **während PIE** an `UniformExpressionCache` für `MID_MI_V2_BirchReveal_0` abgestürzt. Keine Messwerte dieses Versuchs verwendet. Gespeicherte Dateien erhalten. Neustart; anschließend Qualität ausschließlich vor PIE gewählt. Alle sechs gültigen Konfigurationen ohne erneuten Absturz abgeschlossen.
- Ein zunächst gesetztes `NoCollision`-Flag wurde beim Wiederladen durch das Standardprofil ersetzt. Das **neue** Proxyprofil wurde deshalb explizit auf `NoCollision` gestellt, neu gespeichert und in PIE verifiziert. Keine ursprüngliche Baumkollision geändert.
- Frühe asynchron angeforderte Screenshots wurden zu nah am Schattenzustandswechsel erstellt. Diese Aufnahmen liegen ausschließlich unter `Saved/TreeShadowProxyV1/RejectedImmediateSwitch/` und dienen nicht als Nachweis. Finale Aufnahmen halten den Zustand nach dem Request weitere zwei Sekunden.
- Die abschließende lokale MCP-Verbindung wurde auf Port 8003 wiederhergestellt, da der nach dem Testabsturz offene CrashReporter Ports 8000/8001 belegt. Crashdaten blieben erhalten; Editor steht mit der neuen Testkarte und ohne PIE/dirty Packages bereit.
- C++ unverändert, kein Build erforderlich. Python-Syntax der neuen Werkzeuge im Speicher geprüft. Ein erster `compileall`-Aufruf konnte nur wegen des gesperrten externen Python-Cachepfads keine Bytecode-Dateien schreiben; anschließend ohne Cache-Schreibzugriff geprüft.
- `git diff --check`: Exit 0, keine Ausgabe (mit lokalem LFS-Zugriff). Keine Projektdateien gestaged.

## Empfehlung und Stopp

Als begrenzter Stil- und Technikversuch gespeichert. **Nicht auf das übrige Gebiet übertragen.** Erst die gröbere Schattenform, die teilweise andere Kronen-Selbstbeschattung und die noch runden Lichtlücken visuell freigeben. Der gemessene kleine Gesamtgewinn rechtfertigt derzeit keine pauschale Übernahme. Weitere Arbeit gegebenenfalls: bessere Formabstimmung und Prüfung echter windbewegter Kronen/dynamischer Sonne, anschließend erneut gleiche Messung. Keine verbindliche Projektentscheidung in TECHNIK oder ENTSCHEIDUNGEN geändert.

## Neu erzeugte Dateien dieses Auftrags

{paths}

Zusätzlich dieser Prüfbericht, das abschließende Dateimanifest und die Werkzeug-README. Frühere und verworfene Arbeitsartefakte bleiben unter `Saved/TreeShadowProxyV1/` erhalten und sind nicht als fertige Assets ausgegeben.

## Abschließender Git-Status

```text
{(O/'GitAfter.txt').read_text().rstrip()}
```
'''
(D/'PRUEFBERICHT.md').write_text(report)
manifest=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='EvidenceManifest.json'];(D/'EvidenceManifest.json').write_text(json.dumps(manifest,indent=2));print('Report saved',len(report),'characters')
