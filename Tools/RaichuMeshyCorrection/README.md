# Meshy-Raichu-Korrektur

Ausschließlich Harrys unverändertes `Art/Characters/Creatures/Incoming/Raichu.glb` verwenden; SHA-256 und tatsächliche Quelle stehen in `Docs/RAICHU_MESHY_KORREKTUR.md`. Keine Modellgenerierung. Die bestehende CreatureExpansionV3-Pipeline übernimmt Rigging, Skinning und Animation, ohne Geometrie oder UVs neu zu erzeugen.

- `InspectSource.py`: ursprüngliches GLB untersuchen und Diagnoseansichten unter Saved schreiben.
- `AuditReferences.py`: tatsächliche AssetRegistry-Abhängigkeiten einschließlich fehlender alter Pakete lesen. Keine Assets speichern.
- `ImportReplacement.py`: bereits ausgeführter, bewachter Erstimport; verweigert einen bestehenden Zielnamensraum. Kein allgemeiner Reimportbefehl.
- `RefreshWork.py`: ausschließlich für die noch unversionierte Arbeitsphase; verweigert bereits versionierte MeshyV1-Assets. Kein Update bestehender Nutzerquellen.
- `RemoveUnwantedAssets.py`, `RemoveUnwantedFiles.py`: **bereits ausgeführte einmalige Entfernung** der im Prüfbericht aufgeführten, exakt abgeglichenen Altdateien. Nicht erneut ausführen. Benötigen die damaligen Referenz-/Hashnachweise unter Saved und überschreiben keine Quellen.

Die allgemeinen Bestands- und Gameplaywerkzeuge in `Tools/ModelsV4` bleiben erhalten. Der alte generische Saved-Berichtschreiber ist historisch, referenziert entfernte Quellen und wird für diese Korrektur nicht benutzt. Historische Prüfmedien enthalten möglicherweise die alte Darstellung; sie sind keine Modellquellen und keine aktiven Spielassets.
