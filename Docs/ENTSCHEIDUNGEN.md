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
- Ursprünglich legten Entwicklungs- und Wachstumsfelder noch keine Formeln fest. Dieser Teil ist durch „Level-, Erfahrungs- und Entwicklungsgrundlage“ unten ersetzt; endgültiges Balancing bleibt offen.
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

## 2026-09-17 – Verbindliche erweiterte visuelle Stilrichtung

**Status: Beschlossen**

- Alle bereitgestellten visuellen Referenzen bilden gemeinsam die verbindliche Stilgrundlage. Die erste Hügelland-Szene bleibt maßgeblich für Perspektive, sichtbaren Ausschnitt und relative Figurengröße.
- Verwendet wird hochwertiges, hochauflösend gezeichnetes 2D ohne Pixel-Art, mit leicht schräger Top-Down- beziehungsweise isometrisch wirkender Perspektive und moderner 2D/2.5D-Tiefenwirkung.
- Figuren bleiben relativ klein gegenüber einer sehr dichten, detailreichen und vollständig inszenierten Umgebung.
- Natürliche Vegetation, Layering, Vordergrundelemente, weiche malerische Beleuchtung und atmosphärische Farbgestaltung gehören verbindlich zum Stil.
- Mittelalterlich und fantastisch geprägte Architektur erhält einen deutlichen Tolkien-/Mittelerde-Einfluss. Konkrete geschützte Orte, Bauwerke, Symbole und Designs werden nicht kopiert.
- Brücken, Treppen, Terrassen, Höhenunterschiede, Klippen, Wasserläufe und Wasserfälle sind wiederkehrende Elemente der Weltgestaltung.
- Ländliche Dörfer und Höfe, größere mittelalterliche Städte, helle akademische oder magische Innenräume, alte Ruinen bei Nacht, Bergwerke und Höhlensysteme, wohnliche Innenräume sowie wasserreiche terrassierte Siedlungen sind gewünschte Szenentypen.
- Innenräume werden ebenso dicht und vollständig gestaltet wie Außenbereiche. Ruinen, Höhlen und unterirdische Orte verwenden dieselbe visuelle Sprache.
- Kreaturen sind sichtbar und natürlich in ihre Lebensräume integriert. Wege, Eingänge, Figuren, Kreaturen und interaktive Objekte bleiben trotz hoher Detaildichte klar lesbar.
- Die technische Kameraart und exakten Pixelgrößen bleiben Gegenstand der Stil-Testszene; die geforderte visuelle Wirkung ist unabhängig davon verbindlich.

## 2026-09-17 – Level-, Erfahrungs- und Entwicklungsgrundlage

**Status: Technische Grundlage umgesetzt; endgültiges Balancing offen**

- Spezies-/Instanztrennung bleibt bestehen. Gemeinsame Basiswerte und Entwicklungswege gehören zur Spezies; Level, kumulative Erfahrung, aktuelle HP und berechnete Statuswerte zur Instanz.
- Die zentrale C++-Berechnung verwendet vorerst Level 1–100 und alle sechs vorbereiteten Wachstumsgruppen. Die Rest-Erfahrung zum nächsten Level wird abgeleitet. XP-Vergabe unterstützt mehrere Level-Ups, begrenzt am Höchstlevel und weist negative oder inkonsistente Eingaben ohne Änderung ab.
- Die vorläufige Statusberechnung verwendet Basiswerte und Level ohne IVs, EVs, Wesen oder Kampfmodifikatoren. Neue Instanzen starten mit vollen berechneten HP; Level-Ups erhalten fehlende HP und beleben Kreaturen mit null HP nicht wieder. Dies ersetzt den bisherigen Basis-HP-Platzhalter.
- Entwicklungswege unterstützen die Auslöser Level, Item, Freundschaft, Ort und besondere Handlung. Zusätzliche Anforderungen werden innerhalb eines Wegs mit UND verknüpft; mehrere Wege sind Alternativen. Mindestlevel plus passender Ort plus besondere Handlung unterstützt ausdrücklich die geplanten ehemaligen Tauschentwicklungen.
- Die Prüfung liefert ausschließlich Eignung beziehungsweise mögliche Ziel-IDs. Sie ändert keine Spezies, verbraucht keine Items und enthält keine visuelle Entwicklung, UI oder neue Gameplay-Anbindung. `Custom` bleibt reserviert und ergibt bis zu einer späteren Implementierung keine Eignung.
- Bestehende Spezies-Assets und ihre bisherigen Entwicklungsfelder bleiben erhalten. Player, Kamera, Interaktion, Maps und Grafik werden durch diese Erweiterung nicht verändert.
- Formeln, HP-Verhalten und konkrete Entwicklungswerte bleiben austauschbare technische Arbeitsregeln. Einzelne Kreaturen, Orte, Prüfungen und endgültige Levelschwellen werden damit nicht festgelegt. API-Details stehen in `Docs/TECHNIK.md`.

## 2026-09-17 – Datengetriebene Attacken- und Kampfgrundlage

**Status: Technische Grundlage; endgültige Kampfregeln und Balancing bleiben offen**

- Attacken verwenden eigene `CreatureMove`-Primary-Data-Assets. Kreatureninstanzen erhalten vier eigene Moveslots mit weicher Attackenreferenz und separaten PP. Speziesdaten und Progression bleiben erhalten.
- Physical/Special/Status wird je Attacke konfiguriert. Effekte, Priorität und Beschreibungen wurden zunächst nur vorbereitet. Die Aussage zur fehlenden Rundensteuerung ist durch „Einfacher 1-gegen-1-Battle-Flow“ unten ersetzt; Statusveränderungen bleiben unimplementiert.
- Trefferprüfung und Schadensberechnung sind getrennte C++-Funktionen ohne Veränderung der beteiligten Kreaturen. Der Aufrufer liefert einen Wurf von 0–99; PP-Verbrauch erfolgt ausdrücklich über eine separate Funktion.
- Eine vorläufige Schadensformel verwendet Level, Basisstärke, passende aktuelle Statuswerte und Typmultiplikatoren. Die 17 Typen verwenden als technische Arbeitsgrundlage die zentral gepflegten Matchups der zweiten Generation. Dies konkretisiert das bisher offene Typensystem für den Prototyp; endgültige Anpassungen bleiben möglich.
- Es gibt noch keine Status-Effektausführung, STAB-Boni, kritischen Treffer, Kampfmodifikatoren, Lernlogik oder Kampfanimationen. Die Aussagen zur fehlenden HP-Anwendung und Battle-UI sind durch die Battle-Session beziehungsweise „Erste funktionale Battle-Testoberfläche“ unten ersetzt. Die bestehenden Welt- und Playersysteme bleiben unverändert.
- Drei neue Platzhalter-Attacken unter `/Game/Data/Moves` dienen den automatisierten Tests. Die Details und Formeln sind in `Docs/TECHNIK.md` beschrieben.

## 2026-09-17 – Einfacher 1-gegen-1-Battle-Flow

**Status: Technischer Battle Flow umgesetzt; weiterführende Kampfregeln bleiben offen**

- Eine getrennte C++-Battle-Session verwaltet eigene Kampfkopien von genau einer aktiven Kreatur pro Seite. Der Zustand ist von der Ausführung getrennt und für spätere UI/Animationen lesbar. Eine automatische Rückübertragung auf Welt-/Inventardaten findet noch nicht statt.
- Jede Runde erhält beide Attackenauswahlen gemeinsam. Höhere Priorität beginnt, danach entscheidet Initiative; bei vollständigem Gleichstand beginnt deterministisch Seite A. Treffer verwenden einen eigenen, per Seed reproduzierbaren Zufallsstrom.
- Beide Auswahlen werden vor Beginn geprüft. Fehlerhafte Runden verändern weder HP, PP, Rundenzähler noch Zufallszustand. Ausgeführte Angriffsversuche kosten eine PP, auch bei Fehlschlag, Immunität oder Status-Platzhalter.
- HP-Anwendung verwendet die vorhandene Schadensberechnung unverändert. Ein K.O. beendet die Runde und den Kampf sofort; die besiegte Kreatur führt keinen ausstehenden Angriff mehr aus. Weitere Aufrufe melden den beendeten Kampf, ohne zusätzliche PP oder HP zu verändern.
- Geordnete Events berichten Auswahl, Ausführung, Fehlschlag, Schaden, Effektivität/Resistenz/Immunität, K.O. und Kampfende. Status-Platzhalter führen weiterhin keine Statuslogik aus.
- Ohne beidseitig gültige Auswahl erfolgt kein Rundenfortschritt. Eine Ersatzattacke bei null PP oder ein erzwungenes Ende von Status-/Immunitätsschleifen wird nicht hinzugefügt.
- Player, Kamera, Interaktion, Maps, Grafik, Progression und bisherige Attacken-/Kampfbausteine bleiben unverändert. Neue Gameplay-Systeme wie Teams, Wechsel, Items, Trainer oder Fangmechanik werden nicht ergänzt. API und Eventdetails stehen in `Docs/TECHNIK.md`.

## 2026-09-17 – Erste funktionale Battle-Testoberfläche

**Status: Technische Testoberfläche umgesetzt; die einfachen UMG-Formen wurden durch die visuelle Überarbeitung vom 2026-09-25 ersetzt. Finale Kreaturen- und UI-Gestaltung bleibt offen.**

- Die neue `Dev_BattleTestMap` verwendet ausschließlich ihren eigenen Battle-Test-GameMode und Controller. Die normale Testmap, Player-Kamera und bisherigen Spielsysteme bleiben unverändert.
- Eine getrennte C++-Presenter-Schicht verbindet die vorhandene BattleSession mit UMG. BattleSession, Schadensberechnung, Kreaturen-, Progressions- und Attackendaten werden nicht verändert. Der Gegner wählt zunächst den ersten gültigen Slot mit PP.
- Das native UMG-Widget zeigt Namen, Level, numerische HP und Balken, vier Attackenbuttons mit Typ/PP sowie ein begrenztes Kampflog. Die ursprünglich rein aus UMG-Formen bestehenden Kreaturen-Platzhalter ohne zusätzliche Texturen wurden am 2026-09-25 durch eigene Testgrafiken ersetzt. Die verbindliche Welt-Stilrichtung bleibt bestehen.
- Verwendet werden TestWater und TestGrass auf Level 20 sowie die drei vorhandenen Testattacken. Der vierte Spielerslot wiederholt die Normal-Attacke mit eigenen PP; es wird keine Lernregel festgelegt.
- Die Eingabe wird sofort bei Auswahl gesperrt. Die ursprüngliche Freigabe direkt nach der Rundenauflösung wurde am 2026-09-25 durch eine Freigabe nach abgeschlossener Kampfinszenierung ersetzt. Nach K.O./Kampfende bleiben Attacken deaktiviert. Ein Testneustart erzeugt eine neue Session. Ohne gültige Attacken meldet die UI den Zustand, ohne eine Ersatzattacke oder neue Kampfregel einzuführen.
- Lesemodelle und vollständige BattleEvents bleiben von der Darstellung getrennt. Widget-Blueprint-Unterklassen, visuelle Ereignisse und ein expliziter Präsentationsabschluss ermöglichen spätere Animationen, Sprites, Sound und Menüs ohne Neuschreiben der BattleSession. Details stehen in `Docs/TECHNIK.md`.

## 2026-09-25 – Visuelle Richtung der Battle-Testoberfläche

**Status: Präsentationsprototyp umgesetzt; finale Battle-Grafiken und UI-Gestaltung offen**

- Die Battle-Testmap zeigt eine selbst erstellte, handgemalte Naturkulisse mit Weg, Bach und Steinbrücke. Sie verwendet eine leicht erhöhte Blickrichtung, malerische Beleuchtung und mehrere Tiefenebenen als Echo der beschlossenen Weltoptik. Die Battle-Kulisse legt weder Weltkamera noch Begegnungsübergang endgültig fest.
- Zwei eigens erzeugte Kreaturen-Platzhalter stehen auf der Kulisse: die eigene Kreatur groß und nah unten links, die gegnerische kleiner und weiter oben rechts. Die Platzhalter sind keine endgültigen Kreaturendesigns.
- Namens- und HP-Bereiche werden als ruhige, organisch gerundete Tafeln gestaltet. Attacken zeigen Name, dezent typgefärbte Kennzeichnung und PP getrennt; das kompakte Log sitzt im unteren Bedienfeld. Sättigung, Kontrast und Dekoration ordnen sich der Lesbarkeit unter.
- Grafiken werden als kleine wiederverwendbare UI-Texturen importiert und in der bestehenden UMG-Widgetklasse angezeigt. Die technische Verbindung zur BattleSession, der Presenter, Testdaten und Kampfregeln bleiben bestehen. Es werden keine fremden Assets oder neuen Plugins eingebunden.

## 2026-09-25 – Erste Kampfinszenierung aus BattleEvents

**Status: Technischer Präsentationsablauf für die Battle-Testmap; finale Animationen und Effekte offen**

- Die vorhandene BattleSession entscheidet weiterhin sofort und vollständig über Zugreihenfolge, Treffer, Schaden, PP und K.O. Eine reine Präsentationsschicht liest anschließend die geordneten Events und zeigt die tatsächlich ausgeführten Aktionen nacheinander. Ausgewählte, aber wegen K.O. nicht ausgeführte Attacken erhalten keine Animation.
- Ein kurzer Impuls markiert den Angreifer. Physical nutzt eine kurze Stoßspur, Special ein einfaches Energiegeschoss, Status einen dezenten Schimmer. Treffer, Fehlschlag und Immunität erhalten unterschiedliche visuelle Rückmeldungen; nur tatsächlicher Schaden führt zu einer weichen HP-Anzeigeänderung. K.O. blendet die betroffene Kreatur ab und senkt sie leicht ab.
- Die Spielereingabe bleibt bis zum Ende der sichtbaren Ereignisfolge gesperrt. Das Kampflog wird mit den einzelnen Aktionen fortgeschrieben. Die visuellen Zeiten sind Testwerte und legen das spätere Kampftempo nicht endgültig fest.
- Die bestehende Naturkulisse und Kreaturen-Platzhalter bleiben erhalten. Die neuen UMG-Effekte benötigen keine zusätzlichen externen Assets. Ereignis- und Schritt-Hooks sind für spätere Blueprint-Animationen, VFX und Sound vorbereitet; Kampfregeln bleiben unverändert.

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
