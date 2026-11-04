# Westland – VisualV2-Integration V1

Stand: 04.11.2026. Bestehendes Projekt, Ausgangscommit `6d44b0bc0af316be3774266975205ede7b5d63cb`, Branch `main`. Ziel ist ausschließlich `/Game/Maps/Dev_WestlandRegion`; VisualV2 bleibt unveränderte Entwicklungsreferenz. Lokaler annotierter Sicherungspunkt vor Migration: `checkpoint/westland-visualv2-v1-pre-migration-20261104`. Keine neue Map, kein Worktree, kein neuer Download und keine neue Vollkopie.

## 1. Ergebnis und Bestandsaufnahme

Geeignete fertige VisualV2-Oberflächen, Architekturdetails und Begegnungsfunktionen wurden regional angepasst übernommen. Bereits gemeinsame Systeme wurden erhalten. Alle 3162 ursprünglichen Actors bleiben vorhanden, einschließlich ihrer ursprünglichen Actor-/Komponententransforms und Kollisionsverträge. Gespeicherte Szenenanzahl: 3203 Actors. Es handelt sich um eine Integration in die vorhandene Region, keine Übernahme der VisualV2-Geometrie.

| System | Vorher in Westland | Integration / Abgrenzung |
|---|---|---|
| Kampf, Fang, Level, EP, Entwicklung, Team, Inventar, Begleiter, Quests, Save/Load | aktuelle gemeinsame Dienste bereits vorhanden | unverändert wiederverwenden und regressionsprüfen; keine zweite Implementierung |
| Kamera, Grafik, Weltuhr | Third Person V3, Profil C, Software-Lumen/IFG, Tageszyklus und 120 Minuten bereits angeschlossen | keine Einstellungsänderung |
| Gelände | 80 organisch bearbeitete statische Kacheln, kein Landscape | Geometrie/Höhen erhalten; eigenes regionales PBR-Bodenmaterial |
| Vegetation | dichte bestehende Baum-, Gras-, Farn-, Strauch- und Blumengruppen | vorhandene regionale Verteilung erhalten; ein Viertel der Blumenplätze variiert, Gesamtzahl unverändert |
| Wege und Brücken | sechs Routen, elf Zugänge, zwei Brücken | tatsächliche regionale Wegmaske; normale doppelte Wegdarstellung entfallen; originale Kollision erhalten; Holzbrücke mit vorhandenen Modulen überarbeitet |
| Gewässer | vorhandener Fluss, drei flache Wasserhabitate; kein Teich | funktionierende Fluss-/Ufergeometrie und Single-Layer-Water-Material erhalten; keine unpassende Teichkopie |
| Gebäude | elf Regionalhäuser plus Heilhaus, zwölf Controller | PBR-Putz/Holz/Stein/Dächer mit weiterhin funktionierendem Cutaway; Grundrisse/Eingänge unverändert |
| NPCs | drei regionale NPCs plus Heilerin, jeweils passende 3D-Darstellung bereits vorhanden | dieselben Quellen, Identitäten, Rollen, Dialoge und Standorte; keine doppelten NPCs oder neuen Missionen |
| Habitate | 16 Zonen, bestehende Regeln und globale Wildgrenze 14 | erhalten; vier V5-Begegnungsfelder an geeignete tatsächliche Zonen gebunden |
| Pokémon-Bewegung | aktuelle Pikachu-/Karpador-Geschwindigkeiten und Clips bereits gemeinsame Artdaten | bestehendes V7-Karpador-Wasser-Opt-in zusätzlich exakt in Westland freigeben; keine anderen Arten-/Rigänderungen |
| Testinhalte | Modellgalerie nicht in Westland | alle 68 Prüfdarsteller bleiben VisualV2; 49 statische Kandidaten sind ausdrücklich keine Wild-Pokémon |

## 2. Regionale Bereiche und Anpassungen

| Regionsteil | Tatsächliche Änderungen / Kontrolle |
|---|---|
| Südlicher Spielerhof / Start | regionale PBR-Böden und Hausmaterialien, bestehende Zugänge/Funde/Dialogquelle erhalten; Hofwiesen-Begegnungsfeld abseits des Weges |
| Dorf / elf Regionalgebäude | Oberflächen einschließlich Seiten und Rückseiten, vorhandene Cutaway-Maskierung; ursprüngliche Zäune/Gärten/Dekorationen erhalten |
| Heilhauszugang und versetzter Innenraum | Türanker und Raumkoordinaten regional statt VisualV2; alle vier Wandseiten sichtbar, stabile Tür, bestehender Raumkamerabegrenzer |
| Nördliche Runde / Steinkreis | Boden-/Wegübergänge, vorhandene Wälder und Missions-/NPC-Standorte erhalten |
| Offene Ostwiesen | zusätzliche vorhandene Blumenformen auf bestehenden Standorten, eigenes Wildwiesen-Begegnungsfeld |
| Waldrand / dichter Wald | regionale Waldbodengewichtung, Bäume/Unterholz erhalten; Waldrandfeld und große Begrenzungsbüsche außerhalb der Routen |
| Waldpfad / Lichtung / Ruinen | bestehende Wege und Habitatidentitäten, eigenes Ruinenfeld und PBR-Untergrund; keine Modellgalerie |
| Fluss / Mühle / beide Brücken | originales Wasser, Uferhöhen, drei Wasserzonen und Steinkollision; Holzmodule auf tatsächliche 16m-Spannweite angepasst |
| Regionsausgang / Kartenübergänge | Gelände und Übergänge erhalten; gemeinsame Grafik-/Zeit-/Save-Dienste geprüft |

Kein pauschales Kopieren von Actor-Koordinaten. Die regionale E/N-Basis, die vorhandene `T_WR_PathCoverage` und tatsächliche Tür-/Raumtransforms sind maßgeblich. Terrainhöhen, Habitatgrenzen, Missions- und NPC-Standorte wurden nicht versetzt.

## 3. Materialien, Vegetation und Brücke

Neuer eigener Assetpfad: `/Game/Environment/WestlandVisualV2IntegrationV1/Materials/`. `M_WI_RegionalGround` ist eine bereinigte Ableitung des vorhandenen V4-PBR-Graphs, mit Westland-Wegmaske und regionalen Wald-/Ufergewichten. Keine VisualV2-Wegmaskenkoordinaten. Bei der abschließenden Graphkontrolle wurde zusätzlich der im V4-Ausgangsgraph enthaltene lokale Teichbett-Farbterm (720/−1800cm) aus der eigenen regionalen Ableitung entfernt; Westland verwendet seine eigene Fluss-/Feuchtigkeitsmaske. Der Originalgraph bleibt unverändert. Vier private `M_WI_Fade*`-Materialien behalten die ursprüngliche Custom-Primitive-Data-0-/Dither-Cutaway-Semantik. Zwei private Instanzen binden die vorhandenen Blumen-/Strauchmaterialien für Instancing.

Wiederverwendet: vorhandene V3/V4-PBR-Stein-/Dach-/Holz-/Pflasteroberflächen, V6-Heilhausdetails, V7-Oak/Lime/Sage-Innenraummaterialien, lokale bereits importierte PBR-Texturabhängigkeiten und StyleHex-Fab-Pflanzennetze. Keine Fab-Originale oder Meshy-Originale verändert. Keine Originaldateien oder neuen lizenzierten Pakete öffentlich hochgeladen; eigene Ableitungen enthalten Assetverweise auf die vorhandene lokale Bibliothek.

Alle 80 Terrainkacheln verwenden die regionale Ableitung. 17 normale Weg-/Zugangsrenderer sind unsichtbar; Actors und Kollisionsflächen bleiben erhalten. Besondere Plätze und Brücken bleiben echte sichtbare Geometrie. Die bereits vorhandene regionale Wegmaske enthält auch drei Platzflächen; diese erscheinen jetzt flächiger erdig/kiesig statt des vorher überwiegend grünen Untergrunds. Das ist im Dorf-Vergleich sichtbar und Teil von Harrys ausstehender Gestaltungsbeurteilung. Kein zusätzliches übereinanderliegendes Gelände.

Wildblumen: 12.369 vorher und nachher. 3.094 bestehende Plätze verwenden vier weitere vorhandene Clump-Formen, weiterhin instanziert, ohne neue Blütenkollision. Die übrigen 9.275 Plätze bleiben bei ihren vorhandenen Gruppen. Bäume, Gras und Unterholz behalten Anzahl, Positionen, Dichte und bisherige Reichweiten. Die verwendeten Alternativnetze besitzen deutlich weniger Dreiecke/Materialslots als die bisherigen mehrteiligen Blüten; ein isolierter GPU-Gewinn nur dieser Maßnahme wurde nicht gemessen und wird nicht behauptet.

Holzbrücke: ursprüngliche Spannweite 1.600cm, Breite 250cm, begehbare Oberkante Z=−23,5cm. 76 maßgerechte Bretter, durchgehende Träger, verbundene Pfosten/Geländer/Diagonalstreben und zwei eingesetzte Lager. Nur drei neue instanzierte Darstellungsgruppen. Die ursprüngliche Brückenkollision bleibt unverändert; neue sichtbare Teile haben keine zweite Spielkollision. Der neue Höhentest entdeckte zunächst eine mehrdeutige Balkenrollausrichtung. Diese wurde über eine definierte Y/Z-Achse korrigiert; der abschließende Test misst Bretteroberkante und Kollisionsboden identisch. Steinbrücke und Flussbettgeometrie bleiben erhalten.

## 4. Heilhaus und NPCs

Originaler Eingang bei (−7742,819; −36097,801; 1107,5)cm, Drehung −45°. Bestehender Innenraumboden Z=1000cm und Raumgröße unverändert. Sieben vorhandene V6-Detailgruppen mit 58 Instanzen wurden relativ zu diesen Türankern übertragen, darunter Rahmen, Wainscot, Decke, Windfang und Glas. Keine neue Raumkopie und kein veränderter Grundriss. Bei der abschließenden Sichtprüfung fehlte unter dem übernommenen Windfang ein Bodenanschluss: Die Tür liegt lokal beiX−670cm, der alte Boden endet beiX−520cm. Eine eigene165×225cm große Bodenfläche schließt diesen Darstellungsstreifen bisX−685cm, bündig aufZ1000cm; keine neue Kollision, kein Schattenlicht und keine Änderung des vorhandenen Tür-/Kollisionssystems. NativeRoomFinal01 und PIERoomFinal01 prüfen diese endgültige Fassung.

Alle 18 bestehenden Innenwandsegmente bleiben sichtbar und sind aus dem Außen-Cutaway ausgeschlossen. Außenfassade und Dach behalten ihre Funktion. Zwölf vorhandene Raumlichter wurden an die geprüfte Innenraumpresentation angepasst; eine vorher in Westland fehlende breite schattenlose Rect-Aufhellung wurde am entsprechenden Raumanker ergänzt. Kein neues dynamisches Schattenlicht. Die Heilerin behält Identität, Dialog, Standort, Heil-/Kontrollpunktfunktion und 3D-Originaldarstellung.

## 5. Habitate, Begegnungen und Modelltestbereich

Vier neue, begehbare Felder verwenden ausschließlich das bestehende V5-System und vorhandene Westland-Zonen: Hofwiese E/N(−288,−181), Wildwiesen(145,25), Waldrand(178,65), Waldruinen(239,175)m. Trigger je 520×360cm, 35 sichtbare kleinere Sträucher; die gesamten Footprints liegen innerhalb der gedrehten Habitatgrenzen. 16 größere Kollisionsbüsche stehen abseits von Wegen, Wasser, Gebäuden, NPCs und Fundobjekten.

Chance 0,18 pro 250cm, globale Pause 12s und 800cm Reiseabstand sowie Wildgrenze 14 bleiben unverändert. Die reale native Zufallsbegegnung, ein normaler Kampfschritt mit AP-Verbrauch und anschließender Fang wurden geprüft. Stehen und Menü lösen keine Würfe aus.

Die einzige Produktions-C++-Änderung erweitert den bestehenden ausdrücklich aktivierten Wasser-Opt-in von VisualV2 auf die bereits zentral definierten zwei integrierten Maps. Tiefen-/Körper-/Hindernis-/Streckenprüfungen bleiben unverändert; der alte serialisierte Feldname bleibt kompatibel. Natürliches Karpador-Schwimmen wurde ohne erzwungenen Spawn oder Ziel beobachtet. Die flachen regionalen Wasserzonen sind keine geeignete Garados-Umgebung; Garados V4 und sein Modell/Clips bleiben unverändert verfügbar.

Nach tatsächlichem Kartenwechsel zu VisualV2 wurden `pm.TestGround.List`, `pm.TestGround.Go Pikachu`, `pm.TestGround.Go Karpador`, `pm.TestGround.Go Aquana` und `pm.TestGround.Return` geprüft. Alle 19 spielbereiten und 49 statischen Modelle, insgesamt 68 Darsteller, bleiben dort vorhanden. Native Rückkehr stellte die gemessene Ausgangsposition wieder her. Der bestehende Save-Loader wechselte anschließend zurück nach Westland mit Team, Begleiter, Uhr und Renderingprofil.

## 6. Performance

Gemessene Hardware: Mac16,12 / Apple M4 / 16GB, macOS27.2; UE5.8.4 / Metal. Separate Development-Spielprozesse, keine Videoaufnahme. Ausgabe 2560×1440, C75 (nominal1920×1080 intern), High2, TAAU über die vorhandene Profil-/Postprocess-Integration, Software-Lumen+IFG, VSM mit vier Strahlen. Die globale AA-CVar allein steht weiterhin auf4 und ist kein Nachweis für tatsächlich verwendetes TSR; die vorhandene Postprocess-Auswahl wurde nicht verändert. Keine globale Qualitätsreduzierung.

Identische sechs Standorte, Third Person V3 / FOV75 / −12°, Mittag B75. Pro Standort drei sechssekündige CSV-Fenster nach vier Sekunden Beruhigung; Reihenfolge der Standorte wiederholt. Uhr für die statische Paarung gehalten, gleiche Anfangsbedingungen und natürliche Bevölkerungsverwaltung; in sämtlichen36 Fenstern jeweils drei vorhandene Populationsactors. Der vollständige lebende Rundgang wird separat ausgewiesen. Fotos erst außerhalb der Messfenster. Sämtliche sechs finalen Nachher-Zeilen stammen einheitlich aus NativeAfterFinal01 nach Bodenanschluss und regionaler Graphbereinigung. Die ursprünglichen Zwischenmessungen aus NativeAfter01 (Heilhaus40,50FPS) und NativeRoomBenchmark01 (44,99FPS) bleiben separat erhalten. Unterschiedliche Laufzeitdrift ist weiter zu berücksichtigen. VSync0, MaxFPS0, GPU-CSV aktiviert, anschließend wiederhergestellt beziehungsweise eigener Prozess beendet.

| Standort | FPS vorher | FPS nachher | GPU vorher ms | GPU nachher ms | Frame-p95 vorher ms | Frame-p95 nachher ms |
|---|---:|---:|---:|---:|---:|---:|
| Dorf | 42.27 | 44.12 | 22.62 | 21.68 | 25.37 | 24.99 |
| Wiese | 36.42 | 38.61 | 26.43 | 24.85 | 29.03 | 28.24 |
| Waldweg | 34.85 | 34.59 | 27.70 | 27.90 | 30.09 | 32.56 |
| Wald | 37.57 | 37.52 | 25.62 | 25.65 | 28.01 | 29.34 |
| Fluss | 37.63 | 39.63 | 25.63 | 24.25 | 28.26 | 28.28 |
| Heilhaus | 52.32 | 43.32 | 17.05 | 21.10 | 21.38 | 25.80 |

| Standort | Game vorher/nachher ms | Render vorher/nachher ms | 1%-Low vorher/nachher FPS |
|---|---:|---:|---:|
| Dorf | 1.66 / 1.83 | 23.65 / 22.66 | 37.75 / 37.29 |
| Wiese | 1.67 / 1.70 | 27.45 / 25.90 | 33.48 / 25.55 |
| Waldweg | 1.59 / 1.57 | 28.69 / 28.91 | 31.39 / 27.29 |
| Wald | 1.65 / 1.69 | 26.61 / 26.64 | 34.68 / 32.60 |
| Fluss | 1.59 / 1.90 | 26.57 / 25.23 | 34.10 / 33.79 |
| Heilhaus | 1.63 / 1.56 | 19.11 / 23.08 | 35.10 / 36.88 |

Die Messung zeigt keinen pauschalen Performancegewinn. Die Außenstandorte sind weitgehend vergleichbar oder teilweise schneller; der Wald liegt praktisch auf Referenzniveau. Das Heilhaus bleibt gegenüber vorher deutlich teurer. Das ist bei der Innenraumerweiterung zu berücksichtigen. Zwischen den Nachher-Wiederholungen besteht deutliche Drift (beispielsweise Dorf 45,14 → 44,73 → 36,78 FPS). Thermik ist eine mögliche, hier nicht nachgewiesene Erklärung; ohne kontrollierte A/B-Thermalmessung werden die Differenzen nicht einzelnen Materialien oder Lichtquellen kausal zugeschrieben. Keine Grafikreduzierung als Gegenmaßnahme.

### Tatsächlicher dynamischer Regionalrundgang

Der zusammenhängende Rundgang lief 706.50s / 4441.20m mit regulären Enhanced-Input-Bewegungen, lebender KI und Weltuhr, ohne Teleport und ohne Foto-/Videoaufnahme. Vorhandener `pm.Speed 3` außerhalb, `pm.Speed 1` am Heilhaus, am Ende auf1 zurückgesetzt. Zusätzliche Ost-Mühlenrunde und vollständiger Waldpfad sind enthalten; alle sechs vorhandenen Hauptrouten wurden abgelaufen. Bestehende Heilhaus-Verlagerung ist eine normale Spielfunktion und keine Testteleportation.

CSV-Rundgang: 33.95 FPS im Mittel; GPU 28.49ms; Game 2.53ms; Render 29.40ms; Frame-p95 36.38ms; 1%-Low 17.02 FPS; größte Framezeit 244.79ms. Der komplette Rundgang liegt vor dem letzten rein dekorativen Windfang-Bodenanschluss; Kollision, Bewegung, Materialien der übrigen Region und Logik blieben dabei unverändert. Die endgültige Raumfassung wurde danach separat in PIE und nativ geprüft. Abschließend wurde noch die geerbte VisualV2-Teichmaske aus dem eigenen regionalen Graph entfernt; keine Geometrie oder Kollision änderte sich. Der endgültige Stand wurde nochmals mit339 Automationstests,12 Map Checks und drei neuen nativen Messfenstern an allen sechs Standorten geprüft. Dieser gemischte Lauf enthält auch vorhandene Dialog-/Menü-/Türsituationen und Streaming; er ist keine reine stationäre GPU-Messung. Die früheren 33,93 FPS stammen aus einer anderen VisualV2-Route und sind kein identischer Westland-Vorhervergleich.

Auffällige CSV-Frames: 2854 über33,33ms, 202 über50ms und 12 über100ms bei 23819 ausgewerteten Frames. Die Ursachen der Spitzen wurden nicht abschließend isoliert.

**Stabile 30 FPS für die gesamte Region sind hier nicht nachgewiesen.** Durchschnitt, p95 und Spitzen werden getrennt ausgewiesen. Keine garantierten 30/60FPS und keine neue temporale Lumen-Freigabe. EditorStartupMap und GameDefaultMap zeigen bereits im vorgefundenen Nutzerstand auf Westland und wurden nicht verändert.

## 7. Tatsächlich ausgeführte Tests

| Prüfung | Ergebnis |
|---|---|
| Editor-Build | Build03, Exit0; vorherige Build01/02 ebenfalls erfolgreich |
| Vollständige Automation | Automation05: 339 bestanden, 0 Fehler, 0 Testwarnungen, 0 ausgelassen / in Arbeit |
| Strenger Wrapper | Engine0 und Wrapper0; Automation01 war mit 338/339 und Wrapper1 ausdrücklich fehlgeschlagen, Ursache behoben und vollständig wiederholt; Automation02 wurde vor Teststart wegen eines noch regulär schließenden Editors abgewiesen |
| Neue Migrationstests | Heilhaus/Anker/vier Wände; vier Habitatfelder und gemeinsame Regeln; Terrain/Wege/Brückenboden/TestGround-Abgrenzung |
| Zwölf Map Checks | EditorGroundFinal01: alle zwölf vorhandenen Maps, jeweils 0 Fehler und 0 Warnungen; keine Prüfmap gespeichert |
| PIE | PIEReview03 mit regionalen Dialogen, Kampf/Fang, Heilung, Kontrollpunkt, Quest/UI, Team/Begleiter, Interior-SaveLoad und acht Tageszeiten; PIEProgression01 mit Glumanda→Glutexo→Glurak, Abbruch/erneutem Versuch und Erhalt individueller Daten |
| Separates Gameplay | NativeFeatures02: Buschbegegnung/Kampf/Fang, Türtempo1/2/3, natürliche Wasserbewegung, Team/Begleiter, tatsächlicher Mapwechsel und68er-Galerie, Rückkehr mit Save-Loader |
| Neustart | NativeRestart01: exakte eigene gespeicherte Party/AP/Inventar/Uhr/Position plus Begleiter und Profil C nach frischem Prozess |
| Kollisionen / Hauszugänge | NativeAccess03: alle elf tatsächlichen Vordertüren mit echten Ein-/Austritten und lokalen Cutaways; alle vier neuen Felder abgelaufen. NativeAccess02 hat zuvor fünf vollständige bestehende Hauszugänge in beiden Richtungen bestätigt. Die alte Gartenhaus-Mittellinie bleibt als konkrete Einschränkung offen; keine Behauptung, alle elf ursprünglichen Weglinien seien vollständig begehbar. Wildpopulation nur für diese spezielle Kollisionsprüfung im isolierten Prozess deaktiviert; lebende KI separat geprüft |
| Vollständiger Rundgang | NativeTour01: alle sechs Routen, Dorf/Nordrunde/Mühle/Brücken/Heilhaus/Wald/Lichtung/Ruinen/Ausgang; echte Eingaben, keine Diagnoseteleports |
| Schutzaudit | ursprüngliche 6914 Dateien, 3578 geschützte Assets und 768 bestehende Saves geprüft; keine fehlenden Dateien, keine unzulässigen Änderungen |
| Hardware-Controller | kein neu zertifizierter physischer Gamepad-Test; bestehende Belegung unverändert, Eingaben automatisiert über EnhancedInput |

Ein früher nativer Galeriecheck maß zu früh nach Mapstart vor dem ersten stabilen Bodenkontakt; nach korrektem Abwarten ist die Rückkehrprüfung bestanden. Eine frühe Zugangsprüfung verlangte zu enges punktgenaues Erreichen eines Kurvenwegs; Routenwegpunkte verwenden nun75cm Toleranz innerhalb des2,2m-Streifens, Tür-/Innenraumziele weiterhin28cm. Die wiederholte genaue Zugangsprüfung fand anschließend eine reale ursprüngliche Unstimmigkeit: Die Gartenhaus-Mittellinie führt gegen die unveränderte Rückwand (Zielweltposition −13317,674/−11485,290cm). Keine neue Kollision und kein neuer Begrenzungsbusch liegen dort. Die Fronttür bleibt über die vorhandene offene Seite erreichbar; alle elf tatsächlichen Vordertüren wurden separat durchlaufen. Der Haupt-Rundgang ist vollständig bestanden, aber die vollständige Begehbarkeit aller elf ursprünglichen Zugangsmittellinien wird ausdrücklich nicht als bestanden ausgegeben. Diese fehlgeschlagenen Zwischenläufe bleiben in Saved und gelten nicht als Erfolge.

Bereits vor Migration vorhandene Experimental-Toolset-Pythonstartmeldung (`PythonTestRunner` im Game-Modus fehlt) tritt auch nachher auf; getrennte Engine-/Infrastrukturmeldung, kein als bestanden umetikettierter Funktionstest. Keine neuen fatalen Fehler, Ensures oder Material-Compile-Fallbacks in den abschließend ausgewerteten Abläufen. `LogOverview.json` enthält getrennte Zähler. Externe idevice_id-/Bad-CPU-Meldungen wurden in diesen finalen Logs nicht gefunden; daraus wird keine Reparatur des iOS-Helfers behauptet. Kein Force Quit.

## 8. Echte Vorher-/Nachher-Aufnahmen und Gesamtübersicht

Alle Bilder sind echte Unreal-Aufnahmen in 2560×1440. NativeViewsBefore01 enthält 27 Ausgangsansichten; NativeViewsAfter01 enthält 33 Nachheransichten; seine fünf Innenraumansichten wurden nach dem Bodenanschluss durch NativeRoomFinal01 erneut aufgenommen. Die gesamte endgültige Auswahl umfasst weiter 33 Ansichten einschließlich neuer Felder und großer Büsche. Positionen, Rotation, FOV, Uhr und ScreenPercentage stehen jeweils in Result.json; der tatsächliche Kameravergleich steht in CameraPairs.json. Alle27 gemeinsamen Ansichten stimmen in FOV, Uhrzeit, ScreenPercentage und Rotation überein; die größte gemessene Positionsdifferenz beträgt lediglich1,10×10⁻⁹cm (Gleitkommapräzision). Der neue Innenraumkamerabegrenzer kann bei wandnahen Innenraumwinkeln die Kamera bewusst verschieben; solche Paare sind keine pixelidentischen Vergleichskameras.

| Bereich | Vorher | Nachher |
|---|---|---|
| Dorf | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Dorf.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/Dorf.png) |
| Wiese | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Wiese.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/Wiese.png) |
| Waldweg | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Waldweg.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/Waldweg.png) |
| Wald | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Wald.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/Wald.png) |
| Fluss | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Fluss.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/Fluss.png) |
| Heilhaus | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/Heilhaus.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeRoomFinal01/Heilhaus.png) |
| WR_Holzbruecke | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/WR_Holzbruecke.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/WR_Holzbruecke.png) |
| WR_Steinbruecke | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/WR_Steinbruecke.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/WR_Steinbruecke.png) |
| HouseCutaway_Aussen | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/HouseCutaway_Aussen.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/HouseCutaway_Aussen.png) |
| WR_Gasthaus_Cutaway_Aussen | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/WR_Gasthaus_Cutaway_Aussen.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/WR_Gasthaus_Cutaway_Aussen.png) |
| WR_Spielerhaus_Cutaway_Aussen | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/WR_Spielerhaus_Cutaway_Aussen.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/WR_Spielerhaus_Cutaway_Aussen.png) |
| WR_Wassermuehle_Cutaway_Aussen | [Original](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsBefore01/WR_Wassermuehle_Cutaway_Aussen.png) | [Nachher](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/NativeViewsAfter01/WR_Wassermuehle_Cutaway_Aussen.png) |

Zusätzliche aktuelle Aufnahmen nach der letzten Graphbereinigung: NativeAfterFinal01/Dorf.png, Wiese.png, Waldweg.png, Wald.png, Fluss.png und Heilhaus.png; gleiche tatsächliche Benchmarkpositionen. Weitere echte Nachweise: PIEReview03 mit acht Tageszeiten und Dialog/Kampf/Heiler/Team; NativeAccess03 mit elf Innenräumen; NativeFeatures02 mit TestGround. Gesamtübersicht: [Editor-Regionsübersicht](../Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/OverviewAfter01/Gesamtansicht.png). Die Übersicht aus großer Höhe zeigt Layout und Wege unter den bestehenden Entfernungs-Cullinggrenzen, keine Beurteilung der Vegetationsdichte. Keine künstlich generierten Beweisbilder.

## 9. Schutz, Grenzen und Erweiterung

VisualV2 und alle anderen Maps bleiben bytegleich. Ebenso Originalmodelle/-animationen einschließlich Garados V4, Fab-Quellen, vorhandene Nutzerdateien und alle vorgefundenen Spielstände. `Config/DefaultEngine.ini` bleibt auf dem vorgefundenen SHA256 `f676a51869c678a5820c869165154b6d6e05ae723c77c622d5fb510957799523` und wird nicht mitcommittet. Die 83 vorbestehenden unversionierten Dateien bleiben erhalten. Beide Vollbackup-Refs zeigen weiterhin auf `03492bd96b4dba44692f675c19d5f11abfa86b4b`; das behauptet keine zusätzliche neue Vollsicherung.

Offen: ursprüngliche Gartenhaus-Zugangsmittellinie kollidiert mit der Rückwand (Vorplatz-/Wegbereinigung separat beurteilen), Performance-Drift und Framezeitspitzen; keine vollständige neue temporale Renderingfreigabe;49 statische Modelle benötigen weiter Rigs/Animationen/Gameplaydaten. Westland enthält weiterhin seine vorhandene modulare Architektur, alte Fernkulissen-/Ufergeometrie und teilweise sichtbare Übergänge. Diese Migration verspricht keine komplette Neumodellierung der Region. Kein Garados in flachen Flusszonen und kein neu erfundener Teich. Der Umfang neuer Zufallsfelder ist bewusst klein; Habitat-, Spawn- und Kampfregeln bleiben gemeinsam.

Westland ist wieder die Hauptentwicklungsmap; VisualV2 bleibt als unveränderte Test-/Vergleichsumgebung verfügbar. Nach geprüftem begrenztem Commit/Push erfolgen keine weiteren Gestaltungsarbeiten bis Harrys visueller und spielerischer Beurteilung.

## 10. Git-Abschluss

Ausgangscommit und lokaler Sicherungspunkt siehe oben. Nur auftragsbezogene Map-, eigene Material-, Werkzeug-, Test- und Dokumentationsänderungen werden berücksichtigt; keine Fab-Originale, Nutzersaves, vorhandenen lokalen Nutzeränderungen oder Kontrollmedien. Der abschließende Commit enthält diesen Bericht; sein Hash und die bestätigte Remote-/LFS-Synchronisation stehen im abschließenden Chat und in `Saved/ProjectRefinement/WestlandVisualV2IntegrationV1/GitFinal.json`.
