# VisualV2 Material Fix V1 – instanzierte V3-Sträucher

18.10.2026 · Unreal Engine 5.8.2 · MacBook Air M4, 16 GB · macOS/Metal.

## Ergebnis

Der graue Standalone-Fallback der zwei HISM-Strauchgruppen (30 + 28 = 58 Instanzen) ist behoben. Der vorhandene Blattmaster besitzt jetzt die gespeicherte Freigabe `Used with Instanced Static Meshes`. Master und Material Instance wurden neu kompiliert/aktualisiert und gezielt gespeichert. Kein neues Material, keine neue Textur und keine neue Map; bestehende Pfade bleiben erhalten.

Frische PIE-/Standalone-Prüfungen bei 1280×720 und 2560×1440, Medium/High, jeweils 75/100 %. 288 reguläre Messabschnitte sowie 40 separate Spielkamera-Bilder. Die reparierten Sträucher verwenden ihren vorgesehenen Atlas und ihre Maskierung. Build, 48/48 Automationstests, drei Map Checks, vollständiger PIE-Fußlauf und gezielter Mac-Cook erfolgreich. Einschränkungen und anfänglicher Diagnoseabsturz ausdrücklich unten.

## 1. Ausgangslage und nachgewiesene Ursache

Slim-Worktree `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`, Ausgangs-HEAD und direkt geprüftes origin/main `4eed31f208a0fdb5a406e73977516ce034d1e22b`. Vor Beginn nur die ältere unversionierte EnvironmentQualityV1-Testkarte und ihre Werkzeuge vorhanden. Vollbackup und Archiv-Ref bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; die neue Historie basiert nicht darauf. Alle 2.891 vorbestehenden Dateien erfasst, beide Materialdateien zusätzlich extern per SHA-256 gesichert.

Betroffene Gruppen: `V2_Instanced_BushA`/`SM_WLA_WildBush_V3_A` mit 30 und `V2_Instanced_BushB`/`SM_WLA_WildBush_V3_B` mit 28 Instanzen. Blatt-Slot verwendet `MI_WLA_FoliageGroups_V3`, Parent `M_WLA_FoliageGroups_V3`. Die Rinden-Slots bleiben auf `MI_WLA_Bark`. 44 weitere Einzelstrauchkomponenten waren bereits regulär belaubt; keine pauschale Neuverteilung.

Die gespeicherte Mastereigenschaft `used_with_instanced_static_meshes` war false. Frische native Starts vor jeder Diagnose melden ausdrücklich die fehlende InstancedStaticMeshes-Nutzung und den Engine-Defaultmaterial-Fallback. Identische Kameraposition zeigt vor der Korrektur graue instanzierte Flächen in Standalone und belaubte Sträucher in PIE.

Der lokale UE-5.8.2-Quellcode `Runtime/Engine/Private/Materials/Material.cpp`, `UMaterial::SetMaterialUsage`, bestätigt das Verhalten: automatisches Setzen/Kompilieren ist an Editorbetrieb außerhalb einer laufenden Spielsitzung gebunden; der Spielpfad ohne passende Nutzungsfreigabe fällt auf das Defaultmaterial zurück. Die Warnung fordert ein erneutes Speichern. Der ursprüngliche V3-Importer setzte die Instancing-Freigabe nicht; der bisherige Validator kontrollierte nur Masked/TwoSided. Diese konkreten Befunde erklären das Auseinanderlaufen, ohne einen fehlenden Texturimport zu unterstellen.

Der tatsächlich verwendete `Paint`-Atlas `T_WLA_FoliageGroups_V3` ist vorhanden, 2048×2048, sRGB, Mips aus TextureGroup, alpha coverage wie bisher. Tint bleibt (0,94; 0,98; 0,91; 1), Masked/TwoSided, Clip 0,45, Roughness 0,95, Specular 0,05. Ein zusätzlich gemeldeter DefaultTexture-Parameter gehört nicht zu den erfassten Paint-Pfaden der Farbausgabe/Opacity-Maske und wurde nicht verändert. Kein UV-, Normalen-, Geometrie- oder Texturfehler als Ursache nachgewiesen.

## 2. Ausschließlich durchgeführte Korrektur

- `M_WLA_FoliageGroups_V3`: genau das fehlende Instancing-Flag gesetzt, Material neu kompiliert und gespeichert.
- `MI_WLA_FoliageGroups_V3`: aktualisiert, Shader-/Parent-Daten neu aufgebaut und gespeichert; Parameter und Parentpfad unverändert.
- `Tools/ImportWestlandAssetLibraryV3.py`: idempotente Prüfung setzt/kompiliert/speichert dasselbe Flag auch bei bereits vorhandenem GraphReady-Material. Der vollständige Importer wurde hier bewusst nicht ausgeführt, da er Texturen und Meshes reimportieren würde.
- `Tools/ValidateWestlandAssetLibraryV3.py`: vorhandener Validator verlangt zusätzlich die gespeicherte Instancing-Freigabe. Kein Lauf mit veraltetem Kamera-A-Gameplayassert als neue Freigabe ausgegeben.
- Eigene eng begrenzte Diagnose-/Abnahmewerkzeuge unter `Tools/VisualV2MaterialFixV1`. Keine Gameplay- oder Buildabhängigkeit von lokalen Reviewbildern.

Vorher/Nachher-Audit: genau ein Unterschied der geprüften Mastereigenschaften, erfasste Graphwurzeln/Knoten und Einstellungen identisch, sämtliche erfassten Instance-Parameter, Texturen, Parent, Materialreferenzen, Komponenten und Instanzanzahlen identisch. Alle Maps, Geometrie-/Texturassets, C++-Dateien, Player-/NPC-Quellen und Animationen bytegleich. Keine Materialduplikate, neue Schatten-, AA-, Lumen- oder Postprocess-Defaults. Kamera B 2850/−50/−45/35, 140-cm-Player, Gehen 210 und Sprint 315 cm/s unverändert.

## 3. Visuelle Ergebnisse und Kameranachweise

Echte Unreal-Spielkameraaufnahmen, keine Konzeptbilder. Fotos nur in separat ausgeschlossenen Reviewsegmenten, nicht in ausgewerteten Timingfenstern. Skeletal-Animationen für Standbilder pausiert und zurückgegeben; die Idle-Phase zwischen Prozessen ist nicht als pixelidentisch garantiert. Kamera und Ausgabegrößen unabhängig aus dem tatsächlichen PlayerCameraManager/Viewport geprüft. Alle 20 Vorher-/Nachher-Bildpaare besitzen dieselbe Kamera, Rotation, FOV und Ausgabegröße; maximale gemessene Positionsabweichung unter 0,000001 cm.

**Vorher – Standalone, grauer Fallback · QHD High/100 %**

![Vorher – Standalone, grauer Fallback](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C8/Wald_2560_1440_2_10000000.png)

**Nachher – Standalone, ursprünglicher Blattatlas · QHD High/100 %**

![Nachher – Standalone, ursprünglicher Blattatlas](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C8/Wald_2560_1440_2_10000000.png)

**Vorher – PIE, bereits belaubt · QHD High/100 %**

![Vorher – PIE, bereits belaubt](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C8/Wald_2560_1440_2_10000000.png)

**Nachher – PIE, vorgesehene Darstellung erhalten · QHD High/100 %**

![Nachher – PIE, vorgesehene Darstellung erhalten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C8/Wald_2560_1440_2_10000000.png)

Die Sträucher behalten nach der Reparatur die beabsichtigte belaubte Darstellung in beiden Modi; die zuvor sichtbaren opaken grauen Blobs verschwinden durch die wieder korrekt angewendete Blattmaskierung. Das ist keine Entfernung von Geometrie. Keine neue Stilisierung oder Materialverfeinerung. Alle acht Konfigurationen pro Modus besitzen eigene Vorher-/Nachher-Bilder; Dorf/Heilhaus und Weg zusätzlich bei QHD/High/100.

## 4. Performance: Methode und vollständiger Vergleich

Je Zustand/Modus acht feste Konfigurationen, drei Orte (Dorf/Heilhaus, Wald, Weg), je drei Wiederholungen. 5 s Warm-up + 3 s Messung. Je Sitzung genau eine Scalability-Stufe, Auflösung und Screen Percentage; keine Qualitätsumschaltung mit lebenden Reveal-MIDs. Mittlere Wiederholung mit umgekehrter Ortsfolge. Native Prozesse bei geschlossenem Editor; eingebettetes PIE, keine schwebenden PIE-Fenster.

Feste Playerpunkte in cm: Dorf (-4100,450,50,15), Wald (-4300,1550,50,15), Weg (-36,6,-47,1,50,15). Profiling-Teleports sind keine Fußlaufprüfung. Ausgabe/RenderTarget/ViewRect, Primary/Secondary-Fraction und fortlaufende Renderer-Beobachtungen geprüft. Intern bei 75 % 960×540 bzw. 1920×1080, bei 100 % volle Ausgabe; vom Renderer-Treiber abgeleitet, kein direktes Pufferreadback. Fenster-/DPI-Metadaten zusätzlich vorhanden. Stock AA-Methode 4, Lumen-Integration 1, VSM-Rays 4/8; kein altes Integrate2/Rays2-Kandidatenprofil. VSync=0, t.MaxFPS=0, Dynamic Resolution=0; rhi.SyncInterval bleibt 1, mögliche 60-Hz-Präsentationsbegrenzung schneller 720p-Fälle beachten.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei einzelnen Lauf-P95, kein gepooltes P95. GPU ist der verfügbare Unreal-CSV-Zähler. Native Renderthread-Wallzeiten enthalten Warten; nahe null liegende PIE-Renderthread- und RHI-Zähler nicht als kostenlose CPU-/Draw-Call-Arbeit interpretieren. Verschachtelte GPU-Scopes nicht summieren.

Vorher und nachher sind zeitlich aufeinanderfolgende Reihen, nicht interleavte Paare. Kurze Fenster, thermische Drift und ein regulärer erneuter Editor-Build zwischen den Zuständen begrenzen kleine Differenzen. C++-Inhalt ist bytegleich. Insbesondere native Vorher-Bilder enthalten den fehlerhaften opaken Fallback: sie sind nicht bildgleich mit der reparierten Maskierung. Daraus keinen qualitätsgleichen Optimierungsgewinn ableiten. Energie-/Thermalprotokoll ab 08:40:29 UTC: Netzbetrieb/100 %. Für die ersten 720p-PIE-Vorher-Konfigurationen fehlen begleitende Thermalstichproben; keine Temperatur-/Taktmessung oder Dauer-FPS-Zusage.

| Modus | Ausgabe/Qualität/SP | Ort | FPS vorher → nachher | Median ms vorher → nachher | P95 ms vorher → nachher | GPU ms vorher → nachher |
|---|---|---|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 % | Dorf | 52.47 → 51.13 | 19.06 → 19.56 | 23.97 → 26.73 | 17.66 → 18.15 |
| PIE | 1280×720 / Medium / 75 % | Wald | 54.40 → 54.49 | 18.38 → 18.35 | 23.37 → 22.95 | 17.23 → 17.24 |
| PIE | 1280×720 / Medium / 75 % | Weg | 52.22 → 49.51 | 19.15 → 20.20 | 23.67 → 23.02 | 18.00 → 18.37 |
| PIE | 1280×720 / Medium / 100 % | Dorf | 43.43 → 43.33 | 23.02 → 23.08 | 28.15 → 27.95 | 21.35 → 21.90 |
| PIE | 1280×720 / Medium / 100 % | Wald | 44.12 → 44.77 | 22.67 → 22.34 | 27.36 → 27.64 | 20.97 → 21.24 |
| PIE | 1280×720 / Medium / 100 % | Weg | 43.27 → 40.16 | 23.11 → 24.90 | 27.83 → 29.65 | 21.38 → 23.06 |
| PIE | 1280×720 / High / 75 % | Dorf | 38.86 → 41.48 | 25.73 → 24.11 | 28.51 → 27.88 | 21.48 → 21.60 |
| PIE | 1280×720 / High / 75 % | Wald | 42.15 → 43.07 | 23.73 → 23.22 | 28.06 → 26.87 | 20.70 → 20.81 |
| PIE | 1280×720 / High / 75 % | Weg | 36.48 → 42.76 | 27.41 → 23.39 | 30.37 → 27.52 | 23.14 → 21.54 |
| PIE | 1280×720 / High / 100 % | Dorf | 31.02 → 32.20 | 32.24 → 31.06 | 33.70 → 32.71 | 29.96 → 29.63 |
| PIE | 1280×720 / High / 100 % | Wald | 31.40 → 33.20 | 31.85 → 30.12 | 33.51 → 32.46 | 29.28 → 28.46 |
| PIE | 1280×720 / High / 100 % | Weg | 30.71 → 31.92 | 32.57 → 31.33 | 34.06 → 32.95 | 30.60 → 29.44 |
| PIE | 2560×1440 / Medium / 75 % | Dorf | 23.36 → 24.89 | 42.81 → 40.17 | 45.90 → 45.38 | 41.51 → 38.47 |
| PIE | 2560×1440 / Medium / 75 % | Wald | 23.70 → 25.65 | 42.20 → 38.99 | 45.71 → 43.85 | 40.02 → 37.65 |
| PIE | 2560×1440 / Medium / 75 % | Weg | 23.30 → 25.42 | 42.91 → 39.33 | 45.87 → 44.35 | 41.42 → 38.08 |
| PIE | 2560×1440 / Medium / 100 % | Dorf | 15.85 → 17.41 | 63.10 → 57.43 | 65.06 → 64.67 | 61.30 → 56.40 |
| PIE | 2560×1440 / Medium / 100 % | Wald | 16.48 → 17.92 | 60.68 → 55.81 | 63.82 → 62.95 | 58.80 → 54.67 |
| PIE | 2560×1440 / Medium / 100 % | Weg | 16.31 → 17.55 | 61.30 → 56.98 | 64.07 → 61.79 | 59.55 → 55.61 |
| PIE | 2560×1440 / High / 75 % | Dorf | 18.19 → 18.76 | 54.99 → 53.31 | 61.51 → 57.80 | 52.84 → 51.76 |
| PIE | 2560×1440 / High / 75 % | Wald | 18.92 → 19.41 | 52.85 → 51.53 | 59.17 → 58.67 | 50.73 → 49.84 |
| PIE | 2560×1440 / High / 75 % | Weg | 18.05 → 18.63 | 55.41 → 53.69 | 61.11 → 60.23 | 53.50 → 52.21 |
| PIE | 2560×1440 / High / 100 % | Dorf | 11.96 → 13.16 | 83.61 → 75.97 | 87.67 → 82.23 | 81.31 → 72.69 |
| PIE | 2560×1440 / High / 100 % | Wald | 12.05 → 13.11 | 82.99 → 76.29 | 93.50 → 87.17 | 80.83 → 74.19 |
| PIE | 2560×1440 / High / 100 % | Weg | 11.87 → 12.57 | 84.26 → 79.57 | 89.26 → 84.76 | 81.39 → 76.50 |
| Standalone | 1280×720 / Medium / 75 % | Dorf | 59.97 → 60.00 | 16.67 → 16.67 | 16.89 → 16.87 | 13.02 → 12.62 |
| Standalone | 1280×720 / Medium / 75 % | Wald | 60.03 → 60.00 | 16.66 → 16.67 | 16.88 → 16.90 | 12.90 → 12.43 |
| Standalone | 1280×720 / Medium / 75 % | Weg | 60.01 → 60.00 | 16.66 → 16.67 | 16.91 → 16.87 | 13.28 → 12.70 |
| Standalone | 1280×720 / Medium / 100 % | Dorf | 60.00 → 60.00 | 16.67 → 16.67 | 16.85 → 16.88 | 13.95 → 14.16 |
| Standalone | 1280×720 / Medium / 100 % | Wald | 60.02 → 60.03 | 16.66 → 16.66 | 16.90 → 16.92 | 13.36 → 13.57 |
| Standalone | 1280×720 / Medium / 100 % | Weg | 59.99 → 60.02 | 16.67 → 16.66 | 16.88 → 16.89 | 14.21 → 14.41 |
| Standalone | 1280×720 / High / 75 % | Dorf | 60.02 → 60.07 | 16.66 → 16.65 | 16.89 → 17.53 | 13.82 → 14.83 |
| Standalone | 1280×720 / High / 75 % | Wald | 60.03 → 60.00 | 16.66 → 16.67 | 16.89 → 16.89 | 13.32 → 13.83 |
| Standalone | 1280×720 / High / 75 % | Weg | 60.02 → 60.00 | 16.66 → 16.67 | 16.91 → 16.94 | 14.15 → 15.05 |
| Standalone | 1280×720 / High / 100 % | Dorf | 54.49 → 47.95 | 18.35 → 20.86 | 20.01 → 22.92 | 16.96 → 19.23 |
| Standalone | 1280×720 / High / 100 % | Wald | 55.39 → 49.79 | 18.06 → 20.09 | 19.28 → 22.05 | 16.60 → 18.66 |
| Standalone | 1280×720 / High / 100 % | Weg | 53.21 → 46.92 | 18.79 → 21.31 | 20.15 → 23.26 | 17.29 → 19.64 |
| Standalone | 2560×1440 / Medium / 75 % | Dorf | 35.62 → 34.45 | 28.07 → 29.03 | 30.73 → 30.78 | 27.59 → 28.05 |
| Standalone | 2560×1440 / Medium / 75 % | Wald | 36.42 → 36.15 | 27.45 → 27.66 | 29.85 → 29.53 | 26.95 → 26.70 |
| Standalone | 2560×1440 / Medium / 75 % | Weg | 35.66 → 33.90 | 28.04 → 29.50 | 30.53 → 31.71 | 27.94 → 28.24 |
| Standalone | 2560×1440 / Medium / 100 % | Dorf | 25.01 → 22.77 | 39.99 → 43.91 | 41.46 → 47.86 | 38.80 → 42.42 |
| Standalone | 2560×1440 / Medium / 100 % | Wald | 25.51 → 23.83 | 39.20 → 41.97 | 40.59 → 44.01 | 37.76 → 40.38 |
| Standalone | 2560×1440 / Medium / 100 % | Weg | 25.08 → 23.07 | 39.88 → 43.35 | 42.69 → 45.49 | 38.41 → 41.90 |
| Standalone | 2560×1440 / High / 75 % | Dorf | 26.81 → 25.68 | 37.30 → 38.94 | 39.90 → 41.47 | 35.53 → 37.00 |
| Standalone | 2560×1440 / High / 75 % | Wald | 27.61 → 26.62 | 36.22 → 37.56 | 37.95 → 40.08 | 34.51 → 36.08 |
| Standalone | 2560×1440 / High / 75 % | Weg | 26.60 → 25.24 | 37.59 → 39.62 | 39.59 → 42.88 | 35.89 → 37.65 |
| Standalone | 2560×1440 / High / 100 % | Dorf | 17.66 → 17.22 | 56.63 → 58.07 | 60.31 → 65.12 | 54.81 → 55.79 |
| Standalone | 2560×1440 / High / 100 % | Wald | 18.48 → 17.64 | 54.12 → 56.68 | 57.67 → 59.79 | 52.41 → 54.83 |
| Standalone | 2560×1440 / High / 100 % | Weg | 17.69 → 17.07 | 56.52 → 58.58 | 58.64 → 61.76 | 54.55 → 56.60 |

Die vollständigen Game-/Renderthread-Zeiten, alle Einzelmediane und verfügbaren GPU-Pässe stehen in den verlinkten JSON-/CSV-Daten. Die Reparatur dient korrekter Darstellung, nicht einer behaupteten FPS-Optimierung. Historische native Messungen mit grauen Sträuchern dürfen weiterhin nicht als korrekt belaubtes Endbudget gelten. Die neue Nachher-Reihe ist eine geeignetere Ausgangsbasis für weitere TSR-/Materialtests; keine solche Optimierung wurde hier übernommen.

## 5. Funktion, Build und Grenzen

Vollständiger echter, automatisiert über Enhanced Input gegangener PIE-Rundweg bei QHD/Medium/75 %: **284.56 m**, 206.4 s, ohne Testteleports. Gebäuderelocation ist die unveränderte normale Spielfunktion. Maximal gemessene Geschwindigkeit 315.00 cm/s einschließlich Sprint. Wanderer-/Liora-Dialog, Quests/Archiv, Wildfang, Trainerkampf, Menü, Brücke/Wald, Heilhaus rein/raus und diagonal, Heilung/PP, Checkpoint, Save/Load, acht Richtungen, Sprint und Sprite-Fallback geprüft. Der Slim-Worktree besaß vor dem Test keinen Dev-Slot. Der erzeugte Testslot wurde gesichert und der ursprüngliche Zustand ohne Slot wiederhergestellt; keine Restaurierung eines nicht vorhandenen Originalfiles behauptet. Keine physische Controllerprüfung oder menschliche Videoabnahme behauptet.

Mac Development Editor Build erfolgreich; tatsächlich Modul kompiliert und gelinkt. Vollständige Projekt-Automation: 48 Success, 0 SuccessWithWarnings/Failed/NotRun/InProcess. Map Checks: zentrale VisualV2, separate GPU-Diagnosekarte und WestlandAssetLibrary. Vollständige zentrale Szenensignatur identisch; keine schmutzigen Map-/Content-Pakete am Ende. Gezielter Mac-Cook der QualityV3-Assets samt benötigten harten Abhängigkeiten erfolgreich, keine paketierte Shipping-/Distributionsprüfung.

Die Vorher-Starts zeigen die reproduzierte Instancing-Warnung; alle acht reparierten nativen Starts wurden geprüft: 0 Instancing-Fallback-Warnungen, 0 Material-/Shaderfehler, 0 Fatalfehler. Der Cook meldet nur den allgemeinen MCP-Lizenzhinweis (auch in der Abschlusszusammenfassung), keine Material-/Shaderfehler. Allgemeine vorhandene Engine-Bootstrap-Condition-Meldungen, idevice_id/Bad-CPU-, Audio-/MCP-/Shutdown-HTTP-Hinweise nicht unterdrückt und nicht mit fehlgeschlagenen strukturierten Projekttests verwechselt.

**Anfängliche Diagnoseprobleme:** Der erste PIE-Messversuch änderte Scalability mit lebenden Birken-Reveal-MIDs und löste eine UE-UniformExpressionCache-Assertion mit Absturz aus. Kein Asset gespeichert, null gültige Segmente, vollständig ausgeschlossen. Daraufhin jede Qualitätsstufe vor einem neuen Spielstart gesetzt; kein Engine-/Gameplaycode als vermeintliche Reparatur geändert. HTTP-Steuerung nach Neustart lief in einen Timeout; alle gültigen Sitzungen wurden über die Editor-Python-Dateiwarteschlange geführt. Ein Monitor bewertete ein reguläres natives Ende (Exit 0, Complete-Datei und vollständige Daten) fälschlich als Fehler; Guard korrigiert, fertige Läufe geprüft und erhalten, nicht überschrieben. Selbstschließende Python-Startversuche bleiben als Setup-Logs erhalten. Kein Force Quit, Reset oder Verwerfen fremder Editorpakete.

Die Laufzeit-Qualitätsumschaltung mit vorhandenen Reveal-MIDs bleibt ein bekannter Engine-/Präsentationsfehler außerhalb dieses Materialfixes. Die Reparatur behebt weder die allgemeinen QHD-GPU-Engpässe noch alle vorhandenen dunklen Waldfiguren/TSR-Artefakte. Keine pauschale Art-/60-FPS-/Shipping-Freigabe.

## 6. Dateien, Nachweise und Sicherung

Alle ursprünglichen Maps und Quellen geschützt, Vollbackup unverändert. Nur zwei bestehende Materialpakete und zwei zugehörige Import-/Validierungsskripte geändert. Neue Werkzeuge/32 statische Pläne unter `Tools/VisualV2MaterialFixV1`, dieser Bericht. Große Kontrollbilder, Rohdaten, Cookausgaben und Logs außerhalb Git. Kein .ini-, C++-, Gameplay-, Mesh-, UV-, Textur-, Animations- oder Kollisionsasset geändert.

[Dateischutz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/ProtectionAudit.json)

[Sicherung/SHA](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/BeforeFiles.json)

[Ursprünglicher Materialaudit](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Before_MaterialAudit.json)

[Reparierter Materialaudit](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/After_MaterialAudit.json)

[Graphvergleich vorher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Before_Graph.json)

[Graphvergleich nachher](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/After_Graph.json)

[Auflösungs-/Kameraprüfung aller 288 Abschnitte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Validation.json)

[Alle Einzelwerte](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Measurements.json)

[96 Drei-Lauf-Zusammenfassungen](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Summary.json)

[48 Vorher-/Nachher-Konfigurationen samt CPU-Zeiten](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Comparison.csv)

[Fußlauf](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Acceptance/MaterialFix_QHD_Foot/FootTest.json)

[Save-Wiederherstellung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Acceptance/MaterialFix_QHD_Foot/SaveRestored.json)

[Finale Szene und Map Checks](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/FinalAudit.json)

[Build](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Build.log)

[Automation](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Automation/Result.json)

[Cook](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Cook/Result.json)

[Shader-/Warnungsprüfung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/WarningAudit.json)

[20 identische Vorher-/Nachher-Kamerapaare](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/PhotoValidation.json)

[Externe Nachweise/SHA](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/EvidenceManifest.json)

[Git-/LFS-Abschluss](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/GIT_ABSCHLUSS.md)

### Alle 40 Vergleichsbilder

| Zustand | Modus | Konfiguration | Datei |
|---|---|---|---|
| Before | PIE | [1280, 720, 1, 75] | [1280_720_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C1/1280_720_1_7500000.png) |
| Before | Standalone | [2560, 1440, 1, 100] | [Wald_2560_1440_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C6/Wald_2560_1440_1_10000000.png) |
| After | Standalone | [1280, 720, 1, 75] | [Wald_1280_720_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C1/Wald_1280_720_1_7500000.png) |
| After | PIE | [1280, 720, 1, 100] | [Wald_1280_720_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C2/Wald_1280_720_1_10000000.png) |
| Before | PIE | [1280, 720, 2, 100] | [Wald_1280_720_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C4/Wald_1280_720_2_10000000.png) |
| Before | Standalone | [1280, 720, 2, 75] | [Wald_1280_720_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C3/Wald_1280_720_2_7500000.png) |
| After | PIE | [2560, 1440, 2, 75] | [Wald_2560_1440_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C7/Wald_2560_1440_2_7500000.png) |
| After | Standalone | [1280, 720, 2, 100] | [Wald_1280_720_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C4/Wald_1280_720_2_10000000.png) |
| After | Standalone | [1280, 720, 2, 75] | [Wald_1280_720_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C3/Wald_1280_720_2_7500000.png) |
| Before | PIE | [1280, 720, 2, 75] | [Wald_1280_720_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C3/Wald_1280_720_2_7500000.png) |
| Before | Standalone | [1280, 720, 2, 100] | [Wald_1280_720_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C4/Wald_1280_720_2_10000000.png) |
| After | PIE | [2560, 1440, 1, 75] | [Wald_2560_1440_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C5/Wald_2560_1440_1_7500000.png) |
| After | Standalone | [2560, 1440, 1, 100] | [Wald_2560_1440_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C6/Wald_2560_1440_1_10000000.png) |
| Before | PIE | [2560, 1440, 1, 100] | [Wald_2560_1440_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C6/Wald_2560_1440_1_10000000.png) |
| Before | Standalone | [1280, 720, 1, 75] | [Wald_1280_720_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C1/Wald_1280_720_1_7500000.png) |
| After | PIE | [2560, 1440, 2, 100] | [Wald_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C8/Wald_2560_1440_2_10000000.png) |
| After | PIE | [2560, 1440, 2, 100] | [Dorf_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C8/Dorf_2560_1440_2_10000000.png) |
| After | PIE | [2560, 1440, 2, 100] | [Weg_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C8/Weg_2560_1440_2_10000000.png) |
| Before | PIE | [2560, 1440, 1, 75] | [Wald_2560_1440_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C5/Wald_2560_1440_1_7500000.png) |
| Before | Standalone | [1280, 720, 1, 100] | [Wald_1280_720_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C2/Wald_1280_720_1_10000000.png) |
| After | PIE | [2560, 1440, 1, 100] | [Wald_2560_1440_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C6/Wald_2560_1440_1_10000000.png) |
| After | Standalone | [2560, 1440, 1, 75] | [Wald_2560_1440_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C5/Wald_2560_1440_1_7500000.png) |
| Before | PIE | [2560, 1440, 2, 100] | [Wald_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C8/Wald_2560_1440_2_10000000.png) |
| Before | PIE | [2560, 1440, 2, 100] | [Dorf_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C8/Dorf_2560_1440_2_10000000.png) |
| Before | PIE | [2560, 1440, 2, 100] | [Weg_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C8/Weg_2560_1440_2_10000000.png) |
| After | Standalone | [2560, 1440, 2, 100] | [Wald_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C8/Wald_2560_1440_2_10000000.png) |
| After | Standalone | [2560, 1440, 2, 100] | [Dorf_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C8/Dorf_2560_1440_2_10000000.png) |
| After | Standalone | [2560, 1440, 2, 100] | [Weg_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C8/Weg_2560_1440_2_10000000.png) |
| Before | Standalone | [2560, 1440, 2, 75] | [Wald_2560_1440_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C7/Wald_2560_1440_2_7500000.png) |
| After | PIE | [1280, 720, 2, 75] | [Wald_1280_720_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C3/Wald_1280_720_2_7500000.png) |
| After | PIE | [1280, 720, 2, 100] | [Wald_1280_720_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C4/Wald_1280_720_2_10000000.png) |
| After | Standalone | [2560, 1440, 2, 75] | [Wald_2560_1440_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C7/Wald_2560_1440_2_7500000.png) |
| Before | PIE | [2560, 1440, 2, 75] | [Wald_2560_1440_2_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C7/Wald_2560_1440_2_7500000.png) |
| Before | Standalone | [2560, 1440, 2, 100] | [Wald_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C8/Wald_2560_1440_2_10000000.png) |
| Before | Standalone | [2560, 1440, 2, 100] | [Dorf_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C8/Dorf_2560_1440_2_10000000.png) |
| Before | Standalone | [2560, 1440, 2, 100] | [Weg_2560_1440_2_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C8/Weg_2560_1440_2_10000000.png) |
| After | Standalone | [1280, 720, 1, 100] | [Wald_1280_720_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_Standalone_C2/Wald_1280_720_1_10000000.png) |
| After | PIE | [1280, 720, 1, 75] | [Wald_1280_720_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_After_PIE_C1/Wald_1280_720_1_7500000.png) |
| Before | PIE | [1280, 720, 1, 100] | [Wald_1280_720_1_10000000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_PIE_C2/Wald_1280_720_1_10000000.png) |
| Before | Standalone | [2560, 1440, 1, 75] | [Wald_2560_1440_1_7500000.png](/Users/harry/Documents/Codex/PokeMonster_VisualV2_MaterialFix_V1_2026-10-18/Evidence/Screenshots/VGB1_MaterialFix_Before_Standalone_C5/Wald_2560_1440_1_7500000.png) |

Die Korrektur und benötigten Werkzeuge sind nach visueller Prüfung, Index-/Diff-/LFS-Kontrolle im Commit `59d18f0004b67764f1a445fd5164b5e7e3c4e6fa` regulär nach origin/main gepusht; Remote-Hash bestätigt. Beide neuen LFS-Pakete (zusammen 34.393 Bytes) wurden unabhängig heruntergeladen und per SHA-256 verifiziert. Der Bericht wird getrennt gesichert; beide Hashes und der abschließende Git-/LFS-Status stehen im externen Git-Abschluss. Keine Testbilder/-videos auf GitHub, kein Force-Push, keine Käufe oder Budgetänderungen.
