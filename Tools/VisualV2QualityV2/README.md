# VisualV2 Quality V2 – gezielte Außen-Motion-Blur-Übernahme

Gespeicherte Änderung ausschließlich in `/Game/Maps/Dev_TestMap_VisualV2`:
Außenvolume `V2_OutdoorExposure`: MotionBlurAmount-Override an, Wert 0.
Innenvolume `V2_House_HH_Art_InteriorLighting`: Override an, ursprünglicher Wert 0,5.
Bloom, Schatten, Lumen und sämtliche anderen vollständigen PP-Settings unverändert.
Kein neues Runtime-System und keine Projekt-CVar-Voreinstellung.

## Werkzeuge und Voraussetzungen

Die Skripte sind explizite Entwicklungswerkzeuge, keine Build- oder Gameplay-Abhängigkeit.
Gespeicherte Projektdateien bleiben ohne lokale Reviewbilder und Saved-Diagnosen nutzbar.
Große Nachweise werden außerhalb von Git aufbewahrt; der Prüfbericht enthält die Pfade.

`Startup.py` öffnet nur die zentrale VisualV2 im geprüften schlanken Worktree, verlangt
saubere Pakete und richtet eine begrenzte Jobwarteschlange ein. Start für eine länger
geöffnete Sitzung über `-ExecCmds="py <absoluter Startup-Pfad>"`; der alternative
Unreal-Schalter ExecutePythonScript beendet den Editor anschließend automatisch.
MCP-Port 8010, optional `Saved/VisualV2QualityV2/Endpoint.json` mit anderem Port.
Die Worktree-Pfadguards sind bewusst eng; vor Verwendung in einer anderen Arbeitskopie
muss deren geprüfter Pfad ausdrücklich eingesetzt werden.

`ApplyMotionBlur.py` ist ein einmaliges, gegen erneute Anwendung gesperrtes
Autorenwerkzeug. Es benötigt die vor der Änderung extern gesicherte Map samt
SHA-256-Metadaten und erzeugt BeforeScene/AfterScene. Nicht gegen den bereits
übernommenen Stand erneut anwenden. `VerifyMap.py` prüft diesen Autorenlauf gegen
seinen lokalen BeforeScene-Nachweis; fehlt dieser, ist zuerst eine neue lesende
Bestandsaufnahme erforderlich. Fehlende historische Diagnosen sind kein Grund,
die zentrale Karte zurückzusetzen.

## Abnahme

`RunAcceptance.py <neues Label> <Breite> <Höhe>` verwendet eingebettetes PIE.
`RunNativeAcceptance.py` startet einen separaten Development-Prozess mit Editorbinary
und `-game`, keinen Shipping-Build. Beide benutzen den echten CharacterMovement-
Player und Enhanced Input, acht Richtungen, Sprint, Dialog-/Kampf-/Fang-/Quest-APIs,
Heilhaus, Save/Load und Sprite-Fallback. Keine Test-Teleports im Fußparcours.
Keine physische Controllerprüfung. Die Runlabels und Ausgabepfade müssen neu sein.
Der vorhandene Dev-Slot wird vor jedem Lauf gesichert und danach bytegleich
wiederhergestellt; neu erzeugte Testslots bleiben separat erhalten.

Die zwölf TSV-Pläne messen ausschließlich den endgültigen, unveränderten Kartenstand
in sechs Auflösung/Qualität/Screen-Percentage-Kombinationen je PIE/Standalone.
Dorf, Wald, Weg jeweils drei Wiederholungen, 5 s Warm-up und 8 s Messung.
Kein neuer kausaler Vorher-/Nachher-Vergleich; historische V1-Werte separat behandeln.
Jeder Standalone-Plan enthält einen ausdrücklich ausgeschlossenen CSVDrain-Abschnitt,
damit der bestehende Probe die vorherige GPU-CSV vor dem automatischen Quit schreiben
kann. Kein C++-Probe oder Renderer wurde dafür geändert.

Erst nach allen Grafikläufen Build und vollständige Projekt-Automation ausführen.
`Summarize.py` liest die Rohdaten, `AnalyzeGPU.py` validiert 108 reguläre Segmente,
Auflösungen, Kameraposen und GPU-Zähler. Überlappende GPU-Pässe nicht addieren,
Null-/fehlende Zähler nicht als kostenlose Arbeit interpretieren. Nahezu null liegende
PIE-Renderthreadwerte sind unbrauchbar; native Renderthreadzeit enthält Warteanteile.
Keine Hash-/Archiv-/Buildarbeit parallel zu den Timingfenstern.
