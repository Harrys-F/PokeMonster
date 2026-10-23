# Entwicklungen manuell im normalen PIE testen

Projekt: `/Users/harry/Developer/PokeMonster`. Bestehende Map `/Game/Maps/Dev_TestMap_VisualV2`. Nur Editor/PIE, keine neue Karte und keine zweite Entwicklungslogik.

## Empfohlene Bedienung

1. VisualV2 im Editor öffnen und **normal Play/PIE** starten. Nur eine PIE-Instanz verwenden. Außerhalb von Kämpfen/Dialogszenen alle Menüs schließen.
2. Unten im Editor die **Cmd**-Konsolenzeile verwenden oder **Fenster → Entwicklerwerkzeuge → Output Log** öffnen. Im **Cmd**-Modus arbeiten (nicht Python). Dort folgende Befehle einzeln abschicken:

```text
pm.EvolutionTest.List
pm.EvolutionTest.Start 1
```

**Nach dem Befehl die Spielansicht anklicken beziehungsweise die Ingame-Konsole schließen**, damit B/Enter und A/Esc wieder die Entwicklungsansicht bedienen und nicht das Konsolen-Eingabefeld.

`List` zeigt das **aktuelle** Team mit Nummern **1–6**, Name, Level, individueller ID und testbarer Zielart. `Start 1` wählt Teamplatz 1; beispielsweise `Start 3` wählt ausschließlich das dritte Team-Pokémon. Es wird kein anderes Team angelegt und kein Pokémon hinzugefügt. IDs und Teamreihenfolge bleiben erhalten. Der Begleiterplatz wird nicht umsortiert.

Der erste gültige Start aktiviert **vor der Teamänderung** einen RAM-Speichertransport im vorhandenen Save-Subsystem. Während der gesamten Testsitzung schreiben normale Speicheraktionen, automatische Angebote, Bestätigung, Abbruch, Heilen und Menü-Speichern ausschließlich in den Arbeitsspeicher. Auch Laden verwendet diesen Testzustand; Löschen des normalen Dev-Saves ist gesperrt. Es entsteht keine Save-Kopie auf der SSD. Der normale Spielstand wird nicht überschrieben. Der zugrunde liegende direkte Schreibhelfer sperrt währenddessen ebenfalls den normalen Slot.

- **Glumanda im gewählten Slot:** vorhandene XP-Vergabe hebt das Level bei Bedarf auf **16**. Das reguläre Angebot ist **Glutexo**.
- **Glutexo im gewählten Slot:** gleiche Vorgehensweise bis **36**, Ziel **Glurak**.
- Bereits höhere Level bleiben erhalten. Es gibt kein Zurückstufen und kein direktes Überspringen der Zwischenform.
- Eventuelle echte Attackenlernangebote aus dem Levelgewinn erscheinen **zuerst**. B/Enter zum Lernen/Ersetzen, Steuerkreuz/Pfeile zur Slotwahl, A/Esc zum Ablehnen. Nichts wird automatisch als gelernt markiert.
- Anschließend erscheint die bestehende vollständige Entwicklungsansicht: **B / Enter** startet, **A / Esc** bricht ab. Abbruch ist auch während der fünfsekündigen Vorschau möglich. Nach Erfolg oder Abbruch mit **B / Enter** zur Oberwelt zurückkehren; eventuelle weitere Lernangebote vorher entscheiden.
- Für die zweite Stufe nach Glutexo-Erfolg einfach erneut `pm.EvolutionTest.Start 1` mit demselben Teamplatz eingeben. Ein bereits vorhandenes Glutexo kann direkt so geprüft werden.
- Nach einem Abbruch kann derselbe `Start`-Befehl erneut ausgeführt werden. Nur die Testkopie erhält dafür zurückgesetzte Angebots-Metadaten; normale Wiederholungsregeln bleiben unverändert.
- Ein gewähltes K.O.-Pokémon bekommt im Test mindestens einen KP, damit das reguläre Angebot geöffnet werden kann. AP, Repertoire, Status und individuelle Identität werden nicht neu erzeugt; reguläre Leveländerungen berechnen die Werte wie bisher.

Falls `pm.Evolution.Auto` früher manuell auf 0 gesetzt wurde, zuerst `pm.Evolution.Auto 1` eingeben. Standard einer frischen Editorsitzung ist 1. Der neue Befehl ändert diesen globalen Schalter nicht ungefragt.

## Test verlassen – wichtig

```text
pm.EvolutionTest.End
```

Dieser Befehl beendet auch eine noch offene Entwicklungsvorschau und stellt **Team, Inventar, Chronik-/Questdaten und Heilpunktzustand vom ersten Teststart** wieder her. Auch zwischenzeitlich im Test gefangene Pokémon/Items/Fortschritte werden verworfen. Bei laufendem Kampf, Dialog oder anderem Menü zuerst zur Oberwelt zurückkehren. Schlägt die Wiederherstellung fehl, bleibt der RAM-Schutz aktiv; dann PIE regulär stoppen.

Alternativ **PIE stoppen**: Der ausschließlich in dieser Game Instance lebende Testzustand wird verworfen, ohne die normale Save-Datei anzufassen. Ein erneuter PIE-Start arbeitet wieder normal. Nach erfolgreichem `End` ist normales Speichern bewusst wieder aktiv. Spielerposition/Kamera werden durch den Konsolenbefehl nicht verändert.

Kein Export des Testteams in den echten Spielstand vorgesehen. Außerhalb von PIE, bei mehreren PIE-Welten, ungültigem Slot, uneindeutiger Route, fehlendem Zielmodell, Kampf oder gesperrtem Kontext wird die Aktion abgewiesen. Die Befehle und der RAM-Testtransport sind mit `WITH_EDITOR` ausgeschlossen und stehen in regulären gepackten Development-/Shipping-Builds nicht zur Verfügung.

## Bereits vorhandene technische Befehle

Diese alten Prüfaufbauten bleiben für bestehende automatisierte Werkzeuge erhalten. **Nicht als sicheren manuellen Einstieg verwenden:** Sie aktivieren für sich allein keinen RAM-Speicherschutz.

```text
pm.EvolutionReview.Party Zunderlauf 15
pm.EvolutionReview.Party Glutexo 35
pm.EvolutionReview.XP next
pm.EvolutionReview.XP 100
pm.EvolutionReview.Victory
pm.EvolutionReview.Victory current
pm.EvolutionReview.Capture EINDEUTIGERNAME
```

- `Party <Zunderlauf|Glutexo> <Level>` **ersetzt das komplette Laufzeitteam** durch eine Prüf-Instanz plus unabhängiges Reserve-Glurak. Glumandas stabile historische Art-ID ist `Zunderlauf`, nicht `Glumanda`.
- `XP next` oder eine nichtnegative XP-Zahl betrifft nur das **erste** Team-Pokémon. Bestehende XP-/Lernlogik wird verwendet.
- `Victory` startet einen technischen ClassicBattle-Sieg-Prüfaufbau mit Glumanda kurz vor Level 16 und einem 1-KP-Gegner; `current` verwendet das aktuelle Team.
- `Capture NAME` erstellt einen separat gerenderten echten QHD-UMG-/3D-Nachweis der offenen Entwicklungsansicht unter Saved; kein gewöhnlicher Screenshot des Mac-Viewportfensters.

Ohne den neuen RAM-Testmodus können die regulären Lern-/Entwicklungsaktionen dieser alten Fixtures in den normalen `PokeMonster_Dev`-Slot speichern. Ihre bisherigen externen QA-Runner sichern/restaurieren deshalb Savebytes gesondert; das ist für den Nutzer nun nicht mehr erforderlich.

## Prüfung dieses Arbeitspakets

Stand 23.10.2026, Ausgangscommit `24ed5d48`:

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build `EvolutionManual_Build02` | Exit 0 |
| Vollständige Automation `EvolutionManual_Automation01` | **188 fachlich bestanden**: 185 ohne Testwarnungen, drei mit externer iOS-Helferwarnung; 0 Fehler / 0 nicht ausgeführte Tests |
| Neuer Automationstest `PokeMonster.EvolutionV2.ManualPIETestConditions` | Bestanden: beide echten Levelrouten, ID/AP-Erhaltung, wiederholbarer Abbruch, keine Rückstufung, fehlendes Ziel, Nicht-PIE-Sperre |
| Strenger QA-Wrapper | **Exit 1, nicht bestanden**, wegen `idevice_id: posix_spawn failed (86, Bad CPU type in executable)` und `Failed to launch Tool`; Warnungen in Bite, VitalThrow und HealingHouse.CollisionAndCutaway. Keine Abschwächung des Wrappers |
| Elf bestehende Maps, `ManualEditor01.log` | Je 0 Fehler und 0 Warnungen; ohne Speicherung |
| Normaler echter Editor-PIE-Lauf `ManualPIE02` | **49 Schritte, 14 Abnahmeprüfungen bestanden**, vier echte Slate-Viewportbilder |
| Bestehendes individuelles Glutexo | Reguläres Lernangebot, Glurak-Entwicklung, späte Stornierung und vollständige Bestätigung; gleiche ID, AP und XP; keine Änderung der übrigen Instanzen |
| Gezielter Teamplatz 2 | Glumanda→Glutexo→Glurak auf demselben Platz und mit derselben ID; Slot 1 unverändert. Glumanda-Prüfteam ausdrücklich erst innerhalb des bereits aktiven RAM-Schutzes vorbereitet |
| Speichern/Laden/Löschen | Evolved-Testzustand in RAM gespeichert und geladen, normaler Slot unverändert; Löschen des normalen Slots abgewiesen |
| Test beenden | End bei abgebrochener und erfolgreicher Sequenz stellt gesamtes ursprüngliches Team samt Angebotsdaten wieder her |
| PIE stoppen / erneut normal starten | RAM-Test verworfen, normaler Spielstand unverändert ladbar, keine Testinstanz in der nächsten Game Instance |

Der erste Nachweis `ManualPIE01` scheiterte an einem **Fehler des Python-Vergleichs**: `str(PrimaryAssetId)` enthielt eine wechselnde Speicheradresse. Beide verglichenen Teams und die Savebytes waren tatsächlich gleich. Der Vergleich benutzt jetzt stabile Assettyp/-namen; `ManualPIE02` vollständig bestanden. Dies war kein maskierter Projektfehler und erforderte keine Save-Wiederherstellung.

Die beim Auftragsbeginn bereits laufende Nutzersitzung entwickelte Glumanda selbst zu Glutexo und änderte dabei den regulären Save. Nach ausdrücklicher Freigabe zum regulären Editor-Schließen wurde **dieser neueste Nutzerstand** bewahrt. Kein älterer Save wurde darüber restauriert. Seit Beginn der eigentlichen neuen Prüfläufe blieb seine SHA-256-Prüfsumme durchgehend `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`. Der QA-Runner kopiert/restauriert keine Save-Dateien.

Lokale, nicht hochgeladene Nachweise:

- `Saved/GlutexoEvolutionV2/ManualPIE02/Result.json`, `SaveUnchanged.json`, `Restart.json`.
- `Saved/GlumandaV11/LiveUI/ManualPIE02LatePreview/ActualSlateViewport.png`.
- `Saved/GlumandaV11/LiveUI/ManualPIE02RealMemberSuccess/ActualSlateViewport.png`.
- `Saved/GlumandaV11/LiveUI/ManualPIE02GlutexoComplete/ActualSlateViewport.png`.
- `Saved/GlumandaV11/LiveUI/ManualPIE02GlurakComplete/ActualSlateViewport.png`.

Wiederholbar über `Tools/GlutexoEvolutionV2/RunManualEvolution.py EINDEUTIGERLABEL` in einer regulär über vorhandenes `ArtSession.py` geöffneten Editorsitzung; der aktuelle normale Save muss ein Glumanda oder Glutexo enthalten. Das ist ein expliziter Prüfaufbau, keine neue Karte. Keine Bilder oder temporären Saves im Commit.

Physischer Controller-Test ist nicht Bestandteil dieses Nachweises. Bestehende B/A-Zuordnung bleibt unverändert. Der Editor-/PIE-Guard ist im Quellcode geprüft; kein zusätzlicher paketierter Shipping-Build wurde erzeugt.
