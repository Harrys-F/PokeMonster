"""Import new reusable props/materials only. Run in the existing Unreal editor.
No existing mesh/material is reimported or modified. Scene dressing is separate.
"""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();ART=ROOT/'Art/HealingHouse';DEST='/Game/Environment/HealingHouse/ExpandedArtV1'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
catalog=json.loads((ART/'ExpandedArtV1/Props.json').read_text());colors={'Wood':(.29,.145,.058),'Timber':(.095,.044,.018),'Plaster':(.66,.52,.34),'Stone':(.29,.265,.22),'Mortar':(.12,.10,.075),'Sage':(.15,.245,.105),'Linen':(.58,.49,.31),'Gold':(.54,.34,.10),'Metal':(.045,.052,.032),'Leaf':(.105,.22,.075),'LeafLight':(.23,.34,.105),'Flower':(.49,.235,.22),'Ceramic':(.39,.215,.11),'Glass':(.11,.26,.20),'Book':(.16,.20,.26),'Paper':(.63,.55,.35),'Fire':(1,.235,.018),'Window':(.40,.50,.34)}
factors={'Wood':.67,'Timber':.7,'Sage':.6,'Stone':.8,'Plaster':.86,'Gold':.65,'Linen':.78,'Leaf':.8,'LeafLight':.75}
colors={n:tuple(c*factors.get(n,1) for c in rgb) for n,rgb in colors.items()}
created=[]
texpath=DEST+'/Textures/T_HH_Art_Surface'
task=unreal.AssetImportTask();task.filename=str(ART/'Textures/ExpandedArtV1/T_HH_Art_Surface.png');task.destination_path=DEST+'/Textures';task.automated=True;task.replace_existing=True;task.save=False;tools.import_asset_tasks([task]);texture=unreal.load_asset(texpath);assert texture
texture.set_editor_property('srgb',False);created.append(texpath)
materials={}
for name,color in colors.items():
 path=DEST+'/Materials/M_HH_Art_'+name
 m=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset('M_HH_Art_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew());lib.delete_all_material_expressions(m);tint=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-500,0);tint.constant=unreal.LinearColor(*color,1)
 if name in ('Wood','Timber','Plaster','Stone','Sage','Linen'):
  sample=lib.create_material_expression(m,unreal.MaterialExpressionTextureSample,-700,160);sample.texture=texture;sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
  mul=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-280,0);lib.connect_material_expressions(tint,'',mul,'A');lib.connect_material_expressions(sample,'RGB',mul,'B');lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
 else:lib.connect_material_property(tint,'',unreal.MaterialProperty.MP_BASE_COLOR)
 rough=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-200,210);rough.r=.84;lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
 spec=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-200,300);spec.r=.10;lib.connect_material_property(spec,'',unreal.MaterialProperty.MP_SPECULAR)
 if name in ('Fire','Window'):
  emission=lib.create_material_expression(m,unreal.MaterialExpressionMultiply,-200,-180);emission.set_editor_property('const_b',2 if name=='Fire' else .2);lib.connect_material_expressions(tint,'',emission,'A');lib.connect_material_property(emission,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 lib.recompile_material(m);materials[name]=m;created.append(path)
tasks=[]
for name,entry in catalog.items():
 path=DEST+'/Meshes/SM_HH_Art_'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(path)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for prop,value in {'combine_meshes':True,'auto_generate_collision':False,'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,'convert_scene':True,'convert_scene_unit':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(prop,value)
 t=unreal.AssetImportTask();t.filename=str(ART/'Exports/ExpandedArtV1'/('SM_HH_Art_'+name+'.fbx'));t.destination_path=DEST+'/Meshes';t.destination_name='SM_HH_Art_'+name;t.automated=True;t.save=False;t.options=ui;tasks.append(t)
tools.import_asset_tasks(tasks)
meshed=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);audit=[]
for name,entry in catalog.items():
 path=DEST+'/Meshes/SM_HH_Art_'+name;mesh=unreal.load_asset(path);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.get_editor_property('imported_material_slot_name')).removeprefix('HH_Art_');assert key in materials,(name,key);mesh.set_material(i,materials[key])
 b=mesh.get_bounding_box();size=b.max-b.min
 assert all(abs(a-v)<.2 for a,v in zip((size.x,size.y,size.z),entry['size_cm'])),(name,size,entry['size_cm'])
 if name in ('WindowWall2m','Bench','Table','Fireplace'):
  meshed.add_simple_collisions(mesh,unreal.ScriptingCollisionShapeType.BOX)
 mesh.set_editor_property('light_map_resolution',64)
 mesh.get_editor_property('asset_import_data').scripted_add_filename(str(ART/'Exports/ExpandedArtV1'/('SM_HH_Art_'+name+'.fbx')),0,'')
 created.append(path);audit.append({'name':name,'bounds_min':[b.min.x,b.min.y,b.min.z],'bounds_max':[b.max.x,b.max.y,b.max.z],'triangles':entry['triangles']})
for path in created:unreal.EditorAssetLibrary.save_asset(path,only_if_is_dirty=False)
out=ROOT/'Saved/HealingArt';out.mkdir(parents=True,exist_ok=True);(out/'ImportAudit.json').write_text(json.dumps({'assets':created,'meshes':audit},indent=2))
unreal.log('HH_EXPANDED_ART_IMPORT_PASSED')
