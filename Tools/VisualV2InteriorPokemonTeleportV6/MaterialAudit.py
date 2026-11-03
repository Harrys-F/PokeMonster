import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';out={}
for row in json.loads((D/'ImportedModels.json').read_text()):
 n=row['target'].split(':')[1];m=unreal.load_asset(row['materials'][0]);out[n]=dict(parent=m.parent.get_path_name(),texture=m.get_editor_property('texture_parameter_values').export_text()if hasattr(m.get_editor_property('texture_parameter_values'),'export_text')else[str(v)for v in m.get_editor_property('texture_parameter_values')],scalars=[str(v)for v in m.get_editor_property('scalar_parameter_values')],vectors=[str(v)for v in m.get_editor_property('vector_parameter_values')],textures=[])
 for obj in row['objects']:
  if obj['kind']=='Texture2D':
   t=unreal.load_asset(obj['path']);out[n]['textures'].append(dict(path=t.get_path_name(),srgb=t.srgb,compression=str(t.compression_settings)))
(D/('MaterialAuditAfter.json'if(D/'TextureRoleCorrection.json').exists()else'MaterialAudit.json')).write_text(json.dumps(out,indent=2))
