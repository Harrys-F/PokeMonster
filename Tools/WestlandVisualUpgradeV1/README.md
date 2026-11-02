# Westland Visual Upgrade V1 – begrenzte Autoren-/Prüfwerkzeuge

Die gespeicherte Map und der C++-Spieler funktionieren ohne diese Skripte. Bericht: `Docs/WESTLAND_VISUAL_UPGRADE_V1.md`. Große Nachweise liegen ausschließlich unter `Saved/ProjectRefinement/WestlandVisualUpgradeV1/`. Keine Nutzer-Saves verwenden.

- `Inspect.py`/`Assets.py`: Bestandsaufnahme vorhandener Maps/Assets.
- `Materials.py`, `Vegetation.py`, `Polish.py`, `FinalizeBanks.py`, `TrunkCollision.py`: sequenzielle, bereits abgeschlossene einmalige Editor-Autorenschritte. **Nicht als Startskript und nicht blind erneut ausführen.** Sie setzen den jeweils vorherigen Stand sowie ein eigenes sauberes Editorfenster voraus. Originale bleiben erhalten; es wird nur die vorhandene Westland-Map bzw. der neue lokale Assetordner gespeichert.
- `ValidateSurfaces.py` und `Audit.py`: finale Materialverbindungen bzw. eng begrenzter gespeicherter Szenenvergleich gegen das lokale Ausgangsinventar. `MapChecks.py`: alle zwölf bestehenden Maps prüfen, nicht speichern.
- `Photos.py`/`Overview.py`: sieben echte paarweise Spielansichten plus separate Editor-Gesamtansicht. Nur eigener isolierter Editor/PIE, vorher eindeutiges `PhotoRequest.json` mit neuem Label.
- `Regression.py`: vorhandenen regionalen Interaktionsprüfer mit eigenem Slot-/Nachweispfad wiederverwenden.
- `RunAutomation.py NeuesLabel`: vorhandener vollständiger strenger Automation-/Report-Vertrag mit isoliertem UserDir, ohne automatisches Prozess-Kill bei Zeitüberschreitung.
- `RunNative.py NeuesLabel NativeSpeed.py`: neuer eigener `-game`-Prozess; prüft Testtempo und reale Stamm-/Kamerakollision.
- `RunNative.py NeuesLabel NativeTour.py`: vorhandene Fußroute über normales Enhanced Input mit `pm.Speed 3`; vor eigenem regulären Save zurück auf1.
- `RunNative.py NeuesLabel WaterSafety.py`: Faktor3-Flussbarriere, vorhandene Stammhüllen, natürliche Population ohne Spawn-/KI-Overrides; zunächst normale Kamerablickrichtung vom Wasser weg, anschließend Fischansicht.
- `RunNative.py NeuesLabel RestartTravel.py --resume-owned-tour`: ausschließlich den bestehenden eigenen `NativeTour02`-Save prüfen; keine Nutzer-Savekopie.

Neue Labels müssen unbenutzte Verzeichnisse sein. Launcher verweigern parallele vorhandene Unreal-Sitzungen und beenden nur ihre eigenen Tests regulär über Unreal. Ein Timeout beendet keinen Prozess gewaltsam. Kein Asset-Reimport, Build oder Mapautorenschritt beim normalen Spielen erforderlich. Physischer Controller wird nicht durch Software-Stickinjektion als getestet erklärt.
