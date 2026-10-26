# Weltuhr V1 – Nutzung und Schnittstellen

## Spielregeln

Ein neuer Spielzustand beginnt an **Tag 1 um 09:00 Uhr**. Ein Spieltag dauert
standardmäßig **120 Echtminuten**. Die Umrechnung lautet:

`Spielsekunden = Echtsekunden × (1440 / Echtminuten_pro_Tag) × Debugmultiplikator`.

Bei 120 Echtminuten sind das 12 Spielsekunden je Echtsekunde: eine Spielminute
nach fünf Sekunden, eine Spielstunde nach fünf Minuten. Die Uhr verwendet keine
Systemuhr und berechnet nach dem Beenden keine Offlinezeit nach.

| Phase | Einschließlich Beginn, ausschließlich Ende | Echtzeit bei 1× |
|---|---|---:|
| Früher Morgen | 04:00–05:00 | 5 Minuten |
| Morgendämmerung | 05:00–07:00 | 10 Minuten |
| Tag | 07:00–18:00 | 55 Minuten |
| Abenddämmerung | 18:00–20:00 | 10 Minuten |
| Nacht | 20:00–04:00, über Mitternacht | 40 Minuten |

Die gespeicherte Uhr beeinflusst in V1 **weder Beleuchtung noch Pokémon-Verhalten**.
Auch eine eingestellte Nacht sieht deshalb vorerst wie die bisherige VisualV2 aus.

## Architektur und Konfiguration

`UPokeMonsterWorldClock` ist ein `UGameInstanceSubsystem`. Dieselbe Instanz bleibt
bei `OpenLevel` und bei Innenraumwechseln erhalten. Keine Uhr-Actors pro Map.
`OnWorldPreActorTick` verarbeitet ausschließlich die Spielwelt der eigenen
GameInstance und höchstens einmal pro Engineframe. `FApp::GetDeltaTime()` liefert
die reale Framedauer, unabhängig von Gameplay-Zeitlupe und World-Delta-Begrenzung.
Doppelte Sekundenpräzision, ganze Tage und Restsekunden vermeiden minutenweise
Rundung. Lange Frames dürfen mehrere Phasen oder Mitternacht überschreiten.
Der erste Frame einer neuen Welt bzw. nach dem Wiederherstellen wird nicht als
nachzuholende Ladezeit gerechnet.

Zentrale Einstellungen in `Config/DefaultGame.ini`, Abschnitt
`/Script/PokeMonster.PokeMonsterWorldClockSettings`:

- `RealMinutesPerDay=120.0`.
- `PhaseStartMinutes`: 240, 300, 420, 1080, 1200, in der obigen Phasenreihenfolge.
- Unreal-Arrays mit `!PhaseStartMinutes=ClearArray` und fünf
  `+PhaseStartMinutes=...`-Einträgen schreiben. Fünf verschiedene, aufsteigende
  Grenzen zwischen 0 und 1439 sind erforderlich.
- Ungültige Konfiguration fällt vollständig auf die Standardkonfiguration zurück.
  Keine Änderung der Geschwindigkeit an mehreren Gameplay-Stellen erforderlich.

## Pausen

Die Uhr liest bestehende Zustände, statt deren Eingabe- oder Pauseverwaltung zu
ersetzen: Reisebuch/Hauptmenü und Untermenüs einschließlich Attackenmeister,
Entwicklungspräsentation, Dialog, aktive Begegnung, Save-Ladevorgang,
Niederlagenrückkehr, fehlende/beginnende Spielwelt und ausdrückliche Unreal-Pause.
Auch die optionale WorldBattle wird wie andere befehlsbasierte Kämpfe angehalten;
ihre Kampfregeln bleiben unverändert. Der Editor-PIE-Pausenschalter ist ebenfalls
Unreal-Pause.

Alle Gründe werden gemeinsam geprüft. Beispielsweise hebt `resume` nur die
Debugpause auf; ein offenes Menü hält die Uhr weiter an. Es gibt keine Freigaben,
die einen anderen Grund löschen könnten. Normale Bewegung im Innenraum lässt die
Uhr weiterlaufen. Kein Zeitsprung bei Ohnmacht. Während synchroner Ladevorgänge
gibt es keine nachträgliche Fortschreibung der verstrichenen Ladezeit.

## Speichern und Laden

Save-Schema **10** erweitert das vorhandene `UPokeMonsterSaveGame` um
`bHasWorldTime` und `FPokeMonsterWorldTime` (Tag, Sekunden seit Mitternacht).
Keine zusätzliche Datei, keine gespeicherten Pausen und kein gespeicherter
Debugmultiplikator. Alle echten Save-/Load-Wege und der bestehende RAM-Testschutz
verwenden dieselben Snapshot-Funktionen. Die Zeit wird erst nach erfolgreicher
Validierung/Übernahme der übrigen Spieldaten wiederhergestellt.

Versionen 1–9 sowie fehlende/ungültige Zeitdaten verwenden Tag 1, 09:00 Uhr.
Dabei bleiben Team, AP, Repertoire, Inventar, Position, Blickrichtung,
Innenraumkontext und Kontrollpunkt dem bisherigen Speichersystem überlassen.
Laden schreibt keine automatische Migration in den alten Slot.

Neue PIE-Sitzungen sind weiterhin neue Spielsessions; einen vorhandenen Stand
über das bestehende **Hauptmenü → Laden → Bestätigen** fortsetzen. Es wird weder
nur die Uhr aus einem fremden Slot vorab eingelesen noch ungefragt ein Nutzersave
automatisch geladen. Nach regulärem Laden – auch nach Editor-/Anwendungsneustart –
gilt exakt die gespeicherte Zeit. Der Debugmultiplikator einer neuen Session ist 1×.

Normales Laden stellt die gespeicherte Weltposition wieder her. Die unabhängige
Niederlagenrückkehr und ihr separater automatischer Slot bleiben erhalten.

## Anzeige und Entwicklerbefehle

Im Kopf des vorhandenen Reisebuchs steht beispielsweise `Tag 3 – 16:42 Uhr`.
Keine zusätzliche dauerhafte HUD-Anzeige. Der bestehende 0,25-s-Menürefresh wird
wiederverwendet; der Rendercache berücksichtigt die angezeigte Minute, nicht jede
Sekunde. B/A/X/L/R/+ und Tastaturbelegung bleiben unverändert.

Im Editor einen gewöhnlichen PIE-Test starten und die **Output-Log-Konsole** öffnen:

| Befehl | Verwendung |
|---|---|
| `pm.WorldClock` oder `pm.WorldClock show` | Tag, Uhrzeit, Phase, Tagesfortschritt, Pause, Geschwindigkeit, Tageslänge ausgeben |
| `pm.WorldClock set 3 16 42` | Tag 3, 16:42:00 setzen |
| `pm.WorldClock set 3 23 59` | Mitternachtswechsel vorbereiten |
| `pm.WorldClock pause` | Entwicklerpause einschalten |
| `pm.WorldClock resume` | Nur Entwicklerpause aufheben |
| `pm.WorldClock speed 5` | 5× normale Geschwindigkeit; ebenso 10 oder 60 |
| `pm.WorldClock speed 0.5` | Auf halbe normale Geschwindigkeit verlangsamen |
| `pm.WorldClock reset` | Geschwindigkeit 1× und Entwicklerpause aus; Uhrzeit bleibt erhalten |
| `pm.WorldClock end` | Vom Debugbefehl gestarteten RAM-Test verwerfen und ursprünglichen Sessionzustand wiederherstellen |

Positive Multiplikatoren bis 3600 sind zugelassen; 0, negative und nicht endliche
Werte sowie ungültige Tage/Stunden/Minuten werden abgewiesen. Genau eine PIE-Welt
muss laufen. Die Befehle und Zeitmutatoren werden nur mit `WITH_EDITOR` gebaut;
in regulären Builds gibt es sie nicht.

**Speicherschutz:** Vor der ersten Änderung aktiviert der Befehl den bestehenden
PIE-RAM-Testschutz, sofern nicht bereits ein isolierter Testslot/RAM-Test aktiv ist.
Normale und automatische Save-Aufrufe bleiben dann im RAM. `end` stellt den
Zustand vor dem Test wieder her, einschließlich Team/Inventar/Zeit; ist ein anderer
Spielzustand noch aktiv, zuerst Kampf oder Dialog beenden. Bei ausdrücklich
isoliertem Testslot ist dessen Teststeuerung zuständig, `end` beendet keinen
beliebigen fremden Test. PIE stoppen verwirft alle temporären Debugzustände.

## Gemeinsame API für spätere Systeme

C++: `GameInstance->GetSubsystem<UPokeMonsterWorldClock>()`; dieselben Getter sind
als Blueprint-Pure-Funktionen verfügbar:

- `GetTime`, `GetDay`, `GetHour`, `GetMinute`, `GetPhase`.
- `GetDayFraction`: normierter Tagesfortschritt in `[0, 1)`.
- `IsClockPaused`, `GetTimeLabel`, `GetRealMinutesPerDay`.
- `OnPhaseChanged`, `OnDayChanged`, `OnTimeSet`: Blueprint-Ereignisse. Fortschritt
  meldet alle überschrittenen Grenzen, gezieltes Setzen/Laden den neuen Zustand.

Zeitänderungen für produktives Gameplay sind in V1 nicht öffentlich schreibbar;
Save-Restore und geschützte Editorbefehle sind die vorgesehenen Wege.
KI, Begegnungen, Sonnenbewegung, Himmel und Wetter sind **noch nicht angebunden**.
