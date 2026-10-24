# Biom-Testmap V1.1 – Prüfbericht

Stand: 24.10.2026. Ausgangscommit `11a1b9ef`. Ziel ist ausschließlich die bestehende `/Game/Maps/Dev_BiomeTestMap_V1`. **Zwischenstand: Wasser sowie Plateau/Höhle geprüft; fünf weitere Pokémon, Ruine und Waldkamera folgen. Keine Gesamtfreigabe V1.1.**

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

Fünf Wiesen-/Flug-Pokémon, Ruine und dichte Waldkamera sind in diesem Zwischenstand noch nicht umgesetzt. Der bestehende V1-Stand ist dort keine V1.1-Abnahme. Gesamttests und abschließende Vorher-/Nachherbewertung folgen erst nach Umsetzung.

## 5. Integrität und Git

Die Baseline erfasst Hashes von 3190 Originaldateien und allen 38 vorgefundenen unversionierten Dateien. Bisher ausschließlich sieben erlaubte Originaldateien (Biom-Terrainquellen, zwei Terrainassets und Biom-Map) geändert; alle 38 ursprünglichen unversionierten Dateien bytegleich. VisualV2, bestehende Pokémonquellen, Spielstände und Vollbackup-Verweise unverändert. Keine neuen Maps/Projektkopien/Worktrees/Backups. Keine Performance-Benchmarkreihe.

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
