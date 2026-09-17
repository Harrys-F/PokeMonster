# Technisches Konzept – PokeMonster

## Projektstatus

PokeMonster befindet sich am Anfang der Entwicklung. Zunächst wird eine kleine, technisch saubere und spielbare Demo erstellt. Das Projekt soll schrittweise erweitert werden.

Harry übernimmt vor allem Planung, Entscheidungen und Tests. Codex und die angeschlossenen Entwicklungswerkzeuge sollen möglichst viel der technischen Umsetzung übernehmen.

## Zielplattform

- ausschließlich macOS
- Einzelspieler
- kein Multiplayer
- kein Ingame-Store
- zunächst kein iPhone- oder iPad-Build

Andere Plattformen werden erst berücksichtigt, wenn dies ausdrücklich neu beschlossen wird.

## Entwicklungsgerät

- MacBook Air mit Apple M4
- 16 GB gemeinsamer Arbeitsspeicher
- ungefähr 400 GB freier interner Speicher
- externe SSD vorhanden

Die aktive Projektentwicklung erfolgt auf der internen SSD. Externe Datenträger können später für zusätzliche Sicherungen, archivierte Builds und große Exportdateien verwendet werden.

## Entwicklungssoftware

- Unreal Engine 5.8.2
- Paper2D
- Enhanced Input
- C++
- Blueprints
- Rider als primäre Entwicklungsumgebung
- Xcode und Apple-Toolchain für macOS-Builds
- Blender für später benötigte Grafiken, Modelle oder vorbereitete Assets
- Git und Git LFS
- Codex und gegebenenfalls MCP-Anbindungen zur Automatisierung

RiderLink und MCP sind Hilfsmittel. Das Unreal-Projekt darf nicht technisch davon abhängig werden, dass diese Werkzeuge jederzeit verfügbar sind.

## Technische Architektur

Das Projekt verwendet eine Kombination aus C++ und Blueprints.

### C++

C++ soll bevorzugt verwendet werden für:

- grundlegende Spiellogik
- Datenstrukturen
- Speicher- und Ladesystem
- Kampfsystem-Grundlagen
- Kreaturen- und Attackendaten
- Inventar-Grundlagen
- wiederverwendbare Komponenten
- Systeme, die stabil und langfristig wartbar sein müssen

### Blueprints

Blueprints sollen bevorzugt verwendet werden für:

- Level- und Ereignislogik
- NPC-Konfiguration
- Dialogabläufe
- Animationen
- visuelle Effekte
- Benutzeroberflächen
- Balancing-Werte
- schnelle Prototypen und Tests

Systeme sollen nicht unnötig doppelt in C++ und Blueprints implementiert werden.

### Kreaturen: Spezies, Instanzen und Fortschritt

`Creatures/PokeMonsterCreatureSpeciesData` enthält die gemeinsamen Artdaten als `UPrimaryDataAsset`: Basiswerte, Wachstumsgruppe und Entwicklungswege. `FPokeMonsterCreatureInstance` referenziert die Spezies und enthält ausschließlich den individuellen Zustand einschließlich Instanz-ID, Level, Gesamt-Erfahrung, aktuellen HP und berechneten Statuswerten.

`UPokeMonsterCreatureProgression` bündelt die Berechnung in C++ und stellt Blueprint-Funktionen bereit. Die Logik benötigt weder eine Map noch Player, Inventar oder UI.

- Levelbereich: 1–100. Eine neu erzeugte Instanz erhält die kumulative XP-Schwelle ihres Startlevels und volle berechnete HP. Der Factory-Parameter `0` verwendet das Startlevel der Spezies; andere Werte werden auf den Levelbereich begrenzt.
- `AddExperience` addiert nichtnegative Gesamt-Erfahrung, verarbeitet mehrere Level-Ups und begrenzt XP auf die Schwelle von Level 100. Auch sehr große `int64`-Beträge sind ohne Überlauf möglich. Das Ergebnis enthält Erfolg, tatsächlich angenommene XP und Anzahl gewonnener Level.
- Negative Beträge, fehlende Spezies oder inkonsistente Kombinationen aus Level und XP werden ohne Zustandsänderung abgewiesen. Ein Betrag von null sowie eine Vergabe am Höchstlevel sind erfolgreiche Vorgänge ohne Änderung.
- `GetExperienceToNextLevel` berechnet die noch fehlenden XP aus der nächsten kumulativen Schwelle. Der Wert wird nicht redundant gespeichert; auf Level 100 ist er null.
- Alle sechs vorbereiteten Wachstumsgruppen sind implementiert: Fast, MediumFast, MediumSlow, Slow, Erratic und Fluctuating. Level 1 beginnt stets bei null XP. Die Kurven sind eine technische Arbeitsgrundlage, kein endgültig beschlossenes Balancing.
- `FPokeMonsterCreatureStats` trennt die sechs berechneten Werte von den Spezies-Basiswerten. Vorläufig gilt: `MaxHP = floor(2 * BasisHP * Level / 100) + Level + 10`; andere Werte verwenden `floor(2 * Basiswert * Level / 100) + 5`. IVs, EVs, Wesen und Kampfmodifikatoren sind nicht enthalten.
- Statuswerte werden beim Erzeugen und bei Level-Ups neu berechnet. Fehlende HP bleiben bei einem Level-Up erhalten; null HP bleiben null. Es gibt keine automatische Wiederbelebung.

#### Entwicklungsprüfung

Ein Eintrag in `Evolutions` beschreibt einen möglichen Entwicklungsweg. `IsEvolutionEligible` prüft ihn ohne Nebenwirkungen; `GetEligibleEvolutions` prüft die Wege der referenzierten Spezies und liefert eindeutige Ziel-IDs. Mehrere Wege sind Alternativen. Alle ausgefüllten Bedingungen innerhalb eines Weges müssen gleichzeitig erfüllt sein.

`FPokeMonsterEvolutionContext` enthält den gerade geprüften Auslöser, das verwendete Item, den aktuellen Ort, die ausgeführte Handlung sowie einen Freundschaftswert von 0–255. Diese Werte liefert künftig das aufrufende Spielsystem. Sie werden durch die Prüfung weder verändert noch verbraucht.

Unterstützt werden Level, Item, Freundschaft, Ort und `SpecialInteraction` für besondere Handlungen/Prüfungen. Jeder Weg kann zusätzlich Mindestlevel, Item-ID, Orts-ID, Aktions-ID und Mindestfreundschaft verlangen. Der Kontext-Auslöser muss zum Weg passen. Beispiel einer ehemaligen Tauschentwicklung: `SpecialInteraction`, `MinimumLevel = 44`, `RequiredLocationId = AncientSanctum`, `RequiredActionId = CompleteTrial`. Erst die passende Handlung am passenden Ort mit ausreichendem Level erfüllt den Weg. Diese Namen und das Level illustrieren ausschließlich die Technik.

Das vorhandene `RequirementId` bleibt als ältere Anforderung für Item-, Orts- und Aktionsauslöser unterstützt; neue Daten sollten die ausdrücklich benannten Felder verwenden. Fehlende Pflichtbedingungen, ungültige Ziele und nicht implementierte `Custom`-Auslöser ergeben `false`. Die Ziel-ID muss den Typ `CreatureSpecies` tragen; Ziel-Assets werden dabei nicht geladen oder auf Existenz geprüft. Die Instanzabfrage schließt eine Entwicklung in dieselbe Spezies aus.

Die Prüfung führt keine Entwicklung aus, verbraucht keine Items und persistiert keine Prüfungsfortschritte. XP-Vergabe löst die Prüfung nicht automatisch aus. UI, tatsächlicher Spezieswechsel, Inventaranbindung und Speicherung folgen später. Ein späterer Ladepfad muss alte oder inkonsistente Instanzdaten ausdrücklich migrieren; ein Speichersystem existiert noch nicht.

Automatisierte Tests unter `PokeMonster.Creatures` decken Asset-Laden, Spezies-/Instanztrennung, alle Wachstumsgruppen, Grenzwerte, Mehrfach-Level-Ups, HP und kombinierte Entwicklungsbedingungen ab. `PokeMonster.Player.Foundation` bleibt als bestehender Regressionstest erhalten.

### Attacken und Kampfgrundlage

`Moves/PokeMonsterMoveData` definiert gemeinsame Attackendaten als `UPrimaryDataAsset` mit dem Primary-Asset-Typ `CreatureMove`. ID, Anzeigename, Kreaturentyp, Kategorie Physical/Special/Status, Basisstärke, Genauigkeit in Prozent, maximale PP und Priorität sind im Editor konfigurierbar. `FPokeMonsterMoveEffect` bereitet Effekt-ID, Beschreibung und Chance vor; Effekte werden noch nicht ausgeführt. Der Asset Manager scannt `/Game/Data/Moves` und berücksichtigt die Assets beim Cooken.

Jede Kreatureninstanz besitzt genau vier zunächst leere `FPokeMonsterMoveSlot`-Einträge. Ein Slot enthält eine weiche Attackenreferenz sowie eigene aktuelle und maximale PP. Gemeinsame Attackendaten enthalten keine verbrauchbaren PP. C++-Zuweisung beziehungsweise `UPokeMonsterBattleLibrary::AssignMove` füllt die PP; dies ist eine technische Konfigurationsfunktion, keine Lern- oder Kampfregel. `ConsumeMovePP` verweigert leere Slots, ungültige Indizes, nichtpositive Kosten und Überziehungen ohne Änderung. Level-Ups lassen Slots und PP unverändert. Eine spätere Änderung der maximalen PP im Data Asset erfordert eine ausdrückliche Migration bereits bestehender Instanzen; inkonsistente Slots werden abgewiesen.

`Battle/PokeMonsterBattleLibrary` bietet getrennte, Blueprint-freundliche Funktionen:

- `CheckHit`: Ein vom Aufrufer gelieferter gleichverteilter ganzzahliger Wurf von 0 bis 99 trifft genau dann, wenn er kleiner als die Genauigkeit ist. 0 Prozent trifft nie, 100 Prozent trifft immer bei gültigem Wurf. Ungültige Daten/Würfe ergeben `false`. Der explizite Wurf erlaubt deterministische Tests; eine spätere Kampfsteuerung liefert den Zufall.
- `CalculateDamage`: Berechnet ausschließlich den Schaden eines bereits getroffenen Angriffs. Physical verwendet Angriff/Verteidigung, Special verwendet Spezial-Angriff/Spezial-Verteidigung. Die Kategorie gehört zur Attacke und wird nicht aus ihrem Typ abgeleitet.
- Vorläufige Formel: `Basis = floor((floor(2 * Level / 5) + 2) * Stärke * Offensive / Defensive / 50) + 2`; anschließend `floor(Basis * Typmultiplikator)`. Wirksame Treffer verursachen mindestens 1 HP, Immunität exakt 0. Extreme positive Werte werden auf `int32` begrenzt; ungültige Daten und nichtpositive relevante Statuswerte liefern ein ungültiges Ergebnis statt einer Division durch null.
- Statusattacken besitzen Stärke 0 und verursachen hier keinen direkten Schaden. Ihre späteren Ziel-, Effekt- und Immunitätsregeln sind nicht implementiert. Die Typentabelle beschreibt die Wirkung direkter Schadensattacken.
- `GetTypeMultiplier` verwendet eine zentral gepflegte Tabelle unter `Battle/PokeMonsterTypeChart.cpp`. Sie umfasst alle 17 Typen mit den Matchups der zweiten Generation, einschließlich der damaligen Stahl-Resistenzen gegen Geist und Unlicht. Die Fakten wurden gegen die [öffentlich einsehbare Typentabelle des pokecrystal-Projekts](https://github.com/pret/pokecrystal/blob/master/data/types/type_matchups.asm) geprüft; es wurden keine ROM-Dateien oder Grafik-/Audio-Assets übernommen.
- Zwei Zieltypen multiplizieren ihre Faktoren: 0, 0,25, 0,5, 1, 2 oder 4. Immunität dominiert. `None` bedeutet ausschließlich fehlender Sekundärtyp; doppelt eingetragene Zieltypen werden nur einmal berücksichtigt. Ungültige Typangaben liefern `-1` und machen eine Schadensberechnung ungültig.

Die Berechnung verändert weder HP noch PP, Speziesdaten oder Progression. Eine spätere Kampfsteuerung muss PP einmal je akzeptiertem Angriffsversuch verbrauchen, auch bei Fehlschlag oder Immunität, danach Treffer und gegebenenfalls Schaden prüfen und anwenden. Diese Reihenfolge wird noch nicht als Rundensteuerung implementiert. Es gibt keine STAB-Boni, kritischen Treffer, zufällige Schadensstreuung, Statusveränderungen, Initiative-Sortierung, Lernlogik, Trainer, Battle-UI oder Animationen. Priorität ist vorerst nur ein Datenfeld. Das endgültige Balancing bleibt offen.

Testdaten unter `/Game/Data/Moves`: `DA_TestNormalPhysical` (Normal/Physical, Stärke 40, Genauigkeit 100, PP 35), `DA_TestFireSpecial` (Feuer/Special, Stärke 50, Genauigkeit 95, PP 25) und `DA_TestStatus` (Normal/Status, Stärke 0, Genauigkeit 100, PP 20). Alle haben Priorität 0. Tests unter `PokeMonster.Moves` und `PokeMonster.Battle` prüfen Laden/Asset-Manager, PP-Trennung und Verbrauch, Treffergrenzen, Schadensformel, alle 289 einfachen Typenpaarungen, Doppeltypen und Immunitäten.

## Darstellung

- 2D-Top-Down-Perspektive
- Paper2D als technische Grundlage
- moderne handgezeichnete 2D-Grafik
- leicht schräge 3/4-Top-Down-Perspektive
- Perspektive und Figurengröße orientieren sich an der ersten Referenzszene
- mehrere visuelle Tiefenebenen
- modulare Paper2D-Assets
- technische Kameraart wird in der Stil-Testszene geprüft
- kleine Figuren im Verhältnis zu einer dichten, detailreichen Umgebung
- Layer für Hintergrund, Boden, begehbare Ebene, Dekoration, Figuren/Kreaturen, Überdachungen und Vordergrund
- wiederverwendbare Module für Außenbereiche, Innenräume, Höhlen, Ruinen, Brücken, Treppen, Terrassen und Wasserfälle
- kontrollierte Sortierung und Überlagerung, damit Figuren korrekt vor und hinter Umgebungselementen erscheinen
- Vordergrundelemente müssen bei längerer Verdeckung transparent oder ausgeblendet werden können
- hochauflösende, sauber gezeichnete Grafiken
- moderne 2D-Darstellung statt absichtlich unscharfer Retro-Grafik
- übersichtliche und gut lesbare Spielwelt
- stimmungsvolle Beleuchtung und Effekte nur in einem für das MacBook sinnvollen Umfang

Die 2.5D-Wirkung entsteht vorrangig durch Paper2D-Sprites, Layering, Skalierung, Sortierung, Farbperspektive, weiche Kontaktschatten und sparsame Effekte. Dreidimensionale Hilfsgeometrie darf für Kollisionen, Höhen, Brücken oder Beleuchtung eingesetzt werden, wenn sie sich der gezeichneten Darstellung unterordnet.

Die technische Kameraart, Sortierregeln, begehbaren Höhenebenen und Übergänge zwischen Innen- und Außenbereichen werden zunächst in kleinen Tests festgelegt. Orthografische, nahezu orthografische und perspektivische Varianten werden nach ihrer visuellen Übereinstimmung mit den Referenzen, ihrer Lesbarkeit und ihrer technischen Stabilität bewertet.

Hohe Umgebungsdichte wird über geteilte Texturen, modulare Assets, Instanzvarianten, begrenzte Materialvielfalt und sichtbarkeitsabhängige Effekte umgesetzt. Transparenzen, große Texturen, dynamische Beleuchtung, Wasserfälle, Nebel und Partikel müssen auf dem MacBook Air M4 mit 16 GB RAM gezielt profiliert werden.

## Grafikprofile

Drei Profile sind vorgesehen:

### Medium

- Standardprofil für das MacBook Air
- flüssige Darstellung
- gute Bildqualität
- reduzierte Effekte
- begrenzte Bildrate
- möglichst effiziente Auslastung
- als Richtwert soll das Gerät nicht dauerhaft vollständig ausgelastet werden

### Hoch

- verbesserte Effekte und Darstellungsqualität
- höhere, aber weiterhin kontrollierte Auslastung

### Ultra

- höchste vorgesehene Darstellungsqualität
- nicht das primäre Entwicklungs- oder Testprofil
- darf das Gerät stärker beanspruchen

Die endgültigen Auflösungen, Bildraten und Scalability-Werte werden nach ersten Leistungstests festgelegt.

## Daten und Versionsverwaltung

Git wird für Quellcode, Konfiguration und Dokumentation verwendet. Git LFS wird für große Binärdateien verwendet, insbesondere:

- `*.uasset`
- `*.umap`
- `*.blend`
- `*.fbx`
- `*.wav`
- `*.psd`

Ordner wie `Binaries`, `DerivedDataCache`, `Intermediate` und `Saved` sollen normalerweise nicht versioniert werden.

Nach stabilen Meilensteinen soll ein Git-Commit erstellt und auf das Remote-Repository übertragen werden.

## Qualitätsregeln

Vor dem Abschluss eines Arbeitsschrittes soll Codex, soweit möglich:

- geänderte Dateien kontrollieren,
- Unreal-Projektdateien nicht unnötig von Hand verändern,
- C++ kompilieren,
- offensichtliche Fehler und Warnungen prüfen,
- vorhandene Tests ausführen,
- erklären, was Harry im Unreal Editor testen soll.

## Noch offene technische Entscheidungen

- genaue Struktur des Kampfsystems
- erweiterte Kreaturen-/Attackendaten, Lernregeln und Persistenz
- Speichersystem und Anzahl der Speicherstände
- konkrete Auflösungen und Bildraten der Grafikprofile
- Umfang der Unreal- und Blender-MCP-Automatisierung
- endgültige Ordnerstruktur innerhalb des Content-Ordners
