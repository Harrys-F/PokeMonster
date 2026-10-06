# Young Trainer – Kopf, Gesicht und Haare V3

Datum: 2026-10-06. Ausgangs-HEAD: `eafab5b Complete healing house art quality V3`.
Ausgangsstatus und Endstatus: `?? Art/Characters/`. Der Charakterordner war bereits
aus den vorherigen Arbeiten unversioniert. Kein Commit, kein Push, nichts gestaged.

## Ergebnis und Grenzen

Der Kopf wirkt jugendlicher und freundlicher als V2: kürzere, weichere untere
Gesichtswirkung, weniger breite Kieferkontur, näher zusammenliegende braune Augen,
kleine Nase und ein schmaler neutral-freundlicher Mund. Die Frisur besitzt
asymmetrische Vordergruppen, mehr seitliches Volumen, einen bedeckten Hinterkopf
und eine unregelmäßige Lockenkontur.

Die angestrebte sofortige, eindeutige Wiedererkennbarkeit als genau die Figur im
Portrait ist **noch nicht erreicht**. Das Gesicht wirkt weiterhin puppenhafter,
die Augen flächiger und die Haargruppen stärker als einzelne modellierte Formen
als in der gezeichneten Referenz. Einzelne Übergänge zeigen noch glatte
Untervolumen zwischen den Locken. Die sichtbaren Unterschiede werden nicht durch
neue Texturen, Kleidung oder Accessoires kaschiert. Dieser Stand ist eine
überprüfbare Korrekturstufe, keine Freigabe für Finalisierung oder Rigging.

## Vorher und nachher

V2 zeigte eine breite, aufgeblähte untere Gesichtshälfte, weit auseinanderliegende
Augen, unruhige Übergänge um Augen und Mund sowie eine überwiegend nach vorn
gekämmt wirkende Haarmasse. Die bisherige Nasenspitze war kantig und der
Mundbereich optisch eingesunken. Das Portrait zeigt dagegen ein weiches Kinn,
kurze Gesichtszüge und klar voneinander lesbare, geschwungene Lockengruppen.

| Merkmal | V2 | V3 |
| --- | --- | --- |
| Nackter Kopf, Breite | ca. 29,38 cm | 29,00 cm |
| Nackter Kopf, Tiefe | ca. 23,39 cm | 25,37 cm |
| Nackter Kopf, Höhe | ca. 24,91 cm | 26,80 cm |
| Unterkante Kopf | ca. Z 107,11 cm | Z 106,40 cm |
| Oberkante Schädel ohne Haare | ca. Z 132,02 cm | Z 133,20 cm |
| Augenmittelpunkte X | ca. ±7,7 cm | ±5,6 cm |
| Augenmittelhöhe | ca. Z 117,97 cm | Z 118,70 cm |
| Weißfläche pro Auge | andere V2-Form | ca. 5,88 × 5,70 cm |
| Iris pro Auge | andere V2-Form | ca. 4,10 × 4,40 cm |
| Mundlinie | unruhiger V2-Übergang | ca. 4,13 cm breit, Z 111,1 cm |
| Kopfregion einschließlich Haare, Breite | ca. 40,02 cm | ca. 41,23 cm |
| Gesamthöhe Figur einschließlich Haare | 140 cm | 140 cm |

Das sind geometrische Weltmaße in neutraler Pose, keine auf das Portrait
registrierten Bildmessungen. Der Schädel wurde bewusst etwas höher und tiefer,
nicht pauschal in allen Achsen vergrößert. Der weichere Gesichtseindruck entsteht
auch durch die neu aufgebaute Wangen-, Kinn- und Augenform.

Die Augen erhalten einfache almondförmige Lider, braune Iris, Pupille und zwei
große Vorschau-Glanzflächen. Die Wölbung wurde nach der Profilkontrolle reduziert,
damit die Augen weniger aufgesetzt wirken. Brauen bleiben einfache weiche Bögen.
Die Nase ist eine kleine Form im Gesichtsmesh, ohne realistische Nasenwurzel.
Die Mundlinie besitzt nur einen leichten freundlichen Bogen. Ohren wurden
verkleinert und 1,1 cm angehoben, ohne Hals oder Körper zu verschieben.

## Haarform und Spielansicht

55 große, unterschiedlich ausgerichtete Gruppen formen Stirn, Krone, Seiten,
Hinterkopf und Nacken. Abgeflachte Querschnitte, längere Bögen, schmalere Spitzen
und fünf herausstehende Konturgruppen ersetzen die zunächst zu runden Locken.
Das Untervolumen wurde an den tatsächlichen Hinterkopf angepasst: Die erste
Variante lag im unteren Hinterkopf teilweise innerhalb des Schädels. V3 bedeckt
dieses Gebiet jetzt bis in den Nacken. Keine Einzelhaare, kein Groom.

Die erhöhte Kamera verdeckte anfangs Augen durch tief vorstehende Stirnhaare.
Deren untere Bereiche wurden örtlich zurückgenommen und die tiefsten Spitzen
angehoben. Beide Augen bleiben in der Front-/Front-3/4-Spielperspektive sichtbar.
Bei der letzten Haarverschlankung sank die obere Kontur um 3,36 mm; ausschließlich
die Haarregion oberhalb Z 132 cm wurde wieder auf Z 140 cm ausgerichtet.
Körper, Füße und Ursprung blieben unverändert.

Geprüft wurden Front, vorne-rechts, rechts, hinten-rechts, hinten, hinten-links,
links und vorne-links sowie zusätzliche Front-/Rück-3/4-Ansichten. Keine Richtung
zeigt verschwundene Haare, freie kahle Schädelstellen oder einen kollabierten
Kopfumriss. Die unterschiedlich beleuchteten glatten Bereiche zwischen Gruppen
sind braunes Haar-Untervolumen. Dessen Sichtbarkeit bleibt ein Formqualitätslimit.

Der zusätzliche Blender-Test übernimmt die vorhandene Außenkamera:
**2500 cm Abstand, horizontaler FOV 35°, Pitch −55°, Figur 140 cm**, acht relative
Ansichtsrichtungen. Diese Werte wurden lesend im Player-C++ und in TECHNIK
bestätigt. Bei 1280 × 720 ist die Figur nur ungefähr 90 Pixel hoch. Augen sind
dann wenige Pixel groß; die genaue Portraitidentität lässt sich daraus nicht
belastbar bestätigen. Die Nahansichten zeigen die Formen besser, ersetzen
aber ausdrücklich nicht den Test bei tatsächlicher Entfernung. Kein Unreal-
Import und kein PIE-Test gehören zu diesem Blender-Arbeitsschritt.

## Erhalt und Topologie

Quelle: `Source/YoungTrainer_HeadHair_V3.blend`, gespeichert und erneut geöffnet.
Vorab-Sicherung: `Source/Stages/07_PreHeadHair.blend`, bytegleich zur V2-Quelle.
Alle 39 zu Beginn vorhandenen Charakterdateien bleiben bytegleich.

Die vier bisherigen Kopf-/Gesichts-/Haarobjekte liegen unverändert in
`YT_HeadHair_Source_V2`, ausgeblendet statt gelöscht. 77 neue Meshobjekte liegen
in `YT_HeadHair_V3`. Die vorhandenen acht Referenz-Empties sind unverändert,
einschließlich Bildern, Ausrichtung, Maßstab, Transparenz und Sperren.
Ein zusätzlicher gepackter Portrait-Ausschnitt steht gesperrt mit 45 %
Transparenz in `REF_PORTRAIT` neben dem Kopf. Keine perspektivische Portrait-
Überlagerung wird als exakte orthografische Registrierung ausgegeben.

Die Körpergeometrie erhält nur einen zusätzlichen relativen Shape Key für die
444 vorhandenen Ohrvertices. Alle Nicht-Ohrvertices dieses Keys entsprechen V2.
Kleidung, Rucksack, übrige Körpergeometrie, UVs, Gewichte, alte Materialien,
Armature, Restpose, Constraints und Actions sind unverändert.

Das neue Kopfmesh hat 2533 Vertices, 2416 Quads und 136 Dreiecke. Je Auge bestehen
vier 40-Punkt-Loops, am Mund vier 20-Punkt-Loops. Wangen/Kiefer sind Teil des
zusammenhängenden Gesichts-/Schädelmeshs. Die Halsanbindung wurde nicht neu
geriggt oder mit dem Körper verschmolzen. Die 100 offenen Kopfkanten gehören
zu den vorgesehenen Augen-/Mundöffnungen; Haarbasis-Unterkante und farbige
Augenflächen haben ebenfalls beabsichtigte Ränder.

Der Audit aller neuen Meshes bestätigt: keine losen Vertices, keine Flächen mit
Nullfläche, keine N-Gons und keine zusätzlichen nichtmanifold Kanten abseits
der vorgesehenen Ränder. Haargruppen sind geschlossen. Dies ist keine Prüfung
aller möglichen Selbstüberschneidungen oder eine Animationsfreigabe.
**Neue Kopfobjekte besitzen keine Armature-Modifier oder neuen Skin-Gewichte.**
Augen-/Mund-Loops bereiten spätere Bearbeitung vor; Gesichtsausdrücke,
Lidschluss und Verformbarkeit wurden gemäß Arbeitsumfang noch nicht animiert.

12 einfache Vorschau-Farbmaterialien betreffen ausschließlich Kopf/Gesicht/Haare
und Ohren. Keine finalen Texturen, neuen UVs oder komplexen Shader entstanden.

## Dateien und Prüfung

Neu in diesem Arbeitsschritt:

- `Source/YoungTrainer_HeadHair_V3.blend`
- `Source/Stages/07_PreHeadHair.blend`
- `Reference/HeadPass/Portrait.png`
- `Authoring/CorrectHeadHair.py`
- `Authoring/RenderHeadHair.py`
- `Authoring/ValidateHeadHair.py`
- `Authoring/CompareHeadHair.py`
- `HEAD_HAIR_V3.json`
- `HEAD_HAIR_V3_PRUEFBERICHT.md`

Native Renderbilder, Vergleichstafeln, Audit und Logs liegen ausschließlich im
ignorierten `Saved/YoungTrainerHeadPass/`. Automatische `.blend1`-Zwischenstände
sind dort erhalten, nicht gelöscht. Die Vergleichstafel zeigt links das
Originalportrait als unverzerrten Ausschnitt, mittig V2, rechts V3, mit gleicher
Blender-Kamera/Beleuchtung für beide Modelle.

Geometrie-/Erhaltungs-Audit: PASS für die endgültige Quelldatei.
Python-Syntax, JSON und Markdown sowie `git diff --check` wurden geprüft.
Für neue unversionierte Texte wurde zusätzlich `git diff --no-index --check`
gegen `/dev/null` ausgeführt. Kein C++ geändert, kein Unreal-Build erforderlich.
Keine bestehenden Projektdateien, Maps oder Assets außerhalb des Charakters
verändert. Kein Rigging, keine Animation, kein Export, kein Unreal-Import.

Die visuelle Freigabe ist ein sinnvoller nächster Git-Sicherungspunkt. Es wurde
noch nichts gestaged. Ausschließlich die neun Dateien dieses Passes wären:

```sh
git add -- Art/Characters/YoungTrainer/Source/YoungTrainer_HeadHair_V3.blend Art/Characters/YoungTrainer/Source/Stages/07_PreHeadHair.blend Art/Characters/YoungTrainer/Reference/HeadPass/Portrait.png Art/Characters/YoungTrainer/Authoring/CorrectHeadHair.py Art/Characters/YoungTrainer/Authoring/RenderHeadHair.py Art/Characters/YoungTrainer/Authoring/ValidateHeadHair.py Art/Characters/YoungTrainer/Authoring/CompareHeadHair.py Art/Characters/YoungTrainer/HEAD_HAIR_V3.json Art/Characters/YoungTrainer/HEAD_HAIR_V3_PRUEFBERICHT.md
```

Dieser Befehl ist nur dokumentiert, nicht ausgeführt. Die bereits vorliegenden
39 Dateien der früheren Charakterarbeiten müssen bei einer späteren gesamten
Charaktersicherung ebenfalls separat berücksichtigt werden.
