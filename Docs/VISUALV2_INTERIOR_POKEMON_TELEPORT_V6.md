# VisualV2 – Interior, Pokémon & Teleport V6

Stand: 03.11.2026. Projektbasis `950e2c973ed41dc51518203d562858c1a90cbcea`, Branch `main`. Ausschließlich vorhandenes Projekt und vorhandene VisualV2. Westland bleibt geschützt.

## 1. Ergebnis und Grenzen

Bestehende TestGround-Befehle sind aus der Editorkonsole während PIE und im Development-Spielprozess wieder nutzbar. Alle 19 bisherigen Ziele sowie 49 neue statische Meshy-Prüfkandidaten sind erreichbar. Pikachu und Karpador bewegen sich nachweislich schneller. Das Heilhaus besitzt eine geschlossene Decke, ausgearbeitete Eingangsseite und wärmere Raumoberflächen bei weiterhin vier sichtbaren Wänden.

**Die 49 neuen Modelle sind keine spielbereiten Pokémon:** Quell-GLBs besitzen keine Skelette, Gewichte oder Animationen. Es wurden keine erfundenen Bewegungen, Arten-/Kampfdaten oder Wildspawns ergänzt. Maßstab/Frontrichtung und spätere LOD-/Animationsfreigabe bleiben offen. Technische Importprüfung ersetzt Harrys gestalterische Abnahme nicht.

**Stabile 30 FPS bleiben nicht nachgewiesen.** Der reale unaufgezeichnete Rundgang erreicht 23,98 FPS, Frame-p95 57,25 ms. Keine globale Grafikreduzierung oder Performanceoptimierung.

## 2. Teleportfehler und gezielte Korrektur

Vorher reproduziert: `pm.TestGround.Go Pikachu` und `Karpador` funktionieren mit dem PIE-Spiel-World, bleiben mit dem tatsächlich übergebenen Editor-World wirkungslos. `PIEBefore02/Result.json` hält diesen Unterschied fest. Ursache ist die bisher ausschließlich am übergebenen World prüfende Konsolenverarbeitung; keine fehlende Map, verlorene Artenregistrierung oder verschobene Actor-Referenz.

Die bestehende TestGround-Klasse löst aus Editor-/Null-Kontext die einzige passende laufende VisualV2-PIE-/Game-Welt auf. Ein expliziter fremder Game-World wird niemals umgeleitet; mehrere passende Welten werden sicher abgelehnt und die Spielkonsole empfohlen. Ungültige Namen liefern eine verständliche Meldung und die verfügbaren Ziele im Log.

Der vorhandene Testboden liegt unverändert bei Mittelpunkt `(-7500,-20000,-20000)` cm. Stationsraster und bestehende Artenregistrierung bleiben erhalten. `TeleportTo` prüft vorhandene Kollisionen. Rückkehranker werden durch weitere Besuche nicht überschrieben. Return stellt ursprüngliche Weltposition, Interaktionsblickrichtung, Kameraart, Third-Person-Orbit und Zoom wieder her. Bestehende Spring-Arme werden nach dem Teleport ohne Lag-Versatz aktualisiert; kein globaler Kameraparameter wird verändert. Der vorhandene Begleiter-Teleportpfad genügt und wurde nicht ersetzt. Team/Inventar/Save-Architektur bleiben unberührt.

### Alle bisherigen funktionierenden Ziele

| Station | Vollständiger Befehl |
|---:|---|
| 1 | `pm.TestGround.Go Bisasam` |
| 2 | `pm.TestGround.Go Glutexo` |
| 3 | `pm.TestGround.Go Glurak` |
| 4 | `pm.TestGround.Go Schiggy` |
| 5 | `pm.TestGround.Go Raupy` |
| 6 | `pm.TestGround.Go Smettbo` |
| 7 | `pm.TestGround.Go Hornliu` |
| 8 | `pm.TestGround.Go Bibor` |
| 9 | `pm.TestGround.Go Habitak` |
| 10 | `pm.TestGround.Go Pikachu` |
| 11 | `pm.TestGround.Go Raichu` |
| 12 | `pm.TestGround.Go Myrapla` |
| 13 | `pm.TestGround.Go Enton` |
| 14 | `pm.TestGround.Go Machomei` |
| 15 | `pm.TestGround.Go Nebulak` |
| 16 | `pm.TestGround.Go Gengar` |
| 17 | `pm.TestGround.Go Karpador` |
| 18 | `pm.TestGround.Go Garados` |
| 19 | `pm.TestGround.Go Glumanda` |

`pm.TestGround.Go` ohne Argument bzw. `0`: Mitte. `pm.TestGround.Go 1` bis `19`: obige Stationen. Historischer interner Alias `pm.TestGround.Go Zunderlauf` bleibt für Glumanda kompatibel; sichtbare Bezeichnung ist Glumanda.

Weitere vorhandene Befehle: `pm.TestGround.List`, `pm.TestGround.Return`, `pm.TestGround.Reset`, `pm.TestGround.Mode auto|idle|walk|run|turn|directions|reset`, `pm.TestGround.React attack|hit|faint|happy`. Die Alternativen werden jeweils einzeln eingegeben. Keine Begegnungen/Speicherung im Modelltestbereich. Freie Außenansicht ist Voraussetzung; kein Besuch während Kampf, Dialog/Input-Sperre oder Innenraumaufenthalt.

### Neue statische Kandidaten

`pm.TestGround.Go Modell:<Name>` verwendet die Tabelle in Abschnitt 5. Leerzeichen im Dateistamm werden durch `_` ersetzt, z. B. `Modell:Nidoran_m`. Nur `Mode idle`, `turn` und `reset` sind verfügbar; Turn ist eine Inspektionsdrehung, keine Körperanimation. Walk/Run/Reaktionen werden ausdrücklich abgelehnt. Return funktioniert wie bei den bisherigen Zielen.

Keine zweite Pokémon-Artenliste: vorhandene TestGround-Klasse entdeckt StaticMesh-Metadaten rekursiv unter `/Game/Characters/Creatures/ModelIntakeV6/<Name>/...`. Ein frischer `-game`-Prozess benötigt den gezielten Metadatenscan beim ausdrücklichen List-/Go-Aufruf. Normales Gameplay lädt diese Modell-/Texturdaten nicht. Jeweils ein transienter Inspektionsactor, alte bewegte Testexemplare während der Rohmodellansicht pausiert/verborgen; kein Wild-Pokémon verdrängt.

Im ersten Arbok-Nachladetest wurde nach dem Laufzeitaufbau eine aktiv gewordene Komponentenkollision beobachtet. Zusätzliches `SetActorEnableCollision(false)` sichert die reine Vorschau unabhängig von nachgeladenen Mesh-Kollisionsvoreinstellungen ab. Der erfolgreiche Nachtest prüft alle 49 Kandidaten auf NoCollision, Bodenkontakt und vollständige Rückkehr.

## 3. Pikachu und Karpador

Nur `DA_Pikachu` und `DA_Karpador` geändert. Keine neuen Clips, keine Rig-, KI-Code-, Habitat- oder Kampfänderung. Authored Walk-/Run-/Swim-Referenzgeschwindigkeiten bleiben unverändert, damit die vorhandene streckenbezogene Phasenberechnung mit dem Tempo skaliert.

| Parameter (cm/s bzw. Sekunden) | Vorher | Nachher |
|---|---:|---:|
| Pikachu Walk-/Run-Override | 14,95 / 32,20 | 42 / 56 |
| Pikachu natürlicher Walk mit Artmultiplikator 0,75 | 11,2125 | 31,5 |
| Pikachu Mindestweg / Pause | 180 cm / 1,4–3,8 s | 110 cm / 0,6–1,8 s |
| Pikachu Animationsreferenz Walk / Run | 13 / 28 | unverändert |
| Karpador Override (0 = Präsentationsvorgabe) | 0 / 0, effektive Basis 35 / 70 | 56 / 61,25 |
| Karpador Art-Walk-Multiplikator | 0,75 | 1,0 |
| Karpador natürlicher Swim | 26,25 | 56 |
| Karpador Swim-Referenz | 35 | unverändert |

Pikachu behält Beschleunigung 90 cm/s², Bremsung 180 cm/s² und Drehgrenze 110°/s. Bestehende Ruhe-, Beobachtungs-, Sozial- und Spielerreaktionen bleiben erhalten. Die kurzen Pausen ersetzen keine natürliche KI.

Karpadors vorhandene Schwimmrate ist auf maximal 1,75× begrenzt. Daher 56/35 = 1,6× beim normalen Schwimmen und 61,25/35 = 1,75× im schnellen Prüfmodus; kein zu hohes Tempo oberhalb der vorhandenen Animation. Der ursprüngliche Walk-Clip dient weiterhin der vorhandenen Fisch-/Zappelbewegung. Land-/Kampfclips und Präsentationsassets bytegleich. Keine künstliche Landlaufanimation.

Gemessen an tatsächlich bewegten Actors: TestGround Pikachu bis 42 cm/s, Karpador bis 56 cm/s; je rund 320 cm sichtbare Strecke im erfassten Prüfabschnitt. Natürliche Population: Pikachu maximal 31,5 cm/s und 151,66 cm Weg im 12-s-Beobachtungsfenster; Karpador maximal 56 cm/s und 491,96 cm. Pausen zählen mit. Alle erfassten Positionen innerhalb der vorhandenen Habitatgrenzen. Keine erzwungenen Wild-KI-Ziele oder geänderten Spawnwahrscheinlichkeiten.

## 4. Heilhaus

Der bisherige versetzte Raum bleibt an seinen bestehenden Koordinaten. Keine Grundriss-, Heiler-, Möbelpositions-, Türschwellen-, Laufkollisions- oder globalen Kameraveränderung. Alle 18 bestehenden Wandactors der vier Seiten bleiben sichtbar, ohne Cutaway/Fade. V5-Türmaskierung und lokale Raumsichtbegrenzung bleiben bestehen.

138 vorhandene Raumactors erhalten ausschließlich lokale Material-/Lichtanpassungen. Sieben neue HISM-Gruppen bündeln dekorative Architektur: Decke, Eichenfachwerk, salbeifarbene Wandbasis, Türhintergrund, kurze Eingangslaibung, Eingangsdecke und matte Fenstereinsätze. Kein vorhandener Actor entfernt. Alle ursprünglichen Außenactors sowie die kompletten V5-Busch-/Zonen-Signaturen sind exakt unverändert.

Neue eigene Materialien unter `/Game/Environment/VisualV2InteriorV6/Materials`: `M_V6_LimePlaster`, `M_V6_SageLimewash`, `M_V6_FrostedWindow`, `M_V6_OakJoinery`, `M_V6_OakFloor`. Eichenmaterialien sind private Ableitungen der vorhandenen Holzoberfläche; Originale nicht geändert. Strukturvariation im Kalkputz, warme Holzfarbtöne, vorhandene Textur-/Normaldetails, keine neuen Fab-Downloads.

Decke bei 3,12 m, sichtbare Balken darunter bei etwa 2,90 m: oberhalb des unveränderten 1,72-m-Kamerablickpunkts. Die vormals kahle Stein-Eingangsseite erhält Putz/Fachwerk/Wandbasis. Ein kollisionsfreier Holz-Türhintergrund liegt deutlich hinter der funktionierenden Übergangsschwelle und verdeckt den Blick aus dem versetzten Raum ins Kartenleere. Er ist keine neue Gameplay-Tür. Matte opake Fenstereinsätze verdecken ebenfalls die unbebaute Umgebung des Remote-Innenraums, ohne zusätzliche Transparenzschichten.

Vorhandene Einrichtung weiterverwendet: QualityV3 `CounterStepped`, `Bookcase`, `HerbShelf`, `Table`, Bänke und beide Behandlungsbetten; ArtV4 Herd, Kräuterschrank, Baldachine, Banner und Fensterborde; ArtV5 Lesesessel, Kissen und Kräuterbücher; bestehende Heilkräutertabletts/Mörser, Pflanzen und Laternen. Kein beliebiges Nachfüllen des Raums.

Alle 13 vorhandenen lokalen Lichter wiederverwendet, kein neues Licht. Lampen wärmer, Fensterlicht neutral-kühler. Vorhandenes breites schattenloses Rect Light von 1000 auf 1500; Kanäle 0+1 unterstützen nun Raum und Figur. Kein globaler Skylight-/Sonnen-/Lumen-/Rendering-Eingriff.

Heiler wird um die unveränderte Tresenkollision über den freien nördlichen Gang erreicht: `(17000,690) → (17230,690) → (17230,560)`. Heilinteraktion restauriert tatsächlich zuvor im Kampf verbrauchte AP und sämtliche KP. Ein-/Ausgang bei pm.Speed 1/2/3, Kamerapitch −12°, Abstand 350 cm, vier sichtbare Wandseiten und isolierter Save/Load bestanden.

## 5. Vollständiger Incoming-Bestand und neue Importe

Tatsächlicher Pfad: `Art/Characters/Creatures/Incoming`; die kleingeschriebene Schreibweise bezeichnet auf diesem Mac denselben Ordner. 88 GLBs plus `.DS_Store`. Gegen den V5-Ausgangsbestand wurden 49 neue GLBs nachgewiesen, insgesamt 608.161.892 Quellbytes. Sämtliche 88 Original-GLBs ohne Skins und Animationen; die 19 bestehenden Spielarten verwenden bereits gesondert aufbereitete Rigs/Clips.

Bereits integrierte Originalquellen erkannt, keine Doppelimporte: Bisasam, Glutexo, Glurak, Schiggy, Raupy, Smettbo, Hornliu, Bibor, Habitak, Pikachu, Raichu, Myrapla, Enton, Machomei, Nebulak, Gengar, Karpador, Garados, Glumanda (`Shiggy.glb` ist die vorhandene Schiggy-Quelle).

20 bereits vor V6 vorhandene, hier nicht neu bearbeitete Quellen: Abra.glb, Aerodactyl.glb, Bisaflor.glb, Bisaknosp.glb, Ditto.glb, Evoli.glb, Georok.glb, Geowaz.glb, Kadabra.glb, Kleinstein.glb, Kokuna.glb, Lavados.glb, Mew.glb, Mewtu.glb, Pantimos.glb, Relaxo.glb, Safcon.glb, Simsala.glb, Turtok.glb, Zapdos.glb. Sie sind nicht als neu integrierte oder spielbereite Arten ausgewiesen.

Alle neuen Quellen besitzen je ein Mesh/ein Material mit OPAQUE/double-sided und eingebetteten JPEG-PBR-Texturen: 31 mit drei, 18 mit zusätzlicher Emission. Interchange übernimmt BaseColor, Metallic/Roughness, Normal und gegebenenfalls Emission. Originale unverändert. Keine Ablösung bestehender spielbarer Modelle.

Importziel jeweils `/Game/Characters/Creatures/ModelIntakeV6/<Name>/<Name>/StaticMeshes/SM_<Name>_Import`; dazu eigene importierte Texturen/Materialinstanz. Meshes besitzen zunächst eine LOD-Stufe. Prüfung normiert die maximale sichtbare Ausdehnung auf 200 cm und setzt die Unterkante auf den Testboden. Dies ist ausdrücklich eine Prüfgröße, kein festgelegter Artmaßstab.

Bei Entoron und Zubat klassifizierte der Importer die blaue BaseColor-Textur irrtümlich als Normalmap (TC_NORMALMAP, sRGB false). An genau diesen zwei eigenen Texturkopien auf TC_DEFAULT/sRGB true korrigiert, Quellbytes und Mastermaterial erhalten. Rollen aller 49 Kandidaten gegen die tatsächlichen GLB-Semantikindizes geprüft; künftiger identischer Import erzwingt diese geprüften Rollen. Frischer nativer Nachtest zeigt korrekt blaue Farben. Frühere grüne/kurzzeitig graue Warmlaufbilder sind kein gültiger finaler Farbvergleich.

Für **jede** folgende Zeile gilt: statischer Import und TestGround-Zugriff bestanden; Rigging/Gewichte, Idle-/Walk-/Run-/Kampfclips, kanonischer Maßstab/Frontrichtung, passende Arten-/Entwicklungs-/Lerndaten und Laufzeitbudget sind vor spielbarer Verwendung noch erforderlich. Deshalb keine dieser 49 Arten neu in die natürliche Weltpopulation aufgenommen.

| Neue Originaldatei | MB (dezimal) | Dreiecke Quelle | Texturen | Vollständiger Prüf-Befehl |
|---|---:|---:|---:|---|
| `Aquana.glb` | 18.85 | 26,231 | 4 | `pm.TestGround.Go Modell:Aquana` |
| `Arbok.glb` | 13.21 | 27,347 | 3 | `pm.TestGround.Go Modell:Arbok` |
| `Arkani.glb` | 13.85 | 26,379 | 3 | `pm.TestGround.Go Modell:Arkani` |
| `Blitza.glb` | 20.76 | 25,752 | 4 | `pm.TestGround.Go Modell:Blitza` |
| `Digda.glb` | 5.33 | 10,096 | 4 | `pm.TestGround.Go Modell:Digda` |
| `Digdri.glb` | 5.31 | 10,338 | 4 | `pm.TestGround.Go Modell:Digdri` |
| `Duflor.glb` | 5.45 | 10,878 | 4 | `pm.TestGround.Go Modell:Duflor` |
| `Entoron.glb` | 5.30 | 21,414 | 3 | `pm.TestGround.Go Modell:Entoron` |
| `Flamara.glb` | 18.27 | 26,236 | 4 | `pm.TestGround.Go Modell:Flamara` |
| `Fukano.glb` | 14.61 | 28,047 | 3 | `pm.TestGround.Go Modell:Fukano` |
| `Giflor.glb` | 6.32 | 10,903 | 4 | `pm.TestGround.Go Modell:Giflor` |
| `Golbat.glb` | 7.26 | 11,228 | 4 | `pm.TestGround.Go Modell:Golbat` |
| `Ibitak.glb` | 16.12 | 26,541 | 3 | `pm.TestGround.Go Modell:Ibitak` |
| `Kicklee.glb` | 6.47 | 26,408 | 3 | `pm.TestGround.Go Modell:Kicklee` |
| `Knofensa.glb` | 5.59 | 11,434 | 4 | `pm.TestGround.Go Modell:Knofensa` |
| `Knogga.glb` | 11.03 | 27,099 | 3 | `pm.TestGround.Go Modell:Knogga` |
| `Knudeluff.glb` | 5.59 | 10,044 | 4 | `pm.TestGround.Go Modell:Knudeluff` |
| `Magmar.glb` | 6.49 | 21,355 | 3 | `pm.TestGround.Go Modell:Magmar` |
| `Nidoking.glb` | 14.08 | 25,877 | 3 | `pm.TestGround.Go Modell:Nidoking` |
| `Nidoqueen.glb` | 14.37 | 25,804 | 3 | `pm.TestGround.Go Modell:Nidoqueen` |
| `Nidoran m.glb` | 11.03 | 26,070 | 3 | `pm.TestGround.Go Modell:Nidoran_m` |
| `Nidoran w.glb` | 12.69 | 25,714 | 3 | `pm.TestGround.Go Modell:Nidoran_w` |
| `Nidorina.glb` | 19.51 | 25,972 | 4 | `pm.TestGround.Go Modell:Nidorina` |
| `Nidorino.glb` | 12.55 | 25,763 | 3 | `pm.TestGround.Go Modell:Nidorino` |
| `Nockchan.glb` | 6.09 | 26,334 | 3 | `pm.TestGround.Go Modell:Nockchan` |
| `Omot.glb` | 8.01 | 11,206 | 4 | `pm.TestGround.Go Modell:Omot` |
| `Onyx.glb` | 6.96 | 21,205 | 3 | `pm.TestGround.Go Modell:Onyx` |
| `Paras.glb` | 6.09 | 10,011 | 4 | `pm.TestGround.Go Modell:Paras` |
| `Parasek.glb` | 6.28 | 10,471 | 4 | `pm.TestGround.Go Modell:Parasek` |
| `Piepi.glb` | 10.50 | 30,869 | 3 | `pm.TestGround.Go Modell:Piepi` |
| `Pixi.glb` | 9.64 | 31,179 | 3 | `pm.TestGround.Go Modell:Pixi` |
| `Pummeluff.glb` | 5.38 | 10,078 | 4 | `pm.TestGround.Go Modell:Pummeluff` |
| `Rattfratz.glb` | 11.37 | 27,439 | 3 | `pm.TestGround.Go Modell:Rattfratz` |
| `Rattikarl.glb` | 13.54 | 27,487 | 3 | `pm.TestGround.Go Modell:Rattikarl` |
| `Rettan.glb` | 14.79 | 26,213 | 3 | `pm.TestGround.Go Modell:Rettan` |
| `Sandamer.glb` | 13.83 | 25,917 | 3 | `pm.TestGround.Go Modell:Sandamer` |
| `Sandan.glb` | 16.13 | 26,771 | 3 | `pm.TestGround.Go Modell:Sandan` |
| `Sarzenia.glb` | 7.35 | 11,350 | 4 | `pm.TestGround.Go Modell:Sarzenia` |
| `Schlurp.glb` | 4.30 | 20,903 | 3 | `pm.TestGround.Go Modell:Schlurp` |
| `Sichlor.glb` | 18.76 | 26,129 | 3 | `pm.TestGround.Go Modell:Sichlor` |
| `Tangela.glb` | 58.07 | 1,382,208 | 3 | `pm.TestGround.Go Modell:Tangela` |
| `Tauboga.glb` | 18.84 | 27,591 | 3 | `pm.TestGround.Go Modell:Tauboga` |
| `Tauboss.glb` | 38.70 | 815,076 | 3 | `pm.TestGround.Go Modell:Tauboss` |
| `Taubsi.glb` | 15.10 | 26,974 | 3 | `pm.TestGround.Go Modell:Taubsi` |
| `Tragosso.glb` | 11.03 | 27,115 | 3 | `pm.TestGround.Go Modell:Tragosso` |
| `Ultrigaria.glb` | 6.22 | 11,194 | 4 | `pm.TestGround.Go Modell:Ultrigaria` |
| `Vulnona.glb` | 11.47 | 30,760 | 3 | `pm.TestGround.Go Modell:Vulnona` |
| `Vulpix.glb` | 11.87 | 31,477 | 3 | `pm.TestGround.Go Modell:Vulpix` |
| `Zubat.glb` | 7.82 | 9,935 | 4 | `pm.TestGround.Go Modell:Zubat` |

Der höchste Quellumfang liegt bei Tangela (1.382.208 Dreiecke). Vor späterer Gameplay-Integration sind abgeleitete LOD-/Geometrieoptimierung und Material-/Animationsbudget erforderlich; nicht am Original und nicht im Rahmen einer globalen Qualitätsreduzierung. Die statische Verfügbarkeit bedeutet keine entsprechende Performancefreigabe.

## 6. Performance

Gemessen auf Mac16,12 / Apple M4, 16 GiB, macOS 27.2 (26B123), UE 5.8.4 CL58902052 / Metal. Frische separate Development-Prozesse. QHD 2560×1440, High, C75/TAAU (nominal 1920×1080 intern), Software-Lumen/IFG, VSM vier Strahlen, Sonne mittags 75°, Uhr 120 Echtminuten/Tag. Bestehende lokale Nutzerkonfiguration nicht geändert.

Je Hauptstelle dreimal 6 Sekunden nach je 4 Sekunden Einlauf, wechselnde Reihenfolge Dorf/Wald/Heilhaus. Mittag über vorhandene isolierte Save-/Clock-Fixture, identische erfasste Kamera/Position und Grafikwerte. Keine Videoaufnahme in Messfenstern; Fotos danach. VSync/FPS-Limit für die Messung temporär aus, ursprüngliche Werte beim Prozessende wiederhergestellt. Pokémon-Population 13 in den gematchten Messfenstern.

| Stelle | FPS vorher → nachher | Frame-p95 ms vorher → nachher | GPU ms vorher → nachher | Game ms vorher → nachher | Render ms vorher → nachher |
|---|---|---|---|---|---|
| Dorf | 23.66 → 23.44 | 48.45 → 57.40 | 29.93 → 29.61 | 3.57 → 3.83 | 42.25 → 42.64 |
| Wald | 24.29 → 25.40 | 47.65 → 44.33 | 40.02 → 38.11 | 3.16 → 3.30 | 41.16 → 39.31 |
| Heilhaus | 24.34 → 28.34 | 46.92 → 42.50 | 39.44 → 32.95 | 3.27 → 3.52 | 40.81 → 35.29 |

Der zusammenhängende reale Rundgang ohne Video umfasst 2350 CSV-Frames: 23.98 FPS, Mittel 41.69 ms, p95 57.25 ms, 1%-Low 5.85 FPS, Maximum 517.24 ms. GPU 34.62 ms, Game 5.07 ms, Render 41.49 ms. Profilabschnitt endet vor Screenshots/Dialog/Kampf/Save/Load/Mapwechsel.

Historische V5-Route: 24,90 FPS / p95 51,55 ms. Die neue Route liegt etwa 3,7 % niedriger, p95 höher. Kein Nachweis allgemeiner Performanceverbesserung und keine 30-FPS-Stabilität. Dorf-p95 ist auch im statischen Vergleich schlechter, während die Innenraummessung deutlich günstiger ausfällt. Thermische/Streaming-/KI- und Laufreihenfolgedrift begrenzen die Kausalzuordnung; kein abwechselndes Hot-Swap-A/B und kein Langzeitbenchmark. Diese Schwankungen werden nicht durch globale Grafikreduzierung kaschiert.

CSV-Spitzen wurden erfasst; keine einzelne Ursache für alle Spitzen behauptet. Grundlegende GPU-/CPU-Überlappung beachten, Passzeiten nicht addieren. Unter anderem laufende Renderer-/Streaming-/PSO-Arbeit sichtbar; die Kosten der Modell-Aufnahmesequenzen gehören nicht zu diesem Benchmark.

## 7. Tests, Fehlversuche und Warnungen

Letzter Editor-Build `EditorBuild05`: Exit 0. Drei neue Automationsfälle: `PokeMonster.VisualV6.TeleportConsoleWorldSafety`, `UnriggedImportInspectionScope`, `PikachuKarpadorSpeedAndStride`. Die bisherigen 330 Tests bleiben enthalten. Der abschließende QA-Report enthält die tatsächlich ausgeführten Werte; siehe unten.

Bestandene echte Abläufe:

- `NativeTeleport04`: sämtliche 19 Namen, Mitte/Index/Glumanda-Alias, ungültiger Name, Rückkehrposition/Blickrichtung/Kamera/Zoom, Begleiter und unverändertes Team, Walk/Run/Turn/Idle, alle 49 Rohmodelle ohne Kollision und mit Bodenkontakt.
- `PIETeleport01`: bestehende Ziele, Editor-Kontext, Bewegung und Rückkehr bestanden; danach an einer echten Rohmodell-Kollisionsprüfung gestoppt und nicht als Gesamt-Pass ausgegeben. Gezielter vollständiger PIE-Nachtest aller Importe `PIEImports03` bestanden.
- `NativeInterior01` und `PIEInterior02`: natürliche sichtbare Begegnung, regulärer Zug/AP-Verbrauch, normaler Fang/Teamzuwachs, Heilerrestaurierung, vier sichtbare Wände, acht Blickrichtungen, Ein-/Ausgang Speed1/2/3, Innenraum-Save/Load.
- `NativeWild02`: bereits gespawnte natürliche Pikachu-/Karpador-Population, tatsächliche Bewegung/Animation und Habitatgrenzen; keine erzwungenen KI-Ziele.
- `NativeGameplay01`: zusammenhängender bestehender Wegerundgang durch Dorf/Wiesen/Wald, Brücke samt Geländerkollision/Speed1/2/3, Kamera, Sprint über Enhanced Input, Cottage, NPC-Dialog, Kampf/Fang, Team/aktiver Begleiter, Weltuhr/Tag-Nacht, Save/Load und tatsächlicher Wechsel nach Dev_TestMap mit Rückladen nach VisualV2.
- `FreshFinal01`: frischer Disk-Start bestätigt unverändertes C75/TAAU/Software-Lumen/IFG/VSM4, Kamera, Uhr und Population.
- `NativeColorFinal01`: korrigierte Entoron-/Zubat-Farben nach frischem Prozess und 5 s Shader-/Streaming-Einlauf sichtbar bestätigt. `PIEColorFinal02` bestätigt dies nach frischem Editorstart und ausreichendem Einlauf ebenfalls.

Alle Saves ausschließlich in eigenen isolierten UserDirs bzw. expliziten PIE-Testslots. Team, AP, Inventar und Uhr beim Save/Load exakt verglichen; Positionstoleranz <0,001 cm und Blickvektor <1e−6 wegen normaler Float-Normalisierung. Kein physischer Controller-Abnahmetest; reale Enhanced-Input-/Spielphysik-Tests und bestehende Controller-Automation, keine Behauptung eines angeschlossenen Gamepads.

Fehlversuche bleiben erhalten: erster Build durch vorhandene Unity-Namenskollision `Capture` zwischen Entwicklungsreview und Save-CPP gestoppt; ausschließlich interner Name des Entwicklungs-Konsolenobjekts präzisiert, Befehl/Entwicklung/Save-Code unverändert. Initiale Python-Material-Property-Ansteuerung korrigiert. Erste Rohmodelltests deckten Kollision und fehlenden frischen Metadatenscan auf. Ein Wild-Beobachtungsskript verwendete zunächst den Wild-Actor statt dessen bestehenden Visual-Actor; nur Prüfschnittstelle korrigiert. Kein solcher fehlgeschlagener Lauf zählt als bestanden.

Bekannte, schon in V5 nachgewiesene Warnung im Kampf-Hintergrund: `MI_WLA_LeafOak missing usage flag InstancedStaticMeshes`, Default-Material-Fallback. Geschütztes gemeinsames Asset nicht verändert; gesondert offen, keine neue V6-Korrektur behauptet. Zusätzlich Engine-Start-/EditorDataStorage-Warnungen, gelegentlicher CMC-Start-Hitch und Warnung zum vielfach abgefragten TAAU-CVar. Engine-eigene Python-Toolset-Startprüfungen melden vor der PokeMonster-Queue `Condition failed`; getrennt von den Report-Ergebnissen ausweisen. Externe iOS-/idevice-Meldungen und kritische Laufzeitfehler separat im finalen Logauszug zählen.

## 8. Echte Bild-/Video-Nachweise

Basis aller folgenden relativen Nachweispfade: `Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6/`. Große Medien und Messdaten bleiben lokal unter Saved, nicht in Git.

- `PIEBefore02/Before_Heilhaus_{0,45,90,135,180,225,270,315}.png`: echte QHD-Vorherbilder. `PIERoomPreview01/After_Heilhaus_<Winkel>.png`: identische Raumstation/Orbitwerte; fortlaufende Uhr, keine exakt eingefrorene Vergleichs-Tageszeit.
- `NativeBefore01/Heilhaus.png` ↔ `NativeAfter01/Heilhaus.png`: zusätzlich tatsächlicher identischer 12:00-/QHD-/C75-Kameravergleich; erfasste Positionsabweichung nur Float-Rundung, <0,1 cm. Weitere gematchte Dorf/Wald-/Umgebungsaufnahmen in denselben Ordnern.
- `ComparisonsFinal/Heilhaus_*.png` und `Heilhaus_NativeNoon.png`: eindeutig beschriftete Layouts dieser echten Fotos, keine generierten Szenen.
- `PIEImports03/Import_<Name>.png`: 47 unverändert gültige statische Kandidatenansichten; für Entoron/Zubat ausschließlich die korrigierten `NativeColorFinal01/Import_<Name>.png` bzw. finalen PIE-Nachtestbilder verwenden. `ComparisonsFinal/ImportOverview_1..3.png` bindet diese korrigierten Quellen ein.
- `NativeTeleport04/After_TestGround_Pikachu.png`, `After_TestGround_Karpador.png` sowie `NativeWild02/Wild_Pikachu.png`, `Wild_Karpador.png`: tatsächliche Spielperspektive/Bewegungszustände.

| Video unter Videos/ | Decodierte echte QHD-Frames | Tatsächliche Intervall-FPS |
|---|---:|---:|
| `Motion_Pikachu.mp4` | 52 | 6.99 |
| `Motion_Karpador.mp4` | 58 | 6.50 |
| `WildMotion_Pikachu.mp4` | 81 | 7.59 |
| `WildMotion_Karpador.mp4` | 93 | 7.87 |

Vorhandener nativer AVFoundation-Encoder, H.264, ursprüngliche Spielzeitstempel. Alle Samples decodiert und Zeitstempel/Framezahl gegen Frames.csv geprüft; keine interpolierten oder vervielfachten Frames. Die begrenzte Screenshot-Aufnahmeleistung (rund 6,5–7,9 FPS) reicht für sichtbare Bewegungsänderung, nicht für eine abschließende hochfrequente temporale/Footsliding-Freigabe. Aufnahme-FPS sind keine Gameplay-FPS. Harrys eigener Spieltest bleibt maßgeblich.

## 9. Schutz und abschließende QA

Vergleich der vollständigen SceneBefore-/PreAuthor-Signatur identisch. Danach nur 138 alte Raumactors angepasst, sieben HISM-Actors ergänzt, keiner entfernt. Alle vorhandenen Außenactors, V5-Begegnungsbüsche/-Zonen sowie Welt-/PP-Einstellungen unverändert. Schutz-Hashes: 6560 vorhandene Arbeitsdateien geprüft, ausschließlich ausdrücklich erlaubte eigene Änderungen; 1757 lokale Original-/Fab-Dateien und 751 vorhandene Save-Dateien unverändert. Die drei schon vor V6 vorhandenen Finder-.DS_Store-Abweichungen gegenüber V5 wurden separat als Ausgangszustand dokumentiert, nicht als V6-Änderung.

`Config/DefaultEngine.ini` bleibt die ursprüngliche lokale Nutzeränderung mit SHA256 `f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523` und wird nicht gestaged. Die beiden Vollbackup-Refs bleiben bei `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Keine neue Map, Worktree, Projektkopie, Originalquelle, globalen Grafikprofile oder Nutzerspielstände verändert; keine Programme gewaltsam beendet.

Original-Incoming-Dateien bleiben lokal/unverändert; keine automatischen Stagings geschützter unversionierter Quellen. Neue eigene abgeleitete Modellimporte und Raum-Assets sowie eng begrenzte C++-/Test-/Werkzeug-/Dokumentationsänderungen werden nach Abschlussprüfung zusammen gesichert. Fab-Originale bleiben lokal. Git-/LFS-Endkontrolle und Abschluss-SHA werden zusätzlich im Chat angegeben.

Nach Abschluss keine weitere Gestaltung oder Übernahme nach Westland. Harry beurteilt Heilhaus, Tempo und neue Modellkandidaten zuerst selbst.

### Finale tatsächlich ausgeführte Prüfung

- `FullAutomationRelease02`: 333 bestanden, 0 mit Testwarnungen, 0 fehlgeschlagen, 0 ausgelassen/in Bearbeitung; Engine-Exit 0, **strenger QA-Wrapper Exit 0**. Nach der letzten Texturkorrektur erneut ausgeführt.
- `EditorColorFinal06`: alle zwölf bestehenden Maps jeweils 0 Fehler und 0 Warnungen. Ausschließlich geöffnet/geprüft, keine geschützte Map gespeichert.
- `PIEColorFinal02`: beide korrigierten Kandidaten mit NoCollision/Bodenkontakt, echten Farben und Rückkehr bestanden.
- `FinalQA.json`: finale Automation, letzter Editor und sieben bestandene native Prüfprozesse auf kritische Laufzeitfehlermarker kontrolliert: keine Fatal-/Ensure-/Script-Fehler und keine unerwarteten Python-Tracebacks. Externe `idevice_id: Bad CPU type`/entsprechende iOS-Meldungen: kein Treffer.
- Gesonderte Engine-Infrastrukturmeldungen: je nativem `-game`-Start sieben Tracebacks aus den experimentellen Engine-Toolsets (fehlende editorseitige `ToolsetDefinition`, `AgentSkill`, `PythonTestRunner`); im Editor/NullRHI stattdessen 17 vor der Projekt-Testqueue ausgegebene `Condition failed`. Dateien/Frame-0-Startkontext nachgewiesen. Diese Logs sind nicht vollständig fehlerfrei; die Meldungen werden nicht als Gameplay-/PokeMonster-Testfehler oder als iOS-Warnung umetikettiert. Keine Engine-/Pluginänderung.
- Vorherige erfolglose Versuche bleiben erhalten und werden nicht in die Pass-Zahlen eingerechnet. Keine vollständige hochfrequente temporale Bildfreigabe behauptet.
