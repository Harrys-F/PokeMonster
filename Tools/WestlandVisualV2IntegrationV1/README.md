# Westland VisualV2 Integration V1

Bestehende Westland-Region; keine neue Map. Quellen unter VisualV2, Originale, Nutzerdateien und Saves schützen. Alle Kontrollmedien bleiben unter `Saved/ProjectRefinement/WestlandVisualV2IntegrationV1`. Vorherdaten niemals überschreiben.

Die Authoring-Skripte sind einmalige, begrenzte Migrationen. Nicht als Spielstartskripte verwenden. Reihenfolge: Bestandsaufnahme/Hash-Manifeste und Git-Checkpoint → Materials → Surfaces → Healer → Bridge → BushFields → Vegetation → Audit; der zusätzliche Vestibülboden wird danach mit `VestibuleFloor.py` an die tatsächliche Bodenkante angepasst. Alle Gruppen sind auftragseigen und `WVI_`-markiert. Materialien nur im eigenen Assetverzeichnis. VisualV2-Koordinaten werden ausschließlich über tatsächliche Türanker in regionale Koordinaten übertragen; Gelände, Wege und Habitatgrenzen kommen aus Westland.

`LaunchEditor.py <Label>` startet ausschließlich einen eigenen isolierten Editor; blockiert bei vorhandenen Editor-/Spielprozessen. Vor ArtControl-Aufträgen muss die PID in `Saved/ProjectRefinement/Ready.json` zur eigenen Launch.json passen. `MapChecks.py` speichert keine Maps. Editor nur sauber regulär schließen, kein automatisches Kill/Discard.

`RunNative.py <Label> <Script.py> [vorherigesLabel]` startet einen separaten Development-Spielprozess explizit auf Westland, ohne DefaultEngine.ini zu ändern. Ergebnis immer zusammen mit `ProcessExit.json` prüfen. Das optionale vorherige Label darf nur abgeschlossene eigene Sitzungen für den isolierten Neustarttest wiederverwenden. Keine Nutzerstände verwenden.

- `CaptureBenchmark.py`: drei wiederholte QHD/High-C75-Messungen an sechs tatsächlichen Positionen; CSV ohne Video/Fotoaufnahme im Messfenster. Mittag wird über den bestehenden Save-Loader in einem neuen eigenen Testslot gesetzt. `Analyze.py` wertet echte Frame-/GPU-/Threadzeiten aus.
- `Views.py`: echte QHD-Aufnahmen; protokolliert tatsächlichen Spieler-/Kameratransform und Uhrzeit. Diagnoseplatzierung ist kein Fußrundgang.
- `PIEReview.py`: vorhandene regionale Dialog-/Kampf-/Fang-/Heiler-/Quest-/Save-/Team-/Tageszeitregression. `Progression.py`: bestehende Entwicklungsabläufe; nur eigene isolierte PIE-Slots.
- `NativeFeatures.py`: echte Buschbegegnung, Türübergänge bei pm.Speed 1/2/3, Wasserbeobachtung, tatsächlicher Mapwechsel und TestGround-Rückkehr. `NativeRestart.py`: frischer Prozess lädt nur den vorherigen eigenen Teststand.
- `NativeAccess.py`: alle elf tatsächlichen Vordertüren in beiden Richtungen, lokale Haus-Cutaways und vier neue Felder; Diagnoseplatzierung zwischen den Gebäuden. Fünf vollständige Zugänge sind im separaten Access02-Lauf bestätigt. Die alte Gartenhaus-Mittellinie trifft die Rückwand und ist ausdrücklich kein bestandener Weglinientest.
- `NativeTour.py`: zusammenhängender tatsächlicher Enhanced-Input-Rundgang auf allen sechs bestehenden Hauptrouten einschließlich der früher ausgelassenen Ost-/Waldäste, lebende KI/Uhr, vorhandener pm.Speed 3 außerhalb/1 am Heilhaus. Keine Screenshots oder Videos während der CSV-Messung. Kein Hardware-Controller-Test.
- `RunAutomation.py`: bestehender strenger Exportvertrag; Engine-Exit, fehlgeschlagene/übersprungene Tests und Testwarnungen werden getrennt geprüft. Exit 1 ist kein Erfolg.
- `ProtectionAudit.py`: SHA-256-Vergleich aller vorbestehenden Dateien, geschützten Assets und Spielstände mit den vor Arbeitsbeginn erzeugten Manifesten. Kein LFS-Prune und keine Bereinigung.

Die Fab-Originale bleiben unverändert lokal. Ihre nötigen bereits importierten Abhängigkeiten müssen auf dem Prüfcomputer vorhanden sein; dieses Werkzeugpaket lädt nichts herunter.

`RoomFinal.py` prüft die kleine Windfang-Bodenfläche und fünf tatsächliche Raumansichten in PIE oder nativ. `RoomBenchmark.py` wiederholt drei gleiche Raum-Messfenster. `VerifyEvidence.py` prüft echte Exit-Codes, die zwölf letzten Map Checks und PNG-Abmessungen. `WriteReport.py` kennzeichnet den vollständigen Rundgang zeitlich vor dem rein dekorativen Bodenanschluss und verwendet die abschließend separat gemessenen Raumwerte.
