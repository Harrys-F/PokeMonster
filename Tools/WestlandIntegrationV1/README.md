# Westland Integration V1

Bestehende Map `/Game/Maps/Dev_WestlandRegion`; keine neue Karte. Die Region ist vollständig gespeichert und benötigt diese Skripte nicht beim Spielen. Originalstand/Ergebnisse stehen in `Docs/WESTLAND_REGION_INTEGRATION_V1.md`.

`Layout.json` dokumentiert ausschließlich neue regionale Zonen, Erscheinungszuordnungen und vorhandene Funditems. Die Arten-, Rhythmus-, Fang-, Attacken- und Entwicklungsregeln bleiben zentral in den bestehenden Systemen. Keine zweite Pokémon- oder NPC-Bibliothek.

`Integrate.py` ist ein **einmaliger** bewachter Autorenlauf gegen die vorab per Commit/SHA geprüfte ursprüngliche Map. Es verweigert Wiederholung/Doppelactors oder einen veränderten Ausgangsstand. Nicht auf der bereits integrierten Map erneut starten oder dafür Daten löschen. Es verwendet bestehende Unreal-APIs; keine Mesh-/Skeleton-/Animationsimporte. Die lokalen Vorher-Inventare/Sicherungsnachweise liegen unter `Saved/ProjectRefinement/WestlandIntegrationV1`.

Prüfungen im bestehenden Projekt:

```sh
python3 Tools/ProjectMaintenance/ProjectQA.py WestlandIntegrationV1/Build_NEUER_NAME Build
python3 Tools/WestlandIntegrationV1/RunAutomation.py Automation_NEUER_NAME
```

Der bestehende strenge Reportvertrag bleibt maßgeblich: mindestens323 vollständige Tests, getrennte Warnungen/Fehler/Skips, kein Erfolg bei Wrapper-Exit1. `MapChecks.py` prüft alle zwölf bestehenden Maps in einem sauberen eigenen Editor ohne Speichern; Ergebnisse aus den begrenzten WESTLAND_INTEGRATION_V1-Logabschnitten auswerten.

`QuickReview.py`: nur eigenes isoliertes Westland-PIE, eigenes UserDir unter dem Prüfverzeichnis und expliziter `PokeMonster_SaveV2_Test_...`-Slot. `Active.json` enthält einen neuen `label`. Gezielte Standortwechsel sind Diagnosen, **kein Fußlauf**. Prüft Original-NPCs/Dialoge, reguläre natürliche Begegnung/Attacke/Fang, echte Heilhaustür, KP/AP/Checkpoint, Menü-Save/Load, bestehende Questanzeige, Tageszeiten, B75/C85, drei Funde, Team und Begleiter. Ein vorhandener QA-Slot wird nicht als Nutzersave verwendet.

`FootTour.py` läuft dagegen mit normalen Enhanced-Input-Bewegungen ohne Testteleports, Geschwindigkeitsänderung oder abgeschaltete KI. Große Positionswechsel dürfen ausschließlich die bestehenden Heilhaustüren sein. Shift wird softwareseitig gedrückt; kein physischer Controller-Nachweis. Stills sind keine Video-/Performancefreigabe.

```sh
python3 Tools/WestlandIntegrationV1/RunNative.py NativeTour01 FootTour.py
python3 Tools/WestlandIntegrationV1/RunNative.py NativeRestart01 RestartTravel.py --resume-owned-tour
```

Nur bei noch nicht vorhandenem Ausgabeordner und ohne andere Unreal-Sitzung. Der zweite Befehl verwendet ausschließlich das vorherige **eigene** NativeTour01-UserDir, ohne Save-Kopie. Niemals Nutzersaves oder fremde Verzeichnisse einsetzen. Kein Mapargument beim Spielstart: verifiziert die konfigurierte Hauptmap. `RestartTravel.py` lädt den echten eigenen Rundgang-Save in einem frischen Prozess, wechselt nach VisualV2 und lädt regulär zurück nach Westland. Zeitüberschreitung beendet keinen Prozess gewaltsam.

`ProgressionSmoke.py` verwendet nur in einer neuen eigenen PIE-Sitzung die bereits vorhandenen `pm.EvolutionReview`-Fixtures und die normale Entwicklungs-UI/Save-Logik. Kein Item-Fixture, kein Überschreiben von Speziesregeln. Levelgrenzen, Abbruch, späterer Versuch, vollständige Enthüllung, individuelle Werte/AP, unabhängige Glurak-Reserve und Begleiter werden geprüft.

`HabitatObservation.py` liest nach dem Ufer-Fund-Test die natürliche Population, Zustände, Fußpunkte/Zone und Karpador im bestehenden Fluss. Keine Spawn-/Bewegungs-/Kollisions-/KI-Overrides. Ausgabe nur lokal in Saved. Die Kontrolle darf nur als bestanden gelten, wenn der tatsächlich natürliche Fisch beobachtet wurde.

Keine Nutzereditoren schließen, keine fremden PID beenden, keine Ausgangsdaten zurücksetzen. Eigene Prüfprozesse regulär beenden; bei Stillstand konkreten Zustand/PID dokumentieren. Kontrollmedien und temporäre Arbeitsdateien nicht versionieren.

`AuditSavedRegion.py` prüft die tatsächliche gespeicherte Map und ursprünglichen NPC-Bindungen lesend. `Views.py` erzeugt ruhige native QHD-Ansichten bei unveränderter Kamera mit diagnostischer Standortwahl, ohne Speichern oder Änderungen an der Welt.
