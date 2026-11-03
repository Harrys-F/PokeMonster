# V4 authoring plan and recovery

Baseline: 38c6d87e, main synchronized with remote. Map bytes match its immutable local LFS object. Saved/ProjectRefinement/VisualV2WorldRefinementV4/MapRecoveryBaseline.json records exact SHA256, size and commit/pointer. No redundant project/map copy or new map is required. All original tracked/untracked files, local assets and saves have separate hash manifests. Do not rerun V3 authoring passes.

1. Fresh native timing/cost isolation, editor read-only geometry/material/instance audit and all 21 before views.
2. Own V4 terrain derivative, asymmetric low rolling shapes with protected roads, building pads, functional actors and habitat water core; continuous non-playable distant land forms to replace blank cut-off horizons. No tree wall.
3. Own ground/material graphs using existing local source textures and baked static masks where profiling justifies removal of repeated per-pixel calculations. Original graphs/assets remain untouched.
4. All house elevations: proper plaster/wood/stone normals, roof mapping along real slopes, bounded window/shutter/sill/brace additions on rear/sides, preserving all doors, layout, collision and cutaway systems. Use existing architecture meshes.
5. Bridge: existing collision remains authoritative; fewer coherently joined visual pieces, bevelled timber, real bearings and connected rails, varied grain. Actual widths/heights checked, all three pm.Speed values tested without changing its implementation.
6. Water: own geometries/materials with irregular shoreline and shallow margins, preserved deep pond/habitat core; stream flow along actual centerline and micro-ripples. No duplicate water layers, Garados and habitats unchanged.
7. Refine existing vegetation placement and consolidate genuinely redundant/material-split draws only after measured evidence. No blanket density reduction or rendering/profile/camera changes.
8. All 21 matched views plus missing healing-house side view, native/PIE routes, terrain projection and water habitat tests, full 325+ suite, build, twelve map checks, strict wrapper, protected hashes. Scope-review commit/push and remote LFS SHA verification. Await Harry's visual review; never update Westland.
