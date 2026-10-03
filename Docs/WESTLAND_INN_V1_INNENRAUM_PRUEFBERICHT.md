# Westland Inn V1 – L-Grundriss, Innenkamera und Innensteuerung

Stand: 2026-10-03. Umsetzung und Prüfung auf UE 5.8.2 / macOS, Blender 5.2.2 LTS. Kein Commit, kein Push, nichts gestaged.

## 1. Ausgangsstand

HEAD `36a8db1 Add interior building camera and controls`; Arbeitsbaum zu Beginn sauber. 655 versionierte Dateien vor Änderungen per SHA-256 erfasst.

## 2. Bereits vorhandenes Gasthaus

Vorhandener quadratischer Inn-Proof: Wandkörper 8,20 × 8,20 m, traufseitige Front, 218 Modulinstanzen, zwei Theken-Cubes, eigener Türschwellen-Cutaway ohne aktivierte Innenkamera. Vorhandene eigene Blenderquelle, acht bereits importierte generische Inn-Kit-Erweiterungen und gemeinsame Materialien wurden weiterverwendet. Kein zweites Gasthaus erstellt. Der ursprüngliche Prüfbericht bleibt ausdrücklich historisch.

## 3. Endgültige Abmessungen

| Teil | Maß |
|---|---|
| Nominaler Gesamtrahmen | 8,00 × 8,00 m mit ausgesparter 2 × 2-m-Außenecke |
| Äußere Wandhülle | 8,20 × 8,20 m |
| Rechteckiger Hauptkörper, Raster | 6,00 m tief × 8,00 m breit |
| Versetzter Rückflügel, Raster | 2,00 m tief × 6,00 m breit |
| Hauptdach | 6,60 × 8,60 m inklusive Überstand |
| Gesamtes Dach einschließlich Abschlussleisten | ca. 8,60 m tief × 8,74 m breit |
| Hauptfirst einschließlich Firstkappe | 5,752 m |
| Flügelfirst einschließlich Firstkappe | 5,085 m |
| Kaminoberkante | 6,080 m |
| Wandhöhe | 3,00 m |

Koordinaten: Gebäude lokales +X führt nach innen, +Y entlang der Front, +Z nach oben. Inn-Map-Ursprung (0,-1500,0) cm. Hauptbau X=-300…300, Y=-400…400 cm; Flügel X=300…500, Y=-200…400 cm.

## 4. Grundform

L-Grundriss: rechteckige Halle plus niedrigerer, um 1 m seitlich versetzter Rückflügel. Parallele Firste mit 8- bzw. 6-m-Spannweite erzeugen eine abgestufte Silhouette. Keine globale Gebäudeskalierung. Öffentliche Front mit versetztem Eingang, zehn Fenstern und markantem Flügelkamin; gleicher Putz-/Fachwerk-/Stein-/Holz-/Schindelstil wie Wohnhaus und Heilhaus.

## 5. Eingang

Echte freie Passage 1,60 × 2,15 m aus vorhandenem Door-Modul. Capsule bleibt 56 cm breit / 96 cm hoch; gerade zentriert 52 cm freie Breite pro Seite. Drei getrennte UCX-Körper für Türwand statt Collision über der Öffnung. Offenes Türblatt und Wetterschutz aus vorhandenen Modulen. Türmittelpunkt (-300,-1600,107,5) cm; Schwellenbox 40 × 160 × 215 cm, 4 cm Hysterese. Gerade und diagonale Passage im Capsule-Audit und PIE bestanden.

## 6–9. Module, Instanzen und Sonderteile

221 Architekturinstanzen aus 27 vorhandenen Modularten, **100 % Wiederverwendung des tatsächlich vorhandenen Stands**. Davon 194 Instanzen aus dem ursprünglichen 25-Modul-Kit (87,78 %) und 27 aus den acht schon vor dieser Aufgabe vorhandenen generischen Inn-Erweiterungen. Alle 33 Bibliotheksmodule geometrisch identisch zum Ausgangsstand; kein Mesh-Reimport. **0 neue allgemeine Module, 0 Sondermeshes, 0 neue FBX-/Material-/Content-Assets.** Zwei vorhandene Engine-Cubes markieren eine einfache Thekenreserve.

| Modul | Instanzen | Herkunft |
|---|---:|---|
| `WallSolid2m` | 5 | ursprüngliches Kit |
| `WallWindowArch2m` | 6 | ursprüngliches Kit |
| `WallWindowDouble2m` | 4 | ursprüngliches Kit |
| `GableHalf3m` | 2 | ursprüngliches Kit |
| `CornerPost3m` | 6 | ursprüngliches Kit |
| `VerticalPost3m` | 16 | ursprüngliches Kit |
| `HorizontalBeam2m` | 16 | ursprüngliches Kit |
| `DiagonalBrace1m` | 3 | ursprüngliches Kit |
| `StonePlinth1m` | 30 | ursprüngliches Kit |
| `RoofPanel1m` | 4 | ursprüngliches Kit |
| `RoofPanelEnd30cm` | 2 | ursprüngliches Kit |
| `EaveTrim1m` | 16 | ursprüngliches Kit |
| `GableTrimHalf3m` | 2 | ursprüngliches Kit |
| `RidgeCap1m` | 8 | ursprüngliches Kit |
| `WindowArch` | 6 | ursprüngliches Kit |
| `WindowDouble` | 4 | ursprüngliches Kit |
| `Chimney60cm` | 1 | ursprüngliches Kit |
| `Porch160cm` | 1 | ursprüngliches Kit |
| `Floor1m` | 62 | ursprüngliches Kit |
| `WallDoor160x2152m` | 1 | bereits vorhandene Inn-Variante |
| `DoorFrame160x215` | 1 | bereits vorhandene Inn-Variante |
| `DoorLeaf160x215` | 1 | bereits vorhandene Inn-Variante |
| `Threshold160cm` | 1 | bereits vorhandene Inn-Variante |
| `GableHalf4m` | 4 | bereits vorhandene Inn-Variante |
| `RoofPanel8mSpan1m` | 12 | bereits vorhandene Inn-Variante |
| `RoofPanel8mSpanEnd30cm` | 3 | bereits vorhandene Inn-Variante |
| `GableTrimHalf4m` | 4 | bereits vorhandene Inn-Variante |

## 10. Innenraum

60 m² nominale Bodenfläche: 48 m² Hauptgastraum plus 12 m² Flügel. Hauptfläche ca. 5,80 × 7,80 m zwischen geschlossenen Wandflächen. Sechs Meter breiter offener Übergang zum Flügel; keine unsichtbare Wand an der Verbindung. Eingang und freie diagonale Hauptlaufwege, links hinten kompakte Thekenreserve (2,60 m lang, Oberkante 0,96 m), rechts Sitzgruppenreserve. Flügel enthält Steinboden-Kaminreserve und Platz für späteren Hinterraum. Keine vollständige Einrichtung, NPCs, Geschäfts-/Übernachtungs- oder Questfunktion. Freier Bereich über dem Eingang für späteres Schild ist im JSON reserviert, ohne Dekoration zu bauen.

## 11. Innenkamera

2000 cm aus dem Wohnhaus-Proof zuerst vollständig zu Fuß getestet. In der tatsächlichen 3092 × 1794-PIE-Ansicht war der vordere Fuß-/Schwellenbereich knapp angeschnitten. Kontrollierter Vergleich mit **2200 cm (+10 %)**: mehr Rand am Eingang, Player dort und im Flügel vollständig lesbar. Gewählt: 2200 cm / Pitch -50° / gebäudelokaler Yaw 0° / FOV 35°, fester Fokus (100,-1500,80) cm. Oberkante der weit entfernten Rückwand liegt weiterhin am oberen Rand; die relevante begehbare Fläche und Player passen. Keine weitergehende Kameraänderung. Wohnhaus bleibt bei 2000 cm.

Außen unverändert: 2500 cm, Pitch -55°, Yaw -45°, FOV 35°, Lag 6 / max. 180 cm. Player unverändert 1,40 m sichtbare Körperhöhe und 210 cm/s.

## 12. Innensteuerung

Bestehende Player-Implementierung unverändert wiederverwendet. Während Eintrittsfade bleibt die äußere Basis; erst bei CutawayAmount 1 wird der Innen-Endpunkt gelatcht und danach der vorhandene 250-Grad/s-Blend ausgeführt (45° in 0,18 s). Innen W nach +X, S zum Eingang, A/D links/rechts. Während Austrittsfade bleibt Innenbasis; erst bei Amount 0 Rückkehr zur Außenbasis. Kein Input-Reset und kein zweites Input-System. Alle acht Richtungen normalisiert, bestehende Animationen/Skalierung/Fußpivot unverändert.

## 13. Explizite Occluder

82 explizit zugewiesene Inn-Actors. Beide Dächer, kameraseitige Vorderwand samt Fenstern/Fachwerk/Sockel/Eingangsdetails, Dachleisten/First, Kamin und die oberen Giebel am Hauptbau-/Flügelanschluss. Diese oberen Anschlussgiebel würden die Figur im Flügel verdecken. Untere Seiten-/Rückwände, Fenster und Fachwerk des Flügels bleiben sichtbar. Der hintere Flügelgiebel bleibt ebenfalls sichtbar. Kein pauschales Seitenwand-Ausblenden und kein automatisches Sichtsystem.

Exakte Actor-Labels:

```text
Inn_WallWindowArch2m_060
Inn_HorizontalBeam2m_061
Inn_VerticalPost3m_062
Inn_WindowArch_063
Inn_StonePlinth1m_064
Inn_StonePlinth1m_065
Inn_WallDoor160x2152m_066
Inn_HorizontalBeam2m_067
Inn_VerticalPost3m_068
Inn_WallWindowDouble2m_069
Inn_HorizontalBeam2m_070
Inn_VerticalPost3m_071
Inn_WindowDouble_072
Inn_StonePlinth1m_073
Inn_StonePlinth1m_074
Inn_WallWindowDouble2m_075
Inn_HorizontalBeam2m_076
Inn_VerticalPost3m_077
Inn_WindowDouble_078
Inn_StonePlinth1m_079
Inn_StonePlinth1m_080
Inn_CornerPost3m_148
Inn_CornerPost3m_149
Inn_GableHalf4m_157
Inn_GableTrimHalf4m_158
Inn_GableHalf4m_159
Inn_GableTrimHalf4m_160
Inn_GableHalf4m_161
Inn_GableTrimHalf4m_162
Inn_GableHalf4m_163
Inn_GableTrimHalf4m_164
Inn_GableTrimHalf3m_166
Inn_GableTrimHalf3m_168
Inn_RoofPanel8mSpan1m_169
Inn_EaveTrim1m_170
Inn_RoofPanel8mSpan1m_171
Inn_EaveTrim1m_172
Inn_RoofPanel8mSpan1m_173
Inn_EaveTrim1m_174
Inn_RoofPanel8mSpan1m_175
Inn_EaveTrim1m_176
Inn_RoofPanel8mSpan1m_177
Inn_EaveTrim1m_178
Inn_RoofPanel8mSpan1m_179
Inn_EaveTrim1m_180
Inn_RoofPanel8mSpanEnd30cm_181
Inn_RoofPanel8mSpanEnd30cm_182
Inn_RoofPanel1m_183
Inn_RoofPanel1m_184
Inn_RoofPanelEnd30cm_185
Inn_EaveTrim1m_186
Inn_EaveTrim1m_187
Inn_RoofPanel8mSpan1m_188
Inn_EaveTrim1m_189
Inn_RoofPanel8mSpan1m_190
Inn_EaveTrim1m_191
Inn_RoofPanel8mSpan1m_192
Inn_EaveTrim1m_193
Inn_RoofPanel8mSpan1m_194
Inn_EaveTrim1m_195
Inn_RoofPanel8mSpan1m_196
Inn_EaveTrim1m_197
Inn_RoofPanel8mSpan1m_198
Inn_EaveTrim1m_199
Inn_RoofPanel8mSpanEnd30cm_200
Inn_RoofPanel1m_201
Inn_RoofPanel1m_202
Inn_RoofPanelEnd30cm_203
Inn_EaveTrim1m_204
Inn_EaveTrim1m_205
Inn_RidgeCap1m_206
Inn_RidgeCap1m_207
Inn_RidgeCap1m_208
Inn_RidgeCap1m_209
Inn_RidgeCap1m_210
Inn_RidgeCap1m_211
Inn_RidgeCap1m_212
Inn_RidgeCap1m_213
Inn_DoorFrame160x215_214
Inn_DoorLeaf160x215_215
Inn_Porch160cm_217
Inn_Chimney60cm_218
```

## 14. L-Grundriss und Innenbereich

Minimale allgemeine C++-Ergänzung: optionale `InteriorRegions`, eine Vereinigungsmenge gebäudelokaler Boxen. Leere Liste erhält exakt das bisherige Ein-Box-Verhalten. Inn nutzt bei Root (100,-1500,150) cm zwei lokale Regionen: Zentrum (-100,0,0), Extent (310,410,200); Zentrum (300,100,0), Extent (110,310,200). Die offene Außenecke zählt nicht zum Innenbereich, die Verbindung hat keine Klassifikationslücke. Beide Komponenten bleiben NoCollision / ohne Gameplay-Overlaps. Bestehende Türschwellen-/Kamera-/Fade-/Steuerungslogik wurde nicht ersetzt.

## 15–17. Eintritt, Austritt und Umkehr

Fade 0,4 s beginnt an der tatsächlichen Schwelle. Kamera und Materialfade teilen denselben Fortschritt. Gehaltenes W blieb beim Eintritt bei 210 cm/s ohne Eingabeabbruch. Nach vollständigem Schwenk Innensteuerung korrekt. Austritt stellt Außenkamera und Außenbasis wieder her. Diagonaler Ein-/Austritt und Stillstand auf der Schwelle bestanden. Drei schnelle Umkehrzyklen ohne hängen gebliebenen Zustand.

Im letzten Lauf erreichten zwei schnelle Zyklen nur einen Teilfade, der dritte wegen eines längeren Frames kurz den vollständigen Innen-Endpunkt. Die Innenbasis bleibt dann beim Rückfade korrekt gelatcht. Eine zunächst zu enge Annahme des externen Auswertungsskripts („alle schnellen Zyklen bleiben Teilfade“) wurde an die tatsächliche Endpunktregel angepasst; dafür war keine Produktänderung nötig. Auch dieser Zyklus kehrte vollständig nach außen zurück.

## 18. Vollständiger PIE-Fußweg

Regulärer PlayerStart, **kein Spawn-Override, kein SetActorLocation/Transform des Players, keine Test-Teleports**. Normalisierte digitale Richtungsvektoren über die bestehende Enhanced-Input-Action im laufenden PIE, normale CharacterMovement-/Collision-Simulation. Wohnhaus betreten/verlassen → Verbindungsweg → Gasthausfassade → W-Eintritt → W/A/S/D → vier Diagonalen → gesamte Halle → Flügel/Kaminreserve → Thekenumgang → S-Austritt → diagonaler Eintritt/Austritt → drei schnelle Umkehrungen → Schwellenpause → Rückweg zum Start.

Finaler Lauf: **1238 aufgezeichnete Frames, 59 abgeschlossene Prüfschritte**. Gehaltenes W im Eintritt 210,00 cm/s; alle acht zugehörigen Flipbooks korrekt. 82 Occluder exakt gemäß Bauplan ausgeblendet; alle übrigen Inn-Module sichtbar. Playerdarstellung im Hauptgastraum, Flügel und Eingangsbereich visuell geprüft. Außerhalb ist wegen unveränderter folgender Kamera unmittelbar vor der Fassade nicht immer das komplette Dach im Bild; keine Kamera-/FOV-Aufweitung dafür vorgenommen. Der Bau ist merklich größer als das Wohnhaus, bleibt aber auf denselben Modulmaßstab bezogen.

## 19. Build, Tests und Audits

- Finaler UE-5.8.2-Development-Editor-Build erfolgreich, keine Compile Errors.
- **37/37 PokeMonster-Automationstests erfolgreich, 0 Warnungstests, 0 Fehler.** Bestehende Player-/BuildingInteriorCamera-/HealingHouse- und Gameplaytests bleiben grün.
- Neuer `PokeMonster.Building.Inn.CameraAndFootprint` prüft Box-Rückwärtskompatibilität, Hauptbau/Flügel/Naht/Außenecke, Gebäude-Rotation, Türbereich, gespeicherte Kamera-/Region-/Fade-Konfiguration und tatsächliche gebäudespezifische Occluder-Zuordnung. Bestehender BuildingInteriorCamera-Test prüft Übergänge, Endpunkt-Basis, Umkehr und Acht-Wege-Normalisierung.
- Map Check: **0 Fehler / 0 Warnungen**.
- 33 Meshes mit Bounds-Abgleich (3-mm-Toleranz), UCX-Anzahl und 39 vollständig zugewiesenen maskierten Materialslots erfolgreich geprüft.
- 15 freie Capsule-Routensegmente, diagonale Türpassage sowie Front-, Rück-, Seiten-, Theken- und Außenecken-Collision geprüft.
- Blenderquelle ausdrücklich gespeichert, wieder geöffnet, 33 Module manifold, Origins/Rotation/Scale angewandt, vollständige Materialien, keine externen Bibliotheken. Keine FBX-Ausgabe nötig.
- Drei redundante Dach-Endstreifen am Anschluss entfernt, um unnötige coplanare Überlappung zu vermeiden; nur Instanzen, keine Meshänderung.
- Alle 645 nicht betroffenen Ausgangsdateien bytegleich. Originalkit, Mesh-/Materialassets, Wohnhaus-Bauplan, Player, Gameplay, Healing House V3 und Dev_TestMap unverändert. Nicht-Inn-Map-Actors inklusive Cottage-Transforms, Assets, Collision und Kamera-/Occluder-Konfiguration vor/nach Reconfiguration gleich.

Prüfartefakte, Rohlogs, Screenshots und Skripte für Input-/Frameauswertung liegen ausschließlich im ignorierten `Saved/WestlandInnCamera` bzw. `/private/tmp/WestlandInnCamera`; sie gehören nicht in Git. Verwendeter Skill: `build-3d-game-rooms` für lokale Architektur-/Öffnungs-/Quellen-/Sichtaudit-Grundsätze. Kein Meshy, externer Download oder neuer Export-/Deployment-Schritt. Die generischen Skill-Paketvorlagen sind keine behauptete menschliche Freigabe; maßgeblich sind die oben beschriebenen tatsächlichen Unreal-/Blender-Prüfungen.

## 20. Sämtliche Dateien

10 bestehende Dateien geändert, 4 Dateien neu:

- `Art/Architecture/Westland/Buildings/WL_Inn_V1.json`
- `Art/Architecture/Westland/Source/WestlandInn_V1.blend`
- `Content/Maps/Dev_BuildingKitTestMap.umap`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`
- `Docs/WESTLAND_INN_V1_PRUEFBERICHT.md`
- `Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp`
- `Source/PokeMonster/World/PokeMonsterBuildingCutaway.h`
- `Tools/Blender/ReviewWestlandInnV1.py`
- `Tools/ValidateWestlandInnV1.py`
- `Docs/WESTLAND_INN_V1_INNENRAUM_PRUEFBERICHT.md`
- `Source/PokeMonster/Tests/PokeMonsterInnCameraTest.cpp`
- `Tools/Blender/RecomposeWestlandInnV1.py`
- `Tools/ConfigureWestlandInnV1.py`

Die Blenderquelle ist `Art/Architecture/Westland/Source/WestlandInn_V1.blend`; der vollständige lokale Pfad lautet `/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Architecture/Westland/Source/WestlandInn_V1.blend`.

## 21. Diff-Prüfung

`git diff --check` erfolgreich, keine Ausgabe. Nach Fertigstellung dieses Berichts nochmals geprüft.

## 22. Git-Status und Sicherungspunkt

```text
 M Art/Architecture/Westland/Buildings/WL_Inn_V1.json
 M Art/Architecture/Westland/Source/WestlandInn_V1.blend
 M Content/Maps/Dev_BuildingKitTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Docs/WESTLAND_INN_V1_PRUEFBERICHT.md
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp
 M Source/PokeMonster/World/PokeMonsterBuildingCutaway.h
 M Tools/Blender/ReviewWestlandInnV1.py
 M Tools/ValidateWestlandInnV1.py
?? Docs/WESTLAND_INN_V1_INNENRAUM_PRUEFBERICHT.md
?? Source/PokeMonster/Tests/PokeMonsterInnCameraTest.cpp
?? Tools/Blender/RecomposeWestlandInnV1.py
?? Tools/ConfigureWestlandInnV1.py
```

Nach eigener Sichtprüfung ist dieser getestete Stand ein sinnvoller Sicherungspunkt. Ausschließlich die oben genannten Projektdateien lassen sich im Projektordner mit folgendem Befehl gezielt stagen (hier **nicht ausgeführt**):

```sh
git add -- \
  Art/Architecture/Westland/Buildings/WL_Inn_V1.json \
  Art/Architecture/Westland/Source/WestlandInn_V1.blend \
  Content/Maps/Dev_BuildingKitTestMap.umap \
  Docs/ENTSCHEIDUNGEN.md \
  Docs/TECHNIK.md \
  Docs/WESTLAND_INN_V1_PRUEFBERICHT.md \
  Source/PokeMonster/World/PokeMonsterBuildingCutaway.cpp \
  Source/PokeMonster/World/PokeMonsterBuildingCutaway.h \
  Tools/Blender/ReviewWestlandInnV1.py \
  Tools/ValidateWestlandInnV1.py \
  Docs/WESTLAND_INN_V1_INNENRAUM_PRUEFBERICHT.md \
  Source/PokeMonster/Tests/PokeMonsterInnCameraTest.cpp \
  Tools/Blender/RecomposeWestlandInnV1.py \
  Tools/ConfigureWestlandInnV1.py
```

Kein Commit und kein Push durchgeführt. Für die eigene Prüfung die gespeicherte `Dev_BuildingKitTestMap` neu laden. Ein bereits vor dem C++-Build laufender Editor muss für die neue optionale Region-Struktur neu gestartet werden; dessen ursprüngliche Sitzung wurde nicht beendet.
