# Entscheidungsprotokoll – PokeMonster

Dieses Dokument hält dauerhafte Entscheidungen, offene Punkte und ersetzte Planungen fest.

## Statusbegriffe

- **Beschlossen:** gilt für die weitere Entwicklung
- **Vorläufig:** aktuelle Arbeitsrichtung, kann geändert werden
- **Offen:** noch keine Entscheidung
- **Ersetzt:** frühere Planung, die nicht mehr gilt

## 2026-09-09 – Grundlegende Spielwelt

**Status: Beschlossen**

- Das Spiel verbindet Kreaturensammeln und Kämpfe mit einer eigenständigen Fantasywelt.
- Die Atmosphäre darf von Mittelerde inspiriert sein.
- Orte, Namen, Karten und Geschichte werden eigenständig gestaltet.
- Gewünschte regionale Stimmungen umfassen Hügelland, uralten Wald, Hochland, Gebirge, monumentale Städte, dunkles Grenzland und Vulkanlandschaft.

## 2026-09-09 – Freund-/Gegenfigur

**Status: Beschlossen**

- Die klassische einfache Rivalenfigur wird durch eine komplexere Freund-/Gegenfigur ersetzt.
- Sie entwickelt sich parallel zum Spieler, reist teilweise mit und führt eigene Untersuchungen durch.
- Sie fordert zunehmend mehr Kontrolle über Kreaturen.
- Ein Wendepunkt entsteht, als sie in einer gefährlichen Situation von einer Kreatur gerettet wird.

## 2026-09-09 – Entwicklungen

**Status: Beschlossen**

- Normale Levelentwicklungen bleiben grundsätzlich erhalten.
- Tauschentwicklungen werden nicht zu einfachen Levelentwicklungen.
- Sie benötigen Mindestlevel, passenden Ort und besondere Handlung oder Prüfung.
- Kadabra, Maschock, Georok und Alpollo dienen als erste Beispiele.
- Konkrete Level und Auslöser bleiben vorläufig.

## 2026-09-10 – Kreaturenumfang

**Status: Beschlossen für den privaten Prototyp**

- Verwendet werden sollen Kreaturen der Generationen 1 und 2.
- Der theoretische Gesamtumfang beträgt maximal 251.
- Die erste Demo verwendet nur eine kleine Auswahl.
- ROM-Dateien und daraus extrahierte Assets werden nicht verwendet.

## 2026-09-10 – Umstieg von 3D auf 2D

**Status: Ersetzt beziehungsweise neu beschlossen**

Frühere Planung:

- 3D-Spiel beziehungsweise größere Open-World-Ausrichtung

Neue gültige Planung:

- modernes 2D-Top-Down-Spiel
- Paper2D in Unreal Engine
- hochauflösende, saubere Grafiken
- klassische Lesbarkeit mit moderner Darstellung
- zuerst eine kleine Demo statt einer großen offenen Welt

## 2026-09-16 – Technische Grundlage

**Status: Beschlossen**

- Unreal Engine 5.8.2
- macOS als einzige Zielplattform
- MacBook Air M4 mit 16 GB gemeinsamem Arbeitsspeicher als Entwicklungs- und Testgerät
- Kombination aus C++ und Blueprints
- Paper2D und Enhanced Input
- Rider und Xcode für die Entwicklung
- Git und Git LFS für Versionsverwaltung und Sicherung
- Codex soll einen großen Teil der technischen Arbeit übernehmen
- Harry plant, entscheidet und testet

## 2026-09-16 – Leistungsprofile

**Status: Vorläufig beschlossen**

Es werden drei Grafikprofile vorbereitet:

- Medium
- Hoch
- Ultra

Medium ist das primäre effiziente Profil für das MacBook Air. Genaue Auflösung, Bildrate und Scalability-Werte werden erst nach Leistungstests festgelegt.

## Aktuell offene Entscheidungen

- endgültiger Spielname
- Namen der Welt, Regionen und Städte
- genaue Hauptgeschichte
- Hauptfigur und Motivation
- Arenen oder eigenes Prüfungssystem
- endgültige Fangmechanik
- endgültiges Kampfsystem
- sichtbare oder zufällige Begegnungen
- linearer Weg oder alternative Routen
- genaue Demo-Kreaturen
- endgültige Attackenverwaltung
- genaue Schnellreise- und Weltfähigkeiten
- konkreter Grafikstil und Auflösung
- Musik- und Soundkonzept
