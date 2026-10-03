"""Non-mutating editor audit: modular reuse, saved collision, materials/routes.
Run after import in the full editor. Reports live checks under ignored Saved/.
"""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandKitV1'
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());layout=json.loads((ART/'Buildings/WL_Cottage_V1.json').read_text())
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not editor.get_game_world(), 'Stop PIE before this saved-asset/editor-physics audit.'
world=editor.get_editor_world()
assert 'Dev_BuildingKitTestMap' in world.get_name(),world.get_name()
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);assert sm
counts={};materials=0
for m in kit['modules']:
 mesh=unreal.load_asset('/Game/Environment/Architecture/Westland/Meshes/'+m['category']+'/'+m['mesh']);assert mesh
 n=sm.get_simple_collision_count(mesh)+sm.get_convex_collision_count(mesh);counts[m['name']]=n
 assert n==len(m['collision_boxes']),(m['name'],n,m['collision_boxes'])
 for slot in mesh.get_editor_property('static_materials'):
  mat=slot.get_editor_property('material_interface');assert mat
  assert mat.get_editor_property('blend_mode')==unreal.BlendMode.BLEND_MASKED
  materials+=1
placed=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor) if a.actor_has_tag('Westland_Cottage')]
assert len(placed)==len(layout['placements'])
actual={m['name']:sum(a.actor_has_tag('Westland_Module_'+m['name']) for a in placed) for m in kit['modules']}
assert actual==layout['module_counts']
ignore=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Pawn)
def trace(a,b):
 return unreal.SystemLibrary.capsule_trace_single_for_objects(world,unreal.Vector(*a),unreal.Vector(*b),28,48,[unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1],False,ignore,unreal.DrawDebugTrace.NONE,True) is not None
route=[(-950,0,50),(-400,0,50),(-250,0,50),(0,100,50),(200,200,50),(200,-200,50),(-200,-200,50),(-250,0,50),(-400,0,50)]
for i in range(1,len(route)):assert not trace(route[i-1],route[i]),('blocked route',i)
assert not trace((-400,-35,50),(-230,35,50)),'diagonal door'
assert trace((-450,200,50),(-200,200,50)),'front wall must block'
assert trace((200,0,50),(350,0,50)),'rear wall must block'
assert trace((0,-200,50),(0,-400,50)),'window sill wall must block'
cut=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Script/PokeMonster.PokeMonsterBuildingCutaway'))[0]
assert cut.get_editor_property('door_threshold').get_unscaled_box_extent()==unreal.Vector(20,65,100)
assert abs(cut.get_editor_property('fade_duration')-.4)<1e-6
assert not cut.is_viewer_inside(unreal.Vector(-330,0,50)) and cut.is_viewer_inside(unreal.Vector(-250,0,50))
assert cut.get_editor_property('use_interior_camera')
assert cut.get_editor_property('interior_camera_distance')==2000
assert cut.get_editor_property('interior_camera_pitch')==-50
bylabel={a.get_actor_label():a for a in placed}
assert set(cut.get_editor_property('occluding_actors'))=={bylabel[p['label']] for p in layout['placements'] if p['cutaway']}
assert not any(p['cutaway'] for i,p in enumerate(layout['placements']) if i in list(range(56,80))+[82,83,88,89,90,91,92,93,94,95,144]), 'Both side walls and their framing remain visible'
assert all(not p['cutaway'] for p in layout['placements'] if p['module']=='WallSolid2m' and p['label'] not in {'Cottage_WallSolid2m_056','Cottage_WallSolid2m_060','Cottage_WallSolid2m_068','Cottage_WallSolid2m_070','Cottage_WallSolid2m_072'}), 'Rear wall remains visible'
(OUT/'RuntimeValidation.json').write_text(json.dumps({'passed':True,'world':world.get_name(),'collision_bodies':counts,'material_slots_checked':materials,'reuse_counts':actual,'free_capsule_route_segments':8,'diagonal_door_sweep':True,'front_rear_window_blocking':True,'cutaway_config':[40,130,200,.4],'interior_camera':[2000,-50,0,35], 'camera_opt_in':True},indent=2)+'\n')
unreal.log('WESTLAND_RUNTIME_VALIDATION_PASSED')
