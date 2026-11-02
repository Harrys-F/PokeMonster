# VisualV2 Environment Polish V2

## Ergebnis und Abgrenzung

Ausgangspunkt `0b103701422f150b340f1de8a041e05e0a3a5577`, `main` synchron mit
`origin/main`. Ausschließlich `/Game/Maps/Dev_TestMap_VisualV2` wird gestaltet.
Westland (`/Game/Maps/Dev_WestlandRegion`), Biom und alle anderen Maps bleiben
bytegleich. Keine Übertragung nach Westland; die gestalterische Beurteilung
liegt anschließend bei Harry.

Fünf nicht kollidierende Wegflächen sind aus der Map entfernt und in eine eigene
Bodenmaterialschicht überführt. 112 tatsächlich belegte dekorative Sprites und
54 alte Gras-Planes sind durch 130 räumliche Meshinstanzen ersetzt. Weitere
62 leere, als sichtbar markierte Sprite-Actors sind entfernt. Elf neue HISM-Gruppen
enthalten insgesamt327 Instanzen einschließlich neuer Pflanzen/Uferdetails.
Elf bestehende Büsche erhalten ausschließlich am Bach niedrigere map-lokale
Skalierungen. Zusammen mit dem Bodenmaterial sind zwölf ursprüngliche Actors
geändert; alle anderen verbleibenden Original-Actors und WorldSettings haben
identische geprüfte Signaturen (`SceneProtection.json`). Keine C++-, Gameplay-,
Kamera-, Renderingprofil- oder Pokémon-Assetänderung.

## Neue Fab-Quellen

Projektbestand und `/Users/Shared/UnrealEngine/Launcher/VaultCache/FabLibrary`
wurden erneut geprüft. Gegenüber dem vorigen Fab-Test sind sieben Cachepakete
neu hinzugekommen; keine neuen externen Downloads. Die zuvor untersuchten
Projektbibliotheken bleiben Quellen; kein ungeprüfter Komplettimport in Git.

| Neues Paket | Tatsächlich geprüft | Einsatz und Eignung |
|---|---|---|
| Bigleaf Hydrangea `b8220edc` | Vorhandene FBX-Varianten, 2K-Farbe/Normal/Roughness/Opacity; A an LOD1:11.584 Dreiecke, ca.104×105×72cm | Sechs maßstäbliche Gartensträucher55–80cm hoch. A ist die aufrechte Pflanze. B ist nur ca.113cm breit und5,7cm hoch,612 Dreiecke; ausdrücklich nicht auf Strauchhöhe aufgeblasen. Der historische Gruppenname `EP2_HydrangeaB` verweist tatsächlich auf MeshA. |
| Matted Pratia `146202e2` | FBX A/B an LOD1:182/926 Dreiecke, vollständige2K-Blattatlanten | 122 niedrige Bodendecker9–17cm, unregelmäßig in bestehenden Wiesenbereichen; freie Wege erhalten. |
| Bolete Mushrooms `6c750219` | Native glTF mit vier einzelnen Pilzmeshes und2K-Farbe/Normal/ORM; gewählte Variante700 Dreiecke | 33 kleine Waldpilze,8–15cm hoch; passend für den geschützten Waldboden. |
| Bolete Mushrooms `83c5683b` | Native glTF mit fünf Varianten und2K-Farbe/Normal/ORM; gewählte Variante746 Dreiecke | 32 kleine Waldpilze, andere Silhouette/Oberfläche; keine erfundene botanische Artzuordnung. |
| Mossy Embankment `65c47533` | FBX,3.084 Dreiecke, Original ca.214×98×42cm,2K-Oberflächen | Vier kleine Moosböschungen23cm hoch, teilweise ins Ufer eingelassen; kein weiterer Wasser-Layer. |
| Mossy Stone Wall `c6fe222d` | Native glTF,8.456 Dreiecke, ca.311×52×87cm, vollständige2K-PBR-Abhängigkeiten lokal geladen | Für spätere Fantasy-Gartenmauern geeignet; hier nicht platziert, da bestehende Zaunführung sinnvoll ist und keine neue unnötige Mauer entstehen soll. Wandkollision/Nutzung nicht als im Gameplay abgenommen behauptet. |
| Grass pack – lowpoly/game-ready `42a2e737` | Ein `source/Grass.fbx`,13 Textur-/Hilfs-PNGs und Cachemetadaten/Thumbnail vorhanden | Nicht in die Map übernommen: das Paket ist eine noch zu separierende Grassammlung; vorhandene geprüfte räumliche Büschel erfüllen den Ersatzbedarf. Keine vollständige Rig-/Mesh-/Materialfreigabe dieses ungenutzten FBX behauptet. |

Importe ausschließlich unter dem bereits ignorierten lokalen
`/Game/Fab/VisualV2TrialLocal/PolishV2`. Eigene einfache Materialgraphen für
Hortensie, Pratia und Böschung liegen unter
`/Game/Environment/VisualV2EnvironmentPolishV2/Materials`.
Die Pilz-/Mauer-Importergebnisse einschließlich ihrer Original-PBR-Materialien
bleiben vollständig lokal. Bisherige PVE-/Megaplant-Bibliotheken besitzen weiterhin
die im V1-Bericht dokumentierten offenen Material-/PVE-Voraussetzungen; kein
unvollständiger Gesamtbaum oder Default-Material-Ersatz wurde eingefügt.

## Wege: tatsächlicher Aufbau vorher

Es gibt **keinen Landscape-Actor** in VisualV2. `V2_Ground` verwendet den bereits
vorhandenen `SM_FAT_StreamGround`, einen StaticMesh-Boden mit erhaltenem Teich und
Bachbett. V1 hatte die Materialien der fünf bestehenden Wegmeshes ersetzt,
keine zweite neue Wegmesh-Reihe zusätzlich zu diesen fünf angelegt.
Diese fünf Flächen lagen aber bereits zusätzlich über dem durchgehenden Boden.

| Actor | Vertices | Mesh-Z | Actor-Z | Tatsächliche Oberflächenhöhe |
|---|---:|---:|---:|---:|
| V2_Path_Main |1239|1,35cm|0,15cm|1,50cm|
| V2_Path_Wild |231|1,35cm|0,30cm|1,65cm|
| V2_Path_VillageLoop |679|1,35cm|0,45cm|1,80cm|
| V2_Path_NorthLoop |1015|1,35cm|0,60cm|1,95cm|
| V2_Path_Cottage |343|1,35cm|0,75cm|2,10cm|

Alle fünf `NoCollision`. UV-unabhängiges Weltkoordinatenmaterial `M_FAT_Path`.
Prüfquelle `GeometryAudit.json`; vollständiger Actor-/Komponentenexport
`MapBefore.t3d` ist UTF-16. Keine externen Actor-Verweise auf die entfernten
Dekorationssprites im Export nachgewiesen. Source-/Werkzeugsuche ergab keine
Gameplay-Anbindung an deren Namen.

## Wege: endgültiger Aufbau

Die fünf Weg-Actors sind tatsächlich entfernt, nicht nur unsichtbar geschaltet.
Originalmesh-/Materialassets bleiben unverändert vorhanden. Ein eigenes
`M_EP2_Ground` bindet eine2048²-Pfadmaske an denselben Boden. Sie verwendet genau
die bestehenden fünf Polylinien; warme, gedämpfte Erde-/Kiesfarbe und zurückhaltende
Normalen werden innerhalb derselben Oberfläche gemischt. Welttexturskalierung
240cm, weiche ca.42cm-Übergänge mit kleinen unregelmäßigen Kanten.
Halbe Kernbreiten Main92,Wild68,VillageLoop115,NorthLoop108,Cottage82cm.
`Tools/VisualV2EnvironmentPolishV2/PathMaskSource.json` enthält die Quelle;
`GeneratePathMask.py` regeneriert ausschließlich die eigene Maske.

Die erste Bildprüfung zeigte weiterhin dominanten Holzmulch der Forest-Path-
Textur. `RefinePaths.py` wechselt im eigenen Graphen auf die vorhandene Fab-
Grass-And-Rubble-Oberfläche mit neutralisierter warmer Erdfärbung. Keine neuen
Weg-Planes, kein Material-Displacement und kein Z-Fighting zwischen mehreren
Wegskins. Terrainmesh, Höhen, physikalische Bodenabfrage, Navigation und Kollision
sind bytegleich erhalten. Die Integration als Materialschicht auf dem tatsächlichen
StaticMesh-Boden vermeidet eine unnötige neue Landscape-Architektur.

Brücke, besonderer Heilhaus-Vorplatz, dessen eigener Zugang und vier feste
Trittsteine bleiben als funktional/gestalterisch begründete Sonderflächen.
Innenraum-Fußbodenplanes und Teppiche sind keine veralteten Pflanzenkarten und
werden nicht pauschal gelöscht. Bereits unsichtbare alte Boden-/Wegprototypen
werden nicht fälschlich als aktuell gerenderte Doppeloberflächen gezählt.

## Flache Dekoration und räumlicher Ersatz

174 dekorative PaperSpriteActors waren als sichtbar markiert. Davon112 mit
belegtem Quellsprite und62 ohne Quellsprite. Tatsächlicher Ersatz der112:
36 Gras-,31 Blumen-,27 Stein- und18 Stumpf-Sprites. Dafür vorhandene StyleHex-
Büschel/Blumen, RockEnv-Kleinsteine und Projekt-Stumpfmodelle instanziert.
Die54 `P2D_Grass_*`-Planes bilden18 alte Kreuzkarten-Gruppen; jede Gruppe wird
durch ein räumliches vorhandenes Mehrhalm-Büschel ersetzt. Zusammen130 Instanzen.

Bei92 alten Sprites war das Component-Collision-Flag zwar QueryAndPhysics,
die verwendeten Sprite-Assets haben aber `SpriteCollisionMode.NONE` und keinerlei
BodySetup; sie stellten keine physikalische Hindernisgeometrie bereit.
Diese Quellen wurden erst nach dieser Prüfung ersetzt. Alle neuen kleinen
Dekorationsgruppen sind ausdrücklich nicht blockierend.

Keine sichtbaren reinen dekorativen PaperSpriteActors verbleiben in der Zielmap.
Bereits ausgeblendete Altobjekte, Editor-Billboards, Figuren-/Pokémon-Komponenten,
Text/UI und Effekte bleiben erhalten. Keine aktuell sichtbaren Baum-Sheets waren
als vollständige zu ersetzende Bäume nachgewiesen; bestehende hochwertige3D-Bäume
werden nicht grundlos ersetzt. Blattatlanten auf räumlichen Pflanzenmeshes sind
keine einzelnen zur Kamera gerichteten alten Busch-/Baum-Sheets.

## Wiese, Wald, Bach und Dorf

Die blühende V1-Wiese und ihre natürlichen freien Zwischenräume bleiben erhalten;
122 niedrige Pratia-Patches ergänzen Bodendetails ohne eine gleichförmige neue
Grasdecke. Bestehende Grashöhen, Farben und HISM-Distanzen bleiben als Basis.
Der Wald erhält65 kleine Pilze beider geprüfter Pakete. Vorhandene Farne, Bäume
und Waldwege bleiben; keine neue Waldkamera und keine Rücknahme der Beech-Rücknahme.

Am Bach ergänzen vier maßstäbliche Moosböschungen die bereits vorhandenen kleinen
Kiesel und das abgesenkte Bett. Die tatsächliche Third-Person-Prüfung zeigte noch
zu hohe alte Uferbüsche; elf davon werden map-lokal auf58cm begrenzt. Ein weiterer
geprüfter Busch blieb bereits darunter. Dadurch mehr Durchblick auf Wasser,
Brücke und Boden. Keine Änderung am Wassermaterial, an der Zahl der Wasserflächen,
Wasserhöhe, Teich, trockener Trennung, Barrieren, Brücke oder GaradosV4.

Der bereits schlüssige U-Zaun des Kräutergartens mit seinen verbundenen Segmenten,
Fass, Kiste und Bank bleibt. Sechs passende Hortensien rahmen Garten-/Hausränder;
keine schwebenden neuen Requisiten, keine unnötige Mauer trotz verfügbarem Paket.
Kleine Dekorationen erhalten bodenbündige Bounds-Anker; der begehbare Fußlauf prüft
die tatsächlichen Laufwege. Keine Gebäude-/Innenraum-Neugestaltung.

## Natürliche Pokémon und Projektschutz

Keine zusätzliche Showpopulation, keine neue Pokémon-Art und keine KI-/Spawn-
Parameteränderung. Vorhandene zehn Zonen, Limit14 und höchstens sechs gleichzeitig
kuratierte Arten bleiben bestehen. Über beide aktiven Läufe beobachtet:
Bisasam,Pikachu,Raupy,Enton,Karpador,Glumanda (stabiler interner Schlüssel
`Zunderlauf`) und Habitak, nicht alle gleichzeitig. Erfasst wurden Wander,Rest,
Idle,Observe,Forage,Social,Group,Curious/Approach,Alert,Sleep,Battle und Cooldown.
Maximal14 im aktiven Lauf,13 in den eingefrorenen Hauptmessungen. Vorhandene
Meshy-Modelle, Tagesrhythmen, Namen, Kampf/Fang und Begleiter weiterverwendet.

KameraV3 bleibt350cm,−12°, nur horizontale Drehung; Referenzgröße140cm.
Software-Lumen/IFG,TAAU,C75%,High,VSM4,120-Minuten-Weltuhr und75° Mittag unverändert.
Die globale AA-CVar4 ist hier nicht der endgültige View-Pfad: der vorhandene
map-eigene TAA-Blendable bleibt identisch, positiveGPU/TAA-/IFG-Pässe bestätigen
den Pfad. QHD-PNGs und Viewport2560×1440 geprüft;1920×1080 ist die rechnerische
interne75%-Zielauflösung, in diesem Auftrag kein neuer interner ViewRect-Nachweis.

Hash-Basis:6328 bereits vorhandene versionierte/unversionierte Dateien,
1709 weitere lokale Originalassets,707 vorhandene Save-Dateien und143 neue
Cacheeingabedateien. Nutzerdiff in `Config/DefaultEngine.ini` ausdrücklich erhalten
und nicht in den Commit aufnehmen. Endprüfung `ProtectionFinal.json`.

## Technische und funktionale Abnahme

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Editor-Build | Exit0,4,18s; vorhandene installierte UE5.8.4 CL58902052, kein Enginewechsel |
| Vollständige Automation |325 succeeded,0 succeededWithWarnings,0 failed/notRun/inProcess |
| Strenger QA-Exportvertrag | Engine0, Wrapper0; `FullAutomation/Result.json` und `Report/index.json` |
| Zwölf bestehende Projektmaps | Je0 Fehler/0 Warnungen zwischen expliziten Map-Check-Markern; keine neue Map, kein Speichern anderer Maps |
| Echter PIE-Lauf | `PIE_Gameplay01`,101,32s, erfolgreich |
| Separater aktiver Development-Lauf | `NativeGameplay01`,110,85s Test/150,79s Prozess, erfolgreich |
| Bewegung/Kollision/Navigation |20 zusammenhängende reale Eingabe-/Physik-Wegpunkte über Wiese,Dorf,Wald,Habitatgrenzen und Brücke; kein Teleport zwischen den Wegpunkten; vorhandene KI bewegt sich weiter |
| Sprint/Steuerung | Bestehende Enhanced-Input-Sprintaktion ein/aus; keine physische Gamepadabnahme behauptet |
| Dialog | Vorhandener Wanderer, Gespräch und Rückkehr zur Steuerung |
| Kampf/Fang | Natürliches Habitat-Pokémon, reguläre ClassicBattle-Attacke/AP-Verbrauch, MasterBall nur im isolierten Testinventar, normaler Fang und eindeutige zusätzliche Teaminstanz |
| Begleiter/Team | Sichtbarer regulärer Begleiter, Teamsortierung und Teamansicht, nach Laden/Reise korrekt |
| Innenraum/SaveLoad | Tatsächlicher Türdurchgang und Rückweg; isolierter Menüroundtrip erhält Team,AP,Inventar,Position,Weltzeit und Cutaway-Zustand |
| Mapwechsel | Tatsächliche Reise zur bestehenden Dev_TestMap und normaler Loader zurück zur gespeicherten VisualV2 einschließlich Team,Position,Begleiter |
| Tageszeit |06/12/19/22 im aktiven Test; Mittag75°, Tageslänge120min |
| Stabilität | Eigener Prüfeditor und Spielprozesse regulär beendet, kein Force Quit; finale Funktionsläufe ohne Fatal/Assertion-/Trial-Materialfehler |

Rohlogs werden nicht als warnungsfrei bezeichnet: Beim Editor/NullRHI-Start stehen
17 bestehende `LogAutomationTest: Error: Condition failed` vor der eigentlichen
325er-Projektserie. Native `-game`-Starts über die Editor-Binärdatei melden weiterhin
experimentelle Engine-Toolset-Pythonfehler wegen fehlender Editor-Typen; keine
Projekt-Gameplayfehler daraus ableiten. `idevice_id: Bad CPU type` wurde in diesen
Endläufen nicht beobachtet und nicht repariert.

Die aufbewahrten Zwischenlogs enthalten eigene, korrigierte Werkzeugfehler:
mehrteiliger glTF-Import statt angenommener Einzelmesh-Ausgabe, präzisierte
Sprite-Kollisionsprüfung, nachträgliche Instancing-Usage zweier neuer lokaler
Pilzmaterialien sowie ein verfrühter Aufnahmestart vor PIE. Diese sind keine
bestandenen Zwischenprüfungen. Die endgültigen PIE-/Native-/Automationsergebnisse
sind oben separat benannt.

## FPS-Vergleich und Aussagegrenzen

AppleM4/Metal, macOS27.2(26B123), separate Development-Spielprozesse über
UnrealEditor `-game`, tatsächliches DeviceProfileMacEditor; kein gepackter
Shipping-Test. Keine Videoaufnahme während der Messungen, VSync/FPS-Limit temporär
0, danach wiederhergestellt. Drei6s-Fenster je sechs Hauptpositionen,4s Wartezeit
vor jedem Fenster; reale QHD-Stills erst nach dem Sampling. Tag1,12:00/75° über
bestehenden Menüpause-/isolierten SaveLoad-Pfad gehalten. **Statische Messung,
keine reguläre bewegte Gameplay-Framerate.**

Die erste vollständige Reihe zeigt starke Drift nach den Bearbeitungs-/Prüfläufen.
Alle tatsächlichen Werte bleiben sichtbar, ohne sie als unveränderliche Kosten
der neuen Gestaltung auszugeben. `pmset -g therm` meldete keine aufgezeichneten
Warnstufen; GPU-Takt/Temperatur wurden nicht gemessen. Thermisches Throttling oder
eine andere konkrete Driftursache ist deshalb nicht bewiesen.

| Standort | FPS vorher | FPS nachher | Nachher-Spanne | GPU vorher/nachher ms | Frame-p95 nachher ms |
|---|---:|---:|---:|---:|---:|
|Blumenwiese|35.11|27.02|22.70–32.05|27.45/36.65|40.97|
|Waldrand|40.79|28.81|23.48–35.48|23.57/33.89|44.91|
|Flussufer|39.09|27.81|23.14–34.88|24.59/34.50|43.08|
|Felsen|46.40|32.42|27.40–40.45|20.59/29.99|37.29|
|Dorf|36.02|25.22|23.35–28.31|26.81/28.87|44.42|
|Lebensraum|45.44|31.65|29.32–34.64|21.03/30.61|33.64|

Dies ist das Mittel der drei Fenster-FPS bzw. Fenster-p95, kein gepooltes p95.
Render-Thread-Zeiten enthalten Warte-/Synchronisationsanteile. GPU-Passbereiche
werden nicht addiert. Vollständige Einzelwerte inklusive Game-/Renderthread,
Basepass,IFG,TAA und Schatten stehen in `Analysis.json` und den unveränderten CSVs.
Vergleich mit V1-Werten aus einer anderen Sitzung ersetzt keinen aktuellen
Kontrolllauf. Keine Grafikqualitätsreduzierung zur Beschönigung dieser Werte.

Der gezielte gepaarte Nachtest ist im folgenden Abschnitt gesondert ausgewiesen;
fehlgeschlagene Referenzrekonstruktionen werden nicht als belastbare Performance-
Vergleiche verwendet. **Stabile30FPS im bewegten Gameplay sind nicht nachgewiesen.**

## Endgültiger gepaarter Nachtest

`NativePaired06`, regulär mit Exit0 beendet. Drei Vergleichspaare je Wiese,
Waldrand und Dorf im selben frischen Development-Prozess: After–Before,
Before–After,After–Before. Vier Sekunden Stabilisierung und sechs Sekunden CSV
je Zustand; keine Videoaufnahme. Kamera,Spielerposition,QHD und Population der
Paarpartner geprüft. Alte Bodenbindung, fünf Wegmeshes,112 Quellsprites,54 Gras-
Planes und elf alte Uferbüsche werden nur im RAM aus dem echten Vorher-Audit
rekonstruiert.182 stationäre Referenz-Actors; neue elf Gruppen und aktuelle
Uferbüsche alternierend ausgeblendet. Positionen,Maßstäbe,Meshbindung und
Sichtbarkeit kontrolliert. Keine Kopie/Änderung der gespeicherten Map.

Ein bloßes Actor-Visible-Flag reicht als Nachweis nicht: die erste echte Sichtprobe
zeigte, dass vor der verzögerten Actor-Konstruktion gesetzte Wegmeshes nicht
vollständig dargestellt wurden. Darum Meshbindung/Komponentensichtbarkeit nach
der Konstruktion setzen und erneut fotografieren. Erst `NativePairedSmoke05`
belegt den tatsächlichen alten braunen Weg mit harter Kante. Nur die danach
abgeschlossene vollständige Reihe06 wird hier quantitativ verwendet.

| Standort | FPS vorher | FPS nachher | Vorher-Spanne | Nachher-Spanne | Framezeit vorher/nachher ms | p95 nachher ms |
|---|---:|---:|---:|---:|---:|---:|
|Blumenwiese|29.21|28.08|23.89–32.70|23.50–31.36|34.88/36.16|38.44|
|Waldrand|32.45|30.36|27.91–37.49|26.34–35.40|31.27/33.44|35.83|
|Dorf|28.40|27.13|25.38–33.53|24.47–32.31|35.76/37.48|39.94|

| Standort | GPUTime-Counter vorher/nachher ms | Basepass vorher/nachher ms | GameThread nachher ms | RenderThread nachher ms |
|---|---:|---:|---:|---:|
|Blumenwiese|33.85/35.16|7.79/8.12|1.70|36.15|
|Waldrand|30.32/32.30|6.61/7.05|2.07|33.42|
|Dorf|34.78/26.73|9.05/9.78|1.72|37.47|

Die gepaarte Framezeit steigt im Mittel um ca.1,28/2,16/1,72ms; kein Performance-
Gewinn behauptet. Auch innerhalb dieser Reihe bleibt zeitliche Drift sichtbar.
Die GPUTime-Zahl im Dorf sinkt, während die reale Framezeit und der Basepass
steigen. Dieser Counter wird deshalb ausdrücklich **nicht** als bewiesene8ms-
GPU-Ersparnis interpretiert. Ursachen der Abweichung/Render-Wartezeiten sind nicht
abschließend isoliert. Keine Summierung überlappender GPU-Pässe.

Die kleineren paarweisen Unterschiede erklären nicht automatisch den ganzen
Unterschied zwischen den getrennten kalten/warmen Hauptreihen. Dies ist eine
Gestaltungsänderung mit messbaren Mehrkosten und verbleibender Messunsicherheit,
keine erfolgreiche30-FPS-Optimierung. Der Waldrand liegt im Mittel knapp über30,
sein p95 aber35,83ms. **Keine stabilen30FPS und keine Freigabe bewegter30FPS.**
`PairedAnalysis.json` enthält alle Einzelpaare. Die Begleiter-/Funktionsläufe
enthalten Aufnahmen,Menüs,Kampf,Laden und Reise und sind kein sauberer FPS-Benchmark.

Zwischenläufe01/02 scheiterten an Python-API-Aufrufen,03 konnte Static-Uferbüsche
nicht verschieben,04 bestand die zusätzliche echte Wegdarstellungsprüfung nicht.
Sie und der kurze Diagnose-/Sichtlauf05 werden nicht als endgültige Performance-
Abnahme gezählt. Alle behalten ihre Rohlogs; keine Produktionsdatei wurde dafür
umgeschrieben. Der Endlauf06 besitzt keine Static-Mobility-Warnungen oder Trial-
Materialfehler. Die ursprüngliche Renderingkonfiguration bleibt während aller
Varianten gleich; nach Prozessende keine temporären Einstellungen erhalten.

## Echte Vergleichsaufnahmen

Neun kontrollierte Bildpaare, jeweils2560×1440, gleiche Kamera/Position innerhalb
0,1cm/Grad, gleiche Tageszeit/Grafikqualität; Idle-/Pokémon-Posen nicht identisch:

`Saved/ProjectRefinement/VisualV2EnvironmentPolishV2/NativeBefore01/<Szene>.png`
und `NativeFinal01/<Szene>.png`.

Szenen: Blumenwiese,Waldrand,Flussufer,Felsen,Dorf,Lebensraum,Kraeutergarten,
Bachbett,Felsgruppe. `Felsen` bezeichnet weiterhin den etablierten Blick bei den
alten Höhenstufen, `Felsgruppe` den eigenen Detailblick auf die gerundeten Felsen.
`Ergebnisuebersicht.png` und `VorherNachher.png` sind nur proportional verkleinerte
echte Unreal-Bilder mit Beschriftung. Keine KI-Bilder, Retusche, erfundenen FPS
oder künstlichen Bewegungsframes. Zusätzliche Nacht-/Innenraum-/Teambelege in den
beiden Gameplayordnern. Keine neue große Rohbild-/Videofolge.

Zum Erkunden vorhandene VisualV2 öffnen. Der erhaltene V1-Besuchshelfer funktioniert
weiter in normalem PIE mit denselben AREA-Werten und geschütztem Rückkehranker:

```text
py exec(open(r"/Users/harry/Developer/PokeMonster/Tools/VisualV2FabAssetTrialV1/Visit.py").read(), {"AREA":"Blumenwiese"})
```

Weitere AREA: Waldrand,Flussufer,Felsgruppe,Kraeutergarten,Lebensraum; Zurueck für
Rückkehr. Kein neuer unabhängiger Teleport-/Speicherdienst eingeführt.

## Offene Grenzen und Git-Umfang

Die dichte, teilweise stilisierte V1-Busch-/Blumenfarbigkeit, die alten rechteckigen
Test-Höhenstufen und der sichtbare Rand der kleinen Testwelt sind keine umfassend
neu gestaltete Landschaft. Nahe Bäume verwenden weiterhin die vorhandene
kamerabezogene Dither-Freistellung; diese wurde nicht umgebaut. Uferansichten sind
freier, aber nicht von jeder Richtung vollständig frei von Vegetation.
PVE-Gesamtpflanzen, ungenutztes Gras-FBX und spätere echte Mauerplatzierung benötigen
eigene gezielte Abnahme. Keine fehlende Spezialfunktion als fertig ausgeben.

Nur eigene Map-, Werkzeug-, Material-/Masken- und Dokumentationsänderungen
versionieren. Fab-Originale/lokale Imports und Kontrollmedien bleiben lokal.
**Ein frischer öffentlicher Checkout benötigt Harrys separat lizenzierte Fab-
Imports.** Keine pauschale Aufnahme der Bibliotheken und kein Lizenzversprechen.
Keine Änderungen an Nutzerkonfiguration, Originalmodellen, GaradosV4 oder Saves.
Kein Worktree, keine Projektkopie, neue Map oder destruktiver Git-Befehl.
Commit-/Remote-/LFS-Nachweise werden lokal in `GitFinal.json` und `RemoteLFS.json`
abgelegt. Der versionierte Bericht ist über `git log -1 --format=%H --
Docs/VISUALV2_ENVIRONMENT_POLISH_V2.md` seinem Abschlusscommit zuzuordnen.
Nach der Sicherung keine weitere Gestaltung, insbesondere keine Westland-Übernahme.
