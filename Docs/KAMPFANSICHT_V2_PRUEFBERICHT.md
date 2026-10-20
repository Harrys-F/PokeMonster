# PokeMonster – Kampfansicht V2: Prüfbericht

Stand: 20.10.2026. Projekt ausschließlich `/Users/harry/Developer/PokeMonster`.
Ausgangscommit: `e51ad523af880e5d211eb0ed3ed55d313b20030a`, lokales main = origin/main.
Zu Beginn keine Änderungen versionierter Dateien, 58 geschützte unversionierte Dateien.

## Ergebnis

Die vorhandene ClassicBattle-Präsentation ist überarbeitet: kompakte klassische
Menüseiten, klarer Fokus, größere nutzbare Bildfläche, boundsabhängige Kamera und
vier echte kleine 3D-Umgebungen. Bestehende BattleSession, EncounterSubsystem,
Presenter, Kreaturenmodelle und Animationen bleiben die Grundlage. Keine neue
Map, zweite Kampflogik, Kreatur oder Änderung an Heilhaus/Oberwelt/Sichtkreis.
Die zentrale VisualV2 nutzt den verbesserten nativen Präsentationscode, ohne dass
ihre Mapdatei neu gespeichert werden musste.

Technisch geprüft mit Build, 61/61 Automationstests, allen elf vorhandenen Maps,
separaten echten PIE-/Standalone-Prüfungen und vollständigem Gameplay-Fußlauf.
Keine pauschale Freigabe einer finalen Attackendatenbank oder aller 251 Modelle.
Physische Switch-Pro-Abnahme und unten benannte bestehende Spielfunktionslücken
bleiben offen. Die Bilder dienen der visuellen Abnahme durch Harry.

## Kamera und 3D-Darstellung

Eigene Kreatur vorne links von schräg hinten, Gegner gegenüber rechts von schräg
vorne. Glumandas reale Meshgröße bleibt 60 cm. Keine Vergrößerung des Modells oder
Änderung des 140-cm-Spielers. Basisabstand 610 cm mit Bounds-Prüfung; tatsächlich
bei Glumanda gegen Glumanda 686,17 cm. V1 nutzte 700 cm. Bühne/Abstand berücksichtigen
größere Meshbounds; konservative Randprüfung hält die Figur innerhalb des Bildes.
Die Bildfläche ist jetzt 1280×540 Layoutpunkte statt 1280×520, RenderTarget
2560×1080. Köpfe, Füße und Schwanzflammen sind in den geprüften Ansichten sichtbar.
Das ist keine Abnahme noch nicht vorhandener Groß-, Flug- oder Flügelmodelle.

Bei Angriff/Treffer bewegt sich nur die Capturekamera um maximal 1/2 cm für
0,35 Sekunden und kehrt exakt zur Ruhestellung zurück. Während der Befehlsauswahl
keine dauernde Kamerabewegung. Oberweltkamera und Pawn bleiben am ursprünglichen
Ort. Kurzes Ein-/Ausblenden betrifft ausschließlich das Kampfwidget.

Die kurzlebige Bühne bleibt in derselben geladenen Welt, nur im ShowOnly-Capture
sichtbar, ohne Kollision/Navigation/Welt-GI-/Distanzfeldwirkung. Bestehende
Lichtquellen, TAA, Lumen, Bloom und Karten bleiben unverändert. Außenvarianten
empfangen das vorhandene Außenlicht plus isolierte schattenlose Füllung auf Kanal 2;
Höhle nur diese lokale Füllung. Keine globalen Beleuchtungsregler verändert.
Kleine weich auslaufende Kontaktmarken liegen auf projizierten Bodenankern und
werden bei Teamwechsel aktualisiert. Sie sind grafische Kontaktmarken, keine
physikalischen Schlagschatten und keine Änderung der Oberweltschatten.

## Vier Kampfumgebungen

| Variante | Bestehende Elemente | Dekorationsinstanzen | Zustand |
|---|---|---:|---|
| Wiese | Grasboden, Gräser/Kräuter, Randsträucher, Steine, Bäume im Hintergrund | 95 | vorbereitet und in PIE/Standalone geprüft |
| Wald | Erdboden, Farne, Unterholz, Baumkulisse aus echter 3D-Geometrie | 102 | vorbereitet und in PIE/Standalone geprüft |
| Höhle | Steinboden und räumliche Felsumfassung, geschützte Mitte | 42 | vorbereitet und geprüft; Bodenmaterial künstlerisch noch verfeinerbar |
| Ruine | Gras/Moos, Säulen, Mauerreste und Steine | 103 | vorbereitet und geprüft; vorhandene stilisierte Bauteile, kein neuer Architekturpass |

Zehn vorhandene Meshes in ISM-Gruppen, drei vorhandene Bodenmaterialien.
Keine zusätzlichen großen Landschaften oder Gebäudemaps. Verwendet werden
`Westland/NaturalGroundV1`, `WestlandAssetLibrary` sowie die vorhandenen V5-/V7-
Moss-/Farnassets. Kein Originalmesh oder Originalmaterial überschrieben.

`EPokeMonsterBattleEnvironment` ergänzt Startdaten und Wild-/Trainerprofile.
Auswahlreihenfolge: explizites Profil, bekannte Region, Actor-Tags, vorhandene
nahe Ruinen bzw. mindestens drei Bauminstanzen innerhalb 650 cm, sonst Wiese.
Bei ISM/HISM zählen tatsächliche Weltpositionen der Instanzen. Dafür gibt es einen
separaten Test mit weit entferntem Gruppenursprung. Höhlen verlangen passende
Metadaten; eine unbekannte Region wird nicht willkürlich zur Höhle. Die Heuristik
ist ein Fallback für Präsentation, keine neue Gameplay-Biomregel. Bestehende
Begegnungsassets wurden nicht umgeschrieben oder um neue Begegnungen ergänzt.

## Oberfläche und Eingaben

- Gegner-KP oben links, eigene KP unten rechts; Name, Level, Zahlen und animierter Balken.
- Befehlsseite mit Kampf, Pokémon, Beutel, Flucht; eigene Unterseiten statt ständig sichtbarer doppelter Status-/Teamanzeigen.
- Vier Attackenslots mit Typ und AP, eigene Teamseite und vorhandenes Fangkommando im Beutel.
- Ein gemeinsames Meldungsfeld statt doppeltem sichtbaren Log; aktiver Button farblich hervorgehoben.
- Proportionale Anpassung an 720p/QHD, 16:9-Referenzlayout; andere Seitenverhältnisse werden eingerahmt.
- Maus/Tastatur, Steuerkreuz und native Slate-Sticknavigation; Nintendo A rechts bestätigt, B unten zurück. Layout ist konfigurierbar.
- Nach einem Zug wird die Befehlsseite einschließlich Fokus wiederhergestellt; erzwungener K.O.-Wechsel bleibt auf der Teamseite.

Der explizite Development-Review belegt alle vier Slots mit vorhandenen Testmoves
(eine Wiederholung), um das Layout zu prüfen. Das gibt normalen Kreaturen keine
neuen Attacken und ist keine neue Attackendatenbank.

### Bewusst offene bestehende Funktionen

Die BattleSession besitzt Move, Switch und Capture, aber keine implementierte
Fluchtaktion/-regel. Flucht zeigt deshalb ausdrücklich „noch nicht implementiert“;
der logische Eingabetest bestätigt dabei Runde 0 ohne Zugverbrauch. Keine erfundene
Fluchtwahrscheinlichkeit, keine parallele BattleSession.

Heilung außerhalb des Kampfs funktioniert unverändert. Heilitems als Kampfzug
fehlen weiterhin; der Beutel benennt diese Lücke. Fangen verwendet das bestehende
Inventar-/Fangkommando. Endgültige Attackennamen und Werte sind nicht vorhanden:
technische IDs wie TestNormalPhysical werden durch lesbare, explizit als Test
markierte Bezeichnungen ersetzt. IDs, AP, Typen, Schaden und Speicheridentitäten
sind unverändert. Die vorhandene Status-Testattacke hat weiterhin keine
implementierte Statuswirkung. Keine finale Wirkung erfunden.

## Angriffe, Übergänge und Gameplay

Vorhandene Attack-/Hit-/Faint-/Happy-Clips und typabhängige kompakte Treffer-/Reise-
effekte werden über dieselben Präsentationsphasen genutzt. Der HP-Verlust läuft
weiter über die animierte Anzeige; die BattleSession bleibt allein zuständig für
das Ergebnis. Keine neuen Feuerstellen am Körper; ursprüngliche Schwanzflamme
und Modell-/Animationsassets erhalten.

Alle vier Umgebungsprüfungen laufen echte Sessions bis zum Sieg. Sie beobachten
Reaktionsclips, Rückgabe der Eingabe, Abbau der Bühne und unveränderte Position/
Kamera. WorldBattle bleibt separat wählbar und hat ebenfalls den Lebenszyklustest
bis zum Sieg bestanden. Keine sichtbaren doppelten Glumandas in den geprüften
Kampfansichten; der vorhandene Welt-Darstellungsunterdrückungspfad bleibt aktiv.

Der vollständige Enhanced-Input-Fußlauf in VisualV2 hat **102 Schritte über
287,77 Meter** ohne Testteleports bestanden, einschließlich:

- Wanderer-/Questdialog, wildes Glumanda und erfolgreicher Fang.
- Trainerkampf, tatsächlicher Wechsel zum gefangenen Glumanda, weitere Teamwechsel und Sieg.
- Quest-/Archivablauf, Save/Load einschließlich Name/KP/AP, Sprite-Fallback.
- Außenbewegung, Sprint (gemessene Geschwindigkeit 315 cm/s), Wald und Baumkronen.
- Heilhaus betreten/verlassen, Heilerinteraktion, Heilung/Speicherung, diagonal geprüfter Übergang und Innen-/Außenkamera.

Der ursprüngliche Dev-Spielstand ist bytegenau restauriert, SHA-256:
`01dd9ebb263dd7dde672e1a9b70f8ae5780494fb9a5f3c1140ed3f0132ce057a`.
Dies ist ein reproduzierbarer tatsächlicher PIE-Lauf über Enhanced Input,
keine Behauptung einer manuellen Controller-Abnahme.

## Technische Prüfungen

| Prüfung | Ergebnis | Lokaler Nachweis |
|---|---|---|
| Mac Development Editor Build | bestanden | Saved/ProjectRefinement/BattleViewV2Build07/Result.json |
| Vollständige Projekt-Automation | 61/61, 0 Warnungen, 0 Fehler, 0 nicht ausgeführt | Saved/ProjectRefinement/BattleViewV2Automation02/Report/index.json |
| Vier Varianten in PIE | bestanden | Saved/BattleViewV2/Review03/Result.json |
| Logische Nintendo-A/B-/D-Pad-Eingaben über Slate | bestanden, inkl. Fokus nach Zug | Saved/BattleViewV2/Input02/Result.json |
| WorldBattle-Ausnahme | bestanden | Saved/BattleViewV2/WorldProof02/Result.json |
| Eigenständiges Development -game 1280×720 | vier Varianten bestanden | Saved/BattleViewV2/Native720p01/Result.json |
| Eigenständiges Development -game 2560×1440 | vier Varianten bestanden | Saved/BattleViewV2/NativeQHD02/Result.json |
| Map Check | 11/11 Maps, jeweils 0 Fehler/0 Warnungen | Saved/BattleViewV2/MapCheckAudit.json |
| Vollständiger Fußlauf | bestanden, Originalsave restauriert | Saved/GlumandaV11/Acceptance/FinalBattleViewV2/ |
| Schutzprüfung | 58 Unversionierte, 11 Maps, Sichtcode unverändert | Saved/BattleViewV2/ProtectionFinal.json |
| Originalquellen-/Assetprüfung | 36 Quellen und 32 ursprüngliche Kreaturenassets unverändert | Saved/GlumandaV11/BattleViewV2FinalSources.json |
| Git LFS lokal | fsck --objects HEAD bestanden | Konsolenausgabe; Remoteprüfung siehe Sicherungsabschnitt |

Die drei neuen Tests behandeln Umgebungs-/Assetvertrag, tatsächliche ISM-Orte und
vorläufige Anzeigenamen ohne Balancingänderung. Der bestehende Profiltest prüft
zusätzlich die Weitergabe der Umgebungswahl. Alte Tests wurden nicht abgeschwächt.

### Fehler und Einschränkungen der Prüfungen

Die ersten zwei Entwicklungsbuilds scheiterten an TObjectPtr-/auto-Zeigerableitungen;
diese sind korrigiert. Der erste Review wurde durch eine falsche Mindestannahme
„mehr als 70 Dekorationen“ bei der bewusst kleineren Höhle gestoppt. Die Prüfung
wurde auf die tatsächliche kleine Bühne korrigiert; finale Reviews bestehen.
Die frühere Warnung wegen zusätzlichem CaptureScene bei aktivem CaptureEveryFrame
ist durch Entfernen des redundanten Aufrufs behoben.
Ein Schutzaufruf mit unzulässigem Dateisuffix im Label wurde vor Zugriff abgewiesen;
der anschließend gültige Schutzaufruf besteht.

61/61 ist das Ergebnis der **Projekttests**, nicht die Behauptung vollständig
meldungsfreier Engineprozesse: Der Editor protokolliert beim Start 17 „Condition
failed“-Zeilen, bereits identisch im vorherigen EditorClassicProof01 vorhanden.
Standalone protokolliert 58 Python-Fehlerzeilen experimenteller Engine-Toolset-
Initialisierung (fehlende exponierte Toolset-/PythonTestRunner-Klassen in -game).
Die Fehlerpayloads der eigenständigen Läufe stimmen als Multimenge überein;
keine zusätzlichen Payloads im finalen QHD-Lauf. Diese Enginepunkte sind offen,
nicht unterdrückt oder als behoben ausgegeben. Audio-/idevice-Startwarnungen,
Editor-DataStorage-Warnungen, PSO-/Startbewegungs- und Shutdownmeldungen bleiben
in lokalen Logs; keine neuen Material-/Shaderfehler unseres Bühnenmaterials
festgestellt. Details: Saved/BattleViewV2/WarningAudit.json.

Kein Switch-Pro-HID-Gerät wurde erkannt (gefiltertes hidutil-Ergebnis 0 Treffer).
Die logischen Slate-Tasten sind geprüft; physischer Controller, tatsächliche
Stickachsen, Bluetooth und Rumble sind nicht hardwareabgenommen. Kein paketierter
Shipping-/Cook-Test und keine Performance- oder FPS-Verbesserung behauptet.
Andere Modelle ohne vorhandene 3D-Quelle bleiben beim bestehenden Fallback.

## Echte Aufnahmen

Die finalen nativen Bilder sind exakt **1280×720** bzw. **2560×1440** einschließlich
UMG, jeweils 20 Bilder aus vier Umgebungen und fünf Ansichten (Befehle, Attacken,
Team, Beutel, Angriff). Abmessungen der tatsächlichen Slate-PNGs separat geprüft:
`Saved/BattleViewV2/ResolutionAuditFinal.json`. PIE-Aufnahmen haben ihre im jeweiligen
CaptureMethod.txt dokumentierte Editorviewportgröße; nicht als native QHD-Fenster
umetikettiert. Das feste 2560×1080-Capturetarget ist von der Fenstergröße zu unterscheiden.

Alle Medien bleiben ausschließlich lokal, nicht auf GitHub:

- `Saved/BattleViewV2/Vier_Umgebungen.png`: beschriftete Übersicht aus vier echten QHD-Aufnahmen.
- `Saved/BattleViewV2/LiveUI/BattleV2_meadow_Moves_NativeQHD02/ActualSlateViewport.png`: Attackenseite in QHD.
- `Saved/BattleViewV2/LiveUI/BattleV2_<meadow|forest|cave|ruins>_<Commands|Moves|Team|Bag|Attack>_NativeQHD02/ActualSlateViewport.png`.
- Entsprechende `_Native720p01`-Ordner für 720p.
- `Saved/BattleViewV2/UI_V1_V2.png`: historische echte V1-Aufnahme gegen aktuelle echte V2. Vergleich der Komposition, kein synchronisierter Pixel-/Animations- oder identischer Moveset-A/B-Test.

Die Übersicht wurde ausschließlich beschriftet und proportional verkleinert,
keine Szene generiert oder retuschiert. Einzelbilder bleiben unbeschnitten.
Reproduzierbarkeit und optionale lokale Nachweise: `Tools/BattleViewV2/README.md`.

## Dateien und Git-Sicherung

Änderungen an Encounter-Startdaten/-Profilen, ClassicBattleScene, BattleWidget,
BattlePresenter, MoveData-Anzeigenamen und dem expliziten Development-Reviewbefehl;
neue BattleEnvironment-Enumeration, BattleViewV2-Automation und Reviewwerkzeuge.
Dokumentation in TECHNIK, ENTSCHEIDUNGEN und diesem Bericht. Der Core-Snapshot wird
nur für die neue geprüfte Dateiliste aktualisiert; keine fehlenden Pflichtdateien
als optional umgestuft. Alle Original-Art-/Content-Dateien, Karten, Playerquellen,
Blenderquellen, unversionierten Nutzerdateien und beide lokalen Backup-Refs bleiben
erhalten. Keine zusätzlichen Worktrees, Projektkopien, vollständigen Projektbackups oder Maps angelegt.

Implementierung einschließlich Tests, Werkzeugen und Bericht:
[`d2f243f95534ee8e3c1f2776dd69d1cb0051f138`](https://github.com/Harrys-F/PokeMonster/commit/d2f243f95534ee8e3c1f2776dd69d1cb0051f138),
`feat: refine classic battle view and encounter environments`.

Regulärer Push auf origin/main erfolgreich; Remote-Hash und Tracking-Ref anschließend
identisch bestätigt. Genau 28 geprüfte Pfade, nur reguläre Git-Dateien. Vollständige
Blobgrößen dieser Dateiliste zusammen 1.160.470 Bytes, deutlich unter 1 GiB; das ist
eine konservative Inhaltsgröße, keine Behauptung einer gemessenen Transportgröße.
Index exakt mit Einzeldateiplan verglichen, `git diff --cached --check` bestanden.
Keine Kontrollmedien, Caches, Builds, Modelle oder Maps aufgenommen.

Git-LFS-Objektmenge unverändert: 1.397 Objekte, 6.644.577.468 Bytes vorhandene
Nutzdaten. Lokales fsck bestanden, serverseitige Verfügbarkeit nach Push für alle
Objekte per Download-Batch-Metadaten bestätigt; keine Nutzdaten erneut heruntergeladen.
**Neue LFS-Uploads: 0 Objekte / 0 Bytes.** Keine Käufe oder Budgetänderungen.
Lokale Nachweise: Saved/BattleViewV2/IndexVerified.json, Push01.json,
RemoteLFSAvailability.json. Core-Snapshot: 3.865 erforderliche Dateien, alle gehasht
vorhanden und unverändert außerhalb der expliziten neuen Prüfliste.

Nach Implementierungspush keine Änderungen versionierter Projektdateien offen;
58 ursprüngliche Unversionierte unverändert erhalten. Beide Backup-Refs weiterhin
03492bd, nicht Vorfahr des schlanken main. Der verifizierte Sicherungsstatus wird
als kleiner nachfolgender Dokumentationscommit dieses Berichts samt dessen
Core-Snapshot-Hash gesichert; die abschließende Commit-ID steht in der Codex-Ausgabe
und in `git log -2`, ohne rekursive Selbstreferenz im Bericht.

## Empfehlung

Die überarbeitete Darstellung ist als nächster technischer Entwicklungsstand
verwendbar. Vor einer endgültigen visuellen Freigabe bitte die vier echten Ansichten
prüfen. Insbesondere Höhlenboden und Ruinenmaterialien können später einen gezielten
Art-Pass erhalten; keine unbelegte Behauptung endgültiger Serienqualität.
Als nächste unabhängige Schritte: physischer Switch-Pro-Test, festgelegte Flucht-
und Heilitemregeln sowie freigegebene endgültige Attackendaten. Große/flugfähige
Kreaturen beim jeweiligen Import gesondert auf Framing und Kontaktmarken prüfen.
Keine weitere Kreatur oder Map automatisch erstellt.
