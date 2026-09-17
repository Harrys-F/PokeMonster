# Entscheidungsprotokoll – PokeMonster

Dieses Dokument hält dauerhafte Entscheidungen, offene Punkte und ersetzte Planungen fest.

## Statusbegriffe

- **Beschlossen:** gilt für die weitere Entwicklung
- **Vorläufig:** aktuelle Arbeitsrichtung, kann geändert werden
- **Offen:** noch keine Entscheidung
- **Ersetzt:** frühere Planung, die nicht mehr gilt

## 2026-09-09 – Grundlegende Spielwelt

**Status: Beschlossen**

- Das Spiel verbindet Kreaturensammeln und Kämpfe mit einer eigenständigen Fantasywelt.
- Die Atmosphäre darf von Mittelerde inspiriert sein.
- Orte, Namen, Karten und Geschichte werden eigenständig gestaltet.
- Gewünschte regionale Stimmungen umfassen Hügelland, uralten Wald, Hochland, Gebirge, monumentale Städte, dunkles Grenzland und Vulkanlandschaft.

## 2026-09-09 – Freund-/Gegenfigur

**Status: Beschlossen**

- Die klassische einfache Rivalenfigur wird durch eine komplexere Freund-/Gegenfigur ersetzt.
- Sie entwickelt sich parallel zum Spieler, reist teilweise mit und führt eigene Untersuchungen durch.
- Sie fordert zunehmend mehr Kontrolle über Kreaturen.
- Ein Wendepunkt entsteht, als sie in einer gefährlichen Situation von einer Kreatur gerettet wird.

## 2026-09-09 – Entwicklungen

**Status: Beschlossen**

- Normale Levelentwicklungen bleiben grundsätzlich erhalten.
- Tauschentwicklungen werden nicht zu einfachen Levelentwicklungen.
- Sie benötigen Mindestlevel, passenden Ort und besondere Handlung oder Prüfung.
- Kadabra, Maschock, Georok und Alpollo dienen als erste Beispiele.
- Konkrete Level und Auslöser bleiben vorläufig.

## 2026-09-10 – Kreaturenumfang

**Status: Beschlossen für den privaten Prototyp**

- Verwendet werden sollen Kreaturen der Generationen 1 und 2.
- Der theoretische Gesamtumfang beträgt maximal 251.
- Die erste Demo verwendet nur eine kleine Auswahl.
- ROM-Dateien und daraus extrahierte Assets werden nicht verwendet.

## 2026-09-10 – Umstieg von 3D auf 2D

**Status: Ersetzt beziehungsweise neu beschlossen**

Frühere Planung:

- 3D-Spiel beziehungsweise größere Open-World-Ausrichtung

Neue gültige Planung:

- modernes 2D-Top-Down-Spiel
- Paper2D in Unreal Engine
- hochauflösende, saubere Grafiken
- klassische Lesbarkeit mit moderner Darstellung
- zuerst eine kleine Demo statt einer großen offenen Welt

## 2026-09-16 – Technische Grundlage

**Status: Beschlossen**

- Unreal Engine 5.8.2
- macOS als einzige Zielplattform
- MacBook Air M4 mit 16 GB gemeinsamem Arbeitsspeicher als Entwicklungs- und Testgerät
- Kombination aus C++ und Blueprints
- Paper2D und Enhanced Input
- Rider und Xcode für die Entwicklung
- Git und Git LFS für Versionsverwaltung und Sicherung
- Codex soll einen großen Teil der technischen Arbeit übernehmen
- Harry plant, entscheidet und testet

## 2026-09-16 – Leistungsprofile

**Status: Vorläufig beschlossen**

Es werden drei Grafikprofile vorbereitet:

- Medium
- Hoch
- Ultra

Medium ist das primäre effiziente Profil für das MacBook Air. Genaue Auflösung, Bildrate und Scalability-Werte werden erst nach Leistungstests festgelegt.

## 2026-09-17 – Player-Basis für den Bewegungstest

**Status: Beschlossen**

- Die technische Player-Basis wird als C++-Klasse auf Grundlage von `APaperCharacter` umgesetzt.
- Die Bewegung verwendet Enhanced Input und unterstützt freie, kamerarelative Bewegung in acht Richtungen.
- Eine perspektivische Kamera blickt leicht schräg von oben auf die Figur und folgt über Camera Lag weich.
- Der vorhandene Paper2D-Flipbook-Component bleibt die Grundlage für spätere Laufanimationen und visuelle Blueprint-Anpassungen.
- Für den ersten Test wird ausschließlich Engine-Geometrie als Platzhalter verwendet; es werden noch keine finalen Grafik-Assets angelegt.
- Ein C++-GameMode setzt den Player als Standard-Pawn. `Dev_TestMap` ist die Start- und Test-Map.

## 2026-09-17 – Richtungs- und Animationszustände des Players

**Status: Beschlossen**

- Die vorhandene `UPaperFlipbookComponent` von `APaperCharacter` dient als zentrale Paper2D-Darstellung des Players.
- Der Player besitzt die Blickrichtungen Up, Down, Left und Right sowie die Zustände Idle und Walking.
- Bei diagonaler Bewegung bestimmt die stärkere Eingabeachse die Blickrichtung; bei gleich starker Eingabe bleibt die zuletzt verwendete Achse erhalten.
- Idle behält die letzte relevante Blickrichtung bei.
- Idle- und Walking-Flipbooks werden je Richtung in C++ strukturiert und können später in Blueprint-Defaults zugewiesen werden.
- Solange keine Flipbooks zugewiesen sind, bleibt ein einfacher Engine-Platzhalter mit Richtungsmarkierung sichtbar.

## 2026-09-17 – Wiederverwendbares Interaktions-Grundsystem

**Status: Beschlossen**

- Interagierbare Weltobjekte implementieren die C++-Schnittstelle `PokeMonsterInteractable`; ihre Prüf- und Reaktionslogik kann später auch in Blueprints umgesetzt werden.
- Der Player verwendet eine eigene Enhanced-Input-Aktion für `E` und `Enter`.
- Das Ziel wird mit einem kurzen Sphere-Trace vor der zuletzt gewählten Blickrichtung ermittelt. Dadurch bleiben diagonale Bewegung und die Darstellung mit vier Richtungen konsistent.
- Der Trace berücksichtigt Sichtblocker, sodass keine Interaktion durch Hindernisse hindurch erfolgt.
- Dialoge, UI und komplexe NPC-Logik bleiben getrennte spätere Systeme und bauen auf der Schnittstelle auf.
- Ein einfacher C++-Test-Actor bestätigt Interaktionen per Zustandswechsel, sichtbarer Größen-/Lichtänderung und Logeintrag.

## 2026-09-17 – Datengetriebene Kreaturen-Grundlage

**Status: Beschlossen**

- Gemeinsame Speziesdaten werden als `UPrimaryDataAsset` unter dem Primary-Asset-Typ `CreatureSpecies` verwaltet.
- Individuelle Kreaturen verwenden eine getrennte Runtime-Struktur mit eigener Instanz-ID, Level, aktuellen HP und Erfahrung. Sie referenzieren ihre Spezies, duplizieren deren Basisdaten aber nicht.
- Die 17 Typen der Generationen 1 und 2 sind als C++-Enum vorbereitet; `None` kennzeichnet einen fehlenden Sekundärtyp.
- Basiswerte, Geschlechtssystem, Startlevel, Wachstumsgruppe, vorbereitete Entwicklungsbedingungen und weiche Paper2D-Flipbook-Referenzen gehören zu den Speziesdaten.
- Entwicklungs- und Wachstumsfelder legen noch keine Formeln oder endgültigen Spielregeln fest.
- Für den Systemtest werden ausschließlich die Platzhalter-Spezies `TestGrass`, `TestFire` und `TestWater` verwendet.

## 2026-09-17 – Visueller Vertical Slice in Dev_TestMap

**Status: Ersetzt durch die illustrierte Paper2D-Arbeitsrichtung unten (Layout und Kollision bleiben Grundlage)**

- Das bestehende Testareal wird mit gedämpften Naturfarben, dichterem Waldrand, einer einfachen Fachwerkhütte und einem Bach mit Holzbrücke ausgestaltet.
- Die Szene nutzt Engine-Grundformen, ein selbst erstelltes Dreiecksprisma für den Dachgiebel und zehn eigene Materialinstanzen unter `/Game/Environment/Prototype/Materials`. Es werden keine externen Assets benötigt. Die Giebel-Quelldatei liegt unter `/Game/Environment/Prototype/Source`.
- Begehbare Flächen, blockierende Stämme/Felsen/Gebäude und rein dekorative Baumkronen/Büsche sind getrennt. Wasser erhält einfache unsichtbare Kollisionskörper mit freier Brückenpassage.
- Player, Gameplay-Systeme und Kamera bleiben unverändert. Diese Szene ist ein visueller Prototyp; finale Grafiken und der endgültige Stil bleiben offen.

## 2026-09-17 – Illustrierter Paper2D-Vertical-Slice

**Status: Vorläufige visuelle Arbeitsrichtung**

- Sichtbare Baum-, Busch-, Fels- und Hüttenformen werden durch eigene generierte, illustrierte Paper2D-Sprites unter `/Game/Environment/Prototype2D` ersetzt. Keine Marketplace-Assets oder externen Downloads. Finale Gestaltung bleibt offen.
- Statische Sprite-Flächen sind auf die vorhandene feste Kamera ausgerichtet; keine Tick- oder Billboard-Gameplay-Logik. Maskierte unbeleuchtete Sprites behalten ihre gemalten Schattierungen.
- Outliner-Ordner trennen Boden, Wege, Wasser, Vegetation, Gebäude, Vordergrund und Kollision. Bodenflächen verwenden eigene kostengünstige Materialien mit weichen Rändern; Kontaktflächen ersetzen harte Umgebungsschatten.
- Vorherige 3D-Actors bleiben unsichtbar erhalten, inklusive bestehender Kollisionskörper. Neue Grafikflächen kollidieren nicht. Player, Enhanced Input, GameMode, Interaktion und Kreaturendaten bleiben unverändert.
- Kameraabstand 1400 cm, Winkel und Camera Lag bleiben unverändert. Vier Texturen werden mit maximal 1024 Pixeln importiert und zwischen allen Instanzen geteilt.

## 2026-09-17 – Grafikstil, Kamera und Figurengröße

**Status: Beschlossen**

- Hauptreferenz ist die erste bereitgestellte Hügelland-Szene.
- Verwendet wird ein moderner, handgezeichneter, hochauflösender 2D-Stil.
- Die Kamera verwendet eine leicht schräge 3/4-Top-Down-Ansicht.
- Perspektive, sichtbarer Ausschnitt und relative Figurengröße orientieren sich am ersten Referenzbild.
- Die weiteren Referenzen bestimmen die Stimmung für uralten Wald, monumentale helle Stadt und dunkles Endgebiet.
- Vor der umfangreichen Asset-Produktion wird eine kleine Stil-Testszene erstellt.
- Die genaue technische Kameraeinstellung und Pixelgröße werden durch diese Testszene bestimmt.

## 2026-09-17 – Verfeinerung des bestehenden Vertical Slice

**Status: Umsetzung innerhalb der beschlossenen Stilrichtung**

- Die vorhandenen Illustrationen bleiben erhalten. Größenvariation, gespiegelte Silhouetten, geringe Ausrichtungsvariation und zusätzliche kleine Pflanzen lockern die Vegetation auf; die Bodenkontakte kollidierender Bäume bleiben bestehen.
- Eigene Materialien unter `/Game/Environment/Prototype2D/Materials` ergänzen Bodenflecken, zusammenhängende organische Wege, natürliche Ufer mit Tiefenfarben und dezenter Wasserbewegung sowie verwittertes Brückenholz. Neue dekorative Flächen besitzen keine Kollision.
- Die Weg- und Wassermaterialien enthalten die Koordinaten dieses Testareals. Für andere Maps benötigen sie eigene Verlaufsvorgaben; sie stellen noch kein allgemeines Landschaftssystem dar.
- Kamera, C++, Input und Spielsysteme bleiben unverändert. Bestehende Kollisionskörper und Brückengeometrie werden beibehalten.

## Aktuell offene Entscheidungen

- endgültiger Spielname
- Namen der Welt, Regionen und Städte
- genaue Hauptgeschichte
- Hauptfigur und Motivation
- Arenen oder eigenes Prüfungssystem
- endgültige Fangmechanik
- endgültiges Kampfsystem
- sichtbare oder zufällige Begegnungen
- linearer Weg oder alternative Routen
- genaue Demo-Kreaturen
- endgültige Attackenverwaltung
- genaue Schnellreise- und Weltfähigkeiten
- endgültige Zielauflösung und exakte Pixelgrößen
- Musik- und Soundkonzept
