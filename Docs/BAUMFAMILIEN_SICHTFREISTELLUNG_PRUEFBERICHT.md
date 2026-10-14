# Sichtfreistellung aller sichtbaren Baumfamilien

Stand: 13.10.2026, Unreal Engine 5.8.2/macOS. Ausgangs-HEAD `9491824 Update gameplay camera and player sight visibility`, Branch `main`. Anfangs ausschließlich `?? Art/Characters/NPCs/`; diese Nutzerarbeit bleibt erhalten. Keine Staging-, Commit- oder Push-Aktion.

## Tatsächlicher Bestand der Testwelt

Geprüfte aktive Karte: `/Game/Maps/Dev_TestMap_VisualV2`, Datei `Content/Maps/Dev_TestMap_VisualV2.umap`.

| Sichtbare Familie | Mesh | Anzahl | Vorher | Jetzt |
| --- | --- | --- | --- | --- |
| Alte V3-Eiche | `SM_WLA_OakAncient_V3` | 41 | Reveal für Rinde und Kronen | unverändert unterstützt |
| Birke | `SM_WLA_Birch_A` | 4 | kein Reveal | alle vier Materialslots unterstützt |

Damit sind **alle zwei tatsächlich sichtbaren Baumfamilien** dieser Testmap angebunden: **45 Komponenten und 98 Materialslots**. Der vollständige Actor-/Materialaudit liegt in `Saved/TreeReveal_20261013/SceneBefore.json`.

Die erhaltenen alten `S_Oak`-Sprites (35) und primitiven Kegelobjekte (58 Cone-Komponenten) sind im Spiel unsichtbar. Sie wurden nicht aktiviert, ersetzt, gelöscht oder zusätzlich mit Reveal versehen. Weitere sichtbare Baum-Meshfamilien wurden im Audit nicht gefunden. Dies ist keine Abnahme sämtlicher Bäume anderer Projektmaps.

## Umsetzung ohne Neuaufbau der Reveal-Materialien

Kamera bleibt **2850 cm / −50° Pitch / −45° Yaw / 35° FOV**. Lag 12/max.45 cm, Substepping, Zieloffset 35 cm, Projektion und deaktivierter Kollisions-Zoom unverändert. Bewegung 210 cm/s, Capsule 28/48 cm, Playerdarstellung und Animationen unverändert.

Der vorhandene Sichtkegel, die tatsächliche Kamera-/Playerdatenübergabe, Dither, Wurzelschutz und **0,25-s-Fade** wurden nicht geändert. Beide Reveal-Master und die MPC bleiben bytegleich.

Vier neue Material Instances verwenden den vorhandenen `M_V2_BarkRevealBase`:

| Ursprüngliches Birkenmaterial | Neue Runtime-Variante |
| --- | --- |
| `MI_WLA_Birch` | `MI_V2_BirchReveal` |
| `MI_WLA_LeafBirch` | `MI_V2_LeafBirchReveal` |
| `MI_WLA_LeafDark` | `MI_V2_LeafDarkReveal` |
| `MI_WLA_LeafLight` | `MI_V2_LeafLightReveal` |

Dieser gemalte Master besitzt bereits dieselben Paint-, Tint-, Roughness-, Metallic- und Specular-Parameter wie die Birkenoriginale. Die Birkenblätter bestehen aus opaker Blattgeometrie; kein neuer Atlas-/Alpha-Master erforderlich. Texturen und sämtliche genannten Werte werden übernommen. Die drei Blattvarianten bleiben zweiseitig, die Rinde einseitig. Keine zusätzlichen Texturen oder Master-Duplikate.

Die bestehende Komponente übernimmt die Instances ausschließlich zur Laufzeit. Sie prüft jetzt explizit **Baum-Meshfamilie plus passende Materialzuweisung**. Ein Gebäude mit einem gemeinsam genutzten Original- oder Reveal-Material wird nicht registriert. Bei EndPlay werden alle ursprünglichen Materialzuweisungen wiederhergestellt. Die Map muss dafür nicht gespeichert werden. Reproduzierbares Autorenwerkzeug: `Tools/ConfigureTreeFamilyReveal.py`.

## Eingebettete PIE-Prüfung

Alle Sitzungen ausschließlich `PlayMode_InViewPort`; kein schwebendes Fenster, kein neuer Viewport-Absturz. Kontrollierte PIE-Spawnpositionen, danach tatsächliche bestehende Enhanced-Input-Bewegung. Keine Baum-/Mapverschiebung. Bewegungstest jeweils zur Kamera, Halt, von der Kamera weg, Halt, diagonal hin und zurück. Dies sind gezielte Sichttests, kein vollständiger Gameplay-Rundweg.

| Prüfung | Start X/Y, cm | Tatsächliches Ergebnis |
| --- | --- | --- |
| Einzelbirke | −1710 / 910 | Birkenöffnung beim Annähern; Figur sichtbar, Originalfarben erhalten |
| Mehrere Eichen | −741 / −740 | Bestehende Freistellung unverändert funktional; bis sechs konservativ aktivierte Baum-Bounds |
| Gemischte Kronen | −2350 / −1750 | Birke und Eiche gleichzeitig angebunden; Körper sichtbar, nur kleine betroffene Kronen-/Astflächen geöffnet |
| Vegetation vollständig dahinter | −3500 / 2600 | Kein Baum aktiviert, alle Fade-Stärken null, hintere Bäume sichtbar |
| Baum unmittelbar dahinter | −2750 / 1850 | Hintere Eiche bleibt erkennbar, keine Ganzbaum-Ausblendung |
| Gebäude zwischen Kamera und Figur | −2500 / 50 | Dach bleibt vollständig sichtbar und verdeckt die Figur bewusst; kein Gebäudereveal |

Zwei zusätzliche Mischbereichsserien (`Mischkronen`, `MischNord`) prüfen Bewegung und Materialzustände. Konservative Bounds allein erwiesen sich als unzureichender Nachweis gleichzeitiger tatsächlicher Verdeckung. Für den gezielten Mischpunkt wurden deshalb vorhandene Mesh-Vertexpositionen lesend in die feste Kamerabasis projiziert; keine Geometrieänderung. Maßgeblicher ergänzender Nachweis: `MischVerifiziert`.

Die Serien protokollieren pro Frame Kamera-/Playerübergabe, Fade-Werte und Familien. **45 Baumkomponenten/98 Runtime-Slots** vorhanden; **1362 Nicht-Baum-Slots** behalten ihre Materialzuweisung. Vollständig hinter dem Player liegende Bounds werden nach dem zulässigen Aus-Fade nicht weiter aktiviert. Eine hoch aufragende Krone kann trotz hinterer Stammposition Teile in die Sichtlinie strecken; nur diese tatsächlichen Vorderflächen dürfen freigestellt werden. Die Stammposition allein ist kein geeigneter Ausblendtest.

Zwischenwerte des Fades beim Bewegen belegt; keine beobachteten wiederholten harten Materialumschaltungen oder Ganzkronen-Pops. Geschwindigkeit maximal 210 cm/s. Kein erweiterter fester Weltkreis, keine Vergrößerung der bestehenden Sichtöffnung.

### Echte Spielkamera-Bilder

Native Unreal-`Shot`-Aufnahmen im eingebetteten Viewport, **2331 × 1346 Pixel**. Originalbilder und Frameprotokolle liegen unter `Saved/TreeReveal_20261013`, sind Arbeitsnachweise und nicht automatisch Git-Inhalt.

- [Birke beim Annähern](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/Einzelbirke_Player_Vorne00000.png)
- [Birke beim Weglaufen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/Einzelbirke_Player_Hinten00000.png)
- [Diagonale Bewegung](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/Einzelbirke_Diagonal00000.png)
- [Mehrere Eichen](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/Eichen00000.png)
- [Eiche und Birke gemeinsam](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/MischVerifiziert00000.png)
- [Gemischter Vergleich: Reveal aktiv](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/MischVerifiziert_Reveal_On00000.png)
- [Gemischter Vergleich: kurzzeitig diagnostisch deaktiviert](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/MischVerifiziert_Diagnostic_Off00000.png)
- [Hintere Vegetation](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/HinterPlayer00000.png)
- [Baum unmittelbar hinter der Figur](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/DirektHinter00000.png)
- [Gebäude bleibt unbeeinflusst](/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/TreeReveal_20261013/Gebaeude00000.png)

Die Diagnoseabschaltung betrifft ausschließlich temporäre Runtime-MIDs bei stehendem Player. Alle Werte und der Tick wurden anschließend wiederhergestellt (`MixVerifiedComparison.json`: `restored=true`). Keine gespeicherten Asset-/Kameraänderungen durch diese Bildkontrolle.

## Build, Tests und Datei-/Map-Sicherheit

- C++-Build erfolgreich. Der erste Build bei noch offenem Editor erzeugte eine Hot-Reload-Bibliothek; nach sauberem Beenden ohne unsaved Map-/Assetpakete wurde ein regulärer Build ausgeführt. Maßgeblich `Saved/TreeReveal_20261013/BuildFinal.log`, `Result: Succeeded`, reguläre `libUnrealEditor-PokeMonster.dylib`.
- Tatsächlich ausgeführt: **41/41 Automationstests erfolgreich, 0 Testfehler, 0 Testwarnungen**. 40 bestehende plus `PokeMonster.Camera.Visibility.TreeFamiliesAndBuildingExclusion`. Ergebnisse in `AutomationResults.json`.
- Neuer Test prüft beide Meshfamilien, vier Birkenzuweisungen, gemeinsame Master-Nutzung, gleiche Paint-/Tint-/Two-Sided-Werte, unveränderten Fade sowie Gebäudeausschluss auch bei gemeinsamem Material. Bestehender Sichtlinien-/Fade-Test bleibt grün.
- Abschließender **Map Check 0 Fehler / 0 Warnungen**, 13.10.2026 19:18:03 UTC.
- SceneBefore/SceneAfter identisch: Actorpositionen, Scale, Bounds, ursprüngliche Materialien und Sichtbarkeitsdaten erhalten. Final kein Dirty-Content-Paket; nur zwei temporäre Automation-Fixture-Maps `/Temp/Untitled_2` und `/Temp/Untitled_4` als dirty geführt, keine Projektmap.
- SHA256-Audit gegen **1453 vorhandene Projektdateien**: alle vorhandenen Content-Assets einschließlich Reveal-Master/MPC sowie alle Maps, Player-/Animations-/Gameplaydateien und NPC-Nutzerquellen unverändert. Nur die unten genannten Source-/Dokumentationsdateien geändert. Kein Reset/Restore/Clean, keine Löschung.
- `git diff --check` erfolgreich, keine Ausgabe.

## Restprobleme und Grenzen

- Dunkle Kleidung in tiefen Schatten bleibt schwerer lesbar; kein Player-/Lichtpass in dieser Aufgabe.
- Temporales Dither ist kein echtes Alpha-Blending. Feine Körnung und bei niedriger Bildrate sichtbare Fade-Schritte bleiben möglich; keine neue FPS-Garantie oder Performance-Abnahme.
- Abdeckung gilt für die zwei tatsächlich sichtbaren Familien dieser Karte. Andere Meshrevisionen, aktivierte alte Sprite-/Kegelbäume, nachträglich gespawnte Komponenten und Split-Screen benötigen eine eigene Anbindung/Prüfung.
- Gebäude können die Figur weiterhin verdecken. Das ist hier ausdrücklich gewollt; bestehendes Gebäudecutaway bleibt ein separates System.
- Keine erneute vollständige Battle-/Quest-/Save-PIE-Strecke; diese Systeme sind unverändert und ihre Automationstests grün. Keine allgemeine visuelle Art-Freigabe behauptet.

## Neue/geänderte Dateien und Git

Fünf bestehende Dateien geändert:

- `Source/PokeMonster/Camera/PokeMonsterCameraVisibilityComponent.cpp`
- `Source/PokeMonster/Camera/PokeMonsterCameraVisibilityComponent.h`
- `Source/PokeMonster/Tests/PokeMonsterCameraVisibilityTest.cpp`
- `Docs/TECHNIK.md`
- `Docs/ENTSCHEIDUNGEN.md`

Sechs neue Projektdateien: die vier oben genannten Instances unter `Content/Environment/DevTestMapVisualV2/Materials/`, `Tools/ConfigureTreeFamilyReveal.py` und dieser Bericht.

```text
 M Docs/ENTSCHEIDUNGEN.md
 M Docs/TECHNIK.md
 M Source/PokeMonster/Camera/PokeMonsterCameraVisibilityComponent.cpp
 M Source/PokeMonster/Camera/PokeMonsterCameraVisibilityComponent.h
 M Source/PokeMonster/Tests/PokeMonsterCameraVisibilityTest.cpp
?? Art/Characters/NPCs/
?? Content/Environment/DevTestMapVisualV2/Materials/MI_V2_BirchReveal.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/MI_V2_LeafBirchReveal.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/MI_V2_LeafDarkReveal.uasset
?? Content/Environment/DevTestMapVisualV2/Materials/MI_V2_LeafLightReveal.uasset
?? Docs/BAUMFAMILIEN_SICHTFREISTELLUNG_PRUEFBERICHT.md
?? Tools/ConfigureTreeFamilyReveal.py
```

Nach Harrys Sichtprüfung ist dies ein sinnvoller separater Sicherungspunkt. Vor einem späteren Sicherungsauftrag mit `git diff --stat` und `git status --short` prüfen; die vorhandene NPC-Arbeit getrennt behandeln. In diesem Auftrag kein Commit und kein Push.
