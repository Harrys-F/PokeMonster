# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
import json,hashlib,statistics
from pathlib import Path
R=_evidence_root;P=R/'Art/Characters/NPCs/Ranger/Review/V2';before=json.loads((P/'ProtectedBefore.json').read_text());after=json.loads((P/'ProtectedAfter.json').read_text());auto=json.load((P/'Automation/index.json').open(encoding='utf-8-sig'));foot=json.loads((P/'FootTest/FootTest.json').read_text());validation=json.loads((P/'MeasurementValidation.json').read_text());audit=json.loads((P/'FinalMapAudit.json').read_text());review=json.loads((P/'UnrealAccepted/Comparison.json').read_text());root=str(R)
def link(label,path):return f'[{label}]({root}/{path})'
text=f'''# PokeMonster – Performance & Ranger Quality V2

Stand: 15.10.2026. **Keine Freigabeempfehlung für eine automatische Übernahme in Dev_TestMap_VisualV2.** Der neue Ranger ist ein funktionsfähiger, sichtbar geprüfter Optimierungskandidat. Die Welt wird dadurch nicht wesentlich schneller. Vor dauerhafter Übernahme sollten die automatische LOD-Grenze und die stark schwankenden Standalone-Bedingungen gezielt nachgeprüft werden. Tests ersetzen diese visuelle/zeitliche Abnahme nicht.

## 1. Ausgangszustand und Projektschutz

HEAD: `{before['head']}`. Der Arbeitsbaum war **bereits geändert**, nicht sauber. Insbesondere VisualV2, TECHNIK, ENTSCHEIDUNGEN, der Dialogue-Header und die komplette uncommittete NPC-Integration waren vorhandene Arbeiten. Sie wurden nicht als eigene Änderungen ausgegeben und nicht zurückgesetzt.

```text
{before['status'].rstrip()}
```

Abschließender SHA-256-Vergleich: **{after['protected_file_count']} anfangs erfasste versionierte/unversionierte Projektdateien unverändert**, keine fehlenden Dateien. Darunter alle zehn Incoming-Originale, ursprüngliche Blenderquellen, Ranger V1, Spieler/Animationen, Originalmaps und bestehende Dokumentation. Ignorierte Build-/Log-/Cachedateien sind von dieser Aussage ausgenommen. Der Dev-Spielstand wurde nach den Tests bytegleich wiederhergestellt. {link('Hash-Nachweis','Art/Characters/NPCs/Ranger/Review/V2/ProtectedAfter.json')}.

Originalbaseline: `/Game/Maps/Dev_TestMap_VisualV2`. Experiment ausschließlich in **`/Game/Maps/Dev_TestMap_RangerPerfV2`** (`Content/Maps/Dev_TestMap_RangerPerfV2.umap`). Kopie über Editor-API, anschließend explizit die neue Welt geladen und nur diese gespeichert. `save_map` schreibt eine Kopie, benennt die aktuelle Welt aber nicht um; ein deshalb abgewiesener zweiter Speicherversuch wurde korrigiert. Die Originaldatei wurde nicht gespeichert.

Keine Veränderung an Gameplay, Kamera, Playermaßstab, Geschwindigkeit, Input, Playeranimationen, Weltgeometrie, Vegetationspositionen, Dialogdefinitionen oder Speicherlogik. Kein Commit, kein Push, nichts gestaged.

## 2. Tatsächliche Messauflösungen

- **A:** tatsächlicher SceneViewport und dessen Render-Target **1280 × 740**, Medium, 75 % Screen Percentage, VSync 0, `t.MaxFPS=0`, Dynamic Resolution 0.
- **B:** tatsächlicher SceneViewport/Render-Target **2331 × 1346**, sonst identische Vorgaben. Das sind **3,31-mal** so viele Ausgabepixel wie A. Die alten 23–27 FPS werden ausdrücklich nicht als 1280×740 ausgegeben.
- **C:** eigener nativer Development-Prozess mit `-game -windowed -ResX=1280 -ResY=740 -ForceRes -NoVSync -NoSound`. Tatsächlicher SceneViewport/Render-Target ebenfalls **1280 × 740**. **Kein paketierter Shipping-Build.** Unreal CSV meldet Metal SM6 / Apple M4 / MacEditor-DeviceProfile.

Die tatsächliche Ausgabegröße, Render-Target-Größe, Screen Percentage und Kamerapose wurden **pro Frame** erfasst. Alle **{validation['valid_segments']} gültigen Segmente** bestanden die Größen-/75-%-Prüfung. Die 75 % beschreiben die konfigurierte 3D-Skalierung; Ausgabepixel und intern ausgerichtete Renderpass-Texturgrößen sind nicht gleichzusetzen. Keine Behauptung einer separat gemessenen internen SceneColor-Ausrichtung.

Das eingebettete PIE ließ sich mit `r.SetRes` allein nicht verlässlich auf die geforderte Größe bringen. Deshalb wurde ein ausdrücklich gestarteter nativer Development-Prüfbefehl ergänzt, der `FSceneViewport::SetFixedViewportSize` verwendet. Kein autonomer Gameplay-Tick. Editor-Overrides wurden scoped auf PIE-Override 0 / Secondary Percentage 100 gesetzt und abschließend auf die ursprünglichen Werte 1 / 0 zurückgestellt. Keine Projekt-Renderkonfiguration gespeichert.

{link('1280×740-Bildnachweis','Art/Characters/NPCs/Ranger/Review/V2/ResolutionSmoke_ResolutionProof00000.png')}; {link('Validierungsdaten','Art/Characters/NPCs/Ranger/Review/V2/MeasurementValidation.json')}.

## 3. Messmethode und Grenzen

Pro Standort drei Wiederholungen; Baseline/Finalvergleich **8 s Warm-up + 10 s Messfenster**. Reihenfolge der Standorte gewechselt. Finale V1/V2-Paare zeitlich verschachtelt; zweite Wiederholung mit umgekehrter V1/V2-Reihenfolge. NPC ohne Gespräch in bestehendem Idle, gleiche Quellidentität/Position/Ausrichtung. Die Einzelposen einer laufenden Idle-Animation sind nicht framegenau phasengleich; jedes Fenster umfasst mehrere Zyklen. Für die Standbilder wurde dagegen dieselbe Idle-Position 0,25 s eingefroren.

| Rohdatenname | Spielerposition cm | Bedeutung |
|---|---|---|
| Dorf | −760 / −1410 / 50,15 | NPC-Vorplatz am Beginn des ursprünglichen Mini-Slices; **kein Gebäudestandort** |
| Wald | −746,5 / −718 / 50,15 | Wald-/Trainerweg |
| Weg | −36,6 / −47,1 / 50,15 | Offener Weg |
| DorfBauten | −4100 / 450 / 50,15 | Heilhaus/Vorplatz; zusätzlich aufgenommen, um echte Gebäude abzudecken |

Kamera unverändert **2850 cm / Pitch −50° / Yaw −45° / FOV 35°**. Automatische Heilhaus-Innenkamera im Fußtest unverändert. Profilierungspositionen wurden gezielt gesetzt und sind **kein behaupteter Fußlauf**. Der spätere komplette Fußtest war eine frische PIE-Sitzung mit Enhanced-Input-Bewegung.

Native Framezeiten aus monotoner Echtzeit. FPS = 1000 / Median-Frametime; P95 mit linearer Quantilinterpolation. Tabellenmediane über drei Messläufe, kein verstecktes Wegmitteln langsamer Läufe. Unreal CSV/GPU-Zähler ergänzen die nativen Framezeiten. Game/Render/GPU überlappen; ihre Zeiten nicht summieren. RenderThreadTime im Standalone enthält Wartezeit und ist keine reine CPU-Rechenzeit.

**Zeitdrift vorhanden:** {validation['thermal_samples']} macOS-Thermal-State-Abfragen meldeten durchgehend „nominal“. Das ist weder ein Temperaturmesswert in °C noch ein Beweis konstanter GPU-Taktrate. Kalte/heiße Blöcke unterscheiden sich deutlich. Daher sind die direkt gepaarten Kontrollen aussagekräftiger als Stunden auseinanderliegende V1-/V2-Blöcke. Keine gemessene Takt-/Temperaturursache behauptet.

Standalone schwankte besonders stark (z. B. finaler NPC-Vorplatz 60,35 → 20,52 → 21,79 FPS). Diese Ergebnisse sind real, aber **kein stabiler Standalone-Nachweis einer Optimierung**. Auflösung und 75 % blieben laut Frameprotokoll gleich. Die Ursache der starken Drift wurde nicht eindeutig isoliert; keine nachträgliche Qualitätsänderung vorgenommen.

Pläne: `Tools/PerformanceRangerV2/Plans/`. Frame-Rohdaten: `Saved/PerformanceRangerV2/*_Frames.csv`; Unreal-Zähler: `Saved/Profiling/CSV/RV2_*.csv`. {link('Auswertung je Messlauf','Art/Characters/NPCs/Ranger/Review/V2/Measurements.json')}. Roh-CSV-Header am Dateiende berücksichtigt, weil Unreal Zähler dynamisch ergänzt.

## 4. FPS, Framezeiten und isolierte A/B-Tests

**Wichtig:** `AfterA`, `AfterB`, `PairedA`, `PairedB` sowie `Unreal/` und `UnrealFinal/` beziehen sich auf einen später verworfenen Custom-LOD-Import. Sie bleiben als Fehlernachweise erhalten, sind aber **kein Optimierungserfolg**. Gültige V2-Reihen sind `FinalPairedA/B`, `FinalAfterC` und `VillageA/B/C`. V1-Baselines und reine V1-Faktortests bleiben gültig, da vor jedem Plan ausdrücklich V1 als Kontrollmesh gesetzt wurde.

'''
text+=(P/'FinalMetricTables.md').read_text()
text+='''
## 5. GPU-/CPU-Analyse und Bedeutung der Faktoren

Die Ergebnisse sprechen für einen überwiegend render-/GPU-begrenzten Ablauf: Game-Thread meist etwa 6–7 ms im PIE, während GPU und Framezeit deutlich höher liegen; steigende Ausgabepixel erhöhen die Zeiten stark. Im Standalone liegt der Game-Thread ungefähr bei 1–2 ms, bei erheblich höheren GPU-/inklusive Renderzeiten. Das ist eine Einordnung, kein lückenloser CPU-/GPU-Scheduler-Nachweis.

Der finale Ranger spart in den gepaarten PIE-Läufen nur ungefähr **0,15–0,91 ms Median-Paardifferenz**, je nach Standort/Auflösung; einzelne Paare haben die Gegenrichtung. Am Gebäudestandort ist er außer Sicht und der Effekt praktisch null. Kein belastbarer großer FPS-Sprung und keine garantierte P95-Verbesserung.

Größere wiederholte Diagnoseeffekte:

- **PostProcessingOff:** ungefähr 3,3–4,3 ms weniger Framezeit. Das ist ein breiter Show-Flag-/Pipeline-Test, kein Beweis für einen einzelnen teuren Effekt; AA/Upscaling/Pipelinefolgen können mit betroffen sein.
- **Alle dynamischen Schatten aus:** etwa 2,2–3,2 ms. Shadow Depths und Shadow Projection sind als GPU-Zähler vorhanden. Die Kategorien können verschachtelt sein; nicht blind addieren.
- **Vegetation unsichtbar:** etwa 2,0–2,5 ms am Wald-/NPC-/Wegstandort; am Heilhaus kein stabiler Framezeitgewinn. Dieser Schalter umfasst Sichtbarkeit und die damit entfallenden Schatten-/Sichtbarkeitsfolgen, nicht ausschließlich Dreiecke.
- **Nur Vegetationsschatten aus:** deutlich kleiner und teils nicht stabil. Daraus folgt nicht, dass alle Schattenkosten von Bäumen stammen.
- **Ranger unsichtbar:** im Wald/Vorplatz etwa 0,55–0,84 ms, auf offenem Weg kein stabiler Gewinn. Enthält auch sichtbarkeitsabhängige Animationsfolgen, nicht reine Geometrie.
- **Ranger ohne Schatten / ohne Animation / konstantes Material:** kleine, teils wechselnde Ergebnisse. Der Flat-Materialtest verändert Normal-/Rauheits-/Texturinputs gemeinsam; keine isolierte Texturbandbreitenmessung.
- **Lokale Punkt-/Spotlichter aus:** kein stabiler Vorteil. Nicht gleichbedeutend mit „sämtliche Beleuchtung kostenlos“; Directional-/Rect-Lichter waren nicht dieser Faktor.

Die Vegetationsauswahl ist exakt im Probe-Code dokumentiert: registrierte StaticMesh-/Instancing-Komponenten mit `SM_WLA_` und Oak/Birch/Bush/Grass/Fern/Flower/Herb, ohne Ruins/Rune/Column. Kein pauschaler Schalter sämtlicher Umgebungsobjekte.

CSV zeigt auch Lumen- und SlateUI-/Unaccounted-Kosten. Das sind auffällige Zähler, keine separat bewiesenen Einzelursachen. **RHI/DrawCalls und passbezogene DrawCall-Zähler lieferten Nullwerte und sind nicht verlässlich auswertbar.** Keine erfundene Draw-Call-Anzahl. Ebenso kein belastbarer quantitativer Overdraw-/Quad-Overdraw-Nachweis. Maskierte/dithernde Vegetation kann Pixelkosten verursachen, obwohl GPU/Translucency 0 meldet. Texture-/Materialslotzahlen sind gemessen; einzelne Texturkosten und NPC-VRAM-Residency nicht isoliert erfasst.

Alle Faktoren nur temporär in der wegwerfbaren PIE-Welt geändert und vor der nächsten Variante zurückgestellt. **Keine abgeschalteten Schatten, Lichter, Vegetation oder Posteffekte in die Testkarte übernommen.**

## 6. Ranger-V2-Blenderquelle und Exporte

Maßgebliche Quelle: `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V2_Protected.blend`. Vollständig gepackt, in separater Blender-Instanz erneut erfolgreich geöffnet. Drei gepackte 2048×2048-Texturen, ursprüngliche UVMap, ein Materialslot. Live-Blender mit der vorhandenen Hobbit-Retopo-Sitzung nicht ersetzt oder gespeichert.

V1-Runtime: 90.000 Dreiecke / 44.390 geometrische Vertices. Bestehende High-Poly-Referenz und V1-Runtime unverändert als Referenzen behalten. Keine neue Retopologie, kein neues Rig, keine neue Animation. 24 Blender-Bones; in Unreal 25 einschließlich importiertem Armature-Root. Bone-/Restpose-Hash identisch mit V1. Source-Bounds bis etwa 1,80063 m / 180,063 cm; der bestehende etwa 1,80-m-Rangermaßstab und die Fußbasis wurden nicht verändert (Spieler weiterhin 1,40 m).

Reduktion kontrolliert vor dem Armature-Modifier. Kopf/Hände über empirisch geprüfte invertierte Vertex-Group-Gewichtung geschützt. Die erste ungeschützte Reduktion zeigte in Nahaufnahmen unvertretbare Gesichtsschäden und wurde verworfen. Keine Behauptung, ein erfolgreich ausgeführter Decimate-Modifier genüge als Qualitätstest.

| Kandidat | Geometrische Vertices | Dreiecke | Status |
|---|---:|---:|---|
| Geschützt LOD0 | 26.890 | 55.000 | Unreal-Kandidat, Kopf/Hände geschützt |
| Geschützt LOD1 | 11.390 | 24.000 | Unreal-Kandidat; nur mit konsistentem Importpfad |
| Geschützt LOD2 | 4.486 | 10.192 | **Verworfen**: sichtbare Kragen-/Kleidungsschäden; nicht im Runtime-Mesh |

Export: `Art/Characters/NPCs/Ranger/Exports/V2_Protected/SK_Ranger_NPC_V2_LOD0.fbx` und `...LOD1.fbx`. Der zusätzliche LOD2-FBX sowie `Exports/V2/` und `Ranger_NPC_V2.blend` sind erhaltene, verworfene Versuche, keine Alternativfreigaben.

Kopf-/Hand-Quellvertices zur Zieloberfläche: gemessen 0 mm Abweichung in den definierten geschützten Regionen. Globaler P95 etwa 1,00 mm / 3,98 mm für LOD0/1; Maximum etwa 7,90 / 29,50 mm. Das ist ein einseitiger Quellvertex-zu-Oberfläche-Test, **kein vollständiger Hausdorff- oder Qualitätsbeweis**. UVs, normalisierte Gewichte und endliche Normalen/Koordinaten geprüft. Vollständige Blender-Idle-/Talk-Zyklen kontrolliert. Unterkörper-/Umhangdetails werden bei LOD1 etwas kantiger; die Vorlage selbst besitzt bereits Oberflächen-/Gesichtsartefakte.

## 7. Unreal-Assets und tatsächlicher Reimport

**Arbeitskandidat:** `/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean`.

Wiederverwendet:

- `/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1_Skeleton`
- `/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1`
- `/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Talk_V1`
- `/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1` und bestehende Texturen.

Keine neuen Gameplay-Collider/Physics Assets. Bestehender NPC-Präsentationsactor und dessen sichtbarkeitsabhängige Animation/URO/kurzer Dreh-Tick weiterverwendet. Kein permanenter zusätzlicher NPC-Actor-Tick.

**Aufgedeckter Importfehler:** Der erste Runtime-Import zeigte bei LOD1 eine falsche Arm-/Körperhaltung, obwohl Bone-Namen, Counts und Blender-Bilder korrekt waren. Beide FBX-Dateien wurden in frischem Blender gelesen: Hierarchie, Bindepose, Objekttransformationen und Vertex-Group-Namen identisch. Der 24k-FBX funktionierte als separat importiertes Skeletal Mesh und als frischer Custom-LOD-Import. Ein nachträglicher Reimport über den anderen Importpfad erzeugte die Fehlpose erneut. Am selben Clean-Asset stellte **Legacy-FBX-Reimport** die korrekte Animation wieder her.

Der fehlerhafte Interchange-Pfad meldete ausdrücklich zwei unterschiedliche BindPose-Matrizen aus FbxCluster/FbxPose und eine nicht passende LOD-Namenskonvention. Diese Warnungen wurden nicht unterdrückt.

Daher Erstimport **und** Custom-LOD-Reimport konsistent mit `Interchange.FeatureFlags.Import.FBX=0`, nur scoped während der Operation und anschließend auf den vorherigen Wert 1 zurückgestellt. Tatsächlicher Reimport durchgeführt, gespeichert und danach aus der Spielkamera animiert geprüft. Keine globale Importer-Konfiguration geändert. Ein erneuter Reimport über einen abweichenden Standardpfad bleibt ein konkretes Wartungsrisiko.

Früher hatte ein automatisch angelegtes LOD-Settings-Asset außerdem eine zusätzliche 50-%-Reduktion aktiviert. Die tatsächlichen Renderdaten wurden deshalb nativ geprüft. Der finale Clean-Kandidat verwendet keine solche automatische Reduktions-DataAsset-Zuweisung. Der erste `SK_Ranger_NPC_V2` und `DA_RangerV2_LODSettings` bleiben **verworfene Diagnose**, `M_Ranger_FlatDiagnostic` ist ausschließlich ein A/B-Prüfmaterial. Keine neuen doppelten Texturen oder Animationsclips.

## 8. LODs, Entfernungen und Speicher

Native Renderdaten des finalen Clean-Assets:

| Mesh/LOD | Renderdreiecke | Rendervertices inkl. UV-/Normalensplits | approximative LOD-Renderdaten-Bytes |
|---|---:|---:|---:|
| V1 LOD0 | 90.000 | 76.506 | 3.528.192 |
| V2 LOD0 | 55.000 | 52.476 | 2.638.944 |
| V2 LOD1 | 24.000 | 27.390 | 1.349.160 |

LOD0: **38,9 % weniger Dreiecke**, etwa 31,4 % weniger Rendervertices. LOD1: 73,3 % weniger Dreiecke gegenüber V1. **Beide gespeicherten LOD-Renderdaten zusammen benötigen etwa 13,0 % mehr als V1**, nicht weniger; ein aktives LOD und der gesamte Asset-Speicher sind unterschiedliche Größen. UE-ResourceSizeEx ist kein vollständiger VRAM-/Prozess-Residency-Nachweis. Serialized UAsset: V1 17.471.356 Bytes, finaler V2-Clean-Kandidat 17.853.627 Bytes zum Prüfzeitpunkt. Originaltexturen geteilt.

ScreenSize LOD0 1,0 / LOD1 **0,12**, Hysterese **0,015**. Keine fixe Metergrenze: Bildschirmgröße, Bounds und Sichtbarkeit wirken mit. Vergleichsbilder bei tatsächlichen Kamera-NPC-Distanzen **27,12 / 28,77 / 30,23 m**; Spieler-NPC-Abstand und Kamerapose im Bildmanifest.

Der erste gezielte LOD-Direktweg traf die vorhandene NPC-Collision; keine Welt geändert. Der umgelegte, bereits im vollständigen Fußlauf bewährte Weg wurde erfolgreich mit Enhanced Input abgelaufen (26,85–37,44 m Kamera-NPC-Distanz), **ohne einen automatischen LOD-Wechsel zu erreichen**. Die frühere dicht erfasste Bildsequenz hatte zusätzliche Screenshot-Hitches und blieb ebenfalls bei LOD0. Deshalb **keinen bestandenen natürlichen LOD-Popping-/Schattenwechseltest behaupten**. Beide erzwungenen LOD-Stufen wurden bei identischer Pose visuell verglichen; sichtbare große Sprünge/Defekte dabei nicht festgestellt. Vor Freigabe die automatische Grenze gezielt justieren und erneut mit realer Bewegung prüfen.

## 9. Echte Bildnachweise

36 unbearbeitete Unreal-Spielkamera-Vergleiche in `Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/`: Dialogdistanz, typische Entfernung, Wald; jeweils Front, Seite, Dreiviertel und Rücken; V1, V2-LOD0 und erzwungenes V2-LOD1. **2331×1346-Ausgabe**, FOV/Position unverändert. Keine generierten Konzeptbilder.

Blender-Nahaufnahmen in `Review/V2/BlenderProtected/`. Fehlgeschlagene Importe in `Unreal/`, `UnrealFinal/`, `NativeAnim/` nicht mit finalen Nachweisen verwechseln. Korrekt animierter Reimport: `NativeAnim_ConsistentReimport/`.

'''
for title,name in [('V1 – Dialogentfernung, Dreiviertel','Dialog_ThreeQuarter_V100000.png'),('V2 LOD0 – gleiche Spielkamera','Dialog_ThreeQuarter_V200000.png'),('V2 LOD1 – erzwungener Vergleich','Dialog_ThreeQuarter_V2LOD100000.png')]:
 text+=f'### {title}\n\n![{title}]({root}/Art/Characters/NPCs/Ranger/Review/V2/UnrealAccepted/{name})\n\n'
text+=f'''Die originale dunkle Haut-/Kleidungswirkung im Schatten bleibt teilweise schwer lesbar; keine eigenmächtige Neuinterpretation der Vorlage. Die geschützte Reduktion beseitigt keine schon in V1 vorhandenen Artefakte. Keine finale Künstlerfreigabe behauptet.

## 10. Animation und Gameplay – tatsächlich durchgeführt

Frischer eingebetteter PIE-Lauf in der Testkopie: **{foot['distance_m']:.2f} m**, {foot['wall_seconds']:.2f} s Wandzeit / {foot['game_seconds']:.2f} s protokollierte Laufzeit. Enhanced Input für Bewegung; bestehende Interaktions-, Menü- und Battle-Presenter-Funktionen per Prüfsystem ausgelöst. Kein menschlicher Handtest behauptet. **Keine Test-Teleports im vollständigen Rundweg**, nur das reguläre bestehende Heilhaus-Relocation-System.

- Menü geöffnet/geschlossen, Eingabesicherung geprüft.
- Wanderer-Dialog und Queststart; Ranger erhält Conversation-Signal und Alpha >0,5; Blickwendung/Gesprächsbildsequenzen aufgenommen.
- Wildkampf **mit erfolgreichem Fang**, danach drei Teammitglieder.
- Liora besiegt; Trainerstatus bestätigt.
- Vor Archivaktivierung gespeichert, Runtime-Trainerstatus kontrolliert verändert, geladen; Trainer und HP/PP korrekt wiederhergestellt. HUD-Bild nach Load zeigt „Untersuche den Archivstein“.
- Archiv aktiviert, Flag im Save vorhanden; Rückdialog sichtbar geändert („Der Archivstein leuchtet wieder…“), aktive Questanzeige beendet.
- Heilhaus gerade hinein, zur Heilerin, alle HP/PP voll, Save/Checkpoint bestätigt, hinaus und diagonal erneut hinein/hinaus. Cutaway/Relocation/Innenbewegungsbasis korrekt.
- Wald-Rundweg, Kronenfreistellung, alle acht Richtungen und abschließendes Menü geprüft.
- **Sprite-Fallback tatsächlich ein-/ausgeschaltet und Sichtbarkeit überprüft**, danach 3D wiederhergestellt.
- Maximal protokollierte normale Geschwindigkeit {foot['max_speed_cm_s']:.6f} cm/s (Float-Toleranz zu 210). Keine neuen Kollisionen oder Abstürze im Rundweg.

Zusätzlicher Python-Direktzugriff auf geschützte Quest-/Save-Felder war nicht möglich; keine Produktions-API dafür aufgebohrt. Der gescheiterte Zusatzprüfer ist dokumentiert, nicht als Erfolg gezählt. Questprüfung hier durch tatsächlichen Ablauf/HUD/Abschlussdialog plus vorhandene Automation. Vollständige Bewegungs-/Interaktionsprotokolle: `Review/V2/FootTest/FootTest.json`, `FootFrames.jsonl`, `FootProgress.json` und Screenshots/Bildsequenzen. `Shot showui` enthält bewusst auch die Editoroberfläche; deren gesamte Bildgröße ist **keine** behauptete Renderauflösung der Performance-Messung.

## 11. Build, Automation und Map Check

- Development Editor Build erfolgreich, letzter Lauf `BuildCleanCandidate.log`, 7,75 s. C++ ausschließlich neues ausdrücklich gestartetes Development-Messwerkzeug; keine bestehenden Gameplaydateien verändert.
- **{auto['succeeded']}/43 Automation erfolgreich**, {auto['failed']} Fehler, {auto['succeededWithWarnings']} Warnungstests, {auto['notRun']} nicht ausgeführt. Frischer Unreal-Prozess mit NullRHI; reine Suite {auto['totalDuration']:.3f} s. NullRHI ersetzt nicht die separat vorgenommenen visuellen PIE-Prüfungen.
- **Map Check der neuen Testkarte: 0 Fehler / 0 Warnungen** (finaler `MAP CHECK`, 09:50 UTC). Der erste Log-Abfrageversuch mit Kategorie MapCheck war technisch nicht verfügbar; anschließende ungekürzte Musterabfrage enthält den tatsächlichen Check.
- Platzierte Actor-Transformationen zur Baseline identisch. Audit zählt in der initialisierten Editorwelt drei zusätzliche Engine-Manager (GameplayDebuggerPlayerManager, AbstractNavData, BuoyancyManager); keine neu platzierten Gameplay-/Geometrieobjekte. Der einzige beabsichtigte Darstellungsunterschied ist das Ranger-Mesh. Präsentationskomponente weiterhin NoCollision, gleicher SourceActor/Idle/Talk/Skeleton. Keine schwebenden PIE-Fenster benutzt.
- Anfängliche Compile-/Python-API-Fehler behoben und ihre Logs erhalten. Zusätzlich im Editor: generische `LogAutomationTest: Condition failed`-Startmeldungen ohne zugeordneten Projekttest, wiederholtes falsches CPU-Format von `idevice_id`, Audio-Samplerate-, MotionVectorSimulation- und MCP-/Socket-/Diagnosewarnungen. Diese sind **nicht** mit den 43 erfolgreichen Projekttests gleichgesetzt oder verschwiegen. Zusätzlich erfasst: Interchange-LOD-Muster-/BindPose-Warnungen im verworfenen Import, eine Warnung über 31 erfolglose ConsoleObject-Lookups für `Shot` (die Screenshotdateien wurden tatsächlich erzeugt und geprüft) sowie EOS-Analytics-Flush-/Heartbeat-Warnungen. Vollständige Logs `EditorWarningsPreRestart.json`, `EditorWarningsFinal.json`, `StartupAutomationMessages.json`, `Automation.log`; keine pauschale Warnungsunterdrückung. Ursache der generischen Startup-Meldungen in diesem Auftrag nicht abschließend ermittelt.

{link('Automation-Report','Art/Characters/NPCs/Ranger/Review/V2/Automation/index.html')} · {link('Map-Check-Meldungen','Art/Characters/NPCs/Ranger/Review/V2/MapCheckLog.json')} · {link('Map-/Actor-Audit','Art/Characters/NPCs/Ranger/Review/V2/FinalMapAudit.json')}.

## 12. Verbleibende Probleme und Freigabeempfehlung

**Empfehlung: V2 in der separaten Testkarte belassen; noch nicht für den dauerhaften Austausch in Dev_TestMap_VisualV2 freigeben.**

Begründung: sichtbare Geometrie im geprüften Zustand weitgehend erhalten, weniger aktive Geometrie, Animation/Gameplay im Fußlauf funktionsfähig. Der FPS-Effekt ist jedoch klein, P95 nicht überall besser, Standalone stark driftend, und ein natürlicher automatischer LOD-Wechsel wurde nicht nachgewiesen. Außerdem muss der konsistente Legacy-Reimport als verbindlicher Arbeitsweg abgesichert bleiben. Das ist keine automatische Künstler-/Performancefreigabe allein wegen grüner Tests.

Offen: automatische LOD-Grenze im sichtbaren Spielbereich fein abstimmen und Übergang/Schatten real ablaufen; stabile zeitlich gepaarte Standalone-Reihe bei kontrollierter Vordergrund-/OS-/Leistungssituation; keine verlässlichen Draw Calls, kein quantitatives Overdraw, keine isolierte Texture-/VRAM-Messung. Keine Ursache für die große Zeitdrift erfunden.

## 13. Konkrete nächste Optimierungsschritte

1. Zunächst die größeren Renderkosten fein isolieren: einzelne Post-/AA-/Upscaling-Effekte unter unveränderter Bildqualität gegentesten; breites PostProcessingOff nicht als Lösung übernehmen.
2. Dynamische Schatten: tatsächlich benötigte Reichweite/Caster, Shadow Depths/Projection und entfernte kleine Objekte gezielt prüfen. Keine pauschale Schattenabschaltung.
3. Wald: passende Vegetations-LODs/Culling und maskierte Material-/Pixelkosten getrennt untersuchen; Gebäudevorplatz zeigt andere Kosten als Wald. Vorhandene Reveal-Materialien/Positionen erhalten.
4. Ranger: konservative automatische LOD-Grenze anhand sichtbarer Übergänge nachziehen, Importvertrag Legacy-FBX bewahren; keine weitere aggressive 10k-Reduktion vor Qualitätsnachweis.
5. Standalone-Ausreißer mit zeitnahen V1/V2-Paaren und zusätzlich verifizierter Vordergrund-/Leistungs-/Speichersituation untersuchen. macOS „nominal“ nicht als Taktstabilitätsbeweis verwenden.

## Dateien, Git und Arbeitsartefakte

Neu in diesem Auftrag: zwei Ranger-V2-Blender-Versuchsversionen, getrennte FBX-Kandidaten, neue RangerV2-Unreal-Assets einschließlich Diagnosen, eine neue Performance-Testkarte, ein Development-C++-Messwerkzeug, reproduzierbare Prüfskripte/Pläne, dieser Bericht sowie Review-/Mess-/Bild-/Lognachweise. **Bestehende Projektdateien aus der Eingangsliste inhaltlich unverändert.**

Maßgebliche Dateien:

- `Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V2_Protected.blend`
- `Art/Characters/NPCs/Ranger/Exports/V2_Protected/SK_Ranger_NPC_V2_LOD0.fbx`, `...LOD1.fbx`
- `Content/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2_Clean.uasset`
- `Content/Maps/Dev_TestMap_RangerPerfV2.umap`
- `Source/PokeMonster/Development/PokeMonsterPerformanceProbe.cpp`
- `Tools/PerformanceRangerV2/`
- `Art/Characters/NPCs/Ranger/Review/V2/`
- `Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md`

Vollständige neue Dateiliste: `Review/V2/NewFiles.json`. Volatile Job-/Ack-/Slate-Dateien, Logs, verworfene Kandidaten, Save-Backups und Buildausgaben sind Arbeits-/Diagnoseartefakte, keine pauschale Empfehlung, alles zu versionieren. Nichts gelöscht. Rohmessungen unter Saved sind bewusst getrennt von Runtime-Assets.

`git diff --check`: erfolgreich, keine Ausgabe. Abschließendes `git status --short`:

```text
__FINAL_GIT_STATUS__
```

Die bereits anfangs geänderte `Dev_TestMap_VisualV2.umap` erscheint weiterhin als M; ihr SHA-256 ist gegenüber dem Eingangszustand identisch. Gleicher HEAD, kein Commit, kein Push, nichts gestaged. Temporäre Editorparameter wiederhergestellt; keine schmutzigen Map-/Contentpakete bei Abschluss. Dev-Spielstand bytegleich zurückgesichert.
'''
(R/'Docs/POKEMONSTER_PERFORMANCE_RANGER_V2_PRUEFBERICHT.md').write_text(text)
print('Report written',len(text),'characters')
