# PokeMonster – Kampfsystem V3: Prüfbericht

Stand: 20.10.2026. Ausschließlich `/Users/harry/Developer/PokeMonster`.
Ausgangspunkt: `a966553e2e59e2cdb4a98e3830ad863d06365d7c`, main = origin/main,
keine fremden Änderungen versionierter Dateien, 58 geschützte unversionierte Dateien.

## Ergebnis

Flucht, Heilitems im Kampf, Glumandas drei belegte Gen-2-Startattacken,
Angriffssenkung/Verbrennung, Kampf-XP und ein AP-Notfallzug sind in die bestehende
BattleSession integriert. ClassicBattle und WorldBattle verwenden dieselben Regeln,
dasselbe Inventar und dieselbe persistente Teamverwaltung. Bestehende Wechsel-,
Fang-, Checkpoint-, Heil- und Save-Funktionen wurden überprüft und erhalten.
Keine neue Map, Kreatur, Kampflogik oder Änderung an Oberwelt, Heilhaus und Sichtkreis.

Editor-Build erfolgreich, 68/68 Automationstests ohne Testwarnungen, neun gezielte
PIE-Kampffälle, alle elf Map Checks ohne Fehler/Warnungen und vollständiger
102-Schritte-Gameplay-Fußlauf erfolgreich. Der physische Switch-Pro-Test wurde
**nicht durchgeführt und nicht als Abschlusskriterium verlangt**.

## Flucht

Normale, ausdrücklich erlaubte Wildbegegnungen nutzen aktuelle Geschwindigkeiten
und Folgeversuche. Bei eigener Geschwindigkeit >= Gegner erfolgt sichere Flucht,
sonst wird der dokumentierte Gen-1/2-Schwellenwert gegen einen Seed-Zufallswert
0–255 geprüft. Division durch null ist abgefangen. Erfolgreiche Flucht beendet
vor einem Gegnerangriff, stellt Oberwelt/Kamera/Eingaben wieder her und setzt
keinen Sieg-/Fangflag. Fehlschlag verbraucht den Zug, Gegnerattacke und gegnerische
AP werden regulär verarbeitet. Andere Aktionen setzen den Versuchszähler zurück;
dies ist die ausdrücklich dokumentierte Projektregel, keine bitgenaue Gesamtadaption.

Trainerkämpfe sowie Test-/Story-Skripte verweigern Flucht zentral und im Menü.
Im echten langsamen PIE-Fall: Schwelle 30, Zufallswert 253, Fehlschlag, danach
Gegnerattacke; nach weiteren Versuchen in Runde 3 entkommen. Bei gleich schneller
oder schnellerer eigener Kreatur Erfolg ohne Gegnerattacke. Seed-Tests prüfen
beide Ergebnisse sowie zurückgewiesene Aktionen ohne Rundenfortschritt.
[Formelreferenz](https://bulbapedia.bulbagarden.net/wiki/Escape).

## Beutel und Heilung

Das bestehende `UPokeMonsterInventorySubsystem` bleibt einzige Bestandsquelle.
Der Beutel listet tatsächlich verfügbare Heilitems und das vorhandene Fanggerät.
Bei mehr als drei Heilitem-Typen wird geblättert. Nach Itemauswahl folgt die
Team-Zielwahl; Zurück verwirft die Auswahl ohne Verbrauch. Auch das aktive
Mitglied und inaktive Teammitglieder können Ziele sein. Volle KP, K.O., ungültiger
Index, fehlender Bestand und nicht erlaubte Itemtypen werden abgewiesen.

Der bisherige `DA_TestHealingItem` heißt spielerseitig **Trank**, behält stabile ID,
Überweltverwendung und seine schon definierte Wirkung von 20 KP. Keine neue
Itembalance oder automatisch hinzugefügter Produktionsvorrat. Gültige Verwendung
verbraucht genau ein Item und den Zug; danach handelt der Gegner gegen die aktive
Kreatur. Heilen wird auf Max-KP begrenzt. Bei abgewiesener Auflösung werden die
ursprünglichen Inventarstapel wiederhergestellt. SaveGame verwendet weiterhin
dieselben Item-IDs/Mengen. Ein Trank heilt keine Verbrennung und belebt nicht wieder.

PIE-Beispiele: inaktives Teammitglied +6 bis volle 29 KP, aktives Mitglied +19 bis
volle 29 KP; jeweils genau ein Trank weniger. Kein falscher Sprung des aktiven
KP-Balkens bei Heilung eines inaktiven Ziels. Textüberlauf im Beutel behoben.

## Verifizierte Glumanda-Daten

| Attacke | Erlernt ab | Typ/Kategorie | Stärke | Genauigkeit | AP | Wirkung |
|---|---:|---|---:|---:|---:|---|
| Kratzer | Start/1 | Normal, physisch | 40 | 100 % | 35 | Schaden |
| Heuler | Start/1 | Normal, Status | 0 | 100 % | 40 | Angriff −1 Stufe |
| Glut | 7 | Feuer, speziell | 40 | 100 % | 25 | Schaden, 10 % Verbrennung |

Gen-2-Lernstand, nicht moderne Lernlevel. Level 10 hat drei Attacken, Slot 4 bleibt
leer. Neue Wild-Glumanda aus dem bestehenden Level-5–7-Profil erhalten die Liste
passend zum tatsächlich gewürfelten Level. Die nächsten Attacken und vollständige
Lernlisten sind nicht Bestandteil dieses kleinen geprüften Datenumfangs.
[Gold/Silver-Datenquelle](https://www.serebii.net/pokedex-gs/004.shtml).

Heuler wirkt im selben Zug auf einen nachfolgenden physischen Gegnerangriff;
Grenze −6, Rücksetzung bei Wechsel. Im PIE-Beispiel sinkt der Folgeschaden von
7 auf 5 KP. Die Statusattacke zeigt keinen erfundenen Schaden an.
[Heuler-Referenz](https://bulbapedia.bulbagarden.net/wiki/Growl_(move)).

Verbrennung halbiert physischen Angriff und verursacht max(1,MaxKP/8) Restschaden.
Glut kann Feuertypen nicht verbrennen. Vorhandene Heilpunkte entfernen die
Verbrennung. Restschaden besitzt eigene Ereignisse/Präsentation und kann K.O.
auslösen. Reihenfolge an Kampf-/Wechselgrenzen bleibt die dokumentierte
vereinfachte Projektauflösung; keine Behauptung sämtlicher Gen-2-Sonderfälle.
[Verbrennungsreferenz](https://bulbapedia.bulbagarden.net/wiki/Burn_(status_condition)).

Bei erschöpften AP steht **Verzweifler** ohne zusätzlichen Lernslot zur Verfügung:
Stärke 50, typneutral, Rückstoß max(1,verursachter Schaden/4). Gelernte AP werden
nicht aufgefüllt. Dies beseitigt die bisherige Bedienungssackgasse auch auf
Gegnerseite. [Gen-2-Daten](https://www.serebii.net/attackdex-gs/struggle.shtml).

## Animationen, Teamwechsel und Kampfende

Vorhandene Attack-/Hit-/Faint-/Happy-Clips bleiben erhalten. Glut erhält einen
kleinen prozeduralen Flame-Sprite während der Projektilphase, ohne neue dynamische
Weltlichter oder teures Partikelsystem. Schwanzflammen bleiben in allen Abläufen
am vorhandenen Anker. Heilung, Flucht und XP lösen keine falsche Attackenanimation
aus. KP-Verlust und aktive Heilung werden interpoliert; Status und Rückstoß haben
zugeordnete Texte. Kein zweites Schadenssystem in der Oberfläche.

Freiwilliger Wechsel verbraucht einen Zug; der Gegner trifft das eingewechselte
Mitglied. Nach K.O. muss ein kampffähiger Ersatz gewählt werden, ohne zusätzlichen
Gegnerzug. Gegnerersatz bleibt automatisch. Beim vollständigen Teamverlust erfolgt
der bestehende Checkpoint-/PlayerStart-Rückweg mit HP/AP-/Statusheilung und wieder
freigegebenen Eingaben. Keine Rückerstattung bereits verbrauchter Items.

Kampf-XP werden nur für besiegte Gegner mit verifiziertem Ertrag vergeben, auf
lebende beteiligte Teammitglieder verteilt. Glumanda: historischer Basisertrag 65,
bestehende Wachstumskurve, Trainerfaktor 1,5. Getrennte ganzzahlige Rundung gemäß
Projektformel, keine Behauptung bitgenauer Original-XP-Arithmetik. Im Wild-PIE-Fall
mit Level-10-Gegner und einem Beteiligten: 92 XP. Levelaufstieg sowie Erlernen von
Glut beim Übergang 6→7 sind automatisiert geprüft. Keine Fang-/Flucht-XP.
Unbekannte Erträge anderer Testarten bleiben 0, statt Endwerte zu erfinden.
[Ertragsreferenz](https://bulbapedia.bulbagarden.net/wiki/Charmander_(Pok%C3%A9mon)),
[XP-Hintergrund](https://bulbapedia.bulbagarden.net/wiki/Experience).

## Spielstände und Schutz

Schema 4 ergänzt nur den persistenten Status. Alte Versionen 1–3 bleiben lesbar.
Bekannte technische Glumanda-Loadouts werden begrenzt migriert; Instanz-ID,
Level, KP und XP bleiben erhalten, verbrauchte AP werden den jeweiligen neuen
Attacken zugeordnet und gegebenenfalls bei deren neuer Kapazität begrenzt.
Eigene/gemischte Attackenlisten werden nicht pauschal überschrieben. Alle alten
Testassets und Primary-Asset-IDs bleiben erreichbar. Kampf-Snapshots bleiben
weiterhin verboten; gespeichert wird der konsistente Oberweltstand.

Der Dev-Spielstand ist nach allen Tests bytegleich wiederhergestellt:
`d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.
58 geschützte unversionierte Dateien, elf Mapdateien und 1.388 Art-/Kreaturen-
Präsentationsdateien unverändert. Beide Vollbackup-Refs zeigen weiterhin auf
`03492bd96b4dba44692f675c19d5f11abfa86b4b`; dieser Commit ist kein Vorfahr von main.
LFS-Objekte von main und Vollbackup wurden lokal mit `git lfs fsck --objects` geprüft.

## Tatsächliche Tests

| Prüfung | Ergebnis / Nachweis |
|---|---|
| Mac Development Editor Build | erfolgreich, `Saved/ProjectRefinement/BattleV3Build08/Result.json` |
| Vollständige Automation | 68 erfolgreich, 0 mit Warnung, 0 fehlgeschlagen, 0 ausgelassen; `BattleV3Automation05/Report` |
| Neue V3-Testgruppen | Flucht; Heiltransaktion; Heuler/Verbrennung/AP; Gen-2-Daten; XP/Wechsel; Save-Migration/Status; AP-Erschöpfung |
| Gezielt ClassicBattle | Wild, Trainer, gescheiterte Flucht, erzwungener Wechsel, Sieg, AP-Erschöpfung bestanden |
| Gezielt WorldBattle | Wild, gesperrte Storyflucht, vollständige Niederlage bestanden |
| Echte Menüeingaben | Enter/Escape und logische Nintendo-A/B-Ereignisse über Slate; keine Hardwarebehauptung |
| Alle vorhandenen Maps | 11 geladen, jeweils 0 Fehler / 0 Warnungen; `Saved/BattleSystemV3/MapCheckResults.json` |
| Vollständiger Gameplay-Fußlauf | 102 Schritte, 287,47 m; Kampf/Fang, Teamwechsel, Quests/Dialoge, Heilhaus, Save/Load, Sprint, Außen-/Innenkamera bestanden |
| Dev-Spielstand | bytegleich wiederhergestellt, `Saved/GlumandaV11/Acceptance/FinalBattleSystemV3/SaveRestored.json` |
| Schutz-/Datenprüfung | bestanden, `FinalProtection.json` / `DataValidation.json` |
| Git-Diff und Index | `git diff --check` / `git diff --cached --check` bestanden, explizite 45-Pfade-Liste |

Die ersten Prüfungen deckten zwei bestehende C++-Buildprobleme auf (Headerreihenfolge
und Namenskollision im Unity-Build); beide behoben. Alte Testassertionen zu
Platzhalterstatus, AP-Sperre und Save-Version 3 wurden an den neuen expliziten
Funktionsstand angepasst, nicht deaktiviert. Ein erster Review-Harness versuchte
nach bereits beendeter Flucht nochmals einen Zug; seine Wartebedingung wurde
korrigiert. Anschließend neun echte Fälle zweimal erfolgreich. Die Schlussdurchsicht
hat außerdem die Abweisung ungültiger Null-Angriffswerte abgesichert und getestet.

Bekannte Engine-Startmeldungen zu Toolsets/Automation-Bedingungen sowie zum nicht
lauffähigen alten iOS-Hilfsprogramm `idevice_id` bleiben in den Originallogs erhalten.
Ein früherer Testlauf enthielt eine asynchron zugeordnete HAL-Warnung; der letzte
vollständige Lauf hat keine Testwarnungen. Kein Verschweigen oder Unterdrücken.
Keine FPS-Benchmarks, umfangreichen GPU-Profile oder physischen Controller-Schleifen.

## Echte Screenshots

Ausschließlich echte Slate-Spielviewport-Aufnahmen aus PIE, kein Konzeptbild und
kein Offscreen-Widget-Render. Angeforderte RHI-Größe 2560×1440; die tatsächlich
aufgenommenen finalen Slate-Bilder sind **2331×1311**, deshalb kein QHD-Nachweis.
Die Bilder bleiben ausdrücklich lokal im ignorierten Saved-Ordner, werden nicht
auf GitHub hochgeladen. 45 finale Bilder unter `Saved/BattleSystemV3/LiveUI` mit
Präfix `BattleV3_Review03_`. Folgende Auswahl zeigt die relevanten Funktionen:

### Attacken mit freiem viertem Slot

2331 × 1311 Pixel.

![Attacken mit freiem viertem Slot](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_2_Moves/ActualSlateViewport.png)

### Beutel mit Trank

2331 × 1311 Pixel.

![Beutel mit Trank](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_0_Bag0/ActualSlateViewport.png)

### Glut während der Angriffsphase

2331 × 1311 Pixel.

![Glut während der Angriffsphase](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_0_EmberTravel/ActualSlateViewport.png)

### Fehlgeschlagene Flucht

2331 × 1311 Pixel.

![Fehlgeschlagene Flucht](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_4_FleeResult/ActualSlateViewport.png)

### Notwendiger Teamwechsel

2331 × 1311 Pixel.

![Notwendiger Teamwechsel](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_5_ForcedSwitch/ActualSlateViewport.png)

### WorldBattle mit unveränderter Weltkamera

2331 × 1311 Pixel.

![WorldBattle mit unveränderter Weltkamera](/Users/harry/Developer/PokeMonster/Saved/BattleSystemV3/LiveUI/BattleV3_Review03_1_Commands/ActualSlateViewport.png)

## Dateien und GitHub

Neue Attacken: `/Game/Data/Moves/DA_Scratch`, `DA_Growl`, `DA_Ember`.
Gezielt geänderte vorhandene Datenassets: `/Game/Data/Creatures/DA_Zunderlauf`,
`/Game/Data/Encounters/DA_Zunderlauf_Wild`, `/Game/Data/Items/DA_TestHealingItem`.
Zusammen sechs LFS-Objekte mit exakt **13.689 Bytes** neuer Nutzlast. Keine
Modell-/Rig-/Animations-/Material- oder Map-Binärdatei geändert.

Quellen: bestehende `Battle`, `UI`, `Creatures`, `Encounter`, `Save` erweitert;
sieben V3-Testgruppen und explizite Development-Prüfkommandos hinzugefügt.
Reproduzierbare Werkzeuge und Anleitung: `Tools/BattleSystemV3/README.md`.
`TECHNIK.md`, `SPIELREGELN.md` und `ENTSCHEIDUNGEN.md` aktualisiert. Erforderlicher
Hashkatalog bleibt vollständig; keine erforderlichen Quellen entfernt/optionalisiert.

Implementierungscommit: `39e9feb6d1df097c651d8e4353e057f9bf5fbab0`
([GitHub](https://github.com/Harrys-F/PokeMonster/commit/39e9feb6d1df097c651d8e4353e057f9bf5fbab0)).
45 gezielt geprüfte Dateien. Regulärer Push erfolgreich, Remote-Hash bestätigt.
Normaler neuer Git-Pack 402.333 Bytes, deutlich unter der vereinbarten 1-GiB-
Planungsgrenze. Alle sechs LFS-Nutzlasten nach Push heruntergeladen und per
SHA-256 bestätigt; keine unnötige erneute Übertragung großer Originalquellen.
Zusätzlich ist die serverseitige Verfügbarkeit aller 1.400 aktuell benötigten
LFS-Objekte (6.644.583.961 Bytes) per Batch-Metadatenprüfung bestätigt, ohne
die großen Nutzlasten nochmals herunterzuladen.
Dieser Bericht wird anschließend in einem separaten Dokumentationscommit gesichert.
Dessen endgültiger Hash steht im Abschluss der Codex-Antwort und in `git log`.

GitHub-Grenzen vor dem Upload anhand offizieller Dokumentation geprüft:
[normale Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github),
[Pushgrenze](https://docs.github.com/en/enterprise-cloud%40latest/get-started/using-git/troubleshooting-the-2-gb-push-limit),
[LFS-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage),
[LFS-Abrechnung](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).
Keine Käufe, Budgetänderungen, Force-Pushes, History-Rewrites oder LFS-Bereinigungen.
Die 13.689 Bytes beschreiben diesen Upload, keine behauptete neue Messung des
kontoweiten kostenpflichtigen Abrechnungsstands.

## Verbleibende Grenzen und Empfehlung

- Physischer Switch-Pro-Controller-Test: ausdrücklich offen für Harry, unabhängig vom technischen Abschluss.
- Weiterhin vereinfachte Projektschadensformel/Gleichstandregel; keine vollständige Gen-2-Kampfmathematik, kein STAB, Volltreffer oder zufälliger Schadensfaktor.
- Vollständige Attackenlisten, Effekte, XP-Erträge aller 251 Arten sowie Attackentausch bei vier belegten Slots sind noch Daten-/Funktionsarbeit. Keine endgültigen Werte erfunden.
- Der bestehende Niederlagenablauf heilt und führt zum Checkpoint zurück; ein automatischer Save unmittelbar nach dieser Rückkehr fehlt weiterhin. Heilen/Speichern am Heilhaus und manuelles Save/Load sind geprüft. Keine neue automatische Save-Regel stillschweigend eingeführt.
- Der Feuerangriff verwendet einen kleinen 2D-Flame-Sprite im vorhandenen Präsentationslayer; keine aufwendige Weltpartikelsimulation. Künstlerischer Effektfeinschliff bleibt möglich.
- Vorhandene Schlachtkulissen und Meshy-Oberflächen bleiben gestalterisch aus V2; erkennbare Sockel-/Felsplatzierungs- und Materialfeinheiten wurden in diesem Funktionsauftrag nicht umgestaltet.

**Empfehlung:** Der hier dokumentierte Funktionsumfang ist technisch geprüft und
als nächste spielbare Grundlage geeignet. Harrys reale Bedienungs- und visuelle
Abnahme bleibt sinnvoll; eine vollständige Pokémon-Regelsimulation oder bereits
bestandener physischer Controller-Test wird ausdrücklich nicht behauptet.
