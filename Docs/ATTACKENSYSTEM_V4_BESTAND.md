# Attackensystem V4 – vollständiger Ausgangsbestand

Ausgangspunkt: `f29f6bf`. 68 kanonische Lernattacken, 19 bereits angebunden, 49 gesperrt; 22 tatsächliche Assets einschließlich drei historischer Testattacken. Die 49 gesperrten Attacken verwenden 40 verschiedene Metadaten-Effektkennungen. Diese Kennungen sind keine vollständige Gen-2-Semantik.

Die Tabelle beschreibt den unveränderten Produktionsbestand. Technische V4-Testkonfigurationen sind keine neuen freigegebenen Attackenassets. `—` bedeutet bei Statusattacken keine Schadensstärke beziehungsweise bei Selbstwirkungen keine normale Trefferprüfung; keine erfundenen Werte. Kategorien entsprechen der bisherigen projektbezogenen Einzelkategorisierung.

| ID / Attacke | Typ | Kategorie | Stärke | Genauigkeit | AP | Vorhanden / benötigte Mechanik |
|---|---|---|---:|---:|---:|---|
| `KarateChop` · Karateschlag | Kampf | Physisch | 50 | 100 | 25 | Offen: Critical – Erhöhte Volltrefferquote |
| `Scratch` · Kratzer | Normal | Physisch | 40 | 100 | 35 | Direkter Schaden ohne zusätzliche Effektkennung |
| `WingAttack` · Flügelschlag | Flug | Physisch | 60 | 100 | 35 | Direkter Schaden ohne zusätzliche Effektkennung |
| `Slam` · Slam | Normal | Physisch | 80 | 75 | 20 | Direkter Schaden ohne zusätzliche Effektkennung |
| `VineWhip` · Rankenhieb | Pflanze | Physisch | 35 | 100 | 10 | Direkter Schaden ohne zusätzliche Effektkennung |
| `Tackle` · Tackle | Normal | Physisch | 35 | 95 | 35 | Direkter Schaden ohne zusätzliche Effektkennung |
| `TailWhip` · Rutenschlag | Normal | Status | — | 100 | 30 | Produktiv: DefenseDown |
| `Leer` · Silberblick | Normal | Status | — | 100 | 30 | Produktiv: DefenseDown |
| `Bite` · Biss | Unlicht | Physisch | 60 | 100 | 25 | Offen: Flinch – Zurückschrecken als sekundärer Effekt |
| `Growl` · Heuler | Normal | Status | — | 100 | 40 | Produktiv: AttackDown |
| `Disable` · Aussetzer | Normal | Status | — | 55 | 20 | Offen: Disable – Zuletzt eingesetzte Attacke zeitweise sperren |
| `Acid` · Säure | Gift | Speziell | 40 | 100 | 30 | Offen: Stage – Säure: Verteidigung -1, 10 % in Gen 2 |
| `Ember` · Glut | Feuer | Speziell | 40 | 100 | 25 | Produktiv: Burn |
| `Flamethrower` · Flammenwurf | Feuer | Speziell | 95 | 100 | 15 | Produktiv: Burn |
| `WaterGun` · Aquaknarre | Wasser | Speziell | 40 | 100 | 25 | Direkter Schaden ohne zusätzliche Effektkennung |
| `HydroPump` · Hydropumpe | Wasser | Speziell | 120 | 80 | 5 | Direkter Schaden ohne zusätzliche Effektkennung |
| `Submission` · Überroller | Kampf | Physisch | 80 | 80 | 25 | Offen: Recoil – Rückstoß relativ zum tatsächlich verursachten Schaden |
| `LowKick` · Fußkick | Kampf | Physisch | 50 | 90 | 20 | Offen: Flinch – Zurückschrecken als sekundärer Effekt |
| `SeismicToss` · Geowurf | Kampf | Physisch | — | 100 | 20 | Produktiv: UserLevelDamage |
| `Absorb` · Absorber | Pflanze | Speziell | 20 | 100 | 20 | Produktiv: DrainHalf |
| `LeechSeed` · Egelsamen | Pflanze | Status | — | 90 | 10 | Produktiv: LeechSeed |
| `Growth` · Wachstum | Normal | Status | — | — | 40 | Offen: Stage – Wachstum: Spezial-Angriff +1 in Gen 2 |
| `RazorLeaf` · Rasierblatt | Pflanze | Physisch | 55 | 95 | 25 | Offen: Critical – Erhöhte Volltrefferquote |
| `SolarBeam` · Solarstrahl | Pflanze | Speziell | 120 | 100 | 10 | Offen: Charge – Aufladen und Angriff in Folgerunde |
| `PoisonPowder` · Giftpuder | Gift | Status | — | 75 | 35 | Offen: PrimaryStatus – Vergiftung |
| `StunSpore` · Stachelspore | Pflanze | Status | — | 75 | 30 | Offen: PrimaryStatus – Paralyse |
| `SleepPowder` · Schlafpuder | Pflanze | Status | — | 75 | 15 | Offen: PrimaryStatus – Schlaf |
| `PetalDance` · Blättertanz | Pflanze | Speziell | 70 | 100 | 20 | Offen: Rampage – Mehrere erzwungene Angriffsrunden, anschließend Verwirrung |
| `DragonRage` · Drachenwut | Drache | Speziell | — | 100 | 10 | Offen: FixedDamage – 40 feste KP, Typimmunität bleibt erhalten |
| `FireSpin` · Feuerwirbel | Feuer | Speziell | 15 | 70 | 15 | Offen: Trap – Bindung mit wiederkehrendem Schaden |
| `ThunderShock` · Donnerschock | Elektro | Speziell | 40 | 100 | 30 | Offen: PrimaryStatus – Sekundäre Paralyse |
| `Thunderbolt` · Donnerblitz | Elektro | Speziell | 95 | 100 | 15 | Offen: PrimaryStatus – Sekundäre Paralyse |
| `ThunderWave` · Donnerwelle | Elektro | Status | — | 100 | 20 | Offen: PrimaryStatus – Paralyse |
| `Thunder` · Donner | Elektro | Speziell | 120 | 70 | 10 | Offen: WeatherAndStatus – Donner: Wetter/Genauigkeit und Paralyse |
| `Confusion` · Konfusion | Psycho | Speziell | 50 | 100 | 25 | Offen: Confusion – Sekundäre Verwirrung |
| `Hypnosis` · Hypnose | Psycho | Status | — | 60 | 20 | Offen: PrimaryStatus – Schlaf |
| `Agility` · Agilität | Psycho | Status | — | — | 30 | Offen: Stage – Initiative +2 |
| `QuickAttack` · Ruckzuckhieb | Normal | Physisch | 40 | 100 | 30 | Direkter Schaden ohne zusätzliche Effektkennung |
| `Rage` · Raserei | Normal | Physisch | 20 | 100 | 20 | Offen: Rage – Raserei: Steigerung bei eingehendem Schaden |
| `NightShade` · Nachtnebel | Geist | Speziell | — | 100 | 15 | Produktiv: UserLevelDamage |
| `Screech` · Kreideschrei | Normal | Status | — | 85 | 40 | Offen: Stage – Verteidigung -2 |
| `DoubleTeam` · Doppelteam | Normal | Status | — | — | 15 | Offen: Stage – Ausweichwert +1 |
| `Smokescreen` · Rauchwolke | Normal | Status | — | 100 | 20 | Offen: Stage – Genauigkeit -1 |
| `ConfuseRay` · Konfusstrahl | Geist | Status | — | 100 | 10 | Offen: Confusion – Verwirrung |
| `Withdraw` · Panzerschutz | Wasser | Status | — | — | 40 | Produktiv: DefenseUp |
| `LightScreen` · Lichtschild | Psycho | Status | — | — | 30 | Offen: Screen – Zeitweiser Spezialschutz des Teams |
| `FocusEnergy` · Energiefokus | Normal | Status | — | — | 30 | Offen: CriticalFocus – Erhöhte Volltrefferstufe |
| `Lick` · Schlecker | Geist | Physisch | 20 | 100 | 30 | Offen: PrimaryStatus – Sekundäre Paralyse |
| `SkullBash` · Schädelwumme | Normal | Physisch | 100 | 100 | 15 | Offen: ChargeAndStage – Schädelwumme: Aufladen mit Verteidigungsanstieg |
| `DreamEater` · Traumfresser | Psycho | Speziell | 100 | 100 | 15 | Offen: DrainAndCondition – Absorption nur gegen schlafendes Ziel |
| `Bubble` · Blubber | Wasser | Speziell | 20 | 100 | 30 | Produktiv: SpeedDown |
| `FurySwipes` · Kratzfurie | Normal | Physisch | 18 | 80 | 15 | Offen: MultiHit – 2–5 Treffer mit kontrollierter Verteilung |
| `Slash` · Schlitzer | Normal | Physisch | 70 | 100 | 20 | Offen: Critical – Erhöhte Volltrefferquote |
| `Curse` · Fluch | ??? · Gen-2-Regelfrage | Status | — | — | 10 | Offen: Curse – Typabhängige Fluchwirkung |
| `Spite` · Groll | Geist | Status | — | 100 | 10 | Offen: Spite – AP der zuletzt eingesetzten Attacke reduzieren |
| `Protect` · Schutzschild | Normal | Status | — | — | 10 | Offen: Protect – Rundenschutz mit sinkender Folgechance |
| `ScaryFace` · Grimasse | Normal | Status | — | 90 | 10 | Offen: Stage – Initiative -2 |
| `Foresight` · Scharfblick | Normal | Status | — | — | 40 | Offen: Identify – Treffer/Geist-Immunität gezielt beeinflussen |
| `DestinyBond` · Abgangsbund | Geist | Status | — | — | 5 | Offen: DestinyBond – Verknüpfte Ohnmacht unter Bedingungen |
| `MeanLook` · Horrorblick | Normal | Status | — | — | 5 | Offen: PreventSwitch – Flucht/Wechsel des Gegners verhindern |
| `RapidSpin` · Turbodreher | Normal | Physisch | 20 | 100 | 40 | Offen: ClearBindings – Turbodreher: Schaden und Befreiung |
| `SweetScent` · Lockduft | Normal | Status | — | 100 | 20 | Offen: Stage – Ausweichwert -1 in Gen 2 |
| `VitalThrow` · Überwurf | Kampf | Physisch | 70 | — | 10 | Offen: NeverMissAndPriority – Überwurf: garantierter Treffer mit später Priorität |
| `Synthesis` · Synthese | Pflanze | Status | — | — | 5 | Offen: WeatherHeal – Wetter-/tageszeitabhängige Heilung |
| `Moonlight` · Mondschein | Normal | Status | — | — | 5 | Offen: WeatherHeal – Wetter-/tageszeitabhängige Heilung |
| `CrossChop` · Kreuzhieb | Kampf | Physisch | 100 | 80 | 5 | Offen: Critical – Erhöhte Volltrefferquote |
| `RainDance` · Regentanz | Wasser | Status | — | — | 5 | Offen: Rain – Regen über mehrere Runden |
| `PsychUp` · Psycho-Plus | Normal | Status | — | — | 10 | Offen: CopyStages – Statuswertstufen des Gegners kopieren |
| `TestNormalPhysical` · TestNormalPhysical | Historische Testdaten | <PokeMonsterMoveCategory.PHYSICAL: 0> | 40 | 100 | 35 | Technischer Altbestand, kein kanonischer Lernlisten-Neuzugang |
| `TestFireSpecial` · TestFireSpecial | Historische Testdaten | <PokeMonsterMoveCategory.SPECIAL: 1> | 50 | 95 | 25 | Technischer Altbestand, kein kanonischer Lernlisten-Neuzugang |
| `TestStatus` · TestStatus | Historische Testdaten | <PokeMonsterMoveCategory.STATUS: 2> | 0 | 100 | 20 | Technischer Altbestand, kein kanonischer Lernlisten-Neuzugang |

## Quellen und Regelgrenzen

- Unveränderte GS-Lernlisten und numerische Metadaten: [PokeAPI, fester Stand `2bf639e5572812a67d2b94903fdcb9d095f5aeb2`](https://github.com/PokeAPI/pokeapi/tree/2bf639e5572812a67d2b94903fdcb9d095f5aeb2/data/v2/csv), lokal `Tools/CreatureProgressionV1/Gen2Reference.json` mit Quellenprüfsummen.
- Tatsächliche Assets: lesender Unreal-Inventarlauf `Saved/MoveEffectsV4/AssetsBefore.json`; pro Asset im begleitenden Bestands-JSON dokumentiert.
- [Ursprüngliche Gen-2-Effektzuordnung](https://github.com/pret/pokecrystal/blob/master/data/moves/moves.asm): insbesondere Säure → Verteidigung, Wachstum → Spezial-Angriff, Lockduft → eine Ausweichstufe; moderne Effektnummern allein reichen nicht. Keine ROM-Dateien oder fremden visuellen Assets übernommen.
- Die vorhandene Projektformel enthält bewusst keinen STAB, keine Volltreffer und keine Schadensstreuung. Diese Abweichung bleibt erhalten. Erhöhte Volltrefferquoten werden nicht durch gewöhnlichen Schaden als vermeintlich vollständig ersetzt.
- Noch offene Generationenfrage: neue Status-/Spezialwirkungen nach Gold/Silber unter Beibehaltung der bisherigen Kategorien und Schadensformel, oder ausschließlich bereits ausdrücklich festgelegte Regeln. Kein ausbleibender Antworttext wird als Freigabe behandelt.
- Vollständige Restpunkte je Attacke: `ATTACKENSYSTEM_V4_WIRKUNGSPLAN.json`.
