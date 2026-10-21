# Kreaturen-Erweiterung V3 – Prüfbericht

Datum: 21.10.2026. Ausschließlich `/Users/harry/Developer/PokeMonster`, `main`. Ausgangspunkt `429861c5cd81409c711ecf52dadb6e798841bccc`. Bearbeitet wurde nur die vorhandene VisualV2; keine neue Map, kein Worktree, keine Projektkopie. Die sieben Arten sind technisch integriert und einzeln geprüft. Verbleibender Animationsfeinschliff und die visuelle Freigabe werden ausdrücklich getrennt von bestandenen Funktionstests behandelt.

## Tatsächlich integrierte Arten

Alle sieben Incoming-GLBs wurden anhand der importierten Geometrie und tatsächlicher Ansichten identifiziert. Alle waren ohne Skelett und ohne Animationen. Jeder besitzt drei eingebettete 2048×2048-JPEGs (Farbe, Normal, Metallic/Roughness). Originaldateien, Originaltopologie, UVs und Körperproportionen blieben erhalten. Ausschließlich gleichmäßige Maßstabsanpassung, anatomischer Ursprung und neue Gewichte/Rigs; keine Neugestaltung und keine Dezimierung. Myraplas cremefarbene Blätter und Nebulaks modellierte Gashülle entsprechen ausdrücklich den gelieferten Dateien.

| Art | Dex | Neutralhöhe | Dreiecke | Bones Blender / Unreal | Originalmaterialslots | Profil | Echte Flucht nach Sieg |
|---|---:|---:|---:|---:|---:|---|---|
| Pikachu | 025 | 40 cm | 137,094 | 21 / 22 | 1 | CURIOUS | 14.82 m / 56.64 s |
| Myrapla | 043 | 50 cm | 224,602 | 15 / 16 | 1 | CALM | 9.05 m / 47.43 s |
| Enton | 054 | 80 cm | 16,491 | 17 / 18 | 1 | SHY | 10.77 m / 29.13 s |
| Machomei | 068 | 160 cm | 21,708 | 22 / 23 | 1 | TERRITORIAL | 16.24 m / 26.24 s |
| Nebulak | 092 | 130 cm | 21,687 | 12 / 13 | 1 | SHY | 13.10 m / 29.48 s |
| Gengar | 094 | 150 cm | 21,695 | 18 / 19 | 1 | TERRITORIAL | 14.48 m / 30.55 s |
| Glurak | 006 | 170 cm | 246,066 | 24 / 25 | 2 | TERRITORIAL | 17.76 m / 33.48 s |

Unreal enthält einen zusätzlichen FBX-Armature-Root. Glurak erhält zusätzlich zum originalen Körpermaterial einen abgetrennten Slot für seine bereits modellierte Schwanzflamme, keine neue Flammengeometrie. Höhen gelten für das vollständige neutrale Originalmodell einschließlich Ohren/Blättern/Gashülle. Laufzeitakteure bleiben auf Maßstab 1. Die Spielfigur bleibt 140 cm.

## Dateien und Austauschpipeline

Für jede oben genannte Art `{Name}`:

- Original: `Art/Characters/Creatures/Incoming/{Name}.glb` – unveränderte SHA-256 im jeweiligen `MeshyV1_ModelAudit.json`.
- Gepackte editierbare Quelle: `Art/Characters/Creatures/{Name}/Source/{Name}_Meshy_V1.blend`, mit verborgener unmodifizierter High-Referenz.
- Originalbilder: `Art/Characters/Creatures/{Name}/Textures/MeshyV1/{Name}_{BaseColor,Normal,MetallicRoughness}.jpg`.
- Sieben FBX: `Art/Characters/Creatures/{Name}/Exports/MeshyV1/{Name}_{Idle,Walk,Run,Attack,Hit,Faint,Happy}.fbx`.
- Geometrie-/Rig- und Animationsdaten: `MeshyV1_ModelAudit.json`, `MeshyV1_AnimationAudit.json` im jeweiligen Artordner.
- Unreal: `/Game/Characters/Creatures/{Name}/MeshyV1`, darunter `Meshes/SK_{Name}_Meshy`, eigenes Skeleton, sieben `Animations/A_{Name}_{Role}`, Material, drei Texturen und `DA_{Name}_Presentation`.
- Gameplay: `/Game/Data/Creatures/DA_{Name}`, `/Game/Data/Encounters/DA_{Name}_Wild`.
- Wiederverwendbare und einmalige geschützte Werkzeuge: `Tools/CreatureExpansionV3/README.md`. Generatoren verweigern vorhandene Quellen standardmäßig; Import verweigert vorhandene Assetziele. Keine ungeprüfte Retarget-Übertragung vom Spieler.

Alle gepackten Quellen wurden erneut geöffnet und sämtliche 49 FBX tatsächlich separat reimportiert. UV-Identität, normalisierte Gewichte, Dreiecks- und Bonezahlen geprüft. Blender-Diagnoserenderings sind ausdrücklich keine Unreal-Abnahme.

## Rigging und Animationen

Sieben eigene 30-Hz-In-place-Clips je Art: Idle 2,0 s, Walk 0,6333 s, Run 0,4 s, Attack 0,8 s, Hit 0,4 s, Faint 1,2 s, Happy 1,0 s. Gemeinsamer vorhandener nativer Animationsblender verwendet die tatsächliche Bewegungsgeschwindigkeit. Nebulaks Walk/Run sind Schwebezyklen, keine Beine; kein neues Flug- oder Schwimmsystem.

Pikachu besitzt eigene Schwanzbones; Myrapla fünf Blattbones und eine starre runde Körper-/Kopfregion über kleinen Füßen; Machomei vier unabhängig animierte Armketten; Nebulak eine stabile Gesichtskugel und acht dezente Hüllenbones; Glurak separate Flügel- und Schwanzketten mit `flame_tip`. Gengars hinterer Ansatz ist vom Beingewicht getrennt. Aus der Gesamtbox abgeleitete falsche Körpermitten wurden bei Pikachu (X −7 cm) und Glurak (Y −25 cm) anatomisch korrigiert.

Automatische Bone-Heat-Gewichte gelangen bei Enton, Machomei und Gengar auf einer temporär verschweißten Hilfskopie; nur Gewichte wurden auf das unveränderte Original übertragen. Unvollständige Bone-Heat-Ergebnisse bei Pikachu/Myrapla wurden verworfen, durch anatomische Gewichtshüllen und topologische Glättung ersetzt. Keine ungewichteten Vertices als Erfolg akzeptiert.

Bei der Schlussprüfung wurde Myraplas Sohlenrand lokal neu an die vorhandenen Fußbones gebunden. Mesh, UVs, gepackte Bilder, Rest-Rig und sämtliche Action-Kurven sind vor/nach dieser Änderung hashidentisch; die neue Quelle wurde wieder geöffnet und alle Exporte erneut validiert. Walk/Run-Mindesthöhe verbessert von −1,16/−1,66 cm auf numerisch 0 cm. Entons Walk verbessert von −0,11 cm auf 0 cm; Run bleibt an einer Extrempose bei −1,23 cm. Weitere geringe Oberflächen-Minima: Pikachu Run −0,43 cm, Gengar −0,48 cm, Glurak −1,10 cm. Das sind tatsächliche deformierte Oberflächenwerte, nicht mit den wesentlich kleineren mathematischen IK-Fehlern zu verwechseln. Kein Anspruch auf endgültig perfekte Fußkontakte. Nebulaks animierte Hülle wird durch 12 cm Schwebeoffset über dem Boden gehalten.

Die zunächst geplante vollständige Neugenerierung wurde von der automatischen Freigabeprüfung wegen möglicher Überschreibung handbearbeiteter Actions/Gewichte abgelehnt. Stattdessen wurde nach Nachweis der Sitzungseigentümerschaft und exakter Quell-/Exportprüfsummen ausschließlich die oben beschriebene lokale Sohlengewichtsänderung ausgeführt. Ein lokales inverses Gewichtsdelta bleibt unter Saved; keine vollständige zusätzliche Sicherungskopie.

## Materialien und Flamme

Originale PBR-Bilder, sRGB nur für Farbe, Normal-Konvertierung sowie G/B-Kanäle für Roughness/Metallic wurden geprüft. Keine globalen Material-/Lichtänderungen. Gluraks ausschließlich am Schwanz vorhandene Originalflamme ist an den eigenen Flammenbone gewichtet und leicht emissiv (0,35); kein doppelter Feuer-Mesh, kein zusätzliches Licht und keine Flammen an Kopf/Rücken. Das ist ein sparsamer animierter Originalmesh-Effekt, keine behauptete Niagara-Flüssigfeuersimulation. Flügel und Nebulak-Hülle sind in beiden ClassicBattle-Perspektiven vollständig innerhalb der vorhandenen Bildkomposition.

## Daten und Kampfsystem

Eigene stabile IDs entsprechen den sieben Namen; bestehende Glumanda-ID `Zunderlauf`, Schiggy und Bisasam bleiben unverändert. Gen-2-Typen, Basiswerte, Fangraten und Wachstumsgruppen stammen aus den jeweils direkt in `Species.json` verlinkten [Serebii-Gen-2-Daten](https://www.serebii.net/pokedex-gs/025.shtml). Historische Basis-XP-Erträge beziehen sich auf Generation 1–4, nicht moderne Generationen.

Sechs neue vorhandensystem-kompatible Attackenassets: Ruckzuckhieb, Absorber, Nachtnebel, Geowurf, Silberblick, Flügelschlag. Verifizierte Gen-2-Werte: Ruckzuckhieb 40/100/30 AP, Priorität +1; Absorber 20/100/20 AP; Nachtnebel 100/15 AP und Geowurf 100/20 AP jeweils Schaden = Nutzerlevel unter Beachtung von Immunitäten; Silberblick 100/30 AP, Verteidigung −1; Flügelschlag 60/100/35 AP. Quellen u.a. [Absorber](https://www.serebii.net/attackdex-gs/absorb.shtml), [Nachtnebel](https://www.serebii.net/attackdex-gs/nightshade.shtml), [Geowurf](https://www.serebii.net/attackdex-gs/seismictoss.shtml), [Ruckzuckhieb](https://www.serebii.net/attackdex-gs/quickattack.shtml).

Kleine notwendige Erweiterung der vorhandenen Kampflogik: Absorber heilt die Hälfte tatsächlich entfernter KP (mindestens 1 bei Schaden), auch beim letzten KO-Treffer; Fixschaden wird weder durch Resistenzen noch Schwächen skaliert, Immunität bleibt erhalten. Regressionen prüfen begrenzte Ziel-KP, Heilmaximum, KO und PP. Kein paralleles Kampfsystem, keine Änderung der ClassicBattle-UI/-Kamera oder WorldBattle-Regeln.

**Lernlisten sind bewusst unvollständig.** Beispielsweise noch nicht implementierte Lähmung/Schlaf/Verwirrung werden nicht als wirkungslose endgültige Attacken angeboten. Entwicklungslevel 11/10/13/36/21/25/36, Habitate und unterstützte Ausschnitte sind keine finale Spielbalance. Keine erfundenen finalen Attackenwerte; vollständige Lerntabellen und Evolutionen bleiben außerhalb dieses Auftrags.

## Oberwelt und Kollision

Genau sieben neue sichtbare Einzelhabitate (`Dev_{Name}_Wild_V3`), GroupSize 1; vorhandene fünf Wildakteure bleiben erhalten. Je nach Entfernung nur lokale Aktivität, keine zusätzlichen Begleiter. Neugierig: Pikachu. Ruhig: Myrapla. Scheu: Enton und Nebulak. Territorial: Machomei, Gengar, Glurak. Entsprechend Herausforderung über die gemeinsame Interaktion beziehungsweise Kampf ausschließlich durch Körperkontakt; Begleiter bleibt ausgeschlossen.

Standorte in cm (Actorzentrum): Pikachu (−1450,100,20), Myrapla (−200,1250,25), Enton (1120,−900,40), Machomei (1350,200,80), Nebulak (−1500,−700,65), Gengar (−1600,650,75), Glurak (−1500,1200,85). Enton auf trockenem Flussrand, keine Wasser-/Brückenänderung. Gengar/Nebulak in bereits vorhandenen dunkleren Waldabschnitten; keine neu erfundene Ruine.

Der vorhandene artspezifische Navigationsradius wird für breite Flügel/Hüllen als Mindestabstand verwendet; physische Begegnungskapseln werden nicht künstlich vergrößert. Mehrere echte, durchgehend kollisions-/bodengeprüfte 2-m-Verbindungen pro Standort. Die dadurch zunächst blockierte Pikachu-Flucht wurde ursächlich behoben: nach tatsächlichem Kontakt darf der besiegte Akteur unter kontinuierlicher Prüfung der wirklichen Körperradien vom Spieler weggehen. Keine Kreuzung des Spielerkörpers, keine dauerhafte Kollisionsabschaltung, keine Durchquerung von Bäumen/Felsen und kein Teleport.

Der erste Pikachu-Nachweis blieb sicher sichtbar stehen (0 cm Laufstrecke); dies wurde nicht als Erfolg gewertet. Nach Korrektur bestanden alle sieben tatsächlichen Habitatbegegnungen: genau ein Kampf, richtige Initiierungsart, Begleiter pausiert, Sieg/XP, sichtbare Erholung/Flucht, erst außerhalb vollständiger visueller Bounds plus Sicherheitsrand entfernt, kein erneuter Kampf und kein unmittelbarer Respawn. Obige Fluchtzeiten sind Spielzeit, keine FPS-Messung. Für winzige Arten gilt artspezifisches Lauftempo statt pauschal erzwungener 75 cm/s. Die Starter bewegen sich weiterhin unverändert.

## Tatsächliche Nachweise und Testbedingungen

Einzelreviews `{Name}UnrealQA`: nativer Animationsblender, tatsächliches Enhanced-Input-Laufen/Sprinten mit einem Begleiter, Idle und Reaktionen, beide ClassicBattle-Seiten, Angriff und Rückkehr. Diese kontrollierte Präsentationsfixture setzt andere Habitat- und Gebietstrigger nur in PIE aus; sie ist kein freier natürlicher Habitatnachweis. Die gesonderten `{Name}Wild01` beziehungsweise `PikachuWild03` verwenden den wirklichen ausgewählten Mapakteur und sein Produktionsprofil, volle Gegner-KP, die gemeinsame Eingabe und den vorhandenen Kampfabschluss. Anfangsposition und kanonisches Level-36-Team sind offen ausgewiesene Testfixtures; keine Produktionswerte wurden dafür verändert.

Fang-/Team-/Heil-/Save-Runde `ExpansionCapture02`: sieben Arten, bestehende Wechsel-, Beutel-, Ballverbrauch-, Teamtransfer-, Heil- und Save/Load-Flows bestanden. Explizite Fixture: über bestehende Progression berechnete Level-100-Reserve, Gegner 1 KP, Seed 51; keine Aussage über Fangbalance. Der erste Lauf scheiterte nur an acht für diese große Reserve unzureichenden Heilitem-Testwiederholungen; zweiter Lauf mit vollständiger Heilung bestanden. Zusätzliche abschließende Quellakteurprüfung und Regressionen werden unten festgehalten.

Jeder schreibende Lauf erhält den ursprünglichen Dev-Spielstand kontrolliert zurück. Ausgangs-SHA-256: `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`. Keine unbelegte physische Switch-Pro-Controller-Abnahme.

## Echte Aufnahmen

Lokale Nachweise unter `Saved/CreatureExpansionV3` (absichtlich nicht GitHub): für jede Art `{Name}UnrealQA/{Name}_World_{4,8,12,16}_QHD00000.png` mit verifizierten **2560×1440** und 100 % Screen Percentage; `{Name}_Battle_0.png` / `_Battle_1.png` sind Exporte des vorhandenen **2560×1080**-Kampf-RenderTargets und ausdrücklich keine 16:9-QHD-Aufnahme. UI-Aufnahmen unter `Saved/GlumandaV11/LiveUI/Expansion_{Name}UnrealQA_{0,1}` haben ihre eigene tatsächliche Slate-Viewportgröße. Zeitlich geordnete Kontakt-/Fluchtbildfolgen in den jeweiligen Wild-Prüfordnern; kein erfolgreiches Video behauptet. Kontrollierte Szenen sind als solche ausgewiesen, keine generierten Konzeptbilder.

## Schutz und bekannte Grenzen

155 Starterdateien, alle 58 vorgefundenen unversionierten Dateien und die zehn anderen Maps wurden separat per SHA-256 gegen den Anfangszustand geprüft. Die sieben nun benötigten unveränderten Incoming-Originale werden gezielt aufgenommen; die übrigen 51 vorgefundenen Dateien bleiben unverändert unversioniert. Snapshot aller 1448 vorbestehenden Mapakteure bestätigt unveränderte Transforms, Mesh-/Materialzuweisungen, Instanzen, Licht- und Kollisionswerte. Kein Heilhaus-/Terrain-/Vegetations-/Beleuchtungsumbau. Vollbackup `03492bd` bleibt unter beiden bestehenden lokalen Ref-Pfaden unverändert und ist kein main-Vorfahr.

Die gelieferten Pikachu-/Myrapla-/Glurak-Meshes sind polygonreich und besitzen hier nur Original-LOD0; keine heimliche Vereinfachung, keine erfundene Performanceverbesserung, keine umfangreichen Benchmarks. Gengar hat bereits im Original kleine dunkle Dreiecksbereiche an Hand-/Armregionen; nicht durch eigenmächtige Neugestaltung kaschiert. Kein echtes volumetrisches Gas bei Nebulak, kein fertiger Flug bei Glurak. Acht Bewegungsrichtungen werden vom bestehenden System unterstützt, aber eine lückenlose Einzelbildabnahme aller sieben Arten in allen acht Richtungen ist noch nicht belegt. Kurze Clips und Randdeformationen bleiben Kandidaten für gezielten Animationsfeinschliff. Technisch integrierbar bedeutet keine automatische endgültige visuelle Freigabe.

## Abschlussprüfungen und GitHub

Siehe nachfolgenden, nach tatsächlichen Ergebnissen ergänzten Abschlussabschnitt. Zwischencommit `f0b73f175c686cbf2c29b2bda3d2af4a28a24b1a` (Drain/Fixschaden und Regressionen) ist regulär auf origin/main verifiziert; keine neuen LFS-Objekte in diesem Commit.


### Abschließende Regressionen

| Prüfung | Tatsächliches Ergebnis | Lokaler Nachweis |
|---|---|---|
| Mac Development Editor, nach letztem Begleiterfix | bestanden, Exit 0, 40,72 s | `Saved/ProjectRefinement/CreatureExpansionV3RoomFixBuild/Result.json` |
| Erzwungener Unity-Build | bestanden, Exit 0, 14,32 s | `Saved/OverworldAIV2/CreatureExpansionV3RoomFixUnity/Result.json` |
| Vollständige PokeMonster-Automation | **91/91**, 0 Warnungen, 0 Fehler, 0 ausgelassen, 32,88 s | `Saved/ProjectRefinement/CreatureExpansionV3ReleaseAutomation/Result.json` |
| Alle vorhandenen Map Checks | **11/11**, jeweils 0 Fehler / 0 Warnungen | `Saved/CreatureExpansionV3/MapChecks.json` |
| Vollständiger Enhanced-Input-PIE-Fußlauf | **bestanden**, 289,10 m, Sprint 315 cm/s, 103 Schritte, keine Testteleports | `Saved/GlumandaV11/Acceptance/CreatureExpansionV3Foot04/FootTest.json` |
| Begleiter im vollständigen Fußlauf | 642 Stichproben, 40 während Kampf verborgen, 41 Innenraumstichproben ohne Schlagschatten, 0 Probleme | `CompanionResult.json` im selben Ordner |
| Niederlage, Heilpunkt-Rückkehr, Autosave und Reload | bestanden, Rückkehrposition identisch, volle KP/gleiche IDs/XP, Speichern im laufenden Kampf gesperrt | `Saved/StarterExpansionV1/CreatureExpansionV3Defeat01/Result.json` |
| Bestehender WorldBattle-Abschluss | bestanden; keine ClassicBattle-Fluchtregel auf Sonderkampf übertragen | `Saved/WildEncountersV2/CreatureExpansionV3World01/Result.json` |

Der Fußlauf prüfte Wanderer-Dialog/Quest, Liora, Fang, Brücke, Archiv, Save/Load, Questabschluss, Heilhaus betreten/verlassen, Heilen/Speichern, Innen-/Außenkamera, Möbelwege, Kronenfreistellung, acht **Spieler**-Laufrichtungen und Sprint. Das kanonische Glurak/Machomei/Zunderlauf-Entwicklungsteam ist eine ausdrückliche Laufzeitfixture. Sämtliche neuen Habitate blieben aktiv. Die acht Spielerrichtungen sind keine nachträgliche Behauptung einer vollständigen Acht-Richtungs-Einzelbildabnahme jedes Pokémon. Der Begleiter-Beobachter zählt auch verborgene versetzte Innenraumübergänge; sein Roh-Maximalabstand von etwa 205,6 m enthält den 200-m-Raumversatz und ist kein behaupteter normaler sichtbarer Folgeabstand.

Frühere Fußläufe bleiben nachvollziehbar: Foot01 wurde an einem wirklich gestarteten Gengar-Kontaktkampf gestoppt, den die alte Weg-Fixture nicht behandelte. Foot02 zeigte eine zu breite neue Test-Abfangbedingung beim regulären Liora-Kampf; sie wurde auf zusätzliche Wegkontakte begrenzt. Foot03 zeigte ein ungeeignetes Kampfverhalten des Testautomaten sowie den tatsächlichen Begleiter-Lichtkanalfehler beim Türübergang. Zusätzliche Wegkämpfe behandelt die neue Fixture über die vorhandene Fluchtaktion. Foot04 bestand die ursprüngliche vollständige Wegstrecke; keine Pokémon wurden dafür aus der Map entfernt oder ihre KI abgeschaltet.

**Behobener Begleiterfehler:** Wenn der Spieler die versetzte Innenraumgrenze verlassen hatte, übernahm der noch drinnen stehende große Glurak dessen Außenlicht-/Schattenstatus. Jetzt prüft der Begleiter seine eigene tatsächliche Raumzugehörigkeit über die bereits vorhandenen gecachten Raumgrenzen. Nur seine Visual-Lichtkanäle und sein lokaler Schattenstatus wechseln entsprechend der bestehenden Konvention. Keine Änderung an Heilhaus, Lichtquellen, Welt-Schatten, Kamera, Starterquellen oder Saveformat. Der erneut gelaufene Editor-/Unity-Build, alle 91 Tests und der vollständige Begleiter-Fußlauf beziehen diesen Fix ein.

### Nicht unterdrückte Umgebungswarnungen

Im Editor04-Startprotokoll stehen vor dem Mapladen 17 `LogAutomationTest: Error: Condition failed` im zeitlichen Umfeld der installierten Engine-`UE::UnifiedErrorTest`-Selbsttests. Die genaue Zuordnung jeder einzelnen Startassertion ist nicht abschließend geklärt; diese Meldungen werden weder entfernt noch als bestandene Projekttests umgedeutet. Die separat exportierte **PokeMonster**-Automation meldet nach tatsächlichem Durchlauf 91/91 ohne Warnungen/Fehler.

Außerdem vorhanden: macOS-`idevice_id`-Hilfsprogramm mit „Bad CPU type“ und bestehende World-Materialwarnungen für `MI_WLA_LeafOak` und `MI_WLA_Stone` wegen fehlendem `InstancedStaticMeshes`-Usageflag (möglicher Defaultmaterial-Fallback). Diese betreffen unveränderte bestehende Umweltmateriale; keine unerlaubte Landschafts-/Materialkorrektur in diesem Auftrag. Die sieben neuen Kreaturenmateriale wurden tatsächlich in PIE gerendert. Map-Check-Zähler sind davon getrennt und überall 0/0.

### Empfehlung

Alle sieben Arten sind als zusätzliche technische Entwicklungsintegration verwendbar: eigene Quellen/Rigs/Clips, passende Größen, bestehende Kampf-/Fang-/Team-/Heil-/Speicherflüsse und echte Habitatflucht. Die gelieferten Modelle sind visuell maßgeblich. Vor endgültiger Animationsfreigabe gezielt Fußrand- und Extremposenfeinschliff, lückenlose Acht-Richtungs-Ansichten und die dokumentierten ursprünglichen Gengar-Oberflächen prüfen. Glurak-Flug, echtes volumetrisches Gas, vollständige Attackenlernlisten und LOD-Optimierung bleiben bewusst offen. Physischer Switch-Pro-Test ebenfalls offen. Keine weiteren Kreaturen oder Welt-Art-Pässe begonnen.


### Fang-Persistenz und abschließender Dateischutz

`Saved/CreatureExpansionV3/ExpansionCapture04/Result.json` prüft alle sieben Fälle nochmals mit der **tatsächlichen stabilen Encounter-ID** des jeweiligen Habitatakteurs. Alle sieben bestanden: Fang/Teamtransfer, korrekter Ballverbrauch, Teamwechsel, volle Heilung, gleiche IDs/KP/XP nach Save/Load, Quellakteur ohne Flucht entfernt und **auch nach Reload weiterhin entfernt**. Die kanonische Level-100-/1-KP-Fixture bleibt explizit ausgewiesen und verändert keine Speziesassets. Fangversuche: Pikachu 1, Myrapla 1, Enton 1, Machomei 9, Nebulak 1, Gengar 9, Glurak 9.

`Saved/CreatureExpansionV3/FinalSafety.json`: alle 58 vorgefundenen unversionierten Dateien bytegleich, alle 155 Starterdateien bytegleich, alle zehn anderen Mapdateien bytegleich, ursprünglicher Dev-Spielstand per SHA-256 restauriert, beide Vollbackup-Refs unverändert, genau ein Worktree im aktiven Projekt. Editor nach allen Prüfungen in VisualV2 ohne PIE und ohne schmutzige Pakete. Der Schutz umfasst auch die bereits vorhandene unversionierte Testmap.

Alle aktuellen sieben gepackten Quellen und ihre jeweils sieben FBX stimmen exakt mit ihren erneuten Reopen-/Roundtrip-Prüfsummen überein. Aktuelle Nachweise: `PikachuValidationFinal`, `MyraplaSoleValidation`, `EntonSoleValidation`, `MachomeiValidationFinal`, `NebulakValidationFinal`, `GengarValidationCorrected`, `GlurakValidationFinal` unter Saved/CreatureExpansionV3. Nach den lokalen Sohlenkorrekturen zusätzlich echte native Reviews `MyraplaSoleUnreal` und `EntonSoleUnreal` bestanden.

### Bilder zur lokalen visuellen Abnahme

Die lokale Übersicht `Saved/CreatureExpansionV3/SiebenArten_UnrealUebersicht.jpg` montiert ausschließlich echte native Kampfaufnahmen, verkleinert und beschriftet. Originale bleiben daneben erhalten; kein Konzeptbild und keine behauptete neue Kampfkamera. Für jede Art liegen die Welt-, Front-/Rück-Kampf- und Kontakt-/Fluchtsequenzen an den oben dokumentierten Stellen. Keine dieser Kontrollmedien wird hochgeladen.

### Sicherungsumfang

Gezielt geprüfte Quellen, Originalbilder, FBX, Unreal-Assets, die vorhandene VisualV2 mit sieben neuen Einzelhabitaten, kleine notwendige Code-/Teständerungen sowie Dokumentation. Keine Caches, Kontrollbilder, Videos, gespeicherten Teststände oder temporären Renderings im Index. `.gitattributes` ergänzt nur die benötigten 21 Original-JPEG-Texturen der sieben neuen Arten; `.gitignore` ergänzt den lokalen Bytecodeordner der neuen Werkzeuge und die einzeln identifizierte, erst in dieser Sitzung neu erzeugte `AutomaticSkin.cpython-313.pyc` des bestehenden Skin-Helfers. Diese Cachedatei wurde bei der Indexprüfung zusätzlich erkannt, nicht gestaged und nicht gelöscht; sämtliche vorbestehenden Dateien bleiben unverändert. Die übrigen 51 vorgefundenen unversionierten Dateien bleiben unverändert außerhalb der Commits.

GitHub-Grenzen wurden anhand der [normalen Git-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) und [LFS-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) geprüft. LFS und normale Git-Daten getrennt: neue LFS-Nutzdaten ungefähr 0,546 GiB, normale geplante Dateiinhalte nur wenige MiB, jede normale Datei deutlich unter 100 MiB und jeder LFS-Einzelinhalt unter 2 GB. Die endgültige Indexliste und exakten Bytes werden vor Commit lokal nachgerechnet. Keine kostenpflichtige Aktion, Budgetänderung oder Quota-Änderung. Live-Abrechnungsdaten sind nicht über diesen Git-Zugang abrufbar; gespeicherte Quoten werden nicht als aktuelle Messung ausgegeben. Bei Quota-/Transportfehler wird ohne Wiederholungsupload gestoppt.
