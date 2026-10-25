# VisualV2 – Beleuchtung und Schatten V3.1

Stand: 25.10.2026. Ausgangspunkt: `464f18957a6cf6e9cd7661d1a50e5807d0fdc07c`,
`main`, ursprünglich mit dem live abgefragten `origin/main` synchron.
Projekt: `/Users/harry/Developer/PokeMonster`; Unreal Engine 5.8.2 / Metal/macOS.

## Ergebnis und exakte Änderung

Die vorhandene VisualV2 erhält sichtbar hellere Schattenoberflächen. Insbesondere
Kronenränder, Baumrinde, Unterwuchs sowie Kleidung und Körperflächen sind besser
lesbar. Sonnige Wege und Wiesen behalten warme Farben; Baum-, Figuren-, Gebäude-
und Felsschatten bleiben sichtbar. Keine neue Lichtquelle und keine neuen Assets.

Ausschließlich `/Game/Maps/Dev_TestMap_VisualV2`, bestehender Actor
`VS_SoftSkyFill` (`DirectionalLight_0`), `DirectionalLightComponent`:

| Einstellung | Vorher | V3.1 |
|---|---:|---:|
| Yaw | 140° | −45° |
| Intensität | 1,12 | 1,8 |

Unverändert: Pitch −40°, Roll 0°, 8000 K, bestehende Lichtfarbe, Kanal 0,
kein Schattenwurf dieses Fülllichts, indirekte Intensität und alle weiteren
Lichteigenschaften. Die Hauptsonne behält Richtung, 7,5 Intensität, 5700 K,
3,5° Source Angle und Schattenwurf. SkyLight, Belichtung, Tonemapping, AO,
Lumen, TAA, Kamera, Innenlicht und die bestehende Spieler-Lesbarkeitshilfe
bleiben unverändert.

Die Wirkung entsteht durch das vorhandene, nun auf die kameraseitigen Flächen
ausgerichtete Fülllicht. Es ist eine künstlerische Ergänzung der Außenbeleuchtung,
keine isotrope physikalische Himmelsbeleuchtung und kein prozentualer Schatten-
Regler. Es hebt auch einige direkt beleuchtete Oberflächen leicht an; die
Vergleiche prüfen deshalb ausdrücklich die Sonnenflächen mit.

**Die weichere Wirkung betrifft den Hell-Dunkel-Kontrast.** Die tatsächliche
Schatten-Penumbra und VSM-Filter wurden nicht verbreitert. Kontaktschatten und
kleine Vertiefungen bleiben kräftiger, damit Objekte ihre Bodenhaftung behalten.

## Untersuchung und verworfene Varianten

Die ursprüngliche Karte verwendet einen stationären SkyLight mit erfasster Szene,
Intensität 1,25, schwarzer unterer Hemisphäre und ohne zugewiesene Cubemap. In der
Map liegen keine SkyAtmosphere-/SkyDome-/Fog-Actors. Das ist eine mögliche
Schwäche der Umgebungsfüllung, kein Beweis einer einzigen Fehlerursache.
Außenbelichtung ist fest (Min/Max 1, Bias 0,3), AO-Intensität 0,65. Es gibt keinen
Grund, diese Werte pauschal zu ändern und damit Sonne oder Kontaktwirkung
zu verschieben.

| Temporäre PIE-Probe | Befund / Entscheidung |
|---|---|
| A: unveränderter Ausgangsstand | Dunkle Kronenränder und kameraseitige Figurenflächen reproduziert. |
| B/C: vorhandene Engine-Tageslicht-Cubemap am SkyLight, Intensität 0,45 / 0,9 | Etwas mehr Füllung, problematische Ränder und Figur weiterhin zu dunkel; verworfen. |
| D: vorhandenes Fülllicht nur auf Yaw −45° drehen | Wirksamer bei Frontflächen, aber schwächere Entlastung dichter Schatten. |
| E: Yaw −45° und Intensität 1,8 | Gewählt: deutlich bessere gemeinsame Lesbarkeit bei zwei Instanzänderungen. |
| F: gedrehtes Fülllicht 1,12 plus SkyLight-Cubemap 0,9 | Weniger gezielter Zugewinn, breitere Sonnenaufhellung, mehr veränderte Parameter; verworfen. |

Die Engine-Cubemap ist ausschließlich eine temporäre Probe; sie wird weder in die
Map übernommen noch als Projektasset kopiert. Keine Wiederholung alter
ShadowAmount-/Screen-Space-Schattenlift-Experimente und keine globalen Shaderänderungen.

## Echte Vorher-/Nachher-Aufnahmen

Zehn Paare aus gewöhnlichem Unreal-PIE, je **2560 × 1440**, bestehende normale
2,5D-Kamera, unveränderte hohe Qualität, primäre und sekundäre Auflösung 100 %,
Dynamic Resolution aus. Pro Paar identische Spieler-/Kameraposition und Rotation
mit maximal 0,03 Toleranz, identischer FOV, Sonne, SkyLight und vollständigen
Postprocess-Werten. Einziger Variantenunterschied sind die beiden Fülllichtwerte.
Vorher-Werte wurden nur im RAM eingesetzt, die gespeicherte Nachher-Map blieb erhalten.

Für Fotoaufstellungen wurde der vorhandene RAM-Savetransport und eine temporäre
Positionssetzung verwendet; dies ist getrennt vom anschließenden echten Fußlauf.
Laufende Animationen und frei bewegte Pokémon sind nicht framegleich. Unterschiede
in deren Pose/Position sind kein Beleuchtungsnachweis. Statische Boden- und
Gebäudeflächen sowie der Kameramatch sind die verlässlicheren Kontrollen.

Die Medien bleiben bewusst lokal unter `Saved/ProjectRefinement/LightingV31`.
Die folgenden Links funktionieren im lokalen Projekt, die Bilder werden nicht auf
GitHub hochgeladen. In jedem Vergleich steht links der vorherige Stand, rechts V3.1.

| Motiv | Echter Vergleich | Originale QHD-Dateien |
|---|---|---|
| Sonnige Wiese | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/SonnigeWiese.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/SonnigeWiese.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/SonnigeWiese.png) |
| Spielfigur unter Krone | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Baumkrone.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Baumkrone.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Baumkrone.png) |
| Kronenrand | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Kronenrand.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Kronenrand.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Kronenrand.png) |
| Dichter Wald | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/DichterWald.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/DichterWald.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/DichterWald.png) |
| Waldweg | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Waldweg.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Waldweg.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Waldweg.png) |
| Heilhaus / Gebäude | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Gebaeude.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Gebaeude.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Gebaeude.png) |
| Felsen | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Felsen.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Felsen.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Felsen.png) |
| NPC / Spieler | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/NPC.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/NPC.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/NPC.png) |
| Pokémon / Ufer | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/PokemonUfer.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/PokemonUfer.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/PokemonUfer.png) |
| Innenraum-Kontrolle | [Vergleich](../Saved/ProjectRefinement/LightingV31/Comparisons/Innenraum.jpg) | [Vorher](../Saved/ProjectRefinement/LightingV31/FinalComparison/Before/Innenraum.png) / [Nachher](../Saved/ProjectRefinement/LightingV31/FinalComparison/After/Innenraum.png) |

Deklarierte Ausschnitte der Originalbilder: sonniges Wiesengras mittlere
Codewerthelligkeit **+5,33 %**, Boden am Kronenrand **+53,60 %**, Innenraumboden
**−0,01 %**. Die Rechtecke und Rohwerte stehen in `ImageControls.json` und im
versionierten `Acceptance.json`. Es sind Bildcodewerte, keine physikalischen
Lichtmessungen oder allgemein gültigen Wahrnehmungsprozente. Der ebenfalls
protokollierte Torsoausschnitt ist wegen Animation/Überlagerung nur ergänzend.
Sonnenflächen wirken in den geprüften Bildern weder ausgebrannt noch ausgewaschen.

Zusätzlich zwei echte kurze Bewegungssequenzen mit je 139 nativ präsentierten
Frames: [Kronenrand](../Saved/ProjectRefinement/LightingV31/Motion/CanopyEdge.mp4)
und [dichter Wald](../Saved/ProjectRefinement/LightingV31/Motion/DenseForest.mp4).
Je ungefähr 5 Spielsekunden, 2331 × 1311 dargestellter Slate-Ausschnitt bei festem
QHD-Spielviewport. Aufnahme bei 0,20 Spielzeitfaktor, danach Normalgeschwindigkeit
über Originalzeitstempel; keine interpolierten Frames, kein Echtzeit-FPS-Nachweis.
Stichproben der Bewegungsframes zeigen keine neue großflächige Schattenumschaltung
oder Lichtquelle. Eine allgemeine Flimmerfreiheit sämtlicher TAA-/Vegetationsfälle
ist mit diesen kurzen Sequenzen nicht bewiesen.

## Technische Prüfungen

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | **Exit 0**, 12,30 s; `LightingV31Build/Result.json`. |
| Vollständige Projekt-Automation | **210 erfolgreich, 0 mit Testwarnungen, 0 fehlgeschlagen, 0 ausstehend**; Engine Exit 0. |
| Strenger vorhandener QA-Wrapper | **Exit 0**, tatsächlich bestanden; `LightingV31Automation/Result.json`. Das gesamte Engine-Log ist trotzdem nicht warnungsfrei. |
| Zwölf bestehende Map Checks | Alle **0 Fehler / 0 Warnungen**, abgegrenzte Logabschnitte und `MapCheckResults.json`. |
| Normaler VisualV2-PIE-Fußlauf | **67 Schritte, 254,57 m**, Eingaben/Physik, eine reguläre Wildbegegnung und Rückkehr; `Footrun/Result.json`. |
| Bewegung / Sprint / Menü | Acht Richtungen, Sprint und Menüfokus bestanden, vorhandene Eingabesimulation. Kein neuer physischer Controller-Test behauptet. |
| Heilhaus | Über normale Wege betreten/verlassen, Heilerinteraktion/Heilung und Innenkamera bestanden. |
| Save/Load | Zweimal vorhandener RAM-Testtransport; Sitzung restauriert, ursprüngliche Save-Datei unverändert. |
| Szenengrenze | **1466 vorhandene Actors, 0 hinzugefügt/entfernt**. Vollständige Inventur erlaubt nur Fülllicht-Yaw und Intensität; sämtliche übrigen Lichtparameter geprüft. |
| Frischer Editorstart | Gespeicherte Map erneut geladen; Werte und komplette Szenengrenze erfolgreich geprüft, keine ungespeicherten Pakete. |

Der Fußlauf setzt einmal einen dokumentierten Startanker und läuft danach tatsächlich
über Wege, Brücke, Wald und Dorf. Keine Teleports entlang des Prüfpfads; das normale
Heilhaus-Innenraumprinzip bleibt aktiv. Er nutzt bestehende Softwareeingaben, keinen
behaupteten menschlichen Tastatur-/Hardwaredurchlauf. Keine Gameplayänderung nötig.

## Warnungen, erster Absturz und Grenzen

- Die externe Engine-iOS-Hilfe `idevice_id` meldet weiterhin `Bad CPU type in executable`,
  Fehler 86. In diesem Lauf lagen diese Meldungen außerhalb der Testzuordnung;
  daher 210 erfolgreiche Tests und Wrapper Exit 0. Die Meldungen werden nicht
  unterdrückt und das gesamte Log wird ausdrücklich nicht als warnungsfrei bezeichnet.
- Weitere beobachtete Startup-Meldungen: `UE::UnifiedErrorTest` / `Condition failed`,
  MCP-HTTP-Listener kann Port 8000 nicht binden, bestehender Python-Namenskonflikt
  `Information` / `bInformation` sowie MCP-Lizenzhinweis. Diese werden getrennt vom
  Projekt-Testresultat geführt; keine Nebenänderungen an Plugins oder Systemeinstellungen.
- Die erste temporäre SkyLight-Probe stürzte nativ mit
  `pthread_rwlock_init failed with error 16` / `PThreadsSharedMutex.h:32` ab.
  Damals wurden zusätzlich viele Animations-/Bewegungskomponenten pausiert und eine
  explizite Sky-Neuerfassung angefordert. **Die genaue Ursache ist ungeklärt**;
  keine gesicherte Schuldzuweisung an SkyLight. Es wurde keine Map gespeichert,
  alle 44 geschützten Dateien waren danach bytegleich. Der Prozess beendete sich
  selbst; kein Force Quit. Die reduzierten Folgestudien ohne diese Zusatzoperationen,
  finaler Fußlauf, Aufnahmen und frischer Editorstart liefen erfolgreich.
- Sehr tiefe Kontaktstellen, dunkle Kleidung und vollständig verdeckte Flächen
  bleiben natürlich dunkler. Die Lösung garantiert keine identische Helligkeit für
  jede Oberflächennormale; sie ist eine gerichtete bestehende Fülllichtlösung.
- Keine neuen Schattenpasses, Lichtquellen, Instanzen oder Shader. Daher keine
  zusätzliche strukturelle Renderlast eingeführt. Keine auffällige neue Störung im
  Fußlauf beobachtet; keine FPS-/GPU-Benchmarkbehauptung oder Leistungsgarantie.

## Schutz, Rücknehmbarkeit und GitHub

Elf andere Maps einschließlich Westland und Biom-Testmap bleiben bytegleich.
Alle 31 vorbestehenden unversionierten Dateien, Originalquellen und der reguläre
Spielstand werden per SHA-256 erhalten. Beide Verweise auf Vollbackup
`03492bd96b4dba44692f675c19d5f11abfa86b4b` bleiben unverändert. Keine Kopie,
kein Worktree, kein neuer Backupordner und keine destruktiven Git-Befehle.

`Settings.json` enthält die vollständigen beiden Zustände. Rücknahme gezielt am
einen bestehenden Actor: Intensität 1,12, Yaw 140°. Keine ganze Map zurücksetzen,
keine fremden Änderungen überschreiben. `Apply.py` erlaubt nur den exakt geprüften
Ausgangsstand; `Validate.py` prüft anschließend die komplette Szene.

GitHub-Sicherung abgeschlossen: Commit **`1a293f50cc8a0362a19577b923f844f402c71fc9`**
(`feat: soften VisualV2 shadow contrast with existing fill light`), regulär auf
`origin/main` gepusht. Lokales HEAD, Tracking-Ref und live abgefragter Remote waren
anschließend identisch. **Ein LFS-Objekt mit 4.773.570 Bytes** wurde von GitHub
zurückgelesen und per SHA-256 verifiziert:
`928afffc4ee62e5336524ff3a493cf9e00fa8bb7981c6401727ac4c969075ed1`.
Keine Budgetänderung, kein Force-Push. Der ergänzende Dokumentationscommit
protokolliert ausschließlich diesen tatsächlichen Nachweis.

19 gezielt kontrollierte Paketdateien; keine Kontrollbilder, Videos, Caches oder
Saves committed. Alle 5450 bisherigen Kerndateien geprüft: 5447 unverändert;
nur Zielmap, Technik und Entscheidungen sind beabsichtigte Bestandsänderungen.
43 geschützte Dateien außerhalb der Zielmap (einschließlich der 31 ursprünglichen
unversionierten Dateien) sind bytegleich. Erweitertes Kernmanifest: 5465 Dateien,
keine fehlend oder unerwartet geändert. Der versionierte Arbeitsbaum ist sauber;
die 31 ursprünglichen unversionierten Dateien bleiben bewusst lokal erhalten.

Die technische Prüfung ist abgeschlossen. Empfehlung: Die freundlichere Variante
an den echten Vergleichen visuell abnehmen; keine automatische Übertragung auf
andere Maps und kein anschließender weiterer Art-Pass.
