# Inventar und Gegenstände V2

Aktives UE-5.8.2-Projekt: `/Users/harry/Developer/PokeMonster`.

- `CreateItems.py` erstellt die eigenen zusätzlichen Item-/Fanggerät-Datenassets. Vorhandener Trank: `DA_TestHealingItem`, stabile ID `TestHealingItem`, unverändert 20 KP. Keine zweite Trankdefinition. Die Entwickler-Prüfmarke ist ausschließlich eine technische Schlüsselitem-Fixture, ohne neue Quest oder Platzierung.
- `PlacePickups.py` fügt genau zwölf Fundactors zur bestehenden VisualV2 hinzu. Verweigert erneutes Ausführen, wenn schon Fundactors vorhanden sind. Vorhandene Actor-Transformationen bleiben unverändert. Die konkrete erste Platzierung und Boden-/Kapselprüfung stehen in `Saved/ProjectRefinement/InventoryV2/PickupLocations.json`.
- `Gameplay.py` führt reale UMG-, Eingabe-, Physik-, Inventar- und Save-Prüfungen ausschließlich mit einem eigenen UserDir unter `Saved/ProjectRefinement/InventoryV2` aus. Niemals gegen Nutzerslots starten. Jeder native Lauf erhält eine eigene Kopie einer ausdrücklich benannten QA-Fixture; PIE benutzt den vorhandenen isolierten Testslotmechanismus.
- `ReferenceSources.json` nennt feste öffentliche PokeAPI-Revisionen, SHA-256 und überprüfte Werte. Generation-2-Heilmengen sind ausdrücklich beauftragte Projektregeln; die bestehende technische Fangformel bleibt erhalten.

Die vorhandene Beuteloberfläche verwenden: B/Enter wählt, A/Esc geht zurück, Steuerkreuz auf/ab navigiert, L/R wechselt wie bisher die übergeordneten Menüs. Im Beutel zusätzlich links/rechts beziehungsweise Bild auf/ab für die Gegenstandskategorie, ZL/S für die Sortierung und ZR/Entf für das Wegwerfen. Wegwerfen fragt Menge und abschließende Bestätigung ab. Bei Äther/Top-Äther folgt nach der Pokémonwahl die Auswahl einer aktiven Attacke. Elixiere betreffen alle vier aktiven Attacken; verbrauchte AP in inaktiven Repertoireeinträgen werden dadurch nicht kostenlos aufgefüllt. Im Kampf stehen Bälle und Medizin im vorhandenen paginierten Beutel.

Interne Abnahmefixtures (nur Editorcode und ausschließlich dieser eigene QA-UserDir):

- `pm.InventoryReview.Target <Teamplatz 1–6> <KP oder -1> <poison|keep> <AP oder -1>` stellt einen Testzustand auf einer Kopie des vorhandenen Individuums her und nutzt `RestorePersistentState`. Keine Speicherung und keine Veränderung von Artenassets.
- `pm.InventoryReview.Quest active|complete` stellt ausschließlich den RAM-Zustand der bereits vorhandenen Mini-Slice-Quest für die Belohnungsprüfung her. Keine neue Quest, Geschichte oder Änderung am Questasset.

Außerhalb dieses QA-Verzeichnisses bleiben beide Befehle wirkungslos; ohne Editorcode sind sie nicht registriert. Normale Spiel- und Debugbedienung bleibt unverändert. Native/PIE-Resultate, fehlgeschlagene Vorläufe und tatsächliche Ausführungsdateien bleiben unter Saved nachvollziehbar. Strenge Vollautomation und Build verwenden unverändert `Tools/ProjectMaintenance/ProjectQA.py`.
