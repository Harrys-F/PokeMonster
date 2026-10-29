"""First import into a new namespace only. Existing species, maps and source assets are immutable."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/ModelsV4';A=R/'Art/Characters/Creatures/Raichu';P='/Game/Characters/Creatures/Raichu/V4';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;created=[]
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
baseline=json.loads((D/'Baseline.json').read_text());assert not any(x.startswith('Content/Characters/Creatures/Raichu/')or x=='Content/Data/Creatures/DA_Raichu.uasset'for x in baseline['files'])
assert not(D/'Import.json').exists(),'Completed import must never run twice'
assert all((x.get_path_name().startswith(P+'/')or x.get_path_name()=='/Game/Data/Creatures/DA_Raichu')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
def save(o):
 assert o.get_path_name().startswith(P+'/')or o.get_path_name().startswith('/Game/Data/Creatures/DA_Raichu.')
 assert unreal.EditorAssetLibrary.save_loaded_asset(o,False);created.append(o.get_path_name());return o
def create(name,folder,cls,factory):
 if unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name):return unreal.load_asset(folder+'/'+name)
 o=T.create_asset(name,folder,cls,factory);assert o;return o
def data(name,folder,cls):
 f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',cls);return create(name,folder,cls,f)
def task(src,folder,name,options):
 if unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name):return [unreal.load_asset(folder+'/'+name)]
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(src),destination_path=folder,destination_name=name,automated=True,save=False,replace_existing=False,options=options).items():t.set_editor_property(k,v)
 T.import_asset_tasks([t]);return list(t.get_objects())
colors={'Coat':((.66,.215,.035),.52),'Cream':((.86,.73,.47),.6),'Brown':((.13,.052,.024),.51),'Gold':((.95,.62,.035),.48),'Eyes':((.008,.009,.012),.19),'Highlight':((.9,.94,.91),.27)};materials={}
for name,(color,roughness)in colors.items():
 if unreal.EditorAssetLibrary.does_asset_exist(P+'/Materials/M_Raichu_'+name):
  materials['Raichu_'+name]=unreal.load_asset(P+'/Materials/M_Raichu_'+name);continue
 m=create('M_Raichu_'+name,P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('used_with_skeletal_mesh',True);m.set_editor_property('two_sided',name in ['Cream','Gold','Brown'])
 c=L.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);c.set_editor_property('constant',unreal.LinearColor(*color,1));assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 f=L.create_material_expression(m,unreal.MaterialExpressionConstant);f.set_editor_property('r',roughness);assert L.connect_material_property(f,'',unreal.MaterialProperty.MP_ROUGHNESS);L.recompile_material(m);materials['Raichu_'+name]=save(m)
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 mesh=next(x for x in task(A/'Exports/V4/Raichu_Idle.fbx',P+'/Meshes','SK_Raichu_V4',ui)if isinstance(x,unreal.SkeletalMesh));sk=mesh.skeleton;slots=list(mesh.materials)
 for slot in slots:
  name=str(slot.material_slot_name);assert name in materials,name;slot.material_interface=materials[name]
 mesh.materials=slots;save(sk);save(mesh);clips={}
 for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
  ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=False,import_as_skeletal=True,import_animations=True,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,use_default_sample_rate=False,custom_sample_rate=30,animation_length=unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME).items():ui.anim_sequence_import_data.set_editor_property(k,v)
  clip=next(x for x in task(A/'Exports/V4'/('Raichu_'+role+'.fbx'),P+'/Animations','A_Raichu_'+role,ui)if isinstance(x,unreal.AnimSequence));dest=P+'/Animations/A_Raichu_'+role
  if clip.get_path_name().split('.')[0]!=dest:assert unreal.EditorAssetLibrary.rename_asset(clip.get_path_name().split('.')[0],dest);clip=unreal.load_asset(dest)
  clip.set_editor_property('enable_root_motion',False);clips[getattr(unreal.PokeMonsterCreatureClip,role.upper())]=save(clip)
finally:unreal.SystemLibrary.execute_console_command(W,'Interchange.FeatureFlags.Import.FBX '+str(old))
p=data('DA_Raichu_Presentation',P,unreal.PokeMonsterCreaturePresentationData)
for k,v in dict(mesh=mesh,clips=clips,walk_speed=35.,run_speed=65.,ground_offset_cm=.3,rig_family=unreal.PokeMonsterCreatureRigFamily.BIPED,reference_size_cm=80.,size_source='Project Models V4: Raichu 0.80m; authored source measured, no actor rescaling.').items():p.set_editor_property(k,v)
assert not p.get_validation_errors(),p.get_validation_errors();save(p)
# Exact Crystal data, no changes to Pikachu or existing move data. No new wild habitat/spawn rule.
s=data('DA_Raichu','/Game/Data/Creatures',unreal.PokeMonsterCreatureSpeciesData);settings=unreal.PokeMonsterCreatureOverworldSettings();settings.set_editor_property('body_radius',38.);settings.set_editor_property('roam_radius',550.);settings.set_editor_property('maximum_active_distance',1400.);behavior=settings.get_editor_property('behavior');behavior.set_editor_property('temperament',unreal.PokeMonsterOverworldTemperament.CURIOUS);settings.set_editor_property('behavior',behavior)
moves=[]
for name in ['ThunderShock','TailWhip','QuickAttack','Thunderbolt']:
 paths=[a for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game/Data/Moves',True)if str(a.asset_name).lower()==('DA_'+name).lower()];assert len(paths)==1,(name,len(paths));m=paths[0].get_asset();assert m.max_pp>0;moves.append(unreal.PokeMonsterLevelMove(level=1,move=m))
for k,v in dict(internal_id='Raichu',display_name='Raichu',pokedex_number=26,base_capture_rate=75,primary_type=unreal.PokeMonsterCreatureType.ELECTRIC,secondary_type=unreal.PokeMonsterCreatureType.NONE,base_stats=unreal.PokeMonsterCreatureBaseStats(hp=60,attack=90,defense=55,special_attack=90,special_defense=80,speed=100),gender=unreal.PokeMonsterGenderData(system=unreal.PokeMonsterGenderSystem.MIXED,female_ratio=.5),starting_level=11,growth_rate=unreal.PokeMonsterGrowthRate.MEDIUM_FAST,base_experience_yield=122,visuals=unreal.PokeMonsterCreatureVisuals(presentation=p),overworld=settings,level_up_moves=moves).items():s.set_editor_property(k,v)
save(s)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'Import.json').write_text(json.dumps({'created':created,'species':s.get_path_name(),'mesh':mesh.get_path_name(),'skeleton':sk.get_path_name(),'existing_assets_changed':False,'map_changed':False},indent=2));print('RAICHU_IMPORTED',len(created))
