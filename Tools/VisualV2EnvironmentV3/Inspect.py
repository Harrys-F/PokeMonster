"""Read-only VisualV2 composition and material-source audit."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/EnvironmentV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
p=D/'BeforeScene.json';assert not p.exists();p.write_text(json.dumps(scene(W),indent=2))
rows=[];mats={}
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:continue
  ms=[c.get_material(i) for i in range(c.get_num_materials())]
  rows.append({'actor':a.get_name(),'label':a.get_actor_label(),'component':c.get_name(),'mesh':c.static_mesh.get_path_name(),'materials':[m.get_path_name() if m else None for m in ms],'pos':c.get_world_location().to_tuple(),'bounds':[v.to_tuple() for v in a.get_actor_bounds(False)],'count':c.get_instance_count() if isinstance(c,unreal.InstancedStaticMeshComponent)else 1})
  for m in ms:
   if not m or m.get_path_name() in mats:continue
   entry={'class':m.get_class().get_name()}
   if isinstance(m,unreal.Material):
    entry['nodes']=[]
    for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
     v={'name':n.get_name(),'class':n.get_class().get_name()}
     for prop in ['code','parameter_name','default_value','constant','texture','value']:
      try:
       x=n.get_editor_property(prop);v[prop]=x.get_path_name()if isinstance(x,unreal.Object)else str(x)
      except Exception:pass
     entry['nodes'].append(v)
   elif isinstance(m,unreal.MaterialInstanceConstant):
    entry['parent']=m.parent.get_path_name();entry['scalars']=str(m.get_editor_property('scalar_parameter_values'));entry['vectors']=str(m.get_editor_property('vector_parameter_values'))
   mats[m.get_path_name()]=entry
(D/'Inventory.json').write_text(json.dumps({'components':rows,'materials':mats},indent=2));unreal.log('ENV3_INSPECT_COMPLETE '+str(len(rows)))
