# VisualV2 Interior, Pokemon & Teleport V6

Nur im bestehenden Projekt. Die Autorierung ist ein einmaliger, bewachter Schritt und darf nicht über vorhandene Ergebnisse erneut ausgeführt werden. Keine Nutzersaves als Fixtures.

- `Inventory.py`, `InspectV6.py`, `ProbeImportAPI.py`: Ist-Zustand lesen; die Before-Dateien bei einer neuen Untersuchung in einem eigenen Nachweisordner erfassen, nicht überschreiben.
- `ImportOne.py`, `ImportModels.py`: native Interchange-GLB-Importe ausschließlich aus den per SHA geprüften neuen Incoming-Quellen. Bestehende Originalmodelle nie überschreiben. `ImportedModels.json` dokumentiert 49 statische Kandidaten, einschließlich eingebetteter PBR-Texturen. Sie besitzen weder Rig noch Animationen und keine spielbaren Arten-Daten.
- `Author.py`: private Raum-Materialien und HISM-Architektur nur im bereits versetzten Heilhaus; bestehende Möbel, Türlogik, Heiler, Kollisionen und Laufwege bleiben erhalten. Nur Pikachu/Karpador-Artdaten ändern. `FinalizeRoom.py` speichert ausschließlich eigene nachträglich als instanziert erkannte Materialien.
- `TeleportReview.py`: alle 19 bestehenden Namen, Index/Alias, ungültiger Name, Editor-Konsole in PIE, ursprüngliche Position/Blickrichtung/Kamera, Begleiter/Team, echte Bewegungen und alle 49 statischen Importe. `ImportReview.py` ist der gezielte Teilnachtest.
- `InteriorReview.py`: natürliche sichtbare Begegnung, regulärer Zug und Fang, Heiltresen um dessen bestehende Kollision herum, HP/AP-Heilung, vier stets sichtbare Wände, acht Kamerarichtungen, Tür mit pm.Speed 1/2/3 und isolierter Save/Load.
- `WildMotionReview.py`: bereits natürlich gespawnte Pokémon beobachten, ohne Ziele/Profil/Spawnregeln zu überschreiben. Pro Art eine begrenzte echte Bewegungssequenz mit Zeitstempeln; keine Gameplay-FPS aus der Aufnahme ableiten.
- `GameplayReview.py`: bestehender zusammenhängender Rundgang, Kamera, Sprint, Brücke, Cottage, Kampf/Fang, Begleiter, Team, Uhr, Innenraum, Save/Load und echter Mapwechsel.
- `LaunchEditor.py`, `RunNative.py`, `RunAutomation.py`, `MapChecks.py`: eigene isolierte Prüfprozesse. Keine automatische gewaltsame Beendigung; bestehende Sitzungen unangetastet. `NativeChecks.py`/`EditorChecks.py` zeigen die tatsächlich verwendeten Prüfabläufe und ihre einmaligen Labels. Für Wiederholungen neue Labels verwenden.
- `CaptureBenchmark.py`: identische QHD/C75/High-Stellen, dreimal sechs Sekunden nach vier Sekunden Einlauf; Video aus. Fotos außerhalb der Messfenster. Shader-/Thermik-/KI-Schwankungen berücksichtigen.
- `VerifyProtection.py`: Originalquellen, bestehende Save-Dateien, lokale Nutzerkonfiguration, geschützte Maps/Dateien und Backup-Refs gegen die beim Auftragsbeginn tatsächlich erfassten SHA-Werte prüfen.

## Bedienung

`pm.TestGround.List`, `Go <Name|1..19>`, `Return`, `Mode auto|idle|walk|run|turn|directions|reset`, `Reset`, `React attack|hit|faint|happy` bleiben erhalten.

Neue statische Kandidaten: `pm.TestGround.Go Modell:Aquana` bzw. `Modell:Nidoran_m`/`Modell:Nidoran_w`. Nur `Mode idle|turn|reset`; Drehung ist eine Inspektionsdrehung, keine Körperanimation. Maximale sichtbare Ausdehnung 200 cm ist eine ausdrücklich nicht kanonische Prüfgröße. Rigs, Gewichte, Größen/Frontrichtung, LODs und Gameplay-Daten sind noch offen.

Die bestehende Artenregistrierung verwaltet weiterhin alle spielbereiten Pokémon. Für ungeriggte Kandidaten liest die vorhandene TestGround-Klasse ausschließlich StaticMesh-Metadaten unter `/Game/Characters/Creatures/ModelIntakeV6/<Name>/...`; keine zweite Artenliste. Neue Kandidaten dort werden bei explizitem List/Go-Aufruf entdeckt. Nur das ausgewählte Modell wird geladen, nach Return entfernt. Kein neuer Wildspawn.

Große Nachweise bleiben unter `Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6/`, nie in Git. Bericht: `Docs/VISUALV2_INTERIOR_POKEMON_TELEPORT_V6.md`.

Abschließende Farbprüfung: `MaterialAudit.py` liest alle importierten Texturrollen. `FixImportedTextureRoles.py` korrigiert einmalig die nachgewiesene falsche Normalmap-Autoerkennung von Entoron/Zubats Farbtexturen; nur eigene Importkopien. Die getesteten GLBs verwenden nach Prüfung BaseColor/MetalRoughness/Normal/Emissive in den Bildindizes 0/1/2/3. Neue unbekannte GLB-Schemata vor Verwendung dieses Importwerkzeugs gesondert prüfen. `ColorReview.py` wartet fünf Sekunden auf Shader/Streaming und testet die zwei korrigierten Kandidaten. `CompareFinal.swift` verwendet ausschließlich die bestätigten finalen Farbbilder. `EncodeReviews.py` decodiert die echten Clips und prüft Zeitstempel ohne Interpolation.
