# Starter-Erweiterung V1 – Prüfbericht

Stand 21.10.2026. Ausgangspunkt main `2a1db9165f37866745a6641619e6d2658bde4216`. Keine neue Map, kein Worktree. Vorhandene 58 unversionierte Dateien im Schutzinventar `Saved/StarterExpansionV1/Initial.json` erfasst. Vollbackup 03492bd bleibt unverändert.

## Arbeitspaket 1: sichere Niederlagen-Speicherung

Rückkehr prüft nun die tatsächlich erfolgreiche Teleportierung; bei blockiertem Ziel ist nur ein ebenfalls kollisionsgeprüfter PlayerStart zulässig. Erst nach erfolgreicher Platzierung und vollständiger Teamheilung wird der abgeschlossene Zustand gespeichert. Der tatsächliche Rückkehrpunkt ist Teil desselben bestehenden SaveGame-Snapshots. Während Kampf und laufender Rückkehr bleiben Snapshots gesperrt.

Der macOS-Speichertransport schreibt die unveränderte SaveGame-Version 4 in eine eindeutige temporäre Nachbardatei, liest und deserialisiert diese zur Kontrolle und ersetzt den Slot über das atomare native `rename` der Apple-Plattformdateischnittstelle. Ein Fehlschlag entfernt nur die eigene temporäre Datei; der vorherige Slot wird nicht vorab gelöscht. Kein zusätzlicher dauerhafter Backupslot. Dies garantiert keinen Schutz vor sämtlichen Hardware-/Stromausfällen. Ladevalidierung und Migrationen 1–3 bleiben erhalten. Ein fehlgeschlagenes Autosave wird im Rückkehrhinweis angezeigt; die erfolgreiche Heilung bleibt erhalten.

Prüfungen:

- Mac Development Editor Build erfolgreich: `Saved/ProjectRefinement/StarterSaveBuild02/Result.json`.
- Vollständige Projekt-Automation: **70/70**, keine Testwarnungen oder Testfehler (`StarterSaveAutomation01`). Neue Prüfungen für die Rückkehrsperre und den geprüften atomaren Austausch einschließlich fehlgeschlagener Dateipromotion.
- Echter ClassicBattle-PIE-Niederlagenablauf mit vorhandener Kamera/UI: **bestanden**, `Saved/StarterExpansionV1/DefeatSave04/Result.json`. Speichern im Kampf abgewiesen; Rückkehr, volle KP, Autosave und identisches Reload von GUID/KP/XP/Rückkehrpunkt nachgewiesen. Die ersten Harness-Läufe benötigten eine Korrektur des Python-Checkpoint-Zugriffs und des GUID-Vergleichs; sie sind nicht als erfolgreiche Abnahmen gezählt.
- Ursprünglicher Dev-Spielstand nach jedem Lauf bytegenau wiederhergestellt: SHA-256 `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.
- ClassicBattle-Darstellung, Kampflogik, Maps, Originalmodelle und bisherige Animationen unverändert.

## Weitere beauftragte Arbeitspakete

Schiggy und Bisasam liegen als originale GLBs vor; Modellintegration und freie Oberweltbewegung sind in Bearbeitung. Dieser Zwischenstand meldet dafür noch keinen Abschluss. Die Gesamtprüfung mit Map Checks und vollständigem Gameplay-Fußlauf folgt nach deren Integration. Kontrollmedien und lokale Prüfdaten bleiben unter Saved und werden nicht hochgeladen. Physischer Switch-Pro-Test ist ausdrücklich kein Abschlusskriterium.
