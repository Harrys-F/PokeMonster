# Glumanda V1.1, Kampfansicht und Sichtkreis

20.10.2026; aktives Projekt `/Users/harry/Developer/PokeMonster`, VisualV2.
Ausgangspunkt `fc5174ee0fd6f1cef1a56bd1d6ea2bec11cf545e`, `main`/Remote identisch.
Keine zusätzliche Map, kein Worktree und keine Projektkopie. 58 vorhandene
unversionierte Dateien, alle elf Maps, Original-GLB, V1-Quellen und Backup 03492bd
zu Beginn per Prüfsummen/Refs erfasst und geschützt.

## Meilenstein 1 – Name und kleiner Modellpass

Sichtbarer Name jetzt **Glumanda**. Die stabile Identität bleibt
`CreatureSpecies:Zunderlauf`; Assetpfad, Prototypnummer, Kampfwerte und Saveformat
werden nicht umbenannt. Team-/Kampf-/Logtexte beziehen ihren Namen bereits aus
GetDisplayName. Der bestehende Fang-/Heil-/Save-Test prüft den sichtbaren Namen
nun ausdrücklich nach der Wiederherstellung. Der Gameplay-Prüflauf benutzt den
aktuellen Spezies-Anzeigenamen statt einer fest codierten alten Testzeichenfolge.

Neue bearbeitbare Quelle:
`Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Meshy_V11.blend`.
Ein Skin-FBX unter `Exports/MeshyV11/Glumanda_Skin_V11.fbx`. Neues Mesh und Profil:
`/Game/Characters/Creatures/Zunderlauf/MeshyV11/SK_Glumanda_V11` und
`DA_Glumanda_V11`. Die vorhandenen sieben Animationen, Skeleton, Materialien,
Texturen und originale Schwanzflamme werden exakt wiederverwendet.

### Tatsächliche Mesh-Reparatur

Zehn kleine echte Randloops: Umfang etwa 1,37–11,19 cm. Nicht mit UV-Seams oder
der absichtlichen Körper-/Flammennaht verwechselt. Die reine Diagnoseverschweißung
des V1-Körpers zeigt 90 Randkanten; nach Reparatur bleiben nur die 43 Kanten der
Flammennaht. Das Render-Mesh wird nicht global verschweißt/remesht.

Zuerst versuchte Diagonal-Kappen ließen bei der unabhängigen Topologieprüfung
14 zusätzliche Randkanten zurück: einzelne Diagonalen kollidierten mit vorhandenen
Quellkanten. Diese Zwischenfassung wurde nicht als bestanden gesichert. Finale
lokale Fächerkappen mit einem 0,02 mm nach innen versetzten Mittelpunkt vermeiden
diese Diagonalen. Keine Verschiebung ursprünglicher Vertices oder UVs.
Neue Kappen verwenden nur benachbarte Original-UV-Bereiche; bei Atlasnähten lokale
Projektion aus einer angrenzenden Fläche statt quer über die Textur zu interpolieren.

Körper: 12.227 → **12.284 Vertices**, 18.198 → **18.245 Dreiecke**.
Mit unveränderter Flamme (3.563 Dreiecke): **21.808 Dreiecke**.
Keine ursprüngliche Fläche entfernt; 47 winzige Kappendreiecke ergänzt.
Form-/UV-Abweichung ursprünglicher Vertices: **0**. Größte Normalen-Differenz nach
Blender-Speicherung 0,000498 als Einheitsvektordifferenz (rund 0,029°), keine
Neugestaltung der Normalen oder Materialien. Bone-Restmatrizen exakt unverändert.
Alle sieben Animationskurven per Signatur identisch; 3 Originalbilder gepackt.

### Knie und Bewegung

Nur Knie-/Gelenkübergänge leicht über benachbarte Gewichte regularisiert.
Stärkere Kandidaten (25/50 %) wegen 4,1/8,2 mm Oberflächendifferenz verworfen.
Übernommen: 12,5-%-Nachbarschaftsanteil, maximal **2,051 mm** animierte Differenz.
Das P99-Maß absoluter logarithmischer Kantenverformung in 14 Walk-/Run-Proben
sinkt von 0,54876 auf 0,53834. Das ist ein begrenzter technischer Gewinn und keine
Behauptung einer vollständig anatomischen oder schnittfreien Animation.
Fuß-IK, 22/36-cm/s-Schrittparameter, 0,60-m-Größe und Schwanzanker bleiben erhalten.

### Prüfungen des ersten Pakets

- Blenderquelle erneut geöffnet, alle ursprünglichen Positionen/UVs und Actions
  verglichen; keine ungewichteten/nichtnormierten Vertices. FBX erneut importiert.
- Mac Development Editor Build `GlumandaV11SkinBuild01`: bestanden.
- Finale echte QHD-PIE-Sequenz: 7 Clips, 8 Richtungen, native Run-Mischung 1,0,
  74 Aufnahmen unter `Saved/GlumandaV11/RuntimeReviewFinal`.
- Neuer Regressionstest: sichtbarer Name, stabile Art-ID, aktiver V1.1-Skin,
  Originalmaterialien/Skeleton/Clips/Flammeneffekt und 60-cm-Silhouette.
- Vollständige Automation `GlumandaV11SkinAutomation01`: 57/57, keine Testwarnungen oder Fehler.

Lokale Bilder/Animation: `Saved/GlumandaV11/Evidence/` (nicht in Git).
Messwerte dauerhaft: `Art/Characters/Creatures/Zunderlauf/MeshyV11_RepairAudit.json`
und `MeshyV11_SourceAudit.json`. Keine Garantie universell gleitfreier Übergänge;
weitere visuelle Feinabnahme der starken Kniebeugung bleibt sinnvoll.

## Meilenstein 2 – doppelter Sichtkreis

Die Radien werden pro Spielwelt zur Laufzeit 55/110 → **110/220 cm** gesetzt.
Radius und Durchmesser verdoppelt; gleiche weiche .25-s-Übergänge, unveränderter
endlicher Kamerakegel und explizite Baumfamilien. Shader, MPC-Asset, Kameradistanz,
sonstige Sichtweiten und alle Maps bytegleich. Die Broadphase berücksichtigt den
vergrößerten äußeren Radius.

Endgültiger Screenshotvergleich `Saved/GlumandaV11/SightAccepted/Result.json`:
beide echte **2560 × 1440**, 100 % Screen Percentage, exakt gleiche Kamera/Rotation
(Toleranz .001 cm), tatsächliche MPC-Werte 55/110 bzw. 110/220 bestätigt. Die
temporäre Positionierung dieses Screenshotdiagnosetests wird zurückgesetzt und
nicht als Fußlauf ausgegeben. Lauf-/Sprintprüfung separat in der vollständigen Route.

Lokale Vorher-/Nachher-Tafel (zwei echte QHD-Bilder, in der Tafel auf 50 % verkleinert):
![Sichtkreisvergleich](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/Evidence/Sichtkreis_Vergleich.png)

## Figurenschatten – bewusst nicht übernommen

Mehrere lokale Verfahren geprüft: bestehender Decal-Ansatz, radiale Surface-/Modulate-
Kontaktfläche und native SelfShadowOnly-/Inset-Flags. Die Bilder zeigen keinen
überzeugend belegten weicheren Bodenkontakt; die Flags entfernen den detaillierten
Bodenschatten in diesem Setup nicht zuverlässig. Ein normales Kontrollmaterial
bestätigt, dass die Hilfsebene sichtbar ist; damit ist die fehlende Wirkung nicht
pauschal als ausgeblendete Geometrie erklärt. Keine unbelegte Rendererursache behauptet.

Der anschließende Versuch, nur die eigenen Materialknoten zu ersetzen, löste eine
Materialeditor-Assertion `!IsRooted()` in `DeleteAllMaterialExpressions` aus. Dieser
Alpha-Kandidat wurde nicht gespeichert oder als erfolgreich geprüft ausgegeben.
Keine fortgesetzte Mutation desselben geladenen Materials nach diesem Absturz.

**Ergebnis:** Der versuchte Schattenbaustein wurde aus Player-/Kreaturenanbindung
entfernt. Seine ausschließlich neuen Versuchsdaten bleiben unter ignoriertem
`Saved/GlumandaV11/Diagnostics/RejectedShadow`; nicht im aktiven Source/Content und
nicht in Git. Bestehende Figuren-, Baum-/Gebäudeschatten, Innenraum, Lichtquellen,
Lumen, Bloom und TAA bleiben erhalten. Dieser Teilauftrag ist weiterhin offen.
Keine globale Licht-/Shadow-Quality-Änderung als Ersatz vorgenommen.

## Meilenstein 3 – klassische Kampfansicht

Neue ausdrücklich freigegebene Regel in SPIELREGELN/ENTSCHEIDUNGEN vor Umsetzung
festgehalten. `ClassicBattle` ist der Default normaler Begegnungen. Wild- und
Trainerprofile können `WorldBattle` für besondere Begegnungen wählen; die Wahl
wird in die bestehenden StartData übernommen, ungültige Modi vor dem Start abgewiesen.

Keine zweite Kampflogik: bestehende BattleSession, Presenter, Zustände und Widget-
Präsentationsphasen bleiben zuständig für Attacken, Schaden, Fang, Wechsel, K.O.,
Team-/Trainerzustand und Rückgabe. Keine neuen Savefelder oder Art-IDs. Keine neue
Map und keine Kameraparameteränderung der Oberwelt.

Eine kurzlebige `APokeMonsterClassicBattleScene` in derselben geladenen Welt zeigt
nur ihre eigenen kollisionsfreien Kreaturen und Bodenfläche per ShowOnly-SceneCapture.
Eigenes Modell schräg hinten links, Gegner schräg vorne rechts. Originalgröße und
Materialien; Bounds passen Bühnen-/Kameraabstand an, nicht die Körpergröße. RenderTarget
2560 × 1040 für das 1280 × 520 große Kampffeld im 1280 × 720-Layout. Moderne ruhige
Fantasy-UI mit Namen/Level/KP, vorhandenen vier Attacken, Teamwechsel und Fangtaste.
Fehlende 3D-Testarten behalten die bereits vorhandenen UI-Testfiguren. Keine der
übrigen unversionierten Meshy-Kreaturen wird als ungeprüfter Ersatz eingebunden.

Nur die kurzlebigen Bühnenmodelle erhalten eine schattenlose Lesbarkeitsfüllung
auf **Lichtkanal 2**. Bestehende Außen-/Innenraumlichter werden nicht geändert.
Bühnenboden kollisions-/navigationsfrei, keine Schatten-/Distanzfeld-/indirekte
Lichtwirkung der Bühnengeometrie auf die Welt. Die Oberweltkamera und der Pawn werden
nicht umgeschaltet oder versetzt. Nach Ende werden Szene/Modelle entfernt und
Eingaben freigegeben. WorldBattle nutzt weiterhin die bisherigen sicheren
Oberwelt-Spawnplätze. Die UI-VFX starten nun vor Sichtbarkeit am Kreaturenanker,
um einen einframeigen Blitz am linken oberen Canvasursprung zu vermeiden.

### Echte Laufzeitnachweise

- `ClassicProofFinal/Result.json`: zwei echte Glumanda, fünf aufgelöste Runden,
  Attack/Hit/Faint/Happy/Idle beobachtet, Victory. Vor/nach identische Pawnposition,
  Kameraposition und ViewTarget; Szene vollständig entfernt, Eingabe freigegeben.
- `WorldProof01/Result.json`: WorldBattle ohne ClassicScene, zwei Kampfmodelle an
  echten Oberwelt-Bodenpositionen, fünf Runden/Victory, gleiche Position/Kamera danach.
- `ButtonInput/Result.json`: echte Space-Eingabe auf den fokussierten UMG-Angriffsbutton
  löst Runde 1 und Schaden aus; anschließend regulär beendet. Kein bloßes Presenter-
  Methodenaufrufen als Ersatz für diese Eingabeabnahme.
- Vollständige Route `Acceptance/FinalV11`: echter Enhanced Input, **292,30 m,
  102 Prüfschritte**, keine Testteleports. Wild-Glumanda gefangen, Team auf drei
  erweitert, zu eigenem Glumanda gewechselt, Trainer besiegt, Quest-/Archivfortschritt,
  Save/Load mit erhaltenen KP/AP, Heilhaus-Heilung/Speichercheckpoint, gerade und
  diagonale Innenraumwechsel, freie Laufwege/Brücke, Dialog und Sprite-Fallback,
  dichter Wald/Kronenfreistellung, acht Richtungen und Sprint **315 cm/s** bestanden.
- Zusätzlicher Beobachter bestätigt ClassicBattle bei Wild-/Trainerkampf, den
  Darstellungswechsel zum eigenen 3D-Glumanda, Aufräumen nach beiden Kämpfen und
  den sichtbaren Namen Glumanda nach Save/Load. Keine neue Schadens-/Fangregel.
- Originaler Dev-Slot danach SHA-genau wiederhergestellt:
  `01dd9ebb263dd7dde672e1a9b70f8ae5780494fb9a5f3c1140ed3f0132ce057a`.

Echte klassische Ansicht (tatsächlicher Slate-Spielviewport **2027 × 1140**, nicht QHD):
![ClassicBattle](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/Evidence/ClassicBattle_Unreal.png)

WorldBattle-Ausnahme, ebenfalls tatsächlicher Slate-Spielviewport:
![WorldBattle](/Users/harry/Developer/PokeMonster/Saved/GlumandaV11/Evidence/WorldBattle_Unreal.png)

Die frühere zusätzliche Offscreen-Widgetaufnahme wurde als solche markiert und
nicht als QHD-Viewportfoto verwendet. Das endgültige Aufnahme-Werkzeug zeichnet nur
den echten Slate-Viewport auf. Modell-/Sichtkreis-Aufnahmen sind echte QHD-Framebuffer;
`Shot showui`-Gesamtfensteraufnahmen werden nicht als 2560×1440-Spielbilder ausgegeben.
Die ROM-Screenshotanhänge bestimmen ausschließlich die Komposition; keine Grafik daraus
importiert. Sieben-Clips-GIF unter `Evidence/Glumanda_Unreal_Bildsequenz.gif` ist eine
zeitlich beschriftete Bildfolge, kein behauptetes Echtzeitvideo.

## Abschließende technische Prüfung

- Finaler Mac Development Editor Build `GlumandaV11FinalBuild`: **bestanden**, 14,45 s.
- Gesamte Automation `GlumandaV11FinalAutomation`: **58/58**, 0 Testwarnungen,
  0 Fehler, keine ausgelassenen Tests; 29,19 s. Neuer Modus-/Profiltest prüft auch
  Lichtkanalisolation, ShowOnly-Capture und fehlende Bühnenkollision. Bestehender
  PIE-Vertrag erweitert um Kameraerhalt, Szenenfreigabe und WorldBattle-Ausnahme;
  die normale Headless-Suite überspringt ihren PIE-Abschnitt wie zuvor. Separate
  tatsächliche PIE-Lebenszyklusnachweise und vollständige Route stehen oben.
- Alle **11** bestehenden Map Checks: **0 Fehler, 0 Warnungen**, keine Map gespeichert.
  `MapCheckFinal.json` enthält die tatsächlichen Engine-Protokollzeilen.
- Nach finalem VFX-Patch erneut echter ClassicBattle-Durchlauf: fünf Runden/Victory,
  Attack/Hit/Faint/Happy/Idle, unveränderte Kamera/Position und entfernte Szene bestätigt.
- Name, Fang, Teamwechsel, Quest, Heilung, Speicherfunktion, Innen-/Außenkamera,
  Kollisionen/Laufbarkeit, Sprite-Fallback, Freistellung und Sprint durch realen
  292,30-m-Fußlauf geprüft; Originalsave bytegenau restauriert.
- SHA-Schutzprüfung sämtlicher anfangs erfassten Dateien bestanden; keine neuen Maps.
- `git diff --check`, explizite Indexkontrolle und `git diff --cached --check` sind
  verbindliche Sicherungsgates; Resultate lokal in `GitFinal.json`/`IndexFinal.json`.
  LFS lokal separat per SHA geprüft; zweites Paket enthält keine neuen LFS-Objekte.
- Keine Standalone-/Performancefreigabe behauptet. Keine neue Kreatur oder Landschaftsgestaltung.

## Grenzen und nächste sinnvolle Arbeit

- Weichere Oberwelt-Figurenschatten nicht gelöst und nicht übernommen.
- Technische Freigabe der klassischen Ansicht für vorhandene Testarten/Glumanda;
  künstlerische Feinabnahme von Hautwirkung, Hintergrund und UI bleibt beim Nutzer.
- Keine Behauptung perfekter Gelenke/aller Bewegungsübergänge oder universeller
  Topologiequalität; die begrenzte Knieverbesserung ist oben messbar eingegrenzt.
- Andere Körperformen/Größen benötigen nach Import eigene visuelle Abnahme.
  Vorhandene generische 2D-Testfiguren sind keine neuen fertigen Pokémon-Modelle.
- SceneCapture erzeugt zusätzliche Laufzeitkosten. Keine FPS-/GPU-Benchmarks und
  keine Performancefreigabe für viele gleichzeitige Szenen; nur eine aktive Szene.
- Erste Classic-Automation brach wegen eines unvollständigen neuen Trainer-Testfixtures
  und anschließend ungeschütztem Testarrayzugriff ab. Pflichtfelder ergänzt und
  fehlgeschlagene Vorbedingungen vor dem Zugriff abgefangen; kein Gameplay-Workaround.
  Frühe Python-Reviewfehler/fehlender Test-Rundenauflösungsaufruf und eine zu früh
  vor der Spawn-Bodensetzung erfasste Vergleichsposition sind in lokalen Fehlversuchen
  erhalten, nicht als bestanden gezählt. Spätere getrennte Nachweise oben bestanden.
- Editorprotokoll enthält wiederkehrende Plattform-/idevice-Warnungen, anfängliche
  PSO-Ladehänger, vereinzelt Audio-Underruns bei synchronen Bildern und den bestehenden
  HttpListener-Port-8000-Konflikt. Projekt-Testwarnungen und Map-Check-Befunde werden
  separat angegeben; diese Meldungen wurden nicht unterdrückt oder als behoben erklärt.

## Git und Schutz

Erstes geprüftes Paket regulär gepusht:
`1ae2a51e29e0a1ebfaedc4d9f74f10e28702cffc` – Name/Modellpass, 26 Pfade,
5 neue LFS-Objekte, 12.144.976 Bytes. Remote-Downloads aller fünf Objekte mit SHA-256
bestätigt. Zweites Paket: ausschließlich die hier dokumentierten Quellen/Werkzeuge/
Regeln und dieser Bericht; keine neuen Binärassets oder Kontrollmedien.
Genauer Abschluss-Commit und Remote/LFS-Nachweis stehen im Abschluss der Codex-Ausgabe
und lokal unter `Saved/GlumandaV11/GitFinal.json`.

58 vorbestehende unversionierte Dateien, 11 Mapdateien, 36 ursprüngliche Quellen
und 32 ursprüngliche Kreaturenassets per anfänglichem SHA-Inventar geprüft.
Beide Backup-Refs bleiben exakt auf 03492bd. Kein Reset/Clean/Force-Push,
keine neue Map/Projektkopie/Worktree, keine anderen Kreaturen und kein Landschaftspass.
Alle Kontrollbilder/-folgen/Fehlversuche bleiben im ignorierten Saved-Bereich.
