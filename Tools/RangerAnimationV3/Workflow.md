# Wanderer V3 – Achsen- und Kontaktprüfung

Experimenteller Arbeitsablauf, keine automatische Artfreigabe. V2 bleibt unverändert.

1. Originaldateien und offene Änderungen per SHA-256 erfassen. Neue Quelle,
   Skeleton, Animationsassets und Testkarte verwenden; Gameplay-Source erhalten.
2. Anatomische Vorderseite visuell bestimmen. Beim Ranger ist Blender −Y vorne;
   nach dem geprüften FBX-Import ist Unreal +X vorne. Lokale Bone-Achsen sind
   davon zu unterscheiden. Nicht allein aus Bone-Namen auf Rotationsachsen schließen.
3. Rest- und Pose-Matrizen von Hüfte, Knie, Knöchel und Fuß aufzeichnen. Die Pose
   bei 0,225 s zwischen Blender und Unreal vergleichen. Ein rückwärts gerichteter
   Kniepol darf nicht durch kleinere Schrittlänge kaschiert werden.
4. Kniepol auf die Ebene senkrecht Hüfte→Knöchel projizieren. Er muss zur
   anatomischen Vorderseite zeigen. Unerreichbare Ziele abfangen, keine stillen
   Kettenstreckungen oder getrennte Fußtranslationen hinzufügen.
5. Knöchelspur und Sohlengeometrie getrennt messen. Ein 29-cm-Knöchelabstand ist
   keine Aussage über die gesamte äußere Schuhbreite.
6. Standphase rückwärts mit tatsächlicher Geschwindigkeit führen; Schwungphase
   mit kontinuierlicher Rückführung und Fußfreiheit. Zyklusdauer × Geschwindigkeit
   muss zum Schrittpaar passen. Anschließend realen Weltkontakt prüfen.
7. Weltkoordinaten-Pins nur für flachen Boden verwenden. Große Korrekturen,
   verworfene Pins, Stopps und Drehungen ausdrücklich prüfen. Schutzgrenzen sind
   keine fertigen Pivotanimationen. Gespräch darf die Standbeine nicht überschreiben.
8. Mantel und Ausrüstung separat beurteilen. Fusionierte Meshy-Geometrie lässt
   keine zuverlässige automatische semantische Gewichtung zu. Keine manuelle
   Weight-Paint-Arbeit behaupten, wenn nur räumliche Skriptmasken verwendet wurden.
9. Echte Bewegungsaufnahme aus dem Unreal-Framebuffer mit tatsächlichen
   Zeitstempeln erstellen. Vorher die Prüfstrecke auf Felsen/Kronen prüfen.
   Vergrößerte Ausschnitte liefern keine zusätzlichen Originalpixel.
10. Video-Capture verursacht Readback-/Encodingkosten. Niemals dessen FPS als
    Performancebeleg benutzen. Messmatrix separat, ohne Blender/Build/Videoencoding.
11. Den richtigen sichtbaren Gameplay-NPC ausdrücklich auswählen; Actor-Iteration
    kann sonst deaktivierte Previewactors liefern. Ausgabe, Render-Target,
    interne Auflösungsfraktion, Kamera und drei AB/BA-Paare verifizieren.
12. Build, vollständige Automation, Map Check und realen Enhanced-Input-Fußlauf
    durchführen. Dev-Save vorher sichern und nur unter Hashkontrolle restaurieren.
    Die Referenzfreigabe benötigt weiterhin eine künstlerische Sichtprüfung.

Offene V3-Arbeit: entspanntere Becken-/Kniehaltung, handgesetzte Übergangs- und
Pivotkontakte, gezieltes manuelles Weight Painting an Gurten/Taschen/Mantel,
gegebenenfalls getrennt genehmigte Zehenartikulation und Gelände-IK.
