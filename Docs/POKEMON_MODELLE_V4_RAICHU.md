# Pokémon-Modelle V4 – Bestand, Raichu und Donnersteinroute

Stand: 29.10.2026 · bestehendes Projekt `/Users/harry/Developer/PokeMonster` · Referenz `/Game/Maps/Dev_TestMap_VisualV2`.

**Raichu: Technisch integriert – visuelle Freigabe ausstehend.** Eigenständig erstellter, bearbeitbarer Blender-Kandidat. Keine Umfärbung/Vergrößerung von Pikachu, kein heruntergeladenes Spielmodell. Technische Tests sind keine automatische optische Endfreigabe.

## 1. Ausgangsstand und Umfang

Lokales main und direkt geprüftes origin/main standen zu Beginn auf `4eeef43a7a4099cd103020e30d8d21f56e7cf76a`, einschließlich `6622e958`. Vorbestehende Nutzeränderungen in `Config/DefaultEngine.ini` und 34 fremde unversionierte Dateien einschließlich 20 Meshy-GLBs wurden erhalten. Die zusätzlich im Baseline-Lauf mitgezählte eigene `Tools/ModelsV4/Baseline.py` ist kein fremdes Nutzerfile. 583 vorbestehende `.sav`-Dateien wurden vor Arbeit per SHA-256 erfasst. Kein neues Projekt, Worktree oder neue Map.

Raichu fehlte in der Unreal-AssetRegistry, sämtlichen Art-Quellen und der zusätzlichen projektweiten Suche einschließlich Saved. Die Suche findet außerhalb der neuen Raichu-/ModelsV4-Verzeichnisse weiterhin keine Raichu-Modellquelle.

Vorher: 18 spielbereite Arten. Nachher: 19. Drei ältere `TestGrass/TestFire/TestWater`-Datensätze besitzen kein spielbares 3D-Modell und zählen nicht mit. Die offene Spielwelt erhält keinen neuen Raichu-Wildspawn; Maximum 14, Zonen und KI bleiben unverändert.

## 2. Vollständiger Bestandsnachweis


Aktuell 22 Arten-DataAssets, 19 spielbare Arten, 405 Assets unter `/Game/Characters/Creatures`: 33 SkeletalMesh, 39 Material, 57 Texture2D, 210 AnimSequence, 28 Skeleton, 35 PokeMonsterCreaturePresentationData, 3 StaticMesh. 212 .fbx, 38 .blend, 38 .glb unter Art/Characters/Creatures. Die 38 GLBs wurden tatsächlich importiert/gelesen und einzeln diagnostisch gerendert; alle 38 Blenderquellen lesend geöffnet. Kein Original wurde gespeichert.


Der versionierte [vollständige strukturierte Bestand](/Users/harry/Developer/PokeMonster/Docs/POKEMON_MODELLE_V4_BESTAND.json) enthält alle Quellpfade, auch alte FBX-/Blendvarianten, jede Unreal-Klasse, Skeleton-/Clipreferenz, Original-UVs/Texturen und Topologiebefunde. Die folgenden Tabellen trennen nutzbare Formen von reinen Quellen.

### 2.1 Spielbare Arten: Identität, aktuelle Quelle und Unreal-Mesh


| Name | Interne ID | Dex | Aktuelle Blenderquelle | Originalquelle | Aktuelles Unreal-Mesh | Skeleton | Einordnung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bisasam | Bisasam | 1 | [Bisasam_Meshy_PolishV2.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Bisasam/Source/Bisasam_Meshy_PolishV2.blend) | Art/Characters/Creatures/Incoming/Bisasam.glb | /Game/Characters/Creatures/Bisasam/PolishV2/SK_Bisasam_Skin.SK_Bisasam_Skin | /Game/Characters/Creatures/Bisasam/MeshyV1/Meshes/SK_Bisasam_Meshy_Skeleton.SK_Bisasam_Meshy_Skeleton | spielbar, bestehender Stand |
| Glutexo | Glutexo | 5 | [Glutexo_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Glutexo/Source/Glutexo_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Glutexo.glb | /Game/Characters/Creatures/Glutexo/MeshyV1/Meshes/SK_Glutexo_Meshy.SK_Glutexo_Meshy | /Game/Characters/Creatures/Glutexo/MeshyV1/Meshes/SK_Glutexo_Meshy_Skeleton.SK_Glutexo_Meshy_Skeleton | spielbar, bestehender Stand |
| Glurak | Glurak | 6 | [Glurak_AnimationCorrections_V61.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Glurak/Source/Glurak_AnimationCorrections_V61.blend) | Art/Characters/Creatures/Incoming/Glurak.glb | /Game/Characters/Creatures/Glurak/AnimationV61/SK_Glurak_V61.SK_Glurak_V61 | /Game/Characters/Creatures/Glurak/AnimationV6/SK_Glurak_V6_Skeleton.SK_Glurak_V6_Skeleton | spielbar, bestehender Stand |
| Schiggy | Schiggy | 7 | [Schiggy_Surface_V2.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Schiggy/Source/Schiggy_Surface_V2.blend) | Art/Characters/Creatures/Incoming/Shiggy.glb | /Game/Characters/Creatures/Schiggy/SurfaceV2/SK_Schiggy_Surface.SK_Schiggy_Surface | /Game/Characters/Creatures/Schiggy/MeshyV1/Meshes/SK_Schiggy_Meshy_Skeleton.SK_Schiggy_Meshy_Skeleton | spielbar, bestehender Stand |
| Raupy | Raupy | 10 | [Raupy_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Raupy/Source/Raupy_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Raupy.glb | /Game/Characters/Creatures/Raupy/MeshyV1/Meshes/SK_Raupy_Meshy.SK_Raupy_Meshy | /Game/Characters/Creatures/Raupy/MeshyV1/Meshes/SK_Raupy_Meshy_Skeleton.SK_Raupy_Meshy_Skeleton | spielbar, bestehender Stand |
| Smettbo | Smettbo | 12 | [Smettbo_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Smettbo/Source/Smettbo_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Smettbo.glb | /Game/Characters/Creatures/Smettbo/MeshyV1/Meshes/SK_Smettbo_Meshy.SK_Smettbo_Meshy | /Game/Characters/Creatures/Smettbo/MeshyV1/Meshes/SK_Smettbo_Meshy_Skeleton.SK_Smettbo_Meshy_Skeleton | spielbar, bestehender Stand |
| Hornliu | Hornliu | 13 | [Hornliu_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Hornliu/Source/Hornliu_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Hornliu.glb | /Game/Characters/Creatures/Hornliu/MeshyV1/Meshes/SK_Hornliu_Meshy.SK_Hornliu_Meshy | /Game/Characters/Creatures/Hornliu/MeshyV1/Meshes/SK_Hornliu_Meshy_Skeleton.SK_Hornliu_Meshy_Skeleton | spielbar, bestehender Stand |
| Bibor | Bibor | 15 | [Bibor_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Bibor/Source/Bibor_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Bibor.glb | /Game/Characters/Creatures/Bibor/MeshyV1/Meshes/SK_Bibor_Meshy.SK_Bibor_Meshy | /Game/Characters/Creatures/Bibor/MeshyV1/Meshes/SK_Bibor_Meshy_Skeleton.SK_Bibor_Meshy_Skeleton | spielbar, bestehender Stand |
| Habitak | Habitak | 21 | [Habitak_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Habitak/Source/Habitak_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Habitak.glb | /Game/Characters/Creatures/Habitak/MeshyV1/Meshes/SK_Habitak_Meshy.SK_Habitak_Meshy | /Game/Characters/Creatures/Habitak/MeshyV1/Meshes/SK_Habitak_Meshy_Skeleton.SK_Habitak_Meshy_Skeleton | spielbar, bestehender Stand |
| Pikachu | Pikachu | 25 | [Pikachu_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Pikachu/Source/Pikachu_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Pikachu.glb | /Game/Characters/Creatures/Pikachu/MeshyV1/Meshes/SK_Pikachu_Meshy.SK_Pikachu_Meshy | /Game/Characters/Creatures/Pikachu/MeshyV1/Meshes/SK_Pikachu_Meshy_Skeleton.SK_Pikachu_Meshy_Skeleton | spielbar, bestehender Stand |
| Raichu | Raichu | 26 | [Raichu_V4.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Raichu/Source/Raichu_V4.blend) | Eigene neue Blenderquelle | /Game/Characters/Creatures/Raichu/V4/Meshes/SK_Raichu_V4.SK_Raichu_V4 | /Game/Characters/Creatures/Raichu/V4/Meshes/SK_Raichu_V4_Skeleton.SK_Raichu_V4_Skeleton | technisch spielbar; optisch offen |
| Myrapla | Myrapla | 43 | [Myrapla_AnimationCorrections_V6.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Myrapla/Source/Myrapla_AnimationCorrections_V6.blend) | Art/Characters/Creatures/Incoming/Myrapla.glb | /Game/Characters/Creatures/Myrapla/AnimationV6/SK_Myrapla_V6.SK_Myrapla_V6 | /Game/Characters/Creatures/Myrapla/AnimationV6/SK_Myrapla_V6_Skeleton.SK_Myrapla_V6_Skeleton | spielbar, bestehender Stand |
| Enton | Enton | 54 | [Enton_PolishV4.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Enton/Source/Enton_PolishV4.blend) | Art/Characters/Creatures/Incoming/Enton.glb | /Game/Characters/Creatures/Enton/PolishV4/SK_Enton_PolishV4.SK_Enton_PolishV4 | /Game/Characters/Creatures/Enton/PolishV4/SK_Enton_PolishV4_Skeleton.SK_Enton_PolishV4_Skeleton | spielbar, bestehender Stand |
| Machomei | Machomei | 68 | [Machomei_AnimationCorrections_V6.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Machomei/Source/Machomei_AnimationCorrections_V6.blend) | Art/Characters/Creatures/Incoming/Machomei.glb | /Game/Characters/Creatures/Machomei/AnimationV6/SK_Machomei_V6.SK_Machomei_V6 | /Game/Characters/Creatures/Machomei/AnimationV6/SK_Machomei_V6_Skeleton.SK_Machomei_V6_Skeleton | spielbar, bestehender Stand |
| Nebulak | Nebulak | 92 | [Nebulak_AnimationCorrections_V6.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Nebulak/Source/Nebulak_AnimationCorrections_V6.blend) | Art/Characters/Creatures/Incoming/Nebulak.glb | /Game/Characters/Creatures/Nebulak/AnimationV6/SK_Nebulak_V6.SK_Nebulak_V6 | /Game/Characters/Creatures/Nebulak/AnimationV6/SK_Nebulak_V6_Skeleton.SK_Nebulak_V6_Skeleton | spielbar, bestehender Stand |
| Gengar | Gengar | 94 | [Gengar_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Gengar/Source/Gengar_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Gengar.glb | /Game/Characters/Creatures/Gengar/MeshyV1/Meshes/SK_Gengar_Meshy.SK_Gengar_Meshy | /Game/Characters/Creatures/Gengar/MeshyV1/Meshes/SK_Gengar_Meshy_Skeleton.SK_Gengar_Meshy_Skeleton | spielbar, bestehender Stand |
| Karpador | Karpador | 129 | [Karpador_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Karpador/Source/Karpador_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Karpador.glb | /Game/Characters/Creatures/Karpador/MeshyV1/Meshes/SK_Karpador_Meshy.SK_Karpador_Meshy | /Game/Characters/Creatures/Karpador/MeshyV1/Meshes/SK_Karpador_Meshy_Skeleton.SK_Karpador_Meshy_Skeleton | spielbar, bestehender Stand |
| Garados | Garados | 130 | [Garados_Meshy_V1.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Garados/Source/Garados_Meshy_V1.blend) | Art/Characters/Creatures/Incoming/Garados.glb | /Game/Characters/Creatures/Garados/MeshyV1/Meshes/SK_Garados_Meshy.SK_Garados_Meshy | /Game/Characters/Creatures/Garados/MeshyV1/Meshes/SK_Garados_Meshy_Skeleton.SK_Garados_Meshy_Skeleton | spielbar, bestehender Stand |
| Glumanda | Zunderlauf | 1002 | [Glumanda_Meshy_V11.blend](/Users/harry/Developer/PokeMonster/Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Meshy_V11.blend) | Art/Characters/Creatures/Incoming/Glumanda.glb | /Game/Characters/Creatures/Zunderlauf/MeshyV11/SK_Glumanda_V11.SK_Glumanda_V11 | /Game/Characters/Creatures/Zunderlauf/MeshyV1/Meshes/SK_Glumanda_Meshy_Skeleton.SK_Glumanda_Meshy_Skeleton | spielbar, bestehender Stand |


Alle 19 nutzen den vorhandenen nativen Animationsproxy und können technisch Begleiter sowie ClassicBattle-Darstellung verwenden. Bei den 18 vorhandenen Arten ist dies Bestandsfähigkeit, keine neue vollständige optische Abnahme jeder Bewegung in diesem Auftrag. Namen und individuelle Identitäten bleiben unverändert; insbesondere Glumanda verwendet weiterhin die kompatible ID `Zunderlauf`.

### 2.2 Größe, Animationen, Begleiter und Entwicklungsformen

`7 Rollen` bedeutet tatsächlich referenzierte Idle, Walk, Run, Attack, Hit, Faint und Happy mit kompatiblem Skeleton. Walk/Run sind bei Schwebe-/Wasserarten die vorhandenen Bewegungsrollen und kein behaupteter zweibeiniger Gang. Referenzgröße ist nicht immer stehende Höhe: Garados 650 cm bezieht sich auf die Körperlänge.


| Name | Referenzgröße | Rig | Idle | Walk | Run | Attack | Hit | Faint | Happy / Begleiter | Entwicklung | Qualität / Einschränkung |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bisasam | 70 cm | ja | ja | ja | ja | ja | ja | ja | ja / Bisaknosp → Bisaflor nur GLB | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Glutexo | 110 cm | ja | ja | ja | ja | ja | ja | ja | ja / Glurak spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Glurak | 170 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Schiggy | 50 cm | ja | ja | ja | ja | ja | ja | ja | ja / Schillok fehlt; Turtok nur GLB | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Raupy | 30 cm | ja | ja | ja | ja | ja | ja | ja | ja / Safcon nur GLB → Smettbo spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Smettbo | 110 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Hornliu | 30 cm | ja | ja | ja | ja | ja | ja | ja | ja / Kokuna nur GLB → Bibor spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Bibor | 100 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Habitak | 30 cm | ja | ja | ja | ja | ja | ja | ja | ja / Ibitak fehlt | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Pikachu | 40 cm | ja | ja | ja | ja | ja | ja | ja | ja / Raichu jetzt spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Raichu | 80 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform; Pichu fehlt | Form/Bewegung neu geprüft, optische Freigabe offen |
| Myrapla | 50 cm | ja | ja | ja | ja | ja | ja | ja | ja / Duflor/Giflor/Blubella fehlen | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Enton | 80 cm | ja | ja | ja | ja | ja | ja | ja | ja / Entoron fehlt | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Machomei | 160 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform; Maschollo/Maschock fehlen | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Nebulak | 130 cm | ja | ja | ja | ja | ja | ja | ja | ja / Alpollo fehlt; Gengar spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Gengar | 150 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Karpador | 90 cm | ja | ja | ja | ja | ja | ja | ja | ja / Garados spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Garados | 650 cm | ja | ja | ja | ja | ja | ja | ja | ja / Endform | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |
| Glumanda | 60 cm | ja | ja | ja | ja | ja | ja | ja | ja / Glutexo → Glurak spielbar | Vorhandene funktionierende Darstellung erhalten; alte Quellen nicht ersetzt |


### 2.3 Nur als unverändertes Modell vorhanden

Diese 20 Incoming-Arten sind **nicht** registriert oder spielbereit. Für keine wird eine interne Laufzeit-ID erfunden. Alle besitzen UVs und eingebettete Texturbilder, aber kein Rig und keine Animation. Originalmaßstäbe sind uneinheitlich; eine kanonische Spielgröße wurde für sie nicht eingerichtet. Begleiter, Kampf und Entwicklung sind daher nicht freigegeben. Die echten Intake-Ansichten zeigen nur Modellbestand, keine Gameplayintegration.


| Name | Registrierte ID | Reale Quelldatei | Dreiecke | UV / Bilder | Rig / Animation | Status | Sichtprüfung / Einschränkung |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Abra | — | Art/Characters/Creatures/Incoming/Abra.glb | 21182 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Aerodactyl | — | Art/Characters/Creatures/Incoming/Aerodactyl.glb | 21897 | ja / 3 | nein / nein | nur Modell | Dünne Flügel/relativ realistischer Look; Stil und Flügelrig offen |
| Bisaflor | — | Art/Characters/Creatures/Incoming/Bisaflor.glb | 21221 | ja / 3 | nein / nein | nur Modell | Weitere Zielquelle; Rig/Clips/Daten fehlen |
| Bisaknosp | — | Art/Characters/Creatures/Incoming/Bisaknosp.glb | 21157 | ja / 3 | nein / nein | nur Modell | Vorhandene Zielquelle für Bisasam; Rig/Clips/Daten fehlen |
| Ditto | — | Art/Characters/Creatures/Incoming/Ditto.glb | 21542 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Evoli | — | Art/Characters/Creatures/Incoming/Evoli.glb | 21152 | ja / 3 | nein / nein | nur Modell | Erkennbarer GLB; alle drei Stein-Zielformen fehlen |
| Georok | — | Art/Characters/Creatures/Incoming/Georok.glb | 20770 | ja / 3 | nein / nein | nur Modell | Dateiname nicht als Artbeweis verwenden; stark stachelige Form visuell vor Integration verifizieren |
| Geowaz | — | Art/Characters/Creatures/Incoming/Geowaz.glb | 17974 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Kadabra | — | Art/Characters/Creatures/Incoming/Kadabra.glb | 21637 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Kleinstein | — | Art/Characters/Creatures/Incoming/Kleinstein.glb | 20688 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Kokuna | — | Art/Characters/Creatures/Incoming/Kokuna.glb | 21111 | ja / 3 | nein / nein | nur Modell | Wichtige Zwischenform; noch kein produktives Modell |
| Lavados | — | Art/Characters/Creatures/Incoming/Lavados.glb | 17167 | ja / 3 | nein / nein | nur Modell | Aufwendige Flügel-/Flammenform; Rig und stilistische Abnahme offen |
| Mew | — | Art/Characters/Creatures/Incoming/Mew.glb | 21579 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Mewtu | — | Art/Characters/Creatures/Incoming/Mewtu.glb | 21142 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Pantimos | — | Art/Characters/Creatures/Incoming/Pantimos.glb | 21523 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Relaxo | — | Art/Characters/Creatures/Incoming/Relaxo.glb | 20879 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Safcon | — | Art/Characters/Creatures/Incoming/Safcon.glb | 21457 | ja / 3 | nein / nein | nur Modell | Wichtige Zwischenform; noch kein produktives Modell |
| Simsala | — | Art/Characters/Creatures/Incoming/Simsala.glb | 20552 | ja / 3 | nein / nein | nur Modell | Einzelnes texturiertes Ausgangsmodell; Rig, Clips, Größe und Artdaten offen |
| Turtok | — | Art/Characters/Creatures/Incoming/Turtok.glb | 20870 | ja / 3 | nein / nein | nur Modell | Zielquelle vorhanden; Schillok-Zwischenform fehlt |
| Zapdos | — | Art/Characters/Creatures/Incoming/Zapdos.glb | 20223 | ja / 3 | nein / nein | nur Modell | Sehr feine Feder-/Flügelkonturen; Spielkamera/Overdraw vor Integration prüfen |


Alle GLBs haben auf Rohdatenebene Randkanten. Das allein belegt keine sichtbaren Löcher: Meshy trennt u. a. UV-/Normaleninseln. Keine Quelle wurde deshalb automatisch repariert oder als unbrauchbar erklärt. Zero-area-Dreiecke wurden in diesen 38 GLB-Prüfungen nicht gefunden. Große Quellmodelle wie Pikachu/Myrapla/Glurak sind keine Neuimporte dieses Auftrags.

### 2.4 Fehlende Formen und historische Varianten

Evoli ist nur als GLB vorhanden; Aquana, Blitza und Flamara fehlen vollständig. Es wird keine dieser drei Steinrouten als spielbar ausgegeben. Ebenfalls fehlen als spielbereite Quellen/Artdaten insbesondere Pichu, Schillok, Ibitak, Entoron, Duflor, Giflor, Blubella, Alpollo, Maschollo und Maschock. Bisaknosp, Bisaflor, Safcon, Kokuna, Turtok, Abra, Kadabra, Simsala sowie Kleinstein, Georok, Geowaz sind als oben genannte Rohquellen vorhanden, aber keine zusätzlichen spielbaren Formen.

33 Skeletal Meshes entsprechen 19 aktuellen Darstellungen plus 14 historischen Varianten, nicht 33 Arten. Die drei Static Meshes sind Nebulaks Gas-Hülle und zwei historische Schwanzflammen, keine eigenständigen Pokémon. Der JSON-Bestand listet alle Pfade. Außerhalb Art liegen 90 ältere Modell-/Backup-/Prüfdateien unter Saved und eine HutGable.obj-Prototypquelle unter Content. Darunter sind sechs ausdrücklich zurückgewiesene alte Glurak-FBX in Saved/CreaturePolishV4/RejectedInputs. Keine zusätzliche Art/Raichu-Quelle gefunden; diese Dateien bleiben unverändert und werden nicht als neue spielbare Modelle gezählt.

## 3. Eigenes Raichu-Modell

Quelle: `Art/Characters/Creatures/Raichu/Source/Raichu_V4.blend`; reproduzierbare Werkzeuge `Tools/ModelsV4`, Herkunft/Regeldaten `ReferenceSources.json`. Kein Modell oder Texturbild heruntergeladen. Eigene zusammengeführte organische Haut, gesondert geformte geschwungene Ohren, Wangen, Pfoten, Rückstreifen, lange dünne Schwanzkette und eigener Blitzabschluss. Keine Wiederverwendung von Pikachus Geometrie/Skeleton.


Aktueller Meshstand: 36,367 Vertices, 72,352 Dreiecke, sechs einfache Materialien, 23 deformierende Quell-Bones. FBX/Unreal führen den zusätzlichen Armature-Wurzelknoten. Gemessene Quellhöhe 80.92 cm bei 80-cm-Referenz, damit ca. 1,1 % Abweichung, keine doppelte Actor-Skalierung. GroundOffset 0,3 cm entspricht dem gemessenen Sohlenabstand. Keine zusätzliche Physics-Asset-Kollision, Lichtquelle, Partikelkomponente oder eigene AnimBlueprint-/Tick-Logik. Aktuell ein Mesh-LOD; spätere LOD-Ableitung bleibt möglich.


Die sechs Materialien verwenden harmonische Basisfarben/Roughness ohne Fell-/Texturaufwand oder Selbstleuchten. UVs sind für spätere Bearbeitung vorhanden; keine fehlenden externen Texturquellen. Technische Quellenprüfung: keine losen Vertices oder Nullflächen; offene Ränder an absichtlich separat aufliegenden Bauch-/Ohr-/Rückenflächen werden nicht als wasserdicht verschwiegen.

Sieben 30-Hz-Clips, Walk 35 cm/s und Run 65 cm/s, in-place. Die bestehende Darstellung skaliert die Clipgeschwindigkeit nach tatsächlicher Bewegung. Eine Animation pro Geschwindigkeit mit 3D-Rotation für acht Richtungen. Bein-IK hält Standphasen; Gewichtsnormalisierung und Oberflächen-Schleifenschluss numerisch geprüft, alle sieben exportierten FBX tatsächlich erneut importiert. Idle/Walk/Run schließen ohne messbaren Oberflächenspalt. Das ersetzt keine umfassende Wahrnehmungsprüfung unter allen Kamera-/Bewegungsbedingungen.

Bei echter Sichtprüfung wurden die zunächst verschobenen Augen, kantigen Ohren und ein schwebender seitlicher Faint-Entwurf korrigiert. Der jetzt importierte Faint-Clip fällt nach vorne mit durchgehend auf die tiefste Oberfläche angepasstem Bodenkontakt. Oberfläche/Ohren/Schwanz besitzen weiterhin einen bewusst einfachen, stilisierten Entwurf; Gesichtsanimation/Blinzeln und künstlerischer Feinschliff bleiben offen. Keine optische Endfreigabe behauptet.

## 4. Raichu-Daten und bestehende Donnersteinroute

Art `CreatureSpecies:Raichu`, Dex 026, Elektro, Basiswerte KP/Angriff/Verteidigung/Sp.Angriff/Sp.Verteidigung/Initiative **60/90/55/90/80/100**, Wachstum MediumFast, Fangrate 75, Basis-EP 122. Keine Übernahme der späteren Initiative 110. Gen-2-Lernliste: Donnerschock, Rutenschlag, Ruckzuckhieb und Donnerblitz auf Level 1, alle als vorhandene Attackenassets. Eine Entwicklung auf Level 11 lehrt nicht rückwirkend automatisch sämtliche Level-1-Attacken; aktive Attacken und tatsächlich gelerntes persönliches Repertoire bleiben gemäß bestehender Regeln erhalten.

Datenquellen: [pokecrystal Raichu-Basisdaten](https://github.com/pret/pokecrystal/blob/master/data/pokemon/base_stats/raichu.asm), [Pikachu-/Raichu-Entwicklung und Lernliste](https://github.com/pret/pokecrystal/blob/master/data/pokemon/evos_attacks.asm#L325-L347), [offizielle Raichu-Referenz](https://www.pokemon.com/de/pokedex/raichu). Keine ROM-/Spielgrafiken übernommen. 80 cm entsprechen dem Nutzerauftrag; Startlevel 11 ist nur die Entwickler-Vorschau, keine neue Levelbedingung der Steinroute.

Die bereits vorhandene Pikachu-Regel und `DA_ThunderStone` bleiben unverändert. Nur die vormals fehlende gültige Zielart ist hinzugefügt. Ablauf: Beutel → Donnerstein → Pikachu → B/Enter → vorhandene Sequenz V2.1. A/Esc bricht vor dem bestehenden Commitpunkt nach fünf Spielsekunden ab; danach gelten die vorhandenen Hinweise und vollständige Farbenthüllung. Atomare ResolveEvolution-/SaveProgress-Transaktion verbraucht exakt einen Stein erst mit erfolgreichem Speichern. Wiederholtes Bestätigen, falsche Ziele, fehlendes Item, Abbruch und tatsächlicher Schreibfehler verursachen keinen zusätzlichen Verbrauch.

## 5. Bestehende Systeme und Datenerhalt

Keine neue Entwicklungs-, Inventar-, Begleiter-, Kampf-, Namens- oder Speicherverwaltung. Kein Schemawechsel: SaveGame 11 bleibt gültig, ältere QA-Fixture wird regulär geladen. Identische individuelle GUID, Level 11, XP, Status, fehlende KP, vier aktive Attacken, Repertoire/AP und Teamposition erhalten; neue Artwerte werden mit dem vorhandenen Rechner bestimmt. Eine bestehende Glurak- oder sonstige Reserveninstanz wird nicht geändert. Der vorhandene Begleiteractor wechselt sein Modell bei unveränderter Individual-ID; kein zweiter Actor bleibt zurück. Normale Teamsortierung und Rücksortierung funktionieren.

Namensanzeige über dieselbe zentrale Darstellung; keine neue Entfernungsgrenze oder Änderung der bestehenden Hinter-Bäumen-Regel. Klassischer Kampf, echte geerbte Attacke/AP-Verbrauch, realer Wildfang, Teamerweiterung und wieder einsetzender Begleiter in PIE und eigenem Prozess geprüft. Keine Änderung an Fangraten, KI-/Tagesrhythmusprofilen, Beleuchtung oder Controllergrundbelegung.

## 6. Tatsächliche Tests


| Prüfung | Ergebnis | Nachweis |
| --- | --- | --- |
| Native01 | BESTANDEN; 82 protokollierte Schritte, 18 Prüfungen, 116.2 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native01/Result.json) |
| Native02 | BESTANDEN; 94 protokollierte Schritte, 22 Prüfungen, 139.6 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Result.json) |
| PIE01 | FEHLGESCHLAGEN; 85 protokollierte Schritte, 17 Prüfungen, 124.2 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/PIE01/Result.json) |
| PIE02 | BESTANDEN; 94 protokollierte Schritte, 22 Prüfungen, 139.1 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/PIE02/Result.json) |
| Restart01 | BESTANDEN; 5 protokollierte Schritte, 3 Prüfungen, 20.0 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Restart01/Result.json) |
| Functional01 | BESTANDEN; 76 protokollierte Schritte, 22 Prüfungen, 228.4 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Functional01/Result.json) |
| Travel01 | BESTANDEN; 2 protokollierte Schritte, 3 Prüfungen, 27.4 s | [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Travel01/Result.json) |


Native01 ist der erste erfolgreiche Kernlauf. PIE01 bestand die Entwicklung/Begleiterstrecke, scheiterte aber am ersten nicht erreichbaren Wildfokus und gilt insgesamt nicht als bestanden. PIE02 und Native02 verwenden begrenzte normale Annäherungs-/Interaktionsversuche; keine ausgeschaltete Wild-KI oder vereinfachte Ersatzkämpfe. Standortwechsel zwischen Teilprüfungen sind explizite Aufstellung, dazwischen echte Enhanced-Input-Bewegung; kein vorgetäuschter durchgehender Map-Fußlauf. Kein neu bestätigter physischer Controller-Test.


- ModelsV4Build01: früher fehlgeschlagener Build, neuer Testcode korrigiert; siehe [Console.log](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4Build01/Console.log).

- ModelsV4Build02: {"mode": "Build", "exit": 0, "seconds": 6.936374187469482}; [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4Build02/Result.json)

- ModelsV4Build03: {"mode": "Build", "exit": 0, "seconds": 9.497750043869019}; [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4Build03/Result.json)

- ModelsV4Automation01: Wrapper nicht bestanden; {'succeeded': 307, 'succeededWithWarnings': 0, 'failed': 1}.

- ModelsV4Automation02: {"mode": "Automation", "exit": 0, "seconds": 67.49132299423218, "summary": {"succeeded": 308, "succeededWithWarnings": 0, "failed": 0, "notRun": 0, "inProcess": 0}}; [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4Automation02/Result.json)

- ModelsV4Automation03: {"mode": "Automation", "exit": 0, "seconds": 41.12445306777954, "summary": {"succeeded": 308, "succeededWithWarnings": 0, "failed": 0, "notRun": 0, "inProcess": 0}}; [Result.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4Automation03/Result.json)


Erster Build: neuer Testcode verwendete TObjectPtr ohne `.Get()`, korrigiert. Erste Automation: 307 bestanden/1 fehlgeschlagen, weil der neue reine BattleSession-Test versehentlich Legacy- statt produktiver Kristall-Effektregeln verwendete; Testfixture korrigiert, keine Produktions-Kampflogik verändert. Die alten fehlendes-Raichu-Erwartungen in einem Inventartest und Wiederholungswerkzeug sind gezielt auf das nun reale Ziel bzw. einen tatsächlich falschen Stein aktualisiert.

Zwölf bestehende Map Checks: jeweils **0 Fehler, 0 Warnungen**. Keine Map gespeichert. Einzelprotokolle: 
[MapCheckResults.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/MapCheckResults.json).


Neue sechs Automationgruppen decken Gen-2-Artendaten/Registrierung, Mesh/Skeleton/alle Rollen/Maßstab, reale Donnersteinroute und individuelle/AP-Übernahme, bestehenden Save-/Partytransport, tatsächliche BattleSession mit Elektroattacke sowie Wechsel im gemeinsamen VisualActor/Namensmaterial ab. Bestehende TestGround-Tests laufen nun mit allen 19 Modellen. Tatsächliche Transaktionsfehler, Neustart, Begleiter und optische Ergebnisse sind zusätzliche Gameplay-/Datei-/Rendernachweise, keine aus einem Unit-Test abgeleiteten Behauptungen.

Externe/alte Engine-Meldungen werden getrennt bewertet: experimentelle ToolsetRegistry-Python-Startfehler (`ToolsetDefinition`, `PythonTestRunner`) in nativen Prozessen, bekannte Startup-Assertions sowie Python-Namens-/Layoutwarnungen sind keine neuen Raichu-Fehler, aber die vollständigen Engine-Logs werden deshalb nicht als warnungsfrei bezeichnet. Die gezielte Logprüfung fand in den aktuellen geprüften Logs keine Fatal-/Ensure-/Assertion-failed-Zeile und keinen `idevice_id: Bad CPU type`-Fehler. Der letzte Automationprozess protokolliert weiterhin 17 bekannte Startup-Condition-Assertions außerhalb der bestandenen Projekt-Testqueue; native Starts je eine frühe Movement-Iterationswarnung und fünf experimentelle Toolset-Missing-Type-Meldungen. Das wird nicht als warnungsfreies gesamtes Engine-Log ausgegeben. Die Engine wurde nicht verändert; Einzelbefunde stehen in `Saved/ProjectRefinement/ModelsV4/LogAudit.json`.

## 7. Echte visuelle Nachweise


- Blender Front: [Front.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Blender/Front.png)

- Blender Back: [Back.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Blender/Back.png)

- Blender Left: [Left.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Blender/Left.png)

- Blender Right: [Right.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Blender/Right.png)

- Blender GameAngle: [GameAngle.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Blender/GameAngle.png)

- Stone_Offer: [Stone_Offer.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Stone_Offer.png)

- Stone_Cancelled: [Stone_Cancelled.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Stone_Cancelled.png)

- Stone_Complete: [Stone_Complete.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Stone_Complete.png)

- Team_Raichu: [Team_Raichu.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Team_Raichu.png)

- Buddy_Village: [Buddy_Village.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Buddy_Village.png)

- Buddy_Forest: [Buddy_Forest.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Buddy_Forest.png)

- TestGround_Raichu: [TestGround_Raichu.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/TestGround_Raichu.png)

- Raichu_Pikachu_Player: [Raichu_Pikachu_Player.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Raichu_Pikachu_Player.png)

- Raichu_ClassicBattle: [Raichu_ClassicBattle.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Native02/Raichu_ClassicBattle.png)

- Restart_Raichu: [Restart_Raichu.png](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Restart01/Restart_Raichu.png)

- Rohmodellübersicht aus tatsächlichen Blender-Intakes: [Incoming_Overview.jpg](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Incoming_Overview.jpg)
- Tatsächliche deformierte Posen: [Motion_Overview.jpg](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/Motion_Overview.jpg)


Die oben verlinkten Native02-/Restart01-Unreal-Aufnahmen sind nativ 2560×1440, aus normaler Spielkamera bzw. unveränderter bestehender Entwicklungs-/Kampfdarstellung. Blender-Ansichten sind ausdrücklich Blender, keine behaupteten Unreal-Bilder. Zusammenstellungen enthalten ausschließlich echte Renderbilder. Zusätzliche PIE-Bilder besitzen die tatsächlich gemessene Editor-Viewportgröße 2940×1696 und werden nicht als native QHD-Bilder umdeklariert; ImageProof.json enthält Abmessungen und SHA-256 aller 26 aktuellen Unrealbilder. Keine KI-Bilder als Nachweis, keine künstliche Video-FPS. Still-Posen erlauben keine vollständige temporale Bewegungsfreigabe. Kein neuer verlässlich flüssiger Gameplayclip erstellt.

## 8. Performance

MacBook Air Mac16,12, Apple M4/16 GB, macOS 27.0.1, UE 5.8.2 (56702186); Hardwareangaben aus dem unmittelbar vorangehenden lokalen Hardwareaudit, keine neue Hardware geschätzt. Profil C unverändert: 2560×1440 Ausgabe, 75 % / etwa 1920×1080 intern, TAAU, High, Software-Lumen/IFG, VSM4. 120 reale Minuten/Spieltag und 75° Mittagssonne bleiben erhalten. Laufzeitwerte beider nativer Prozesse bestätigen das Profil. Die separaten Prozesse verwenden die Development-Editorbinärdatei mit `-game` und eigenem UserDir; kein gekochter Shipping-Build wurde behauptet. Kein Recorder während der kurzen CSV-Fenster; Screenshots danach. Normale KI und echter Raichu-Begleiter aktiv.


| Lauf / Ort | valide Frames | FPS Mittel | Frame ms | GPU ms | Game ms | Render ms | p95 ms | 1%-Low FPS | Maximum ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Native01 / Forest | 307 | 37.25 | 26.85 | 26.45 | 2.34 | 26.84 | 29.38 | 32.60 | 31.19 |
| Native01 / Village | 227 | 36.11 | 27.69 | 27.31 | 2.87 | 27.39 | 29.80 | 17.46 | 81.65 |
| Native02 / Forest | 228 | 30.39 | 32.91 | 32.48 | 2.43 | 32.92 | 35.61 | 26.73 | 37.59 |
| Native02 / Village | 227 | 30.07 | 33.26 | 32.85 | 2.95 | 33.03 | 36.52 | 16.43 | 82.54 |


CSV-Metadaten und unplausible Werte ausgeschlossen; Renderthreadzeiten können GPU-Wartezeit enthalten und beweisen keinen neuen CPU-Engpass. Das CSV enthält nur seine tatsächlich gespeicherten gültigen Frames, nicht jede Sekunde des vollständigen Testablaufs. 1%-Low = 1000 / Mittel der langsamsten rund 1 % der gültigen Framezeiten; bei kurzen Fenstern stark ausreißerempfindlich. Die Zahl gilt nicht als vollständiger Langzeitbenchmark.

Erster Lauf rund 36–37 FPS, zweiter rund 30 FPS mit p95 über 33,3 ms; Dorf-Maxima über 80 ms. **Stabile 30 FPS nicht nachgewiesen.** Keine kausale Zuordnung der Laufdrift oder der Spitzen zu Raichu behauptet. Werte liegen im zuvor berichteten groben 25–40-FPS-Bereich, sind aber kein streng gepaarter Modellkostenvergleich. Kampf/Testgelände technisch und optisch geprüft, nicht separat als belastbarer GPU-Benchmark ausgegeben. Keine Qualitätsreduzierung oder Renderingumstellung.

## 9. Einschränkungen und nächste Modelle

- Raichu technisch verfügbar, visuelle Endfreigabe offen; eigener stilisierter Kandidat mit schlichten Materialflächen und noch einfacher Mimik. Kein Anspruch auf identische Qualität aller bisherigen Meshy-Texturen.
- Numerisch geschlossene Fußtracks und geprüfte Posen ersetzen keine abschließende Beurteilung von Gang/Schwanz/Faint bei Echtzeitbewegung. Kameraabhängige Details und größere Animationsauslenkungen später gezielt abnehmen.
- 72.352 Dreiecke/sechs Slots und ein LOD: kein unnötiges neues Laufzeitsystem, dennoch spätere abgeleitete LODs für viele gleichzeitige Exemplare sinnvoll. Kein neuer Raichu-Wildspawn in diesem Auftrag.
- 20 weitere Meshy-Arten bleiben echte, aber ungeriggte/unregistrierte Quellen. Besonders Safcon/Kokuna sowie Bisaknosp/Bisaflor bieten sich an, vorhandene Ketten zu schließen. Turtok benötigt zunächst Schillok. Evoli allein genügt keiner Steinroute, solange Aquana/Blitza/Flamara fehlen.
- Frühere besondere Tauschentwicklungen erhalten keine erfundenen endgültigen Level/Orte/Prüfungen. Keine weiteren Arten oder neuen Attackeneffekte implementiert.
- Vorbestehende Grafikprofil-/Framezeit-/temporale IFG-Fragen bleiben offen; keine neue visuelle Renderingfreigabe aus diesem Modellauftrag ableiten.

## 10. Dateischutz und Git


Abschließender Hashnachweis: {"baseline_project_files": 5956, "authorized_existing_files_changed": ["Docs/ENTSCHEIDUNGEN.md", "Source/PokeMonster/Tests/PokeMonsterInventoryV2Test.cpp", "Tools/EvolutionV3/Gameplay.py", "Tools/InventoryV2/Gameplay.py"], "unexpected_changes": [], "missing_baseline_files": [], "preexisting_saves_checked": 583, "changed_or_missing_preexisting_saves": [], "protected_untracked_checked": 34, "changed_protected_untracked": [], "user_DefaultEngine_unchanged": true, "protected_maps_unchanged": true, "backup_refs_unchanged": true}; [ProtectionFinal.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/ProtectionFinal.json).


Technik-/Datencommit `67476bc23652da2ba19192a0f916edad4fe17344` wurde regulär auf origin/main gepusht. Alle 25 neuen LFS-Objekte (28797214 Bytes) wurden anschließend vom Server heruntergeladen und per SHA-256 verifiziert; LFS-Dry-Run leer. Dieser Prüfbericht wird in einem getrennten Dokumentationscommit gesichert. Der danach erzeugte [abschließende Git-/LFS-Nachweis](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/GitFinal.json) nennt beide tatsächlichen Commits und den abschließenden main/origin/main-Abgleich. Budget-/Zahlungseinstellungen wurden nicht geändert. Feature-Nachweis: [GitFeature.json](/Users/harry/Developer/PokeMonster/Saved/ProjectRefinement/ModelsV4/GitFeature.json).
