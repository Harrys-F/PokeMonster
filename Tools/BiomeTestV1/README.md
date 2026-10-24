# Biome-Testmap V1 – Werkzeughinweise zur visuellen Prüfung

Nicht verbindliche Arbeitsbeschreibung; TECHNIK, ENTSCHEIDUNGEN und Grafikfreigaben bleiben unverändert.

## Im Editor spielen

1. Das vorhandene `/Users/harry/Developer/PokeMonster/PokeMonster.uproject` mit UE 5.8.2 öffnen.
2. Im Content Browser `/Game/Maps/Dev_BiomeTestMap_V1` öffnen.
3. **Play / Selected Viewport** mit normalem PlayerStart verwenden. Keine Automation oder Konsolenaktivierung nötig.
4. Mit den bisherigen Bewegungseingaben laufen; Shift halten oder die bestehende L3-Sprintumschaltung verwenden.

Die 1,40-m-Spielfigur, 2,5D-Kamera (FOV35, Arm2850cm, Pitch−50°, Yaw−45°), Geschwindigkeiten und Eingabebelegung stammen unverändert aus dem aktuellen Character.

Vom beschrifteten Zentrum aus, bezogen auf die Spielkamera:

- **Links oben:** Wiese / Waldrand mit Bisasam70cm, Pikachu40cm und separater freier Glurak170cm-Fluglichtung.
- **Rechts oben:** Bach / Teich, westliches flaches Ufer mit Schiggy50cm und Enton80cm; weiter oben eine Holzbrücke.
- **Links unten:** Felsbereich. Am Abzweig den nach links führenden Hang hinauf auf die tatsächliche 3-m-Plattform zu Machomei160cm. Der untere Weg führt in den offenen Höhlenschnitt zu Glutexo110cm.
- **Rechts unten:** dichter Wald mit Nebulak130cm; der Weg führt weiter zur begehbaren offenen Ruine mit Gengar150cm.

Neun echte Pokémon-Exemplare plus ein grüner, ausdrücklich beschrifteter Wasser-Prüfkörper. Keine künstliche Skalierung. Alle sind ausschließlich visuelle, nicht fangbare Testinstanzen. Goldini fehlt im Projekt; der Marker ist **kein** Goldini-Modell.

## Abgrenzung

Nur diese Map verwendet `PokeMonsterBiomeTestGameMode`. Kämpfe und normaler Save/Load/Delete sind hier gesperrt, der Begleiter ist deaktiviert, und es werden keine Teaminstanzen angelegt. Keine NPCs, Dialoge, Fortschritts-UI oder regulären Begegnungsactoren werden platziert. Nach PIE-Ende existieren die Testinstanzen nicht mehr; beim nächsten normalen Play werden sie aus den **gespeicherten** Habitatdefinitionen neu erzeugt.

Bestehende Maps behalten ihren bisherigen GameMode und alle Systeme. Der neue Habitat-Verweis in der gemeinsamen Bewegungs-Komponente ist dort null. Medienparameter und Auftrieb werden nur für ausdrücklich zugewiesene Biome-Habitate aktiviert.

## Medien und Grenzen

- Land: Bodenprojektion, trockene Ziele, native Wegsuche und Kollisionsprüfungen.
- Amphibisch: flache Ufer, kontinuierlicher Übergang zu artspezifischer Eintauchtiefe (Schiggy23cm, Enton35cm).
- Rein Wasser: Prüfkörper bleibt innerhalb eines Wasserbereichs mit ausreichender Tiefe; keine Landziele.
- **Wasseranimation ist ein Prototyp:** vorhandene Idle-Pose, unterdrückter Landgang und dezenter Auftrieb. Keine fertig erstellte Schwimmanimation, kein Unterwassersystem.
- Glurak: vorhandene Takeoff-/Hover-/Land-Animationen; begrenztes bodennahes Schweben zwischen sicheren Punkten, 0,5–1,5m. Kein freier 3D-Flug und kein Reiten.
- Nebulak: geländebezogener Schwebekörper45cm plus vorhandenes kleines organisches Schweben. Keine Flügelanimation erforderlich.
- Kein geeigneter fliegender Höhlenbewohner vorhanden; Glutexo läuft im offenen Höhlenschnitt. Keine fertige Höhlenflug-Demonstration.
- Entfernte Instanzen pausieren ab38m und laufen nach Wiederannäherung ohne Neuspawn oder Teleport weiter.

Höhle und Ruine sind bewusst oben und zur Kamera hin offen. Bäume nutzen die bestehenden Kamera-Freistellungsmaterialien. Tieferes Wasser ist für die Spielfigur blockiert; das ist keine unsichtbare allgemeine Wegsperre, sondern die Grenze des ausdrücklich nicht implementierten Spieler-Schwimmsystems. Die Brücke verbindet beide Ufer.

## Werkzeuge / Wiederholbarkeit

`Layout.py`: Koordinaten in cm; u nach Bildschirmrechts, v nach Bildschirmoben. Welt `(x,y)=((u+v)/sqrt(2),(u−v)/sqrt(2))`. Je Biom ca44m, gesamtes Gelände104×104m.

`BuildTerrain.py`: neuer Blender-Höhenquellstand / FBX. Vor dem Export wird Blender-Y für die Unreal-FBX-Konvertierung kompensiert. Standardmäßig wird eine vorhandene Quelle nicht überschrieben; `--replace-owned-biome-v1` ist ausschließlich für diese neue eigene Quelle vorgesehen.

`PrepareAssets.py` und `CreateMap.py` sind **einmalige Autorenwerkzeuge**, keine bei jedem Start benötigten Skripte. `CreateMap.py` verweigert eine bereits vorhandene Zielmap. `IsolateMaterials.py` dokumentiert die einmalige Umstellung auf private Instancing-Materialkopien; nicht erneut blind ausführen. `ReimportTerrain.py` ist strikt auf die beiden neuen Gelände-/Wassermeshes begrenzt.

`RunWalkReview.py LABEL [--no-sequence]` verwendet eine bereits laufende autorisierte ArtControl-Editorsitzung und einen **normalen PIE-Start**, danach echte Enhanced-Input-Aktionen und unveränderte Kollisionen. Es teleportiert die Spielfigur nicht. Neue Ergebnisverzeichnisse müssen eindeutig sein; alte Nachweise werden nicht überschrieben. Das ist eine softwaregesteuerte Begehung und kein Hardware-Controller-Test.

`RefineSightAndCave.py`: einmalige maplokale Korrektur von Höhlenkollision und Beobachtungslichtung. Alle103 Bäume bleiben erhalten.

`MapChecks.py`: lesende Prüfung aller12 Maps, keine Saves.

`Overview.py`: vorübergehende Unreal-SceneCapture-Übersicht, ausdrücklich **keine** Aufnahme der normalen Spielkamera. Die biomeweisen QHD-Aufnahmen im Prüfbericht stammen aus der unveränderten echten Spielkamera.

Lokale Bild-/Videonachweise und der ursprüngliche Abnahmebericht liegen unter `Saved/BiomeTestV1/`. Keine Kontrollmedien versionieren. Der textbasierte dauerhafte Prüfbericht liegt unter `Docs/BIOM_TESTMAP_V1_PRUEFBERICHT.md`. Die ursprüngliche Erstellung vom 23.10.2026 umfasste keinen Commit/Push; der ausdrückliche Sicherungsauftrag vom 24.10.2026 erlaubt die gezielte Versionierung dieses geprüften Pakets. Die visuelle Abnahme bleibt davon unabhängig.

Versioniert sind die 16 hier ausgewählten Autoren-, Audit-, Begehungs- und Anleitungsdateien. Einmalige lokale Diagnose-/Sitzungshelfer und der historische Berichtsgenerator sind kein Laufzeitbedarf; sie bleiben lokal erhalten. Insbesondere werden die vorhandenen Generatoren bei der Git-Sicherung nicht erneut ausgeführt und keine bestehenden Maps erneut gespeichert.
