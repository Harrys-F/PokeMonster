# Pokémon-Animationsfeinschliff V4 – Prüfbericht

Stand: 21.10.2026. Ausgangspunkt `da1481482a1272b5df94295b64ca2eade71e7bf8`, aktives Projekt `/Users/harry/Developer/PokeMonster`. Ausschließlich bestehende VisualV2; keine neue Map, kein Worktree, kein neues Pokémon, keine Habitat-Erweiterung. Der Auftrag ist **teilweise umgesetzt**: stärkere Glurak-Flügelanimationen sind ausdrücklich nicht freigegeben.

## Tatsächliche Änderungen

| Bereich | Ergebnis |
|---|---|
| Nebulak | Gesicht geschützte, organisch bewegte Gashülle; äußere Gasbones, langsame Materialverformung und begrenztes temporales Rand-Dithering. In Oberwelt und ClassicBattle aktiv. |
| Enton | Renn-Bodeneindringung durch falsch beeinflusste Schwanz-/Bauchvertices korrigiert; kein künstliches Vergrößern der Füße. |
| Glurak | Orange Flügelrückseiten; dunkle Innenseiten, originale Texturen und Proportionen. Bewährtes Original-Skeleton, Originalgewichte und sieben Originalclips wiederverwendet. Stärkere Flügelschläge verworfen. |
| Alle zehn | Sieben Rollen frameweise aus den Quellen geprüft, acht Walk-/Run-Richtungen im echten PIE-Vorführbetrieb. Keine pauschale Animationserneuerung. |
| Testgelände | Explizit gestartete, transiente Vorführfläche am westlichen Kartenrand; verschwindet nach PIE. Kein normaler Habitat-/Save-Inhalt. |
| Team | Auswahl nach Instanz-ID, Tausch beliebiger belegter Plätze, freie Ziele ans dichte Teamende; volle Instanzdaten bleiben erhalten. Teamplatz 1 aktualisiert den einzigen Begleiter. Während Kampf/Niederlagenrückkehr gesperrt. |
| Schatten | Bestehendes schattenloses Außen-Fülllicht `VS_SoftSkyFill` 0,65 → 1,0. Alle übrigen Kartenwerte unverändert. |

## Quellen, Geometrie und Import

Neue gepackte Blenderquellen liegen unter `Art/Characters/Creatures/{Enton,Nebulak,Glurak}/Source/{Name}_PolishV4.blend`; Exporte unter `Exports/PolishV4`, Prüfdaten in der jeweiligen `PolishV4_Audit.json`. Die unveränderte Meshy-Referenz ist weiterhin enthalten. Packed-Reopen, originale Topologie/UVs und echter FBX-Rückimport wurden geprüft.

| Modell | Vertices | Bones | Neue notwendige FBX-Dateien |
|---|---:|---:|---:|
| Enton | 11.090 | 17 | 1 Mesh-/Idle-Export; sieben bestehende Actionkurven |
| Nebulak | 14.852 | 12 | 7, davon Idle mit Mesh |
| Glurak | 135.600 | 24 | 1 Mesh-/Idle-Export; Originalclips in Unreal |

Neue Unreal-Namensräume: `/Game/Characters/Creatures/{Enton,Nebulak,Glurak}/PolishV4/`. Jeweils eigenes `SK_*_PolishV4` und `DA_*_Presentation`; Enton/Nebulak mit eigenem kompatiblem Skeleton und sieben Clips. Die drei bestehenden Spezies-Datenassets verweisen auf diese Profile; Spezies-IDs und Saveformat bleiben unverändert. Gluraks neue Darstellung verwendet nach Prüfung aller Bone-Namen, Eltern und Resttransformationen das vorhandene MeshyV1-Skeleton und dessen sieben Clips. Eine absichtlich falsche Spezies wird vom Kompatibilitätstest zurückgewiesen.

Enton: 899 Schwanz- und 173 zentrale Bauchvertices behutsam neu gewichtet; Sohlen bleiben unverändert. Ursprünglich lag der tiefste Run-Schwanzpunkt ungefähr 1,23 cm unter dem Boden, endgültig innerhalb numerischer Rundung auf Bodenniveau. Restgeometrie, UVs und Originalmaterialien bleiben erhalten.

Nebulak: Gesichtsbereich über Gas-Gewichte maskiert; WPO mit drei langsamen Richtungen, rechnerisch maximal 3,6 cm XY/2,28 cm Z, schwache innere Farbvariation. Das bestehende Schweben mit 12 cm Bodenabstand bleibt erhalten. Masked/TAA-Dithering ist **keine echte volumetrische Transparenz**; kleine zeitliche Randunruhe bleibt möglich und bedarf visueller Abnahme. Keine zusätzliche Partikel- oder Volumensimulation.

Glurak: Rückseitenmaske mit weichen Übergängen und Schutz bereits orangefarbener Körperflächen. Zusätzliche Flügelgewichtungs- und Bewegungsversuche ergaben keine zuverlässig saubere Verbesserung und wurden nicht übernommen. Der ursprüngliche Run besitzt weiterhin bis ungefähr 1,10 cm rechnerische Bauchunterschreitung; dieser Befund bleibt offen. Keine erfolgreiche neue Flügelmechanik behauptet.

## Vorführung und echte Aufnahmen

`Tools/CreaturePolishV4/README.md` beschreibt die reproduzierbaren Aufrufe. Das Gelände um −5200/−2300 cm besteht nur während der expliziten PIE-Vorführung: neutrale 46×46-m-Fläche, zehn VisualActors ohne Begegnungs-IDs. Native Animationen, artspezifische Referenzgeschwindigkeiten und acht Richtungen; zwischen Takes erfolgen dokumentierte Positionsresets. Das ist eine kontrollierte Modellprüfung und kein natürlicher KI-Fußlauf. Originalspielerzustand und Dev-Save werden kontrolliert.

Weltaufnahmen: tatsächlich 2560×1440, Screen Percentage 100 %, bestehende 2,5D-Spielkamera. ClassicBattle-RenderTargets bleiben gemäß bestehender Darstellung **2560×1080**; echte Slate-Menüaufnahmen besitzen die separat protokollierte Fenstergröße und werden nicht als QHD ausgegeben. Keine Videoabnahme behauptet; zeitlich geordnete Original-PNG-Folgen mit tatsächlichen Aufnahmezeiten liegen lokal unter `Saved`.

Die folgenden Medienpfade sind lokale, optionale Nachweise und werden nicht auf GitHub hochgeladen:

- Vorher alle zehn: `Saved/CreaturePolishV4/BeforeAll10Final/Frame4_QHD00000.png`.
- Endgültige acht Richtungen: `Saved/CreaturePolishV4/FinalAll10Directions/`.
- Endgültige Reaktionen: `Saved/CreaturePolishV4/FinalAll10Reactions/`.
- Nebulak-Bewegung: `Saved/CreaturePolishV4/FinalNebulakFlow/`.
- Glurak-Rückseiten: vorher `BeforeGlurakRear/`, endgültig `FinalGlurakRearBound/`, jeweils unter `Saved/CreaturePolishV4`.
- Beide Battle-Perspektiven: `Saved/CreatureExpansionV3/PolishV4NebuBattle/` und `PolishV4GlurakFinal03/`.
- Team vor/nach: `Saved/CreaturePolishV4/LiveUI/PolishV4_Team01_{Before,After}/ActualSlateViewport.png`.

Frühe Takes mit falscher Rotator-Parameterreihenfolge, Zwischenständen der Flügelgewichtung oder fehlgeschlagenen API-Aufrufen gelten nicht als Endabnahme. Die späteren korrekt ausgerichteten Takes ersetzen diese Nachweise.

## Moderate Schattenaufhellung

SkyLight +15 % brachte keinen überzeugenden, konsistenten Vergleich und wurde verworfen. Stattdessen wurde ausschließlich das bereits vorhandene schattenlose Außen-Fülllicht angepasst. Sonne 7,5, SkyLight 1,25, Lichtfarben/-richtungen, VSM, Lumen, TAA, Bloom, Exposure und private adaptive Spieleraufhellung bleiben unverändert. Baum-/Gebäude-/Figurenschatten werden weiterhin berechnet. Keine Schattengeometrie ersetzt oder entfernt.

Sechs feste Vergleiche: Sonne, Baumkrone, überlappende Kronen, Wiese, Flussufer, Innenraum. Finale Kameratransformabweichung jeweils 0. `FillComparisonFixed/Result.json` enthält Bedingungen; die Dateibezeichnung `Fill08` ist historisch, der tatsächliche endgültige Kandidatenwert ist **1,0**, nicht 0,8.

| Fester Bildausschnitt | Vorher Code-Luma | Nachher | Relative Änderung |
|---|---:|---:|---:|
| Krone, Figur/Boden | 52,04 | 55,01 | +5,71 % |
| Krone, dunkler Weg | 33,10 | 39,09 | +18,10 % |
| Überlappende Kronen | 19,25 | 22,93 | +19,12 % |
| Sonnenbereich | 126,13 | 127,81 | +1,33 % |
| Innenraum | 96,576 | 96,555 | −0,021 % |

Dies sind ausgewählte Bildschirm-Codewerte, **keine physikalische Schattenmessung, kein flächendeckender Prozentnachweis und kein Performancegewinn**. Restliche Schwankung insbesondere innen entspricht zeitlicher Aufnahmeabweichung. Die Bildwirkung bleibt zur visuellen Abnahme vorzulegen. `VerifyAccepted.py` prüft alle 1455 Actorzustände; ausschließlich die Intensität dieses einen Fülllichts darf abweichen.

## Team, Gameplay und Testmethodik

`ReorderParty(InstanceId,TargetIndex)` tauscht vollständige Instanzen. Keine Teilrekonstruktion, keine neuen IDs. Ungültige/duplizierte Mitglieder, ungültige Ziele, Kampf und Niederlagenrückkehr werden abgewiesen. Die vorhandene dichte Team-Liste und das Saveformat bleiben erhalten: freie Zielplätze hängen das Mitglied ans Teamende, erzeugen keine leeren Zwischenplätze. UI benennt dieses Verhalten ausdrücklich.

Tastatur-Pfeile/Enter und tatsächliche Slate-Ereignisse geprüft; Akzeptieren verwendet die bestehenden Interaktions-Keys, D-Pad/Navigation ist softwareseitig vorbereitet. Physischer Switch-Pro-Test bleibt offen. Test `PokeMonster.Overworld.Team.ReorderPreservesInstances` vergleicht vollständige Strukturen einschließlich KP, AP, XP, Level und Status sowie Snapshot-Restore und Kampfsperre.

Echte PIE-Prüfungen: Teamplatz 5→1, sofortige Anzeige, genau ein gewechselter Begleiter, freier Platz, Save/Load, aktive Kampfsperre. Die vorhandenen Begegnungsprüfungen verwenden ausdrücklich deklarierte Laufzeitfixtures (u. a. Level/Team/RNG); sie beweisen Abläufe, keine natürliche Fangrate oder Spielbalance.

Ein separater echter Enhanced-Input-Fußlauf absolvierte 103 Schritte und 290,79 m inklusive Sprint (315 cm/s), Wald/Brücke, Dialogen/Quest, Kampf/Fang, Heilhaus, Heilung und Save/Load. Begleiterprotokoll: 636 Samples, davon 40 im Kampf verborgen und 42 innen ohne Schatten; keine gemeldeten Issues. Raumwechsel erklären große Distanzspitzen; daraus wird keine normale Verfolgungsdistanz abgeleitet.

Der ursprüngliche Dev-Spielstand wurde nach Schreibtests anhand der eindeutig zugeordneten Testausgabe restauriert; SHA-256 weiterhin `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`. Keine fremden Saveänderungen überschrieben.

## Grenzen und offene Punkte

- Stärkere Glurak-Flügelanimationen, kleine dunkle Restbereiche an gefalteten Flügelrändern und seine geringe Run-Bauchunterschreitung bleiben offen; keine vollständige Animationsfreigabe.
- Frameaudit findet auch bereits bestehende minimale Run-Unterschreitungen bei Pikachu (~0,43 cm) und Gengar (~0,48 cm); keine ungeprüfte Gewichtsänderung dieser Modelle.
- Fußgleiten und alle Extremposen sind durch finite Takes nicht mathematisch ausgeschlossen; keine vollständige künstlerische Abnahme aller 70 Clips behauptet.
- Nebulaks weicher Masked-Rand ist temporal und muss in Bewegung visuell abgenommen werden.
- Physischer Controller bleibt offen; keine Hardwareprüfung behauptet.
- Keine FPS-Benchmarks, kein GPU-Profiling und keine neuen Habitate.
- 14 selbst erzeugte Glurak-Zwischenprodukte (sechs FBX und acht ungenutzte neue Animationsassets/Skeleton) wurden nach Registry-Prüfung ohne externe Referenzen und SHA-Prüfung ausschließlich in `Saved/CreaturePolishV4/RejectedInputs` verschoben. Keine Löschung, keine fremden/unversionierten Originaldateien betroffen; nicht auf GitHub hochgeladen. `RejectedInputsMoved.json` enthält Einzelpfade und Hashes.

## Abschließende technische Ergebnisse und GitHub

- Mac Development Editor Build07 erfolgreich (33,29 s); zusätzlicher Unity-Build erfolgreich. Frühere Compile-/API-Fehlversuche sind in lokalen Logs erhalten und korrigiert, nicht als erfolgreiche Tests gezählt.
- Elf vorhandene Maps: jeweils 0 Fehler / 0 Warnungen im finalen Map Check; keine andere Map gespeichert. Darunter auch die vorhandene geschützte unversionierte Testmap.
- Blender: alle drei gepackten Quellen erneut geöffnet, neun notwendige FBXs zurückimportiert; alle 70 finalen Sourceclips frameweise gelesen. Quelle/UV/Topologie-Prüfungen erfolgreich.
- Team-UI, Save/Load und Begleiterwechsel: `Team01/Result.json` erfolgreich.
- Alle sieben zusätzlichen Spezies: `Saved/CreatureExpansionV3/PolishV4Capture01/Result.json`, Fang/Verbrauch/Team/Heilung/Save erfolgreich.
- Enton: echte Niederlagenflucht 1093,08 cm; Nebulak 1269,16 cm; endgültiger Glurak 1525,37 cm in 29,02 Spielsekunden. Vor Entfernung außerhalb des Kamerabilds, genau ein Kampf und kein unmittelbarer Respawn. Glurak erhielt 1074 XP im deklarierten Testfixture.
- Niederlagen-Autosave: `Saved/StarterExpansionV1/PolishV4Defeat/Result.json` erfolgreich; WorldBattle-Sonderausgang `Saved/WildEncountersV2/PolishV4WorldOutcome/Result.json` erfolgreich.
- Endgültige Glurak-Battle-Darstellung und beide Perspektiven: `PolishV4GlurakFinal03` erfolgreich. Der erste finale Versuch wurde durch ein Wildkontakt-Ereignis im Aufnahmefixture abgebrochen; der reine Präsentationslauf pausiert nun ausdrücklich Wild-Ticks/Kollisionen im PIE. Das ist keine Produktionsänderung. Anschließende natürliche Kontakt-/Fluchtprüfung separat erfolgreich.
- Ein Editorstart mit einmaligem Python-Startparameter beendete den Editor regulär vor der Queue; daraus folgende Timeouts sind **keine** Gameplay-Pässe. Dauerhafte Queue mit regulärem ExecCmd-Start geprüft.
- Team-Arbeitspaket bereits regulär auf `origin/main`: `b5e17eb4bc1db2d80633e7fe8338f25c77d422dd`; exakt 15 geprüfte Pfade, kein LFS-Upload, Remote bestätigt.
- Vollständige Automation01: **92 erfolgreich, 0 Warnungen, 0 Fehler** vor finaler Glurak-Rückbindung. Automation02 und finale Automation03: jeweils **91 erfolgreich + 1 erfolgreich mit Warnungen, 0 fehlgeschlagen, 0 nicht ausgeführt**. Der strenge Projekt-QA-Wrapper lehnt beide Warnläufe ab; kein warnungsfreier finaler Gesamtlauf behauptet.
- Finale Warnung traf `PokeMonster.Creature.ExpansionV3.ImportedAssetsAndStableIdentities`, dessen Zustand trotzdem `Success` und Fehlerzahl 0 ist: zwei asynchrone `LogHAL`-Einträge vom installierten iOS-Gerätescanner `idevice_id` (`Bad CPU type`, Fehler 86). `file` bestätigt x86_64-Binary; der Mac ist ARM64. Enginequelle `IOSDeviceHelper.cpp` zeigt den Hintergrundaufruf. Engineinstallation, Warnfilter und Tests wurden nicht zur Erzeugung eines grünen Ergebnisses verändert. Eine Installation/Reparatur der Apple-/Epic-Hilfssoftware ist nicht Teil dieses Auftrags.
- Zusätzlich in Engine-Startlogs: installierter CoreUnifiedErrorTest-Startupbefund, bekannte ältere Material-Instancing-Hinweise `MI_WLA_LeafOak`/`MI_WLA_Stone`, Audio-/iOS-Erkennungshinweise. Diese werden nicht als neue Projektregression oder behoben ausgegeben; Rohlogs bleiben lokal erhalten.
- Alle 51 zu Beginn vorhandenen geschützten unversionierten Dateien per SHA unverändert. Von 365 überwachten ursprünglichen Karten-/Kreaturdateien weicht nur die beabsichtigte VisualV2-Map ab; drei Spezies-Datenverweise sind gesonderte beabsichtigte Änderungen. Beide lokalen Backup-Refs bleiben unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; dessen Commit wird nicht Teil von `main`.
- Das zweite Arbeitspaket enthält 81 gezielt geprüfte Projektpfade plus aktualisiertes Core-Manifest. Davon 40 LFS-Dateien mit insgesamt 106.276.411 Bytes (ca. 101,35 MiB); keine Screenshots, Videos, Caches oder Builds. Notwendige neun FBX-Exports, drei gepackte Blenderquellen, drei Quellen-Audits und die tatsächlich benötigten Unreal-Assets sind enthalten. Historische Einmal-Werkzeuge sind als solche dokumentiert und gegen Überschreiben veröffentlichter V4-Dateien gesperrt.
- Auch nach Auslagerung der 14 eigenen verworfenen Zwischenprodukte: alle elf Map Checks weiterhin 0 Fehler / 0 Warnungen (`ReleaseMapChecks.json`). Es gibt keinen fehlgeschlagenen Gameplay-Assertionstest; der abschließende strenge Automation-Gate bleibt aufgrund der oben genannten externen Warnung ausdrücklich offen.
- Remote-/LFS-Quittung wird nach der regulären Sicherung ergänzt. Die aktuelle Kontingentanzeige des GitHub-Kontos ist hier nicht eingesehen; keine Kauf-, Budget- oder Kontoeinstellung geändert. Historische `origin/main`-LFS-Pointer ergeben 7.052 GiB an eindeutigen Objekten; das ist keine kontoweite Abrechnung oder Messung verwaister Remoteobjekte. Neue LFS-Übertragung wird getrennt protokolliert und bei Quota-/Netzfehler nicht wiederholt.



## Empfehlung

Teamverwaltung und Enton-Korrektur sind funktional geprüft. Nebulaks Gasdarstellung, Gluraks Rückseitenfarbe und die moderate Außen-Füllung liegen zur visuellen Abnahme vor. **Keine vollständige künstlerische Freigabe aller zehn Animationen:** Gluraks größere Flügelbewegungen und kleine restliche Kontakt-/Maskenprobleme bleiben ausdrücklich offen. Auch der finale strenge Warnungsfrei-Gate ist wegen der installierten iOS-Hilfssoftware nicht erfüllt, obwohl alle 92 Projekttests ihre Assertions bestanden. Kein weiterer Kreaturen- oder Habitat-Ausbau nach diesem Auftrag.
