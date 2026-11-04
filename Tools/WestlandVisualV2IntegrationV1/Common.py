"""Bounded saved-map authoring, never a runtime dependency."""
import unreal,json,math,random,sys,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';ROOT='/Game/Environment/WestlandVisualV2IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();actors={a.get_actor_label():a for a in A.get_all_level_actors()};SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
rng=random.Random(41107);groups={}
def component(a,cls):
 h,error=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=cls,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,error;return c
def own(label,cls=unreal.Actor,location=unreal.Vector()):
 label='WVI_'+label;assert label not in actors,'Already migrated; never duplicate';a=A.spawn_actor_from_class(cls,location);a.set_actor_label(label);a.tags=['WestlandVisualV2IntegrationV1'];a.set_folder_path('WestlandRegion/VisualV2IntegrationV1');actors[label]=a;return a
def group(label,mesh,materials,shadow=False,cull=0):
 a=own(label);c=component(a,unreal.HierarchicalInstancedStaticMeshComponent)
 for i,m in enumerate(materials):c.set_material(i,unreal.load_asset(m)if isinstance(m,str)else m)
 c.set_static_mesh(unreal.load_asset(mesh)if isinstance(mesh,str)else mesh);assert c.static_mesh;c.set_collision_profile_name('NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_editor_property('affect_distance_field_lighting',shadow)
 if cull:c.set_cull_distances(int(cull*.85),cull)
 groups[label]=c;return c
def finish(name,data):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Never save an auto-edited original';assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/name).write_text(json.dumps(data,indent=2))
