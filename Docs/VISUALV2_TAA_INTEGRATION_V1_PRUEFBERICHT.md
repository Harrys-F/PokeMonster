# VisualV2 TAA Integration V1 – Prüfbericht

## Ergebnis

Die zentrale `/Game/Maps/Dev_TestMap_VisualV2` verwendet jetzt für ihre tatsächliche Spielansicht **TAA mit unveränderten Originalschatten**. Keine neue Map erstellt. Die zuvor getrennt geprüften Shadow-Blob-Varianten sind nicht aktiviert. Globaler Projektstandard und alle anderen bestehenden Maps bleiben unverändert.

Der begrenzte Bewegungsvergleich auf der vorhandenen `/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1` ergab keinen auffälligen zusätzlichen dauerhaften Figuren-Nachzieheffekt, der eine Übernahme blockiert hätte. TAA ist bei 75 % sichtbar weicher. Feines Blattwerk und die bestehenden Dither-Revealkanten sind auch damit nicht vollständig ruhig. Keine Behauptung einer artefaktfreien oder menschlich freigegebenen 60-FPS-Videoabnahme. Anschließend wurde die gespeicherte Wahl ohne AA-Konsolenoverride erneut bewegt und unter echten Renderbedingungen geprüft.

## Ausgangsstand und Schutz

Slim-Worktree `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`. Anfangs-HEAD und direkt geprüfter origin/main `a0d6109cb3f2154f3de81bec3082319174f5de39`. Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt auf altem lokalem main und Archiv-Ref unverändert und außerhalb der neuen Remote-Historie.

2999 vorbestehende versionierte/unversionierte Dateien inventarisiert. Vorhandene unversionierte `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap` und `Tools/VisualV2EnvironmentQualityV1/` weder verändert noch aufgenommen. Unreal war zu Beginn geschlossen; keine fremde unsichere Sitzung verworfen. VisualV2 vor Änderungen extern bytegleich gesichert: [Originalmap](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Dev_TestMap_VisualV2_Before.umap), [Dateiinventar](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/BeforeFiles.json). Keine Originalquelle, Animation, Vegetation oder Gameplaydatei zurückgesetzt/gelöscht.

Vorher-SHA `c979ab35f10a0e9ea9a69479c10793783a9d03164116b0afe02967e8693cfe35`; nachher `441e9dc5592db4b7e551e861099dd3e82bbb146c4df5be90f498e0ad62256140`. Vollständiger erfasster Szenen-/PP-Vergleich bei 1348 Actors: genau ein neuer AA-Eintrag am vorhandenen `V2_OutdoorExposure`; alle anderen Einstellungen identisch. Frisch erneut geöffnete Datei gegen dieselbe Nachher-Signatur geprüft. [Änderungsaudit](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/MapChangeAudit.json).

## Technische Integration

UE 5.8.2 bietet die AA-Methode nicht als Feld des `PostProcessSettings`-Structs an. Deshalb ein kleines natives `UPokeMonsterTemporalAABlendable` über die vorhandene Engine-Schnittstelle `IBlendableInterface`, als map-eigenes Objekt am vorhandenen ungebundenen Volume, Gewicht 1. Keine neue Actor-/Gameplay-Architektur und kein zusätzlicher Postprocess-Materialpass.

Es setzt ausschließlich `FSceneView::AntiAliasingMethod` auf TAA und den zugehörigen vorhandenen Screen-Percentage-Modus passend zu `r.TemporalAA.Upsampling`. Editoransichten, Scene Captures und bewusst deaktiviertes AA bleiben unberührt. Keine globale CVar-/Projektconfig-Änderung; `r.AntiAliasingMethod` bleibt 4. Der unabhängige Renderthread-Beobachter bestätigt die tatsächlich gerenderte Methode **2** bei integrierter Wahl und **4** bei der TSR-Gegenprobe. Der globale CVar-Wert allein wäre deshalb kein Nachweis.

Lichtquellen einschließlich Skylight, Positionen, Farben, Intensitäten, Lumen-GI/Reflexionen, Bloom, Belichtung, Nebel, alle ursprünglichen Schatten, Vegetationsdichte/-geometrie, Kamera B 2850/−50/−45/35, Player 140 cm, Gehen 210 cm/s, Sprint 315 cm/s und Gameplay bleiben erhalten. Außen-MotionBlurAmount 0 und Innenwert 0,5 bleiben unverändert. Das Blendable wird auch im Innenraum geerbt; dessen Beleuchtung wird nicht umgestellt.

Zur gezielten Deaktivierung genügt später das Entfernen bzw. Gewicht 0 dieses einen Eintrags; es gibt keinen weltweiten Quality-Schalter. Das ist keine zusätzliche automatische Rückfallregel im Spiel.

## Bewegungsprüfung und echte Aufnahmen

Vorausgehend zwölf reale Eingabesequenzen auf der bestehenden GPU-Testmap: 720p Medium 75/100 %, QHD Medium/High 75/100 %, jeweils TSR/TAA mit Originalschatten. Tatsächliche Spielkamera, Gehen, Sprinten, Stop, diagonale Umkehr, Kamera-Lag, NPC-Idle und Gespräch. Zwei explizite Anfangspositionierungen pro Kurzsequenz, deshalb keine Behauptung eines teleportfreien Fußlaufs für diese Aufnahmen. Separate vollständige Gameplay-Fußläufe unten.

Danach sechs Kurzsequenzen mit der gespeicherten integrierten Wahl ohne AA-Konsolenoverride. Der Originalrecorder für Ranger V3 wurde nicht verändert; neues explizites Development-Aufnahmewerkzeug liest ausschließlich den tatsächlichen Spiel-Framebuffer. JPEG-Frames mit tatsächlichen Spiel-/Wandzeitstempeln; Videos ohne erfundene Zwischenbilder. Aufnahme-/Encodingkosten sind von den Leistungsmessungen ausgeschlossen. Die veröffentlichten Waldvideos enden vor der expliziten Standortpositionierung zum NPC; sie zeigen keine als Fortbewegung ausgegebene Test-Teleportation. Zusätzliche echte Tür-/Innenraumsequenzen aus dem teleportfreien Gameplay-Rundweg liegen separat vor. Insgesamt 18 auf Vollständigkeit geprüfte Bildfolgen mit 6437 tatsächlichen Frames. Auflösung und Zeitabstände in [MotionInventory](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/MotionInventory.json).

Proceed to scoped integration and revalidation. No conspicuous additional persistent player trails/double contours seen in the reviewed successive frames. TAA is softer at 75%, fine foliage/dither remains imperfect in both methods. This is not a claim of artifact-free 60fps video.

Kein auffälliger neuer lang anhaltender Ghost-Trail im geprüften Bereich. Kleine temporale Kantenunruhe/Ditherreste sind weiterhin sichtbar, speziell an feinen Blättern, Haaren und Schattenkanten. 75 % verliert etwas Detail gegenüber 100 %. Es wird keine Perfektion behauptet. Diese Entscheidung gilt für die geprüfte feste Kamera und vorliegenden Figuren/Materialien; spätere neue Materialien oder Windanimationen benötigen eigene Prüfung. Niedrige QHD-Bildrate und ReadPixels-Aufwand begrenzen die Aufnahmefrequenz. Die Videos enthalten keine künstliche Bewegungsglättung.

## Messmethode

Integrierte zentrale VisualV2, kein Ersatzlevel als Ergebnis ausgegeben. 1280×720 Medium 75/100 %, 2560×1440 Medium und High jeweils 75/100 %. PIE und eigenständiges UnrealEditor Development `-game` bei geschlossenem Editor getrennt, kein paketierter Shipping-Build.

Drei feste Orte: Dorf/Heilhaus (−4100,450,50,15), Wald (−4300,1550,50,15), Weg (−36,6,−47,1,50,15) cm. Je drei interleavte Paare, mittlere Wiederholung in umgekehrter Reihenfolge. 5 s Aufwärmen + 5 s Messung pro Abschnitt; 240 reguläre Abschnitte aufgezeichnet; 216 vollständig ausgewertete Abschnitte und 72 Drei-Lauf-Gruppen. Vierundzwanzig alte Wegabschnitte aus vier Gruppen werden durch vierundzwanzig vollständige Nachmessungen ersetzt (Begründung unten). Die Gegenprobe deaktiviert vorübergehend ausschließlich das gespeicherte AA-Blendable und nutzt TSR, anschließend vollständige ursprüngliche PP-Einstellungen restauriert. Keine Beleuchtung-/Schatten-/Material-/Vegetationsdiagnose gleichzeitig.

Renderer-Methode, Viewport, RenderTarget, ViewRect und fortlaufende Renderer-Fractions in jedem regulären Abschnitt verifiziert. 75 % intern 960×540 bzw. 1920×1080, 100 % volle Ausgabegröße. Interne Maße aus beobachteten Treiber-Fractions abgeleitet, kein direkter SceneColor-Pufferreadback. Fenster/DPI/aktive Präsentation gesondert protokolliert.

VSync=0, t.MaxFPS=0, Dynamic Resolution=0; `rhi.SyncInterval` unverändert. Werte nahe 60 FPS können durch Metal-Fensterpräsentation begrenzt sein. Originale Scalability-Profile vor frischem PIE; kein Live-High→Medium-Wechsel. Zwischen Profilen ändern sich deren normale Qualitätsvorgaben, innerhalb jedes AA-Vergleichs sind alle Nicht-AA-Werte gleich.

FPS = 1000 / Median der drei Laufmediane. P95 = Median der drei Lauf-P95, kein gepooltes P95. Kurze Messfenster begrenzen kleine Unterschiede und garantieren keinen Dauerbetrieb. Game-/Renderthreadzähler enthalten teils Wartezeit/Nullwerte; GPU-Scopes sind verschachtelt und werden nicht summiert. Null-Draw-Call-Zähler nicht als kostenlose Renderarbeit interpretiert. Thermische Stichproben {'nominal': 687}, Energiezustand im Rohprotokoll. Keine unabhängigen Celsius-/Taktwerte; kleine Steuer-/Auswertungsprozesse und Zeitdrift begrenzen die Genauigkeit.

## Vorher/Gegenprobe und integrierte TAA – gemessene Werte

Alle Zeiten ms, jeweils Median aus drei Läufen. TSR-Gegenprobe derselben integrierten Map, keine historischen, abweichend gemessenen FPS als kausaler Vergleich.

| Modus | Ausgabe / Profil / SP | Ort | FPS TSR → TAA | Bildzeit TSR → TAA | P95 TSR → TAA | GPU TSR → TAA |
|---|---|---|---:|---:|---:|---:|
| PIE | 1280×720 / Medium / 75 % | Dorf | 54.02 → 59.71 | 18.51 → 16.75 | 22.17 → 21.04 | 17.55 → 15.73 |
| PIE | 1280×720 / Medium / 75 % | Wald | 55.18 → 59.99 | 18.12 → 16.67 | 21.94 → 17.11 | 17.23 → 15.29 |
| PIE | 1280×720 / Medium / 75 % | Weg | 52.22 → 59.14 | 19.15 → 16.91 | 22.93 → 20.28 | 18.33 → 15.90 |
| PIE | 1280×720 / Medium / 100 % | Dorf | 43.81 → 50.31 | 22.83 → 19.88 | 27.61 → 23.99 | 21.87 → 18.79 |
| PIE | 1280×720 / Medium / 100 % | Wald | 44.62 → 52.56 | 22.41 → 19.03 | 27.14 → 23.15 | 21.55 → 18.23 |
| PIE | 1280×720 / Medium / 100 % | Weg | 42.33 → 50.44 | 23.62 → 19.83 | 28.34 → 24.09 | 22.68 → 18.89 |
| PIE | 2560×1440 / Medium / 75 % | Dorf | 26.96 → 30.58 | 37.09 → 32.70 | 45.62 → 35.02 | 35.83 → 31.67 |
| PIE | 2560×1440 / Medium / 75 % | Wald | 27.23 → 31.08 | 36.73 → 32.18 | 45.04 → 35.20 | 35.75 → 31.45 |
| PIE | 2560×1440 / Medium / 75 % | Weg | 26.86 → 30.07 | 37.23 → 33.26 | 46.11 → 35.98 | 36.13 → 32.38 |
| PIE | 2560×1440 / Medium / 100 % | Dorf | 18.36 → 23.76 | 54.47 → 42.09 | 63.75 → 47.28 | 53.11 → 40.54 |
| PIE | 2560×1440 / Medium / 100 % | Wald | 18.95 → 24.39 | 52.78 → 41.00 | 61.09 → 47.14 | 51.49 → 40.03 |
| PIE | 2560×1440 / Medium / 100 % | Weg | 18.41 → 23.62 | 54.33 → 42.34 | 64.07 → 48.22 | 52.83 → 41.01 |
| PIE | 2560×1440 / High / 75 % | Dorf | 20.22 → 26.66 | 49.45 → 37.51 | 55.80 → 46.10 | 47.59 → 35.54 |
| PIE | 2560×1440 / High / 75 % | Wald | 20.73 → 27.37 | 48.24 → 36.53 | 55.40 → 44.83 | 46.72 → 34.74 |
| PIE | 2560×1440 / High / 75 % | Weg | 19.89 → 25.93 | 50.27 → 38.57 | 58.81 → 46.62 | 48.81 → 36.61 |
| PIE | 2560×1440 / High / 100 % | Dorf | 14.66 → 18.45 | 68.20 → 54.19 | 77.71 → 62.30 | 66.71 → 51.99 |
| PIE | 2560×1440 / High / 100 % | Wald | 14.76 → 19.26 | 67.74 → 51.91 | 80.13 → 61.88 | 65.98 → 50.41 |
| PIE | 2560×1440 / High / 100 % | Weg | 14.02 → 18.25 | 71.33 → 54.79 | 83.79 → 62.80 | 69.67 → 52.42 |
| Standalone | 1280×720 / Medium / 75 % | Dorf | 93.48 → 103.57 | 10.70 → 9.66 | 11.78 → 11.42 | 10.21 → 9.09 |
| Standalone | 1280×720 / Medium / 75 % | Wald | 97.41 → 109.28 | 10.27 → 9.15 | 11.30 → 11.39 | 9.92 → 8.64 |
| Standalone | 1280×720 / Medium / 75 % | Weg | 92.35 → 98.68 | 10.83 → 10.13 | 11.87 → 12.01 | 10.13 → 9.73 |
| Standalone | 1280×720 / Medium / 100 % | Dorf | 64.71 → 79.79 | 15.45 → 12.53 | 17.26 → 14.74 | 14.57 → 11.72 |
| Standalone | 1280×720 / Medium / 100 % | Wald | 66.66 → 83.37 | 15.00 → 11.99 | 16.52 → 13.72 | 14.20 → 11.18 |
| Standalone | 1280×720 / Medium / 100 % | Weg | 74.58 → 85.03 | 13.41 → 11.76 | 14.54 → 13.59 | 12.59 → 11.07 |
| Standalone | 2560×1440 / Medium / 75 % | Dorf | 34.44 → 46.18 | 29.04 → 21.66 | 31.89 → 23.61 | 28.00 → 20.58 |
| Standalone | 2560×1440 / Medium / 75 % | Wald | 35.64 → 47.30 | 28.06 → 21.14 | 31.20 → 23.48 | 26.99 → 20.14 |
| Standalone | 2560×1440 / Medium / 75 % | Weg | 44.34 → 56.96 | 22.55 → 17.56 | 24.39 → 19.63 | 21.70 → 16.76 |
| Standalone | 2560×1440 / Medium / 100 % | Dorf | 23.32 → 31.52 | 42.88 → 31.72 | 46.39 → 36.93 | 41.81 → 30.50 |
| Standalone | 2560×1440 / Medium / 100 % | Wald | 23.57 → 32.73 | 42.42 → 30.56 | 46.26 → 33.53 | 41.32 → 29.54 |
| Standalone | 2560×1440 / Medium / 100 % | Weg | 28.89 → 39.81 | 34.62 → 25.12 | 36.28 → 26.49 | 33.65 → 24.15 |
| Standalone | 2560×1440 / High / 75 % | Dorf | 25.54 → 33.15 | 39.16 → 30.17 | 42.27 → 32.53 | 37.33 → 28.02 |
| Standalone | 2560×1440 / High / 75 % | Wald | 25.62 → 33.94 | 39.04 → 29.46 | 41.88 → 31.72 | 37.25 → 27.33 |
| Standalone | 2560×1440 / High / 75 % | Weg | 22.69 → 28.99 | 44.08 → 34.49 | 49.33 → 39.68 | 41.88 → 32.23 |
| Standalone | 2560×1440 / High / 100 % | Dorf | 17.09 → 23.48 | 58.50 → 42.59 | 64.75 → 46.49 | 56.38 → 40.65 |
| Standalone | 2560×1440 / High / 100 % | Wald | 17.23 → 23.86 | 58.04 → 41.91 | 65.28 → 45.76 | 56.10 → 39.88 |
| Standalone | 2560×1440 / High / 100 % | Weg | 16.65 → 22.72 | 60.07 → 44.02 | 65.23 → 47.19 | 57.87 → 41.76 |

## Aktuelle Restkosten im nativen QHD/High/100-Wald

| Zähler | ms |
|---|---:|
| GPUTime | 39.878 |
| GameThreadTime | 2.322 |
| RenderThreadTime | 41.929 |
| GPU/LumenScreenProbeGather | 10.636 |
| GPU/LumenSceneLighting | 0.976 |
| GPU/ShadowProjection | 6.947 |
| GPU/ShadowDepths | 2.535 |
| GPU/Basepass | 3.417 |
| GPU/TAA | 1.673 |

RenderThreadTime ist hier eine Wallzeit einschließlich GPU-/Present-Warten, kein reines CPU-Budget. GPU-Scopes überlappen bzw. sind verschachtelt und werden nicht addiert. Alle ausgewerteten Fenster waren laut Telemetrie aktiv (Anteil 1,0). Die hohen 720p-Unreal-Framezahlen sind Engine-Durchsatzmessungen, keine separat gemessene physische Monitor-Präsentationsrate.

## Verbleibender Performancebedarf

TAA ersetzt keinen vollständigen QHD-Optimierungsdurchgang. Insbesondere native QHD/High/100 erreicht im geprüften Wald noch keine garantierten 30/60 FPS. Lumen-GI, Originalschatten und Material-/Auflösungsarbeit bleiben erhebliche Budgets. Verfügbare GPU-/Game-/Render-/Schatten-/GI-Zähler je Gruppe und einzelne Laufwerte im vollständigen JSON; keine verschachtelten Scopes addieren. Keine weitere Environment-Optimierung in diesem Auftrag. Zuerst visuelle Nutzerprüfung der TAA-Darstellung, danach getrennte gezielte Untersuchungen mit unveränderter Beleuchtung und fairen Paarvergleichen.

## Gameplay und technische Prüfung

- Integrated_PIE_QHD_Medium100: vollständiger Enhanced-Input-Fußlauf **284.41 m**, 205.2 s, maximal 315.00 cm/s; bestanden, kein Testteleport. Dev-Slot nach Prüfung auf ursprünglichen Zustand zurückgegeben (anfangs vorhanden: False).
- Integrated_Standalone_720p_Medium75: vollständiger Enhanced-Input-Fußlauf **272.64 m**, 222.0 s, maximal 315.00 cm/s; bestanden, kein Testteleport. Dev-Slot nach Prüfung auf ursprünglichen Zustand zurückgegeben (anfangs vorhanden: False).
- Integrated_Standalone_QHD_Medium100: vollständiger Enhanced-Input-Fußlauf **292.37 m**, 217.4 s, maximal 315.00 cm/s; bestanden, kein Testteleport. Dev-Slot nach Prüfung auf ursprünglichen Zustand zurückgegeben (anfangs vorhanden: False).

Vorhandener Wanderer-Dialog/Quest, Liora, Wildkampf/Fang, Team-/Menülogik, Archivabschluss, Heilhaus gerade und diagonal, Innenraum und Heilerin/HP/PP/Checkpoint, Save/Load, Bewegung in acht Richtungen, Sprint, Collision und Sprite-Fallback über den bestehenden Prüfablauf. Keine manuelle Controllerprüfung behauptet.

Mac Development Editor Build1 (Aufnahmehilfsmittel) und Build2 (AA-/Probe-Fassung) und Build3 (ausschließlich korrigierter Test-Zeitstempel) erfolgreich. Vollständige Automation: **{'succeeded': 49, 'succeededWithWarnings': 0, 'failed': 0, 'notRun': 0, 'inProcess': 0}**. Der neue Test prüft den echten AA-Callback einschließlich Gewicht 0, Editor-/Capture-Ausschluss, unveränderter globaler AA-Einstellung sowie Kamera/Bloom/Exposure. Drei Map Checks: zentrale VisualV2, bestehende GPU-Testmap und WestlandAssetLibrary; jeweils 0 Fehler/0 Warnungen. Frisch erneut geladene VisualV2 stimmt mit der gespeicherten Nachher-Signatur überein.

## Fehlversuche und Grenzen

Der erste Automationslauf hatte 48 bestehende Erfolge und einen fehlgeschlagenen neuen Test: In dessen künstlicher View-Family fehlte der von Unreal verlangte explizite Zeitstempel (CVS.bTimesSet). Testaufbau korrigiert, produktive AA-/Probe-Funktionen unverändert, danach vollständiger Lauf wiederholt. Der fehlgeschlagene Lauf bleibt separat unter Automation_InitialFixtureFailure erhalten.

Die erste Videokodierung konnte im sandboxbeschränkten Prozess den nativen AVFoundation-Encoder nicht starten (OSStatus −12903); Quelldaten und fehlgeschlagener Ausgang blieben erhalten. Derselbe Encoder arbeitete im autorisierten Prozess erfolgreich. Keine Unreal- oder Modellkorrektur dafür.

Zwei terminale native CSV-Zählerdateien (C4/C5, jeweils Abschnitt 17 auf dem Weg) blieben leer; zwei weitere aus C2/C3 (Abschnitt 17) waren unvollständig und ohne auswertbaren finalen Zählerheader. Die vorhandenen Bildzeit-/Auflösungs-/AA-Telemetrien wurden nicht um erfundene GPU-Werte ergänzt. Stattdessen vollständige drei Paarvergleiche der vier Weggruppen unter identischen Konfigurationen mit Auslaufzeile erneut gemessen. Alle vierundzwanzig ursprünglichen Wegabschnitte dieser vier Gruppen aus der finalen Auswertung ausgeschlossen und durch vierundzwanzig vollständig geprüfte Nachmessungen ersetzt. Exakter I/O-/Exitgrund nicht weiter bewiesen; Rohdateien unverändert erhalten.

Die ersten C1-Fotos waren ungültig: Das Foto-Inventar bearbeitete einen Python-Struct-Proxy und entfernte zur Textauswertung temporär den AA-Eintrag. Die unabhängige tatsächliche Renderer-Methode erkannte 4 statt 2. Die regulären Abschnitte 0–17 davor sind korrekt bestätigt und bleiben getrennt gültig. Foto-Inventar korrigiert: neues unabhängiges Struct per Textimport. CPhotoC1 in frischer Sitzung erneut aufgenommen und mit Methode 2/4 geprüft. Keine ungültigen Bilder in finalen Vergleichen, keine Änderung der gespeicherten Map durch das Foto-Inventar. Fehlversuche lokal erhalten. Ein anfänglicher Analyse-Indentationsfehler wurde ohne Projekt-/Messdatenänderung korrigiert. System-Python ohne Pillow; vorhandene gebündelte Python-Laufzeit genutzt, nichts installiert.

Aufnahmevideos beruhen auf tatsächlichen Bildern, nicht auf Blender oder Konzeptbildern. Keine 60-FPS- oder menschliche Videoabnahme. Kein Shipping-/Cook-Performancebeleg, keine Hardware-Kernelanalyse, keine exakte Temperaturmessung. Standalone protokolliert bei jedem Start 58 Python-Fehlerzeilen aus experimentellen Engine-Toolsets: ToolsetDefinition/AgentSkill sind im -game-Prozess nicht exponiert. Der vollständige Meldungs-Fingerprint ist exakt identisch zu einer bereits vor dieser Aufgabe vorhandenen nativen AA-Studien-Baseline. Keine zusätzlichen Fehler unseres Python-Werkzeugs oder Material-/Shader-/Instancing-Fehler in den finalen Läufen. Diese vorhandenen Startfehler wurden weder behoben noch unterdrückt; sie bleiben ein offener Engine-/Toolset-Punkt und sind keine fehlerfreie Shipping-Abnahme. Allgemeine weitere Engine-/MCP-/Audio-/idevice-Meldungen bleiben ebenfalls in den Logs und im externen WarningAudit erhalten. Fehler nicht unterdrückt.

## Dateien, Bilder und Git

- Map: `Content/Maps/Dev_TestMap_VisualV2.umap` (Git LFS).
- AA: `Source/PokeMonster/Rendering/PokeMonsterTemporalAABlendable.h/.cpp`.
- Development: eigener AA-Review-Recorder, eng begrenzte Erweiterung des vorhandenen Performance-Probes um tatsächliche Renderer-AA und isolierte Blendable-Gegenprobe.
- Test: `Source/PokeMonster/Tests/PokeMonsterTemporalAATest.cpp`.
- Reproduzierbare Werkzeuge/Pläne: `Tools/VisualV2TAAIntegrationV1/`.
- Bestätigte technische Entscheidung in `Docs/TECHNIK.md` und `Docs/ENTSCHEIDUNGEN.md`.

- [Vollständige Messergebnisse](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/Summary.json)
- [Unabhängige Validierung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/Validation.json)
- [Echte Vergleichsfotos](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/Photos.json)
- [Bewegungsinventar](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence/MotionInventory.json)
- [Alle lokalen Nachweise](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Evidence)
- [Git-Abschluss](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/GIT_ABSCHLUSS.md)

## Direkt zugängliche Bildvergleiche und echte Videos

**Standalone QHD/High/100: links TSR, rechts integriertes TAA**

![Standalone QHD/High/100: links TSR, rechts integriertes TAA](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/ImageReview/Standalone_QHD_High100_AB.png)

**Gespeicherte TAA-Wahl gegenüber geprüftem B bei Bewegung**

![Gespeicherte TAA-Wahl gegenüber geprüftem B bei Bewegung](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/ImageReview/Integrated_2560_1440_Q2_SP100.png)

- [TSR, QHD/High/100, echte Waldsequenz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos/TSR_QHD_High100.mp4)
- [Integriertes TAA, QHD/High/100, echte Waldsequenz](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos/TAA_Integrated_QHD_High100.mp4)
- [Integriertes TAA, 720p/Medium/75](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos/TAA_Integrated_720p_Medium75.mp4)
- [Echter Standalone-Heilhausübergang, QHD](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos/Door_Integrated_Standalone_QHD_Medium100.mp4)

Alle neun erfolgreich encodierten Videos und deren Quellen: [Videomanifest](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/Videos/Manifest.json). Keine Zwischenbildsynthese. Aufnahmelast nicht für FPS-Angaben verwendet. Drei zusätzliche Türsequenzen aus den vollständigen Fußläufen sind neben den 18 Kurzsequenzen separat vorhanden.

Kontrollbilder, Videos, Rohdaten und Caches werden nicht hochgeladen. Ausschließlich geprüfte benötigte Dateien gezielt committen; reguläre Pushes und Remote/LFS-Prüfung. Der Vollbackup bleibt unverändert. Endgültige Commit-Hashes im verlinkten Git-Abschluss und in der Abschlussantwort.

Git-Status vor Sicherung:

```text
 M Content/Maps/Dev_TestMap_VisualV2.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp
?? Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
?? Source/PokeMonster/Development/PokeMonsterTAAReviewCapture.cpp
?? Source/PokeMonster/Rendering/
?? Source/PokeMonster/Tests/PokeMonsterTemporalAATest.cpp
?? Tools/VisualV2EnvironmentQualityV1/
?? Tools/VisualV2QualityV2/__pycache__/
?? Tools/VisualV2TAAIntegrationV1/
```
## Verifizierte GitHub-Sicherung

Implementierungscommit: `f463d46059d2fdce5aa4e63473fee28fab0dc3dd` (`render: integrate map-scoped TAA in VisualV2`), 63 gezielt geprüfte Pfade. Regulärer Push auf `origin/main` erfolgreich; Remote direkt mit `ls-remote` bestätigt. Kein Force-Push.

Indexprüfung: 357.458 Bytes normaler Git-Dateiinhalte, eine neue LFS-Map mit 3.260.579 Bytes. Alle normalen Einzeldateien unter der GitHub-Grenze; normaler Transfer weit unter der zusätzlichen 1-GiB-Vorgabe. Keine Videos, Kontrollbilder, Rohmessungen oder Caches aufgenommen. `git diff --cached --check` vor dem Commit ohne Befund.

Das neue LFS-Objekt `441e9dc5592db4b7e551e861099dd3e82bbb146c4df5be90f498e0ad62256140` wurde nach dem Push separat über GitHub LFS heruntergeladen: Bytezahl und SHA-256 stimmen exakt. Anschließender LFS-Dry-Run ohne ausstehendes Objekt. Der zusätzliche Upload beträgt 3.260.579 Bytes, nicht die Gesamtbelegung des Kontos. Live-Abrechnung und tatsächlich verbleibendes Kontingent sind über die verfügbaren Zugänge nicht zuverlässig auslesbar; deshalb keine Behauptung einer gemessenen Gesamtbelegung oder Kostenabrechnung. Keine Käufe, Budgetänderungen oder Quota-Fehler.

Dieser Bericht wird anschließend separat committed und regulär gepusht. Seine endgültige Commit-ID und die abschließenden Statusprüfungen stehen in [GIT_ABSCHLUSS.md](/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/GIT_ABSCHLUSS.md). Kein zirkuläres Eintragen der eigenen Commit-ID in die versionierte Datei.

Vorhandene unversionierte EnvironmentQuality-V1-Testkarte und deren Werkzeugordner bleiben unberührt. Der lokale, nicht aufgenommene Python-Cache unter `Tools/VisualV2QualityV2/__pycache__/` bleibt ebenfalls erhalten. Vollbackup und Archiv-Ref `03492bd96b4dba44692f675c19d5f11abfa86b4b` unverändert; dieser Commit ist kein Vorfahr der neuen Remote-Historie.
