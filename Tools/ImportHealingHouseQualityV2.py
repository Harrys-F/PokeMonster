"""Create own painterly quality materials and revised forms. No V1 asset reimport.
Westland ground textures/cluster meshes use an independent reusable namespace.
"""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();H='/Game/Environment/HealingHouse/QualityV2';W='/Game/Environment/Westland/NaturalGroundV1';tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
def wire(source,output,destination,input_name):
 assert lib.connect_material_expressions(source,output,destination,input_name),(source.get_name(),destination.get_name(),input_name)

textures={};paths=[]
for name in ['Wood','Stone','Plaster','Cloth','Grass','Earth']:
 ground=name in ('Grass','Earth');dest=W if ground else H;prefix='T_WL_Painted' if ground else 'T_HH_Painted';file=ROOT/('Art/Environment/Westland/NaturalGroundV1/Textures' if ground else 'Art/HealingHouse/Textures/QualityV2')/(prefix+name+'.png');path=dest+'/Textures/'+prefix+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  task=unreal.AssetImportTask();task.filename=str(file);task.destination_path=dest+'/Textures';task.destination_name=prefix+name;task.automated=True;task.save=False;tools.import_asset_tasks([task])
 t=unreal.load_asset(path);assert t;t.set_editor_property('srgb',True);t.set_editor_property('max_texture_size',1024);t.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);textures[name]=t;paths.append(path)
materials={}
def mat(name,texture,tint,scale=1,world=False):
 ground=name in ('Grass','Earth','GrassLeaf0','GrassLeaf1','GrassLeaf2','FlowerCream');dest=W if ground else H;prefix='M_WL_NG_' if ground else 'M_HH_Q2_';path=dest+'/Materials/'+prefix+name
 m=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset(prefix+name,dest+'/Materials',unreal.Material,unreal.MaterialFactoryNew());lib.delete_all_material_expressions(m);m.set_editor_property('two_sided',name.startswith(('GrassLeaf','Flower')))
 color=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-300,0);color.constant=unreal.LinearColor(*tint,1)
 if texture:
  sample=lib.create_material_expression(m,unreal.MaterialExpressionTextureSample,-500,150);sample.texture=textures[texture];sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
  if world:
   pos=lib.create_material_expression(m,unreal.MaterialExpressionWorldPosition,-1000,300);mask=lib.create_material_expression(m,unreal.MaterialExpressionComponentMask,-820,300);mask.set_editor_property('r',True);mask.set_editor_property('g',True);wire(pos,'',mask,'');mul=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-670,300);mul.set_editor_property('const_b',scale);wire(mask,'',mul,'A');wire(mul,'',sample,'UVs')
  else:
   uv=lib.create_material_expression(m,unreal.MaterialExpressionTextureCoordinate,-750,150);uv.set_editor_property('u_tiling',scale);uv.set_editor_property('v_tiling',scale);wire(uv,'',sample,'UVs')
  mix=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-120,0)
  if name=='Grass':
   desat=lib.create_material_expression(m,unreal.MaterialExpressionDesaturation,-320,200);fraction=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-520,300);fraction.r=.25;wire(sample,'RGB',desat,'');wire(fraction,'',desat,'Fraction');wire(desat,'',mix,'A')
  elif texture=='Cloth':
   base=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-480,420);base.constant=unreal.LinearColor(*((.43,.42,.33) if name=='Linen' else (.20,.28,.12)),1);blend=lib.create_material_expression(m,unreal.MaterialExpressionLinearInterpolate,-300,250);blend.set_editor_property('const_alpha',.22);wire(base,'',blend,'A');wire(sample,'RGB',blend,'B');wire(blend,'',mix,'A')
  else:wire(sample,'RGB',mix,'A')
  wire(color,'',mix,'B');lib.connect_material_property(mix,'',unreal.MaterialProperty.MP_BASE_COLOR)
 else:lib.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
 r=lib.create_material_expression(m,unreal.MaterialExpressionConstant,0,160);r.r=.88 if ground else .80;lib.connect_material_property(r,'',unreal.MaterialProperty.MP_ROUGHNESS)
 s=lib.create_material_expression(m,unreal.MaterialExpressionConstant,0,260);s.r=.12;lib.connect_material_property(s,'',unreal.MaterialProperty.MP_SPECULAR)
 lib.delete_unused_expressions(m);lib.recompile_material(m);materials[name]=m;paths.append(path);return m
for name,tex,tint in [('Wood','Wood',(.92,.82,.71)),('Timber','Wood',(.48,.42,.35)),('WoodLight','Wood',(.98,.88,.76)),('WoodDark','Wood',(.88,.79,.69)),('Stone','Stone',(.88,.82,.75)),('Plaster','Plaster',(1.0,.98,.92)),('Sage','Cloth',(.9,1,.82)),('Linen','Cloth',(1.25,1.12,.86))]:mat(name,tex,tint)
mat('Grass','Grass',(.66,.72,.62),1/190,True);mat('Earth','Earth',(.86,.80,.73),1/220,True)
for i,c in enumerate(((.08,.14,.047),(.13,.20,.07),(.21,.25,.09))):mat('GrassLeaf'+str(i),None,c)
mat('FlowerCream',None,(.72,.58,.32))
cat=json.loads((ROOT/'Art/HealingHouse/QualityV2/Props.json').read_text());meshed=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for name,p in cat.items():
 dest=W if p['ground'] else H;prefix='SM_WL_NG_' if p['ground'] else 'SM_HH_Q2_';path=dest+'/Meshes/'+prefix+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
  for k,v in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(k,v)
  t=unreal.AssetImportTask();t.filename=str(ROOT/('Art/Environment/Westland/NaturalGroundV1/Exports' if p['ground'] else 'Art/HealingHouse/Exports/QualityV2')/(prefix+name+'.fbx'));t.destination_path=dest+'/Meshes';t.destination_name=prefix+name;t.options=ui;t.automated=True;t.save=False;tools.import_asset_tasks([t])
 mesh=unreal.load_asset(path);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.get_editor_property('imported_material_slot_name')).removeprefix('HH_Art_');m=materials.get(key) or unreal.load_asset('/Game/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_'+key);assert m,key;mesh.set_material(i,m)
 if name in ('Bench','Fireplace') and meshed.get_simple_collision_count(mesh)==0:meshed.add_simple_collisions(mesh,unreal.ScriptingCollisionShapeType.BOX)
 mesh.set_editor_property('light_map_resolution',64);paths.append(path)
for path in paths:assert unreal.EditorAssetLibrary.save_asset(path,False),path
out=ROOT/'Saved/HealingQualityV2';out.mkdir(parents=True,exist_ok=True);(out/'ImportAudit.json').write_text(json.dumps({'assets':paths},indent=2));unreal.log('ART_QUALITY_V2_IMPORT_PASSED')
