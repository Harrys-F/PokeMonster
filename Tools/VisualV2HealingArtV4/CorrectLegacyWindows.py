"""Replace proven decorative primitive window pots, retain their original parts hidden."""
import unreal,json,sys,copy,shutil
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_HeilhausArt_V4_2026-10-19');E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'LegacyWindowCorrection.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(s):
 s=copy.deepcopy(s)
 for a in s['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return s
B=canon(scene(w));assert B==canon(json.loads((S/'AfterScene.json').read_text()));shutil.copy2(R/'Content/Maps/Dev_TestMap_VisualV2.umap',O/'Dev_TestMap_VisualV2_V4_BeforeLegacyWindows.umap');delta=json.loads((S/'Delta.json').read_text());changed=[];pots=[];hidden=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 label=a.get_actor_label()
 if not label.startswith('V2_House_HH_V3_WindowHerb_'):continue
 c=a.get_component_by_class(unreal.StaticMeshComponent);assert c and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow;row={'name':a.get_name(),'label':label,'mesh_before':c.static_mesh.get_path_name(),'materials_before':[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]}
 if label.endswith('_Pot'):
  assert c.static_mesh.get_path_name().startswith('/Engine/BasicShapes/Cylinder.');oldloc=a.get_actor_location();oldscale=a.get_actor_scale3d();row.update(location_before_cm=oldloc.to_tuple(),scale_before=oldscale.to_tuple());family=['FlowerPlant','TrailingHerb','NarrowHerb','BroadHerb'][int(label.split('_')[-2])];m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Meshes/SM_HA4_'+family);c.set_editor_property('override_materials',[]);assert c.set_static_mesh(m);assert a.set_actor_location(unreal.Vector(oldloc.x,oldloc.y,oldloc.z-6.48),False,True);a.set_actor_scale3d(unreal.Vector(.42,.42,.42));row.update(location_after_cm=a.get_actor_location().to_tuple(),scale_after=a.get_actor_scale3d().to_tuple(),family=family);pots.append(a.get_name())
 else:
  assert any(t in label for t in ['_Leaf','_Flower']) and c.static_mesh.get_path_name().startswith('/Engine/BasicShapes/Sphere.');c.set_visibility(False,False);row['legacy_component_retained_invisible']=True;hidden.append(a.get_name())
 row.update(mesh_after=c.static_mesh.get_path_name(),materials_after=[c.get_material(i).get_path_name() for i in range(c.get_num_materials())]);changed.append(row)
assert len(pots)==8 and len(hidden)==28,(len(pots),len(hidden));F=canon(scene(w));assert F['actors'].keys()==B['actors'].keys() and F['world_settings']==B['world_settings'];names=set(pots+hidden)
for name,old in B['actors'].items():
 current=F['actors'][name]
 if name not in names:assert current==old,name;continue
 test=copy.deepcopy(current)
 if name in pots:
  assert test['label']==old['label'];test['transform']=old['transform']
  for oc,nc in zip(old['components'],test['components']):nc['transform']=oc['transform'];nc['materials']=oc['materials'];nc['props']['static_mesh']=oc['props']['static_mesh']
 else:
  for oc,nc in zip(old['components'],test['components']):nc['props']['visible']=oc['props']['visible']
 assert test==old,name
(S/'LegacyWindowCorrection.json').write_text(json.dumps({'replaced_pot_actors':pots,'retained_hidden_leaf_flower_actors':hidden,'changes':changed,'source':'Tools/DressHealingHouseV3.py pot/WindowHerb purely decorative, no collision or shadows.','runtime_visibility':'BuildingCutaway changes Actor hidden state only; retained component visibility false persists.'},indent=2));delta['changed']+=changed;delta['legacy_window_pots_replaced']=8;delta['legacy_primitive_parts_retained_hidden']=28;delta['existing_actors_unchanged']-=36;(S/'Delta.json').write_text(json.dumps(delta,indent=2));(R/'Art/World/VisualV2HealingArtV4/Scope.json').write_text(json.dumps(delta,indent=2));(S/'CandidateScene.json').write_text(json.dumps(scene(w),indent=2));unreal.log('HA4_LEGACY_WINDOW_DECORATION_CORRECTED')
