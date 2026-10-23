"""Import one explicitly reviewed new species namespace, each with its own skeleton. Never reimport an original asset."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/GlutexoEvolutionV2';request=json.loads((O/'ImportRequest.json').read_text());name=request['species'];specs=json.loads((R/'Tools/GlutexoEvolutionV2/Species.json').read_text());spec=specs[name];audit=json.loads((R/'Art/Characters/Creatures'/name/'MeshyV1_ModelAudit.json').read_text());assert not(O/('Import'+name+'.json')).exists();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();W=E.get_editor_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[];rows=[]
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
 for species,height,walk,run,family in [(name,spec['height'],audit['walk_speed_m_s']*100,audit['run_speed_m_s']*100,getattr(unreal.PokeMonsterCreatureRigFamily,audit['rig_family'].upper()))]:
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
  flame_material=None
  if name=='Glutexo':
   assert len(slots)==2;flame_material=create('M_Glutexo_OriginalTailFlame',P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());flame_material.set_editor_property('two_sided',True);flame_material.set_editor_property('used_with_skeletal_mesh',True)
   color=node(flame_material,unreal.MaterialExpressionTextureSample,texture=textures['BaseColor'],sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);assert L.connect_material_property(color,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
   glow=node(flame_material,unreal.MaterialExpressionMultiply,const_b=.35);assert L.connect_material_expressions(color,'RGB',glow,'A');assert L.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
   rough=node(flame_material,unreal.MaterialExpressionConstant,r=.8);assert L.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);L.recompile_material(flame_material);save(flame_material,P)
  for index,slot in enumerate(slots):slot.material_interface=flame_material if flame_material and index==1 else material
  mesh.materials=slots;save(sk,P);save(mesh,P);clips={}
  for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
   ui=unreal.FbxImportUI()
   for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
   for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
   clip=next(x for x in task(A/'Exports/MeshyV1'/(species+'_'+role+'.fbx'),P+'/Animations','A_'+species+'_'+role,ui)if isinstance(x,unreal.AnimSequence));dest=P+'/Animations/A_'+species+'_'+role
   if clip.get_path_name().split('.')[0]!=dest:assert not unreal.EditorAssetLibrary.does_asset_exist(dest);assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
   clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip,P)
  profile=data('DA_'+species+'_Presentation',P,unreal.PokeMonsterCreaturePresentationData)
  for k,v in dict(mesh=mesh,clips=clips,walk_speed=walk,run_speed=run,ground_offset_cm=-12. if name=='Nebulak'else 0.,rig_family=family,reference_size_cm=height,size_source=spec['source'],effect_anchors=[]).items():profile.set_editor_property(k,v)
  assert not profile.get_validation_errors(),list(profile.get_validation_errors());save(profile,P);rows.append({'species':species,'profile':profile.get_path_name(),'skeleton':sk.get_path_name(),'height_cm':height,'clips':len(clips),'material_slots':len(slots),'ground_offset_cm':0.})
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))

# Resolve existing productive move assets by stable ID; never create parallel moves.
moves={}
for path in unreal.EditorAssetLibrary.list_assets('/Game/Data/Moves',recursive=True,include_folder=False):
 asset=unreal.load_asset(path)
 if isinstance(asset,unreal.PokeMonsterMoveData):
  key=str(asset.internal_id)
  assert key not in moves,('Duplicate move ID',key)
  moves[key]=asset
for level,key in spec['moves']:assert key in moves,('Missing productive move',key)
profile=unreal.load_asset(rows[0]['profile']);s=data('DA_'+name,'/Game/Data/Creatures',unreal.PokeMonsterCreatureSpeciesData)
settings=unreal.PokeMonsterCreatureOverworldSettings();settings.set_editor_property('body_radius',float(spec.get('navigation_radius',spec['radius'])));settings.set_editor_property('roam_radius',550. if spec['height']<100 else 750.);settings.set_editor_property('maximum_active_distance',1400.);behavior=settings.get_editor_property('behavior');behavior.set_editor_property('temperament',getattr(unreal.PokeMonsterOverworldTemperament,spec['behavior']));settings.set_editor_property('behavior',behavior)
for k,v in dict(internal_id=name,display_name=name,pokedex_number=spec['dex'],base_capture_rate=spec['capture'],primary_type=getattr(unreal.PokeMonsterCreatureType,spec['types'][0]),secondary_type=getattr(unreal.PokeMonsterCreatureType,spec['types'][1]),base_stats=unreal.PokeMonsterCreatureBaseStats(**dict(zip(['hp','attack','defense','special_attack','special_defense','speed'],spec['stats']))),gender=unreal.PokeMonsterGenderData(system=unreal.PokeMonsterGenderSystem.MIXED,female_ratio=spec['female']),starting_level=spec['level'],growth_rate=getattr(unreal.PokeMonsterGrowthRate,spec['growth']),base_experience_yield=spec['xp'],visuals=unreal.PokeMonsterCreatureVisuals(presentation=profile),overworld=settings,level_up_moves=[unreal.PokeMonsterLevelMove(level=l,move=moves[m])for l,m in spec['moves']]).items():s.set_editor_property(k,v)
save(s,'/Game/Data');wild=data('DA_'+name+'_Wild','/Game/Data/Encounters',unreal.PokeMonsterEncounterProfile);wild.set_editor_property('entries',[unreal.PokeMonsterWildEncounterEntry(species=s,min_level=spec['level'],max_level=spec['level'],weight=1)]);save(wild,'/Game/Data');rows[0].update(species_asset=s.get_path_name(),wild_profile=wild.get_path_name(),initial_level=spec['level'],implemented_moves=spec['moves'])
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(O/('Import'+name+'.json')).write_text(json.dumps({'assets':created,'models':rows,'no_existing_assets_changed':True,'no_map_saved':True},indent=2));unreal.log('GLUTEXO_IMPORTED '+name)
