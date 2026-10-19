"""Check saved V7 material graphs, source references and visual-only groups."""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2WorldArtV7';A=R/'Art/World/VisualV2WorldArtV7';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();rows=[]
for r in json.loads((A/'AssetManifest.json').read_text())['materials']:
 m=unreal.load_asset(r['new']);assert m and isinstance(m,unreal.Material)
 nodes=unreal.MaterialEditingLibrary.get_material_expressions(m);custom=[n for n in nodes if isinstance(n,unreal.MaterialExpressionCustom)]
 field=(A/'RouteField.hlsl').read_text();count=0
 for n in custom:
  code=n.get_editor_property('code')
  if field in code:assert all(unreal.MaterialEditingLibrary.get_inputs_for_material_expression(m,n));count+=1
 assert count==(1 if r['key']=='Ground' else 2)
 rows.append({'asset':r['new'],'verified_custom_nodes':count,'source':r['old']})
delta=json.loads((A/'Scope.json').read_text());actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
for g in delta['new_groups']:
 a=actors[g['name']];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and c.get_instance_count()==g['count'] and c.static_mesh.get_path_name()==g['mesh'];assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;assert not c.get_editor_property('affect_distance_field_lighting') and not c.get_editor_property('affect_dynamic_indirect_lighting')
 assert [c.get_material(i).get_path_name() for i in range(c.get_num_materials())]==g['materials']
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(S/'MaterialVerification.json').write_text(json.dumps({'materials':rows,'hism_groups':len(delta['new_groups']),'instances':delta['new_instances'],'zero_new_collision':True,'no_shader_compilation_claim_from_graph_check':True},indent=2));unreal.log('WA7_MATERIAL_GROUP_VALIDATION_PASS')
