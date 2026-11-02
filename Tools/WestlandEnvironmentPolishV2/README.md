# Westland Environment Polish V2

Die gespeicherte Map funktioniert ohne diese Skripte. Ausschließlich vorhandenes Projekt und vorhandene Map; kein Laufzeit-Spawn-/Gelände-Generator. Große Ergebnisse unter `Saved/ProjectRefinement/WestlandEnvironmentPolishV2/`, Bericht unter `Docs/WESTLAND_ENVIRONMENT_POLISH_V2.md`.

Abgeschlossene einmalige Autorenfolge im eigenen sauberen Editor: Inspect/Assets/InspectDetails → Vorher-Bilder/Performance → Densify → Flowers → Water → Terrain → RocksBed → Ground → Reground → ForestFloor → PolishReview → TuneWater → BankGuard → ShoreFit → RegroundBanks. **Nicht blind erneut ausführen**: Guards schützen bereits vorhandene Assets und Nachweislabels. Alle Terrain-/Flussänderungen betreffen ausschließlich neue lokale Derivate. Bibliotheksoriginale bleiben unverändert. Die Shapes-Masken schützen Wege/Pads und den zentralen Wasserfreiraum. BankGuard verwendet unveränderte Ausgangstiles und begrenzte Korrekturen; ShoreFit prüft reale Ufer-Schnittpunkte.

`Common.py` teilt Autoren-HISM-/Material-/Bodenfunktionen. `Photos.py` erstellt neun echte Third-Person-Motive mit neuem `PhotoRequest.json`-Label; `Performance.py` liest ein unbenutztes `PerformanceRequest.json`-Label und misst fünf feste Standorte dreimal ohne Video mit CSV-GPU-Zählern. Kein Grafikprofilwechsel. Echte Boden-/Kamerakollisionsunterschiede werden dokumentiert.

`Audit.py`: eng begrenzter Szenen-/Terrain-/Wegevergleich. `MapChecks.py`: zwölf vorhandene Maps prüfen, nicht speichern. `Regression.py`: bestehenden regionalen Gameplayprüfer mit eigenem Slot wiederverwenden. `FinishEditorChecks.py` war die begrenzte Abschlussfolge ausschließlich für den eigenen sauberen Prüfeditor; nicht für eine beliebige Nutzersitzung vorgesehen. Normale Beendigung, kein Force Quit.

- `RunAutomation.py NEUES_LABEL`: bestehender strenger vollständiger Automation-/Report-Vertrag mit eigenem UserDir; beendet bei einem Timeout keinen Prozess gewaltsam.
- `RunNative.py NEUES_LABEL NativeTour.py`: komplette bestehende Enhanced-Input-Regionsroute; `pm.Speed 3` außen, `pm.Speed 1` am bestehenden ausgelagerten Heilhaustürübergang. Faktor3 kann den Innenraumboden vor der Relocation überlaufen; das wurde auch mit Originalterrain reproduziert; als bestehende Einschränkung getrennt dokumentiert, keine Produktions-Tür-/Geschwindigkeitslogik geändert.
- `RunNative.py NEUES_LABEL NativeSpeed.py`: tatsächliche Software-WASD-/Stickgeschwindigkeiten1/2/3 plus Stamm-/Kamerakollision. Kein behaupteter physischer Controller-Test. Zuvor `GeneratePhysicsProbes.py` für die49 tatsächlichen Terrain-Kollisionsproben ausführen.
- `RunNative.py NEUES_LABEL WaterSafety.py`: natürliche Wasserpopulation ohne Spawn-/KI-Overrides, vorhandene Flussbarriere und tatsächliche einfache Stammhüllen.
- `RunNative.py NEUES_LABEL RestartTravel.py --resume-owned-tour`: ausschließlich den eigenen erfolgreich geprüften `NativeTour03`-Save laden, kein Nutzersave.
- `NativeDoor.py`: separate diagnostische Platzierungen und echte Türbewegungen1/3; letzte Kontrolle verwendet nur in diesem Prozess Originalterrain und deaktivierte neue Zusatzkollisionen. Keine Assets oder Spielstände gespeichert. Fehlgeschlagene Diagnosefälle werden als solche ausgegeben.

Labels müssen neue Verzeichnisse sein. Launcher verweigern vorhandene parallele Unreal-Sitzungen. Eigene Tests beenden sich regulär über Unreal, keine automatischen Kills oder Asset-Reimports. Ausgangsinventar und QA-Dateien sind lokale Prüfgrundlagen, keine Spielabhängigkeiten.
