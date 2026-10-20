import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world();L=unreal.MaterialEditingLibrary;D='/Game/Environment/HealingHouse/ArtV4';actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
m=unreal.load_asset('/Game/Characters/NPCs/SilverLady/HealerArtV4/Materials/M_WestlandHealer_HerbalLinen')
for n in L.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionTextureSample) and n.texture and n.texture.get_name()=='T_SilverLady_MetalRough':n.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
for label,a in actors.items():
 if label.startswith('ArtV4_HerbalBanner') or label.startswith('ArtV4_HerbalWindowShelf'):a.set_actor_rotation(unreal.Rotator(yaw=90 if a.get_actor_location().x>17300 else 0),False)
 if label.startswith('ArtV4_Hearth'):
  a.set_actor_location(unreal.Vector(17342,55,0),False,True);a.set_actor_rotation(unreal.Rotator(yaw=90),False)
 if label.startswith('ArtV4_RemedyCabinet'):a.set_actor_location(unreal.Vector(17342,820,0),False,True);a.set_actor_rotation(unreal.Rotator(yaw=90),False)
 if label.startswith('ArtV4_FlagstoneApron'):a.set_actor_location(unreal.Vector(16950,500,.2),False,True)
actors['V2_House_HH_Art_MainRunner'].set_actor_location(unreal.Vector(16825,500,2.1),False,True)
# Existing rug mesh has relief geometry for the old motif. Bind all sections of the same asset,
# but keep its original collider untouched. The new woven design remains the underlying surface.
# Purpose-specific natural stone shader; it uses the existing painted stone texture.
path=D+'/Materials/M_HH4_Flagstone';assert not unreal.EditorAssetLibrary.does_asset_exist(path);stone=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_HH4_Flagstone',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());P=L.create_material_expression(stone,unreal.MaterialExpressionWorldPosition);T=L.create_material_expression(stone,unreal.MaterialExpressionTextureObjectParameter);T.set_editor_property('parameter_name','PaintedStone');T.set_editor_property('texture',unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_PaintedStone'));V=L.create_material_expression(stone,unreal.MaterialExpressionVertexColor);N=L.create_material_expression(stone,unreal.MaterialExpressionCustom);args=[]
for k in ['P','Tex','C']:i=unreal.CustomInput();i.set_editor_property('input_name',k);args.append(i)
N.set_editor_property('inputs',args);N.set_editor_property('code','float3 t=Texture2DSample(Tex,TexSampler,P.xy/77+float2(.13,.29)).rgb;float macro=sin(P.x*.017+sin(P.y*.013))*cos(P.y*.021);return t*float3(.48,.43,.34)*(.86+.18*macro)*lerp(.70,1.06,C.r);');N.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
for k,n in [('P',P),('Tex',T),('C',V)]:L.connect_material_expressions(n,'',N,k)
L.connect_material_property(N,'',unreal.MaterialProperty.MP_BASE_COLOR)
for v,prop in [(.94,unreal.MaterialProperty.MP_ROUGHNESS),(.08,unreal.MaterialProperty.MP_SPECULAR)]:n=L.create_material_expression(stone,unreal.MaterialExpressionConstant);n.set_editor_property('r',v);L.connect_material_property(n,'',prop)
L.recompile_material(stone);unreal.EditorAssetLibrary.save_loaded_asset(stone,False)
for label,a in actors.items():
 if label.startswith('ArtV4_FlagstoneApron') or (label.startswith('ArtV4_Hearth') and 'Flames' not in label):a.static_mesh_component.set_material(0,stone)
# New major furnishings receive simple collision; existing blockers and doorways stay unchanged.
SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for key in ['Hearth','RemedyCabinet']:
 mesh=unreal.load_asset(D+'/Meshes/SM_HH4_'+key);assert SM.get_simple_collision_count(mesh)==0;SM.add_simple_collisions(mesh,unreal.ScriptingCollisionShapeType.BOX);assert SM.get_simple_collision_count(mesh)==1;unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
 for label,a in actors.items():
  if label.startswith('ArtV4_'+key+'_'):a.static_mesh_component.set_collision_profile_name('BlockAll');a.tags=['ArtV4','PhysicalFurniture']
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(R/'Saved/ArtPassV4/DraftCorrections.json').write_text(json.dumps({'stone_material':stone.get_path_name(),'hearth_position':[17342,55,0],'cabinet_position':[17342,820,0],'fixture_yaw':90,'new_major_furniture_collision':['Hearth','RemedyCabinet'],'surface_height_correction':True,'healer_sampler_fixed':'MetalRough uses Masks matching existing texture compression'},indent=2))
