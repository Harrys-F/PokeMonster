# Oberwelt-KI V2, Charakter-Sichtbarkeit und Starterkorrekturen

Stand: 21.10.2026. Projekt `/Users/harry/Developer/PokeMonster`, bestehende `/Game/Maps/Dev_TestMap_VisualV2`. Keine neue Map, kein Worktree, keine Projektkopie. Ausgangspunkt `21bda2840f5f729533ad5dda07594f55491b85cb` auf `main == origin/main`.

## Ergebnis

- **Übernommen: Variante B, gezielte Charakteraufhellung.** Ein kleines schattenloses Fülllicht wirkt in konservativ erkannten dunklen Bereichen ausschließlich auf die Spielfigur. Globale Sky-Aufhellung A bleibt verworfene, zurückgenommene Diagnose. Keine Änderung der bestehenden Lichtquellen, der Spielertexturen oder des Sichtkreisradius.
- Vier wiederverwendbare Oberweltprofile in der vorhandenen Wanderkomponente: neugierig, scheu, territorial und ruhig. Artspezifisch konfigurierbar, mit Überschreibung pro platzierter Begegnung. Kein zweites Kampf-/KI-System.
- Begleiter bleibt ausschließlich Teamplatz 1, reagiert früher auf loslaufenden Spieler, holt beim Sprinten auf und bleibt während ClassicBattle verborgen/pausiert.
- Zwei tatsächliche kleine Öffnungen an Schiggys Augenrand lokal geschlossen. Neue Quelle und Skin; Originaleingabe, Originalquelle, vorhandene Flächen/UVs/Gewichte, Originalmaterial und sieben Animationen erhalten.
- Abschließender expliziter Unity-Build erfolgreich; **84/84 Automationstests**, keine Testwarnungen. Map Check aller **11 vorhandenen Maps: 0 Fehler, 0 Warnungen**. Vollständiger Enhanced-Input-Fußlauf und separate Fang-/Wechsel-/Niederlagenprüfungen bestanden.
- Keine FPS-Benchmarks oder GPU-Profilreihen. Physischer Switch-Pro-Test ausdrücklich offen. Die visuelle Freigabe durch Harry wird durch technische Tests nicht ersetzt.

## 1. Ausgangsprüfung und Schutz

Gelesen: AGENTS.md und relevante Abschnitte von TECHNIK, ENTSCHEIDUNGEN, SPIELIDEE, SPIELREGELN, GRAFIKSTIL sowie Starter-Feinschliff V2 und Schattenqualität V8. Editor und Blender waren zunächst geschlossen, keine fremden geöffneten Pakete. Sämtliche Laufzeitvarianten fanden ausschließlich im PIE statt. Im Editor wurden nur neue SurfaceV2-Assets und die drei expliziten Spezieskonfigurationen gespeichert, keine Map.

Die ursprünglichen **58 unversionierten Einzeldateien** wurden vor Beginn und abschließend mit SHA-256 verglichen: unverändert. Ebenso **301 geschützte versionierte Dateien**, darunter sämtliche vorhandenen Maps, ursprüngliche Kreaturen-/Spielerquellen sowie World-/UI-Code. Sieben weitere Incoming-Modelle bleiben unangetastet und uncommittet. Keine Original-GLB reimportiert, keine vorhandene Blenderquelle überschrieben.

Das Vollbackup `03492bd96b4dba44692f675c19d5f11abfa86b4b` bleibt unter `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd` unverändert erreichbar und ist kein Vorfahr des schlanken `main`. Kein Reset, Clean, Force-Push oder LFS-Prune.

## 2. Charakterlesbarkeit: Untersuchung und Entscheidung

### Tatsächliches Setup

- Sonne: bewegliches Directional Light, Intensität 7,5, Schatten aktiv, Pitch −48°, Yaw −100°, warme Lichtfarbe.
- SkyLight: stationär, Intensität 1,25, keine laufende Neuberechnung des Cubemaps.
- Vorhandenes weiches Richtungsfülllicht: Intensität 0,65, keine Schatten. Unverändert.
- Virtual Shadow Maps aktiv; TAA bleibt aktiv.
- Spielermesh `SK_Player_Meshy_V2`, Material `M_Player_Meshy` aus MeshyV1 unverändert; 140-cm-Maßstab bleibt bestehen.
- Bestehende Kronenfreistellung verändert gezielt die Verdeckung, nicht die Helligkeit der Spielfigur. `RevealRadiusScale` bleibt **2,0**.
- Die untersuchten Oak-/Birch-Meshes besitzen **keine Kollision** und erlauben keinen CPU-LOD-Zugriff. Gewöhnliche Sonnenstrahlen würden daher gerade die Blattschatten übersehen.

### Reale Vergleichsvarianten

| Variante | Umsetzung im Vergleich | Bewertung |
|---|---|---|
| Original | Bestehende Lichtwerte, Fülllicht aus | Figur im tiefen Kronenschatten schlecht lesbar |
| A | SkyLight vorübergehend +15 %: 1,25 → 1,4375 | Wirkt auf die gesamte Welt; zurückgenommen, nicht übernommen |
| B, erzwungene Diagnose | Nur Figur, 20 lm, ohne Zusatzschatten, gleicher Standort | Gesicht/Kleidung besser erkennbar, Bodenschatten bleiben erhalten |
| B, automatisch | Gleiche lokale Lichtwirkung nur bei konservativer Schattenabschätzung | Gewählte Umsetzung; Grenzen siehe unten |

20 lm ist die kalibrierte Intensität dieser kleinen Lichtquelle, **kein behaupteter pauschaler 20–30-%-Bildmultiplikator**. Die gewünschte dezente visuelle Aufhellung wurde anhand der echten Bilder beurteilt. Kleidung und Körper erhalten weiterhin normale diffuse/speculare Materialbeleuchtung; kein Unlit-/Emissive-Ersatz.

Das Fülllicht ist beweglich, besitzt 280 cm Reichweite, wirft keine Schatten und hat keine indirekte Lichtintensität. Es verwendet Oberwelt-Lichtkanal 2, den nur das Spielermesh zusätzlich empfängt. Begleiter übernehmen diesen privaten Kanal ausdrücklich nicht. Die vorhandene ClassicBattle-Szene nutzt ebenfalls Kanal 2, liegt aber räumlich in ihrer bisherigen separaten Capture-Anordnung weit außerhalb der kurzen Lichtreichweite; sie wurde nicht umgebaut.

### Automatische Aktivierung und Grenzen

Fünf Abtastpunkte werden fünfmal pro Sekunde geprüft. Massive kollidierende Schattenwerfer werden gegen tatsächliche Sonnenstrahlen getestet. Kollisionslose Bäume werden ausschließlich über innere, zur Sonne projizierte Kronenvolumen konservativ angenähert. Die Intensität blendet weich ein/aus. Im Innenraum hat der vorhandene Kanal 1 Vorrang und schaltet das Fülllicht unmittelbar aus.

**Keine exakte VSM-/Lumen-Schattenmessung:** einzelne Blattlücken, Wind, teilweise beschattete Körper und andere Kronenformen werden nicht pixelgenau erkannt. Die Methode kann Schattenbereiche auslassen; seltene Fehlzuordnungen an Kronenlücken sind außerhalb der geprüften Punkte möglich. Keine Behauptung einer standortunabhängig perfekten Schattenklassifizierung. Neue Baumformen benötigen erneute Sichtprüfung.

| Geprüfter Punkt | XY in cm | Original / automatische Füllstärke | Ergebnis |
|---|---|---|---|
| Sonne | −760 / −1410 | 0 / 0 lm | Keine dauerhafte Sonnenaufhellung |
| Tiefer Kronenschatten | −1320 / −720 | 0 / 20 lm | Figur besser lesbar |
| Überlappende Kronen | −1300 / −850 | 0 / 20 lm | Beide Kronenkerne nachgewiesen, lokale Aufhellung |
| Öffnung in Baumkronen | −1910 / 530 | 0 / 0 lm | Keine unnötige Aufhellung dieses offenen Bereichs |
| Heilhaus innen | 16900 / 670 | 0 / 0 lm | Bestehende warme Innenbeleuchtung erhalten |

Der vollständige Fußlauf protokollierte 620 Sichtbarkeitsstichproben, davon 61 innen: innen maximal 0 lm, Sichtkreis durchgehend 2,0. Keine allgemeine Tageslicht-, Schatten-, Lumen-, Bloom-, Belichtungs- oder Kameraänderung.

### Bildnachweise

Die Dateien unter Saved sind lokale Entwicklungsnachweise und werden **nicht** auf GitHub hochgeladen. QHD-Weltaufnahmen sind echte 2560 × 1440 Framebufferbilder bei 100 % Screen Percentage; Kamera B bleibt Pitch −50°, Yaw −45°, FOV 35°. Gleiche Standorte und eingefrorene Spielerpose, jeweils fünf Sekunden Einlaufzeit. Wind/andere laufende Figuren können zwischen Bildern variieren; daraus wird keine Leistungsbehauptung abgeleitet.

- A/B-Ausgangsvergleich: `Saved/OverworldAIV2/LightingCompare/`
- Automatische finale Vergleiche: `Saved/OverworldAIV2/LightingFinal/`
- Überlappung/Öffnung: `Saved/OverworldAIV2/LightingOverlap/`
- Unveränderte Pixelausschnitte nebeneinander: `Saved/OverworldAIV2/Comparisons/Canopy_Player.png` und `Sun_Player.png`.

## 3. Schiggy: nachgewiesener Befund und lokale Korrektur

Originalquelle: `Art/Characters/Creatures/Schiggy/Source/Schiggy_Meshy_V1.blend`, SHA-256 `370643ec5faf226874940278c5b998df610db8ac216acc13de85e1d93fa9fca5`.

Die zwei schwarzen Öffnungen neben einem Auge bleiben im Original sowohl ohne Normal Map als auch mit neutralem Clay-Material sichtbar. Damit sind sie als Geometriefehler belegt. Die 6.599 ursprünglichen offenen Meshkanten dürfen hingegen nicht pauschal geschlossen werden: zahlreiche UV-/Teilmesh-Grenzen benötigen eine getrennte Bewertung.

Die endgültige Reparatur folgt den tatsächlichen 5- bzw. 4-Kanten-Randzyklen. Je ein neuer Mittelpunkt erhält interpolierte vorhandene Gewichte, insgesamt neun Dreiecke schließen die beiden Lücken. Eine nur temporär positionsverschweißte Diagnose bestätigt genau neun weniger nicht-manifold Kanten: **471 → 462**, Randkomponenten **14 → 12**. Die Originalgeometrie selbst wird nicht verschweißt.

| Merkmal | Original | Surface V2 |
|---|---:|---:|
| Quellvertices | 14.162 | 14.164 |
| Dreiecke / tatsächlicher FBX-Reimport | 21.273 | 21.282 |
| Blender-Bones | 20 | 20 |
| Unreal-Importhierarchie einschließlich FBX-Wurzel | 21 | 21, Namen/Eltern/Ruheposen zum Original geprüft |
| Materialien | 1 | 2, zweites nur auf den neun Reparaturdreiecken |
| Größe | 0,50 m | Reimport gemessen 0,50000001 m |
| Originalclips | 7 | Dieselben 7 Unreal-Objekte, kein Retargeting/Neuerstellen |

Alle bisherigen Punkte, Flächen, UV-Ecken und Gewichte sind unverändert erhalten. Die ursprünglichen Ecknormalen bleiben bis auf die kleine Rundungsabweichung beim Speichern erhalten; gemessener maximaler Komponentenfehler etwa 0,000392. Keine Nullflächen im endgültigen Mesh. Für alle sieben Clips wurden je 33 Posen auf endliche Geometrie und Höhen geprüft; zusätzlich echte Unreal-Animations-/Kampftests.

Die ursprünglichen Atlasrandbereiche besitzen keine brauchbaren Informationen für die zuvor fehlenden Flächen. Eine direkte UV-Extrapolation erzeugte sichtbare Flecken und wurde verworfen. Das lokale deckende Reparaturmaterial nutzt aus benachbarten Originalflächen abgenommene, korrekt sRGB→Linear umgerechnete Vertexfarben. Es verändert keine Originaltextur und keine bestehende Materialfläche. Die winzigen Kappen erhalten keine zusätzliche Normal Map; eine feine Naht kann im extremen Nahbild weiterhin erkennbar sein. Keine vollständige Neuvernetzung und keine Behauptung eines insgesamt wasserdichten Modells.

### Dateien

- Neue bearbeitbare Quelle: `Art/Characters/Creatures/Schiggy/Source/Schiggy_Surface_V2.blend`
- Export: `Art/Characters/Creatures/Schiggy/Exports/SurfaceV2/Schiggy_Surface.fbx`
- Reproduktionsaudit: `Art/Characters/Creatures/Schiggy/SurfaceV2_Audit.json`
- Neuer Skin: `/Game/Characters/Creatures/Schiggy/SurfaceV2/SK_Schiggy_Surface`
- Profil: `/Game/Characters/Creatures/Schiggy/SurfaceV2/DA_Schiggy_Presentation`
- Lokales Material: `/Game/Characters/Creatures/Schiggy/SurfaceV2/M_Schiggy_LocalSurfaceCaps`
- Spezies behält die ID `Schiggy`; nur die visuelle Referenz zeigt auf das neue Profil.

### Texturen und Entfernung

Alle drei bisherigen Texturen bleiben 2048². BaseColor behält den bereits zuvor geprüften No-Mip-Workaround gegen chartfremde Atlasflecken; Normal und Metallic/Roughness verwenden weiterhin ihre Texture-Group-Mips, LOD Bias 0. Kein pauschales Hochsetzen von Auflösungen, keine neue LOD-Stufe, keine globale Mipänderung.

Es wurde kein neuer eigenständiger Mip-Fehler nachgewiesen. Mögliche feinste Distanzaliasing-/Atlasnahtprobleme sind damit nicht pauschal erledigt. Eine spätere echte Atlasüberarbeitung wäre ein eigenes Arbeitspaket.

Nachweise: `Saved/OverworldAIV2/SchiggyLinearFinal/` sind **Blender-Diagnosen**, keine Unreal-Abnahme. Echte native ClassicBattle-Detailvergleiche liegen in `Saved/OverworldAIV2/SchiggyClose/Before` und `After` (PNG, **2560 × 1080**, vorhandenes Capture-Format), mit UI zusätzlich unter `Saved/GlumandaV11/LiveUI/AIV2_Schiggy_Before/` und `AIV2_Schiggy_After/`. Die UI-Screenshots besitzen ihre tatsächlich gemessene Slate-Größe und werden nicht als QHD ausgegeben. Echte QHD-Oberweltpaare liegen in `Saved/OverworldAIV2/SchiggyNativeQHD/Before00000.png` und `After00000.png`: identische Kamera und Kreaturenposition, Skalierung 1,0, unveränderte native `PokeMonsterCreatureAnimInstance`. Die Idle-Atmung läuft dabei weiter; keine Behauptung einer auf dieselbe Millisekunde eingefrorenen Pose. Der Begleiter wurde vorher durch echte Enhanced-Input-Spielerbewegung auf den bestehenden Weg geführt.

## 4. Wiederverwendbare Oberweltprofile

Spezies: `DA_*/Overworld/Behavior`. Pro Begegnung: `OverworldMovement.OverrideBehavior` und `BehaviorOverride`, vor `Configure` setzen. Laufzeitstatus und Warn-/Cooldownzeit sind sichtbar, werden aber nicht als zusätzliche Saveidentität gespeichert.

| Profil | Verhalten |
|---|---|
| Neugierig | Sichtkontakt, vorsichtige Annäherung, Beobachten in respektvollem Abstand, Rückzug innerhalb des persönlichen Raums |
| Scheu | Rückzug vom Spieler; erreichbare Ausweichrichtungen, getrennte Erkennungs-/Lösedistanz |
| Territorial | Einmalige Warn-/Angriffsgeste, Sichtkontakt, mindestens 2,5 s Warnung und höchstens 160 cm vor normaler Begegnung |
| Ruhig | Langsameres Wandern, längere unregelmäßige Pausen; keine automatische zusätzliche Gruppenerzeugung |

Voreinstellung: Erkennen 550 cm, persönlicher Raum 170 cm, Lösen 750 cm, Cooldown 30 s. Territoriale Automatikauslösung benötigt zusätzlich das tatsächliche Verlassen des Reaktionsbereichs, bevor sie wieder scharf wird. Ein bloßer Ablauf der Zeit genügt nicht. Kontakt übergeht die territoriale Warnung nicht; bewusstes manuelles Interagieren bleibt möglich. `CanInitiateEncounter` kann die automatische Auslösung deaktivieren.

Konfiguration der drei vorhandenen Arten: Glumanda/Zunderlauf territorial (22 cm/s Wanderziel), Schiggy scheu (19,5 cm/s), Bisasam neugierig (27,2 cm/s). Das sind anpassbare Spielkonfigurationen, keine Behauptung offizieller Art-Persönlichkeiten. Ruhig wurde über eine temporäre Begegnungsüberschreibung geprüft. Mehrere bewusst platzierte ruhige Individuen können kleine Gruppen bilden; kein neuer Gruppenspawner und keine neue Spezies.

Die bestehenden Habitatgrenzen, Wasser-/Bodenprüfungen, lokale A*-Suche, Beschleunigung, Bremsung und Drehbegrenzung bleiben Grundlage. Alle Reaktionsziele benutzen dieselbe Erreichbarkeitsprüfung. Bei blockierten Rückzugswegen werden alternative Richtungen versucht; kein Durchlaufen von Wänden oder willkürliches Verlassen des Habitats. Es bleibt eine begrenzte lokale Suche, kein vollständiges Navigations-/Schwimmsystem.

### Echte PIE-Verhaltensprüfung

Alle vier Profile wurden vergleichbar an einem **bereits vorhandenen Wildakteur** mit temporärer Konfiguration geprüft, ohne Mapänderung oder Save. Scheu vergrößerte den Abstand in 14 s um etwa 2,9 m. Neugierig näherte sich etwa 1,3 m und wechselte zu Observe. Ruhig legte gut 2 m Wanderstrecke zurück. Territorial löste nach etwa 2,6 s Warnzeit den bestehenden Kampf aus; normale Flucht und Kamerarückkehr funktionierten.

Eine zusätzliche Prüfung hielt den Spieler nach Kampfende über **33 Sekunden** im Bereich: Cooldown erreichte 0, dennoch kein wiederholter Automatikkampf. Kampf-RNG und Kampfrechnungen werden nicht durch das Wander-RNG ersetzt.

Nachweise: `Saved/OverworldAIV2/BehaviorFinalBuild/Result.json`, `BehaviorRearmFinal/Result.json` samt Framezuständen und echten QHD-Bildern für Scheu/Neugierig/Ruhig. Territoriale Kampfdarstellung und Rückkehr sind über Zustand/Encounterresultat belegt; kein erfundener Hardwaretest.

## 5. Begleiter und Gameplay

Nur das erste Teammitglied erzeugt einen Begleiter. Ist es kampfunfähig oder ohne gültige 3D-Präsentation, erscheint kein stillschweigend ausgewähltes anderes Mitglied. Lockeres Wandern/Umsehen bei Stillstand bleibt bestehen. Bei loslaufendem Spieler erfolgt Rückruf bereits ab dem freien Wanderradius, ansonsten gilt die bisherige größere Rückrufdistanz. Aufholen nutzt tatsächliche Spielergeschwindigkeit und vorhandene artspezifische Sprintclips.

Echter Enhanced-Input-Lauf mit Brücke, Richtungswechseln und Sprint: Player maximal **315 cm/s**, Begleiter maximal **385 cm/s**, 62 Rückrufstichproben. Größter vorübergehender Abstand etwa **646 cm**, anschließend zuverlässige Rückkehr; kein behauptetes dauerhaftes Unterschreiten von 300 cm. Keine regulären Testteleports im Bewegungsnachweis. Exakt ein Begleiter, keine zusätzliche Kollision, korrektes Ausblenden/Pausieren und Wiederherstellen nach ClassicBattle. Alle drei Arten nacheinander als Begleiter geprüft.

Vollständiger Fußlauf: **102 Schritte, 286,76 m**, acht Richtungen, Sprint, Menüs, Wanderer-Dialog/Quest, Liora, Fang, Archivabschluss, Heilhaus/Heilung, beide Türübergangsrichtungen, Innen-/Außenkamera sowie Save/Load. Ein territorial automatisch begonnener Kampf ersetzt im Prüflauf die frühere manuelle E-Auslösung; keine Spielregeln oder Wegeführung dafür geändert.

Separate Prüfungen: Schiggy/Bisasam fangen, Teamwechsel, Heilitem-/Heilungs-/Inventar-/Saveübergaben; vier Classic-/WorldBattle-Konstellationen mit Angriff, Rückkehr und identischer Speicherung; tatsächliche Niederlage mit Teamheilung, Rückkehr, Autosave und erneutem Laden. Bestehende Kämpfe, Fangregeln, Teamdaten und Saveformat bleiben Grundlage.

Der ursprüngliche Dev-Slot wurde nach jedem schreibenden Test kontrolliert restauriert. End-SHA-256 unverändert: `d9bf0677d2f06bb96bfe20f0eec7a9b369ba010117de0d49f13b9d027f8dbf6b`.

## 6. Tests, Fehlversuche und Grenzen

| Prüfung | Finaler Stand |
|---|---|
| Mac Development Editor Build | bestanden |
| Erzwungener Unity-Build, adaptive Ausschlüsse aus | bestanden, `Saved/OverworldAIV2/UnityFinal/` |
| Projekt-Automation | **84 erfolgreich, 0 fehlgeschlagen, 0 Testwarnungen**, `Saved/ProjectRefinement/OverworldAIV2_AutomationFinal84/` |
| Alle vorhandenen Map Checks | **11 Maps, 0 Fehler/0 Warnungen**, `Saved/OverworldAIV2/MapChecks.json` |
| Profile/territoriale Rückkehr/kein Wiederholen nach Cooldown | bestanden |
| Begleiter/Sprint/ClassicBattle-Pause | bestanden, `Saved/StarterExpansionV1/OverworldV2Movement02/` |
| Vollständiger Gameplay-Fußlauf | bestanden, `Saved/GlumandaV11/Acceptance/OverworldAIV2Foot01/` |
| Niederlagen-Autosave | bestanden, `Saved/StarterExpansionV1/OverworldV2Defeat03/` |
| Fang/Wechsel/Heilung/SaveLoad | bestanden, `OverworldV2Capture03/` |
| Classic-/WorldBattle und SaveLoad | vier Fälle bestanden, `OverworldV2Models03/` |
| Quelle erneut geöffnet, Originalhash, FBX-Reimport, 7 × 33 Posen | bestanden |
| Kamera/140-/60-/50-/70-cm-Maßstäbe und Spezies-IDs | erhalten |
| Physischer Switch-Pro-Controller | **offen**, nicht ausgeführt/abgewartet |

Nicht verschwiegen: erste lokale Diagnoseroutinen verwendeten nicht verfügbare Python-Aufrufe bzw. falsche Socket-/Eigenschaftsnamen; diese wurden korrigiert. Eine zu einfache Kappentriangulierung/UV-Extrapolation genügte der Topologie-/Sichtprüfung nicht und wurde durch den nachgewiesenen Randzyklusverschluss ersetzt. Der alte Wander-Test erwartete fälschlich ständiges Wandern auch bei territorialem Beobachten; die neue Anforderung wird jetzt getrennt geprüft. Ein erster territorialer Rückkehrprüfer rief eine nicht vorhandene Confirm-Funktion auf; die finale Prüfung wartet den bestehenden Abschlussablauf ab.

Nach dem ersten Code-Commit deckte ein erneuter Build eine **Unity-Namenskollision** eines lokalen Typalias auf. Umbenennung und ausdrücklich erzwungener Unity-Build beheben dies ohne History-Rewrite. Die neue Skin-Prüfung hatte zunächst irrtümlich die 20 Blender-Bones auch für Unreal erwartet; die strengere finale Prüfung vergleicht stattdessen die unveränderte vollständige Originalhierarchie und Ruheposen, einschließlich Importwurzel.

Ein eigener neuer Materialusage-Status wurde beim Reimport zunächst als offenes Paket erkannt. Es wurden ausschließlich die nachweislich neu erzeugten SurfaceV2-Pakete gezielt fertiggestellt/gespeichert, kein Save All und kein fremdes Paket. Blockierte nachfolgende Testaufrufe gelten nicht als bestanden; erst die dokumentierten finalen Läufe zählen. Eine lesende Assetabfrage traf auf den bereits geschlossenen Editor und wurde später nach regulärem Start ausgeführt. Künstlich angehaltene SingleNode-Oberweltposen erwiesen sich als ungeeignete Prüfbilder und werden nicht als visuelle Abnahme verwendet. Der endgültige Oberweltvergleich benutzt ausschließlich die tatsächliche native Spiel-Animationsinstanz; normale Laufzeit- und Kampfdarstellung sind vollständig sichtbar.

Engine-Startmeldungen (unter anderem bekannte ConditionFailed-Validierung, iOS-Hilfsprogramm mit falscher CPU-Architektur und Audio-/Python-Hinweise) bleiben in den vollständigen Logs erhalten. Keine pauschale Behauptung eines vollständig warnungsfreien Engine-Starts. Der finale Projekt-Automationslauf selbst hat keine Testwarnungen/-fehler. Keine bestehenden Materialprobleme anderer historischer Testmaps stillschweigend repariert.

Offen: pixelgenaue Schattenklassifizierung bei Wind/Blattlücken, feinste Schiggy-Naht-/Atlas-/Distanzaliasingbewertung und physischer Controller. Keine neue Schwimm-KI, kein automatischer Gruppenspawner und keine allgemeine Environmentoptimierung. Kleine Kreaturen können durch vorhandene Szenendetails verdeckt sein; der Spieler-Sichtkreis wird ausdrücklich nicht für alle Kreaturen vergrößert.

## 7. Git/GitHub und nächste Abnahme

Bereits verifizierter Code-Meilenstein: `470a5110fd3598ba2ef7619f329b7e983ad69b82`. Der ebenfalls regulär gepushte Asset-/Validierungscommit `187bf25677d509a48b7bda37fb270b38444330eb` enthält die endgültigen SurfaceV2-Assets, Speziesprofile, Unity-Korrektur, Werkzeuge und diesen Prüfbericht. Beide Remote-Commits wurden direkt über `git ls-remote origin refs/heads/main` bestätigt. Acht neue/geänderte LFS-Objekte mit insgesamt **12.222.885 Bytes** wurden hochgeladen und anschließend separat von GitHub heruntergeladen; alle acht SHA-256-Prüfsummen stimmen. Normale Git-Dateien: unkomprimierte Obergrenze der 39 vorgemerkten Pfade **999.005 Bytes**, deutlich unter 1 GiB; sämtliche normalen Einzeldateien unter 100 MiB. Keine Kontrollmedien aufgenommen. Der reine Dokumentationsnachtrag wird separat regulär gesichert.

Nur benötigte Quellen, Assets, Prüfwerkzeuge und Dokumentation werden aufgenommen. Keine Kontrollbilder, Videos, Shader-Caches, Builds oder Saved-Ausgaben. Kein Force-Push, keine Käufe oder Budgetänderungen. Nach technischer Sicherung endet dieser Auftrag; weitere Kreaturen oder Landschaftsarbeiten werden nicht begonnen.

Empfehlung: die gezielte Variante B und das konfigurierbare KI-System als geprüfte Arbeitsgrundlage verwenden. Die oben benannten konservativen Schatten-/Atlasgrenzen bleiben offen. Visuelle Abnahme anhand der echten Sonnen-/Schatten- und Schiggy-Nachweise; technische Tests ersetzen diese Entscheidung nicht.

### Abschlusskontrolle

Der getrackte Arbeitsbaum war nach dem Asset-Push sauber. Verblieben sind ausschließlich dieselben 58 geschützten unversionierten Einzeldateien wie zu Beginn (die kurze Statusansicht fasst Verzeichnisse zusammen). 4064 erforderliche Kernpfade wurden vor dem Commit tatsächlich gegen den Index geprüft; keine fehlenden oder abweichenden Quellen. Acht lokale LFS-Objekte wurden vor dem Commit zusätzlich mit Arbeitsdatei und Indexpointer per SHA-256 verglichen. Remote-Downloadnachweis lokal: `Saved/OverworldAIV2/RemoteLFSAsset.json`. Ursprünglicher Spielstand und beide Backup-Refs unverändert. Engine nach den Sichtprüfungen sauber geschlossen, kein offenes/fremdes Paket verworfen.

Die nativen Oberweltaufnahmen zeigen den vollständigen Begleiter in der echten Spiel-Animationsinstanz. Frühere SingleNode-Diagnosebilder bleiben ausschließlich lokale Fehlversuchsnachweise und sind nicht die visuelle Referenz dieses Abschlusses.
