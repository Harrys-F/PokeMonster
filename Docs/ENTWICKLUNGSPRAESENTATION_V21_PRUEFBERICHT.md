# Entwicklungspräsentation V2.1 – Prüfbericht

25.10.2026. Ausschließlich `/Users/harry/Developer/PokeMonster`, Ausgangsstand `a87b8263`, vorhandene VisualV2. Keine neue Map, keine Asset-/Modelländerung, kein neues Entwicklungssystem.

## Ergebnis

Beide vorhandenen Entwicklungen werden größer, zentriert und unverzerrt präsentiert. Alte und neue Silhouette überblenden weich; drei dezente Lichtwellen, 16 sparsame Lichtpunkte und eine kurze Lichtsteigerung begleiten den Wechsel. Die weiße Überlagerung verschwindet vollständig, danach spielt das neue Pokémon seine vorhandene Happy-Animation. Erst anschließend erscheint „Glumanda hat sich zu Glutexo entwickelt!“ beziehungsweise „Glutexo hat sich zu Glurak entwickelt!“.

Die Weltgrößen bleiben 60/110/170 cm; kein Actor-/Mesh-Scale wird verändert. Die Bühne passt jede Form anhand ihrer direkt projizierten orientierten Grenzen einschließlich Effekten ein. Das bisherige verzerrte Bildseitenverhältnis und die übermäßig großen weltachsenparallelen Rahmen sind korrigiert. Weltkamera und ClassicBattle bleiben unverändert.

## Tatsächlich untersuchter Vorher-Ablauf

`Baseline02` führte beide alten Sequenzen bis zum Erfolg und zurück ins Spiel aus, einschließlich RAM-Save/Load. Der frühere Widget-Ablauf tauschte die Vorschau nach 2,5 s und übernahm nach 5 s die Daten; Erfolgsmeldung und Happy starteten gleichzeitig mit dem Entfernen des Overlays. Die erste Erfolgsaufnahme zeigte noch einen ausgewaschenen Renderframe. Die kurzen historischen Videos mit 5,9 s konnten den vollständigen farbigen Ausklang und die Rückkehr nicht belegen. Der alte Framebuffer-Recorder erfasste außerdem die Welt hinter der UMG-Oberfläche; solche Aufnahmen gelten hier ausdrücklich nicht als Präsentationsnachweis.

## Neuer Ablauf und Abbruch

| Zeit ab B/Enter | Darstellung und Eingabe |
|---|---|
| Vor Beginn | Originalmodell, Angebot; B beginnt, A bricht ab |
| 0–2,35 s | Ruhiger Lichtaufbau und langsames Pulsieren |
| 2,35–4,45 s | Kontinuierliche Überblendung zweier tatsächlich gerenderter Formen |
| Bis unter 5 s | A/Esc kann einschließlich später Vorschau abbrechen; ursprüngliche Spezies bleibt bestehen |
| 5 s | Unveränderter atomarer Übernahme-/Speicherpunkt im bestehenden Encounter-Dienst |
| 5–5,85 s | Licht klingt aus; keine Abbruch- oder vorzeitigen Weiter-Hinweise |
| 5,85–7,8 s | Overlay vollständig entfernt, Originalmaterialien und vorhandene Happy-Animation |
| Ab 7,8 s | Erfolgsmeldung mit beiden Namen; B/Enter weiter, gegebenenfalls reguläre Lernangebote, dann Oberwelt |

A nach der Datenübernahme beendet oder überspringt die Enthüllung nicht. Die Ablaufzeit verwendet Weltzeit; zusätzliches Screenshot-Zeichnen beschleunigt die Sequenz nicht. Der vollständig deckende Bildschirm rendert nur seine transienten Bühnenansichten. Sein vorheriger Welt-Renderzustand wird beim normalen Schließen, Abbruch, Test-End und Widget-Abbau wiederhergestellt.

## Vollständige echte Videos

Die beiden finalen MP4 enthalten Angebot, Beginn, vollständige Verwandlung, farbige Enthüllung, Happy, Erfolg und mindestens zwei Spielsekunden normale Oberwelt. Echte präsentierte Slate-/UMG-Frames, **2331 × 1312**, keine Konzeptbilder oder synthetischen Zwischenbilder. Das ist die tatsächlich erfasste Mac-Viewportgröße, kein als QHD ausgegebenes Fenster.

**Aufnahmemethode:** Nur der ausdrücklich aktivierte technische PIE-Prüflauf lief mit Zeitfaktor **0,25**. Codierung mit den ursprünglichen Spielzeitstempeln ergibt normale Wiedergabegeschwindigkeit und genügend echte Bewegungsphasen. Die folgende Abtastung bezeichnet Bilder pro dargestellter Spielsekunde, **keine Echtzeit-FPS-Messung**. Reale Zeitstempel bleiben in den lokalen CSV-Dateien erhalten.

| Entwicklung | Originalframes | Spielzeit | Bilder/Spielsekunde | 95%- / größter Bildabstand | Lokal gespeichertes MP4 |
|---|---:|---:|---:|---:|---|
| Glumanda → Glutexo | 419 | 13.81 s | 30.27 | 0.046 / 0.072 s | [Vollständiges Video](../Saved/ProjectRefinement/EvolutionPresentationV21/Review03/Glutexo_FullPIE.mp4) |
| Glutexo → Glurak | 472 | 13.82 s | 34.09 | 0.046 / 0.079 s | [Vollständiges Video](../Saved/ProjectRefinement/EvolutionPresentationV21/Review03/Glurak_FullPIE.mp4) |

Die codierten Videolängen betragen rund 13,86 s beziehungsweise 13,85 s einschließlich letzter Framehaltezeit. Originalbilder, Videos und Vergleichsmedien bleiben ausschließlich in `Saved`.

## Vorher/Nachher und Enthüllung

| Ansicht | Vorher, tatsächlicher Slate-Viewport | Nachher, tatsächlicher Slate-Viewport |
|---|---|---|
| Glumanda im Angebot | [Vorher](../Saved/GlumandaV11/LiveUI/EvolutionV21_Baseline02_Glutexo_Before/ActualSlateViewport.png) | [Nachher](../Saved/GlumandaV11/LiveUI/EvolutionV21_Review03_Glutexo_Before/ActualSlateViewport.png) |
| Glutexo vor zweiter Stufe | [Vorher](../Saved/GlumandaV11/LiveUI/EvolutionV21_Baseline02_Glurak_Before/ActualSlateViewport.png) | [Nachher](../Saved/GlumandaV11/LiveUI/EvolutionV21_Review03_Glurak_Before/ActualSlateViewport.png) |
| Vollständig enthülltes Glutexo | — | [Originalfarben und Erfolg](../Saved/GlumandaV11/LiveUI/EvolutionV21_Review03_Glutexo_Revealed/ActualSlateViewport.png) |
| Vollständig enthülltes Glurak | — | [Originalfarben und Erfolg](../Saved/GlumandaV11/LiveUI/EvolutionV21_Review03_Glurak_Revealed/ActualSlateViewport.png) |

Gleiche technische Fixture und dieselben unveränderten Modelle; die Präsentationsrahmung ist die beauftragte Änderung. Materialien und Texturen wurden nicht umgestaltet. Vorhandene Meshy-Oberflächen und Gluraks bestehende Flügelgeometrie bleiben sichtbar und sind nicht Gegenstand einer Modellkorrektur.

## Prüfungen

| Prüfung | Tatsächliches Ergebnis |
|---|---|
| Finaler Editor-Build `EvolutionV21_Build08` | Exit 0 |
| Finale volle Automation `EvolutionV21_Automation04` | 206 Success + 1 SuccessWithWarnings, **207 fachlich bestanden**, 0 Failed/NotRun/InProcess; Engine Exit 0 |
| Strenger finaler QA-Wrapper | **Exit 1, nicht bestanden** wegen externer iOS-Helferwarnung in `PokeMonster.CrystalMoves.Production.Submission` |
| Externe Warnung | `idevice_id`: `posix_spawn failed (86, Bad CPU type in executable)`, anschließend `Failed to launch Tool`; nicht als Projekt-/Attackenfehler oder warnungsfrei ausgegeben |
| Vorheriger Vollauf `EvolutionV21_Automation03` | 207 Success, Wrapper Exit 0; vor letzter präziser Rahmungsregression, ersetzt nicht das finale Ergebnis |
| Zwei neue Präsentations-Automationstests | Timeline/5-s-Abbruchgrenze, kontinuierliche Überblendung, farbiger Ausklang vor Erfolg, vollständige zentrierte Bounds und orientierte Flügelrahmung bestanden |
| Alle **zwölf** aktuell vorhandenen Map Checks | Je 0 Fehler / 0 Warnungen; keine Map gespeichert |
| Normaler PIE-Prüflauf `V21LateCancel01` | **47 Schritte, 14 Prüfungen bestanden**, normale Spielzeit; tatsächlicher später Abbruch bei **4,660 s**, Wiederholung und beide Entwicklungsstufen |
| Vollständige Aufnahmeläufe `Review03` | Sieben Prüfungen bestanden; vollständige farbige Happy-Phase, A-Sperre nach Übernahme, beide Rückkehrwege, RAM-Save/Load |
| Daten / Save-Kompatibilität | Gleiche IDs, Level/XP, aktive Attacken, Repertoire und verbrauchte AP; unabhängiges Reserve-Glurak und anderer Teamplatz unverändert; RAM-Test-End stellt Originalteam wieder her |
| Normaler PIE-Neustart | Originaler normaler Save erneut geladen, kein Testteam oder RAM-Zustand übernommen |
| Controller | Bestehende Apple-GC-Zuordnung softwareseitig verwendet: physisch B entspricht hier UE FaceButton_Right, A FaceButton_Bottom; Tastatur Enter/Esc geprüft. Kein neuer Hardwaretest behauptet |

Save-Datei durchgehend SHA-256 `46558ee2cc7ce9a4fc8331a92ccfe751044c0730376872f534a941022655ddac`. Keine Save-Kopie, kein Zurückschreiben älterer Savebytes. Alle 31 anfänglichen unversionierten Dateien geschützt. Vollbackup `03492bd` und sämtliche Modell-/Animations-/Mapassets unverändert.

## Werkzeuge, Schutz und verbleibende Grenzen

Der vorhandene Recorder besitzt einen optionalen asynchronen Slate-Modus über das engineinterne RHI-Modul; der bisherige Framebuffer-Modus bleibt kompatibel. Framepfade und tatsächliche Zeitstempel sind überprüfbar. Die ersten Entwicklungsaufnahmen `Review01/02` waren zu niedrig abgetastet und werden nicht als finale Bewegungsabnahme verwendet. Ein vor dem Slate-Aufbau ignorierter Bildgrößenaufruf wurde vor der finalen Prüfung korrigiert. Im alten manuellen Prüfskript verzögerte ein Schritt irrtümlich das Bestätigen statt den späteren Abbruch; der neue gemeinsame späte Prüfschritt belegt nun tatsächlich 4,660 s. Diese Werkzeugfehler werden nicht als Produktfehler verborgen.

Die externe iOS-Helferwarnung bleibt offen. Die sichtbaren Originalmodelle/Animationen wurden bewusst erhalten; keine neue VFX-Produktion, kein Modellfeinschliff und keine Änderungen an Entwicklungsregeln, Lern-/AP-/Speichersystem, Controllergrundbelegung, Landschaft, Heilhaus oder Kampfkameras. Physische Controllerprüfung und endgültige visuelle Nutzerabnahme bleiben gesondert. Keine Performance-Testreihe.

Maschinenlesbare Zusammenfassung: `ENTWICKLUNGSPRAESENTATION_V21_TESTERGEBNISSE.json`. Wiederholung und Videoexport: `Tools/GlutexoEvolutionV2/README.md`.

## GitHub-Sicherung

Nur benötigter C++-Code, geprüfte Werkzeuge und Dokumentation werden gezielt gesichert. Keine Bild-/Videodateien, Caches, Builds, Originalmodelle oder Spielstände im Commit. Es entstehen keine neuen LFS-Assets. Remote-/LFS-Verifikation und Commit-ID werden nach dem regulären Push im Abschluss ergänzt. Kein Force-Push und keine Budgetänderung.
