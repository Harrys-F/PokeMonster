"""Corrections from actual QHD review, limited to own trial derivatives/components."""
import unreal,json,math,random,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';ROOT='/Game/Environment/VisualV2FabAssetTrialV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);ML=unreal.MaterialEditingLibrary;assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();actors={a.get_actor_label():a for a in A.get_all_level_actors()}
def segment(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/max(1,dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
src=unreal.load_asset('/Game/Environment/PokemonAIV3/Meshes/SM_AIV3PondGround');mesh=unreal.load_asset(ROOT+'/Meshes/SM_FAT_StreamGround');dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,vs,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);old=unreal.GeometryScript_List.convert_vector_list_to_array(vs);new=[];count=0
for p in old:
 z=p.z;d=min(segment(p.x,p.y,(-910,-320),(1100,-320)),segment(p.x,p.y,(720,-320),(720,-680)))
 if z>-100 and d<61:w=max(0,min(1,(61-d)/25));z-=34*w*w*(3-2*w);count+=1
 new.append(unreal.Vector(p.x,p.y,z))
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(new));opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,mesh,opt,unreal.GeometryScriptMeshWriteLOD());assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
# Re-read the actual saved mesh; mutable Unreal Array values are copies, not references.
dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,ps,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);ps=unreal.GeometryScript_List.convert_vector_list_to_array(ps);nearest=min(ps,key=lambda p:p.x*p.x+(p.y+320)**2);assert nearest.z<-30,nearest
# Separate subdued leaf instance, leaving flower colours untouched.
q=ROOT+'/Materials/MI_FAT_Shrubs';mi=unreal.AssetToolsHelpers.get_asset_tools().create_asset('MI_FAT_Shrubs',ROOT+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());srcmi=unreal.load_asset(ROOT+'/Materials/MI_FAT_Flowers');ML.set_material_instance_parent(mi,srcmi.parent)
for prop in ['scalar_parameter_values','vector_parameter_values','texture_parameter_values']:mi.set_editor_property(prop,srcmi.get_editor_property(prop))
ML.set_material_instance_scalar_parameter_value(mi,'Texture Brightness',.75);ML.set_material_instance_vector_parameter_value(mi,'Custom Color',unreal.LinearColor(.06,.16,.025,1));assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False);actors['FAT_FabShrubs'].modify();actors['FAT_FabShrubs'].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent).set_material(0,mi)
# Rounded SimpleRocks silhouettes with the compatible local RockEnv surface.
replaced=[];rng=random.Random(261104)
for j in range(1,4):
 a=actors['FAT_Outcrop'+str(j)];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);trans=[c.get_instance_transform(i,True)for i in range(c.get_instance_count())];a.modify();c.clear_instances();source=unreal.load_asset('/Game/SimpleRocks/3D_Assets/Meshes/Rocks/SM_SimpleRock_'+['03A','11A','17A'][j-1]);c.set_material(0,unreal.load_asset('/Game/RockEnv_Pack/Instancials/Rock/MI_Rock_1'));c.set_static_mesh(source);b=source.get_bounding_box()
 for t in trans:
  p=t.translation
  # Keep all new round rocks at existing flat-earth sites; no perched cubes on test steps.
  x=p.x;y=p.y
  if y<1500 and x>-1550:x-=500;y+=160
  h=rng.uniform(55,105);sc=h/(b.max.z-b.min.z);t.translation=unreal.Vector(x,y,-b.min.z*sc-5);t.scale3d=unreal.Vector(sc,sc,sc);c.add_instance(t,True)
 replaced.append(dict(actor=a.get_actor_label(),mesh=source.get_path_name(),instances=c.get_instance_count()))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'No original material usage changes permitted';assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'Polish.json').write_text(json.dumps(dict(bed_vertices=count,actual_bed_vertex=nearest.to_tuple(),rounded_outcrops=replaced,foliage_tint='own shrub instance only'),indent=2))
