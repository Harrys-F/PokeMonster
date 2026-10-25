# VisualV2 Environment Quality V3 – Prüfbericht

Stand: 25.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`.
Ausgangsstand `ef1ba32749ae800e3093098e7a7b6d62410ff33a`, zu Beginn direkt auf GitHub bestätigt.
Einzige bearbeitete Karte: `/Game/Maps/Dev_TestMap_VisualV2`.

## Ergebnis

Die bestehende Karte ist tatsächlich überarbeitet und nach regulärem Neuladen in Unreal geprüft.
Die sichtbarste Verbesserung sind räumliche Grasgruppen auf den bisher weitgehend texturierten
Flächen. Größere Bodenstrukturen, zusätzliche Vegetationsinseln, Stein-/Fassadendetails und
weicher beleuchtetes Wasser ergänzen den vorhandenen malerischen 2,5D-Stil. Wege bleiben frei.
Keine neue Karte, keine neuen Gebäude oder Gebiete und keine Übernahme der Biom-Waldkamera
oder Schwimmtechnik. Die visuelle Endabnahme bleibt bei Harry.

**Editor-Build erfolgreich; 210 Automationstests ohne Fehlschlag, davon einer mit externen
Warnungen; zwölf Map Checks jeweils 0 Fehler/0 Warnungen; echter 254,83-m-PIE-Fußlauf bestanden.**
Der strenge QA-Wrapper hat wegen der Warnungen **Exit 1**, keinen vollständigen Pass.
Einzelne tiefe Kronenschattenränder lassen die Figur weiterhin zu dunkel erscheinen.

## Tatsächliche Änderungen

| Bereich | Umsetzung und sichtbare Wirkung |
|---|---|
| Gras | Drei neue echte, gebogene Halm-Meshes, 28/37/31 Halme je Büschel; Ausgangshöhen 17,4/28,1/32,9 cm. 3.548 Büschel in ungleichen Pflanzentaschen mit freien Bereichen. Opaque, zweiseitig, matte Oberfläche, unter 1 cm Spitzenbewegung. Keine transparenten Gras-Bildkarten. |
| Boden | Drei private Ableitungen der vorhandenen Landschaftsmaterialien. Größere Wiesen-/Waldboden-Texturmaßstäbe, sanfte Makrofarbvariation und flache Normalenstruktur. Bestehende regionale Erde-/Laub-/Moos-/Kiesmischungen und organische Wegmasken weiterverwendet. |
| Unterholz und Ufer | 70 zusätzliche vorhandene Farne, 55 Blüten-/Kräutergruppen, 25 Wurzelstücke, 70 Moospolster und 85 Kieselgruppen. Insgesamt **3.853 zusätzliche Instanzen in acht HISM-Gruppen**. Abstandsfelder halten Wegkorridore, Wasser, Gebäude und Interaktionsstellen frei. |
| Felsen | Private bemalte Steinvarianten mit gebrochener Farbvariation, dezenten Riss-/Normaldetails und Moos auf geeigneten oberen Flächen. Originalmeshes und Collider bleiben erhalten. |
| Gebäude | Fünf private Varianten für vorhandenes Holz, Fachwerk, Stein, Putz und Dach. Unregelmäßige Verwitterung ergänzt die vorhandenen gemalten Texturen. Die bestehende Cutaway-Anbindung bleibt enthalten; Innenraum und Gebäudegeometrie unverändert. |
| Brücke | Bestehende Geometrie und Kollision unverändert; weniger gesättigtes, matteres gealtertes Eichenholz mit dezenter Maserung und Abnutzung. |
| Wasser | Ursprüngliche Form und weiche Ufermaske erhalten. Beleuchtete transparente Oberfläche mit langsam bewegten Normalen, Tiefen-/Randfarben und Unterstützung für Bildschirmreflexionen. Kein Planar-Capture, keine Brechung, keine neue Wasser- oder Schwimmlogik. |
| Licht | Ausschließlich das vorhandene schattenlose Außenfülllicht `VS_SoftSkyFill`: Intensität **1,0 → 1,12**. Dies ist kein behaupteter visueller Prozentgewinn. Hauptlicht, Skylight, Belichtung, Innenlicht, Lumen, TAA und Kameras bleiben erhalten. Keine zusätzlichen detaillierten Blattschatten. |

Neue Laufzeitassets ausschließlich unter `/Game/Environment/VisualV2EnvironmentV3`:
**17 Assets**, davon drei Grasmeshes und 14 Materialien/Instanzen.
Eine neue Blenderquelle und drei zugehörige FBX-Exporte liegen unter
`Art/World/VisualV2EnvironmentV3`. Alle bisherigen Blender-/Meshy-Quellen bleiben erhalten.
Es wurden keine externen Modelle erzeugt, gekauft oder Plugins installiert.

Die Instanzgruppen haben keine Kollision, keinen eigenen Schattenwurf und keinen zusätzlichen
Distance-Field-/dynamischen GI-Beitrag; Culling 5.000–7.000 cm. Bestehende Vegetation und
Bäume werden nicht entfernt. Baumrinde und Kronengeometrie bleiben die vorhandenen Assets;
Wurzeln, Moos und Unterholz verfeinern ihre Einbindung. Keine neue Baum-Modellfamilie behauptet.

## Isolation und Wiederherstellung

`Art/World/VisualV2EnvironmentV3/Scope.json` dokumentiert jede neue Instanz, sämtliche
**120 Materialbindungen** und die einzige Lichtänderung. Der vollständige Szenenvergleich
prüft alle **1.458 vorhandenen Actors**, ihre Transforms, Kollisionen, bisherigen Instanzen,
Postprocessing und WorldSettings. Außer den dokumentierten Materialbindungen und der
Fülllichtintensität bleiben sie gleich; acht dekorative Actors kommen hinzu, keiner entfällt.

Gemeinsame Ausgangsassets werden ausschließlich gelesen. Westland, Biom-Testmap und alle
anderen elf Karten bleiben bytegleich. Geschützt sind außerdem die 31 schon zuvor
unversionierten Dateien, Spielstände, alle Charakter-/Pokémon-Assets und Originalquellen.
Der vorhandene Kerndateivertrag wird nur mit exakt freigegebenen Änderungen fortgeschrieben.
Die beiden Vollbackup-Refs bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.
Keine Projektkopie, kein Worktree, kein Save-Backup und kein destruktiver Git-Befehl.
Ein regulärer Git-Revert des Arbeitspakets kann die Gestaltung zurücknehmen.

## Echte QHD-Vergleiche

**14 geprüfte Vorher-/Nachherpaare**, jeweils echte Unreal-Ausgabe mit **2560×1440** und
unveränderter normaler Spielkamera. Perspektive −50°/−45°, FOV 35°, Außenabstand 2850 cm;
Innenraum verwendet seine bestehende Kamera. Primärer/sekundärer Screen Percentage 100,
Dynamic Resolution aus; alle erfassten `sg.*`-Qualitätswerte 3. Player-/Kamerapositionen und
Rotationen stimmen je Paar innerhalb 0,03 cm/Grad überein.

Zusätzlich zu den ursprünglichen Vorheraufnahmen wurde der frühere Umgebungszustand für
kontrollierte A/B-Bilder **ausschließlich in einer temporären PIE-Welt** rekonstruiert:
ursprüngliche Materialbindungen/Fülllicht, neue Dekoration unsichtbar. Kein Quellasset und
keine Karte zurückgeschrieben. So sind die vollständigen finalen Qualitätswerte direkt
vergleichbar. Figurenposen, Wasser, Gras und temporale Verarbeitung können zeitlich abweichen.
Fotopositionierung ist ausdrücklich vom tatsächlichen Fußlauf getrennt.

Die Tafeln skalieren beide echten Bilder identisch; keine generierten oder retuschierten
Szenenpixel. Alle Medien bleiben lokal unter `Saved/ProjectRefinement/EnvironmentV3/`.

![Wiese – echter Unreal-Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Wiese.jpg)

![Bach und Brücke – echter Unreal-Vergleich](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/BachBruecke.jpg)

Weitere Vergleiche:

- [Wald und Unterholz](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Wald.jpg)
- [Ostwald](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Ostwald.jpg)
- [Wege und Felsen](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/WegeFelsen.jpg)
- [Heilhaus](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Heilhaus.jpg)
- [Fassade](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Fassade.jpg)
- [Uferabzweig](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Uferabzweig.jpg)
- [Spielfigur im Sonnenlicht](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Sonne.jpg)
- [Spielfigur im Schatten](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/Schatten.jpg)
- [Innenraumkontrolle](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/InnenraumKontrolle.jpg)
- [Pokémon an der Wiese](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/PokemonWiese.jpg)
- [Pokémon im Wald](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/PokemonWald.jpg)
- [Pokémon am Ufer](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/Comparisons/PokemonUfer.jpg)

Verlustfreie QHD-Originale: `VerifiedBefore/` und `VerifiedFinal/`; ursprüngliche
unveränderte Vorherserie: `Before/`. `Comparisons.json` enthält die SHA-256-Zuordnung.

Kurze echte Bewegungsnachweise:
[Gras und Kamerabewegung](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/MotionFinal/Grass.mp4),
[Wasser und Brücke](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EnvironmentV3/MotionFinal/Water.mp4).
134/128 tatsächlich dargestellte Frames, jeweils rund fünf Spielsekunden,
26,88/25,42 Samples pro Spielsekunde. Aufnahme mit Zeitdilatation 0,20 und anschließender
Wiedergabe anhand der echten Spielzeitstempel; **kein Echtzeit-FPS-Messwert** und keine
Zwischenbilder. Tatsächlicher Slate-Ausschnitt 2331×1311, kein als QHD ausgegebenes Upscaling.
Die separaten Standbilder sind echte QHD-PNGs. In den kurzen Sequenzen keine dominanten
Alpha-Muster; feinste Halme und TAA bleiben dennoch Gegenstand der visuellen Abnahme.

## Prüfungen und behobene technische Probleme

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | Erfolgreich, Exit 0, `EnvironmentV3Build02/Result.json`. |
| Vollständige Automation | **209 Success, 1 SuccessWithWarnings, 0 fehlgeschlagen, 0 nicht ausgeführt**, Engine Exit 0. |
| Strenger QA-Wrapper | **Exit 1** wegen der unten benannten Warnungen; ausdrücklich kein vollständiger Pass. |
| Zwölf vorhandene Map Checks | Jeweils **0 Fehler / 0 Warnungen**, scoped Engine-Log und `MapCheckResults.json`. |
| Echter VisualV2-PIE-Fußlauf | **67 Schritte, 254,83 m**, reale Eingaben/Physik, kein Testteleport während der Route; eine dokumentierte Startaufstellung davor. |
| Gameplay im Fußlauf | Brückenquerung, Wald-/Dorfwege, acht Richtungen, Sprint, Menü/Fokus, ein normaler Wildkampf mit Rückkehr, Heilhaus betreten/verlassen, B-Heilerinteraktion und Heilung. |
| Save/Load | RAM-Preview des bestehenden Systems, keine Kopie/Überschreibung der Save-Datei; SHA-256 des echten Saves unverändert. |
| Frisch geladenes Endprojekt | Scope erneut bestanden; keine Material-Kompilierfehler oder Default-Material-Fallbacks im frischen finalen Editorlog. |
| Kampf/Fang/Team/Fortschritt/Entwicklung | Bestehende vollständige Automation ohne Fehlschlag; keine Änderungen an diesen Implementierungen. Kein neuer manueller Fang-/Entwicklungsfilm in diesem Art-Auftrag. |
| Controller | Vorhandene Softwareeingaben verwendet; keine Änderung der Belegung, kein neuer physischer Hardwaretest behauptet. |
| Performance | Keine FPS-/GPU-Testreihe. Instancing, Opaque-Gras und unveränderte Schattenwerfer; keine Performancegarantie aus Zeitlupenaufnahmen abgeleitet. |

**Externe Warnungen:** Im Test `PokeMonster.Creatures.Overworld.SmoothMovementAndFirstPartySlot`
meldet der Engine-Helfer `idevice_id` zweimal `posix_spawn ... failed (86, Bad CPU type in executable)`
beziehungsweise `Failed to launch Tool`. Diese Warnungen bleiben offen. Generische
Engine-Startup-Selbsttestmeldungen (`Condition failed`) sind von Projektassertions getrennt.

Der erste Build deckte eine bislang verdeckte Unity-Build-Kollision zwischen anonymen
Konsolenregistrierungen beider Testgelände auf. Ausschließlich der interne Namensraum in
`PokeMonsterNPCTestGround.cpp` wurde getrennt; öffentliche Befehle und Verhalten unverändert.
Keine NPC-Rigs oder Animationen verändert. Der anschließende Build und die Automation bestanden
mit dem genannten externen Warnstatus.

Weitere korrigierte Autoren-/Prüffehler: Anschlussname des neuen Vertexfarbeninputs,
reservierter HLSL-Variablenname bei der Farbraumkorrektur, Totzone des simulierten Stick-Signals
im ersten Fußtest und eine lokale Pfadvariable des Aufnahmehelfers. Die Wiederholungen sind
erfolgreich; vorherige Fehlerlogs wurden nicht als erfolgreiche Prüfungen gewertet.
Die erste zu blasse Grasfassung und die Wasserprobe mit harten Per-Pixel-Kronensilhouetten
wurden verworfen. Die verwendete weichere Wasserfassung ist im Fußlauf und Endvergleich geprüft.

## Grenzen und Empfehlung

- Die neue räumliche Vegetation ist aus der normalen Spielkamera klarer lesbar.
  Bestehende feine Texturperiodik und einzelne flach wirkende Alt-Pflanzen bleiben erkennbar.
- Wasser bleibt stilisiert. Bildschirmreflexionen können nur verfügbare Bildinhalte darstellen;
  keine vollständigen Offscreen-/Planarreflexionen oder neue Wasserphysik behauptet.
- An einzelnen tiefen Kronenrändern bleibt die braune Spielfigur zu dunkel. Die vorhandene
  gezielte Charakteraufhellung und Sichtfreistellung bleiben erhalten. Ein zusätzlicher
  temporärer Fülllichtversuch mit 1,35 brachte dort keine ausreichende Verbesserung und
  wurde **nicht gespeichert**. Keine erneute globale Schatten-Aufhellung auf Verdacht.
- Keine neue Baumgeometrie, keine vollständige Neuerstellung aller Boden-/Gebäudetexturen
  und keine automatische künstlerische Freigabe. Figuren, Pokémon, Wege und Innenraum
  funktionieren weiterhin; die Randfall-Lesbarkeit benötigt eine spätere gezielte Abnahme.
- Originalquellen, übrige Karten und unversionierte Dateien bleiben geschützt.
  Keine Kontrollmedien oder generierten Builds werden auf GitHub hochgeladen.

Empfehlung: Diesen geprüften Umgebungsstand anhand der 14 Bildpaare visuell abnehmen.
Eine weitere automatische Ausweitung oder ein zusätzlicher Landschaftspass ist nicht Teil
 dieses Abschlusses. Präzise Resultate: `Tools/VisualV2EnvironmentV3/Acceptance.json`.

## GitHub

Nur geprüfte neue Quellen/Assets/Werkzeuge, VisualV2, die minimale Buildkorrektur und
Dokumentation werden gezielt gesichert. Keine History-Änderung, kein Force-Push, keine
Budgetänderung. Das bestätigte Git-LFS-Budget von 0 USD bleibt unangetastet.
Konkrete Commit- und Remote-/LFS-Ergebnisse werden nach der Sicherung ergänzt.
