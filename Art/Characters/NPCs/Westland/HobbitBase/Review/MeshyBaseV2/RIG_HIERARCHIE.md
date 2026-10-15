# Bestehendes Rig: 25 Bones, unverändert

| Bone | Parent | Deform | Head (m) | Tail (m) |
| --- | --- | --- | --- | --- |
| root | — | True | [0.0, 0.0, 0.0] | [0.0, 0.0, 0.12] |
| pelvis | root | True | [0.0, 0.0, 0.61] | [0.0, 0.0, 0.74] |
| spine | pelvis | True | [0.0, 0.0, 0.74] | [0.0, 0.0, 0.91] |
| chest | spine | True | [0.0, 0.0, 0.91] | [0.0, 0.0, 1.055] |
| neck | chest | True | [0.0, 0.0, 1.055] | [0.0, 0.0, 1.13] |
| head | neck | True | [0.0, 0.0, 1.13] | [0.0, 0.0, 1.37] |
| cape_upper | chest | True | [0.0, 0.105, 1.015] | [0.0, 0.145, 0.66] |
| cape_lower | cape_upper | True | [0.0, 0.145, 0.66] | [0.0, 0.18, 0.275] |
| cape_left | cape_upper | True | [0.17, 0.14, 0.66] | [0.17, 0.18, 0.28] |
| cape_right | cape_upper | True | [-0.17, 0.14, 0.66] | [-0.17, 0.18, 0.28] |
| clavicle_l | chest | True | [0.035, 0.0, 1.035] | [0.215, 0.0, 1.04] |
| upperarm_l | clavicle_l | True | [0.215, 0.0, 1.04] | [0.425, -0.005, 1.043] |
| lowerarm_l | upperarm_l | True | [0.425, -0.005, 1.043] | [0.585, -0.024, 1.025] |
| hand_l | lowerarm_l | True | [0.585, -0.024, 1.025] | [0.697, -0.038, 1.005] |
| clavicle_r | chest | True | [-0.035, 0.0, 1.035] | [-0.215, 0.0, 1.04] |
| upperarm_r | clavicle_r | True | [-0.215, 0.0, 1.04] | [-0.425, -0.005, 1.043] |
| lowerarm_r | upperarm_r | True | [-0.425, -0.005, 1.043] | [-0.585, -0.024, 1.025] |
| hand_r | lowerarm_r | True | [-0.585, -0.024, 1.025] | [-0.697, -0.038, 1.005] |
| bag | spine | True | [0.22, -0.04, 0.78] | [0.245, -0.04, 0.59] |
| thigh_l | pelvis | True | [0.105, 0.0, 0.61] | [0.133, -0.009, 0.32] |
| shin_l | thigh_l | True | [0.133, -0.009, 0.32] | [0.16, 0.0, 0.085] |
| foot_l | shin_l | True | [0.16, 0.0, 0.085] | [0.16, -0.16, 0.05] |
| thigh_r | pelvis | True | [-0.105, 0.0, 0.61] | [-0.133, -0.009, 0.32] |
| shin_r | thigh_r | True | [-0.133, -0.009, 0.32] | [-0.16, 0.0, 0.085] |
| foot_r | shin_r | True | [-0.16, 0.0, 0.085] | [-0.16, -0.16, 0.05] |

Keine Pose-Constraints und keine separaten IK-/Steuerbones vorhanden. Die Zweigelenk-Beinlösung wurde beim Erstellen der ursprünglichen Animationen ausgeführt und in FK-Bone-Keys gebacken. Hier wird kein Solver neu ausgeführt.

Handbones ermöglichen grobe Arm-/Handgesten, aber keine unabhängigen Fingerbewegungen. Füße besitzen keine Zehen-/Foot-Roll-Bones. Gesicht und Augen besitzen keine eigenen Bones. Zusätzliche Bones erfordern eine gesonderte Freigabe.
