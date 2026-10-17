# Meshy NPC Integration V1 – Werkzeugübersicht

Projekt: `/Users/harry/Developer/PokeMonster/Game/PokeMonster`.

Diese Skripte gehören ausschließlich zum Integrationsdurchgang. Nicht blind den gesamten Ordner ausführen. Vorhandene Quellen und Incoming bleiben unverändert; Import-, Reparatur- und Exportskripte dürfen ausschließlich die hier neu erzeugten NPC-Ordner bearbeiten.

## Verwendete Hauptschritte

- `PrepareSource.py`: je GLB eine unabhängige neue Blenderquelle; Factory-Startup, fordert noch nicht existierenden Zielordner.
- `RangerRuntimePilot.py`, `RepairRangerPilot.py`, `ExportRanger.py`: geprüfter stationärer Ranger-Pilot, einschließlich dokumentierter verworfener Erstgewichte.
- `HumanoidVariants.py`, `RepairActionPersistence.py`, `FixArcherGear.py`: drei Kandidaten mit eigenen Gelenkpositionen; keine automatische Walk-Freigabe.
- `StaticReviewExport.py`: bewusst nur statische Reduktionsprüfstände. Kein Retopologie- oder Rigging-Nachweis. Unapplizierte Decimate-Modifikatoren können beim erneuten Laden sehr teuer sein.
- `ImportNPCAssets.py`: eigene neue Unreal-Pfade; keine fremden Assets ersetzen. Explizite Skeletal-Materialnutzung und Materialinstanz-Aktualisierung erforderlich.
- `BindRangerVisual.py`: ausschließlich neue VisualV2-Darstellung des vorhandenen Wanderers. Python-Rotatoren immer mit `pitch=`, `yaw=`, `roll=` übergeben.
- `ReviewAtWanderer.py`: tatsächliche Spielkamera; temporäre Kandidatenanzeige an der bestehenden Darstellung, anschließend Rückgabe. Kein Speichern während dieses PIE-Vergleichs.
- `FootTest.py`: vollständiger Fußlauf über bestehendes Enhanced Input und Gameplay. Vorher Dev-Slot extern bytegenau sichern, nach StopPIE wiederherstellen.
- `PerformanceTour.py`: reale Viewportauflösung protokollieren; r.SetRes ändert eingebetteten PIE nicht zuverlässig. Keine parallelen Blender-/Build-Jobs während Messungen.
- `ConnectivityAudit.py`, `ReopenSources.py`, `ReopenRuntime.py`, `ReadStaticLibraries.py`, `InspectStaticFBXUV.py`, `FinalEditorAudit.py`: lesende bzw. auf eigene neue Pakete begrenzte Prüfungen.

## Diagnose-/Sitzungswerkzeuge

`Inspect*`, `ConfigurePIE.py`, `GameCameraReviews.py` und `StopReviewInspectSpawn.py` enthalten auch explorative API-Prüfungen. Die erste freie Vorschauposition bzw. Actor-Spawn-Versuche gelten nicht als erfolgreiche Abnahme. Maßgeblich sind die letzten Bilder in `FinalScreenshots.json` und `ReviewAtWanderer.py`.

`Queue.py`, `RunInEditor.py` und `MCPClient.py` benötigen die vorhandene lokale Unreal-MCP-Sitzung. Slate-Referenzen dürfen nach einem Editorneustart nicht ungeprüft wiederverwendet werden. Der Queue-Callback wurde zum Abschluss entfernt. `CloseForBuild.py` beendet den Editor nach begrenzter Prüfung; nicht als allgemeines Speicherskript verwenden.

Der Ergebnisbericht und seine offenen Punkte haben Vorrang vor älteren Pilot-Statusfeldern. Kein Modell ist allein aufgrund erfolgreicher Skriptausführung produktionsreif.
