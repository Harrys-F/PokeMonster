"""Import only new starter namespaces, each with its own skeleton. Never reimport an original asset."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterExpansionV1';assert not(O/'ImportModels.json').exists();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();W=E.get_editor_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[];rows=[]
def save(o,namespace):
 assert o.get_path_name().startswith(namespace+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(o,False);created.append(o.get_path_name());return o
def create(name,folder,cls,factory):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name),folder+'/'+name
 a=T.create_asset(name,folder,cls,factory);assert a;return a
def task(source,folder,name,options=None):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name)
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(source),destination_path=folder,destination_name=name,automated=True,save=False,replace_existing=False).items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);return list(t.get_objects())
def data(name,folder,cls):
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',cls);return create(name,folder,cls,f)
def node(m,cls,**props):
 n=L.create_material_expression(m,cls)
 for k,v in props.items():n.set_editor_property(k,v)
 return n
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 for species,height,walk,run,family in [('Schiggy',50.,26.,50.,unreal.PokeMonsterCreatureRigFamily.BIPED),('Bisasam',70.,32.,72.,unreal.PokeMonsterCreatureRigFamily.QUADRUPED)]:
  P='/Game/Characters/Creatures/'+species+'/MeshyV1';A=R/'Art/Characters/Creatures'/species;textures={}
  for typ in ['BaseColor','Normal','MetallicRoughness']:
   a=next(x for x in task(A/'Textures/MeshyV1'/(species+'_'+typ+'.jpg'),P+'/Textures','T_'+species+'_'+typ)if isinstance(x,unreal.Texture2D));a.set_editor_property('srgb',typ=='BaseColor')
   if species=='Schiggy'and typ=='BaseColor':a.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
   if typ=='Normal':a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);a.set_editor_property('flip_green_channel',True)
   elif typ=='MetallicRoughness':a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
   textures[typ]=save(a,P)
  material=create('M_'+species,P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());material.set_editor_property('two_sided',True);material.set_editor_property('used_with_skeletal_mesh',True)
  for typ,sampler,channels in [('BaseColor',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR,[('RGB',unreal.MaterialProperty.MP_BASE_COLOR)]),('Normal',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,[('RGB',unreal.MaterialProperty.MP_NORMAL)]),('MetallicRoughness',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS,[('G',unreal.MaterialProperty.MP_ROUGHNESS),('B',unreal.MaterialProperty.MP_METALLIC)])]:
   sample=node(material,unreal.MaterialExpressionTextureSample,texture=textures[typ],sampler_type=sampler)
   for channel,prop in channels:assert L.connect_material_property(sample,channel,prop)
  L.recompile_material(material);save(material,P)
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
  mesh=next(x for x in task(A/'Exports/MeshyV1'/(species+'_Idle.fbx'),P+'/Meshes','SK_'+species+'_Meshy',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials)
  for slot in slots:slot.material_interface=material
  mesh.materials=slots;save(sk,P);save(mesh,P);clips={}
  for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
   ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
   clip=next(x for x in task(A/'Exports/MeshyV1'/(species+'_'+role+'.fbx'),P+'/Animations','A_'+species+'_'+role,ui)if isinstance(x,unreal.AnimSequence));dest=P+'/Animations/A_'+species+'_'+role
   if clip.get_path_name().split('.')[0]!=dest:assert not unreal.EditorAssetLibrary.does_asset_exist(dest);assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
   clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip,P)
  profile=data('DA_'+species+'_Presentation',P,unreal.PokeMonsterCreaturePresentationData)
  for k,v in dict(mesh=mesh,clips=clips,walk_speed=walk,run_speed=run,ground_offset_cm=0.,rig_family=family,reference_size_cm=height,size_source='https://www.serebii.net/pokedex-gs/'+('007'if species=='Schiggy'else'001')+'.shtml',effect_anchors=[]).items():profile.set_editor_property(k,v)
  assert not profile.get_validation_errors(),list(profile.get_validation_errors());save(profile,P);rows.append({'species':species,'profile':profile.get_path_name(),'skeleton':sk.get_path_name(),'height_cm':height,'clips':len(clips),'material_slots':len(slots),'ground_offset_cm':0.})
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
# Only verified, currently supported Gen-2 moves. No inert placeholder effects.
moves={}
for name,german,typ,cat,power,accuracy,pp in [('Tackle','Tackle',unreal.PokeMonsterCreatureType.NORMAL,unreal.PokeMonsterMoveCategory.PHYSICAL,35,95,35),('VineWhip','Rankenhieb',unreal.PokeMonsterCreatureType.GRASS,unreal.PokeMonsterMoveCategory.SPECIAL,35,100,10),('WaterGun','Aquaknarre',unreal.PokeMonsterCreatureType.WATER,unreal.PokeMonsterMoveCategory.SPECIAL,40,100,25)]:
 m=data('DA_'+name,'/Game/Data/Moves',unreal.PokeMonsterMoveData)
 for k,v in dict(internal_id=name,display_name=german,type=typ,category=cat,base_power=power,accuracy=accuracy,max_pp=pp,priority=0).items():m.set_editor_property(k,v)
 moves[name]=save(m,'/Game/Data')
moves['Growl']=unreal.load_asset('/Game/Data/Moves/DA_Growl');assert moves['Growl']
for row in rows:
 name=row['species'];water=name=='Schiggy';s=data('DA_'+name,'/Game/Data/Creatures',unreal.PokeMonsterCreatureSpeciesData);stats=[44,48,65,50,64,43]if water else[45,49,49,65,65,45];profile=unreal.load_asset(row['profile'])
 for k,v in dict(internal_id=name,display_name=name,pokedex_number=7 if water else 1,base_capture_rate=45,primary_type=unreal.PokeMonsterCreatureType.WATER if water else unreal.PokeMonsterCreatureType.GRASS,secondary_type=unreal.PokeMonsterCreatureType.NONE if water else unreal.PokeMonsterCreatureType.POISON,base_stats=unreal.PokeMonsterCreatureBaseStats(**dict(zip(['hp','attack','defense','special_attack','special_defense','speed'],stats))),gender=unreal.PokeMonsterGenderData(system=unreal.PokeMonsterGenderSystem.MIXED,female_ratio=.125),starting_level=13 if water else 10,growth_rate=unreal.PokeMonsterGrowthRate.MEDIUM_SLOW,base_experience_yield=66 if water else 64,visuals=unreal.PokeMonsterCreatureVisuals(presentation=profile)).items():s.set_editor_property(k,v)
 levels=[(1,'Tackle'),(13,'WaterGun')]if water else[(1,'Tackle'),(4,'Growl'),(10,'VineWhip')];s.set_editor_property('level_up_moves',[unreal.PokeMonsterLevelMove(level=l,move=moves[m])for l,m in levels]);save(s,'/Game/Data');wild=data('DA_'+name+'_Wild','/Game/Data/Encounters',unreal.PokeMonsterEncounterProfile);level=13 if water else 10;wild.set_editor_property('entries',[unreal.PokeMonsterWildEncounterEntry(species=s,min_level=level,max_level=level,weight=1)]);save(wild,'/Game/Data');row['species_asset']=s.get_path_name();row['wild_profile']=wild.get_path_name();row['initial_level']=level;row['implemented_level_moves']=levels
assert str(unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf').get_internal_id())=='Zunderlauf';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(O/'ImportModels.json').write_text(json.dumps({'assets':created,'models':rows,'no_existing_assets_changed':True,'no_map_saved':True},indent=2));unreal.log('STARTER_MODELS_IMPORTED')
