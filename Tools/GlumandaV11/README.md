# Glumanda V1.1 – Modell-/Namensbaustein

Nur aktives Projekt `/Users/harry/Developer/PokeMonster`.
`InspectMesh.py` und `InspectRepairedMesh.py` prüfen positionsverschweißte
Diagnosekopien, nicht das originale Render-Mesh. `PrepareMesh.py` erzeugt aus
der erhaltenen V1-Quelle eine eigene V1.1-Quelle: zehn kleine Randloops als
flache, UV-projizierte Kappen; alle ursprünglichen Vertices/UVs bleiben erhalten.
Die absichtliche 43-Kanten-Grenze zur Schwanzflamme bleibt offen.
Kniegewichte werden nur mit gemessenem Deformationsgewinn und maximal 3 mm
animierter Oberflächenabweichung übernommen. Keine Retopologie/Decimation.
Eine existierende eigene Arbeitsdatei darf nur nach Vergleich mit dem ausdrücklich
lokal erfassten `OwnedSourceRevision.json` überschrieben werden. Nicht blind auf
manuell veränderte Quellen anwenden. `.blend1` wird nicht erzeugt oder gelöscht.

`ValidateMesh.py` öffnet V1/V1.1 unabhängig neu, vergleicht Positionen, UVs,
Normalen mit Float-Toleranz, Bone-Restmatrizen und alle sieben Animationskurven;
prüft echte verbleibende Randkanten, Gewichte und FBX-Roundtrip.
Blender-Aufruf: `/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 3 --python Tools/GlumandaV11/ValidateMesh.py`.

`RenameGlumanda.py` korrigiert ausschließlich den Anzeigenamen der bestehenden
Spezies. `ImportMesh.py` importiert nur den eigenen V1.1-Skin, verwendet exakt das
vorhandene Skeleton, alle sieben Clips, Originalmaterialien und die Schwanzflamme.
Ein vorhandener eigener Kandidat wird nur mit lokalem Importnachweis und geprüftem
Quellpfad aktualisiert; keine Originalassets reimportieren.
`ReviewCandidate.py` nutzt die bestehende reine Darstellungs-API in PIE für sieben
Clips und acht Richtungen. `ApplyMesh.py` bindet das bestandene Profil einmalig.
Alle Ergebnisse/Medien bleiben im ignorierten `Saved/GlumandaV11`; Bildfolgen sind
keine Echtzeitvideos. `PrepareEvidence.py` schneidet nur echte QHD-Aufnahmen zu.

Geprüfte Grenzen und Gesamtfortschritt:
`Docs/GLUMANDA_V11_KAMPFANSICHT_SICHTKREIS_PRUEFBERICHT.md`.
