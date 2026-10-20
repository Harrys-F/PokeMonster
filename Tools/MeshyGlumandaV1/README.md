# Meshy-Glumanda V1 – kontrollierter Einzelimport

Nur `/Users/harry/Developer/PokeMonster`. Vollständiger Ergebnisbericht:
`Docs/MESHY_GLUMANDA_INTEGRATION_V1_PRUEFBERICHT.md`.
Original: `Art/Characters/Creatures/Incoming/Glumanda.glb`; ausschließlich diese
Incoming-Datei ist Teil dieses Imports. Andere Modelle nicht mitverarbeiten.

## Tatsächlich verwendeter Ablauf

1. `InspectSource.py` in Blender 5.2.2 im Hintergrund: GLB lesen, Front/Profil und
   tatsächliche Mesh-/Materialdaten prüfen. Original nie speichern/verändern.
2. `PrepareModel.py`: neue eigene `.blend`, unveränderte Referenzcollection,
   einheitliche 0,60-m-Normalisierung, originales Schwanzflammenmesh isolieren,
   23 anatomisch angepasste Bones. Erstimport-Schutz nicht umgehen.
3. `RefineWeights.py`: Bone Heat auf einer nur temporär verschweißten Arbeits-
   hülle, Gewichte zurück auf das unveränderte Render-Mesh; Kopf, Sohlen und
   Übergang der Schwanzflamme kontrolliert behandeln. Kein Render-Remesh.
4. `AnimateExport.py`: sieben eigene Clips, sagittale Bein-IK, Walk 22 cm/s,
   Run 36 cm/s, FBX und gepackte Blenderquelle. Nur eigene Arbeitsdatei und
   eigene Exporte werden geschrieben. Nicht blind nach manuellen Änderungen
   erneut ausführen: diese Schritte erzeugen Gewichte/Animationen neu.
5. `ValidateSource.py`: Datei erneut öffnen, Gewichte/Clips/Topologie prüfen und
   Walk-FBX erneut importieren. Aufruf der Blender-Werkzeuge beispielsweise:
   `/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/MeshyGlumandaV1/ValidateSource.py`.
6. `Intake.json` mit `Tools/CreaturePipelineV2/preflight.py` prüfen. Vorhandene
   Zielassets führen beim späteren Wiederholen absichtlich zu einer Ablehnung;
   das ist kein Auftrag, freigegebene Assets zu überschreiben. Front/Profil
   wurden durch tatsächliche Renderprüfung bestätigt, keine menschliche
   Designfreigabe wird vorgetäuscht.
7. `ImportAssets.py` nur in sauberem Unreal-Editor über die bestehende
   ArtControl-Warteschlange: Kandidat in eigenem MeshyV1-Namespace, eigene
   Skeleton-/Animationsassets, Originaltexturen, tatsächliche Socket-Transformation
   einschließlich Skalierung im Effekt-Offset kompensieren. Der Importer lehnt
   einen bereits abgeschlossenen Import ab; teilweise eigene Importe werden nur
   nach Prüfung ihres Quellpfads wiederverwendet. Kein Originalasset reimportiert.
8. `ReviewUnrealCandidate.py` in PIE zeigt den Kandidaten über `SetPresentation`
   ohne Änderung von Speziesdaten: sieben Clips, acht Richtungen, native Run-Mischung,
   QHD-Aufnahmen und Socket-Prüfung. Beendigung restauriert die Speziesdarstellung.
   Ergebnisse/Medien bleiben unter ignoriertem `Saved/MeshyGlumandaV1`.
9. `ApplyCandidate.py` ist eine einmalige, bewachte Änderung ausschließlich von
   `DA_Zunderlauf.Visuals.Presentation` nach bestandener Kandidatenprüfung.
   Art-ID, Kampfwerte, Save-Format, Collider und Karten bleiben erhalten.
10. `RunGameplay.py <neues_alphanumerisches_Label>` führt den bestehenden echten
    Enhanced-Input-Rundweg aus. Originalen Dev-Save gezielt vorübergehend halten
    und bytegleich restaurieren. Keine parallelen manuellen Save-Vorgänge.
    Ein fehlgeschlagener Lauf bleibt sichtbar; bei Abbruch zuerst Original-Save
    und Testzustand prüfen. Der Annäherungspunkt folgt der tatsächlichen wilden
    Kreatur und führt nicht durch ihren Kollider.
11. `CheckMaps.py` fordert lesende Map Checks aller vorhandenen Karten an;
    tatsächliche Fehler-/Warnungszahlen anschließend aus dem Editorlog auswerten.
    `ValidateScope.py` prüft Originale, Karten, Save und Backup-Verweise.
12. Build, gesamte Automation, Quellen, Diff und LFS prüfen; gezielt sichern.

## Grenzen

Das Meshy-Original enthält UV-Seams und kleine offene Stellen. Kein pauschales
Lochschließen, Remesh, Decimation oder Material-Neudesign wurde durchgeführt.
LBS-Kniekompression, schnelle Übergänge und Drehungen bleiben visuelle
Feinabnahmepunkte. Analytische Standphasenprüfung ersetzt keine universelle
Foot-Sliding-Garantie. Keine neuen Gesichtsanimationen, LOD-, Cook-, Standalone-
oder Performancefreigabe. Die alte Zunderlauf-V1-Darstellung bleibt verfügbar.
`PrepareEvidence.py` verarbeitet echte Unreal-Aufnahmen zu Ausschnitten/GIF;
das GIF ist eine zeitlich geordnete Bildfolge, keine Echtzeit-Videoaufnahme.
