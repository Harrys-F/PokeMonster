# Pokémon-Entwicklungen V3 – gezielte Erweiterung

Auftrag vom 29.10.2026. Tatsächlicher Ausgang: `76064ec022b30cc3ad01f887e80c7f633bbb573a`, main und origin/main vor Beginn identisch. Der vorhandene [V2-Prüfbericht](/Users/harry/Developer/PokeMonster/Docs/POKEMON_ENTWICKLUNGEN_V2_PRUEFBERICHT.md), seine Feature-Commits `bbed7461`/`285ec475`, die spätere Präsentation V2.1 und Fortschritt/Population V4 wurden berücksichtigt. **Keine Neuentwicklung des Entwicklungssystems oder der Präsentation.**

Die Bestandsdaten stammen aus einem neuen Unreal-Asset-Audit und einem abschließenden frischen Commandlet-Vergleich. Die funktionalen Abschlussprüfungen sind bestanden. Der letzte strenge Automation-Wrapper bleibt wegen einer externen HTTP-Warnung **Exit 1**, ausdrücklich nicht vollständig bestanden.

## A – vollständig vorhanden, beibehalten

| Funktion | Tatsächlicher Stand |
|---|---|
| Art und Individuum | Primary-Asset-Identität, individuelle GUID, Teaminstanz und berechnete Werte getrennt |
| Gemeinsame Entwicklungslogik | `CreatureProgression`: Bedingungen, Zielmodellvalidierung und atomarer Spezieswechsel |
| Glumanda-Kette | Historische ID Zunderlauf → Glutexo ab 16 → Glurak ab 36; kein Überspringen |
| Präsentation | Bestehende Bühne in derselben Welt, Aufleuchten/Übergang/Originalfarben/Happy bzw. Idle, Erfolgsmeldung |
| Bestätigung/Abbruch | B/Enter, A/Esc; bestehende Abbruchgrenze 5 s, farbige Enthüllung bis 5,85 s, Erfolg ab 7,8 s; unverändert |
| Levelangebot und Wiederholung | Sichere Oberwelt nach Kampf/Lernentscheidung; Abbruch unterdrückt Wiederholungs-Spam, späterer Levelaufstieg oder Sieg erlaubt neues Angebot |
| Datenübernahme | GUID, Level, numerische EP, gespeicherte Wachstumskurve, Status, vier aktive Slots, Repertoire/AP, Teamplatz; fehlende KP bleiben erhalten |
| Begleiter und Kampf | Bestehender Artwechsel aktualisiert Darstellung/Skeleton/Clips/Maße; andere vorhandene Glurak-/Garados-Instanzen bleiben eigenständig |
| Lernattacken | Nur der echte Eintrag am Entwicklungslevel wird angeboten, keine pauschale neue Ziel-Lernliste; vorhandene Entscheidung/Repertoireverwaltung |
| Gemeinsame Bedingungen | Mindestlevel, Item-ID, Freundschaftsschwelle, Ort und Handlung als UND-Bedingungen; alternative Routen als ODER |
| Tageszeit | Zentrale Weltuhr, halboffene Minutenfenster einschließlich Mitternacht; keine neue Uhr oder artspezifische Zeitregel |
| Welt/Quest/Dialog | Persistente bestehende WorldFlags, Quest-Abschlussflags, Dialogbedingungen und Custom-Actions; kein neues Quest- oder Dialogsystem |
| Speichern | Engine-SaveGame, validierende Rückwärtsmigration, getrennte manuelle Position/Kontrollpunkt/Weltzeit, atomare macOS-Dateiübernahme |

Der V2-Bericht beschreibt den damaligen Save-Stand 8 und damalige QA-Warnungen; Ausgang dieses Auftrags war bereits Schema 10 und die verbesserte Präsentation V2.1. Diese Historie wird nicht als aktueller Fehler oder neue Funktion ausgegeben.

## B – teilweise vorhanden, jetzt gezielt ergänzt

1. **Karpador → Garados ab Level 20:** Beide bestehenden Arten, vollständige sieben Animationsrollen und passende Modelle sind spielbereit, die Route fehlte jedoch im Karpador-Artdatenasset. Genau dieser Eintrag wird hinzugefügt. Keine neue Art, kein Modellimport, keine Ersatz-Zwischenform.
2. **Entwicklungsgegenstand verwenden:** Die vorhandene Kategorie Evolution und `DA_TestEvolutionItem` waren konfiguriert, im Beutel aber nicht anwendbar. Die vorhandene Itemwahl öffnet nun dieselbe Teamwahl wie Heilitems. Ein gültiges Ziel erzeugt ein Angebot im bestehenden Entwicklungsdienst und öffnet dieselbe Sequenz. Ungeeignete Ziele melden „Keine passende spielbereite Entwicklung · kein Item verbraucht“.
3. **Atomarer Gegenstandsverbrauch:** Vorbereiten und Abbrechen kosten nichts. Erst nach erneuter Prüfung von Itembesitz, Bedingungen und Zielmodell wird genau ein Gegenstand zusammen mit der erfolgreichen Entwicklung gespeichert. Scheitert Speichern, werden Pokémon, Inventarstapel, Chronik, Questfortschritt und Flags auf den vorherigen Zustand zurückgesetzt. Mehrdeutige Zielauswahl wird abgewiesen, kein beliebiges erstes Ziel gewählt.
4. **Angebot merken:** Schema 11 ergänzt ausschließlich `PendingEvolutionItemId` zur bestehenden Ziel-/Level-Metadatenstruktur. Dadurch kann ein gespeichertes Itemangebot mit dem tatsächlich ausgewählten Item fortgesetzt werden. Es wird kein Item vorab abgezogen oder ein zweites Inventar geführt.

Die Itemanbindung ist allgemein nutzbar, **derzeit existiert aber keine vollständige reguläre Stein-Entwicklungskette im spielbaren Artenbestand**. Insbesondere ist der Teststein kein Donnerstein und erhält nicht stillschweigend dessen Identität. Es werden keine neuen Items vergeben, keine bestehenden Items umbenannt und keine Artregeln erfunden.

## C – fehlende Modelle, Individualdaten oder Spielinhalte

| Voraussetzung | Fehlender Teil / Konsequenz |
|---|---|
| Freundschaftsentwicklung | Der vorhandene reine Prüfer kennt einen Wert 0–255; individuelle Freundschaft, Zuwachs-/Verlustregeln und deren Save-Feld existieren nicht. Kein künstlicher Standardwert oder unfertige Ersatzökonomie. |
| Steinarten | Kein regulärer Donner-/Blatt-/Sonnenstein im Assetbestand; nur Test-Entwicklungsstein. Passende Formen wie Raichu beziehungsweise Duflor/Giflor/Blubella fehlen. Itemdienst und Auswahl sind vorbereitet, diese Inhalte bleiben offen. |
| Besondere Prüfungen | Endgültige Mindestlevel, konkrete Prüfungen, gültige Ortskennungen und Dialog-/Quest-Inhalte fehlen. Keine Ersetzung durch bloße Level- oder Tauschentwicklung. |
| Spezielle Weltanbindung | Der vorhandene reine Bedingungsprüfer kann Level + Ort + abgeschlossene Handlung + Zeit gemeinsam prüfen. Künftige konkrete NPC-/Ortsereignisse müssen den geprüften Kontext liefern; keine willkürliche globale Ortskennung aus einem beliebigen WorldFlag ableiten. Automatische Oberweltangebote führen weiterhin Levelrouten und explizite Itemangebote aus. |
| Nicht importierte Formen | Eine Incoming-GLB ohne Artasset, geprüftes Rig, Clips und Präsentation ist keine spielbare Entwicklungsform. Keine neuen Importe in diesem Auftrag. |

## Vollständiger vorhandener Artenbestand und Ketten

Der neue Audit findet **21 Arten-DataAssets, davon 18 zentral registrierte spielbereite Pokémon**. TestGrass/TestFire/TestWater sind drei technische Vorlagen, keine zusätzlichen Pokémon. Die Modelltestumgebung bleibt bei denselben 18 Registrierungen.

| Kette / vorhandene Arten | Spielbarer Entwicklungsstand nach V3 | Fehlende Formen / Daten |
|---|---|---|
| Bisasam | Level-16-Regel schon vorhanden, Ausführung sicher blockiert | Bisaknosp und Bisaflor nur Incoming-Originale, keine spielbereiten Arten |
| Glumanda, Glutexo, Glurak | **Glumanda ≥16 → Glutexo ≥36 → Glurak vollständig** | Keine |
| Schiggy | Level-16-Regel schon vorhanden, Ausführung blockiert | Schillok fehlt; Turtok nur Incoming, kein Überspringen |
| Raupy, Smettbo | Keine direkte Raupy→Smettbo-Route erfunden | Safcon nur Incoming, Daten-/Modellintegration der Zwischenform fehlt; regulär Raupy 7→Safcon 10→Smettbo |
| Hornliu, Bibor | Keine direkte Hornliu→Bibor-Route erfunden | Kokuna nur Incoming; regulär Hornliu 7→Kokuna 10→Bibor |
| Habitak | Noch keine spielbare Folgeroute | Ibitak fehlt; regulär ab 20 |
| Pikachu | Vorhandene Itemregel verlangt ThunderStone → Raichu, Ziel blockiert | Raichu und Donnerstein fehlen; Pichu als frühere Gen-2-Form nicht eingebunden |
| Myrapla | Vorhandene Level-21-Regel zu Duflor blockiert | Duflor, Giflor und Blubella fehlen; keine Blatt-/Sonnensteinroute ohne ihre Quellen/Ziele |
| Enton | Vorhandene Level-33-Regel zu Entoron blockiert | Entoron fehlt |
| Machomei | Eigenständiges Pokémon bleibt unverändert, keine weitere Gen-1/2-Entwicklung | Machollo und Maschock fehlen, besondere Maschock-Prüfung offen |
| Nebulak, Gengar | Vorhandene Nebulak-Level-25-Regel zu Alpollo blockiert | Alpollo fehlt; besondere Alpollo→Gengar-Bedingungen offen, kein direkter Sprung |
| Karpador, Garados | **Neu: Karpador ≥20 → Garados vollständig über bestehenden Pfad** | Keine |

Für Arten ohne Zielmodell werden keine künstlichen spielbaren Routen erzeugt. Bereits vorhandene vorbereitete Regeln bleiben erhalten und melden fehlende Zielpräsentationen. Eingebundene Endformen dürfen eigenständig existieren, ohne dass dadurch ihre noch fehlenden Vorformen automatisch als verfügbar gelten.

### Verbindliche besonderen Entwicklungen

| Künftige Route | Gemeinsam nötige Bedingungen | Noch offener Spielinhalt |
|---|---|---|
| Kadabra → Simsala | Mindestlevel + Gelehrter/Magier + passende abgeschlossene Prüfung/Ort | Beide Modelle nur Incoming; endgültiges Level, NPC-Dienst, Prüfung und Ort |
| Maschock → Machomei | Mindestlevel + geeigneter Ort + abgeschlossene Kraftprüfung | Maschock, endgültiges Level, Prüfungsinhalt und Ortsanbindung |
| Georok → Geowaz | Mindestlevel + Bergwerk + besondere abgeschlossene Handlung | Modelle nur Incoming, Artintegration, endgültiges Level, Handlung und Bergwerkbindung |
| Alpollo → Gengar | Mindestlevel + Geisterstätte + abgeschlossene Handlung | Alpollo, endgültiges Level, konkrete Geisterstätte/Handlung |

Die vorhandene Quest kann eine bestätigte Handlung als CompletionFlag in den bestehenden Weltflags ablegen; Dialoge können dieselben Flags prüfen oder setzen. Die neue Automation verwendet diese wirklichen Klassen für den UND-Bedingungsnachweis. Technische IDs `V3_TEST_*`, ein Level von 42 und Freundschaft 220 sind **ausschließlich Testgrenzen**, keine beschlossenen Regeln für diese vier Arten.

## Datenquelle und Änderungsgrenze

Karpadors Level-20-Route ist anhand der öffentlichen strukturierten [PokeAPI-Entwicklungsdaten](https://raw.githubusercontent.com/PokeAPI/pokeapi/2bf639e5572812a67d2b94903fdcb9d095f5aeb2/data/v2/csv/pokemon_evolution.csv) mit fester Revision `2bf639e5572812a67d2b94903fdcb9d095f5aeb2` belegt. Metadaten, SHA-256 und ausgewählter Datensatz stehen in `Tools/EvolutionV3/ReferenceSources.json`; die API-Struktur beschreibt die [PokeAPI-Dokumentation](https://pokeapi.co/docs/v2#evolution-chains). Keine ROM- oder Originalspieldateien verwendet. Diese klassische Levelregel ändert keine Gen-2-Projektentscheidung. Moderne Zusatzformen und Trigger außerhalb unseres Artenumfangs werden nicht übernommen.

`Tools/EvolutionV3/BindKarpador.py` verändert ausschließlich das bestehende `DA_Karpador`. Der Vorgang ist gegen unerwartete bestehende Routen und fehlende spielbereite Quelle/Ziel gesperrt. Glumanda-/Glutexo-/Garados-Artdaten, Lernlisten, Meshes, Größen und Animationen werden nicht gespeichert oder verändert.

## SaveGame und Transaktionen

Schema 11 speichert die stabile Item-ID eines offenen Itemangebots. Schemata 1–10 erhalten für dieses neue Feld `None`; ihre übrigen Migrationen bleiben erhalten. Es werden keine Items, Freunde, Pokémon oder Entwicklungsangebote für alte Spielstände erfunden. Ein unter Schema 10 gespeichertes Glumanda-Levelangebot bleibt ein Levelangebot. Speichern nach einer erfolgreichen Entwicklung bewahrt dieselbe GUID, denselben Teamplatz, Erfahrung, Status und alle aktiven und inaktiven AP-Zustände. Ein Item-Abbruch leert die Itemauswahl, kostet nichts und kann sofort über erneute Itemwahl wiederholt werden. Der bisherige Level-Abbruchschutz bleibt unverändert.

Eine gespeicherte Auswahl ist kein unbegrenztes Recht auf Entwicklung: Zielmodell, aktuelle Bedingungen und vorhandene Itemmenge werden bei Annahme erneut geprüft. Ein inzwischen fehlender Gegenstand verhindert die Übernahme, ohne das Pokémon zu verändern. Es bleibt derselbe atomare Speicherdienst zuständig; kein separater Item-Save und keine Kopie des Teams als neue Instanz.

## Prüfungen und Nachweise

Nachweisordner: `Saved/ProjectRefinement/EvolutionV3/`. Vorhandene Nutzerspielstände werden ausschließlich per Hash überwacht. Neue Tests benutzen eigene UserDir-Spielstände oder isolierte PIE-Slots.

Build 01 deckte eine nicht mit umbenannte private Testreferenz `PendingHealingItem` auf; der bestehende Controller-Test wurde auf `PendingUseItem` angepasst und um die Stein-Zielwahl erweitert. Nach den erfolgreichen Builds 02/03 wurde ein echter Wiederaufnahmefehler des neuen Itempfads im PIE reproduziert und korrigiert. **Finaler Editor-Build 04: Exit 0, 10,49 Sekunden.**


### Weitere Incoming-Modelle, noch keine spielbereiten Arten

38 GLB-Originale liegen in Incoming. Zu den 18 spielbereiten Arten kommen diese **20 noch nicht integrierten Originale**; sie werden weder importiert noch als fertige Entwicklung ausgegeben:

| Incoming-Gruppe | Stand / für spätere Entwicklung nötig |
|---|---|
| Bisaknosp, Bisaflor | Artdaten, Rig/Clips und Präsentation fehlen; Bisasam-Kette später vollständig binden |
| Turtok | Noch nicht spielbereit; zusätzlich fehlt Schillok vollständig |
| Safcon, Kokuna | Zwischenformen noch nicht spielbereit; keine Abkürzung zu Smettbo/Bibor |
| Abra, Kadabra, Simsala | Alle drei nur Originalquellen; regulärer erster Schritt und eigene spätere Prüfung müssen nach Integration gebunden werden |
| Kleinstein, Georok, Geowaz | Alle drei nur Originalquellen; besondere zweite Entwicklung bleibt inhaltlich offen |
| Evoli | Nur Originalmodell; Aquana, Blitza, Flamara, Psiana und Nachtara fehlen. Freundschaft und konkrete Gen-2-Zeitbedingungen benötigen später geprüfte individuelle Daten, keine automatische Ableitung aus Beleuchtungsphasen. |
| Aerodactyl, Ditto, Lavados, Mew, Mewtu, Pantimos, Relaxo, Zapdos | Noch nicht integrierte Formen ohne weitere Entwicklung innerhalb Generation 1/2; keine späteren Mega-/Babyformen hinzuerfinden |

Vorhandenes Iteminventar: `TestCaptureDevice` (Test-Fanggerät), `TestHealingItem` (Trank), `TestEvolutionItem` (Test-Entwicklungsstein). Die drei Itemassets bleiben bytegleich; der Audit findet keinen regulären Donner-/Blatt-/Sonnenstein.

### Abschließende Prüftabelle

| Prüfung | Tatsächlicher Abschluss / Quelle |
|---|---|
| Editor-Build | `Saved/ProjectRefinement/EvolutionV3Build04/Result.json`: Exit 0 |
| Vollständige finale Automation | `EvolutionV3Automation02/Report/index.json`: **294 Success + 1 funktional bestanden mit Warnung = 295**, 0 Failed, 0 NotRun, 0 InProcess |
| Strenger finaler QA-Wrapper | **Exit 1**; genau eine während eines Tests aufgezeichnete externe HTTP-Konnektivitätswarnung, unten erläutert; `StrictQAFinal.json` |
| Vorheriger voller Lauf | `EvolutionV3Automation01`: 295/295 ohne Testwarnungen, Wrapper Exit 0; lag vor der abschließenden Wiederaufnahmekorrektur und ersetzt den finalen Warnstatus nicht |
| Neue Automation | Drei Tests unter `PokeMonster.EvolutionV3`: Karpador-Daten/Schwellen/Identität/KP/Status/AP/Lernen; Itemangebot/Native-Serialisierung/Legacy 1–10/ungültige Itemmetadaten; vorhandene Quest-Flags und kombinierte Bedingungen |
| Zwölf Map Checks | Finale Editor02-Logs: zwölf Maps, jeweils **0 Fehler / 0 Warnungen**; `MapCheckResults.json` |
| Separater Entwicklungsablauf | `NativeEvolution05`: **117 Schritte / 42 Prüfungen**, bestanden, 146,74 s; alle drei Levelrouten plus technische Itemanbindung |
| Finale PIE-Entwicklung | `PIEEvolution02`: **117 Schritte / 42 Prüfungen**, bestanden, 149,92 s, einschließlich echter UI-Schreibfehler-Wiederaufnahme |
| Separates allgemeines Gameplay | `NativeFunctional01`: **76 Schritte / 22 Prüfungen**, bestanden; 231,08 s. Dieser breite Lauf lag vor der isolierten Wiederaufnahmekorrektur; betroffene Abläufe danach durch NativeEvolution05 und vollständige finale PIE-Regression geprüft. |
| Finale PIE-Gameplay-Regression | `PIEFunctional01`: **76 Schritte / 22 Prüfungen**, bestanden, 226,06 s; Kampf/Attacke/Flucht/Fang, Team-/Begleiterwechsel, Innenraum, Save/Load, Weltuhr/Tagesphasen und Wasser |
| Frischer Spielprozess nach Speichern | `RestartWrite02` und `RestartRead02`: alle individuellen Teamfelder, Itembestand 2, Position und Begleitermesh wiederhergestellt. Gespeichert Tag 4 um 16:42; nach rund 0,6 Echtsekunden normal laufender Uhr geladen Tag 4 16:42:07, entsprechend der bestehenden 12-fachen Geschwindigkeit. |
| Mapwechsel | `Travel01`: VisualV2 → bestehende Dev_TestMap → VisualV2; Team/KP/AP, Weltuhr, Begleiter und Grafikprofil erhalten |
| Controller-Software | `PIECycles01/movement`: 46 Eingabeschritte / 12 Prüfungen bestanden; acht Richtungen, Sprint, X, Plus, B/A, Steuerkreuz und L/R. HardwareSPG → 100 → C konsistent, C wiederhergestellt. Keine neue physische Controllerabnahme behauptet. |
| Vorhandene RAM-Testbefehle | `ManualPIE02`: vier Prüfungen bestanden. Karpador 19 erreicht über `pm.EvolutionTest.Start 1` die echte Level-20-Route; Abbruch, End-Wiederherstellung, erneuter Start, bestätigte vollständige Garados-Sequenz und echtes Biss-Lernangebot. `End` stellt denselben Karpador 19 einschließlich Daten und alle Disk-Save-Hashes wieder her. |
| Editorstabilität | Finaler Editor 15999: vier PIE-Zyklen und reguläres Schließen, keine schmutzigen Maps/Contentpakete. Auch Editor 14407 vor dem Korrekturbau regulär geschlossen. Kein Force Quit. |
| Frischer Asset-Abgleich | `AssetComparison.json`: 21 Artassets, 18 spielbereite Arten, Items identisch; einzig Karpadors neue Route, erfasste Identitäts-/Visual-/Clipfelder sonst identisch |
| Bildnachweise | Acht echte native 2560×1440-PNGs des finalen separaten Laufs, Header geprüft: `QHDProof.json` |

Die allgemeinen Abläufe prüfen außerdem die bestehende Wald-/Wiesen-/Dorfpopulation, beide Wasserarten mit Bewegung und Mediengrenzen, die 18 unabhängigen Modellstationen, NPC-Dialoge, Innen-/Außenkamera, gespeicherte Position und den unabhängigen Kontrollpunkt. Das globale Habitatlimit 14, sechs gleichzeitige Arten, alle Zonen, die Teich-/Bachtrennung und der gemeinsame Namens-Overlay-Code bleiben unverändert. Es wurden keine neuen Performancebenchmarks und keine neuen Videofolgen gestartet; aus dieser Entwicklungsintegration wird kein neuer FPS-Gewinn behauptet.

### Nachgewiesener Fehler und Korrektur

`PIEEvolution01` reproduzierte einen echten Fehler des zunächst ergänzten Itempfads: Nach erzwungenem Schreibfehler am Sequenzabschluss blieben Pokémon und Item korrekt erhalten, die erneute explizite Auswahl scheiterte aber am noch offenen Angebot beziehungsweise an der bestehenden Präsentations-Fehlersperre.

Die Korrektur bleibt im selben EncounterSubsystem/Controller: Eine explizite Auswahl darf **nur ihr eigenes** noch gültiges Itemangebot mit demselben Item und Ziel fortsetzen; andere Angebote werden nicht ersetzt. Erst nach erfolgreicher neuer Prüfung/Speicherung wird die Präsentationssperre für diesen ausdrücklichen Versuch zurückgesetzt. NativeEvolution05 und PIEEvolution02 bestätigen danach den tatsächlichen UI-Fehler, die unveränderten Daten/Items, die erneute Auswahl, den erfolgreichen Abschluss, genau einen Verbrauch und die Abweisung einer nochmaligen Übernahme. Keine parallele Fehler-/Entwicklungsverwaltung.

### Vorversuche und Warnungen ehrlich getrennt

NativeEvolution01 scheiterte an einem Python-GUID-Objektvergleich, NativeEvolution02/03 an einem nicht exportierten beziehungsweise geschützten internen Präsentationszeiger. Der Prüfer verwendet danach GUID-Werte und den öffentlich unterstützten SkeletalMesh-Getter. Es wurde kein Produktionsmodell zur Anpassung an den Prüfer verändert. NativeEvolution04 bestand bereits 112 Schritte; der finale Lauf 05 ergänzt den vollständigen UI-Schreibfehlerfall und besteht 117 Schritte.

Der erste Start der PIE-Gesamtregression verwendete versehentlich den nativen Startadapter. Seine UserDir-Sperre verhinderte die Ausführung; danach wurde der vorhandene PIE-Adapter mit richtigem isolierten Slot verwendet. ManualPIE01 versuchte RAM-Vorschau und benannten Testslot gleichzeitig zu verwenden: Der bestehende Schutz wies dies ohne Teammutation korrekt ab. ManualPIE02 prüft die RAM-Vorschau in einer frischen, weiterhin durch eigenes UserDir abgegrenzten Sitzung. Diese Fehlversuche werden nicht als bestandene Läufe gezählt.

Im letzten vollständigen Automationlauf ist die einzige testzugeordnete Warnung:

`LogHttp: HTTP request timed out after 3.00 seconds URL=https://www.google.com/generate_204`

Sie fiel im Test `PokeMonster.NPC.Library.OrdinaryPIEGroundAndIsolation` an. Dieser Test meldete funktional Success, 1 Warning, 0 Errors. Der **unveränderte strenge Wrapper beendet sich deshalb mit Exit 1**. Keine Filteränderung und kein wiederholtes „Glückslaufen“ bis zu einem verschwiegenen Exit 0. Das ist ein Infrastruktur-/Konnektivitätsbefund, kein als extern umetikettierter fehlgeschlagener Entwicklungstest.

Die absichtlich schreibgeschützten eigenen QA-Saveverzeichnisse erzeugen in NativeEvolution05 und im finalen Editor je zwei erwartete Speicherverweigerungen. Berechtigungen werden im Fehlerpfad wiederhergestellt; ursprüngliche Spielstände bleiben unberührt. In sieben geprüften Abschlusslogs gibt es keinen Fatal-/Assert-/Ensure-Abbruch. Separate `-game`-Starts zeigen bekannte experimentelle Engine-Toolset-Importfehler (`ToolsetDefinition`/`PythonTestRunner` fehlen dort); diese bleiben gesondert in `LogReview.json` und wurden nicht durch Änderungen an Engine-Plugins kaschiert.

Die externe iOS-Helfermeldung `idevice_id: Bad CPU type in executable` tritt in diesen sieben Abschlusslogs nicht auf. Das ist kein Nachweis einer allgemeinen Reparatur dieses Helfers; es wurden weder Rosetta/Homebrew installiert noch Engine-Helfer ersetzt.

## Echte Aufnahmen und Bedienung

Alle folgenden Bilder liegen lokal unter `Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/`, tatsächlich 2560×1440, kein generierter Nachweis und keine hochskalierte kleinere Aufnahme:

- [Glumanda → Glutexo, Originalfarben und Erfolg](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/Glumanda_Complete.png)
- [Glutexo → Glurak, Originalfarben und Erfolg](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/Glutexo_Complete.png)
- [Karpador → Garados](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/Karpador_Complete.png)
- [Technische Itemfixture, ausdrücklich keine reguläre Karpador-Steinregel](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/Item_TechnicalFixture_Complete.png)
- [Team nach erfolgreichem Abschluss](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/EvolutionV3/NativeEvolution05/TeamAfter.png)

Die drei jeweiligen `*_Cancelled.png` dokumentieren den Abbruch. Im langen Ablauf wird jeweils an der echten Grenze 16/36/20 angeboten und abgebrochen; der spätere bestätigte Versuch erfolgt nach dem nächsten Level 17/37/21. Exakte direkte Grenzentwicklungen sind zusätzlich automatisiert geprüft, Karpador auf Level 20 außerdem im vorhandenen manuellen RAM-PIE-Befehl bestätigt. Die Präsentationsgeometrie und Originalgrößen bleiben unverändert.

Normaler Entwicklungs-Test im Editor: `pm.EvolutionTest.List`, `pm.EvolutionTest.Start <Teamplatz 1–6>`, `pm.EvolutionTest.End`. Die bestehenden Befehle erkennen Karpador automatisch aus seiner echten Route. Nicht mit benannter Testslot-Isolation kombinieren; Start schützt den normalen Nutzerslot durch den bestehenden RAM-Transport. B/Enter bestätigt und A/Esc bricht ab. Späterer manueller Start kann den Test wiederholen; End verwirft Testdaten.

## Verbleibende Grenzen und Git-Umfang

- Spielbar sind weiterhin nur die vorhandene Glumanda-Kette und jetzt zusätzlich Karpador→Garados. Eingebundene Endformen sind keine Behauptung, alle Vorformen seien vorhanden.
- Der generische Itempfad ist technisch und spielbar über bestehende UI geprüft; eine echte reguläre Steinroute benötigt noch passende Arten/Modelle und ein korrekt identifiziertes reguläres Item. Die Testfixture ersetzt diese Inhalte nicht.
- Individuelle Freundschaft und endgültige Sonderprüfungen/Orte/Mindestlevel bleiben fachlich offen. Keine Platzhaltermodelle, erfundenen Werte, reine Level-Ersatzrouten oder neue Quests.
- Der letzte strenge QA-Wrapper ist wegen der dokumentierten HTTP-Warnung **nicht vollständig bestanden**. Alle 295 fachlichen Tests und die bezeichneten finalen Gameplayprüfungen bestehen.
- Die bekannte allgemeine temporale IFG-/Framezeitabnahme wird durch diese Entwicklungstests nicht nachträglich als abgeschlossen ausgegeben. Rendering bleibt geschützt.

Nur eigene geprüfte Quell-/Test-/Werkzeug-/Dokumentationsdateien und das eine Karpador-Artdatenasset werden für den Abschluss vorgemerkt. Medien und große QA-Ausgaben verbleiben unter Saved. Der Abschlusscommit und die tatsächliche Remote-/LFS-Synchronisation werden nach dem regulären Push in der Abschlussmeldung benannt.


### Abschließender Dateischutz

SHA-256-Abgleich gegen den vor Beginn erfassten Stand: **6.436 ursprüngliche Dateien geprüft, 531 bestehende Spielstände und 34 geschützte unversionierte Dateien unverändert**. Alle Maps einschließlich VisualV2, Westland und Biom-Testmap, Originalmodelle, Blenderquellen, Animationen und Grafikprofile bleiben bytegleich. Die bereits vorhandene Nutzeränderung an `Config/DefaultEngine.ini` ist unverändert und ausdrücklich vom Commit ausgeschlossen. Beide lokalen Vollbackup-Verweise bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Nachweise: `ProtectionFinal.json` und `Baseline.json`.

Zusätzlich sind die tatsächlich geladenen Basiswerte, Wachstumskurven, EP-Erträge und Lernlisten aller 18 Arten mit dem vorherigen geprüften Stand verglichen: unverändert. Einzig Karpadors neue Entwicklungsroute unterscheidet sich (`ProgressionDataComparison.json`). Die gezielte Commitauswahl umfasst 26 Dateien, darunter genau ein neues LFS-Objekt für das bestehende Karpador-Datenasset; keine Kontrollmedien, Caches, Testspielstände oder unbeteiligten Nutzerdateien.
