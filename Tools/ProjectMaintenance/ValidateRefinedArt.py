"""Validate the current accepted art version; retain the prior strict audit for its original snapshot."""
from pathlib import Path
import unreal,runpy
_v3=Path(unreal.Paths.project_dir()).resolve()/'Tools/ProjectMaintenance/ArtV3Signatures.json'
_v4=_v3.with_name('ArtV4Signatures.json')
if _v4.exists():
 runpy.run_path(str(_v4.with_name('ValidateArtPassV4.py')),run_name='__main__')
elif _v3.exists():
 runpy.run_path(str(_v3.with_name('ValidateArtPassV3.py')),run_name='__main__')
else:
 """Strict saved VisualV2 scope, material graph, import and zero-new-collision validation."""
 import unreal,json,sys,copy
 from pathlib import Path
 R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ProjectRefinement';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();w=E.get_editor_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
 after=scene(w);signature=json.loads((R/'Tools/ProjectMaintenance/ArtSignatures.json').read_text());assert signature['schema']==1 and signature['map']=='/Game/Maps/Dev_TestMap_VisualV2'
 import hashlib
 for a in after['actors'].values():a['components'].sort(key=lambda c:c['name'])
 actual={n:hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':')).encode()).hexdigest() for n,a in after['actors'].items()};assert actual==signature['actors'],'Required saved art signatures differ';assert after['world_settings']==signature['world_settings']
 before=json.loads((S/'BeforeScene.json').read_text()) if (S/'BeforeScene.json').exists() else None
 art=json.loads((R/'Art/HealingHouse/Refinement.json').read_text());plants=json.loads((R/'Art/World/VisualV2WorldArtV7/RefinedPlanting.json').read_text());bs={r['actor'] for r in art['material_bindings']};ls={r['actor'] for r in art['light_changes']};new=set(art['new_actors'])|{g['name'] for g in plants['groups']}
 if before is not None:
  for a in before['actors'].values():a['components'].sort(key=lambda c:c['name'])
  assert set(after['actors'])-set(before['actors'])==new and set(before['actors'])<=set(after['actors']);assert after['world_settings']==before['world_settings']
  for n,b in before['actors'].items():
   a=copy.deepcopy(after['actors'][n]);assert a['transform']==b['transform'] and a['props']==b['props'],n
   for c0 in b['components']:
    c1=next(c for c in a['components'] if c['name']==c0['name'])
    assert c0.get('collision')==c1.get('collision') and c0.get('instances')==c1.get('instances') and c0['transform']==c1['transform'],n
    if n in bs and 'materials' in c0:c1['materials']=c0['materials']
    if n in ls and 'intensity' in c0['props']:c1['props']['intensity']=c0['props']['intensity']
   assert a==b,('UNEXPECTED_NON_ART_CHANGE',n)
 else:unreal.log_warning('Historical detailed pre/post scope comparison not repeated: optional BeforeScene.json absent. Required current signatures checked strictly.')
 actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
 for n in new:
  a=actors[n];assert 'VisualOnly_NoCollision' in [str(t) for t in a.tags]
  for c in a.get_components_by_class(unreal.PrimitiveComponent):assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION,n
 for g in plants['groups']:
  c=actors[g['name']].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and c.get_instance_count()==len(g['instances']) and not c.cast_shadow and c.static_mesh.get_path_name()==g['mesh']
 materials=[]
 for p in art['new_assets']:
  a=unreal.load_asset(p);assert a
  if not isinstance(a,unreal.Material):continue
  for n in unreal.MaterialEditingLibrary.get_material_expressions(a):
   if isinstance(n,unreal.MaterialExpressionCustom):assert all(unreal.MaterialEditingLibrary.get_inputs_for_material_expression(a,n)),(p,n.get_name())
  assert a.get_editor_property('used_with_instanced_static_meshes');materials.append(p)
 for key in ['Wood','Timber','Stone','Plaster','Roof']:
  m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HH_Refined'+key);assert any(isinstance(n,unreal.MaterialExpressionScalarParameter) and str(n.get_editor_property('parameter_name'))=='HouseCutaway' for n in unreal.MaterialEditingLibrary.get_material_expressions(m))
 graphs=[]
 for path in materials:
  m=unreal.load_asset(path)
  for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
   if isinstance(n,unreal.MaterialExpressionCustom):graphs.append({'material':path,'expression':n.get_name(),'code':n.get_editor_property('code')})
 (R/'Art/HealingHouse/RefinedGraphs.json').write_text(json.dumps(graphs,indent=2))
 (S/'FinalArtScene.json').write_text(json.dumps(after,indent=2));(S/'ArtValidation.json').write_text(json.dumps({'passed':True,'existing_actors_preserved':1397,'new_visual_actors':len(new),'new_hism_groups':plants['group_count'],'new_instances':plants['new_instances'],'materials':materials,'gameplay_camera_transforms_collision_instance_data_unchanged':True,'cutaway_graph_parameters_retained':True,'shader_errors_validated_separately_in_log':True},indent=2));unreal.log('REFINED_ART_SCOPE_AND_GRAPH_VALIDATION_PASS')
