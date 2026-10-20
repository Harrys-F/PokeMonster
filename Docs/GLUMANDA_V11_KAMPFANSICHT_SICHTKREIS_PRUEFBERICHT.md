# Glumanda V1.1, Kampfansicht und Sichtkreis

20.10.2026; aktives Projekt `/Users/harry/Developer/PokeMonster`, VisualV2.
Ausgangspunkt `fc5174ee0fd6f1cef1a56bd1d6ea2bec11cf545e`, `main`/Remote identisch.
Keine zusätzliche Map, kein Worktree und keine Projektkopie. 58 vorhandene
unversionierte Dateien, alle elf Maps, Original-GLB, V1-Quellen und Backup 03492bd
zu Beginn per Prüfsummen/Refs erfasst und geschützt.

## Meilenstein 1 – Name und kleiner Modellpass

Sichtbarer Name jetzt **Glumanda**. Die stabile Identität bleibt
`CreatureSpecies:Zunderlauf`; Assetpfad, Prototypnummer, Kampfwerte und Saveformat
werden nicht umbenannt. Team-/Kampf-/Logtexte beziehen ihren Namen bereits aus
GetDisplayName. Der bestehende Fang-/Heil-/Save-Test prüft den sichtbaren Namen
nun ausdrücklich nach der Wiederherstellung. Der Gameplay-Prüflauf benutzt den
aktuellen Spezies-Anzeigenamen statt einer fest codierten alten Testzeichenfolge.

Neue bearbeitbare Quelle:
`Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Meshy_V11.blend`.
Ein Skin-FBX unter `Exports/MeshyV11/Glumanda_Skin_V11.fbx`. Neues Mesh und Profil:
`/Game/Characters/Creatures/Zunderlauf/MeshyV11/SK_Glumanda_V11` und
`DA_Glumanda_V11`. Die vorhandenen sieben Animationen, Skeleton, Materialien,
Texturen und originale Schwanzflamme werden exakt wiederverwendet.

### Tatsächliche Mesh-Reparatur

Zehn kleine echte Randloops: Umfang etwa 1,37–11,19 cm. Nicht mit UV-Seams oder
der absichtlichen Körper-/Flammennaht verwechselt. Die reine Diagnoseverschweißung
des V1-Körpers zeigt 90 Randkanten; nach Reparatur bleiben nur die 43 Kanten der
Flammennaht. Das Render-Mesh wird nicht global verschweißt/remesht.

Zuerst versuchte Diagonal-Kappen ließen bei der unabhängigen Topologieprüfung
14 zusätzliche Randkanten zurück: einzelne Diagonalen kollidierten mit vorhandenen
Quellkanten. Diese Zwischenfassung wurde nicht als bestanden gesichert. Finale
lokale Fächerkappen mit einem 0,02 mm nach innen versetzten Mittelpunkt vermeiden
diese Diagonalen. Keine Verschiebung ursprünglicher Vertices oder UVs.
Neue Kappen verwenden nur benachbarte Original-UV-Bereiche; bei Atlasnähten lokale
Projektion aus einer angrenzenden Fläche statt quer über die Textur zu interpolieren.

Körper: 12.227 → **12.284 Vertices**, 18.198 → **18.245 Dreiecke**.
Mit unveränderter Flamme (3.563 Dreiecke): **21.808 Dreiecke**.
Keine ursprüngliche Fläche entfernt; 47 winzige Kappendreiecke ergänzt.
Form-/UV-Abweichung ursprünglicher Vertices: **0**. Größte Normalen-Differenz nach
Blender-Speicherung 0,000498 als Einheitsvektordifferenz (rund 0,029°), keine
Neugestaltung der Normalen oder Materialien. Bone-Restmatrizen exakt unverändert.
Alle sieben Animationskurven per Signatur identisch; 3 Originalbilder gepackt.

### Knie und Bewegung

Nur Knie-/Gelenkübergänge leicht über benachbarte Gewichte regularisiert.
Stärkere Kandidaten (25/50 %) wegen 4,1/8,2 mm Oberflächendifferenz verworfen.
Übernommen: 12,5-%-Nachbarschaftsanteil, maximal **2,051 mm** animierte Differenz.
Das P99-Maß absoluter logarithmischer Kantenverformung in 14 Walk-/Run-Proben
sinkt von 0,54876 auf 0,53834. Das ist ein begrenzter technischer Gewinn und keine
Behauptung einer vollständig anatomischen oder schnittfreien Animation.
Fuß-IK, 22/36-cm/s-Schrittparameter, 0,60-m-Größe und Schwanzanker bleiben erhalten.

### Prüfungen des ersten Pakets

- Blenderquelle erneut geöffnet, alle ursprünglichen Positionen/UVs und Actions
  verglichen; keine ungewichteten/nichtnormierten Vertices. FBX erneut importiert.
- Mac Development Editor Build `GlumandaV11SkinBuild01`: bestanden.
- Finale echte QHD-PIE-Sequenz: 7 Clips, 8 Richtungen, native Run-Mischung 1,0,
  74 Aufnahmen unter `Saved/GlumandaV11/RuntimeReviewFinal`.
- Neuer Regressionstest: sichtbarer Name, stabile Art-ID, aktiver V1.1-Skin,
  Originalmaterialien/Skeleton/Clips/Flammeneffekt und 60-cm-Silhouette.
- Vollständige Automation `GlumandaV11SkinAutomation01`: 57/57, keine Testwarnungen oder Fehler.

Lokale Bilder/Animation: `Saved/GlumandaV11/Evidence/` (nicht in Git).
Messwerte dauerhaft: `Art/Characters/Creatures/Zunderlauf/MeshyV11_RepairAudit.json`
und `MeshyV11_SourceAudit.json`. Keine Garantie universell gleitfreier Übergänge;
weitere visuelle Feinabnahme der starken Kniebeugung bleibt sinnvoll.

## Weitere autorisierte Pakete – noch in Arbeit

Als Nächstes: Sichtkreis-Radien 55/110 → 110/220 cm mit unverändertem weichem
Übergang; gezielte weichere Bodenschatten nur für Spielfigur und Glumanda;
anschließend ClassicBattle als normale Darstellung bei unveränderter BattleSession
und optionalem WorldBattle. Bisher keine dieser Änderungen als fertig behauptet.
Abschließender Gameplay-Rundweg, Map Checks, Bilder und Git-Nachweise folgen im
Gesamtabschluss. Die beigefügten alten Pokémon-Screenshots dienen der Komposition,
nicht als importierte ROM-Grafiken oder Vorgabe für Pixelart.
