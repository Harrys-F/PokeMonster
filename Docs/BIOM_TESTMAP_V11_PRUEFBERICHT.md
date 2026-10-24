# Biom-Testmap V1.1 – Prüfbericht

Beginn: 24.10.2026; technischer Abschluss: 25.10.2026. Ausgangscommit `11a1b9ef`. Ziel ist ausschließlich die bestehende `/Game/Maps/Dev_BiomeTestMap_V1`. **Alle fünf Arbeitspakete umgesetzt und funktional geprüft, sieben neue Meshy-Arten integriert. Gesamtfußlauf, Build, zwölf Map Checks und frischer PIE-Start bestanden. Strenger QA-Wrapper Exit 1 wegen externer iOS-Helferwarnungen. Visuelle Nutzerabnahme bleibt ausstehend.**

## 1. Wasserbiom

Die unveränderten Incoming-Originale Karpador (SHA-256 `eaafa7d88721182fd94786624be5358b49da259a238208e315f2788423c2cf77`) und Garados (`ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9`) wurden eindeutig anhand der tatsächlichen Modelle identifiziert. Beide sind ursprünglich ungeriggte, texturierte GLBs ohne Animationen. Eigene Blenderquellen enthalten die Originalgeometrie/UVs, angepasste Rigs und sieben in-place Clips. Karpador nutzt Schwanz-, Flossen- und Körperbewegungen; Garados eine zehnteilige Körperkette. Keine Neugestaltung.

Karpador: Nr. 129, 90 cm. Garados: Nr. 130, **650 cm entlang der Körpermittellinie**, keine 6,5 m hohe stehende Figur. Die vorhandene S-Krümmung und Proportionen bleiben erhalten; tatsächliche aufrechte Meshhöhe rund 373,5 cm. Entsprechende Herkunft steht im Präsentationsprofil. Originaldaten: feste, bereits im Projekt verwendete pret/pokecrystal-Revision `5c877ef55197039c9676e8e3eec6d254b1c40fe8`. Quellen und Fakten unter `Tools/BiomeTestV1/ReferenceSourcesV11.json` und `SpeciesV11.json`. Nicht unterstützte Lernattacken bleiben ausdrücklich unverfügbar; keine erfundenen Ersatzwerte.

Schiggy erhält eine separate Schwimmquelle und einen optionalen Präsentationsoverride nur im Biom-Habitat. Seine bestehende Spezies, Oberfläche, Originalclips und Darstellung in anderen Karten bleiben unverändert. Die gemeinsame Präsentation mischt ein optionales, streng skeletongeprüftes Schwimmclip-Paar ein; Profile ohne diese Erweiterung bleiben bei ihrer bisherigen Darstellung.

Der Teich besitzt nun einen ausreichend tiefen Kern und einen flachen Übergang am Schiggyufer. Fischbewegungen sind auf reale Wassertiefe, Körperfreiraum und Habitatgrenzen beschränkt. Ein kleiner begehbarer Holzsteg mit tatsächlicher Bodenkollision und Geländern erlaubt Beobachtung aus der unveränderten Spielkamera. 103 bestehende Bäume bleiben erhalten; einige Uferbäume wurden innerhalb dieser Testmap umgruppiert. Goldini wird nicht durch ein falsches Modell vertreten: Der generische Wasserprüfmarker ist durch Karpador ersetzt.

### Nachgewiesene Korrekturen und Grenzen

* Der Unreal-Texturimport erkannte Garados' blaue Albedo fälschlich als Normalmap. Shaderfehler und graue Standarddarstellung waren reproduzierbar. Ausschließlich die neue Albedo wurde auf Color/TC_DEFAULT/sRGB korrigiert; der Importadapter setzt dies künftig ausdrücklich. Tatsächliche Unreal-Aufnahmen zeigen wieder das ursprüngliche Blau/Weiß.
* Eine zunächst zu steile Unterwasserböschung verhinderte Schiggys Schwimmen. Die flache Einstiegsböschung und nur für untergetauchten Boden zulässige stärkere Neigung wurden separat korrigiert. Land-Steilhangprüfung bleibt erhalten.
* Der neue Steg blockierte den alten Schiggy-Startpunkt tatsächlich. Nur dieser Habitatstart wurde an freie Uferpositionen verlegt. Zwei Fußlauf-Routenversuche kollidierten korrekt mit Geländern; die Route wurde angepasst, keine Kollision deaktiviert.
* Schwimmen ist oberflächennah; kein Unterwasserspiel, keine universelle Wasser-Navigation und kein Anspruch auf vollständige Fuß-/Flossen-Physik.

## 2. Prüfungen Paket Wasser

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | Build02/03/04 Exit 0; erster Build scheiterte an bestehender Unity-Namensüberschneidung zweier lokaler Konsolenregistrierungen. Nur interne C++-Variablennamen korrigiert. |
| Vollständige Automation | 190 erfolgreich + 1 erfolgreich mit Warnungen; 0 Fehler, 0 übersprungen. OptionalSwimmingContract bestanden. |
| Strenger QA-Wrapper | **Exit 1**, externe iOS-Helfer-Warnung `idevice_id / posix_spawn 86 (Bad CPU type)`. Funktionale Automation erfolgreich, Wrapper ausdrücklich nicht warnungsfrei bestanden. |
| Map Checks | 12 Karten (elf bestehende plus Biom), jeweils 0 Fehler/0 Warnungen; abschließende Wiederholung nach restlichen Paketen erforderlich. |
| Normaler PIE-Fußlauf WaterPIE08 | 172,44 m, 15/15 Ziele; Enhanced Input, reale Kollision, keine Teleports. Keine Habitatüberschreitung. |
| Tatsächliche Schwimmanimation | Knochenbewegung gemessen: Karpador 4,84 cm, Garados 25,51 cm, Schiggy 6,51 cm; Fischbewegung nur im Wasser, Schiggy an Land und im Wasser. Das sind Pose-/Funktionsprüfungen, keine FPS-Benchmarks. |
| Kampf und Speicherung WaterGameplay01 | Fünf echte Classic-/WorldBattle-Prüfkonstellationen, beide Fischperspektiven, tatsächliche Attackenrunde, Fang beider Arten, Teamwechsel, Heilung und RAM-Save/Load bestanden. Explizite technische Testparteien, kein Nachweis natürlicher Wildkontakt-Auslösung. |
| Spielstandschutz | Vor/nach beiden Prüfungen gleicher SHA-256 `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`. Bestehender RAM-Prüftransport wird vor Aktivierung temporären Gameplay-Zugriffs eingeschaltet und anschließend zurückgesetzt. |

## 3. Echte lokale Bildnachweise

Alle Medien bleiben ausschließlich unter ignoriertem `Saved/`, nicht auf GitHub. Keine Konzeptbilder als Implementierungsnachweis.

* `Saved/BiomeTestV11/Before01/`: fünf identische QHD-Kamerastandorte als Ausgangsvergleich (Wasser, Wiese, Felszugang, Ruine, dichter Wald), inklusive tatsächlicher Positions-/Kamerametadaten.
* `Saved/BiomeTestV11/WaterPIE08/JettyObservation_QHD.png`, `WestBank_QHD.png`, `EastBank_QHD.png`: echte Spielkamera 2560×1440, 100 % Renderauflösung.
* `Saved/BiomeTestV11/WaterGameplay01/`: Funktionsprotokoll; einfache HighResShot-Dateien zeigen nur die Hintergrundwelt. Die tatsächlichen Kampf-/Fangmenü-Aufnahmen liegen als Slate-UI-Erfassung unter `Saved/GlumandaV11/LiveUI/`. RenderTarget-Bilder sind nicht automatisch QHD-Spielkameraaufnahmen.
* `Saved/BiomeTestV11/WaterMotion01/`: eigenständiger echter Bewegungsnachweis; Aufzeichnung und Auswertung separat, keine generierten Zwischenbilder.

## 4. Noch ausstehende Pakete

Historischer Wasser-Zwischenstand inzwischen durch die Pakete 6–9 ergänzt. Alle fünf Pakete sind umgesetzt; die abschließenden Gesamttests stehen in Abschnitt 10.

## 5. Integrität und Git

Die Baseline erfasst Hashes von 3190 Originaldateien und allen 38 vorgefundenen unversionierten Dateien. Bisher ausschließlich acht erlaubte Originaldateien (Biom-Terrainquellen, zwei Terrainassets und Biom-Map) geändert; alle 38 ursprünglichen unversionierten Dateien bytegleich. VisualV2, bestehende Pokémonquellen, Spielstände und Vollbackup-Verweise unverändert. Keine neuen Maps/Projektkopien/Worktrees/Backups. Keine Performance-Benchmarkreihe.

Commit-, Remote- und LFS-Nachweise werden nach dem geprüften Sicherungsschritt ergänzt. Kostenbudget bleibt 0 USD, keine Budgetänderung.

Wasser-Nachprüfung: WaterMotion01 bestand erneut 173,21 m / 15 Ziele ohne Teleports. Drei reale lokale 1280×720-Bewegungssequenzen mit jeweils etwa sechs Sekunden, 28–29 tatsächlichen Frames und Originalzeitstempeln erzeugt (größtes Intervall 0,278 s; keine Behauptung kontinuierlicher 30/60-fps-Videos). Erneuter Abhängigkeitsaudit und zwölf Map Checks nach dem letzten Startpunktfix bestanden. Tatsächliche Slate-Kampfansicht visuell kontrolliert: Garados vollständig eingerahmt, Originalfarben sichtbar; große Größenunterschiede bleiben bewusst erhalten.

## 6. Paket Plateau und Höhle

Das vorhandene Terrain erreicht jetzt 1500 cm. Ein etwa 90 m langer Weg mit mehreren Kehren überwindet den Höhenunterschied; größte geplante Mittellinienneigung etwa 23 %. Die tatsächliche maximale Player-Fußhöhe betrug 1501,9 cm (leichte CharacterMovement-Floor-Abstände). Bestehende Rock-Botanik und Actors wurden um die geänderte Geländehöhe versetzt, ohne Originalassets oder andere Maps zu ändern. Machomei bleibt auf der Oberseite.

Ein sichtbarer Bogen aus vorhandenen Felsmodellen liegt am Fuß des Plateaus, Außen-Türpunkt UV ungefähr (−2900, −3450) cm. Zugang vom Hub über die östliche Basis und südlich um den Berg (konkrete Wegpunkte in Layout.CAVE_ROUTE). Die vorhandene BuildingCutaway-Technik versetzt den Spieler unter vollständiger Maske in einen Raum derselben Map bei Welt (25000, 0, 150) cm. Kein neues Level, kein zweites Tür-/Kamerasystem. Der Rückweg führt durch denselben Felsbogen.

Drei vorhandene Cave-Wände und ihre Collider werden wiederverwendet. Eigener Boden, Felsgruppen und Moospolster lassen eine breite mittlere Passage und Randwege frei. Der Raum ist ein begehbarer technischer Höhlenraum; rechteckiger Grundriss und einfache Felsschichtung bleiben sichtbare Art-Grenzen, keine Behauptung einer finalen handgestalteten Höhle. Die neue raumfeste Innenkamera (4550 cm, Pitch −50°, gleicher Yaw/FOV) zeigt die Raumgrenzen; Außenkamera bleibt unverändert. Nur dieser Raum verwendet eigene Kanal-1-Lichter. Deren zunächst bestätigte Überbelichtung stammte aus Candela-Einheiten; korrigiert auf explizite 1200/650/750 Lumen. Keine Außenlicht-, Belichtungs- oder globalen Lumenänderungen.

Der ausschließlich Biom-eigene Bodenmaterialgraph ersetzt im vorhandenen Felsmaskenbereich das erkennbare Mauerwerksmuster durch räumlich berechnete, malerische Schichtung und unterdrückt Erde auf steilen Felsflächen. Gras-, Ufer- und Waldtexturbindungen bleiben erhalten. Die neue Felsfläche hat einfache Oberflächendetails; weitere Art-Verfeinerung ist damit nicht automatisch freigegeben.

Ein optionaler expliziter InteriorOwner erlaubt nur dem zugewiesenen Biom-Glutexo, in genau diesem versetzten Höhlenraum zu wandern. Andere wilde Pokémon meiden Gebäude weiterhin. Das vorhandene Roaming-/Pfadsystem und die vorhandene Kreaturendarstellung bleiben die einzigen Systeme. Raumdarstellung verwendet ausschließlich lokale Lichtkanäle, bestehende Glutexo-Assets bleiben unverändert.

### Tatsächliche Prüfungen

* CaveBuild01: Editor-Build Exit 0.
* CavePIE01: 394,10 m, 35/35 Ziele, rund 1502,1 cm Fußhöhe; Hin-/Rückweg und Höhlen-Glutexo funktionsfähig. Sichtprüfung zeigte Überbelichtung und Mauerwerkswiederholung; deshalb keine visuelle Abnahme dieses Zwischenbilds.
* CavePIE02 nach gezielter Korrektur: 393,25 m, 35/35 Ziele, 1501,9 cm Fußhöhe; genau zwei erlaubte versetzte Türwechsel mit Maske 1,0 vor und nach dem Ortswechsel. Keine fremde Teleportfunktion. Glutexo legte im Raum 405,3 cm zurück. Boden-, Seiten-/Rückwand- und Ausgänge im tatsächlichen Fußlauf geprüft.
* Beide Läufe: bestehender Save-SHA unverändert. Tatsächliche QHD-Spielbilder unter `Saved/BiomeTestV11/CavePIE02/{Ascent_8,CaveApproach_4,CaveCentre,CaveExit}_QHD.png`. Bilder des ersten problematischen Innenlichts bleiben als lokaler Vorher-Nachweis erhalten. Der geänderte Innenkameraabstand wird ausdrücklich ausgewiesen; dies ist kein Vergleich bei identischer Innenkamera.
* Zwölf Map Checks und vollständige Automation werden für diesen Sicherungsschritt erneut ausgeführt; genaue Ergebnisse folgen unten.

Wasser-Sicherung: Commit `6e7615a3b0fdc15c9bcb676f87b829295a411734` regulär auf GitHub gepusht; 60 LFS-Objekte (152714462 Bytes) anschließend vollständig anhand heruntergeladener Remote-SHA-256 verifiziert. Main/origin/main waren an diesem Sicherungspunkt identisch.

Plateau-/Höhlen-Abschlussprüfung: erneuter Assetaudit ohne fehlende Referenzen; alle zwölf Map Checks 0 Fehler/0 Warnungen. CaveAutomation01: Engine Exit 0, 190 erfolgreich plus 1 erfolgreich mit Warnungen, 0 fehlgeschlagen/übersprungen. Strenger Wrapper weiterhin **Exit 1** ausschließlich durch protokollierte externe `idevice_id / posix_spawn 86`-Warnungen (diesmal im DragonRage-Testkontext). Kein warnungsfreier QA-Erfolg behauptet. Fünf kurze lokale tatsächliche Bildsequenzen unter CavePIE02, Originalzeitstempel, maximal 0,210 s Abstand; keine generierten Zwischenframes. Alle 38 ursprünglichen unversionierten Dateien, übrigen Originalquellen und VisualV2 weiterhin bytegleich, Vollbackup-Verweise unverändert.


## 7. Paket Wiese und fünf weitere Arten – technische Umsetzung

| Art | Dex | Originalgröße | Dreiecke | Rig |
|---|---:|---:|---:|---|
| Raupy | 010 | 30 cm | 20990 | sieben Knochen, segmentierter Körper |
| Hornliu | 013 | 30 cm | 21237 | sieben Knochen, segmentierter Körper |
| Smettbo | 012 | 110 cm | 21188 | 14 Knochen, getrennte obere/untere Flügel |
| Bibor | 015 | 100 cm | 21267 | 14 Knochen, Flügel, Arme, Beine, Hinterleib |
| Habitak | 021 | 30 cm | 26586 | 14 Knochen, Flügelspitzen, Beine, Schwanz |

Verbindliche Quelle jeweils die eindeutig identifizierte gleichnamige Incoming-GLB. Neutralgeometrie, originale UVs und extrahierte Originaltexturen bleiben erhalten; nur einheitliche metrische Skalierung und technische Skin-/Rigvorbereitung. Eigene gepackte Blenderquellen und sieben Standardclips pro Art, bei Habitak zusätzlich Takeoff/Hover/Land. Die strenge bestehende Quellenprüfung wurde auf die vorhandene Clipanzahl parametrisiert, nicht abgeschwächt: alle fünf Source02-Prüfungen mit normalisierten Gewichten, identischen UVs und tatsächlichen FBX-Roundtrips erfolgreich. Ein im eigenen Rig nachgewiesener etwa 7-mm-Knie-/Knöchelversatz wurde vor Import durch explizite lokale Posenberechnung korrigiert; Kontrollprobe <1e−8 m. Das ist keine Behauptung perfekter Fußphysik.

Die gespeicherte Testmap enthält fünf zusätzliche begrenzte Habitate und 685 zusätzliche Botanikinstanzen in asymmetrischen Gruppen (240 Gräser, 120 höhere Gräser, 170 Blüten, 90 Klee, 65 Kräuter), mit freien Wegen und Beobachtungsflächen. Insgesamt 15 Habitate mit 16 Exemplaren im normalen PIE. Smettbo/Bibor verwenden ihre Flügelanimationen und getrennte 130/155-cm-Flugebenen; die Bodenfreiheit und der reale Körperraum werden geprüft. Habitak nutzt dieselben Roaming-/GroundHover-Funktionen wie vorhandene Arten, nur mit eigener ausdrücklich aktivierter Überflugoption. Normales Abheben und Landen verlangen eine freie Säule zum Boden. Die Kampfpause erhält bei genau dieser Option die sichere Flughöhe; andere Arten/Maps werden nicht umgestellt. Kein allgemeines freies dreidimensionales Flugsystem.

Vier tatsächlich benötigte Attackenassets wurden mit festen Kristall-Quellen an vorhandene Effektmechaniken gebunden: Furienschlag, Giftstachel, Pikser und Fadenschuss. Kein neues Kampfsystem, keine Änderung bestehender Move-Assets. Originaldaten und SHA-256 unter ReferenceSourcesV11.json/MoveBindingsV11.json. Noch fehlende Lernattacken sind ausdrücklich nicht verfügbar: Smettbo SUPERSONIC/WHIRLWIND/GUST/PSYBEAM/SAFEGUARD; Bibor TWINEEDLE/PURSUIT/PIN_MISSILE; Habitak PURSUIT/MIRROR_MOVE/DRILL_PECK. Es wurden keine erfundenen Ersatzattacken eingesetzt. Die aktuellen Testlevel besitzen überprüfte spielbare Attacken.

### Nachgewiesene Fehler und begrenzte Korrekturen

* Längere Beobachtung zeigte, dass drei feste Insekten-/Fischziele durch vier gespeicherte jüngste Ziele vollständig gesperrt wurden. Die Historie ist nun ausschließlich bei endlichen Biom-Ankersätzen auf höchstens Anzahl minus zwei begrenzt; unbeschränkte Roamer anderer Maps behalten vier Einträge. Die Nachprüfung verlangt Bewegung auch im letzten Beobachtungsfenster.
* MeadowPIE02 stoppte am strengen Endfenster für Habitak: der ruhige Testroamer hielt unmittelbar beim nahen Beobachter an. Dies war die vorhandene Observe-Reaktion; der Beobachtungspunkt wurde zurückgesetzt, keine KI-Regel entfernt. Nicht sichtbare Skelette werden wie bisher nicht ausgewertet; Knochenbewegung wird zusätzlich bei tatsächlich naher Beobachtung geprüft.
* MeadowPIE03 zeigte Dauerbewegung und alle Flugzustände, flog im natürlichen Zufallspfad aber nicht über den ausgewählten Felsen. Dieser Lauf ist wegen seiner damaligen Überfluganforderung ausdrücklich fehlgeschlagen. Ein separater reproduzierbarer Überflug-/Kampfpausentest ist zusätzlich zwingender Nachweis, kein Weglassen der Hindernisprüfung.
* FlightPause01 beobachtete keinen passenden natürlichen Überflug vor dem Timeout; kein erfolgreicher Pausennachweis behauptet. FlightPause02 steuert nur zwei temporäre sichere Zielanker im PIE, niemals Position oder Pose der Kreatur: tatsächlicher Überflug über den rund 79-cm-Felsen, 18 Kampfpausenframes mit 0 cm Positions-/Höhenabweichung, danach Weiterflug und sichere Landung bestanden. Ursprüngliche Zielanker wiederhergestellt. Der Spielerbeobachtungspunkt und die RAM-Kampfparteien sind ausdrücklich technische Fixtures.
* MeadowGameplay01 scheiterte an der künstlichen Begrenzung auf 20 Fangversuche für Smettbo; keine nachgewiesene fehlerhafte Fangformel. MeadowGameplay02 verwendet kontrollierte Zufallsquellen und unveränderte Produktionswahrscheinlichkeiten, höchstens 40 Versuche. Tatsächlich benötigte Versuche Raupy/Hornliu/Smettbo/Bibor/Habitak: 1/1/2/3/1. Keine Fangchance zugunsten des Tests verändert.

### Geprüfte Funktionen und echte Nachweise

MeadowGameplay02 bestand elf reale Classic-/WorldBattle-Konstellationen, beide klassischen Perspektiven aller fünf Arten, tatsächliche Attackenrunden, Teamwechsel, Fang aller fünf, Heilung und exakten RAM-Save/Load-Vergleich einschließlich Identität, aktiven/erlernten Attacken, AP, Status und offenen Angeboten. Keine natürliche Wildkontaktprüfung: die Biom-Exemplare sind bewusst visuelle, speicherisolierte Testtiere; normale Begegnungen werden über dieselben vorhandenen Klassen und Art-/Wildprofile vorbereitet.

AirBuild06: Editor-Build Exit 0. MeadowAutomation03: Engine und strenger Wrapper Exit 0, 203 erfolgreich, 0 fehlgeschlagen/übersprungen/Warnungszustände in diesem Lauf. Der vorherige MeadowAutomation01 hatte 202 erfolgreich plus 1 erfolgreich mit externer iOS-Helferwarnung und deshalb Wrapper Exit 1. Auch im aktuellen Editorlog treten externe idevice_id/posix_spawn-86-Warnungen auf; es wird kein allgemein warnungsfreier Enginezustand behauptet.

Echte QHD-Spielkameraaufnahmen unter Saved/BiomeTestV11/MeadowViews02 zeigen alle fünf in Originalgröße neben dem Spieler. Explizite reine Foto-Positionierung des Spielers, keine inszenierten Kreaturenposen oder Skalierungsänderungen. Reale Kampfoberfläche separat als ActualSlateViewport.png unter Saved/GlumandaV11/LiveUI/BiomeV11_MeadowGameplay02_*. Einfaches HighResShot zeigt hier nur die Hintergrundwelt und gilt nicht als UI-Nachweis.

Bewegungsvideos bleiben lokal: MeadowPIE01/Habitak_ActualPIE_Flight.mp4 (150 echte Frames, 9,949 s, maximaler Abstand 0,129 s) und MeadowViews02/InsectWings_ActualPIE.mp4 (131 Frames, 7,925 s, maximal 0,122 s). Keine generierten oder interpolierten Zwischenbilder, keine Behauptung 30/60-fps-Aufzeichnung. Die abschließenden Laufwerte stehen im folgenden Absatz.


MeadowPIE04: normaler Enhanced-Input-Fußlauf 88,71 m, 4/4 Beobachtungsziele, kein Teleport. Im letzten 30-s-Fenster bewegten sich Raupy/Hornliu/Smettbo/Bibor/Habitak noch 178,9/155,8/1364,5/1535,6/389,8 cm. Alle fünf zeigten bei sichtbarer Beobachtung animierte Knochen. Habitak durchlief Grounded/Takeoff/Hover/Landing, erreichte 139 cm und legte 2453,9 cm im tatsächlichen Flug zurück; 15 natürliche Felsüberflug-Samples zusätzlich zum gezielten FlightPause02. Keine Habitatüberschreitung. Lokales Video MeadowPIE04/HabitakFlight_ActualPIE.mp4: 155 echte Frames, 10,136 s, maximal 0,141 s Abstand.

Wasser-Regressionslauf WaterPIE09 nach der Historienkorrektur: 172,78 m, 15/15 Ziele, Knochenbewegung aller drei, Schiggy an Land/im Wasser, keine Habitatüberschreitung. Auch im letzten 15-s-Fenster noch Karpador 296,1 cm, Garados 454,8 cm, Schiggy 183,2 cm. Assetaudit ohne fehlende Referenzen, 103 erhaltene Bäume und 15 gültige Habitate. Zwölf explizite Map Checks jeweils 0 Fehler/0 Warnungen. Der Auswerter trennt die zusätzlichen automatischen Ladechecks von den expliziten BEGIN/END-Prüfungen. Save-SHA in sämtlichen genannten Endprüfungen unverändert. Alle 3190 Baseline-Originale vorhanden, nur acht genehmigte Biom-Dateien geändert; alle 38 ursprünglichen unversionierten Dateien bytegleich, Vollbackup-Refs unverändert.

Plateau-/Höhlensicherung: Commit bdd559d3 regulär auf origin/main vorhanden; sieben LFS-Objekte (7729955 Bytes) durch tatsächlichen Remote-Download und SHA-256 bestätigt.


## 8. Paket begehbare Ruine

Die vorhandene Ruine erhielt einen echten 3D-Steinbogen, vier zusätzliche stehende Säulen, zwei umgestürzte Säulen, vier eingestürzte hintere Steinreste und fünf Wandranken. Dazu 131 eingebettete unregelmäßige Pflastersteine, 88 Moospolster, 23 Farne, 28 Kräuter, 20 Blütengruppen und 38 kleine Schuttgruppen. Zentrale Erinnerungssäule/Runenstein und der alte Grundriss bleiben erhalten. 103 Bäume, Gelände, Lichtquellen und Gengars Art-/Habitatdaten bleiben erhalten. Keine neue Map oder Architekturquelle erforderlich.

Der erste reale Fußlauf RuinPIE01 traf einen neuen Torpfeiler am bisherigen Abzweig (2800,−2800). Nur das neue Portal und seine zwei präzisen Pfeilercollider wurden 250 cm tiefer versetzt; reale Kollision bleibt aktiv, mittlere Öffnung rund 230 cm. RuinPIE02 bestand danach 14/14 Ziele und 110,96 m ohne Teleports: Eingang, mittlerer Laufweg, beide Seitenwege, Runenstein und Rückkehr zum Hub. Gengar bewegte sich 979,4 cm, ohne sein Habitat zu verlassen. Save-SHA unverändert.

Die QHD-Sichtprüfung zeigte zusätzlich die überdehnten UV-Strukturen der drei alten Wandmeshes. Nur diese Komponenten verwenden nun einen privaten Steinmaterialklon mit originalem Textursample in Weltprojektion und unregelmäßigen 112×58-cm-Fugen, ohne zusätzliche Textursamples oder Material-Layer. Andere neue Steine verwenden einen eigenen instancingfähigen Klon des vorhandenen Natursteinmaterials. Keine Originalmaterialien oder Originalmeshes geändert. Eine anfängliche UV-Verbindung wurde vom tatsächlichen UE-Eingangsnamen UVs statt Coordinates abhängig korrigiert; der Editor verhinderte bis zur sauberen Fertigstellung den PIE-Start. Tatsächliche Nachherbilder zeigen Steinstruktur statt der gestreckten früheren Maserung.

Echte identische Vergleichskamera: Before01/Ruine_QHD.png und RuinAfter02/Ruine_QHD.png (beide QHD, Positions-/Kameradaten in Result.json). Zusätzlich freie Figurendarstellung und Wege im tatsächlichen Fußlauf unter RuinPIE02. Keine Licht- oder Kameravarianten für diese Ruinenbilder. Die einfachen hohen alten Wandformen bleiben eine gestalterische Grenze; keine Behauptung einer final ausgearbeiteten Ruinenstadt. Endgültige visuelle Abnahme durch den Nutzer.

RuinAssetAudit ohne fehlende Abhängigkeiten, alle zwölf expliziten Map Checks erneut 0 Fehler/0 Warnungen. Das Assetpaket verändert keine seit AirBuild06/MeadowAutomation03 erfolgreich geprüfte native Spiellogik. Gesamter Build und Automation werden nach dem letzten Kamerapaket nochmals wiederholt.

Wiesensicherung: a196c77647ca2dd7aa9e5b23e17357204e708e7a regulär auf origin/main, 136 tatsächliche Remote-LFS-Objekte / 198363016 Bytes vollständig mit SHA-256 bestätigt. Der Verifier kann jetzt auch ein bereits weiterbearbeitetes Map-File über sein unveränderliches lokales LFS-Objekt dem früheren Commit zuordnen, ohne die Arbeitsdatei zurückzuschreiben. Die zunächst zu große Metadatenanfrage wurde mit HTTP 413 zurückgewiesen; feste 32er-Anfragen verifizieren denselben Satz erfolgreich. Keine Upload-Wiederholung, Budgetänderung oder kostenpflichtige Aktivierung.


## 9. Ausschließlich lokale Kamera im dichten Wald

Gewählte Vergleichsvariante: 1700 cm Abstand nur im markierten dichten Wald, mit sanfter 0,8-s-Überblendung und 180 cm weichem Rand. Standard bleibt 2850 cm, Pitch −50°, Yaw −45°, FOV 35°. Gebiet UV-Mitte (3200,−1700) cm, Halbausdehnung (1050,650,600) cm. Actor `Biome_DenseForestCamera_V11`. Keine neue Taste, kein globaler Zoom und keine Änderung der Bewegungsrichtungen. Der Zone-Schalter bEnabled lässt sich für einen rücknehmbaren Vergleich deaktivieren.

Die vorhandene CameraVisibility verarbeitet weiterhin dieselben Baumfamilien und denselben Grundsichtkegel (110/220 cm). Nur 40 ausdrücklich zugeordnete Bäume dieser Map besitzen private Materialvarianten. Zusätzliches weiches Fenster ausschließlich in oberer Kronengeometrie, Übergang ab Zielhöhe +240 bis +480 cm, endlicher Kamera→Figur-Korridor mit 220/380-cm-Softwindow. Untere Stämme und Unterholz bleiben; Originalmaterialien anderer Karten werden nicht verändert. ShadowPassSwitch verwendet im Schattenpass den ursprünglichen Maskeneingang. Außenlichtquellen, GI-/Bloom-/TAA-Einstellungen, Spieleraufhellung und Original-Schattenparameter bleiben erhalten.

Drei tatsächlich verglichene reine Zoomstufen stehen unter ForestCandidates01: 2850/1700/1200 cm, identischer Spielerpunkt/Yaw/Pitch/FOV. 1200 cm ist für diesen Stil zu nah; reines 1700-cm-Zoom behält eine enge Sichtöffnung. Die erste komplette Kronenvariante ForestCompare01 nahm visuell zu viel Dach weg und wurde verworfen. ForestCompare02 erhält durch das endliche Fenster mehr seitlichen Blätterrahmen; sie zeigt Boden, Farne, Wurzeln und Stämme zusammen mit größerer Figur klarer. Es ist ein schräger Cutaway-Einblick, keine physisch unter allen Kronen befindliche frei drehbare Kamera. Sehr dunkle Waldschatten bleiben sichtbar; keine zusätzliche Aufhellung kaschiert das.

Beim Ergänzen des vierten Materialeingangs erzeugte Unreal vor dessen Anschluss Zwischenkompilierungen mit „Custom missing input 4 (C)“. Gespeicherte Graphen wurden daraufhin ausdrücklich auf alle vier Verbindungen, getrennte originale Schatteneingänge und eigene erfolgreiche Shaderauswertung geprüft und abschließend neu kompiliert (ForestMaterialValidation). Keine aktive fehlerhafte Fassung als Erfolg ausgegeben; frische Editorprüfung steht zusätzlich im Abschlussabschnitt. Die anfängliche Diagnose wird damit präzisiert: Zwischenkompilierwarnung beim Graphumbau, vollständig verbundener Endgraph gültig.

ForestPIE01 zeigte Ein-/Ausblendung korrekt, wurde aber nach bestätigtem Hinderniskonflikt im anschließenden automatisch gewählten Ruinen-Abzweig über seinen eigenen Cleanup abgebrochen. Keine Bäume oder Collider entfernt. Die Prüfrouten führen nun über den tatsächlich freien alten Waldabzweig. ForestPIE02: 139,34 m, 17/17 Ziele, normaler PIE mit Enhanced Input, kein Test-Teleport. 103 Zwischenframes der Übergänge; 1700 cm in der Zone, exakt 2850 cm und keine zusätzliche Kronenüberblendung an Lichtung, Ruine und Hub. Pitch/Yaw/FOV und SightRadiusScale 2 durchgehend geprüft. Lokale echte Bewegungssequenz ForestPIE02/ForestCamera_ActualPIE.mp4: 383 Originalframes, 25,097 s, maximal 0,203 s Abstand; keine interpolierten Frames und keine FPS-Messung.

ForestBattle01: tatsächlicher Angriff und anschließende Flucht in ClassicBattle und WorldBattle bei aktiver lokaler Kamera. 106 beobachtete Kampfpausenframes, Abstandabweichung 0 cm. Danach korrekte Fortsetzung sowie Rückkehr zu 2850 cm außerhalb des Waldes. Individuelle AP/Identität über RAM-Save/Load unverändert. Rein technischer, ausdrücklich speicherisolierter Parteien-/Beobachtungsaufbau, keine natürliche Wildbegegnung. Reale Slate-Menübilder unter Saved/GlumandaV11/LiveUI/BiomeV11_ForestBattle01_*.

Ruinensicherung: 26a88c66082c6e12fe5d8743f78e51161af7d9e6 auf origin/main, drei Remote-LFS-Objekte / 2094353 Bytes vollständig mit SHA-256 verifiziert.

## 10. Abschließende Gesamtprüfung

| Schlussprüfung | Tatsächliches Ergebnis |
|---|---|
| Ein normaler zusammenhängender PIE-Start | FinalLoop01: **904,74 m**, Wasser15/15, Wiese4/4, Plateau/Höhle35/35, Wald17/17, Ruine14/14. Dieselbe Welt/Spielersitzung, tatsächliches Enhanced Input und Kollisionen. Keine Fahrer-Teleports; genau der vorhandene maskierte Höhlenwechsel hin/zurück erlaubt. |
| Editor-Build | BiomeV11_FinalBuild Exit0. |
| Vollständige Automation | Engine Exit0: **204 erfolgreich +1 erfolgreich mit Warnungen**, 0 fehlgeschlagen, 0 übersprungen. Enthält alle bisherigen Gameplayprüfungen und neue Spezies-/Move-/Flug-/Kamerascope-Prüfungen. |
| Strenger QA-Wrapper | **Exit1**, ausdrücklich kein warnungsfreier Pass. Beide Warnungen des erfolgreichen CurseBranchesCapsAndSwitchReset-Tests stammen aus `idevice_id / posix_spawn86 (Bad CPU type)` im externen Engine-iOS-Helfer. Keine Filteränderung am Wrapper. Bestehende Startmeldungen zur MCP-Lizenz und Python-Namensüberschneidung Information bleiben separat, nicht als neue Funktionsfehler ausgegeben. |
| Map Checks / Referenzen | Alle zwölf vorhandenen Karten 0 Fehler/0 Warnungen; keine fehlenden Abhängigkeiten.103 Bäume und15 Habitate mit16 Exemplaren erhalten. |
| Außenbeleuchtung | Lichtpositionen/-richtungen, Intensitäten, Farben, Temperaturen, Schattenparameter sowie Belichtung/Bloom/Lumen mit unveränderter VisualV2 verglichen. Identisch bis1e−6 numerischer Toleranz; ein zunächst beanstandeter Rollunterschied lag nur bei1e−14 Grad aus Quaternion-Rundung. Keine Lichtkorrektur vorgenommen. Lokale Höhlenlichter separat. |
| Frischer Editor / gewöhnliches Play | FreshPIEValidation:15 gespeicherte Habitate erzeugen alle16 Exemplare automatisch, Skalierung1 und gültige Profile; normale Save-Zugriffe bleiben gesperrt. Final gespeicherte Kronenmasken vollständig verbunden und nach Neustart gültig, keine Materialkompilierfehler im frischen Editor10-Log. ForestCompare03 bestätigt echte QHD-A/B-Darstellung. |
| Kampf, Fang, Team, Heilung und RAM-Save | WaterGameplay01/MeadowGameplay02 für alle sieben Arten; ForestBattle01 für Kamerakontexte und beide Präsentationen. Tests ausdrücklich technische Fixtures, keine natürlichen Wildkontaktbeweise. Individuelle Identität/AP erhalten. |
| Quellen / Spielstand / Backup | Alle3190 Baseline-Dateien vorhanden; ausschließlich acht beauftragte Biom-Originaldateien geändert. Alle38 ursprünglichen unversionierten Dateien bytegleich. VisualV2, übrige Maps/Modelle/Quellen und Save-SHA unverändert. Beide Vollbackup-Refs unverändert auf03492bd96b4dba44692f675c19d5f11abfa86b4b. Keine neue Map, Projektkopie, Worktree oder Vollsicherung. |

Physische Controller-Hardware wurde nicht erneut geprüft; funktionierende Grundbelegung bleibt unverändert. Keine FPS-Benchmark- oder umfangreiche GPU-Profilingreihe. Shaderstatistik wurde ausschließlich als erfolgreicher Kompilierungsnachweis verwendet.


## 11. Lokale echte Vorher-/Nachher-Aufnahmen

Die folgenden Links verweisen auf lokale, ignorierte Dateien. Nur dieser Textbericht wird versioniert; **keine Vergleichsbilder oder Videos auf GitHub**. Alle Vergleichsdateien sind tatsächliche2560×1440-Unreal-Ansichten bei100% Renderauflösung. Wiese/Ruine verwenden dieselben Kamerapunkte. Wasser/Felszugang verwenden denselben XY-Punkt/Yaw/Pitch/FOV; die physisch geänderte Steg-/Geländehöhe verändert die Kamerahöhe geringfügig, genaue Werte in den Result.json-Metadaten. Wald-A/B hält Spielerpunkt/Yaw/Pitch/FOV fest; der Abstand ist ausdrücklich die untersuchte Variable.

| Bereich | Vorher | Geprüfter Nachherstand |
|---|---|---|
| Wiese | [QHD vorher](../Saved/BiomeTestV11/Before01/Wiese_QHD.png) | [QHD nachher](../Saved/BiomeTestV11/RuinAfter02/Wiese_QHD.png) |
| Wasser / Steg | [QHD vorher](../Saved/BiomeTestV11/Before01/Wasser_QHD.png) | [QHD nachher](../Saved/BiomeTestV11/RuinAfter02/Wasser_QHD.png) |
| Plateauzugang | [QHD vorher](../Saved/BiomeTestV11/Before01/Felszugang_QHD.png) | [QHD nachher](../Saved/BiomeTestV11/RuinAfter02/Felszugang_QHD.png) |
| Ruine | [QHD vorher](../Saved/BiomeTestV11/Before01/Ruine_QHD.png) | [QHD nachher](../Saved/BiomeTestV11/RuinAfter02/Ruine_QHD.png) |
| Dichte Waldkamera | [Originalsicht A](../Saved/BiomeTestV11/ForestCompare03/DensePath_A_OriginalSight_QHD.png) | [Gewählte lokale Variante B](../Saved/BiomeTestV11/ForestCompare03/DensePath_B_LocalCanopy_QHD.png) |
| Waldrand | [Originalsicht A](../Saved/BiomeTestV11/ForestCompare03/CanopyEdge_A_OriginalSight_QHD.png) | [Lokale Variante B](../Saved/BiomeTestV11/ForestCompare03/CanopyEdge_B_LocalCanopy_QHD.png) |

Weitere tatsächliche Detail-/Figurenaufnahmen: [Raupy](../Saved/BiomeTestV11/MeadowViews02/Raupy_GameCamera_QHD.png), [Hornliu](../Saved/BiomeTestV11/MeadowViews02/Hornliu_GameCamera_QHD.png), [Smettbo](../Saved/BiomeTestV11/MeadowViews02/Smettbo_GameCamera_QHD.png), [Bibor](../Saved/BiomeTestV11/MeadowViews02/Bibor_GameCamera_QHD.png), [Habitak](../Saved/BiomeTestV11/MeadowViews02/Habitak_GameCamera_QHD.png), [Höhle](../Saved/BiomeTestV11/CavePIE02/CaveCentre_QHD.png), [Plateau](../Saved/BiomeTestV11/CavePIE02/Ascent_8_QHD.png), [Schwimmbereich](../Saved/BiomeTestV11/WaterPIE09/JettyObservation_QHD.png).

Tatsächliche Bewegungsdateien: [Habitak Abheben/Flug/Landen](../Saved/BiomeTestV11/MeadowPIE04/HabitakFlight_ActualPIE.mp4), [Smettbo/Bibor Flügel](../Saved/BiomeTestV11/MeadowViews02/InsectWings_ActualPIE.mp4), [Waldkamera hinein/hinaus](../Saved/BiomeTestV11/ForestPIE02/ForestCamera_ActualPIE.mp4). Wasserbewegungssequenzen und Originalzeitstempel unter Saved/BiomeTestV11/WaterMotion01. Keine synthetischen Zwischenbilder.

## 12. Verbleibende Grenzen und Empfehlung

- Begrenzte Schwimmflächen und Flugkorridore sind wiederverwendbare Erweiterungen der vorhandenen Biom-/Roaming-/Präsentationsklassen; keine universelle dreidimensionale Luftnavigation, kein Unterwasser-/Reitsystem. Außerhalb entsprechend vorbereiteter Habitate keine pauschale Umstellung bestehender Arten.
- Die Biom-Map bleibt bewusst ein sicheres visuelles Testgelände. Normale Exemplare beeinflussen Fang-/Team-/Save-Daten nicht. Gameplaywirkung ist mit echten bestehenden Systemen in expliziten RAM-Fixtures geprüft; neue natürliche Begegnungsgebiete außerhalb dieser Map sind hier nicht automatisch angelegt.
- Zusätzliche höhere Lernattacken aus Abschnitt7 bleiben unverfügbar; keine endgültigen Ersatzwerte. Die vorhandenen49 Attackenwirkungen wurden nicht zurückgebaut.
- Prozedural erstellte Grundanimationen und Gewichte sind geprüft; feinste Fuß-/Flügelkontakte sind kein Anspruch auf vollständige Animationsperfektion. Höhle und Ruine behalten einfache alte Grundformen. Sehr dunkle Waldschatten und sichtbare temporale Fensterränder sind bei visueller Abnahme besonders zu beurteilen; vorhandene Lichtstimmung wurde dafür nicht verändert.
- Externer iOS-Helferfehler und bestehende Startwarnungen bleiben offen. Strenger Wrapper weiterhin Exit1. Keine Änderung der Engine-Helfer oder Warnungsunterdrückung in diesem Auftrag.

Empfehlung: Den normalen PIE-Test der vorhandenen Biom-Map zur visuellen Abnahme verwenden, besonders Schwimmbewegung, Habitaks kleine Hindernisüberflüge, Höhlenrückweg und Waldkamerafenster. Keine automatische Übertragung auf VisualV2 und keine weiteren Kreaturen oder Landschaftspässe in diesem Auftrag.
