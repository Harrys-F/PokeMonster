# Hobbit-Player: Bildquellen und Zuordnung

Alle PNGs in diesem Ordner sind transparente, auf 256 × 512 Pixel normierte Arbeitsdateien. Die Bodenlinie ist für alle Posen gleich; die Paper2D-Sprites verwenden `Bottom Center` als Pivot und 3,4 Pixel pro Unreal-Einheit.

| Spielrichtung | Walk (beide Frames) | Idle |
| --- | --- | --- |
| Down | Bild 2: Front, Frames 1–2 | Bild 1: Front |
| DownRight | Bild 2: Front-Right, Frames 1–2 | Bild 1: dreiviertel Front |
| Right | Bild 2: Right, Frames 1–2 | Bild 2: Right, Frame 1 |
| UpRight | Bild 2: Back-Right, Frames 1–2 | Bild 2: Back-Right, Frame 1 |
| Up | Bild 2: Back, Frames 1–2 | Bild 1: Rücken |
| UpLeft | Bild 2: Back-Left, Frames 1–2 | Bild 2: Back-Left, Frame 1 |
| Left | Bild 2: Left, Frames 1–2 | Bild 2: Left, Frame 1 |
| DownLeft | Bild 2: Front-Left, Frames 1–2 | Bild 2: Front-Left, Frame 1 |

Bild 1 enthält keine eindeutig passenden, sauberen Idle-Ansichten für Right, UpRight, UpLeft, Left und DownLeft. Die jeweiligen Walk-Frames 1 aus Bild 2 dienen daher als **vorläufige** Standbilder. Die Walk-Flipbooks spielen zwei unterschiedliche Frames mit 8 FPS ab; die Idle-Flipbooks halten einen Frame. Die Originalreferenzen wurden vom Nutzer als Chat-Anhänge bereitgestellt.
