# Pokémon-KI V2 – Prüfbericht

Projekt: `/Users/harry/Developer/PokeMonster` · Datum: 26.10.2026 · Ausgangsstand: `a85062139926cfd2fe7c93d3c790765400a56aa7` · Branch: `main`.

**Ergebnis:** Sechs Arten verwenden zusätzliche natürliche Aktivitäten im bestehenden System. Sozialablauf und Rückkehr sind in echtem PIE nachgewiesen; im kurzen Standardprofil-Fenster trat noch kein spontaner Sozialabschluss auf. Finaler Build erfolgreich, 252 native Tests ohne Testfehler, zwölf Map Checks ohne Fehler/Warnungen. Der strenge Automation-Wrapper endet wegen eines Tests mit externen iOS-Helferwarnungen mit Exit 1. Keine Map-/Asset-/Save-Änderungen.

## Umfang und vorhandene Grundlage

Erweitert wird ausschließlich die vorhandene `PokeMonsterCreatureRoamingComponent`. Vorhanden waren bereits kollisionsgeprüftes Wandern mit begrenztem A*, Beschleunigung, weiche Drehungen, Pausen, Vegetationshindernisse, Spieler-Sichtlinien, neugieriges Annähern, scheues Ausweichen, territoriale Warnung/Verfolgung, Kontakt-/Herausforderungsregeln, sichtbare Niederlagenflucht und Begleiter-Rückruf. Diese Systeme werden wiederverwendet. Kein zweiter KI-Controller, Behavior Tree oder konkurrierender Zustandsautomat.

Die erste Freischaltung gilt nur für wilde Bisasam, Pikachu, Zunderlauf/Glumanda, Myrapla, Enton und Nebulak auf VisualV2. Die normale Map besitzt bereits alle sechs Arten und eine dreiköpfige Bisasam-Gruppe. Keine dauerhafte Platzierung und keine `.umap`-Änderung waren erforderlich. Begleiter, Biome-Verträge und andere Maps sind ausgenommen.

## Verhaltensbausteine und Prioritäten

| Aktivität | Tatsächliche Umsetzung |
|---|---|
| Idle | Kurze ruhige Umgebungsbeobachtung mit weicher Blickwendung; neues `Idle`, getrennt von der bisherigen Spielerbeobachtung. |
| Wander | Vorhandenes habitatgebundenes Wandern, erreichbare Ziele, Sektoren-/Zielhistorie, bestehende Geschwindigkeiten und Animationen. |
| Observe / Alert | Bestehende Aufmerksamkeit gegenüber dem Spieler; kann eine Hintergrundaktivität unterbrechen. |
| Rest | Längere ruhige Idle-Phase ohne Laufbewegung. |
| Sleep | Längere Idle-Pause, unterbrechbar, eigene Wiederholungssperre. Keine vorgetäuschte Schlafpose oder Ohnmachtsanimation. |
| Forage | Erreichbare Stelle aufsuchen, dort verweilen und zur nächsten Aktivität wechseln. Pflanzennahe Profile verwenden einmalig erfasste Vegetationsanker; sonst Bodenstellen. Kein Hunger-/Nahrungssystem. |
| Social | Geeigneten sichtbaren Nachbarn wahrnehmen, gegenseitig reservieren, mit Sicherheitsabstand annähern, kurz einander zuwenden/verweilen und wieder lösen. |
| Flee | Vorhandenes scheues Ausweichen bzw. separate prioritäre Niederlagenflucht. |
| Territorial | Vorhandene Warnung und Verfolgung. Normaler Kampf weiterhin ausschließlich bei tatsächlichem Kontakt. |

Kampf, Heilpunkt-Rückkehr, Niederlagenflucht, Präsentationssperren und relevante Spielerreaktionen unterbrechen Ambient-Aktivitäten. Sozialreservierungen werden beidseitig gelöst. Nach der Unterbrechung folgt eine normale Pause/Neuauswahl. Vorhandene Enum-Nummern bleiben stabil; neue Werte sind angehängt.

Aktivitäten werden gewichtet statt hektisch pro Tick ausgewürfelt. Die erste Auswahl wartet auf die gestaffelte Nachbarschaftsabfrage. Wanderstrecken werden nicht durch eine abgelaufene Aktivitätsdauer mitten im Lauf abgebrochen. Nahrungssuche und Sozialannäherung haben ein Reisezeitlimit von 20 Sekunden. Nicht erreichbare Ziele führen sicher zu einer ruhigen Alternative. Kleine Abstandskorrekturen zwischen bereits nahen Nachbarn dürfen über den bestehenden Planner erfolgen.

## Sechs Standardprofile

Gewichte sind relative Chancen bei einer zulässigen Neuauswahl, keine Prozentwerte. Situationen, fehlende geeignete Partner und Abklingzeiten schließen Aktivitäten aus.

| Art / stabile interne ID | Vorhandenes Reaktionstemperament erhalten | Wander / Beobachten / Ruhe / Schlaf / Nahrung / Sozial | Besonderheit |
|---|---|---|---|
| Bisasam | Curious | 3 / 2 / 4 / 0,5 / 5 / 2 | Pflanzennahe Ziele, Artgenossen bevorzugt. |
| Pikachu | Curious | 7 / 2 / 1 / 0,2 / 3 / 2 | Kürzere Aktivitäten 4–9 s, Pflanzenrand, Abstandhalten bei zu großer Nähe bleibt erhalten. |
| Glumanda / Zunderlauf | Territorial | 5 / 4 / 2 / 0,5 / 4 / 2 | Bodenbeobachtung/-suche; vorhandene territoriale Begegnungsregel bleibt bestehen. |
| Myrapla | Calm | 2 / 2 / 5 / 1 / 5 / 2 | Pflanzennahe Ziele, längere Ruhe (Basis 20 s). |
| Enton | Shy | 4 / 4 / 3 / 0,5 / 3 / 4 | Ruhige Aktivitäten und geeignete artübergreifende Kontakte; vorhandenes Ausweichen bleibt erhalten. |
| Nebulak | Shy | 5 / 5 / 2 / 0,2 / 1 / 0,5 | Zurückhaltende Kontakte; vorhandenes visuelles Schweben bleibt erhalten. Keine erzwungene Gehpose. |

Übrige Basiswerte: Aktivität 5–12 s, Ruhe 15 s, Schlaf 22 s mit leichter Dauerstreuung; Wiederholungssperren Social 35 s, Schlaf 90 s, Nahrungssuche 20 s. Persönlichkeiten und Begegnungen können dieselbe `ActivityOverride`-Struktur verwenden, ohne neue KI-Klassen anzulegen.

Es gibt noch keine allgemeine Weltuhr. `ActivityPeriod` bietet Day/Evening/Night als spätere Anbindung; Evening verdoppelt und Night vervierfacht nur das relative Schlafgewicht. Standard ist Day. Keine neue Tagesbeleuchtung, reale Uhrzeitsteuerung oder feste tägliche Ortsroute wird behauptet.

## Wahrnehmung, Sozialregeln und Entfernung

- Lokale Kollisions-Broadphase statt permanenter vollständiger Pokémon-Paarvergleiche. Sozialradius standardmäßig 500 cm, zeitlich gestaffelt; höchstens zwölf Kandidaten werden näher geprüft.
- Art, aktueller Zustand, Reservierung, Entfernung, Höhenunterschied, grobe Blickrichtung und Sichtlinie werden geprüft. Artübergreifende Kontakte benötigen passende Profile auf beiden Seiten.
- Ein Pokémon kann nur einen Sozialpartner reservieren. Bereits vorhandene lokale Paare begrenzen weitere Besuche. Ein Partner wartet, der andere verwendet einen einmalig geplanten begrenzten Annäherungsweg; kein endloses Nachplanen hinter einem bewegten Partner.
- Abstand basiert auf beiden Navigationsradien plus 75 cm; bei scheuem Initiator zusätzliche 100 cm. Bei Hindernissen bleibt die vorhandene Kollisions-/Bodenprüfung maßgeblich.
- Normale Spieler-Sichtlinien werden außerhalb unmittelbarer Nähe 0,25–0,45 s zwischengespeichert. Tatsächliche Kontakterkennung und geteilte Interaktionsaktion bleiben unverändert.
- Ab 4000 cm Spielerentfernung ruhen niedrig priorisierte Aktivitäten und ihre Planung. Niederlagenflucht ist ausdrücklich ausgenommen. Nahe Bewegung bleibt pro Bild kontinuierlich. `OnlyTickPoseWhenRendered` bleibt erhalten.

## Tatsächliche PIE-Nachweise

Alle Bilder und Framefolgen stammen aus dem realen Unreal-Projekt. Keine generierten Konzeptbilder, keine Kameravergrößerung und keine Modellgrößenänderung. QHD-Standbilder: 2560 × 1440. Diagnosepositionierungen des Spielers sind in den Rohdaten ausgewiesen.

- `Saved/ProjectRefinement/PokemonAIV2/ConnectedPIE04/Result.json`: normaler zusammenhängender PIE-Lauf, rund 141 Spielsekunden; 75 s unbeeinflusste Aktivitäten, Beobachtungen mehrerer Arten, scheue Reaktionen, echte Eingabe-Fußlaufstrecke über 100 cm, isoliertes natives Disk-Save/Load, erhaltene Team-Identitäten/Level/KP, wieder freie Steuerung und weiterlaufende KI. Original-Save unverändert. Aufgezeichnet wurden unter anderem Rest, Idle, Wander, Sleep, Forage und Retreat. Nahrungssuchen wurden mehrfach abgeschlossen.
- `VisualPIE02`: sechs echte Artaufnahmen und 25 s native Myrapla-Beobachtung. Bestehende Bisasam-Gruppe beendet einen Sozialbesuch unter temporär sozialbetonten/ruhigen Profilen. Keine zusätzlichen Tiere oder gespeicherten Positionen. Dieser Abschnitt ist ausdrücklich ein technischer Profiltest.
- `GameplayPraxisV1/wild/PokemonAIV2TerritorialVictory`: tatsächliche Annäherung, Warnung, genau ein Kontaktkampf, ClassicBattle, Sieg, sichtbare Erholung und Flucht, Entfernung erst außerhalb des Sichtfelds. Drei erfolgreiche Fluchtpläne, null blockierte Schritte im Abschlussdatensatz, Begleiter wieder sichtbar; rund 70 s Wandzeit.
- `GameplayPraxisV1/wild/PokemonAIV2CuriousFlee`: Berührung startet bei neugierigem Bisasam keinen Kampf, gerichtete gemeinsame Interaktion startet ihn, erfolgreiche Spielerflucht, Wildtier bleibt aktiv, Wiederholungssperre und Begleiter-Rückkehr; rund 11 s Wandzeit.

Die vollständige Kampf-, Fang-, Fortschritts-, Controller-, WorldBattle- und Speicherregression ist zusätzlich Bestandteil der nativen PokeMonster-Automation. Ein erneuter physischer Switch-Pro-Test wurde nicht durchgeführt und wird nicht behauptet.

### Ehrliche Grenzen der Bildbelege

Baumkronen/hohe Vegetation verdecken auf mehreren unverändert gerenderten Habitatansichten kleine Pokémon deutlich. Vor allem Myrapla und Teile der Bisasam-Gruppe sind dadurch schlecht beurteilbar. Die Landschaft, Modelle, Kamera und der Sichtkreis wurden deswegen nicht verändert. Die normalen Aufnahmen sind kein Beleg für eine neue Schlafpose oder eine spezielle Fressanimation: diese Version verwendet ruhiges Idle mit Blickwendung.

Frühere fehlgeschlagene Prüfaufbauten bleiben lokal erhalten und zählen nicht als bestandene Ergebnisse: `ConnectedPIE01` startete mit bereits laufender Begegnung; `VisualPIE01` hatte keinen gefundenen Beobachterpunkt für Enton; `Performance01` wollte einen schreibgeschützten Diagnostikwert setzen; `ConnectedPIE03` verwendete einen ungünstigen Diagnosepunkt nahe einem inzwischen herangelaufenen territorialen Tier; die finale Kamerasuche prüft deshalb Mindestabstände. `VisualPIE03` und die ersten `SocialClearing`-Versuche erreichten innerhalb des Testlimits keinen Sozialabschluss. Die native Diagnose deckte die anfängliche Aktivitätsauswahl vor der ersten Wahrnehmung auf; dafür wurde ein zusätzlicher echter Welt-/Bewegungstest ergänzt. Kein fehlgeschlagener Aufbau wurde durch künstliche Bilder ersetzt.

## Kurzer Performancevergleich

`Performance03/Result.json`: je acht Spielsekunden, dieselben initialen Instanzpositionen, bestehende Arten; native vollständige Komponentenzeit im echten PIE, Messflagge im Normalspiel aus.

| Aktive Instanzen | Erweiterung aus: Komponenten-ms/Bild | Erweiterung an: Komponenten-ms/Bild |
|---|---:|---:|
| 1 | 0,095 | 0,090 |
| 3 | 0,212 | 0,139 |
| 8 | 0,465 | 0,217 |
| 8, entfernt | — | 0,0014 |

Bei acht entfernten Instanzen: keine neuen Pläne, Wahrnehmungen oder Aktivitätsentscheidungen. Bei acht nahen Instanzen: Sichtlinienzählung 156 ohne Erweiterung gegenüber 32 mit Erweiterung im kurzen Vergleich. Unterschiedliche Aktivitätsverläufe machen daraus keinen allgemeinen Beschleunigungsfaktor. Gesamtbildzeiten schwankten etwa zwischen 55 und 66 ms in beiden Modi; die bestehende schwere Editor-Szene bleibt eine Einschränkung. Kein isolierter GPU-Kostennachweis, keine große Benchmarkreihe. Diese finale Stichprobe enthält die korrigierte erste Auswahl.

## Technische Prüfungen und Schutz

Die finalen Ergebnisse, sichtbaren Sozialnachweise sowie Commit-/Remote-Status werden nach der letzten Validierung unten ergänzt. Geprüfte Zwischenstände: `PokemonAIV2Build04` erfolgreich; `PokemonAIV2Automation03` 251 erfolgreiche Tests, keine Testwarnungen/Fehler, strenger Wrapper Exit 0. Nach Diagnoseerweiterung: `Build05` erfolgreich, `Automation04` 250 erfolgreich + ein Test mit externer iOS-Warnung, null Fehler; strenger Wrapper Exit 1. Das ist ausdrücklich kein vollständig bestandener strenger QA-Lauf.

Zwölf vorhandene Map Checks waren mit 0 Fehlern und 0 Warnungen erfolgreich. Exakter Editor-Szenenvergleich identisch, keine schmutzigen Map-/Contentpakete. `Baseline.json` schützt 73 vorhandene Dateien (einschließlich aller zwölf Maps, vorhandener Saves und 31 fremder unversionierter Dateien) sowie beide unveränderten Vollbackup-Verweise auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Keine Originalmodelle, Animationen, Spezies-/Attackenidentitäten oder Save-Schemata geändert. Keine zusätzlichen Backups, Maps, Projektkopien oder Worktrees.

Bekannte externe Warnungen: Apple/iOS-`idevice_id`, `posix_spawn` 86 / Bad CPU type, außerdem vorhandene Engine-/Plugin-Startwarnungen. Ein einzelner CharacterMovement-Zeitschritt-Hinweis beim PIE-Start des Messaufbaus wird getrennt von der nativen KI-Zeit ausgewiesen; kein Absturz. Keine Warnungsfreiheit des gesamten Engine-Logs behauptet.

## Weiterführung

Für weitere Arten können dieselben Profile verwendet werden. Vor einer breiten Übertragung: mapbezogene Freischaltung bewusst erweitern, geeignete eigene Ruhe-/Schlaf-/Nahrungssuchanimationen hinzufügen, Weltuhr anbinden und natürliche Sozialhäufigkeit über längere Beobachtungen abstimmen. Gemeinsames längeres Wandern, Gruppenhierarchien, Hunger, Zucht oder Ökosystemsimulation sind nicht implementiert. Die bestehende Begegnungsregel bleibt verbindlich.


## Finaler Prüfstand und lokale Medien

- Editor-Build `PokemonAIV2Build06`: Exit 0.
- Vollständige Automation `PokemonAIV2Automation05`: **252 Tests**, davon **251 ohne Testwarnung, einer mit zwei externen iOS-Helferwarnungen**, **0 fehlgeschlagen**, **0 ausgelassen**. Native Engine Exit 0. Der strenge Wrapper endet weiterhin mit **Exit 1** und gilt ausdrücklich als **nicht vollständig bestanden**. Betroffener Test: `PokeMonster.Creature.ExpansionV3.ImportedAssetsAndStableIdentities`; beide Warnungen betreffen ausschließlich `idevice_id`/Bad CPU type. Alle sieben neuen `NaturalActivities`-Tests bestehen. Frühere Ergebnisse ersetzen diesen finalen Warnstatus nicht.
- Finaler zusammenhängender `ConnectedPIE04`-Lauf: bestanden. Mehrfache abgeschlossene Nahrungssuchen bei Glumanda, Bisasam und Enton, eine bei Myrapla; Schlaf bei Bisasam und Myrapla, scheue Reaktion bei Enton/Nebulak und Beobachten/Annähern bei Bisasam. Keine unzulässige Begegnung oder festhängende Aktivität. Im ca. zweiminütigen Standardprofil-Beobachtungsfenster **kein spontaner Sozialabschluss**; natürliche Häufigkeit bleibt über längere Zeit abzustimmen.
- `SocialClearing06`: nach der Korrektur bestanden. Zwei **vorhandene** Gruppen-Bisasam werden ausschließlich für diesen PIE-Sichtaufbau kurz auf eine bereits vorhandene freie Wiese versetzt und sozialbetont konfiguriert. Vollständige Annäherung, gegenseitiges Beobachten, Abschluss und wieder beginnendes Wandern. Kleinster gemessener Abstand **151,44 cm**, keine Teleportation während der Interaktion. Keine gespeicherte neue Platzierung und kein zusätzliches Pokémon. Frühere fehlgeschlagene Aufbauten 01–05 bleiben dokumentiert.
- Abschließende zwölf Map Checks im finalen `Editor04.log`: jeweils 0 Fehler, 0 Warnungen. `FinalMapChecks.json` enthält die einzelnen Logbelege. Exakte Editor-Szene nach allen Tests identisch, keine ungespeicherten Pakete. Editor regulär geschlossen.
- `Protection.json`: alle 73 vorher vorhandenen geschützten Dateien identisch, 31 fremde unversionierte Dateien erhalten, Vollbackup unverändert erreichbar, kein kanonischer Recovery-Save angelegt.

Lokale echte QHD-Nachweise (bewusst nicht auf GitHub hochgeladen):

- [Sozialannäherung](../Saved/ProjectRefinement/PokemonAIV2/SocialClearing06/SocialApproach.png)
- [Sozialkontakt aus normaler Spielkamera](../Saved/ProjectRefinement/PokemonAIV2/SocialClearing06/SocialObserve.png)
- [Abschluss des Sozialbesuchs](../Saved/ProjectRefinement/PokemonAIV2/SocialClearing06/SocialCompleted.png)
- [Vollständiger Sozial-Gameplayclip](../Saved/ProjectRefinement/PokemonAIV2/Videos/PokemonAIV2SocialClearing06.mp4): **2560 × 1440**, 368 echte Frames, 26,71 s aufgezeichnete Spielzeit, durchschnittlich **13,74 reale Samples/s**. Originalzeitstempel, keine erfundenen oder interpolierten Zwischenbilder. Ausreichend für den Aktivitätsablauf; kein hochfrequenter Animations-Fußkontakt-Test.
- Sechs native Artansichten liegen unter `VisualPIE02/01_…` bis `06_…`; die beschriebenen Kronenverdeckungen bleiben dort sichtbar.

Alle Rohdaten unter `Saved/ProjectRefinement/PokemonAIV2/`, Framequellen im vorhandenen Recorderverzeichnis `Saved/VisualV2TAAIntegrationV1/Recordings/`. Medien und Test-Saves bleiben lokal und ignoriert.

## Git-Sicherung

Es werden ausschließlich die geprüften C++-Quellen, Tests, benötigten Prüfwerkzeuge und diese Dokumentation gesichert. Ein einzelner bestehender Save-Test-Konsolenhelfer erhielt wegen eines beim Unity-Build sichtbar gewordenen Namenskonflikts einen eindeutigen C++-Variablennamen; sein Konsolenbefehl und seine Funktion bleiben unverändert. Keine Asset-, Map-, Animations-, Save- oder LFS-Datei wird verändert oder hochgeladen. Der vollständige V5-Evidenzsnapshot `CoreFiles.json` wird als historischer Snapshot unverändert belassen.
