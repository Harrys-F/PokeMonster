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

Die Berechnungsfunktionen verändern weder HP noch PP, Speziesdaten oder Progression. Die unten beschriebene Battle-Session verwendet sie für die Rundensteuerung und übernimmt PP-Verbrauch, Zugreihenfolge sowie HP-Anwendung. Es gibt weiterhin keine STAB-Boni, kritischen Treffer, zufällige Schadensstreuung, Statusveränderungen, Lernlogik, Trainer oder Kampfanimationen. Eine erste separate Battle-Testoberfläche ist unten beschrieben. Das endgültige Balancing bleibt offen.

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

Das SaveGame-Schema ist Version 3: Es speichert Quest-ID, Status und Schritt sowie gemeldete Fangarten-IDs, aber keine Questdefinition. Beim Laden werden Quest-IDs gegen registrierte Quest-Assets validiert, bevor der Runtime-Zustand ersetzt wird. Versionen 1 und 2 bleiben lesbar: Aus `Slice_Liora` und `Slice_ArchiveSeal` wird bereits belegbarer Mini-Slice-Fortschritt rekonstruiert; ein bloßes früheres Wanderer-Gespräch ist in alten Saves nicht nachweisbar und wird nicht erfunden. Version 0 und künftige unbekannte Versionen werden abgewiesen.

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

## Aktuelle feste Overworld-Kamera (09.10.2026)

Nach dem zwischenzeitlichen 2000-cm-Stand wurde der Außenabstand am 09.10.2026 auf Harrys ausdrücklichen Folgeauftrag wieder auf 2500 cm gesetzt. Die übrigen neuen Kameraparameter bleiben erhalten. `APokeMonsterPlayerCharacter` behält das vorhandene SpringArm-/CameraComponent-System: **2500 cm**, Pitch **−55°**, bestehender Yaw **−45°**, Roll **0°**, perspektivisch, FOV **35°**. Absolute SpringArm-Rotation sowie deaktivierte Controller-/Pawn- und Rotationsvererbung halten die Außenansicht unabhängig von Actorrotation und acht Sprite-Blickrichtungen fest. Keine neue diagonale Kameradrehung. `TargetOffset=(0,0,35)` cm fokussiert leicht oberhalb des Figurenmittelpunkts und platziert sie ungefähr mittig, leicht unterhalb.

Positions-Lag bleibt aktiv, mit **12** statt 6, maximal **45 cm** statt 180; Substepping **1/60 s**, kein Rotations-Lag. Kamerakollision bleibt deaktiviert, daher kein Verkürzen des Arms an Dach/Vegetation. Das löst keine grafische Verdeckung durch Baumkronen; bestehende per-building Cutaways bleiben zuständig. Keine neue Occlusion-Logik.

Bei 140 cm aufrechter Körperhöhe und 16:9 liegt die Projektion bei ungefähr 9 Prozent der Spielbildhöhe. Transparente Leinwand und Collisionhöhe dürfen nicht als Körpermaß dienen. Der Anteil hängt bei unverändertem horizontalem FOV vom Seitenverhältnis ab. Der vorhandene Blueprint-/Map-Audit findet keine Player-Blueprint-Overrides: `Dev_TestMap`, HealingHouse- und BuildingKit-Testmap verwenden den nativen Pawn über `PokeMonsterGameMode`, ohne platzierte Playerinstanzen. Keine Map-/Assetänderung ist erforderlich.

`CalculateCameraRelativeMovement` verwendet bereits die horizontale Kamerabasis: Bildschirm oben entlang Camera Forward, rechts entlang Camera Right, Diagonalen normalisiert. Die vorhandene Innenkamera-/Endpunkt-/Steuerungsanbindung bleibt unverändert; keine Drehung der Eingaben mit der Figur. Raumfeste Innenkameras behalten ihre eigenen Abstände/Winkel sowie Relocation, Fade und Bewegungsbasis-Blend. Ältere Architekturberichte und deren 2500/6/180-Angaben beschreiben historische Außenwerte. Aktuelle Prüfung: `OVERWORLD_KAMERA_2026_10_09_PRUEFBERICHT.md`.


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
