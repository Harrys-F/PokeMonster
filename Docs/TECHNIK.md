# Technisches Konzept – PokeMonster

## Aktiver Projektpfad ab 19.10.2026

Der einzige aktive Entwicklungsordner ist `/Users/harry/Developer/PokeMonster`.
`PokeMonster.uproject`, `Art`, `Content`, `Source`, `Docs` und `Tools` liegen direkt darin.
Das bestehende Repository und seine Git-/LFS-Objekte wurden ohne neue Projektkopie
an diesen Pfad angehoben. `main` folgt dem bisherigen GitHub-Repository `origin/main`.
Der vollständige lokale Backup-Commit bleibt auf `backup/full-03492bd` und dem
Archiv-Ref erhalten; er gehört weiterhin nicht zur schlanken Remote-Historie.

Der alte schlanke Worktree ist bis zur ausdrücklichen Bereinigungsfreigabe erhalten,
aber kein aktiver Entwicklungsort. Historische Berichte behalten die damaligen
Pfadbezeichnungen; diese sind keine aktuelle Pfadanweisung. Keine neuen Projektkopien,
Versionsordner oder Maps ohne Freigabe; vor zusätzlichen Worktrees nachfragen.
Prüfprotokolle und Kontrollmedien bleiben lokal unter `Saved`, außerhalb von Git.

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

Die Prüfung führt keine Entwicklung aus, verbraucht keine Items und persistiert keine Prüfungsfortschritte. XP-Vergabe löst die Prüfung nicht automatisch aus. Die ID eines Entwicklungsitems aus dem Inventar kann als `UsedItemId` in den Prüfungskontext übergeben werden; tatsächlicher Spezieswechsel, Itemverbrauch und UI folgen später. Der erste Ladepfad prüft Level, XP, HP und PP ausdrücklich und lehnt unbekannte Versionen ab; Migrationsregeln für spätere Versionen sind noch nicht implementiert.

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

Die Berechnungsfunktionen verändern weder HP noch PP, Speziesdaten oder Progression. Die unten beschriebene Battle-Session verwendet sie für die Rundensteuerung und übernimmt PP-Verbrauch, Zugreihenfolge sowie HP-Anwendung. Historischer Prototypstand (durch die spätere Battle-/Fortschrittsentwicklung und die Kristall-Anbindung von V4 ersetzt): Damals fehlten STAB-Boni, kritische Treffer, zufällige Schadensstreuung, Statusveränderungen, Lernlogik, Trainer und Kampfanimationen. Eine erste separate Battle-Testoberfläche ist unten beschrieben. Das endgültige Balancing bleibt offen.

Testdaten unter `/Game/Data/Moves`: `DA_TestNormalPhysical` (Normal/Physical, Stärke 40, Genauigkeit 100, PP 35), `DA_TestFireSpecial` (Feuer/Special, Stärke 50, Genauigkeit 95, PP 25) und `DA_TestStatus` (Normal/Status, Stärke 0, Genauigkeit 100, PP 20). Alle haben Priorität 0. Tests unter `PokeMonster.Moves` und `PokeMonster.Battle` prüfen Laden/Asset-Manager, PP-Trennung und Verbrauch, Treffergrenzen, Schadensformel, alle 289 einfachen Typenpaarungen, Doppeltypen und Immunitäten.

### Battle-Session: 1-gegen-1 und Teams

`UPokeMonsterBattleSession` unter `Battle/PokeMonsterBattleSession.h/.cpp` ist ein eigenständiges, Blueprint-freundliches `UObject` ohne World-, Actor- oder Tick-Abhängigkeit. Es verwendet die bestehenden Attacken-, Typen- und Schadensfunktionen unverändert. `FPokeMonsterBattleState` hält bis zu sechs individuelle Teammitglieder und je Seite genau eine aktive Kreatur, deren Index, Phase, Rundenzähler und Gewinner. Die Phasen sind `Uninitialized`, `AwaitingChoices`, `AwaitingSwitch` und `Finished`.

`Initialize(SideA, SideB, RandomSeed)` bleibt der 1-gegen-1-Einstieg. `InitializeTeams(TeamA, TeamB, RandomSeed)` akzeptiert je ein bis sechs Mitglieder; das erste ist aktiv und muss kampffähig sein. Doppelte Instanz-IDs und ungültige Daten werden vor dem Start abgewiesen. Die Session hält eigene Kopien ihres Zustands und starke Referenzen auf alle verwendeten Spezies-/Attacken-Assets, damit deren weiche Instanzreferenzen zwischen Runden nicht durch Garbage Collection verloren gehen. Die übergebenen Kreaturen außerhalb der Session werden nicht automatisch verändert. Ein späterer Aufrufer kann die fertigen Teamzustände aus `GetState()` gezielt übernehmen; Speichern, Belohnungen und XP-Vergabe werden hier nicht ergänzt. Der Aufrufer muss die Session selbst über eine `UPROPERTY` oder eine andere starke Unreal-Referenz halten.

`ResolveRound(SlotA, SlotB)` erhält beide Auswahlen gemeinsam (Slotindizes 0–3). Die Session prüft zunächst beide Kreaturen, Attacken und PP sowie die Schadensberechenbarkeit. Ungültige Eingaben liefern einen strukturierten Fehler mit betroffener Seite. HP, PP, Phase, Rundenzähler und Zufallszustand bleiben dann vollständig unverändert; es entstehen keine Erfolgs-Events. Der Aufrufer kann anschließend korrigierte Auswahlen übergeben.

Für eine gültige Runde gilt:

1. Höhere Attackenpriorität beginnt; bei Gleichstand höhere berechnete Initiative (`Speed`). Bei vollständigem Gleichstand beginnt deterministisch Seite A.
2. Beide gültigen Auswahlen werden als Events ausgegeben. Ausgeführte Aktionen folgen anschließend in der tatsächlichen Zugreihenfolge.
3. Jeder tatsächlich ausgeführte Angriffsversuch verbraucht genau eine PP, auch bei Fehlschlag, Immunität oder einer Statusattacke ohne implementierten Effekt.
4. Ein eigener, mit dem Start-Seed initialisierter `FRandomStream` liefert Trefferwürfe von 0–99. Gleiche Ausgangsdaten, Seeds und Auswahlen ergeben denselben Ablauf; abgewiesene Runden verbrauchen keine Zufallswürfe.
5. Bei einem Treffer wird der vorhandene Schaden auf die verbleibenden Ziel-HP begrenzt und angewendet. Immunität verändert keine HP. Statusattacken durchlaufen PP-/Trefferprüfung, führen aber noch keine Effekte aus.
6. Bei null HP folgt ein K.O.-Event; die besiegte Kreatur führt ihre vorgemerkte Attacke nicht aus und verbraucht dafür weder PP noch einen Zufallswurf. `BattleEnded` und `Finished` folgen erst, wenn auf der besiegten Seite kein Teammitglied mehr kampffähig ist. Andernfalls wartet `AwaitingSwitch` auf Ersatz.
7. Ohne K.O. wartet die Session auf die nächsten beiden Auswahlen. Nach Kampfende werden weitere Runden ohne Änderung abgewiesen. Eine gestartete Session wird nicht durch erneutes Initialisieren überschrieben.

`FPokeMonsterBattleResult` enthält Erfolg, Fehlercode/Fehlerseite, Rundennummer, Gewinner und eine geordnete Eventliste. `FPokeMonsterBattleEvent` unterstützt `MoveChosen`, `MoveExecuted`, `Missed`, `Damage`, `SuperEffective`, `NotVeryEffective`, `Immune`, `KnockedOut`, `BattleEnded` sowie `SwitchChosen` und `SwitchedIn`. Events enthalten Seiten, Instanz-IDs, Attacken-ID, Slot und Kategorie; Wechselereignisse tragen den Teamindex. Passende Events ergänzen Trefferwurf, PP vorher/nachher, Typmultiplikator sowie tatsächlichen HP-Verlust und HP vorher/nachher. Nicht zutreffende HP-/PP-/Wurfwerte sind `-1`. Bei K.O. bezeichnet `Source` den Verursacher und `Target` die besiegte Kreatur; bei Kampfende ist `Source` der Gewinner. Neutrale Wirkung wird durch `Damage` mit Faktor 1 dargestellt. Immunität erzeugt keinen künstlichen Schadenseintrag; Status-Platzhalter bleiben anhand ihrer Kategorie erkennbar.

Die Session verwaltet keinen unbegrenzten Eventverlauf: Der Aufrufer erhält die Ergebnisse je Aufruf und kann sie später für UI/Animationen aufbewahren. Fehler umfassen insbesondere ungültige Slots/Teamindizes, fehlende Spezies/Attacken, ungültige Status-/PP-Daten, null PP, bereits besiegte Kreaturen, fehlende Initialisierung und einen bereits beendeten Kampf. Es gibt keine automatische Ersatzattacke bei aufgebrauchten PP und kein erzwungenes Ende für reine Status-/Immunitätsrunden; sie benötigen weitere sinnvolle Auswahlen. Es läuft keine automatische Endlosschleife. Items, Trainer, Fangmechanik und Statuszustände sind weiterhin nicht enthalten.

`ResolveTurn(ChoiceA, ChoiceB)` nimmt je Seite eine Attacke oder einen freiwilligen Wechsel an. Beide Entscheidungen werden geprüft, bevor HP, PP, Runde oder Zufall geändert werden. Wechsel werden vor den Attacken ausgeführt; die wechselnde Seite greift in dieser Runde nicht an, die andere darf die eingewechselte Kreatur angreifen. Zwei Wechsel verbrauchen ebenfalls eine Runde ohne Attacke. `ResolveRound(SlotA, SlotB)` bleibt als kompatibler Attacke-gegen-Attacke-Aufruf erhalten. Nach K.O. mit verbleibenden Teammitgliedern weist die Session weitere Angriffe ab, bis `ForceSwitch(Side, TeamIndex)` den besiegten aktiven Platz ersetzt hat. Ein Pflichtwechsel erhöht die Rundenzahl nicht. Die Teamlisten halten HP, PP und Level jedes Exemplars unabhängig; `SideA` und `SideB` sind Ansichten des jeweils aktiven Exemplars und werden nach jeder Runde in den zugehörigen Teamplatz zurückgeschrieben.

Tests unter `PokeMonster.Battle.Session` prüfen Priorität, Initiative und Gleichstand, Auswahl-/Eventreihenfolge, HP-/PP-Anwendung, Treffer und Fehlschläge, Typeneffektivität und Immunität, frühes K.O. auf beiden Seiten, mehrere aufeinanderfolgende Runden, Kampfende, atomare Fehlerbehandlung, Seed-Reproduzierbarkeit und Asset-Lebensdauer über Garbage Collection. Alle bisherigen Projekt-Tests bleiben Bestandteil der Gesamtsuite.

### Erste Battle-Testoberfläche

`/Game/Maps/Dev_BattleTestMap` ist eine separate Testmap mit eigenem `APokeMonsterBattleTestGameMode` und `APokeMonsterBattleTestController`. Sie verändert weder den globalen GameMode noch `Dev_TestMap` oder die bestehende Player-Kamera. Ein statischer CameraActor stellt den View bereit; ein Welt-Pawn wird für diesen reinen Oberflächentest nicht benötigt. Der Controller startet nun eine Team-Demo mit je zwei individuellen Testkreaturen; `StartDemo` und `InitializeBattle` bleiben als 1-gegen-1-Testpfade erhalten.

Die Klassen unter `UI` trennen drei Aufgaben:

- `UPokeMonsterBattlePresenter` hält eine eigene BattleSession, nimmt Attacken- oder Wechselwahl entgegen und wählt für den Gegner den ersten gültigen Slot mit verbleibenden PP. Nach Gegner-K.O. wechselt er automatisch auf den nächsten kampffähigen Platz; nach Spieler-K.O. verlangt er eine Auswahl. Er berechnet keinen Schaden selbst, sondern ruft ausschließlich die Session auf. Lesemodelle liefern Namen, Level, HP, Teams, vier Attacken mit Typ/PP sowie Status und Kampflog. Die vollständigen geordneten BattleEvents bleiben über `OnRoundResolved` verfügbar.
- `APokeMonsterBattleTestController` startet die Testbegegnung, erstellt das Widget, aktiviert Maus/UI-Eingabe und löst die gewählte Runde nach einer kurzen Auswahlpause von 0,22 Sekunden aus. Der Presenter sperrt weitere Eingaben sofort bei Auswahl und bis `FinishPresentation`. Doppelte Auflösung und vorzeitiges Entsperren werden abgewiesen. Das Widget ruft `FinishPresentation` erst nach der sichtbaren Eventfolge auf; ohne Widget oder bei einem Fehler erfolgt die Freigabe sofort.
- `UPokeMonsterBattleWidget` ist ein natives UMG-Widget mit skalierter Oberfläche, HP-Balken, vier Buttons, scrollendem Log und zwei eigenen transparenten Kreaturen-Platzhaltern. Die eigene Kreatur steht unten links, der Gegner oben rechts. Die Gestaltung kann durch eine Widget-Blueprint-Unterklasse mit den gleichnamigen Controls und den Ereignissen `OnBattleViewUpdated`, `OnBattleRoundResolved` und `OnBattlePresentationStep` ersetzt oder ergänzt werden; `WidgetClass` am Testcontroller ist dafür konfigurierbar.

Die ältere 1-gegen-1-Demo (`StartDemo`) verwendet `DA_TestWater` gegen `DA_TestGrass`, beide auf Level 20 mit anfänglich 52 beziehungsweise 50 HP. Die Battle-Testmap startet nun `StartTeamDemo`: je zwei individuelle Exemplare derselben vorhandenen Test-Spezies auf Level 20 und 18. Die vier Spielerslots enthalten `DA_TestNormalPhysical`, `DA_TestFireSpecial`, `DA_TestStatus` und erneut `DA_TestNormalPhysical`. Der vierte Slot besitzt eigene PP; für diesen Test ist kein viertes Attacken-Asset nötig. Gegnerauswahl und Seed sind für reproduzierbare Tests festgelegt. Diese Zusammenstellung ist keine Lern- oder endgültige Kampfregel.

Während der Auflösung sind Attacken, Wechsel und Neustart gesperrt. Nach Kampfende bleiben alle Attacken und Wechsel deaktiviert; „Neu starten“ erzeugt eine frische Team-Session. Leere oder erschöpfte Slots sind nicht auswählbar. Fehlen auf einer Seite alle gültigen Attacken, meldet die Oberfläche dies und bietet den Testneustart an. Statusattacken verbrauchen PP und durchlaufen die Trefferprüfung, lösen aber weiterhin keine Effekte aus. Das Log hält maximal 80 Zeilen. Es gibt keine Rückübertragung auf Welt-Kreaturen, Belohnungen, Items, Fangmechanik oder Statuszustände.

Für die Oberfläche kommen die Engine-Module UMG, Slate und SlateCore hinzu, keine externen Plugins. Die Platzhalter sind ausdrücklich Testgrafiken und ersetzen nicht die beschlossene visuelle Stilrichtung. Ein Widget-Blueprint wird für den Test nicht benötigt.

Seit der visuellen Überarbeitung vom 2026-09-25 verwendet die native UMG-Oberfläche drei eigene Texturen aus `/Game/Battle/Textures`: eine handgemalte Naturkulisse (`T_BattleGlen`) und zwei transparente Kreaturen-Platzhalter (`T_TestWater`, `T_TestGrass`). Die verkleinerten Quelldateien liegen unter `Content/Battle/Source`; nur die importierten Texturen werden zur Laufzeit geladen. Die Kulisse wird als 1280 × 720 Pixel große UI-Fläche gezeichnet, die Sprites sind auf maximal 768 Pixel begrenzt. Es entstehen keine zusätzlichen Welt-Actors, Lichter, Materialien oder Tick-Effekte.

Die eigene Kreatur steht groß im linken Vordergrund, der Gegner kleiner und höher im rechten Hintergrund. Naturstein, Bach, Brücke und Vegetation schaffen Tiefe innerhalb der Battle-Kulisse; Weltkamera und `Dev_TestMap` bleiben unabhängig. Ruhige HP-Tafeln und ein dunkles unteres Bedienfeld trennen die Daten von der Illustration. Attackenname, Typkennzeichnung und PP erhalten eigene Textfelder; Typfarben sind gedämpft. Der HP-Balken wechselt bei niedrigeren HP von Grün über Ocker zu Rot. Das kompakte Log bleibt scrollbar und die bestehende Widget-Bindung samt Buttonnamen bleibt erhalten. Diese Darstellung ist eine erste spielbare Präsentation, keine Entscheidung über finale Kreaturendesigns oder den Übergang von Welt zu Kampf.

Seit der ersten Kampfinszenierung vom 2026-09-25 übersetzt `UPokeMonsterBattlePresentationPlan` die bereits abgeschlossene `FPokeMonsterBattleResult`-Eventliste in eine Folge tatsächlich ausgeführter Aktionen. `MoveChosen` allein erzeugt keine Aktion; ein wegen K.O. unterbliebener Zug erscheint daher nicht. Jede Aktion trägt Angreifer, Ziel, Kategorie, PP danach, Treffer/Miss/Immunität, gegebenenfalls Schaden, HP vorher/nachher und K.O./Kampfende. Die Umwandlung verändert weder Session noch Kreaturen.

Teamwechsel erzeugen in derselben Eventfolge eine eigene `SwitchedIn`-Präsentationsaktion. Das Widget blendet die bisherige Kreatur kurz ab, aktualisiert Namen und HP des eingewechselten Teammitglieds und zeigt danach gegebenenfalls den gegnerischen Angriff. Nach Gegner-K.O. wird der automatische Ersatz als eigene kurze Folge vor der nächsten Eingabe dargestellt. Eine freiwillige Wechselwahl und die Team-Schaltflächen sind während jeder Präsentation gesperrt. Die Test-UI zeigt für den Spieler bis zu sechs Teamplätze mit aktivem, kampffähigem oder K.O.-Zustand und rechts die Gegnerplätze. Vorhandene Kreaturen-Platzhaltergrafiken werden zunächst weiterverwendet.

Das Widget hält während der Darstellung zunächst die bisher sichtbaren HP, PP und Logzeilen zurück. Pro Aktion zeigt es Angreifer-Impuls, eine UMG-Stoßspur (Physical), einen Energiepunkt (Special) oder einen schwachen Schimmer (Status), danach nur bei tatsächlichem Treffer eine Zielreaktion. Bei Schaden sinkt der HP-Balken weich auf den im Event enthaltenen Endwert; Text folgt der dargestellten Aktion. Miss und Immunität zeigen eigene Meldungen ohne Trefferreaktion oder HP-Verlust. K.O. senkt die betroffene Kreatur ab und blendet sie aus. Aktionen laufen in der von der BattleSession gelieferten Reihenfolge; nach dem letzten Schritt wird die Eingabe freigegeben oder bleibt bei Kampfende gesperrt. Ein 30-Hz-Timer läuft nur während dieser kurzen Inszenierung. `OnBattlePresentationStep` stellt Phasen für spätere Blueprint-VFX, Kreaturenanimationen und Sound bereit. Die Zeiten und Platzhalter sind reine Testwerte.

`PokeMonster.Battle.UI.BindingAndInputLock`, `PokeMonster.Battle.UI.UnavailableMoves` und `PokeMonster.Battle.UI.MissedStatusLog` prüfen Datenanbindung, Eingabesicherung, PP/HP/Log, Status- und Miss-Meldungen, K.O./Ende, Neustart sowie fehlende Daten und nicht verfügbare Attacken. `PokeMonster.Battle.Presentation.EventSequence` prüft die Übersetzung geordneter BattleEvents einschließlich Miss, Immunität und K.O. Zum manuellen Test die Battle-Testmap öffnen und Play starten.

`PokeMonster.Battle.Team.SwitchAndKO` prüft Teamgrößen, manuelle Wechsel als Zug, Erhalt von HP/PP, Pflichtwechsel, automatischen Gegnerersatz und Kampfende erst nach vollständigem Team-K.O. Die vorhandenen 1-gegen-1-Tests verwenden weiter `Initialize` beziehungsweise `StartDemo`.

### Overworld-Begegnungen

`Encounter/PokeMonsterEncounterSubsystem` ist die zentrale Koordination für Kämpfe aus einer geladenen Spielwelt. `FPokeMonsterEncounterStartData` enthält Begegnungs-ID, Art (`Test`, `Wild`, `Trainer`), optionales Spielerteam, Gegnerteam, Seed und Quell-Actor. `FPokeMonsterEncounterEndData` liefert ID, Art, Ergebnis (`Victory`, `Defeat`, `Captured`; `Fled` und `Cancelled` sind für spätere Regeln reserviert), beide individuellen Teams mit HP/PP und Rundenzahl zurück. Es gibt noch keine Fluchtaktion oder Trainer-KI; das getrennte Game-Instance-Inventar ist unten beschrieben.

Der einzelne `PokeMonsterBattleEncounterActor` in `Dev_TestMap` nutzt die bestehende `PokeMonsterInteractable`-Schnittstelle. Bei `E` oder `Enter` legt er nur für den ersten Test ein zweiköpfiges Team aus den vorhandenen Test-Spezies und -Attacken an. Das Spielerteam bleibt im Game-Instance-Subsystem über spätere Begegnungen derselben Spielsitzung erhalten und kann mit dem unten beschriebenen Dev-Slot gespeichert werden. Eine bereits besiegte Gruppe wird nicht stillschweigend geheilt. Weitere Begegnungen können stattdessen eigene Startdaten übergeben.

`StartEncounter` initialisiert die vorhandene Battle-Session über den Presenter, bevor es die Overworld sperrt. Während des Kampfs ignoriert der Character Bewegungs- und Interaktionsversuche, stoppt seine laufende Bewegung und die UMG-Oberfläche besitzt den UI-Fokus. Das Widget verwendet in der Overworld dieselbe Darstellung und Ereignisfolge wie in `Dev_BattleTestMap`, ohne deren Neustartknopf. Es löst die Auswahl zeitversetzt über den Presenter aus; die Map bleibt geladen, die Weltkamera und Welt-Actors bleiben erhalten. Nach der letzten sichtbaren Kampfaktion übernimmt das Subsystem `TeamA` als Spielerteam, entfernt das Overlay, aktiviert die Weltsteuerung und sendet `OnEncounterEnded` mit dem strukturierten Ergebnis. `Dev_BattleTestMap` und ihr eigener Controller bleiben ein unabhängiger technischer Testpfad.

`PokeMonster.Encounter.OverworldIntegration` prüft die Testdaten auch ohne PIE und in PIE zusätzlich echten Kampfstart, Eingabesperre, Team-IDs, Sieg/Niederlage, HP-/PP-Rückgabe und erneute Steuerbarkeit. Den vollständigen manuellen Ablauf in `Dev_TestMap` mit dem Testmarker, sichtbarer UI und Rückkehr ebenfalls in PIE prüfen.

### Datengetriebene Wildbegegnungen

`UPokeMonsterEncounterProfile` ist ein `UPrimaryDataAsset` unter `/Game/Data/Encounters` (Asset-Manager-Typ `EncounterProfile`). Ein Eintrag enthält eine weiche Speziesreferenz, Mindest-/Höchstlevel, ein positives Gewicht, bis zu vier Startattacken sowie optional Tageszeit, Gebiets-ID und eine erforderliche Bedingungs-ID. Diese einfachen `FName`-Kennungen sind noch keine fertige Uhr-, Regionen- oder Questlogik. Ein `FPokeMonsterEncounterContext` liefert die aktuellen Werte; nicht passende oder ungültige Einträge nehmen nicht an der Auswahl teil. Ein fest gesetzter `FRandomStream` wählt gewichtet Spezies und Level reproduzierbar aus. Das Ergebnis ist ein neues individuelles Exemplar mit eigenen HP, Erfahrung und Moveslot-PP; die Profildaten bleiben unverändert.

`UPokeMonsterEncounterSubsystem::PrepareWildEncounter` formt dieses Exemplar zu den vorhandenen `FPokeMonsterEncounterStartData` mit `Kind=Wild` und genau einem Gegner. `StartWildEncounter` ruft anschließend unverändert `StartEncounter` auf. `EPokeMonsterEncounterSource` unterscheidet sichtbare Kreatur, Zone, Script/Story und eine spätere Zufallsquelle; die Quellenkennung wird bis zum Endergebnis weitergereicht. BattleSession, Presenter, UMG-Overlay, Eingabesperre und HP-/PP-Rückgabe sind dieselben wie beim bisherigen Weltkampf. Der bisherige `PokeMonsterBattleEncounterActor` bleibt für seinen separaten Techniktest bestehen.

`DA_DevWild` enthält vorläufig `TestGrass` (Gewicht 3) und `TestFire` (Gewicht 1), jeweils Level 5–7 und vorhandene Testattacken. In `Dev_TestMap` startet `PokeMonsterVisibleWildCreatureActor` den Kampf bei kurzem Kontakt oder über die bestehende `E`-/`Enter`-Interaktion. Sein vorhandenes Paper2D-Busch-Sprite und die Beschriftung sind reine Platzhalter. Nach Sieg oder erfolgreichem Fang wird der Actor standardmäßig für diese Spielsitzung ausgeblendet und seine Kollision abgeschaltet; nach einer Niederlage bleibt er verwendbar. `PokeMonsterWildEncounterZone` ist eine kleine markierte Overlap-Fläche; sie löst mit festem Seed pro PIE-Sitzung höchstens einmal aus und erzeugt keine laufenden Zufallskämpfe. Beide Dev-Actors legen bei leerem Spielerteam einmalig das bereits vorhandene Testteam an; ein besiegtes Team wird dabei nicht geheilt. Für spätere reguläre Begegnungen wird das echte Team an denselben Startvertrag übergeben.

`PokeMonster.Encounter.WildProfileAndSources` prüft Profil-Laden, Gewichtung, Levelbereich, optionale Filter, neue Instanzdaten und die gemeinsame Datenübergabe beider Quellen. Die bestehenden Encounter- und Battle-Tests bleiben dafür unverändert.

### Fangprototyp

Jedes `UPokeMonsterCreatureSpeciesData` besitzt einen editierbaren `BaseCaptureRate` (1–255, vorläufiger Standard 120). `UPokeMonsterCaptureDeviceData` ist ein eigenes Primary Data Asset unter `/Game/Data/Capture`; `DA_TestCaptureDevice` liefert einen vorläufigen Bonus von 1,25. `DA_TestCaptureItem` verknüpft dieses bestehende Fanggerät mit dem allgemeinen Item- und Inventarsystem. `FPokeMonsterCaptureLibrary` berechnet die Fangchance aus verbleibenden/maximalen HP, Basiswert und Itembonus. Ein Roll von 0–9999 aus dem Seed der BattleSession entscheidet reproduzierbar; die Formel ist eine technische Testformel und keine endgültige Balancing-Regel.

Nur eine als Wildkampf initialisierte BattleSession akzeptiert die Spielerwahl `Capture`. Ein abgewiesener Versuch verändert weder Runde noch Zustand. Ein gültiger Versuch verbraucht den gesamten Spielerzug. Bei Erfolg erzeugt die Session `CaptureChosen`, `CaptureSucceeded` und `BattleEnded`, bewahrt das konkrete Wild-Exemplar samt ID, Level, HP und PP und beendet den Kampf mit `EndReason=Captured`, bevor der Gegner handelt. Bei Fehlschlag folgt auf `CaptureFailed` der normale gegnerische Angriff. Die übrigen Attacken-, Schaden-, Team- und K.O.-Regeln bleiben gleich.

Der Presenter zeigt die Aktion nur im Wildkampf mit mindestens einem passenden Inventargegenstand an. Bei einem bestätigten Versuch entfernt er vor der BattleSession-Auflösung genau ein Item; weist die Session den Versuch ab, stellt er das Item wieder her. Erfolg und Fehlschlag verbrauchen es gleichermaßen. Das bestehende UMG-Widget bietet dort `Fangen`, sperrt Eingaben während der Auflösung und zeigt eine kurze Flug-/Fangsequenz mit Erfolg- oder Fehlschlag-Feedback vor einem möglichen gegnerischen Zug. Das Encounter-Subsystem wandelt den Session-Ausgang in `Outcome=Captured` um und ergänzt die gefangene Instanz bei weniger als sechs Mitgliedern am Spielerteam. Bei vollem Team bleibt dieses unverändert; `CaptureTransfer=TeamFull` und `CapturedCreature` liefern eine strukturierte Übergabe an eine spätere Reserve/Storage, die noch nicht implementiert ist. Der sichtbare Wildactor wird nach Fang deaktiviert. `PokeMonster.Capture.WildBattleAndTeamTransfer` prüft Chancen, Seed, Wildbeschränkung, Zugablauf, Events, Teamübernahme und volles Team.

### Items und Sitzungsinventar

`Items/PokeMonsterItemData` definiert Items als `Item`-Primary-Data-Assets unter `/Game/Data/Items`. Gemeinsame Daten sind stabile interne ID, Name, Beschreibung, Kategorie (`Capture`, `Healing`, `Battle`, `Evolution`, `KeyItem`, `Misc`), optionales Icon, maximale Stückzahl je Stapel und Nutzbarkeit in Overworld/Kampf. Capture-Items referenzieren das bestehende `UPokeMonsterCaptureDeviceData` für den Fangbonus; Healing-Items besitzen einen einfachen HP-Betrag. Ein Entwicklungsitem verwendet seine stabile Item-ID im vorhandenen `FPokeMonsterEvolutionContext`.

`UPokeMonsterInventorySubsystem` lebt in der Game Instance und hält individuelle Stapel als weiche Item-Referenz plus Menge. `AddItem` verteilt Mengen auf begrenzte Stapel, `RemoveItem` prüft den Gesamtbestand vor jeder Änderung, und `GetQuantity`/`HasItem` arbeiten stapelübergreifend. `GetStacks` und `RestoreStacks` bilden die validierte Übergabe an das Save-System; das erste Overworld-Menü zeigt Bestand und Kategorien nur lesend an. Zum Test erhält jede neue Game Instance einmalig fünf `DA_TestCaptureItem`; ein erfolgreich geladener Spielstand ersetzt diesen Testbestand vollständig. Kämpfe füllen den Bestand nicht nach.

`UseHealingItem` kann außerhalb aktiver Encounter lebenden Kreaturen fehlende HP bis zum Maximum zurückgeben und verbraucht nur bei tatsächlicher Heilung ein Item. `UseHealingItemOnPartyMember` im EncounterSubsystem wendet dies auf das bestehende Spielerteam an, ohne ein Menü vorauszusetzen. K.O.-Wiederbelebung, Kampfheilung und Entwicklungsdurchführung sind nicht Teil dieses Schritts. `DA_TestHealingItem` und `DA_TestEvolutionItem` dienen vorerst den Daten- und Automatisierungstests.

### Trainerkampf-Prototyp

`UPokeMonsterTrainerProfile` ist ein eigenes `TrainerProfile`-Primary-Data-Asset unter `/Game/Data/Trainers`. Eine stabile interne ID identifiziert den Trainer unabhängig von Actor und Map; Anzeigename und Trainerklasse sind Präsentationsdaten. Ein bis sechs Teameinträge referenzieren Spezies, Level 1–100 und jeweils ein bis vier Startattacken. `BuildTeam` erzeugt für jeden Kampf neue individuelle Exemplare mit eigenen HP, PP und Instanz-IDs. Drei optionale Texte decken die Ansprache vor dem Kampf sowie Reaktionen nach Spieler-Sieg und -Niederlage ab. `DA_DevTrainer` verwendet ausschließlich bestehende Test-Spezies und -Attacken.

Der in `Dev_TestMap` platzierte `APokeMonsterTrainerNPC` nutzt die vorhandene Interaktionsschnittstelle. Auf `E`/`Enter` zeigt er den kurzen Dialogplatzhalter als Text in der Welt; währenddessen ist Overworld-Eingabe gesperrt. Danach startet `StartTrainerEncounter` über dasselbe EncounterSubsystem und Battle-Overlay wie die bisherigen Weltkämpfe. Der Trainer-Kampftyp übergibt `bAllowCapture=false` an die BattleSession; die Fangschaltfläche ist nicht verfügbar und ein direkt eingereichter Fangzug wird abgewiesen. Es gibt keine neue Schadens-, Team- oder UI-Kampfregel.

Das Game-Instance-Subsystem führt `DefeatedTrainerIds` für die laufende Spielsitzung. Nur ein Spieler-Sieg über einen Trainerkampf trägt die Trainer-ID ein; eine Niederlage lässt den Trainer erneut herausforderbar. Ein besiegter NPC zeigt danach einen anderen Text und startet keinen weiteren Kampf. Beim erneuten Laden der Map liest er den Zustand aus demselben Subsystem; ein Save/Load aktualisiert den sichtbaren Text auch in der bereits geöffneten Map. Team-HP und -PP folgen weiterhin dem vorhandenen Encounter-Endvertrag. Geld, Belohnungen, NPC-KI und Cutscenes bleiben offen.

### Save/Load – erster Dev-Slot

`Save/PokeMonsterSaveGame` ist ein versioniertes `USaveGame` (Schema 2), `UPokeMonsterSaveSubsystem` ein `UGameInstanceSubsystem`. Der einzige reguläre Slot heißt `PokeMonster_Dev`. `SaveCurrentGame`, `LoadGame`, `HasSaveGame` und `DeleteDevSave` sind Blueprint-aufrufbar; in PIE stehen zusätzlich die Konsolenbefehle `PMSave`, `PMLoad`, `PMHasSave`, `PMDeleteDevSave` und `PMDevSaveRoundTrip` am Player zur Verfügung. Der Round-Trip-Test verweigert das Überschreiben eines bereits vorhandenen Dev-Saves. Es gibt noch kein Save-Menü, allgemeines Autosave, Cloud-Sync oder weitere Spielstände; der unten beschriebene RestPoint kann auf Wunsch gezielt speichern. Der Slot liegt unter Unreals ignoriertem Verzeichnis `Saved/SaveGames` und gehört nicht in Git.

Der Snapshot speichert Teammitglieder mit Instanz-ID, Spezies-ID, Level, kumulativer XP, aktuellen HP sowie vier Attacken-IDs und aktuellen PP. Inventarstapel enthalten Item-ID und Menge. Besiegte Trainer-IDs und abgeschlossene Encounter-IDs halten den derzeit relevanten Weltzustand fest: der sichtbare Wildactor nach Sieg/Fang und die einmalig ausgelöste Testzone. Diese Flags verwenden konfigurierbare stabile Encounter-IDs. Schema 2 speichert außerdem den aktiven Checkpoint mit stabiler ID, Map-Paketpfad, Position und Rotation. Spezies-, Attacken- und Itemdefinitionen bleiben ausschließlich in den Primary Data Assets; berechnete Statuswerte und Max-PP werden beim Laden aus den Assets neu ermittelt.

Das Laden löst jede Primary Asset ID über den Asset Manager auf und prüft Typ, Existenz und Identität, bevor Runtime-Systeme geändert werden. Level/XP-Konsistenz, HP-Grenzen, Moveslots/PP, Teamgröße, doppelte Instanz-IDs, Stapelgrenzen, Checkpoint und Schema-Version werden ebenfalls geprüft. Fehlende oder ungültige Daten werden geloggt und der bisherige Runtime-Zustand bleibt erhalten. Version 1 wird ohne aktiven Checkpoint nach Schema 2 migriert; unbekannte ältere oder neuere Formate werden abgewiesen. Speichern und Laden sind während eines aktiven Encounter und der Niederlagenrückkehr gesperrt. Automatisierte Tests liegen unter `PokeMonster.Save` und `PokeMonster.Overworld.Checkpoint`; der PIE-Diagnosebefehl verändert Team, Inventar und Flags, speichert sie, leert den Zustand, lädt ihn und prüft HP, XP, PP, Bestände und Flags.

### Erste Overworld-UI

Der `PokeMonsterGameMode` verwendet für die normale Overworld den `APokeMonsterOverworldPlayerController`; die separate `Dev_BattleTestMap` behält ihren eigenen Controller. Der Overworld-Controller erzeugt ein UMG-Widget beim Spielstart und verwendet für die Testmap das vorhandene Entwicklungsteam. `FPokeMonsterOverworldViewBuilder` bildet Team und Inventarstapel aus den bestehenden Game-Instance-Subsystemen in ein reines Lesemodell ab. Das HUD zeigt bis zu sechs Mitglieder mit Name, Level, HP und K.O.-Status sowie eine Inventar-Schaltfläche und bei gültigem Ziel einen Interaktionshinweis. Das Menü enthält Team- und Inventaransichten; letztere zeigt Name, Kategorie und Menge, aber noch keine Item-Nutzung.

Die C++-Widgetklasse stellt einen ruhigen, grün-/pergamentfarbenen UMG-Fallback mit benannten Elementen und einem Blueprint-Hook für spätere Gestaltung bereit. Sie verwendet keine neuen Texturen oder externen Assets. `Tab` ist als Enhanced-Input-Aktion zum Öffnen belegt; im Menü wechseln `T` und `I` zwischen Team und Inventar, während `Tab`, `Esc` oder der Schließen-Button das Menü schließen. Während des Menüs sperrt der Controller mit der vorhandenen Player-Funktion Bewegung und Weltinteraktion und gibt UI-Fokus/Maus frei. Ein aktiver Encounter oder bereits gesperrte Overworld-Eingabe verhindert die Öffnung. Beim Kampfstart blendet das Encounter-Startsignal die Overworld-UI sofort aus; nach Kampfende erscheint sie mit aktualisierten HP/PP wieder. Das Battle-Widget, die BattleSession und die Kampfregeln bleiben unverändert. Eine kleine Timer-Aktualisierung hält HUD, Team und Inventar nach Encounter, Heilung oder Laden aktuell.

### NPCs und mehrseitige Dialoge

`Dialogue/PokeMonsterDialogueData` definiert geordnete Seiten als `Dialogue`-Primary-Data-Assets unter `/Game/Data/Dialogues`. Jede Seite enthält Sprechername, Text, optionales Portrait, eine optionale Bedingung und eine optionale Folgeaktion. Bedingungen lesen vorhandene World-Flag- oder Trainer-Sieg-IDs; die Seiten werden beim Gesprächsstart für den aktuellen Zustand ausgewählt. Ein Flag kann am Ende einer Seite gesetzt werden. Für spätere Story-/Questaktionen gibt es eine benannte `Custom`-Folgeaktion, die an den Quell-Actor gemeldet wird. Entscheidungen, Verzweigungen und Questketten sind noch nicht implementiert.

`UPokeMonsterDialogueSubsystem` hält genau ein laufendes Gespräch pro Game Instance. Es verwaltet Seitennavigation und sperrt über `SetOverworldInputLocked` die bestehende Bewegung und Weltinteraktion. Start ist bei aktivem Kampf oder bereits gesperrter Overworld ausgeschlossen. Abschließen der letzten Seite oder Schließen gibt die Steuerung frei. `APokeMonsterNPC` implementiert die vorhandene `PokeMonsterInteractable`-Schnittstelle, referenziert ein Dialog-Asset und besitzt eine optionale Paper2D-Sprite-Komponente; sein einfacher Textplatzhalter ist durch Sprite/Blueprint austauschbar. Auch andere Interaktions-Actors können künftig dasselbe Subsystem starten.

Der Overworld-Controller zeigt das eigene UMG-Dialogwidget mit Sprecher, Text, Seitenstand und Weiter-/Schließen-Buttons über dem HUD an und gibt ihm Tastatur-/Mausfokus. `Enter`, `E` oder Leertaste blättern weiter; `Esc` schließt. Das vorhandene Overworld-Menü bleibt währenddessen durch dieselbe Eingabesperre geschlossen. `Dev_TestMap` enthält den dreiseitigen Wanderer und die Archivarin mit zustandsabhängigem Text. Ihr Testflag `Dev_NPCMet` nutzt die bereits gespeicherten abgeschlossenen World-/Encounter-IDs; es ist keine neue Save-Version nötig. Der bestehende Trainer-NPC verwendet weiterhin seinen bisherigen kurzen Welt-Textplatzhalter, kann später aber als Quell-Actor an das allgemeine Dialog-Subsystem angeschlossen werden. Automatisierte Prüfungen liegen unter `PokeMonster.Dialogue`.

### Heil- und Speicherorte

`APokeMonsterRestPoint` unter `Interaction` ist ein wiederverwendbarer, Blueprint-fähiger Overworld-Actor mit der vorhandenen `PokeMonsterInteractable`-Schnittstelle. Sein Name, Einstiegstext, optionale Paper2D-Sprite-Darstellung und `bSaveAfterRest` sind pro platzierter Instanz konfigurierbar. Ohne Sprite zeigt der Testactor einen einfachen Stein-/Kristall-Platzhalter aus vorhandenen Projektmaterialien. In `Dev_TestMap` steht ein Heilschrein; dort ist automatisches Speichern standardmäßig ausgeschaltet, damit ein Testbesuch keinen bestehenden `PokeMonster_Dev`-Spielstand überschreibt.

Die Interaktion startet zunächst einen kurzen Dialog. `Weiter` führt die Heilung aus; `Esc` oder der Schließen-Button vor diesem Schritt brechen ohne Heilung ab. Das EncounterSubsystem heilt das persistente Spielerteam nur außerhalb eines Kampfs: Es prüft eine Kopie aller Mitglieder und übernimmt sie erst nach vollständig erfolgreicher Wiederherstellung. `FPokeMonsterCreatureInstance::RestoreFully` setzt auch K.O.-Mitglieder auf volle berechnete HP und füllt die PP aller belegten Moveslots auf. Instanz-IDs, Level, XP, Inventar und Welt-Flags bleiben erhalten. Bei leerem Team erscheint ein eigener Hinweis.

Wenn `bSaveAfterRest` aktiviert ist, ruft der Actor **nach** erfolgreicher Heilung das bestehende `UPokeMonsterSaveSubsystem::SaveCurrentGame` für den Dev-Slot auf. Das Ergebnis wird als zweite Dialogmeldung angezeigt. Ein Save-Fehler wird geloggt und ausdrücklich gemeldet; die Heilung bleibt bestehen. Ein allgemeines Autosave wird nicht eingeführt. `PokeMonster.Overworld.RestPoint.HealAndSave` prüft HP, PP, K.O.-Heilung, Save-Aufruf und -Fehler sowie den leeren Teamfall.

### Checkpoint und Rückkehr nach Niederlage

`UPokeMonsterCheckpointSubsystem` hält pro Spielsitzung einen optionalen aktiven Rückkehrort. Ein entsprechend konfigurierter RestPoint registriert ihn nach erfolgreicher Teamheilung und vor einem optionalen Speichern. Die stabile Checkpoint-ID, der Map-Paketpfad ohne PIE-Präfix sowie die freie Spielerposition und Blickrichtung werden im Save-Schema 2 abgelegt. Der Testschrein in `Dev_TestMap` aktiviert `Dev_TestRestPoint`, überschreibt aber weiterhin nicht automatisch den Dev-Spielstand.

Ein vollständiger Teamverlust wird am zentralen Encounter-Abschluss erkannt, unabhängig davon, ob ein Trainer- oder Wildkampf endete. Die Battle-UI wird entfernt, während die Overworld-Eingabe gesperrt bleibt. Ein kurzes UMG-Dunkeloverlay meldet die Ohnmacht; danach wird der Spieler zum Checkpoint versetzt, auch über einen Map-Wechsel hinweg. Ohne aktivierten Checkpoint dient der `PlayerStart` der aktuellen Map als sicherer Fallback; `Dev_TestMap` besitzt zusätzlich die festgelegte Position `(-1000, -1100, 100)` für den Fall eines fehlenden PlayerStart-Actors. Nach der Rückkehr heilt die bereits vorhandene Teamroutine HP und PP vollständig und die Overworld-Eingabe wird wieder freigegeben. Trainer- und World-Flags sowie individuelle Kreaturendaten abgesehen von HP/PP bleiben unverändert. Es gibt keine Geldstrafe, keinen Itemverlust und kein neues Kampfsystem. Der PIE-Konsolenbefehl `PMDevDefeatReturn` startet einen bewusst verlorenen, einzügigen Wild-Testkampf; nach Auswahl einer Attacke lässt sich der vollständige Rückkehrablauf reproduzierbar prüfen.

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

## Mini-Vertical-Slice in `Dev_TestMap`

Der abgegrenzte Testabschnitt nutzt die vorhandene Overworld und ihre Paper2D-Umgebung. Die Outliner-Ordner `MiniSlice/01_Start` bis `04_Ziel` ordnen Checkpoint, Hauptweg/Abzweigung, Trainerprüfung und Archivstein; flache Steinsprites markieren die optionale Abzweigung. Die bestehenden Begegnungs-, Dialog-, Kampf-, Fang-, Inventar-, HUD- und Save-Subsysteme bleiben die einzigen Träger des Spielzustands.

Der Archivstein ist ein kleiner wiederverwendbarer C++-Actor (`Story/PokeMonsterStoryGoal`). Er liest die stabile Trainer-ID `Slice_Liora` und das Welt-Flag `Slice_ArchiveSeal` aus dem EncounterSubsystem. Vor dem Trainersieg ist das Ziel gesperrt; nach dem Sieg bestätigt eine Dialogseite das Ziel und setzt über die vorhandene Dialog-Folgeaktion das Flag. Die visuelle Zielanzeige aktualisiert sich auch nach dem Laden eines Spielstands. NPC-Dialogseiten prüfen dasselbe Flag. Der Dev-Save speichert das Flag über die bereits vorhandenen World-IDs und den Trainerstatus über besiegte Trainer-IDs.

Für einen Testlauf: In `Dev_TestMap` am Schrein starten, den Wegweiser-NPC ansprechen, optional der sichtbaren Wildkreatur auf der Abzweigung begegnen, Liora besiegen, am Archivstein interagieren und anschließend die geänderten NPC-Texte prüfen. `PMSave` und `PMLoad` prüfen den persistierten Fortschritt. Diese Testhandlung legt keine endgültige Geschichte fest.

## Datengetriebene Questgrundlage

`Quest/PokeMonsterQuestData` ist ein `UPrimaryDataAsset` mit stabiler interner ID, Titel, Beschreibung, Typ, optionalen Voraussetzungen und Abschluss-Flag sowie geordneten Zielen. Unterstützte Zielarten sind NPC-Gespräch, Trainersieg, Welt-Flag, Fangereignis, Inventarbesitz und Ortsinteraktion. `PokeMonsterQuestSubsystem` hält Queststatus und erreichten Schritt. Trainer-IDs, Welt-Flags und Itembestände werden bei jeder Aktualisierung aus Encounter- und InventorySubsystem gelesen; sie werden nicht als zweite Quest-Wahrheit kopiert. Gespräche und Fangereignisse werden beim Eintreten gemeldet. Das Quest-HUD zeigt nur Titel und nächstes Ziel einer aktiven Hauptquest.

Die erste Definition `/Game/Data/Quests/DA_SliceArchiveQuest` beschreibt Wanderer → `Slice_Liora` → `Slice_ArchiveSeal`. Die zweite Seite des bestehenden Wanderer-Dialogs startet sie über `StartQuest`; nach Gesprächsende zählt das Dialog-Asset als erstes Ziel. Bestehende Sieg- und Archivsteinlogik bleiben für die beiden weiteren Ziele maßgeblich. Die Wild-Abzweigung ist kein Ziel. Dialogbedingungen `QuestActive` und `QuestCompleted` erlauben statusabhängige Seiten, während die vorhandenen WorldFlag-Bedingungen der Slice-NPCs weiter funktionieren. `Dev_TestMap` wird hierfür nicht verändert.

Das damalige SaveGame-Schema 3 (seit Kampfsystem V3 auf Version 4 erweitert) speichert Quest-ID, Status und Schritt sowie gemeldete Fangarten-IDs, aber keine Questdefinition. Beim Laden werden Quest-IDs gegen registrierte Quest-Assets validiert, bevor der Runtime-Zustand ersetzt wird. Versionen 1 und 2 bleiben lesbar: Aus `Slice_Liora` und `Slice_ArchiveSeal` wird bereits belegbarer Mini-Slice-Fortschritt rekonstruiert; ein bloßes früheres Wanderer-Gespräch ist in alten Saves nicht nachweisbar und wird nicht erfunden. Version 0 und künftige unbekannte Versionen werden abgewiesen.

## Heilhaus-Function-Gate

`/Game/Maps/Dev_HealingHouseTestMap` ist eine eigene funktionale Blockout-Map, nicht das endgültige Gebäudeasset. Außenbereich und Innenraum liegen auf derselben durchgehenden Boden-Collision; die 240 cm breite Türöffnung braucht weder Levelwechsel noch Türschwelle. Gebäudekörper, Dach, Türrahmen, Fenster, Innenraum und funktionale Actors sind getrennt im Outliner organisiert. `Tools/BuildHealingHouseTestMap.py` erzeugt ausschließlich die neue Map und verweigert das Überschreiben einer vorhandenen Map.

Die Hüterin ist ein konfigurierter `PokeMonsterRestPoint` mit vorhandener Archivarin-Spritegrafik. Sie nutzt den bestehenden Dialog, vollständige Teamheilung und PP-Wiederherstellung. `bActivateCheckpoint` setzt `Dev_HealingHouse` an der freien Spielerposition bei Benutzung, bevor `bSaveAfterRest` den bestehenden Dev-Slot speichert. Der Dialog kündigt das Speichern an; ein Save-Fehler macht die Heilung nicht rückgängig. Niederlagen verwenden unverändert das CheckpointSubsystem, einschließlich Rückkehr aus einer anderen Map. Welt-, Trainer- und Questzustände bleiben bei ihren bisherigen Besitzern. Die Heilhaus-Map führt keine neue Kampf- oder Storylogik ein.

`World/PokeMonsterBuildingCutaway` unterscheidet außen und innen an einer kleinen, nicht kollidierenden Türschwellen-Box (40 × 240 × 230 cm, Zentrum (-450, 0, 115) cm). Erst beim Passieren des 4-cm-Hysteresebandes startet der reversible 0,4-Sekunden-Fade der konfigurierten Dächer und kameraseitigen Fassaden. Ein stehender Player im Hystereseband behält den zuletzt erkannten Zustand. Direkte Innenraumspawns werden über die begrenzte Innenraumfläche korrekt initialisiert. Ein maskierter `DitherTemporalAA`-Materialpfad liest den Ausblendanteil aus Custom Primitive Data Index 0; im Endzustand verborgenes Rendering wird zusätzlich abgeschaltet. Beim Verlassen und Sitzungsende werden Sichtbarkeit und ursprüngliche Primitive-Daten wiederhergestellt. Boden, Rückwände, Einrichtung und sämtliche Kollisionen bleiben unverändert. Der Tresen blockiert Pawn-Collision, ignoriert jedoch Visibility-Traces, damit die bestehende kurze Interaktion die Hüterin erreicht. Kleine Dekorationen, Dach und Türrahmen haben keine Gameplay-Collision.

Der Prototype verwendet bestehende Materialien und Sprites. Sein bewusst einfacher Gebäudeblockout ist durch den Function-Gate-Auftrag freigegeben; die verbindliche gezeichnete Grafikrichtung bleibt das spätere Gestaltungsziel. Die vollständige visuelle Laufprüfung in PIE muss getrennt von den automatisierten Layout-/Subsystemtests ausgewiesen werden.

Prüfstand: 34 Automationstests erfolgreich, darunter drei Heilhaus-Tests für die gespeicherte Map, echte Kapsel-Sweeps in einer isolierten Physikwelt, Cutaway-Sichtbarkeitswechsel sowie Rast → Checkpoint → Save/Load → Niederlagenheilung mit Erhalt von Quest-, Welt- und Trainerzuständen. PIE wurde per lokaler Unreal-MCP-Verbindung mit dem normalen Außenstart gestartet; Player und Overworld-HUD sind sichtbar. Der vollständige Fußweg und die reale Hüter-Interaktion bleiben offen, weil die verfügbare UI-Fernsteuerung keine wirksamen Bewegungs-Eingaben liefert. Ein gesonderter Innenraumstart wurde von der automatischen Freigabeprüfung als Test-Teleport abgelehnt und nicht ausgeführt.

## Blender-Heilhaus V1

Blender ist für diesen Prototyp die modulare Architekturquelle: `Art/HealingHouse/Source/HealingHouse_V1.blend`. Die mitgelieferte Konzepttafel liegt unter `Art/HealingHouse/Review/Concept_HealingHouse.png`. V1 übernimmt Dachsilhouette, seitlichen offenen Vorbau, Fachwerk, hellen Putz, warme Fenster und Kamin als einfache Formen; Schindeln, Ornamentik und finales Interior Dressing sind ausdrücklich nicht enthalten. Der Innenraum bleibt eine einzige begehbare Ebene; die Referenz-Obergeschossräume sind noch nicht umgesetzt.

Blender verwendet Meter (`scale_length = 1`). Der Gebäudekörper misst 10,30 m Breite × 9,30 m Tiefe; einschließlich Dachüberstand und seitlichem Vorbau umfasst die Architektur 12,20 m × 9,90 m. Der First liegt bei 6,40 m, die Kaminabdeckung bei 7,02 m. Wände sind 30 cm dick; die ausgeschnittene Eingangspassage hat 2,40 m Breite und 2,30 m Höhe bei Bodenhöhe null. Tür und sechs Fenster sind mit angewandten Exact-Booleans echte Öffnungen. Der einfache, seitlich offene Vorbau ist kein zweiter Eingang oder Innenraum.

24 Architekturmodule enthalten insgesamt 1.124 Dreiecke. Alle Architektur-Origins liegen gemeinsam auf dem Gebäudeursprung; Rotation und Scale sind in die Geometrie eingearbeitet. `HH_Walls`, `HH_Floor`, `HH_Roof_Main`, `HH_Roof_Porch`, `HH_DoorFrame`, `HH_WindowFrames`, `HH_Chimney`, `HH_Timber` und `HH_Counter` werden durch separate kameraseitige Fassaden-, Giebel-, Glas-, Fundament- und Vorbauteile ergänzt. Die sieben Material-Slots heißen Plaster, Wood, Timber, Stone, Roof, Metal und Glass. Der 1,40-m-Maßstabsblock ist nur eine Blender-Prüfhilfe und wird nicht exportiert.

`Tools/Blender/BuildHealingHouseV1.py` erstellt eine getrennte Szene und schreibt ausschließlich diese Szene mit Abhängigkeiten. `FinalizeHealingHouseSource.py` speichert sie anschließend in einer separaten Hintergrundinstanz als normale Blender-Datei; die ursprüngliche Live-Szene mit Cube, Camera und Light wird nicht gelöscht. FBX-Export: ausgewählte Architekturmeshes, keine Kameras/Lichter/Animationen, Unit Scale, X Forward/Z Up, trianguliert. Unreal übernimmt X und Z und spiegelt die rechte Blender-Y-Achse ins linkshändige Weltkoordinatensystem. Die Quellgeometrie berücksichtigt dies bewusst. Der Export liegt unter `Art/HealingHouse/Exports/HealingHouse_V1.fbx`.

`Tools/ImportHealingHouseV1.py` importiert getrennte Static Meshes unter `/Game/Environment/HealingHouse/Meshes`, erstellt sieben einfache Materialien unter `Materials` und prüft die Grenzen jedes Moduls gegen Blender (Toleranz 3 mm). Import-Scale ist 1; Meter werden über FBX-Einheiten in Zentimeter umgesetzt. Automatische Konvex-Collision und ein kombinierter Haus-Mesh sind deaktiviert. Texturen werden nicht importiert. Geometrie- und Importprüfungen stehen unter `Art/HealingHouse/Review`.

Die Importmodule werden zuerst 12 m neben dem Original geprüft und danach als kontrollierter visueller Ersatz an dessen Ursprung gesetzt. Der ursprüngliche Blockout bleibt als unsichtbare, mit `HealingHouse_RetainedBlockout` markierte Referenz erhalten. Seine einfachen Boden-, Wand- und Tresenblocker sowie die Türöffnung bleiben die Gameplay-Collision; die neuen visuellen Meshes haben NoCollision. Hüterin, RestPoint, Checkpoint-ID, Dialoge und Save-Einstellungen bleiben identisch. Vorhandene Ruhe-/Reserve-/Versorgungseinrichtung bleibt stehen. Das bestehende `PokeMonsterBuildingCutaway` erhält zusätzlich die neuen Dächer und kameraseitigen Fassadenteile; seine C++-Logik bleibt unverändert. Spielerbewegung 210 cm/s, Kamera, Figurenanimationen und Figurenskalierung werden nicht angepasst.

Die bestehende Player-Darstellung wurde zusätzlich aus dem Idle-Flipbook vermessen: 150,59 cm Sprite-Flächenhöhe vor Skalierung, bei der unveränderten BeginPlay-Skalierung 0,36 etwa 54,21 cm. Dies ist die Höhe in der Sprite-Ebene, keine gemessene Körpergröße entlang Welt-Z. Der separate 1,40-m-Blender-Block ist eine Architektur-Prüfhilfe; es erfolgte keine Anpassung der Spielfigur. Die bereits vorhandene Hüterin bleibt ebenfalls unverändert.

V1-Prüfung am 02.10.2026: Mac-Development-Build erfolgreich; alle 34 Automationstests unter `PokeMonster` erfolgreich, einschließlich der erweiterten Heilhaus-Tests. Map Check: keine Fehler oder Warnungen. In der neu gestarteten Editor-Sitzung war diesmal ein echter PIE-Fußweg ohne Spawn-Override oder Teleport möglich: Außenstart → Eingang → freier Innenbereich → Hüterin → Heil-/Checkpoint-/Speicherbestätigung → Eingang → Außenbereich. Cutaway wurde beim Eintritt und wieder sichtbare Fassade beim Verlassen beobachtet. Gleichzeitige diagonale Tastendrücke waren mit der Fernbedienung nicht möglich; diagonale Freigängigkeit wurde durch die bestehenden Capsule-Sweep-Tests geprüft. Die PIE-Testgruppe hatte bereits volle HP; die Wiederherstellung reduzierter HP/PP wurde automatisiert geprüft. Details und vollständige Dateiliste stehen in `Docs/HEILHAUS_V1_PRUEFBERICHT.md`.

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
- spätere Migrationsregeln, Speicheroberfläche und Anzahl endgültiger Speicherstände
- konkrete Auflösungen und Bildraten der Grafikprofile
- Umfang der Unreal- und Blender-MCP-Automatisierung
- endgültige Ordnerstruktur innerhalb des Content-Ordners

## Scale Calibration von Player und Architektur

Die historische V1-Messung oben beschreibt den Ausgangsstand. Die Kalibrierung trennt Leinwand, Alpha-Körper, Render-Bounds und Gameplay-Collision. Der Player verwendet visuelle Component-Scale (0,66; 0,66; 1,086758), einen Sohlen-Pivot (128,488) und pro Frame normierte Pixels Per Unreal Unit (3,4 × Körperpixel / 438). Seine Paper2D-Fläche steht aufrecht (Yaw 45°, Roll 0°); die sichtbare Körperhöhe beträgt dadurch tatsächlich 140 cm in Welt-Z. Getrennte Breiten-/Höhenskalierung erhält die Bildschirmproportionen unter der unveränderten -55°-Kamera. Eine zur Kamera gekippte Fläche mit nur passender Bildschirmhöhe wäre für die Verdeckung durch echte 3D-Tresen geometrisch zu niedrig. Die Sprite-Komponente sitzt am Capsule-Fuß, die Capsule bleibt 96 cm hoch und 56 cm breit. Sie ist eine Navigations-/Kollisionshülle, keine Körpergrößenreferenz. Messung und Vergleich stehen in `SCALE_CALIBRATION.md`.

## Aktuelle feste Overworld-Kamera B (13.10.2026)

Harrys Übernahmeauftrag vom 13.10.2026 ersetzt Kamera A (2500 cm/−55°) durch Kamera B. `APokeMonsterPlayerCharacter` behält das vorhandene SpringArm-/CameraComponent-System: **2850 cm**, Pitch **−50°**, bestehender Yaw **−45°**, Roll **0°**, perspektivisch, FOV **35°**. Absolute SpringArm-Rotation sowie deaktivierte Controller-/Pawn- und Rotationsvererbung halten die Außenansicht unabhängig von Actorrotation und acht Blickrichtungen fest. `TargetOffset=(0,0,35)` cm bleibt unverändert.

Positions-Lag bleibt aktiv, mit **12** statt 6, maximal **45 cm** statt 180; Substepping **1/60 s**, kein Rotations-Lag. Kamerakollision bleibt deaktiviert, daher kein Verkürzen des Arms an Dach/Vegetation. Gebäude behalten ihre bestehenden per-building Cutaways. Die kameraabhängige Vegetationsfreistellung wird unabhängig davon auf die tatsächliche Sichtlinie umgestellt; ihre Umsetzung/Prüfung ist unten separat dokumentiert.

Bei 140 cm aufrechter Körperhöhe und 16:9 liegt die Projektion bei ungefähr 9 Prozent der Spielbildhöhe. Transparente Leinwand und Collisionhöhe dürfen nicht als Körpermaß dienen. Der Anteil hängt bei unverändertem horizontalem FOV vom Seitenverhältnis ab. Der vorhandene Blueprint-/Map-Audit findet keine Player-Blueprint-Overrides: `Dev_TestMap`, HealingHouse- und BuildingKit-Testmap verwenden den nativen Pawn über `PokeMonsterGameMode`, ohne platzierte Playerinstanzen. Die native Kameraübernahme benötigt keine Mapänderung; die davon abhängigen Kronenmaterialien werden für Kamera B separat angepasst.

`CalculateCameraRelativeMovement` verwendet bereits die horizontale Kamerabasis: Bildschirm oben entlang Camera Forward, rechts entlang Camera Right, Diagonalen normalisiert. Die vorhandene Innenkamera-/Endpunkt-/Steuerungsanbindung bleibt unverändert; keine Drehung der Eingaben mit der Figur. Raumfeste Innenkameras behalten ihre eigenen Abstände/Winkel sowie Relocation, Fade und Bewegungsbasis-Blend. Ältere Architekturberichte und deren 2500/6/180-Angaben beschreiben historische Außenwerte. Kamera-A-Prüfung historisch: `OVERWORLD_KAMERA_2026_10_09_PRUEFBERICHT.md`; aktuelle Kamera-B-Prüfung: `KAMERA_B_SICHTFREISTELLUNG_PRUEFBERICHT.md`.


## Heilhaus V2: aktuelle Proportionen

Die historischen Blockout-Abmessungen oben sind für `Dev_HealingHouseTestMap` durch den V2-Proportions-Pass ersetzt: Hauptkörper 9,00 m breit / 9,30 m tief, First 6,40 m, freie Passage 1,70 × 2,15 m. Die map-konfigurierte Türschwellen-Box ist 40 × 170 × 215 cm groß und liegt bei (-450, 0, 107,5) cm; die generischen C++-Defaults und die Übergangslogik bleiben unverändert. Maßgeblich sind die Map-Komponentenwerte. 0,4-s-Fade, 4-cm-Hysterese und CPD Index 0 bleiben bestehen.

Die neue Quelle wird gezielt mit `Tools/Blender/ApplyHealingHouseV2Proportions.py` aus dem vorherigen V2-Stand angepasst. Nach Sichtprüfung exportiert `ExportHealingHouseV2Proportions.py` das Haus und einzelne geänderte Module; `Tools/ImportHealingHouseV2Proportions.py` aktualisiert nur diese V2-Meshes und notwendige Map-Abmessungen. Alle Reimport-Quellen liegen unter `Art/HealingHouse/Exports/V2Modules`; die Unreal-Hierarchie bleibt gleich. Keine globale Haus-, Player- oder Kameraskalierung. Prüfbericht: `Docs/HEILHAUS_V2_PROPORTIONEN.md`.

## Heilhaus V3: aktuelle Front und editierbares Dressing

Für die Heilhaus-Testmap ersetzt V3 die oben dokumentierte V2-Türbreite: **150 × 215 cm** freie Passage, Türschwellen-Extent **(20, 75, 107,5) cm**, Weltzentrum **(-450, 0, 107,5) cm**. Die beiden Eingangswand-Blocker haben innere Y-Kanten bei ±75 cm; die 56-cm-Player-Capsule bleibt unverändert. 0,4-s-Fade, 4-cm-Hysterese und CPD Index 0 bleiben unverändert. Tür, geteiltes mittleres Fachwerk und Rundfenster liegen auf derselben Y=0-Achse. Gebäude 900 × 930 cm, nominaler First 640 cm, Player 140 cm, Kamera 2500 cm / FOV 35° und Bewegung 210 cm/s bleiben verbindlich.

Aktuelle Blender-Quelle: `Art/HealingHouse/Source/HealingHouse_V3.blend`, separate Front-Gate-Sicherung: `HealingHouse_V3_Front.blend`. Die V1-/V2-Quellen bleiben erhalten. Nach explizitem Speichern folgt ein lesender Wiederöffnungs-/Renderdurchlauf, danach der modulare FBX-Export. Die zwölf geänderten Architekturmodule aktualisieren vorhandene V2-Meshes; acht separate Props und neun Materialien liegen unter `/Game/Environment/HealingHouse/V3`. Kleine Deko-Actors verwenden Engine-Geometrie und vorhandene Prototype2D-Sprites; keine Änderungen dieser vorhandenen Assets.

Die fünf großen Blender-Möbel erhalten nach dem Import im vollständigen Editor je einen einfachen Convex-Kollisionskörper (`FinalizeHealingHouseV3Collision.py`). Der Interchange-Import hat den angeforderten automatischen Collision-Aufbau im Commandlet nicht übernommen; Capsule-Sweeps sichern das tatsächliche Blocking ab. Die isolierte Automation-Physikwelt bereitet importierte BodySetup-Daten vor dem Kopieren mit `CreatePhysicsMeshes` vor; dadurch ist die Prüfung auch nach frischem Null-RHI-Start unabhängig vom Editor-Cache. Kleine Dekoration bleibt `NoCollision`, große Möbel ignorieren `Visibility`, damit die bestehende kurze Interaktion die Hüterin erreicht. Originale Blockout-Möbel bleiben als ausgeblendete, nicht blockierende Rückfallobjekte erhalten.

PaperSprite-Deko wird vor `SetSprite` vorübergehend `Movable` gesetzt, die erfolgreiche Zuweisung geprüft und anschließend wieder `Static` gesetzt. Andernfalls kann `SetSprite` im Commandlet still abgewiesen werden. Bodenplatzierung verwendet die tatsächlichen Component-Bounds. Neue frontseitige Mesh-Dekoration verwendet maskierte `HouseCutaway`-Materialien mit CPD-Index 0 und wird in der vorhandenen Occluder-Liste registriert; keine Änderung der Schwellenlogik.

Die drei zusätzlichen warmen, schattenfreien Point Lights werden bewusst schwach eingesetzt: Eingang 2,8, Tresen 3,6, Ruhebereich 2,4 bei deaktiviertem inverse-square falloff. Bestehendes Tages-/Fülllicht bleibt erhalten. Die maßgebliche Sichtprüfung erfolgt in tatsächlichem PIE mit unveränderter Spielkamera; Blender-Renders sind ergänzende Quellprüfungen.

## Westland Building Kit V1

Die unabhängige Architekturquelle ist `Art/Architecture/Westland/Source/WestlandBuildingKit_V1.blend`. V3 wird nur als Referenz gelesen. Neue Meshdaten und Materialien sind keine verlinkten Blender-Bibliotheksdaten; die Unreal-Materialgraphen sind eigenständige Kopien der sieben V2/V3-Architekturmaterialien. Vorhandene Texturen dürfen dabei unverändert gemeinsam gelesen werden. HealingHouse-Quellen, Meshnamen und Referenzen bleiben erhalten.

Das Grundraster beträgt 1 m, Standard-Wandfelder sind 2 m breit und 3 m hoch bei 20 cm Dicke. Zusätzliche 1-m-Wände sowie 30-cm-Dach-Endstücke schließen das Raster ab. Modul-Origins liegen auf Fußpunkt/Bay-Anfang beziehungsweise First/Traufe, nicht auf dem Gebäudemittelpunkt. Blender verwendet +X nach innen, -Y entlang des Wandfelds und +Z nach oben; FBX überführt dies in Unreals +X/+Y/+Z. Scale und Rotation der Bibliotheksmeshes sind angewandt. Gebäudeinstanzen verwenden nur Positionen und 90°-/180°-Rotationen, keine globale Skalierung. Fachwerk sitzt bewusst 14 cm vor der Wandmittelebene, sodass es nicht in der 20-cm-Putzwand verschwindet.

V1 umfasst 25 Meshmodule. Dach und Halbgiebel verwenden zunächst eine standardisierte 6-m-Spannweite mit 2:3-Neigung; die Gebäudelänge ist durch wiederholte 1-m-Dachstreifen variabel. Andere Spannweiten benötigen künftig zusätzliche kompatible Varianten, nicht gestreckte Fenster oder Türen. Kit-Definition und exakte Cottage-Instanzen stehen in `WestlandBuildingKit_V1.json` und `Buildings/WL_Cottage_V1.json`.

Neue Unreal-Assets liegen unter `/Game/Environment/Architecture/Westland/Meshes/{Walls,Timber,Roof,Windows,Doors,Structural}` und `Materials`. Die Building-Komposition ist als editierbare Einzelactors im Map-Ordner `Westland/Buildings/Cottage` organisiert und durch den portablen JSON-Bauplan beschrieben; kein monolithischer Hausmesh und kein neuer Gameplay-Actor nötig.

Die eigene Testmap `/Game/Maps/Dev_BuildingKitTestMap` enthält ein privates 6×6-m-Rasterhaus (lichte Fläche ca. 5,8×5,8 m), First nominal 5 m, Tür 130×200 cm, drei Fenster, kleine Regenhaube und Kamin. Alle 148 sichtbaren Hausbestandteile verwenden Kitmodule, ohne nur für dieses Haus erzeugte Sondermeshes. Die separate Modulgalerie steht außerhalb des Eingangslaufwegs. Innen bleibt die Fläche absichtlich ohne Wohnungs-Dressing.

Wände, Böden und Schwelle enthalten benannte UCX-Boxkörper; die Türwand hat getrennte linke/rechte/lintel Körper und keinen Konvexkörper über der Passage. Der Legacy-FBX-Import im vollständigen Editor liest diese expliziten Bodies deterministisch. Im Python-Commandlet fehlt ihm die erforderliche Slate-Anwendung; deshalb wird dieser Import bewusst im vollständigen Editor ausgeführt. Dekorative Balken, Fenster, Dach und Galerie haben NoCollision. Der bisherige `PokeMonsterBuildingCutaway` wird unverändert konfiguriert: Türbox 40×130×200 cm bei (-300,0,100) cm, 4-cm-Hysterese, 0,4-s-Fade, bestehende maskierte CPD-0-Materialtechnik. Gameplay-Collision bleibt unabhängig vom Fade. Player 140 cm, Kamera 2500 cm/FOV 35°, Lag und Bewegung 210 cm/s bleiben unverändert.

## Westland Inn V1: additive Kit-Erweiterung (historischer Erst-Proof)

Die separate Quelle `Art/Architecture/Westland/Source/WestlandInn_V1.blend` liest die unveränderte Kit-V1-Quelle. Alle 25 bestehenden Modulgeometrien und Materialien bleiben unverändert; acht neue generische Varianten werden separat in `WestlandBuildingKit_InnExtensions_V1.json` definiert und unter `Exports/InnExtensions` exportiert. Der Gasthaus-Bauplan ist `Buildings/WL_Inn_V1.json`; er dokumentiert jede Instanz, Position, Rotation, Wiederverwendung und Raumreserve.

Das Gasthaus verwendet ein 8×8-m-Raster, Außenwandhülle ca. 8,2×8,2 m, lichte Fläche 7,8×7,8 m und nominalen First 5,667 m. Die Traufseite ist die Front, der First läuft quer zum Wohnhausfirst. Versetzte Tür 160×215 cm, neun Fenster, kleine 30 cm höher montierte vorhandene Regenhaube, rückwärtiger Kamin und einfache Theken-/Kaminreserven schaffen eine öffentliche Raumwirkung. Es werden keine vorhandenen Tür-/Fenstermodule gestreckt und keine Gebäude global skaliert.

Neue Varianten: öffentliche 2-m-Türwand, Rahmen, Türblatt und Schwelle für 160×215 cm; Halbgiebel und Giebelabschluss für 8-m-Spannweite; Dachstreifen für diese Spannweite in 1-m- und 30-cm-Längen. Neigung 2:3, Raster, Montageanker, Materialslots und UCX-Prinzip bleiben kompatibel. Die Türwand besitzt drei getrennte UCX-Körper, die Passage bleibt frei. Die 218 Instanzen verwenden 186 unveränderte Kitmodule (85,32 %) und 32 neue Varianten. 15 ursprüngliche Modularten werden direkt wiederverwendet. Zwei einfache Engine-Cubes markieren die Theke; keine weiteren Haus-Sondermeshes, neue Materialassets oder Gameplayklassen.

`Dev_BuildingKitTestMap` wird additiv erweitert: Wohnhaus, bestehende 25-teilige Galerie und PlayerStart bleiben erhalten, Gasthauszentrum (0,-1500,0) cm. Acht Varianten stehen zusätzlich in der Galerie. Das gemeinsame Testgelände ist vergrößert, einfache Wege verbinden beide Gebäude. Der generische Cutaway bleibt unverändert: Schwellenzentrum (-400,-1600,107,5) cm, Box 40×160×215 cm, 4-cm-Hysterese, 0,4-s-Fade. Beide Gebäude haben getrennte Cutaway-Actors. Camera 2500 cm/FOV 35°, Player 140 cm und 210 cm/s bleiben bestehen. Keine NPCs, Übernachtungs-/Handels-/Questlogik oder vollständige Gasthauseinrichtung.


> Dieser Abschnitt beschreibt die ursprüngliche quadratische Komposition. Der aktuelle Stand wird unten unter „Westland Inn: L-Grundriss, Innenkamera und Wiederverwendung“ beschrieben.

## Wohnhaus: optionaler Innenkamera-Proof

`APokeMonsterBuildingCutaway` bietet `bUseInteriorCamera` (Default false), Abstand, Pitch, lokalen Yaw-Offset zur Türschwelle und einen raumlokalen Zielpunkt. `WL_Cottage_Cutaway` aktiviert den Proof: 2000 cm, Pitch -50°, Yaw 0°, Zielhöhe 80 cm. Die View bleibt raumfest. Healing House blieb bei diesem ursprünglichen Proof unverändert; seine spätere optionale Erweiterung steht unter „Healing House: Expanded Interior Prototype“. Das Gasthaus nutzt denselben opt-in Innenmodus; Details unten.

`APokeMonsterPlayerCharacter::CalcCamera` berechnet zuerst die unveränderte SpringArm-/CameraComponent-Ansicht und mischt nur Position/Rotation mit der raumfesten Ansicht. Ein schwacher Gebäudeverweis verhindert Besitz-/Lebensdauerabhängigkeiten. `CutawayAmount` ist die gemeinsame einzige Übergangsquelle; Kamera-Smoothstep und Quaternion-Slerp ändern weder Fade-Dauer noch Hysterese. Der opt-in Cutaway tickt pro Frame. Nach Ausstieg oder Entfernung des Providers gilt wieder exakt die normale Kameraberechnung. FOV und alle SpringArm-/Lag-Parameter bleiben erhalten.

Die normale CameraComponent bleibt außerhalb die Bewegungsbasis. Bei aktivierter Innenkamera wird erst am vollständig erreichten Endpunkt auf die horizontale Raumkamera-Basis gewechselt; beim Verlassen erst nach vollständigem Rückschwenk zurück. Ein nachgelagerter Yaw-Blend mit 250 Grad/s vermeidet einen abrupten 45-Grad-Wechsel bei gehaltenem Input. Ein einziger gemerkter Endpunktzustand genügt auch bei Fade-Umkehr. Der Player tickt für diesen opt-in Modus beziehungsweise den auslaufenden Basis-Blend; außerhalb ist sein zusätzlicher Tick deaktiviert. Blickrichtung und Interaktion basieren auf dem letzten Weltbewegungsvektor, die vorhandenen acht Flipbooks werden relativ zur gerenderten Kamera ausgewählt. Eine reine Z-Drehung der Sprite-Ebene hält die Darstellung frontal lesbar. Sprite-Skalierung, Fußpivot und Flipbook-Assets bleiben unverändert. Beide Cottage-Seitenwände sowie die Rückwand bleiben sichtbar; die explizite Liste enthält nur Front-/Dachteile. `ConfigureCottageInteriorCamera.py` aktualisiert ausschließlich die Cottage-Occluder-/Kamera-Konfiguration; der JSON-Bauplan und die bestehenden Autorenwerkzeuge erhalten dieselben Zuordnungen. Kein Mesh-Reimport, keine Blender-Dateiänderung und keine andere Testmap.

Aktueller Folge-Prüfbericht: `Docs/WESTLAND_WOHNHAUS_INNENSTEUERUNG_PRUEFBERICHT.md`. Der erste Kamera-Prüfbericht bleibt als ausdrücklich historischer Zwischenstand erhalten.


## Westland Inn: L-Grundriss, Innenkamera und Wiederverwendung

Der vorherige quadratische Inn-Proof ist durch eine 6 × 8-m-Halle mit einem versetzten 2 × 6-m-Rückflügel ersetzt. Die eigene `WestlandInn_V1.blend` und `WL_Inn_V1.json` enthalten 221 Architekturinstanzen aus bereits vorhandenen Modulen und zwei unveränderte Engine-Cube-Typen als Thekenreserve. Keine neuen Architekturmeshes, FBX-Dateien oder Materialien. `RecomposeWestlandInnV1.py` aktualisiert die vorhandene Inn-Komposition, `ConfigureWestlandInnV1.py` konfiguriert ausschließlich deren Actors und den nötigen Eingangsweg. Der ursprüngliche `BuildWestlandInnV1.py` bleibt das historische Bootstrap-Werkzeug für die damaligen acht Modulvarianten; für den aktuellen Grundriss das Recompose-Werkzeug verwenden.

`InteriorRegions` in `APokeMonsterBuildingCutaway` beschreibt optional die Vereinigung mehrerer Boxen in den lokalen Zentimeterkoordinaten von `InteriorArea`. Die leere Liste bewahrt die bisherige Ein-Box-Auswertung. Beim Inn verhindern zwei Teilboxen eine Innenkamera in der offenen Außenecke. Die gesamte Raumhülle dient weiter als gemeinsamer Transform/Fokus; es gibt nur einen Provider, eine Türschwelle und einen Fade. Keine zusätzlichen Gameplay-Overlaps oder Collision.

Der Inn aktiviert die vorhandene Innenkamera: nach PIE-Vergleich von 2000 und 2200 cm gewählte 2200 cm / Pitch -50° / lokaler Yaw 0°, Fokus Welt (100,-1500,80) cm, FOV 35°. Die explizite Occluder-Liste umfasst beide Dächer, Front, obere Anschlussgiebel und die zugehörigen störenden Dach-/Frontdetails. Untere Seiten-/Rückwände einschließlich Flügel bleiben sichtbar. Türen-/Fensteröffnungen und Capsule-Collision stammen vollständig aus den unveränderten UCX-Assets. Eintritt/Austritt und schnelle Umkehr verwenden die bereits validierten 0,4-s-Übergänge, Endpunkt-Latches und den nachgelagerten 0,18-s-Bewegungsbasis-Blend. Keine neue Input- oder Playerimplementierung.

## Westland Village Core V1

`/Game/Maps/Dev_WestlandVillage` ist ein eigener Dorfkern. Die beiden bestehenden Entwicklungs-Testmaps und Healing House V3 bleiben unverändert. Der explizite Bauplan `Art/World/Westland/WestlandVillage_V1.json` enthält Welttransforms, Modulinstanzen, Türmaße, Wege und den vorbereiteten Heilhausplatz. `Tools/BuildWestlandVillageV1.py` erstellt ausschließlich diese Map; bei Wiederholung ersetzt es nur mit `WestlandVillageOwned` markierte Actors. Gemeinsame Kit-, Sprite- und Materialassets werden nicht überschrieben.

Vier Wohnhäuser variieren vorhandene 1-/2-m-Wandmodule und 6-/8-m-Dachspannweiten; das bestehende L-Gasthaus wird vollständig wiederverwendet. Alle fünf Gebäude nutzen getrennte `PokeMonsterBuildingCutaway`-Instanzen, gedrehte Türschwellen und explizite Dach-/Frontlisten. Seiten- und Rückwände bleiben erhalten. Wohnhäuser verwenden 2000 cm, das Gasthaus 2200 cm Innenabstand. Außen bleiben 2500 cm, FOV 35°, Pitch −55° und Yaw −45°; Endpunkt-Latch und vorhandener Bewegungsbasis-Blend werden unverändert übernommen. Dieser verwendet weiterhin 250 Grad/s (45 Grad in 0,18 s). Bei den gedrehten Dorfhäusern ist der Winkelunterschied kleiner; die entsprechend kürzere tatsächliche Blendzeit folgt derselben bestehenden Implementierung, keinem neuen Steuerungsmodus.

Das sanfte Gelände und die gekrümmten Wegbänder werden mit bereits verfügbarer nativer GeometryScript-Editor-API erzeugt. Das Gelände besitzt 9800 Dreiecke und aktivierte beidseitige Flächen-Collision (`Use Complex As Simple`); hausnahe Plateaus werden weich ins Gelände eingeblendet. Die fein unterteilten Wegbänder besitzen 14176 Dreiecke und haben auf ihren Map-Komponenten keine Collision. Ihre Höhe wird baryzentrisch aus den tatsächlichen Gelände-Dreiecken ermittelt und um 3 cm angehoben; Längsschritte von höchstens 25 cm und acht Querstreifen vermeiden durchscheinende Grasflächen an Krümmungen. Das eigene unbeleuchtete Wegmaterial `M_WV_Path` verwendet Weltposition für dezente Erdvariation und Band-UVs für weiche Ränder. Eine einfache feste Belichtung vermeidet Helligkeitspumpen; sie ist keine finale Dorfbeleuchtung.

Vorhandene Paper2D-Vegetation bleibt rein visuell; kleine separate Stammkörper bilden die Collision, ihre Hilfsgeometrie ist im Spiel verborgen. Es gibt keine unsichtbare äußere Dorfwand und kein neues Vegetations-Fade-System. `ValidateWestlandVillageV1.py` prüft gespeicherte Assetreferenzen, Materialslots, Modulmaße, Collision und alle Türschwellen. `TestWestlandVillageV1PIE.py` führt einen nachvollziehbaren Fußlauf über Enhanced Input aus und prüft die Kamera-/Steuerungsendpunkte. Seine Protokolle und Review-Aufnahmen liegen ausschließlich im ignorierten `Saved/WestlandVillage`.

## Healing House: Expanded Interior Prototype

### Verbindliche Building-Cutaway-Regel (geprüft am 2026-10-04)

Im vollständig erreichten Innenmodus werden grundsätzlich **Dach und kameraseitige Vorderwand** einschließlich ihrer verdeckenden Front-/Türbauteile ausgeblendet. **Beide Seitenwände und die Rückwand bleiben sichtbar.** Keine pauschale Seitenwand-Ausblendung. Weitere Wandteile dürfen nur nach Sichtprüfung aus der tatsächlich verwendeten Innenkamera als einzelne, explizite Occluder ergänzt werden, wenn sie den Player oder wichtige Innenraumbereiche störend verdecken. Die konkrete Ausnahme und ihre Begründung gehören in den jeweiligen Prüfbericht. Auch L-/T-/Flügelgrundrisse verwenden gebäudespezifische `OccludingActors`-Listen; keine automatische Regel nach Wandnamen oder eine globale Laufzeitänderung für alle Gebäude.

Für das bestehende Expanded Healing House wurden elf übernommene `CameraSide`-Einträge entfernt: Liste 118 → 107. Die ausgelagerten Seiten-/Rückwände waren bereits nicht Teil der Liste und bleiben samt Balken erhalten. Im ausgelagerten Raum sind ausschließlich zwei Frontwände, zwei Türpfosten, Türlintel und Türbalken Occluder; die übrigen 101 Referenzen sind vorhandene äußere Dach-/Frontbauteile und deren Anbauten/Deko, einschließlich weiterhin deaktivierter Altversionen. Der Raum hat bereits ein offenes Oberteil; ein neues Innenraumdach wurde nicht hinzugefügt. Nach dem Fußlauf entlang beider Seiten und der Rückwand aus **2600 cm / FOV 35° / Pitch −50° / lokalem Yaw 0°** ist kein zusätzlicher Seitenwand-Occluder erforderlich. Diese Prüfung verändert weder Außenhülle noch die Cutaway-Listen von Wohnhaus, Gasthaus oder Dorf.

`ConfigureHealingHouseExpandedCutaway.py` korrigiert ausschließlich die vorhandene Referenzliste. Das einmalige Autorenwerkzeug übernimmt dieselbe explizite Ausschlussliste für spätere Reproduktion; der bestehende Raum wird nicht erneut gebaut. Mapaudit und `TestHealingHouseExpandedCutawayPIE.py` sichern Front-Ausblendung, sichtbare Seiten-/Rückwände und unveränderte Kamera/Steuerung ab. Prüfbericht: `HEALING_HOUSE_EXPANDED_CUTAWAY_PRUEFBERICHT.md`.

### Bestehender Expanded-Interior-Aufbau

Der geprüfte Stand basiert auf `32bba08` (Westland Village Core V1). Nur `Dev_HealingHouseTestMap` aktiviert die neue, standardmäßig deaktivierte Option `bUseRelocatedInterior`. Wohnhaus, Gasthaus und Dorf verwenden weiterhin **In-place Interior**: die vorhandene raumfeste Kamera wird innerhalb der Außenhülle über denselben CutawayAmount eingemischt. **Relocated/Expanded Interior** ist eine alternative Gebäudekonfiguration, keine Vorgabe für alle Gebäude.

Für die ausgelagerte Variante ergänzt `APokeMonsterBuildingCutaway` zwei nicht kollidierende Komponenten: `RelocatedInteriorArea` und `RelocatedDoorThreshold`, dazu `RelocatedCameraTarget`. Beide Türpunkte müssen gleich ausgerichtet sein; das wird in BeginPlay geprüft. `MapDoorwayPosition` transformiert die tatsächliche Pawnposition aus dem lokalen Koordinatensystem der Quelltür in dasjenige der Zieltür. Seiten-, Boden- und Bewegungsoffsets bleiben erhalten. Es gibt weder Map-Wechsel noch Streaming oder einen zweiten äußeren Heilhaus-Actor.

Das Heilhaus außen bleibt 9,00 × 9,30 m mit nominalem First 6,40 m. Der zusätzliche Raum besitzt 12,00 m Breite entlang Y und 10,00 m Tiefe entlang X; nominal 120 m², gegenüber 83,7 m² Außenrahmen rund 43,4 % mehr Fläche. Wände sind 3 m hoch. Raumzentrum (20000,0,150) cm; Tür außen (-450,0,107,5), innen (19500,0,107,5) cm, beide inward +X. Der Ortsversatz beträgt 19950 cm. Beide Passagen bleiben 150 × 215 cm; Schwellenextent (20,75,107,5) cm und Hysterese 4 cm bleiben erhalten. Der innere Türwand-Kollisionsquerschnitt ist bewusst ebenfalls 30 cm dick, damit eine innen freie Position außen nicht im Pfosten landet.

Der ursprüngliche reversible Dach-/Front-Cutaway behält FadeDuration 0,4 s. Nur bei aktivierter Relocation kommt ein schwarzer CameraManager-Fade um den Mittelpunkt hinzu: Smoothstep-Maske für CutawayAmount 0,3–0,7, vollständig schwarz bei 0,5. Vor dem Ortswechsel wird mindestens ein vollständig maskierter Frame gerendert; der Wechsel selbst bleibt ebenfalls vollständig maskiert. Ohne die Frame-Haltezeiten umfasst das Maskenfenster 0,16 s. Die tatsächliche Dauer hängt zusätzlich von der Framerate ab. Position und Kamera wechseln gemeinsam unter der Maske; die Kamera fährt nicht sichtbar über die räumliche Trennung. Eingabe wird dabei nicht gesperrt oder gelöscht. Geschwindigkeit bleibt erhalten; nur die SpringArm-Lag-Historie wird am verdeckten Ortswechsel neu initialisiert, nicht dessen Konfiguration.

Eine Capsule-Sweep-Prüfung verhindert die Versetzung in einen blockierten Zielbereich. Bei Ablehnung wird die Maske entfernt und erst nach einer neuen Schwellenquerung erneut versucht. Checkpoint-/Load-Rückkehr in den entfernten Raum oder nach draußen wird als unabhängige Ortsänderung erkannt und nicht nochmals um den Türversatz verschoben. Die bestehenden Save-/Checkpoint-Strukturen speichern weiterhin Weltposition und Map; keine neue Save-Version oder doppelte Gameplaydaten.

Innenkamera nach Vergleich von 2200/2400/2600 cm: **2600 cm**, FOV 35°, Pitch −50°, lokaler Yaw 0°, fester Zielpunkt Welt (19940,0,80) cm. Das bewahrt mehr Platz für den Player am Eingang. Außen bleiben 2500 cm, FOV 35°, Pitch −55°, Yaw −45° und Lag 6/maximal 180 cm. Die vorhandene Endpunkt-Steuerung und ihr 250-Grad/s-Blend (45 Grad in 0,18 s) bleiben unverändert. Für die Sprite-Ausrichtung wird beim verdeckten räumlichen Wechsel direkt die tatsächlich gewählte Kameraseite verwendet. Playerhöhe 140 cm, Sprites/Pivots, Collision, 210 cm/s, acht Richtungen und Interaktionsreichweite 150 cm bleiben erhalten.

V3-Möbel, Hüterin, Behandlungsmaterial, beide unterschiedlich großen Betten, Regale, Teppich und Sitzecke werden als bestehende Actors versetzt, nicht neu modelliert. Zwei vorhandene Innenlichtquellen folgen dem Raum ohne neue Einstellungen. 42 neue Architekturinstanzen verwenden vorhandene Kit-/Heilhaus-Meshes und Engine-Cubes; keine neuen Mesh-, Material-, Sprite-, Blender- oder FBX-Assets. `BuildHealingHouseExpandedInterior.py` ist ein einmaliges Autorenwerkzeug mit Map-/Wiederholungswachen. `ValidateHealingHouseExpandedInterior.py` prüft den gespeicherten Stand; `TestHealingHouseExpandedPIE.py` bewegt den Player ausschließlich über Enhanced Input. Reviewbilder/Protokolle bleiben im ignorierten `Saved/HealingExpanded`.

Nachweise: `HEALING_HOUSE_EXPANDED_INTERIOR_PRUEFBERICHT.md`. Fußlauf mit zehn aufeinanderfolgenden vollständigen Ein-/Austrittsrunden, insgesamt 21 Ein- und 21 Austritten, Hüter-Interaktion sowie Wohnhaus-/Gasthaus-Regression bestanden. Alle 38 Automationstests erfolgreich; Map Check 0 Fehler/0 Warnungen. Die endgültige visuelle Freigabe bleibt Harrys Sichtprüfung.

## Healing House Expanded Interior: Art & Dressing V1

Der Art-Pass auf `78c5e35` verändert ausschließlich die Einrichtung und Material-/Lichtkomposition des vorhandenen Expanded-Raums in `Dev_HealingHouseTestMap`. Raum 12 × 10 m, Außenhülle, Türschwellen, Relocation, Übergangsmaske, Kamera, 0,4-s-Cutaway, 0,18-s-Steuerungsblend und Gameplay bleiben erhalten. Die frühere Angabe „keine neuen Kunstassets“ beschreibt weiterhin den technischen Erst-Prototyp; dieser Folgepass ergänzt eigene Assets. Harrys visuelle Freigabe steht aus.

Neue Quelle: `Art/HealingHouse/Source/HealingHouse_ExpandedArt_V1.blend`; 17 wiederverwendbare Props, separat gespeicherte und erneut geöffnete Quelle, geprüfte UVs/Geometrie, danach FBX unter `Exports/ExpandedArtV1`. Eigene Unreal-Meshes, Materialien und eine 512²-Oberflächentextur liegen unter `/Game/Environment/HealingHouse/ExpandedArtV1`. Bestehende V3-Liegen, Regale, Kräutertisch, Heilutensilien und Laternen werden als Map-Instanzen wiederverwendet; Originalquellen und gemeinsam verwendete Assetdateien werden nicht überschrieben.

Sechs Innenwandfelder erhalten Fensteröffnungen und innenseitige Rahmen. Ihre ursprünglichen Wand-Collision-Körper bleiben als verborgene Kopien erhalten; die neuen sichtbaren Fensterwände verwenden das persistente Profil `NoCollision`. Kleine Dekoration und Dielen sind ebenfalls `NoCollision`. Nur Kamin, Sitzmöbel, Tisch und rückwärtige Regale erhalten zusätzliche einfache Möbel-Collision; sie ignorieren den Interaktionskanal. Tresenaufbau nutzt die vorhandene Collision. Seine beiden sichtbaren Nutzungshöhen betragen 80/105 cm; Sitzhöhe ca. 45 cm, Tisch ca. 75 cm, Liegen weiterhin ca. 70 cm.

Die explizite Liste mit 107 Occludern und die ursprünglichen maskierten Frontmaterialien bleiben unverändert. Neue und wiederverwendete Seiten-/Rückwandgestaltung bleibt sichtbar; keine zusätzliche Wand-Ausnahme. Eigene opake Art-Materialien dürfen die vorhandenen Fade-Materialien nicht ersetzen. Der Innensockel ergänzt nur visuelle Steinflächen.

Vier kleine schattenlose Innenlichter ergänzen die zwei bestehenden Innenlichtquellen. Ein räumlich begrenztes, nicht ungebundenes PostProcessVolume wirkt ausschließlich im ausgelagerten Innenraum; keine Änderung an Kamera/FOV oder Außenbeleuchtung. Farbige Materialflächen erhalten dezente Oberflächenvariation, keine externen Downloads und keine neue Abhängigkeit. Der Prototyp bleibt in Detailgrad und malerischer Wirkung deutlich einfacher als die Referenz.

`DressHealingHouseExpandedArtV1.py` ist ein einmaliges Autorenwerkzeug mit Schutz gegen Wiederholung; Import, Blender-Review/Export und die lesenden Audits sind getrennt. `ValidateHealingHouseExpandedInterior.py` prüft auch die legitime unterschiedliche Innenseite der Fensterbays und verlangt aufrechte Wandrotationen. `TestHealingHouseExpandedArtV1PIE.py` führt ausschließlich Enhanced-Input-Fußbewegung aus; die normale Spiel-Relocation ist kein Test-Teleport. Prüfbericht und Dateiliste: `HEALING_HOUSE_EXPANDED_ART_V1_PRUEFBERICHT.md`. Reviewbilder und Testzustände bleiben unter ignoriertem `Saved/HealingArt`.

### Healing House Art Quality V2 / Westland Natural Ground V1 (Oberflächen/Formen teilweise durch V3 ersetzt)

Der Qualitäts-Pass auf `0d656cf` behält das Art-V1-Layout und alle technischen Systeme bei. Er ersetzt in dieser Testmap die bisherigen einfachen Oberflächenzuweisungen und drei fehlerhafte Regalpositionen. Originalquellen und gemeinsam genutzte Assets bleiben unverändert. Eigene Varianten liegen unter `/Game/Environment/HealingHouse/QualityV2`; sechs selbst erzeugte gemalte Farbtexturen bedienen Holz, Stein, Putz, Stoff sowie Westland-Gras/Erde. Laufzeitauflösung maximal 1024, Mips/Streaming und keine zusätzlichen Mikro-PBR-Maps. Kleine Form-/UV-Anpassungen betreffen nur eigene Möbel-/Bodenvarianten; Liegen erhalten eine nicht kollidierende, leicht gefaltete Decke.

Wiederverwendbare Bodenmittel liegen unter `/Game/Environment/Westland/NaturalGroundV1`. Welt-XY-Texturierung liefert dieselbe Gras-/Erdprobe auf Grundfläche, organischem Wegband und Vorplatz. Der Weg verwendet UV 0–1 für die Querblendmaske, aufwärts gerichtete Dreiecke und einen opaken Gras-/Erdblend. `CourtCenter_cm` und `CourtHalfSize_cm` machen den Vorplatzblend an andere Flächen anpassbar. Die sechs Gras-/Kräuter-/Steinmodule sind separat exportiert; ihre Instanzverteilung steht im cm-/Seed-JSON. Die Steinmodule teilen das eigene V2-Steinmaterial und benötigen diese Content-Abhängigkeit beim Übernehmen.

Sechs native HISM-Komponenten halten 321 Instanzen ohne neue Gameplayklasse, Ticklogik oder Player-Collision. Opake zweiseitige Blattgeometrie ohne dynamische Schatten, Culling 3200–4300 cm; insgesamt 28608 instanzierte Detaildreiecke plus 1152 Wegdreiecke. Mehrere Materialsektionen sind weiterhin mehrere Render-Batches. Diese Werte ersetzen keine Performanceprüfung in einem großen Dorf. Tür-/Wegmitte bleiben frei, dichte Gruppen liegen an Rändern und wenig betretenen Flächen.

Die vorhandenen lokalen Art-Lichter und der räumlich begrenzte Innen-Postprocess werden moderat abgestimmt; Kameras und Außenlicht bleiben erhalten. Beide Seiten-/Rückwände und dieselben 107 Occluder bleiben unverändert. Regale werden mit ihrem Bestand verschoben und gegen Architektur-Bounds sowie im Fußlauf geprüft. Gameplay-Collision-Profile und alle anderen Maps bleiben bytegleich.

Blenderquelle `Art/HealingHouse/Source/HealingHouse_QualityV2.blend` wurde gespeichert, erneut geöffnet und vor FBX-Export visuell geprüft. Import, einmaliges Dressing, Materialverfeinerung, lesender Audit und Enhanced-Input-Fußtest sind getrennte Werkzeuge. Materialgraphen unter UE 5.8.2 müssen die tatsächlichen Pin-Namen verwenden; Sample-UVs, Desaturation-Eingang und beide Custom-Blend-Eingänge werden nach Wiederöffnung geprüft. Vollständiger Fußlauf, Healing/PP/Checkpoint/Save, Map Check und alle 38 Automationstests bestanden. Originaler Dev-Spielstand nach Tests bytegleich wiederhergestellt. Prüfbericht: `HEALING_HOUSE_ART_QUALITY_V2_PRUEFBERICHT.md`; lokale Nachweise ausschließlich unter ignoriertem `Saved/HealingQualityV2`. Harrys visuelle Freigabe steht aus.

### Healing House Art Quality V3 / Reference Polish

Der Pass auf `26428cf` erweitert ausschließlich die visuelle Heilhaus-Testszene. `HealingHouse_QualityV3.blend` enthält 34 wiederverwendbare Formvarianten: zusammenhängender 80/105-cm-Empfang mit durchgehendem Unterbau und Rahmen, geformte Möbel, sieben botanische Familien, Fensterkästen/Schmiedehaken, Guardian-Schild und gezielte Dach-/Fassadenvarianten. Die bisherigen Quellen, Daten und gemeinsam genutzten Gebäudeassets bleiben erhalten. Schindelreihen sind zusammenhängende, flach überlappende Geometrie mit gemaltem Terrakotta-Albedo; keine einzeln tickenden Schindeln. V2-Holz/Stein/Putz/Stoff sowie vorhandene Buch-/Gefäß-/Fenster-/Symbolmittel werden wiederverwendet. Einzige neue Bitmap ist die selbst erzeugte Terrakottatextur mit maximal 1024 Laufzeitauflösung, Mips und Streaming.

Zehn vorhandene kollidierende Möbelactors behalten exakt ihre ursprüngliche Mesh-/Collision-Komponente als unsichtbaren Blocker; eigene NoCollision-Darstellungsactors liegen auf derselben Transformation. Dies vermeidet eine Änderung des Laufgefühls durch dekorative Profile. Alle übrigen neuen Möbel-/Pflanzen-/Fassadenmeshes sind rein visuell. Kleine Pflanzen blockieren weder Player noch Interaktion. Die vorhandenen 107 Cutaway-Referenzen bleiben erhalten; zehn zusätzliche kameraseitige Fensterkasten-/Pflanzenactors folgen demselben Fade. Keine neue Ausblendung einer Seiten-/Rückwand, keine neue Cutaway-Logik.

Die vier vorhandenen Westland-Bodenmaterialien erhalten einen gemeinsam dokumentierten Shader `Art/HealingHouse/QualityV3/GroundBlend.hlsl`: drei gemischte Grasproben bei 190/271/413 cm und zwei Erdproben bei 220/337 cm, jeweils versetzt bzw. gedreht, plus zurückhaltende großräumige Farbvariation. Ursache der V2-Wiederholung war eine einzige identische Welt-XY-Probe je Oberflächentyp. Weg-/Vorplatzmasken und deren Parameter bleiben kompatibel. Höchstens fünf Farbtexturproben, keine weitere Bodenbitmap, kein teures mehrlagiges Noise-/PBR-System. Die 321 HISM-Details, sechs Modularten, ihre räumlichen Gruppen und 3200–4300-cm-Culling bleiben erhalten. Nicht das gesamte Gras flächig mit Geometrie bedecken. `Dev_WestlandVillage` wurde nicht bearbeitet; diese Materialpfade werden im derzeitigen Mapbestand nur von `Dev_HealingHouseTestMap` verwendet. Vor einer Übernahme ins Dorf bleibt eine gesonderte Sicht-/Performanceprüfung nötig.

Lokale Innenlichter verwenden räumlich begrenzten physikalischen Abfall: Kamin als einzige zusätzliche schattenwerfende lokale Lichtquelle, warme Laterneninseln und sechs schwache gerichtete Fensterlichter. Der bounded Innen-Postprocess wird zurückhaltend abgestimmt. Kameras, Raum, Übergänge, Relocation, Player, Heilerin und sämtliche Gameplay-Systeme bleiben unverändert. Neue Materialien werden aus echter PIE-Kamera farblich beurteilt, da die Außenbeleuchtung helle botanische Albedos sonst ausbleicht. Keine globale Außenlicht-/Kameraänderung.

Quellen öffnen/auditieren und visuell prüfen, danach erst FBX exportieren. Import, einmaliges Dressing, Materialkorrektur, lesender Audit und Fußtest sind getrennte Werkzeuge. Reviewbilder und Laufzeit-/Testnachweise bleiben unter ignoriertem `Saved/HealingQualityV3`. Der vollständige Prüfbericht `HEALING_HOUSE_ART_QUALITY_V3_PRUEFBERICHT.md` dokumentiert Ergebnis und verbleibende Referenzunterschiede. Harrys visuelle Prüfung bleibt ausdrücklich offen.

Die bestehende Möbelprüfung erkennt zusätzlich die Trennung in unveränderten Kollisionsproxy und sichtbare Quality-V3-Darstellung. Sie fordert eine sichtbare Ersatzdarstellung mit identischer Transformation, ohne zweite Collision, sowie einen weiterhin aktivierten Player-Blocker. Nur der Automationstest wird dafür erweitert; kein Gameplay-C++ wird geändert.

V3-Abschlussprüfung: vollständiger Enhanced-Input-Fußlauf ohne Test-Teleports, gerade/diagonale Türpassage, sämtliche Funktionszonen und Heilerin einschließlich Healing/PP/Checkpoint/Save bestanden. Build der erweiterten Automationstestdatei erfolgreich; 38/38 Automationstests, Map Check 0 Fehler/0 Warnungen sowie Import-/Material-/Collisionaudit bestanden. Originaler Dev-Spielstand nach allen Tests bytegleich wiederhergestellt. Keine visuelle Nutzerfreigabe vorweggenommen.

## Westland Asset Library V1 – isolierte Prüfbibliothek (10.10.2026)

Quelle: `Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V1.blend`, 46 separate Meshes aus 24 Grundtypen. Meter in Blender, Zentimeter in Unreal, Boden-Pivots und getrennte UCX-Kollision; Vegetation ohne Kollision, Bäume mit Stammkollision. Unreal-Ziel ausschließlich `/Game/Environment/WestlandAssetLibrary`, Reviewmap `/Game/Maps/Dev_WestlandAssetLibrary`. Die gesicherte Region bleibt unverändert.

Zwei einfache Opaque-Materialmaster mit jeweils einem Farbtextur-Sample; Blattmaster zweiseitig, keine Alpha-Masken. Holz-/Steintexturen aus Healing House werden unverändert referenziert. UV0 ist bewusst überlagertes Material-Tiling; Unreal generiert getrennt UV1. Drei LODs bei Meshes über 1000 Dreiecken, Distanzfelder deaktiviert. Unterwuchs wird in der Reviewmap über HISM instanziert, ohne Schatten und Kollision, mit 65–90-m-Culling. Diese Reviewwerte sind keine pauschale Freigabe für eine dicht bepflanzte Region.

Die native Kamera 2500 cm / Pitch −55° / Yaw −45° / FOV 35°, Playerkörperhöhe 1,40 m und Bewegung 210 cm/s bleiben erhalten. PlayerStart verwendet Yaw 0°, damit die bestehende relative Spriteausrichtung korrekt bleibt. Offene Art- und Normalenprobleme sowie Leistungsgrenzen siehe `Docs/WESTLAND_ASSET_LIBRARY_V1_PRUEFBERICHT.md`; keine finale Artfreigabe oder Regionsintegration.

### Westland Asset Library – Art Quality V2 (10.10.2026)

V1 bleibt in `Source/WestlandAssetLibrary_V1.blend` und Git-HEAD `0add5a5` erhalten. Neue Art-Quelle: `Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V2.blend`. Nur die 20 bisherigen A/B-Meshes von alter/junger Eiche, Birke, Obstbaum, Busch, Farn, Stumpf, Wurzel, Säule und Runenstein werden an ihren bestehenden Unreal-/FBX-Pfaden ersetzt. Keine weiteren Objekttypen oder Regionsintegration. Testmap unverändert im eigenen Namespace; lediglich V2-Tags und die Ausrichtung der beiden Runensteine zur Spielkamera werden angepasst.

Baum-/Buschkronen verwenden verzweigte Geometrie und einzelne gebogene Blätter ohne geschlossene primitive Kronenkerne. Vier gemalte Blattfamilien teilen den bisherigen opaken, zweiseitigen Ein-Sample-Master. Quellen 627×627 Pixel pro Blattfamilie, Mips/Streaming; keine Alpha-Masken oder zusätzliche Mikro-PBR-Maps. Rinde, Holz und Stein werden wiederverwendet. UV0 bleibt bewusst überlagertes Material-Tiling. Lightmap-UV-Generierung ist beim Import aktiviert; der MeshDescription-Audit liest einen Quell-UV-Kanal. Ein separat geprüfter Render-UV1-/Lightmap-Unwrap wird damit nicht zugesichert; die Testmap verwendet dynamische Beleuchtung.

V1-Warnungen entstanden durch ungültige Ecknormalen/Binormalen an triangulierten Blattspitzen sowie kollabierte UV-Dreiecke der Säulen. V2 verwendet eindeutige Blattspitzen, gültige Dreiecksflächen und planar gemappte separate Endkappen. Gespeicherte Quelle erneut öffnen, tatsächliche Corner-Normalen und Tangentenbasis nach Triangulierung prüfen, dann FBX mit Tangenten exportieren. Unreal importiert Normalen/Tangenten; reduzierte LODs berechnen diese mit MikkTSpace neu. MikkTSpace bleibt aktiviert. Der geprüfte Reimport einschließlich LOD-Build erzeugt keine Normalen-/Binormalenwarnungen.

Die 18 Revisionen über 1000 Dreiecken verwenden drei LODs mit ungefähr 100/60/30 Prozent Dreiecken und ScreenSize 1/0,4/0,15. Die beiden Wurzeln mit jeweils 228 Dreiecken bleiben bei einem LOD. Stamm-/Objekt-UCX und Vegetation ohne Kollision bleiben erhalten. Die 99 HISM-Unterwuchsinstanzen, Sichtweiten, Kamerawerte, Player und Gameplay bleiben unverändert. Zusätzliche Formkomplexität ersetzt keine Performanceprüfung; LOD0-Dreiecksbudget und aktive Materialsektionen separat betrachten.

Performanceaufnahmen müssen den tatsächlichen Viewport, Skalierungsstufe, 75-Prozent-Renderauflösung, Spawnpunkt und Vordergrund-/Hintergrunddrosselung berücksichtigen. Schatten-/Vegetationsabschaltung dient nur kurzzeitig der Kostendiagnose und wird zurückgenommen. CPU-/GPU-Zähler und Grenzen ihrer Messbarkeit im V2-Prüfbericht. `DumpDetailedPrimitives` ist auf dem geprüften macOS-/UE-5.8.2-Stand wegen eines nativen Renderthread-/Slate-Assertions kein zuverlässiges Diagnosewerkzeug. Nicht verfügbare Nullzähler werden nicht als null Draw Calls ausgegeben.

Technische Prüfung bedeutet keine finale visuelle Freigabe. Kronenform, Dichte, botanische Variation und Ruinenoberflächen werden mit den Spielkamera-Bildern im Bericht bewertet; Harrys Sichtprüfung bleibt offen. Vollständiger Bericht: `Docs/WESTLAND_ASSET_LIBRARY_ART_QUALITY_V2_PRUEFBERICHT.md`.


## Westland Asset Library: Art Quality V3 (11.10.2026)

V3 ergänzt genau eine alte Eiche und zwei Wildstrauchvarianten als getrennte Assets unter `/Game/Environment/WestlandAssetLibrary/QualityV3`. V1/V2-Quellen und gemeinsame Materialien bleiben erhalten; keine Migration der Region. Separate Blenderquelle `Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V3.blend`, individuelle FBX-Exporte und Manifest `ArtQualityV3.json`.

Die V3-Krone verwendet gekrümmte, gemalte Blattgruppenkarten statt großer einzelner V2-Blätter. Ein eigener RGBA-Atlas, vier Gruppen, ein Texture-Sample, Masked/TwoSided, Clip 0,45, Roughness 0,95 und Specular 0,05. PNG-Quelle 1254²; Unreal-Laufzeitgröße 2048² mit Mips und Alpha-Coverage. Rindenbild und Unreal-Rindeninstanz werden wiederverwendet. Diese neue Masked-Variante ersetzt die opake V2-Darstellung nicht global.

LOD0: 12068 / 3284 / 3396 Dreiecke; je zwei belegte Sektionen/Slots, drei LODs. Gültige UV0-, Corner-Normalen- und Tangenten-/Binormalenbasis wird nach erneutem Öffnen geprüft. Keine eindeutige gebackene Lightmap-UV1 zugesichert; die Prüfszene verwendet dynamisches Licht. Eiche: eigener geerdeter UCX-Stammkörper, 1,74 × 1,70 × 4,80 m; Sträucher ohne Collision.

Nur die Bibliotheks-Testmap erhält die additive Vergleichsgruppe und einen gekrümmten Weg. 67 vorhandene Unterwuchsinstanzen auf drei HISM-Komponenten, ohne Collision/Schatten, Culling 6000–8000 cm; neue große Vergleichsobjekte bis 10000 cm. Das eigene Wegband besitzt 1512 aufwärts gerichtete Dreiecke und explizite Normalen/Mikk-Tangenten, keine Collision/Schatten. Enge Kurven werden pro Dreieck auf konsistente Ausrichtung geprüft.

Performancevergleich tauscht nur drei Meshes in der PIE-Kopie am identischen, zu Fuß erreichten Standort. Beide Varianten temporär Movable, tatsächlicher Meshtausch und Materialreferenzen geprüft; danach ursprüngliche Meshes, Overrides, Sichtbarkeit, Schatten und Mobilität zurückgeben. Medium/75 %, 1280 × 740, gleiche Kamera, 10 s Warmup/30 s CSV. Opaque-/Schatten-/Sichtbarkeitsdiagnosen sind keine gespeicherten Qualitätseinstellungen.

Kamera 2500/−55/−45/35, Lag 12/max.45, Player 140 cm/210 cm/s, C++, Gameplay und andere Maps bleiben unverändert. Fußlauf und 38/38 bestehende Automationstests bestanden, Map Check 0/0. Dichte Eichenkrone kann die Figur aus nächster Nähe verdecken; keine Vegetations-Fade-Logik hinzugefügt. Keine finale Art-/Regionsfreigabe. Vollständige Maße, Bildnachweise, Kosten und Grenzen: `WESTLAND_ASSET_LIBRARY_ART_QUALITY_V3_PRUEFBERICHT.md`.


### Meshy-Player – Animation Quality V2 (12.10.2026)

Die von Harry beauftragte 3D-Playerdarstellung bleibt eine getrennte, kollisionsfreie `PokeMonsterMeshyVisualComponent` am vorhandenen PaperCharacter. Acht Weltblickrichtungen drehen ausschließlich das Mesh. Kamera, Capsule, 140-cm-Referenzkörper, 210 cm/s und Gameplay bleiben unverändert; vorhandene Paper2D-Flipbooks bleiben über `SetMeshyEnabled(false)` erreichbar.

V2 verwendet 25 Knochen, eigenes Mesh/Skelett und Idle (3 s)/Walk (0,55 s) unter `/Game/Characters/YoungTrainer/MeshyV2`; vorhandene V1-Materialien/Textures bleiben erhalten. `PokeMonsterMeshyAnimInstance` mischt die Clips über 0,18 s, hält die Laufphase am Stop und setzt die Rate aus tatsächlichem Tempo / 210 cm/s. Gedämpfte begrenzte Zubehörfedern reagieren auf Beschleunigung/Drehung und verändern ausschließlich Umhang-/Taschenbones. Keine Root Motion oder Stoffsimulation. Original und funktionierende V1-Blenderquelle bleiben unverändert. Prüfungen, Bildsequenzen und verbleibende Art-/Topologiegrenzen: `MESHY_PLAYER_ANIMATION_QUALITY_V2_PRUEFBERICHT.md`. Technisch geprüft, visuelle Freigabe ausstehend.

## Dev_TestMap_VisualV2: isolierte Gameplay-Referenzwelt (12.10.2026)

Die modernisierte Arbeitskarte liegt unter `/Game/Maps/Dev_TestMap_VisualV2`. Sie wurde über die Editor-SaveMap-/LoadLevel-API aus der vorhandenen `/Game/Maps/Dev_TestMap` erzeugt. Originalkarten und Projekt-Startmap bleiben erhalten. Der ursprüngliche 40 × 40-m-Gameplaykern behält seine Startpunkte, Dialoge, Begegnungen und Ziele an denselben Actor-Positionen; ein kompakter Dorf-/Waldrundweg erweitert die begehbare Umgebung. Neue Bodenunterlage 90 × 65 m; keine pauschale Vergrößerung auf 150 × 120 m.

Bei Erstellung am 12.10.2026 nutzte die Karte die vorhandene Meshy-V2-Darstellung: Player 140 cm, 210 cm/s, Capsule-Radius 28 cm/Halbhöhe 48 cm, damalige Außenkamera A 2500 cm/−55°/−45°/35°, Lag 12/max.45. Die Außenkamera ist seit 13.10.2026 durch Kamera B ersetzt. Paper2D-Fallback und Gameplay bleiben bestehen. Bestehende NPC-Grafiken erhalten ausschließlich lokale Größen-/Fußpunktkorrekturen in der Kopie; dies ist keine neue NPC-Architektur.

Das bestehende Quality-V3-Heilhaus einschließlich 12 × 10-m-Expanded-Interior, Heilerin und generischem Cutaway wird mit remappten Actor-Referenzen in die Kopie integriert. Innenraumübergang und 0,4-s-Cutaway verwenden dieselben Systeme. Die kopierte Heilerin registriert den eindeutigen Checkpoint `VisualV2_HealingHouse`. Kein Quelllevel wird zur Laufzeit mitgeladen; die ursprüngliche Heilhaus-Testmap wird nicht geändert.

Unterwuchs nutzt sieben statische HISM-Gruppen mit 459 Instanzen, ohne Collision/Schatten, Culling 4500–6500 cm. Kleine neue Pflanzen sind vom Distance-Field-/dynamischen Indirect-Lighting-Beitrag ausgenommen. Das Wohnhaus verwendet 148 vorhandene Kit-Module in 29 statischen HISM-Gruppen, Culling 6000–8500 cm. Instancing-fähige Materialkopien liegen ausschließlich unter `/Game/Environment/DevTestMapVisualV2/Materials`; gemeinsame Kit-Materialien werden nicht gespeichert oder umgestellt.

Fünf native, gekrümmte Wegbänder verwenden 5952 Dreiecke, berechnete Normalen/Tangenten und ein eigenes Material mit handgemalter Erde und räumlich geditherten, unregelmäßigen Wegkanten. Überlappende opake Grasränder verursachten Flecken an Kreuzungen; die neue Masked-Variante und um 0,15 cm gestaffelte Visualhöhen verhindern das Überdecken benachbarter Wege und Z-Fighting. Keine Weg-Collision, keine Wegschatten, keine zusätzlichen Texturimporte. Vorhandene V3-Eichen und Sträucher sowie NaturalGround- und Heilhaus-Materialfamilien werden wiederverwendet.

Historischer Erststand vom 12.10.2026 (durch die folgende Kamera-B-Anbindung ersetzt): Für neue V3-Eichen gab es eine begrenzte, kamerabezogene Masked-/Dither-Freistellung: Blattmaterial und eigene Rindenvariante öffnen einen weichen räumlichen Korridor zum Kamerafokus. Der reine Blatt-Fade verdeckte den Player weiterhin durch Äste; die geprüfte Variante bezieht deshalb obere Stamm-/Astflächen ein und erhält die Wurzelbasis. Keine zusätzlichen Actor-Ticks oder weltweiten Materialänderungen. Die Berechnung setzt die aktuelle feste Außenkamera voraus; sie ist kein allgemeines System für beliebige Kameras und kein zeitgesteuertes Ganzbaum-Fade. Birken und andere unveränderte Baumfamilien sind nicht automatisch abgedeckt.

Nachweise, Vergleichsmessungen, echte Spielkamera-Aufnahmen und verbleibende Art-/Performancegrenzen stehen in `DEV_TESTMAP_VISUAL_V2_PRUEFBERICHT.md`. Technische Prüfung ist keine finale menschliche Art-Freigabe.

## Kamera B: tatsächliche Sichtlinie und Kronen-Fade (13.10.2026)

`PokeMonsterCameraVisibilityComponent` ist eine rein visuelle Komponente am bestehenden Player. Sie verändert keine Bewegung, Animation, Collision, Interaktion oder Spielzustände. Ein einmaliger Materialscan registriert ausschließlich die vorhandenen eigenen Kronen-/Rinden-Reveal-Materialien, in VisualV2 41 Baumkomponenten. Andere Materialien und Gebäude werden nicht registriert. Keine Map wird für diese Anbindung gespeichert.

`MPC_PlayerSight` übergibt pro Frame tatsächliche Playerposition plus unveränderten 35-cm-Zieloffset und tatsächliche PlayerCameraManager-Position. Dadurch folgen Farbe und Schatten derselben Kamera-/Player-Sichtlinie, einschließlich Camera Lag und vorhandener Innenkamerawechsel. Keine fest eingebauten 2500-/2850-cm-Vektoren im Material. Weltbezogene Werte gelten pro World für den vorhandenen einzelnen lokalen Player; Split-Screen ist nicht vorbereitet.

Ein begrenzter perspektivischer Sichtkegel ersetzt den alten festen Kamerafokus-Korridor. Radius am Ziel: innen 55/außen 110 cm, zur Kamera proportional schmaler, räumlich mit Smoothstep weich. Gültiger Abschnitt 0,06–0,995 der Kamera→Player-Strecke, außerhalb volle Materialdeckkraft. Hinter dem Ziel werden keine Fragmente freigestellt. Eine konservative Bounds-Prüfung aktiviert je Baum einen reversiblen 0,25-s-Fade; der Shader beschränkt ihn anschließend pro Fragment auf den tatsächlichen Sichtkegel. Keine Ganzbaum-Sichtbarkeitsschaltung und kein größerer Weltkreis. Untere Wurzelbereiche bleiben geschützt.

Im Kamera-B-Erststand wurden nur die zwei bestehenden lokalen Reveal-Master angepasst; `MI_V2_BarkReveal` und importierte Originalmeshes/-texturen behalten ihre Pfade. Runtime-MIDs werden bei EndPlay auf die Originalzuweisungen zurückgegeben. Die zunächst fehlende Birkenfamilie wurde anschließend wie unten beschrieben angebunden. Weitere Familien werden nicht automatisch umgestellt. Das Autorenwerkzeug `ConfigurePlayerCameraBVisibility.py` muss nach einem erneuten Ausführen alter Einmal-Bauskripte angewendet werden.

Build erfolgreich; alle 40 Tests (39 bestehende plus Sichtlinien-/Fade-Test) erfolgreich. PIE-Aufnahmen prüfen Dorf, freien Weg, Wald, eine große Krone, überlappende Kronen, Vorwärts-/Rückwärts-/Diagonalbewegung. Player in den geprüften Aufnahmen sichtbar, in tiefem Schatten weiterhin dunkel. Temporales Dither ist kein echtes Alpha-Blending. Grenzen und der protokollierte PIE-Fenster-Absturz stehen in `KAMERA_B_SICHTFREISTELLUNG_PRUEFBERICHT.md`.

## Sichtfreistellung: vollständige Baumfamilien der VisualV2 (13.10.2026)

Der tatsächliche Szenenaudit findet zwei sichtbare Baumfamilien: 41 `SM_WLA_OakAncient_V3` und vier `SM_WLA_Birch_A`. Die erhaltenen alten Sprite-/Kegelbäume sind im Spiel unsichtbar und werden nicht aktiviert. Beide sichtbaren Familien sind nun abgedeckt: 45 Komponenten/98 Materialslots. Kamera B, Kegelform, tatsächliche Kamera-/Playerposition, 0,25-s-Fade und Wurzelschutz bleiben unverändert.

Vier Material Instances (`MI_V2_BirchReveal`, `MI_V2_LeafBirchReveal`, `MI_V2_LeafDarkReveal`, `MI_V2_LeafLightReveal`) verwenden den unveränderten `M_V2_BarkRevealBase`. Dieser bereits vorhandene gemalte Master bietet Paint/Tint/PBR-Parameter und denselben Sichtkegel. Die Birkenblätter bestehen aus opaker Blattgeometrie, benötigen also keinen zusätzlichen Atlas-Alpha-Master. Originaltexturen, Tint, Roughness/Metallic/Specular und zweiseitige Blattdarstellung werden übernommen. Keine neuen Master, keine Originalmaterial-, Mesh- oder Mapänderung. Das Werkzeug `ConfigureTreeFamilyReveal.py` erstellt diese Instances reproduzierbar.

Die vorhandene Komponente prüft nun explizit Meshfamilie **und** Material. Nur die freigegebenen Eichen-Reveal-Materialien bzw. vier originalen Birken-Materialzuweisungen können Runtime-MIDs erhalten. Gebäude bleiben auch bei gemeinsam genutzten Holz-/Blattmaterialien ausgeschlossen. EndPlay stellt bei Birken ebenfalls ihre ursprünglichen Materialzuweisungen wieder her. Andere Meshfamilien, nachträglich gespawnte Komponenten und Split-Screen bleiben außerhalb der geprüften Anbindung.

Build erfolgreich, 41/41 Automationstests erfolgreich einschließlich `TreeFamiliesAndBuildingExclusion`; Map Check 0 Fehler/0 Warnungen. Eingebettetes PIE prüft einzelne Birken, mehrere Eichen, gemischte Kronen, Zur-/Von-Kamera- und Diagonalbewegung, hintere Vegetation und ein verdeckendes Gebäude. Kein schwebendes PIE, kein neuer Absturz. Nachweise und verbleibende Lesbarkeits-/Dithergrenzen: `BAUMFAMILIEN_SICHTFREISTELLUNG_PRUEFBERICHT.md`.

## Meshy-NPC-Darstellung V1

In `Dev_TestMap_VisualV2` kann ein `APokeMonsterNPCVisualActor` ausschließlich die Darstellung eines bestehenden NPCs übernehmen. SourceActor, Interaktionskapsel, Name, Dialogdaten und Speicheridentität bleiben am Original-NPC. Die neue native AnimInstance blendet Idle/Gespräch in 0,18 s; sie führt keine NPC-Fortbewegung ein. `bUseVisual=false` stellt den erhaltenen PaperSprite wieder her. Der erste geprüfte Einsatz ist der Wanderer mit Ranger-Mesh. Materialien verwenden einen gemeinsamen neuen Parent mit expliziter Skeletal-Mesh-Nutzung. Weitere Modelle gelten nur entsprechend ihrem Prüfstatus in `MESHY_NPC_INTEGRATION_V1_PRUEFBERICHT.md`, nicht automatisch als freigegeben.
## Verbindlicher Grafik-Performance-Teststandard (15.10.2026)

Bei Grafik-, Vegetations-, Material-, Beleuchtungs- und Performanceänderungen sind beide Ausgabegrößen zu prüfen:

| Ausgabe | Scalability | Screen Percentage |
|---|---|---|
| 1280 × 740 | Medium | 75 % und 100 % |
| 2560 × 1440 (QHD) | Medium und High | jeweils 75 % und 100 % |

Je Konfiguration Dorf, dichter Wald und offener Weg: mindestens drei Messläufe mit festgehaltenen Kameraposen, gleichen NPC-/Szenenzuständen, definierter Aufwärmphase und Messdauer. Vorher/Nachher zeitlich verschachteln und die Reihenfolge wechseln, um Zeitdrift zu erkennen. Median-FPS, Median-Framezeit, P95-Framezeit und zuverlässig verfügbare GPU-/CPU-Zeiten je Lauf protokollieren. Überlappende GPU-Pässe nicht addieren; fehlende oder konstante Nullzähler als nicht auswertbar kennzeichnen.

Tatsächliche Fenstergröße, Spiel-Viewport und Render-Target-Größe sowie Screen Percentage und interne Rendergröße gesondert überprüfen. Ein `r.SetRes`-Aufruf oder Editorfenstertitel allein ist kein Auflösungsnachweis. Aus dem konstanten Renderer-Treiber abgeleitete interne Bildgrößen ausdrücklich von direkt gemessenen Renderpass-/Pufferabmessungen unterscheiden. Dynamische Auflösung, VSync, FPS-Limit, Vordergrunddrosselung, Warm-up, Messfenster, Gerät und zeitliche/thermische Schwankungen festhalten. PIE und eigenständige Prozesse getrennt ausweisen; `-game` mit Editorbinary ist kein paketierter Shipping-Build.

Vergleichsscreenshots auch in tatsächlichen 2560 × 1440 bei gleicher Kamera, Position, Beleuchtung und Qualität erzeugen. Nicht verfügbare Auflösungen oder unzuverlässige Messungen offen benennen. Vorher/Nachher ausschließlich unter gleichen Bedingungen vergleichen. Richtwerte: stabile 60 FPS bei Standard/Medium und QHD/Medium, zunächst mindestens 30 FPS bei QHD/High, langfristig 60 FPS. Dies sind keine Garantien; sichtbare Qualität geht vor aggressiven Einsparungen. Dauerhafte globale Grafikabsenkungen erst nach messbarem und visuell akzeptablem Vergleich.


## VisualV2 Quality V2: Außen-Motion-Blur aus (17.10.2026)

In der zentralen `/Game/Maps/Dev_TestMap_VisualV2` setzt ausschließlich das vorhandene ungebundene `V2_OutdoorExposure`-Volume den MotionBlurAmount-Override auf 0. Das höher priorisierte, begrenzte `V2_House_HH_Art_InteriorLighting`-Volume überschreibt denselben Parameter ausdrücklich mit dem bisherigen Wert 0,5; andernfalls würde es die neue Außen-Abschaltung erben. Priority, Blend-Radius und sämtliche anderen PP-Felder bleiben unverändert. Keine globale Deaktivierung über r.MotionBlurQuality oder Projektkonfiguration.

Der vollständige Szenen-/PP-Textvergleich bestätigt genau drei Feldänderungen bei 1348 Actors: Außen-Override an, Außen-Amount 0, Innen-Override an. Bloom, VSM-/Lumen-Parameter, Beleuchtung, Vegetation, Kamera, Player und Gameplay unverändert. Keine Übernahme anderer EnvironmentPerfV1-Maßnahmen. Geprüft mit vier echten Fußläufen einschließlich Sprint, Dialog, Kampf/Fang, Heilhaus, Save/Load sowie 108 regulären GPU-Profilsegmenten in PIE/Standalone bei 1280×720 und QHD; für diesen Auftrag gilt ausdrücklich 720 statt des historischen 740-Pixel-Standards. Kein neuer kausaler FPS-Gewinn gegenüber historischen Reihen behauptet. Bericht: `VISUALV2_QUALITY_V2_PRUEFBERICHT.md`.


## VisualV2 TAA Integration V1 (18.10.2026)

Die Spielansicht von `/Game/Maps/Dev_TestMap_VisualV2` verwendet TAA mit Originalschatten. Ein einziges map-eigenes `UPokeMonsterTemporalAABlendable` am vorhandenen ungebundenen `V2_OutdoorExposure` wählt über die Engine-Schnittstelle `IBlendableInterface` ausschließlich die AA-Methode und deren passenden Screen-Percentage-Modus. Kein zusätzlicher Postprocess-Materialpass, kein Actor-Tick und keine globale Renderer-Konfigurationsänderung. Andere bestehende Maps bleiben beim bisherigen Standard. Normale Editoransichten, Scene Captures und deaktivierte AA-Diagnostik werden nicht umgestellt.

UE 5.8 besitzt hierfür kein Feld im `PostProcessSettings`-Struct. Deshalb bleibt der globale `r.AntiAliasingMethod`-Wert 4; der tatsächlich gerenderte Spielview verwendet Methode 2. Eine CVar-Abfrage allein ist kein Integrationsnachweis. Der vorhandene Development-Probe protokolliert nun die tatsächliche View-Methode unabhängig aus dem Renderthread. Temporäre TSR-Gegenproben setzen nur das Gewicht dieses Blendables auf 0 und restaurieren anschließend die ursprünglichen Einstellungen.

Lichtquellen, Lumen, Bloom, Exposure, Originalschatten, Vegetation, Kamera B, Player und Gameplay bleiben unverändert. Außen-MotionBlur 0 und Innenwert 0,5 bleiben bestehen. Keine neue Map. Speicherung und erneutes Öffnen gegen vollständige erfasste Szenen-/PP-Signatur geprüft: genau ein zusätzlicher AA-Eintrag bei unveränderten übrigen 1348 Actors.

49/49 Automationstests, drei Map Checks ohne Fehler/Warnungen und drei vollständige Enhanced-Input-Fußläufe bestanden. Tatsächliche Ausgabe-/Treibergrößen bei 1280×720 Medium sowie QHD Medium/High, jeweils 75/100 %, in PIE und eigenständigem Development-Prozess geprüft. TAA bei 75 % etwas weicher; feine Vegetation und bestehendes temporales Dither bleiben nicht vollständig ruhig. QHD/High/100 im geprüften nativen Wald: TSR 17,23 FPS/56,10 ms GPU, integriertes TAA 23,86 FPS/39,88 ms GPU. Kurze interleavte Messfenster, keine Dauer-FPS-Garantie und kein Shipping-Test. Bekannte native Engine-Toolset-Startfehler sind zur Vorher-Baseline identisch und im Bericht getrennt aufgeführt. Bericht: `VISUALV2_TAA_INTEGRATION_V1_PRUEFBERICHT.md`.


## VisualV2 World Art Quality V1: lokaler Heilhausbereich (19.10.2026, örtlich durch V2 ersetzt)

Im V1-Stand verwendet die zentrale Map im begrenzten Heilhaus-Vorplatz und Wegsaum fünf private Materialzuweisungen aus `/Game/Environment/VisualV2WorldArtV1/Materials`. Die Originalmaterialien und Wegmeshes bleiben erhalten. Die Änderungen an Gras-/Erdtönen und Wegkanten sind im Shader räumlich begrenzt; ein altes opakes Heilhaus-Wegband erhält lokal eine maskierte Kante, damit es keinen grünen Streifen über den neuen Vorplatz malt. Sechs zusätzliche HISM-Gruppen enthalten 175 vorhandene Gras-, Kräuter-, Blüten-, Farn- und Steininstanzen ohne Collision, Schattenwurf oder zusätzlichen Distance-Field-/Indirect-Lighting-Beitrag; Culling 4500–6500 cm. Keine neue Map, keine neuen Meshes oder Texturen. Licht, Originalschatten, TAA, Kamera und Gameplay bleiben erhalten.

Dies ist ein begrenzter Gestaltungsschritt zur menschlichen Abnahme, keine Freigabe für die übrige Welt. Autorenfolge und Wiederherstellungsdaten liegen unter `Tools/VisualV2WorldArtQualityV1` und `Art/World/VisualV2WorldArtV1/HealingHouseDressing.json`; Medien sind optional und nicht in Git. Prüfungen, gemessene Mehrkosten und offene Artgrenzen: `VISUALV2_WORLD_ART_QUALITY_V1_PRUEFBERICHT.md`.

## VisualV2 World Art Quality V2: Gruppierung und Materialabschnitte (19.10.2026)

V2 ersetzt im selben begrenzten Heilhausbereich die V1-Instanzpositionen und
lokalen Bodenmaterialvarianten. Die sechs HISM-Gruppen behalten exakt 175
Instanzen, ihre Größen, Bodenhöhen, Collision-/Schattenvorgaben und Culling
4500–6500 cm. Unterschiedlich große Pflanzentaschen und freie Bodenstellen
ersetzen die gleichmäßigere V1-Verteilung. Bestehende Topfpflanzen bleiben
unverändert. Vier private Bodenmaterialien variieren lokal die vorhandenen
Texturkoordinaten, ohne neue Texturen, zusätzliche Texturabfragen oder Änderungen
an den Wegmasken.

Drei private Gras-/Kräutermeshes verwenden positionsgleiche Dreiecke, kopierte
UVs/Corner-Normalen und ein gemeinsames Vertexfarben-Material. Über alle sechs
Gruppen sinken LOD0-Mesh-Abschnitte von 17 auf 10 und Komponenten-Materialbindungen
von 19 auf 12; zwei historische Farnbindungen sind keine zusätzlichen
Renderabschnitte. Das ist keine gemessene Draw-Call-Zahl. Kein LOD wird reduziert.
Keine Änderung an Beleuchtung, Originalschatten, TAA, Lumen, Kamera oder Gameplay.

Interleavte V1/Merged/V2- und HISM/Einzelobjekt-Diagnosen ergeben keinen
belastbaren allgemeinen FPS-Gewinn. Die Materialvereinfachung wird wegen ihrer
geringeren Abschnittszahl und erhaltenen sichtbaren Form genutzt, nicht als
behauptete QHD-Lösung. Quellen und Werkzeuge: `Art/World/VisualV2WorldArtV2` und
`Tools/VisualV2WorldArtQualityV2`; kompakte Messwerte und Grenzen stehen im
`VISUALV2_WORLD_ART_QUALITY_V2_PRUEFBERICHT.md`. Keine Kontrollmedien in Git.


### Heilhaus Art Quality V4 – begrenzter Abnahmestand, 19.10.2026

Nur die bestehende Dev_TestMap_VisualV2: private V4-Boden-/Hausmaterialien und botanische Varianten unter /Game/Environment/VisualV2HealingArtV4. Zwei neue Blenderquellen, elf kollisionsfreie Meshes, vier neue HISM-Gruppen mit 147 örtlichen Instanzen. 26 neuere Töpfe ersetzt; zusätzlich acht alte dekorative Fensterpflanzen umgebunden und ihre 28 Grundkörper unsichtbar erhalten. Alle ursprünglichen 175 kleinen HISM-Instanzen bleiben bestehen. Geprüfte HouseCutaway-Funktion beibehalten. Licht, Schatten, Lumen, Bloom, TAA, Kamera und Gameplay unverändert. Keine neue Map und keine FPS-/GPU-Benchmarks. V3-Originalquellen bleiben als Referenz erhalten, visuelle V4-Freigabe durch Harry steht aus. Ergebnis: Build erfolgreich, 49/49 Projekttests, Map Check 0/0, echter 102-Schritt-PIE-Fußlauf. Einzelheiten und Grenzen in VISUALV2_HEILHAUS_ART_QUALITY_V4_PRUEFBERICHT.md.


### World Art Quality V5 – drei Musterbereiche, 19.10.2026

Der aktuelle Nutzerauftrag benennt den vorhandenen Heilhausbereich V4 als
freigegebene Qualitätsreferenz. Ausschließlich in der bestehenden VisualV2 sind
nun ein Wald-, ein Wiesen- und ein Uferabschnitt örtlich gestaltet: vier begrenzte
Bodenmaterialbindungen, 17 zusätzliche kollisionsfreie HISM-Gruppen mit 407
Instanzen. Originale bleiben erhalten; drei neue Blender-Pflanzenformen und zwei
Bodenalbedos liegen unter Art/World/VisualV2WorldArtV5, private Unreal-Varianten
unter /Game/Environment/VisualV2WorldArtV5. Keine neue Karte, keine Änderung an
Licht, Schatten, Lumen, Bloom, TAA, Kamera, Player oder Gameplay. Build, 49/49
Projekttests, Map Check 0/0 und 102-Schritt-PIE-Fußlauf erfolgreich. Echte QHD-
Vergleiche in Medium/High, PIE/Standalone, ohne FPS-/GPU-Benchmark. Grenzen und
Nachweise: VISUALV2_WORLD_ART_QUALITY_V5_PRUEFBERICHT.md. Die visuelle Abnahme
der drei V5-Muster bleibt offen; keine Ausweitung auf die gesamte Karte.


### World Art Quality V6 – Wegsäume und Gruppierung, 19.10.2026

Die vier örtlichen V5-Bodenbindungen werden in derselben VisualV2 durch drei
private V6-Materialvarianten ersetzt; V5-Assets/Quellen bleiben unverändert.
Die sichtbare Breite folgt örtlich den vorhandenen Wegkurven, einschließlich der
unmittelbar angrenzenden Wiesenwegkreuzung. Keine neue Weggeometrie oder Navigation.
399 Instanzen in 16 V5-Dekorationsgruppen neu gruppiert, acht Wurzeln unverändert,
insgesamt weiterhin 407 Instanzen. Keine neuen Actor, Meshes oder Texturen.
Licht, Originalschatten, Lumen, Bloom, TAA, Kamera, Player und Gameplay unverändert.
Build, 49/49 Projekttests, Map Check 0/0 und 102-Schritt-PIE-Fußlauf erfolgreich.
40 finale QHD-Originalaufnahmen in Medium/High und PIE/Standalone; keine FPS-/GPU-
Benchmarks. Quellen: Art/World/VisualV2WorldArtV6 und Tools/VisualV2WorldArtV6;
Grenzen und Nachweise in VISUALV2_WORLD_ART_QUALITY_V6_PRUEFBERICHT.md.
V6 bleibt auf die drei Muster und angrenzenden Wegabschnitte begrenzt;
Harrys visuelle Freigabe steht aus, keine automatische Ausweitung.


### World Art V7 – vorhandene VisualV2-Wege und Landschaft (19.10.2026)

Der ausdrücklich zur Ausweitung freigegebene V6-Stil wird in der bestehenden VisualV2 auf alle fünf Außenwegfamilien übertragen. Drei private Materialien unter `/Game/Environment/VisualV2WorldArtV7/Materials` erweitern das sichtbare Boden-/Wegfeld; Geometrie, Kollision und Steuerungsbasis bleiben unverändert. 23 neue kollisionsfreie HISM-Gruppen mit 658 Bestandsasset-Instanzen ergänzen Wald, Wiese und das weitere Ufer. Vorhandene V6-Gruppen, Originalmaterialien und andere Karten bleiben erhalten. Quellparameter und Instanzen: `Art/World/VisualV2WorldArtV7`; begrenzte Reproduktions-/Prüfwerkzeuge: `Tools/VisualV2WorldArtV7`.

Lichtquellen, Belichtung, Lumen, TAA, Kamera und gespeicherte Schattenparameter bleiben unverändert. `DirectionalLightComponent.shadow_amount` bewirkte im isolierten VSM-Bildversuch keine geeignete Aufhellung; es wurde keine Schattenvariante gespeichert. Eine ungefähr 50 % hellere wahrgenommene Schattenwirkung bleibt eine offene visuelle Entscheidung, keine bestätigte technische Einstellung.

Build, 49/49 Projekt-Automation, Map Check 0/0, realer 102-Schritt-PIE-Rundweg und QHD-Medium-100-%-Bildprüfung in PIE sowie nativem Standalone bestanden. Keine FPS-/GPU-Benchmarkfreigabe. V7 wartet auf visuelle Abnahme. Details und Einschränkungen: `Docs/VISUALV2_WORLD_ART_QUALITY_V7_PRUEFBERICHT.md`.


## Map-Lebenszyklus: aktuelle Tests und historische Versuche

`Tools/ProjectMaintenance/MapLifecycle.json` nennt exakt sechs nach QA zur Entfernung vorgesehene B-Karten und ihren Wiederherstellungspunkt `8cc96f9`. Der aktuelle NPCMotionV3-Audit benötigt die V2-Map nicht mehr: eine unveränderlich gehashte Actor-Signaturfixture erhält die Mesh-/Material-/Collision-/Transform-/LOD-/Instanz-/Lichtvergleiche. Historische Mapwerkzeuge prüfen ihre expliziten Voraussetzungen vor Arbeitsschritten und beenden fehlende Szenen mit Exit 2, niemals als Testpass oder mit stiller Kartenerzeugung. BuildingKit, HealingHouse, Dev_TestMap, NPCMotionV3, GPU-Diagnose, VisualV2, WestlandRegion und AssetLibrary bleiben reguläre Prüfkarten; zusätzlich die geschützte unversionierte EnvironmentQuality-Map und vorerst Village/BattleTest. Keine Assets oder Quellversionen werden zusammen mit einer Karte gelöscht.

Die sechs vollständig abgelösten Karten sind nach erfolgreicher Phase-1-Prüfung entfernt: EnvironmentPerfV1/V2/V3, NPCMotionV2, RangerPerfV2 und TreeShadowProxyV1. Elf Maps bleiben einschließlich der geschützten unversionierten Testmap sowie Village/BattleTest erhalten. Nach Entfernung: erneuter Editor-Build, vollständige Automation und elf Map Checks; Ergebnisse im Abschlussbericht des Gesamtauftrags. Git-Historie, LFS-Payloads und alle zugehörigen Art-/Animationsassets bleiben erhalten.

### VisualV2 – integrierter Art-Pass nach Kartenbereinigung (19.10.2026)

VisualV2 verwendet private Heilhaus-/Landschafts-Materialvarianten, 14 zusätzliche kollisionsfreie HISM-Gruppen und drei neue Blender-Detailmeshes. Die vorhandenen Shader-/Cutaway-Systeme, TAA, Kameras, Wegführung, Kollisionen und Gameplay bleiben erhalten. Der bestehende Himmelsfüllanteil und vorhandene Innen-/Fensterlichter wurden im ausdrücklich erweiterten Art-Auftrag abgestimmt. Quellen, konkrete Werte und Abnahmegrenzen stehen in `PROJEKTBEREINIGUNG_GRAFIKVERBESSERUNG_V2_PRUEFBERICHT.md`; reproduzierbare Werkzeuge und zusammengefasste Prüfergebnisse unter `Tools/ProjectMaintenance/`. Lokale Kontrollbilder unter `Saved/` sind optional und keine erforderlichen Testfixtures.

### Art-Pass V3 – opt-in Innenraumbeleuchtung und statische NPC-Präsentation (20.10.2026)

BuildingCutaway besitzt eine standardmäßig ausgeschaltete `bUseShadowlessInteriorLighting`-Option. Vorbereitete Raumgeometrie und schattenlose Raumlichter verwenden Lichtkanal 1. Nur während des tatsächlichen Aufenthalts im Raum werden die Primitive-Komponenten des Players diesem Kanal zugeordnet und ihr Schattenwurf deaktiviert; beim Verlassen, Abschalten oder EndPlay werden die ursprünglichen drei Kanalbits und Schattenflags komponentengenau restauriert. Außenlicht, Kamera und Gameplay werden nicht global geändert. Die bestehende NPC-Präsentation kann über `StaticPresentationMesh` ausdrücklich ein ungeriggtes Modell anzeigen; nur dann entsteht eine zusätzliche transiente statische Komponente. Skeletal-NPCs erhalten keine leere Zusatzkomponente. Der bestehende Sprite-Fallback und die Quellinteraktion bleiben erhalten. `bShadowlessInteriorPresentation` ist eine gesonderte opt-in Raumzuordnung. Build und 50/50 Automationstests einschließlich Rückkehr-/Fallback-Regression bestanden; die Kartenaktivierung und visuelle Abnahme folgen separat.

### Art-Pass V3 – Aktivierung in VisualV2 (20.10.2026)

Die zuvor separat geprüfte opt-in Grundlage ist nun ausschließlich im Heilhaus der VisualV2 aktiviert. Raumkomponenten und vorhandene Raumlichter verwenden Kanal 1 ohne Schlagschatten; eine breite schattenlose RectLight ergänzt 550 lm bei 5000 K, 650 × 500 cm Quellfläche und null GI-Beitrag. Außenlichter, Außenschatten, Postprocessing, TAA und beide Kameras bleiben unverändert. Die ursprünglichen Player-Lichtkanäle und Schattenflags werden beim Verlassen restauriert. Der reale Ein-/Ausgang einschließlich Diagonalen und die Blickwendung des optionalen statischen SilverLady-Modells sind geprüft.

Der Heilpunkt behält Identität, Transform, Kollision, Dialog-, Heil-, Checkpoint- und Speicherfunktion; nur seine Darstellung wechselt auf eine unabhängige SilverLady-Standpose. Das Modell besitzt noch keine freigegebenen Animationen. Zwei neue gefaltete Farnvarianten ersetzen nur die VisualV2-Bindungen von 224 vorhandenen Instanzen; Wege werden materialseitig leicht unregelmäßiger. Das sporadische Fensterflackern ist weiterhin nicht sicher reproduziert und ausdrücklich nicht als behoben freigegeben. Build, 50/50 Automation, elf Map Checks und vollständiger 102-Schritt-PIE-Fußlauf bestanden. Details: ART_PASS_V3_HEILHAUS_LANDSCHAFT_PRUEFBERICHT.md; maschinenlesbare Ergebnisse: Tools/ProjectMaintenance/ArtV3Acceptance.json. Visuelle Abnahme bleibt bei Harry.

### Grafikpass V4 – bestehendes VisualV2-Heilhaus und Wegsäume (20.10.2026)

Der aktuelle V4-Stand ersetzt nur die VisualV2-Präsentationsbindung der statischen V3-Heilerin durch eine unabhängige Skeletal-Variante unter `/Game/Characters/NPCs/SilverLady/HealerArtV4`. Drei Deform-Bones plus FBX-Helfer, vier Sekunden ruhige Idle; kein vollwertiges Walk-/Gestenrig und kein Physics Asset. Der Heilpunkt, Sprite-Fallback, Dialog-/Heil-/Speicherlogik und alle Originalquellen bleiben erhalten. Die alte statische Darstellung bleibt als Referenz verfügbar.

Das vorhandene schattenlose Raumlicht wird auf 800 lm und 900×800 cm erweitert; Lichtfarbe, Kanal 1 und null GI-Beitrag bleiben bestehen. Nur im Innenraum, keine Außenlicht-/Schatten-/TAA-/Lumen-Änderung. Neue eigene Blender-Props ergänzen Kamin, Arzneischrank, Borde, Bettgestelle, Pflanzenbanner, flachen Teppich und Steinzone. Nur Kamin/Schrank erhalten einfache neue Möbelkollisionen; bestehende verschobene Möbelblocker werden mitgeführt. 727 neue dekorative HISM-Instanzen und zwei niedrige Zäune ergänzen Weg-/Waldränder ohne neue Gameplay-Kollision. Bestehende Bäume und Wegeführung bleiben erhalten.

Die vorhandene Materialinstanz `MI_WLA_MossStone` erhält ausschließlich das nachgewiesene InstancedStaticMesh-Usage-Bit; Parent, Texturen, Parameter und sichtbare Materialfunktion bleiben gleich. V4-Actor-Signaturen und Scope-Prüfung sind Pflicht, lokale Kontrollmedien optional. Details, tatsächliche Tests und offene visuelle Grenzen: `Docs/GRAFIKPASS_V4_PRUEFBERICHT.md`, kompakt `Tools/ProjectMaintenance/ArtV4Acceptance.json`. Fensterflackern weiterhin nicht sicher reproduziert; keine bestätigte endgültige Behebung.

### Grafikpass V5 – Holzboden und unveränderte SilverLady (20.10.2026)

V5 ersetzt die V4-Steinzone im bestehenden VisualV2-Heilhaus vollständig: die einzelne kollisionsfreie FlagstoneApron-Instanz ist entfernt, die dreißig bisherigen Boden-Visuals verwenden nahtlos anschließende Plane-Flächen am bisherigen Ort und ein durchgehendes weltbasiertes gealtertes Holzmaterial. Bestehender Bodencollider, Teppiche und Laufwege bleiben erhalten. Alte Quellen/Assets bleiben als Entwicklungsreferenzen bestehen.

Die V4-Gewand-Neufärbung ist für die aktuelle Heilerin ersetzt: die vorhandene riggte Kopie bindet auf Komponentenebene wieder exakt `/Game/Characters/NPCs/SilverLady/Materials/MI_SilverLady_V1`. Geometrie, Polygonstruktur, UVs und Objekttransformation der riggbaren Kopie stimmen nach Blender-Fingerprints exakt mit der ursprünglichen Heilpose überein. Keine neue Gesichts-, Haar-, Proportions- oder Kleidungsmodellierung. Das bestehende dezente Vier-Sekunden-Idle bleibt unverändert. Die statische Quelle und der V4-Gewandshader werden nicht überschrieben.

Nur das vorhandene schattenlose Kanal-1-Raumlicht wird flächiger eingestellt (1000 lm, 1200×1000 cm); Außenlicht, Außenschatten, Kameras, Lumen, Bloom und TAA bleiben erhalten. Drei eigene Blender-Detailmeshes ergänzen Polster, Lesesessel und Bücher. Nur der neue Sessel erhält eine zusätzliche Möbelkollision. Private V5-Wegmaterialien und Umgruppierungen vorhandener V4-Instanzen erhalten Wegeführung, Bäume, Instanzanzahl und bestehende Kollisionen; zwei ausdrücklich unpassende V4-Zauninstanzen entfernt. Aktueller strenger Prüfvertrag: `ValidateArtPassV5.py`/`ArtV5Signatures.json`. Details und offene Fensterdiagnose im V5-Prüfbericht.

### Zunderlauf V1 – optionale Skeletal-Kreaturendarstellung (20.10.2026)

`FPokeMonsterCreatureVisuals::Presentation` ergänzt die vorhandenen Flipbooks um eine optionale `UPokeMonsterCreaturePresentationData` mit Mesh, sieben Clips, eigenen Walk-/Run-Geschwindigkeiten, Bodenoffset und Schwanzflamme. `APokeMonsterCreatureVisualActor` besitzt keine Kollision. Sein nativer Animationsproxy blendet Idle/Walk/Run, passt die Zyklusphase an die tatsächliche Bewegung an und spielt Attack/Hit/Faint/Happy unabhängig von der Kampfberechnung ab. Die bestehenden Spezies-, Instanz-, Fang-, Team-, Heil- und Speicherregeln bleiben zuständig; kein neues Saveformat.

VisualV2 verwendet am bestehenden optionalen Wild-Actor `/Game/Data/Creatures/DA_Zunderlauf` und `/Game/Data/Encounters/DA_Zunderlauf_Wild`. Ausgangsposition, Encounter-ID und bisheriger Kollider bleiben erhalten. Kleine Umgebungsbewegung ist nur für diese Instanz eingeschaltet; andere Encounter-Actors behalten standardmäßig ihre bisherige statische Darstellung. Bodenanpassung betrifft ausschließlich die sichtbare Kreatur.

Historischer V1-Stand (für normale Begegnungen durch ClassicBattle ersetzt, siehe unten): Weltkämpfe behalten die geladene Map und bestehende Kamera. Temporäre kollisionsfreie Kreaturenansichten folgen den vorhandenen Widget-Präsentationsphasen. Die flächige Testkampf-Hintergrundillustration wird bei Weltbegegnungen nicht mehr über die tatsächliche Welt gelegt. Arten ohne eigenes 3D-Modell behalten ihre vorhandenen UI-Figuren; der separate Battle-Testmodus bleibt erhalten.

Quelle: `Art/Characters/Creatures/Zunderlauf/Source/Zunderlauf_V1.blend`, 49.904 Körperdreiecke, 23 Blender-Bones plus FBX-Wurzel in Unreal, drei gepackte 2048²-Texturen. Das eigene Rig verwendet keine Spieler- oder Ranger-Retargets. Vorläufig ca. 65,2 cm Körperhöhe; 140-cm-Spieler unverändert. Walk 35 cm/s, Run 60 cm/s. Feuer ausschließlich als kleine opaque, emissive und vertexbewegte Geometrie am `tail_socket`; keine Flammen am Körper und keine globale Lichtänderung. Der Stand benötigt gesonderte visuelle Abnahme; keine automatische Übertragung auf weitere Kreaturen. Ablauf und Grenzen: `Tools/ZunderlaufV1/README.md` und Kreaturen-Prüfbericht.

### Kreaturen-Pipeline V2 – modellunabhängiger Importvertrag (20.10.2026)

Die bestehende Trennung aus Spezies, Instanzzustand und optionaler Präsentation bleibt maßgeblich. `UPokeMonsterCreaturePresentationData::GetValidationErrors` prüft Mesh/Skeleton, Materialslots, Idle und vorhandene Cliprollen, exakte Skeletonidentität, Clipdauer, Root-Motion-Flag, Geschwindigkeiten, Bodenoffset, Größenherkunft und Effekt-Anker. `SetSpecies` verwirft ungültige Kandidaten vor jeder Änderung einer funktionierenden Darstellung. `RigFamily`, `ReferenceSizeCm` und `SizeSource` sind Metadaten; keine automatische Retarget-, Größen- oder Bewegungsentscheidung.

Zusätzliche `EffectAnchors` erlauben einfache kollisionsfreie Mesh-Effekte an pro Modell definierten Bones/Sockets, mit lokalem Offset und optional weltaufrechter Rotation. Der vorhandene `TailFlame`-Pfad bleibt unverändert gültig. Keine Migration bestehender Assets und keine neue Save-Version. Das Saveformat speichert weiter stabile Spezies-IDs und individuelle HP/PP/Level/XP, keine visuellen Assetpfade.

`Tools/CreaturePipelineV2` enthält lesende Blender-/Unreal-Inspektion, SHA-/Pfad-/Skalierungs-Vorprüfung, einen bewusst unvollständigen Glumanda-Plan sowie Kandidaten- und Map-Prüfer. Keine automatische 251er-Erzeugung oder Batchintegration. Am Pipeline-V2-Ausgangspunkt existierten vier technische Spezies mit Prototypnummern; dies war kein vollständiger Größenkatalog. Glumandas belegtes späteres Ziel ist 60 cm Stehhöhe; die bestehende Zunderlauf-V1-Größe bleibt unverändert. Die nationale Nummer im Intake ist getrennt von bestehenden Spielidentitäten. Vollständiger Ablauf einschließlich Längenmessung bei anderen Körperformen und konkretem identitätserhaltendem Austausch: `Docs/KREATUREN_PIPELINE_V2.md`. Große Körper, Flug-/Schwimm-KI und universelle Gelände-IK sind damit nicht automatisch abgenommen.

## Meshy-Glumanda Integration V1 (20.10.2026)

`CreatureSpecies:Zunderlauf` verwendet jetzt das separat importierte Meshy-Profil
`/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation`.
Die unveränderte Nutzer-GLB, gepackte Blenderquelle, drei originale 2K-JPEGs und
sieben FBX-Clips liegen unter den bestehenden Kreaturenverzeichnissen.
60 cm Höhe, 21.761 Dreiecke einschließlich originaler Schwanzflamme, eigenes
23-Bone-Blender-Rig (24 UE-Bones einschließlich FBX-Wrapper), Walk 22 cm/s,
Run 36 cm/s. Die einzige persistente Gameplay-Datenänderung ist die optionale
Darstellungsreferenz; stabile Art-ID, Saves, Karten und Zunderlauf-V1-Assets bleiben.
Die Flamme ist die originale Geometrie und folgt `tail_socket`; tatsächliche
Socket-Skalierung wird im Effekt-Offset kompensiert. Kein zweiter Flammeneffekt.
Vollständige Prüfungen und Grenzen: `MESHY_GLUMANDA_INTEGRATION_V1_PRUEFBERICHT.md`;
Reproduktion: `Tools/MeshyGlumandaV1/README.md`. Keine abschließende künstlerische
Freigabe oder universelle Rig-/LOD-Freigabe für weitere Arten daraus ableiten.

### Glumanda V1.1 – lokaler Skin-/Namenspass

Anzeigename Glumanda bei unveränderter Art-ID `Zunderlauf`. Das aktive Profil
`/Game/Characters/Creatures/Zunderlauf/MeshyV11/DA_Glumanda_V11` verwendet einen
lokal reparierten Skin (18.245 Körperdreiecke) auf exakt dem vorhandenen Skeleton.
Alle sieben Originalclips, Materialien, Texturen und Schwanzflamme bleiben Referenzen
auf V1. Quelle/UV-/Restpose-/Actionvergleich und FBX-Roundtrip sind eigenständig geprüft;
zehn echte kleine Randloops geschlossen, nur die Flammennaht bleibt absichtlich offen.
Kein neues Saveformat. `Tools/GlumandaV11/README.md` beschreibt den bewachten Ablauf.


### Glumanda V1.1 – Sichtfreistellung und getrennte Kampfpräsentation

Die vorhandene Sichtfreistellung setzt zur Laufzeit `PlayerSightShape` auf
110/220 cm statt 55/110 cm. `RevealRadiusScale=2` verdoppelt Radius und Durchmesser,
nicht nur die Fläche; Broadphase folgt dem äußeren Radius. Fadezeit .25 s,
endlicher Kamerakegel, Baum-/Material-Opt-in und Original-MPC bleiben erhalten.
Die Figurenschatten-Versuche wurden wegen unzureichender Sichtqualität verworfen;
kein aktiver Kontaktflächenbaustein und keine globale Schatten-/Lichtänderung.

`EPokeMonsterBattlePresentationMode` wählt ClassicBattle (Default) oder WorldBattle.
Wild- und Trainerprofile reichen ihre Einstellung an `EncounterStartData` weiter;
ungültige Werte werden vor Eingabesperre und Sessionstart abgewiesen. Bestehende
BattleSession, Presenter, Fang, Team, Trainerzustand, Heilung und Saves bleiben gemeinsam.

ClassicBattle erzeugt nur zur Laufzeit eine `APokeMonsterClassicBattleScene` in
derselben geladenen Welt, mit ShowOnly-SceneCapture, kollisionsfreien Kreaturen und
RenderTarget 2560x1080 im 1280x720-UMG-Layout (Kampfansicht V2). Eigene Figur hinten links, Gegner vorne
rechts. Meshgröße unverändert; Kameraabstand/Bühnenabstand richten sich nach Bounds.
Namen/Level/KP, Attacken, Fang und Wechsel verwenden die bestehenden Widgetbindungen.
Die normale Spielkamera und der Pawn werden nicht umgeschaltet oder teleportiert.
Nur die Bühne nutzt eine schattenlose Füllleuchte auf Kanal 2; nur ihre kurzlebigen
Meshes empfangen Kanal 2. Keine Änderung bestehender Lichtquellen. Keine Kollision,
Navigation, indirekte Licht-/Distanzfeldwirkung der Bühne. Ende/Wechsel räumt die
kurzlebigen Actors auf. Spezialbegegnungen können den bestehenden WorldBattle-Pfad
mit Originalkamera wählen. Fehlende 3D-Arten behalten vorhandene Prototyp-UI-Figuren;
keine erfundenen Ersatzmodelle. Noch keine Freigabe beliebiger Groß-/Flugmodelle.

`pm.CreatureReview.Start classic|world [meadow|forest|cave|ruins]` ist ein expliziter Development-Prüfaufruf,
kein Gameplaystart und kein Save-Schreiber. `pm.CreatureReview.CaptureLiveUI Name`
schreibt bei `BattleV2_`-Präfix unter `Saved/BattleViewV2/LiveUI/`, sonst unter
`Saved/GlumandaV11/LiveUI/`, verweigert vorhandene
Ausgaben und erfasst den tatsächlichen Slate-Spielviewport in seiner echten Größe.
Kein Offscreen-Widgetrender wird als Viewportfoto bezeichnet. Werkzeuge und Grenzen:
`Tools/GlumandaV11/README.md`, Gesamtprüfung im Glumanda-V1.1-Bericht.


### Kampfansicht V2 – Menüseiten und Umgebungen

Die klassische Ansicht hat eine ruhige 3D-Standardkamera, Gegnerkarte oben links,
eigene Karte unten rechts und die Seiten Befehle, vier Attackenslots, Team und
Beutel. AP/KP kommen weiterhin aus der bestehenden BattleSession/Presenter-Ansicht.
Doppelte sichtbare Logs und winzige Teamstatusanzeigen sind entfernt; Zuginformationen
erscheinen im gemeinsamen Meldungsfeld. Technische Testattacken erhalten ausdrücklich
vorläufige, lesbare Namen; IDs, Schaden, Typen und Saveformat ändern sich nicht.

`BattleEnvironment` in Wild-/Trainerprofil und EncounterStartData wählt Auto,
Meadow, Forest, Cave oder Ruins. Explizite Profile haben Vorrang vor Region/Actor-Tags,
danach folgen vorhandene Ruinen bzw. mindestens drei nahe Bauminstanzen innerhalb
650 cm. Bei ISM/HISM werden Weltpositionen der einzelnen Instanzen geprüft, nicht
nur der Gruppenursprung. Nicht zugeordnete Orte verwenden Wiese. Höhlen werden
nicht aus unbekannten Ortsnamen erfunden; entsprechende Metadaten müssen gesetzt
werden. Dies ist Präsentationsmetadatum, keine neue Biome-/Begegnungslogik.

Zehn vorhandene Meshes und drei Bodenmaterialien erzeugen kleine, kollisionsfreie,
nur im Capture sichtbare Bühnen. Keine neuen Maps oder Änderungen bestehender
Umgebungsassets. Höhle empfängt nur die isolierte Füllung, Außenvarianten weiterhin
das vorhandene Licht. Bühne, Kreaturen und Füllung wirken nicht auf Welt-GI oder
Distanzfelder; ihre dynamischen Schatten sind deaktiviert. Federnde Kontaktmarken
im Widget folgen projizierten Bodenankern, einschließlich Teamwechsel. Sie sind
keine physikalischen Schlagschatten. Kamerabewegung endet nach 0,35 Sekunden bei
exakt derselben Ruhestellung. Glumandas Meshmaß bleibt 60 cm. Bounds-Framing passt
Abstand und Bühne an; große/flugfähige künftige Modelle brauchen eigene Sichttests.

Steuerkreuz/Stick navigieren das Raster, Nintendo A bestätigt rechts/B unten geht
zurück; `bNintendoButtonLayout=false` tauscht die logischen Bestätigen/Zurück-Tasten.
Tastatur und Maus bleiben nutzbar. Nach dem Zug wird der Befehlsfokus wiederhergestellt.
Die Oberfläche skaliert im 16:9-Referenzlayout, andere Seitenverhältnisse werden
proportional eingerahmt. Ein-/Ausblendung betrifft nur die Kampfoberfläche.

Historischer Stand Kampfansicht V2, ersetzt durch Kampfsystem V3: Fluchtregeln und Heilitems innerhalb eines Kampfzugs fehlten.
V2 zeigte dies ohne Zugverbrauch an; seit V3 bietet der Beutel Fanggerät und Heilitems. Keine erfundenen finalen Werte oder
parallele Kampfaktionen. Anleitung: `Tools/BattleViewV2/README.md`;
Ergebnisse und Einschränkungen: `KAMPFANSICHT_V2_PRUEFBERICHT.md`.


### Kampfsystem V3 – Spielaktionen und Gen-2-Starterdaten (20.10.2026)

Die vorhandene BattleSession verarbeitet zusätzlich Flucht und Heilitem-Züge.
Flucht ist nur bei ausdrücklich erlaubten nicht geskripteten Wildbegegnungen aktiv;
Trainer, Test- und Storybegegnungen bleiben gesperrt. Die geprüfte Gen-1/2-
Geschwindigkeitsformel verwendet einen Zufallswert 0–255 und Folgeversuche.
Andere Aktionen setzen den Versuchszähler zurück (bewusst dokumentierte Projektregel).
Erfolg beendet ohne Gegnerzug und ohne Sieg-/Fangflag; Fehlschlag erlaubt den Gegnerzug.

Der Beutel listet tatsächlich vorhandene Heilitems, bei mehr als drei Typen seitenweise.
Zielwahl aus dem eigenen Team, auch inaktive Mitglieder. Nur lebende verletzte Ziele;
kein Verbrauch vor gültiger Auswahl. Das bestehende Inventar entfernt genau ein Item,
stellt bei abgewiesener Auflösung die ursprünglichen Stapel wieder her und der Gegner
handelt danach. `DA_TestHealingItem` heißt spielerseitig Trank und behält 20 KP Heilung,
seine stabile ID und seine Überweltverwendung. Kein automatisch gewährter Itemvorrat.

`DA_Zunderlauf` behält Identität und Darstellung. Opt-in Lernliste: Kratzer/Heuler
Level 1, Glut Level 7; Level 10 hat drei belegte Slots. Vierfachbelegung wird nicht
künstlich aufgefüllt. Neue Wildexemplare erhalten die zum ausgewürfelten Level
passende Liste. Dies ist der belegte Starter-Teilumfang, kein vollständiger Pokédex.
Heuler senkt Angriff bis −6; Wechsel setzt die Stufe zurück. Glut hat 10 % Verbrennung,
Feuertypen sind dagegen immun. Verbrennung halbiert physischen Angriff und verursacht
max(1,MaxKP/8) Restschaden. Heilpunkte heilen auch Verbrennung, der Trank allein nicht.

Ist keine Attacke mit AP verfügbar, kann Verzweifler typneutral mit Stärke 50 und
Rückstoß max(1,verursachter Schaden/4) verwendet werden. Kein neuer Lernslot und
keine aufgefüllten AP. Beide Seiten bleiben dadurch handlungsfähig.

Kampf-XP: belegter Glumanda-Ertrag 65, vorhandene Wachstumskurven, lebende am jeweiligen
Gegner beteiligte Mitglieder; Trainerbonus 1,5. Unbekannte Spezies-Erträge bleiben 0,
bis sie verifiziert sind. Keine Fang-/Flucht-XP. Levelaufstieg füllt bekannte neu
verfügbare Lernattacken nur in freie Slots, ersetzt keine Spielerwahl automatisch.
Die vorhandene vereinfachte Schadensformel und Gleichstandregel bleiben erhalten;
keine Behauptung vollständiger Generation-2-Simulation (unter anderem kein STAB,
Volltreffer, zufällige Schadensstreuung oder komplette Status-/Attackenbibliothek).

Save-Schema 4 ergänzt `Status`. Versionen 1–3 bleiben lesbar; bekannte technische
Glumanda-Testloadouts werden eng begrenzt in die neue Liste übertragen. Identität,
Level, XP und KP bleiben erhalten; bereits verbrauchte AP werden den entsprechenden
neuen Attacken zugeordnet. Alte Assets/IDs bleiben erreichbar; gemischte eigene
Attackenlisten werden nicht umgeschrieben. Kampfzustände sind weiterhin nicht
speicherbar, nur der konsistente Oberweltstand. Niederlagen nutzen unverändert den
bestehenden Checkpoint-/Heilablauf; ein automatischer Save unmittelbar nach dieser
Rückkehr ist weiterhin nicht implementiert. Heilen/Speichern am Heilhaus und manuelles
Speichern bleiben verfügbar.

ClassicBattle und WorldBattle verwenden dieselben Befehls-/Beutel-/Teamseiten und
Ereignisse. Ausführung sperrt Mehrfachklicks; HP-Veränderungen werden interpoliert,
Statusattacken zeigen keinen Schadenswert. Glut erhält einen kleinen zeitlich
gebundenen Flame-Sprite ohne neue Weltbeleuchtung; Schwanzflammen bleiben unverändert.
Prüfablauf: `Tools/BattleSystemV3/README.md`. Physischer Switch-Pro-Test ausdrücklich offen.

### Starter-Erweiterung: Schiggy, Bisasam und freie Landbewegung (21.10.2026)

Zwei zusätzliche Meshy-Spezies verwenden eigene Rigs: Schiggy 50 cm (Biped), Bisasam 70 cm (Quadruped). Glumanda bleibt 60 cm unter der bestehenden ID Zunderlauf. Originale in Incoming bleiben unverändert. Je sieben eigene Clips und unabhängige Unreal-Namensräume; keine Veränderung der ClassicBattle-Kamera, UI, Umgebungen oder Regeln. Originaldaten und Messgrenzen stehen im `STARTER_ERWEITERUNG_V1_PRUEFBERICHT.md`.

`Species.Overworld` und `Creatures/Overworld` steuern größere Landhabitate, kollisionsgeprüfte lokale Routen, Ruhephasen und einen rein visuellen Begleiter des vorhandenen Teams. Bewegung wird vor der Präsentation aktualisiert, damit deren Geschwindigkeitsmessung nicht zwischen zwei Tick-Zeitpunkten springt. Optionaler Begleiter-Sprint nutzt ein temporäres Profil; Kampfclips bleiben erhalten. Tatsächliche Playergeschwindigkeit wird berücksichtigt, nicht fest auf 210 cm/s gesetzt. Keine zusätzliche Spieler-Kollision, kein zweites Party-/Save-System und keine Schwimm-/Flugnavigation. Bestehende Wasserblocker und Gebäudegrenzen bleiben wirksam. Ausführlicher Konfigurations-/Import-/Prüfablauf: `KREATUREN_PIPELINE_V2.md`, Abschnitt 10.

Nach Niederlage wird erst nach kollisionsgeprüfter Rückkehr und vollständiger Heilung automatisch gespeichert. Saveformat 4 bleibt kompatibel; macOS schreibt zunächst eine geprüfte temporäre Nachbardatei und ersetzt den Slot atomar. Ein Fehler darf den vorhandenen Slot nicht vorab löschen. Historische QA verwendete den realen Dev-Slot mit SHA-kontrollierter Wiederherstellung; für Speichersystem V2 ersetzt durch ausschließlich isolierte PIE-Testslots ohne Kopieren/Umbenennen des Nutzersaves.

## Starter-Feinschliff V2 (21.10.2026)

Begleiterwahl ist nun strikt Teamplatz 1, ohne Ersatz durch spätere Mitglieder. Landbewegung nutzt Beschleunigung, Ausbremsen und begrenzte Winkelbeschleunigung, kollisionsgeprüfte Pfadglättung und eine begrenzte Zielhistorie. Keine Änderung an Playergeschwindigkeit, Kamera, Habitatpositionen oder Kollisionen.

Die vorhandene BattleSession unterstützt zusätzlich physische Verteidigungsstufen, Initiative-Stufen, Rutenschlag/Panzerschutz, Blubbers 10-%-Initiativesenkung und kampflokale Egelsamen mit Gras-Immunität, KP-Entzug/Heilung und Rücksetzung beim Wechsel des betroffenen Pokémon. Vorhandene vereinfachte Schadens-/Fluchtregeln bleiben Grundlage; dies ist keine vollständige Gen-2-Emulation. Vier kleine Datenassets, keine neue Attackendatenbank. Vorhandene individuelle Attackenslots werden nicht automatisch neu belegt.

Zwei getrennte visuelle Korrekturen: Glumandas Faint-Pose am Schwanzansatz; Bisasams zentrale Bauchgewichte. Originale Quellen, Modelle, Materialien und Skeletons bleiben erhalten. Schiggys vorhandene No-Mip-BaseColor bleibt unverändert, solange kein nachgewiesener neuer Distanzfehler vorliegt. Details und Grenzen: `STARTER_FEINSCHLIFF_V2_PRUEFBERICHT.md`, Pipeline-Abschnitt 11.

### Oberwelt-KI V2 und Charakterlesbarkeit (21.10.2026)

Die bestehende `UPokeMonsterCreatureRoamingComponent` erhält artspezifische `Overworld.Behavior`-Profile: Curious, Shy, Territorial und Calm. An vorhandenen Wildakteuren kann das Profil über `OverworldMovement.OverrideBehavior` pro Begegnung ersetzt werden. Die bestehende lokale Wegsuche prüft weiterhin Boden, Wasser, Hindernisse und Habitatgrenzen. **Ersetzt durch Wilde Begegnungen V2:** Der frühere territoriale Sichtkontakt-/Warnzeit-/Nahbereichs-Automatismus gilt nicht mehr. Keine neuen persistenten Zustände oder Spezies-IDs. Die frühere Beschränkung auf einzeln platzierte Gruppenmitglieder wird unten durch ausdrücklich konfiguriertes `GroupSize` ersetzt.

Der Begleiter bleibt ausschließlich Teamplatz 1. Er beginnt bei loslaufendem Spieler früher zu folgen, nutzt weiterhin das vorhandene Aufholtempo und bleibt kollisionslos. ClassicBattle pausiert/verbirgt ihn. Innere Lichtkanäle und Schattenfreiheit des Heilhauses bleiben erhalten.

Die bevorzugte Aufhellung ist ein kleines, schattenloses Fülllicht ausschließlich für die Spielfigur auf reserviertem Lichtkanal 2. Vorhandene Sonnen-/Sky-/Fülllichter und Materialien werden nicht verändert. `pm.PlayerFill.Mode`: 0 aus, 1 automatische konservative Kronen-/Blockerabschätzung (Standard), 2 erzwungene Diagnose. `pm.PlayerFill.Lumens` standardmäßig 20 lm ist eine kalibrierte Lichtstärke, **keine Zusicherung einer prozentualen Bildaufhellung**. Fünf Messpunkte, fünf Aktualisierungen pro Sekunde, geglättete Wirkung. Innenraumkanal 1 schaltet das Licht aus; Begleiter übernehmen den privaten Kanal 2 nicht. Der Sichtkreis bleibt 2,0.

Kollisionslose Baumkronen werden anhand ihrer inneren, sonnenprojizierten Volumen konservativ angenähert. Das ist keine Abfrage des tatsächlichen VSM-/Lumen-Schattenpuffers. Solide kollidierende Schattenwerfer werden mit Sonnenstrahlen geprüft. Einzelne Blattlücken, Wind und Teilbeschattung sind bekannte Grenzen; neue Vegetationsformen benötigen eine erneute Sichtprüfung. Sonnenlicht, Kronenöffnung, tiefer Schatten und Innenraum müssen getrennt verglichen werden. Eine globale Sky-Aufhellung bleibt zurückgenommene Diagnose.


### Wilde Pokémon und Begegnungen V2
Verhaltensabhängige Initiierung im vorhandenen Profil: Kontakt ausschließlich für territorial/aggressiv, gezielte gemeinsame Interaktion für ruhig/neugierig/scheu. Kapseloberflächen statt Sensorsphärenradius; gültige Sichtlinie und Richtungs-/Entfernungsgewichtung bei Herausforderungen. Kein neues Kampf- oder Eingabesystem. Die gemeinsame Interaktionsaktion bleibt erhalten. Seit dem ausdrücklichen Switch-Pro-Auftrag vom 22.10.2026 ist B zusätzlich standardmäßig zugeordnet; die frühere vorläufige Belegung ohne Gamepad-Taste ist damit ersetzt. Siehe Nintendo-Switch-Pro-Abschnitt unten.

Nach normalem Classic-Wildsieg bleibt die abgeschlossene Begegnung kurz sichtbar, nutzt die bestehende lokale Wegsuche zum Verlassen des Kamerabilds und wird erst danach deaktiviert. Eine konservative vollständig projizierte Visual-Boundingbox entscheidet über das Sichtfeld. Fang, Spielerflucht, Niederlage und WorldBattle sind gesondert behandelt. Ein unerreichbarer Fluchtweg führt zu sichtbarem nicht-interaktivem Warten mit Wiederholungsplanung, niemals zu einem sichtbaren Teleport.

Explizite kleine Gruppen nutzen stabile individuelle IDs, eigene Seeds und Idle-Phasen. Nur das angesprochene Mitglied kämpft. In VisualV2 ist eine Bisasam-Dreiergruppe am bestehenden Habitat aktiviert; keine zusätzliche Map oder Spezies. Ablauf, Einstellungen, Migrationsschutz und Prüfgrenzen: `Tools/WildEncountersV2/README.md`. Der ältere `OverworldAIV2/ReviewBehavior.py` dokumentiert die ersetzte Nahbereichsregel und ist keine aktuelle Begegnungsabnahme mehr.

Die lokale Hinderniskern-Prüfung erfolgt kontinuierlich pro Wegsegment zusätzlich zur Bodenabtastung, damit schmale Eckenkreuzungen nicht erst im tatsächlichen Bewegungsschritt abgewiesen werden. Explizites Laden eines Vor-Sieg-Snapshots reaktiviert abgeschlossene Wildakteure am ursprünglichen Map-Spawn und initialisiert ihr Habitat neu. Laden eines Nach-Sieg-Snapshots lässt sie abgeschlossen; die normale Flucht teleportiert nicht. Beide Richtungen werden im bestehenden Dev-Slot mit geprüfter Originalwiederherstellung getestet.


### Kreaturen-Erweiterung V3 (21.10.2026)

Sieben weitere gelieferte Meshy-Arten (Pikachu, Myrapla, Enton, Machomei, Nebulak, Gengar, Glurak) nutzen eigene packed Blenderquellen, Rigs und je sieben Clips. Eigene stabile IDs/Dex/Originalhöhen; Starter und Saveformat unverändert. Vorhandene Darstellung und Habitat-/Kampfsysteme werden wiederverwendet. Der artspezifische Navigationsabstand ist von der Körperkontaktkapsel getrennt; eine besiegte Kreatur darf den Anfangskontakt unter kontinuierlicher Körperradiusprüfung verlassen. Absorber und levelabhängiger Fixschaden erweitern ausschließlich die vorhandene Attackenauflösung. Lernlisten/Testlevel bewusst nicht vollständig/final. Exakte Dateien, Testergebnisse und Grenzen: `KREATUREN_ERWEITERUNG_V3_PRUEFBERICHT.md`, Werkzeugablauf `Tools/CreatureExpansionV3/README.md`.

Ein während des V3-Fußlaufs belegter Begleiter-Türübergangsfehler ist lokal korrigiert: Lichtkanäle und Schattenstatus der Begleitervisualisierung folgen deren eigener tatsächlicher Zugehörigkeit zum vorhandenen versetzten Innenraum, nicht vorzeitig dem bereits hinausgelaufenen Spieler. Raum- und Außenlichter bleiben unverändert.


## Kreaturen-Animationsfeinschliff V4 (21.10.2026)

- Teamumordnung nutzt `ReorderParty(InstanceId, TargetIndex)` im vorhandenen EncounterSubsystem. Vollständige Instanzen tauschen; freie Ziele hängen im bisherigen dichten Array ans Teamende. Kein Save-Schemawechsel, während Kampf/Niederlagenrückkehr gesperrt. Teamplatz 1 bestimmt weiterhin den einzigen Begleiter. UI verwendet vorhandene Interaktions-Keys und Navigationsereignisse; Hardwaretest Switch Pro offen.
- `Tools/CreaturePolishV4/RunShowcase.py` erzeugt ausschließlich auf ausdrücklichen Aufruf ein transientes Vorführgelände im PIE der vorhandenen VisualV2. Keine dauerhaften Schauspieler, keine Spezies-IDs für Begegnungen, kein Habitat-/Save-Inhalt, keine zusätzliche Map. Keine allgemein wiederholbaren Importskripte aus den einmaligen Refine-Werkzeugen ableiten.
- Enton/Nebulak/Glurak verwenden eigene `PolishV4`-Darstellungsprofile. Enton erhält korrigierte Schwanz-/Bauchgewichte, Nebulak gesichtsgeschützte Gasbone-/Materialbewegung und begrenztes temporales Rand-Dithering. Gluraks neue Farbvariante verwendet exakt Originalgewichte, Original-Skeleton und alle sieben MeshyV1-Clips; stärkere Flügelanimationen und Run-Korrektur wurden nicht übernommen.
- Ausschließlich bestehendes Außen-Fülllicht `VS_SoftSkyFill` 0,65 → 1,0 nach festen QHD-Vergleichen. Sonne, SkyLight, Lichtfarben/-richtungen, Lumen, Belichtung, TAA, Bloom und adaptive private Spieleraufhellung bleiben unverändert. Innenraum bleibt unverändert. Bild-Code-Luma-Werte sind keine physikalischen Prozentwerte und keine Performanceaussage.
- Nachweise und Grenzen: `Docs/POKEMON_ANIMATIONSFEINSCHLIFF_V4_PRUEFBERICHT.md`, Teamdetails `Docs/TEAMREIHENFOLGE_V4.md`. Originalbilder, Logs und Testspielstände ausschließlich lokal unter `Saved`, nicht auf GitHub.


### Bewegungsüberarbeitung V5 – Glurak, Nebulak, Player

Historischer Stand: Die aktive Clip-/Präsentationsauswahl ist durch die unten dokumentierten V6-Korrekturen ersetzt; V5-Quellen und Rückfallassets bleiben erhalten.

Glurak und Nebulak verwenden separate `/Game/Characters/Creatures/<Name>/MotionV5`-Präsentationen; Quellen/Exporte liegen unter den bestehenden Art-Verzeichnissen. Die V4-Quellen und Assets bleiben Rückfallstände. Spezies-IDs, sieben normale Rollen und Save-Schema bleiben unverändert. Gluraks optionaler `Ground Hover` ergänzt drei eigene Clips auf dem exakten Mesh-Skeleton; bodennah 90±4 cm, kein Flug-Navigationsmodus. Visueller Ursprung trennt Lift von Bodenkapsel/Pfad. Takeoff/Land halten kurz an; Freiraumsäule und kontinuierlicher Wegsweep berücksichtigen rotierende Flügel, Decken sowie vorhandene kollisionslose Baum-/Felsdekoration. Keine Innenraum-Hover-Automatik. Battle-Visuals bekommen keinen Roaming-Kontext.

Nebulaks deckendes Originalgesicht bleibt erhalten. Die Zusatzhülle verwendet das vorhandene Effekt-Ankersystem, Mesh-Referenzkoordinaten und inverse importierte Kopf-Bind-Transformation einschließlich FBX-Skalierung; kein geratenes Bone-Offset. Eine kombinierte 2.520-Dreiecks-Hülle und getrenntes vorhandenes Gasmaterial verwenden echte Transparenz und mehrere unabhängige Materialströmungen; keine Volumen-/Lichtsimulation.

Der Player behält sein originales V2-Mesh/Skeleton. Neue Idle/Walk/Run-Clips unter `/Game/Characters/YoungTrainer/MotionV3`, Referenz 210/315 cm/s und Zyklen 0,55/0,45 s. Rein visuelle Drehbegrenzung sowie glatte Start-/Stopblends verändern keine Interaktionsrichtung, Kamera oder Eingaben. Source-IK hält Knie-/Sprunggelenk zusammen; keine Garantie vollständigen Fuß-Lockings bei engen Wendungen.

Abschluss: Development Editor Build, 94/94 Projekt-Automation ohne Testwarnungen, 11 Map Checks 0/0 und vollständiger PIE-Fußlauf mit Save-Restaurierung. Bekannte Engine-Start-/iOS-Warnungen und die unveränderten Battle-Umweltmaterial-Usage-Warnungen bleiben separat im [Prüfbericht](MOTION_REFINEMENT_V5_PRUEFBERICHT.md). Reproduzierbare Werkzeuge unter `Tools/MotionRefinementV5`; alle echten Kontrollmedien ausschließlich lokal im ignorierten `Saved/`.


## Nintendo Switch Pro Controller V1 (22.10.2026)

Bestehende Enhanced-Input-Aktionen und UMG-Kontexte werden weiterverwendet. Für das tatsächlich gelesene Apple-GameController-Backend (`Slate.MacControllerPreferGCImpl=1`) gilt B = `Gamepad_FaceButton_Right`, A = `Gamepad_FaceButton_Bottom`, X = `Gamepad_FaceButton_Left`; dies sind Framework-Tastennamen, keine Aussage über Xbox-Tastenpositionen. Der gemeinsame Helfer `PokeMonsterControllerInput` berücksichtigt den abweichenden vorhandenen Legacy-HID-Pfad ohne Umschalten des Backends. Physische B-Bestätigung im Kampf wurde vom Nutzer vorab bestätigt; alle neu ergänzten physischen Funktionen bleiben bis zur Hardwareabnahme separat offen.

B verwendet dieselbe `InteractAction` wie E/Enter. X und Tab öffnen das vorhandene Team-/Beutel-Reisebuch. L/R wechseln seine zwei Kategorien, Steuerkreuz navigiert, B wählt Quelle/Ziel für freie Teamumordnung oder ein Heilitem und anschließend ein Teamziel. A bricht zuerst die jeweilige Auswahl ab. Heilung und Verbrauch bleiben in den bestehenden Encounter-/Inventar-APIs. Plus beziehungsweise Escape in der Oberwelt öffnet die Hauptseite desselben Widgets (Team, Beutel, Speichern, Fortsetzen); Speichern verwendet den bisherigen Save-Slot und dasselbe Schema.

L3 ist ein dauerhafter, nicht im Spielstand gespeicherter Sprintmodus: an-/abschalten auch im Stand; Anhalten löscht ihn nicht. Menüs, Dialoge, Kämpfe und Innenräume pausieren nur die tatsächliche Sprintbewegung. Nach Freigabe setzt Bewegung den gewählten Modus fort. Gehen/Sprint bleiben 210/315 cm/s, Shift bleibt Haltesprint. Dies ersetzt ausdrücklich das frühere automatische Löschen des L3-Zustands beim Anhalten.

UMG fängt Bestätigen/Abbrechen bereits im Preview-Pfad vor generischer Slate-Button-Aktivierung ab. Wiederholte Bestätigungs-/Abbruch-/Kategorie-/Menütasten lösen keine zusätzlichen Kontextwechsel aus. Der Fokus kehrt nach Schließen zur Spielansicht zurück. Ein nicht konsumierender Slate-Beobachter aktualisiert Eingabehinweise und zeigt auf `pm.Input.Trace 1` rohe UE-Tastenereignisse; `0` schaltet die Diagnose ab. `pm.Input.Key`/`pm.Input.Axis` sind ausdrücklich Entwicklungssimulationen und kein physischer Controller-Nachweis.

Prüfwerkzeuge: `Tools/SwitchProControllerV1/README.md`. Tatsächliche Testergebnisse und offene Hardwaretasten: `Docs/NINTENDO_SWITCH_PRO_CONTROLLER_V1_PRUEFBERICHT.md`.


### Dauerhaft erreichbares Pokémon-Testgelände (22.10.2026)

`Development/PokeMonsterCreatureTestGround` erzeugt beim gewöhnlichen PIE-BeginPlay
der bestehenden VisualV2 automatisch einen isolierten Entwicklungsbereich mit
allen zehn vorhandenen Visuals. Die versionierte Funktion ersetzt für manuelles
Besuchen die bisher erforderliche explizite Showcase-Erzeugung. Kein neuer
Kartenstand, keine neue Gameplay-/KI-Architektur. Weitere Maps und Standalone
bleiben ausgenommen. Mittelpunkt −7500/−4000/0 cm; Zugang `pm.TestGround.Go`,
Stationen `pm.TestGround.Go 1..10`, Rückkehr `pm.TestGround.Return`. Die normale
Steuerung bleibt frei, keine Tasten werden umbelegt.

Vorhandene Präsentationen und Wanderkomponente liefern Idle/Walk/Run/Reaktionen
und Gluraks begrenztes Schweben. Reine beschriftete Test-Visuals haben weder
Encounter- noch Save-Identität. Die Laufzeitobjekte dürfen beim PIE-Ende
verschwinden; ihre automatische Verfügbarkeit beim nächsten normalen Play ist
durch die native Entwicklungsfunktion gesichert. Anleitung und Grenzen:
`Tools/CreatureTestGroundV1/README.md`.


### Animations- und Modellkorrekturen V6 (22.10.2026)

Aktive Player-Clips liegen unter `/Game/Characters/YoungTrainer/AnimationV6`, weiterhin auf dem unveränderten V2-Mesh/Skeleton. V6-Quellen sind in den bestehenden Art-Verzeichnissen separat gespeichert. 24 statt 32 cm Fußmittenabstand, vorhandene 210/315 cm/s und 0,55/0,45-s-Zyklen; Ellbogenbeugung berücksichtigt den tatsächlich abgesenkten Oberarm statt nur die Restbasis. Keine neue Cloth-Simulation und keine unbewiesene Mantel-/Hosen-Regewichtung.

Glurak, Nebulak, Machomei und Myrapla verwenden eigene `AnimationV6`-Präsentationen mit exakt kompatiblen Rest-Bones. Gluraks 90-cm-Bodenhover bleibt erhalten. Nebulaks deckender innerer Kern und restaurierte Kernflächen sind eine lokale Darstellungsreparatur. Die optionale `OverworldFloatAmplitudeCm` gehört ausschließlich zur Darstellung: Floating-Rig, 0..10 cm, nur mit vorhandenem Roaming-Kontext; eigenständige Battle-Visuals bleiben ohne Lift/Neigung.

Pikachu und Schiggy verwenden nur individuelle Oberweltüberschreibungen: 14,95/32,2 beziehungsweise 29,9/57,5 cm/s. Authored-Clipreferenzgeschwindigkeiten, Kampfwerte und Save-Schema bleiben erhalten. Das permanente Testgelände respektiert nun dieselben Artenüberschreibungen wie Wild-/Begleiterbewegung. Quellen-/Importwerkzeuge und wiederholbare Prüfungen: `Tools/AnimationCorrectionsV6/README.md`. Grenzen und Nachweise: `Docs/ANIMATIONS_UND_MODELLKORREKTUREN_V6_PRUEFBERICHT.md`.


### Animationsfeinschliff V6.1 (23.10.2026)

Player verwendet das getrennte `YoungTrainer/AnimationV61/SK_Player_V61` auf dem originalen V2-Skeleton und unveränderten V6-Idle/Walk/Run-Clips. Gezielt korrigierte Hosen-/Mantelgewichte statt Neumodellierung. Glurak verwendet ein eigenes V6.1-Mesh/Profil auf seinem exakten V6-Skeleton, alle zehn V6-Clips und Materialien bleiben dieselben. Die ergänzte Rückseitenmaske schließt die zuvor wegen fehlenden Flügel-Bone-Einflusses ausgelassenen äußeren Wurzelflächen ein.

Der bestehende Player-Animator erhält eine kleine begrenzte Zweibein-Standkorrektur über die Engine-Funktion `AnimationCore::SolveTwoBoneIK`. Bodenabfragen erfolgen ausschließlich im Game-Thread; die Poseauswertung verwendet nur vorbereitete Trefferdaten. Keine neue Animationsgraph-/Movement-Architektur. Weltkontakt wird beim starken Pivot, zu großer Korrektur, Teleport, fehlendem Boden oder langem Frameabstand freigegeben. Der gemessene Abstand der CharacterMovement-Kapsel zum Boden wird ausschließlich am visuellen Mesh ausgeglichen. `pm.PlayerFootIK 0|1` dient der reversiblen Diagnose; Standard 1. Kamera, Geschwindigkeiten 210/315 cm/s, Kapsel, Controller und Gameplay bleiben erhalten. Grenzen und tatsächliche Messungen im V6.1-Prüfbericht.

Prüfwerkzeuge: `Tools/AnimationCorrectionsV61`. Medien nur im ignorierten Saved-Verzeichnis, keine Kontrollbilder/-videos im Git. Historische V6-Quellen und Assets bleiben erhalten; erneutes Ausführen der einmaligen Import-/Aufbauwerkzeuge ersetzt keine freigegebene Aktualisierung.


### Pokémon-Fortschritt V1 (23.10.2026)

`CreatureInstance::AddExperience` verwendet weiterhin die vorhandenen Wachstumskurven und erhält fehlende KP (K.O. bleibt K.O.). Levelübergreifende Lernangebote werden stabil nach Level sortiert, gegen bereits bekannte und wartende Attacken dedupliziert und bei vollen vier Slots in `PendingMoves` gesammelt. `ResolveMoveLearning(INDEX_NONE)` lehnt genau ein Angebot ab; Slot 0–3 ersetzt ausschließlich diesen Slot mit vollen AP. Andere individuelle Werte bleiben erhalten.

Die vorhandene `BattleSession` und ihr Presenter sperren weitere Aktionen beziehungsweise den Begegnungsabschluss bis zur Lernentscheidung. Der vorhandene Moves-Bildschirm zeigt die Ersatzslots; der Zurückbutton wird zu Ablehnen. B/Enter, A/Esc und Steuerkreuz/Pfeile verwenden dieselbe zentrale Eingabezuordnung. Automatisches Lernen, XP, Level davor/danach und noch nicht implementierte Lernattacken erhalten eigene Informationsevents innerhalb derselben Präsentationsfolge.

Save-Schema **5** ergänzt `PendingMoves` als `CreatureMove`-PrimaryAssetIDs. Alte Versionen 1–4 erhalten eine leere Warteschlange; alle übrigen IDs/KP/XP/AP bleiben nach den bisherigen Regeln erhalten. Warteschlangen werden vor Austausch des Runtime-Teams vollständig validiert; doppelte, bekannte, fehlende oder zum Level unzulässige Einträge werden abgewiesen. Normalerweise entscheidet der Spieler alle Angebote vor der Rückkehr zur Oberwelt. Außerhalb eines Kampfes entstandene gespeicherte Angebote werden beim nächsten Kampf fortgesetzt; ein allgemeines Trainings-/Erinnerungsmenü ist noch offen.

`FPokeMonsterLevelMove` bleibt die einzige Lernliste. Nicht implementierte Originalattacken verwenden einen leeren Move-Verweis plus `UnavailableMoveName`/`UnavailableReason`, statt funktionslose Platzhalter-Assets zu erzeugen. Die gepinnte Gold-/Silber-Referenz und deren Rohdatenprüfsummen liegen unter `Tools/CreatureProgressionV1/Gen2Reference.json`; 102 Einträge, 68 unterschiedliche Attacken, davon 19 mit unterstützter Mechanik. Drei neue Assets liegen unter `/Game/Data/Moves/ProgressionV1` (Flamethrower, Slam, HydroPump). Keine bestehenden Originalattackenwerte wurden überschrieben. Die bestehende vereinfachte Kampfmathematik ist weiterhin keine bitgenaue Gen-2-Simulation.

`CreatureProgression::GetEvolutionOptions` ergänzt die bestehende Bedingungsprüfung um die Zustände MissingSpecies/MissingVisuals/Ready. Selbst Ready bedeutet nur verfügbare Zieldefinition und gültige Darstellung, keine ausgeführte Entwicklung. Level-, Item-, Freundschafts-, Orts- und Prüfkontexte verbrauchen nichts und ändern keine Kreatur. Fehlende Zielmodelle werden explizit gemeldet. Die historischen Zunderlauf-IDs/Basiswerte/Wachstumskurve bleiben aus Save-Kompatibilitätsgründen unverändert; ihre Originaldatenmigration ist eine getrennte offene Aufgabe.

Werkzeuge, ausdrückliche PIE-Fixtures und Grenzen: `Tools/CreatureProgressionV1/README.md`. Prüfbericht: `POKEMON_FORTSCHRITTSSYSTEM_V1_PRUEFBERICHT.md`.


## Attackenverwaltung V2 – persönliche Erinnerungen und NPC-Dienst

`FPokeMonsterCreatureInstance` erweitert die vorhandenen vier aktiven Slots um
`LearnedMoves`: eindeutige tatsächlich erlernte Attacken mit persönlichem AP-Stand.
Ersetzen bewahrt die alte Attacke; Ablehnen und offene Angebote ergänzen keine
Kenntnisse. Beim Levelaufstieg bleibt die bestehende V1-Entscheidung erhalten.
`RestoreFully` heilt auch inaktive AP. Normale Reaktivierung initialisiert AP
niemals über `AssignMove`, sondern kopiert den gespeicherten Zustand.

Save-Schema 6 ergänzte stabile Move-IDs/AP für das Repertoire. Das aktuelle Schema 7 ergänzt den validierten individuellen Schlafzähler, ohne diese Move-IDs/AP zu verändern. Alte Versionen 1–5
migrieren ausschließlich aktive Kenntnisse; vor V2 nicht gespeicherte vergessene
Attacken können nicht erfunden werden. Historische technische doppelte aktive
Slots bleiben lesbar; ihre eindeutige Erinnerung verwendet konservativ den
niedrigsten AP-Stand. Neu zusammengestellte Sets sind eindeutig, enthalten ein
bis vier erlernte Attacken und weiterhin genau vier physische Slots.

`APokeMonsterNPC::Service = RememberMoves` nutzt den vorhandenen Interactable-
Vertrag und `APokeMonsterOverworldPlayerController`. Das bestehende Reisebuch
stellt Repertoireansicht und Meisterentwurf dar. Nur eine bestätigte private
EncounterSubsystem-Transaktion darf das aktive Set neu zusammenstellen:
nahegelegener lebender Meister, gleiche Welt, kein Kampf, keine offenen Lernangebote,
seit Öffnen unveränderte individuelle Daten. Der bestehende atomare Speicherpfad
schreibt erst nach Prüfung; bei Schreibfehler wird die Laufzeitänderung zurückgenommen.
Alle übrigen Menüs bieten keinen solchen Schreibpfad. Der gewöhnliche technische
Erstellungs-/Lernhook bleibt für bestehende Factory-, Trainer- und Lernsysteme erhalten.

Die spätere Weltplatzierung ist für das versteckte optionale Wissenstal reserviert.
Mangels identifizierten spielbaren Wissensgebiets wird nur ein expliziter transienter
PIE-Test-NPC verwendet. Keine neue Map und kein dauerhafter Ersatz-NPC. Weitere
Meister und Entwicklungsprüfungen werden dadurch weder freigeschaltet noch umgesetzt.
Bedienung und Prüfanleitung: `Tools/MoveManagementV2/README.md`.


### Attackensystem V4 – gemeinsame Effektbasis (23.10.2026)

Die bestehende BattleSession wertet weiterhin ClassicBattle und WorldBattle aus. Attacken können typisierte Effektlisten kombinieren; ohne explizite Liste bleiben bestehende Effektkennungen kompatibel. Technisch geprüft sind gemeinsame Stufen, primäre Statusgrundlagen, Heilung/Absorption/Rückstoß, Fixschaden/Mehrfachtreffer und kampflokale Schutz-/Verwirrungsgrundlagen. Neue Statusprofile sind nur ausdrücklich aktivierbar; die normale Schadensformel und bisherigen Kategorien bleiben unverändert. Unfertige Effektarten werden abgewiesen.

Die 49 bisher gesperrten kanonischen Lernattacken werden durch dieses Teilpaket noch nicht produktiv freigeschaltet. Gen-2-Spezialregeln und Volltrefferfragen bleiben offen. Vollständige Architektur und Grenzen: `ATTACKENSYSTEM_V4_ARCHITEKTUR.md`; Bestand und Restpunkte: `ATTACKENSYSTEM_V4_BESTAND.md`, `ATTACKENSYSTEM_V4_WIRKUNGSPLAN.json`.


## Attackensystem V4: produktive Kristall-Anbindung (Fortsetzung)

Normale `FPokeMonsterEncounterStartData` wählen ausdrücklich `FPokeMonsterBattleEffectRules::Crystal()`. Dieselbe `UPokeMonsterBattleSession` verarbeitet ClassicBattle und WorldBattle; es gibt keine zweite Kampfauflösung. Das historische Legacy-Profil bleibt nur für bestehende gezielte Prototyptests verfügbar.

`CrystalMovePlan.json` verbindet überprüfte Kristallwerte mit 49 neuen Move-Assets unter `/Game/Data/Moves/EffectsV4`. Die bestehenden zehn Spezies erhalten ausschließlich vollständige Referenzen ihrer bisherigen 102 Lernlisteneinträge. Speziesidentitäten, Originalquellen, Präsentationen, Modelle und Oberweltparameter bleiben geschützt. `ValidateCrystalData.py` prüft diese Bindungen nach einem frischen Editorstart. Die unveränderte ursprüngliche Gen2Reference.json dokumentiert weiterhin den früheren Supportstand und wird nicht als aktuelle Freischaltungsliste missverstanden.

Mehrzügige Aktionen, Horrorblick/Feuerwirbel, Aussetzer, Groll, Wetter, Fluch und Abgangsbund gehören zum vorhandenen flüchtigen Kampfzustand. Primäre Statusprobleme und der Schlafzähler bleiben im bereits eingeführten Save-Schema 7; es ist keine weitere Save-Version notwendig. AP-Verbrauch läuft weiterhin durch die individuelle `ConsumeMovePP`-Funktion und damit durch dasselbe dauerhafte Repertoire. Menüs und Gegnerauswahl verwenden die Auswahl- und Wechselsperren der Session.

`pm.CrystalMoves.Start` ist ein expliziter, nicht gespeicherter Entwicklungsprüfaufbau mit echten produktiven Attackenassets und kontrollierten Laufzeitwerten. Er ist kein neues Habitat und keine neue Map. Vergleichsaufnahmen und QA-Prozesslogs bleiben lokal unter `Saved/MoveEffectsV4`; sie werden nicht versioniert.


## Glutexo-Integration V1 (23.10.2026)

Eigene Spezies `Glutexo`, Dex 005, 110 cm, eigenes Meshy-Rig und sieben Clips im bestehenden Kreaturenpfad. Neue Quellen/Unreal-Assets unabhängig von Glumanda/Glurak; normales VisualV2-PIE-Testgelände umfasst elf Stationen. Bestehende IDs, Save-Schema und Maps unverändert. Prüffälle und externe QA-Warnung: `GLUTEXO_INTEGRATION_V1_PRUEFBERICHT.md`.


## Pokémon-Entwicklungen V2 (23.10.2026)

Ersetzt die reine V1-Bereitschaftsanzeige für verfügbare Levelziele: `CreatureProgression::ApplyEvolution` wechselt atomar dieselbe Instanz auf eine vorhandene Route mit vollständig gültigem Zielprofil. `EncounterSubsystem` führt persistente Angebote, Abbruch, bestehendes Lernen und Save-Transaktionen am bisherigen Team aus. Glumanda/Zunderlauf ≥16 → Glutexo, Glutexo ≥36 → Glurak; kein Überspringen. Andere Trigger bleiben vorbereitete Bedingungsprüfungen.

Save-Schema **8** liest weiterhin 1–7 und ergänzt `PendingEvolutionTarget`, `LastEvolutionOfferedLevel` und optionalen individuellen Wachstumskurven-Verweis. Dieser erhält die unveränderten numerischen XP/Level historischer Glumanda bei Zielarten mit anderer Kurve. Neue eigenständige Glutexo verwenden Medium Slow. Slots, Repertoire, verbrauchte AP, Status und bestehende IDs bleiben erhalten. KP verwenden die bisherige Regel „fehlende KP erhalten, K.O. nicht wiederbeleben“.

`PokeMonsterEvolutionWidget` ist eine reversible same-world Capture-/UMG-Präsentation auf der vorhandenen Bühnenklasse, keine neue Map und keine parallele Kampflogik. Die Daten werden erst nach fünf Sekunden erfolgreich gespeichert; Vorschauwechsel und Abbruch davor sind nicht persistent. Die Präsentation V2.1 verwendet zwei getrennte Ansichten derselben transienten Bühne für eine echte Silhouettenüberblendung. Unverzerrte 16:9-Einpassung und direkt projizierte orientierte Modellgrenzen vergrößern nur die Darstellung. Nach dem unveränderten Übernahmepunkt bei 5 s verschwindet das Overlay bis 5,85 s vollständig; Happy und die Erfolgsmeldung folgen getrennt, letztere ab 7,8 s. Der vorherige Welt-Renderzustand wird nach dem vollständig deckenden Widget wiederhergestellt; Gameplay und Weltkamera laufen unverändert weiter. Ablaufzeit stammt aus der Weltzeit und wird durch zusätzliche Screenshot-Zeichnungen nicht beschleunigt. Neue Level-Lernangebote verwenden denselben individuellen Lernpfad. `pm.Evolution.Auto` ist ausschließlich ein Entwicklungsprüfgate, Standard 1. Details, tatsächliche Warnungen und Grenzen: `POKEMON_ENTWICKLUNGEN_V2_PRUEFBERICHT.md`.

## Sicherer manueller PIE-Entwicklungstest (23.10.2026)

`pm.EvolutionTest.List`, `Start <Teamplatz 1–6>` und `End` kapseln vorhandene XP-, Lern- und Entwicklungsdienste in einen expliziten Editor-/PIE-Test. Speichern und Laden verwenden währenddessen ausschließlich serialisierte RAM-Snapshots im bestehenden Save-Subsystem; der normale Slot ist auch gegen direktes Schreiben/Löschen geschützt. End stellt die ursprünglichen Sitzungsdaten wieder her, PIE-Stopp verwirft den Test. Nur die gewählte Instanz erhält Angebote; normale Builds enthalten die Befehle nicht. Alte `EvolutionReview`-Fixtures bleiben unverändert und sind allein nicht speicherisoliert. Bedienung und tatsächliche Nachweise: `ENTWICKLUNG_MANUELL_IM_PIE.md`.

## Biom-Testmap V1.1 – optionale Schwimmclips (24.10.2026)

Die bestehende CreaturePresentation erlaubt ein optionales Paar SwimIdleClip/SwimClip auf exakt demselben Skeleton mit positiver Referenzgeschwindigkeit. Ohne Paar bleibt das bisherige Verhalten erhalten; unvollständige Paare werden abgewiesen. Nur das Biom-Habitat kann einen privaten Präsentationsoverride setzen (Schiggy), ohne Spezies-/Save-Identität umzuschreiben. Schwimmhöhe und Körperfreiheit bleiben im bestehenden Habitat-/Roamingpfad; steiler Boden wird nur unter Wasser akzeptiert. Serpentine Körperlänge ist Größenmetadatum, die Kollisionshalfhöhe stammt aus tatsächlichen Meshbounds.

Der isolierte Biom-GameMode sperrt regulär Kampf-/Speicherzugriff. Seine ausdrücklich gestartete PIE-Prüffunktion schaltet zuerst den bestehenden Save-RAM-Prüftransport ein und aktiviert erst danach temporäres Gameplay. Ende restauriert den ursprünglichen RAM-Zustand und die Sperre; außerhalb Editor-PIE ist diese Funktion unwirksam. Kein zweites Speicher- oder Kampfsystem. Aktueller Zwischenbericht: BIOM_TESTMAP_V11_PRUEFBERICHT.md.

### Biom V1.1 – explizit zugeordneter Höhlenraum

Der 15-m-Testfelsen verwendet einen im vorhandenen Terrain ausgeformten Kehrenweg. Die Höhle nutzt ausschließlich BuildingCutaway.bUseRelocatedInterior innerhalb derselben Map. Ein optionaler BiomeHabitat.InteriorOwner erlaubt dem zugewiesenen Exemplar genau diesen versetzten Raum; andere Gebäude bleiben für wilde Roamer ausgeschlossen. Nur die lokale Raumdarstellung nutzt Kanal 1; Außenbeleuchtung und VisualV2 werden nicht verändert. Raumlichter werden ausdrücklich in Lumen konfiguriert. Kein neues Tür-/Kamerasystem.

### Biom V1.1 – geprüfte begrenzte Flugbereiche

Ein ausdrücklich gesetztes Aerial-Medium verwendet eine begrenzte horizontale Flughöhe über dem Habitatanker, prüft Bodenabstand und reale Körperfreiräume und verwendet weiterhin die vorhandene lokale Wegsuche, Beschleunigung und Drehung. Es ist kein allgemeines dreidimensionales Flug-/Reitsystem. Smettbo/Bibor verwenden dies nur in ihren Biom-Testbereichen. Habitak verwendet vorhandene GroundHover-Zustände; eine neue standardmäßig ausgeschaltete Habitatoption erlaubt nur im stationären Flugsegment Luftwegprüfungen über niedrigen Hindernissen. Abheben/Landen verlangen weiterhin eine freie Bodensäule. Gluraks bisherige GroundHover-Regel und alle Zonen ohne Option bleiben unverändert. MeadowPIE04 und FlightPause02 prüfen echten Überflug, sichere Landung und Kampfpausen über einer realen Kollision. Quellen, sieben Standardclips je Art und Save-Verträge aller sieben Neuarten sind geprüft. Keine universelle Flugnavigation.

Der vorhandene ausdrücklich gestartete JPEG-Spielviewport-Recorder wird zusätzlich für Dev_BiomeTestMap_V1 freigegeben, unverändert maximal 20 Hz, zwei ausstehende Schreibaufträge, reale Spielzeitstempel und nur unter Saved/. Der historische Konsolenname pm.TAAReview.CaptureStart ändert kein AA und führt keine Benchmarks aus. Damit sind tatsächliche Flugbewegungssequenzen ohne zweiten Recorder prüfbar; QHD-Vergleichsbilder bleiben separate verlustfreie Aufnahmen.

Bei wenigen festen Biom-Zielankern bleibt die Verlaufsliste auf maximal Anzahl minus zwei beschränkt; sie kann den endlichen Korridor nicht dauerhaft erschöpfen. Freie Roamer anderer Maps behalten ihre bisherige Vier-Ziele-Historie. Prüfnachweise und bewusst fehlende Lernattacken stehen im Biom-V1.1-Bericht.

### Biom V1.1 – lokale dichte Waldkamera

Ein expliziter ForestCameraZone-Actor interpoliert ausschließlich den bestehenden SpringArm-Abstand. Fester Yaw/Pitch/FOV, Inputbasis und Grundsichtkegel bleiben erhalten. Die zusätzliche obere Kronenmaske verwendet vorhandene CameraVisibility-MIDs, bekannte Eichen-/Birkenmeshes und nur private Materialien unter BiomeTestV1/DenseForestV11 als doppelten Opt-in. Außerhalb der Zone ist die zusätzliche Stärke null, Originalabstand wird exakt restauriert. Keine zusätzliche Verdeckungs-/Eingabearchitektur. Schattenpass erhält die ursprüngliche Opacity-Maske. Aktive Begegnungen pausieren die Zoneninterpolation; Übergänge und beide Kampfpräsentationen sind im PIE geprüft. Ein Actor in der Biom-Map; keine überlappenden Zonen konfiguriert.

## NPC-Präsentationsbibliothek (25.10.2026)

`UPokeMonsterNPCPresentationData` prüft Mesh/Skeleton, Rollenclips, Materialslots,
Dauer, In-place, Geschwindigkeiten und optionale Kontaktknochen. `ApplyPresentation`
ändert nur die vorhandene VisualActor-Präsentation nach vollständiger Validierung;
Gameplayquelle und Kollisionskörper bleiben zuständig. Originalmaterial kann am
Component überschrieben werden, ohne ein geteiltes Mesh umzufärben. Gespräch und
Begrüßung betreffen bei Bibliotheksprofilen den Oberkörper, Walk/Run teilen eine
Gangphase. Optionale Fußpins sind für flachen Boden, keine universelle Gelände-IK.

Profile unter `/Game/Characters/NPCs/Library/Profiles`. Drei vorhandene Humanoiden-
Skeletons und das bestehende Heilerinnenmesh werden weiterverwendet. Sieben neue
Skelettmeshes waren für die übrigen Rig-/Quellenstände nötig. Keine Doppelimporte
von Originaltexturen für die zehn bestehenden NPC-Materialien. Workflow:
`Tools/NPCExpansion/README.md`; geprüfte Quellen in `Source/*_NPCLibrary.blend`.

`UPokeMonsterNPCTestGround` existiert nur in VisualV2-PIE. Elf normale NPC-Quellen
mit rein technischem Dialog und vorhandener Präsentation, keine persistente
Questidentität. `pm.NPCGround.Go [0..11]`, `.Mode auto|idle|walk|run`, `.Greet`,
`.Return`; Mittelpunkt (-7500,3000,0) cm. Bewegung nutzt begrenzte Testziele,
Beschleunigung und echte Kapselsweeps, Randbegrenzung schützt vor Absturz.
Besuch nutzt den bestehenden PIE-RAM-Savetransport und eigenen Rückkehranker.
Andere Karten, regulärer Game-Betrieb, Shipping und Controllerbelegung unverändert.

## VisualV2 Environment Quality V3 (25.10.2026)

Ausschließlich VisualV2 bindet `/Game/Environment/VisualV2EnvironmentV3`:
private Ableitungen der bestehenden Boden-/Weg-/Fassadenmaterialien, bemalte
Steinvarianten und gealtertes Brückenholz. Originalmaterialien, andere Maps,
Gebäudemeshes, Weggeometrie und sämtliche bestehenden Kollisionen bleiben erhalten.
Drei neue opaque, gebogene Grashalm-Meshes aus einer eigenen Blenderquelle
verwenden Vertexfarben, höchstens 33 cm Ausgangshöhe und unter 1 cm Spitzenbewegung.
3.548 Grasbüschel plus 305 vorhandene Farn-/Blüten-/Wurzel-/Moos-/Kieselinstanzen
liegen in acht kollisions- und schattenfreien HISM-Gruppen mit freien Wegkorridoren.
Keine neue Blattschatten- oder Kameramethode.

Der Bach erhält beleuchtete Transluzenz mit weicher `TLM_SURFACE`-Volumenbeleuchtung,
bewegten Normalen und aktivierter Unterstützung für Bildschirmreflexionen.
Die tatsächliche Reflexionswirkung hängt von den bestehenden Qualitäts-/Renderwerten
ab. Kein Planar-Capture, keine neue Wassergeometrie, keine Brechung und keine
Übernahme der Biom-Schwimmtechnik. Die verworfene Per-Pixel-Lichtprobe zeigte
zu harte Kronensilhouetten. Vorhandenes schattenloses Außenfülllicht: 1,0 → 1,12;
Hauptlicht, Skylight, Belichtung, Innenlicht, TAA und Kameras unverändert.

Autorenquelle und Reversibilität: `Art/World/VisualV2EnvironmentV3/Scope.json`.
Prüfungen und echte lokale Bildvergleiche: `VISUALV2_ENVIRONMENT_QUALITY_V3_PRUEFBERICHT.md`.
Eine nebenbei gefundene Unity-Build-Namenskollision der vorhandenen NPC-/Kreaturen-
Testkonsolen wird durch einen eigenen C++-Namensraum der NPC-Registrierungen behoben;
Befehlsnamen, Verhalten, Rigs und Animationen bleiben gleich.

## VisualV2 Beleuchtung und Schatten V3.1 (25.10.2026)

Die V3-Außenfülllicht-Einstellung (1,12 bei Yaw 140°) ist für VisualV2 durch
V3.1 ersetzt: vorhandener Actor `VS_SoftSkyFill` / `DirectionalLight_0`, Intensität
1,8 und Yaw −45°. Pitch −40°, Temperatur 8000 K, Lichtfarbe, Kanäle, schattenloser
Betrieb und alle übrigen Eigenschaften bleiben erhalten. Keine neue Lichtquelle.
Die Ausrichtung füllt zuvor schlecht beleuchtete, kameraseitige Oberflächen;
die Hauptsonne, SkyLight, Belichtung, AO, Lumen, TAA und Kameras ändern sich nicht.
Das reduziert den wahrgenommenen Schattenkontrast; die eigentliche Schatten-
Penumbra und VSM-Filter bleiben gleich. Vorhandene Kontaktverschattung bleibt.

Die Änderung liegt nur auf einer bestehenden Lichtinstanz dieser Map, nicht in
geteilten Assets oder Projektdefaults. Andere Maps und Innenraumbeleuchtung
werden nicht umgestellt. Exakte reversible Werte: `Tools/VisualV2LightingV31/Settings.json`.
Vollständige Szene bis auf diese zwei Einstellungen, elf andere Maps und der
Save werden per Hash/Editorinventur geprüft. Bericht:
`VISUALV2_BELEUCHTUNG_SCHATTEN_V3_1_PRUEFBERICHT.md`.


## Speichersystem V2 – unabhängige Weltposition und Kontrollpunkt (26.10.2026)

Save-Schema **9** bleibt im vorhandenen nativen SaveGame-Transport und liest Versionen 1–8. `PlayerLocation` enthält Map-Package ohne PIE-Präfix, Position, Actorrotation, tatsächliche horizontale Blickrichtung und den bestehenden Innenraumkontext. `ActiveCheckpoint` bleibt unabhängig: nur ausdrückliches Aktivieren setzt ihn. Normales Speichern verändert ihn nicht; Niederlage verändert den manuellen Speicherstand nicht.

Das bestehende Hauptmenü bietet Team, Beutel, Speichern, Laden, automatischen Stand laden und Fortsetzen. Speicher-/Ladeaktionen verlangen eine gesonderte Bestätigung; A bricht ab, gehaltene beziehungsweise doppelte B-Eingaben schreiben nicht mehrfach. Tastatur und physische Nintendo-Belegung bleiben unverändert. `PMSave`/`PMLoad` bleiben Entwicklungsbefehle, normale Bedienung benötigt sie nicht.

`PokeMonster_Dev` bleibt der manuelle Slot. `PokeMonster_Recovery` enthält automatische Sicherungen nach Heilung, Niederlagenrückkehr und geprüften Lern-/Entwicklungs-/Meisterentscheidungen. Diese verwenden denselben atomaren Schreibpfad und überschreiben den manuellen Stand nicht. Beide Slots persistieren die jeweils aktuelle Position und den unabhängigen Kontrollpunkt. Automatisch laden ist eine ausdrückliche Menüentscheidung; ein normales Laden wählt immer den manuellen Slot.

Runtime-Laden validiert erst sämtliche Team-/Fortschrittsdaten und anschließend den Zielort; bei Weltwechsel bleibt das vorhandene GI-Subsystem Träger des ausstehenden Snapshots. Neue Spielfiguren sind bis Abschluss von Laden/Rückkehr gesperrt. Nach Niederlagen wird vor der automatischen Sicherung begrenzt auf stabilen Bodenkontakt gewartet. Bestehende Innenraum-/Kameradienste werden am tatsächlichen Ziel synchronisiert, keine neuen Räume oder Kameraparameter.

Alte Spielstände ohne brauchbare Position verwenden den gespeicherten, verfügbaren Kontrollpunkt oder einen kollisionsgeprüften PlayerStart. Blockierte neue Positionen werden zuerst im gleichen Innenraumkontext innerhalb 2 m gesucht, danach am gleichen Map-Kontrollpunkt beziehungsweise Start. Fehlende Maps, NaN, ungültige Blickrichtungen oder fehlender Boden führen nie zum Verlust von Teamdaten oder zu einem automatischen Überschreiben des Slots. Fehlt ein sicherer Ort vollständig, wird abgebrochen. Kampf, Dialog, aktive Entwicklungspräsentation, Türübergang und laufende Schreib-/Ladetransaktionen sperren reguläre Menüzugriffe. Vertrauenswürdige interne Entscheidungscommits sind getrennt von Menüzugriffen, bleiben aber während Kampf/Transition gesperrt.

Neue Tests nutzen `UseIsolatedPIETestSlot` ausschließlich in Editor-PIE mit festem Testpräfix; normale Builds aktivieren ihn nicht. Der vorhandene Entwicklungs-RAM-Transport bleibt erhalten. Beide schützen die kanonischen Nutzer-Slots auch gegen direkte Low-Level-Schreibaufrufe. Werkzeuge: `Tools/SaveSystemV2/README.md`; tatsächliche Ergebnisse im `SPEICHERSYSTEM_V2_LERNATTACKEN_V1_PRUEFBERICHT.md`.


## Lernattacken V1 (26.10.2026)

Fünf bestehende Speziesassets erhalten ausschließlich ihre 16 bisher unverfügbaren Kristall-Lernzeilen. 15 neue `CreatureMove`-Assets unter `/Game/Data/Moves/LearnMovesV1` nutzen die bestehende primäre Assetregistrierung, dieselben persönlichen Slots/Repertoire/AP und den vorhandenen Savevalidator. Kein weiteres Save-Schema. `BuildPlan.py` reproduziert Werte aus gepinnten Move-Rohdaten und der vorhandenen `SpeciesV11.json`; `Import.py` überschreibt keine gefüllte andere Lernzeile und prüft sämtliche geschützten Spezieseigenschaften. `Validate.py` prüft die produktive Bindung nach frischem Editorstart.

Neue Effektkennungen werden an das bestehende Enum angehängt. `ForcedMoveData`/`LastExecutedMove` sind ausschließlich flüchtige Kampfreferenzen mit GC-geschützter Aufbewahrung in derselben Session. Eine kopierte mehrzügige Attacke verbraucht nur den Spiegeltrick-Slot, keinen gegnerischen oder persönlichen kopierten AP-Slot. Bodyguard ist ein fünf Runden anhaltender Teamzustand; Wechsel setzt nur individuelle flüchtige Zustände zurück. Verfolgung verschiebt die vorhandene Wechseltransaktion hinter den abgefangenen Treffer, statt eine zweite Schadensfunktion zu erstellen. Wirbelwind nutzt einen eigenen angehängten Endgrund für Text/Outcome, keinen Sieg/XP/Fang. Besondere Kämpfe ohne Fluchtfreigabe werden nicht dadurch beendet. Trainerwechsel verlangt eine kampffähige Reserve und die vorhandene negative Zugpriorität.

32 zusätzliche native Automationfälle prüfen 15 produktive Wirkungen, 16 Levelbindungen und gemeinsame Randfälle. Die vorhandene `pm.CrystalMoves.Start`-Prüffunktion kennt zusätzlich diese produktiven Assets und fünf Lernarten. Der neue `pm.LearnMovesV1.Prepare`-Prüfaufbau existiert nur im Editor-PIE mit ausdrücklich ausgewähltem isoliertem Testtransport. Er verwendet normale XP-, Lern-, Kampf- und Savefunktionen; keine zweite Lernimplementierung. Werkzeuge und genaue Grenzen: `Tools/LearnMovesV1/README.md` und gemeinsamer Prüfbericht.


### Pokémon-KI V2: Ambient-Aktivitäten (26.10.2026)

`Creatures/Overworld/PokeMonsterCreatureActivities` enthält validierbare gemeinsame Profile und reproduzierbare gewichtete Auswahl. `PokeMonsterCreatureRoamingActivities.cpp` erweitert die existierende Wanderkomponente; kein weiterer Controller und keine zweite konkurrierende Zustandsmaschine. Aktivitätsdauer, Reisephase und Partnerreservierung gehören zum vorhandenen `BehaviorState`.

Die sechs VisualV2-Testarten werden über ihre unveränderte interne ID freigeschaltet. `bOverrideActivities`/`ActivityOverride` erlauben lokale Konfiguration. Andere Maps, Begleiter und explizite `BiomeHabitat`-Verträge sind ausgeschlossen. Die V2-Weltaktivitäten beeinflussen weder Kampfwerte noch AP, Repertoire, Speziesidentität oder Save-Schema.

Wahrnehmung: Kollisions-Broadphase im lokalen Radius, höchstens zwölf näher geprüfte Kandidaten, Art-/Zustands-/Blickrichtungsfilter und Sichtlinie. Spieler-Sichtlinien werden außerhalb unmittelbarer Nähe 0,25–0,45 Sekunden zwischengespeichert; physische Kontaktprüfung und gemeinsames Herausfordern bleiben unverändert. Paarreservierung und 20-Sekunden-Anreiselimit verhindern Endlosschleifen. Schlaf, Forage und Social haben getrennte Abklingzeiten. Entfernte Hintergrundaktivitäten werden ab 4000 cm angehalten; Niederlagenflucht läuft weiterhin.

Optionales flüchtiges `bMeasureActivityCost` misst nur während gezielter Entwicklungsprüfungen die vollständige native Komponenten-Tickzeit. Standardmäßig deaktiviert, kein Hintergrund-Profiler. Testwerkzeuge unter `Tools/PokemonAIV2`, lokale Rohdaten und echte Medien ausschließlich unter `Saved/ProjectRefinement/PokemonAIV2` beziehungsweise dem vorhandenen Framebuffer-Recorder.

Siehe Prüfbericht für genaue Aufrufe, Testaufbauten, Profile und noch fehlende Schlaf-/Nahrungssuchanimationen sowie die vorbereitete, aber noch nicht an eine Weltuhr gebundene Tagesphase.


### Pokémon-KI V2.1 / EP-Anzeige V1

`TryStartSocial` führt Anfrage, Profilprüfung, Zusage/Ablehnung und die gegenseitige
Reservierung auf dem Game Thread aus. Etablierte Ruhephasen dürfen nach
`MinimumSeconds` Besuche annehmen. Zusätzliche Einladungsfenster während Wander/Idle/Rest
liegen 8–13 s auseinander; ihre Chance folgt dem vorhandenen Sozialgewicht.
`SocialAcceptance` beträgt standardmäßig 0,85, bei Myrapla 0,70 und Nebulak 0,45.
Ablehnung unterbricht den Empfänger nicht und sperrt wiederholte Anfragen kurz.
Abstand: beide Navigationsradien + 65–95 cm, bei scheuem Partner weitere 100 cm;
Annäherungswinkel ±16°, höchstens ein geplanter Weg. Reisezeitlimit 20 s,
Gesamtlimit 30 s; Verweilen MinimumSeconds + 2–6 s. Periodische Sichtprüfung
0,8–1,2 s, kein erneutes laufendes Planen zum beweglichen Partner. Beide Partner
werden bei Unterbrechung freigegeben. Wahrnehmung bleibt lokale Broadphase mit
höchstens zwölf näher geprüften Kandidaten und vorhandener Distanzreduzierung.

`FPokeMonsterExperienceView` berechnet LevelStart/NextLevelStart, Earned/Required,
Remaining/Fraction und MAX aus existierenden Progression-Funktionen. Ungültige Daten
werden als nicht verfügbar angezeigt. OverworldView und BattlePresenter teilen
dieselbe Berechnung; der Menü-Rendercache berücksichtigt auch EP-Änderungen ohne
Levelaufstieg. Zugang: X → Team → L → Pokémon-Info → Pokémon mit B auswählen;
Tastatur Tab/Enter/Pfeile/Esc und die bisherigen Kategorien bleiben erhalten.

BattleSession-Ereignisse erfassen nur zusätzliche Vorher-/Nachher-Metadaten um die
unveränderte EP-Transaktion. PresentationPlan übernimmt diese pro Empfänger-ID.
Die bestehende BattleWidget-Präsentation animiert den Balken über reale Levelgrenzen,
auch mehrfach, ohne erneut EP zu vergeben. Die XP-Phase misst verstrichene Spielzeit,
damit mehrfach dispatchte Timer bei niedriger Bildrate nicht beschleunigen.

Prüfwerkzeuge: `Tools/PokemonAIV21ExperienceV1/`. Nur isolierte PIE-Saves, keine
Map-Speicherung. `pm.CreatureReview.CaptureLiveUI <Name> qhd` erhält die originale
Slate-Aufnahme und rendert zusätzlich die laufende PIE-/UMG-Ansicht in QHD. Die
zweite Datei ist ausdrücklich ein Live-Render und keine Desktopaufnahme.
Details und Einschränkungen: `POKEMON_KI_V2_1_EP_ANZEIGE_V1_PRUEFBERICHT.md`.

## Weltuhr V1

`Time/PokeMonsterWorldClock` ist die einzige GameInstance-Zeitquelle: Tag,
Tagessekunden, fünf konfigurierbare Phasen, Tagesfortschritt und Pauseabfrage.
Standardtag 120 Echtminuten, neuer Zustand Tag 1 09:00. Ein gefilterter
World-Pre-Tick verwendet reale Framedauer und vorhandene Gameplay-Sperren; keine
Uhr pro Map. Save-Schema 10 ergänzt das bestehende SaveGame additiv; Altstände
fallen nur bezüglich der Uhr auf den Startwert zurück. Debugbefehle sind
Editor-PIE-exklusiv und verwenden vorhandenen RAM-Speicherschutz. Die technische
Uhr V1 bleibt unverändert; Tag-Nacht V1 konsumiert ihre Werte
ausschließlich für VisualV2-Beleuchtung. KI-Anbindung bleibt offen. API,
Konfiguration und Zeitbefehle: `WELTUHR_V1.md`.

## Tag-Nacht-Beleuchtung V1 (VisualV2)

`Lighting/PokeMonsterDayNight` ist ein ausschließlich auf VisualV2 aktives
World-Subsystem. Es liest die GameInstance-Weltuhr und ihre Phasengrenzen;
kein eigener Zeitfortschritt, keine Save-Felder und keine neue Pausenlogik.
0,1-Sekunden-Timer, bei gleicher Weltzeit keine Lichtneuberechnung; `OnTimeSet`
aktualisiert nach Debugänderung/SaveLoad sofort. Bei Mapwechsel neuer
Darstellungscontroller, weiterhin dieselbe Uhr.

Vorhandenes Hauptlicht dient tags als Sonne und nachts als schwaches Mondlicht;
vorhandenes schattenloses Fülllicht bleibt die einzige zusätzliche gerichtete
Aufhellung. SkyLight, feste Belichtung, Schattenverfahren und Charakterlicht
bleiben bestehen. Eine transiente Engine-Himmelskugel erhält nur eine eigene
Materialinstanz; keine Änderungen gemeinsam genutzter Assets. Keine weiteren
dynamischen Schattenlichter, Atmosphären- oder Wetter-Simulation.

Konfiguration: `PokeMonsterDayNightSettings` in DefaultGame.ini. Mittagsmaximum
B75 oder C85, vorläufig B75; 12:00-Azimut −100°. Die endgültige visuelle Wahl
bleibt Harry vorbehalten. Editor-PIE: `pm.DayNight show|B|C|on|off`. `off`
stellt die ursprünglichen Sonnen-/Fülllichtwerte wieder her. Uhrzeit steuert
weiter ausschließlich `pm.WorldClock`. Details, Vergleich und Einschränkungen:
`TAG_NACHT_BELEUCHTUNG_V1_PRUEFBERICHT.md`.


## Rendering-Standard V5

`Rendering/PokeMonsterGraphicsProfile` bleibt die einzige Laufzeit-Profilverwaltung.
Der konfigurierte Standard `VariantC` setzt Software-Lumen + IFG (HWRT 0 / FinalGatherMethod 0)
bei QHD/High/75 %/TAAU. Die bestehenden reversiblen CVar-Scopes restaurieren
Editorwerte beim PIE-Ende und respektieren höher priorisierte Nutzer-Overrides.
`pm.Graphics HardwareSPG` setzt die 75-%-Hardware-Lumen-/SPG-Referenz (1/1),
`pm.Graphics 100` behält native 100 % mit Hardware-Lumen/SPG und ursprünglichen
Schattenwerten. Keine Save- oder Asset-Abhängigkeit. Auswahl gilt für diesen
Prozess; ein frischer Editor-/Spielprozess beginnt wieder mit C. Editor-Vorschau
außerhalb PIE wird nicht global umgestellt. Exakte Werte, Befehle und tatsächliche
Tests stehen in `RENDERING_STANDARD_V5.md`.
