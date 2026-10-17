# Ranger V2: ausdrücklich ausgelöste Prüfwerkzeuge

Dieser Ordner gehört zum Performance-/Ranger-V2-Versuch. Keine Produktions-Gameplay-Änderung und kein automatischer Start. Originalkarte, NPC-Identität, Kamerawerte und Originalassets bleiben erhalten.

## Reproduzierbare Messung

`PokeMonsterPerformanceProbe.cpp` registriert nur Development-Konsolebefehle:

- `pm.Perf.Run <absoluter TSV-Pfad>`: stellt tatsächliche SceneViewport-Ausgabegröße ein, protokolliert Ausgabe- UND Render-Target-Größe, scoped Medium/75 %, VSync aus/uncapped. Warm-up und Messdauer aus TSV. Erfasst native Framezeiten und Unreal CSV/GPU-Daten. Snapshot/Wiederherstellung der geänderten Komponenten, Materialien, Schatten, CVars und Playerposition.
- `pm.Perf.Stop`: kontrollierter Abbruch und Wiederherstellung.
- `pm.Perf.AuditLODs`: tatsächliche Renderdreiecke/-vertices, LOD-Grenzen und ungefährer LOD-Renderdaten-Speicher. Optional `FixV2` ausschließlich für das neue `SK_Ranger_NPC_V2`: importierte LODs ohne nachgeschaltete automatische Engine-Reduktion bauen. Keine V1-Reparatur.

Die festen Profilierungspositionen sind Messpositionen, kein behaupteter Fußlauf. `FootTestV2.py` läuft separat in einer frischen PIE-Sitzung mit Enhanced-Input-Bewegung. Nur die existierende reguläre Heilhaus-Relocation ist dabei zulässig.

Vor einem Probe-Start setzt `StartProbe.py` den Ranger in der wegwerfbaren PIE-Welt ausdrücklich auf **V1**, sodass `V1` und jeder A/B-Kontrollzustand auch in einer V2-Testkarte tatsächlich V1 sind. V2-Zeilen tauschen nur das Präsentationsmesh temporär aus. Keine Messung parallel mit Blender, Build oder Automation ausführen.

`Summarize.py` wertet native Frames und den abschließenden Unreal-CSV-Header aus: CSV erweitert den Header zur Laufzeit. Nullzähler sind keine Messung von null Kosten. Passzeiten können verschachtelt/überlappend sein und dürfen nicht unkritisch summiert werden.

## Kandidaten

`BuildRangerV2.py` erzeugt die **verworfene** ungeschützte Reduktion. `BuildRangerV2Protected.py` schützt Kopf und Hände mit empirisch geprüfter Decimate-Gewichtung. Auch der geschützte 10k-Kandidat wurde wegen sichtbarer Kragenschäden verworfen. Arbeitsmaster: `Ranger_NPC_V2_Protected.blend`, Runtime nur 55k und 24k. Kein neues Rig, keine neuen Spieleranimationen, keine neuen Texturen.

Importskripte ersetzen ausschließlich die in diesem Versuch neu angelegten V2-Assets. Die frühen Fehlerläufe und Renderings bleiben als Diagnose erhalten; sie sind keine freigegebenen Alternativen. `CreatePerfMap.py` zeigte, dass `save_map` eine Kopie schreibt, aber die aktuelle Welt nicht umbenennt. `FinishPerfMap.py` lädt deshalb explizit die neue Kopie und speichert nur diese. Der Originaldatei-Hash wird abschließend geprüft.

## Grenzen

LOD-ScreenSize ist eine Bildschirmgrenze, keine feste Meterdistanz. Tatsächliche Distanzen/PredictedLOD in den Prüfmanifesten verwenden. Der 10k-Kandidat ist nicht Teil des Unreal-SkeletalMesh. Keine automatische Freigabe für die Baseline-Karte.

## Maßgeblicher Unreal-Kandidat und Reimport

**Nur `SK_Ranger_NPC_V2_Clean` ist der endgültig weiter geprüfte Kandidat.** Der erste `SK_Ranger_NPC_V2`-Import ist verworfene Diagnose. `Unreal/` und `UnrealFinal/` zeigen fehlgeschlagene LOD-Pose-Nachweise; finale Aufnahmen liegen in `UnrealAccepted/`. `AfterA/AfterB/PairedA/PairedB` sind verworfene V2-Messungen. Finale Reihen beginnen mit `Final`, ergänzt um `Village...`. Die V1-Baselines und V1-Faktortests bleiben gültig.

**Importer konsistent halten:** Erstimport, Custom-LOD-Import und Custom-LOD-Reimport verwenden den Legacy-FBX-Pfad. `Interchange.FeatureFlags.Import.FBX` nur während des Imports auf 0 setzen und im `finally` wiederherstellen. Ein kontrollierter Vergleich am selben neuen Clean-Asset zeigte: Standard-Reimport unter dem anderen Importpfad erzeugt eine falsche LOD1-Pose; Legacy-Reimport desselben Assets stellt die richtige Pose wieder her. `ConsistentReimport.py` und `NativeAnim_ConsistentReimport/` sind der tatsächliche Reimport-/Animationsnachweis. Keine globale Importer-Umstellung speichern.
