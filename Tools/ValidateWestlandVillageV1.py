"""Read-only Village Core V1 saved-map, modular-asset and collision audit.
Run in the full editor with Dev_WestlandVillage loaded and PIE stopped.
Writes only local ignored Saved/WestlandVillage/Validation.json evidence.
"""
import unreal,json,math
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'Saved/WestlandVillage';R.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'Art/World/Westland/WestlandVillage_V1.json').read_text())
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not editor.get_game_world()
w=editor.get_editor_world();assert w.get_name()=='Dev_WestlandVillage'
allactors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in allactors}
kit=[]
for name in ('WestlandBuildingKit_V1.json','WestlandBuildingKit_InnExtensions_V1.json'):kit+=json.loads((ROOT/'Art/Architecture/Westland'/name).read_text())['modules']
ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);mats=set();asset_checks=[]
for item in kit:
 path='/Game/Environment/Architecture/Westland/Meshes/'+item['category']+'/'+item['mesh'];m=unreal.load_asset(path);assert m,path
 b=m.get_bounding_box()
 for i,(lo,hi) in enumerate(zip((b.min.x,b.min.y,b.min.z),(b.max.x,b.max.y,b.max.z))):assert abs(lo-item['min_m'][i]*100)<.3 and abs(hi-item['max_m'][i]*100)<.3
 count=ss.get_simple_collision_count(m)+ss.get_convex_collision_count(m);assert count==len(item['collision_boxes']),(path,count)
 for slot in m.get_editor_property('static_materials'):
  mat=slot.get_editor_property('material_interface');assert mat and mat.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED;mats.add(mat.get_path_name())
 asset_checks.append({'name':item['name'],'triangles':m.get_num_triangles(0),'collision_bodies':count})

def wp(b,p):
 c,s=math.cos(math.radians(b['yaw'])),math.sin(math.radians(b['yaw']))
 return [b['origin_cm'][0]+p[0]*c-p[1]*s,b['origin_cm'][1]+p[0]*s+p[1]*c,b['origin_cm'][2]+(p[2] if len(p)>2 else 50)]
ground=by['WV_MeadowTerrain'];ignore=[ground]+[a for a in allactors if isinstance(a,unreal.Pawn)]
def sweep(a,b):
 return unreal.SystemLibrary.capsule_trace_single_for_objects(w,unreal.Vector(*a),unreal.Vector(*b),28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,ignore,unreal.DrawDebugTrace.NONE,True)
def free(a,b):assert sweep(a,b) is None,('blocked capsule',a,b)
def block(a,b):assert sweep(a,b) is not None,('nonblocking wall',a,b)
checked=[]
for b in data['buildings']:
 placed=[a for a in allactors if a.actor_has_tag('WV_Building_'+b['id'])]
 actual=Counter(next(str(t).removeprefix('WV_Module_') for t in a.tags if str(t).startswith('WV_Module_')) for a in placed)
 assert actual==b['module_counts'],b['id']
 for i,entry in enumerate(b['placements']):
  a=by['WV_'+b['id']+'_'+str(i).zfill(3)+'_'+entry['module']];v=a.get_actor_location();expected=wp(b,[p*100 for p in entry['position_m']]);assert all(abs(vv-ee)<.01 for vv,ee in zip((v.x,v.y,v.z),expected));assert a.get_actor_scale3d()==unreal.Vector(1,1,1)
 cut=by['WV_'+b['id']+'_Cutaway'];assert cut.get_editor_property('use_interior_camera')
 assert abs(cut.get_editor_property('fade_duration')-.4)<1e-6;assert cut.get_editor_property('interior_camera_distance')==b['camera_distance_cm']
 assert len(cut.get_editor_property('occluding_actors'))==sum(p['cutaway'] for p in b['placements'])
 assert all(a.actor_has_tag('WV_Occluder') for a in cut.get_editor_property('occluding_actors'))
 threshold=cut.get_editor_property('door_threshold').get_unscaled_box_extent();assert threshold==unreal.Vector(20,b['door_m'][0]*50,b['door_m'][1]*50)
 door=b['door_local_cm'];x,y=door[:2]
 free(wp(b,(x-130,y,50)),wp(b,(x+130,y,50)))
 free(wp(b,(x-75,y-60,50)),wp(b,(x+75,y+60,50)))
 free(wp(b,(x+85,y,50)),wp(b,(0,y,50)))
 # Solid front away from the door and both side walls remain real obstacles.
 h=b['body_m'][1]*50;d=b['body_m'][0]*50
 side_y=-h+80 if abs(y-(-h+80))>150 else h-80
 block(wp(b,(x-100,side_y,50)),wp(b,(x+100,side_y,50)))
 block(wp(b,(0,-h-80,50)),wp(b,(0,-h+80,50)))
 if b['kind']=='Inn':
  assert len(cut.get_editor_property('interior_regions'))==2
  for a,z in [((0,100,50),(240,250,50)),((240,250,50),(400,200,50)),((400,200,50),(430,300,50)),((430,300,50),(420,-100,50))]:free(wp(b,a),wp(b,z))
  block(wp(b,(60,-230,50)),wp(b,(150,-230,50)))
 assert not cut.is_viewer_inside(unreal.Vector(*wp(b,(x-6,y,50))))
 assert cut.is_viewer_inside(unreal.Vector(*wp(b,(x+6,y,50))))
 checked.append({'id':b['id'],'modules':len(placed),'occluders':len(cut.get_editor_property('occluding_actors')),'straight_and_diagonal_door_sweeps':True,'front_and_side_wall_collision':True,'interior_distance_cm':b['camera_distance_cm']})
# Floor coverage across all named path control points, including entrance and reserve.
height_samples=[]
for path in data['paths']:
 for p in path['points']:
  hit=unreal.SystemLibrary.line_trace_single_for_objects(w,unreal.Vector(p[0],p[1],150),unreal.Vector(p[0],p[1],-150),[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,[],unreal.DrawDebugTrace.NONE,True)
  assert hit,(path['id'],p);height_samples.append({'path':path['id'],'point':p[:2]})
material_slots=0;used_assets=set()
for a in allactors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh;assert m,(a.get_actor_label(),'no mesh');used_assets.add(m.get_path_name())
  for i in range(c.get_num_materials()):assert c.get_material(i),(a.get_actor_label(),'missing material',i);material_slots+=1
 for c in a.get_components_by_class(unreal.PaperSpriteComponent):
  assert c.get_sprite(),a.get_actor_label();used_assets.add(c.get_sprite().get_path_name());assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
terrain=ground.static_mesh_component.static_mesh
assert terrain.get_num_triangles(0)==9800 and ss.is_section_collision_enabled(terrain,0,0)
assert terrain.get_editor_property('body_setup').get_editor_property('collision_trace_flag')==unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
# Verify the generated transparent path graph, including unnamed ComponentMask pins.
mat=unreal.load_asset('/Game/Environment/WestlandVillage/Materials/M_WV_Path');lib=unreal.MaterialEditingLibrary
for e in unreal.ObjectIterator(unreal.MaterialExpressionComponentMask):
 if e.get_outer()==mat:assert all(lib.get_inputs_for_material_expression(mat,e))
assert lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_OPACITY)
assert len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway')))==5
assert len(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PlayerStart))==1
(R/'Validation.json').write_text(json.dumps({'passed':True,'map':w.get_name(),'kit_meshes':asset_checks,'existing_materials':sorted(mats),'buildings':checked,'architecture_instances':sum(b['modules'] for b in checked),'terrain_height_checks':len(height_samples),'material_slots':material_slots,'unique_referenced_visual_assets':sorted(used_assets),'terrain_triangles':9800,'terrain_complex_collision':True,'missing_assets':0,'new_kit_modules':0},indent=2)+'\n')
unreal.log('WV_VALIDATION_PASSED')
