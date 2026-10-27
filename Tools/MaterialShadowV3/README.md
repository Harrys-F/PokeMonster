# VisualV2: Material- und Schattenprüfung V3

Produktive Änderung: nur `r.Shadow.Virtual.SMRT.RayCountDirectional=4` in VisualV2/Grafikprofil C. `pm.Graphics 100` bleibt die bisherige 100-%-/8-Strahlen-Referenz. Lumen, DF-Schatten, High, TAAU und Spielsysteme bleiben erhalten. Messergebnisse und Grenzen: [Prüfbericht](../../Docs/VISUALV2_MATERIAL_SCHATTEN_V3.md).

## Reproduzierbare Einzelprozessmessung

Nur bei regulär geschlossenem Editor aus dem Projektordner starten. Der Launcher verweigert den Start bei laufendem UnrealEditor und beendet niemals fremde Prozesse. Jeder neue Lauf braucht ein unbenutztes Label und einen ausdrücklich ausgewählten vorhandenen QA-Spielstand unter `Saved/SaveGames`, dessen Name `PokeMonster_SaveV2_Test_` beginnt. Keine Nutzerslots verwenden.

Beispiel mit dem hier tatsächlich erstellten isolierten QA-Slot:

```sh
python3 Tools/MaterialShadowV3/RunVSM.py MSV3ProductionRepeat01 --fixture Saved/SaveGames/PokeMonster_SaveV2_Test_PerfMSV3PIE01.sav --mode production --expected-rays 4
python3 Tools/MaterialShadowV3/Analyze.py MSV3ProductionRepeat01
```

- `production`: drei Wiederholungen Dorf/Wald um 12:00, ohne den Strahlenwert im Test zu setzen. Prüft den gebauten Produktivstandard.
- `matrix`: fünf Orte × vier Uhrzeiten × drei Wiederholungen × acht/vier Strahlen. Beide Varianten bleiben dabei bei QHD/75 %; es ist kein 75-/100-%-Auflösungsvergleich. Rund 18 Minuten Messfenster plus Start/Ende, nicht unbeaufsichtigt neben anderer Arbeit starten.
- `smoke`: ein kurzer Kontroll-/Vier-Strahlen-Vergleich in Dorf/Wald. Kein Ersatz für eine vollständige Messreihe.

Je Fenster vier Sekunden Aufwärmen, fünf Sekunden Messung; Ausgabe und interne Renderer-Abmessungen werden in jedem aufgezeichneten Frame geprüft. `Analyze.py` muss erfolgreich enden, bevor Zahlen als gültig gelten. Frame-p95 verwendet die gepoolten Frames der drei Wiederholungen. GPU-Pass-Scopes nicht ungeprüft addieren.

Der bestehende Profiling-Probe `pm.EnvPerf2.Run` bleibt zuständig. Frisches eigenes `-UserDir`, kopierter QA-Save, RAM-only Unterdrückung zufälliger Kontaktkämpfe, keine Aufnahmen. Jede temporäre CVar wird am Ende zurückgesetzt; der Prozess endet regulär. Bei Timeout bleibt der Prozess zur Diagnose bestehen, keine gewaltsame Beendigung. Keine Änderungen an Maps, Assets, Save-Schema oder Nutzerkonfiguration.

Kurze frische Läufe und lange thermisch/zeitlich driftende Reihen nicht direkt als Versionsgewinn vergleichen. Das Projektziel stabiler 30 FPS mit Reserve ist in dieser Prüfung nicht erreicht.
