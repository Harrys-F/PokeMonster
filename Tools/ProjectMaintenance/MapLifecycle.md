# Map lifecycle

Six obsolete map files may be removed after the phase-one QA; exact paths and immutable source hashes are in MapLifecycle.json. The historical commit and LFS payloads remain available. Historical entry points refuse absent scenes with exit 2 and an explicit NOT EXECUTED message; they never silently create replacement maps. No archived source assets are removed.

The current NPCMotionV3 FinalMapAudit compares against the required, SHA-256-pinned actor signatures from the original NPCMotionV2 map. Collision, mesh, material, transform, LOD, instance and light comparisons remain strict. Existing missing/new-actor assertions remain unchanged. The archived source map is not needed to run this current regression check.

The retained current map fixtures remain required by CoreFiles.json. Do not turn missing required files into a pass. Generic historical replays require an explicitly approved restore into the same project using the recorded Git commit and LFS objects; do not create project copies or maps automatically. BattleTest and WestlandVillage stay because their independent test coverage has not been replaced.
