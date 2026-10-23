# Pokémon-Fortschritt V1

Vorhandene CreatureInstance, CreatureProgression, BattleSession, BattlePresenter/Widget
und SaveSubsystem werden erweitert. Kein zweites Fortschrittssystem und keine Mapänderung.

## Verifizierte Daten

`Gen2Reference.json`: Gold/Silber, Versionengruppe 3, zehn vorhandene Arten, 102
Level-Einträge / 68 unterschiedliche Attacken. Öffentliche PokeAPI-Metadaten, keine
ROM-Dateien, Bilder oder fremden Modelle. Die exakte Git-Revision und acht
Quell-CSV-Prüfsummen sind enthalten. `FetchReference.py` erzeugt die Datei nur,
wenn noch keine geprüfte Referenz existiert; Rohdownloads bleiben in Saved.
Historische Änderungen werden je Feld rückwärts bis Gen 2 angewendet. Moderne
Attackenstärken dürfen nicht ungeprüft übernommen werden.

19 Attacken nutzen vorhandene unterstützte Mechaniken. Neu: Flammenwurf (95/100/15,
10 % Verbrennung), Slam (80/75/20), Hydropumpe (120/80/5). Werte: Stärke/Genauigkeit/AP.
49 Spezialwirkungen sind noch nicht vollständig implementiert. Ihre Namen, Level
und offenen Wirkungen bleiben in **derselben** `LevelUpMoves`-Liste als explizite
nicht spielbare Einträge erhalten. Sie werden bei Erreichen des Levels verständlich
angezeigt, aber nicht als falsche funktionierende Attacken gelernt.
Panzerschutz hat in den Quelldaten keine Trefferprüfung; die vorhandene Engine-API
bildet seine Selbstwirkung mit 100 % ab, ohne eine neue Originalgenauigkeit zu behaupten.

`PrepareData.py` ist der **einmalige Migrationsnachweis**, kein wiederkehrender
Importer. Vorhandene Entwicklungsregeln führen vor jeder Mutation zur Ablehnung.
Keine Originalvisuals, Basiswerte, Wachstumskurven, individuellen Saves oder Maps ändern.
Nicht blind erneut ausführen. `ValidateData.py` prüft den fertigen Stand rein lesend.

## Lernentscheidungen

Erfahrung und Werte verwenden die vorhandenen Regeln. Freie Slots werden wie bisher
automatisch gefüllt und jetzt sichtbar gemeldet. Bei vier belegten Slots wird
`PendingMoves` in Levelreihenfolge gesammelt. Ersetzen verändert genau einen Slot;
Ablehnen nur das betreffende Angebot. Die übrigen AP und die Instanz-ID bleiben erhalten.

Der bestehende BattlePresenter hält nach der Rundenpräsentation den Übergang zur
Oberwelt bzw. zum nächsten Gegner an, bis die Lernangebote entschieden sind.
Die vorhandenen vier Attackenbuttons dienen als Ersatzwahl, der Zurückbutton heißt
hier Ablehnen. B/Enter bestätigt, A/Esc lehnt ab, Steuerkreuz/Pfeile navigieren.
Kein zusätzlicher Kampfzug und kein paralleles Eingabesystem.

Save-Schema 5 speichert offene Angebote als Primary Asset IDs. Schema 1–4 bleibt
lesbar. Unbekannte, doppelte, bereits bekannte oder noch nicht erreichbare Lernangebote
werden beim Laden atomar zurückgewiesen. Im normalen Kampfablauf werden Angebote
vor Rückkehr zur Oberwelt abgeschlossen. Extern vergebene XP mit gespeicherter
Restwarteschlange werden beim nächsten Kampf erneut angeboten; ein allgemeines
Oberwelt-Trainings-/Attackenerinnerungsmenü gehört noch nicht zum Teilumfang.

## Entwicklungen

Die vorhandene reine Bedingungsprüfung bleibt maßgeblich. Neue Optionsabfrage
unterscheidet fehlende Zielart, fehlende gültige Darstellung und verfügbare Zieldarstellung.
Sie ändert keine Spezies, ersetzt kein Modell und verbraucht keine Gegenstände.
Normale vorbereitete Levelwege: Bisasam/Glumanda/Schiggy 16, Myrapla 21,
Enton 33, Nebulak 25. Pikachu: Kontext-ID ThunderStone (noch kein neues Inventaritem).
Keine Zielart wurde importiert. Insbesondere sind vorhandene unversionierte GLB
keine integrierten Entwicklungsmodelle. Freundschaft und Ort/Prüfung werden über
den vorhandenen Kontext geprüft; konkrete ehemalige Tauschentwicklungen bleiben
entsprechend SPIELREGELN vorläufig, statt Level/Orte eigenmächtig festzulegen.

## Wiederholbare Prüfungen

- Editor regulär geschlossen: `Tools/ProjectMaintenance/ProjectQA.py NeuerBuild Build`
  und `... NeuerAutomation Automation`.
- Im bestehenden sauberen ArtSession-Editor `ArtControl.py script
  Tools/CreatureProgressionV1/ValidateData.py` und `.../MapChecks.py`.
- `RunPIE.py NeuerAlphanumerischerName`: gewöhnlicher PIE-Start, sechs **explizite
  Laufzeitfixtures** in VisualV2. Echte KO-XP, Lernwahl, freie Slots, blockierte
  Entwicklung, ClassicBattle und WorldBattle. Wildakteure/Trigger werden nur in dieser
  isolierten PIE-Fixture ausgesetzt; dies ist kein Nachweis natürlicher Wildbegegnungen.
  Kein Dev-Save-Schreibzugriff; Vorher-/Nachher-SHA müssen identisch sein.
- `pm.ProgressionV1.Start classic|world replace|free|evolution` ist ausschließlich
  eine ausdrückliche Entwicklungsfixture, nicht für normale Spielstände gedacht.
- Der bestehende vollständige Gameplay-Fußlauf, Controller-/Team-/Save-Probe und
  Niederlagen-/Autosave-Test ergänzen die gezielten neuen Tests.

Kontrollbilder und Logs bleiben in Saved. Native UI-Aufnahmen stammen aus
`pm.CreatureReview.CaptureLiveUI`; ihre tatsächlichen Pixelmaße werden separat
validiert. Ein logischer 2560×1440-Gameviewport garantiert keine gleich große
Slate-Aufnahme. Keine Bilder hochskalieren oder als echte QHD-Nachweise umetikettieren.
Simulierte B/A-Eingaben sind kein physischer Controller-Hardwaretest.
