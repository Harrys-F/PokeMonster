# Technisches Konzept – PokeMonster

## Projektstatus

PokeMonster befindet sich am Anfang der Entwicklung. Zunächst wird eine kleine, technisch saubere und spielbare Demo erstellt. Das Projekt soll schrittweise erweitert werden.

Harry übernimmt vor allem Planung, Entscheidungen und Tests. Codex und die angeschlossenen Entwicklungswerkzeuge sollen möglichst viel der technischen Umsetzung übernehmen.

## Zielplattform

- ausschließlich macOS
- Einzelspieler
- kein Multiplayer
- kein Ingame-Store
- zunächst kein iPhone- oder iPad-Build

Andere Plattformen werden erst berücksichtigt, wenn dies ausdrücklich neu beschlossen wird.

## Entwicklungsgerät

- MacBook Air mit Apple M4
- 16 GB gemeinsamer Arbeitsspeicher
- ungefähr 400 GB freier interner Speicher
- externe SSD vorhanden

Die aktive Projektentwicklung erfolgt auf der internen SSD. Externe Datenträger können später für zusätzliche Sicherungen, archivierte Builds und große Exportdateien verwendet werden.

## Entwicklungssoftware

- Unreal Engine 5.8.2
- Paper2D
- Enhanced Input
- C++
- Blueprints
- Rider als primäre Entwicklungsumgebung
- Xcode und Apple-Toolchain für macOS-Builds
- Blender für später benötigte Grafiken, Modelle oder vorbereitete Assets
- Git und Git LFS
- Codex und gegebenenfalls MCP-Anbindungen zur Automatisierung

RiderLink und MCP sind Hilfsmittel. Das Unreal-Projekt darf nicht technisch davon abhängig werden, dass diese Werkzeuge jederzeit verfügbar sind.

## Technische Architektur

Das Projekt verwendet eine Kombination aus C++ und Blueprints.

### C++

C++ soll bevorzugt verwendet werden für:

- grundlegende Spiellogik
- Datenstrukturen
- Speicher- und Ladesystem
- Kampfsystem-Grundlagen
- Kreaturen- und Attackendaten
- Inventar-Grundlagen
- wiederverwendbare Komponenten
- Systeme, die stabil und langfristig wartbar sein müssen

### Blueprints

Blueprints sollen bevorzugt verwendet werden für:

- Level- und Ereignislogik
- NPC-Konfiguration
- Dialogabläufe
- Animationen
- visuelle Effekte
- Benutzeroberflächen
- Balancing-Werte
- schnelle Prototypen und Tests

Systeme sollen nicht unnötig doppelt in C++ und Blueprints implementiert werden.

## Darstellung

- 2D-Top-Down-Perspektive
- Paper2D als technische Grundlage
- hochauflösende, sauber gezeichnete Grafiken
- moderne 2D-Darstellung statt absichtlich unscharfer Retro-Grafik
- übersichtliche und gut lesbare Spielwelt
- stimmungsvolle Beleuchtung und Effekte nur in einem für das MacBook sinnvollen Umfang

## Grafikprofile

Drei Profile sind vorgesehen:

### Medium

- Standardprofil für das MacBook Air
- flüssige Darstellung
- gute Bildqualität
- reduzierte Effekte
- begrenzte Bildrate
- möglichst effiziente Auslastung
- als Richtwert soll das Gerät nicht dauerhaft vollständig ausgelastet werden

### Hoch

- verbesserte Effekte und Darstellungsqualität
- höhere, aber weiterhin kontrollierte Auslastung

### Ultra

- höchste vorgesehene Darstellungsqualität
- nicht das primäre Entwicklungs- oder Testprofil
- darf das Gerät stärker beanspruchen

Die endgültigen Auflösungen, Bildraten und Scalability-Werte werden nach ersten Leistungstests festgelegt.

## Daten und Versionsverwaltung

Git wird für Quellcode, Konfiguration und Dokumentation verwendet. Git LFS wird für große Binärdateien verwendet, insbesondere:

- `*.uasset`
- `*.umap`
- `*.blend`
- `*.fbx`
- `*.wav`
- `*.psd`

Ordner wie `Binaries`, `DerivedDataCache`, `Intermediate` und `Saved` sollen normalerweise nicht versioniert werden.

Nach stabilen Meilensteinen soll ein Git-Commit erstellt und auf das Remote-Repository übertragen werden.

## Qualitätsregeln

Vor dem Abschluss eines Arbeitsschrittes soll Codex, soweit möglich:

- geänderte Dateien kontrollieren,
- Unreal-Projektdateien nicht unnötig von Hand verändern,
- C++ kompilieren,
- offensichtliche Fehler und Warnungen prüfen,
- vorhandene Tests ausführen,
- erklären, was Harry im Unreal Editor testen soll.

## Noch offene technische Entscheidungen

- genaue Struktur des Kampfsystems
- genaue Datenhaltung für Kreaturen und Attacken
- Speichersystem und Anzahl der Speicherstände
- konkrete Auflösungen und Bildraten der Grafikprofile
- Umfang der Unreal- und Blender-MCP-Automatisierung
- endgültige Ordnerstruktur innerhalb des Content-Ordners
