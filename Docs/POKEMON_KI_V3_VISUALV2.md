# Pokémon-KI V3 und VisualV2 – Prüfbericht

Stand: 29.10.2026 (Arbeitsbeginn 28.10.2026). Ausgangscommit `fa582035`. Ausschließlich das bestehende Projekt und die bestehende VisualV2 wurden bearbeitet.

## Tatsächlicher Bestand und Umfang

Der geprüfte Ausgangsstand besitzt **zehn Lebensraumzonen, 14 kuratierte Wildarten und 18 registrierte Testmodelle**. Die im Auftrag genannten acht Zonen/zwölf Arten waren älter. Keine Art und keine vorhandene Zone wurde deshalb entfernt oder neu erfunden. Das Limit bleibt **zehn Wild-Pokémon und sechs gleichzeitig vertretene Arten**.

Das vorhandene Entwicklungsteam bleibt Glumanda 15, Garados 30, Pikachu 11; Plätze 4–6 bleiben bei einer neuen leeren Entwicklungsparty frei. Geladene Partys werden durch die KI nicht ersetzt. `Zunderlauf` bleibt ausschließlich die bestehende interne Glumanda-Kennung.

## Gemeinsame KI und Wahrnehmung

Erweitert wurden `PokeMonsterCreatureRoamingComponent`, die vorhandenen Activities/Behavior-Strukturen und die bestehenden Habitatregeln. Navigation, Kollisionsprüfungen, Begegnungsquellen, soziale Reservierungen und Weltuhr werden weiterverwendet. Es gibt keinen zusätzlichen KI-Controller und keine zweite Zustandsmaschine.

Die optionalen Wahrnehmungswerte sind in `Config/DefaultPokeMonsterHabitats.ini` an den vorhandenen Regeln hinterlegt. Die bisherigen Temperamente, Bewegungsparameter, Encounterprofile, Spawngewichte, Artmaxima und Aktivitätsrhythmen bleiben maßgeblich. Der Manager kopiert das vorhandene Artprofil und ergänzt ausschließlich die freigegebenen Wahrnehmungswerte. Nicht konfigurierte ältere Instanzen behalten ihre bisherigen Sinne.

* Sichtfeld und Sichtlinie berücksichtigen Blickrichtung und echte Hindernisse. Innerhalb des persönlichen Nahbereichs gilt Rundumwahrnehmung; eine blockierte Sichtlinie wird dadurch nicht übergangen.
* Wahrnehmungsabfragen erfolgen verteilt, nicht für jedes nahe Pokémon in jedem Frame. Reaktionsverzögerung und 1,4 Sekunden Sichtverlustgedächtnis vermeiden hektisches Ein-/Ausschalten.
* Nach bestätigtem Sichtverlust wird höchstens der zuletzt angenommene Sichtpunkt verfolgt. Sichtstatus wird zwischen den Sensorprüfungen gecacht; neue Hindernisse werden daher spätestens bei der nächsten Sichtprüfung berücksichtigt.
* Neugier beginnt mit kurzem Beobachten. Die Untersuchung endet spätestens nach sieben Sekunden; danach folgen 8–13 Sekunden ohne erneutes Hinterherlaufen. Unmittelbarer Nahraum bleibt ein Rückzugsgrund.
* Scheue Arten werden im äußeren Wahrnehmungsbereich aufmerksam und fliehen bei weiterer Annäherung. Territorialverhalten warnt zunächst und verfolgt höchstens sechs Sekunden. Der Warn-/Sichtzustand allein startet keinen Kampf.
* Die vorhandenen Kontakt- bzw. ausdrücklichen Herausforderungsregeln bleiben erhalten. Wasser-Pokémon werden weiterhin vom Ufer herausgefordert.
* Menüs und die bestehende Weltuhrpause halten die neuen zeitabhängigen Abläufe an. Die 120-Minuten-Tageslänge wurde nicht verändert.

### Artprofile

Projektseitige KI-Konfiguration, keine neu behaupteten kanonischen Pokémon-Regeln. Reichweiten sind Zentimeter; die zweite Reichweite beim Verlassen beträgt mindestens Erfassungsradius + 200 cm. Abfrage/Reaktion in Sekunden.

| Art | Bisheriges Temperament | Reichweite / Sichtfeld | Abfrage / Reaktion | Tagesrhythmus | Bevorzugte Anker / Gruppenneigung |
|---|---|---|---|---|---|
| Bisasam | Curious | 650 / 200° | 0.5 / 0.5 | tagaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Pikachu | Curious | 650 / 200° | 0.5 / 0.5 | tagaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Glumanda | Territorial | 700 / 220° | 0.45 / 0.35 | flexibel | Felsen |
| Myrapla | Calm | 500 / 180° | 0.7 / 0.7 | nachtaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Enton | Shy | 850 / 240° | 0.35 / 0.2 | dämmerungsaktiv | Ufer |
| Nebulak | Shy | 850 / 240° | 0.35 / 0.2 | nachtaktiv | ruhige Erkundung |
| Schiggy | Shy | 850 / 240° | 0.35 / 0.2 | flexibel | Ufer |
| Raupy | Calm | 500 / 180° | 0.7 / 0.7 | tagaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Hornliu | Shy | 850 / 240° | 0.35 / 0.2 | tagaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Smettbo | Curious | 650 / 200° | 0.5 / 0.5 | tagaktiv | Pflanzen/Bäume, Artgenossen-Gruppe |
| Bibor | Territorial | 700 / 220° | 0.45 / 0.35 | tagaktiv | Artgenossen-Gruppe |
| Habitak | Territorial | 700 / 220° | 0.45 / 0.35 | tagaktiv | Felsen, Artgenossen-Gruppe |
| Karpador | Calm | 500 / 180° | 0.7 / 0.7 | flexibel | ruhige Erkundung |
| Garados | Territorial | 850 / 220° | 0.45 / 0.35 | flexibel | ruhige Erkundung |

### Zustände, Gruppen und Umwelt

Die bestehenden Zustände Rest, Wander, Observe, Approach, Retreat/Flee, Warning/Warn, Cooldown, Follow, Idle, Sleep, Forage und Social bleiben erhalten. Alert, Curious, Chase, Group und Battle wurden am Ende der bestehenden Aufzählung ergänzt; alte Zustandsnummern bleiben gleich. Geschwindigkeit und vorhandene Idle-/Geh-/Laufanimationen stellen diese Zustände dar. Schlaf bleibt eine technisch getrennte Ruheaktivität mit vorhandener Idle-Darstellung.

Gruppen sind kleine, gegenseitig reservierte Artgenossen-Paare. Sie verwenden die bisherige Einladung, Annahme/Ablehnung, Annäherung, Ausrichtung, Abstandskontrolle und begrenzte Verweildauer. Gefahr informiert den reservierten Artgenossen einmal und löst anschließend beide Reservierungen. Kampf, Verfügbarkeit, Distanz, Hindernisse und Zeitgrenzen behalten Vorrang. Es gibt keine Schwarm- oder globale Gruppensuche. Die vorhandene lokale Broadphase prüft höchstens zwölf Kandidaten und begrenzt benachbarte Paare.

Umweltpunkte werden beim Einrichten aus tatsächlichen Pflanzen-/Baum-/Felsmeshes einschließlich Instanzen bzw. den vorhandenen Wassergrenzen gewonnen; der Cache bleibt auf 64 Punkte begrenzt. Der vorhandene Planer prüft Zugänge und Körperfläche. Ungeeignete Punkte werden verworfen. Es werden weder Nahrung noch neue Ressourcen oder Spezialanimationen vorgetäuscht.

Gruppen entstehen opportunistisch bei geeigneten nahen Partnern; garantierte Gruppenspawns wurden nicht eingeführt. Eine spontane Gruppeninteraktion wurde im Dichtetest mit unveränderter Bisasam-KI beobachtet. Die Naturbeobachtung im regulären Fußlauf belegte Nahrungssuche und Spielerreaktionen; dort wird keine nicht beobachtete Gruppenhäufigkeit behauptet.

## Teich und Bach

Der bisherige 18 × 13 m große Teich bei `(720, -1000)` überlappte den Bach-/Auslaufbereich. Sein Zentrum liegt jetzt bei **`(720, -1800)`**. Die nördliche Teichkante liegt bei Y = −1150, das geometrische Auslaufende bei etwa Y = −744. Dadurch bleiben **406 cm trockener Boden** zwischen den Wasserflächen. Die Materialränder sind weich; die Angabe bezeichnet die geometrischen Grenzen.

Wasserhöhe 4,2 cm und maximale Beckentiefe 424,2 cm bleiben erhalten. Der neue Boden füllt das alte Becken und bildet das gleich große versetzte Becken mit sanften Ufern. Vier Bodentraces auf dem Trennstreifen treffen durchgehend Z = 0. Ein echter Lauf über den Streifen prüft zusätzlich Spieler und Begleiter.

Die bestehende elliptische Spielersperre wurde mitversetzt; sie wurde nicht durch eine rechteckige Sperre ersetzt. Die Zonen `PondWater` und `PondShore` folgen der Verschiebung, alle anderen Zonen bleiben an ihren bisherigen Positionen. Die zwölf vorhandenen Wasserziele und die gemeinsame körperabhängige Planung bleiben bestehen. Karpador/Garados behalten ihre individuelle Eintauchtiefe von 43/180 cm und die vorhandene Schwimmdarstellung.

449 vorhandene Vegetationsinstanzen und ein Busch wurden aus dem neuen Becken auf das Ufer versetzt, der zugehörige bestehende Kollisionshelfer wurde ausgerichtet. Anzahl, Modelle und Materialien dieser Pflanzen bleiben erhalten. Wege, Brücke und Bachverlauf wurden nicht umgebaut.

Neue abgeleitete Dateien liegen ausschließlich unter `Art/World/PokemonAIV3` und `Content/Environment/PokemonAIV3`; die bisherigen Blender-/FBX-/Materialquellen bleiben erhalten. Zwei mapbezogene Materialkopien ändern nur die Teichposition/Maskierung. `Tools/PokemonAIV3/BuildPond.py` und `SeparatePond.py` dokumentieren die einmalige, bewachte Herstellung. Keine neue Map.

## Wildnamen und Modelltestgelände

Die vorhandene TextRender-Technik ist gemeinsam in `PokeMonsterCreaturePresentation` gekapselt. Wilde Pokémon verwenden ihre tatsächlichen Speziesnamen und die Oberkante der aktuellen Modellgrenzen, nicht eine pauschale Pokédex-Länge. Damit liegt insbesondere Garados' Name nicht 6,5 m über dem Boden. Schrift und dezente Farbe entsprechen dem Modelltestgelände; Wildnamen verwenden 24, Testnamen weiterhin 26 cm Schriftgröße.

Die Position folgt dem Modell, die Beschriftung richtet sich zur Kamera. Sichtbarkeitsprüfungen laufen etwa fünf- bis sechsmal pro Sekunde, Text wird nur bei Änderungen neu aufgebaut. Standardreichweite: 26 m plus 2,5 m Austrittshysterese. Kamerabild, echte Sichtlinie, Entfernung, Lebenszustand und Kampf werden berücksichtigt. Logische Wasserbarrieren verdecken die Namen nicht; echte Weltgeometrie weiterhin schon. Überlappende Namen werden nach stabiler Encounter-ID zurückgenommen; der vorhandene Herausforderungsmarker hat Vorrang.

Die neue Wildnamen-Logik ist auf VisualV2 begrenzt. Andere Maps behalten ihre bisherige Fokusdarstellung. Die 18 unabhängigen Testmodelle, ihre Registrierung, Begegnungssperre und Bedienbefehle bleiben erhalten. `pm.WildNames 0` schaltet weder deren Testbeschriftung noch den bestehenden Fokusmarker ab.

```text
pm.WildNames 1                 // Standard: Wildnamen ein
pm.WildNames 0                 // Wildnamen aus, Fokusmarker bleibt
pm.WildNames.Distance 2600     // Standardreichweite in cm
pm.TestGround.List
pm.TestGround.Go Glumanda
pm.TestGround.Mode walk        // auch idle, run, turn, directions, auto
pm.TestGround.Reset
pm.TestGround.Return
```

Es wurde keine zweite Optionsoberfläche eingeführt. Die Namensoption ist ein zentraler Laufzeit-Konsolenwert; nach einem neuen Prozess gilt wieder der Standard Ein. Speicherdaten werden dafür nicht verändert.

## Funktionale und technische Prüfungen

Letzter Editor-Build: `PokemonAIV3Build07`, Exit 0. Letzte vollständige funktionale Automation (NullRHI): `PokemonAIV3Automation05`, **289 bestanden, 0 mit Testwarnung, 0 fehlgeschlagen, 0 ausgelassen; Unreal-Exit 0, strenger QA-Wrapper Exit 0**. Auch Automation04 bestand vollständig. Vier neue Tests prüfen Sichtfeld/Kompatibilität, Reaktionszeit/Sichtverlust/Pause, begrenzte Verfolgung/Kampf-Lebenszyklus und Gruppen/Unterbrechung. Bestehende Tests prüfen zusätzlich die 14 Regelbindungen und Beschriftungsanker aller 18 Modelle.

Alle **zwölf bestehenden Maps** wurden im eigenen sauberen Editor geprüft: jeweils **0 Fehler, 0 Map-Check-Warnungen**. Nur VisualV2 wurde gespeichert. Das bedeutet nicht, dass sämtliche Engine-Logs warnungsfrei wären.

| Echter Lauf | Ergebnis | Nachweis |
|---|---|---|
| NativeFunctional01 | **bestanden** | 76 Schritte / 22 Prüfungen: Team, Modelle, Dialog, Innenraum, Uhr, Kampf, Fang, Save/Load, Teamsortierung/Begleiter |
| WorldFootwalk01 | **bestanden** | 32 Wegpunkte, 368,1 m, keine Routenteleports, anschließend 90 s Naturbeobachtung |
| PondStripWalk01 | **bestanden** | 24,5 m hin/zurück über den Bodenstreifen, konstante sichere Fußhöhe |
| WaterGameplay01 | **bestanden** | Karpador vom Ufer bekämpft/gefangen; Team/HP/AP/Repertoire gespeichert und geladen; Garados mehr als vier Ziele |
| Travel01 | **bestanden** | VisualV2 → vorhandene Dev_TestMap → VisualV2; Team, Uhr und Grafikprofil erhalten |
| NamesAudit03 | **bestanden** | Dorf, Wiese, Wald, Karpador, Garados; Modellanker, Ausschalten und Entfernung |
| PIEFunctional03 | **bestanden** | 76 Schritte / 22 Prüfungen im echten PIE |
| WaterInteractionPIE01 | **bestanden** | gewöhnliche Spieler-Herausforderung für Karpador und Garados im PIE |

Controller-/Start-Stopp-Prüfung: **bestanden**; zusätzliche Movement- und Tagesphasen-PIE-Zyklen, einschließlich regulärem Beenden des eigenen Editors. Die Eingaben sind Softwareprüfungen der vorhandenen Switch-Pro-Belegung; kein neuer physischer Controller-Test.

Der echte Fußlauf dauerte 247.6 s. Er erfasste Idle/Rest/Wander, Forage, Alert, Observe, Retreat, Approach, Warning, Chase, Curious und Sleep. Höchster protokollierter Nahrungssuche-Zähler eines Individuums: **3**. Die 10-Individuen-/6-Arten-Grenzen wurden in sämtlichen Stichproben eingehalten.

Der Wasserlauf dauerte 242.9 s; Karpador wurde nach **2 Attacken und 1 Ballwurf** regulär gefangen. Die kurze gezielte PIE-Uferprüfung verwendet ausdrücklich technische, nicht gespeicherte Uferpositionen; der natürliche Wasserlauf wartet dagegen auf die tatsächliche Schwimmroute.

## Performance und Grenzen der Vergleiche

Verifiziert: Mac16,12 / Apple M4 / 16 GiB, macOS 27.0.1, Unreal 5.8.2/Metal. Separate Development-Spielprozesse (`UnrealEditor -game`), keine aktive Videoaufnahme. QHD 2560 × 1440, High, 75 %, tatsächliche interne Pixel 1920 × 1080, TAAU, Software-Lumen + IFG, VSM mit vier Strahlen. Kein Grafikprofil wurde verändert.

Jedes ausgewertete Frame wurde auf Auflösung, tatsächliches AA/Upscaling, Kameraperspektive und aktives Fenster kontrolliert. Drei 15-s-Messfenster je Zustand, acht Sekunden Warm-up, wechselnde Reihenfolge. Weltuhr, Sonne, KI, NPCs und regulärer Begleiter laufen. Die Routen sind vor und nach der Änderung dieselben; Sprint ist ausgeschaltet. Die erste Referenzserie mit einem übernommenen Sprint-Latch wurde vor der Auswertung als ungeeignet ausgeschlossen und durch die korrigierten `Before*02`-Serien ersetzt.

### Bewegte reguläre Welt

FPS sind Mittel der drei Fenster, p95 ist das Mittel ihrer jeweiligen p95-Werte. CPU-AI ist die gemessene gesamte Wander-/Aktivitätskomponentenzeit pro realer Sekunde, nicht die GPU-Zeit und nicht der vollständige Game Thread. Die Ein-/Ausschaltvergleiche enthalten auch Modell-/Animations-/Schattenkosten.

| Stand / Ort | Wildpopulation | FPS | GPU ms | Game ms | Render ms | Frame-p95 ms | AI ms/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| Before / Village | [0, 0] | 35.05 | 27.89 | 2.22 | 28.72 | 31.16 | 0.00 |
| Before / Village | [5, 9] | 34.68 | 28.04 | 2.42 | 28.85 | 32.35 | 4.23 |
| Before / Forest | [0, 0] | 29.12 | 33.49 | 2.53 | 34.26 | 40.63 | 0.00 |
| Before / Forest | [4, 10] | 29.40 | 33.12 | 2.52 | 34.02 | 40.50 | 5.98 |
| After / Village | [0, 0] | 31.40 | 30.61 | 2.89 | 31.84 | 35.43 | 0.00 |
| After / Village | [5, 9] | 31.37 | 30.54 | 3.53 | 31.73 | 35.67 | 7.94 |
| After / Forest | [0, 0] | 26.05 | 37.29 | 3.50 | 38.38 | 43.30 | 0.00 |
| After / Forest | [4, 10] | 26.15 | 36.96 | 3.79 | 38.27 | 43.18 | 10.48 |

Im späteren Durchlauf liegen Dorf/Wald mit natürlicher Population bei **31,37/26,15 FPS**. Auch die Leerläufe ohne Wild-Pokémon sind gegenüber vorher langsamer. Daher ist die gesamte Vorher-/Nachher-Differenz **kein isolierter KI-Kostennachweis**. Netzbetrieb und volle Batterie waren gleich; die frühere Dorfserie enthielt auch thermischen Zustand 0, die Nachserien ausschließlich Zustand 1 („Fair“). Eine konkrete Ursache der gesamten Drift wurde damit nicht bewiesen.

Innerhalb der Nachserien beträgt die mittlere Game-Thread-Differenz mit gegenüber ohne Wildpopulation etwa 0,64 ms im Dorf und 0,29 ms im Wald. GPU-Differenzen haben wechselndes Vorzeichen und werden nicht als Einsparung der KI ausgegeben. **Stabile 30 FPS sind weder im Wald noch allgemein nachgewiesen.** Die p95-Werte und einzelne Spitzen bleiben offen.

### Technischer 0/5/10-Dichteaufbau und Namen

Gleichartige Bisasam werden ausschließlich im isolierten Testprozess über die vorhandene Habitatverwaltung eingerichtet. Es sind echte verwaltete Wild-Actors mit regulärer KI, Kollision und Beschriftung. Die hierfür vorübergehend erhöhte artinterne Anzahl und Zonenbelegung werden nicht in die Projektkonfiguration übernommen. Alle zehn Modelle waren in den Zehnerfenstern sichtbar; das ist kein repräsentativer Test von zehn unterschiedlichen großen Pokémon.

| Anzahl | Namen | FPS | GPU ms | Game ms | Render ms | Frame-p95 ms | AI ms/s |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | Aus | 43.13 | 22.17 | 2.32 | 23.35 | 25.24 | 0.00 |
| 5 | Aus | 41.35 | 23.10 | 2.65 | 24.30 | 26.06 | 8.21 |
| 5 | Ein | 40.14 | 23.82 | 2.84 | 25.08 | 27.01 | 9.25 |
| 10 | Aus | 36.76 | 25.69 | 3.37 | 27.23 | 29.59 | 13.08 |
| 10 | Ein | 38.13 | 24.67 | 3.38 | 26.25 | 28.33 | 12.00 |

Die Namens-GPU-Differenzen sind nicht konsistent genug für einen belastbaren isolierten Einzelkostenwert. Zehn Namen waren bei aktivierter Option sichtbar; bei ausgeschalteten Namen kann weiterhin ein Fokusmarker erscheinen. Die vollständigen Verteilungen, 1-%-Low-Werte und Spitzen liegen in `PerformanceDensity.json` und `PerformanceRoutes.json`. Es werden keine Rendering-Passzeiten ungeprüft addiert.

**Prüfskript-Einschränkung:** `Density04` erfasste alle 15 Messfenster und bestand deren laufende Auflösungs-/Anzahlprüfungen. Sein Abschluss ist trotzdem als fehlgeschlagen gespeichert: Die Python-Konstruktion eines nicht exportierten Structs verhinderte die In-Memory-Rücksetzung. Der Prozess wurde regulär beendet; keine Konfigurationsdatei wurde gespeichert. Der gezielte korrigierte Lauf `DensityRestore01` bestätigt vollständige Regel-/Zonen-/Cvar-Rücksetzung. Die danach frisch gestarteten Dorf-/Waldprozesse verifizieren erneut Maximum 10/6, 14 ursprüngliche Regeln ohne Dichte-Testmarkierung und das unveränderte Grafikprofil. Die Messfenster werden getrennt vom gescheiterten Skriptabschluss bewertet; dieser wird nicht als bestanden umdeklariert.

## Visuelle Nachweise

Echte Unreal-QHD-PNGs, keine generierten Bilder. Die Dateien bleiben lokal unter `Saved/ProjectRefinement/PokemonAIV3`, nicht im Git-Commit. Die beiden Teich-Vergleichsbilder verwenden identische Kamerapositionen und enthalten beide bereits die neuen Namen; sie vergleichen gezielt nur die Teichgeometrie.

| Motiv | Datei unter diesem Saved-Verzeichnis |
|---|---|
| Teich/Bach vorher | `BeforePond02/Strip.png` |
| Teich/Bach nachher | `AfterPond01/Strip.png` |
| Dorf / Wiese / Wald mit Namen | `NamesAudit03/Village.png`, `Meadow.png`, `Forest.png` |
| Karpador / Garados | `NamesAudit03/Karpador.png`, `Garados.png` |
| Zehn sichtbare Namen | `Density04/Density10_Names1_R3_AfterBenchmark.png` (erst nach Ende des Messfensters) |
| Modelltestgelände | `NativeFunctional01/Model_Pikachu.png` |
| Innenraum / Kampf | `NativeFunctional01/C_Interior.png`, `C_ClassicBattle.png` |
| Wasserfang | `WaterGameplay01/WaterClassicBattle.png`, `WaterCapturedTeam.png` |
| Echter Fußlauf / Bodenstreifen | `WorldFootwalk01/Walk_6.png`, `PondStripWalk01/Walk_2.png` |

Die Sichtbarkeitsgrenzen sind bewusst konservativ. Dichte Kronen können einen Namen verdecken; am Kamerarand kann Text angeschnitten werden. Die Überlappungsbehandlung verwendet eine Näherung der Textbreite. Eine umfassende temporale Videoabnahme wird nicht behauptet.

## Fehler, Warnungen und verbleibende Punkte

* Automation01/02 enthielten einen Fehler im neuen Testaufbau: Ein einfacher Pawn ohne Root stand tatsächlich auf dem Pokémon statt vier Meter entfernt. Der Aufbau wurde korrigiert; die Wahrnehmung musste dafür nicht entschärft werden.
* Automation03 brach einmal mit `pthread_rwlock_init failed with error: 16` in Unreals MassEntity-Modul während des bestehenden Heilhaus-Tests ab. Ursache **nicht abschließend geklärt**, keine unbelegte Engine-Fehlerbehebung. Die anschließenden vollständigen Läufe Automation04/05 bestanden. Der Abbruch bleibt als eigener Fehlernachweis erhalten und wird nicht den iOS-Warnungen zugeschlagen.
* Bekannte externe iOS-Helfer-/Architekturmeldungen und die experimentellen Python-Toolset-Startmeldungen werden nicht durch Änderungen an Engine oder Installation verdeckt. Die letzten funktionalen Automationsberichte haben keine Testwarnungen; das ist keine Aussage, dass jeder native/editorseitige Log warnungsfrei ist. Telemetrie-/HTTP-Warnungen bleiben separat.
* PIEFunctional01 übersprang sein 180-ms-Ausrichtungsfenster durch eine gemessene 227-ms-Framepause. Der Prüfablauf wartet jetzt auf die tatsächlich erreichte Blickrichtung. PIEFunctional02 wählte für den Fang erneut das gerade bekämpfte Bisasam während seiner regulären 30-Sekunden-Sperre. Der korrigierte Lauf verwendet einen anderen über `CanInteract` freigegebenen natürlichen Gegner; keine Spielsperre wurde umgangen. PIEFunctional03 besteht vollständig.
* Frühere Namens-/Dichte-Prüfskripte scheiterten an Unreal-Python-Bindings bzw. an einer für Spieler ungeeigneten Kreaturen-Bodenprüfung. Das sind dokumentierte fehlgeschlagene Prüfversuche; die korrigierten Prüfungen und Rohdaten bleiben daneben erhalten.
* Schlaf hat weiterhin Idle-Darstellung. Kein Schwarm, kein Hunger-/Ökosystem, keine garantierten Gruppen und keine neue Animation.
* Die nachhaltige Grafikleistung/Framezeitspitzen bleiben ein eigener offener Punkt; keine Grafikqualität wurde zur Verbesserung dieser Messwerte abgesenkt.

## Projektschutz und Erweiterung

Die neuen Regeln sind Daten der vorhandenen kuratierten Habitatliste, keine zweite Artenregistrierung. Neue spielbereite Arten werden weiterhin über das vorhandene Register im Modelltestgelände angeboten; Wild-Lebensräume erfordern bewusst passende bestehende Habitatregeln. Wahrnehmung, Interessen und Gruppenneigung können darin angepasst werden.

Die abschließende Hashkontrolle gegen **6.403 ursprüngliche Dateien** ist bestanden: **475 bestehende Save-Dateien und 34 geschützte unversionierte Dateien** sind bytegleich erhalten, ebenso Originalquellen, Modelle/Animationen, alle anderen Maps und die bestehende Nutzerkonfiguration. Die 20 geänderten bisherigen Dateien entsprechen ausschließlich dem ausdrücklich geprüften Umfang; zusammen mit elf neuen Dateien werden 31 eigene Dateien versioniert. `Config/DefaultEngine.ini` enthält bereits vorher vorhandene Nutzeränderungen; sie gehören nicht zum Commit. Vollbackup-Verweise bleiben erhalten. Nur eigene geprüfte Dateien werden versioniert; der Commit und die geprüfte Synchronisation mit `origin/main` werden im Abschlusschat genannt.
