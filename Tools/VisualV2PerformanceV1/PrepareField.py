"""Own derived materials only: replace static route scan with a linear data lookup.

The three earlier, unsuccessful BVH assets are our disposable candidates. Their
other graph nodes/inputs still match the unchanged original clones. This step
reuses those owned candidates, never resaves shared originals or the map.
"""
import unreal,json,re,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);L=unreal.MaterialEditingLibrary
assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert(D/'MaterialCandidates.json').exists();assert not(D/'FieldPrepared.json').exists()
texpath='/Game/Environment/VisualV2PerformanceV1/Textures/T_PV1_RouteField';assert not unreal.EditorAssetLibrary.does_asset_exist(texpath)
task=unreal.AssetImportTask();task.filename=str(R/'Art/World/VisualV2PerformanceV1/RouteField.png');task.destination_path='/Game/Environment/VisualV2PerformanceV1/Textures';task.destination_name='T_PV1_RouteField';task.automated=True;task.save=False;task.replace_existing=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);tex=unreal.load_asset(texpath);assert tex
tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP);tex.set_editor_property('compression_no_alpha',False);tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS);tex.set_editor_property('filter',unreal.TextureFilter.TF_BILINEAR);tex.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);tex.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP);tex.set_editor_property('never_stream',True);assert unreal.EditorAssetLibrary.save_loaded_asset(tex,False)
replacement='''float2 nearest(float2 p, Texture2D field, SamplerState fieldSampler){
// PV1: linear, lossless RGBA8 data. Distances in RG, widths in BA.
float4 v=Texture2DSampleLevel(field,fieldSampler,(p-float2(-7000,-5000))/float2(11000,10000),0);
return float2(dot(v.rg,float2(256,1))*(8192.0/257.0),dot(v.ba,float2(256,1))*(256.0/257.0));}'''
results=[]
for name in ['Ground','MainPath','NorthPath']:
 source=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_'+name);m=unreal.load_asset('/Game/Environment/VisualV2PerformanceV1/Materials/M_PV1_'+name);assert m
 sourcecodes={x.get_name():x.get_editor_property('code')for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom)if x.get_outer()==source and'W6Route'in x.get_editor_property('code')};nodes={x.get_name():x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom)if x.get_outer()==m};field=L.create_material_expression(m,unreal.MaterialExpressionTextureObjectParameter,-1600,2400);field.set_editor_property('parameter_name','PV1Route');field.set_editor_property('texture',tex);field.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR);rows=[]
 for key,old in sourcecodes.items():
  code,n=re.subn(r'float2 nearest\(float2 p\)\{.*?return float2\(d,base\);\}',replacement,old,flags=re.S);assert n==1;assert code.count('route.nearest(v6p)')==1;code=code.replace('route.nearest(v6p)','route.nearest(v6p,PV1Route,PV1RouteSampler)');node=nodes[key];node.set_editor_property('code',code);arg=unreal.CustomInput();arg.set_editor_property('input_name','PV1Route');node.set_editor_property('inputs',list(node.get_editor_property('inputs'))+[arg]);assert L.connect_material_expressions(field,'',node,'PV1Route');rows.append({'node':key,'source_sha256':hashlib.sha256(old.encode()).hexdigest(),'candidate_sha256':hashlib.sha256(code.encode()).hexdigest(),'source_chars':len(old),'candidate_chars':len(code)})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);results.append({'source':source.get_path_name(),'candidate':m.get_path_name(),'nodes':rows})
if hasattr(unreal,'AssetCompilingManager'):unreal.AssetCompilingManager.finish_all_compilation()
(D/'FieldPrepared.json').write_text(json.dumps({'texture':tex.get_path_name(),'linear':not tex.srgb,'dimensions':[tex.blueprint_get_size_x(),tex.blueprint_get_size_y()],'no_mips':True,'resident_bytes':16777216,'proof':json.loads((D/'RouteFieldProof.json').read_text()),'materials':results},indent=2));unreal.log('PERF1_FIELD_READY')
