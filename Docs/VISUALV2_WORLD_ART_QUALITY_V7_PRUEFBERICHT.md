# VisualV2 World Art Quality V7 – Prüfbericht

Stand: 19.10.2026. **Landschaftspass technisch geprüft, visuelle V7-Abnahme offen. Die gewünschte Schattenaufhellung wurde nicht übernommen.**

## Ausgangspunkt und Schutz

- Schlanker Worktree: `/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree`, Branch `codex/slim-backup-v5`.
- Ausgangs-HEAD und direkt geprüftes `origin/main`: `971d060ba2854d8ee744db010b94191802d676ee`.
- Einzige bearbeitete Karte: `/Game/Maps/Dev_TestMap_VisualV2`; Datei `Content/Maps/Dev_TestMap_VisualV2.umap`.
- AGENTS, Grafikstil, Technik, Entscheidungen, Spielidee/Spielregeln und V4–V6-Unterlagen berücksichtigt. Der aktuelle Auftrag gibt den V6-Stil zur Ausweitung frei; eine V7-Abnahme wird daraus nicht abgeleitet.
- Vorherkarte außerhalb des Projekts gesichert: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Dev_TestMap_VisualV2_Before.umap`; SHA-256 stimmt mit dem Ausgangsstand überein.
- Alle 1.374 bisherigen Akteure erhalten. Exakter Szenenvergleich erlaubt nur sechs Materialbindungen; hinzu kommen 23 neue dekorative Akteure. Keine alten Instanzen entfernt oder verschoben. Alle 16 anderen Karten einschließlich Westland, AssetLibrary und fremder Testmap sind per SHA-256 unverändert; Kartenanzahl weiterhin 17.
- Lokales `main` und `refs/archive/pokemonster/full-backup-03492bd` bleiben auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Das Vollbackup ist kein Vorfahr des schlanken Branches.

Zu Beginn vorhanden und weiterhin ausgeschlossen:

```
?? Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
?? Tools/VisualV2EnvironmentQualityV1/
?? Tools/VisualV2QualityV2/__pycache__/
```

## Gestalterische Änderungen

Die V6-Methode für sichtbare Wegbreiten, unregelmäßige Schultern, festgetretene Erde und regional gefärbte Bodenmischungen wurde auf alle fünf vorhandenen Wegfamilien erweitert: Main, Wild, VillageLoop, NorthLoop und Cottage. Die Mittellinien stammen aus den vorhandenen Catmull-Rom-Ribbons. 118 Distanzsegmente approximieren sie mit tatsächlich ermitteltem Maximalfehler unter 4 cm. Weder Wegmeshes noch Kollisionen oder Navigation wurden geändert. Die sichtbare Breite variiert lokal; die kurze Wild-Abzweigung bleibt schmaler. Der V4-Heilhausbereich wird aus der neuen Flächenübertragung ausgespart.

Wald erhält weitere Moos-/Laubflächen, ungleich große Farn- und Unterholzgruppen; Wiese erhält unterschiedlich hohe Grasgruppen, Klee, Kräuter, kleine Blüteninseln und Freiflächen. Am östlichen Wasserabzweig und Teich ergänzen feuchte Bodenmischung, Kies, Ufergras, Schilf und vereinzelte Steine die bereits bearbeiteten Ufer. Der vorhandene Wasser-SDF wird nur lesend als Abstandsfunktion nachgebildet; Wassergeometrie, Wasserverlauf, Brücke und Material des Wassers bleiben unverändert.

| Erweiterungsbereich | Zusätzliche Instanzen |
|---|---:|
| Westlicher Wald | 126 |
| Östlicher Wald / Archivumgebung | 150 |
| Südliche Wiese / Dorfwege | 228 |
| Weiteres Flussufer / Wasserabzweig | 154 |
| **Gesamt** | **658 in 23 HISM-Gruppen** |

Die Gruppen verwenden vorhandene V3-/V4-/V5-Assets und deren funktionierende Instancing-Materialien. Keine neuen Meshes, Texturen, Blenderdateien oder Materialfamilien für Pflanzen erforderlich. Unterschiedliche Größen, Höhen, Ausrichtungen, Abstände und ungleiche Pflanzentaschen ersetzen eine Rasterverteilung. Freie Bereiche und Schutzabstände zu Wegen, Türen, Wasser, Brücke und Interaktionen bleiben erhalten. Alle 407 V5-/V6-Instanzen bleiben an ihren bisherigen Positionen.

Neue Details sind rein visuell: NoCollision, kein zusätzlicher Tick, kein eigener Schatten-/Distanzfeld-/GI-Beitrag, gleiche 4.500–6.500-cm-Cull-Distanzen wie die bisherigen Details. Das verändert nicht den Schattenwurf bestehender Bäume, Figuren oder Gebäude. Es wurde keine Leistungsverbesserung gemessen oder behauptet.

Neue benötigte Dateien:

- `Art/World/VisualV2WorldArtV7/`: README, RouteField-HLSL/JSON, AssetManifest und vollständige Instanz-/Bindungsquelle Scope.json.
- `Content/Environment/VisualV2WorldArtV7/Materials/`: `M_WA7_Ground`, `M_WA7_MainPath`, `M_WA7_NorthPath`.
- `Tools/VisualV2WorldArtV7/`: begrenzte Anwendung, Szenen-/Lichtprüfung, echte Kameraaufnahmen, Build, Automation, Map Check, Fußlauf, Review-Zusammenstellung.
- Karte sowie dieser Bericht und bestätigte technische Dokumentation. Keine Änderung am Spieler, NPC-Rigs, Animationen, Eingaben oder C++-Gameplay.

## Isolierte Schattenuntersuchung – nicht übernommen

Aktives Setup: Virtual Shadow Maps (`r.Shadow.Virtual.Enable=1`), vorhandenes bewegliches Hauptlicht mit Intensität 7,5, Richtung Pitch −48° / Yaw −100°, Temperatur 5.700 K; bestehendes Fill-Light und Skylight unverändert. Die mapbezogene TAA-Lösung bleibt erhalten; der globale AA-CVar allein beschreibt diese nicht vollständig.

Im vorhandenen Engine-Quellcode wurde `UDirectionalLightComponent::ShadowAmount` mit der Beschreibung „amount of shadow occlusion“ gefunden (`DirectionalLightComponent.h`, ungefähr Zeile 263; Setter in `.cpp`, ungefähr Zeile 1404). Die gefundenen Fade-Verwendungen liegen im konventionellen ShadowSetup; im untersuchten VSM-Projektionspfad wurde kein entsprechender wirksamer Anschluss gefunden. Entscheidend war der tatsächliche Bildvergleich:

In ausschließlich temporären PIE-Welten wurde nur dieser Schattenparameter am Hauptlicht auf 1,0, 0,5 und 0,0 gesetzt. Keine Änderung gespeichert; keine Änderung an Intensität, Lichtfarbe, Richtung, Belichtung, Lumen oder Materialien für diesen Versuch. Je Zustand acht identische QHD-Ansichten einschließlich Wald, Heilhaus, Wiese, Ufer, Spielfigur und Innenraum.

**Ergebnis:** Weder 0,5 noch der Extremwert 0 hellten die relevanten Schatten sichtbar in Richtung des gewünschten Ziels auf. In allen 16 Paarvergleichen war die mediane Helligkeitsänderung der ausgewählten dunklen Bildpunkte 0. Kleine mittlere Unterschiede bleiben durch temporale Verarbeitung, Animation und Wasser möglich. Diese Dunkelpixelanalyse ist ausdrücklich keine isolierte physikalische Schattenmessung und kein Nachweis einer prozentualen Wahrnehmungsänderung. Das visuelle 50-%-Ziel wurde nicht erreicht.

Die gespeicherte Karte behält `ShadowAmount=1`. Zusätzlicher Feldvergleich sämtlicher erfasster Directional-/Point-/Spot-/Skylight-Parameter sowie vollständiger Postprocess-Einstellungen bestätigt den Originalstand. Ein anfänglicher Vergleichsfehler des Prüfskripts (Python-Tupel gegenüber JSON-Listen) wurde korrigiert; die erneute Prüfung ist bestanden. Keine tatsächliche Lichtabweichung wurde übergangen.

Nicht als Ersatz eingesetzt: Aufhellung dunkler Tonwerte im Postprocessing, Emissive auf Boden oder Pflanzen, höheres Skylight oder Fill-Light. Diese Verfahren würden auch unbeschattete dunkle Materialien, indirekte Helligkeit oder Innenräume verändern. Eine globale Aufhellung wäre keine saubere Schattenkorrektur.

**Optionen zur gesonderten Freigabe:** Eine echte, rendererbezogene Abschwächung des direkten Schattenfaktors erfordert im untersuchten Setup eine gezielte Renderer-/Shader-Erweiterung mit zusätzlicher Material-, Kontakt- und Innenraumprüfung. Alternativ müsste die Vorgabe unveränderter Füllbeleuchtung ausdrücklich gelockert werden; das wäre eine andere Beleuchtungsentscheidung. Vereinfachte/durchbrochene Schatten-Caster verändern die Schattenform und lösen keine einheitliche Aufhellung von Figuren und Gebäuden. Keine dieser Alternativen ist hier automatisch umgesetzt. Schattenübernahme bleibt zur Entscheidung gestoppt.

## Echte QHD-Bildvergleiche

Jeweils **2560 × 1440 tatsächlicher Viewport und PNG**, Medium, primärer und sekundärer Screen Percentage 100, Dynamic Resolution 0. Acht feste Positionen: Westwald, Ostwald, Südwiese, Wegkreuzung, Uferabzweig, Heilhaus, V6-Waldkontrolle und Innenraum. Außenkamera unverändert 2850 cm / Pitch −50° / Yaw −45° / FOV 35°; vorhandene Innenraumkamera wird unverändert verwendet. Kamera, Rotation und Spielerposition stimmen je Paar innerhalb 0,02 cm/Grad überein.

16 geprüfte Vorher-/Nachher-Paare: acht eingebettetes Editor-PIE, acht eigenständiger nativer `-game`-Betrieb. Letzteres ist kein gecookter Shipping-Build. Fotoaufstellungen verwenden gezielte Positionswechsel; diese sind getrennt vom echten Fußlauf. Keine synthetischen Bilder, keine Retusche, keine Aufhellung der Nachherbilder. Tafeln sind ausschließlich identisch verkleinerte Originalaufnahmen mit Beschriftung.

Lokale Vergleichstafeln (bewusst nicht auf GitHub):

- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Ostwald_V6_V7.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Suedwiese_V6_V7.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Uferabzweig_V6_V7.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Wegkreuzung_V6_V7.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Heilhaus_V6_V7.jpg`
- `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/PIE_Innenraum_V6_V7.jpg`
- Entsprechende `Standalone_*`-Tafeln sowie `ShadowProbe_*` im selben Ordner.
- Vollständiges Paarverzeichnis mit Originalpfaden und SHA-256: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/Comparisons/Manifest.json`.
- Originale: `Saved/VisualV2WorldArtV7/Photos/`; getrennte Schattenprobe vor der Landschaftsänderung: `PIE_Q1_ShadowHalf_2560_1440` und `PIE_Q1_ShadowZero_2560_1440`.

## Tatsächliche Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | bestanden, Exit 0 |
| Vollständige Projekt-Automation | **49/49**, 0 Warnungen/Fehler/nicht ausgeführt |
| Frisch geladene zentrale Karte / Map Check | **0 Fehler, 0 Warnungen**, gespeicherte Szene stimmt exakt |
| Materialgraphen und neue HISM-Gruppen | Referenzen und Einstellungen korrekt; frische Standalone-Logs ohne Shader-Kompilierfehler |
| Vollständiger eingebetteter PIE-Fußlauf | **102 Schritte, 284,20 m**, keine Test-Teleports, bestanden |
| Dev-Spielstand | ursprüngliche Abwesenheit nach Test wiederhergestellt; keine Nutzerdaten ersetzt |
| QHD-PIE und Standalone | echte Vorher-/Nachheraufnahmen, identische Bedingungen |
| Andere Karten und Backup | Hashes/Refs unverändert |
| FPS-/GPU-Benchmarks | auftragsgemäß nicht durchgeführt |

Der Fußlauf verwendet reale Enhanced-Input-Eingaben und die bestehende Spielphysik: acht Richtungen, Sprint bis unverändert 315 cm/s, normales Gehen 210 cm/s, Anhalten, Kamera, Kollision, Menü, Wanderer-Dialog/Quest, Liora-Kampf, Wildkampf/Fang, Archivabschluss, Save/Load, Brückenquerung, Heilhaus-Ein-/Ausgang einschließlich diagonaler Schwelle, Heilen/Checkpoint, Baumkronenfreistellung und NPC-Sprite-Fallback. Es ist ein automatisierter echter PIE-Durchlauf, keine manuelle menschliche Abnahme.

Bestehende experimentelle Engine-Python-Toolsets melden in Standalone sowohl vorher als auch nachher 58 Fehlerzeilen mit denselben 47 normalisierten Fingerprints (u. a. fehlende ToolsetDefinition/PythonTestRunner). Keine neuen Fingerprints, keine fehlgeschlagenen Projekt-Automationstests, keine neuen Shaderfehler. Diese Engine-Meldungen sind nicht behoben oder verschwiegen. Weitere bekannte macOS-Hilfstool-/Audio-/MCP-Meldungen bleiben außerhalb dieses Art-Passes.

Nicht durchgeführt: High-/75-%-Matrix, Shipping-Cook, thermischer Dauertest oder FPS-Profiling. Für diese rein visuelle V7-Abnahme wurde QHD Medium bei 100 % verwendet; daraus folgt keine Performancefreigabe.

## Bewertung und offene Punkte

Die Wegfamilien besitzen nun eine gemeinsame regionale Oberflächensprache; außerhalb der V6-Musterbereiche sind Bodenstrukturen, Unterholz und Ufersäume abwechslungsreicher. Die Wege bleiben frei und klar lesbar. Das Wasser selbst bleibt stilistisch einfacher als seine neue Ufergestaltung; seine Form und sein Material wurden bewusst erhalten. Einzelne alte Pflanzen-/Baumformen bleiben als Bestandsassets erkennbar. Es handelt sich um eine Verbesserung der vorhandenen Welt, keine vollständige Neumodellierung.

**Wichtigster Restpunkt:** Figuren in sehr tiefen Kronenschatten bleiben stellenweise zu dunkel. Die gewünschte ungefähr halbierte Schattenwirkung ist offen. Keine automatische künstlerische Freigabe allein aufgrund der technischen Tests. V7-Bilder und Schattenoptionen werden Harry zur visuellen Entscheidung vorgelegt; danach stoppen.

## GitHub-Sicherung

Gezielt, ohne pauschales Staging, in zwei Schritten: (1) benötigte V7-Quellen/Werkzeuge und drei private Materialien, (2) geprüfte Karte und Dokumentation. Quell-/Materialcommit: `ad9d4e78b077c207dae3107bc0d1e687f3636679`. Der abschließende Kartencommit wird mit tatsächlichem Hash und Remote-/LFS-Nachweis in `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/GIT_ABSCHLUSS.json` und der Codex-Abschlussantwort ausgewiesen; keine Selbstreferenz auf einen erst entstehenden Commit-Hash im selben Commit.

Vor jedem Commit vollständige Indexliste, Planvergleich, LFS-Pointer/Objekte und `git diff --cached --check`; normale Git-Daten deutlich unter 1 GiB pro Push, normale Einzeldateien unter 100 MiB. Neue LFS-Materialien 168.389 Bytes; neue Kartenrevision 3.724.794 Bytes, zusammen **3.893.183 Bytes** benötigte LFS-Objektdaten. Tatsächliche serverseitige Verfügbarkeit wird durch unabhängigen Download mit SHA-256 geprüft. Das ist Objektumfang, kein auslesbarer Kontoverbrauch/Billingnachweis. Keine Käufe oder Budgetänderungen.

Offizielle Größen-/LFS-Informationen am 19.10.2026 geprüft: [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits), [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), [LFS billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).

Keine Kontrollbilder, Videos, Renderings, Saves oder temporären Ausgaben hochladen. Keine Löschungen, Force-Pushes, History-Rewrites oder LFS-Bereinigungen. Nach Abschluss sollen ausschließlich die drei bereits vorher fremden unversionierten Pfade offen bleiben; tatsächlicher Abschlussstatus im externen Git-Nachweis.

Vollständige lokale Prüfbelege: `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/FinalEvidence.json` und `/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19/QA/`; ausführliche Engine-Ausgaben zusätzlich in `Saved/VisualV2WorldArtV7/`.
