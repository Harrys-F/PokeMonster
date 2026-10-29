# Pokémon-Modellbestand und wiederholbare Gameplayprüfung

Verbindlich: ausschließlich Harrys Meshy-Pokémon aus Incoming verwenden. Keine selbst erstellten/prozedural generierten Ersatzmodelle. Die früheren Raichu-Erstellungswerkzeuge und deren exklusiven Assets wurden im Korrekturauftrag entfernt.

`Inventory.py`, `InspectSources.py`, `InspectIncoming.py` bleiben allgemeine Bestandswerkzeuge. `Run.py` und `Gameplay.py` prüfen bestehende Beutel-/Entwicklungs-/Begleiter-/Kampf-/Save-Funktionen mit isolierten QA-Fixtures. Sie erzeugen keine Pokémon-Modelle. Review-Requests sind auf Saved/ProjectRefinement/ModelsV4 beziehungsweise RaichuMeshyCorrection begrenzt.

Die aktive Raichu-Darstellung stammt aus `Art/Characters/Creatures/Incoming/Raichu.glb`; Arbeitsquelle `Art/Characters/Creatures/Raichu/Source/Raichu_Meshy_V1.blend`. Technische Vorbereitung über die vorhandene `Tools/CreatureExpansionV3`-Pipeline mit explizitem Namen Raichu. Originalgeometrie/UVs/Texturen erhalten. Raichu-spezifische Rig-/Gewichtsparameter verändern keine andere Art.

Nachweise und Löschliste: `Docs/RAICHU_MESHY_KORREKTUR.md`. Der frühere V4-Bericht ist historisch ersetzt.

Bestehende Befehle: `pm.TestGround.List`, `pm.TestGround.Go Pikachu`, `pm.TestGround.Go Raichu`, `pm.TestGround.Mode idle|walk|run|turn|directions|auto`, `pm.TestGround.React attack|hit|faint|happy`, `pm.TestGround.Reset`, `pm.TestGround.Return`.
