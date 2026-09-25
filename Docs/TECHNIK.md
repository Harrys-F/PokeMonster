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

Die Berechnungsfunktionen verändern weder HP noch PP, Speziesdaten oder Progression. Die unten beschriebene Battle-Session verwendet sie für die Rundensteuerung und übernimmt PP-Verbrauch, Zugreihenfolge sowie HP-Anwendung. Es gibt weiterhin keine STAB-Boni, kritischen Treffer, zufällige Schadensstreuung, Statusveränderungen, Lernlogik, Trainer oder Kampfanimationen. Eine erste separate Battle-Testoberfläche ist unten beschrieben. Das endgültige Balancing bleibt offen.

Testdaten unter `/Game/Data/Moves`: `DA_TestNormalPhysical` (Normal/Physical, Stärke 40, Genauigkeit 100, PP 35), `DA_TestFireSpecial` (Feuer/Special, Stärke 50, Genauigkeit 95, PP 25) und `DA_TestStatus` (Normal/Status, Stärke 0, Genauigkeit 100, PP 20). Alle haben Priorität 0. Tests unter `PokeMonster.Moves` und `PokeMonster.Battle` prüfen Laden/Asset-Manager, PP-Trennung und Verbrauch, Treffergrenzen, Schadensformel, alle 289 einfachen Typenpaarungen, Doppeltypen und Immunitäten.

### 1-gegen-1-Battle-Session

`UPokeMonsterBattleSession` unter `Battle/PokeMonsterBattleSession.h/.cpp` ist ein eigenständiges, Blueprint-freundliches `UObject` ohne World-, Actor- oder Tick-Abhängigkeit. Es verwendet die bestehenden Attacken-, Typen- und Schadensfunktionen unverändert. `FPokeMonsterBattleState` enthält genau eine aktive Kreatur je Seite, Phase, Rundenzähler und Gewinner. Die Phasen sind `Uninitialized`, `AwaitingChoices` und `Finished`.

`Initialize(SideA, SideB, RandomSeed)` startet eine neue Session mit zwei gültigen, lebenden und unterschiedlichen Kreatureninstanzen. Die Session hält eigene Kopien ihres Zustands und starke Referenzen auf die verwendeten Spezies-/Attacken-Assets, damit deren weiche Instanzreferenzen zwischen Runden nicht durch Garbage Collection verloren gehen. Die übergebenen Kreaturen außerhalb der Session werden nicht automatisch verändert. Ein späterer Aufrufer kann die fertigen Kreaturenzustände aus `GetState()` gezielt übernehmen; Speichern, Belohnungen und XP-Vergabe werden hier nicht ergänzt. Der Aufrufer muss die Session selbst über eine `UPROPERTY` oder eine andere starke Unreal-Referenz halten.

`ResolveRound(SlotA, SlotB)` erhält beide Auswahlen gemeinsam (Slotindizes 0–3). Die Session prüft zunächst beide Kreaturen, Attacken und PP sowie die Schadensberechenbarkeit. Ungültige Eingaben liefern einen strukturierten Fehler mit betroffener Seite. HP, PP, Phase, Rundenzähler und Zufallszustand bleiben dann vollständig unverändert; es entstehen keine Erfolgs-Events. Der Aufrufer kann anschließend korrigierte Auswahlen übergeben.

Für eine gültige Runde gilt:

1. Höhere Attackenpriorität beginnt; bei Gleichstand höhere berechnete Initiative (`Speed`). Bei vollständigem Gleichstand beginnt deterministisch Seite A.
2. Beide gültigen Auswahlen werden als Events ausgegeben. Ausgeführte Aktionen folgen anschließend in der tatsächlichen Zugreihenfolge.
3. Jeder tatsächlich ausgeführte Angriffsversuch verbraucht genau eine PP, auch bei Fehlschlag, Immunität oder einer Statusattacke ohne implementierten Effekt.
4. Ein eigener, mit dem Start-Seed initialisierter `FRandomStream` liefert Trefferwürfe von 0–99. Gleiche Ausgangsdaten, Seeds und Auswahlen ergeben denselben Ablauf; abgewiesene Runden verbrauchen keine Zufallswürfe.
5. Bei einem Treffer wird der vorhandene Schaden auf die verbleibenden Ziel-HP begrenzt und angewendet. Immunität verändert keine HP. Statusattacken durchlaufen PP-/Trefferprüfung, führen aber noch keine Effekte aus.
6. Bei null HP folgen K.O.- und Kampfende-Event; die Session wird `Finished` und speichert den Gewinner. Die besiegte Kreatur führt ihre vorgemerkte Attacke nicht aus und verbraucht dafür weder PP noch einen Zufallswurf.
7. Ohne K.O. wartet die Session auf die nächsten beiden Auswahlen. Nach Kampfende werden weitere Runden ohne Änderung abgewiesen. Eine gestartete Session wird nicht durch erneutes Initialisieren überschrieben.

`FPokeMonsterBattleResult` enthält Erfolg, Fehlercode/Fehlerseite, Rundennummer, Gewinner und eine geordnete Eventliste. `FPokeMonsterBattleEvent` unterstützt `MoveChosen`, `MoveExecuted`, `Missed`, `Damage`, `SuperEffective`, `NotVeryEffective`, `Immune`, `KnockedOut` und `BattleEnded`. Events enthalten Seiten, Instanz-IDs, Attacken-ID, Slot und Kategorie; passende Events ergänzen Trefferwurf, PP vorher/nachher, Typmultiplikator sowie tatsächlichen HP-Verlust und HP vorher/nachher. Nicht zutreffende HP-/PP-/Wurfwerte sind `-1`. Bei K.O. bezeichnet `Source` den Verursacher und `Target` die besiegte Kreatur; bei Kampfende ist `Source` der Gewinner. Neutrale Wirkung wird durch `Damage` mit Faktor 1 dargestellt. Immunität erzeugt keinen künstlichen Schadenseintrag; Status-Platzhalter bleiben anhand ihrer Kategorie erkennbar.

Die Session verwaltet keinen unbegrenzten Eventverlauf: Der Aufrufer erhält die Ergebnisse je Aufruf und kann sie später für UI/Animationen aufbewahren. Fehler umfassen insbesondere ungültige Slots, fehlende Spezies/Attacken, ungültige Status-/PP-Daten, null PP, bereits besiegte Kreaturen, fehlende Initialisierung und einen bereits beendeten Kampf. Es gibt keine automatische Ersatzattacke bei aufgebrauchten PP und kein erzwungenes Ende für reine Status-/Immunitätsrunden; sie benötigen weitere sinnvolle Auswahlen. Es läuft keine automatische Endlosschleife. Teams, Wechsel, Items, Trainer, Fangmechanik und Statuszustände sind weiterhin nicht enthalten.

Tests unter `PokeMonster.Battle.Session` prüfen Priorität, Initiative und Gleichstand, Auswahl-/Eventreihenfolge, HP-/PP-Anwendung, Treffer und Fehlschläge, Typeneffektivität und Immunität, frühes K.O. auf beiden Seiten, mehrere aufeinanderfolgende Runden, Kampfende, atomare Fehlerbehandlung, Seed-Reproduzierbarkeit und Asset-Lebensdauer über Garbage Collection. Alle bisherigen Projekt-Tests bleiben Bestandteil der Gesamtsuite.

### Erste Battle-Testoberfläche

`/Game/Maps/Dev_BattleTestMap` ist eine separate Testmap mit eigenem `APokeMonsterBattleTestGameMode` und `APokeMonsterBattleTestController`. Sie verändert weder den globalen GameMode noch `Dev_TestMap` oder die bestehende Player-Kamera. Ein statischer CameraActor stellt den View bereit; ein Welt-Pawn wird für diesen reinen Oberflächentest nicht benötigt.

Die Klassen unter `UI` trennen drei Aufgaben:

- `UPokeMonsterBattlePresenter` hält eine eigene BattleSession, nimmt die Spielerauswahl entgegen und wählt für den Gegner den ersten gültigen Slot mit verbleibenden PP. Er berechnet keinen Schaden selbst, sondern ruft ausschließlich die bestehende Session auf. Lesemodelle liefern Namen, Level, HP, vier Attacken mit Typ/PP sowie Status und Kampflog. Die vollständigen geordneten BattleEvents bleiben über `OnRoundResolved` verfügbar.
- `APokeMonsterBattleTestController` startet die Testbegegnung, erstellt das Widget, aktiviert Maus/UI-Eingabe und löst die gewählte Runde nach einer kurzen Auswahlpause von 0,22 Sekunden aus. Der Presenter sperrt weitere Eingaben sofort bei Auswahl und bis `FinishPresentation`. Doppelte Auflösung und vorzeitiges Entsperren werden abgewiesen. Das Widget ruft `FinishPresentation` erst nach der sichtbaren Eventfolge auf; ohne Widget oder bei einem Fehler erfolgt die Freigabe sofort.
- `UPokeMonsterBattleWidget` ist ein natives UMG-Widget mit skalierter Oberfläche, HP-Balken, vier Buttons, scrollendem Log und zwei eigenen transparenten Kreaturen-Platzhaltern. Die eigene Kreatur steht unten links, der Gegner oben rechts. Die Gestaltung kann durch eine Widget-Blueprint-Unterklasse mit den gleichnamigen Controls und den Ereignissen `OnBattleViewUpdated`, `OnBattleRoundResolved` und `OnBattlePresentationStep` ersetzt oder ergänzt werden; `WidgetClass` am Testcontroller ist dafür konfigurierbar.

Die Demo verwendet vorhandene Assets: `DA_TestWater` gegen `DA_TestGrass`, beide auf Level 20 mit anfänglich 52 beziehungsweise 50 HP. Die vier Spielerslots enthalten `DA_TestNormalPhysical`, `DA_TestFireSpecial`, `DA_TestStatus` und erneut `DA_TestNormalPhysical`. Der vierte Slot besitzt eigene PP; für diesen Test ist kein viertes Attacken-Asset nötig. Gegnerauswahl und Seed sind für reproduzierbare Tests festgelegt. Diese Zusammenstellung ist keine Lern- oder endgültige Kampfregel.

Während der Auflösung sind Attacken und Neustart gesperrt. Nach Kampfende bleiben alle Attacken deaktiviert; „Neu starten“ erzeugt eine frische Session. Leere oder erschöpfte Slots sind nicht auswählbar. Fehlen auf einer Seite alle gültigen Attacken, meldet die Oberfläche dies und bietet den Testneustart an. Statusattacken verbrauchen PP und durchlaufen die Trefferprüfung, lösen aber weiterhin keine Effekte aus. Das Log hält maximal 80 Zeilen. Es gibt keine Rückübertragung auf Welt-Kreaturen, Belohnungen, Items, Wechsel, Fangmechanik oder zusätzliche Kampfregeln.

Für die Oberfläche kommen die Engine-Module UMG, Slate und SlateCore hinzu, keine externen Plugins. Die Platzhalter sind ausdrücklich Testgrafiken und ersetzen nicht die beschlossene visuelle Stilrichtung. Ein Widget-Blueprint wird für den Test nicht benötigt.

Seit der visuellen Überarbeitung vom 2026-09-25 verwendet die native UMG-Oberfläche drei eigene Texturen aus `/Game/Battle/Textures`: eine handgemalte Naturkulisse (`T_BattleGlen`) und zwei transparente Kreaturen-Platzhalter (`T_TestWater`, `T_TestGrass`). Die verkleinerten Quelldateien liegen unter `Content/Battle/Source`; nur die importierten Texturen werden zur Laufzeit geladen. Die Kulisse wird als 1280 × 720 Pixel große UI-Fläche gezeichnet, die Sprites sind auf maximal 768 Pixel begrenzt. Es entstehen keine zusätzlichen Welt-Actors, Lichter, Materialien oder Tick-Effekte.

Die eigene Kreatur steht groß im linken Vordergrund, der Gegner kleiner und höher im rechten Hintergrund. Naturstein, Bach, Brücke und Vegetation schaffen Tiefe innerhalb der Battle-Kulisse; Weltkamera und `Dev_TestMap` bleiben unabhängig. Ruhige HP-Tafeln und ein dunkles unteres Bedienfeld trennen die Daten von der Illustration. Attackenname, Typkennzeichnung und PP erhalten eigene Textfelder; Typfarben sind gedämpft. Der HP-Balken wechselt bei niedrigeren HP von Grün über Ocker zu Rot. Das kompakte Log bleibt scrollbar und die bestehende Widget-Bindung samt Buttonnamen bleibt erhalten. Diese Darstellung ist eine erste spielbare Präsentation, keine Entscheidung über finale Kreaturendesigns oder den Übergang von Welt zu Kampf.

Seit der ersten Kampfinszenierung vom 2026-09-25 übersetzt `UPokeMonsterBattlePresentationPlan` die bereits abgeschlossene `FPokeMonsterBattleResult`-Eventliste in eine Folge tatsächlich ausgeführter Aktionen. `MoveChosen` allein erzeugt keine Aktion; ein wegen K.O. unterbliebener Zug erscheint daher nicht. Jede Aktion trägt Angreifer, Ziel, Kategorie, PP danach, Treffer/Miss/Immunität, gegebenenfalls Schaden, HP vorher/nachher und K.O./Kampfende. Die Umwandlung verändert weder Session noch Kreaturen.

Das Widget hält während der Darstellung zunächst die bisher sichtbaren HP, PP und Logzeilen zurück. Pro Aktion zeigt es Angreifer-Impuls, eine UMG-Stoßspur (Physical), einen Energiepunkt (Special) oder einen schwachen Schimmer (Status), danach nur bei tatsächlichem Treffer eine Zielreaktion. Bei Schaden sinkt der HP-Balken weich auf den im Event enthaltenen Endwert; Text folgt der dargestellten Aktion. Miss und Immunität zeigen eigene Meldungen ohne Trefferreaktion oder HP-Verlust. K.O. senkt die betroffene Kreatur ab und blendet sie aus. Aktionen laufen in der von der BattleSession gelieferten Reihenfolge; nach dem letzten Schritt wird die Eingabe freigegeben oder bleibt bei Kampfende gesperrt. Ein 30-Hz-Timer läuft nur während dieser kurzen Inszenierung. `OnBattlePresentationStep` stellt Phasen für spätere Blueprint-VFX, Kreaturenanimationen und Sound bereit. Die Zeiten und Platzhalter sind reine Testwerte.

`PokeMonster.Battle.UI.BindingAndInputLock`, `PokeMonster.Battle.UI.UnavailableMoves` und `PokeMonster.Battle.UI.MissedStatusLog` prüfen Datenanbindung, Eingabesicherung, PP/HP/Log, Status- und Miss-Meldungen, K.O./Ende, Neustart sowie fehlende Daten und nicht verfügbare Attacken. `PokeMonster.Battle.Presentation.EventSequence` prüft die Übersetzung geordneter BattleEvents einschließlich Miss, Immunität und K.O. Zum manuellen Test die Battle-Testmap öffnen und Play starten.

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
