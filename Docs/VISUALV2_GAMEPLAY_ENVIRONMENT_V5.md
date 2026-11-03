# VisualV2 Gameplay & Environment V5 – Prüfbericht

03.11.2026. Ausgangsstand `9b7b4a6d3e4e4bc5f6cfae04b23db1311aba2efd`, bestehendes `main`/`origin/main`. Bestehende VisualV2 weiterbearbeitet. **Technische Prüfung bestanden; die visuelle Abnahme bleibt Harry vorbehalten. Keine Übernahme nach Westland.** Die zusätzlichen Pflanzen kosten im gemessenen Rundgang Leistung; stabile 30 FPS werden ausdrücklich nicht behauptet.

## 1. Bestand und tatsächlicher Umfang

Die vorhandene Hauptfläche bleibt 90×65m groß. Statisches V4-Geländemesh, fünf bestehende Wegzüge, zwei funktionale Gebäude, abgesetzter Heilhausraum, Brücke/Bach und getrennter Teich. Alle neun Arbeitsabschnitte und 21 Vergleichspunkte wurden erneut kontrolliert. Keine neue Map, kein Worktree, keine Downloads. Ursprüngliche Gelände-, Gebäude-, Brücken- und Wassergeometrie bleiben erhalten.

Bestand: [InspectionBefore.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/InspectionBefore.json), [SceneBefore.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/SceneBefore.json), [Inventory.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Inventory.json). Der bestehende Git-/LFS-Stand ist der Wiederherstellungspunkt; keine neue Mapkopie oder zusätzliche Sicherung behauptet.

## 2. 2D-Platzhalter und beide NPCs

| Vorhandener Actor | Endgültige Darstellung | Erhaltene Funktion |
|---|---|---|
| `Slice_Waldhueterin_Liora`, XY −750/−600cm | Vorhandenes `DA_NPC_ElvenArcher`, 195cm, `SK_ElvenArcher_NPC_V1`, vorhandene Idle-/Begrüßungs-/Bewegungsdaten | `DA_SliceGuardian`, Traineridentität `Slice_Liora`, Vor-/Nachkampftexte, regulärer Trainerkampf |
| `Slice_Archivarin_Abzweig`, XY −1050/−1260cm | Vorhandenes `DA_NPC_ElvenScholar`, 195cm, `SK_ElvenScholar_Library`, vorhandene Idle-/Gesprächsdaten | `DA_SliceArchivistDialogue`, NPC-Identität, Quest-/Dialoginhalte und normale Interaktion |
| `Slice_Ruhepunkt` | Vorhandener schlanker 3D-Runenstein, 70cm hoch | Alter Heil-/Kontrollpunkt und seine Position/Kollision |
| `Slice_Ziel_Alter_Archivstein` | Derselbe vorhandene Stein, 100cm hoch | Ursprünglicher Quest-Actor, Identität, Position und Kollision |

Beide Figuren verwenden ausschließlich das vorhandene `PokeMonsterNPCVisualActor.ApplyPresentation` mit bestehenden validierten Bibliotheksprofilen. Keine neue NPC-/Dialogverwaltung, kein Rig-, Modell- oder Animationsumbau. Die eigenen Darstellungsactors hängen am ursprünglichen Interaktionsactor. Seine XY-Position und Rotation bleiben erhalten; die Kapselhöhe wird auf 97,5cm und die Quelle auf die tatsächliche Bodenhöhe plus halbe Figurenhöhe gesetzt. Keine schwebenden Füße. Die Darstellungsmeshes besitzen keine zweite Interaktionskollision.

Die zunächst zu breiten Ersatzbrocken wurden nach der Umrissprüfung verworfen. Finale Steinradien: 17,93/25,62cm innerhalb der unveränderten funktionalen Radien 48/45cm. Diese zwei bestehenden interaktiven Anker dürfen weiterhin an ihrer bisherigen Wegkante liegen; sie sind keine neuen dekorativen Sperren. [StonePolish.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/StonePolish.json).

Die zehn alten Wild-/Galerie-Spriteactors werden bereits vom bestehenden Habitat-System vor dem ersten Spielbild suspendiert. Sie wurden nicht als neue Arten reaktiviert oder gelöscht. Technische Editor-Billboards, UI, Effekte und sinnvolle Foliage-Cards bleiben erhalten. **Laufzeitaudit: keine sichtbaren aktiven PaperSprite-Platzhalter.** Ein vorhandener Sammelgegenstand südlich der Archivarin wurde beim ersten Test korrekt vor dem NPC ausgewählt; der freie westliche Zugang bestätigt ihren unveränderten Dialog. Lioras bestehender Trainerkampf wurde mit normalen Attacken-/Wechselaktionen bis zum Sieg gespielt.

## 3. Freie Wege und ganze Map

280 vorhandene Pflanzen-/Dekorinstanzen bzw. Komponenten von Wegflächen an geeignete Ränder versetzt: 210 im Hauptdurchgang, 70 zusätzlich aus den alten Heilhaus-Grasgruppen. Kein pauschales Löschen der Vegetation. Geprüft wurden `Main`, `Wild`, `VillageLoop`, `NorthLoop`, `Cottage` samt Zugangspads und Brückenzugängen. Die Clearance berücksichtigt transformierte Meshgröße, Skalierung und einen konservativen umschließenden XY-Radius; der Actor-Pivot allein genügt nicht.

Finale Audit: **13254 bodennahe Vegetationsumrisse, keine Überstände in die erfassten Wegflächen**, alle ursprünglichen Actors erhalten, WorldSettings unverändert, keine fehlenden direkten harten/weichen Map-Abhängigkeiten. Fensterpflanzen und entfernte technische Kollisionsproxies werden nicht als Weggras behandelt. Die tatsächliche Begehbarkeit mit Spielerkapsel, Begleiter und Kamera wurde zusätzlich im zusammenhängenden nativen Rundgang geprüft; eine rein geometrische Radiusprüfung wäre hierfür nicht ausreichend. [Audit.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Audit.json), [EntranceClearance.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/EntranceClearance.json).

| Abschnitt | V5-Bearbeitung / bewusste Erhaltung |
|---|---|
| SW | Zusammenhängende dichtere Blumenmischungen, westliches Wiesen-Buschfeld, kurze südliche Begrenzungsgruppen, freie Dorf-/Cottagewege |
| SC | Start-/Abzweigwege von störenden Pflanzen/Stümpfen befreit; Archivarin und funktionaler Ruhepunkt in 3D; übrige offene Spielräume erhalten |
| SE | Teich-/Wasserhabitat kontrolliert, ohne neue Blumen oder Sperren im Wasser; Garados und Unterwasserbereich unverändert |
| MW | Heilhauszugang und alte bodennahe Vorplatzgräser bereinigt, Garten-/Fensterpflanzen erhalten; lokaler Innenraumübergang verbessert |
| MC | Liora in 3D, freie Haupt-/Waldwege und Brückenzugänge; keine neuen Sperren auf der Brücke |
| ME | Schlanker Archivstein, kleinere gruppierte Randbegrenzungen, vorhandene Bach-/Ruinenzugänge und Ufer erhalten |
| NW | Gruppierte Wald-/Wiesenübergänge, begehbares Westwald-Buschfeld, kurze westliche Begrenzung abseits der Route |
| NC | Kleinere Blütengruppen, Buschfelder an Waldrand und nördlicher Lichtung; nördliche Rundroute bleibt frei |
| NE | Gruppierte Blumen am vorhandenen östlichen Waldrand, bestehende Baum-/Felsgruppen kontrolliert; keine pauschale Baumverdichtung |

## 4. Blumen und große Begrenzungsbüsche

**2.270 neue Blumeninstanzen** in fünf HISM-Gruppen: Blau457, Violett486, Rot679, Cremeweiß418, Gelb230. Natürliche Punktwolken in neun unterschiedlich großen Wiesen-/Randbereichen mit lokalen Farbschwerpunkten, Höhen24–43cm und gemischten vorhandenen Gräsern. Die Summe ist aus den tatsächlichen Gruppen gezählt; keine automatische Begegnungsfläche auf normalen Blumenwiesen.

19 große vorhandene StyleHex-3D-Büsche in kurzen unregelmäßigen Gruppen, ungefähr145–185cm hoch. Ein HISM für die Darstellung, je eine einfache passende Kapselkollision für diese großen Begrenzungspflanzen. Keine umlaufende Baum-/Buschwand und keine neuen Sperren an Wegen, Türen, NPCs oder Questzugängen. Der echte Kollisionsversuch stoppt vor dem Strauch; die kleinen Buschfeldpflanzen bleiben dagegen kollisionsfrei. Die übrige Wildbewegung verwendet weiterhin bestehende Bodenprojektion/Kollisions-Sweeps; kein neues Navigationssystem.

Vorhandene V3-Blumenmaterialvarianten und `SM_WLA_Wildflowers_A`, bestehende Sträucher `SM_Fol_Bush_1`, vorhandene Bibliotheks-NPCs und `SM_WLA_Runestone_A` werden wiederverwendet. Keine Fab-Originale, Mastermaterialien, Texturen oder Modelle geändert. Keine neuen Downloads oder Pokémon-Modelle.

## 5. Begehbare Buschfelder und gemeinsamer Encounter-Pfad

| Vorhandenes Habitat | Mittelpunkt XY (cm) | Halbausdehnung (cm) | Kleine Pflanzen |
|---|---|---|---|
| WestMeadow / Meadow | −4950 / −2100 | 300 / 220 | 54 |
| WestForest / Forest | −4880 / 1430 | 270 / 210 | 48 |
| ForestEdge / Edge | −2300 / 1400 | 160 / 160 | 16 |
| NorthGlade / Glade | −2250 / 2620 | 250 / 145 | 28 |

146 kleinere Sträucher in vier gemeinsamen HISM-Gruppen, etwa48–66cm hoch, ohne Pflanzenkollision. Je Feld **ein bestehender `PokeMonsterWildEncounterZone` mit explizitem Distanzmodus**, kein Gameplay-Actor pro Pflanze. Die Felder liegen vollständig innerhalb der tatsächlichen bestehenden Landhabitate und abseits normaler Wege/Haustüren. Ihre Trigger sind unsichtbar. Keine neue Berührungs-/Windanimation hinzugefügt: vorhandene Darstellung bleibt erhalten.

| Zentrale Einstellung | Standard |
|---|---|
| Aktivierung | an, nur ausdrücklich platzierte Buschfelder |
| Zufallschance | 18% pro gültigem Bewegungsschritt |
| Prüfdistanz | 250cm tatsächlich gelaufene XY-Strecke |
| Gemeinsamer Cooldown | 12s nach Start und erneut nach Ende eines regulären Kampfes |
| Zusätzliche Mindeststrecke | 800cm in gültigen Buschfeldern zwischen Begegnungen |
| Abtastung | 0,2s, nur solange der lokale Spieler im Feld ist |
| Teleport-/Ausreißergrenze | über500cm je Abtastung wird verworfen und neu verankert |
| Zulässige Habitattypen | Meadow, Edge, Forest, Glade |

Quelle: `Config/DefaultPokeMonsterBushEncounters.ini`; korrekt als einzelne Unreal-INI-Arrayeinträge. Bei Stillstand keine Prüfungen, höchstens eine Prüfung pro begrenzter Abtastung. Menüs, Dialoge, aktive Kämpfe, Laden, gesperrte Eingabe, Spiel-/Weltuhrpause und Gebäudeübergänge verhindern Begegnungen. Begleiter/NPCs sind keine lokalen Spieler und starten keine Feldprüfung. Keine dauerhaften zusätzlichen Actor-Ticks.

Die vorhandenen Habitatregeln, registrierten spielbereiten Arten und Encounterprofile wählen Art und Level. Die zentrale Weltuhr bestimmt Tagesphase und vorhandene Artgewichtung. Der Start erfolgt über `StartWildEncounter`/ClassicBattle mit Quellenactor der Zone. **Kein zusätzliches sichtbares Wild-Pokémon wird gespawnt; das globale Limit bleibt14.** Wiederholbare Zufallsbegegnungen speichern keine permanenten Abschluss-IDs. Die bisherige Einmal-Zone anderer Maps bleibt per Default unverändert.

Debug: `pm.BushEncounters.Enable -1` verwendet Konfiguration, `0` aus, `1` an. `pm.BushEncounters.Debug 1` protokolliert echte Würfe und Kampfbeginn; danach `0`. Keine Debuggeschwindigkeit oder Zufallszustände neu im SaveGame gespeichert. Einstellbare Seeds erlauben reproduzierbare Tests; ein neues Level/Spielprozess initialisiert diese Zonenfolge neu. Zeit-/Strecken-Cooldown ist Laufzeitzustand des bestehenden Welt-Subsystems.

**Echter Nachweis:** unveränderte Chance18%, nach 12 Prüfungen regulärer Raupy-Kampf im WestMeadow, anschließender normaler Fang mit isoliertem Testgegenstand, Team3→4 und Rückkehr zur Welt. Keine erzwungene100%-Chance, kein direkt gestarteter Ersatzkampf. Nach Kampfende verbleiben anfangs12s/800cm; weitere Bewegung während des Cooldowns startet keinen zweiten Kampf. Menü-/Dialog-/Stillstandssperren und große Buschcollision real geprüft. [NativeFeatures05](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeFeatures05/Result.json); [echter Zufallskampf mit Oberfläche](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeFeatures05/Tatsaechliche_Zufallsbegegnung.png).

## 6. Heilhaus: Übergang und vier sichtbare Wände

Der bestehende abgesetzte Raum bleibt erhalten: Außentür X−3550/Y500, Innentür X16400/Y500cm. **Nur sechs abgesetzte Frontwand-/Türbauteile aus der alten OccludingActors-Liste genommen.** Die18 bestehenden Wandactors der vier Wandgruppen bleiben sichtbar, Material-Fadewert0. Außen-Cutaway und übrige Gebäude bleiben erhalten; keine vier Wände werden ausgeblendet, um eine Kameraaufnahme zu ermöglichen.

Opt-in `StableDoorwayTransition`: Bewegung während der vorhandenen kurzen Schwarzblende räumlich halten, Richtungseingabe behalten, mindestens150cm auf der Zielseite landen, Bewegungsmodus und Geschwindigkeit anschließend korrekt freigeben. Verdeckter Übergang statt eines sichtbaren räumlichen Sprungs. Blockierte Ziele werden weiterhin geprüft und abgewiesen; auch dann wird die Bewegung freigegeben. Laden und EndPlay lösen den temporären Bewegungszustand auf. Die bestehende Save-Zugriffssperre deckt für diese opt-in Tür jetzt auch den gesamten Übergang ab.

Opt-in `ConstrainThirdPersonToRoom`: tatsächliche Kamera-XY innerhalb der vorhandenen Raumbegrenzung halten,85cm Randabstand. **Außen unverändert:** Third Person, tatsächliche bestätigte Höhe ca.1,72m, −12°,350cm, nur horizontaler Orbit. Lokale Begrenzung ändert weder Pitch/FOV noch Außeneinstellungen. Vier Innenraum-Blickrichtungen und die unveränderte Kamerakollision wurden geprüft. Dach-/Decken-Cutaway bleibt bestehen; der Raum erhält keine neue globale Kameraperspektive oder neue Beleuchtungsarchitektur.

Echter Ein-/Austritt bei `pm.Speed 1`, `2`, `3` bestanden, danach steuerbar. Heilung und bestehende Kontrollpunkt-/Speicherfunktion über den seitlichen freien Zugang um die unveränderte Theke geprüft. Ein anfänglicher Test versuchte direkt durch die Theke zu laufen und wurde korrekt blockiert; keine Möbelkollision dafür entfernt. Menü-Save/Load im Raum erhält Team/HP/PP, Inventar und Weltzeit exakt. Weltposition und Blickrichtung bleiben innerhalb0,001cm bzw.1e−6 normierter Richtung; eine erneute Normalisierung änderte im Test nur die letzte Nachkommastelle der Blickrichtung (≈1e−16), keine Spielinhalte. Vor der Heilung wurden AP durch einen echten Kampfzug verbraucht; danach wurden volle HP und AP ausdrücklich kontrolliert. Kein neues Speicherformat, keine Migration und keine Nutzerdatei überschrieben.

## 7. Echte Bilder und Vergleichbarkeit

Finale21 QHD-Paare: **BeforeAtlas → AfterAtlas03**, identische bestehende XY-/Yaw-/Auflösungs-/Mittagsfixierung, normale TP3, C75/High. Tatsächliche Kamera-/Spielerabweichungen werden pro Punkt in [Analysis.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Analysis.json) ausgegeben; Kollisionsverkürzung oder durch versetzte Objekte freier gewordene Sicht wird nicht als künstlich identische Kamera ausgegeben. Keine künstlichen Bilder und keine nachträgliche Aufhübschung. Vergleichstafeln ordnen nur die echten Aufnahmen an.

- [Gesamte finale 21-Punkte-Übersicht](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/WholeMapContactSheet.png)
- [Blumenwiese vorher/nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Comparisons/Suedwiese.png)
- [Westwald und Buschfeld vorher/nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Comparisons/Westwald.png)
- [Heilhauszugang vorher/nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Comparisons/HeilhausFront.png)
- [Start-/Abzweigwege vorher/nachher](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/Comparisons/Startwiese.png)
- NPCs: `BeforeDetails/Slice_Waldhueterin_Liora.png`, `BeforeDetails/Slice_Archivarin_Abzweig.png` → gleiche Ansichten in `AfterDetails01/`; zusätzliche besser einsehbare reale Ansichten in `NativeFeatures05/`.
- Heilhausinnenraum: `BeforeDetails/HeilhausInnen_0/90/180/270.png` → `AfterDetails01/`; zusätzliche Wand-/Kameraprüfung in `NativeFeatures05/Heilhaus_VierWaende_*.png`.
- [Großer Kollisionsbusch](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeFeatures05/Grosser_Kollisionsbusch.png), [kleines begehbares Feld](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeFeatures05/Begehbares_Buschfeld.png) und oben verlinkter tatsächlicher Zufallskampf.

Die ersten Versuchsserien, fehlerhafte Fixtures und Zwischen-Atlanten bleiben als Arbeitsnachweise in Saved erhalten, sind aber nicht der finale Qualitätsnachweis. Der frühe Kampfscreenshot ohne SHOWUI zeigte nur die Welt; der gültige native Nachweis verwendet den tatsächlichen UE-Screenshotmodus `Shot showui` und zeigt die Kampffläche samt Bedienoberfläche.

## 8. Gemessene Performance

Mac16,12 / AppleM4 /16GiB, macOS27.2 (26B123), UE5.8.4 CL58902052, Metal. Separater Development-Spielprozess, gleiche explizite Map, isolierter UserDir, `-nosound`, keine Videoaufnahme. Ausgabe2560×1440,75% (nominal1920×1080), High2, vorhandenes TAAU, Software-Lumen+IFG, VSM mit4Strahlen; Weltuhr120min, Mittag75°. Keine Rendering-/Grafikreduzierung. Frisch gestarteter Prozess bestätigt diese Profilwerte. Der globale AA-Fallbackwert allein wird nicht mit dem projektspezifisch aktiven TAAU-View-Pfad gleichgesetzt.

Frische V5-Vorherbasis und endgültiger Nachherstand: je drei6s-CSV-Fenster an sechs Hauptpunkten nach4s Beruhigung, zusätzlich drei Detailpunkte je ein Fenster. Weltzeit dabei auf12Uhr gehalten. Startwartezeit und Shader-/Assetladen vor Messbeginn; keine garantierte vollständige PSO-Vorwärmung behauptet. Zeitabhängige Drift und die natürliche Population13–14 begrenzen eine exakte Kausalaussage. VSync/FPS-Limit nur temporär0, anschließend zurückgesetzt. Fotos außerhalb der CSV-Messfenster.

| Messpunkt | FPS vorher | FPS nachher | GPU vorher ms | GPU nachher ms | p95 vorher ms | p95 nachher ms |
|---|---:|---:|---:|---:|---:|---:|
| Blumenwiese | 30.10 | 23.04 | 32.32 | 42.45 | 39.80 | 46.94 |
| Waldrand | 31.99 | 25.81 | 30.25 | 37.65 | 38.23 | 41.36 |
| Flussufer | 31.78 | 25.56 | 30.52 | 38.14 | 38.66 | 41.87 |
| Felsen | 35.80 | 29.39 | 17.11 | 20.73 | 33.12 | 38.43 |
| Dorf | 29.11 | 24.52 | 24.74 | 29.23 | 40.34 | 43.99 |
| Lebensraum | 32.70 | 28.19 | 29.25 | 34.32 | 36.52 | 40.72 |
| Kraeutergarten | 26.37 | 25.02 | 27.30 | 28.69 | 40.99 | 42.64 |
| Bachbett | 26.33 | 26.96 | 36.45 | 36.14 | 42.38 | 39.44 |
| Felsgruppe | 31.12 | 30.13 | 30.25 | 32.06 | 34.46 | 34.75 |

Zusammenhängender Bewegungslauf: gesamte42-Wegpunkt-Route mit echter Enhanced-Input-Eingabe und physikalischer Spielfigur, laufender Weltuhr, aktiver KI und Begleiter. Keine Platzierungsteleports innerhalb der Route. Messung endet vor Fotos, Dialogen, Kämpfen, Testgeländebesuchen und Save/Load. Ein Rundgang ist kein Langzeit-Stabilitätsnachweis.

| Bewegter Rundgang | früherer V4-Nachweis (historisch) | endgültiger V5-Lauf |
|---|---:|---:|
| FPS | 27.60 | 24.90 |
| Frame-p95 ms | 45.18 | 51.55 |
| 1-%-Low FPS | 16.95 | 10.13 |
| Größter Frame ms | 106.35 | 263.12 |
| GPU ms | 31.20 | 33.32 |
| Game Thread ms | 2.62 | 3.01 |
| Render Thread ms, inklusive möglicher Warteanteile | 36.20 | 40.10 |
| Base Pass ms | 7.14 | 7.82 |
| Shadow Depths ms | 3.90 | 4.19 |
| IFG ms | 2.58 | 2.84 |

Der erste native V5-Lauf vor der ergänzenden Versetzung der70 Vorplatz-Grasinstanzen maß25,72FPS/p9549,73ms. Der endgültige Lauf wird in der Tabelle vollständig einschließlich seiner Ausreißer ausgewiesen; keine Auswahl nur des besseren Ergebnisses. Eine Spitze von263,12ms trat im letzten Rundgang auf. Die parallel protokollierten GPU-/Thread-Zähler dieses Frames belegen allein keine eindeutige Ursache; ohne passenden Trace wird weder Lumen noch thermische Drosselung dafür verantwortlich gemacht.

**Der FPS-Verlust gegenüber dem früheren V4-Lauf wird nicht verschwiegen:** -9.79%. Der historische Lauf wurde in diesem Auftrag nicht erneut dynamisch vermessen; die zusätzliche frische statische Vorherbasis steht separat oben. Messdrift und veränderte Sicht-/Populationszustände verhindern, den gesamten Unterschied allein den Blumen oder der neuen Logik zuzuschreiben. Keine GPU-Passzeiten ungeprüft addiert; Render-Thread-Zeit wird nicht als reine CPU-Arbeitslast interpretiert. **Stabile30FPS nicht erreicht/nachgewiesen.** Die gewünschte höhere Dichte wurde nicht durch ein niedrigeres Renderingprofil kompensiert.

## 9. Technische und funktionale Tests

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | EditorBuild02 und final EditorBuild03 Exit0 |
| Vollständige Automation | 330/330 bestanden,0 fehlgeschlagen,0 mit Warnungen,0 nicht ausgeführt |
| Strenger QA-Exportvertrag | Finaler WrapperExit0, EngineExit0; vollständiger Reportexport |
| Zusätzliche Tests | Distanz/Stillstand/Pause/Teleport, zentrale Habitatprofile, geteilter Cooldown/Streckenbudget; Türbewegung/Speed1–3/Load; Raumkamera/blockiertes Türziel |
| Zwölf Map Checks | Alle12:0Fehler/0Warnungen, andere Maps nur geladen/geprüft und nicht gespeichert |
| Echte PIE-Tests | Neue NPCs, Archivarin, Liora-Trainerkampf, große Buschcollision, echte Zufallsbegegnung/Fang/Cooldown, vier Innenwandgruppen, Tür Speed1/2/3, Innenraum-Save/Load |
| Endgültiger nativer Gameplaylauf | Ganze42-Punkte-Route, Dorf/Wiese/Wald/Waldrand/Habitatübergänge, normale Bewegung/Sprint/Kamera, Brücke/Geländer/Cottage, Kampf/Attacke/Fang, Begleiter/Teamsortierung, Save/Load, echter Mapwechsel |
| Nativer Featurelauf | Neue Busch-/Sperrlogik, großer Strauch, echte Zufallsbegegnung+UI, Fang, Heilung, Wand-/Kamera-/Speedprüfung und exaktes Save/Load einschließlich Blickrichtung |
| Frischer letzter Spielstart | Gespeicherte NPC-/Busch-/Heilhausoptionen vorhanden; C75/TAAU/SW-Lumen/IFG/VSM4 und120min unverändert |
| Physisches Gamepad | Kein echter Hardware-Controllertest als bestanden behauptet; bestehende automatisierte Eingabetests und reale injizierte Enhanced-Input-Bewegung verwendet |

Maßgebliche Ergebnisse: [Build](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/EditorBuild03/Result.json), [330 Tests / strenger Wrapper](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/FullAutomationRelease/Result.json), [Map Checks](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/MapCheckResults.json), [finaler nativer Lauf](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeGameplay02/Result.json), [nativer Featurelauf](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/NativeFeatures05/Result.json), [PIE-Features](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/PIEFeatures08/Result.json), [Liora-Trainerkampf](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/PIETrainer01/Result.json), [frischer Start](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/FreshFinal01/Result.json).

Fehlversuche sind nicht als bestanden gezählt: erster Build mit zwei Compilerfehlern korrigiert; Automation01 mit einem Fehler der INI-Habitatarray-Syntax korrigiert, anschließend Automation02 und finaler vollständiger Release grün. Python-API-/Fixturefehler und die Theken-Blockade stehen in [RawLogReview.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/RawLogReview.json). Mehrere kontrollierte PIE-Starts/-Stops und alle eigenen nativen Prozesse wurden regulär beendet; kein Force Quit. Ein unbelegter allgemeiner Editor-Hang-Fix wird nicht behauptet.

### Externe und rohe Logmeldungen

Der strenge Wrapper bewertet den vorhandenen Projekt-Testexport. Rohlogs werden nicht als vollständig fehlerfrei bezeichnet. Engine-Python-Toolset-/TestRunner-Startmeldungen werden getrennt ausgewiesen. Im finalen Automation-Rohlog stehen17 Condition-Meldungen, alle vor Beginn der Projekt-Testqueue; der anschließende vollständige Projekt-Testexport enthält0 Fehler/0 Warnungstests. Die bekannte iOS-Helfermeldung trat in diesen finalen Logs nicht auf; eine Reparatur dieses externen Helfers wird nicht behauptet. Keine kritischen Absturz-/Assertionmeldungen in den final geprüften Läufen.

| Lauf | Externe iOS-Helferzeilen | Rohe Python-Fehlerzeilen | Eigene V5-Fixturefehler im finalen nativen Lauf |
|---|---:|---:|---:|
| NativeGameplay02 | 0 | 58 | 0 |
| NativeAfter02 | 0 | 58 | 0 |
| NativeFeatures05 | 0 | 58 | 0 |
| FreshFinal01 | 0 | 58 | 0 |
| FullAutomationRelease | 0 | 0 | 0 |

## 10. Projektschutz, Grenzen und Sicherung

SHA256-Vergleich: **6478 ursprüngliche versionierte/unversionierte Dateien**, 1757 lokale Original-/Fab-Assets und 733 vorher vorhandene Spielstände kontrolliert. Keine fehlenden Dateien, keine unerwarteten Änderungen. Nur die auftragsbezogene Map, die notwendigen vorhandenen C++-Erweiterungspunkte und Entscheidungen sind im bestehenden Bestand geändert. Neue eigene Konfiguration, Tests und Werkzeuge sind separat hinzugefügt. Westland/andere Maps, Pokémon-/Garados-Modelle/-Animationen, Dialog-/Questdaten, Originalmaterialien und Nutzerdateien unverändert.

Die vorbestehende lokale Änderung an `Config/DefaultEngine.ini` bleibt ausdrücklich erhalten, SHA256 `f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523`; sie wird nicht gestaged. Die34 geschützten vorherigen unversionierten Nutzerdateien bleiben lokal. Beide Vollbackup-Refs zeigen weiterhin auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Kein LFS-Prune, keine neuen Map-/Projektkopien. [ProtectionFinal.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/ProtectionFinal.json).

Offen bleiben Harrys visuelle Beurteilung, die bestehende stilisierte Vegetations-/Architekturqualität und die Performance unterhalb stabiler30FPS. Die Buschfelder sind bewusst begrenzte gemeinsame Triggerflächen; kein vollständiges Ökosystem, kein neues Schlaf-/Bewegungs-/Spawnmodell. Kein Kontaktbiegen kleiner Pflanzen oder neue Spezialanimation behauptet. Die zwei funktionalen Steinanker bleiben bewusst an ihrer bisherigen Position; ihre Darstellung ist jetzt schmaler als die bestehende Kollision. Fensterpflanzen/Editoricons/technische Folien bleiben absichtlich erhalten.

Die endgültige Map-SHA256 lautet `2402c3a261808627ccdc6eb6c30ea012535c47d89f7a107b379257afa1b094d7`. Eigener V5-Abschlusscommit enthält diesen Bericht und ausschließlich den geprüften Umfang; konkrete Commit-/Remote-/LFS-Verifikation steht anschließend in `Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5/GitFinal.json`/`RemoteLFS.json` und der Abschlussnachricht. Keine Kontrollmedien, lokalen Fab-Originale oder Nutzerspielstände werden gepusht. Nach Abschluss keine weitere Gestaltung und keine Übernahme nach Westland.
