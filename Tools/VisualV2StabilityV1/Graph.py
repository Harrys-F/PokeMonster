import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';sys.path.insert(0,str(R/'Tools/VisualV2MaterialFixV1'));from GraphAudit import graph
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if m and ('Oak'in m.get_name()or'Birch'in m.get_name()):
   row={'actor':a.get_actor_label(),'component':c.get_path_name(),'mesh':m.get_path_name(),'pos':c.get_world_location().to_tuple(),'slots':[]}
   for i,material in enumerate(c.get_materials()):
    master=material.get_base_material();row['slots'].append({'slot':i,'material':material.get_path_name(),'base':master.get_path_name(),'paint':str(unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(material,'Paint'))if isinstance(material,unreal.MaterialInstanceConstant)else None})
   rows.append(row)
paths={s['base']for r in rows for s in r['slots']};(D/'Graph.json').write_text(json.dumps({'trees':rows,'graphs':{p:graph(unreal.load_asset(p))for p in paths}},indent=2))
