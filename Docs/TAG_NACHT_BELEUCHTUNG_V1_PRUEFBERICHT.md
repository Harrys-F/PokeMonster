# PokeMonster – Tag-Nacht-Beleuchtung V1: Prüfbericht

Stand: 26.10.2026. Ausgang: `e0b5a0e5`, einschließlich `bf83a4bd` (Weltuhr V1).
Ziel ausschließlich `/Game/Maps/Dev_TestMap_VisualV2`. B75 ist vorläufig empfohlen;
**keine der beiden Varianten ist endgültig visuell freigegeben. Harry entscheidet.**

## 1. Ausgangszustand und Schutz

Vor Änderungen wurden fünf echte QHD-PIE-Aufnahmen und eine native Profilerreihe
angelegt. `Saved/ProjectRefinement/DayNightV1/Before`, `Inspection.json`,
`OriginalScene.json`, `Baseline.json` dokumentieren Zustand und Prüfsummen.

| Bestandteil | Tatsächlicher Ausgang / Behandlung |
|---|---|
| Hauptlicht | `DirectionalLight_1` / `DirectionalLight_Dev`, movable, Pitch −48°, Yaw −100°, Intensität 7,5, 5700 K, Schatten an, Source Angle 3,5°, Kanal 0 |
| Fülllicht | `DirectionalLight_0` / `VS_SoftSkyFill`, Pitch −40°, Yaw −45°, 1,8, 8000 K, keine Schatten, Kanal 0 |
| SkyLight | `SkyLight_1` / `SkyLight_Dev`, stationary, 1,25, keine Echtzeitaufnahme, untere Hemisphäre schwarz; unverändert |
| Belichtung | Außenprofil Min/Max 1, Bias 0,3; AO 0,65; unverändert |
| Kamera | Normalspiel Pitch −50°, Yaw −45°, FOV 35°, Arm 2850 cm; unverändert |
| Charakterlicht | Vorhandene gezielte adaptive Aufhellung/Kanal 2; keine Parameter-/Codeänderung |
| Innenräume | Bestehende Raumlichter/Kanal 1; unverändert |
| Himmel zuvor | Kein vorhandener SkyAtmosphere-/SkyDome-Aktor im Ausgangsaudit |

Keine Map-, Modell-, Animations-, Pokémon-/KI-, Controller-, Kampf- oder
Speicherdatei wurde geändert. Zur Laufzeit bestehende Lichtquellen weiterverwendet;
keine neue Punkt-, Füll- oder Schattenlichtquelle. Prüfungen schützen alle zwölf
Mapdateien, vorhandene Nutzersaves und die ursprünglichen unversionierten Dateien.

## 2. Technische Umsetzung / Weltuhr

`Lighting/PokeMonsterDayNight` ist ein auf VisualV2 begrenztes World-Subsystem.
Es liest ausschließlich `UPokeMonsterWorldClock`: Tagesfortschritt, Tagesphase und
zentrale Phasengrenzen. **Kein eigener Zeitfortschritt, keine zweite Uhr, keine
Save-Erweiterung. Tageslänge weiterhin 120 Echtminuten.**

Ein World-Timer prüft alle 0,1 Sekunden. Bei unveränderter Uhrzeit werden keine
Lichtwerte neu gesetzt. `OnTimeSet` aktualisiert sofort nach Debugänderung oder
Laden. Beim Weltwechsel bleibt die GameInstance-Uhr erhalten; der neue
VisualV2-Controller wertet sie beim BeginPlay direkt aus. Andere Maps bleiben
inaktiv. Beim Abschalten/PIE-Ende werden ursprüngliche Lichtwerte zurückgesetzt.
Falls die notwendigen Lichtquellen oder die Uhr fehlen, werden keine Ersatzlichter
erstellt und keine uncachierten Originalwerte zurückgeschrieben.

Die bestehenden Menü-, Dialog-, Kampf-, Lade- und expliziten Pausenregeln der Uhr
werden konsumiert, nicht umgebaut. Beleuchtung hat keine eigene Pausenverwaltung.

## 3. Sonnenbahn, Mond und Konfiguration

Künstlerische Kosinusbahn: Sonnenaufgang 05:00, höchster Stand exakt 12:00,
Horizont um 19:00. Die Punkte werden aus den zentralen Phasen abgeleitet.
Maximalhöhe ausschließlich B75 oder C85. Licht-Yaw bei Mittag −100° und
Fortschreibung 15° je Ingame-Stunde; damit ändern sich Schatten nachvollziehbar.
`SunAzimuth` bezeichnet im Code die Unreal-Lichtrichtung (Yaw), nicht einen
zusätzlich astronomisch berechneten Standortwinkel.

Ein vorhandenes Hauptlicht wird nachts für kühles Mondlicht wiederverwendet.
Kein zweiter dynamischer Schattenwerfer. Sanfte quaternionbasierte Überblendung
während der lichtarmen Übergänge. Mondrichtung nachts Pitch −50°, Yaw 10°;
keine Mondphasen oder astronomisch exakte Bahn.

| Konfiguration | Wert |
|---|---:|
| Vorläufiges Mittagsmaximum | B75; C85 weiter verfügbar |
| Tageslicht / schattenloses Fülllicht | 7,5 / 1,8 |
| Nacht-Mondlicht / Fülllicht | 0,5 / 0,9 |
| Farbtemperatur | Sonnendämmerung 3100 K → Tag 5700 K; Mond 8500 K |
| Aktualisierung | maximal 10 Prüfungen/s, keine Neuberechnung bei gehaltener Zeit |

Konfiguration zentral in `DefaultGame.ini`, Abschnitt
`PokeMonsterDayNightSettings`. SkyLight, feste Exposition, Schattenverfahren und
Source Angle werden nicht verändert. Die Nachtwerte entstanden aus realen
Bildprüfungen: 0,12/0,22 war zu dunkel; 0,35/0,65 wurde geprüft; 0,5/0,9 gewählt.
Das indirekte Fülllicht kompensiert im frühen Morgen den zurückgehenden Mondanteil,
damit die Gesamthelligkeit vor Sonnenaufgang nicht zunächst absinkt.

## 4. Tagesphasen und Himmel

| Phase | Uhrzeit | Darstellung |
|---|---|---|
| Früher Morgen | 04–05 | Kühles Grundlicht, sanfte Aufhellung, noch Sterne |
| Morgendämmerung | 05–07 | Niedrige wärmere Sonne, zunehmendes Licht, Sterne blenden aus |
| Tag | 07–18 | Natürliche Tagesfarben, hohe Mittagssonne und kurze Schatten |
| Abenddämmerung | 18–20 | Gold-/Orangehorizont, sinkende Sonne, gedämpfter Übergang |
| Nacht | 20–04 | Kühles schwaches Mondlicht, deutlich dunklerer Boden, Sterne |

Eine transiente Himmelskugel verwendet vorhandene Engine-Geometrie und
`M_Sky_Panning_Clouds2` mit eigener Laufzeit-Materialinstanz. Kein Eingriff in
Engine- oder gemeinsam genutzte Materialassets. Keine Atmosphären-, Wetter- oder
Volumen-Simulation. Keine Echtzeit-SkyLight-Recaptures; die Kugel ist ausdrücklich
von Sky-/Reflection-Captures ausgeschlossen.

Im echten Himmelsnachweis wurde ein Fehler gefunden und korrigiert: Der
Engine-Parameter „Sun height“ multipliziert ausschließlich die Sterntextur.
Negative Sonnenhöhe erzeugte dunkle Flecken. Er bleibt jetzt positiv; die eigene
Sternhelligkeit steuert die Ausblendung. Die Sonnenscheibenrichtung berücksichtigt
CameraVectorWS und entspricht der tatsächlichen Lichtquelle. `Sky05` belegt Sonne,
Tag, Dämmerung und weiße Sterne. Diese vier Aufnahmen verwenden ausdrücklich eine
vorübergehend nach oben gerichtete Diagnosekamera; die normale Spielkamera wurde
anschließend exakt wiederhergestellt.

## 5. B75 gegen C85 – identische QHD-Bedingungen

Echte normale PIE-Spielkamera, 2560×1440 intern/extern, High 2, TAA. Fünf Szenen:
Wiese, Baumkrone, Gebäude, Waldweg, Felsen/Gelände. Uhr exakt 12:00, gleiche
Sonnenintensität/-farbe/-temperatur, Yaw, Fülllichter, SkyLight, Belichtung, FOV und
Spieler-/Kameraposition. `ComparisonValidation02.json` prüft alle fünf Paare.

Nur die maximale Sonnenhöhe wird bewusst verändert. Zur Vergleichbarkeit werden
Spieler-Idle und vorhandenes adaptives Charakterlicht pro Paar eingefroren, danach
wieder aktiviert. Drei bestehende Testgelände-Pokémon dienen temporär als
Farb-/Größenreferenzen; keine neuen Modelle/Begegnungen. Originaltransforme werden
wiederhergestellt. Animationen anderer Weltakteure und Vegetation können zwischen
Aufnahmen natürlich unterschiedliche Momentbilder besitzen.

| Kriterium | B75 | C85 |
|---|---|---|
| Schattenlänge | Kurz, noch klar räumlich lesbar | Sehr kurz, konzentriert an Füßen/Stämmen |
| Gebäude-/Geländetiefe | Mehr seitliche Abstufung | Gleichmäßiger von oben, etwas flacher |
| Figur/Pokémon | Gut voneinander/Untergrund unterscheidbar | Ebenfalls lesbar, geringe zusätzliche Helligkeit von oben |
| Wege | Klar sichtbar | Klar sichtbar |
| 2,5D-Gesamtwirkung | Vorläufig bevorzugt | Sinnvolle kompakte Alternative |
| Leistung | Siehe wiederholte Messwerte; kein pauschaler Vorteil behauptet | Keine zuverlässige allgemeine Überlegenheit abgeleitet |

**Empfehlung B75**, weil die kurzen Schatten in der schrägen Kamera weiterhin
Form und Abstand vermitteln. C85 bleibt vollständig umschaltbar. Diese Empfehlung
ersetzt keine Nutzerfreigabe.

## 6. Tatsächliche Bildnachweise

Alle Pfade relativ zum Projekt; Bilder liegen lokal unter `Saved` und sind nicht
als neue Git-LFS-Assets hochgeladen. Native PNGs unverändert. Kontaktblätter bestehen
nur aus verkleinerten Originalaufnahmen und Beschriftungen, ohne Nachbelichtung.

* [B75/C85, fünf Szenen](../Saved/ProjectRefinement/DayNightV1/Noon_B75_C85.jpg)
* [Original/B75/C85](../Saved/ProjectRefinement/DayNightV1/Original_B75_C85.jpg)
* [Tageszyklus](../Saved/ProjectRefinement/DayNightV1/Cycle_B75.jpg)
* Vorher vor Implementierung: `Saved/ProjectRefinement/DayNightV1/Before/*.png`
* Native Bildpaare: `.../Comparison02/B75/{Wiese,Baumkrone,Gebaeude,Waldweg,Felsen}.png` und analog `C85`.
* Acht Tageszeiten: `.../Comparison02/Cycle/Time0430.png`, `Time0600.png`, `Time0900.png`, `Time1200.png`, `Time1600.png`, `Time1900.png`, `Time2200.png`, `Time0000.png`.
* Nacht unter Krone / beim NPC: `.../Comparison02/Cycle/NightCanopy.png`, `NightNPC.png`.
* Innenraum: `.../Gameplay01/InteriorDay.png`, `InteriorNight.png`, `InteriorLoaded.png`.
* Zusätzliche Himmelsdiagnose: `.../Sky05/{Day,Dawn,Dusk,Night}.png`.

Wege, Silhouetten und Pokémon-Farben bleiben im geprüften Nachtaufbau erkennbar.
Dunkle Mantel-/Hautdetails sind nachts bewusst gedämpft; keine künstlichen
Leuchtkonturen. Die Lesbarkeit bei individuellen Displayhelligkeiten und die
endgültige Nachtästhetik bleiben Teil der visuellen Nutzerprüfung.
Innenraumvergleich: Grundhelligkeit/Materialfarben bleiben stabil; der außerhalb
des ausgeschnittenen Raums sichtbare Hintergrund wechselt mit dem Himmel.

## 7. Performance – native wiederholte Messung

Vorhandenes `pm.EnvPerf2`, keine neue Benchmarkarchitektur. Gleiche normale
Kameraorte Dorf (−4100,450) und Wald (−4300,1550), QHD 2560×1440 bei 100 % intern,
High 2, TAA 2, VSync/Framelimit während der scoped Messung deaktiviert und danach
zurückgesetzt. Je Fall/Ort drei Wiederholungen, 3 s Aufwärmen + 5 s Aufnahme.
Native Frame- und GPU-CSV-Dateien, keine aus Screenshots geschätzten Zeiten.

Die erste neue Serie ist **ungültig als Abnahmenachweis**: Eine echte
`Dev_VisibleWild`-Begegnung begann bereits während der vorangehenden Himmelsaufnahme.
Die Uhr pausierte regelgerecht; der vermeintlich bewegte Fall bewegte sich nicht.
`PerformanceSeries01/Invalidated.json` kennzeichnet das; Rohdaten bleiben erhalten.
Auch der erste Reise-Reset schlug deshalb an der echten Kampfpause fehl.
Keine Weltuhr-/Kampflogik wurde dafür geändert.

Die gültige Serie `PerformanceSeries02` verwendet frisches PIE und leert nur
vorübergehend die Encounter-Profile der laufenden Wildinstanzen. Wander-KI,
Animationen, Sichtbarkeit und Spielereingabe bleiben aktiv; die Bindungen werden
anschließend wiederhergestellt. Jeder Messframe verlangt keinen Kampf und den
vorgesehenen Pausenzustand. Der dynamische Fall verlangt echten Uhrfortschritt.

| Zustand | Ort | FPS¹ | Frame ms | Frame-Spanne² | P95 ms | GPU ms | GPU-Spanne² | Schatten ms³ |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Ursprung vor Implementierung | Dorf | 10.96 | 91.22 | 90.29–91.27 | 98.62 | 78.96 | 78.25–79.41 | 10.11 |
| Ursprung vor Implementierung | Wald | 10.21 | 97.92 | 96.32–98.14 | 101.75 | 84.67 | 83.16–84.94 | 13.70 |
| 12:00 B75 | Dorf | 9.78 | 102.22 | 102.18–102.42 | 112.29 | 88.52 | 88.03–91.72 | 10.66 |
| 12:00 B75 | Wald | 9.25 | 108.06 | 106.93–108.91 | 122.11 | 94.32 | 92.92–94.95 | 13.17 |
| Originalkontrolle gleiche Sitzung | Dorf | 9.81 | 101.95 | 101.92–103.85 | 110.37 | 88.76 | 87.93–90.34 | 14.09 |
| Originalkontrolle gleiche Sitzung | Wald | 9.41 | 106.27 | 105.64–106.65 | 115.21 | 93.56 | 93.12–93.65 | 15.17 |
| 12:00 C85 | Dorf | 9.98 | 100.18 | 100.13–100.56 | 111.51 | 87.63 | 87.16–87.77 | 12.40 |
| 12:00 C85 | Wald | 9.43 | 106.00 | 105.15–106.31 | 114.99 | 92.38 | 92.15–94.79 | 14.07 |
| 06:00 Morgendämmerung | Dorf | 9.90 | 101.00 | 100.74–102.00 | 110.40 | 87.01 | 85.79–87.64 | 11.25 |
| 06:00 Morgendämmerung | Wald | 9.58 | 104.40 | 104.27–105.45 | 114.25 | 91.69 | 88.50–93.14 | 11.85 |
| 19:00 Abenddämmerung | Dorf | 9.91 | 100.93 | 99.30–102.54 | 111.00 | 87.43 | 86.79–90.29 | 11.78 |
| 19:00 Abenddämmerung | Wald | 8.94 | 111.90 | 107.67–112.19 | 120.94 | 97.86 | 94.21–99.37 | 16.20 |
| 22:00 Nacht | Dorf | 9.70 | 103.06 | 102.41–105.12 | 112.16 | 89.02 | 87.95–89.22 | 10.78 |
| 22:00 Nacht | Wald | 9.26 | 107.99 | 106.96–111.50 | 116.89 | 94.16 | 93.19–96.04 | 14.13 |
| B75 mit laufender Uhr (1×) | Dorf | 9.48 | 105.46 | 104.66–107.25 | 128.34 | 91.88 | 91.77–94.32 | 18.58 |
| B75 mit laufender Uhr (1×) | Wald | 8.93 | 111.93 | 110.31–113.20 | 121.05 | 96.94 | 96.15–98.78 | 17.30 |

¹ FPS = 1000 / Median-Framezeit. ² Spanne der drei Wiederholungsmediane, nicht
Konfidenzintervall. Zentrale Werte sind Mediane der drei Mediane; P95 analog.
³ Summe der Mediane nativer GPU-Scopes ShadowDepths, ShadowProjection und
DistanceFieldShadows; keine exklusive Zerlegung der gesamten Framezeit.

Ausgang und spätere Kontrollreihe werden separat ausgewiesen. Unterschiede
zwischen Sitzungen/wechselndem Weltzustand dürfen nicht pauschal dem neuen Zyklus
zugeschrieben werden. Aussagekräftiger sind die Varianten und die Originalkontrolle
innerhalb derselben gültigen Sitzung. Schwankungen/Einzelframe-Ausreißer bleiben in
`PerformanceSummary.json` und den Rohdaten sichtbar. Der bestehende QHD-High-Aufbau
ist auf diesem Mac bereits deutlich GPU-limitiert und kein 30-/60-FPS-Nachweis.
Es wurde keine globale Performanceoptimierung oder weitere Kameravariante begonnen.

In der gültigen Sitzung liegt B75 bei 88,52/94,32 ms GPU (Dorf/Wald),
die Originalkontrolle bei 88,76/93,56 ms. Mit tatsächlich bewegter Sonne
91,88/96,94 ms: gegenüber gehaltenem B75 +3,36/+2,62 ms GPU und
+3,23/+3,88 ms Framezeit. Schatten-Scopes steigen dabei erwartungsgemäß.
Das ist ein messbarer Zusatzaufwand, keine behauptete Kostenneutralität. C85
zeigt hier etwas kleinere Mediane, aber keinen allgemein gesicherten
Performancevorteil; die visuelle Empfehlung bleibt B75.

Dynamischer B75-Fall: (Day=1,SecondsOfDay=43200.000000) → (Day=1,SecondsOfDay=43804.107266).
Das ist tatsächliche 1×-Fortschreibung der vorhandenen 120-Minuten-Uhr, kein
beschleunigter Ersatz für die Performanceaufnahme.

## 8. Build, Automation, Maps, PIE und Save/Load

* Finaler Editor-Build `DayNightV1Build09`: Exit 0.
* Finale vollständige Automation `DayNightV1Automation08`: 270 ohne Warnungen, 2 mit Warnungen, 0 fehlgeschlagen; insgesamt 272. Strenger Wrapper: **Exit 1**.
* 267 vorherige Tests plus fünf neue DayNight-Tests: B/C unterscheiden ausschließlich Höhe; Verlauf/Exaktgrenzen/Mitternacht; zentrale Phasen/Nachtkontrast/früher Morgen; deterministische Auswertung/Weltuhr; Mapbegrenzung/Konfiguration.
* Zwölf vorhandene Map Checks: jeweils 0 Fehler, 0 Warnungen; ursprüngliche Editor-Map wiederhergestellt, nichts gespeichert.
* `Gameplay01`: gewöhnlicher Start 09:00, B/C-Umschaltung, Pause/Fortsetzen, echte Menübedienung mit Lichtpause, normaler softwaregesteuerter Fußlauf, beschleunigter echter Morgenphasenwechsel, Tür hinein/hinaus, Nacht im Heilhaus, reguläres Save/Load mit exakter Uhr-/Licht-/Raumkamera-/Team-/Kontrollpunkt-Wiederherstellung, Mitternacht, echter ClassicBattle-Sieg mit Rückkehr der Kontrolle.
* `Travel02`: echter OpenLevel-Rundweg über vorhandene Dev_TestMap; gleiche GameInstance, Tag 11 22:00 exakt erhalten; kein Zyklus/Himmel auf anderer Map; bei Rückkehr sofort Nacht; Uhr und Kontrolle laufen nach Freigabe weiter.
* `Sky05`: echte zusätzliche Himmelsprüfung, Kamera/Eingabesituation wiederhergestellt.
* Nutzerspielstände unverändert; ausschließlich eigene isolierte Slots bzw. vorhandener RAM-Testschutz. Keine Änderung der Positions-/Kontrollpunktregeln, kein Zeitsprung durch Niederlage.
* Eingabeschritte sind Softwareprüfungen, keine neue physische Switch-Pro-Hardwareabnahme. B/A-Zuordnung und alle vorhandenen Eingabe-/Kampfsysteme bleiben unverändert.

Bekannte externe Meldungen: `idevice_id` kann mit „Bad CPU type in executable“
(86) nicht starten. Im finalen Testlauf sind 2 Tests von diesen externen Warnungen betroffen; deshalb endet der strenge Wrapper mit Exit 1, obwohl keine fachlichen Tests fehlschlagen.

Weitere bereits im Ausgangslog vorhandene
Engine-Startmeldungen: generische „Condition failed“ vor der Testqueue sowie
HttpListener-Port 8000 belegt. Nicht als neue Projekt-Kampf-/Lichtfehler ausgegeben.

Zusätzlich wurde im Editor eine Material-Usage-Warnung für das unverändert
vorhandene `MI_WLA_LeafOak` (InstancedStaticMeshes) beobachtet. Kein gemeinsames
Material ungeprüft resaved; separat offen. Finale Logs enthalten keine neuen
Struct-Initialisierungsfehler, Abstürze, Ensures oder Blueprint-Runtimefehler.

## 9. Entwicklerbedienung

Nur Editor-PIE, Konsole oder Output-Log-Kommandozeile:

```text
pm.WorldClock pause
pm.WorldClock set 1 12 0
pm.DayNight on
pm.DayNight B
pm.DayNight C
pm.DayNight show
pm.WorldClock set 1 22 0
pm.WorldClock speed 60
pm.WorldClock resume
pm.WorldClock reset
```

`B` = 75°, `C` = 85°. `pm.DayNight off` stellt ursprüngliches Sonnen-/Fülllicht
wieder her und blendet den Laufzeithimmel aus; `on` aktiviert den Zyklus wieder.
B/C-Wahl ist für den laufenden Weltcontroller; nach Mapneustart gilt die zentrale
INI-Vorgabe B75. Debugzeit bleibt bestehender Weltuhr-Testschutz; keine permanente
Geschwindigkeitsänderung. Nach Vergleichen `pm.WorldClock reset` verwenden.

## 10. Grenzen und offene visuelle Entscheidung

* B/C und endgültige Nachtästhetik sind noch nicht durch den Nutzer freigegeben.
* SkyLight/Umgebungsreflexionen bleiben statisch; kein dynamischer HDR-Capture oder vollständiger physikalischer Atmosphärenwechsel. Eine bewusst kleine, günstige Himmelslösung.
* Mondlicht ohne sichtbaren Mondkörper/Mondphasen; Sonne/Mond teilen sich ein Schattenlicht.
* Die feste schräge Standardkamera zeigt vorwiegend Boden; Himmel-Diagnosen sind ausdrücklich andere Kameras, keine Belege einer geänderten Spielkamera.
* Vorhandene Objektverdeckung/Laub-/Materialprobleme werden nicht als Beleuchtungsreparatur umgestaltet. Kein erneuter Landschafts- oder Kamerapass.
* Performancewerte sind ein begrenzter Vergleich, keine Kostenneutralitäts- oder Ziel-FPS-Garantie.
* Fehlversuche bleiben erhalten: erster Build (nicht vorhandene Color-API), erste Automation (zu schnelle rotationsabhängige Mondüberblendung), frühe zu dunkle Nachtprofile, zwei Himmels-Python-Initialisierungsfehler, ungültige erste Performance-/Reiseserie. Behobene neue Struct-Initialisierungen und Stern-/Sonnenscheibenfehler sind in finalem Build/Nachweis geprüft.

Maschinenlesbarer [Abnahmenachweis](TAG_NACHT_BELEUCHTUNG_V1_NACHWEIS.json):
37 native QHD-Bilder mit SHA-256, fünf geprüfte Bildpaare, zwölf Map Checks,
Automation, PIE-Ergebnisse und alle Performance-Mediane.

## 11. Git und Artefakte

Quellcode, zentrale Lichtkonfiguration, Projektdokumentation und reproduzierbare
Prüfwerkzeuge werden gezielt gesichert. Keine Map-/Content-/Art-/Save-Dateien;
keine neuen LFS-Objekte erforderlich. Lokale native Bild-/CSV-Nachweise verbleiben
im angegebenen Saved-Verzeichnis. Geschützte Dateien: 84
Prüfsummen unverändert; ursprüngliche unversionierte Dateien: 31
erhalten; beide Vollbackup-Referenzen unverändert.

Implementierung und geprüfte Werkzeuge: **`e1fc3517`**
(`feat(lighting): add VisualV2 world-clock day and night cycle`). Normaler Push
auf `origin/main` erfolgreich; serverseitiger `ls-remote`-Abgleich bestätigt den
Commit. LFS-Status leer, LFS-Dry-Run ohne ausstehende Objekte, Pointer-fsck OK.
Es wurden keine neuen LFS-Daten hochgeladen und keine Budgets geändert.

Dieser Abschlussnachtrag ist ein eigener reiner Dokumentationscommit; dessen
Hash ist im Git-Verlauf dieses Berichts beziehungsweise im abschließenden
`Saved/ProjectRefinement/DayNightV1/GitFinal.json` festgehalten. Nach seinem Push
wird main nochmals serverseitig mit origin/main abgeglichen. Die 31 ursprünglichen
unversionierten Dateien bleiben absichtlich außerhalb des Commits.
