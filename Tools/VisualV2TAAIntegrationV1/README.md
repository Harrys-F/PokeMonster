# VisualV2 – lokale TAA-Integration V1

Keine neue Map. Die vorhandene GPU-Testmap dient nur der vorausgehenden Bewegungsprüfung.
In VisualV2 wird ein einziges natives `PokeMonsterTemporalAABlendable` mit Gewicht 1
am bestehenden Außen-Postprocess-Volume gespeichert. Es wählt für temporale
Spielansichten TAA und den passenden vorhandenen Temporal-Upscale-Pfad.
Es fügt keinen Bildfilter-/Materialpass hinzu und setzt keine globalen CVars.
Editoransichten, Scene Captures und ausdrücklich deaktiviertes AA bleiben unberührt.
Licht, Lumen, Bloom, Exposure, Originalschatten und Gameplay bleiben erhalten.

## Nachweise erzeugen

Alle Ausgaben unter `Saved/VisualV2TAAIntegrationV1` sind lokal und optional.
Abgeschlossene Nachweise nicht überschreiben; für Wiederholungen eigene Labels bzw.
einen separaten Nachweisordner verwenden. Fehlende lokale Bilder sind kein
fehlendes Build-Asset und kein bestandener visueller Test.

- Development Editor bauen. `LaunchEditor.py <neues_Loglabel>` öffnet ausschließlich
  die vorhandene GPU-Testmap. Auf den aktuellen PID in `Ready.json` warten.
- `RunMotion.py Breite Höhe Qualität ScreenPercentage A|B` zeichnet eine echte
  Eingabesequenz mit Spielkamera auf. A=TSR, B=TAA; Originalschatten.
- `ReviewMotion.py` erzeugt beschriftete, aufeinanderfolgende Originalpixelausschnitte
  aus tatsächlich vorhandenen Frames; Pillow erforderlich. Keine Interpolation.
- `EncodeRecording.swift` encodiert die Frames mit ihren tatsächlichen Zeitstempeln
  über macOS AVFoundation. Aufnahmeaufwand gehört nicht in Performancemessungen.
- `CloseEditor.py` verlangt beendetes PIE und keine ungesicherten Pakete.
- Die einmalige `ApplyTAA.py` verweigert Wiederholung und verlangt die geprüfte
  externe Vorher-Sicherung. Sie erlaubt genau einen AA-Eintrag und prüft alle
  sonstigen erfassten Szenen-/PP-Einstellungen vor dem gezielten Map-Save.
- `LaunchEditor.py <neues_Loglabel> Dev_TestMap_VisualV2`, dann `VerifyMap.py`:
  gespeicherte Map in einem frischen Editor erneut gegen die Signatur prüfen.
- `RunPhase.py PIE|Standalone 1..6`: dreimal Dorf/Wald/Weg, je TSR-Gegenprobe und
  gespeicherte native TAA-Wahl, 5 s Warm-up + 5 s Messung. Gegensinnige Reihenfolge
  in der mittleren Wiederholung. Tatsächliche AA-Methode aus dem Renderthread,
  Viewport-/Target-/ViewRect-Größe und interne Renderer-Fractions werden erfasst.
- Die TSR-Gegenprobe setzt nur das Gewicht dieses Blendables temporär auf 0;
  nach jeder Zeile und am Ende werden ursprüngliche komplette PP-Structs restauriert.
- `Analyze.py` prüft die vollständige Matrix. `--partial` meldet nur abgeschlossene
  Gruppen; es darf keine unvollständige Matrix als vollständige Abnahme ausgeben.
- `RunIntegratedMotion.py Breite Höhe Qualität ScreenPercentage` prüft dieselbe
  Sequenz ausschließlich mit der gespeicherten Wahl; kein AA-Konsolenoverride.
- `RunAcceptance.py PIE|Standalone <neues_Label> Breite Höhe ScreenPercentage`:
  vollständiger vorhandener Enhanced-Input-Fußlauf ohne Test-Teleports mit Dialog,
  Kampf/Fang, Heilhaus, Menü, Sprint und Save/Load. Der tatsächliche Dev-Slot wird
  vorher gesichert und nach Prozess-/PIE-Ende unverändert restauriert. Fehler und
  gleichzeitige Save-Änderungen stoppen die automatische Wiederherstellung.
- Bei geschlossenem Editor `RunQA.py Automation` und `RunMapChecks.py`.

## Mess- und Qualitätsgrenzen

720p Medium 75/100 %, QHD Medium/High 75/100 %, PIE und eigenständige Development-
Prozesse getrennt. `-game` ist kein paketierter Shipping-Build. Interne Pixelmaße
werden aus tatsächlichen Renderer-Fractions abgeleitet, nicht direkt aus einem
SceneColor-Puffer gelesen. GPU-Scopes nicht addieren. Nullzähler nicht als kostenlose
Renderarbeit ausgeben. VSync=0/t.MaxFPS=0 garantieren keine unbegrenzte Metal-
Fensterpräsentation; `rhi.SyncInterval` bleibt unverändert.

Die anfänglichen C1-Fotosegmente sind ausdrücklich verworfen: Ein Foto-Inventar
bearbeitete eine Struct-Proxy-Referenz. Die davor liegenden regulären Messungen
haben unabhängig bestätigte Methoden 4/2. Das korrigierte Inventar arbeitet mit
einem separaten Struct. `CPhotoC1` liefert erneute Bilder; der Analyzer prüft diese
statt der ungültigen Bilder. Alle verworfenen Nachweise bleiben lokal erhalten.

Verdichtete, zeitlich geordnete Bildfolgen und die daraus encodierten Videos sind
keine 60-FPS-Abnahme. TAA kann bei 75 % weicher wirken; feine Vegetation und die
vorhandenen Dither-Revealkanten bleiben Gegenstand visueller Beurteilung.

Bei diesem Durchgang waren die terminalen GPU-CSV-Dateien der vier nativen
Konfigurationen ohne Fotosegmente (C2–C5) leer oder unvollständig. Vollständige
drei Paarvergleiche der Weggruppen werden deshalb unter CRecheck2–CRecheck5 mit
Auslaufzeile erneut erfasst. Alle ursprünglichen 24 Wegabschnitte bleiben erhalten,
werden aber durch 24 vollständige neue Abschnitte ersetzt. Keine Mischung alter
Bildzeiten und neuer GPU-Zähler. Der aktuelle Native-Runner enthält diese Nachmessungen.
Für neue Messkampagnen immer genügend Auslaufzeit vor dem Prozessende vorsehen.
