# Arbeitsanweisungen für Codex

## Projekt

Dieses Repository enthält das Unreal-Engine-Projekt „PokeMonster“.

Vor größeren Änderungen müssen die passenden Dokumente im Ordner `Docs` gelesen werden:

- `Docs/TECHNIK.md`
- `Docs/SPIELIDEE.md`
- `Docs/SPIELREGELN.md`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/GRAFIKSTIL.md`

Vor Änderungen an Kamera, Levelgestaltung, Sprites, Beleuchtung oder visuellen Effekten muss `Docs/GRAFIKSTIL.md` gelesen werden.

Größere Abweichungen von der festgelegten Perspektive und Figurengröße benötigen vorher Harrys Zustimmung.

Visuelle Arbeiten müssen außerdem die verbindliche hohe Umgebungsdichte, die kleinen Figuren im Verhältnis zur Welt, die malerische 2D/2.5D-Tiefenwirkung und die klare Lesbarkeit begehbarer Wege berücksichtigen. Das gilt für Außenbereiche, Innenräume, Höhlen und Ruinen gleichermaßen.

Neue visuelle Entwürfe sollen die in `Docs/GRAFIKSTIL.md` beschriebenen Szenentypen, Layer und Höhenstrukturen wiederverwenden. Eine Vereinfachung zu Pixel-Art, einer weitgehend leeren Prototypumgebung oder einer vorwiegend dreidimensionalen Darstellung benötigt vorher Harrys Zustimmung.

## Zusammenarbeit

Harry plant, entscheidet und testet das Spiel. Codex soll möglichst viel der technischen Umsetzung übernehmen.

Codex soll:

- Arbeitsschritte verständlich und ohne unnötige Fachsprache erklären.
- bei wichtigen oder unumkehrbaren Entscheidungen vorher nachfragen.
- bestehende Dateien und Nutzeränderungen erhalten.
- keine funktionierenden Systeme ohne ausdrücklichen Grund vollständig ersetzen.
- Änderungen in kleinen, überprüfbaren Schritten durchführen.
- nach Änderungen geeignete Tests oder Builds ausführen.
- Fehler nicht verbergen, sondern Ursache und mögliche Lösung nennen.
- Harry auf sinnvolle Git-Sicherungspunkte hinweisen.
- zu Sicherungspunkten die konkreten Git-Befehle nennen.
- dauerhafte technische oder gestalterische Entscheidungen in `Docs/ENTSCHEIDUNGEN.md` dokumentieren.
- offene Fragen nicht eigenmächtig als endgültig entschieden behandeln.

## Technische Grundregeln

- Unreal Engine 5.8.2 verwenden.
- Zielplattform ist ausschließlich macOS.
- Das Spiel wird als modernes 2D-Top-Down-Spiel mit Paper2D entwickelt.
- C++ wird für grundlegende, wiederverwendbare Systeme verwendet.
- Blueprints werden für Inhalte, Konfiguration, Feineinstellungen und schnelle Tests verwendet.
- Enhanced Input verwenden.
- Auf die begrenzten Ressourcen eines MacBook Air M4 mit 16 GB gemeinsamem Arbeitsspeicher achten.
- Ressourcenintensive Funktionen nur verwenden, wenn sie für das 2D-Spiel einen klaren Vorteil bringen.
- Neue Abhängigkeiten oder Plugins nicht ohne vorherige Erklärung installieren.
- Keine Dateien aus Pokémon-ROMs oder anderen geschützten Spielen übernehmen.
- Zugangsdaten, Schlüssel und persönliche Daten dürfen nicht in Git gespeichert werden.

## Dokumentation

Wenn eine Entscheidung geändert wird:

1. betroffene Dokumentation aktualisieren,
2. alten Stand in `Docs/ENTSCHEIDUNGEN.md` als ersetzt kennzeichnen,
3. anschließend die technische Umsetzung anpassen.


## Verbindlicher aktiver Projektordner (19.10.2026)

- Ausschließlich `/Users/harry/Developer/PokeMonster` aktiv verwenden; Unreal-Projekt: `PokeMonster.uproject` direkt darin.
- Lokales `main` folgt dem bestehenden `origin/main` von `git@github.com:Harrys-F/PokeMonster.git`.
- Das lokale Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unter `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` erreichbar. Diese Backup-Verweise nicht pushen oder umschreiben; kein LFS-Prune.
- Keine zusätzlichen Projektkopien oder Versionsordner anlegen. Vor einem technisch notwendigen separaten Worktree ausdrücklich um Erlaubnis fragen.
- Vorhandene Testumgebungen verwenden; neue Unreal-Maps nur nach ausdrücklicher Freigabe.
- Der frühere schlanke Worktree bleibt vorerst bestehen. Keine Entfernung oder Bereinigung ohne weitere Freigabe.
- Nach erfolgreich geprüften Arbeitspaketen nur benötigte Quellen, Assets, Werkzeuge und Dokumentation sinnvoll committen und regulär pushen; Remote und LFS überprüfen. Keine Kontrollmedien oder temporären Dateien hochladen.


## Verbindliche Pokémon-Modellquellen – Raichu-Korrektur (29.10.2026)

- Für sämtliche Pokémon ausschließlich Harrys eigene Meshy-Modelle aus dem bestehenden `Art/Characters/Creatures/Incoming` (einschließlich ausdrücklich zugeordneter Unterordner) verwenden. Tatsächlichen Pfad und Groß-/Kleinschreibung zuerst prüfen.
- Pokémon-Modelle weder selbst modellieren noch prozedural generieren oder durch selbst erstellte Ersatzmodelle austauschen. Auch ein als Prototyp gekennzeichneter Ersatz ist dafür nicht freigegeben. Frühere Erlaubnisse für eigene Pokémon-Ersatzmodelle sind durch diese Regel ersetzt.
- Blender nur für Import, Rigging, Skinning, Animationen, Skalierung und technische Bearbeitung des eindeutig identifizierten Meshy-Originals verwenden. Die ursprüngliche Gestalt muss von Harrys Modell stammen.
- Meshy-Originale unverändert erhalten; Arbeitsquellen im vorgesehenen Artenverzeichnis anlegen. Keine ungeprüften Downloads, generierten Alternativen oder falschen Arten als Ersatz.
- Fehlt die Quelle oder ist ihre Artzuordnung nicht eindeutig, den genauen Projektpfad bei Harry erfragen. Keine Quelle erfinden und keine funktionierenden Referenzen auf ein falsches/fehlendes Modell umbiegen.
- Das selbst erstellte Raichu ist durch das korrekte Meshy-Raichu zu ersetzen und mit seinen ausschließlich eigenen Modell-/Material-/Export-/Generator-Dateien tatsächlich aus dem Arbeitsstand zu löschen. Erst Referenzen prüfen und ersetzen, dann entfernen; keine bloße Deaktivierung. Andere Pokémon, gemeinsam genutzte Assets, Spielstände und Nutzerdateien schützen. Keine Git-Historie umschreiben oder LFS-Prune ausführen.
