# Gameplay- und Controller-Praxistest V1

26.10.2026 · `/Users/harry/Developer/PokeMonster` · Unreal 5.8.2 / Metal/macOS.
Ausgangsstand `45068771198d68c6605c89bc4c7bfed38150e218`, `main`, live mit
`origin/main` synchron. Testumgebung ausschließlich bestehende VisualV2.

## Gesamtbewertung

**Der zusammenhängende RAM-geschützte Gameplayablauf ist bestanden:** 74 Schritte,
262,19 Meter tatsächliche Bewegung, natürlicher Wildkampf mit Sieg, XP/Levelaufstieg,
NPC-Dialog, Begleiterwechsel, Heilhaus, Heilung und zweimal exakter Save/Load-Vergleich.
Eine weitere natürliche Begegnung wurde regulär per Flucht beendet. Keine kritische
Zustandsblockade oder Datenkorruption im abschließenden Ablauf nachgewiesen.

Das ist **keine vollständige Hardware- oder Veröffentlichungsfreigabe**.
Der Switch Pro Controller war bei der Abfrage nicht verbunden. Es fehlen weiterhin
16 Lernbindungen, und das bestehende Fortsetzen/Positionsspeichern ist eingeschränkt.
Der strenge QA-Wrapper endet wegen externer iOS-Warnungen mit **Exit 1**.

Keine Produktionsänderung an Gameplay, Karten, Modellen, Animationen, Kameras,
Eingabebelegung oder freigegebener Entwicklungspräsentation war erforderlich.
Geändert werden ausschließlich Prüfadapter, dieser Bericht und Prüfmetadaten.

## Prüfaufbau und Schutz

17 erfolgreich abgeschlossene RAM-PIE-Sitzungen plus frischer normaler Start-/Ladetest.
Bestehende native Battle-, Wild-, Progression-, Evolution-, NPC- und Inputprüfungen
wurden wiederverwendet. Kein paralleles Spielsystem. Der vorhandene
`BeginPIEMemoryPreview`-Transport wird über den bereits bestehenden Testgelände-Dienst
aktiviert, bevor temporäre Team-/XP-/Itemdaten verändert werden. Keine neuen NPCs
oder Rollen platziert, keine Originalmodelle importiert.

Die normalen Speicherfunktionen serialisieren dabei echte Zustände ausschließlich
im RAM. Der reale Dev-Slot wird weder umbenannt noch kopiert oder zurückgeschrieben.
Vorher-/Nachher-SHA-256 schützt seine Bytes; normaler PIE-Stopp verwirft Fixtures.
Die normale feste 2,5D-Kamera, Licht V3.1 und alle 1466 Editoractors blieben erhalten.
Die vollständige Szeneninventur ist nach Map Checks und frischem Editorstart gleich.
Alle zwölf Maps, Originalquellen, 31 vorbestehenden unversionierten Dateien und beide
Vollbackup-Verweise werden zusätzlich per Dateiintegrität geprüft.

## Zusammenhängender Durchlauf – Journey07

Ein klar ausgewiesenes vorhandenes Testteam wird im RAM vorbereitet: Glumanda
Level15 plus unabhängiges Glurak36. Glumanda steht durch den bestehenden XP-Dienst
**einen XP vor Level16**; das ist eine seltene Zustandsfixture, kein neuer Balancewert.
Startanker einmal vor der Wegmessung gesetzt. Danach keine Testteleports;
der normale Ortsversatz des Heilhaus-Innenraums bleibt Bestandteil des Spiels.

1. Team-/Begleiterauswahl über X, Steuerkreuz und B; Glumanda wird Teamplatz1.
2. Tatsächliches Hinlaufen zur unveränderten wilden Glumanda-Mapinstanz.
3. Genau eine ClassicBattle-Begegnung, zwei Kampfrunden, Sieg mit AP-/KP-Veränderung.
4. **46 XP**, von 4095 auf 4141, Level **15 → 16**; reguläre XP-/Werteverarbeitung.
5. Wanderer erreichen, mit B sprechen, Dialogseiten bestätigen und weiterspielen.
6. Wege, Brücke, Felsdurchgang und Dorf; erster RAM-Save/Load einschließlich absichtlicher
   Inventar-/Teamänderung zwischen Speichern und Laden. Exakter Ausgangszustand wiederhergestellt.
7. Heilhaus über den normalen Eingang betreten; Innenkamera, Heilerin und Rückweg.
   KP sowie aktive AP werden vollständig geheilt.
8. Waldrunde mit Licht-/Schattenwechseln; weitere natürliche Glurak-Begegnung,
   drei Runden bis erfolgreicher Flucht, Rückkehr zur Oberwelt.
9. Durch eine dynamische Pokémon-Engstelle mit seitlichen normalen Stickeingaben
   ausweichen; keine Eingabesperre, keine Änderung der Kollisionen.
10. Acht Richtungen, Sprint, Menüfokus und zweiter exakter RAM-Roundtrip; weiterlaufen.

**1721 Begleiterstichproben:** höchstens ein sichtbarer Begleiter, richtige Art aus
Teamplatz1. Das rohe Abstandmaximum von rund 204 m enthält den bestehenden großen
Heilhaus-Ortsversatz und ist ausdrücklich **kein** stabiler Außenabstand.
Deshalb wurde ein gezielter separater Außenlauf ergänzt: 151 Stichproben,
maximal **540,17 cm**, nach Stillstand **130,34 cm**, maximale Spielergeschwindigkeit
**315 cm/s**. Kein Teleport entlang dieses Bewegungsabschnitts.

Der besiegte erste Gegner durchlief Recovering → Escaping → Removed. Entfernung
wurde am tatsächlichen Übergang geprüft, nicht bei einem späteren Zurückkehren
zur bereits leeren Habitatstelle. Abschlussmarkierungen überstanden den RAM-Roundtrip.

## Tatsächlich ausgeführte PIE-Prüfungen

| Lauf | Ergebnis / Umfang |
|---|---|
| Controller01 | **48 Checks**: Stick, L3-Toggle, B/A, X, L/R, Plus, Dpad, wiederholte/überlappende Eingaben, Menüfokus, Items, Dialog, Herausforderung, Kampf, Teamtausch, ein Begleiter, RAM-Speichern/Laden. |
| Battle01 | **9 Fälle** in ClassicBattle/WorldBattle: Items, Heuler, Glut, Wechsel, Flucht/Fehlschlag, Trainer-/Storysperre, Sieg, erzwungener Wechsel, Niederlage, leere AP/Notfallzug. |
| Progression01 | **6 Fälle**: Lernen/Ersetzen und Ablehnen in Classic/World, freie Slots, fehlende Entwicklungsmodelle sicher blockiert. Tatsächliche KO-XP und Lern-UI. |
| Themes01 | Wiese, Wald, Höhle, Ruine; Menüs, Angriffs-/Trefferrollen, Kamera-/Positionsrückkehr und Entfernung der transienten Kampfbühne. |
| Evolution01 | **14 Checks / 47 Schritte**: Glumanda → Glutexo → Glurak, Slot2, unabhängiges Reserve-Glurak, IDs/XP/AP/Repertoire, RAM-Save/Load und spätes Abbrechen bei **4,605 Spielsekunden** vor der unveränderten Fünf-Sekunden-Grenze. Vollständige farbige Enthüllung und Rückkehr. |
| Aggressive01 | Tatsächlicher Kontakt startet genau eine Begegnung; Annäherung alleine nicht; reguläre Spielerflucht. |
| Territorial01 | Warnung/Kontakt, genau ein Kampf, Sieg, sichtbare Erholung/Flucht. **1354,64 cm** Flucht in etwa **42,94 Spielsekunden**, Entfernung erst außerhalb des Bildes. |
| Shy01 | Scheues Verhalten, kein automatischer Kontaktkampf, gerichtete Herausforderung bei Nähe und reguläre Flucht/Cooldown. |
| Curious01 | Kein automatischer Kontaktkampf; gültige gerichtete Herausforderung und korrekte Rückkehr. |
| Capture01 | Ruhiges Pokémon, Kontakt ohne Autostart, Fangtransfer und sofortige Source-Entfernung ohne KO-Flucht. Vorhandene ausdrücklich bezeichnete **1-KP-/Seed51-Fangfixture**; kein Fangquotentest. |
| Group01 | Drei vorhandene Bisasam mit eigenen Seeds/Zielen/Pausen; zwei gerichtete Zielwahlen; nur ein Mitglied kämpft, übrige pausieren; ein Begleiter kehrt zurück. |
| Collision01 | Echter Vorwärts-/Rückwärtsinput an bestehendem Baumstamm, Felsen und Heilhauswand; blockiert korrekt und lässt sich wieder verlassen. Nur diagnostische Anfangspositionen, Landschaftskollisionen unverändert. |
| Movement01 | Echter nativer Bewegungsclip: acht Richtungen, Gehen, Sprinten und Stoppen aus unveränderter Spielkamera; keine Animationen bearbeitet. |
| NPC01 | Original-Wanderer und Heilerin: richtige Dialogquellen, aktive Gesprächspräsentation, Heilung, Bewegungsfreigabe und RAM-Save/Load. Keine neue NPC-Bibliotheksfreigabe. |
| Repertoire01 | **8 Checks**: Team → Inventar → Attacken mit L/R, B/A, reine Ansicht, keine Änderung aktiver Attacken/AP; tatsächliches offenes Level19-Lernangebot bleibt beim RAM-Laden erhalten. |
| Follower01 | Separater stabiler Außenabstand, Sprint-Nachholen und genau ein Begleiter, ohne Innenraum-Transfer im Messfenster. |

Im echten Kampf wurden vorhandene Angriffs-/Trefferreaktionen, KP-/AP-Verarbeitung
und Heuler/Glut-Rückmeldungen geprüft. Weitere Effektkategorien und Randfälle werden
von der bestehenden vollständigen Automation abgedeckt; nicht jede einzelne der
75 vorhandenen Move-Assets wurde hier erneut in einem eigenen PIE-Kampf vorgeführt.

## Bestehender Nutzerspielstand und Grenzen des Fortsetzens

Ein frischer normaler PIE erzeugt zunächst das bestehende Dev-Team. Das ist kein
Autoload des Nutzerslots. **`PMLoad` lädt den vorhandenen Slot ausdrücklich.**
Der tatsächliche unveränderte Nutzerslot wurde zweimal erfolgreich über diesen
bestehenden Dienst geladen: eine gespeicherte Teaminstanz, identische vollständige
Instanzdaten einschließlich IDs, HP/XP, aktiven/erlernten Attacken, AP und Angeboten.
Die native Versions-/Datenprüfung blieb maßgeblich. Kein Speicheraufruf oder
Rückschreiben einer Migration; der Dateihash blieb identisch.

Ein verzögerter Neustartversuch befand sich inzwischen in einer natürlichen
Wildbegegnung. Dort wurde Laden korrekt abgewiesen. Der anschließend sofort
geprüfte frische Oberweltstart lud denselben unveränderten Slot erfolgreich;
die Abweisung war kein Nachweis eines beschädigten Saves.

**Offen:** Schema8 speichert Team, Inventar, Fortschritt und aktiven Heil-/Rückkehrpunkt,
aber keine beliebige aktuelle Pawntransform. Die zwei stationären RAM-Roundtrips
beweisen deshalb keine Positionspersistenz nach Weglaufen oder Neustart.
Automatisches Fortsetzen und vollständiges ortsgenaues Fortsetzen sind hier nicht
als implementiert ausgegeben. Ihre Einführung wäre eine zusätzliche Spielfunktion;
in diesem Prüfauftrag wird das bestehende Schema nicht erweitert.

Die Niederlagenfälle zeigten im Engine-Log `placed=1 healed=1 autosaved=1` im
RAM-geschützten Ablauf. Native Regressionen prüfen alte Saveversionen, Persistenz,
Repertoire/AP, Fang und Heilung. Das ersetzt keine Behauptung über nicht gespeicherte
aktuelle Weltpositionen.

## Noch ungebundene Lernattacken

21 Speziesassets einschließlich drei technischen Testarten und 75 Move-Assets
wurden rein lesend inventarisiert. Die dokumentierten **16 Einträge / 15 unterschiedlichen
Attacken** sind unverändert ausdrücklich unverfügbar. Keine davon hat bereits ein
passendes produktives Move-Asset. Daher liegt keine bloße, eindeutig korrigierbare
Referenzlücke vor. Es wurden keine neuen Wirkungen oder unbestätigten Werte erfunden.

| Art | Level und vorhandene Quellkennung ohne produktive Bindung |
|---|---|
| Bibor | 20 TWINEEDLE · 30 PURSUIT · 35 PIN_MISSILE |
| Garados | 1 THRASH · 35 TWISTER · 50 HYPER_BEAM |
| Habitak | 25 PURSUIT · 31 MIRROR_MOVE · 37 DRILL_PECK |
| Karpador | 1 SPLASH · 30 FLAIL |
| Smettbo | 18 SUPERSONIC · 23 WHIRLWIND · 28 GUST · 34 PSYBEAM · 40 SAFEGUARD |

Quelle des Bestands: tatsächliche LevelUpMoves und bestehender Kristall-Importplan
`Tools/BiomeTestV1/SpeciesV11.json`, bestehende Quellen-/Bindungsdateien und
`BIOM_TESTMAP_V11_PRUEFBERICHT.md`. Keine Übernahme neuer Attackendaten.
Die zuvor fertiggestellten 49 V4-Wirkungen wurden nicht zurückgebaut.

## Build, Automation, Map Checks und Logs

| Prüfung | Ergebnis |
|---|---|
| Editor-Build | **Exit 0**, vorhandener nativer Stand aktuell, 3,00 s. Keine C++-Änderung in diesem Auftrag. |
| Vollständige Automation | **209 Success + 1 Success mit Warnungen**, **0 fehlgeschlagen**, 0 ausstehend; Engine Exit0. |
| Strenger QA-Wrapper | **Exit 1 – nicht bestanden.** Keine Unterdrückung und keine Wiederholung zum Erzwingen eines grünen Ergebnisses. |
| Zugeordnete Warnungen | Genau zwei externe `idevice_id`-/`posix_spawn 86`-Zeilen bei `PokeMonster.CrystalMoves.Edges.AllTenLearnlistsUseValidStableAssets`. Keine ungültige Lernattacke in diesem Test behauptet. |
| Zwölf Map Checks | Je **0 Fehler / 0 Warnungen** in abgegrenzten `PRAXIS_MAPCHECK_BEGIN/END`-Abschnitten. |
| Szenenvergleich | Alle **1466 Editoractors** und deren erfasste Einstellungen unverändert, keine schmutzigen Pakete. |
| Native kritische Signaturen | Kein erneutes `pthread_rwlock_init`-, SIGSEGV-, Fatal- oder natives Assertion-failed-Vorkommnis in den geprüften Logs. |

Das gesamte Engine-Log ist nicht warnungs-/fehlerzeilenfrei: bekannte
`UE::UnifiedErrorTest`-Startup-Ausgaben, Python-Namenskonflikt, iOS-Helfer und
Audio-/Bewegungs-Time-Step-Hinweise sind enthalten. Beim Laden vieler Maps gab es
SkinnedAsset-Speicherschätzungen über dem temporär verfügbaren Budget.
Außerdem wurde beim frischen Start die bestehende Warnung für
`MI_WLA_LeafOak` ohne InstancedStaticMeshes-Usage beobachtet: möglicher
Defaultmaterial-Fallback, keine ungeprüfte Änderung am geteilten Originalmaterial.
Keine umfangreiche Performanceprüfung oder Leistungsgarantie.

## Fehler und Korrekturen des Prüfaufbaus

Produktionscode oder Assets wurden nicht geändert. Anfangs scheiterten zusätzliche
Adapter an nicht exponierten/read-only Python-APIs. Die Adapter nutzen nun die
vorhandenen XP-/Load-Dienste und öffentliche Abfragen. Direkter Zugriff auf
nicht freigegebene Save-Payload-Felder wurde nicht umgangen.

Journey01/02: Initialisierungsfehler. Journey03: nicht exponierte Completed-ID-Abfrage.
Journey04: falsche Prüferwartung bei späterer Rückkehr zur bereits entfernten Instanz;
der tatsächliche Entfernungszeitpunkt lag korrekt außerhalb des Bildes.
Journey05: zusätzlicher stärkerer Wildgegner gewann regelkonform; der Test durfte
nicht jeden zusätzlichen Kampf als garantierten Sieg voraussetzen.
Journey06: starrer Geradeauspfad traf die dynamische Engstelle.
**Nur Journey07 ist als vollständiger End-to-End-Pass gewertet.** Alle früheren
Fehlernachweise bleiben lokal erhalten. Nachfolgende unabhängige Tests liefen weiter.

Die Engstelle am Waldrückweg hatte keine Eingabesperre. Nahe Körper von Gengar und
Glurak verengten die Passage; seitliche Stickeingaben führten weiter. Das bleibt ein
Komfort-/Platzierungsbefund für spätere manuelle Bewertung, keine stillschweigende
Änderung der Kontaktkämpfe oder Habitatpositionen.

## Echte lokale Bilder und Bewegung

184 aktuelle native Bilder sind mit tatsächlichen Pixelmaßen und SHA-256 in
`Saved/ProjectRefinement/GameplayPraxisV1/Media.json` indexiert. QHD-Spielkamera-
Bilder sind 2560×1440; Slate-UI-Aufnahmen behalten ihre tatsächliche Fensterauflösung.
Keine hochskalierten Bilder als QHD ausgegeben. Keine Konzeptbilder.

- [Zusammenhängender Lauf: Heilhaus](../Saved/ProjectRefinement/GameplayPraxisV1/Journey07/Footrun/Heilhaus.png)
- [Kontakt und sichtbare KO-Flucht – Originalframe-Übersicht](../Saved/ProjectRefinement/GameplayPraxisV1/ContactAndEscape_Overview.jpg)
- [Team-/Controller-Menü](../Saved/GlumandaV11/LiveUI/PraxisController015/ActualSlateViewport.png)
- [Repertoire: Nur Ansicht, AP und Meisterhinweis](../Saved/GlumandaV11/LiveUI/PraxisRepertoire01ReadOnly/ActualSlateViewport.png)
- [Wald-Kampfumgebung](../Saved/BattleViewV2/LiveUI/BattleV2_forest_Commands_Themes01/ActualSlateViewport.png)
- [Vollständig enthülltes Glurak nach Entwicklung](../Saved/GlumandaV11/LiveUI/Evolution01GlurakComplete/ActualSlateViewport.png)
- [Später erlaubter Abbruch](../Saved/GlumandaV11/LiveUI/Evolution01LatePreview/ActualSlateViewport.png)
- [Vorhandene Heilerin](../Saved/ProjectRefinement/GameplayPraxisV1/NPC01/Heilerin_Interaction_QHD.png)
- [Begleiter nach Sprint und Anhalten](../Saved/ProjectRefinement/GameplayPraxisV1/Follower01/FollowerSettled.png)
- [Echter Bewegungsclip](../Saved/ProjectRefinement/GameplayPraxisV1/Movement01/Motion/PlayerMovement.mp4)

Der Bewegungsclip enthält 186 tatsächlich präsentierte Frames über etwa neun
Spielsekunden, 2331×1311 Slate-Pixel. Aufnahme bei Zeitfaktor0,20, Wiedergabe mit
Original-Spielzeitstempeln, rund20,72 Abtastungen je Spielsekunde. Keine
Zwischenbildsynthese und kein Echtzeit-FPS-Nachweis. Kurze visuelle Stichproben
belegen keine perfekte Fuß-IK auf jedem Terrain. An der Glurak-Nahansicht bleiben
auffällige fächerartige Flächen am Flügelansatz ein visueller Sichtbefund ohne hier
abschließend diagnostizierte Ursache; Modell/Happy-Clip/Präsentation bleiben erhalten.

## Noch manuell am Switch Pro zu prüfen

Bluetooth-Inventur: „Nintendo Switch ProCon“, Nintendo Vendor0x057E/Product0x2009,
Abschnitt **device_not_connected**. Laufender Unreal-Backendwert:
`Slate.MacControllerPreferGCImpl=1`. Bestehende Softwarezuordnung unverändert:
B→FaceButton_Right, A→FaceButton_Bottom, X→FaceButton_Left; L3, L/R, Dpad und Plus
wie bisher. Das ist kein Nachweis physischer Tastenereignisse.

Nach Verbindung im normalen PIE prüfen:

1. Linker Stick in acht Richtungen; L3 einmal an/aus, danach Menüs/Kampf/Innenraum.
2. B am Wanderer/Heilhaus und an gültigem ruhigen/neugierigen/scheuen Wildziel;
   A zurück. Territoriale Kämpfe weiterhin nur bei tatsächlichem Kontakt.
3. X, dreifacher Kategorienwechsel mit R/L, Dpad, B/A; Teamplatz1/Begleiter ändern.
4. Plus öffnen/fortsetzen, wiederholtes schnelles B/A/X und überlappende Eingaben.
5. ClassicBattle: Attacke, Item, Wechsel und Flucht; danach wieder laufen/interagieren.
6. Falls die physischen Beschriftungen abweichen: `pm.Input.Trace 1` zeigt echte
   Rohkeys; anschließend `pm.Input.Trace 0`. Keine Xbox-Zuordnung erraten.

Vor dem Fortsetzen eines bestehenden Slots zunächst `PMLoad`; Tests mit geändertem
Team nur unter vorhandenem RAM-Schutz durchführen. Automatisierte `pm.Input`-
Ereignisse sind als Simulation markiert und dürfen nicht als Hardware-Pass gelten.

## Dateiintegrität

Die abschließende SHA-256-Prüfung bestätigt **5465 von 5465 bisherigen
Kerndateien unverändert**. Alle **44 geschützten Dateien** – 31 vorherige
unversionierte Originale, zwölf Maps und der reale Nutzersave – sind bytegleich.
Beide Backup-Verweise zeigen weiterhin auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`.
Auch nach dem letzten Begleiterlauf: VisualV2 ohne aktives PIE, 1466 Actors
unverändert und keine ungespeicherten Pakete. Das neue Prüfpaket umfasst 29 Dateien
einschließlich aktualisiertem Kerndatei-Hashmanifest; keine Produktionsassets.

## Abschluss und GitHub

Technisch geprüfter Zwischenstand mit bestandenem zusammenhängendem RAM-Ablauf,
keine neue Spielfunktion. Offen bleiben physische Hardwareprüfung, die genannten
Lernbindungen, Fortsetzen/Positionspersistenz und visuelle Restabnahme.
Die ausstehende Freigabe der Biom-V1.1 und NPC-Bibliothek wird nicht vorweggenommen.

**Prüfpaket:** `d2d9778637e06570d2c21e40815e0fc7c670db43`
(`test: verify VisualV2 gameplay and controller practice`). Normaler Push erfolgreich;
lokales `main`, `origin/main` und die live abgefragte GitHub-Referenz waren danach
identisch. Exakt die 29 vorgesehenen Dateien im Commit, verfolgter Arbeitsbaum sauber;
31 vorherige unversionierte Dateien weiterhin erhalten.

**LFS:** Keine LFS-Dateien in diesem Paket geändert, null Objekte/Bytes zu übertragen,
keine ausstehenden LFS-Uploads. Kein neuer LFS-Download als Nachweis behauptet.
Dieser Verifikationsnachtrag wird getrennt gesichert; anschließend erneute Live-Prüfung
von `main`/`origin/main`. Finale Git-Nachweise bleiben lokal in
`Saved/ProjectRefinement/GameplayPraxisV1/FinalGit.json`.
Keine Bilder, Videos, Saves, Caches oder Builds hochladen. Vollbackup
`03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unverändert erreichbar.
