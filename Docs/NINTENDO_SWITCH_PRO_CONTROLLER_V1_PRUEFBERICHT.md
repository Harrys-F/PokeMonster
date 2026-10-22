# Nintendo Switch Pro Controller V1 – Prüfbericht

Stand: 22.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, `main`, Ausgangscommit `624aaf4460aada95d2c0b4faffab31c3aa889f92` (zu Beginn identisch zu GitHub).

**Ergebnis:** Softwareseitige Belegung im vorhandenen Enhanced-Input-/UMG-System umgesetzt und geprüft. **96/96 Automationstests, 46 echte PIE-Slate-Eingabeprüfungen und elf Map Checks erfolgreich.** Vollständiger Gameplay-Rundweg: 103 Schritte, 294,36 m, ohne Test-Teleports. Die neu belegten physischen Controllerfunktionen benötigen weiterhin Harrys Hardwareabnahme.

## Tatsächliche Belegung

| Physische Nintendo-Taste | UE-Key im aktiven Apple-GC-Backend | Funktion |
|---|---|---|
| Linker Stick | `Gamepad_Left2D` | Bestehende Acht-Richtungs-Bewegung |
| L3 | `Gamepad_LeftThumbstick` | Sprintmodus an/aus, auch im Stand |
| B | `Gamepad_FaceButton_Right` | Bestätigen, Interagieren, Herausfordern, Attacke/Item/Teamziel auswählen, Dialog weiter |
| A | `Gamepad_FaceButton_Bottom` | Auswahl abbrechen, zurück, Menü/Dialog schließen |
| X | `Gamepad_FaceButton_Left` | Gemeinsames Team-/Beutel-Schnellmenü |
| L / R | `Gamepad_LeftShoulder` / `Gamepad_RightShoulder` | Vorige/nächste der zwei vorhandenen Kategorien |
| + | `Gamepad_Special_Right` | Hauptseite desselben Reisebuchs / fortsetzen |
| Steuerkreuz | `Gamepad_DPad_*` | Menü-, Team-, Item- und Kampfauswahl |

Die Zuordnung wurde nicht aus einer Xbox-Tastenzeichnung abgeleitet: Der anfangs laufende Editor meldete `Slate.MacControllerPreferGCImpl=1`; der lokale Unreal-5.8.2-Quellcode `ApplicationCore/Private/Apple/AppleControllerInterface.cpp` ordnet `buttonB/buttonA/buttonX` an Right/Bottom/Left. Die bereits vom Nutzer bestätigte physische B-Kampfeingabe wird beibehalten und auch an die bestehende Oberwelt-Interaktionsaktion gebunden. Der vorhandene Legacy-HID-Pfad ordnet B/A/X anders zu; der zentrale Helfer folgt dessen dokumentierter Tabelle, ohne das Backend umzustellen. Eine zusätzliche lesende GameController-Abfrage außerhalb des Editors lieferte keine Geräte-Metadaten; daraus wird weder ein Verbindungsfehler noch eine Hardwareabnahme abgeleitet.

## Umsetzung

- Gemeinsamer kleiner Tastenhelfer für Charakter, Reisebuch, Dialog und Kampf. Keine neue Steuerungsarchitektur. Ein nicht konsumierender Slate-Beobachter aktualisiert Hinweise und kann Rohereignisse anzeigen.
- Die bisher fehlende B-Gamepadbelegung verwendet dieselbe `InteractAction` wie E/Enter und damit dieselbe Zielauswahl, Reichweite und Wild-/NPC-/Gebäude-/Heilpunktlogik. Kontaktregeln aggressiver/territorialer Pokémon unverändert; Begleiter wird kein Interaktionsziel.
- L3 bleibt bis zum nächsten Klick gewählt. Stoppen löscht den Modus nicht; UI, Kampf und Innenräume pausieren nur seine Wirkung. 210/315 cm/s, Shift-Haltesprint, Animationen und Kamera bleiben erhalten.
- X/Tab öffnet das bestehende Team-/Inventarwidget. L/R und Steuerkreuz sind vollständig bedienbar. B wählt Quelle/Ziel der freien Teamumordnung oder ein vorhandenes Heilitem und danach dessen Teamziel. A bricht zunächst die aktuelle Auswahl ab. Gültigkeit, Heilwirkung und Verbrauch bleiben in den vorhandenen Inventar-/Encounter-APIs.
- Plus öffnet eine Hauptseite im gleichen Widget: Team, Beutel, Speichern, Fortsetzen. Vorhandener Save-Slot und Schema unverändert. Keine zweite Menü-/Inventarlogik.
- UMG-Preview-Eingaben verhindern generische Slate-Aktivierung mit der falschen Nintendo-Taste. Wiederholte Bestätigung/Abbruch/Kategorie-/Menütasten werden abgefangen. Fokus kehrt nach Menü, Dialog und Kampf zur Spielansicht zurück. Der alte widersprüchliche Kampfhinweis „A bestätigen / B zurück“ ist korrigiert.

## Durchgeführte Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | Erfolgreich, final `SwitchProBuild06` |
| Vollständige Projekt-Automation | **96/96**, 0 Testwarnungen, 0 fehlgeschlagen, 0 nicht ausgeführt |
| Echte PIE-Slate-Eingaben | **46 Prüfungen bestanden**: Stick, L3, X, L/R, B/A, Plus, Wiederholungssperren, Fokus, Keyboard-Shortcuts, Teamumordnung, Heilitem-Abbruch/Verbrauch, Save/Load, Wanderer-Dialog, Myrapla-Herausforderung, tatsächliche Attacke und Kampf-Teamwechsel |
| Begleiter separat mit tatsächlichen Startermodellen | Ein sichtbarer Glumanda-Begleiter; B-Teamumordnung aktualisiert ihn zu Schiggy; ClassicBattle versteckt/pausiert ihn; nach Kampf kehrt genau der korrekte Begleiter zurück |
| Map Checks | Alle elf vorhandenen Maps geladen, jeweils **0 Fehler / 0 Warnungen**, ohne Speichern |
| Vollständiger PIE-Fußlauf | **103 Schritte / 294,36 m**, kein Test-Teleport, maximal 315 cm/s; Menü, Dialog/Quest, Kontakt-Wildkampf, Fang, Trainerkampf, Brücke/Wald, Heilhaus hinein/hinaus, Heilen, Checkpoint, Save/Load und Sprint bestanden |
| Originalspielstand | Vor und nach Eingabeprüfungen sowie Fußlauf bytegleich restauriert |
| Maps / Assets | Alle elf Map-SHA-256 unverändert; keine Art-/Content-/Modell-/Animationsdatei geändert |

Die isolierten Eingabeproben verwenden ausdrücklich protokollierte Diagnosepositionen für Wanderer/Myrapla und vorhandene ungespeicherte BattleV3-/StarterReview-Fixtures. Sie sind keine natürlichen Fußwege und ersetzen nicht den separat geprüften Rundweg. Der normale vollständige Rundweg hatte ein Legacy-Team ohne sichtbare 3D-Begleiter; dessen leere Begleiterbeobachtung ist deshalb **kein** entsprechender Sichtbarkeitsnachweis. Diese Lücke wurde mit den separaten tatsächlichen Startermodellen geschlossen. Die Fixture-Parteien dürfen nicht mit dem realen gespeicherten Nutzerteam verwechselt werden.

Original-Save-SHA-256: `eeab48f3c5652ef6d24b7f386ee7c26973336c929edf39aa7f6593d407a913df`.

## Vorläufe, Warnungen und Grenzen

Neue Test-Fixtures mussten zunächst hinsichtlich Freundschaftsdeklaration/TArray-Aufbau korrigiert werden; ein durch Unity-Build verdeckter unvollständiger Controller-Typ wurde durch einen normalen CPP-Setter behoben. Eine alte Mapping-Anzahlerwartung 15 wurde ausdrücklich auf die genehmigten 19 Belegungen aktualisiert. Die anschließenden 96 Tests bestehen. Python-Prüfvorläufe wurden an tatsächlich verfügbare UMG-/GUID-APIs und den bestehenden verzögerten Kampfabschluss angepasst; keine fehlgeschlagenen Vorläufe als bestanden gezählt. Alle Vorlaufdaten bleiben unter Saved erhalten.

Ein veralteter Editor-Ready-Eintrag führte zunächst zu einem nicht gestarteten Test. Der Runner prüft jetzt den tatsächlichen Editorprozess; Initialisierungsfehler stoppen das eigene PIE und geben einen unberührten gehaltenen Originalspielstand nur ohne Zielkonflikt zurück. Zwischenzeitlich erschien ein zweiter Editorprozess; die eigene saubere Sitzung wurde regulär beendet und erst mit einer einzelnen Sitzung fortgefahren. Kein Save All, Discard All oder Force Quit.

Vorbestehende Engine-/Umgebungswarnungen separat: `idevice_id` Fehler 86 auf ARM, Meldungen zur Python-Namenskollision `Information`, frühe Engine-Logtestmeldungen „Condition failed“, zeitweise Audio-Abtastratenabfrage sowie bestehende Material-Usage-Hinweise zu InstancedStaticMeshes. Die exportierten Projekt-Automationstests und Map Checks haben keine entsprechenden Testfehler/-warnungen. Keine Material-/Renderkorrektur in diesem Eingabeauftrag vorgenommen.

**Noch physisch prüfen:** B in Oberwelt/Dialog/Beutel/Team, A zurück, L3 inklusive Stop/Menü/Kampfrückkehr, X, beide Schultertasten, Plus sowie Steuerkreuz in allen neuen Menüs. Vom Nutzer zuvor bestätigt sind ausschließlich Stickbewegung, Kampf-Steuerkreuz und physisches B-Bestätigen im Kampf. Analogstick-Menünavigation bleibt optional und wurde nicht als physisch geprüft ausgegeben. macOS-Systemremappings oder abgefangene Systemtasten können nur mit dem tatsächlichen Gerät abschließend ausgeschlossen werden.

Rohereignisse: in PIE `pm.Input.Trace 1`, danach `pm.Input.Trace 0`. Die Anzeige nennt den echten UE-Key und das gewählte Backendprofil. `pm.Input.Key`/`pm.Input.Axis` sind dagegen ausdrücklich **Simulationen**, kein Hardwarebeleg.

## Dateien und Sicherung

Geändert: bestehender Player/Controller, Reisebuch/View-Modell, Dialog-/Kampfwidget, bestehende Mapping-/Sprinttests, TECHNIK und ENTSCHEIDUNGEN. Neu: `PokeMonsterControllerInput.h/.cpp`, zwei gezielte Tests in `PokeMonsterSwitchProInputTest.cpp`, der nur für Entwicklung gebaute Slate-Simulationshelfer, `Tools/SwitchProControllerV1/` und dieser Bericht. Keine neue Map, kein Worktree, keine Projektkopie, keine zusätzliche Pokémon- oder Spielerquelle. Keine Änderung der Kampfkameras oder Landschaft.

Kompakte versionierbare Ergebnisse: `Tools/SwitchProControllerV1/Acceptance.json`; Werkzeuganleitung: `Tools/SwitchProControllerV1/README.md`. Rohlogs und Spielstand-Testnachweise ausschließlich unter ignoriertem `Saved/ProjectRefinement/SwitchPro*` und `Saved/GlumandaV11/Acceptance/SwitchProFinalFoot/`; keine Kontrollmedien oder Caches für Git vorgesehen. Das Pflichtdateimanifest wird für die geprüften Quellen aktualisiert. Vollbackup `03492bd` und LFS-Bestand bleiben unverändert. Keine neuen LFS-Nutzdateien zu übertragen.

**Freigabeempfehlung:** Softwarestand ist technisch geprüft; vollständige physische Switch-Pro-Freigabe erst nach den genannten Nutzertests. Git-Commit und regulärer Push werden nach abschließender Umfangs-/Remoteprüfung erstellt; der neue Hash wird im Abschluss genannt.
