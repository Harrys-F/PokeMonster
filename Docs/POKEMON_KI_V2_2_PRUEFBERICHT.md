# Pokémon-KI V2.2 – Einzelprüfung Paket B

26.10.2026. Auf einzeln geprüftem Beleuchtungscommit `230ff51e`. [Maschinenlesbarer Nachweis](POKEMON_KI_V2_2_NACHWEIS.json). Gemeinsame Integration folgt mit gesondertem Nachtrag.

## Architektur

Bestehender `PokeMonsterCreatureRoamingComponent` mit seinen Aktivitäten, Kollisions-/Habitatplaner, Gefahrenprioritäten und gegenseitigen Sozialreservierungen bleibt maßgeblich. `PokeMonsterCreatureRhythm` liefert ausschließlich Multiplikatoren für die vorhandene gewichtete Auswahl. Keine zweite Uhr, kein zusätzlicher Controller/Scheduler, kein neuer Spawn, keine Animationsänderung.

`DefaultGame.ini`, Abschnitt `PokeMonsterCreatureRhythmSettings`, enthält sechs editierbare `SpeciesProfiles`. `bOverrideRhythm`/`RhythmOverride` am vorhandenen Bewegungskomponent erlauben individuelle Begegnungskonfiguration. Zuordnung/Multiplikatoren sind ohne Codeänderung anpassbar; weitere Arten können später mit bestehendem Aktivitätsprofil freigegeben werden. Aktuell nur aktive Wildaktivitäten der sechs Arten auf VisualV2, weder Begleiter noch Biom-Testmap/Westland. Unbekannte, doppelte oder ungültige Profile werden nicht aktiviert.

| Art / stabile ID | Profil | Bevorzugte Aktivität | Ruhe/Schlaf/Nahrung/Sozialkontakte |
|---|---|---|---|
| Bisasam | Diurnal | Tag | Tagsüber Pflanzen/Nahrung und Besuche; nachts mehr Ruhe/Schlaf |
| Pikachu | Diurnal | Tag | Erkunden und Kontakt bevorzugt tagsüber; nachts seltener |
| Glumanda / Zunderlauf | Flexible | Ganztägig | Aktivitätsfaktor 0,75–0,85; auch nachts Nahrung/Erkundung |
| Myrapla | Nocturnal | Nacht | Tagsüber erhöhte Ruhe-/Schlafchance, nachts mehr Nahrungssuche |
| Enton | Crepuscular | Morgen/Abend | Aktivitätsfenster aus zentralen Dämmerungsgrenzen, sonst mehr Ruhe |
| Nebulak | Nocturnal | Nacht | Tagsüber vorwiegend ruhig; nachts Schweben/Erkunden/Nahrung; weiterhin schwebende Darstellung |

Rhythmuskurven beziehen Grenzen aus der bestehenden Weltuhrkonfiguration, Tagesdauer unverändert 120 Echtminuten. Individuelle ±45 Ingame-Minuten aus separatem Seed-Stream verändern die etablierte Bewegungs-Zufallsfolge nicht. Sanfte Aktivitätsfaktoren statt harter Schlaffristen. Aktiv/ruhig-Multiplikatoren: Wander 1,35/0,25, Nahrung 1,6/0,35, Sozial 1,4/0,15, Ruhe 0,6/2,2, Schlaf 0,15/8; Empfangsbereitschaft 1/0,2. Bestehende Artgewichte bleiben individuell wirksam. Kein zusätzlicher alter pauschaler Nacht-Schlafmultiplikator auf die bereits gewichteten Profile.

Laufende Aktionen/Wege und angenommene Besuche bleiben bei Phasen-/Zeitsprüngen erhalten und enden regulär; nachfolgende Entscheidungen nutzen neue Gewichte. Vorhandene Mindestzeiten und Abklingzeiten bleiben erhalten. Schlaf ist eigener Zustand, vorläufig bestehende Idle-Animation. Schlafende initiieren/akzeptieren keine gewöhnlichen Besuche, Ruhende akzeptieren zusätzlich nur mit halber Chance. Keine garantierten Besuche bei jeder Beobachtung.

## Weltuhr, Pausen und Speicherung

Vorhandene `OnTimeSet`-/`OnPhaseChanged`-Ereignisse aktualisieren Gewichte sofort, einschließlich Save/Load. Regulär alle drei Sekunden innerhalb des bestehenden Bewegungsticks; beschleunigte Debugzeit mindestens 0,5 s, keine neue dauernde Suche. Pause wird aus der vorhandenen Weltuhr abgefragt: Ambienttimer und Bewegung halten an, während vorhandene Gefahr-/Spielerreaktionen Vorrang behalten. Ungültige Sozialpartner werden auch während Pause gegenseitig freigegeben; gültige Paare bleiben pausiert. Delegates werden bei Neukonfiguration/EndPlay entfernt. Distanzoptimierung bleibt bestehen.

Keine persistenten Aktivitäts-/Zeitfelder hinzugefügt. Maßgebliche Weltzeit bleibt im Speichersystem V2; kurzlebige Tätigkeiten werden nach Laden/Travel neu initialisiert. Team, Identitäten, AP, Erfahrung, Entwicklung und Kontrollpunkte unverändert. Kein Tagesrhythmus beeinflusst Spawnrate, Fangrate oder Kampfwerte.

## Einzelprüfung

- Editor-Build `DayRhythmV22_Build02`: Exit 0. Erster Build scheiterte an durch geänderte Unity-Dateigruppierung sichtbar gewordenen alten Namenskollisionen. Ausschließlich lokale Hilfsnamen `Ids` → `NPCTestSpeciesIds` und Beleuchtungstest-`Sample` → `LightingAt` umbenannt; NPC-Funktion/Assets unverändert.
- Vollständige Automation `DayRhythmV22_Automation01`: **279 bestanden, 0 fehlgeschlagen, 0 übersprungen, 0 Testwarnungen**, Engine und strenger Wrapper Exit 0. Das bezeichnet die Testauswertung; bekannte externe iOS-Helferwarnungen im Editor sind weiterhin vorhanden. Paket A hatte separat Wrapper Exit 1 und wird dadurch nicht rückwirkend warnungsfrei.
- Sechs neue Tests: konfigurierbare Profile/Fehlerfälle; kontrollierte 12.000 Auswahlen je Art für Schlaf/Nahrung/Sozialgewichtung; jeder Tagesminute/Mitternacht/Offset; echte zentrale Uhrereignisse und Delegateabbau; pausierte Aktivität/aufweckende Gefahr; gegenseitige Reservierungen über Zeitsprung/Pause und Bereinigung ungültiger Partner. Bestehende KI-/Sozialtests weiter vollständig bestanden.
- Echter gewöhnlicher VisualV2-PIE-Lauf `RhythmB02`, 94 s: acht vorhandene Wildinstanzen aus sechs Arten in **unveränderten Habitaten**, keine Aktivitäts-/Profil-/Bewegungserzwingung. Beleuchtungszyklus für diese unabhängige B-Prüfung ausgeschaltet; dadurch sind `Noon.png`/`Night.png` QHD-Aufnahmen der unterschiedlichen KI-Zeitpunkte bei derselben ursprünglichen Beleuchtung, keine Tag-Nacht-Bildvergleiche.
- Sofortige Gewichtungsänderung 12 → 22 und Sprünge zu 06/18/04/12/22, vollständiger Ambient-Pausenhalt sowie zuverlässige Fortsetzung bestanden. Jede Stichprobe prüft ursprüngliches Habitat, gegenseitige Exklusivreservierung und kein Gehen/Partner während Schlaf. Kein unerwünschter Kampf.
- Tatsächliche spontane Bisasam-Besuche tagsüber abgeschlossen; nachts überwiegend Ruhe, auch Schlaf beobachtet. Pikachu tagsüber Wanderung, nachts überwiegend Ruhe. Glumanda auch nachts Nahrungssuche. Nebulak tagsüber Idle/Ruhe, nachts Nahrung/Wanderung. Enton nachts auch Schlaf, tagsüber Ruhe. **Myrapla blieb in dieser kurzen Nachtstichprobe überwiegend ruhend**, obwohl Nachtgewichte korrekt erhöht waren; seltene Entscheidungen/Restdauern sind keine garantierten Zeitpläne. Längere gemeinsame Tagesbeobachtung folgt. Vollständige Häufigkeiten im Nachweis, keine repräsentative Populationsstatistik aus 35 Sekunden.
- Zwölf Map Checks: jeweils 0 Fehler/0 Warnungen. Szene identisch, keine Map gespeichert. 85 geschützte Prüfsummen, 31 ursprüngliche unversionierte Dateien und beide Vollbackup-Referenzen unverändert.

## Kurzer CPU-Vergleich

Nativer vorhandener Komponenten-Scope im echten PIE, pro Fall 8 Sekunden; gleiche Ausgangstransformationen und Seeds, KI V2.1 ohne Rhythmus gegenüber V2.2, beide unter gleichem Licht und tatsächlicher laufender 1×-Uhr. Keine Begegnung, keine Input-Sperre. Angaben Summe der gemessenen Komponenten in ms pro Frame:

| Aktive Instanzen | V2.1 | V2.2 |
|---|---:|---:|
| 1 | 0,1210 | 0,1165 |
| 3 | 0,1218 | 0,1311 |
| 8 | 0,2858 | 0,2557 |
| 8 weit entfernt | – | 0,0027 |

Drei Gewichtungsabfragen pro achtsekündigem Nahfall je Instanz statt pro Frame; entfernte Instanzen bleiben reduziert. Keine auffälligen zusätzlichen CPU-Kosten. Einzelstichproben mit anderen zufälligen Aktionen sind **kein Nachweis einer allgemeinen Beschleunigung**. GPU-/Framezeiten bleiben von der bestehenden schweren QHD-Szene dominiert. Kein neues Benchmarksystem.

## Grenzen und nächste Prüfung

Schlaf besitzt vorerst nur Idle-Darstellung. Kein reales Futter-/Hungerökosystem, keine neuen Spawnregeln, keine festen Schlafstunden. Persönlichkeits-/Artenunterschiede können kurze Beobachtungen überlagern. Der zuerst vor der Beobachtung idelnde PIE-Lauf war bereits in einen normalen Wildkampf geraten; `RhythmB01` wurde deshalb abgebrochen und nicht als bestanden gewertet. Erfolgreicher Nachweis ausschließlich frischer `RhythmB02`.

Gemeinsam folgen vollständiger beschleunigter Tagesumlauf, acht Zeitpunkte unter V1.1-Licht, Innenraum/SaveLoad/Mapwechsel/Kampf und weiterer tatsächlicher Fußlauf. Physische Controllerprüfung nicht behauptet, Grundbelegung unverändert. Originalaufnahmen und Testslots bleiben lokal unter `Saved/ProjectRefinement/DayNightV11AI22/`; keine Kontrollmedien oder LFS-Daten eingecheckt.
