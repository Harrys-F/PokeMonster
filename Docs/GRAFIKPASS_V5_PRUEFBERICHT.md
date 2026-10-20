# Grafikpass V5 – Heilhaus, ursprüngliche SilverLady, Wald und Wege

Stand: 20.10.2026. Ausschließlich `/Users/harry/Developer/PokeMonster`; bestehende Karte `/Game/Maps/Dev_TestMap_VisualV2`. Ausgangsstand `c705896d31c4caebecc54c07b8919b5ba9c41af6`, auf `main` und direkt geprüftem origin/main identisch.

## Ergebnis

V5 ist tatsächlich in der vorhandenen Unreal-Map umgesetzt. Die V4-Steinbodeninstanz ist vollständig entfernt, das Heilhaus hat wieder einen durchgehenden Holzboden. Wartebereich, Kamin und Arbeitsdetails sind verbessert. SilverLady verwendet wieder exakt ihr ursprüngliches Material; Form, Gesicht, Frisur, Kleidungsschnitt und Proportionen wurden nicht umgestaltet. Wege zeigen weniger einheitliches Orangebraun, stärker wechselnde Erd-/Sandtöne und echte kleine Kiesinseln. Vorhandenes Unterholz wurde gezielt umgruppiert, zwei unpassende V4-Zaunelemente entfernt.

**Editor-Build, 50/50 Projekttests, elf Map Checks und vollständiger realer Gameplay-Fußlauf bestanden.** Die künstlerische Abnahme bleibt beim Nutzer. Das Fensterflackern ist weiterhin nicht sicher reproduziert und ausdrücklich nicht als endgültig behoben erklärt. Kein weiterer automatischer Landschafts-Art-Pass; die Kreaturenintegration wurde nicht begonnen.

## Schutz und Vorbereitung

AGENTS.md, GRAFIKSTIL.md, TECHNIK.md, ENTSCHEIDUNGEN.md, SPIELIDEE.md, SPIELREGELN.md sowie die relevanten V4-Unterlagen gelesen. Vorhandenen Blender-/Unreal-Workflow und die vorher bereitgestellte Konzeptreferenz verwendet. Keine Konzeptkunst als Unreal-Nachweis ausgegeben.

53 vorhandene unversionierte Dateien vor/nachher einzeln per SHA-256 geprüft und unverändert erhalten. Darunter die vier Kreaturen-GLBs, eine unversionierte Testkarte, frühere Bereinigungsunterlagen und Prüfwerkzeuge. Sämtliche zehn anderen vorhandenen Mapdateien bytegleich erhalten. Bestehende Blenderquellen und Originalassets unverändert; neue Details separat. Keine neuen Maps, Projektkopien, Worktrees oder vollständigen Backups. Keine Dateilöschung außerhalb der ausdrücklich freigegebenen drei Mapinstanzen; keine Git-Resets, kein Clean, Prune oder History-Rewrite.

Vollbackup unverändert unter `backup/full-03492bd` und `refs/archive/pokemonster/full-backup-03492bd`: `03492bd96b4dba44692f675c19d5f11abfa86b4b`. Der Backup-Commit ist kein Vorfahr der neuen Remote-Historie.

## 1. Steinboden vollständig entfernt / Holz

Entfernt wurde genau die kollisionsfreie Actor-Instanz mit `SM_HH4_FlagstoneApron` aus der VisualV2. Das alte Meshasset und seine Blenderquelle bleiben als Entwicklungsreferenz erhalten; **null Steinbodeninstanzen** in der gespeicherten aktuellen Karte. Kamin und Wandsockel dürfen weiterhin Naturstein sein.

Die dreißig vorhandenen 2-m-Boden-Visuals hatten geringfügig kleinere, abgeschrägte Außenkanten und dadurch ein zusätzliches großes Plattenraster. Sie verwenden am selben Ort jetzt exakt anschließende Plane-Flächen und das neue gemeinsame weltbasierte `M_HH5_AgedOak`. Kein zusätzlicher aufgesetzter Materialfleck und kein neuer Bodencollider. Die originale begehbare Bodenfläche, sämtliche Gebäudekollisionen und Laufwege sind erhalten.

Das Material verwendet die vorhandene gemalte Holztextur mit unterschiedlich breiten Dielen (14/21/18/25 cm), versetzten Längen/Fugen, ungleichen harmonischen Brauntönen, dezenter Abnutzung und feiner Maserung. Weltkoordinaten führen das Muster über alle Module fort, statt es pro 2-m-Platte neu zu beginnen. Matte Rauheit 0,91 und niedriger Specular-Anteil. Die bestehenden grünen Teppiche liegen weiterhin flach im Holzbodenbereich; keine Steinfläche darunter oder daneben.

Die QHD-Spielkamera zeigt den Holz-/Brauncharakter und das entfernte große Plattenraster klar. Die Gestaltung bleibt eine materialbasierte Holzoberfläche auf realem Boden; keine Behauptung, einzelne Dielen seien vollständig dreidimensional ausgearbeitet. In großen Flächen ist weiterhin Wiederholung der zugrundeliegenden Textur möglich, jedoch kein Neustart an jedem alten Bodenmodul.

## 2. Einrichtung und Licht

Empfang hinten, Wartebereich links, beide Heilbetten rechts und große Schränke an den Wänden erhalten. Der Hauptweg vom Eingang bis zur Heilinteraktion bleibt frei.

- Kamin: eigenes mattes, warmgraues Kalksteinmaterial mit vorhandener gemalter Steintextur; ursprüngliche echte Bogen-/Mauergeometrie erhalten. Keine neue Feuerlichtquelle oder starken Kontraste.
- Ein maßstäblicher Lesesessel mit abgerundeter Holzverbindung, Armlehnen, gepolsterter Sitz-/Rückenfläche; Sitzhöhe ungefähr 43–46 cm, Gesamthöhe ungefähr 1,03 m für den 1,40-m-Player.
- Vier neue gewölbte Leinenpolster auf den vorhandenen Wartebänken; echte Naht-/Randgeometrie.
- Kleiner Beistelltisch aus vorhandenem Tischasset neben dem Sessel; neue gebundene Kräuterbücher.
- Weitere Bücher und vorhandenes Heilmittel-Tablett am bestehenden Kräuterarbeitstisch, auf gemessener Tischhöhe positioniert. Regale, Kräuterborde, Pflanzen, vorhandene Betten und Teppiche weiterverwendet; keine wahllose zusätzliche Füllung.
- Hauptlaufweg nicht zugestellt. Nur der neue Sessel erhält eine eigene einfache Möbelkollision; kleine Dekoration bleibt kollisionsfrei. Bestehende Möbelkollisionen nicht entfernt oder verschoben.

Das vorhandene schattenlose diffuse Innenraumlicht wurde von 800 auf 1000 lm und von 900×800 auf 1200×1000 cm erweitert. Temperatur bleibt auf dem bisherigen Wert, Lichtkanal 1, kein Schlagschatten und null indirekter GI-Beitrag. Das macht Randbereiche gleichmäßiger lesbar, ohne Außenbeleuchtung oder Außenschatten anzutasten. Dekoratives Kaminleuchten bleibt unverändert ohne zusätzliche Lampe. Keine globale Lumen-/Exposure-/Skylight-Änderung.

Die Runtime-Prüfung bestätigt bei tatsächlichem Aufenthalt im Raum die schattenfreien Playerkomponenten und die Rückkehr zu Außenlichtkanälen/Schattenflags beim Verlassen. Vorhandene schattenfreie Raum-/NPC-Komponenten und die neuen Möbel bleiben diesem Raumkonzept zugeordnet. Räumliche Materialwirkung bleibt erhalten; ein natürlicher Helligkeitsabfall ist weiterhin vorhanden, keine völlig flache Beleuchtung behauptet.

## 3. SilverLady – ursprüngliches Erscheinungsbild wiederhergestellt

**V4-Neufärbung deaktiviert.** Der bestehende riggte Heilhaus-NPC bindet auf seiner Mesh-Komponente wieder genau:

`/Game/Characters/NPCs/SilverLady/Materials/MI_SilverLady_V1`

Das ist die vorhandene Original-Materialinstanz mit ihren ursprünglichen Texturen, Normalen-/Rauheits-/Metallinformationen und Farben; kein neuer grüner/cremefarbener Shader oder Umfärbe-Multiplikator auf der Figur. Der unbenutzte V4-Gewandshader bleibt als alte Entwicklungsreferenz erhalten, wird in dieser Präsentation jedoch nicht mehr ausgewertet.

Ein unabhängiger lesender Blender-Vergleich bestätigt die riggbare V4-Kopie gegen die originale `SilverLady_HealerPose.blend`: **177.228 Vertices, 149.999 Dreiecke, identische Vertexkoordinaten, Polygonindizes, UVs und Objekttransformation**. Keine neue Frisur, keine Gesichts-, Proportions- oder Kleidungsmodellierung. Die Heilpose ist eine technische Pose des vorhandenen Modells, keine neue Körpergestaltung.

- Geometrie-SHA-256: `ceab26358a50a567fc3c03680f7496994cca80d36c880cc4f794b97edb8890ef`
- Polygonstruktur-SHA-256: `1cc3defdf12b0fbafca3b8dfe52e025244e05acf2c3052a07946dd046a9388cf`
- UV-SHA-256: `12e1990c1c58e848ec8dd9a4d56c8e67b2cfa09cdacf1a2179a9534e2c60ff45`

Nachweis: `Art/Characters/NPCs/SilverLady/ArtV5_OriginalAppearance.json`. Das originale Materialasset selbst blieb bytegleich; die gespeicherte VisualV2-Komponentenbindung ist der technische Wiederherstellungsschritt. Unterschiedliche Raumbeleuchtung kann die sichtbare Helligkeit beeinflussen; kein Anspruch pixelidentischer Renderbilder bei unterschiedlichem Innenlicht.

Die bestehende dezente Vier-Sekunden-Idle und das kleine Rig mit drei Deform-Bones plus FBX-Helfer bleiben erhalten. Kein unnötiges neues Rig und keine riskante zusätzliche Gewand-/Gesichtsanimation. 19 echte QHD-Idle-Bilder und Runtime-Bonesampling bestätigen Bewegung ohne Verschiebung des Actor-Ursprungs. Weitergehende Idle-Gestik wurde nicht als neue Verbesserung behauptet.

Position hinter dem Empfang, Skalierung 0,905 (rund 1,72 m), bestehender Heilpunkt, NPC-Identität, Blickwendung, Dialog, Heilfunktion und Speicherung erhalten. Keine zusätzliche Figurenkollision. Der Sprite-Fallback ist weiterhin funktionsfähig. Die frühere V4-Idee einer eigenständigen Kleidungs-/Gesichts-Neugestaltung wird gemäß dem ausdrücklichen V5-Auftrag nicht fortgesetzt.

## 4. Waldwege und Waldränder

Drei neue private V5-Wegmaterialvarianten ändern die Oberfläche, nicht Wegeführung, Masken, Brücke oder Bodenkollision. Mehrere Weltmaßstäbe kombinieren lehmige Braun-/Erdtöne, sandige abgetretene Bereiche, kleine Kies-/Laubflecken und wechselnde Farbstruktur. Die erste zu blasse, sandig gleichmäßige Fassung wurde nach echten QHD-Aufnahmen korrigiert: dunklere Erdanteile, stärkere gebrochene Farb-/Kiesinseln und echte kleine Kiesgeometrie in begrenzten Wegtaschen.

96 der schon vorhandenen 160 V4-Kieselinstanzen wurden in unregelmäßige, flach eingebettete Gruppen innerhalb des Waldwegs umgeordnet; übrige Kiesel bleiben am Rand. Keine neuen Hindernisse: sämtliche betroffenen Kleinteile sind weiterhin kollisionsfrei. Alle Wegmittellinien und Steuerungsrichtungen bleiben erhalten. Kein Leistungsbenchmark oder behaupteter Performancegewinn.

Zwei unpassende V4-Zauninstanzen entfernt, ihre Meshassets nicht gelöscht. Die 55 V4-Farninstanzen und der Waldanteil der bestehenden V4-Grasgruppe (112 Grasinstanzen) wurden in ungleich große Inseln mit unterschiedlichen Höhen umgeordnet. Vorhandene gefaltete 3D-Farne weiterverwendet. Keine neuen Außeninstanzen, Bäume oder dichte gleichmäßige Reihen. Alle älteren Pflanzen/Bäume und ihre Positionen erhalten.

Die 23 V4-Strauchinstanzen wurden kleiner und mit mehr Freiräumen angeordnet. Eine erste Umgruppierung ragte in der tatsächlichen Spielkamera zu weit auf den Weg; vor Abnahme korrigiert. Finale Strauchzentren liegen mindestens 140 cm außerhalb des nächstgelegenen bestehenden Wegrands. Die sichtbare Figur bleibt im finalen Waldvergleich frei. Neues privates Totholzmaterial reduziert den zuvor orangefarbenen, frisch geschnitten wirkenden Astton, ohne originale Baum-/Vegetationsmaterialien zu verändern.

Die Anzahl der 727 V4-Unterholz-/Kleinteilinstanzen bleibt gleich. Die endgültigen Unterschiede sind Farb-/Materialvariation, andere Gruppierung, ruhigere Totholztöne, Kiesinseln und die zwei entfernten Zäune. Keine Behauptung einer vollständigen neuen Pflanzenbibliothek oder restlos beseitigter flacher Wirkung aller alten Pflanzen.

## 5. Fenster und TAA

78 tatsächliche 1280×720-Bilder in vier zeitlich geordneten Sequenzen: Innenraum still, Innenraumbewegung, Annäherung außen, Rückweg außen. Die sichtbaren Fenster blieben in den geprüften Abschnitten stabil; der letzte Teil des Außenrückwegs zeigt das Fenster nicht mehr. Innen nutzt das Spiel seine unveränderte feste Raumkamera.

**Das sporadische Fensterflackern ist nicht zuverlässig reproduziert.** Daher keine bestätigte Ursache und keine spekulative Änderung an Fenstermaterial, Geometrie, TAA, Lumen oder globalen Lichtwerten. Keine Videoabnahme behauptet; Einzelbildfolgen sind keine lückenlose zeitliche Prüfung.

TAA bleibt über das vorhandene map-eigene `PokeMonsterTemporalAABlendable` am unveränderten OutdoorExposure-Volume erhalten. Wichtig zur Messinterpretation: Der globale `r.AntiAliasingMethod`-CVar steht im bestehenden Projekt bewusst auf 4; das Blendable wählt TAA pro Spielansicht. Der CVar allein ist deshalb **kein gemessener Nachweis der endgültigen View-Methode**. Unveränderte Map-/Postprocess-Signatur und vorhandener bestandener TemporalAA-Projekttest bestätigen den Erhalt des bestehenden Pfades. Kein zusätzlicher Renderthread-/GPU-Profilinglauf in diesem Art-Auftrag.

## 6. Echte QHD-Vergleiche

Alle neun statischen Vorher-/Nachher-Paare: echte Unreal-PIE-Spielkamera, **2560×1440 Pixel**, High, **100 % Screen Percentage**, FOV 35°. Spielerposition, Kamera und Rotation je Paar mit maximal weniger als 0,001 cm/Grad Differenz geprüft. Außen weiterhin Pitch −50°/Yaw −45°, innen die vorhandene feste Raumkamera. Fotopositionierung diagnostisch; der getrennte Gameplay-Rundweg ist ohne Testteleports.

Die Vergleichstafeln setzen lediglich zwei echte, verkleinerte QHD-Aufnahmen nebeneinander: links V4 vor der Änderung, rechts V5. Die originalen PNGs liegen unverkleinert lokal. Keine generierten Bilder als Testnachweis. Kontrollbilder und Aufnahmen werden nicht hochgeladen.

### Wald

![Wald V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Wald.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Wald00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Wald00000.png)

### Wiese

![Wiese V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Wiese.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Wiese00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Wiese00000.png)

### Flussufer

![Flussufer V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Flussufer.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Flussufer00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Flussufer00000.png)

### Uferabzweig

![Uferabzweig V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Uferabzweig.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Uferabzweig00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Uferabzweig00000.png)

### Heilhaus

![Heilhaus V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Heilhaus.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Heilhaus00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Heilhaus00000.png)

### Fassade

![Fassade V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Fassade.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Fassade00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Fassade00000.png)

### Innenraum

![Innenraum V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Innenraum.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Innenraum00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Innenraum00000.png)

### Empfang

![Empfang V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Empfang.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Empfang00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Empfang00000.png)

### Heilbereich

![Heilbereich V4 / V5](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/Heilbereich.jpg)

[QHD vorher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Before/Heilbereich00000.png) · [QHD nachher](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/VerifiedFinal/Heilbereich00000.png)

Zusätzliche Detailausschnitte aus derselben echten QHD-Aufnahme (vergrößerte Crops, keine zusätzlichen Kameraperspektiven):

- [Holzboden](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/BodenDetail.jpg)
- [SilverLady mit Originalmaterial](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/SilverLadyDetail.jpg)
- [Wartebereich](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/WartebereichDetail.jpg)
- [Kamin](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/Comparisons/KaminDetail.jpg)
- [Fenster-Bildübersicht](/Users/harry/Developer/PokeMonster/Saved/ArtPassV5/WindowContact.jpg)

### Visuelle Eigenbewertung

| Frage | Tatsächlicher Befund |
|---|---|
| Steinboden vollständig entfernt? | Ja, null FlagstoneApron-Instanzen; nur Holz und die bestehenden Teppiche auf der Bodenfläche. |
| Holzboden hochwertiger? | Durchgehender, ohne das alte große Plattenraster; wechselnde Dielenbreiten und ruhigere Brauntöne. Feine Texturwiederholung bleibt möglich. |
| Heilhaus gemütlicher? | Sessel, Polster, Beistelltisch/Bücher und besser lesbarer Steinkamin; Raummitte frei. Noch schlichter als die Konzeptillustration. |
| SilverLady originalgetreu? | Originale Meshform/UVs/Transform nachgewiesen, exaktes Originalmaterial wieder gebunden; keine neue Farben-/Gesichts-/Haarform. |
| Wege natürlicher? | Deutlich weniger durchgehendes Orangebraun, sichtbare Erd-/Sand-/Kiesgruppen. Insgesamt etwas sandiger; Palette zur visuellen Abnahme vorgelegt. |
| Waldränder glaubwürdiger? | Unterschiedliche Farnhöhen, weniger Strauchband, dunklere Äste und keine beiden unpassenden Zäune. Einige ältere Pflanzen bleiben einfach. |
| Innenraum gleichmäßig? | Breiteres ausschließliches Raumlicht, keine neuen direkten Schlagschatten; Randabfall bleibt erhalten. |
| Spielbarkeit erhalten? | Vollständiger echter Rundweg und drei Möbelkollisionsproben bestanden. |

## 7. Technische Ergebnisse

| Prüfung | Ergebnis |
|---|---|
| Mac Development Editor Build | Exit 0, 12.08 s; keine C++-Änderung. |
| Vollständige Projekt-Automation | **50/50**, null Warnungstests, fehlgeschlagene oder übersprungene Tests; Exit 0, 27.88 s. |
| Alle vorhandenen Map Checks | Elf Karten geladen; jeweils null Fehler und Warnungen. Keine andere Karte gespeichert. |
| Ranger-V3-Regressionsaudit | Bestehender FinalMapAudit unverändert auf NPCMotionV3 ausgeführt; bestanden. |
| Gespeicherte Map frisch geladen | Strenger V5-Signatur-/Änderungsumfangsvergleich bestanden; erneute Prüfung nach Gameplay ebenfalls bestanden. |
| Vollständiger Gameplay-Fußlauf | **102 Schritte, 285.11 m, 179.74 Spielsekunden**, ohne Testteleports; bestanden. |
| Bewegung/Kamera | Acht Richtungen, Richtungswechsel, normales Gehen 210 cm/s, Sprint maximal 315 cm/s, Außen-/Innenübergänge. |
| Gameplay | Wanderer-/Liora-Dialoge, Quest-/Archivabschluss, Brücke, Wildkampf/Fang, Menü, Heilhaus gerade/diagonal rein/raus, Heilung/Checkpoint und Save/Load bestanden. |
| Runtime-Licht-/NPC-Audit | 324 Innenframes, 2326 Außenframes, 37 Gesprächsframes, null Auditfehler. |
| Möbelkollisionen | Kamin, Arzneischrank und neuer Sessel blockieren tatsächlichen Enhanced Input; Rückweg möglich, kein Durchfallen. Separate Diagnose-Startpositionen, kein Ersatz für den vollständigen Fußlauf. |
| SilverLady / Idle | Originalmaterial im Runtime-Audit geprüft; Blickwendung, Heilinteraktion und Sprite-Fallback bestanden. 19 echte Idle-Einzelbilder über rund zehn Sekunden. |
| Neue Blenderquelle | In unabhängigem Blenderprozess erneut geöffnet; keine fehlenden Texturen, Geometrie/UVs und Datei-SHA unverändert durch die Prüfung. |
| Python-Sicherheitstests | MapLifecycle 5/5, DevelopmentEvidence 8/8. |
| Erforderliche Projektdateien | 3694 Dateien im Art-Snapshot per SHA-256 bestanden; Bericht wird separat ergänzt. |
| Git | Arbeits- und Index-Diff-Check bestanden; ausschließlich explizite geprüfte Pfadliste. |

Der originale Dev-Spielstand ist nach dem Fußlauf bytegenau restauriert:
`a0ad009a7b3c6f883d1413b0f96df5b25bc7ab953d0154e29ae50f35ad48bf0a`.

Kein FPS-Benchmark, keine umfangreiche GPU-Analyse, keine neue Standalone-/Cook-Abnahme und kein neues Video. Diese nicht ausgeführten Prüfungen sind keine behaupteten Erfolge.

### Diagnosen und Warnungen

- Erste lesende Inventarausgabe musste Unreal-Arrays für JSON in Listen umwandeln. Keine Assetänderung dadurch.
- Erste Bodensichtprüfung führte zu den dokumentierten Erd-/Kies-/Strauchkorrekturen; nicht als finaler Erfolg ausgegeben. Bücher/Tablett anhand tatsächlicher importierter Tisch-/Meshbounds korrigiert.
- Die von V4 abgeleitete Möbelprobe schrieb zunächst in den alten ignorierten Reviewpfad. Die drei tatsächlich bestandenen V5-Proben wurden unter V5 erhalten; die alte zweifache V4-Metadatei aus ihrer unveränderten versionierten ArtV4Acceptance-Kopie wiederhergestellt. Alle V5-Diagnosepfade korrigiert. Keine Originalquelle, kein Asset und keine der 53 geschützten unversionierten Projektdateien betroffen.
- Der allgemeine historische BlenderSources-Prüfer erlaubt nur bereits versionierte Quellen und lehnte die neue noch ungestagte V5-Datei korrekt ab. Eigener unabhängiger lesender V5-Reopen-Audit danach bestanden; der alte Guard wurde nicht gelockert. Der abgelehnte Aufruf wird nicht als erfolgreicher Source-Test gezählt.
- Die enge Stagingvorbereitung stoppte zuerst bei den expliziten `SM_HH5_*.fbx`-Namen, weil diese nicht `V5` heißen. Genau diese drei erstellten Exporte in die Positivliste aufgenommen; danach kompletter Index-/LFS-Check bestanden. Keine pauschale Aufnahme.
- Kein bestätigter neuer Material-/Shaderkompilierungsfehler. Engine-Logs enthalten weiterhin bekannte generische Startup-`Condition failed`-Meldungen vor den Projekttests, `idevice_id`/Bad-CPU-type-, Audio-/MotionVectorSimulation-/MCP-/Telemetrie-Warnungen. Nicht unterdrückt; 50/50 bezieht sich auf die strukturierten Projekttests, nicht auf ein vollständig warnungsfreies Engine-Startlog.

## 8. Neue Quellen und Assets

Neue unabhängige Quelle: `Art/HealingHouse/Source/HealingHouse_ArtV5.blend`. Drei eigene FBX-Exporte unter `Art/HealingHouse/Exports/SM_HH5_*.fbx`. Keine neue SilverLady-Blenderquelle notwendig: vorhandene riggbare Geometrie ist nachweislich originalgetreu; nur Originalmaterialbindung in der Map geändert.

| Mesh | Vertices | Dreiecke |
|---|---:|---:|
| LinenCushion | 768 | 1528 |
| ReadingChair | 2298 | 4492 |
| HerbalBooks | 636 | 1224 |

Unreal-Meshes und sieben private Materialien unter `/Game/Environment/HealingHouse/ArtV5/`. `M_HH5_AgedOak`, `M_HH5_LinenJoinery`, `M_HH5_HearthLimestone`, `M_HH5_Deadwood` sowie `M_HH5_LandscapeGround/MainPath/NorthPath`. Bestehende shared Materialien, Originaltextures, V4-Quellen und die SilverLady-Assets selbst unverändert.

Versionierte Umsetzungs-/Prüfwerkzeuge unter `Tools/ProjectMaintenance/*V5*.py`, Actor-Vertrag `ArtV5Signatures.json`, kompakte Ergebnisse `ArtV5Acceptance.json`. Geometrie-/Kontakt-/Material-/Gruppierungsnachweise unter `Art/HealingHouse/ArtV5_*.json` und `Art/World/VisualV2WorldArtV7/ArtV5_*.json`. Umsetzungsskripte sind einmalige zustandsabhängige Schritte, nicht blind auf V5 erneut ausführen.

## 9. GitHub-Sicherung

- Art-Commit: `a6d731c21ff4e1bf09beabc3861084e9213178e8` – `art: polish VisualV2 wood floors and restore SilverLady`.
- Regulärer Push `c705896..a6d731c` nach origin/main erfolgreich; Remote-Commit direkt mit `git ls-remote` bestätigt.
- 45 explizit geprüfte Commitpfade. Normale Git-Inhalte unkomprimiert: 1.643.969 Bytes; 15 LFS-Objekte mit zusammen 5.260.896 Bytes.
- Alle 15 Remote-LFS-Inhalte tatsächlich heruntergeladen und SHA-256 sowie Größe mit den lokalen/indexierten Quellen verglichen. Erfolgreich; keine Zugangsdaten oder Download-URLs gespeichert.
- Getrackter Arbeitsbaum nach Art-Commit sauber. Der folgende Dokumentationscommit enthält ausschließlich diesen Bericht und den dazu passenden erforderlichen Dateisnapshot; keine neuen LFS-Inhalte.

Der Bericht wird anschließend als getrenntes Dokumentationspaket gesichert; sein eigener Commit-Hash steht im Git-Log und in der Abschlussantwort. Keine Kontrollbilder, Videos, Caches oder temporären Dateien hochgeladen. Keine kostenpflichtigen GitHub-Aktionen, Budgetänderungen oder Force-Pushes.

Vorhandener, bewusst unversionierter Restbestand (nach Art-Commit; bleibt unverändert):

```text
?? Art/Characters/Creatures/
?? Content/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1.umap
?? Docs/ALTER_WORKTREE_ABC_DATEILISTE.csv
?? Docs/ALTER_WORKTREE_ABSCHLUSSPRUEFUNG.md
?? Docs/ALTER_WORKTREE_DATEIINVENTAR.csv
?? Docs/ALTER_WORKTREE_ENTFERNUNG_PRUEFBERICHT.md
?? Docs/ALTER_WORKTREE_REIMPORT_PRUEFUNG.json
?? Docs/ALTE_ARBEITSORDNER_AUFRAEUMEN_V1_PRUEFBERICHT.md
?? Docs/SPEICHERBEREINIGUNG_V2_LOESCHLISTE.csv
?? Docs/SPEICHERBEREINIGUNG_V2_LOESCHLISTE.txt
?? Docs/SPEICHERBEREINIGUNG_V2_PRUEFBERICHT.md
?? Docs/SPEICHERBEREINIGUNG_V2_ZURUECKGESTELLT.csv
?? Docs/SPEICHERBEREINIGUNG_V3_PRUEFBERICHT.md
?? Tools/VisualV2EnvironmentQualityV1/
?? Tools/VisualV2QualityV2/__pycache__/
```

Das sind die geschützten 53 Einzeldateien, in `git status --short` teils als Verzeichnis zusammengefasst. Kein behaupteter vollständig leerer Git-Status; der getrackte Entwicklungsstand ist sauber und mit origin/main abzugleichen.

## 10. Verbleibende Punkte und Stopp

Fensterflackern bleibt ohne reproduzierten Befund offen. Die Szene ist technisch geprüft und gegenüber V4 gezielt verbessert; die Konzeptillustration wird nicht als vollständig erreicht oder die Gestaltung automatisch als endgültig freigegeben erklärt. Einzelne ältere Pflanzen-/Möbelformen bleiben einfacher, und die neue Wegpalette ist sandiger als vorher. SilverLady bleibt verbindlich beim Originalmodell; keine weitere optische Neugestaltung.

Nach V5 stoppen. Kein weiterer Landschafts-Art-Pass und keine Änderungen an den vorhandenen Kreaturen-Originalen. Die Kreaturenintegration ist der nächste gesonderte Entwicklungsabschnitt.
