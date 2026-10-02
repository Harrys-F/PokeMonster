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
- Damals blieb der Kameraabstand bei 1400 cm; dieser Abstand ist durch die kontrollierte Anpassung vom 2026-10-02 unten ersetzt. Winkel und Camera Lag bleiben unverändert. Vier Texturen werden mit maximal 1024 Pixeln importiert und zwischen allen Instanzen geteilt.

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

- Eine getrennte C++-Battle-Session verwaltet eigene Kampfkopien von genau einer aktiven Kreatur pro Seite. Der Zustand ist von der Ausführung getrennt und für spätere UI/Animationen lesbar. **Der damalige Stand ohne Rückübertragung wurde durch die Overworld-Begegnungskoordination vom 2026-09-25 unten ersetzt.**
- Jede Runde erhält beide Attackenauswahlen gemeinsam. Höhere Priorität beginnt, danach entscheidet Initiative; bei vollständigem Gleichstand beginnt deterministisch Seite A. Treffer verwenden einen eigenen, per Seed reproduzierbaren Zufallsstrom.
- Beide Auswahlen werden vor Beginn geprüft. Fehlerhafte Runden verändern weder HP, PP, Rundenzähler noch Zufallszustand. Ausgeführte Angriffsversuche kosten eine PP, auch bei Fehlschlag, Immunität oder Status-Platzhalter.
- HP-Anwendung verwendet die vorhandene Schadensberechnung unverändert. Für die damalige reine 1-gegen-1-Session beendete ein K.O. Runde und Kampf sofort; **die allgemeine Kampfende-Regel wurde am 2026-09-25 durch die Teamregel unten ersetzt**. Die besiegte Kreatur führt keinen ausstehenden Angriff mehr aus.
- Geordnete Events berichten Auswahl, Ausführung, Fehlschlag, Schaden, Effektivität/Resistenz/Immunität, K.O. und Kampfende. Status-Platzhalter führen weiterhin keine Statuslogik aus.
- Ohne beidseitig gültige Auswahl erfolgt kein Rundenfortschritt. Eine Ersatzattacke bei null PP oder ein erzwungenes Ende von Status-/Immunitätsschleifen wird nicht hinzugefügt.
- Player, Kamera, Interaktion, Maps, Grafik, Progression und bisherige Attacken-/Kampfbausteine blieben bei diesem damaligen Schritt unverändert. Teams und Wechsel waren **zu diesem Zeitpunkt noch nicht enthalten; dieser Stand wurde durch die Teamentscheidung vom 2026-09-25 unten ersetzt**. Items, Trainer und Fangmechanik bleiben weiterhin offen. API und Eventdetails stehen in `Docs/TECHNIK.md`.

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

## 2026-09-25 – Erste Team- und Wechselmechanik

**Status: Technische Grundlage und funktionale Battle-Test-UI; endgültige Team- und Trainerregeln offen**

- Die BattleSession hält bis zu sechs individuelle Kreaturen je Seite und genau eine aktive. Der bisherige `Initialize`-/`ResolveRound`-Pfad bleibt als Ein-Kreaturen-Fall gültig. HP, PP und Level gehören weiter zum jeweiligen Exemplar und bleiben beim Wechsel erhalten.
- Ein freiwilliger Wechsel ist die Aktion der wechselnden Seite für diese Runde. Wechsel werden vor Attacken ausgeführt; eine gegnerische Attacke trifft deshalb die eingewechselte Kreatur. Bei K.O. ohne verbleibendes kampffähiges Teammitglied endet der Kampf. Andernfalls ist ein Ersatzwechsel nötig; dieser Pflichtwechsel kostet keinen zusätzlichen Zug. Die Testgegnerseite nimmt den nächsten kampffähigen Teamplatz automatisch.
- `SwitchChosen` und `SwitchedIn` ergänzen die geordneten BattleEvents. Die vorhandene Präsentationsschicht zeigt den Wechsel als eigene Aktion und hält die Eingabe bis zum Abschluss gesperrt. Die Battle-Testmap zeigt beide Teams und ermöglicht dem Spieler freiwillige und erzwungene Wechsel. Sie verwendet für Teammitglieder vorhandene Test-Spezies und Platzhaltergrafiken; finale Artworks und komplexe Team-Menüs sind offen. **Ersetzt:** Eine erste einfache Team-Ansicht in der Overworld ist seit der UI-Entscheidung unten vorhanden.
- Schadensformel, Attackendaten, Typentabelle, Status-Platzhalter sowie Player-, Weltkamera- und Map-Systeme werden nicht geändert. Items, Fangmechanik und Statuszustände bleiben ausgenommen.

## 2026-09-25 – Erster Overworld-Kampfübergang

**Status: Technischer Testablauf umgesetzt; endgültige Begegnungsinszenierung offen**

- Ein einzelnes interagierbares Testobjekt in `Dev_TestMap` startet die vorhandene BattleSession und UMG-Präsentation als Overlay, ohne die Weltmap zu wechseln. `Dev_BattleTestMap` bleibt als eigenständiger Test erhalten. Damit ist die bisher offene Frage nach dem endgültigen Welt-Kampf-Übergang noch nicht entschieden; andere Inszenierungen können später an denselben Start-/End-Datenvertrag anschließen.
- Ein Game-Instance-Subsystem sperrt während der Begegnung Weltbewegung und -interaktion, bewahrt den Weltzustand, hält das individuelle Spielerteam innerhalb der laufenden Spielsitzung und überträgt HP/PP nach Kampfende zurück. Es meldet Sieg oder Niederlage strukturiert an die Overworld; Abbrechen und Flucht sind vorerst nur reservierte Ergebniswerte ohne Spielmechanik.
- Dieser Schritt verwendet ausschließlich bestehende Test-Spezies, Testattacken und die vorhandene Battle-UI. Er ergänzt weder Zufallsbegegnungen noch Trainerlogik, Items, Fangmechanik oder dauerhafte Speicherung.

## 2026-09-25 – Datengetriebener Wildbegegnungs-Prototyp

**Status: Zwei kontrollierte Testquellen umgesetzt; endgültige Begegnungshäufigkeit und Weltlogik offen**

- Wildbegegnungen verwenden ein eigenes Primary-Data-Asset mit gewichtetem Speziespool, Levelspanne, Startattacken und optionalen Tageszeit-, Gebiets- und Bedingungsfiltern. Ein Seed erlaubt reproduzierbare Tests. Das Profil beschreibt gemeinsame Vorgaben; jeder Kampf erzeugt ein individuelles Exemplar.
- Sichtbare Kreatur und einmalig auslösende Testzone in `Dev_TestMap` übergeben ihre Gegner an das bestehende `PokeMonsterEncounterSubsystem`. Es unterscheidet Quellen strukturiert, während BattleSession, UI und Overworld-Rückkehr gemeinsam bleiben. Script-/Story- und spätere Zufallsquellen sind technisch vorgesehen, aber noch nicht als Gameplay umgesetzt.
- Der sichtbare Actor verwendet vorerst ein vorhandenes Paper2D-Platzhalter-Sprite und kann nach Sieg deaktiviert werden. Die Zone löst nur kontrolliert und mit festem Seed aus. Beide nutzen vorläufig das vorhandene Testteam, wenn noch kein Spielerteam existiert. Das ist keine Entscheidung über spätere Spawn-, Tageszeit-, Fang- oder Zufallsregeln.

## 2026-09-25 – Erster Fangprototyp für Wildkämpfe

**Status: Funktionaler Testablauf; der damals unbegrenzte Testgegenstand wurde durch die Inventarentscheidung vom 2026-09-26 ersetzt. Fangbalancing und Reserve bleiben offen.**

- Die bisherige Aussage „keine Fangmechanik“ in den Entscheidungen zu Battle Flow, Team und Overworld-Begegnung ist durch diesen Prototyp **ersetzt**. `Capture` ist eine eigene BattleSession-Zugwahl ausschließlich für Wildkämpfe. Ein gültiger Versuch kostet den Zug; bei Erfolg endet der Kampf sofort, bei Fehlschlag darf der Gegner angreifen.
- Spezies erhalten einen gemeinsamen Basis-Fangwert, das eigenständige `TestCaptureDevice` einen konfigurierbaren Bonus. Aktuelle/maximale HP und ein Seed bestimmen die technische Testchance. Diese Formel legt kein endgültiges Fangbalancing fest. **Ersetzt:** Die damals unbegrenzte Verfügbarkeit des Testgegenstands gilt seit der Inventarentscheidung unten nicht mehr.
- `Captured` ist ein eigenständiger Kampf- und Encounter-Ausgang. Das gefangene individuelle Exemplar geht mit Level, HP und PP in ein Team mit freiem Platz über. Bei sechs Mitgliedern meldet das Ergebnis `TeamFull` und trägt die Kreatur für eine spätere Reserveübergabe; ein dauerhaftes Storage-System gibt es noch nicht. Der sichtbare Wildactor wird nach Fang deaktiviert.
- Die bestehende Battle-UI erhält nur eine kleine `Fangen`-Aktion und Ereignispräsentation. Weltkamera, Map, Kampf-Schadensberechnung und andere Spielsysteme bleiben unverändert.

## 2026-09-26 – Erste Trainerkampf-Grundlage

**Status: Funktionaler Testtrainer; die Aussage zur fehlenden dauerhaften Speicherung ist durch die Save-Entscheidung unten ersetzt. Weitere Trainerregeln offen.**

- Die bisherige Aussage „keine Trainerlogik“ beim Overworld-Kampfübergang und Wildbegegnungs-Prototyp ist für diesen Testtrainer **ersetzt**. Trainerdaten liegen in einem eigenen Primary Data Asset mit stabiler ID, Name, Klasse, Team, Leveln, Startattacken und optionalen Vor-/Nachkampftexten. Ein Trainerkampf verwendet dieselbe BattleSession, Teamlogik und Overlay-Präsentation wie andere Begegnungen. Fangaktionen bleiben gesperrt.
- Ein platzierter Paper2D-Test-NPC in `Dev_TestMap` spricht den Spieler zunächst über einen einfachen Welt-Textplatzhalter an und startet danach den Kampf. Nach Spieler-Sieg zeigt er einen anderen Text und bietet keinen unmittelbaren Rückkampf. Nach Niederlage ist ein erneuter Versuch möglich. Dies legt kein späteres Dialogsystem, NPC-Verhalten oder endgültige Trainerinszenierung fest.
- Der besiegte Zustand wird anhand der Trainer-ID im Game-Instance-Subsystem gehalten. **Ersetzt:** Seit der Save-Entscheidung unten werden diese IDs auch dauerhaft im Dev-Slot gespeichert. Geld und Belohnungen werden weiterhin nicht eingeführt.

## 2026-09-26 – Erste Item- und Inventargrundlage

**Status: Technische Sitzungsgrundlage; die Savegame-Aussage ist durch die Entscheidung unten ersetzt. Ökonomie und umfassende Item-Nutzung bleiben offen.**

- Allgemeine Itemdaten liegen als eigene Primary Data Assets vor und sind von Inventarmengen getrennt. Die Kategorien Capture, Healing, Battle, Evolution, KeyItem und Misc sind vorbereitet. Die bestehenden Fangbonus-Daten bleiben erhalten; das neue Capture-Item referenziert das vorhandene `TestCaptureDevice`.
- Ein Game-Instance-Subsystem hält mehrere mengenbegrenzte Stapel je Item über Encounter hinweg. **Ersetzt:** Die Stapelliste wird seit der Save-Entscheidung unten im Dev-Slot gespeichert und validiert wiederhergestellt. Für den Entwicklungstest beginnt eine neue Spielsitzung einmalig mit fünf Fangitems; diese Vorgabe ist kein endgültiges Startinventar.
- Der vorhandene Fangbutton setzt nun Bestand voraus. Jeder durch die BattleSession angenommene Fangversuch verbraucht ein Item, bei Erfolg wie Fehlschlag. Trainerkämpfe behalten das Fangverbot. Die BattleSession und Fangchance bleiben unverändert; der Presenter übernimmt die Inventarprüfung an der UI-Grenze.
- Ein Test-Heilitem stellt außerhalb des Kampfs HP wieder her, jedoch nicht bei K.O. oder vollen HP. Ein Test-Entwicklungsitem liefert seine ID an die bestehende reine Entwicklungsprüfung; eine tatsächliche Entwicklung samt Verbrauch bleibt offen. Shops, Geld, Inventarmenü und weitere Kampfitems sind nicht beschlossen.

## 2026-09-26 – Erster versionierter Dev-Spielstand

**Status: Technischer Testslot; Umfang späterer Savegames bleibt offen**

- Die bisherigen Aussagen „noch kein Speichersystem“ bei Kreaturenfortschritt, Inventar und Trainerstatus sind für diesen ersten Test **ersetzt**. Ein zentrales Unreal-`USaveGame` mit Schema-Version 1 und ein Game-Instance-Save-Subsystem speichern in `PokeMonster_Dev` Teamzustand, XP, HP, Moveslots/PP, Inventarstapel, besiegte Trainer-IDs und abgeschlossene sichtbare bzw. zonenbasierte Testbegegnungen.
- Assetdefinitionen bleiben datengetrieben. Der Spielstand enthält nur stabile Primary Asset IDs; beim Laden werden die Assets aufgelöst und individuelle Werte validiert. Fehlende Assets und unbekannte/inkompatible Versionen führen zu einer klaren Ablehnung ohne teilweisen Austausch des Runtime-Zustands. Spätere Migrationen sind an der Schema-Prüfung vorgesehen, aber noch nicht entschieden.
- Ein einzelner Dev-Slot und Konsolenbefehle dienen der Prüfung. Mehrere Spielstände, Speicheroberfläche, Autosave, Cloud-Synchronisation und endgültige Regeln für Weltzustände sind nicht beschlossen. Save-Dateien liegen außerhalb der Git-Historie unter `Saved/SaveGames`.

## 2026-09-26 – Erste Overworld-UI

**Status: Funktionales HUD und Ansichtsmenü; finale Menügestaltung und Item-Bedienung offen**

- Die normale Test-Overworld erhält einen eigenen PlayerController für das HUD. Die Battle-Testmap bleibt unabhängig. Team und Inventar werden ausschließlich aus den vorhandenen Subsystemen gelesen; ihre Gameplay-Logik wird nicht in Widgets kopiert. Ein vorhandenes Entwicklungsteam macht das HUD in `Dev_TestMap` sofort prüfbar.
- Das kleine HUD zeigt Team-Name, Level, HP und K.O. sowie einen Zugang zur Tasche. Ein einfaches Menü zeigt Team und Inventar inklusive Kategorie und Menge. Die Darstellung nutzt zunächst UMG-Formen in ruhigen Wald- und Pergamentfarben; diese Entscheidung legt keine finalen Icons oder Menüillustrationen fest.
- `Tab` öffnet das Menü; `Tab`, `Esc` oder der Button schließen es. Währenddessen sind Weltbewegung und Interaktion gesperrt und die UI erhält Maus-/Tastaturfokus. Während eines Encounters bleibt das Overworld-Menü geschlossen und das HUD verborgen, damit die vorhandene Battle-Präsentation allein sichtbar ist. Item-Nutzung, Team-Sortierung, Detailseiten und ein endgültiges Menüsystem bleiben offen.

## 2026-09-26 – Wiederverwendbare NPC- und Dialoggrundlage

**Status: Funktionaler linearer Dialog mit optionalen Zustandsbedingungen; Story-/Questregeln offen**

- Die frühere Aussage, Dialoge seien nur ein späteres System, ist für einfache mehrseitige Overworld-Gespräche **ersetzt**. Geordnete Seiten stehen in eigenen Primary Data Assets; sie enthalten Sprecher, Text und eine optionale Portraitreferenz. Bedingungen können vorhandene World-Flags oder besiegte Trainer prüfen. Eine Seite kann ein Flag setzen oder eine benannte Folgeaktion an den Quell-Actor melden. Daraus entstehen noch keine verzweigten Entscheidungen oder Questketten.
- Ein allgemeiner Paper2D-fähiger NPC-Actor verwendet die bestehende Interaktionsschnittstelle. Ein Game-Instance-Subsystem führt jeweils ein Gespräch und sperrt währenddessen die vorhandene Overworld-Steuerung. Die UMG-Dialogbox übernimmt den UI-Fokus; das Overworld-Menü kann nicht parallel geöffnet werden. Nach Abschluss oder Schließen erhält der Spieler die Steuerung zurück.
- `Dev_TestMap` enthält einen dreiseitigen Test-NPC und einen Test-NPC, dessen Text nach Setzen des Testflags `Dev_NPCMet` wechselt. Dieses Flag wird über die bereits vom Dev-Save erfassten abgeschlossenen World-/Encounter-IDs gespeichert; damit ändert sich das Save-Schema nicht. Die vorhandene Trainer-Ansprache bleibt vorerst ihr Welt-Textplatzhalter und ist **noch nicht** auf das neue Dialogsystem migriert. Die allgemeine Quell-Actor-/Folgeaktionsschnittstelle bereitet den Anschluss vor. Endgültige NPC-Grafiken, Portraits, Dialoglayout, Quests und Entscheidungen bleiben offen.

## 2026-09-26 – Erster Heil- und Speicherort

**Status: Wiederverwendbarer Test-Schrein; endgültige Ruhepunkt-Gestaltung und Speicherregeln offen**

- Ein interaktiver RestPoint nutzt die bestehende Dialogfolgeaktion: Der Einstiegstext wird bestätigt, danach werden alle Teammitglieder einschließlich K.O.-Mitgliedern auf volle HP und alle belegten Moveslots auf volle PP gesetzt. Bei leerem Team findet keine Heilung oder Speicherung statt. Abbruch vor der Bestätigung verändert den Zustand nicht.
- Speichern ist pro RestPoint optional und geschieht nach erfolgreicher Heilung über den bestehenden Dev-Slot. Ein Speicherfehler lässt die Heilung bestehen und erzeugt eine eigene Rückmeldung. Der in `Dev_TestMap` platzierte Test-Schrein speichert standardmäßig nicht automatisch, damit vorhandene Entwicklungsspielstände nicht durch bloße Interaktion überschrieben werden. Dies ersetzt die bisherige Aussage „kein Autosave“ **nicht**: Es gibt weiterhin kein allgemeines Autosave-System und keine endgültige Speicherort-Regel.
- Die erste Darstellung ist ein austauschbarer Stein-/Kristall-Platzhalter mit optionaler Paper2D-Sprite-Komponente. Andere Arten von Heilorten können denselben Actor mit anderem Text, Sprite und Save-Schalter verwenden. Das Save-Schema und die übrigen Team-, Inventar- und Encounter-Regeln bleiben unverändert.

## 2026-09-26 – Checkpoint und Niederlagenrückkehr

**Status: Erster Rückkehrablauf für Testkämpfe; frühere offene Strafen und Speicherregeln sind durch die Entscheidung vom 2026-09-28 unten ersetzt.**

- Ein RestPoint kann nach bestätigter Heilung optional einen stabil benannten Checkpoint setzen. Gespeichert werden Map-Paket, die beim Aktivieren freie Position des Spielers und seine Blickrichtung. Der Testschrein in `Dev_TestMap` setzt einen Checkpoint, speichert den Dev-Slot aber weiterhin nicht automatisch.
- Die bisherige Rückkehr an derselben Weltposition nach einem vollständigen Kampfverlust ist **ersetzt**. Trainer- und Wildniederlagen führen über denselben Encounter-Abschluss zu einer kurzen Ohnmachtsanzeige, gesperrter Steuerung, Rückkehr zum Checkpoint beziehungsweise zum sicheren PlayerStart-Fallback, vollständiger HP-/PP-Heilung und erneuter Freigabe der Overworld. Besiegte Trainer- und World-Flags werden dabei nicht zurückgesetzt; eine Niederlage markiert keinen Trainer als besiegt.
- Das Dev-Save-Schema steigt von Version 1 auf Version 2. Version-1-Spielstände werden ohne aktiven Checkpoint geladen, während ungültige Checkpoint-Daten vor der Übernahme abgewiesen werden. **Ersetzt als Designstand:** Die damalige offene Frage nach Strafen und allgemeinem Autosave ist durch die Entscheidung vom 2026-09-28 geklärt; der beschriebene technische Stand bleibt unverändert.

## 2026-09-26 – Zusammenhängender Overworld-Testabschnitt

**Status: Kleiner spielbarer Entwicklungsschnitt; Handlung und Weltgestaltung bleiben Platzhalter.**

- `Dev_TestMap` bleibt die gemeinsame technische Overworld-Testmap. Ein gruppierter Abschnitt führt vom bestehenden Ruhe-/Checkpoint-Schrein über den Hauptweg und eine markierte optionale Wildkreatur-Abzweigung zur Trainerprüfung und zum Archivstein. Zwei normale NPCs geben vor und nach dem Ziel unterschiedliche Hinweise. Bestehende visuelle Prototype2D-Assets werden wiederverwendet; weder Kamera noch Kern-Gameplayregeln ändern sich.
- Die Trainerprüfung benutzt ein eigenes datengetriebenes Testprofil mit stabiler ID `Slice_Liora`. Ein Sieg wird vom vorhandenen EncounterSubsystem registriert. Der Archivstein prüft diese ID und setzt nach bestätigtem Ziel-Dialog das World-Flag `Slice_ArchiveSeal`. NPC-Seiten reagieren über die vorhandenen Dialogbedingungen auf dieses Flag. Es gibt hierfür keinen neuen Questmanager und keine neue Speicherstruktur.
- Der bestehende Dev-Slot bewahrt Trainerstatus und Ziel-Flag. Der Testabschnitt soll in wenigen Minuten durchspielbar sein; optionale Wildbegegnung und Fangversuche bleiben für den Abschluss nicht erforderlich. Das Ereignis ist keine endgültige Story, Trainerfigur oder Speziesauswahl.

## 2026-09-27 – Lesbarkeit des Mini-Vertical-Slice

**Status: Verfeinerte Entwicklungsdarstellung; finale Figuren- und Ortsgrafiken bleiben offen.**

- Der vorhandene Ablauf in `Dev_TestMap` bleibt erhalten. Zusätzliche, unregelmäßig gruppierte Paper2D-Bäume, Büsche und Steine rahmen Start, Wild-Abzweigung, Lioras Bereich und Archivstein. Die begehbare Wegmitte bleibt frei. Die vorhandene Boden-Kollisionsfläche reicht nun bis an den Rand der optionalen Abzweigung, damit dort kein unsichtbarer Bodenabbruch entsteht.
- Die vorhandenen Interaktions-Actors verwenden bis zu eigenen Grafiken zugewiesene, farblich unterscheidbare Prototype2D-Sprites. Wenn dem Player noch keine Richtungs-Flipbooks zugewiesen wurden, verwendet er zur Laufzeit eine kleine vorhandene Trainer-Silhouette statt des weißen Testkubus. Zugewiesene spätere Flipbooks haben Vorrang.
- Kamerawinkel und -abstand sowie sämtliche Kampf-, Dialog-, Fang-, Speicher- und Fortschrittsregeln bleiben unverändert. Die derzeitigen Motive sind austauschbare Platzhalter und legen keine endgültige Figurengestaltung fest.

## 2026-09-27 – Figurenlesbarkeit und Welt-Details im Mini-Slice

**Status: Austauschbare illustrierte Entwicklungs-Assets; keine finale Figur oder Kreatur festgelegt.**

- Der bisherige einheitliche Trainer-Sprite als Player-Fallback ist **ersetzt** durch vier gezeichnete Paper2D-Richtungsansichten. Die vorhandenen C++-Blickrichtungen bleiben maßgeblich; spätere Blueprint-Flipbooks haben weiterhin Vorrang. Der kleine Figurenmaßstab und die feste Kamera bleiben erhalten.
- Wanderer, Archivarin und Liora erhalten unterschiedliche Silhouetten und Kleidung; die sichtbare Wildbegegnung erhält eine eigene, ausdrücklich vorläufige Waldkreatur-Grafik. Permanente Welt-Testbeschriftungen sind in `Dev_TestMap` ausgeblendet, während die vorhandene Interaktionsanzeige im HUD bestehen bleibt.
- Unregelmäßig gesetzte, kollisionsfreie Gras-, Blüten-, Wurzel- und Stein-Sprites verdichten die Ränder des Mini-Slice. Die Wegmitte und Interaktionspunkte bleiben frei. Das Overworld-HUD wird kompakter und typografisch ruhiger, ohne seine Funktionen zu ändern. Kampf-, Encounter-, Inventar-, Speicher- und Dialogregeln bleiben unverändert.

## 2026-09-28 – Normale Niederlage, Rettung und Speicherfreiheit

**Status: Verbindliche Designregel; die vorhandenen Systeme werden in diesem Schritt nicht neu gebaut.**

- Bei einer normalen Niederlage wird der Spieler bewusstlos oder kampfunfähig, nicht getötet. Eine eigene Kreatur beschützt ihn oder holt Hilfe. Er erwacht an der zuletzt aktivierten Hüterstätte oder im zuständigen Heilhaus; dort wird das Team geheilt und der Fortschritt automatisch gespeichert. Die Rettung trägt das Thema Vertrauen statt Kontrolle und spiegelt den späteren Wendepunkt der Freund-/Gegenfigur.
- Kreaturen, Erfahrung und wichtige Gegenstände bleiben erhalten. Verbrauchte Gegenstände bleiben verbraucht, zeitlich begrenzte Verstärkungen enden. Vorerst gibt es keinen Geldverlust. Vor wichtigen Story- und Bosskämpfen werden faire Kontrollpunkte vorgesehen.
- Manuelles Speichern und weitere Autosaves sollen möglich sein. Hüterstätten sind nicht die einzige Speichermöglichkeit. Die früher als offen bezeichneten Verlust- und Autosave-Regeln sind damit **ersetzt**.
- **Technisch bereits vorhanden:** gemeinsamer Niederlagenrückweg für Wild- und Trainerkämpfe mit Ohnmachtsanzeige, Checkpoint-/PlayerStart-Rückkehr und HP-/PP-Heilung; versionierter Dev-Slot für Team, Inventar, Welt- und Checkpointzustand; Konsolenbefehle für manuelles Save/Load; optionales Speichern am RestPoint. Der Testschrein aktiviert derzeit einen Checkpoint ohne Autosave.
- **Nur beschlossen, noch nicht implementiert:** Kreaturen-Rettungsinszenierung, ausgestaltete Hüterstätte/Heilhaus, automatisches Speichern nach Niederlage, allgemeine Autosaves, reguläres Speichermenü, Story-/Boss-Kontrollpunkte und zeitlich begrenzte Verstärkungen. Die aktuelle Technik wird dadurch nicht fälschlich als vollständig ausgegeben.

## 2026-09-28 – Wege und Umgebung des Mini-Vertical-Slice

**Status: Überarbeiteter Entwicklungsabschnitt in `Dev_TestMap`; vorhandene Prototype2D-Grafiken bleiben austauschbar.**

- Der sichtbare Hauptweg folgt weichen Kurven vom Start über Wanderer und Liora, über die Brücke und durch die Felsenpassage zum Archivstein. Eine eigene geschwungene Abzweigung führt zur Wildkreatur. Die bisherigen geraden Weg-Rechtecke sind ausgeblendet; der durchgehende Boden bleibt begehbar. Die Wegbreite und die freien Zugänge sind auf die vorhandene freie 8-Wege-Bewegung ausgelegt.
- Die Brücke ist im Verhältnis zur Playerfigur schmaler und kürzer. Deck und Geländer bleiben begehbar beziehungsweise begrenzend, während die Wassergrenzen an die neuen Brückenränder anschließen. Große Felsen in der Passage sind kleiner und versetzt, sodass diagonale Linien offen bleiben.
- Zusätzliche vorhandene Gras-, Blüten-, Busch-, Wurzel-, Stein- und Baum-Sprites bilden unregelmäßige Gruppen. Hütte und Start wirken wohnlicher, die Wild-Abzweigung dichter, Lioras Prüfungsplatz klarer gefasst und der Archivstein älter und leicht verwildert. Dekorative Kronen und kleine Bodendetails blockieren den Player nicht; feste Hindernisse wie Stämme, Haus, Geländer und Wasser behalten ihre Funktion.
- Kamera, Playerbewegung mit 210 cm/s, 8-Wege-Steuerung, Blickrichtungslogik und Input bleiben unverändert. Vier hochwertige diagonale Playeransichten sind weiterhin ein separater Grafikpunkt.

## 2026-09-30 – Erste Quest- und Story-Fortschrittsgrundlage

**Status: Technische Grundlage und Mini-Slice-Testquest; keine endgültige Story oder Quest-Menüführung.**

- `UPokeMonsterQuestData` definiert geordnete Ziele. `UPokeMonsterQuestSubsystem` verwaltet Start, aktiven Schritt und Abschluss. Trainer-, Welt- und Inventarziele lesen die vorhandenen Subsysteme; Dialog- und Fangereignisse werden explizit gemeldet. Die frühere Mini-Slice-Entscheidung „kein Questmanager“ ist durch diese Erweiterung überholt.
- Der Wanderer startet „Das Siegel des Archivs“ per Dialog-Folgeaktion. Lioras vorhandene Trainer-ID und das vorhandene Archiv-Flag bestimmen die nächsten Schritte; die Wild-Abzweigung bleibt optional. Im Overworld-HUD erscheinen nur Questname und aktuelles Ziel, nicht ein vollständiges Questbuch.
- SaveGame-Version 3 speichert ausschließlich stabilen Questfortschritt und Fangereignis-IDs. Versionen 1/2 werden kontrolliert gelesen; bereits belegte Trainer- und Archivmeilensteine werden daraus rekonstruiert. Früheres bloßes Sprechen mit dem Wanderer kann aus einem alten Save nicht erkannt werden. Kampf-, Fang-, Bewegung-, Kamera- und Checkpointregeln bleiben unverändert.

## 2026-10-01 – Heilhaus als eigenständiger Function-Gate-Prototyp

**Status: Begehbarer Gebäudeblockout; keine endgültige Architektur oder Grafik.**

- Die neue `Dev_HealingHouseTestMap` nutzt einen offenen Eingang in derselben Welt. Kein Streaming, keine zweite Innenraum-Map und keine künstliche Türschwelle. `Dev_TestMap` bleibt unverändert.
- Die Hüterin verwendet den vorhandenen RestPoint mit NPC-Sprite, Dialog, HP-/PP-Heilung, Checkpoint und Dev-Save. Der freie Benutzungsort wird vor dem Speichern zum Checkpoint. Es entsteht kein zweites Heil-, Save- oder Niederlagensystem. Der bestehende Dev-Slot wird bei bestätigter Rast gespeichert; der Dialog kündigt dies ausdrücklich an.
- Eine kleine gebäudebezogene Cutaway-Box schaltet Dach und kameraseitige Fassade unsichtbar, ohne die Wandkollisionen zu verändern. Sie prüft die Spielerposition auch nach Spawn oder Niederlagenrückkehr. Das ist kein allgemeines Occlusion-Framework. Die vorhandene Kamera bleibt unverändert.
- Gebäudekörper, Dach, Tür, Fenster, Einrichtung und funktionale Actors sind getrennte Bauteile. Der breite Hauptlaufweg und die offene Tür orientieren sich am vorhandenen Player mit 56 cm Kapseldurchmesser und 96 cm Kapselhöhe. Der Tresen blockiert Bewegung, lässt jedoch Interaktions-Traces zum Hüter durch. Kleine Deko bleibt nichtblockierend.

## 2026-10-02 – Blender-Heilhaus V1 als austauschbare Gebäudehülle

**Status: Modularer lokaler Architekturprototyp; keine endgültige Spielgrafik.**

- Blender wird für dieses Gebäude als Quelle außerhalb von `Content` genutzt. Meter im Quellmodell werden über FBX-Einheiten zu Unreal-Zentimetern; X/Z bleiben erhalten, die Y-Achse wird wegen der unterschiedlichen Koordinatenhändigkeit bewusst gespiegelt. Die Importgrenzen sämtlicher Module werden geprüft.
- Der bestehende Heilhaus-Grundriss und die 2,40 × 2,30 m große, ebenerdige Eingangspassage bleiben die funktionale Referenz. Der neue Gebäudekörper ist 10,30 × 9,30 m groß, mit Vorbau/Überstand 12,20 × 9,90 m. Der First liegt bei 6,40 m. Es gibt weiterhin nur ein begehbares Erdgeschoss; das Konzept-Obergeschoss ist noch kein Feature.
- 24 getrennte Module mit insgesamt 1.124 Dreiecken und sieben einfachen Material-Slots bilden die neue Hülle. Dach, vorderer Giebel und kameraseitige Fassadenteile sind unabhängig ausblendbar. Keine finalen Schindeln, Blumen, Ornamente oder hochauflösenden Texturen wurden produziert.
- Der lokale Export-/Importweg verwendet FBX mit getrennten Static Meshes und ohne automatische Ganzhaus-Collision. Nach Prüfung neben dem Original wurde nur dessen Darstellung ersetzt. Der alte Blockout bleibt unsichtbar erhalten und liefert weiterhin einfache Gameplay-Collision. Hüterin, RestPoint, Checkpoint, Save/Load und die vorhandene Cutaway-Logik werden wiederverwendet; Player und Spielkamera bleiben unverändert.

- **Für V1 historisch, durch die anschließende Scale Calibration ersetzt:** Scale 0,36 blieb im Architektur-Prototyp zunächst erhalten. Die 54,21 cm bezeichneten nur die transparente Sprite-Leinwand; der 1,40-m-Block war eine Blender-Prüfhilfe.
- Der funktionale V1 wurde mit erfolgreichem Mac-Build, allen 34 PokeMonster-Automationstests und einem echten PIE-Fußweg von außen zur Hüterin und zurück überprüft. Der bestehende Dev-Slot wurde durch die reguläre Hüterinnen-Interaktion gespeichert; der vorherige Slot wurde zuvor temporär gesichert.

## 2026-10-02 – Player-/Heilhaus-Scale-Calibration

- Die Figur soll einen aufrechten Körper von ungefähr 140 cm repräsentieren. Der tatsächliche Alpha-Körper der 256 × 512-Pixel-Quellen umfasst 429–438 Pixel, nicht die gesamte Leinwand. Die bisherige Sprite-Skalierung 0,36 ergab nur 45,42–46,38 cm sichtbare Höhe in der Sprite-Ebene.
- Die bisherige Sprite-Neigung von Roll -55° wird durch eine aufrechte Paper2D-Fläche (Yaw 45°, Roll 0°) ersetzt. Eine nur auf Bildschirmhöhe kalibrierte geneigte Fläche hatte geometrisch nur etwa 49 cm Höhe: Am 92-cm-Tresen wurde der Kopf falsch verdeckt. Visuelle Component-Scale (0,66; 0,66; 1,086758) erhält die schmale Bildschirm-Silhouette und gibt dem Körper tatsächlich 140 cm Welt-Z-Höhe. Kamera und ihre Perspektive bleiben unverändert. Die Änderung betrifft ausschließlich die Sprite-Darstellung.
- Der gemeinsame Fuß-Pivot liegt bei Quellpixel (128,488), an der sichtbaren Sohle. Pixels Per Unreal Unit wird pro Pose anhand ihrer Alpha-Körperhöhe normiert (3,4 × Körperpixel / 438). Das ergibt gleiche sichtbare Körperhöhe ohne Richtungs-/Frame-Sprünge. Die PNGs und Flipbook-Zuordnungen bleiben unverändert.
- Die Sprite-Komponente wird rein visuell um die unveränderte Capsule-Halbhöhe nach unten versetzt. Actor-Scale 1, Capsule 28-cm-Radius/48-cm-Halbhöhe, Bewegung 210 cm/s, Kamera, Interaktion und alle Gameplay-Systeme bleiben unverändert. Vergleichsreferenzen sind kurzlebige Debug-Zeichnungen im PIE, keine gespeicherten Actors.
- Vollständige Messwerte und Prüfung: `Docs/SCALE_CALIBRATION.md`.

## 2026-10-02 – Kontrollierter Overworld-Kameraabstand

- Der tatsächlich verwendete Perspektivabstand der SpringArm-Kamera wird von 1400 auf 2000 cm erhöht. In PIE wurden zuerst 1800 cm und danach 2000 cm bei gleichem Winkel/FOV verglichen. 2000 cm geben die bessere Übersicht; die kalibrierte 140-cm-Figur bleibt lesbar. Kein Abstand ab 2200 cm wurde getestet oder übernommen.
- Außenansicht, Eingang/Vorplatz, offenes Gelände und Innenraum wurden in `Dev_HealingHouseTestMap` verglichen. Auch bei 2000 cm passt das große Heilhaus unmittelbar vor dem Eingang nicht vollständig ins Bild. Eine vollständige Referenzkomposition würde zusätzlich eine andere Bildausrichtung erfordern; diese Aufgabe ändert ausschließlich den Abstand.
- Perspektive, Rotation (-55°, -45°, 0°), FOV 35°, Camera Lag mit Geschwindigkeit 6 und maximal 180 cm bleiben unverändert. Sprite-/Actor-Skalierung, 140 cm Körperhöhe, Capsule, 210 cm/s Bewegung, Input, Blickrichtungen und Gameplay werden nicht angepasst. Die Maps werden nicht gespeichert oder verändert.
- Die bestehende Scale-Calibration-Testassertion prüft den neuen Kameraabstand; die Körpergrößen-Prüfungen bleiben unverändert. Mac-Development-Build erfolgreich; alle 35 vorhandenen PokeMonster-Automationstests erfolgreich, einschließlich Player Foundation, Scale Calibration und HealingHouse. Zusätzliche PIE-WASD-Prüfung in `Dev_TestMap`: tatsächliche Bewegung und Kamerafolgen bestätigt; im offenen Wegbereich bleiben Figur und NPCs lesbar. Vorhandene Vordergrund-Baumkronen können die Figur weiterhin verdecken; daran wird bei dieser reinen Abstandsanpassung nichts geändert.

## Aktuell offene Entscheidungen

- endgültiger Spielname
- Namen der Welt, Regionen und Städte
- genaue Hauptgeschichte
- Hauptfigur und Motivation
- Arenen oder eigenes Prüfungssystem
- endgültige Fangmechanik
- endgültiges Kampfsystem
- endgültige Verteilung sichtbarer, Zonen- und möglicher Zufallsbegegnungen
- linearer Weg oder alternative Routen
- genaue Demo-Kreaturen
- endgültige Attackenverwaltung
- genaue Schnellreise- und Weltfähigkeiten
- endgültige Zielauflösung und exakte Pixelgrößen
- Musik- und Soundkonzept
