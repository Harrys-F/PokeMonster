"""One-time VisualV2 authoring: derived floor/water/materials, same-sized pond.
No shared or original assets are edited. Requires a clean owned editor. The
serialized habitat centers in DefaultPokeMonsterHabitats.ini must match this tool.
"""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world()
assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not(D/'PondSeparated.json').exists()
folder='/Game/Environment/PokemonAIV3';names=['SM_AIV3PondGround','SM_AIV3PondWater'];tasks=[]
assert all(not unreal.EditorAssetLibrary.does_asset_exist(folder+'/Meshes/'+n)for n in names)
import_fbx=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX')
unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
for name in names:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
 for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,generate_lightmap_u_vs=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/'Art/World/PokemonAIV3/Exports'/(name+'.fbx')),destination_path=folder+'/Meshes',destination_name=name,automated=True,save=False,replace_existing=False,options=ui).items():task.set_editor_property(k,v)
 tasks.append(task)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(import_fbx))
materials=[]
for name in ['M_V2PondWater','M_V2RiverConnection']:
 target=folder+'/Materials/'+name.replace('V2','AIV3');assert not unreal.EditorAssetLibrary.does_asset_exist(target)
 material=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2PokemonWaterTeamV1/Materials/'+name,target);assert material;changed=0
 for expression in unreal.MaterialEditingLibrary.get_material_expressions(material):
  if isinstance(expression,unreal.MaterialExpressionCustom):
   code=expression.get_editor_property('code')
   if 'float2(720,-1000)'in code:expression.set_editor_property('code',code.replace('float2(720,-1000)','float2(720,-1800)'));changed+=1
 assert changed==1,(name,changed)
 unreal.MaterialEditingLibrary.recompile_material(material);assert unreal.EditorAssetLibrary.save_loaded_asset(material,False);materials.append(material)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in actors};g=by['V2_Ground'];water=by['P2D_Surface_Pond_Water'];barrier=by['VS_WaterBlockPond'];groundmat=g.static_mesh_component.get_material(0)
for name,mat in zip(names,[groundmat,materials[0]]):
 mesh=unreal.load_asset(folder+'/Meshes/'+name);assert mesh;mesh.set_material(0,mat)
 if name==names[0]:mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
g.static_mesh_component.set_static_mesh(unreal.load_asset(folder+'/Meshes/'+names[0]));g.set_actor_transform(unreal.Transform(),False,False)
water.static_mesh_component.set_static_mesh(unreal.load_asset(folder+'/Meshes/'+names[1]));water.static_mesh_component.set_material(0,materials[0]);water.set_actor_transform(unreal.Transform(),False,False);water.set_actor_hidden_in_game(False);water.static_mesh_component.set_hidden_in_game(False);water.static_mesh_component.set_visibility(True)
by['P2D_OrganicWater'].static_mesh_component.set_material(0,materials[1])
assert 'Cylinder'in barrier.static_mesh_component.static_mesh.get_path_name()
barrier.set_actor_location(unreal.Vector(720,-1800,100),False,False)
def radial(x,y):return math.hypot((x-720)/900,(y+1800)/650)
def bank(x,y,extra=0):
 dx,dy=(x-720)/900,(y+1800)/650;length=math.hypot(dx,dy)
 if length<.001:dx,dy,length=1,0,1
 return 720+900*dx/length*(1.13+extra),-1800+650*dy/length*(1.13+extra)
changes=[];instances=[]
for a in actors:
 if a in [g,water,barrier]or a.get_actor_label().startswith('VS_WaterBlock'):continue
 components=a.get_components_by_class(unreal.InstancedStaticMeshComponent)
 for c in components:
  for i in range(c.get_instance_count()):
   transform=c.get_instance_transform(i,True);x,y,z=transform.translation.to_tuple()
   if radial(x,y)<1.08:
    nx,ny=bank(x,y,(i%7)*.019);transform.translation=unreal.Vector(nx,ny,z);assert c.update_instance_transform(i,transform,True,True,True)
    instances.append({'actor':a.get_actor_label(),'component':c.get_name(),'index':i,'before':[x,y,z],'after':[nx,ny,z]})
 if components:continue
 name=a.get_actor_label();x,y,z=a.get_actor_location().to_tuple()
 if name.startswith(('V2_Tree_','V2_Bush_','V2_Stone_'))and radial(x,y)<1.16:
  nx,ny=bank(x,y,.20 if 'Tree'in name else(len(changes)%5)*.025)
  changes.append({'actor':name,'before':[x,y,z],'after':[nx,ny,z]});a.set_actor_location(unreal.Vector(nx,ny,z),False,False)
# Align only matching legacy collision helpers with the explicit relocated art.
helpers=[];seen=set()
for row in changes:
 original=row['actor'].split('_P2D_',1)[1];before=row['before'];after=row['after'];aliases=[original]
 if original.endswith('_Trunk'):aliases=[x for x in by if x.startswith(original[:-6]+'_')]
 elif original.endswith('Trunk'):aliases=[x for x in by if x.startswith(original[:-5])]
 for name in aliases:
  if name not in by or name in seen:continue
  a=by[name];old=a.get_actor_location();assert (old.x-before[0])**2+(old.y-before[1])**2<250**2,(name,old,before)
  new=unreal.Vector(after[0],after[1],old.z);a.set_actor_location(new,False,False);seen.add(name);helpers.append({'actor':name,'before':old.to_tuple(),'after':new.to_tuple()})
assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
(D/'PondSeparated.json').write_text(json.dumps({'center':[720,-1800],'size_cm':[1800,1300],'depth_cm':424.2,'dry_gap_cm':406,'water_z':4.2,'decorations':changes,'instances':instances,'collision_helpers':helpers,'materials':[x.get_path_name()for x in materials]},indent=2))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
