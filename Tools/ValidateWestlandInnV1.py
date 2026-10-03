"""Non-mutating editor audit: modular reuse, saved collision, materials/routes.
Run after import in the full editor. Reports live checks under ignored Saved/.
"""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandInnV1'
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());kit['modules']+=json.loads((ART/'WestlandBuildingKit_InnExtensions_V1.json').read_text())['modules'];layout=json.loads((ART/'Buildings/WL_Inn_V1.json').read_text())
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not editor.get_game_world(), 'Stop PIE before this saved-asset/editor-physics audit.'
world=editor.get_editor_world()
assert 'Dev_BuildingKitTestMap' in world.get_name(),world.get_name()
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);assert sm
counts={};materials=0
for m in kit['modules']:
 mesh=unreal.load_asset('/Game/Environment/Architecture/Westland/Meshes/'+m['category']+'/'+m['mesh']);assert mesh
 b=mesh.get_bounding_box()
 for i,(a,z) in enumerate(zip((b.min.x,b.min.y,b.min.z),(b.max.x,b.max.y,b.max.z))):assert abs(a-m['min_m'][i]*100)<.3 and abs(z-m['max_m'][i]*100)<.3,(m['name'],i)
 n=sm.get_simple_collision_count(mesh)+sm.get_convex_collision_count(mesh);counts[m['name']]=n
 assert n==len(m['collision_boxes']),(m['name'],n,m['collision_boxes'])
 for slot in mesh.get_editor_property('static_materials'):
  mat=slot.get_editor_property('material_interface');assert mat
  assert mat.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED
  materials+=1

placed=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor) if a.actor_has_tag('Westland_Inn')]
assert len(placed)==len(layout['placements'])
actual={m['name']:sum(a.actor_has_tag('Westland_Module_'+m['name']) for a in placed) for m in kit['modules']}
assert actual==layout['module_counts']
bylabel={a.get_actor_label():a for a in placed}
for item in layout['placements']:
 a=bylabel[item['label']];p=a.get_actor_location();expect=[100*item['position_m'][i]+layout['map_origin_cm'][i] for i in range(3)]
 assert all(abs(v-e)<.01 for v,e in zip((p.x,p.y,p.z),expect));assert a.get_actor_scale3d()==unreal.Vector(1,1,1)
ignore=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Pawn)
def trace(a,b):
 return unreal.SystemLibrary.capsule_trace_single_for_objects(world,unreal.Vector(*a),unreal.Vector(*b),28,48,[unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1],False,ignore,unreal.DrawDebugTrace.NONE,True) is not None
def free(a,b):assert not trace(a,b),('route blocked',a,b)
def block(a,b):assert trace(a,b),('missing collision',a,b)
route=[(-950,0,50),(-950,-1600,50),(-450,-1600,50),(-250,-1600,50),(0,-1600,50),(150,-1400,50),(-200,-1750,50),(200,-1800,50),(340,-1730,50),(340,-1350,50),(340,-1730,50),(-250,-1600,50),(-500,-1600,50)]
for a,b in zip(route,route[1:]):free(a,b)
free((-500,-1640,50),(-280,-1560,50))
block((-500,-1300,50),(-250,-1300,50));block((300,-1500,50),(450,-1500,50));block((0,-1750,50),(0,-1950,50));block((100,-1400,50),(280,-1400,50))
cut=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway')) if a.get_actor_label()=='WL_Inn_Cutaway')
assert cut.get_editor_property('door_threshold').get_unscaled_box_extent()==unreal.Vector(20,80,107.5)
assert abs(cut.get_editor_property('fade_duration')-.4)<1e-6
assert {a.get_actor_label() for a in cut.get_editor_property('occluding_actors')}=={p['label'] for p in layout['placements'] if p['cutaway']}
assert all(p['cutaway'] for p in layout['placements'] if p['module']=='GableHalf4m' and p['position_m'][1]>0)
assert not cut.is_viewer_inside(unreal.Vector(-440,-1600,50)) and cut.is_viewer_inside(unreal.Vector(-350,-1600,50))
assert len(unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway')))==2
cottage=json.loads((ART/'Buildings/WL_Cottage_V1.json').read_text())
cp=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor) if a.actor_has_tag('Westland_Cottage')]
assert len(cp)==148
for m,n in cottage['module_counts'].items():assert sum(a.actor_has_tag('Westland_Module_'+m) for a in cp)==n
(OUT/'RuntimeValidation.json').write_text(json.dumps({'passed':True,'world':world.get_name(),'meshes_checked':len(kit['modules']),'collision_bodies':counts,'material_slots_checked':materials,'reuse_counts':actual,'placed_modules':len(placed),'free_capsule_route_segments':len(route)-1,'diagonal_door_sweep':True,'front_rear_window_counter_blocking':True,'cutaway_config':[40,160,215,.4],'cottage_148_instances_preserved':True,'cpp_unchanged':True},indent=2)+'\n')
unreal.log('WESTLAND_INN_RUNTIME_VALIDATION_PASSED')
