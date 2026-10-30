# Garados Wasserbewegung V2

**Abschluss 30.10.2026:** Technisch umgesetzt und geprüft. Horizontaler Wasser-Rig, elf Clips, geschwindigkeitsabhängige Körperwellen, Kurven und weiches Beobachten; ursprüngliche Land-/Kampfdarstellung erhalten. Finaler Build15,314/314 Tests mit strengem Exit0, zwölf fehler-/warnungsfreie Map Checks, echte PIE-/Native-/Save-/Neustart-/Entwicklungsprüfungen bestanden. Stabile30FPS und eine hochfrequente abschließende künstlerische Bewegungsfreigabe sind ausdrücklich nicht nachgewiesen.

## Auftrag und Ausgangsstand

Projekt `/Users/harry/Developer/PokeMonster`, Unreal 5.8.2, Apple M4/Metal, VisualV2. Ausgangscommit `0d1c0a19e093c91d0500062d5352f41ff5de16dd`, main/origin/main synchron. Die bereits vorhandenen lokalen Rendering-Änderungen in `Config/DefaultEngine.ini` gehören Harry und bleiben unangetastet und außerhalb dieses Commits. Keine neue Map, kein Worktree, keine Landschafts- oder Renderingänderung.

## Quelle und nachgewiesene Ursache

Einzige Modellquelle ist Harrys `Art/Characters/Creatures/Incoming/Garados.glb`, SHA-256 `ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9`. Die bestehende Arbeitsquelle `Garados/Source/Garados_Meshy_V1.blend` hat SHA-256 `634be2dec767ac422cb8ae406cb92892578c095e370dd3ec55ad731a52344836`. Beide Originale bleiben unverändert.

Die aufgerichtete Haltung stammt aus der bereits S-förmigen Meshy-Geometrie und dem ursprünglichen Rig mit zwölf Bones; die alte Schwimmbindung verwendete die vorhandene Gehbewegung. Sie ist keine fehlerhafte Actor-Pitch-Rotation. Eine bloße horizontale Actor-Rotation oder ein unverändertes Entrollen der alten Gewichte verursachte starke Verzerrungen und wurde verworfen.

Die Originaloberfläche besteht aus 24.049 Vertices, 26.298 Dreiecken und dreizehn getrennten Oberflächenteilen einschließlich ursprünglicher Flossen, Hörner und weiterer Merkmale. Die technische Wasser-Ableitung verwendet exakt diese Flächen, UVs und Materialien. Keine neue Pokémon-Geometrie, keine neuen Texturen. Die Positionen vorhandener Vertices werden für die horizontale technische Ruhepose korrigiert; eine Behauptung unveränderter Vertexpositionen wäre falsch.

## Technische Ableitung und Animation

`Tools/GaradosWaterV2/PrepareWaterSource.py` erzeugt die eigene Wasser-Arbeitsdatei `Source/Garados_Water_V2.blend`. Ein kontinuierlicher Längsparameter auf der verbundenen Original-Körperoberfläche verhindert die Verwechslung nah beieinanderliegender Windungen. Abgetrennte ursprüngliche Merkmale bleiben an ihren ursprünglichen Körperansätzen. Zwölf Glättungsschritte, höchstens vier Bone-Einflüsse je Vertex, 20 Wirbelsäulensegmente plus Kopf und Root (22 Bones). Der Kopf erhält einen ruhigen Übergang in den Vorderkörper. Diagnose und Wiedererzeugung stehen in `Tools/GaradosWaterV2/README.md`.

Elf exportierte Skeletal Animations: SwimIdle, SwimSlow, SwimNormal, SwimFast, SwimTurnLeft, SwimTurnRight, SwimObserve, SwimAttack, SwimHit, SwimFaint und SwimHappy. Keine neue Animationsarchitektur: Die vorhandene `PokeMonsterCreatureAnimInstance`/ihr Proxy mischt Geschwindigkeit, Kurve und Beobachtung. Die Wellen werden offline als Bone-Keyframes erstellt; kein zusätzlicher Actor-Tick und kein neues AnimBP.

| Parameter | Wert / Wirkung |
|---|---|
| Langsam / normal / schnell | 35 / 70 / 125 cm/s Referenz |
| Wellenperiode | 1,6 s bei normaler Rate; langsame/schnelle Rate und Amplitude werden gemischt |
| Ruhe / Beobachtung | 2,4-s-Clips mit dezenter Bewegung |
| Aufrichten / Absenken | jeweils 2,5 s kontinuierliche Mischung; 3 s Nachhaltezeit |
| Vorderkörper | bis ca. 50° aufgerichtet, Hinterkörper bleibt unter Wasser |
| Richtungswechsel | 35°/s, 70°/s²; Körperkurve und verzögertes Schwanzfolgen |
| Kataloglänge | bestehende 650 cm unverändert; ausgerollte Körperachse ohne Kopf ca. 588 cm |
| Nav-Freiraum | 400 cm Radius; sämtliche 587 exportierten Animationsframes haben höchstens ca. 376,3 cm horizontalen Radius |
| Wasser | bestehende Oberfläche 4,2 cm, Garados-Tiefgang 180 cm; zusätzlicher freier Unterwasserraum 130 cm |

`WaterReviewRelease` prüft alle 587 Frames, Topologie, UVs und animierte Grenzen. Ruhepose-Kantenverhältnisse: Median ca. 1,00; p95 ca. 1,23; p99 ca. 2,21. Sehr kurze ursprüngliche Kanten können stärker gedehnt sein (Maximum ca. 14,43). Die grobe Meshy-Oberflächenstruktur und feine Übergänge an Hals/Schwanz sind verbleibende Modellgrenzen. Kein Anspruch vollständig unverformter Oberfläche oder endgültiger künstlerischer Freigabe.

Die neue Wasser-Mesh-/Skeleton-Auswahl erfolgt innerhalb der bisherigen einzelnen SkeletalMeshComponent. Die ursprüngliche Hauptdarstellung, das ursprüngliche Skeleton und alle sieben Land-/Kampfclips bleiben erhalten. Reaktionszustände werden beim Skeletonwechsel zurückgesetzt, damit kein Clip des jeweils anderen Skeletons ausgewertet wird. Der Wasser-Name folgt dem Kopfanker statt dem erweiterten Culling-Bounds.

## Wasser-KI, Grenzen und Begegnung

Die bestehende RoamingComponent und derselbe begrenzte Planer bleiben zuständig. Nur lange Wasser-Ableitungen erhalten erodierte kontinuierliche Ziele innerhalb der vorhandenen Zone statt der für die aufgerichtete Pose zu engen alten Wegpunkte. Dieselben Boden-, Sicht-, Grenz- und Wegprüfungen bleiben aktiv. Gleitende Bewegungsrichtung folgt der gedämpften Körperrichtung; Beobachtung verlangsamt die Bewegung.

Die gesamte animierte Silhouette wird konservativ abgesichert: Mittelpunkt, zwölf Rand-Bodenproben und eine flache Unterwasser-Box gegen kleine Steine zwischen den Proben. Die bestehende physische Kontaktkapsel bleibt unverändert. Für andere Fische gibt es weiterhin diese Kontaktkapsel, keine neue artikulierte Kollision jedes einzelnen Schwanzsegments. Andere Fische werden über denselben Subsystem-Filter sowohl vor dem Spawn als auch bei der großen **Geländeprüfung** während der Bewegung ausgeblendet, aber weiterhin im eigenen Kontakt-Sweep und beim tatsächlichen Actor-Sweep geprüft. Kein globales Abschalten von Kollision.

Der vorhandene Teich reicht für begrenzte natürliche Strecken; die konservative Hülle beschränkt die verfügbare Mitte deutlich. Der schmale Bach ist für diese Silhouette ungeeignet und wird nicht vergrößert. Kein Schwimmen über Land. Vom Ufer verwendet die vorhandene Interaktion für lange Schwimmer deren bestehenden Wahrnehmungsradius (Garados insgesamt bis 850 cm einschließlich Spielerreichweite), weiterhin mit Sichtprüfung, gültigem Lebenszustand und bestehendem Input. Andere Arten behalten ihre Reichweite.

Beobachten folgt bestehenden Zuständen wie Observe/Alert/Warning/Curious/Social. Beim Pausieren der Weltuhr bleibt der Haltungsübergang stehen. Die Modelltestumgebung nutzt dieselben Clips mit einem reinen Präsentations-Bodenoffset; im echten Wasser wird dieser Offset nicht angewendet.

## Früher fehlgeschlagener Garados-Test

Im früheren Raichu-Functional03-Lauf legte Garados in etwa 89 Sekunden 0 cm zurück. Die Daten zeigen Rest/Idle und keine erfolgreichen oder abgelehnten Planungen. Die genaue historische Ursache ist damit **nicht nachgewiesen**. Ein erneuter Lauf mit ursprünglicher Darstellung bewegte Garados in 95 Sekunden um 3.623,87 cm: Der ursprüngliche Stillstand war in diesem Lauf nicht reproduzierbar. Dessen parallel laufende Blender-Arbeit macht die CSV ungeeignet für einen sauberen Performancevergleich.

Ein erster neuer nativer Lauf (`NativeWater01`) zeigte trotz erfolgreich beendeter Beobachtung tatsächlich 0 cm Garados-Bewegung und 15 abgelehnte Planungen. Das ist **kein bestandener Bewegungstest**. Die neue konservative Bodenprüfung traf den nahen Karpador. Der A/B-Versuch `PeerProbe02` bewies: dieselbe Position ungültig mit Karpador-Kollision, gültig nach ausschließlich temporärer Deaktivierung dieser Kollision. Die Deaktivierung wurde sofort zurückgesetzt. Der Produktionsfix trennt Gelände und physischen Fischkontakt; der neue Automationstest prüft beide Seiten. Ein zusätzlicher Spawn-Regressionsfall platziert einen Fisch diagonal in495cm Abstand, also bereits außerhalb des unveränderten490cm-Mindestabstands. Die konservative Box betrachtet ihn ohne Filter trotzdem als Gelände; derselbe Gelände-Filter beseitigt diese falsche Ablehnung, ohne physische Mindestabstände oder Kontakt-Sweeps zu ändern. `PeerProbe03` bestätigt die wieder gültige Geländeprojektion.

Der abschließende Zusatztest verwendet unverändert die ursprüngliche Schwelle: Beide aktuell vorhandenen Fische müssen >20 cm schwimmen; jeder Messpunkt muss in der Zone, auf korrektem Tiefgang und in Wasserpose liegen. Keine Abschwächung der Kriterien.

## Technische Prüfungen

- Finaler Editor-Build `Build15`: Exit0, ca.16,41s einschließlich regulärem Editor-Abschluss, eigentlicher Unreal-Build9,81s (voller Build11 ca.48,63s, Build13 mit gemeinsamem Spawnfilter ca.21,40s). Zusätzlich feste Tick-Abhängigkeit des langen Wasser-Visuals nach seiner RoamingComponent, entsprechend dem bestehenden Begleiter.
- Vollständige finale Automation `AutomationFinal4` auf Build15: **314 erfolgreich,0 Warnungstests,0 fehlgeschlagen,0 übersprungen; Engine Exit0, strenger Wrapper Exit0**, ca.29,35s. Vorherige finale Läufe AutomationFinal/Final2 auf Build11/12 waren ebenfalls314/314 mit Exit0. AutomationFinal3 auf Build14 war313 erfolgreich +1 erfolgreich mit externer Warnung =314 funktional; sein strenger Exit1 bleibt ausdrücklich **nicht vollständig bestanden**. Der betroffene NPC-Test protokollierte einen HTTP-Timeout zu `https://www.google.com/generate_204`. Automation01 hatte ebenfalls einen externen HTTP-Warntest und strengen Exit1. Keine Warnung unterdrückt.
- Fünf neue Regressionstests: kontinuierlicher Haltungswechsel/Pause/Yaw-Wrap; volle Bodenhülle; Produktions-Rig und isoliertes Land-/Kampfskeleton mit tatsächlicher Auswertung von Angriff, Treffer und Ohnmacht beider Rigs; natürlicher Planer mit drei Seeds einschließlich 817758721; Fische sind keine Geländeoberfläche, bleiben aber physische Hindernisse.
- Zwölf Map Checks im finalen eigenen Editor06: je null Fehler/null Warnungen; Logs mit `GARADOS_WATER_MAPCHECK_BEGIN/END`. Keine Map gespeichert/geändert.
- Echter PIE03: 129,67 s, Garados 547,02 cm natürliche Bewegung, Wander/Idle/Observe/Warning, vollständiges Beobachtungsalpha 1. Enhanced-Input-Fußlauf und Sprint bestanden. Reguläre Spielerinteraktion vom Ufer, Garados-Kampfeintritt auf Originalrig und normaler MasterBall-Fang bestanden. Save/Load über das Spielmenü erhält vollständige individuelle Teamdaten, Position und Weltzeit in isoliertem Testslot (`PIEGameplay02.json`).
- Eigene Editor-Sitzungen wurden regulär beendet; kein Force Quit, keine verworfenen Nutzeränderungen. Fehlgeschlagene frühe Python-Helfer/API-Versuche sind in den jeweiligen Logs/Results erhalten und zählen nicht als bestandene Gameplay-Prüfung.

### Warnungen außerhalb der funktionalen Testserie

UE meldet beim Modulstart bestehende `Condition failed`-Diagnosen, einen Python-Namenskonflikt, MotionVectorSimulation-Thread-Hinweise und im Editor eine fehlende InstancedStaticMeshes-Usage einer Westland-Materialinstanz. Keine Reparatur fremder Assets in diesem Auftrag. HTTP-/Telemetry-Shutdown-Warnungen sind getrennt von Projekt-Tests zu betrachten. Externe iOS-Helferwarnungen, soweit im jeweiligen Log vorhanden, sind keine Garados-Ursache. Der finale Testreport hat keine Testwarnungen; dies bedeutet nicht, sämtliche Engine-Startlogs seien warnungsfrei.

## Abschließende native Nachweise

### Wasser-Zusatztest und Bildnachweis

`NativeWater02/Result.json`: bestanden, Engine Exit 0; ca. 110,05 s einschließlich Aufbau und 95-s-Beobachtung. Garados 213,46 cm, Karpador 2.053,88 cm; ursprüngliche Bewegungs-/Grenz-/Tiefgangskriterien unverändert. Dieser Lauf liegt vor der abschließenden reinen Tick-Abhängigkeit; die sieben Animationen wurden anschließend im nativen Motion07 auf dem finalen Build erneut geprüft.

Echte **2560 × 1440**-Aufnahmen auf dem unveränderten Teich: `Saved/ProjectRefinement/GaradosWaterV2/Motion03/01_Slow.png` bis `07_Lowering.png` (02_Normal, 03_Fast, 04_Turn, 05_Raising, 06_Observe). Die normale Kameraprojektion bleibt erhalten: Arm 2.850 cm, Pitch −50°, Yaw −45°, FOV35°. Ausschließlich der Test-Kamera-Zieloffset zentriert Garados; keine veränderte Weltgröße. Der Aufnahmecode setzt danach Offset, Lag, Geschwindigkeit, Tags und natürliche Steuerung zurück.

`Motion07/Result.json` auf Build12: **sieben tatsächliche Phasen bestanden**, normale Simulationsgeschwindigkeit 1,0. Erfasste Bewegung: 35,0 / 70,0 / 125,0 cm/s, zugehörige Slow-/Normal-/Fast-Mischungen, sichtbare Körperkurve, Beobachtungsalpha 0,31 → 1,00 → 0,74 → 0. Das Aufrichten wird durch die bestehende Spielerwahrnehmung am Ufer ausgelöst. Absenken und erneute Fortbewegung verwenden denselben bestehenden Planer.

Der Nachtest zeigt die Bedeutung der neuen festen Abhängigkeit: Das lange Wasser-Visual wertet die Position erst **nach** dem Bewegungscomponent-Tick aus. Ohne diese Abhängigkeit schwankte die abgeleitete visuelle Geschwindigkeit im Aufnahmelauf trotz normalem Bewegungs-Sollwert; der qualifizierte Normal-Blend wurde nicht erreicht. Mit Abhängigkeit ließen sich sämtliche Geschwindigkeiten und Übergänge unter Aufnahme qualifiziert erfassen. Kein pauschaler Nachweis, dass alle Aufnahme-Kosten dadurch beseitigt wären.

### Video und tatsächliche Aufnahmeleistung

Video: `Saved/ProjectRefinement/GaradosWaterV2/Garados_Water_V2_Motion.mp4`, H.264, **1280 × 720**, ca. 25,66 s, 498 echte Frames. Enthält langsames/normales/schnelles Schwimmen, Kurve, Aufrichten, Beobachten und Absenken. Verifikation: `VideoVerification.json`, 498 decodierte Frames, eindeutige Original-Zeitstempel, keine Interpolation/duplizierten Ersatzframes; maximale PTS-Quantisierung ca. 0,85 ms.

**19,40 Bilder/s nach Spielzeitstempeln, 18,79 erfasste Bilder/s nach realer Aufnahmezeit. Keine 30-FPS-Aufnahme.** Für diese Sichtprüfung wurde ausschließlich im eigenen Prozess der bereits bekannte SDR-Framebuffer `r.DefaultBackBufferPixelFormat=0` benutzt, weil der vorhandene Recorder das normale HDR-Format nicht unterstützt. Die Video-Ausgabe ist gegenüber dem QHD-Bildsatz reduziert; kein geändertes Produktionsprofil. Ein eigener vorheriger 0,25-Zeitlupenversuch scheiterte am Normal-Blend und ist kein Abnahmenachweis. Der erfolgreiche finale Clip läuft mit 1,0.

Fehlversuche bleiben nachvollziehbar: Motion01 falscher Python-Struct-Setter; Motion02 schreibgeschützter BehaviorState; Motion03 vollständige QHD-Bilder, aber 0 Videoframes wegen inkompatiblem Framebuffer; Motion04/05/06 erreichten die qualifizierte Normalphase im Aufnahmefenster nicht. Ihre Helfer-/Videoergebnisse sind keine bestandenen Bewegungsabnahmen. `Motion03/Assessment.json` korrigiert ausdrücklich die zu optimistische reine Aufnahmeskript-Erfolgsmeldung: sieben gültige Bilder, Video fehlgeschlagen.

Die 19-FPS-Sequenz und geprüften Körper-/Blendwerte belegen die Grundbewegung, ersetzen aber keine abschließende künstlerische Beurteilung sämtlicher feiner Oberflächenübergänge. Keine vollständige hochfrequente visuelle Freigabe behauptet.

### Weitere native Regression und Performance

`Saved/ProjectRefinement/EvolutionV3/GaradosWaterV2Native01/Result.json`: **51 Schritte bestanden**, Engine Exit 0, ca. 83,64 s. Die vorhandene geschützte Entwicklungs-Testfixture wird ausschließlich im eigenen EvolutionV3-UserDir verwendet; kein Nutzerspielstand. Karpador bleibt auf Level19 unverändert, normales Angebot auf Level20, Abbruch während der laufenden Sequenz, Save/Load des Abbruchs ohne Doppelangebot, erneuter tatsächlicher Levelaufstieg auf21, volle bestehende Enthüllung und Garados-Erfolg. Gleiche individuelle Identität, XP/Level/Status, HP-Defizit, aktive Attacken, Repertoire und AP; unabhängige Glurak-Reserve bleibt exakt unverändert.

Modelltestgelände über vorhandene Befehle Go Garados / idle / walk / run / turn / directions / auto und Return besucht. Landbegleiter vor/nach Galerie und echtem Kampf weiterhin ursprüngliches Mesh/Skeleton. Reguläre Spielerinteraktion mit wildem Enton, Garados in ClassicBattle auf Originalrig, geerbte schadensfähige Attacke mit exakt einem AP Verbrauch, echter MasterBall-Fang und Teamzuwachs, Rückkehr des Begleiters und Save/Load des vollständigen entwickelten/gefangenen Teams bestanden. Die konkreten Clip-Auswertungen Angriff/Treffer/Ohnmacht beider Rigs sind zusätzlich automatisiert geprüft; dies ist kein gesonderter vollständiger Niederlagen-/Ohnmachts-Gameplaylauf. Physischer Controller nicht neu getestet; bestehende Eingabebelegung bleibt unverändert.

`GaradosWaterV2/Restart01/Result.json`: **bestanden**, frischer Prozess, ca. 27,99 s zuzüglich Engine-Aufbau. Der exportierte eigene Spielstand stellt das gesamte entwickelte/gefangene Team einschließlich Identitäten, Reihenfolge und AP exakt wieder her. Aktiver Landbegleiter mit Originalrig. Echter Wechsel VisualV2 → vorhandene Dev_TestMap → VisualV2; Team und Begleiter bleiben erhalten. Frischer Standard weiterhin HardwareRayTracing=0, FinalGatherMethod=0 (bestehendes IFG), ScreenPercentage75, TAAU1, VSM1, VSM-Strahlen4 und Weltuhr120min. Keine Rendering- oder Mapdatei gespeichert.

`Performance02` (vor der letzten Mindeststrecken-Korrektur): frischer separater Development-Prozess, echte Ausgabe 2560×1440, High (alle zehn sg-Qualitäten2), ScreenPercentage75, TAAU1, Software-Lumen/IFG0, VSM1/4, VSync0, t.MaxFPS0, normales Zeitmaß, laufende Weltuhr um09Uhr, 14 aktive Wild-Pokémon einschließlich natürlich erschienenem Garados. Position (1300,−1200,50,15), drei15-s-Fenster nach mindestens20s Warm-up, keine Aufnahme, kein paralleler Build/Blender/Encoder. Nachweis Result.json und drei CSV-Dateien unter Performance02.

| Fenster | Frames | Ø FPS | Frame ms | GPU ms | Game ms | Render ms | Frame-p95 ms | 1-%-Low FPS | Maximum ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 506 | 33.71 | 29.67 | 28.69 | 2.57 | 29.66 | 33.21 | 25.99 | 43.05 |
| 2 | 455 | 30.31 | 32.99 | 32.07 | 2.74 | 32.99 | 38.00 | 22.46 | 47.81 |
| 3 | 425 | 28.29 | 35.35 | 34.37 | 2.47 | 35.38 | 42.09 | 18.34 | 89.04 |

FPS =1000/arithmetisches Mittel der tatsächlichen CSV-Framezeit; p95 als nächster Rang; 1-%-Low =1000/Mittel der langsamsten aufgerundeten1% der Frames. Keine Schätzung aus der Aufnahmebildrate. CPU-Spalten sind die benannten Unreal-CSV-Zeiten, keine separat gemessene reine Nutzarbeit jedes Threads.

**Keine stabilen30FPS nachgewiesen.** Die Fenster liegen zwischen28,29 und33,71FPS; p95 bis42,09ms und einzelne Frames bis89,04ms. Die GPU-/Renderzeiten steigen über die kurze Reihe bei niedriger Game-Thread-Zeit. Ursache der Drift ist nicht isoliert nachgewiesen; weder ausschließlich Garados noch Thermik als bestätigte Ursache ausgeben. Ein sauberes identisch gepaartes Vorher/Nachher des alten Rigs liegt nicht vor.

Der getrennte Kontrolllauf Performance01 hatte13 aktive Pokémon, **keinen Garados**, 34,18/34,39/32,09FPS und28,23/28,05/30,17ms GPU. Er zählt nicht als Garados-Abnahme und erlaubt wegen anderer Population und zeitlicher Drift keine reine Kostenrechnung des neuen Rigs. Der ältere Baseline02-Lauf unter paralleler Blender-Arbeit wird ausdrücklich nicht für einen Performancegewinn verwendet.

Vorhandene opt-in Roaming-Kostenmessung nur am Garados: 1.644Ticks, insgesamt28.136,57µs Arbeit, im Mittel **17,11µs bzw.0,0171ms/Tick**; zwölf gemessene Planungen zusammen1.017,54µs. Das misst den bisherigen Instrumentierungsumfang der RoamingComponent, nicht alle Render-/Animations-/Subsystemkosten. Keine neuen Wassereffekte oder Lichtquellen; zusätzliche GPU-Kosten sind durch diesen Kurztest nicht separat isoliert.


## Grenzen und Erweiterbarkeit

- Der bestehende Landbegleiter bleibt beim ursprünglichen aufgerichteten/geringelten Mesh und seinen bisherigen Clips. Eine neue schwimmende Begleiter-Navigation ist nicht Teil dieser Architektur und wird nicht vorgetäuscht.
- Bestehende Wasseroberflächenbewegung bleibt aktiv; keine neue Verdrängungssimulation, kein zusätzliches dynamisches Licht, keine dauerhaften Partikelsysteme.
- Renderingprofil C, Software-Lumen/IFG, TAAU75, High, VSM4, Mittag75° und Weltuhr120min bleiben unverändert. Keine neue Art, kein geändertes Save-Schema, keine neuen Kampfdaten.
- Neue optionale Wasserfelder sind für andere Arten leer; die bisherige Darstellung und deren Regeln bleiben dadurch erhalten.
- Kontrollmedien und Messdateien unter Saved werden nicht eingecheckt. Große technische Arbeitsquellen/FBXs/UE-Assets werden über das bestehende LFS übertragen.

### Ergänzung zum letzten PIE-/Spawn-Nachtest

PIE04 lief auf Build12 im frischen eigenen Editor04. Garados erschien erst ab etwa Sekunde81 des unveränderten100-s-Beobachtungsfensters und verbrachte die verbleibenden19s in Rest (keine Planungen/keine Ablehnungen). Die >20cm-Bewegungsprüfung schlug damit ausdrücklich fehl; kein bestandener Lauf. Beim Nachprüfen zeigte sich die noch ungleiche Behandlung anderer Fische **vor** dem Spawn: dort fehlte der bereits während der Bewegung verwendete Gelände-Filter. Dieser ist jetzt zentral in `HabitatSubsystem::IgnoreWaterTerrainPeers` zuständig. Kein geänderter Zufallswert, keine geringere Bewegungsschwelle und keine verkleinerte Ufer-/Geländehülle. Der historische Raichu-0cm-Test bleibt hinsichtlich seiner damaligen Ursache ungeklärt. Die endgültigen Automation-/PIE-Nachweise sind nachfolgend dokumentiert.

### Belegter Mindeststrecken-Randfall und Korrektur

PIE05 ließ im frühen100-s-Fenster keinen Garados zu; dies bleibt ein fehlgeschlagener Nachweis. Im weiterlaufenden Spiel erschien Garados natürlich und bewegte sich184,46cm. PIE06 scheiterte bereits am korrekten Schutz gegen eine zweite Initialisierung desselben isolierten Slots. PIE07 begann deshalb ordnungsgemäß mit dem bereits isolierten Slot und beiden vorhandenen Fischen, maß über volle100s **zusätzliche** Bewegung statt alter kumulierter Strecke: Karpador955,37cm, Garados0cm. Auch dieser Lauf ist ausdrücklich fehlgeschlagen. Er zeigte echte erfolglose Wegplanung, nicht bloß Schlafen.

`RouteProbe.json` prüfte die reale aktuelle Position (700,78,−1756,99) und45 Ziele. Nur vier waren mit unveränderter voller Körperhülle gültig und traversierbar:58,21 /70,44 /140,95 /156,79cm Entfernung. Die alte Mindeststrecke180cm verwarf sie alle. Das Ergebnis blieb identisch nach ausschließlich temporärem Deaktivieren des Karpador-Kontakts (im finally sofort wiederhergestellt): diese Sperre stammt **nicht** vom anderen Fisch. Damit ist der Randfall konkret eingegrenzt.

Für lange Wasserformen leitet derselbe bestehende Planer die Mindeststrecke nun aus dem halben freien Zonenrand nach Abzug des vollständigen400cm-Körperradius ab, begrenzt durch die bisherige artspezifische Mindeststrecke. Im vorhandenen Teich: min(180,(610−400)/2)=105cm. In großen Gewässern bleibt180cm bestehen. Nur wenn dieser kompakte Wasserfall vorliegt, merkt sich die Zielhistorie ein Ziel statt vier; vier Ausschlusskreise konnten den gesamten schmalen sicheren Korridor erschöpfen. Weiterhin16 Kandidaten, dieselben Boden-/Weg-/Ufer-/Kontaktprüfungen, kein Positionssprung und keine veränderte Testschwelle. Andere Arten und Landregeln bleiben unverändert.

Der bestehende NaturalPlanner-Test bildet den Randfall nun mit vier Felsriegeln nach: vollständige sichere Körperhülle, aber kein Ziel180cm vom Zentrum entfernt. Drei unveränderte Seeds, je240s Simulation, weiterhin >100cm Strecke und mehrere Planungen. `TargetedFinal2`: fünf Tests erfolgreich,0 Warnungen/Fehler/Skips, strenger Exit0, ca.30,90s. Die finale Gesamtserie AutomationFinal4 bestand314/314 mit strengem Exit0; die endgültigen echten PIE-/Native-Prüfungen sind nachfolgend dokumentiert.

## Finale Abnahme auf Build15 (30.10.2026)

- **PIE09 bestanden**, ca.126,27s, volle100s Beobachtung beider natürlich vorhandener Fische. Garados **817,51cm zusätzliche Strecke**, Karpador **1.207,27cm zusätzlich**, unveränderte Schauspieleridentitäten und keine erneuten Spawns als Streckenersatz. Alle Messpunkte in der Zone, auf korrektem Tiefgang und in Wasserpose. Garados insgesamt1.037,94cm, mehrere erfolgreiche neue Wege. Nachweis `PIE09/Result.json`; echtes QHD-Bild aus der normalen Spieler-Kamera: `PIE09/Pond00000.png`.
- `PIEFootFinal.json`: Gehen/Sprinten über Enhanced Input bestanden. `PIEGameplayFinal.json`: normale Uferinteraktion, Original-Garados-Rig in ClassicBattle, echter Fang mit unterschiedlicher Instanz, Erhalt vorhandener Teamidentitäten und Menü-Save/Load von vollständigem Team, exakter Position und pausierter Weltzeit bestanden, ca.12,29s.
- **Zwölf finale Map Checks** im eigenen Editor06: je0 Fehler/0 Warnungen; keine Map gespeichert. Reguläres PIE-Ende und sauberer Editor-Abschluss. Keine gewaltsame Prozessbeendigung. Mehrere eigene Editor-/PIE-Zyklen ohne reproduzierten Engine-Shutdown-Stillstand.
- **Restart02 bestanden**, frischer finaler Development-Prozess, ca.27,49s zuzüglich Aufbau: exakter entwickelter/gefangener eigener Teamstand, Garados-Landbegleiter, VisualV2 → vorhandene Dev_TestMap → VisualV2, alle ursprünglichen Renderingwerte C/Software-IFG/TAAU75/VSM4 und120-Minuten-Weltuhr erhalten. Kein temporäres SDR-Aufnahmeformat als Standard übernommen.
- Entwicklung/Angriff/Fang wurden wie oben im tatsächlichen nativen Entwicklungslauf geprüft; die reine Folgekorrektur der engen natürlichen Wasserwegwahl ändert diese Systeme nicht.

### Letzte Performance mit korrigierter natürlicher Wegwahl

`Performance03`: finaler Build15, frischer Development-Prozess, 2560×1440, High, TAAU75, Software-Lumen/IFG, VSM4, Weltuhr aktiv um09Uhr, **14 aktive Pokémon einschließlich Garados**, drei15-s-Fenster ohne Recorder, Blender, Build oder Encoder. Keine eingefrorene Welt. Ergebnis:

| Fenster | Frames | Ø FPS | Frame ms | GPU ms | Game ms | Render ms | Frame-p95 ms | 1-%-Low FPS | Maximum ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 406 | 27.05 | 36.96 | 35.90 | 2.45 | 36.99 | 42.42 | 21.65 | 48.22 |
| 2 | 334 | 22.24 | 44.96 | 43.86 | 2.55 | 44.94 | 53.71 | 15.53 | 66.95 |
| 3 | 294 | 19.56 | 51.12 | 50.15 | 2.55 | 51.22 | 63.12 | 13.87 | 74.20 |

**Stabile30FPS ausdrücklich nicht erreicht.** Die letzte Reihe liegt bei19,56–27,05FPS und GPU35,90–50,15ms. Der klare Anstieg im Verlauf ist nicht isoliert erklärt und darf weder als ausschließlich neue Garados-Kosten noch als bestätigte Thermikursache ausgegeben werden. Auch die vorherigen Reihen zeigten Drift; Population und Ablauf sind nicht exakt gepaart. Keine Performanceverbesserung gegenüber dem alten Rig behauptet.

Garados bewegte sich während dieser Messung zusätzlich238,72cm. Seine opt-in Roaming-Instrumentierung:1.223Ticks, insgesamt28.239,69µs, im Mittel **23,09µs bzw.0,0231ms/Tick**, sechs Planungen zusammen519,13µs. Niedrige gemessene Game-Thread-Zeiten bei hohen GPU-/Renderzeiten; weder vollständige Animationskosten noch einzelne GPU-Pässe wurden separat isoliert. Keine neue Wassersimulation oder zusätzliche Lichtquelle.

Nach der Messung zeigte `pmset -g therm` keine aufgezeichnete thermische/Leistungswarnstufe. Das ist keine Messung von GPU-Takt oder Temperatur während der Fenster. Desktop-Renderer/WindowServer waren beim späteren Prozess-Schnappschuss aktiv; deren Einfluss wurde nicht isoliert. Keine Nutzerprogramme geschlossen und keine Grafikqualität reduziert, um bessere Zahlen zu erzeugen.

### Fehlgeschlagene reine Prüfeinrichtung

PIE08 verwendete eine ungeeignete entfernte Testposition (4000,1000), an der kein begehbarer Boden vorhanden war; der ausschließlich eigene Testspieler fiel dort. Dieser Aufnahmeversuch scheiterte und wird nicht als Spiel- oder Bewegungsabnahme gewertet. Er wurde ohne Speichern auf den bekannten sicheren Boden zurückgesetzt. PIE09 nutzt danach den bestehenden isolierten Slot und den sicheren Beobachtungspunkt; keine erneute Initialisierung eines bereits gesetzten Slots, keine herabgesetzte Streckenschwelle und keine erzwungenen KI-Zustände. Der zusätzliche Blick auf alle sicheren Routen war nötig, um die eigentliche180cm-Wegwahlsperre zu erkennen.

## Projektschutz und Git-Umfang

`ProtectionFinal.json` vergleicht6.003 erfasste Dateien und612 zuvor vorhandene Spielstände mit der Bestandsaufnahme. Nur die ausdrücklich eigenen Quellen/Darstellungsdaten/Dokumente dürfen abweichen. Alle34 geschützten unversionierten Dateien, Original-GLB, ursprüngliche Blender-Arbeitsquelle, Originalmesh/-Skeleton/-Materialien/-Texturen/-Clips, sämtliche Maps und Nutzerspielstände bleiben unverändert. Beide Vollbackup-Verweise bleiben auf03492bd96b4dba44692f675c19d5f11abfa86b4b; kein History-Rewrite oder LFS-Prune.

Gezielter Commit nur anhand `CommitManifest.json` (59 eigene Dateien). Die vorhandenen Nutzeränderungen in DefaultEngine.ini sowie alle geschützten unversionierten Dateien bleiben außerhalb des Commits. Aufnahmen, QA-Spielstände und große Messdateien unter Saved werden nicht hochgeladen. Normales Pushen nur von main; bestehendes bestätigtes LFS-Budget0USD wird nicht verändert. Abschließende tatsächliche Commit-/Remote-/LFS-Ergebnisse stehen im Chat und sind mit git log/status nachvollziehbar.
