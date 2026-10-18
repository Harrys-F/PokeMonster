# VisualV2 TAA/TSR und weiche Bodenschatten – isolierter Versuch

Es wird **keine Map erzeugt oder gespeichert**. Ausschließlich die vorhandene
`/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` wird zur Laufzeit untersucht.
Die zentrale VisualV2, alle Lichtquellen, Postprocess-Volumes und Originalassets
bleiben unverändert. Die Strauchmaterialkorrektur des aktuellen HEAD ist Voraussetzung.
Kein automatischer Start beim Laden der Map und keine Änderung von Projektdefaults.

## Vier Varianten

- `SoftAA:A`: TSR (Methode 4), Originalschatten.
- `SoftAA:B`: TAA (Methode 2), Originalschatten.
- `SoftAA:C`: TSR, neue Bodenprojektionen und komponentenweise ausgeschaltete
  Vegetations-/Figurenschatten.
- `SoftAA:D`: TAA, dieselbe Schattenvariante.

Die nativen Development-Befehle `pm.SoftShadows.Test 1` und `0` sind explizite
Versuchswerkzeuge. Nur die oben genannte Spiel-/PIE-Welt ist freigeschaltet.
Bei Stop/Ende werden die ursprünglichen CastShadow-Werte wiederhergestellt.
Gebäude, DirectionalLight, Skylight, Lumen, Exposure und Bloom werden nicht verändert.
Keine neuen Gameplay-Collider oder Bewegungsregeln.

Der Test nutzt einen gemeinsamen texturlosen Deferred-Decal-Master mit zwei
Material Instances. Dichte: Baum 0,45; Figur 0,50. Breite weiche, leicht gelappte
Ränder ohne Blatt-/Astkonturen. Keine aufwendige Echtzeit-Stoff-/Schatten-Simulation.
Baumprojektionen sind statisch. Figuren folgen nach dem Actor-/Physics-Tick und vor dem Rendern pro Frame; Bodenhöhe und Normale
werden höchstens alle 0,05 s per bestehender WorldStatic-Kollision ermittelt und
zwischen Abfragen auf der lokalen Bodenebene fortgeführt. Verdeckte/deaktivierte
Quellfiguren werden berücksichtigt. Neue später gespawnte Figuren werden in diesem
begrenzten Prototyp noch nicht automatisch registriert.

## Ablauf

1. Development Editor bauen. `LaunchEditor.py <neuer_Logname>` starten; auf das
   frische `Saved/VisualV2AASoftShadowsV1/Ready.json` warten.
2. `Control.py VerifyAssets.py`. Neue Materialien sind bereits versioniert;
   `PrepareAssets.py` ist nur der einmalige Erzeuger und verweigert vorhandene Ziele.
3. `RunStudy.py PIE`: acht feste Qualitäts-/Auflösungskonfigurationen, frisches
   eingebettetes PIE pro Konfiguration, alle vier Faktoren interleavt. Editor endet
   nur bei sauberem Zustand. Keine schwebenden PIE-Fenster.
4. Bei geschlossenem Editor `RunStudy.py Standalone`. Standalone bedeutet
   UnrealEditor Development `-game`, **kein paketierter Shipping-Build**.
5. `Analyze.py` validiert tatsächliche Viewport-/Target-/ViewRect-Dimensionen,
   Renderer-Fractions, Kamera und unveränderte erfasste Licht-/PP-Werte.
6. Frischen Editor für `RunCost.py PIE` und `RunAcceptance.py <A|B|C|D> <neues_Label>
   2560 1440` starten. Letzteres sichert/restauriert den tatsächlichen Dev-Slot,
   nutzt den vorhandenen vollständigen Enhanced-Input-Fußlauf und schreibt echte,
   zeitlich protokollierte Bewegungsframes. Keine Profiling-Teleports im Fußlauf.
7. Editor sauber schließen; `RunQA.py Automation`, optional `RunQA.py Cook` und
   `RunMapChecks.py`. Map Checks erfolgen in getrennten Prozessen, ohne Map-Saves.

Messpläne: 1280×720 und QHD, Medium/High, je 75/100 %, drei Orte und drei Läufe.
Pro Segment 3 s Warm-up + 3 s Messung. Foto-/Drainzeilen (Repeat >=90) sind von
Timingstatistiken ausgeschlossen. Kurze Messfenster und thermische Drift begrenzen
kleine Differenzen. FPS nahe 60 können trotz VSync=0/t.MaxFPS=0 präsentationsbegrenzt
sein. GPU-/CPU-Scopes nicht addieren; Nullzähler sind kein kostenloser Renderpass.

`BeginCost.py` isoliert bei identisch abgeschalteten Objektschatten die Rasterkosten
sichtbarer/unsichtbarer Decals. Die unterschiedlichen Repeatbereiche werden explizit
protokolliert. Zusätzliche ProfileGPU-Aufnahmen sind keine Timingmessungen.

## Bekannte Grenzen

- Wegfall echter Schatten verändert auch die Eigenverschattung der Vegetation.
  Unveränderte Lichtwerte allein beweisen deshalb keine identische Lichtwirkung.
- Die Projektion ist kein physikalischer Schattenwurf auf höhere Objekte.
- Sehr unebenes Gelände, Höhenkanten, viele Überlappungen und neu gespawnte Figuren
  benötigen zusätzliche Abnahme. Die Testwelt ist überwiegend flach.
- Laufzeitwechsel High→Medium mit lebenden Reveal-MIDs hat bereits in früheren
  Untersuchungen eine UE-Shadercache-Assertion ausgelöst. Qualität immer vor PIE
  setzen; keine solche Umschaltung als bestandene Prüfung ausgeben.
- Lokale Kontrollbilder, Logs und Messdaten liegen unter Saved bzw. im externen
  Prüfbereich; sie sind keine erforderlichen Build-/Gameplay-Dateien.

Maßgeblich für Resultate, tatsächliche Fehler und Freigabeempfehlung ist der
zugehörige Prüfbericht. Keine automatische Übernahme der Versuchsvariante in VisualV2.

Nach der statischen Matrix wurde ausschließlich der Zeitpunkt der Figuren-Nachführung korrigiert. `RunFollowSpotcheck.py` liefert zusätzliche identische QHD/High/100%-Kontrollen der finalen Fassung; die vollständige statische Matrix bleibt getrennt ausgewiesen.
