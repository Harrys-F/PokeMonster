import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();L=unreal.MaterialEditingLibrary;out={'property_api':hasattr(L,'get_material_property_input_node'),'materials':[]}
for path in ['/Game/Environment/VisualV2EnvironmentV3/Materials/M_EQ3_Stream','/Game/Environment/WestlandAssetLibrary/Materials/M_WLA_Painted','/Game/Environment/VisualV2WorldArtV5/Materials/M_WLA_Painted_Instanced']:
 m=unreal.load_asset(path);d={'path':path,'shading':str(m.get_editor_property('shading_model')),'blend':str(m.get_editor_property('blend_mode')),'nodes':[]}
 for n in L.get_material_expressions(m):
  v={'class':n.get_class().get_name(),'name':n.get_name()}
  for p in ['parameter_name','texture','code']:
   try:v[p]=str(n.get_editor_property(p))
   except Exception:pass
  d['nodes'].append(v)
 out['materials'].append(d)
(R/'Saved/ProjectRefinement/EnvironmentV3/SurfaceAudit.json').write_text(json.dumps(out,indent=2))
