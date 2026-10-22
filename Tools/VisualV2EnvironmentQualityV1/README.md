# VisualV2 Environment Quality V1

Isolierter Einzelfaktorvergleich im schlanken Worktree. Die Testkarte ist eine unveränderte API-Kopie von VisualV2, keine freigegebene Render-Voreinstellung.

Vorhandener nativer `pm.EnvPerf.Run`-Probe: MotionBlurOff (`r.MotionBlurQuality=0`), BloomOff (`r.BloomQuality=0`), VSMRayCount2 (`r.Shadow.Virtual.SMRT.RayCountDirectional=2`), LumenIntegrate2 (`r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=2`). Immer genau ein Faktor, vollständiger Restore zwischen Segmenten/Ende. Die beiden Qualitätsschalter wirken auch auf Innenräume und sind deshalb Messvarianten, kein Vorschlag für globale Projektdefaults.

Sechs Auflösung/Qualität/Percentage-Kombinationen gemäß Prüfbericht; aktuelle Nutzervorgabe 720 statt historischer 740 Pixel. Je Modus und Konfiguration drei Orte, drei Wiederholungen, Kontrolle vor und nach vier Einzelfaktoren, in Wiederholung 2 umgekehrte Faktorenfolge. Warm-up 5 s, Messfenster 8 s; kurze Stichproben, kein Dauerstabilitätsbeweis. Keine Screenshots oder Datei-/Buildaudits während Messfenstern. Profiling-Positionswechsel sind keine Gameplay-Fußprüfung.

Qualität ausschließlich vor PIE ändern; eingebettetes PIE verwenden. Keine schwebenden PIE-Fenster. Native Prozesse mit `-game` sind Development, kein Shipping. Originalmaps niemals speichern. Ergebnisse unter Saved/EnvironmentPerfV1 mit eindeutigem Präfix VEQ1_, neue Status-/Bildnachweise unter Saved/VisualV2EnvironmentQualityV1.
