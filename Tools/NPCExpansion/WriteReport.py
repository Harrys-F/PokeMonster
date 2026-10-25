"""Generate the factual NPC report from local verified evidence; media stays outside Git."""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/NPCExpansion';configs=json.loads((R/'Tools/NPCExpansion/Library.json').read_text());profiles=json.loads((O/'FinalProfiles.json').read_text());videos={x['id']:x for x in json.loads((O/'Motion02/Videos.json').read_text())};reopen={x['id']:x for x in json.loads((O/'SourceReopen.json').read_text())};lines=[]
for i,a in enumerate(configs):
 id=a['id'];incoming='Art/Characters/NPCs/Incoming/'+a['input']+'.glb' if id!='HobbitBase' else 'Art/Characters/NPCs/Westland/HobbitBase/Incoming/4K_Base_V1/Meshy_Hobbit.glb';p=profiles[i];mesh_status='bestehendes Mesh/Skeleton' if a.get('reuse_mesh') or id=='SilverLady' else 'eigenes benötigtes Skelettmesh';motion='Stand, Gespräch, Begrüßung'+(', Gehen' if a['walk'] else '')+(', Laufen'if a['run']else'');lines.append(f"| {i+1} | {id} | `{incoming}` | {a['height']:.2f} m | {reopen[id]['bones']} | {motion} | {mesh_status} |")
media=[]
for a in configs:
 id=a['id'];v=videos[id];media.append(f"| {id} | [Vorn]({R}/Saved/ProjectRefinement/NPCExpansion/PIE02/{id}_Front.png), [Seite]({R}/Saved/ProjectRefinement/NPCExpansion/PIE02/{id}_Side.png), [Hinten]({R}/Saved/ProjectRefinement/NPCExpansion/PIE02/{id}_Rear.png) | [Video]({R}/{v['file']}) | {v['seconds']:.2f} s / {v['frames']} / {v['game_time_sample_hz']:.2f} Hz |")
text=f'''# NPC-Ausbau mit vorhandenen Meshy-Modellen – Prüfbericht

Stand: 25.10.2026. Ausgangspunkt `e804343beadb9761143399c9bc878cb094acb0f2`, Branch `main`.
Ausschließlich `/Users/harry/Developer/PokeMonster`; bestehende VisualV2.

## Ergebnis

Elf vorhandene NPC-Quellen als wiederverwendbare, validierte 3D-Präsentationen
aufbereitet: zehn Modelle aus NPCs/Incoming sowie die bestehende Hobbitquelle.
Kein Modell generiert, keine Ersatzfigur gebaut. **Neun Figuren können gehen,
sechs zusätzlich laufen. SilverLady und TreeBeing bleiben bewusst stationär.**
70 Rollenclips: Idle, Talk, Greet, jeweils zwei Drehrollen sowie vorhandene passende
Walk-/Run-Rollen. Keine Behauptung, dass jeder lange Mantel bereits ein fertiges
physikalisches Stoffrig besitzt. Die verbindliche Originaloptik bleibt erhalten.

Vorhandener Wanderer = technische Ranger-Darstellung; das sind keine zwei neuen
Geschichtsrollen. Seine neue Präsentation und die Heilerin sind direkt an ihre
bisherigen Source-Actors gebunden. Identitäten, Transform, Dialog und Heilfunktion
bleiben bestehen. Keine endgültigen Rollen, Berufe, Namen oder Standorte neu festgelegt.
Archivarin und Liora bleiben funktional erhalten; für sie wurde ohne eindeutige
Modellzuordnung kein beliebiges männliches Modell beziehungsweise eine zweite
Heilerinnenkopie als neue endgültige Darstellung eingesetzt.

## Gefundene Quellen und tatsächlicher Animationsstand

Alle elf GLBs besitzen ursprünglich **kein Skeleton und keine Animationen**.
Geometrie und eingebettete Texturen wurden anhand der Dateien und vorhandener
Arbeitsquellen geprüft; die Abbildungen bestätigen die Dateizuordnung. Die zehn
allgemeinen Meshy-Quellen haben je einen Mesh, ein Material und drei eingebettete
2048er JPEGs. Die Hobbitquelle besitzt ihren älteren eigenen 4K-Intake;
verwendet wird ihre vorhandene geprüfte Arbeitsfassung mit 2048er Texturen.

Höhen sind die bisherigen sichtbaren Gesamtmaße einschließlich Hut/Ausrüstung/
Reitern, keine neu festgelegten anatomischen Größen aller Völker. Spieler: 1,40 m.
Die bestehende Heilerin behält zusätzlich ihren bisherigen Actor-Maßstab.

| Station | Technische ID | Unveränderte Incoming-Quelle | Bibliothekshöhe | Blender-Knochen | Tatsächliche Rollen | Integration |
|---|---|---|---:|---:|---|---|
'''+ '\n'.join(lines)+f'''

### Gezielte Korrekturen

- Ranger: ursprüngliche detailreichere 90.000-Dreiecke-Arbeitsgeometrie erhalten;
  vorwärts gerichteten Knielöser aus der früheren V3 weiterverwendet, die übermäßig
  abgesenkte 7,8-cm-Beckenhaltung reduziert. Geschwindigkeit und Schrittlänge werden
  gekoppelt; Kontaktstabilisierung und weichere Gang-/Lauf-/Stoppübergänge ergänzt.
- Eigene Gelenkmarken und Referenzgeschwindigkeiten je Körperform; kurze Zwergen-
  und Hobbitbeine werden nicht aus dem 1,80-m-Ranger nur proportional abgeleitet.
- DarkArmored: konkret gemessenen Bodendurchtritt der vorderen Rüstungsbahn
  behoben. Diese Fläche war an Schienbeine gebunden; Saum und Stoffbahn sind jetzt
  vom Beinschwung getrennt. Kein Laufclip für schwere bodenlange Rüstung erzwungen.
- SilverLady: Vollrig-Ärmelversuch wegen deutlicher Faltungen/Dehnungen verworfen.
  Das bestehende geprüfte Dreiknochen-Mesh mit Originalmaterial wird weitergenutzt.
  Atmung, dezente Kopf-/Gesprächsbewegung, Begrüßungsnicken; **kein Gehen/Laufen
  und kein vorgetäuschtes Handwinken**. Gesicht, Haare, Körper und Kleidung nicht
  neu gestaltet. Innenraum-Schattenfreiheit bleibt gesetzt.
- TreeBeing: verwachsene Bodenwurzeln und fest ins Mesh integrierte Reiter erhalten.
  Stamm-/Astbewegung und Astbegrüßung; **kein unsicherer Gehzyklus** übernommen.
- Drei schon geeignete Humanoidenmeshes (WhiteHairedWarrior, DwarfWarrior,
  ElvenArcher) samt Skeleton wiederverwendet. Geometrie, UVs, Gewichte,
  Ruhe-Skelett und Objektmatrix im Blendervergleich exakt identisch. Ihre neuen
  Clips verwenden die alten Skeletons, keine unnötigen Modell-Doppelimporte.
- Alte statische FBX-Materialgraphen verloren teilweise Roughness/Metallic.
  Neue Blender-Arbeitsquellen verwenden wieder die Originalkanäle und gepackte
  Texturen. Unreal verwendet bestehende Materialinstanzen; nur für die bisher
  nicht vorhandene Hobbit-3D-Darstellung waren eigene Importassets nötig.

## Wiederverwendbare Architektur

`UPokeMonsterNPCPresentationData` enthält ausschließlich Präsentation: Mesh,
Materialüberschreibungen, Clips, Höhenmetadaten und Geschwindigkeitsreferenzen.
Validierung prüft Mesh/Skeleton, exakte Clip-Skeleton-Zuordnung, Dauer, Root-Motion,
Materialslots, Geschwindigkeiten und benötigte Kontaktknochen. Ungültige Profile
ersetzen keine funktionierende Darstellung.

Bestehender `PokeMonsterNPC`/RestPoint, DialogSubsystem, Interact-Aktion und
`PokeMonsterNPCVisualActor` bleiben maßgeblich. Gespräch/Begrüßung betrifft den
Oberkörper; die Fußkette wird nicht vom Gesprächsclip überschrieben. Gait-Phase
bleibt zwischen Walk/Run erhalten, Tempo folgt tatsächlicher Bewegung. Optionale
Fußstabilisierung arbeitet auf flachem Boden und verwirft unerreichbare alte Pins.
Kein neuer Dialog-, Quest-, Speicher- oder produktiver NPC-KI-Unterbau.

Profile: `/Game/Characters/NPCs/Library/Profiles/DA_NPC_<ID>`.
Neue Blenderquellen: `Art/Characters/NPCs/<ID>/Source/<ID>_NPCLibrary.blend`,
Hobbit unter seinem vorhandenen Westland/HobbitBase-Quellordner. Die Dateiorganisation
platziert keinen NPC in der Westland-Map. Alle ursprünglichen Quellen bleiben bestehen.

Animations-FBX enthält nur Knochen/Kurven; Geometrie wird einmal im benötigten
Mesh-FBX gehalten. **70 tatsächlich importierte Clips / 28.441 Knochenposen**
vorher/nachher verglichen: maximale Positions-, Skalierungs- und Quaternion-
Komponentendifferenz jeweils **0**. Bei drei wiederverwendeten Skeletons wurde
nur der ursprüngliche Armature-Wrappername wiederhergestellt; deformierende
Knochen und Posewerte bleiben identisch. Vorläufige, ausschließlich in diesem
Auftrag erzeugte Doppelimporte wurden nach Referenz-/Git-Prüfung verworfen;
keine vorher vorhandene Datei wurde dafür entfernt.

## Normaler PIE-Testbereich

Bei jedem gewöhnlichen PIE-Start in VisualV2 verfügbar, nicht nur während Automation.
Mittelpunkt **(-7500, 3000, 0) cm**, elf getrennte Stationen. NPCs sind ausdrücklich
mit TEST gekennzeichnet; ihre Dialoge enthalten keine Quest-/Weltfolgeaktionen.

```text
pm.NPCGround.Go           # Mitte besuchen
pm.NPCGround.Go 1         # Station 1; 1..11 nach obiger Tabelle
pm.NPCGround.Mode idle    # weitere Werte: auto, walk, run
pm.NPCGround.Greet
pm.NPCGround.Return
```

Zum NPC schauen, mit der bestehenden B-/E-Interaktion ansprechen. Dialog regulär
bestätigen. Besuch nur außerhalb Kampf/gesperrter Innenraumzustände. Rückkehranker
bleibt erhalten. Während des Besuchs nutzt Speichern den vorhandenen RAM-Transport;
Rückkehr stellt den ursprünglichen Sitzungsstand her. Keine Save-Kopie oder neue
Save-Datei. Bei anderem bereits aktivem RAM-Test übernimmt der Bereich dessen Schutz
nicht eigenmächtig. Entwicklungskommandos nur Editor-PIE, nicht regulärer Game-/Shipping-
Betrieb. Westland und Biom-Testmap erhalten keinen Testbereich.

Individuelle Ziele/Pausen, Beschleunigung, sanfte Drehungen und Capsule-Sweeps im
freien Testfeld; bei Blockade abbremsen und neues Ziel wählen. Niedrige Randbegrenzung
schützt vor versehentlichem Verlassen. Dies ist **kein vollständiger produktiver
NavMesh-NPC-Pfadplaner für komplexe Gebäude/Treppen**.

## Echte Unreal-Nachweise

33 QHD-Ansichten (2560×1440) aus unveränderter Spielkamera, je vorn/seitlich/hinten,
mit Spieler als Größenreferenz. [Übersicht echter Aufnahmen]({O}/NPC_Bibliothek_QHD_Uebersicht.jpg)
ist eine ausdrücklich beschriftete Montage, kein einzelner Spiel-Screenshot.
[Wanderer vorher]({O}/Wanderer_Before_QHD.png) /
[nachher]({O}/Wanderer_After_QHD.png): gleiche XY-Position und Rotation;
Boden-Settling-Abweichung in Z kleiner als 0,00001 cm. Keine geänderte Kamera.
[Heilerin – tatsächliche Interaktion]({O}/Heilerin_Interaction_QHD.png).

Finale elf Videos: zusammen 106,96 Spielsekunden, **24,62–27,03 echte Bilder je
Spielsekunde**. Keine erfundenen/interpolierten Zwischenbilder. QHD-Spielviewport (2560×1440), bestehende Render-Einstellungen;
aufgezeichneter tatsächlicher Slate-Ausschnitt **2331×1311**, nicht als 2560er
Videodatei ausgegeben. Für dichte Bewegungsprüfung wurde PIE bei der Aufnahme auf
0,25-fache Spielzeit verlangsamt und mit echten Spielzeitstempeln normal schnell
encodiert. Das ist keine Echtzeit-FPS-Messung. Die ersten dünneren Framebufferfolgen
PIE02 (ca. 13 Hz, einschließlich Dialogzuständen) sind ergänzende Diagnosen.

| Figur | QHD-Spielkamera | Vollständiger kurzer Bewegungsclip | Dauer / Bilder / Spielzeit-Abtastung |
|---|---|---|---|
'''+ '\n'.join(media)+f'''

Alle Medien bleiben lokal in `Saved`; keine Kontrollbilder oder Videos auf GitHub.

## Prüfungen

- Editor-Build: `NPCExpansionBuild07`, erfolgreich.
- Elf Blender-Arbeitsquellen erneut geöffnet; genau ein Laufzeitmesh und ein Rig,
  benötigte Rollen vorhanden, wirksame Gewichte normalisiert, verwendete
  Originaltexturen gepackt. Historische unbenutzte Posegruppen zählen nicht als
  zusätzliche deformierende Gewichte.
- Sechs NPC-Automationstests nach Korrektur erfolgreich; vollständige relevante
  Automation und abschließende Rand-/Wiederverwendungsprüfung folgen im finalen QA-Lauf.
- Zwölf vorhandene Maps geprüft, jeweils 0 Fehler / 0 Map-Check-Warnungen. Keine
  neue Map. Ein Map-Check-Ergebnis ist kein allgemeines warnungsfreies Engine-Log.
- Normaler PIE: elf echte NPCs ohne QA-Spawner verfügbar, elf passende B-Ziele,
  Gesprächszustände, Gang-/Lauf-/Begrüßungsfolgen, Richtungen, freie Spielerbewegung.
  B war eine **softwareseitige Slate-Simulation**, kein neuer physischer Hardwaretest.
- Ursprünglicher Wanderer und Heilerin: ursprüngliche Dialogquelle, Blickwendung/
  Präsentationsreaktion, vollständige Heilung und bestehender Save/Load-Rundlauf bestätigt.
- Vorhandene Save-Datei über alle aufgezeichneten Durchläufe SHA-256-identisch:
  `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`.

## Offene Qualitätsgrenzen und Fehlversuche

SilverLady benötigt für überzeugendes Gehen weiterhin gezielte Gewand-/Ärmelarbeit;
TreeBeing eine separate Lösung für verbundene Wurzeln/Reiter. Keine falsche
Vollständigkeitsbehauptung für diese zwei Figuren. Weitere Roben/Rüstungen nutzen
bewusst zurückhaltendes Gehen. Keine Finger-, Gesichtslippen-, Cloth-Simulation,
Terrain-IK oder handanimierten Extrem-Pivots. Subtile Durchdringungen können bei
Nahsicht/Extremposen weitere lokale Arbeit erfordern; Spielkamera und diese Clips
ersetzen keine beliebige Rundum-Animationsfreigabe.

Der erste NPC-Isolationstest rief Engine-BeginPlay unzulässig zweimal auf und
verursachte einen Ensure; Testaufbau korrigiert, nicht der Fehler unterdrückt.
Ein erster PIE-Versuch nach Import/Automation stürzte mit
`pthread_rwlock_init failed with error: 16` ab. Frischer Editor, vollständiger
Funktionslauf, alle elf Bewegungsclips und erneuter PIE-Start nach den korrigierten
NPC-Tests liefen stabil. Die genaue native Ursache des einmaligen Absturzes ist
nicht abschließend bewiesen; frühere Logs bleiben lokal erhalten.

Bekannte externe iOS-Helfer-Warnungen (`idevice_id`, Bad CPU type 86), gegebenenfalls
CoreAudio-Gerätewarnung und belegter Plugin-HTTP-Port werden separat protokolliert.
Keine funktionierenden Controller-Eingaben oder Kamera-/Landschaftssysteme verändert.
Ein strenger QA-Wrapper mit Exit 1 wird nicht als warnungsfrei bestanden dargestellt.

## Git / Schutz

Nur NPC-Quellen, notwendige Bibliotheksassets, gezielte VisualV2-Bindung, Code,
Werkzeuge und Dokumentation. Keine Änderung der Biom-/Westland-Maps, Pokémon-
Assets/Animationen, Incoming-Originale oder vorher vorhandenen 31 unversionierten
Dateien. Lokales Vollbackup `03492bd` und Git-Historie bleiben erhalten.

Commit-/Remote-/LFS-Abschluss wird nach finaler QA ergänzt. Normales `origin/main`,
kein Force-Push; bestätigtes Git-LFS-Budget 0 USD, keine Budget-/Zahlungsänderung.
'''
qa_path=O/'FinalQA.json'
if qa_path.exists():
 qa=json.loads(qa_path.read_text());text=text.replace('Sechs NPC-Automationstests nach Korrektur erfolgreich; vollständige relevante\n  Automation und abschließende Rand-/Wiederverwendungsprüfung folgen im finalen QA-Lauf.', 'Vollständige relevante Automation: **210 Tests, 209 Success, 1 SuccessWithWarnings,\n  0 Fehler, 0 nicht ausgeführt**. Engine Exit 0; strenger Wrapper **Exit 1** wegen\n  zweier externer idevice_id-Warnungen in PokeMonster.BiomeV11.SpeciesPersistence.Garados.\n  Kein Projektfehler, keine Warnungsunterdrückung. Alle sechs NPC-Tests erfolgreich,\n  einschließlich echter Kapselkollision an der Randbegrenzung und Originalmesh-Wiederverwendung.')
 text=text.replace('- Normaler PIE: elf echte NPCs', '- Abschließender normaler PIE nach finalem Build: alle neun Gehfiguren tatsächlich\n  bewegt, zwei bewusst stationär, drei Originalmeshes kontrolliert, echter Spieler-\n  Eingabetest gegen Randkollision, Rückkehr und RAM-Save/Load bestanden.\n- Normaler PIE: elf echte NPCs')
git_path=O/'GitVerification.json'
if git_path.exists():
 info=json.loads(git_path.read_text());assert info['remote_lfs_sha256_verified']
 text=text.replace('Commit-/Remote-/LFS-Abschluss wird nach finaler QA ergänzt.', '**Feature-Commit:** `'+info['feature_commit']+'`, auf dem bestehenden GitHub-Repository nach origin/main gepusht. Alle '+str(info['remote_lfs_count'])+' LFS-Objekte / '+str(info['remote_lfs_bytes'])+' Bytes anschließend direkt vom Remote heruntergeladen und per SHA-256 bestätigt. Lokales main und origin/main nach Feature-Push synchron. Abschlussdokumentation folgt als separater kleiner Dokumentationscommit.')
(R/'Docs/NPC_AUSBAU_MESHY_PRUEFBERICHT.md').write_text(text)
