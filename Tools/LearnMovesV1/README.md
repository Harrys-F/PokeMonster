# Lernattacken V1 – begrenzte produktive Bindung

Bestehende Quellen: `Tools/BiomeTestV1/SpeciesV11.json` und bereits gepinnte pret/pokecrystal-Kristall-Daten. `Plan.json` enthält 15 tatsächliche Move-Datensätze und 16 unveränderte Lernlevel. Originalquellen werden nur als Fakten/Hashes referenziert; keine ROM-Dateien oder kopierte Engine/Spielimplementierung.

`BuildPlan.py` liest die bestehenden lokalen Rohreferenzen unter Saved und erzeugt denselben Plan. `Import.py` läuft einmal im sauberen Editor, legt ausschließlich den eigenen Datenpfad an und prüft bei Wiederaufnahme jedes bereits vorhandene Asset; mismatched Daten abbrechen. Pro Spezies bleiben alle anderen Lernzeilen und Originaleigenschaften erhalten. `Validate.py` ist rein lesend und für einen frischen Editorstart gedacht. Kein Modell-Reimport.

Nach Editor-Build und autorisiert gestarteter vorhandener ArtSession:

```
python3 Tools/ProjectMaintenance/ArtControl.py script Tools/LearnMovesV1/Validate.py
python3 Tools/LearnMovesV1/RunReview.py EigenesLernLabel learning
python3 Tools/LearnMovesV1/RunReview.py EigenesKampfLabel production
```

Eindeutige alphanumerische Labels, vorhandene Ergebnisse niemals überschreiben. `learning` verwendet reale KO-XP, bestehende B/A-Lernmenüs, alle fünf betroffenen Arten, Ablehnen/freie Slots und anschließendes Laden über das normale Hauptmenü. `production` spielt alle 15 produktiven Move-Assets in ClassicBattle und je einen Pfad aller fünf Arten in WorldBattle. Kontrollierte Runtime-Kampfwerte sind ausdrücklich technische Prüffakten, keine Balanceänderung. Testslots sind eigene `PokeMonster_SaveV2_Test_*`-Dateien; keine Originalslots kopieren, laden oder ändern. Alle Nachweise bleiben lokal unter Saved.

Native Tests: `PokeMonster.LearnMovesV1` (32 Fälle). Gesamte `PokeMonster`-Automation erneut ausführen und den tatsächlichen strengen Exit dokumentieren. Gemeinsame Save-/Lern-/Meisterregeln und fehlende Zielmodelle werden zusätzlich durch die bestehenden Tests abgedeckt. Physischen Controller-Test nicht behaupten.

Die unterstützten neuen Komponenten sind durch vorhandene fehlende Lernattacken begründet. Kein allgemeines neues Flugsystem: Windbonus gilt nur für explizit markiertes mechanisches Aufladen, niemals für dekoratives Schweben. Kein rückwirkendes Lernen abgelehnter oder früher übersprungener Attacken. Persönlich Erlerntes bleibt dauerhaft, nachträgliches Aktivieren bleibt meistergebunden und bewahrt AP.
