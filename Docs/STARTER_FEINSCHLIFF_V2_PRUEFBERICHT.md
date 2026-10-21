# Starter-Feinschliff V2 – Prüfbericht

Stand 21.10.2026, aktives Projekt `/Users/harry/Developer/PokeMonster`, Ausgangscommit `d1c9deef87ac542f845ddb4f201ed4711ea6e794`. Keine neue Map, Projektkopie oder Worktree. VisualV2, Weltgestaltung, Heilhaus, Kamera, Beleuchtung und ClassicBattle-Aufbau bleiben erhalten.

## Geprüfter Meilenstein: Oberweltbewegung

- Begleiter wird ausschließlich aus Teamplatz 1 ausgewählt. Bei kampfunfähigem/ungültigem oder visuell nicht unterstütztem ersten Mitglied wird kein anderes Mitglied ersatzweise gespawnt. Keine automatische Teamumsortierung.
- Beschleunigung, Bremsen und begrenzte Winkelbeschleunigung statt sofortiger Geschwindigkeitswechsel. Individuelle Parameter bleiben in den vorhandenen Spezies-Einstellungen. Normale Walk-/Run-Referenzgeschwindigkeiten bleiben erhalten.
- Zufallsziele berücksichtigen vier zuletzt gewählte Ziele und seltener besuchte Habitatsektoren. Es werden ausschließlich tatsächlich erreichbare Ziele angenommen.
- Kollisiongeprüfte Pfadglättung und Anschluss an den exakten Zielpunkt, auch wenn dessen gerundete Rasterzelle nicht begehbar ist. Keine Abkürzung durch Wasser oder Hindernisse.
- Fehlgeschlagene Begleiter-Rückrufpfade werden zeitlich begrenzt erneut gesucht; bisher konnte die leere Route jeden Frame eine neue Suche auslösen.

Echter PIE-Test `Saved/StarterExpansionV1/PolishMovement02/Result.json`: bestanden, 17 Prüfschritte einschließlich Sprint/Brücke, Rückruf, ClassicBattle-Pause, Rückkehr, genau einem Begleiter und Wechsel aller drei Begleiterspezies. Keine Testteleports. Gemessene Wild-Auslenkungen während des Laufs: Glumanda 603,96 cm, Schiggy 514,27 cm, Bisasam 581,69 cm. Alle innerhalb ihrer bestehenden Habitate. Nach 65 Sekunden Beobachtung: 2/3/3 erfolgreiche Pläne, keine blockierten Schritte in dieser Stichprobe. Maximaler Begleiterabstand im Sprint-/Brückenlauf 830,48 cm, maximale Bewegungsgeschwindigkeit 385,00 cm/s, anschließender Rückruf bestanden. Dies beweist keine universelle Navigation über beliebiges Terrain.

Der erste Testlauf `PolishMovement01` scheiterte durch überschießende binäre Testeingaben an einem Wegpunkt. Teststeuerung auf dosierte analoge Eingabe nahe dem Ziel angepasst; keine Spielersteuerung verändert. Der Dev-Spielstand wurde jeweils anhand SHA-256 wiederhergestellt.

Mac Development Editor Build erfolgreich. Gemeinsame Testsuite nach nachfolgend vorbereiteten Korrekturen: 80/80 erfolgreich, keine Testwarnungen oder Fehler (`StarterPolishAutomation02`). Ein vorheriger Lauf hatte 79/80: historischer Glumanda-Test erwartete noch den alten aktiven Präsentationspfad. Er prüft nun weiterhin das originale reparierte V11-Mesh und die sechs unveränderten Clips; nur die bewusst korrigierte Faint-Bindung ist getrennt.

## Weitere Teile dieses Auftrags

Animierte Modellkorrekturen und vier verifizierte Attackenwirkungen sind lokal vorbereitet. Abschließende Unreal-Sichtung, gemeinsame Gameplayprüfung, Map Checks, Quellen-/LFS-Schutzprüfung und zugehöriger GitHub-Meilenstein folgen. Dieser Zwischenstand ist noch keine vollständige visuelle Abnahme.

Physischer Switch-Pro-Controller-Test bleibt ausdrücklich offen. Keine FPS-Benchmarks durchgeführt. Kontrollmedien liegen ausschließlich im ignorierten `Saved/` und werden nicht hochgeladen.
