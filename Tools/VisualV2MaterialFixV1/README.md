# VisualV2 Material Fix V1

Gezielte Korrektur ausschließlich am vorhandenen Blattmaster:
`M_WLA_FoliageGroups_V3.used_with_instanced_static_meshes = true`.
Keine Graph-, Tint-, Textur-, Mesh-, Map-, Kamera- oder Gameplayänderungen.
`ApplyFix.py` verlangt einen vorherigen Audit und saubere Pakete, kompiliert
Master/Instance und speichert nur diese erlaubten Materialpakete.

## Prüfung

Editor explizit mit `-ExecCmds=py <Startup.py>` öffnen, nicht mit dem
selbstschließenden `-ExecutePythonScript`. Die Datei-Jobwarteschlange steuert
nur diese aktive Editorsitzung. Kein Netzwerkdienst erforderlich.
Vor jedem PIE-Start `Preset.py` ausführen. Qualitätsstufen nicht bei lebenden
Reveal-MIDs wechseln: das kann in UE 5.8.2/Metal eine UniformExpressionCache-
Assertion auslösen. Feste Qualität/Screen Percentage pro Sitzung, eingebettetes
PIE über den LevelEditorSubsystem; keine schwebenden Fenster.

32 statische Pläne: Vorher/Nachher, PIE/native, acht Konfigurationen mit 720p
und QHD, Medium/High, 75/100%. Je Plan drei Standorte mit drei Wiederholungen,
5 s Warm-up + 3 s Messung. Die kurzen Messfenster sind Zustandsvergleiche,
keine belastbare Dauer-FPS-Zusage. Repeat 90 sind ausschließlich Bildnachweise,
Repeat 99 ist CSV-Drain; beide aus Performanceauswertung ausschließen.
Die `VGB1_`-Labels nutzen den stock-Scalability-Pfad des bestehenden EnvPerf2-
Probes; keine alten Integrate2/Rays2-Kandidatenprofile übernehmen.

Vorher native graue Fallbacks und nachher korrekte Maskierung sind ausdrücklich
nicht bildgleich. Mehrarbeit nach Reparatur ist kein Optimierungsfehler.
Auflösung/Renderer-Fractions, Kamerapose, Kontroll-CVars und GPU-CSVs prüfen.
Native `-game` ist Development mit Editorbinary, kein Shipping-Build.

Große Bilder, CSVs, Logs und lokale Sicherungen verbleiben außerhalb Git.
Fehlende Reviewnachweise sind keine Gameplay- oder Build-Abhängigkeiten.
Absoluten Slim-Worktree-Pfad vor Wiederverwendung bewusst anpassen.
