# Teamreihenfolge V4

Das bestehende Oberwelt-Teammenü unterstützt Auswahl einer Kreatur und danach eines
Zielplatzes. Belegte Plätze tauschen die **vollständigen Instanzen**. Freie Zielplätze
verschieben ans Ende der dicht gespeicherten Liste; leere Zwischenplätze werden
nicht als ungültige Kreaturen gespeichert. Dies wird im Menü ausdrücklich erklärt.

- Tastatur: Pfeile für Zielplatz, vorhandene Interaktionsbelegung (E/Enter) zur Auswahl,
  Escape zum Abbrechen der Auswahl, danach Escape/Tab zum Schließen.
- Controller: UMG-Navigation und die bereits konfigurierbare gemeinsame
  Interaktionsaktion. Keine neue feste Switch-Taste. Physischer Controller-Test offen.
- Auswahl über Instanz-ID, nicht über einen inzwischen veralteten Arrayindex.
- Ungültige IDs/Ziele, doppelte Instanzen, laufender Kampf und Niederlagenrückkehr
  werden abgewiesen. Die UI zeigt die neue Reihenfolge sofort.
- Teamplatz 1 bleibt der einzige aktive Begleiter. Das vorhandene Begleitersystem
  erkennt die neue Instanz; keine zusätzliche Kreatur wird erzeugt.
- Save-Schema 4, Spezies-IDs und Kampflogik bleiben unverändert.

## Prüfungen

`PokeMonster.Overworld.Team.ReorderPreservesInstances` vergleicht sämtliche
reflektierten Instanzfelder, testet Platz 5 → 1, freie Plätze, ungültige Ziele,
Kampfsperre und Snapshot-Restore.

Die echte PIE-Prüfung `Tools/CreaturePolishV4/RunTeam.py Team01` hat Platz 5 → 1
über native Slate-Pfeil-/Enter-Eingaben durchgeführt. Identitäten, KP, AP, Level,
Erfahrung und Status blieben gleich; UI und einzelner Myrapla-Begleiter wechselten
korrekt. Auch echtes Schreiben/Laden des Dev-Slots, ein freies Ziel und die
Kampfsperre bestanden. Der ursprüngliche Dev-Spielstand wurde aus den ausschließlich
im Arbeitsspeicher gehaltenen Originalbytes nach Prüfung des Test-Schreibstands
exakt restauriert.

Lokale Nachweise: `Saved/CreaturePolishV4/Team01/` und
`Saved/CreaturePolishV4/LiveUI/PolishV4_Team01_*/`. Bilder sind keine Git-Eingaben.
