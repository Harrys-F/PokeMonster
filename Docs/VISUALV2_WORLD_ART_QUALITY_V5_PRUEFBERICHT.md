# VisualV2 World Art Quality V5 – Prüfbericht

Stand: 19.10.2026. **Drei begrenzte Musterbereiche umgesetzt und technisch geprüft; visuelle Abnahme durch Harry offen. Keine automatische Ausweitung.**

## 1. Ausgangslage und Sicherung

- Schlanker Entwicklungs-Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`.
- Branch `codex/slim-backup-v5`; Ausgangs-HEAD und direkt abgefragtes `origin/main`: `507fa818f5c9445810262ed0f37053ded730df97`.
- Verbindlich bestehende Karte: `/Game/Maps/Dev_TestMap_VisualV2` / `Content/Maps/Dev_TestMap_VisualV2.umap`. **Keine neue Map.**
- Heilhaus V4 ist durch den aktuellen Nutzerauftrag die gestalterische Referenz. Ältere V4-Dokumente beschrieben noch eine ausstehende Abnahme; dieser Auftrag erlaubt ausdrücklich die drei neuen Musterbereiche. Die V5-Muster selbst sind noch nicht visuell freigegeben.
- Vor Änderungen: reale Kartendatei extern kopiert und SHA-256 geprüft; Hashes aller 17 vorhandenen Karten erfasst. Originalzustand und Ablaufnachweise außerhalb des Repositories: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19/`.
- Lokales `main` und `refs/archive/pokemonster/full-backup-03492bd` unverändert auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; dieser Commit ist kein Vorfahr des schlanken Entwicklungsstands.
- Drei vorhandene fremde/unzugeordnete unversionierte Einträge vollständig erhalten und von der Sicherung ausgeschlossen:
  `Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap`, `Tools/VisualV2EnvironmentQualityV1/`, `Tools/VisualV2QualityV2/__pycache__/`.

Gelesen: AGENTS, GRAFIKSTIL, TECHNIK, SPIELIDEE, SPIELREGELN, relevante ENTSCHEIDUNGEN sowie Heilhaus-/World-Art-Prüfberichte und die tatsächlichen V4-Quellen. Vorhandene offene Blender-Sitzung nicht verändert. Eigene Unreal-Sitzungen starteten nur mit sauberer Karte; gespeichert wurde ausschließlich die geprüfte zentrale Karte, kein „Save All“ oder Verwerfen fremder Zustände.

## 2. Gestaltungsumfang

Koordinaten in Unreal-cm; weiche Materialmasken um die angegebenen Zentren. Keine rechteckigen, neu aufgesetzten Bodenplatten.

| Musterbereich | Zentrum / begrenzter Materialbereich | Tatsächliche Arbeit |
|---|---|---|
| Wald | (-3400, 1810), Ellipse etwa 21,6 × 12,8 m; zusätzlich Y-Maske oberhalb des Heilhausbereichs | Neuer Moos-/Laubboden mit gedämpftem Braun und Grün, unterschiedlich große Farn-/Unterholzgruppen, niedriges Moos, Gras, acht Wurzelinstanzen an zwei unveränderten vorhandenen Eichen; freie Lichtungszone und geschützter Wegkorridor. |
| Wiese | (-2320, -1960), etwa 16 × 11,4 m | Vorhandenes V4-Grasmotiv mit zwei unterschiedlich skalierten/gedrehten Abfragen und Makrovariation, wechselnde Grasgrößen/-höhen, Klee, Kräuter, zurückhaltende Wildblumen, kleine Kiesel; offene Bodenstellen zwischen den Pflanzentaschen. |
| Flussufer | (-250, -320), etwa 19 × 9,6 m; nur schmale beidseitige Ufermasken am vorhandenen geraden Bachabschnitt | Gedämpfte feuchte Erde/Kies, unterschiedlich große Steine, Moos, Farne, Ufergras und modelliertes gebogenes Schilf. Brückenzugang und Wegkorridor ausgespart. |

Bestehende Bäume, Wege, Wasserlauf, Brücke und Gebäude unverändert. Keine neuen Gelände-Kollisionen oder modellierten Höhenänderungen: kleine Bodenunregelmäßigkeiten entstehen ausschließlich durch visuelle Steine, Wurzeln, Blattgeometrie und Materialstruktur. Keine neue Patrouille, Quest oder andere Gameplaylogik.

### Platzierungen

| Bereich | Neue Instanzen | Gruppen / Verteilung |
|---|---:|---|
| Wald | 130 | 24 Farn A, 16 Farn B, 10 Wildsträucher, 42 Gras, 30 Moos, 8 Wurzeln |
| Wiese | 156 | 78 Gras, 34 Klee, 14 Blüten, 15 Kräuter, 15 Kieselgruppen |
| Flussufer | 121 | 22 Schilf, 30 Gras, 22 Moos, 12 Farn, 28 Kieselgruppen, 7 Ufersteine |
| **Summe** | **407** | **17 neue HISM-Gruppen** |

Unregelmäßig große, überlappende Pflanzentaschen statt Raster. Größen und Drehungen variiert; freigehaltene Lichtungen und Interaktionsbereiche. Alle neuen Komponenten `NoCollision`, ohne Tick oder zusätzliche eigene Schatten/Distance-Field-/indirekte Lichtbeiträge. Culling 4500–6500 cm. Dies ändert keine vorhandenen Schatteneinstellungen und ist kein gemessener Performancegewinn.

## 3. Assets und Quellen

Wiederverwendet: Heilhaus-V4-Gras, Kräuter und Blüten; bestehende Westland-Farne, V3-Wildsträucher, Wurzeln, Kiesel und Felsen. Vorhandene Quellen und gemeinsame Materialien nicht überschrieben.

Nur die fehlenden botanischen Formen neu in Blender modelliert:

| Quelle | Vertices Blender | Dreiecke Blender/Unreal | Maße vor Instanzskalierung | Unreal-Materialslots |
|---|---:|---:|---|---:|
| CloverPatch | 2.376 | 3.608 | 40,06 × 43,67 × 14,16 cm | 1 |
| MossCushion | 4.416 | 6.624 | 60,40 × 57,08 × 5,62 cm | 1 |
| ReedTuft | 2.252 | 3.600 | 71,07 × 66,41 × 106,29 cm | 2 |

Zusammen 13.832 unterschiedliche Dreiecke in den drei neuen Quellformen; keine globale LOD-/Polygonreduktion. Unreal splittert importbedingt einige Vertices an UV-/Normalengrenzen (2.728 / 4.416 / 2.664 tatsächliche Importvertices). Das Schilf wird unterschiedlich skaliert; kein pauschales mannshohes Gras. Blattflächen sind bewusst offene, zweiseitig dargestellte Pflanzenoberflächen und keine als wasserdicht behaupteten Volumenkörper.

Dauerhafte Dateien:

- `Art/World/VisualV2WorldArtV5/Source/Westland_ThreeBiomes_Details_V5.blend`
- `Art/World/VisualV2WorldArtV5/Exports/SM_WA5_{CloverPatch,MossCushion,ReedTuft}.fbx`
- `Art/World/VisualV2WorldArtV5/Textures/T_WA5_{ForestFloor,WetBank}.png`
- `Details.json`, `AssetManifest.json`, `RegionalMasks.hlsl`, `Scope.json`, `TexturePrompts.json` im selben Arbeitsbereich.
- 17 neue Unreal-Assets unter `/Game/Environment/VisualV2WorldArtV5`: drei Meshes, zwei Texturen, drei private Bodenmaterialien, zwei botanische Materialvarianten und sieben private instancingfähige Material-/Instance-Varianten.
- Werkzeuge und README unter `Tools/VisualV2WorldArtV5/`.

Die zwei neuen Bodenalbedos wurden mit Imagegen erstellt; genaue Prompts sind erhalten. **Tatsächliche Quelldateien 1254 × 1254 Pixel**, keine angeblichen nativen 2K-/4K-Texturen. Unreal: sRGB, Power-of-two-Stretch, MaxTextureSize 2048. Kein eingebranntes Studiolicht als gewünschter Materialeffekt. Wiese verwendet die bereits vorhandene V4-Grastextur. Keine neue externe Modellbibliothek, kein Kauf, kein Plugin.

Instancingfähige Kopien verwenden dieselben vorhandenen Texturen und Parameter. Die funktionierenden Reveal-Materialien der bestehenden Baumkronen wurden nicht neu aufgebaut oder geändert. Materialinstancing wird auf den tatsächlichen Komponentenbindungen geprüft, um den früheren grauen Standalone-Fallback nicht erneut einzuführen.

## 4. Schutzprüfung der Karte

- Bestand: 1.357 erfasste Szenenakteure; danach 1.374. Vier vorhandene Akteure ändern ausschließlich ihre Bodenmaterialbindungen: `V2_Ground`, `V2_Path_NorthLoop`, `V2_Path_VillageLoop`, `V2_Path_Main`.
- Die übrigen **1.353 vorhandenen Akteure** stimmen in den erfassten Eigenschaften vollständig mit dem Vorher-Snapshot überein. Keine vorhandenen Akteure entfernt. Positionen, Meshes und Collision der vier Bodenakteure unverändert.
- Welt-/Lichteinstellungen gleich; unverändert bestehende Kamera 2850 cm / Pitch -50° / Yaw -45° / FOV 35°, Player, Animationen, 140-cm-Maßstab, 210 cm/s Gehen und 315 cm/s Sprint.
- Vorhandene Outdoor-TAA-Blendable und Originalschatten behalten, kein AA-Override für die integrierten Nachheraufnahmen.
- Materialfarbänderungen räumlich durch Masken begrenzt; keine Änderung an Wasser-Opacity, Wasserform, Weg-Opacity oder Brückengeometrie. Das vorhandene einfache Brückenaussehen bleibt bewusst bestehen.
- Alle **16 anderen Kartendateien SHA-256-identisch**, einschließlich WestlandRegion, AssetLibrary, NPCMotionV3 und bestehender Experimente. Keine neue Karte, kein Inhalt im Vollbackup geändert.
- Erneutes Laden der gespeicherten VisualV2 entspricht dem geprüften Szenensnapshot; keine offenen Content-/Map-Pakete beim Schließen.

## 5. Echte QHD-Bildnachweise

Vorher = gespeicherter freigegebener Heilhaus-V4-/VisualV2-Ausgangsstand; Nachher = V5. Für jeden der drei Bereiche komplette echte Spielkameraaufnahme mit Spielfigur als Größenreferenz sowie Detailausschnitt. Zusätzlich Heilhaus-Kontrollansicht. Front-/Review-Kameras ändern die permanente Gameplaykamera nicht.

| Ansicht | Spielerposition X/Y in cm | Kamera |
|---|---|---|
| Wald | -3300 / 2050 | unveränderte Kamera B |
| Wiese | -2100 / -1760 | unveränderte Kamera B |
| Flussufer | -350 / -130 | unveränderte Kamera B |
| Heilhaus-Kontrolle | -4100 / 450 | unveränderte Kamera B |

**32 finale Originalaufnahmen:** jeweils vier Ansichten × Vorher/Nachher × Medium/High × eingebetteter PIE/nativer Standalone-`-game`-Betrieb. PNG und gemessener Spielviewport jeweils **2560 × 1440**, Primary und Secondary Screen Percentage 100 %, DynamicRes 0. Kamera-, Blickrichtungs-, FOV- und Spielerwerte aus den Result.json-Dateien vor/nach verglichen (maximale Abweichung unter 0,02 cm/Grad). Keine FPS-Messmatrix und kein künstlicher Auflösungsvergleich.

- Originale lokal: `Saved/VisualV2WorldArtV5/Photos/{PIE|Standalone}_Q{1|2}_{BeforeFinal|AfterFinal}_2560_1440/`.
- Dauerhafte lokale Kopie aller 32 Originale + Metadaten, bytegleich geprüft: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19/Originals/`.
- 28 beschriftete Vergleichstafeln (16 Gesamt-/Kontrollvergleiche + 12 Bodendetails): `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19/Comparisons/`.
- Vollständige Pfad-/Crop-Zuordnung: `Comparisons/Manifest.json`; SHA-Nachweis: `OriginalsSHA256.json` im externen Ergebnisordner.
- Hauptvergleiche: `PIE_Q2_Wald_BeforeAfter.png`, `PIE_Q2_Wiese_BeforeAfter.png`, `PIE_Q2_Flussufer_BeforeAfter.png` dort; Details jeweils `*_GroundDetail.png`. Ebenso tatsächliche Standalone- und Medium-Vergleiche vorhanden.

Nur Beschriftung, gleichmäßige Verkleinerung der Gesamtbilder und unveränderte Originalpixel-Ausschnitte. Keine Retusche, keine Konzeptbilder als Unreal-Nachweis, keine geänderte Beleuchtung. Vorläufige frühere Candidate-/Before-Serien sind nicht der finale Vorher/Nachher-Nachweis.

## 6. Tatsächliche technische Tests

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build, UE 5.8.2 | erfolgreich; kein C++ geändert |
| Vollständige PokeMonster-Automation | **49/49 erfolgreich**, 0 mit Warnungen, 0 fehlgeschlagen, 0 nicht ausgeführt |
| Map Check VisualV2 nach frischem Laden | **0 Fehler / 0 Warnungen**, persistierter Szenensnapshot gleich |
| Blenderquelle speichern/erneut öffnen | erfolgreich, drei Meshes, keine fehlenden externen Bilder erforderlich |
| Blender-Geometrie/UV | keine Nullflächen, Nullnormalen, nichtendlichen Vertices oder degenerierten UV-Dreiecke in den drei neuen Formen |
| Unreal-Import | gemessene Dreiecke und cm-Maße stimmen; 0 einfache Kollisionskörper, gültige Materialslots |
| QHD-Darstellung | Medium + High jeweils PIE + Standalone erfolgreich aufgenommen; keine neuen Shader-/Materialfallback-Meldungen |
| Gameplay-Fußlauf | **102 Schritte, 284,91 m**, echte Enhanced-Input-Bewegung im gerenderten eingebetteten PIE; keine Test-Teleports |
| Spiellogik im Fußlauf | Wanderer-Dialog/Quest, Wildkampf/Fang, Liora-Kampf, Archivabschluss, Menü, Save/Load, Brücke, Heilung/PP, Checkpoint, gerade und diagonale Hausein-/ausgänge, Cutaway, Kronen-Reveal, acht Geh-/Sprintrichtungen, Stillstand; erfolgreich |
| Dev-Spielstand | vor dem Test nicht vorhanden; Testresultat extern im lokalen Acceptance-Ordner erhalten und ursprüngliche Abwesenheit wiederhergestellt |
| Git-Whitespace | `git diff --check` erfolgreich; Index vor jedem Sicherungscommit separat geprüft |

Der Fußlauf ist eine reproduzierbare Automationsroute im echten PIE und keine behauptete manuelle Nutzerabnahme. Foto-Positionssetzung ist von diesem Lauf getrennt. Standalone-Sichtprüfung erfolgte über den nativen Editor-`-game`-Start; **kein gekochter Shipping-Build**, dort kein zweiter vollständiger Gameplaylauf behauptet.

**Vorhandene Engine-/Toolset-Diagnosen bleiben offen:** im Standalone vor und nach V5 jeweils 58 Python-Fehlerzeilen mit denselben 47 normalisierten Fingerprints (u. a. experimentelle Engine-Toolsets: fehlende `unreal.ToolsetDefinition` / `unreal.PythonTestRunner`). Kein neuer Fingerprint. Außerdem bestehende macOS-/iOS-Tool-/Audio-Diagnosen. Diese sind nicht durch V5 behoben oder verschwiegen; sie sind von den 49 erfolgreichen Projekt-Automationstests und dem fehlerfreien Map Check zu unterscheiden. Keine neue Kompilierungs-, Defaultmaterial- oder Tangenten-/Binormalenwarnung bei den V5-Imports festgestellt.

Keine FPS-Benchmarks, kein umfangreiches GPU-Profiling, keine Leistungsgewinnbehauptung. Unnötig hohe Belastung durch HISM und begrenzten Umfang vermieden, aber Laufzeitkosten dieses Art-Passes nicht als gemessen ausgegeben.

## 7. Selbstkritische visuelle Bewertung und offene Punkte

- Wald nun klar als Waldboden erkennbar; Laub, Moos und Farne binden die vorhandenen Bäume besser an. Der Weg bleibt offen. Trotz unterschiedlich skalierter Abfragen bleibt das prozedural überblendete Laubmotiv bei genauer Nahbetrachtung als wiederholbare Textur erkennbar. Noch keine individuelle handgemalte Unikat-Bodenfläche.
- Wiese wesentlich lesbarer und abwechslungsreicher, mit bewusst freien Flächen. Im Gesamtbild wirken manche kleinen Kräuter/Blüten zurückhaltend; keine Behauptung, dass alle Details aus jeder Entfernung gleich gut lesbar sind. Bestehende Bäume, Bank und Gebäude bestimmen weiterhin die Bildkomposition.
- Feuchtes Kiesufer und Schilfsilhouetten verbessern die Land-Wasser-Grenze sichtbar. Im tiefen bestehenden Kronenschatten kann Schilf sehr dunkel wirken. Licht/Schatten wurden deshalb ausdrücklich nicht verändert. Wasseroberfläche und bestehende einfache Brücke sind kein neu gestalteter V5-Qualitätssprung.
- Zusätzliche Wurzeln sind niedrig und teilweise durch vorhandene Stämme/Kronen verdeckt; keine neuen sichtbaren Stamm-/Bodenanschlussfehler festgestellt, aber keine garantierte Nahaufnahmequalität in jedem Winkel.
- Neue Pflanzen haben bewusst keinen eigenen Schattenwurf; vorhandene Welt-/Gebäudeschatten bleiben vollständig erhalten. Ob kleine Pflanzen künftig feinere Kontaktschatten benötigen, ist eine gestalterische Abnahmefrage, keine bereits entschiedene Optimierung.
- Keine abschließende Bewertung von Wind-/Langzeit-LOD-Verhalten oder einer größeren Welt. Keine Freigabe allein anhand technischer Tests.

**Empfehlung:** Die drei kleinen Musterbereiche zur visuellen Abnahme vorlegen. Waldlaubdichte, Wiesenfarbigkeit und Lesbarkeit des Schilfs im Schatten gezielt beurteilen. Erst danach auf weitere Flächen übertragen. Entwicklung an diesem Umfang stoppen.

## 8. Git-/GitHub-Sicherung

Nur benötigte Art-Quellen, Importdateien, private Unreal-Assets, Tools, zentrale Karte und Dokumentation sichern. Neue Textur-PNGs gezielt in `.gitattributes` als LFS; vorhandene `.blend`-/`.fbx`-/`.uasset`-/`.umap`-Regeln beibehalten. **Keine Vergleichsbilder, Videos, Saved-Ausgaben oder temporären Renderings im Commit.**

Zwei logische Sicherungsschritte: (1) botanische Quellen, private Materialien/Assets und reproduzierbare Werkzeuge; (2) begrenzter VisualV2-Stand und bestätigte Dokumentation. Vor jedem Commit vollständigen Index mit expliziter Dateiliste, LFS-Pointern, lokalen Objekt-SHA-256 und `git diff --cached --check` prüfen. Vor/nach jedem normalen Push Remote prüfen; Remote-LFS-Dateien unabhängig herunterladen und SHA-256 vergleichen. Kein Force-Push oder History-Rewrite; kein Kauf/Budgetwechsel/Prune.

GitHub-Grenzen am 19.10.2026 erneut in den offiziellen Dokumenten geprüft: [normale Dateien](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), [LFS-Kontingente](https://docs.github.com/en/billing/concepts/product-billing/git-lfs). 100-MiB-Git-Dateigrenze; konservative 2-GB-LFS-Einzeldateiprüfung. Normale Git-Daten je Push deutlich unter 1 GiB. Tatsächliche Kontobilling-Anzeige nicht über diese Werkzeuge zugänglich; keine neue Behauptung über eine persönlich abgerufene Restquote. Der kleine V5-Payload wird getrennt erfasst, keine kostenpflichtige Freigabe erteilt.

Verifizierte Commit-Hashes, tatsächliche LFS-Objektbytes und endgültiger Git-Status werden nach der Sicherung in `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V5_2026-10-19/GIT_ABSCHLUSS.json` festgehalten und im Abschluss genannt. Der Bericht behauptet keinen Push vor dessen Durchführung. Originalzustand, Schutzprüfung und tatsächliche Testergebnisse: `InitialState.json`, `FinalEvidence.json`, `QA/` im selben externen Ordner.
