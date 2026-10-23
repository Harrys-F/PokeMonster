# Attackenverwaltung V2 – reproduzierbare Prüfungen

Nur im bestehenden Projekt `/Users/harry/Developer/PokeMonster` ausführen.
Keine Map, Quelle oder Originaldatei wird durch diese Werkzeuge gespeichert.
Kontrollmedien und Ergebnisse bleiben ausschließlich unter `Saved`.

## Normale Bedienung

X / Tab öffnet das vorhandene Reisebuch. L/R wechselt zyklisch zwischen
Team, Inventar und Attacken. „Attacken“ ist eine **reine Ansicht**. Pokémon und
Attacke über Steuerkreuz/↑↓ wählen; B/Enter bestätigt, A/Esc geht zurück.
Das vorhandene Tauschen von Teamplätzen und die Begleiterbestimmung bleiben
in der Teamkategorie. Die Attackenansicht bietet keinen Loadout-Schreibzugriff.

## Wiederverwendbare NPC-Anbindung

Ein vorhandener `APokeMonsterNPC` erhält in der Instanz
`Service = RememberMoves` und den Anzeigenamen „Meister der Erinnerungen“.
Er benötigt für diesen Dienst kein zusätzliches Dialog-Data-Asset.
Der bestehende Interactable-Vertrag, B/E-Eingang und Controller öffnen den Dienst.
Keine separate NPC-, Interaktions-, Speicher- oder Kampfarchitektur.

**Noch keine permanente Platzierung:** Die Weltintegration ist für das versteckte,
optionale Wissenstal reserviert. Keine Ersatzplatzierung im Heilhaus oder Startdorf.
Das Gebiet ist im derzeitigen Bestand nicht als spielbarer Wissensort mit Zugang
identifiziert. Erst nach dessen tatsächlicher Ausarbeitung einen vorhandenen NPC
vor Ort konfigurieren; dieses Werkzeug legt keine Region oder Karte an.

Im Meistermenü:

1. Team-Pokémon auswählen.
2. Erlernte Attacken mit B auswählen. Eine aktive Attacke wird aus dem Entwurf
   genommen; eine inaktive angefügt. Bei vier Plätzen zuerst einen Ersatzplatz wählen.
3. Zum Neuordnen eine aktive Attacke herausnehmen und an gewünschter Stelle
   in gewünschter Reihenfolge wieder anfügen oder die vorhandenen Plätze gezielt ersetzen. Alle Änderungen
   sind zunächst ausschließlich ein Entwurf; bis zu vier eindeutige Attacken,
   mindestens eine aktive Attacke. Vier physische Kampfslots bleiben bestehen.
4. Unterhalb des Repertoires „Entwurf prüfen“ wählen.
5. B übernimmt und speichert atomar im bestehenden Dev-Slot. A geht zum Entwurf
   zurück. Zur Pokémon-Auswahl zurückgehen oder Schließen verwirft den Entwurf.

Geprüft werden NPC-Dienst, tatsächliche Reichweite, gleiche Welt, kein Kampf,
identische individuelle Pokémon-Daten seit dem Öffnen und keine offenen
Lernangebote. Verlässt der Meister die Reichweite oder wird entfernt, schließt
der Dienst. Fehlgeschlagenes Speichern setzt den Laufzeitzustand zurück.
L/R, I/T und andere Kategorien erlauben im Meistermenü keinen Umweg.

## Technischer Testaufbau

Nur Editor/Development; niemals als dauerhafte Weltplatzierung ausgeben:

- Normalen PIE-Lauf in VisualV2 starten.
- Konsole: `pm.MoveManagementV2.Prepare`. Bei vorhandenem Dev-Spielstand wird
  dieser Fixture-Befehl ausdrücklich verweigert. Für reproduzierbare Tests den
  folgenden Runner mit Save-Schutz verwenden.
- Der Befehl ersetzt ausschließlich das flüchtige Testteam durch zwei Schiggy
  mit unterschiedlicher Lernhistorie und erzeugt `TechnicalTest_MasterOfMemories`
  100 cm in Interaktionsrichtung. Er schreibt selbst keinen Spielstand.
- Interaktion über normales B/E. Ein **bestätigter** Meisterabschluss speichert
  absichtlich über den regulären Speicherpfad. Für automatisierte Tests deshalb
  ausschließlich den folgenden Runner mit Save-Schutz verwenden.

Mit dem sauberen `ArtSession.py`-Editor:

```sh
python3 Tools/MoveManagementV2/RunReview.py EindeutigerAlphanumerischerName
```

Der Runner hält den originalen Dev-Slot vorübergehend unter einem eindeutigen
`moves-v2-held.sav`-Namen, prüft konkurrierende Schreibzugriffe und restauriert
anschließend die ursprünglichen Bytes/SHA-256. Ein Prüffehler wird nicht
verschwiegen. Bei Timeout nicht manuell überschreiben: Sitzung und gehaltenen
Slot zuerst prüfen. Keine Projektkopie und kein vollständiges Backup.

Die Prüfung verwendet echte PIE/UMG-Menüs und simulierte Slate-Eingaben,
keinen physischen Controller. Die sechs Screenshots stammen vom nativen
Slate-Viewport. Die tatsächliche Bildgröße steht in `CaptureValidation.json`;
logische 2560×1440 sind nicht automatisch native QHD-Bildpixel.

`MapChecks.py` lädt und prüft die elf vorhandenen Maps lesend, inventarisiert
Actor-Namen/Klassen/Positionen/Tags und sucht benannte Tal-Assets. Das Ergebnis
ist ein Standortbefund, kein Beweis über jede unbenannte Landschaftsform.

## Datenvertrag

`FPokeMonsterCreatureInstance::LearnedMoves` enthält eindeutige
`FPokeMonsterMoveSlot`-Datensätze einschließlich AP. Aktive Slots behalten ihr
bestehendes Format. Erlernen und Verbrauch synchronisieren die persönliche
Erinnerung; Reaktivieren kopiert den AP-Zustand und initialisiert ihn niemals neu.
Heilung restauriert legitim aktive **und inaktive** AP. Neue Levelattacken folgen
weiter V1; abgelehnte/offene Angebote werden nicht gelernt.

Save-Schema 6 serialisiert stabile Move-IDs und AP für das Repertoire.
Versionen 1–5 bleiben lesbar und übernehmen nur tatsächlich aktive Attacken.
Vor V2 vergessene, damals nicht gespeicherte Kenntnisse sind nicht rekonstruierbar.
Historische technische Doppelbelegungen bleiben im alten aktiven Set erhalten;
für die eindeutige Erinnerung wird der niedrigste vorhandene AP-Stand verwendet.
Ein neues Meisterset erlaubt keine Doppelbelegung und füllt keine AP auf.

`SetActiveLearnedMoves` ist privat; der einzige Produktionsaufrufer ist die
autorisierte Transaktion im bestehenden EncounterSubsystem. Das technische
`AssignMove` für Erstellung/Lernen ist kein UI-Dienst. Erweiterungen um besondere
Lehrer oder Entwicklungsprüfungen müssen explizite eigene Bedingungen erhalten;
dieser Dienst schaltet keine unbekannten Attacken oder Entwicklungen frei.


## Vollständiger Gameplay-Nachweis

```sh
python3 Tools/MoveManagementV2/ValidateGameplay.py EindeutigerFußlaufname
```

Der ältere Fußlauf-Runner wertet seinen zusätzlichen ClassicBattle-Beobachter
nicht selbst aus. Dieser Validator prüft ausdrücklich auch `CreatureGameplay.json`
und Save-Restaurierung. Ein fehlgeschlagener Zusatzbeobachter ist kein vollständiger
Gameplay-Pass. Die bestehende strenge Positionsschwelle wurde nicht gelockert;
`Tools/GlumandaV11/ObserveGameplay.py` protokolliert nun den tatsächlichen Delta-
und Geschwindigkeitswert, falls die Positionsprüfung scheitert. Der erste
sporadische Glurak-Hinweis dieses Auftrags bleibt im Bericht ausdrücklich erhalten.
