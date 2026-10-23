# Attackensystem V4 – geprüfte gemeinsame Effektbasis

Ausschließlich bestehendes Projekt und vorhandene VisualV2. Keine Produktionsattacke wird durch diese Werkzeuge automatisch angelegt oder umgebunden.

- `Inventory.py`: im sauberen Editor über den vorhandenen ArtControl-Skriptauftrag alle tatsächlichen Move-Assets lesend inventarisieren. Neue eindeutige JSON-Ausgabe unter Saved; diesen Pfad an Audit.py übergeben.
- `Audit.py --inventory Saved/MoveEffectsV4/AssetsBefore.json --output Saved/MoveEffectsV4/AuditNeuePruefung.json`: tatsächlichen lesenden UE-Bestand mit unveränderter GS-Metadatenreferenz verbinden; bestehende Ausgabe nicht überschreiben.
- `MapChecks.py`: im sauberen Editor über `Tools/ProjectMaintenance/ArtControl.py script Tools/MoveEffectsV4/MapChecks.py` alle elf vorhandenen Maps prüfen, danach VisualV2 laden. Speichert keine Map oder Assets.
- `RunReview.py <neues alphanumerisches Label>`: gewöhnlichen VisualV2-PIE-Start ausführen, danach 20 ausdrücklich technische Kampffälle über bestehende Encounter-/UMG-/Input-Pfade prüfen. Alle zehn vorhandenen Modelle in ClassicBattle und WorldBattle; neun Effektkategorien, AP-Verbrauch, Rückkehr und nativen Bildnachweis prüfen. Keine Save-Schreibvorgänge. Nachher PIE beenden.
- `pm.MoveEffectsV4.Start classic|world stages|status|heal|drain|recoil|multi|confusion|protect|screen Zunderlauf|Schiggy|Bisasam|Pikachu|Myrapla|Enton|Machomei|Nebulak|Gengar|Glurak`: ausschließlich explizite, transiente Entwicklungsfixture. Nicht als echte Attackendaten oder reguläre Begegnung ausgeben, danach PIE beenden; das veränderte Testteam nicht speichern. Nicht in Shipping enthalten.

Die Fixture verwendet bewusst technische Attackennamen, konstante Prüfwerte und ein explizit aktiviertes erweitertes Statusprofil. Sie beweist die gemeinsame Integration, nicht die vollständige Originalwirkung aller 49 fehlenden Attacken. Normale Begegnungen behalten das bisherige Regelprofil.

Native UI-Bilder bleiben unter `Saved/GlumandaV11/LiveUI/`, Ergebnisse unter `Saved/MoveEffectsV4/`. Die logische Testauflösung ist 2560×1440; tatsächliche Slate-Pixelmaße werden separat ohne Skalierung erfasst. Kontrollbilder und Save-Prüfdateien nicht versionieren.

Build/Automation: vorhandenes `Tools/ProjectMaintenance/ProjectQA.py`, neuer eindeutiger Ergebnisname. Der strenge Wrapper bleibt unverändert: Warnungen können trotz erfolgreicher Assertions Exit 1 verursachen. Externe `idevice_id`-Warnungen nicht unterdrücken oder als warnungsfreien Erfolg melden.
