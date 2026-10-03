# Westland Inn V1 – Prüfbericht


> Historischer Erst-Proof: Die quadratische Komposition und reine Box-Konfiguration wurden ersetzt. Aktueller L-Grundriss, Innenkamera und Steuerungsprüfung: [WESTLAND_INN_V1_INNENRAUM_PRUEFBERICHT.md](WESTLAND_INN_V1_INNENRAUM_PRUEFBERICHT.md).

Stand: 03.10.2026. Zweiter Architektur-Proof für Westland Building Kit V1; keine neuen Gameplay-Systeme, kein Commit, Push oder Staging.

## Ausgangsstand und Architektur

1. **Ausgangs-HEAD:** `b819214 Add Westland building kit V1`; `git status --short` zu Beginn ohne Ausgabe. 626 bestehende Dateien wurden per SHA-256 gegen den Ausgangsstand erfasst. Relevante AGENTS-/Grafik-/Technik-/Entscheidungsvorgaben und Kit-V1-Bericht wurden gelesen. Die vorhandene Kitquelle wurde im getrennten Hintergrundprozess geöffnet; der ursprüngliche Wohnhaus-/Asset-/Collision-Audit wurde vor dem Ergänzen bestanden.
2. **Gasthausmaße:** 8,00×8,00-m-Konstruktionsraster; Außenwandhülle ca. 8,20×8,20 m, Dach einschließlich Überständen ca. 8,60×8,60 m. Wandhöhe 3 m, First nominal 5,667 m, einschließlich Firstmodul ca. 5,752 m. Kamin maximal ca. 6,08 m. Die Hauptform liegt zwischen dem 6,20×6,20-m-Wohnhaus und dem öffentlichen Heilhaus V3 (9,00×9,30 m, First 6,40 m). Keine globale Skalierung.
3. **Grundform:** Einfache quadratische Haupthalle mit kleiner vorhandener Eingangshaube. Die Traufseite bildet die öffentliche Front; der First läuft quer zum Wohnhausfirst. Versetzter Eingang, drei Frontfenster, weitere Seiten-/Rückfenster und rückwärtiger Kamin sorgen für eine andere Silhouette und Nutzung. Keine Heilhauskopie und keine skalierte Wohnhauskomposition. Ein L-Flügel wäre zusätzliche Komplexität ohne erforderliche Funktion im ersten Proof; daher nicht umgesetzt. Ein späteres Schild hat Platz unter der Fronttraufe neben dem Eingangsbereich; noch kein Schild/Dressing erzeugt.
4. **Tür:** Freie Passage **160×215 cm**, 20-cm-Wandtiefe, Fußpunkt bei lokal (-4,-1,0) m beziehungsweise Welt (-400,-1600,0) cm. Türblatt 158×210 cm, Scharnier-Pivot, nach außen 90° geöffnet; Rahmen und Türblatt ohne Collision. Die unveränderte 56-cm-Capsule lässt nominell 52 cm je Seite. Der öffentliche Eingang ist sichtbar großzügiger als die Wohnhaustür 130×200 cm.

## Exakte Wiederverwendung

5./6./7. **Module und Instanzhäufigkeiten:** 218 Modulinstanzen, davon 186 aus 15 unveränderten V1-Modularten (**85,32 %**), 32 aus acht neuen Varianten (**14,68 %**). 23 Modularten werden insgesamt verwendet. 38.144 Dreiecke in den platzierten Modulinstanzen; die acht neuen Module zusammen enthalten 2.712 Dreiecke. Die zwei einfachen Engine-Cubes für den Thekenblockout kommen separat hinzu (24 Dreiecke).

Alle Namen haben das Meshpräfix `SM_WL_`. Nullwerte dokumentieren ausdrücklich, welche V1-Module nicht verwendet wurden.

| Modul | Herkunft | Inn-Instanzen |
|---|---|---:|
| WallSolid1m | V1 unverändert | 0 |
| WallSolid2m | V1 unverändert | 6 |
| WallWindowArch2m | V1 unverändert | 5 |
| WallWindowDouble2m | V1 unverändert | 4 |
| WallDoor2m | V1 unverändert | 0 |
| GableHalf3m | V1 unverändert | 0 |
| CornerPost3m | V1 unverändert | 4 |
| VerticalPost3m | V1 unverändert | 12 |
| HorizontalBeam2m | V1 unverändert | 18 |
| DiagonalBrace1m | V1 unverändert | 4 |
| StonePlinth1m | V1 unverändert | 30 |
| RoofPanel1m | V1 unverändert | 0 |
| RoofPanelEnd30cm | V1 unverändert | 0 |
| EaveTrim1m | V1 unverändert | 16 |
| GableTrimHalf3m | V1 unverändert | 0 |
| RidgeCap1m | V1 unverändert | 8 |
| DoorFrame130x200 | V1 unverändert | 0 |
| DoorLeaf130x200 | V1 unverändert | 0 |
| WindowArch | V1 unverändert | 5 |
| WindowDouble | V1 unverändert | 4 |
| WindowRound | V1 unverändert | 0 |
| Chimney60cm | V1 unverändert | 1 |
| Porch160cm | V1 unverändert | 1 |
| Floor1m | V1 unverändert | 68 |
| Threshold130cm | V1 unverändert | 0 |
| WallDoor160x2152m | Neue generische Variante | 1 |
| DoorFrame160x215 | Neue generische Variante | 1 |
| DoorLeaf160x215 | Neue generische Variante | 1 |
| Threshold160cm | Neue generische Variante | 1 |
| GableHalf4m | Neue generische Variante | 4 |
| RoofPanel8mSpan1m | Neue generische Variante | 16 |
| RoofPanel8mSpanEnd30cm | Neue generische Variante | 4 |
| GableTrimHalf4m | Neue generische Variante | 4 |

Die acht Erweiterungen sind notwendig, weil Wiederholung weder aus einer 130×200-cm-Tür eine 160×215-cm-Passage noch aus einer 6-m-Dachspannweite eine passende 8-m-Spannweite erzeugt. Fenster/Türen werden nicht gestreckt. Öffentliche Türwand, Rahmen, Blatt und Schwelle sind allgemeine Größenvarianten; Halbgiebel, Dachstreifen in 1 m/30 cm und Giebelabschluss standardisieren die zusätzliche 8-m-Spannweite. Raster, 2:3-Neigung, Montageanker, Materialslots und Exportachsen bleiben kompatibel. Keine gasthauseigene Einmal-Wand und kein monolithischer Hausmesh.

Alle 25 ursprünglichen Blender-Modulgeometrien und ihre Materialslotnamen wurden per Geometriehash innerhalb der neuen Quelle gegen die geladene Kit-V1-Quelle geprüft. Die ursprüngliche `.blend`, FBXs, 25 Unreal-Meshes und sieben Westland-Materialassets bleiben unverändert. Die neue Quelle enthält lokale Kopien/Instanzen ohne externe Blender-Bibliothekslinks; sie wird ausdrücklich gespeichert, lesend wieder geöffnet und vor dem Export geprüft. Nur die acht neuen Varianten werden exportiert/importiert. Unreal verwendet alle sieben bisherigen Westland-Materialien direkt weiter; keine neuen Material- oder Texturassets.

8. **Sonderteile:** Keine individuellen Gasthaus-Architekturmeshes. Zwei skalierte Engine-Cubes markieren Thekenkörper und Arbeitsplatte; sie werden nicht als Sondermesh exportiert. Zwei vorhandene horizontale Balken bilden den Thekenabschluss, vier vorhandene Bodenmodule mit unverändertem Steinmaterial markieren den Kaminbereich. Dies ist ein räumlicher Blockout, keine komplette Einrichtung. Keine NPCs, Handel, Übernachtung, Quest, VFX oder neue Lichtstimmung.
9. **Innenraum:** Lichte Halle ca. **7,80×7,80 m**, etwa 81 % mehr Grundfläche als im Wohnhaus. Eingang und freie Hauptfläche sind verbunden; Tisch-/Bankreserven im mittleren/vorderen Bereich, Theke rückseitig rechts, Steinfläche für späteren Kamin rückseitig links. Theke ca. 4 m lang, Oberkante 96 cm; Weg hinter der Theke ca. 92 cm breit und normal erreichbar. Keine Tile-Korridore. Noch kein Hinterraum, Obergeschoss oder finale Möblierung.
10. **Cutaway:** Bestehende `PokeMonsterBuildingCutaway`-Klasse unverändert. Eigener Actor pro Gebäude. Gasthaus-Schwellenbox **40×160×215 cm**, Zentrum **(-400,-1600,107,5) cm**, lokale +X-Richtung nach innen. 4-cm-Hysterese und **0,4-s-Fade**. Dach, Front und tatsächliche kameraseitige +Y-Fassade samt Giebel/Fachwerk/Fenstern werden ausgeblendet; Hintergrundwände bleiben sichtbar. Kein Annäherungs-Fade. CPD 0 und vorhandene maskierte Materialien unverändert.
11. **Collision:** Türwand drei getrennte UCX-Convex-Körper (links/rechts/Lintel), Schwelle ein Körper. Bisherige Wand-/Bodenkollisionen werden unverändert verwendet. Kleine Dekoration, Dach und Galerie NoCollision; die Theken-Engine-Cubes blockieren. Blocking ignoriert Visibility für die bestehende Interaktion. Wände bleiben bei Cutaway physisch aktiv. Der Audit prüft freie Capsule-Wege inklusive Verbindung, Eingang, diagonaler Passage, Hauptfläche und Thekenumgang sowie Blocking von Front-/Rückwand, Fensterwand und Theke.
12. **Wirkung neben dem Wohnhaus:** Wohnhaus, Gasthaus und Modulübersicht bleiben getrennt. Gasthauszentrum (0,-1500,0) cm, Wohnhaus weiterhin (0,0,0). Die breitere Trauffront, größere Dachfläche und neun statt drei Fenster vermitteln eine öffentliche Halle; gleiche Materialien/Fachwerk-/Sockel-/Schindelsprache erhält die Westland-Zugehörigkeit. Beide sind normal begehbar. Die 148 Wohnhausinstanzen samt Transforms wurden unverändert bestätigt. Nur Testgelände und Verbindungs-/Eingangsweg wurden für die größere Prüfanordnung ergänzt; keine Dorfgestaltung.
13. **2500-cm-Spielkamera:** Abstand 2500 cm, FOV 35°, Winkel (-55°,-45°,0°), Lag-Geschwindigkeit 6/maximal 180 cm, Player 140 cm und 210 cm/s unverändert. Die Spielansicht ist maßgeblich, Blender-Renders dienen nur Quell-/Geometrieprüfung. Tür und Fenster sind klar größer/öffentlicher als beim Wohnhaus. Die weite Halle, Theke und Kaminreserve bleiben unter Cutaway lesbar. Nahe der Fassade passt das volle Dach wie schon bei den anderen Architektur-Proofs nicht komplett in den playerzentrierten Ausschnitt; Kamera und FOV werden dafür nicht verändert. Keine Aussage über finale Beleuchtung oder vollständige Gasthausausstattung.

## Prüfung, Arbeitskorrekturen und Erhalt

14. **PIE-Fußweg:** **Vollständiger finaler Durchlauf bestanden**, normaler Außenstart und Rückkehr bei (-944,71,-3,44,46,34) cm. Livewerte: SpringArm 2500 cm, FOV 35°, Rotation (-55°,-45°,0°), Lag 6/maximal 180 cm, Bewegung 210 cm/s. Ablauf: normaler PlayerStart → Wohnhaus ansehen und separat betreten/verlassen → Verbindungsweg → Gasthausfront → gerade durch Tür → Hauptfläche → diagonale Wege zu Theke/Kaminreserve → hinter Theke → diagonal hinaus → diagonal hinein → gerade hinaus → zurück zum Wohnhausstart. Keine Teleports oder Spawn-Overrides.
15. **Map Check / Audits / Tests:** Map Check der gespeicherten, neu geladenen und nach finalem PIE erneut geprüften Map **0 Fehler, 0 Warnungen**. Blender prüft 33 Meshmodule auf manifold Geometrie, Origins/Scale/Rotation, Materialien und fehlende externe Links; V1-Geometriehashes identisch. Unreal prüft alle 33 Modulbounds (3-mm-Toleranz), 39 Materialslots, gespeicherte einfache/Convex-Collision, Instanzpositionen/-counts, freie/blockierende Laufwege und exakte Cutaway-Occluder. Originaler Wohnhaus-Audit nach dem Ergänzen ebenfalls bestanden. Kein C++ verändert; kein Build notwendig. Der gesamte bestehende PokeMonster-Automationstestbestand wurde in einem frischen Null-RHI-Prozess geprüft: **35 erfolgreich, 0 fehlgeschlagen, 0 mit Warnungen, 0 nicht ausgeführt**, Exit-Code 0. Player Foundation/ScaleCalibration, HealingHouse, Battle, Encounter, Inventory, Quest und Save bleiben grün. Neue Python-AST-, JSON- und Text-Whitespace-Prüfungen ebenfalls bestanden.

Tatsächlich gefundene Arbeitsfehler und Korrekturen:

- Die erste Transform-Erhaltungsprüfung verglich Python-Struct-Strings einschließlich Speicheradressen. Sie schlug trotz identischer numerischer Werte an; korrigiert auf numerische Position/Rotation/Scale. Vor dem Speichern wurden sämtliche Cottage-Transforms gegen den ursprünglichen Bauplan geprüft.
- Nach einem Level-Reload konnte der Slate-Konsolentext einen Eingaberest enthalten. Die Konsoleneingabe wird nun vor jedem Prüfaufruf kontrolliert geleert; Ausführungsmarker werden abgewartet. Die neu geladene Map und beide Audits wurden danach eindeutig geprüft.
- Ein erster Fußlauf verlor unterwegs den Viewport-Fokus. An derselben Position funktionierten normale Tasten nach erneutem Fokussieren; keine Collision und kein Teleport. Der finale Test wurde vollständig vom normalen Start wiederholt und bestanden.
- Der erste Inn-Cutaway nahm die falsche Y-Fassade aus der Cottage-Vorlage an. Die tatsächliche Spielansicht zeigte einen stehenbleibenden Vordergrundgiebel. Ausschließlich die neue Inn-Occluder-Konfiguration wurde auf die kameraseitige +Y-Fassade korrigiert; keine Änderung des Cutaway-Codes oder der Wohnhauskonfiguration.

Arbeitsnachweise, Renders, Runtime-Audits, PIE-Bilder und Automationsergebnisse liegen unter dem bereits ignorierten `Saved/WestlandInnV1`; lokale Logs/Helper unter `/private/tmp/WestlandInnV1`. Diese gehören nicht ins Repository. Dauerhafte Dateien sind Blenderquelle, Bauplan/Erweiterungsdefinition, acht FBX-Reimport-Quellen, acht neue Meshassets, Autorenwerkzeuge und Dokumentation.

16. **25 neue Dateien und 3 geänderte bestehende Dateien**; die vollständige Liste steht unten. Die anderen **623 von 626** Ausgangsdateien sind SHA-256-bytegleich. Insbesondere Kit-V1-Quelle, bestehende Westland-Meshes/Materialien, Cottage-Bauplan, Healing House V3, Dev_TestMap und C++ bleiben unverändert.
17. **`git diff --check`: Exit-Code 0, ohne Ausgabe.**
18. Abschließendes `git status --short` steht unten. HEAD weiterhin `b819214`. Kein Staging, Commit oder Push.

## Vollständige Dateiliste

Geänderte bestehende Dateien:

- `Content/Maps/Dev_BuildingKitTestMap.umap`
- `Docs/ENTSCHEIDUNGEN.md`
- `Docs/TECHNIK.md`

Neue Dateien:

- `Art/Architecture/Westland/Buildings/WL_Inn_V1.json`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_DoorFrame160x215.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_DoorLeaf160x215.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_GableHalf4m.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_GableTrimHalf4m.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_RoofPanel8mSpan1m.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_RoofPanel8mSpanEnd30cm.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_Threshold160cm.fbx`
- `Art/Architecture/Westland/Exports/InnExtensions/SM_WL_WallDoor160x2152m.fbx`
- `Art/Architecture/Westland/Source/WestlandInn_V1.blend`
- `Art/Architecture/Westland/WestlandBuildingKit_InnExtensions_V1.json`
- `Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorFrame160x215.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorLeaf160x215.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_GableTrimHalf4m.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpan1m.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpanEnd30cm.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Threshold160cm.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_GableHalf4m.uasset`
- `Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallDoor160x2152m.uasset`
- `Docs/WESTLAND_INN_V1_PRUEFBERICHT.md`
- `Tools/Blender/BuildWestlandInnV1.py`
- `Tools/Blender/ExportWestlandInnV1.py`
- `Tools/Blender/ReviewWestlandInnV1.py`
- `Tools/ImportWestlandInnV1.py`
- `Tools/ValidateWestlandInnV1.py`

## Abschließender Git-Status

```text
 M Content/Maps/Dev_BuildingKitTestMap.umap
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
?? Art/Architecture/Westland/Buildings/WL_Inn_V1.json
?? Art/Architecture/Westland/Exports/InnExtensions/
?? Art/Architecture/Westland/Source/WestlandInn_V1.blend
?? Art/Architecture/Westland/WestlandBuildingKit_InnExtensions_V1.json
?? Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorFrame160x215.uasset
?? Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorLeaf160x215.uasset
?? Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_GableTrimHalf4m.uasset
?? Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpan1m.uasset
?? Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpanEnd30cm.uasset
?? Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Threshold160cm.uasset
?? Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_GableHalf4m.uasset
?? Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallDoor160x2152m.uasset
?? Docs/WESTLAND_INN_V1_PRUEFBERICHT.md
?? Tools/Blender/BuildWestlandInnV1.py
?? Tools/Blender/ExportWestlandInnV1.py
?? Tools/Blender/ReviewWestlandInnV1.py
?? Tools/ImportWestlandInnV1.py
?? Tools/ValidateWestlandInnV1.py
```

Der bestandene Architektur-/Fußweg-/Automationstest ist ein sinnvoller späterer Git-Sicherungspunkt. Es wurde nichts gestaged. Für ausschließlich diese 28 Projektdateien kann nach eigener Prüfung folgender Befehl verwendet werden; er wurde nicht ausgeführt:

```sh
git add -- \
  Content/Maps/Dev_BuildingKitTestMap.umap \
  Docs/ENTSCHEIDUNGEN.md \
  Docs/TECHNIK.md \
  Art/Architecture/Westland/Buildings/WL_Inn_V1.json \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_DoorFrame160x215.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_DoorLeaf160x215.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_GableHalf4m.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_GableTrimHalf4m.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_RoofPanel8mSpan1m.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_RoofPanel8mSpanEnd30cm.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_Threshold160cm.fbx \
  Art/Architecture/Westland/Exports/InnExtensions/SM_WL_WallDoor160x2152m.fbx \
  Art/Architecture/Westland/Source/WestlandInn_V1.blend \
  Art/Architecture/Westland/WestlandBuildingKit_InnExtensions_V1.json \
  Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorFrame160x215.uasset \
  Content/Environment/Architecture/Westland/Meshes/Doors/SM_WL_DoorLeaf160x215.uasset \
  Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_GableTrimHalf4m.uasset \
  Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpan1m.uasset \
  Content/Environment/Architecture/Westland/Meshes/Roof/SM_WL_RoofPanel8mSpanEnd30cm.uasset \
  Content/Environment/Architecture/Westland/Meshes/Structural/SM_WL_Threshold160cm.uasset \
  Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_GableHalf4m.uasset \
  Content/Environment/Architecture/Westland/Meshes/Walls/SM_WL_WallDoor160x2152m.uasset \
  Docs/WESTLAND_INN_V1_PRUEFBERICHT.md \
  Tools/Blender/BuildWestlandInnV1.py \
  Tools/Blender/ExportWestlandInnV1.py \
  Tools/Blender/ReviewWestlandInnV1.py \
  Tools/ImportWestlandInnV1.py \
  Tools/ValidateWestlandInnV1.py
```

Prüf-/Screenshot-/Log-Dateien unter `Saved/WestlandInnV1` und `/private/tmp/WestlandInnV1` sind ausdrücklich nicht enthalten. Kein Commit und kein Push durchgeführt.
