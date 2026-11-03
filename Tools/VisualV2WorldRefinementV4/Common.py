import unreal,json,math,random,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';ROOT='/Game/Environment/VisualV2WorldRefinementV4';ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py')));actors={a.get_actor_label():a for a in A.get_all_level_actors()};SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups={};changes=[];rng=random.Random(2601104)
def material(n):return unreal.load_asset(ROOT+'/Materials/M_WR4_'+n)
def group(key,path,ms=None,shadow=True,collision='NoCollision'):
 if key in groups:return groups[key]
 m=unreal.load_asset(path);assert m,path;a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WR4_'+key);a.set_folder_path('VisualV2/WorldRefinementV4');a.tags=['VisualV2WorldRefinementV4'];h,error=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,error;c.set_collision_profile_name(collision);c.set_cast_shadow(shadow);c.set_editor_property('generate_overlap_events',False)
 if ms:
  for i,v in enumerate(ms):c.set_material(i,unreal.load_asset(v)if isinstance(v,str)else v)
 c.set_static_mesh(m);groups[key]=c;return c
def centred(c,p,size,rotation=None):
 b=c.static_mesh.get_bounding_box();v=b.max-b.min;s=unreal.Vector(size[0]/v.x,size[1]/v.y,size[2]/v.z);rot=rotation or unreal.Rotator();offset=unreal.MathLibrary.transform_location(unreal.Transform(rotation=rot,scale=s),(b.min+b.max)*.5);t=unreal.Transform(location=unreal.Vector(*p)-offset,rotation=rot,scale=s);c.add_instance(t,True)
def save(name,extra=None):
 ds=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name().startswith((ROOT+'/', '/Game/Fab/VisualV2RefinementLocal/'))for p in ds),[p.get_path_name()for p in ds]
 for p in ds:assert unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(p.get_path_name()),False)
 assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');d=dict(changes=changes,groups=[dict(label=c.get_owner().get_actor_label(),count=c.get_instance_count(),mesh=c.static_mesh.get_path_name())for c in groups.values()]);d.update(extra or{});(D/name).write_text(json.dumps(d,indent=2))
