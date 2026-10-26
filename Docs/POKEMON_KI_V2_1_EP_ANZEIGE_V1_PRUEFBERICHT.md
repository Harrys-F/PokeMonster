# Pokémon-KI V2.1 und EP-Anzeige V1 – Prüfbericht

Datum: 26.10.2026 · Projekt: `/Users/harry/Developer/PokeMonster` · Ausgangsstand: `19577343c70e79fcb26d97f93d6df6b37dc8f44a` · Map: `/Game/Maps/Dev_TestMap_VisualV2`.

**Ergebnis:** Koordinierte Sozialbesuche und abgeleitete EP-Anzeigen sind implementiert. Spontane Besuche mit unveränderten Standardprofilen sind in gewöhnlichem PIE nachgewiesen. Ein tatsächlicher ClassicBattle-Sieg führt sichtbar über Level 16; die Werte stimmen nach nativem Disk-Save/Load. Finaler Editor-Build erfolgreich, 261 native Tests ohne Testfehler. Zwei Tests enthalten externe iOS-Helferwarnungen; der strenge Automation-Wrapper endet mit Exit 1 und ist ausdrücklich nicht vollständig bestanden. Zwölf finale Map Checks und die ergänzenden PIE-Kampfregressionen sind erfolgreich; Git-/LFS-Befund steht unten.

## A – vorhandene KI gezielt erweitert

Die bestehende `PokeMonsterCreatureRoamingComponent` bleibt die einzige Zustands- und Bewegungsinstanz. Wandern, Ruhe, Schlaf, Nahrungssuche, Spielerbeobachtung, scheues Ausweichen, territoriale Warnung, Kontakt-/Herausforderungsregel, Niederlagenflucht und Begleiter bleiben erhalten. Keine zusätzliche Art, kein neuer Controller, Behavior Tree oder Gruppenautomat.

Bisher wurden soziale Partner fast nur beim Ende einer Aktivität gesucht. Aktive Ruhephasen konnten keine Anfrage annehmen. Ein wartender Partner hatte außerdem nur indirekt über den Initiator ein Zeitlimit. V2.1 ergänzt:

- Zeitlich begrenzte Anfragen auch während etabliertem Wandern, Idle und Ruhe. Ruhe besitzt eine Mindestdauer; Schlaf, Nahrungssuche, Spielerreaktionen und Kampf werden nicht für eine Einladung unterbrochen.
- Der Empfänger prüft Verfügbarkeit und eigene Annahmebereitschaft. Ablehnung erhält seine laufende Aktivität und setzt kurze Anfrage-Sperren auf beiden Seiten.
- Exklusive gegenseitige Einzelreservierung auf dem Game Thread. Eine Gegenanfrage oder ein drittes Pokémon kann den Partner nicht übernehmen.
- Nach Zusage wartet der Empfänger und richtet sich aus; der Initiator nutzt einen begrenzten kollisionsgeprüften Annäherungsweg. Kein Nachjagen eines ständig bewegten Ziels. Beide wenden sich während des Kontakts weich einander zu.
- Variationen bei Anbahnung (8–13 s Einladungsfenster mit artabhängiger Chance), Anlaufrichtung (±16°), Abstand (beide Navigationsradien + 65–95 cm, bei scheuem Partner weitere 100 cm), Dauer (MinimumSeconds + 2–6 s) und anschließender Pause (1–2,5 s).
- Reisezeitlimit 20 s und zusätzlich unabhängiges Gesamtlimit 30 s bei beiden Partnern. Entfernung, Sichtunterbrechung, Pause, Präsentationssperre, Flucht, verborgener/deaktivierter Partner oder Neukonfiguration lösen die Verbindung beidseitig. Bestehende Spielerreaktionen und Kämpfe behalten Vorrang.
- Ruhe/Neuauswahl und die bestehende Sozial-Abklingzeit verhindern Dauerschleifen. Es werden keine gemeinsamen langen Wanderzüge simuliert.

### Artprofile und effiziente Wahrnehmung

Die übrigen Gewichte und bisherigen Temperamente sind unverändert. Die Annahmechance ist konfigurierbar, kein garantierter Kontakt.

| Art / stabile ID | Vorhandenes Temperament | Sozialgewicht | Annahme gültiger Anfrage |
|---|---|---:|---:|
| Bisasam | neugierig | 2 | 85 % |
| Pikachu | neugierig | 2 | 85 % |
| Glumanda / Zunderlauf | territorial | 2 | 85 % |
| Myrapla | ruhig | 2 | 70 % |
| Enton | scheu | 4 | 85 % |
| Nebulak | scheu | 0,5 | 45 % |

Die Freischaltung bleibt auf diese sechs wilden Arten in VisualV2 begrenzt. Begleiter und Biome-Verträge sind ausgeschlossen. Lokale Broadphase statt vollständiger Paarvergleiche, höchstens zwölf näher geprüfte Kandidaten, gestaffelte Anfragen und Sichtprüfungen (0,8–1,2 s während Kontakt). Vorhandene Entfernungspause ab 4000 cm und Render-/Animationsoptimierungen bleiben erhalten. Keine Weltuhr, neue Schlafpose oder neue Animation; Schlaf bleibt Idle.

### Sozialtests und echte Beobachtungen

Alle elf `PokeMonster.Creatures.NaturalActivities.*`-Tests bestehen. Vier davon sind neu: Zusage/Ablehnung und Mindest-Ruhezeit, Partnerausfall/-entfernung/-neukonfiguration, spontane Besuche mit Standardprofilen sowie die tatsächliche scheue Spielerreaktion gegen eine laufende Reservierung. Bestehende Tests decken zusätzlich dritte Partner, Hindernisse, Mindestabstände, Reise/Abschluss, Unterbrechung und Rückkehr ab. Kontrollierte Mechanismustests verwenden explizit 0/100 % Annahme; diese Testwerte werden nicht als normale Artprofile übernommen.

Normale PIE-Nachweise ohne versetzte Pokémon und ohne Profil-/Zustandsvorgabe:

- `SpontaneousSocial01`: Abschluss innerhalb rund 112 s; zusätzlich eine tatsächlich abgelehnte Anfrage.
- `SpontaneousSocial02`: Abschluss innerhalb rund 59 s.
- `SpontaneousSocial03`: Abschluss innerhalb rund 60 s; nur für die Aufnahme anschließend dokumentierte Beobachterposition, drei nicht zu den sechs Zielarten gehörende territoriale Tiere vorübergehend pausiert.
- `ConnectedPIEFinal01`: rund 142 s zusammenhängender Standardlauf, 75 s unbeeinflusste Aktivitäten, Annäherung/scheue Reaktionen, realer Eingabe-Fußlauf über 100 cm, isoliertes Speichern/Laden und wieder freie Steuerung. Unveränderte Nutzer-Save-Prüfsumme.

Die sichtbaren Sozialabschlüsse dieser kurzen normalen Läufe betreffen die bereits vorhandene Bisasam-Gruppe. Für die anderen fünf Arten wird kein eigener visueller Sozialabschluss behauptet; teilweise gibt es dort nur ein einzelnes passendes Tier. Ihre Wahrnehmungs-/Reaktionsprofile und die gemeinsame Mechanik bleiben konfigurierbar und getestet.

**Klarer zusätzlicher Bildaufbau:** `StandardProfileClearing02` versetzt ausschließlich zwei bereits vorhandene Gruppen-Bisasam während PIE auf eine bestehende freie Wiese, begrenzt deren temporäre Habitate auf 180 cm und verwendet unveränderte Art-/Reaktionsprofile. Kein Spawn, keine erzwungene Sozialaktivität, keine gespeicherte Platzierung. Abschluss nach rund 54 s, kleinster gemessener Partnerabstand etwa 141,68 cm. Dieser Aufbau illustriert die Bewegung, ersetzt die normalen Habitatnachweise aber nicht.

Die ersten normalen Fotos enthalten starke Kronenverdeckung beziehungsweise ungünstigen Bildausschnitt. `StandardProfileClearing01` lief wegen auseinanderwandernder Partner ohne Abschluss in sein Testlimit; das ist ein fehlgeschlagener visueller Aufbau und wird nicht als bestanden gewertet. Er bleibt lokal erhalten. Für die bessere Aufnahme wurde nur der temporäre Prüfbereich begrenzt, keine produktive Habitat- oder Landschaftsänderung übernommen.

## B – EP-Anzeige aus bestehenden Daten

`FPokeMonsterExperienceView` ist ein gemeinsamer, rein lesender UI-Snapshot für OverworldView und BattlePresenter. Keine neuen Save-Felder, Erfahrungskurven, EP-Erträge oder Fortschrittsregeln.

Berechnung mit der individuellen verwendeten Wachstumskurve einschließlich vorhandener Entwicklungs-Overrides:

```
Levelbeginn = ExperienceForLevel(Kurve, Level)
Nächste Grenze = ExperienceForLevel(Kurve, Level + 1)
EP innerhalb des Levels = Gesamt-EP − Levelbeginn
Benötigt für dieses Level = Nächste Grenze − Levelbeginn
Fehlend = Nächste Grenze − Gesamt-EP
Balken = EP innerhalb des Levels / Benötigt
```

Das konfigurierte Höchstlevel 100 zeigt einen vollen Balken und „MAX“, ohne Level-101-Abfrage, negative Restwerte oder Division durch null. Fehlende/inkonsistente Daten werden als nicht verfügbar angezeigt und nicht still verändert.

### Bedienung und Darstellung

Das bestehende Reisebuch verwendet seine bisherige Attackenansicht jetzt als **Pokémon-Info**. Kein zweiter Statusbildschirm: **X → Team → L → Pokémon-Info → Pokémon mit B wählen**. Danach Level, blauer EP-Balken, aktuelle/benötigte EP und fehlende EP bis zum nächsten Level. Das Repertoire bleibt lesend; Aktivieren/Neuordnen ist weiter ausschließlich beim Meister möglich. Drei statt vier gleichzeitig sichtbare Repertoirezeilen schaffen Platz ohne größeres Menü; Navigation erreicht weiterhin alle Einträge.

Im eigenen ClassicBattle-Status stehen unveränderte lesbare KP und darunter ein schmaler blauer EP-Balken. Gegneranzeige, Kameras und Kampfmenüs bleiben erhalten. Die eigene Karte ist nur um zehn logische Pixel höher. Echte Vorher-/Nachherwerte der bestehenden EP-Transaktion werden als Präsentationsmetadaten übergeben, nach Empfänger-ID zugeordnet und animiert. Keine zweite EP-Vergabe. Wechsel zeigt den richtigen individuellen Fortschritt. Die neue EP-Phase verwendet verstrichene Spielzeit, damit mehrfache Timeraufrufe in langsamen Bildern nicht beschleunigen.

B bestätigt, A geht zurück, X öffnet, L/R wechseln Kategorien, Steuerkreuz navigiert. Tastatur bleibt nutzbar. Im tatsächlichen Apple-GC-Backend meldet die Software B als `Gamepad_FaceButton_Right`, A als `Gamepad_FaceButton_Bottom`, X als `Gamepad_FaceButton_Left`; die physisch benannten Nintendo-Tasten werden nicht nach Xbox-Positionen vertauscht. Kein neuer physischer Controller-Test wird behauptet.

### EP-Tests und tatsächliche Zahlen

Fünf neue native Tests `PokeMonster.UI.Experience.*` bestehen: alle sechs bestehenden Kurven an Beginn/Mitte/kurz vor Grenze sowie MAX/Fehlerdaten; mehrfache Levelaufstiege mit Lernen und Entwicklung; bestehender Save-Roundtrip und Teamplatzwechsel; echte Info-Widget-/Cache-/Controllerbindung; echte Kampf-EP, Präsentationsbindung und Wechsel. Die komplette bisherige Lern-, Entwicklungs-, Fang-, Heil-, Repertoire-, AP-, Save-, ClassicBattle-/WorldBattle- und Eingaberegression ist zusätzlich enthalten.

`ExperiencePIE03` ist ein normal gestartetes PIE mit ausdrücklich gekennzeichneten vorhandenen Editor-Party-/Sieg-Fixtures und ausschließlich einem neuen isolierten Testslot:

| Zeitpunkt | Level | Gesamt-EP | EP im Level | Benötigt | Fehlend |
|---|---:|---:|---:|---:|---:|
| Vor Sieg | 15 | 4095 | 720 | 721 | 1 |
| Nach tatsächlichem Sieg, +20 EP | 16 | 4115 | 19 | 817 | 798 |
| Nach Disk-Save/Load | 16 | 4115 | 19 | 817 | 798 |
| MAX-Prüfung | 100 | 1000000 | MAX | — | 0 |

Kampfsieg, sichtbarer Grenzübertritt, sieben unterschiedliche aufgezeichnete EP-Stände, B/A/X/L-/Steuerkreuz- sowie Enter-Bedienung, anderer Teampartner, MAX, Rückkehr und weiter freie Steuerung sind nachgewiesen. Identität, Level, EP, KP, AP und Position bleiben nach isoliertem Disk-Save/Load erhalten. Die spätere MAX-Prüfung wird durch Laden dieses Testslots zurückgenommen. Nutzersaves bleiben unverändert.

`ExperiencePIE01` brach ausschließlich wegen eines falschen Python-API-Namens im neuen Prüfskript vor der eigentlichen Prüfung ab. Korrigiert auf `GameplayStatics.get_player_pawn`. `ExperiencePIE02` bestand, zeigte bei der Aufnahme aber die Timer-Beschleunigung; die finale Korrektur ist in Build04/Automation02/ExperiencePIE03 geprüft. Keine ältere Prüfung wird als Beleg für den finalen Code ersetzt oder beschönigt.

## Medien – echte Unreal-Daten, lokal belassen

Prüfmedien liegen bewusst unter ignoriertem `Saved/`, keine Kontrollvideos/Caches auf GitHub. Alle Bilder/Frames stammen aus dem laufenden Unreal-Projekt; keine generierten Konzeptbilder oder interpolierten Zwischenbilder.

- [Spontaner Sozialkontakt, normale Habitatpositionen](../Saved/ProjectRefinement/PokemonAIV21ExperienceV1/SpontaneousSocial01/SocialObserve.png) – QHD, eingeschränkte Sichtbarkeit am Bildrand.
- [Klarer Sozialkontakt, deklarierter temporärer Lichtungsaufbau](../Saved/ProjectRefinement/PokemonAIV21ExperienceV1/StandardProfileClearing02/SocialObserve.png) – QHD 2560×1440, normale Kameraperspektive/-größe.
- [Pokémon-Info vor dem Kampf](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03StatusBefore/LivePIEViewportQHD.png).
- [Kampf vor EP-Gewinn](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03BattleBefore/LivePIEViewportQHD.png).
- [Sichtbarer Levelaufstieg](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03LevelUp/LivePIEViewportQHD.png).
- [Pokémon-Info nach dem Kampf](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03StatusAfter/LivePIEViewportQHD.png).
- [Nach Save/Load](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03AfterLoad/LivePIEViewportQHD.png).
- [MAX](../Saved/GlumandaV11/LiveUI/AIV21ExperiencePIE03Maximum/LivePIEViewportQHD.png).
- [EP-Gameplay-Clip](../Saved/ProjectRefinement/PokemonAIV21ExperienceV1/Videos/AIV21ExperiencePIE03.mp4): 210 Originalframes über 28,59 Spielsekunden, tatsächliche Stichprobe **7,31 Hz**, 2331×1311. Sechs Frames mit wechselnder Aufnahmeauflösung beim QHD-Render sind im Video ausgelassen; Rohframes und originale Zeitstempel bleiben erhalten. Kein Hochrechnen auf QHD oder behauptete hohe Bewegungsbildrate.
- [Sozialbewegung, Lichtung](../Saved/ProjectRefinement/PokemonAIV21ExperienceV1/Videos/AIV21StandardProfileClearing02.mp4): 279 Originalframes, 23,52 Spielsekunden, **11,82 Hz**, 2560×1440; keine ausgelassenen Auflösungswechsel und keine interpolierten Bilder.

**Aufnahmemethode unterscheiden:** `ActualSlateViewport.png` ist die unveränderte tatsächliche Slate-Viewport-Aufnahme (2331×1311). Die separat benannte `LivePIEViewportQHD.png` rendert dieselbe laufende PIE-Viewport-/UMG-Struktur nativ in 2560×1440, einschließlich realer Spielszene und Daten. Sie ist ein echtes Unreal-Live-Render, ausdrücklich keine Desktopaufnahme. Beide Dateien und die Methodenbeschreibung liegen nebeneinander. Die eingeschränkte Videobildrate und Kronenverdeckung bleiben sichtbare Grenzen; kein Landschafts-/Kameraumbau für schönere Nachweise.

## Kurzer Vergleich mit KI V2

Frische achtsekündige PIE-Stichproben vor und nach der Änderung, dieselben Instanzpositionen und Messmethode; native gesamte Komponentenzeit pro Bild, Messflagge im Normalbetrieb aus. Keine Video-Kodierung während dieser Messungen.

| Aktive Instanzen, Aktivitäten an | KI V2 ms/Bild | KI V2.1 ms/Bild |
|---|---:|---:|
| 1 | 0,0804 | 0,0844 |
| 3 | 0,0821 | 0,0843 |
| 8 | 0,1820 | 0,1451 |
| 8, entfernt | 0,0012 | 0,0015 |

Keine auffällige zusätzliche Komponentenlast in dieser kurzen Stichprobe. Unterschiedliche Aktivitätsverläufe erlauben keinen allgemeinen Beschleunigungsfaktor. Entfernte Instanzen haben keine neuen Aktivitätsentscheidungen, Nachbarschaftsabfragen oder Pläne. Keine isolierte GPU-Aussage, kein Langzeit-/Großweltbenchmark. Rohdaten: `BaselineV2Performance01/Result.json` und `V21Performance01/Result.json` im Aufgaben-Nachweisordner.

## Technische Abnahme und Schutz

- Finaler Editor-Build: `PokemonAIV21ExperienceBuild04`, Exit 0.
- Vollständige Automation: `PokemonAIV21ExperienceAutomation02`, **261 Tests**, **259 ohne Testwarnungen + 2 mit externen iOS-Warnungen**, **0 fehlgeschlagen, 0 ausgelassen**. Native Engine Exit 0; **strenger QA-Wrapper Exit 1**. Alle elf NaturalActivities- und fünf Experience-Tests erfolgreich.
- Bekannte externe Warnungen betreffen `idevice_id`, `posix_spawn` 86 / Bad CPU type. Sie werden nicht als Projektfehler oder als warnungsfrei bestanden dargestellt.
- Alle zwölf finalen Map Checks: jeweils **0 Fehler / 0 Warnungen**. Die exakte Editor-Szene blieb identisch und ohne schmutzige Map-/Contentpakete; temporäre Editorpräferenzen zurückgesetzt, Editor regulär geschlossen.
- Ergänzende echte PIE-Regressionsläufe `AIV21TerritorialVictory`, `AIV21CuriousFlee`, `AIV21ShyCapture`: alle bestanden. Genau ein territorialer Kontaktkampf, keine Auslösung durch bloße Annäherung; sichtbare Flucht des besiegten Tiers etwa 1353 cm bis außerhalb des Bildes, kein sofortiger Respawn; gerichtete Herausforderung, erfolgreiche Spielerflucht mit Sperre sowie Fang/Teamübernahme/Begleiter-Rückkehr. Alle verwenden die vorhandenen Prüf-Fixtures mit RAM-Schutz des Nutzersaves.
- `FinalVerification.json`: sämtliche 75 Bestandsdateien und 31 fremden unversionierten Dateien identisch, beide Vollbackup-Verweise unverändert, kein kanonischer Recovery-Save. Sieben echte QHD-UI-Render auf Dateidimensionen geprüft.
- Log-Audit: keine Fatal-/Assertion-/Ensure-/Blueprint-Runtime-/Linker-Fehler in den geprüften Editorlogs. Die 17 generischen `LogAutomationTest: Condition failed`-Startdiagnosen treten bereits identisch im unveränderten KI-V2-Ausgangsstart auf; sie werden getrennt von den tatsächlich ausgeführten 261 Tests ausgewiesen. Die dokumentierten Python-/Prüfaufbau-Abbrüche bleiben sichtbar.
- Die zwei mit externen Warnungen abgeschlossenen finalen Tests sind `PokeMonster.CrystalMoves.Production.SolarBeam` und `PokeMonster.NPC.Library.OrdinaryPIEGroundAndIsolation`; je zwei iOS-Helferwarnungen. Keine Warnung betrifft die neue EP- oder Soziallogik.
- Vorher erfasst: **75 Bestandsdateien**, darunter zwölf Maps, 31 fremde unversionierte Dateien und vorhandene Saves. Finale Prüfung vollständig identisch; beide Vollbackup-Verweise auf `03492bd96b4dba44692f675c19d5f11abfa86b4b` unverändert. Kein kanonischer Recovery-Save angelegt. Nur isolierte Testslots neu geschrieben.

Keine Map, kein Content-/Modell-/Animationsasset, keine Spezies- oder Attacken-ID, keine Welt-/Heilhausgestaltung, keine Controllerbelegung und kein Save-Schema verändert. Keine neuen Maps, Modelle, Kopien, Worktrees oder Backups. Die zwei Positionsregeln des Speichersystems, Entwicklung V2.1 und ortsgebundene Attackenverwaltung bleiben erhalten.

## Verbleibende Einschränkungen

- Schlaf verwendet weiterhin Idle; keine Weltuhr, eigenen Schlaf-/Fressanimationen oder komplexen Sozialgruppen.
- Natürliche Sozialhäufigkeit bleibt situationsabhängig. Ein Einzeltier ohne geeigneten Partner erhält keinen künstlich erzwungenen Kontakt. Langfristige Frequenzabstimmung außerhalb der kurzen Beobachtungen bleibt sinnvoll.
- Die vorhandene dichte Vegetation kann normale Habitataufnahmen stark verdecken. Der klare Lichtungsbeleg ist als temporärer visueller Prüfaufbau gekennzeichnet.
- Videos sind echte, zeitgestempelte Stichproben mit begrenzter Bildrate, keine endgültige Abnahme hochfrequenter Animationen.
- Physischer Switch-Pro-Test wurde nicht wiederholt; geprüft sind vorhandene Softwareeingaben und unveränderte Belegung.
- Der strenge QA-Wrapper bleibt wegen externer Engine-Warnungen nicht vollständig bestanden.

## Git-Abschluss

Arbeitspaket A: **`ff13b0c1`**, `feat: coordinate ambient Pokemon social visits`, fünf ausschließlich KI-bezogene Quelldateien. Normaler Push nach `origin/main` erfolgreich. Arbeitspaket B: **`8691f7748a7e7fe598ede09f5a26281991553eb7`**, `feat: show individual Pokemon experience progress`, 31 kontrollierte Textdateien einschließlich Dokumentation und reproduzierbarer Prüfwerkzeuge. Normaler Push erfolgreich.

Serverprüfung per `git fetch`, `git ls-remote` und `rev-list`: `main == origin/main == 8691f7748a7e7fe598ede09f5a26281991553eb7`, Abstand **0/0** am Kontrollpunkt nach Paket B. LFS-Status und `git lfs push --dry-run origin main`: **keine ausstehenden Objekte**, keine neuen LFS-Assets oder -Uploads, keine Budget-/Abrechnungsänderung. Bestehende Asset-/LFS-Verweise unverändert; kein erneuter Download sämtlicher historischer LFS-Objekte behauptet.

Versionierte Arbeitsdateien sauber. Exakt die 31 bereits vorher unversionierten Original-/Biome-Hilfsdateien bleiben unverändert unversioniert; keine Prüfmedien, generierten Builds, Caches oder Saves committed. Alle 75 Schutzprüfsummen und beide Vollbackup-Verweise erneut identisch bestätigt. Keine anderen Prozesse beendet, Editor regulär geschlossen.

Dieser reine Berichtsnachtrag wird separat als `docs: record AI and experience validation status` gesichert. Der danach serverseitig geprüfte endgültige Commit-/Remote-Stand wird zusätzlich in [GitFinal.json](../Saved/ProjectRefinement/PokemonAIV21ExperienceV1/GitFinal.json) festgehalten und in der Abschlussantwort genannt; dadurch muss der Bericht seinen eigenen Commit-Hash nicht vorwegnehmen.
