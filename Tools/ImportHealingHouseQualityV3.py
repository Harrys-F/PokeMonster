"""Import reviewed V3 FBX; reuse V2 paint, create scoped fade variants.
Four existing Westland ground materials receive the shared anti-tiling graph.
No original source mesh or texture reimport, no gameplay/C++ mutation.
"""
import unreal,json,re
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve()
H='/Game/Environment/HealingHouse/QualityV3';W='/Game/Environment/Westland/NaturalGroundV1'
lib=unreal.MaterialEditingLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
OUT=ROOT/'Saved/HealingQualityV3';OUT.mkdir(parents=True,exist_ok=True)
catalog=json.loads((ROOT/'Art/HealingHouse/QualityV3/Props.json').read_text())
assert (OUT/'Blender/SourceAudit.json').exists(), 'Reopen/review/export first'
paths=[];materials={};fade={}
def wire(a,out,b,pin):assert lib.connect_material_expressions(a,out,b,pin),(a.get_name(),b.get_name(),pin)
def node(m,cls,x,y):return lib.create_material_expression(m,cls,x,y)
def constant(m,value,x,y):
    o=node(m,unreal.MaterialExpressionConstant,x,y);o.r=value;return o
def tint(m,color,x,y):
    o=node(m,unreal.MaterialExpressionConstant3Vector,x,y);o.constant=unreal.LinearColor(*color,1);return o
def material(name,color,two_sided=False,metal=False):
    path=H+'/Materials/M_HH_Q3_'+name
    if two_sided and not unreal.EditorAssetLibrary.does_asset_exist(path):
        assert unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/HealingHouse/V3/Materials/M_HH_V3_Sage',path)
    m=unreal.load_asset(path) or tools.create_asset('M_HH_Q3_'+name,H+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
    if not two_sided:lib.delete_all_material_expressions(m)
    m.set_editor_property('two_sided',two_sided)
    c=tint(m,color,0,0);lib.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
    r=constant(m,.73 if metal else .86,0,150);lib.connect_material_property(r,'',unreal.MaterialProperty.MP_ROUGHNESS)
    if metal:
        q=constant(m,.35,0,230);lib.connect_material_property(q,'',unreal.MaterialProperty.MP_METALLIC)
    lib.delete_unused_expressions(m);lib.recompile_material(m);materials[name]=m;paths.append(path);return m
for name,c in [('Leaf',(.028,.072,.018)),('LeafLight',(.085,.15,.04)),('LeafDark',(.015,.04,.007)),('Flower',(.24,.06,.035)),('FlowerCream',(.40,.27,.09)),('Ceramic',(.14,.06,.025))]:material(name,c,name.startswith(('Leaf','Flower')))
material('Metal',(.04,.045,.032),False,True)
for key in ['Wood','Timber','Stone','Sage','Linen']:
    materials[key]=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_'+key)
for key in ['Gold','Mortar','Fire','Paper','Glass','Book','Window']:
    materials[key]=unreal.load_asset('/Game/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_'+key)
materials['Cream']=unreal.load_asset('/Game/Environment/HealingHouse/V3/Materials/M_HH_V3_Cream')
# The only new bitmap; original generated PNG remains intact in Art/.
texturepath=H+'/Textures/T_HH_PaintedTerracotta'
if not unreal.EditorAssetLibrary.does_asset_exist(texturepath):
    task=unreal.AssetImportTask();task.filename=str(ROOT/'Art/HealingHouse/Textures/QualityV3/T_HH_PaintedTerracotta.png')
    task.destination_path=H+'/Textures';task.destination_name='T_HH_PaintedTerracotta';task.automated=True;task.save=False;tools.import_asset_tasks([task])
rooftexture=unreal.load_asset(texturepath);assert rooftexture
rooftexture.set_editor_property('srgb',True);rooftexture.set_editor_property('max_texture_size',1024)
rooftexture.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO)
rooftexture.set_editor_property('never_stream',False);paths.append(texturepath)
# Copy only material graphs, preserving their established HouseCutaway behavior.
for key in ['Wood','Timber','Stone','Plaster','Roof','Metal','Glass','Sage','Cream']:
    old=('/Game/Environment/HealingHouse/V3/Materials/M_HH_V3_'+key) if key in ['Sage','Cream'] else ('/Game/Environment/HealingHouse/Materials/M_HH_V2_'+key)
    path=H+'/Materials/M_HH_Q3_Fade_'+key
    if not unreal.EditorAssetLibrary.does_asset_exist(path):assert unreal.EditorAssetLibrary.duplicate_asset(old,path)
    m=unreal.load_asset(path);expressions=list(lib.get_material_expressions(m))
    assert any(isinstance(x,unreal.MaterialExpressionScalarParameter) and str(x.get_editor_property('parameter_name'))=='HouseCutaway' for x in expressions)
    samples=[o for o in expressions if isinstance(o,unreal.MaterialExpressionTextureSample)]
    for sample in samples:
        tex={'Wood':'Wood','Timber':'Wood','Stone':'Stone','Plaster':'Plaster'}.get(key)
        if tex:sample.set_editor_property('texture',unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Textures/T_HH_Painted'+tex))
        if key=='Roof':sample.set_editor_property('texture',rooftexture)
        uv=node(m,unreal.MaterialExpressionTextureCoordinate,-800,100);wire(uv,'',sample,'UVs')
    if key in ['Wood','Timber','Stone','Plaster','Roof']:
        c=tint(m,{'Wood':(.95,.84,.70),'Timber':(.47,.40,.32),'Stone':(.90,.83,.73),'Plaster':(1,.98,.90),'Roof':(.85,.76,.69)}[key],-250,240)
        mul=node(m,unreal.MaterialExpressionMultiply,0,0);wire(samples[0],'RGB',mul,'A');wire(c,'',mul,'B')
        lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
    lib.delete_unused_expressions(m);lib.recompile_material(m);fade[key]=m;paths.append(path)
materials['Roof']=fade['Roof']
def material_key(m):return re.sub(r'[._]\d+$','',str(m)).split('_')[-1]
editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for name,entry in catalog.items():
    path=H+'/Meshes/SM_HH_Q3_'+name
    if not unreal.EditorAssetLibrary.does_asset_exist(path):
        ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False
        ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
        for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(k,v)
        task=unreal.AssetImportTask();task.filename=str(ROOT/'Art/HealingHouse/Exports/QualityV3'/('SM_HH_Q3_'+name+'.fbx'))
        task.destination_path=H+'/Meshes';task.destination_name='SM_HH_Q3_'+name;task.automated=True;task.options=ui;task.save=False
        assert Path(task.filename).exists();tools.import_asset_tasks([task])
    mesh=unreal.load_asset(path);assert mesh
    exterior=name in ['Roof_Main','Roof_Porch','Roof_Entry','Roof_Trim','Timber_Front','Timber_CameraSide','Timber_Far','Timber_Entry','Stone_Front','Stone_CameraSide','Stone_Far','Chimney','Windows_Front','Windows_CameraSide','Windows_Far','DoorFrame','GuardianSign']
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        key=material_key(slot.get_editor_property('imported_material_slot_name'));m=fade.get(key) if exterior else materials.get(key)
        if not m:m=materials.get(key)
        assert m,(name,key);mesh.set_material(i,m)
    mesh.set_editor_property('light_map_resolution',64)
    assert editor.get_number_verts(mesh,0)>0
    # Collision remains on the original actor; map authoring adds this visual mesh.
    assert editor.get_simple_collision_count(mesh)==0
    paths.append(path)

GROUND_CODE=r'''
float2 p=P.xy;
float2 a=p/190.0;
float2 b=float2(p.x*.809-p.y*.588,p.x*.588+p.y*.809)/271.0+float2(.371,.137);
float2 c=float2(p.y,-p.x)/413.0+float2(.163,.619);
float3 g0=Texture2DSample(GTex,GTexSampler,a).rgb;
float3 g1=Texture2DSample(GTex,GTexSampler,b).rgb;
float3 g2=Texture2DSample(GTex,GTexSampler,c).rgb;
float macro=sin(p.x*.0017+sin(p.y*.0021))*cos(p.y*.0013-p.x*.0007);
float blend=.38+.16*macro;
float3 g=lerp(g0,g1,blend)*.70+g2*.30;
g=lerp(g,dot(g,float3(.299,.587,.114)),.25)*float3(.66,.72,.62);
g*=1+.075*macro;
if(Mode<.5)return g;
float3 d0=Texture2DSample(DTex,DTexSampler,p/220.0+float2(.19,.43)).rgb;
float3 d1=Texture2DSample(DTex,DTexSampler,float2(p.x*.6+p.y*.8,-p.x*.8+p.y*.6)/337.0+float2(.73,.27)).rgb;
float3 d=lerp(d0,d1,.42+.14*macro)*float3(.86,.80,.73)*(1+.035*macro);
if(Mode<1.5)return d;
float irregular=sin(p.x*.027+sin(p.y*.04))*.035+sin(p.x*.073)*.018;
float edge=abs(UV.y*2-1)+irregular;
float alpha=1-smoothstep(.65,.99,edge);
float ends=smoothstep(0,.035,UV.x)*(1-smoothstep(.965,1,UV.x));
if(Mode<2.5)return lerp(g,d*(1-.08*(1-saturate(edge))),alpha*ends);
float2 q=(p-Center.xy)/Extent.xy;
float radius=length(q)+sin(p.x*.026+p.y*.018)*.035+cos(p.y*.047)*.024;
return lerp(g,d,1-smoothstep(.69,.98,radius));
'''
for name,mode in [('Grass',0),('Earth',1),('PathBlend',2),('ForecourtBlend',3)]:
    m=unreal.load_asset(W+'/Materials/M_WL_NG_'+name);assert m
    lib.delete_all_material_expressions(m)
    custom=node(m,unreal.MaterialExpressionCustom,0,0);custom.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    inputs=[]
    for key in ['GTex','DTex','P','UV','Mode','Center','Extent']:
        i=unreal.CustomInput();i.set_editor_property('input_name',key);inputs.append(i)
    custom.set_editor_property('inputs',inputs);custom.set_editor_property('code',GROUND_CODE)
    for key,tex,y in [('GTex','Grass',0),('DTex','Earth',200)]:
        obj=node(m,unreal.MaterialExpressionTextureObjectParameter,-700,y);obj.set_editor_property('parameter_name',key)
        obj.set_editor_property('texture',unreal.load_asset(W+'/Textures/T_WL_Painted'+tex));wire(obj,'',custom,key)
    pos=node(m,unreal.MaterialExpressionWorldPosition,-700,400);wire(pos,'',custom,'P')
    uv=node(m,unreal.MaterialExpressionTextureCoordinate,-700,550);wire(uv,'',custom,'UV')
    wire(constant(m,mode,-700,650),'',custom,'Mode')
    for key,param,val,y in [('Center','CourtCenter_cm',(-850,0,0,0),750),('Extent','CourtHalfSize_cm',(325,340,0,0),950)]:
        o=node(m,unreal.MaterialExpressionVectorParameter,-700,y);o.set_editor_property('parameter_name',param);o.set_editor_property('default_value',unreal.LinearColor(*val));wire(o,'',custom,key)
    lib.connect_material_property(custom,'',unreal.MaterialProperty.MP_BASE_COLOR)
    lib.connect_material_property(constant(m,.88,0,150),'',unreal.MaterialProperty.MP_ROUGHNESS)
    lib.connect_material_property(constant(m,.12,0,250),'',unreal.MaterialProperty.MP_SPECULAR)
    assert all(lib.get_inputs_for_material_expression(m,custom));lib.recompile_material(m)
    paths.append(m.get_path_name().split('.')[0])
for path in paths:assert unreal.EditorAssetLibrary.save_asset(path,False),path
(OUT/'ImportAudit.json').write_text(json.dumps({'assets':paths,'meshes':len(catalog),'ground_shader_max_samples':5,'original_textures_reused':True},indent=2)+'\n')
(ROOT/'Art/HealingHouse/QualityV3/GroundBlend.hlsl').write_text(GROUND_CODE.strip()+'\n')
unreal.log('QUALITY_V3_IMPORT_PASSED')
