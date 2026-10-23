# Spielregeln und Mechaniken – PokeMonster

## Status dieses Dokuments

Dieses Dokument unterscheidet zwischen beschlossenen Regeln und noch offenen Entwürfen. Offene Punkte dürfen nicht ohne Rücksprache als endgültige Vorgabe umgesetzt werden.

## Grundregeln

Beschlossen:

- Einzelspieler
- 2D-Top-Down-Perspektive
- Erkundung einer zusammenhängenden Fantasywelt
- Kreaturen können gesammelt und im Kampf eingesetzt werden
- die Demo enthält nur einen kleinen Teil des später möglichen Umfangs
- normale Levelentwicklungen bleiben grundsätzlich erhalten
- bisherige Tauschentwicklungen erhalten besondere eigene Bedingungen

## Begegnungen mit Kreaturen

Die genaue Darstellung wilder Kreaturen ist noch offen.

Mögliche Varianten:

- sichtbare Kreaturen in der Spielwelt
- Begegnungen in bestimmten Geländearten
- eine Mischung aus beiden Systemen

Diese Entscheidung soll erst nach einem kleinen spielbaren Bewegungstest getroffen werden.

## Kampfsystem

Als Grundlage ist ein rundenbasiertes Kreaturenkampfsystem vorgesehen.

Vorläufige Merkmale:

- Kreaturen besitzen Lebenspunkte
- Kreaturen verfügen über mehrere Attacken
- vier gleichzeitig verwendbare Attacken sind als klassische Ausgangslösung vorgesehen
- Typen, Stärken und Schwächen sollen eine taktische Rolle spielen
- Statusveränderungen können später ergänzt werden
- Kämpfe sollen verständlich und nicht unnötig langsam sein

Noch nicht entschieden:

- spätere Erweiterungen über den technischen 1-gegen-1-Kampf hinaus
- genaue Schadensformel
- endgültige Anpassungen des Typensystems (technische 17-Typen-Grundlage siehe unten)
- spätere Änderungen der vorläufigen Reihenfolge aus Priorität, Initiative und Gleichstandregel
- Schwierigkeitsgrad
- Erfahrungskurve
- Darstellung des Übergangs zwischen Welt und Kampf

Codex darf zunächst nur eine kleine erweiterbare Grundlage erstellen und keine komplexe vollständige Kampfmathematik festlegen.

Technischer Prototypstand: Vier individuelle Moveslots, getrennte Attacken-Data-Assets, PP-Verbrauch sowie Treffer- und Schadensberechnung sind vorhanden. Die zentral gepflegte Typentabelle verwendet vorerst die 17 Typen und Matchups der zweiten Generation; Physical/Special/Status wird unabhängig davon je Attacke festgelegt. Die Battle-Session unterstützt weiterhin 1-gegen-1 und nun Teams mit bis zu sechs Kreaturen je Seite. Pro Seite ist genau eine aktiv. Priorität geht vor Initiative, bei Gleichstand beginnt Seite A. Ein freiwilliger Wechsel verbraucht den Zug; die Gegenseite kann die eingewechselte Kreatur angreifen. Nach K.O. ist ein kampffähiger Ersatz nötig, sofern vorhanden. Erst der Ausfall des ganzen Teams beendet den Kampf. Eine besiegte Kreatur greift nicht mehr an. Fehlerhafte Auswahlen werden ohne Rundenfortschritt abgewiesen. Endgültiges Balancing und weitere Kampfregeln bleiben offen; der geprüfte V3-Teilumfang steht unten. Technische Details stehen in `Docs/TECHNIK.md`.

## Niederlage, Rettung und Speichern

**Beschlossene Spielregel:** Bei einer normalen Niederlage stirbt der Spieler nicht. Er wird bewusstlos beziehungsweise kampfunfähig; eine eigene Kreatur schützt ihn oder holt Hilfe. Er erwacht an der zuletzt aktivierten Hüterstätte oder im zuständigen Heilhaus. Das Team wird dort vollständig geheilt und der Fortschritt automatisch gespeichert. Kreaturen, Erfahrung und wichtige Gegenstände bleiben erhalten. Bereits verbrauchte Gegenstände werden nicht zurückgegeben, zeitlich begrenzte Verstärkungen enden. Vorerst wird kein Geld abgezogen. Vor wichtigen Story- und Bosskämpfen sind faire Kontrollpunkte vorzusehen. Manuelles Speichern und weitere Autosaves sind ebenfalls möglich; Hüterstätten sind nicht die einzige Speichermöglichkeit.

Die Rettung durch eine eigene Kreatur macht Vertrauen statt Kontrolle spielerisch sichtbar und spiegelt den späteren Wendepunkt der wiederkehrenden Freund-/Gegenfigur.

**Bereits technisch vorhanden:** Vollständige Teamniederlagen in Wild- und Trainerkämpfen führen nach einer Ohnmachtsanzeige zum aktivierten RestPoint-Checkpoint oder ersatzweise zum PlayerStart und heilen HP/PP. Ein Dev-Slot speichert und lädt Team, Inventar, Weltfortschritt und Checkpoint; `PMSave`/`PMLoad` erlauben manuelles Speichern per Konsole. RestPoints können optional nach dem Heilen speichern. Der Testschrein aktiviert einen Checkpoint, speichert aber derzeit nicht automatisch.

**Noch nicht umgesetzt:** Die sichtbare Rettung durch eine Kreatur, Hüterstätten/Heilhäuser als ausgestaltete Orte, das automatische Speichern nach Niederlage, allgemeine Autosaves und ein reguläres manuelles Speichermenü, faire Story-/Boss-Kontrollpunkte sowie eine Verwaltung zeitlich begrenzter Verstärkungen. Die beschlossenen Verlustregeln dürfen nicht mit bereits implementierten Strafen verwechselt werden.

## Sammeln und Fangen

Das Sammeln soll glaubwürdig in Geschichte und Welt eingebunden werden.

Noch offen ist, ob Kreaturen:

- klassisch gefangen,
- durch Vertrauen gewonnen,
- durch Aufgaben überzeugt
- oder über eine Kombination dieser Methoden rekrutiert werden.

Ein endgültiges Fangsystem wird später beschlossen.

## Entwicklungen

### Normale Entwicklungen

Normale Levelentwicklungen der Generationen 1 und 2 bleiben grundsätzlich erhalten.

### Frühere Tauschentwicklungen

Tauschentwicklungen werden nicht durch einfache Levelentwicklungen ersetzt.

Sie benötigen:

1. ein festgelegtes Mindestlevel,
2. einen thematisch passenden Ort,
3. eine besondere Handlung, Prüfung oder Begegnung.

Vorläufige Beispiele:

- Kadabra: ungefähr ab Level 44 bei einem Gelehrten, Magier oder Heiligtum
- Maschock: ungefähr ab Level 36 in einem Steinbruch oder nach einer Kraftprüfung
- Georok: Entwicklung in einer besonderen Höhle oder Bergwerk-Umgebung
- Alpollo: Entwicklung in einer alten Ruine oder Geisterstätte

Die endgültigen Level, Orte und Auslöser werden später festgelegt.

Andere besondere Entwicklungsarten werden einzeln geprüft und passend für das Einzelspiel angepasst.

## Attacken und TM/VM

Das klassische TM-/VM-System soll nicht unverändert übernommen werden.

Bevorzugte Richtung:

- keine Attacken sollen nur deshalb dauerhaft blockiert werden, weil eine einmalige TM fehlt,
- Reiseaktionen sollen nicht unnötig feste Attackenplätze belegen,
- Attacken könnten über Training, Lehrer, Orte, Prüfungen oder freie Auswahl bereits erlernter Attacken verwaltet werden.

Die frühere offene Regel zur freien Auswahl ist durch die Entscheidung
„Attackenverwaltung V2“ ersetzt: Maximal vier aktive Kampfattacken; tatsächlich
erlernte Attacken bleiben im individuellen Repertoire. Levelaufstiegsangebote
können unmittelbar aktiviert oder abgelehnt werden. Nachträgliches Reaktivieren
und Neuordnen ist ausschließlich bei freigegebenen Attackenmeistern möglich.
Das normale Team-/Attackenmenü ist nur eine Ansicht. Verbrauchte AP bleiben auch
bei inaktiven Attacken erhalten. Der erste „Meister der Erinnerungen“ ist für
das versteckte optionale Wissenstal reserviert, nicht für Heilhaus oder Startdorf.
Weitere Lehrer, TM/VM-Ersatz und spezielle Techniken bleiben offen.

## Reise und Weltfähigkeiten

Vorgesehen:

- Reit-Kreaturen können später als Schnellreise oder schnellere Fortbewegung dienen.
- Fliegen, Surfen oder Schwimmen können später freigeschaltet werden.
- solche Fähigkeiten können an Spielfortschritt, Level, Vertrauen oder Prüfungen gebunden sein.
- Reiseaktionen sollen möglichst nicht das Mitführen bestimmter VM-Attacken erzwingen.

Für die erste Demo ist nur die normale Bewegung notwendig.

## Arenen und Fortschritt

Noch nicht entschieden ist, ob das Spiel:

- klassische Arenakämpfe,
- regionale Prüfungen,
- Aufgaben bestimmter Gemeinschaften,
- Wächterkämpfe
- oder ein vollständig eigenes Fortschrittssystem verwendet.

Eine eigene, zur Fantasywelt passende Lösung wird bevorzugt geprüft. Klassische Arenen dürfen nicht automatisch eingebaut werden.

## Gegenstände

Grundlegende Gegenstände sind vorgesehen, beispielsweise:

- Heilgegenstände
- Statusheilung
- wichtige Schlüsselgegenstände
- Reise- und Erkundungsgegenstände
- Ausrüstung oder Materialien, falls diese später benötigt werden

Die endgültige Gegenstandsliste und das Wirtschaftssystem sind offen.

## Schwierigkeitsgrad und Balancing

Das Spiel soll zugänglich sein, aber taktische Entscheidungen ermöglichen.

Für die Demo gilt:

- wenige klar verständliche Systeme
- keine unnötig große Gegenstandsmenge
- keine extremen Levelphasen
- kurze Testwege
- Kämpfe müssen schnell wiederholbar und leicht anpassbar sein

## Performance-Regeln

- Medium ist das primäre Testprofil.
- Die Bildrate soll begrenzt werden.
- Dauerhafte Volllast soll nach Möglichkeit vermieden werden.
- Ultra darf höhere Anforderungen besitzen, ist aber nicht der Maßstab der Demo.
- Effekte werden nur eingesetzt, wenn sie die Atmosphäre sichtbar verbessern.

## Inhalts- und Rechte-Regeln

- Keine Inhalte direkt aus ROM-Dateien extrahieren oder übernehmen.
- Keine fremden Grafiken, Sounds, Musikstücke oder Karten ohne passende Nutzungserlaubnis verwenden.
- Mittelerde dient nur als atmosphärische Inspiration.
- Für eigene Orte werden eigene Namen, Karten und Gestaltungen entwickelt.
- Eine öffentliche Veröffentlichung mit originalen Pokémon wäre ohne entsprechende Rechte nicht vorgesehen.

### Kampfpräsentation (20.10.2026, Nutzerfreigabe)
Normale Begegnungen verwenden ClassicBattle: eigene Kreatur schräg hinten links,
Gegner schräg vorne rechts, Namen/Level/KP und bestehende Kampfbefehle. Nach Ende
wird dieselbe Oberweltposition mit bisheriger Kamera wieder freigegeben. Besondere
Story-/Bossbegegnungen können WorldBattle im Begegnungsprofil wählen. Beide Modi
verwenden dieselbe BattleSession; Darstellung verändert keine Kampf- oder Save-Regeln.


### Kampfsystem V3 – aktueller spielbarer Teilumfang

Normale Wildkämpfe erlauben Flucht abhängig von Geschwindigkeit und wiederholten
Versuchen. Fehlgeschlagene Flucht verbraucht den Zug; Trainer- und geskriptete
Storykämpfe erlauben sie nicht. Heilitems im Beutel verbrauchen bei gültiger
Verwendung einen Zug und genau einen Gegenstand. Auch ein inaktives verletztes
Teammitglied kann geheilt werden; volle KP, K.O. und ungültige Ziele werden abgewiesen.

Glumanda hat auf Level 10 nach dem Gen-2-Lernstand Kratzer, Heuler und Glut; der
vierte Slot bleibt leer. Heuler senkt den Angriff des Ziels, Glut kann Verbrennung
verursachen. Verbrennung bleibt bis zur Heilung bestehen. Bei vollständig fehlenden
AP steht Verzweifler mit Rückstoß zur Verfügung. Freiwilliger Wechsel kostet den
Zug, ein notwendiger Ersatz nach K.O. keinen zusätzlichen Zug. Kampf-XP nutzen
belegte Ertragsdaten und die bestehenden Wachstumskurven. Dieser kleine Teilumfang
ersetzt die früheren offenen Flucht-/Heilitem-Platzhalter, kein endgültiges Gesamtbalancing.


### Wilde Begegnungen V2
Territoriale/aggressive Wild-Pokémon beginnen normale Kämpfe nur bei tatsächlichem Kontakt mit der Spielfigur. Ruhige, neugierige und scheue Pokémon werden über die gemeinsame Interaktionsaktion gezielt herausgefordert. Warnung, Sichtkontakt und Annäherung allein starten keinen Kampf. Begleiter sind ausgeschlossen.

Besiegte sichtbare Wild-Pokémon verlassen nach ClassicBattle sichtbar den Spielbereich; sie werden erst außerhalb des Kamerabildes entfernt. Gefangene werden direkt übertragen und entfernt. Nach erfolgreicher Spielerflucht bleiben Wild-Pokémon mit kurzer Wiederholungssperre erhalten. Besondere WorldBattle-Regeln bleiben gesondert.


## Attacken: verbindliches Kristall-Profil (V4-Fortsetzung, 23.10.2026)

Der frühere vereinfachte Prototypstand ist für normale Begegnungen durch das vom Nutzer festgelegte Kristall-/Generation-2-Profil ersetzt. Die Kategorie richtet sich bei Schadensattacken nach dem Typ: Feuer, Wasser, Pflanze, Elektro, Eis, Psycho, Drache und Unlicht sind speziell; die übrigen echten Elementtypen physisch. Fluch hat den nicht-elementaren Typ ???.

STAB, Typentabelle der zweiten Generation, Volltreffer, Schadensstreuung, Status- und Genauigkeitsstufen werden gemeinsam verarbeitet. Attackenwerte und Effekte stammen aus dem gesondert geprüften Kristall-Plan. Groll erhält den verminderten AP-Zustand im individuellen Repertoire. Die Beschränkung auf vier aktive Attacken und die ortsgebundene Neuordnung beim Meister bleiben unverändert.

Ausdrückliche Projektabweichungen bleiben: Seite A gewinnt einen Initiativegleichstand; Erfahrungsteilung und bisherige individuelle Werteberechnung bleiben erhalten. Historische reine Prototyp-Rechentests verwenden weiter das ausdrücklich getrennte Legacy-Profil, normale Begegnungen das Kristall-Profil. Zufall erfolgt mit der vorhandenen testbar gesetzten FRandomStream-Quelle, nicht mit einer ROM-Zufallsfolge. Integerüberläufe und technische Originalspiel-Bugs werden nicht absichtlich nachgebaut.

Der normale Kampfkontext ist zunächst Tag ohne Wetter. Regen entsteht durch Regentanz; Sonne und Sand können für vorhandene wetterabhängige Attacken als begrenzter Kampfkontext vorgegeben und getestet werden. Dies verändert keine Weltbeleuchtung und erzeugt kein neues Weltwetter-System. Getragene Kampfitems, Ordenboni, Delegator und weitere bislang nicht vorhandene Attackensysteme werden hier nicht eingeführt.

Nachweise und genaue Einschränkungen: `ATTACKENSYSTEM_V4_ABSCHLUSSPRUEFBERICHT.md`, `ATTACKENSYSTEM_V4_ABNAHMETABELLE.md`, Quellen mit festen Revisionen in `ATTACKENSYSTEM_V4_KRISTALL_QUELLEN.json`.


### Spielbare Levelentwicklungen V2

Glumanda/Zunderlauf entwickelt sich frühestens ab Level 16 zu Glutexo, Glutexo frühestens ab Level 36 zum vorhandenen Glurak. Angebote erfolgen im sicheren Zustand nach Kampf-/Lernabschluss. B bestätigt, A kann die laufende Präsentation vor ihrer endgültigen Übernahme abbrechen. Ein späterer Levelaufstieg oder ein anderer Kampfsieg bietet einen neuen Versuch; keine sofortige Wiederholung nach Abbruch. Eine Zwischenform wird niemals übersprungen.

Dieselbe individuelle Kreatur behält Identität, Level, numerische XP, ihre verwendete Erfahrungskurve, Status, Attackenrepertoire und verbrauchte AP. Neue Artwerte werden berechnet; fehlende KP bleiben erhalten, K.O. wird nicht geheilt. Neue Attacken am Entwicklungslevel werden regulär angeboten. Fehlende Zielmodelle blockieren die Ausführung ohne Datenänderung. Die besonderen Regeln ehemaliger Tauschentwicklungen bleiben bestehen.
