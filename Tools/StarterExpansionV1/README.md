# Starter-Erweiterung V1

Bestehende Kreaturen-Pipeline V2, keine neue Kampf-/Fang-/Speicherlogik. Alle Befehle vom aktiven Projekt aus. Prüfmedien ausschließlich unter Saved.

1. Blender `--background --python-exit-code 3 --python Tools/StarterExpansionV1/InspectModels.py -- NeuerPruefname`: GLB-Geometrie und Originaloptik prüfen. Eingang `Shiggy.glb` bleibt genau so benannt.
2. `PrepareModels.py`: ausschließlich fehlende neue Quellen erzeugen; Originalreferenz, unveränderte Dreiecke/UVs und gepackte Texturen. `RigLayout.py` enthält tatsächlich eingepasste Gelenkpositionen. `AutomaticSkin.assign_heat` löst auf einer temporär verschweißten Hilfskopie und überträgt ausschließlich normalisierte Gewichte. Kein Retargeting von Glumanda.
3. `AnimateModels.py`: sieben eigenständige Clips und FBX. Bestehende Aktionen/Exporte werden standardmäßig abgewiesen. `-- --revise-generated` ist ausschließlich für eine bewusst freigegebene Revision dieser generierten Arbeitsdateien, nicht für fremde oder manuell bearbeitete Quellen.
4. `ValidateBlender.py -- NeuerPruefname`: echte erneute Öffnung und FBX-Reimport aller Clips sowie große Poseansichten. Numerische Fußprüfung ersetzt keine Sichtprüfung.
5. Sauberer bestehender Unreal-Editor mit `Tools/ProjectMaintenance/ArtSession.py`; erst nach frischer Ready.json `ArtControl.py script Tools/StarterExpansionV1/ImportModels.py`. Nur neue Asset-Namensräume, Import nie auf vorhandene Originalassets. Eigene Skeletons, Normal-G-Invertierung, MR-Kanäle aus glTF. Schiggy-BaseColor vorerst ohne Mips gegen nachgewiesenes Atlasbleeding; in Bewegung prüfen.
6. Editor schließen; `ProjectQA.py <NeuerName> Build` und `Automation`. Alle vorhandenen Maps mit `CheckMaps.py` nur lesend prüfen.
7. `RunModels.py <NeuerName>`: vier wirkliche Classic-/WorldBattle-Abnahmen, Save/Load und automatische Wiederherstellung des ursprünglichen Dev-Slots. Explizite `pm.StarterReview.*`-Befehle sind nur Entwicklungsfixtures, verändern keine Assets und sind im Shipping-Build nicht registriert.
8. `RunDefeatSave.py <NeuerName>`: echter Niederlagen-/Autosave-/Reload-Lauf, ursprünglichen Dev-Spielstand wiederherstellen. Ein abgebrochener Lauf darf keinen konkurrierend geänderten Slot überschreiben.

Spezies-IDs Schiggy/Bisasam und Zunderlauf bleiben unabhängig von Modell-/Dateinamen stabil. Nur nachgewiesen unterstützte Gen-2-Attacken anbieten; offene Wirkungen im Prüfbericht benennen. Eigene Hilfs-/Prüfdateien sind kein Anlass, andere unversionierte Nutzerdateien aufzunehmen oder zu entfernen. Keine neue Map und keine Performance-Testreihen.
