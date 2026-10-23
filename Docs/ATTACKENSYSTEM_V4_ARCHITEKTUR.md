# Attackensystem V4 – gemeinsame Effektarchitektur, Teilpaket

## Geltungsbereich

Dies ist eine kompatible technische Grundlage mit geprüften Integrationsfällen. Die 49 fehlenden Lernattacken sind noch nicht als neue Produktionsassets aktiviert. Der genaue Restumfang steht im Wirkungsplan. Vor allem neue Status-/Spezialregeln und Volltreffer dürfen nicht unbemerkt eine andere Generation oder ein anderes Balancing einführen.

Die bestehende BattleSession bleibt die einzige Rundenauswertung für ClassicBattle und WorldBattle. Presenter, Darstellung und Encounter verwenden weiterhin dieselbe Sitzung. Keine zweite Kampflogik, NPC-, Fortschritts- oder Save-Architektur.

## Datenvertrag

`UPokeMonsterMoveData.Effects` ist eine geordnete Liste typisierter Effektbausteine. Eine explizite Liste hat Vorrang vor der bisherigen einzelnen Effektkennung. Bleibt sie leer, werden vorhandene Attackenkennungen kompatibel übersetzt. Leech Seed und Struggle behalten ihre bisherigen Lebenszyklen und Identitäten.

| Baustein | Gemeinsame Verarbeitung | Grenze |
|---|---|---|
| Stage | Angriff, Verteidigung, Spezial-Angriff, Spezial-Verteidigung, Initiative, Genauigkeit, Ausweichen; ±6; Meldung an Grenze | Originaldaten müssen Stufe und Ziel definieren |
| PrimaryStatus | Verbrennung plus ausdrücklich aktivierbare Paralyse, Schlaf, Vergiftung, Einfrieren; konfigurierbare Chance/Immunität | Neues Statusprofil ist standardmäßig aus; keine Behauptung vollständiger Gen-2-Regeln |
| Heal / Drain / Recoil | Bruchteil von maximalen KP bzw. tatsächlich entfernten KP, Mindestwirkung 1 bei positiver Fraktion, Überheilung/Overkill begrenzt | Keine erfundenen Wetter- oder Tageszeitregeln |
| FixedDamage | Konstante KP oder Anwenderlevel; Typimmunität bleibt wirksam | Keine pauschale Normalisierung von Typimmunitäten |
| MultiHit | Explizite Trefferzahlgewichte; AP einmal, Trefferprüfung einmal, Abbruch beim KO | Verteilung vor Bindung jeder Originalattacke prüfen |
| Flinch / Confusion | Aktionsverhinderung und kampflokale Verwirrung; Zurücksetzen beim Wechsel | Technisches Profil, kein Ersatz fehlender finaler Originaldaten |
| Protect / Screen | Einrundenschutz mit konfigurierbarer Folgechance; zeitweiser Spezialschutz des Teams | Exakte Generationsausnahmen noch vor Produktionsbindung prüfen |

Unfertige deklarierte Effektarten wie Aufladen, Bindung, Wetter, Groll und Abgangsbund werden von `IsConfigured()` abgewiesen. Volltrefferboni sind bis zur Regelfestlegung ebenfalls nicht zulässig. Doppelte Treffer-/Fixschaden-Steuerbausteine, ungültige Brüche, Wahrscheinlichkeiten und Verteilungen werden abgewiesen. Eine unvollständige Konfiguration wird nicht als scheinbar fertige Attacke aktiviert.

## Rundenauswertung

Auswahl und Daten werden vor Mutation validiert. Runde und Zufallsstrom werden gemeinsam auf einer vorläufigen Kopie verarbeitet und erst bei erfolgreicher Auflösung übernommen. Ungültige Auswahl verändert weder AP noch Runde oder Zufallsfolge. Chancewerte 0 und 100 sind reproduzierbar getestet; der bisherige zusätzliche Zufallszug für zulässige alte Verbrennungs-/Initiativeeffekte bleibt erhalten.

Aktionsverhinderung wird vor AP-Verbrauch geprüft. Bei einer tatsächlich versuchten, aber verfehlten oder geschützten Attacke werden AP verbraucht. Ein Mehrfachtreffer verbraucht nur einmal AP; nach KO folgen keine weiteren Treffer. Absorption und Rückstoß verwenden den tatsächlich entfernten Schaden. Die bisherigen Regeln für Fang, Flucht, Wechsel, Ohnmacht und Erfahrung bleiben aktiv.

Spezialstufen werden nun genauso wie vorhandene physische Stufen auf die jeweilige Berechnung angewandt. Die bisherige Schadensformel bleibt ansonsten erhalten: weiterhin kein STAB, keine Volltreffer oder Schadensstreuung, keine Umstellung auf die historische typgebundene Physical-/Special-Aufteilung. Neue Schutz-/Statusprofile werden ausdrücklich über den vorhandenen Encounter-Vertrag an dieselbe Sitzung übergeben; normale Begegnungen wählen sie nicht automatisch.

## Speichern und Fortschritt

Save-Version 7 ergänzt den individuellen Schlafzähler. Die bisherigen Statuswerte None=0 und Burn=1 bleiben unverändert; neue Werte werden angehängt. Versionen 1–6 werden weiter gelesen. Aktive Attacken, persönliches Repertoire, AP und offene Lernangebote bleiben in den bisherigen Datenstrukturen. Kein freies Neuordnen außerhalb des Meisters. Dessen bestehender Vergleichsschutz berücksichtigt nun auch den Statuszähler.

Flinch, Verwirrung, Schutz und Stufen bleiben kampflokal. Ein Pokémon-Wechsel setzt individuelle volatile Effekte zurück; ein Team-Spezialschutz bleibt am Team bis zum Ablauf. Anhaltende Primärstatusdaten können mit Status und Zähler gespeichert werden. Normales Heilen entfernt Status und Zähler und erhält die bisherige zulässige AP-Heilung.

## Darstellung

Die ClassicBattle-Oberfläche und Kameras werden nicht neugestaltet. Der vorhandene Ereignispfad erhält Meldungen und allgemeine Statuskürzel. Mehrfachtreffer werden zu einer korrekten kumulierten KP-Animation zusammengeführt. Rückstoß, Vergiftung, Verwirrung und Heilung verwenden den vorhandenen KP-Darstellungspfad. Wirksame Statuskombinationen dürfen nicht mehr fälschlich den alten Hinweis „keine Wirkung“ anzeigen. Neue aufwendige VFX entstehen nicht; spezifische visuelle Spezialeffekte bleiben offen.
