# Wilde Pokémon und Begegnungen V2

Aktuelles Projekt und bestehende VisualV2. Keine neue Map, kein zweites KI-, Interaktions- oder Kampfsystem.

## Konfiguration

`Species.Overworld.Behavior.Initiation`: `ByTemperament` (Standard), `Contact`, `Challenge`, `Disabled`. ByTemperament verwendet Kontakt für Territorial/Aggressive und Herausforderung für Calm/Curious/Shy. `bCanInitiateEncounter=false` sperrt beide Wege. Bestehende Enumwerte bleiben erhalten; Aggressive ist angehängt. Begegnungen können das gesamte Profil wie bisher über `OverworldMovement.OverrideBehavior/BehaviorOverride` ersetzen. Änderungen vor `Configure` setzen.

Kontakt prüft die tatsächlichen beiden Kapseloberflächen einschließlich maximal 2 cm Bewegungstoleranz. Die alte Sensorsphäre ist kein Distanz-Kampftrigger mehr. Warnung/Verfolgung starten keinen Kampf. Eine laufende Begegnung, Eingabesperre, Niederlagenrückkehr und Wiederholungssperren sperren beide Wege. Territorial erfordert zusätzlich weiterhin das Verlassen des Reaktionsradius vor neuer Aktivierung. `EncounterRadius` bleibt nur für serialisierte Altprofile bestehen; er bestimmt keine Kampfauslösung mehr.

Die vorhandene Interactable-Schnittstelle wählt unter erreichbaren gültigen Zielen anhand Entfernung und Blickrichtung; Sichtlinie, Höhenunterschied und Reichweite werden geprüft. Ein kleiner Pfeil markiert ausschließlich das gewählte Wild-Pokémon, der HUD-Hinweis nennt dessen Art. Begleiter implementieren diese Schnittstelle nicht und sind kollisionslos. E/Enter bleiben erhalten. `GetInteractionAction` stellt dieselbe Enhanced-Input-Aktion bereit; `SetInteractionControllerKey` erlaubt eine ausdrücklich gewählte Gamepad-Zuordnung oder None. Standard ist None, keine vorweggenommene Switch-Pro-Taste. Physischer Test offen.

## Abschluss und Flucht

Die bestehende BattleSession vergibt XP und liefert das Ergebnis. `PresentationMode` wird im bestehenden EndData mitgeführt. Classic-Wildsieg: Recovering (0,9 s vorhandene Hit-Reaktion), Escaping, gegebenenfalls WaitingForExit, Removed. Faint wird zuvor in der bestehenden Kampfansicht gezeigt. Kein neuer Aufstehclip wird behauptet. Schon der Sieg setzt die bestehende Abschluss-ID; Laden eines Nach-Sieg-Snapshots erzeugt den besiegten Gegner nicht neu. Beim ausdrücklichen Laden eines Vor-Sieg-Snapshots wird der reaktivierte Actor an seinen unveränderten Map-Spawn zurückgesetzt, mit neu initialisiertem Habitat und kurzer Kontaktsperre. Diese explizite Snapshot-Wiederherstellung ist kein Teleport während normaler Flucht.

Flucht verwendet dieselbe lokale A*-Suche und Boden-/Wasser-/Gebäude-/Kollisionsprüfung. Nur dieser Zustand darf das normale Habitat verlassen (höchstens 60 m vom Habitatursprung). Ziele werden in begrenzten Etappen von 3/5,5/8,5 m gesucht; Geschwindigkeit beruht auf vorhandener Run-Referenz. Kollisionslose Baumstämme und größere Boulder erhalten ausschließlich lokale konservative Hinderniskerne; Landschaft und Playerkollision bleiben unverändert. Instanztransforms werden einzeln ausgewertet. Keine globale Vegetationskollision. Die erweiterten Kernboxen werden zusätzlich kontinuierlich entlang jedes Wegsegments geprüft: Eine kurze diagonale Eckenkreuzung darf nicht zwischen den 25-cm-Bodenproben verschwinden.

Entfernung erst, wenn die projizierte vollständige Visual-Boundingbox mindestens 96 Pixel außerhalb des tatsächlichen Player-Viewports liegt, mindestens 0,4 s stabil und nach mindestens 1,5 s Flucht. Schatten/Verdeckung allein genügen nicht. Der kleine abgeschlossene Source-Actor bleibt für Save-Restore erhalten, versteckt, ohne Kollision oder Tick; Visual und Mesh-Tick sind ebenfalls aus. Kein laufender Respawner wird neu eingeführt.

Ist kein Weg erreichbar, bleibt der Gegner sichtbar und nicht interaktiv und plant alle 1,5 s erneut. Nach vier Fehlplanungen ist `EscapeBlocked` sichtbar. Kein Timeout-Teleport oder Ausblenden im Bild. Bei späterem Weg bzw. Verlassen des Bilds kann der Abschluss erfolgen. Der Spieler kann eine Flucht weiterverfolgen; eine feste Despawnzeit wird deshalb nicht garantiert.

Fang: sofortiger bisheriger Team-/Reserveübergang, Removed, keine Flucht. Spielerflucht: Active, Cooldown, notwendige Kontakttrennung. Niederlage: bestehende Rückkehr/Heilung/Autosave. WorldBattle: bisheriger Abschluss, kein automatischer Classic-Fluchtzustand.

## Kleine Gruppen

Explizites `GroupSize` am vorhandenen Wild-Actor (1–4, Standard 1), `GroupSpacing` 120–400 cm. VisualV2 aktiviert nur Bisasams bestehendes Habitat mit Größe 3. Mitglieder bekommen stabile IDs `<RootID>_Group_1/2`, unabhängige Seeds, eigene Positionen/Ziele/Pausen und versetzte Idle-Phasen; Laufkadenz bleibt geschwindigkeitsabhängig. Eigene Kapselmaße werden vom Habitatgeber übernommen. Kinder sind keine angehängten Gruppen-Kampfteilnehmer. Abschlussmarkierung und Fang gelten nur für das betroffene Mitglied. Kein automatisches Wiederauffüllen im Sichtfeld.

## Prüfung

Guarded Editor: vorhandene `Tools/ProjectMaintenance/ArtSession.py`, Steuerung `ArtControl.py`.

- `RunEncounter.py LABEL SPECIES TEMPERAMENT Victory|Fled|Captured [east|west]`: echte PIE-Interaktion bzw. Enhanced-Input-Kontaktbewegung, normale Session, QHD-Bildfolge und Ergebnisdaten. Runtime-Startposition, Party und optionales Profil sind ausdrücklich Fixtures; kein behaupteter Fußlauf vom PlayerStart. Fangabschluss verwendet die vorhandene kontrollierte 1-KP-/Seed-51-Fixture; das ist kein Fangquoten-/Balancingtest. Dev-Slot wird geprüft und bei tatsächlichen Testschreibvorgängen kontrolliert restauriert.
- `RunPersistence.py LABEL`: tatsächlicher Sieg/XP, Flucht, Nach-KO-Save/Load ohne Respawn sowie explizites Laden eines Vor-KO-Snapshots mit Wiederaktivierung am Map-Spawn; Originalslot SHA-geprüft restaurieren.
- `RunWorldOutcome.py LABEL`: WorldBattle-Sieg mit sichtbarem Source-Actor; ausdrücklich keine Classic-Flucht.
- `RunGroup.py LABEL`: natürliche, zeitversetzte Gruppenbewegung, danach ausdrücklich bezeichnete Nahbereichs-Fixture für zwei unterschiedliche Zielrichtungen und gemeinsame Interaktion; Kampf mit nur einem Mitglied und Begleiterpause.
- `RunFullGameplay.py LABEL`: bestehender vollständiger Enhanced-Input-Fußlauf ohne Testteleports; Wild-Kontakt ersetzt alte manuelle E-Auslösung. Dialoge/Quest/Liora/Kampf/Fang/Heilhaus/SaveLoad/Sprint, Originalslot kontrolliert restaurieren.
- Bestehende `RunMovement`, `RunModels`, `RunCapture`, `RunDefeatSave` bleiben separate Regressionen. Die neue Gruppe erhöht die Anzahl aktiver Wildakteure von 3 auf 5; alte starre Drei-Actor-Annahmen gelten nicht mehr.
- `ExportOpenMapState.py` lädt/speichert nie eine Map. `ExportDiskMapState.py` ist ausschließlich eine getrennte speicherlose Commandlet-Prüfung. `ConfigureGroup.py` ist eine einmalige, vollständig serialisiert verglichene Migration: unbekannte Differenzen stoppen sie. Transiente Engine-Debugakteure und deren erzeugte Labels sind getrennt dokumentiert.

Build/Automation: `ProjectQA.py`, zusätzlich `RunUnityBuild.py`. Alle vorhandenen Maps mit `StarterExpansionV1/CheckMaps.py`. Kontrollmedien, T3D-Diagnosen und Logs bleiben ausschließlich unter ignoriertem Saved; keine Uploads dieser Dateien.

`ConfigureGroup.py` ist ein einmaliger Migrationsnachweis dieses Durchlaufs und benötigt dessen lokale Initial-/Exportbelege. Im gesicherten aktuellen Projekt ist GroupSize bereits 3; das Werkzeug verweigert eine blinde erneute Migration. `VerifySafety.py` vergleicht gegen den lokalen Startbeleg des jeweiligen Durchlaufs. Solche ignorierten Belege sind keine Spiel-/Build-Abhängigkeiten. Die Laufzeitprüfungen erzeugen ihre Requests und frische Zielordner selbst; `RunPersistence` liest zuvor die aktuelle Editor-Map über `Inspect.py` ein.
