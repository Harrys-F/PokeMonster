"""Inspect runtime presentation only. No input, teleport, save, species exchange or map write."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();worlds=[w for w in unreal.ObjectIterator(unreal.World) if unreal.GameplayStatics.get_player_pawn(w,0)]
assert len(worlds)==1;w=worlds[0];rows=[]
inventory=json.loads((R/'Saved/CreaturePipelineV2/UnrealInventory.json').read_text());profiles={row['mesh']:unreal.load_asset(row['presentation']) for row in inventory['species'] if row.get('presentation')}
for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor):
 mesh=v.get_editor_property('mesh');d=profiles.get(mesh.get_skeletal_mesh_asset().get_path_name());assert d and not d.get_validation_errors();assert mesh.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 if d.get_editor_property('tail_flame'):
  f=v.get_editor_property('flame');assert f.get_attach_socket_name()==d.get_editor_property('flame_bone');assert f.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
 rows.append({'profile':d.get_path_name(),'mesh':mesh.get_skeletal_mesh_asset().get_path_name(),'validation_errors':list(d.get_validation_errors())})
result={'world':w.get_name(),'runtime_presentations':rows,'checked_presentations':len(rows),'passed':bool(rows),'no_gameplay_actions':True};(R/'Saved/CreaturePipelineV2/PIESmoke.json').write_text(json.dumps(result,indent=2));assert rows,'No 3D creature instance observed; do not claim a runtime pass';unreal.log('CREATURE_PIPELINE_V2_PIE_SMOKE_PASS')
