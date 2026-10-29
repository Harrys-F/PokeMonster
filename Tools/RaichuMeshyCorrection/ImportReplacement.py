"""Existing Meshy FBX/material workflow; change only the stable Raichu species presentation."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';A=R/'Art/Characters/Creatures/Raichu';P='/Game/Characters/Creatures/Raichu/MeshyV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not unreal.EditorAssetLibrary.does_directory_exist(P),'No blind reimport of a completed replacement'
source=R/'Art/Characters/Creatures/Incoming/Raichu.glb';expected=json.loads((D/'SourceDiscovery.json').read_text())[0]['sha256'];assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[];W=E.get_editor_world()
def create(name,folder,cls,factory):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name);a=T.create_asset(name,folder,cls,factory);assert a;return a
def save(a):assert a.get_path_name().startswith(P+'/');assert unreal.EditorAssetLibrary.save_loaded_asset(a,False);created.append(a.get_path_name());return a
def data(name,folder,cls):
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',cls);return create(name,folder,cls,f)
def task(src,folder,name,options=None):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name);t=unreal.AssetImportTask()
 for k,v in dict(filename=str(src),destination_path=folder,destination_name=name,automated=True,save=False,replace_existing=False).items():t.set_editor_property(k,v)
 if options:t.options=options
 T.import_asset_tasks([t]);return list(t.get_objects())
textures={}
for typ in ['BaseColor','Normal','MetallicRoughness']:
 t=next(x for x in task(A/'Textures/MeshyV1'/('Raichu_'+typ+'.jpg'),P+'/Textures','T_Raichu_'+typ)if isinstance(x,unreal.Texture2D));t.set_editor_property('srgb',typ=='BaseColor')
 if typ=='Normal':t.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);t.set_editor_property('flip_green_channel',True)
 elif typ=='MetallicRoughness':t.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
 textures[typ]=save(t)
m=create('M_Raichu_Meshy',P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('two_sided',True);m.set_editor_property('used_with_skeletal_mesh',True)
for typ,sampler,channels in [('BaseColor',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR,[('RGB',unreal.MaterialProperty.MP_BASE_COLOR)]),('Normal',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,[('RGB',unreal.MaterialProperty.MP_NORMAL)]),('MetallicRoughness',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS,[('G',unreal.MaterialProperty.MP_ROUGHNESS),('B',unreal.MaterialProperty.MP_METALLIC)])]:
 n=L.create_material_expression(m,unreal.MaterialExpressionTextureSample);n.set_editor_property('texture',textures[typ]);n.set_editor_property('sampler_type',sampler)
 for c,p in channels:assert L.connect_material_property(n,c,p)
L.recompile_material(m);save(m);old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 mesh=next(x for x in task(A/'Exports/MeshyV1/Raichu_Idle.fbx',P+'/Meshes','SK_Raichu_Meshy',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials);assert len(slots)==1
 for slot in slots:slot.material_interface=m
 mesh.materials=slots;save(sk);save(mesh);clips={}
 for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
  clip=next(x for x in task(A/'Exports/MeshyV1'/('Raichu_'+role+'.fbx'),P+'/Animations','A_Raichu_'+role,ui)if isinstance(x,unreal.AnimSequence));dest=P+'/Animations/A_Raichu_'+role
  if clip.get_path_name().split('.')[0]!=dest:assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
  clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip)
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
p=data('DA_Raichu_Meshy_Presentation',P,unreal.PokeMonsterCreaturePresentationData)
for k,v in dict(mesh=mesh,clips=clips,walk_speed=28.,run_speed=55.,ground_offset_cm=0.,rig_family=unreal.PokeMonsterCreatureRigFamily.BIPED,reference_size_cm=80.,size_source='Harry Meshy Original: Art/Characters/Creatures/Incoming/Raichu.glb; SHA256 '+expected+'; 0.80m normalized standing height, source geometry/UV unchanged.').items():p.set_editor_property(k,v)
assert not p.get_validation_errors(),p.get_validation_errors();save(p)
s=unreal.load_asset('/Game/Data/Creatures/DA_Raichu')
def stable():return {'id':str(s.get_internal_id()),'name':str(s.get_display_name()),'dex':s.get_pokedex_number(),'capture':s.get_base_capture_rate(),'types':[str(s.get_primary_type()),str(s.get_secondary_type())],'stats':s.get_base_stats().export_text(),'growth':str(s.get_growth_rate()),'xp':s.get_base_experience_yield(),'gender':s.get_editor_property('gender').export_text(),'level':s.get_editor_property('starting_level'),'learnset':[x.export_text()for x in s.level_up_moves],'evolutions':[x.export_text()for x in s.get_evolutions()],'overworld':s.overworld.export_text()}
before=stable();s.set_editor_property('visuals',unreal.PokeMonsterCreatureVisuals(presentation=p));assert stable()==before;assert unreal.EditorAssetLibrary.save_loaded_asset(s,False)
assert len(unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species())==19;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
(D/'Replacement.json').write_text(json.dumps({'source':str(source.relative_to(R)),'source_sha256':expected,'created':created,'stable_species':s.get_path_name(),'only_presentation_changed':True,'preserved_species_data':before,'active_presentation':p.get_path_name(),'active_mesh':mesh.get_path_name()},indent=2));print('MESHY_RAICHU_BOUND',len(created))
