# Entwicklungsdaten V3 und gezielte Abnahme

Aktives Projekt: `/Users/harry/Developer/PokeMonster`, UE 5.8.2.

- `Audit.py`: liest alle Arten- und Itemassets sowie das bestehende Artenregister. Schreibt nur `Saved/ProjectRefinement/EvolutionV3/AssetAudit.json`. Incoming-Modelle werden nicht als spielbar gewertet.
- `BindKarpador.py`: bewachter, wiederholbarer Eintrag Karpador → Garados ab Level 20. Verändert ausschließlich das bereits vorhandene Karpador-DataAsset, niemals Modelle, Clips oder Maps. Bei einer unerwarteten bestehenden Regel wird abgebrochen.
- `ReferenceSources.json`: feste Revision, URL, SHA-256 und ausgewählte öffentliche PokeAPI-Metadaten. Keine ROM-Daten.
- `Gameplay.py`: tatsächliche UMG-/Inventar-/Save-/Begleiterabnahme. Nur mit einem eigenen UserDir unter `Saved/ProjectRefinement/EvolutionV3`; niemals gegen Nutzerslots starten. Die QA-Startparameter und exakten verwendeten Skripte bleiben in den jeweiligen `Launch.json`/`RuntimeUsed.py` unter Saved nachvollziehbar.

Normale Bedienung: vorhandener Beutel → Entwicklungsitem → vorhandene Teamwahl → dieselbe Entwicklungssequenz. B/Enter bestätigt, A/Esc bricht ab. Ungültige Ziele verbrauchen kein Item. Eine vollständige reguläre Steinroute fehlt derzeit; `DA_TestEvolutionItem` ist kein Donnerstein.

Die bestehende isolierte PIE-Entwicklerbedienung bleibt erhalten: `pm.EvolutionTest.List`, `pm.EvolutionTest.Start <Teamplatz 1–6>`, `pm.EvolutionTest.End`. Sie nutzt weiterhin die wirkliche Levelroute und nun auch den registrierten Karpador-Eintrag. Start/End verwenden den vorhandenen RAM-Speicherschutz; keine zweite Entwicklungslogik. Während eines normalen eigenen PIE-Tests zuerst Kampf, Dialog und Menüs schließen.

Für die automatische Abnahme erweitert der bestehende Review-Helfer seine Laufzeitfixtures ausschließlich in unserem abgegrenzten EvolutionV3-UserDir: `pm.EvolutionReview.Party Karpador <Level>` sowie `pm.EvolutionReview.ItemFixture on|off`. Die Itemfixture schaltet **nur im Arbeitsspeicher** Karpadors Route auf den vorhandenen Teststein um und stellt sie vor dem Ende beziehungsweise bei World-Cleanup wieder her. Das ist ausdrücklich keine reguläre Karpador-Steinregel und steht weder normalen Nutzerverzeichnissen noch Builds ohne Editorcode zur Verfügung. Keine dieser Fixture-Einstellungen oder Testitems wird in Artassets gespeichert.

Build und strenge volle Automation verwenden unverändert `Tools/ProjectMaintenance/ProjectQA.py`. Finale Ergebnisse, bekannte Setup-Fehlschläge und Warnungen stehen in `Docs/POKEMON_ENTWICKLUNGEN_V3_ERWEITERUNG.md`.
