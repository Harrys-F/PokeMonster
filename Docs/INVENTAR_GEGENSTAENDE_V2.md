# Inventar- und Gegenstandssystem V2 – Prüfbericht

Stand: 29.10.2026. Projekt `/Users/harry/Developer/PokeMonster`, Referenz
`/Game/Maps/Dev_TestMap_VisualV2`. Ausgangscommit
`1e8be2ecaae0a300d8fc4ad89a2743de8eb15c70` auf `main`, vor Beginn identisch mit
`origin/main`. Funktions-/Datencommit: `6622e958e5d5e94e4cca7ab2b1dcf051c2941615`. Der Bericht wird anschließend
separat gesichert. Der tatsächliche abschließende Remote-/LFS-Nachweis liegt lokal
unter `Saved/ProjectRefinement/InventoryV2/GitFinal.json` und wird im Chat gemeldet.

## 1. Ergebnis und tatsächlicher Umfang

Das bestehende Inventar ist um auswählbare Ballarten, gemeinsame Medizinwirkungen,
Sortierung, bestätigtes Wegwerfen, einmalige Questbelohnungen und zwölf dauerhafte
Weltfunde erweitert. Keine zweite Inventar-, Kampf-, Interaktions- oder
Speicherverwaltung. Der alte Trank mit ID `TestHealingItem` bleibt unverändert;
eine anfänglich angelegte eigene identische Trankkopie wurde vor der Sicherung nach
Referenzprüfung entfernt und die drei Fundreferenzen auf das vorhandene Asset gebunden.

Es gibt **29 konfigurierte Itemassets**: drei vorhandene, 25 zusätzliche
Standarddefinitionen und eine ausdrücklich technische Schlüsselitem-Fixture.
Damit stehen 26 Standarddefinitionen einschließlich des vorhandenen Tranks bereit.
Sechs davon sind Entwicklungssteine; eine vollständig visuell spielbare reguläre
Steinroute fehlt weiterhin mangels Zielarten/-modellen. Es wurden keine fehlenden
Formen, Modelle, Geschichten oder besonderen Prüfungen erfunden.

## 2. Bestandsaufnahme A/B/C

| Kategorie | Vorhandener Zustand | Maßnahme |
|---|---|---|
| A – vollständig | Individuelle Pokémon, vier aktive Attacken, Repertoire, Team, Begleiter, XP und Level | Erhalten und regressionsgeprüft |
| A – vollständig | Levelentwicklungen Glumanda 16 → Glutexo 36 → Glurak, Karpador 20 → Garados; Sequenz, Abbruch, Save-Transaktion V3 | Wiederverwendet, vollständige bestehende Abnahme erneut ausgeführt |
| A – vollständig | BattleSession, Wild-/Trainerfangverbote, technische Fangformel und Rücknahme bei ungültiger Runde | Weiterverwendet |
| A – vollständig | SaveGame 11, Migrationen, manuelle Position getrennt vom Kontrollpunkt, Weltflags | Ohne neues Format verwendet |
| A – vollständig | Questbedingungen `ItemOwned`, Weltflags, bestehende Dialog-/Custom-Aktionen | Beibehalten |
| B – teilweise | Drei Itemassets: Testfanggerät, 20-KP-Trank, Teststein | Neue belegte Daten ergänzen; alte Identitäten und Daten erhalten |
| B – teilweise | HP-Heilung und Beutel-/Teamwahl | Gemeinsame Medizin, AP-Auswahl, Beschreibungen und sichere Persistenz vervollständigt |
| B – teilweise | Mehrere Stapel, positive Mengen, Überlaufprüfungen | Gesamtmenge, Vorprüfung der optionalen Kapazität und großer Allokationen ergänzen |
| B – teilweise | Entwicklungsitem-Transaktion V3, aber keine regulären Steine | Sechs Datenassets; vorhandene Routen und Modellprüfung verwenden |
| C – fehlte | Statusheilung, Beleber, AP-Mittel, reguläre Ballauswahl | Produktiv angebunden |
| C – fehlte | Kategorienfilter, Sortierung, Mengenwahl und bestätigtes Wegwerfen | In bestehendem Widget ergänzt |
| C – fehlte | Sichtbare dauerhaft eingesammelte Weltgegenstände | Bestehendes Interaktionsinterface und zwölf Fundactors |
| C – fehlte | Einmalige gespeicherte Quest-Itembelohnung | Eine Methode am vorhandenen Questsubsystem, keine neue Quest |

## 3. Gemeinsame Architektur und Daten

`UPokeMonsterItemData` behält ID, Namen, Beschreibung, Kategorie, Icon,
Stapelgröße, Overworld-/Battle-Freigabe und das vorhandene Fanggerät.
Dazu kommen Medizinart, volle/teilweise Wiederherstellung, Statusauswahl,
Einzel-/Alle-Attacken-Ziel, Verbrauchs- und Schutzflag sowie optionale Verkaufswerte
und Weltmeshes. Keine redundanten Mengen im Asset. Verkaufswerte sind mangels
festgelegter Wirtschaft nicht erfunden; es gibt keinen neuen Shop.

Ein gemeinsamer Effektprüfer arbeitet auf der individuellen Pokémon-Instanz;
Oberwelt und BattleSession verwenden ihn. Die BattleSession berücksichtigt zusätzlich
ihren flüchtigen Verwirrungszustand. Presenter und Session teilen dessen
Zielprüfung. Erfolgloser beziehungsweise unzulässiger Einsatz verbraucht nichts.
Kampfitems belegen weiterhin einen Zug. Änderungen am Individuum bleiben auf die
beabsichtigte HP-/Status-/AP-Wirkung begrenzt.

Die bisherigen Kategorien bleiben mit ihren Enum-Identitäten erhalten:
Pokébälle, Medizin, Kampf, Entwicklung, Wichtig und Sonstiges. Keine zweite Liste
oder Änderung bestehender Kategorienummern. Mehrere physische Stapel desselben
Items erscheinen im Beutel als eine summierte Zeile. Die drei Sortierungen sind
vorhandene Reihenfolge, Kategorie und kulturabhängig verglichener Anzeigename.

Eine optionale `MaxStackSlots`-Grenze wird vor der Änderung geprüft; null erhält die
bisherige reguläre Kapazität. Eine absurde Einzelvergabe darf technisch höchstens
65.536 neue Stapel erzeugen. Das verhindert riesige Allokationen, ohne alte
Inventare beim Laden zurückzusetzen. Negative/null Mengen und int32-Überläufe
werden abgewiesen; fehlgeschlagene Vorgänge ändern keine vorhandenen Stapel.

## 4. Standardgegenstände

| Stabile ID | Deutscher Name | Max. je Stapel | Wirkung / Status |
|---|---|---:|---|
| `PokeBall` | Pokéball | 99 | Fangbonus 1× |
| `GreatBall` | Superball | 99 | Fangbonus 1,5× |
| `UltraBall` | Hyperball | 99 | Fangbonus 2× |
| `MasterBall` | Meisterball | 99 | Garantiert nur ein bereits fangbares Wildziel |
| `TestHealingItem` | Trank | 20 | 20 KP; bestehendes Asset unverändert |
| `SuperPotion` | Supertrank | 99 | 50 KP |
| `HyperPotion` | Hypertrank | 99 | 200 KP |
| `MaxPotion` | Top-Trank | 99 | Alle KP |
| `Antidote` | Gegengift | 99 | Vergiftung |
| `BurnHeal` | Feuerheiler | 99 | Verbrennung |
| `IceHeal` | Eisheiler | 99 | Einfrieren |
| `Awakening` | Aufwecker | 99 | Schlaf |
| `ParalyzeHeal` | Para-Heiler | 99 | Paralyse |
| `FullHeal` | Hyperheiler | 99 | Alle primären Statusprobleme; im Kampf auch Verwirrung |
| `Revive` | Beleber | 99 | K.O.: halbe maximale KP, abgerundet, mindestens 1 |
| `MaxRevive` | Top-Beleber | 99 | K.O.: volle KP |
| `Ether` | Äther | 99 | 10 AP für eine aktive Attacke |
| `MaxEther` | Top-Äther | 99 | Alle AP für eine aktive Attacke |
| `Elixir` | Elixier | 99 | Je 10 AP für alle aktiven Attacken |
| `MaxElixir` | Top-Elixier | 99 | Alle AP für alle aktiven Attacken |
| `FireStone` | Feuerstein | 99 | Bestehende Entwicklungsprüfung |
| `WaterStone` | Wasserstein | 99 | Bestehende Entwicklungsprüfung |
| `ThunderStone` | Donnerstein | 99 | Pikachu-Regel vorhanden, Raichu fehlt |
| `LeafStone` | Blattstein | 99 | Keine Myrapla-Abkürzung |
| `MoonStone` | Mondstein | 99 | Nur passende vorhandene Route, sonst Ablehnung |
| `SunStone` | Sonnenstein | 99 | Duflor/Blubella fehlen |

Der vorhandene `TestCaptureDevice`-Itemtyp bleibt mit seinem bisherigen
Fangbonus 1,25 erhalten; er wird nicht still zum Pokéball umbenannt.
`TestEvolutionItem` bleibt ein Teststein. Die bestehende einmalige
Entwicklungs-Testausstattung wird nicht durch eine neue reguläre Startausstattung ersetzt.
`DevelopmentInventoryKey` („Entwickler-Prüfmarke“) ist kein regulärer Fund,
Startgegenstand oder endgültiger Questinhalt.

## 5. Fang, Medizin und AP

Die technische bestehende Formel bleibt:
`clamp((Basisfangrate / 255) × ((3×MaxKP − KP)/(3×MaxKP)) × Ballbonus, 0, 1)`.
Die neue Meisterball-Eigenschaft garantiert nur einen bereits erlaubten Wildfang;
Trainer- und andere Fangverbote werden davor geprüft. Tatsächlich geworfene Bälle
werden auch bei Misserfolg verbraucht, technisch abgelehnte Runden erhalten ihren
Bestand zurück. Vier verschiedene Bälle werden durch den vorhandenen paginierten
Kampfbeutel und denselben Presenter gewählt.

Statusmittel heilen nur passende primäre Probleme. Hyperheiler beseitigt zusätzlich
Verwirrung im Kampf. Beleber sind ausschließlich für kampfunfähige Ziele zulässig,
setzen deren Status zurück und regenerieren keine AP. KP-, Status- und AP-Mittel
beleben nicht nebenbei wieder. Kein Item heilt über maximale KP/AP hinaus.

Äther und Top-Äther verlangen die Auswahl einer **aktiven** Attacke.
Elixiere bearbeiten alle aktiven Slots, nicht das gesamte inaktive Repertoire.
Deren jeweils zugehörige persönliche AP bleiben konsistent. Der dokumentierte
Sonderfall alter technischer Spielstände mit doppelten aktiven Attacken behält
unabhängige Slot-AP: Heilung darf einen anderen Slot nicht absenken; der eindeutige
Repertoireeintrag behält das konservative Minimum. Dafür gibt es einen eigenen
Grenzfall im Automationstest. Keine freie Attackenneuordnung und keine AP-Regeneration
durch Wechsel, Teamsortierung oder Entwicklung.

## 6. Entwicklungssteine und fehlende Inhalte

| Route | Tatsächlicher Stand |
|---|---|
| Pikachu → Raichu / Donnerstein | Pikachu und bestehende Itemregel vorhanden; Donnerstein jetzt vorhanden; Raichu-Daten/Modell fehlen, deshalb sichere Ablehnung |
| Evoli → Aquana / Blitza / Flamara | Incoming-Evoli ist kein spielbereit integrierter Artendatensatz; Zielarten/-modelle fehlen |
| Vulpix → Vulnona / Feuerstein | Keine vollständigen spielbereiten Quelldaten/Zielmodelle |
| Fukano → Arkani / Feuerstein | Keine vollständigen spielbereiten Quelldaten/Zielmodelle |
| Myrapla → Giflor | Keine solche Abkürzung; Myrapla behält Level 21 → Duflor |
| Duflor → Giflor / Blattstein | Duflor/Giflor fehlen |
| Duflor → Blubella / Sonnenstein | Duflor/Blubella fehlen |
| Mondstein | Definierter Gegenstand, keine erfundene verfügbare Zielroute |

Regulär vollständig spielbar bleiben die drei vorhandenen Levelentwicklungen.
Die Abnahme der Itemsequenz verwendet ausschließlich die bereits vorhandene,
ausdrücklich technische V3-RAM-Fixture Karpador/Garados/Teststein. Sie prüft
Abbruch, Wiederholung, Verlust des reservierten Bestands, Schreibfehler und
Verbrauch genau eines Items bei erfolgreichem Abschluss. Die tatsächliche
Karpador-Levelroute wird vor Testende wiederhergestellt; keine Artdatei verändert.

## 7. Bedienung im vorhandenen Beutel

- B beziehungsweise Enter: auswählen/bestätigen; A beziehungsweise Esc: zurück/abbrechen.
- Steuerkreuz auf/ab: Zeile beziehungsweise Menge wählen.
- L/R: bestehende übergeordnete Menünavigation bleibt erhalten.
- Links/rechts beziehungsweise Bild auf/ab im Beutel: Gegenstandskategorie.
- ZL/S: Reihenfolge → Kategorie → Name → Reihenfolge.
- ZR/Entf: Wegwerfen, Menge wählen, anschließend nochmals endgültig bestätigen.
- Bei AP-Einzelmitteln folgt auf die Pokémonwahl die Attackenwahl.

Die Itemliste wird innerhalb der bisherigen Menügröße paginiert. Beschreibungen,
Mengen, Sortierung und Kategorie sind sichtbar. Der ursprüngliche Zeilenaufbau
der kleinen Teamanzeige bleibt erhalten; nur neue Beschreibungen/Meldungen
werden bei Bedarf umgebrochen. Schlüsselitems und explizit geschützte Items sind
nicht wegwerfbar. Normaler Itemeinsatz, Wegwerfen und neue Funde verwenden die
vorhandene automatische Speichertransaktion; Schreibfehler nehmen die Änderung zurück.

## 8. Weltgegenstände und zwölf Fundorte

`APokeMonsterWorldItem` implementiert `IPokeMonsterInteractable`. Die vorhandene
Spieler-Zielwahl, Taste und Sichtprüfung bleiben maßgeblich; der Fundactor prüft
zusätzlich Nähe, Hindernisse, Gültigkeit und seine gespeicherte Kennung. Keine
zweite Interaktionsverwaltung. Es gibt weder Tick noch Kollision, Partikel oder
zusätzliche Lichtquellen. Die vorhandene Kiste
`/Game/Environment/WestlandAssetLibrary/Meshes/Village/SM_WLA_Crate_A` ist ausdrücklich
eine **generische Funddarstellung**, kein fertiges originales Pokémon-Itemmodell.
Ein Item kann später über sein vorhandenes neues optionales Weltmesh anders aussehen.

Eine erfolgreiche Transaktion fügt die Menge hinzu, markiert die eindeutige
Weltkennung und speichert. Erst danach wird der Fund ausgeblendet. Fehler rollen
Menge und Kennung zurück. Erneute Interaktion kann keine zweite Vergabe erzeugen.
Beim Laden wird die Sichtbarkeit ereignisgesteuert mit dem geladenen Weltzustand
abgeglichen; beim Mapwechsel übernehmen die neuen Mapactors dieselben Kennungen.

Alle IDs haben das feste Präfix `Pickup.VisualV2.V1.`; Koordinaten in cm:

| ID-Suffix | Inhalt | Item-ID | Position X, Y, Z | Prüfung |
|---|---|---|---|---|
| `Village1` | Pokéball × 2 | `PokeBall` | (-2500, -1500, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Village2` | Trank × 1 | `TestHealingItem` | (-2050, -1350, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Village3` | Gegengift × 1 | `Antidote` | (-3180, -1060, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Meadow1` | Pokéball × 1 | `PokeBall` | (-320, -700, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Meadow2` | Trank × 1 | `TestHealingItem` | (-1000, -1350, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Meadow3` | Para-Heiler × 1 | `ParalyzeHeal` | (-600, 400, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Forest1` | Pokéball × 1 | `PokeBall` | (-2550, 1400, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Forest2` | Gegengift × 1 | `Antidote` | (-4350, 1400, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Forest3` | Supertrank × 1 | `SuperPotion` | (-4000, 1800, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Forest4` | Aufwecker × 1 | `Awakening` | (750, 1900, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Pond1` | Trank × 1 | `TestHealingItem` | (-300, -1900, 1) | nativ + PIE + Kollisionsweg bestanden |
| `Pond2` | Superball × 1 | `GreatBall` | (1100, -2600, 1) | nativ + PIE + Kollisionsweg bestanden |

Verteilung: drei Dorf, drei Wiese/Wege, vier Wald/Waldrand, zwei Teichumgebung.
Kein Meisterballfund. Bestehende Actor-Transformationen wurden beim Platzieren
verglichen und erhalten. Boden- und Kapselprüfung verwarfen einen ungeeigneten
Wiesenpunkt und verschoben nur den neuen Fund um 80 cm.

In den echten nativen/PIE-Läufen wurde jeder Fund aus einer geprüften Nahposition
mit normaler Enhanced-Input-Bewegung erreicht und über die normale E-Interaktion
aufgenommen. Zwischen den Fundorten verwendete die Automation Testteleports;
das ist kein vorgetäuschter ununterbrochener Fußlauf. Zusätzlich bestätigt ein
**nur lesender Kollisionsgraph vom vorhandenen PlayerStart** alle zwölf Verbindungen:
80-cm-Raster, tatsächliches Pawn-Profil, Kapselradius 28 cm, halbe Höhe 48 cm,
8073 Bodenproben und 7700 verbundene Zellen.
Ergebnis: zwölf von zwölf erreichbar, keine Asset-/Mapänderung durch diese Prüfung.

In PIE06 nahm ein echtes wildes Pokémon einmal den normalen Interaktionsfokus ein.
Der Test fing es über den vorhandenen Meisterball-/Kampfpfad, kehrte in dieselbe
Welt zurück und nahm danach den noch unveränderten Fund auf. Keine Wild-KI,
Fangchance, Hinderniskollision oder Spawnregel wurde für den Nachweis deaktiviert.

## 9. Schlüsselitems, Quests und Dialoge

Die bestehenden `ItemOwned`-Bedingungen und Dialog-/Custom-Aktionen bleiben erhalten.
`GrantItemReward(QuestId, RewardId, Item, Quantity)` ergänzt ausschließlich das
vorhandene Questsubsystem: nur eine abgeschlossene Quest mit vorhandenem Fortschrittseintrag und eine stabile
Belohnungskennung dürfen vergeben. Die vorhandenen Weltflags speichern
`QuestReward.<QuestId>.<RewardId>`; Wiederholung und voller/ungültiger Bestand
vergaben nichts. Bei Schreibfehler bleibt die Belohnung erneut abrufbar.

Die Entwickler-Prüfmarke belegt konkrete Aufnahme, Nicht-Wegwerfbarkeit und
Save/Load eines Schlüsselitems. Es wurde keine neue fertige Quest, Geschichte,
besondere Entwicklungsprüfung oder endgültiges magisches Artefakt angelegt.
Der Belohnungshook ist für bestehende Quest-/Dialogabläufe nach deren Abschluss
verfügbar; es wird keine zusätzliche Belohnungsverwaltung eingeführt.

## 10. Speichern und Rückwärtskompatibilität

**Schema bleibt 11.** Vorhandene Mengen werden weiterhin als stabile Item-IDs und
Stapel gespeichert. Kategorien und Wirkungen stammen wie bisher aus dem Asset;
keine redundanten Kategorien-/Effektfelder im Spielstand. Fund- und Belohnungs-IDs
verwenden die bestehenden CompletedEncounterIds. Alte Stände kennen diese neuen
Kennungen nicht und finden die Gegenstände regulär vor. Migrationen 1–10 bleiben
bestehen; der vorhandene Gesamtumfang prüft diese mit.

Automatische Fortschrittstransaktionen überschreiben den normalen manuellen Slot
nicht. Laden eines älteren manuellen Standes stellt dessen Inventar und Weltzustand
zusammen wieder her, kein Mischen mit späteren Fundmengen. Kontrollpunkt,
Niederlageregel, gespeicherte Spielerposition, Blickrichtung, Innenraum,
Weltuhr und individuelle Pokémon-Daten werden nicht neu interpretiert.

Die Fehlerabnahme machte ausschließlich das eigene QA-Saveverzeichnis vorübergehend
schreibgeschützt. Medizin, Wegwerfen und Aufnahme schlugen danach korrekt fehl und
ließen die vollständigen vorherigen Mengen/Individuen/Kennungen unverändert.
Die Berechtigung wurde anschließend beziehungsweise im Fehlerpfad zurückgesetzt.
Keine vorhandene Nutzer-Savedatei wurde dafür verändert.

## 11. Tatsächlich ausgeführte Qualitätssicherung

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build `InventoryV2Build12` | Bestanden, Mac Development Editor, UE 5.8.2 |
| Finale volle Automation `InventoryV2Automation08` | 302 bestanden, 0 fehlgeschlagen, 0 Testwarnungen, 0 nicht ausgeführt |
| Strenger QA-Wrapper | **Exit 0** im finalen Lauf |
| Zwölf Map Checks, Editor04 | 12 × 0 Fehler, 0 Warnungen |
| Nativer Inventarlauf `Native06` | 168 Schritte, 42 Prüfungen, alle zwölf Funde, bestanden |
| Finaler PIE-Lauf `PIE06` | 168 Schritte, 42 Prüfungen, alle zwölf Funde, echter Wildfang dazwischen, bestanden |
| Frischer Prozess `RestartRead02` | 4 Schritte, exakte Team-/Mengen-/Fundflag-Wiederherstellung, bestanden |
| Breite native Regression `Functional01` | 76 Schritte, 22 Prüfungen, bestanden |
| Mapwechsel `Travel01` | VisualV2 → bestehende Dev_TestMap → VisualV2; Mengen/Team/Begleiter/Weltuhr/Profil und zwölf verborgene Funde erhalten |
| Bestehende Entwicklung V3 erneut | 117 Schritte, 42 Prüfungen, drei Levelrouten und technische Itemtransaktion, bestanden |
| Grobe globale Erreichbarkeit + lokale echte Bewegung | 12/12 bestanden |
| Controller | Bestehende Softwareprüfungen plus injizierte normale Eingaben; keine neue physische Controllerabnahme behauptet |

Die breite Regression umfasst normale Bewegung/Sprint, regulären Begleiter,
Modelltestgelände und Rückkehr, Wasser-Pokémon, Innenraum-/Kamerarückkehr,
Tag-Nacht-Grenzen und Mitternacht, Menüs, Kampf, Attacke, Flucht, Fang, Teamwechsel
und Save/Load. Keine Änderung der 120-Minuten-Weltuhr, Mittagssonne, KI-Profile,
Lebensräume, Namensregel oder Renderingprofile.

Neue automatische Prüfungen decken Datenidentitäten, KP/Status, Wiederbelebung,
Einzel-/Alle-AP, Repertoire und historische Doppel-Slots, Stapelgrenzen,
Schlüsselitems, vier Ballarten, Trainerfangverbot, echten BattleSession-Einsatz,
Verwirrungsheilung, Save-Transport und fehlende Stein-Zielmodelle ab.
Der bestehende UI-Test wurde um die nun verlangte Beschreibung ergänzt.

Fehlgeschlagene Vorläufe bleiben nachvollziehbar unter Saved. Beispiele:
UHT akzeptierte `INDEX_NONE` als reflektierten Defaultparameter nicht (auf −1
berichtigt); frühe Testfixtures versuchten im PIE geschützte Daten direkt zu setzen;
der Test nahm zunächst fälschlich 99 statt der bestehenden Trank-Stapelgröße 20 an.
Das waren korrigierte Build-/Teststeuerungsfehler. `Native05` wurde zudem durch
regulären Wildkontakt am Fund unterbrochen. Kein solcher Vorlauf wird als bestanden
oder als endgültiger Abnahmestand ausgegeben.

## 12. Warnungen und Infrastruktur

Testanzahl und Wrapperstatus sind von vollständiger Log-Warnungsfreiheit zu trennen.
Ein früher Lauf hatte den bekannten externen HTTP-Timeout zu
`https://www.google.com/generate_204` und Exit 1; dieser gilt nicht als bestanden.
Der finale Wrapper ist Exit 0 mit obigem tatsächlichem Ergebnis. Erwartete
Schreibfehler stammen ausschließlich aus der kontrollierten Fehlerabnahme.

Native Starts protokollieren weiterhin bekannte Engine-Experimental-Toolset-
Pythonmeldungen (`PythonTestRunner`/`ToolsetDefinition`). Editor-/Automationsstarts
enthalten außerdem bereits vor der Projekttest-Warteschlange `Condition failed`-
Meldungen des Engine-Testframeworks. Sie werden nicht zu „warnungsfreien Logs“
umgedeutet. Die ausgewerteten Abnahmeläufe haben keine Fatal-/Ensure-/Crashsignatur.
Bekannte externe iOS-Helferwarnungen werden separat betrachtet: in den ausgewerteten
finalen Logs **0 Treffer** für `Bad CPU type in executable`; keine Installation,
Ersetzung oder angebliche Reparatur des Engine-iOS-Helfers durchgeführt.

## 13. Performance – Messwerte, keine Stabilitätsbehauptung

Bestätigtes Gerät: MacBook Air `Mac16,12`, Apple M4,
16 GB, macOS 27.0.1, UE 5.8.2 Build 56702186.
Separater Development-Spielprozess, QHD 2560 × 1440, High, Profil C,
75 % TAAU (nominell 1920 × 1080 intern), Software-Lumen/IFG,
VSM vier Strahlen, VSync aus, kein FPS-Limit. Die Laufzeitwerte sind in
`Native06/Result.json` enthalten; originale Projekt-/Profilkonfiguration blieb erhalten.

Je eine kurze ca. zehnsekündige normale Messung mit aktiver Welt, ohne Videoaufnahme.
Screenshots liegen außerhalb der Messfenster. Vorrang haben echte CSV-Framezeiten;
CSV-Metadaten/-Kopfzeilen werden nicht als Frames gezählt. Threadzeiten enthalten
gegebenenfalls Warteanteile und werden nicht zu einer fiktiven Gesamtzeit addiert.

| Native06-Szenario | Ø FPS | Ø Frame ms | Frame-p95 ms | Ø GPU ms | Ø Game ms | Ø Render ms | Frames |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dorf vor Rundgang | 38.19 | 26.19 | 27.70 | 25.28 | 2.43 | 26.18 | 230 |
| Wald vor Rundgang | 39.94 | 25.03 | 27.21 | 24.17 | 2.33 | 25.03 | 229 |
| Geöffneter Beutel | 38.65 | 25.88 | 27.50 | 24.92 | 2.13 | 25.87 | 228 |
| Dorf nach zwölf Funden | 24.52 | 40.79 | 48.01 | 39.75 | 3.82 | 40.86 | 73 |
| Dorf nach Save/Load | 25.14 | 39.78 | 46.32 | 38.87 | 2.98 | 39.80 | 73 |

**Stabile 30 FPS im gesamten Ablauf sind nicht nachgewiesen.** Vor dem Rundgang
liegen diese kurzen Fenster über 30, danach darunter. Weltzeit, Populationszustand
und Laufzeitbedingungen änderten sich; das ist kein isolierter kausaler Nachweis
der Kosten der zwölf Items. Die Fundactors haben nachweislich keinen Tick,
kein zusätzliches Licht und keinen zusätzlichen Schattenwurf und keine Kollisionsblocker.

Frühere normale Fenster Native03 lagen bei ca. 32–37 FPS; ein späteres Fenster
Native05 war erheblich langsamer. Die zusätzliche GPU-Passdiagnose Native04
(`-csvGpuStats`) erreichte nur ca. 9,5 FPS und ist ausdrücklich **keine** normale
Gameplayreferenz. Die Schwankungsursache wurde in diesem Inventarauftrag nicht
als Renderingfehler identifiziert oder durch unbewiesene Grafikänderungen kaschiert.
Keine Performanceoptimierung oder allgemeine 30-FPS-Freigabe behauptet.
Rohdaten und getrennte Auswertung: `PerformanceSummary.json`, `Perf_*.csv`.

## 14. Echte Aufnahmen

Alle sieben nativen Hauptnachweise sind echte Unreal-PNGs mit bestätigten
2560 × 1440 Pixeln (`QHDProof.json`), keine generierten Bilder.
Lokal unter `Saved/ProjectRefinement/InventoryV2/Native06/`:

- [Beutel](../Saved/ProjectRefinement/InventoryV2/Native06/01_Bag.png)
- [Gegenstand / Pokémon-Zielwahl](../Saved/ProjectRefinement/InventoryV2/Native06/02_Target.png)
- [AP-Attackenauswahl](../Saved/ProjectRefinement/InventoryV2/Native06/03_PP_Target.png)
- [Fund in der Welt](../Saved/ProjectRefinement/InventoryV2/Native06/04_World_Village1.png)
- [Aufnahmemeldung](../Saved/ProjectRefinement/InventoryV2/Native06/05_Received_Village1.png)
- [Wald-Fundort](../Saved/ProjectRefinement/InventoryV2/Native06/04_World_Forest2.png)
- [Wald-Aufnahme](../Saved/ProjectRefinement/InventoryV2/Native06/05_Received_Forest2.png)

Zusätzliche echte PIE-Aufnahmen liegen unter `PIE06/`; Entwicklungsnachweise unter
`Saved/ProjectRefinement/EvolutionV3/InventoryV2EvolutionRegression01/`.
Messdateien, Testspielstände und Kontrollmedien bleiben lokal unter Saved und
werden gemäß Projektregel nicht hochgeladen. Die Links benötigen diese lokalen Dateien.

## 15. Projektschutz, Quellen und verbleibende Grenzen

Die Hashprüfung umfasst 5913 vorbestehende Projektdateien,
**553 bestehende .sav-Dateien** und **34 geschützte unversionierte Dateien**.
Keine unerwartete Änderung, keine geänderte vorhandene Savedatei, keine geänderte
geschützte Quelle. Die vorbestehende lokale `Config/DefaultEngine.ini`-Änderung
bleibt bytegleich und uncommittet. Westland/Biom-Map, Originalmodelle und die
Backup-Gitverweise bleiben erhalten. Keine neue Map, Projektkopie oder Worktree.
Eigene Prozesse wurden regulär beendet; kein Force Quit.

Verlässliche Referenzen: ausdrückliche Gen-1/2-Heilmengen des Auftrags, bestehende
Projektwerte und [öffentliche PokeAPI-Item-Metadaten](https://github.com/PokeAPI/pokeapi/blob/2bf639e5572812a67d2b94903fdcb9d095f5aeb2/data/v2/csv/item_prose.csv).
Revision, Dateien und SHA-256 stehen in `Tools/InventoryV2/ReferenceSources.json`.
[API-Dokumentation](https://pokeapi.co/docs/v2#items) beschreibt das verwendete
Itemdatenmodell. Keine ROM-Dateien, keine übernommenen fremden Spielassets.

Offen bleiben passende integrierte Stein-Zielarten/-modelle, endgültige besondere
Entwicklungsprüfungen und Questinhalte, individuelle Item-Icons/-Weltmodelle sowie
die allgemeine Framezeitstabilität. Kein Shop, keine erfundenen Preise und keine
neuen Kampfwert-Boostitems ohne belegten vorhandenen Bedarf. Controller wurde
softwareseitig, nicht erneut physisch freigegeben. Keine dieser Einschränkungen
wird als bereits fertiggestellter Inhalt ausgegeben.

Bedienung, begrenzte QA-Fixtures und Wiederholung: `Tools/InventoryV2/README.md`.
Der Featurecommit enthält nur eigene geprüfte Quellen, Daten, die gezielte
VisualV2-Erweiterung und notwendige Dokumentation. Remote und LFS werden nach dem
abschließenden normalen Push kontrolliert; keine Budget-/Zahlungsänderungen.
