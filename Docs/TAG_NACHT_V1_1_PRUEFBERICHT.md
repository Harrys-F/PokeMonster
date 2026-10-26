# Tag-Nacht V1.1 – Einzelprüfung Paket A

Stand: 26.10.2026. Basis `f712b662` einschließlich `e1fc3517`. Die nachfolgende KI-Erweiterung wird separat implementiert und geprüft. Maschinenlesbare Resultate: [Nachweis](TAG_NACHT_V1_1_NACHWEIS.json).

## Umsetzung und sichtbare Änderungen

75° ist gemäß Nutzerentscheidung regulärer Mittag. `pm.DayNight C` wählt weiterhin 85° als Debugvergleich; `pm.DayNight B` kehrt zurück. Keine 60°-Mittagsvariante. Weltuhr, 120-Minuten-Tag und Kameraperspektive unverändert.

Morgens steigt die direkte Helligkeit zwischen 05:00 und 06:39 statt erst 07:00 vollständig an. Wärmere niedrige Sonne (2900–5700 K nach Sonnenhöhe), kühles Restlicht unverändert. Abends sinkt die Sonne bis 19:30 statt 19:00; um 19:00 bleiben sichtbares warmes Direktlicht und lange Schatten. Das ist eine gestalterische Sonnenbahn, keine astronomische Simulation. Kurven und Farben sind kontinuierlich; keine Filter, neuen Strahlen-VFX oder Belichtungsänderungen.

Nacht: Mondbeitrag 0,50 → 0,55; unverschattetes vorhandenes Fülllicht 0,90 → 1,10. Zusammen 1,65 gegenüber 9,30 am Mittag. Nacht bleibt deutlich dunkler, Wege/Vegetation etwas besser lesbar. Keine neuen Lichtquellen, kein leuchtendes Charakter-/Pokémon-Material. Himmelsfarbverlauf behutsam wärmer. SkyLight 1,25, Exposition und AO unverändert; keine SkyLight-Neuerfassung pro Frame. Ein vorhandenes Directional Light dient weiterhin Sonne und Mond, das zweite vorhandene Licht bleibt schattenlos.

## Schattenaktualisierung und Messung

Ursache der Mehrkosten: Bei laufender Sonne wird die Schattencaster-Rotation regelmäßig ungültig. SkyLight, Himmelskomplexität, Schattenauflösung und Zahl der Schattenlichter wurden nicht erhöht. Neuer maximaler Winkelfehler `RotationThresholdDegrees=0.025`: Lichtkurven weiter alle 0,1 s, Rotation erst beim Überschreiten. Debug-Zeitsprünge/B-C-Umschalten sofort exakt. Null reproduziert V1. Keine Reduktion von Grafikqualität oder Schattenauflösung.

QHD 2560×1440, High=2, 100% Renderauflösung, unveränderte Kamera; je drei Wiederholungen pro Dorf/Wald, je 3 s Aufwärmen + 5 s Messung, normale laufende Weltuhr 1×. KI/Animationen aktiv; nur Begegnungsauslösung transient gesperrt. Jede Messung prüft, dass kein Kampf aktiv ist und die Uhr tatsächlich läuft. Kontrollmessung am Ende gegen Drift. Mediane der drei Einzelmediane in ms:

| Zustand | Dorf GPU | Wald GPU | Dorf Frame | Wald Frame | Dorf ShadowDepths |
|---|---:|---:|---:|---:|---:|
| Unveränderte V1-Referenz | 89,23 | 92,59 | 102,48 | 104,12 | 10,32 |
| V1.1 ohne Begrenzung | 89,88 | 92,65 | 103,87 | 105,48 | 10,55 |
| V1.1 mit Begrenzung | 85,48 | 90,01 | 99,86 | 103,20 | 6,50 |
| Sonne gehalten | 83,85 | 88,54 | 96,92 | 101,90 | 2,54 |
| Ohne Begrenzung, Rückkontrolle | 88,02 | 91,59 | 101,82 | 104,63 | 9,09 |

Gewinn gegenüber beiden bewegten Kontrollen: Dorf 2,54–4,41 ms, Wald 1,58–2,65 ms. Restkosten gegenüber gehaltener Sonne ca. 1,47–1,63 ms. Einzelmedian-Spannen und sämtliche Rohpfade im Nachweis; keine generelle FPS-Zusage. Die vorhandene Szene ist insgesamt GPU-lastig, hier ungefähr 9,5–10 FPS. Das ist kein neuer breiter Performance-Art-Pass. Rotationsänderungen im begrenzten Messlauf 90 statt 461 Auswertungen. Schattenpass als Ursache bestätigt, weitere Qualitätssenkungen nicht übernommen.

## Echte Bilder und Bewegungsnachweis

Alle Pfade unter `Saved/ProjectRefinement/DayNightV11AI22/`:

- `Before01/` und `AfterA01/`: jeweils Wiese und Baumkrone um 06, 09, 12, 19, 22, 00 Uhr, zwölf QHD-Paare. Kamera/Position/FOV numerisch gleich (Differenzen unter 0,000001 cm/Grad). Animationen/Graswind bleiben echt und laufen unabhängig.
- `LightingCompareA.jpg`: lediglich verkleinerte/beschriftete Originale, keine Belichtungs- oder Bildkorrektur.
- `GameplayA01/InteriorDay.png`, `InteriorNight.png`, `InteriorLoaded.png`: tatsächlicher Gebäudeübergang und Wiederherstellung.
- `Videos/Raw.mp4`, `Videos/Cached.mp4`: jeweils ca. acht Sekunden echte präsentierte Frames, Originalzeitstempel, keine Zwischenbilder. Tatsächliche Aufnahmefrequenz 5,96 bzw. 5,30 Hz trotz höherem angefragtem Limit. `ShadowFrames.jpg` zeigt Originalframes Anfang/Mitte/Ende. Keine auffälligen Schattensprünge in diesen Stichproben; geringe Bildrate begrenzt die endgültige Bewegungsbeurteilung. Winkelabweichung zusätzlich automatisiert begrenzt. Erste Recorder-Anfrage lag außerhalb seines erlaubten Ordners und erzeugte keine Aufnahme; nur bestätigter zweiter Lauf `ShadowMotionA02` gilt als Nachweis.

Die drei vorübergehend neben der Figur gezeigten Starter stammen vom bestehenden Testgelände; eindeutige TEST-Beschriftung, nur PIE-Transformationen, kein verändertes Habitat/Save/Asset. Unbeteiligte wild lebende Pokémon können sich zwischen Aufnahmen bewegen.

## Technische Einzelprüfung

- Editor-Build `DayNightV11A_Build02`: Exit 0.
- Volle native Automation `DayNightV11A_Automation01`: **273 funktional bestanden, 0 fehlgeschlagen, 0 übersprungen**; davon **272 ohne Warnung, 1 mit Warnung**, Engine Exit 0. Strenger ProjectQA-Wrapper **Exit 1**, ausdrücklich nicht vollständig bestanden.
- Bekannte externe Warnung: macOS `idevice_id` (iOS-Helfer) Bad CPU type/Startfehler. Zusätzlich vorgefunden: generische frühe Engine-Condition-/HTTP-Port-8000-Meldungen und bereits vorhandene fehlende Instancing-Nutzung von `MI_WLA_LeafOak`; keine gemeinsamen Assets dafür resaviert.
- Zwölf bestehende Maps: jeweils **0 Fehler, 0 Warnungen** bei Map Check. Keine Map gespeichert.
- Gewöhnlicher PIE-Start, B75/C85, Menüpause/Fortsetzen, echter Fußlauf, beschleunigte Morgendämmerung/Mitternacht, tatsächlicher Heilhaus-Ein-/Ausgang, isoliertes Innenraum-Save/Load mit exakter Weltzeit/Team/Kontrollpunkt, bestehender ClassicBattle-Sieg und Steuerungsrückkehr bestanden (`GameplayA01`, 16 Assertions).
- Echter Mapwechsel VisualV2 → bestehende Dev_TestMap → VisualV2: gleiche GameInstance/Weltzeit, außerhalb VisualV2 kein Lichtzyklus/Himmelsaktor, Rückkehr sofort korrekte Nacht, Steuerung wieder frei (`TravelA01`).
- 85 geschützte Dateiprüfsummen, 31 ursprüngliche unversionierte Dateien und beide Vollbackup-Verweise unverändert; Editor-Szene identisch, keine schmutzigen Pakete. Keine neuen Content-/Art-/Save-Identitäten oder LFS-Nutzdaten.

## Grenzen und Fortsetzung

Visuelle Feinabnahme bleibt anhand der Originalbilder möglich. Schatten-/Grasbewegung kann bei dieser Aufnahmefrequenz nicht abschließend hochfrequent beurteilt werden. GPU-Vorteile sind orts- und hardwareabhängig; verbleibende dynamische Schattenkosten sind dokumentiert. Keine neue Sonnenstrahlenproduktion, kein Wetter, keine Änderungen an Spawn-/Kampfregeln. Paket B und gemeinsame Abnahme erhalten einen eigenen Bericht und Commit. Physischer Controller-Test nicht behauptet; bestehende Belegung unverändert.
