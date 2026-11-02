"""Own target-map graphs; licensed texture inputs remain local, originals unchanged."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2FabAssetTrialV1';ROOT='/Game/Environment/VisualV2FabAssetTrialV1';ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and all(x.get_path_name().startswith(ROOT+'/')for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
def new(name):
 p=ROOT+'/Materials';m=unreal.load_asset(p+'/'+name)if unreal.EditorAssetLibrary.does_asset_exist(p+'/'+name)else AT.create_asset(name,p,unreal.Material,unreal.MaterialFactoryNew());ML.delete_all_material_expressions(m);m.set_editor_property('used_with_instanced_static_meshes',True);return m
def node(m,cls):return ML.create_material_expression(m,cls)
def custom(m,code,inputs,typ=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 n=node(m,unreal.MaterialExpressionCustom);n.set_editor_property('code',code);n.set_editor_property('output_type',typ);ls=[]
 for k in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',k);ls.append(i)
 n.set_editor_property('inputs',ls)
 for k,(src,pin)in inputs.items():assert ML.connect_material_expressions(src,pin,n,k)
 return n
def sample(m,asset,uv,normal=False):
 t=node(m,unreal.MaterialExpressionTextureSampleParameter2D);t.texture=unreal.load_asset(asset);assert t.texture,asset;t.set_editor_property('parameter_name',t.texture.get_name());t.set_editor_property('sampler_source',unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)
 if normal:t.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 assert ML.connect_material_expressions(uv,'',t,'UVs');return t
def finish(m):ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def scalar(m,value,prop):n=node(m,unreal.MaterialExpressionConstant);n.r=value;assert ML.connect_material_property(n,'',prop)
# Author a cheap spatial blend over the existing checked ground color map.
m=new('M_FAT_Ground');P=node(m,unreal.MaterialExpressionWorldPosition);uv=custom(m,'return (P.xy-float2(-6000,-3250))/float2(9000,6500);',{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);base=sample(m,'/Game/Environment/VisualV2PerformanceV1/Textures/T_PV1_GroundColorSRGB',uv);base.set_editor_property('sampler_source',unreal.SamplerSourceMode.SSM_CLAMP_WORLD_GROUP_SETTINGS)
uv=custom(m,'return P.xy/230.0;',{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2)
g=sample(m,'/Game/Pack_Bonus/Textures/Grass_2/T_Pack_Bonus_Grass_2_basecolor',uv);f=sample(m,'/Game/Fab/VisualV2TrialLocal/Ground/T_sfjmafua_2K_B',uv);r=sample(m,'/Game/Fab/VisualV2TrialLocal/Ground/T_pjwey0_2K_B',uv)
code='''float2 p=P.xy;
float meadow=saturate((1-length((p-float2(-4500,-2100))/float2(1100,620)))*4);
float forest=saturate((1-length((p-float2(-4350,1600))/float2(1100,1100)))*4);
forest=max(forest,saturate((1-length((p-float2(-2050,1450))/float2(550,450)))*4));
float bank=1-smoothstep(0.04,.20,abs(length((p-float2(720,-1800))/float2(900,650))-1));
float rock=saturate((1-length((p-float2(-1100,1100))/float2(520,470)))*4);
float variation=.94+.06*sin(p.x*.004+sin(p.y*.003));
float3 c=lerp(B,G*float3(.9,1.0,.83)*variation,meadow*.72);
c=lerp(c,F*1.15,forest*.78);c=lerp(c,R*.78,max(bank,rock)*.72);return c;'''
c=custom(m,code,{'P':(P,''),'B':(base,'RGB'),'G':(g,'RGB'),'F':(f,'RGB'),'R':(r,'RGB')});assert ML.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
n=sample(m,'/Game/Pack_Bonus/Textures/Grass_2/T_Pack_Bonus_Grass_2_normal',uv,True);nn=custom(m,'return normalize(lerp(float3(0,0,1),N,.38));',{'N':(n,'RGB')});assert ML.connect_material_property(nn,'',unreal.MaterialProperty.MP_NORMAL);scalar(m,.87,unreal.MaterialProperty.MP_ROUGHNESS);finish(m)
# World-space textured path, no displacement and no collision changes.
p=new('M_FAT_Path');P=node(p,unreal.MaterialExpressionWorldPosition);uv=custom(p,'return P.xy/190.0;',{'P':(P,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT2);c=sample(p,'/Game/Fab/VisualV2TrialLocal/Ground/T_ugsnfawlw_2K_B',uv);t=custom(p,'return C*float3(1.18,1.08,.91);',{'C':(c,'RGB')});assert ML.connect_material_property(t,'',unreal.MaterialProperty.MP_BASE_COLOR);n=sample(p,'/Game/Fab/VisualV2TrialLocal/Ground/T_ugsnfawlw_2K_N',uv,True);assert ML.connect_material_property(n,'RGB',unreal.MaterialProperty.MP_NORMAL);scalar(p,.9,unreal.MaterialProperty.MP_ROUGHNESS);finish(p)
# Own simple foliage instances; their licensed parents remain in the imported pack.
rows=[]
for name,src in [('MI_FAT_Flowers','MI_Fol_Foliage_Atlas'),('MI_FAT_Grass','MI_Fol_Grass_AlphaCut')]:
 q='/Game/StyleHex_Studio/Free_Packs/FREE_Stylized_Grass_Flowers_Foliage/Materials/Mat_Foliage/'+src;old=unreal.load_asset(q);mi=AT.create_asset(name,ROOT+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());ML.set_material_instance_parent(mi,old.parent)
 # Copy parameter overrides only, not the licensed parent graph.
 for prop in ['scalar_parameter_values','vector_parameter_values','texture_parameter_values']:mi.set_editor_property(prop,old.get_editor_property(prop))
 if 'Flowers'in name:ML.set_material_instance_scalar_parameter_value(mi,'Texture Brightness',1.15)
 ML.set_material_instance_scalar_parameter_value(mi,'Wind Instance Influence',.15);assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False);rows.append(dict(own=mi.get_path_name(),local_parent=old.parent.get_path_name()))
(D/'Materials.json').write_text(json.dumps(rows,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
