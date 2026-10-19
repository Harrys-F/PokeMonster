import unreal,json
from pathlib import Path
S=Path(unreal.Paths.project_dir())/'Saved/VisualV2HealingArtV3';rows=[]
for name in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 m=unreal.load_asset('/Game/Environment/VisualV2WorldArtV2/Materials/M_WAQ2_'+name)
 rows.append({'name':name,'expressions':[{'type':n.get_class().get_name(),'code':n.get_editor_property('code') if isinstance(n,unreal.MaterialExpressionCustom) else ''} for n in unreal.ObjectIterator(unreal.MaterialExpression) if n.get_outer()==m]})
(S/'GroundGraphs.json').write_text(json.dumps(rows,indent=2))
