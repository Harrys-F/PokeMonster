# Attackensystem V4 – Abnahme der 49 ursprünglich offenen Wirkungen

Die Architektur allein gilt nicht als Abnahme. Jede Zeile ist an ein gespeichertes produktives Asset gebunden und hat einen eigenen bestandenen Kampflogiktest. Zusätzlich wurde jede Attacke im echten ClassicBattle-PIE ausgeführt; zehn ergänzende WorldBattle-Fälle decken alle vorhandenen Pokémon ab.

Die PIE-Aufbauten verwenden echte Move-Assets und Modelle, aber kontrollierte Laufzeitwerte. Ein Treffer oder Zusatzeffekt wird aus Screenshots nicht unterstellt: Fehlschläge sind protokolliert, Wahrscheinlichkeiten und Randfälle separat automatisiert nachgewiesen. 49/49 Wirkungen sind implementiert, produktiv gebunden und automatisiert positiv beobachtet. Keine dieser 49 Gameplaywirkungen bleibt offen.

Stand: Automation 182/182, strenger Wrapper Exit 0. Die 59 PIE-Fälle stammen aus Build 10; die anschließend gezielt korrigierte Gen-2-Reihenfolge kombinierter Statusprobleme ist in Build 11 mit vollständiger Automation und zusätzlichen Regressionen abgesichert. Die nachfolgenden gemeinsamen Gameplaynachweise des Abschlussberichts erfolgen im abschließenden Build.

| Nr. | ID / Name | Gen-2-Kategorie | Stärke / Genauigkeit / AP | Wirkung | Produktiv | Automation | PIE | Offen |
|---:|---|---|---|---|---|---|---|---|
| 2 | `KarateChop` · Karateschlag | physisch | 50 / 100 / 25 | Erhöhte Volltrefferchance. | ja | bestanden | ausgeführt | nein |
| 44 | `Bite` · Biss | speziell | 60 / 100 / 25 | Kann das Ziel zurückschrecken lassen (30 %). | ja | bestanden | ausgeführt | nein |
| 50 | `Disable` · Aussetzer | Status | 0 / 55 / 20 | Blockiert die zuletzt verwendete Attacke für 2–8 Züge. | ja | bestanden | ausgeführt; Fehlschlag protokolliert | nein |
| 51 | `Acid` · Säure | physisch | 40 / 100 / 30 | Kann die Verteidigung des Ziels um eine Stufe senken (10 %). | ja | bestanden | ausgeführt | nein |
| 66 | `Submission` · Überroller | physisch | 80 / 80 / 25 | Verursacht Rückstoß in Höhe eines Viertels des verursachten Schadens. | ja | bestanden | ausgeführt | nein |
| 67 | `LowKick` · Fußkick | physisch | 50 / 90 / 20 | Kann das Ziel zurückschrecken lassen (30 %); Stärke 50 nach Kristall-Regeln. | ja | bestanden | ausgeführt | nein |
| 74 | `Growth` · Wachstum | Status | 0 / 100 / 40 | Erhöht den Spezial-Angriff um eine Stufe. | ja | bestanden | ausgeführt | nein |
| 75 | `RazorLeaf` · Rasierblatt | speziell | 55 / 95 / 25 | Erhöhte Volltrefferchance. | ja | bestanden | ausgeführt | nein |
| 76 | `SolarBeam` · Solarstrahl | speziell | 120 / 100 / 10 | Lädt einen Zug lang auf und greift dann an. Bei Sonne sofort; Regen und Sandsturm schwächen den Angriff. | ja | bestanden | ausgeführt | nein |
| 77 | `PoisonPowder` · Giftpuder | Status | 0 / 75 / 35 | Vergiftet das Ziel. Gift- und Stahl-Pokémon sind immun. | ja | bestanden | ausgeführt | nein |
| 78 | `StunSpore` · Stachelspore | Status | 0 / 75 / 30 | Paralysiert das Ziel. | ja | bestanden | ausgeführt | nein |
| 79 | `SleepPowder` · Schlafpuder | Status | 0 / 75 / 15 | Versetzt das Ziel in Schlaf. | ja | bestanden | ausgeführt | nein |
| 80 | `PetalDance` · Blättertanz | speziell | 70 / 100 / 20 | Greift 2–3 Züge lang an; danach kurz verwirrt. | ja | bestanden | ausgeführt | nein |
| 82 | `DragonRage` · Drachenwut | speziell | 0 / 100 / 10 | Verursacht genau 40 KP Schaden. | ja | bestanden | ausgeführt | nein |
| 83 | `FireSpin` · Feuerwirbel | speziell | 15 / 70 / 15 | Fesselt das Ziel für 2–5 Züge und entzieht wiederholt ein Sechzehntel seiner maximalen KP. | ja | bestanden | ausgeführt | nein |
| 84 | `ThunderShock` · Donnerschock | speziell | 40 / 100 / 30 | Kann das Ziel paralysieren (10 %). | ja | bestanden | ausgeführt | nein |
| 85 | `Thunderbolt` · Donnerblitz | speziell | 95 / 100 / 15 | Kann das Ziel paralysieren (10 %). | ja | bestanden | ausgeführt | nein |
| 86 | `ThunderWave` · Donnerwelle | Status | 0 / 100 / 20 | Paralysiert das Ziel. Gegen Boden-Pokémon wirkungslos. | ja | bestanden | ausgeführt | nein |
| 87 | `Thunder` · Donner | speziell | 120 / 70 / 10 | Kann das Ziel paralysieren (30 %). Trifft bei Regen sicher; bei Sonne ungenauer. | ja | bestanden | ausgeführt | nein |
| 93 | `Confusion` · Konfusion | speziell | 50 / 100 / 25 | Kann das Ziel verwirren (10 %). | ja | bestanden | ausgeführt | nein |
| 95 | `Hypnosis` · Hypnose | Status | 0 / 60 / 20 | Versetzt das Ziel in Schlaf. | ja | bestanden | ausgeführt | nein |
| 97 | `Agility` · Agilität | Status | 0 / 100 / 30 | Erhöht die Initiative um zwei Stufen. | ja | bestanden | ausgeführt | nein |
| 99 | `Rage` · Raserei | physisch | 20 / 100 / 20 | Wird durch gegnerische Treffer stärker, solange Raserei fortgesetzt wird. | ja | bestanden | ausgeführt | nein |
| 103 | `Screech` · Kreideschrei | Status | 0 / 85 / 40 | Senkt die Verteidigung des Ziels um zwei Stufen. | ja | bestanden | ausgeführt | nein |
| 104 | `DoubleTeam` · Doppelteam | Status | 0 / 100 / 15 | Erhöht den Ausweichwert um eine Stufe. | ja | bestanden | ausgeführt | nein |
| 108 | `Smokescreen` · Rauchwolke | Status | 0 / 100 / 20 | Senkt die Genauigkeit des Ziels um eine Stufe. | ja | bestanden | ausgeführt | nein |
| 109 | `ConfuseRay` · Konfusstrahl | Status | 0 / 100 / 10 | Verwirrt das Ziel. | ja | bestanden | ausgeführt | nein |
| 113 | `LightScreen` · Lichtschild | Status | 0 / 100 / 30 | Schützt das Team fünf Züge lang vor Spezialschaden. | ja | bestanden | ausgeführt | nein |
| 116 | `FocusEnergy` · Energiefokus | Status | 0 / 100 / 30 | Erhöht die Volltrefferstufe um eins. | ja | bestanden | ausgeführt | nein |
| 122 | `Lick` · Schlecker | physisch | 20 / 100 / 30 | Kann das Ziel paralysieren (30 %). | ja | bestanden | ausgeführt | nein |
| 130 | `SkullBash` · Schädelwumme | physisch | 100 / 100 / 15 | Erhöht beim Aufladen die Verteidigung und greift im nächsten Zug an. | ja | bestanden | ausgeführt | nein |
| 138 | `DreamEater` · Traumfresser | speziell | 100 / 100 / 15 | Wirkt nur gegen schlafende Ziele und heilt die Hälfte des verursachten Schadens. | ja | bestanden | ausgeführt | nein |
| 154 | `FurySwipes` · Kratzfurie | physisch | 18 / 80 / 15 | Trifft 2–5-mal; jeder Treffer kann ein Volltreffer sein. | ja | bestanden | ausgeführt | nein |
| 163 | `Slash` · Schlitzer | physisch | 70 / 100 / 20 | Erhöhte Volltrefferchance. | ja | bestanden | ausgeführt | nein |
| 174 | `Curse` · Fluch | Status | 0 / 100 / 10 | Geister opfern die Hälfte ihrer maximalen KP für einen Fluch. Andere Pokémon steigern Angriff und Verteidigung, verlieren aber Initiative. | ja | bestanden | ausgeführt | nein |
| 180 | `Spite` · Groll | Status | 0 / 100 / 10 | Entzieht der zuletzt verwendeten Attacke des Ziels 2–5 AP. | ja | bestanden | ausgeführt | nein |
| 182 | `Protect` · Schutzschild | Status | 0 / 100 / 10 | Schützt diesen Zug. Wiederholter Einsatz hat sinkende Erfolgschancen. | ja | bestanden | ausgeführt | nein |
| 184 | `ScaryFace` · Grimasse | Status | 0 / 90 / 10 | Senkt die Initiative des Ziels um zwei Stufen. | ja | bestanden | ausgeführt | nein |
| 193 | `Foresight` · Scharfblick | Status | 0 / 100 / 40 | Durchschaut das Ziel: erleichtert Treffer und hebt seine Geist-Immunität gegen Normal und Kampf auf. | ja | bestanden | ausgeführt | nein |
| 194 | `DestinyBond` · Abgangsbund | Status | 0 / 100 / 5 | Wird der Anwender anschließend direkt besiegt, nimmt er den Angreifer mit. | ja | bestanden | ausgeführt | nein |
| 212 | `MeanLook` · Horrorblick | Status | 0 / 100 / 5 | Verhindert Wechsel und Flucht, solange der Anwender im Kampf bleibt. | ja | bestanden | ausgeführt | nein |
| 229 | `RapidSpin` · Turbodreher | physisch | 20 / 100 / 40 | Befreit den Anwender von Egelsamen und fesselnden Wirbeln. | ja | bestanden | ausgeführt | nein |
| 230 | `SweetScent` · Lockduft | Status | 0 / 100 / 20 | Senkt den Ausweichwert des Ziels um eine Stufe. | ja | bestanden | ausgeführt | nein |
| 233 | `VitalThrow` · Überwurf | physisch | 70 / 100 / 10 | Trifft sicher, wird aber später als gewöhnliche Attacken ausgeführt. | ja | bestanden | ausgeführt | nein |
| 235 | `Synthesis` · Synthese | Status | 0 / 100 / 5 | Heilt abhängig von Tageszeit und Wetter; am Tag wirksamer. | ja | bestanden | ausgeführt | nein |
| 236 | `Moonlight` · Mondschein | Status | 0 / 100 / 5 | Heilt abhängig von Tageszeit und Wetter; nachts wirksamer. | ja | bestanden | ausgeführt | nein |
| 238 | `CrossChop` · Kreuzhieb | physisch | 100 / 80 / 5 | Erhöhte Volltrefferchance. | ja | bestanden | ausgeführt | nein |
| 240 | `RainDance` · Regentanz | Status | 0 / 90 / 5 | Lässt es fünf Züge lang regnen. Wasser wird stärker, Feuer schwächer. | ja | bestanden | ausgeführt | nein |
| 244 | `PsychUp` · Psycho-Plus | Status | 0 / 100 / 10 | Übernimmt die Statuswertstufen des Ziels. Schlägt bei unveränderten Zielwerten fehl. | ja | bestanden | ausgeführt | nein |

Alle vollständigen Assetpfade, Testnamen und lokalen Screenshotpfade stehen in `ATTACKENSYSTEM_V4_ABNAHME.json`. Details zu Projektabweichungen, Warnungen, gemeinsamen Prüfungen und Git-Sicherung stehen im Abschlussbericht. Kontrollmedien werden nicht in Git aufgenommen.
