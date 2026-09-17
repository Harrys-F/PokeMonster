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
- Verlustbedingungen
- Darstellung des Übergangs zwischen Welt und Kampf

Codex darf zunächst nur eine kleine erweiterbare Grundlage erstellen und keine komplexe vollständige Kampfmathematik festlegen.

Technischer Prototypstand: Vier individuelle Moveslots, getrennte Attacken-Data-Assets, PP-Verbrauch sowie Treffer- und Schadensberechnung sind vorhanden. Die zentral gepflegte Typentabelle verwendet vorerst die 17 Typen und Matchups der zweiten Generation; Physical/Special/Status wird unabhängig davon je Attacke festgelegt. Eine getrennte Battle-Session führt inzwischen 1-gegen-1-Runden bis zum K.O. aus: Priorität vor Initiative, bei Gleichstand Seite A zuerst. Eine besiegte Kreatur greift nicht mehr an. Fehlerhafte Auswahlen werden ohne Rundenfortschritt abgewiesen. Endgültiges Balancing, Lernregeln, Status-Effekte und erweiterte Kampfregeln bleiben offen. Technische Details stehen in `Docs/TECHNIK.md`.

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

Das endgültige Attackenlernsystem ist noch offen.

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
