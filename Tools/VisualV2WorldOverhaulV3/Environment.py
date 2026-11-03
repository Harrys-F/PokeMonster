"""Whole-map geometry/surface pass. Originals never saved; gameplay actors untouched."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert not(D/'Environment.json').exists()
assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/Meshes/SM_WOV_Ground'),'Derived terrain already created; do not rerun'
# One map-local terrain derivative replaces the old box steps with smooth walkable land.
source=unreal.load_asset('/Game/Environment/VisualV2FabAssetTrialV1/Meshes/SM_FAT_StreamGround');mesh=unreal.EditorAssetLibrary.duplicate_asset(source.get_path_name(),ROOT+'/Meshes/SM_WOV_Ground');assert mesh;dm,_=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(source,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,ps,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);ps=unreal.GeometryScript_List.convert_vector_list_to_array(ps);new=[];edited=0
for p in ps:
 dz=height(p.x,p.y)if p.z>-100 else 0;new.append(unreal.Vector(p.x,p.y,p.z+dz));edited+=dz>.01
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(new));opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,mesh,opt,unreal.GeometryScriptMeshWriteLOD());mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);mesh.set_material(0,unreal.load_asset(ROOT+'/Materials/M_WOV_Ground'));assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);a=actors['V2_Ground'];a.modify();a.static_mesh_component.set_static_mesh(mesh);a.static_mesh_component.set_material(0,unreal.load_asset(ROOT+'/Materials/M_WOV_Ground'));changes.append(dict(actor=a.get_name(),label=a.get_actor_label(),kind='one continuous sculpted terrain and integrated whole-map surface'))
for name in ['Hill_Step_Low','Hill_Step_Mid','Hill_Lookout']:
 a=actors[name];a.modify();a.static_mesh_component.set_visibility(False);a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);changes.append(dict(actor=a.get_name(),label=name,kind='obsolete box step surface/collision replaced by continuous mound'))
# Surface bindings only; building silhouettes, doorways, interior logic and colliders unchanged.
for a in actors.values():
 label=a.get_actor_label()
 if not label.startswith(('V2_House_','V2_Cottage_','V2_Village_','V2_Archive_','V2_Fence_','FAT_Garden'))or a.get_editor_property('hidden'):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
  edits=[]
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   name=old.get_name().lower();target=None
   if any(w in name for w in ['roof','shingle']):target='Roof'
   elif any(w in name for w in ['timber','wood','oak','cedar']):target='Timber'
   elif any(w in name for w in ['plaster','ochre']):target='Plaster'
   elif any(w in name for w in ['stone','mortar','masonry']):target='Stone'
   if label in ['V2_House_Forecourt','V2_House_HH_Q2_OrganicApproach']:target='Cobbles'
   if target:a.modify();c.set_material(i,unreal.load_asset(ROOT+'/Materials/M_WOV_'+target));edits.append(dict(slot=i,before=old.get_path_name(),after=target))
  if edits:changes.append(dict(actor=a.get_name(),label=label,kind='map-local architectural surfaces',slots=edits))
for label,key in [('P2D_OrganicWater','Stream'),('P2D_Surface_Pond_Water','Pond')]:
 a=actors[label];a.modify();a.static_mesh_component.set_material(0,unreal.load_asset(ROOT+'/Materials/M_WOV_'+key));changes.append(dict(actor=a.get_name(),label=label,kind='same single water surface and depth, moving normal highlights'))
# Existing bridge: keep its exact walkable deck collision, avoid duplicate visible decks.
a=actors['VS_BridgeDeck'];a.modify();a.static_mesh_component.set_visibility(False);changes.append(dict(actor=a.get_name(),label=a.get_actor_label(),kind='retained exact 24cm collision deck, no duplicate rendered box'))
for label,a in actors.items():
 if not label.startswith('VS_Bridge')or label=='VS_BridgeDeck':continue
 a.modify();a.static_mesh_component.set_material(0,unreal.load_asset(ROOT+'/Materials/M_WOV_Timber'))
 if label.startswith('VS_BridgePlank'):p=a.get_actor_location();a.set_actor_location(unreal.Vector(p.x,p.y,21.75),False,False)
 if label.startswith('VS_BridgePost'):
  p=a.get_actor_location();s=a.get_actor_scale3d();mid=abs(p.y+320)<1;low=24 if mid else-8;high=113;a.set_actor_location(unreal.Vector(p.x,p.y,(low+high)/2),False,False);a.set_actor_scale3d(unreal.Vector(s.x,s.y,(high-low)/100))
 changes.append(dict(actor=a.get_name(),label=label,kind='bridge material, joined posts/plank elevation'))
def cube(label,p,scale,rot=None,collision=False):
 a=A.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*p),rot or unreal.Rotator());a.set_actor_label('WOV3_'+label);a.set_folder_path('VisualV2/WorldOverhaulV3');a.tags=['VisualV2WorldOverhaulV3'];c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));c.set_material(0,unreal.load_asset(ROOT+'/Materials/M_WOV_Timber'));a.set_actor_scale3d(unreal.Vector(*scale));c.set_collision_profile_name('BlockAll'if collision else'NoCollision');c.set_cast_shadow(True);return a
for x in [-416,-284]:cube('BridgeStringer_'+str(x),(x,-320,12),(2.24,.12,.14),unreal.Rotator(yaw=90))
for x in [-435.49,-264.51]:
 for ya,yb in [(-407.5,-320),(-232.5,-320)]:
  a=unreal.Vector(x,ya,29);b=unreal.Vector(x,yb,83);v=b-a;cube('BridgeBrace_'+str(x)+'_'+str(ya),((a+b)*.5).to_tuple(),(v.length()/100,.055,.065),unreal.MathLibrary.make_rot_from_x(v))
for side in [-1,1]:cube('BridgeApproach_'+str(side),(-350,-320+side*136,10.0),(1.50,.65,.045),unreal.Rotator(roll=-side*math.degrees(math.atan2(24,60))),True)
save('Environment.json',dict(terrain_vertices_edited=edited,mounds=mounds,bridge_span_cm=210,bridge_visible_top_cm=24,bridge_water_height_cm=4.4,bridge_floor_clearance_cm=19.6,building_floorplans_unchanged=True))
