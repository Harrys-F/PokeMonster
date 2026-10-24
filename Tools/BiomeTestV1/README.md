# Biom-Testmap V1.1 – Zugang und Prüfwerkzeuge

Projekt ausschließlich `/Users/harry/Developer/PokeMonster`, Unreal 5.8.2. Vorhandene Map `/Game/Maps/Dev_BiomeTestMap_V1`, keine zusätzliche Map. Der historische V1-Stand mit 3-m-Plattform und Wasserprüfkörper ist durch V1.1 ersetzt; historische Resultate bleiben in `Docs/BIOM_TESTMAP_V1_PRUEFBERICHT.md` erhalten.

## Normal im Editor spielen

1. `PokeMonster.uproject` öffnen.
2. Im Content Browser `Dev_BiomeTestMap_V1` öffnen.
3. Gewöhnlich **Play / Selected Viewport** verwenden. Keine Automation, Konsolenaktivierung oder Setup-Skripte notwendig.
4. Vorhandene Bewegungs-/Sprintsteuerung verwenden. Keine neue Controllerbelegung.

15 gespeicherte Habitat-Actors erzeugen 16 reine Testexemplare. Beim PIE-Ende verschwinden die Laufzeitexemplare; beim nächsten normalen Play entstehen sie aus den gespeicherten Definitionen erneut. Dies ist unabhängig vom Pokémon-Testgelände in VisualV2.

Vom beschrifteten Hub aus, bezogen auf die Spielkamera:

- **Links oben:** Wiese mit Bisasam/Pikachu, Glurak-Fluglichtung sowie Raupy/Hornliu am Boden, Smettbo/Bibor in begrenzten Flugbereichen und Habitak mit Abheben/Flug/Landen. Weitere 685 unregelmäßig gruppierte Botanikinstanzen.
- **Rechts oben:** Schiggy/Enton am Ufer, Karpador und Garados im ausreichend tiefen Teich; Steg und Brücke begehbar. Schiggy verwendet hier ein eigenes Schwimmprofil. Kein Goldini-Ersatzmarker mehr.
- **Links unten:** 15-m-Plateau zu Machomei über einen langen Kehrenweg ab UV ungefähr (−900,−1000). Höhlenzugang über die östliche Basis nach Süden um den Berg, UV (−2900,−3450). Bestehender maskierter BuildingCutaway-Übergang in denselben Map-Raum bei Welt (25000,0,150), mit Glutexo. Rückweg durch denselben Eingang.
- **Rechts unten:** Nebulak im Wald, dichter Wald mit lokaler Kamera, begehbare alte Ruine mit Gengar, Steinbogen, Säulenresten, Pflaster, Schutt und Bewuchs.

Originalgrößen bleiben erhalten, etwa Raupy/Hornliu/Habitak je30 cm und Garados650 cm entlang der Körperachse statt650 cm vertikaler Höhe. Die Spielfigur bleibt140 cm groß.

## Kamera und Wasser

Standard: FOV35°, Arm2850 cm, Pitch−50°, Yaw−45°. Nur der Actor `Biome_DenseForestCamera_V11` aktiviert1700 cm in einer dichten Waldzone, Mitte UV (3200,−1700), Halbausdehnung (1050,650,600) cm. Übergang0,8 s, weicher Rand180 cm. Sein `bEnabled`-Schalter deaktiviert die lokale Variante rücknehmbar. Die normalen Sichtkegelradien bleiben110/220 cm. Zusätzliche Freistellung betrifft nur obere Kronen vorbereiteter privater Baum-Materialvarianten; Stämme/Unterholz und ursprünglicher Schatteneingang bleiben.

Tieferes Wasser ist für die Spielfigur blockiert; Steg und Brücke erlauben Beobachtung/Überquerung. Kein Spieler-Unterwassersystem. Fische bleiben im Schwimmbereich; Schiggy wechselt zwischen Ufer und Wasser. Smettbo/Bibor fliegen auf begrenzten Höhenebenen; Habitak nutzt vorhandenes GroundHover und darf im ausdrücklich freigegebenen Flugsegment niedrige Hindernisse überqueren. Kein universelles freies3D-Flug- oder Reitsystem.

## Gameplay- und Spielstandschutz

Nur diese Testmap verwendet `PokeMonsterBiomeTestGameMode`. Normale Testtiere erzeugen keine unbeabsichtigten Fang-/Team-/Save-Ereignisse; Begleiter und normale Save/Load/Delete-Zugriffe sind hier deaktiviert. Bestehende Maps und persönliche Daten bleiben erhalten.

`ReviewGameplayV11.py` und `ReviewForestBattleV11.py` aktivieren ausschließlich über den vorhandenen expliziten RAM-Prüftransport kurzzeitig reale Kämpfe/Fang/Heilung und stellen danach die Sperre wieder her. Diese technischen Parteien sind keine natürlichen Wildkontakt-Nachweise. Neue Art-/Wildprofile und Präsentationen verwenden bestehende Gameplayklassen; fehlende Lernattacken bleiben ausdrücklich unverfügbar.

## Wiederholbare Prüfung

Eine autorisierte, sauber geladene `EditorSession.py`/ArtControl-Queue wird vorausgesetzt:

```sh
python3 Tools/BiomeTestV1/RunFinalV11.py EindeutigerLaufname
```

Alle fünf vorhandenen Routen laufen in **einem gewöhnlichen PIE-Start**, mit tatsächlichen Enhanced-Input-Aktionen und Kollisionen. Keine Fahrer-Teleports; nur die echte Türfunktion versetzt in den Höhlenraum. Kein Disk-Save oder Benchmark. Ein fehlgeschlagener Schritt wird dokumentiert, nicht als Erfolg ausgegeben. Alte Ergebnisverzeichnisse werden nicht überschrieben. Dies ist keine Hardware-Controllerprüfung.

Einzelne `Review*V11.py`-Werkzeuge verwenden benannte Requests unter `Saved/BiomeTestV11`. `CompareForestCameraV11.py` erstellt ausdrücklich positionierte echte A/B-Fotos; das ist kein Fußlauf. `CaptureForestCandidatesV11.py` prüft getrennte Kameraabstände. `ValidateForestMaterialsV11.py` prüft vollständige Verbindungen, getrennten Schatteneingang und endgültige Shaderkompilierung. `AssetAudit.py` und `MapChecks.py` lesen Referenzen beziehungsweise alle12 vorhandenen Maps ohne diese zu speichern.

`Layout.py` definiert Zentimeterkoordinaten: u Bildschirmrechts, v Bildschirmoben, Welt `(x,y)=((u+v)/sqrt(2),(u−v)/sqrt(2))`. Die Upgrade-/Refine-/Importwerkzeuge dokumentieren **einmalige** geprüfte Autorenoperationen und dürfen auf dem fertigen Stand nicht blind erneut laufen. `CreateMap.py` verweigert eine vorhandene Map. Der historische `RunWalkReview.py` gehört zum alten V1-Aufbau und ist nicht der aktuelle Gesamttest.

Aktueller Bericht: `Docs/BIOM_TESTMAP_V11_PRUEFBERICHT.md`. Echte QHD-Bilder, Videos, Originalzeitstempel und Prüfresultate nur lokal unter `Saved/BiomeTestV11`; tatsächliche Kampfmenüaufnahmen unter `Saved/GlumandaV11/LiveUI`. Keine Kontrollmedien versionieren. Vorhandene lokale Diagnose-/Sitzungshelfer bleiben erhalten und sind kein Laufzeitbedarf.
