"""Westland-only derived surfaces. Original assets and reference map remain untouched."""
import unreal,json,sys,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';ROOT='/Game/Environment/WestlandVisualUpgradeV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();L=unreal.MaterialEditingLibrary
assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert all(x.get_path_name().startswith(ROOT)for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
assert not (D/'SurfaceAudit.json').exists(),'Never repeat completed authoring'
assert hashlib.sha256((R/'Content/Maps/Dev_WestlandRegion.umap').read_bytes()).hexdigest()==json.loads((D/'Baseline.json').read_text())['files']['Content/Maps/Dev_WestlandRegion.umap']
created=[];bindings=[]
def clone(src,name):
 path=ROOT+'/Materials/'+name;m=unreal.load_asset(path)if unreal.EditorAssetLibrary.does_asset_exist(path)else unreal.EditorAssetLibrary.duplicate_asset(src,path);assert m;created.append(m.get_path_name().split('.')[0]);return m
def custom(m,code,inputs,kind=unreal.CustomMaterialOutputType.CMOT_FLOAT3):
 node=L.create_material_expression(m,unreal.MaterialExpressionCustom);node.set_editor_property('code',code);node.set_editor_property('output_type',kind);arr=[]
 for k in inputs:i=unreal.CustomInput();i.set_editor_property('input_name',k);arr.append(i)
 node.set_editor_property('inputs',arr)
 for k,(v,o)in inputs.items():assert L.connect_material_expressions(v,o,node,k),k
 return node
def save(m):L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
task=unreal.AssetImportTask();task.filename=str(R/'Art/World/WestlandVisualUpgradeV1/ForestCoverage.png');task.destination_path=ROOT+'/Textures';task.destination_name='T_WVU_ForestCoverage';task.automated=True;task.replace_existing=True;task.save=False;unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);tex=unreal.load_asset(ROOT+'/Textures/T_WVU_ForestCoverage');assert tex;tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS);assert unreal.EditorAssetLibrary.save_loaded_asset(tex,False);created.append(tex.get_path_name().split('.')[0])
# Same painted grass/earth textures and original regional path mask. Only map-local clones.
matmap={}
for key in ['Grass','PathBlend']:
 source='/Game/Environment/WestlandRegion/Materials/M_WR_'+key;m=clone(source,'M_WVU_'+key);target=next(x for x in L.get_material_expressions(m)if isinstance(x,unreal.MaterialExpressionCustom)and 'float3 g0=Texture2DSample'in x.get_editor_property('code'));code=next(x.get_editor_property('code')for x in L.get_material_expressions(unreal.load_asset(source))if isinstance(x,unreal.MaterialExpressionCustom)and 'float3 g0=Texture2DSample'in x.get_editor_property('code'))
 assert 'if(Mode<.5)return g;'in code and 'if(Mode<1.5)return d;'in code
 code=code.replace('if(Mode<.5)return g;','')
 patch='''
// Map-local forest-floor coverage from original Westland tree locations.
float2 en=float2((p.x+p.y)*.007071067812,(p.x-p.y)*.007071067812);
float2 regionUV=float2((en.x+500)/1000,(400-en.y)/800);
float forest=Texture2DSample(FTex,FTexSampler,regionUV).r;
float river=25+35*sin((en.y+70)/150)+200*max(0,(-en.y-80)/220);
float shore=1-smoothstep(3.4,8.2,abs(en.x-river));
float litter=.5+.25*sin(p.x*.018+sin(p.y*.023))+.25*cos(p.y*.031-p.x*.009);
float3 forestEarth=d*lerp(float3(.60,.65,.51),float3(.78,.72,.57),litter);
g=lerp(g,forestEarth,saturate(forest*.80));
g=lerp(g,d*float3(.69,.72,.60),shore*.76);
if(Mode<.5)return g;
'''
 target.set_editor_property('code',code.replace('if(Mode<1.5)return d;',patch+'if(Mode<1.5)return d;'));i=unreal.CustomInput();i.set_editor_property('input_name','FTex');target.set_editor_property('inputs',list(target.get_editor_property('inputs'))+[i]);t=L.create_material_expression(m,unreal.MaterialExpressionTextureObjectParameter);t.set_editor_property('parameter_name','WestlandForestCoverage');t.set_editor_property('texture',tex);t.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS);assert L.connect_material_expressions(t,'',target,'FTex')
 pos=next(x for x in L.get_material_expressions(m)if isinstance(x,unreal.MaterialExpressionWorldPosition));normal=custom(m,'float2 p=P.xy;return normalize(float3(.035*cos(p.x*.11+sin(p.y*.05)),.030*sin(p.y*.13+p.x*.03),1));',{'P':(pos,'')});assert L.connect_material_property(normal,'',unreal.MaterialProperty.MP_NORMAL);save(m);matmap[source]=m
# Reuse the actual current VisualV2 pond's lit translucency/SSR/roughness/normal architecture.
water=clone('/Game/Environment/PokemonAIV3/Materials/M_AIV3PondWater','M_WVU_River');nodes=L.get_material_expressions(water);color=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionCustom)and 'float pond='in x.get_editor_property('code'));pos=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionWorldPosition));uv=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionTextureCoordinate));assert any(str(i.get_editor_property('input_name'))=='UV'for i in color.get_editor_property('inputs'));assert L.connect_material_expressions(uv,'',color,'UV')
color.set_editor_property('code','''
struct WaterPaint {float hash(float2 p){return frac(sin(dot(p,float2(127.1,311.7)))*43758.5453);}float noise(float2 p){float2 i=floor(p),f=frac(p);f=f*f*(3-2*f);return lerp(lerp(hash(i),hash(i+float2(1,0)),f.x),lerp(hash(i+float2(0,1)),hash(i+1),f.x),f.y);}};
WaterPaint f;
float along=UV.y*8;float edge=abs(UV.x*2-1);float deep=1-smoothstep(.28,.96,edge);
float grain=f.noise(P.xy*.027),macro=f.noise(float2(UV.x*4,along*.18));
float3 col=lerp(float3(.087,.125,.079),float3(.022,.080,.095),deep);
col*=.94+.10*macro;float flow=sin(along*4.6+sin(UV.x*10+T*.23)*.65+T*.75);
float glint=pow(saturate(flow),22)*(.35+.65*grain);
col+=float3(.009,.016,.015)*glint*deep;
float opacity=lerp(.38,.72,deep)*(1-smoothstep(.97,1,edge));
return float4(col,opacity);
''')
normal=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionCustom)and 'return normalize'in x.get_editor_property('code'));normal.set_editor_property('code','float2 q=float2((P.x+P.y)*.70710678,(P.x-P.y)*.70710678);float a=q.y*.040+sin(q.x*.018+T*.18)*.8+T*.6;float b=q.y*.09+q.x*.02+T*.32;return normalize(float3(.038*cos(a)+.018*sin(b),.058*sin(a)+.019*cos(b),1));')
oldopacity=L.get_material_property_input_node(water,unreal.MaterialProperty.MP_OPACITY);sd=L.create_material_expression(water,unreal.MaterialExpressionSceneDepth);pd=L.create_material_expression(water,unreal.MaterialExpressionPixelDepth);fade=custom(water,'return A*saturate(max(0,SD-PD)/50.0);',{'A':(oldopacity,''),'SD':(sd,''),'PD':(pd,'')},unreal.CustomMaterialOutputType.CMOT_FLOAT1);assert L.connect_material_property(fade,'',unreal.MaterialProperty.MP_OPACITY);save(water)
matmap['/Game/Environment/WestlandRegion/Materials/M_WR_River']=water
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for n in range(c.get_num_materials()):
   m=c.get_material(n);src=m.get_path_name().split('.')[0]if m else''
   if src in matmap:a.modify();c.set_material(n,matmap[src]);bindings.append(dict(actor=a.get_name(),component=c.get_name(),slot=n,before=src,after=matmap[src].get_path_name()))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'No shared assets changed'
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'SurfaceAudit.json').write_text(json.dumps(dict(assets=created,bindings=bindings,water_geometry_unchanged=True,render_settings_unchanged=True),indent=2));unreal.log('WESTLAND_VISUAL_SURFACES_SAVED')
