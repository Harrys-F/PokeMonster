# Kampfsystem V3 prüfen

Nur im bestehenden Projekt `/Users/harry/Developer/PokeMonster`, Unreal 5.8.2.
Keine neue Map, kein zweites Inventar oder Kampfsystem. Physischer Switch-Pro-Test
ist ausdrücklich Harrys spätere Prüfung und kein Abschlusskriterium.

## Voraussetzungen

Sauberer eigener Editorzustand; keine fremden ungespeicherten Pakete verwerfen.
`ProjectQA.py <frischerName> Build` und danach `... Automation` bei geschlossenem
Editor ausführen. Aktuelle Suite enthält 68 Tests, davon sieben neue V3-Gruppen.
Fehler und Warnungen im ursprünglichen Report erhalten, nicht unterdrücken.

Eigene Sitzung mit `ArtSession.py` starten. `ArtControl.py` verweigert Start/Schließen
bei fremden Dirty Packages. `ValidateData.py` prüft ausschließlich lesend die
Gen-2-Teilmenge und den bestehenden 20-KP-Trank. `PrepareData.py` ist das einmalige,
eng begrenzte Authoring für den V2-Ausgangsstand; kein allgemeines Reimportwerkzeug.
Schon gespeicherte neue Attacken werden nicht blind überschrieben.

## Tatsächlicher PIE-Test

`python3 Tools/BattleSystemV3/RunPIE.py <frischerAlphanumerischerName>`

Verwendet neun explizite, ungespeicherte Fixture-Begegnungen in VisualV2:
Classic-/World-Wildkampf mit Heilung von aktivem/inaktivem Teammitglied, Heuler,
Glut, Wechsel und Flucht; Trainer-/Story-Fluchtsperre; gescheiterte Flucht;
erzwungener Wechsel; Teamniederlage und Checkpoint-Heilung; Sieg; AP-Erschöpfung.
Eigene Fixture-Geschwindigkeiten und Start-KP sind Testbedingungen, keine neuen
Speziesdaten. Es werden weder Map noch Asset noch Dev-Spielstand gespeichert.
`pm.BattleV3.Start` und `pm.BattleV3.Click` sind ausschließlich explizite
Development-Kommandos; sie verwenden echte Encounter-/UMG-Aktionen. Produktions-
Begegnungen ändern dadurch keine Teams oder Bestands-NPCs.

Der Test schickt Enter/Escape und logische Nintendo-A/B-Ereignisse durch Slate.
Dies ist ein Softwaretest, kein angeschlossener Switch-Pro-Controller.
Tatsächliche Slate-Bilder mit Metadaten liegen ausschließlich unter
`Saved/BattleSystemV3/LiveUI`. Eine angeforderte RHI-Größe ist nicht automatisch
die tatsächliche Slate-Ausgabegröße; immer PNG-/CaptureMethod-Maße angeben.
Kein Offscreen-Rendern des live eingebundenen Widgets für vermeintliche QHD-Belege.

## Vollständiges Gameplay und Maps

`python3 Tools/GlumandaV11/RunGameplay.py FinalBattleSystemV3`
führt den vorhandenen vollständigen Enhanced-Input-Fußlauf aus. Kein Label mit
Präfix `Battle` verwenden, das würde den historischen Kurzmodus wählen. Der Runner
sichert ausschließlich den notwendigen Dev-Testspielstand, prüft gegen parallele
Änderungen und stellt ihn danach bytegleich wieder her. Kein Projektbackup.

Bei beendetem PIE `ArtControl.py script Tools/BattleSystemV3/CheckMaps.py`: sämtliche
bestehenden Maps lesend laden und MAP CHECK ausführen, danach VisualV2 laden.
Kein Save All, keine neue Karte. Marker `BATTLE_V3_FINAL_MAPCHECK_*` im Engine-Log
zur Zuordnung von Fehler-/Warnungszahlen verwenden.

`Protection.py <frischesLabel>` vergleicht die zu Auftragsbeginn erfassten
58 unversionierten Dateien, elf Maps, sämtliche Art- und Kreaturen-Präsentations-
Dateien, den Dev-Spielstand und beide Backup-Refs. Das lokale `Initial.json` ist
Sitzungsnachweis, kein erforderliches Runtime-Asset. Neue Arbeitsläufe benötigen
vor Beginn ein eigenes bewusst erfasstes Inventar; historische Hashes nicht ersetzen,
um eine fehlgeschlagene Prüfung zu verschleiern.

## Grenzen

Datenquellen und Abweichungen stehen im Prüfbericht. Nur Kratzer/Heuler/Glut sind
für den aktuellen Glumanda-Stand verifiziert. Keine komplette Gen-2-Schadens- oder
Attackenbibliothek, keine erfundenen Erträge anderer Spezies. Originalmodelle,
Animationsassets, Oberwelt, Heilhaus und Sichtkreis bleiben unverändert.
