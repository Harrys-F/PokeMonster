# Kampfansicht V2 – echte Laufzeitprüfung

Nur im aktiven Projekt. Keine Mapkopien, kein Asset-Speichern, kein paralleles
Kampfsystem. `Saved/BattleViewV2` bleibt lokaler Entwicklungsnachweis.

- `ProjectQA.py <neuesLabel> Build|Automation` aus `Tools/ProjectMaintenance`:
  vorhandener Editor-Build und vollständige PokeMonster-Tests; Editor vorher sauber schließen.
- Editor mit der vorhandenen `ArtSession.py` starten. Sie verweigert ungesicherte
  Pakete. Kein Save All, kein Verwerfen.
- `python3 Tools/BattleViewV2/RunPIE.py <neuesLabel> Review|Input|World`:
  vier Umgebungen/Menüs/Angriff und Lebenszyklus; logische Nintendo-Gamepad-Events
  durch Slate; beziehungsweise bestehende WorldBattle-Ausnahme. Die Inputprüfung
  zertifiziert keinen physischen Controller.
- `python3 Tools/BattleViewV2/RunNative.py <neuesLabel> 2560 1440`
  oder `1280 720`: vier Umgebungen im eigenständigen Development-`-game`-Prozess,
  Editor vorher schließen. Kein paketierter Shipping-/Cook-Test.
- `Tools/GlumandaV11/RunGameplay.py <neuesLabel>`: bestehender vollständiger
  Enhanced-Input-Fußlauf einschließlich Fang/Wechsel/Heilhaus/Save-Load und exakter
  Wiederherstellung des ursprünglichen Dev-Slots. Nicht parallel starten.
- `ArtControl.py script Tools/BattleViewV2/CheckMaps.py`: alle vorhandenen Maps
  laden/prüfen, ohne Speichern; nur außerhalb von PIE und bei sauberen Paketen.

`pm.CreatureReview.Start classic|world [meadow|forest|cave|ruins]` startet nur auf
expliziten Development-Aufruf eine flüchtige Glumanda-vs-Glumanda-Prüfung.
`pm.BattleView2.Input Focus|A|B|Left|Right|Up|Down` verwendet tatsächliche Slate-
Gamepad-Ereignisse mit logischer Nintendo-Belegung. Keine Hardware-Simulation als
physische Abnahme ausgeben.

`pm.CreatureReview.CaptureLiveUI BattleV2_<eindeutigerName>` fotografiert exakt den
nativen Slate-Spielviewport unter `Saved/BattleViewV2/LiveUI/`. Vorhandene Aufnahmen
werden nicht überschrieben. Die tatsächliche Größe steht in `CaptureMethod.txt`;
eine angeforderte RHI-Auflösung ist kein Nachweis derselben Slate-Fenstergröße.
Andere Namen behalten das ältere Ausgabeziel `Saved/GlumandaV11/LiveUI`.

Die Reviewskripte prüfen echten Sessionfortschritt, Reaktionsclips, Rückgabe von
Eingabe/Kamera/Pawn und Abbau der Bühne. Sie verändern keine Speziesdaten und
schreiben keinen Spielstand. Alle Ausgaben bleiben lokal, keine Pflichtfixtures
für Build oder Automation. Fehlende Fluchtregeln, in-battle Heilitems und endgültige
Attackendaten werden nicht durch Reviewwerkzeuge erfunden.

`Protection.py <neuesLabel>` vergleicht SHA-256 mit dem lokalen `Initial.json`
dieser Sitzung einschließlich geschützter Unversionierter, Maps, Sichtcode,
Dev-Spielstand und Backup-Refs. Das Inventar ist kein mitgeliefertes Testfixture.
Fehlt es, ist die historische Schutzprüfung nicht ausführbar; niemals einen
fehlenden Vergleich als bestanden melden.
