"""Fine, bounded soil wear and organic edge breakup. No route or mesh edits."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';L=unreal.MaterialEditingLibrary;assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for family in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_'+family);changed=[]
 for n in unreal.ObjectIterator(unreal.MaterialExpressionCustom):
  if n.get_outer()!=m:continue
  code=n.get_editor_property('code');old=code
  if n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3:
   needle='if(Mode<1.5)return d;';assert needle in code
   code=code.replace(needle,'''float useWear=localPaint*(1-smoothstep(.12,.72,abs(UV.y*2-1)));d*=1+.032*useWear;
float edgeVegetation=localPaint*smoothstep(.52,.96,abs(UV.y*2-1));float fleck=smoothstep(.15,.85,.5+.25*sin(p.x*.083+p.y*.051)+.25*cos(p.y*.097-p.x*.067));
if(Mode>1.5 && Mode<2.5)d=lerp(d,g,edgeVegetation*fleck*.30);
if(Mode<1.5)return d;''')
  elif family in ['HealingPath','LegacyApproach']:
   needle='float edge=abs(UV.y*2-1)+irregular;' if family=='HealingPath' else 'float e=abs(UV.y*2-1)+'
   if family=='HealingPath':code=code.replace(needle,'irregular+=art*(.019*sin(p.x*.143+p.y*.097)+.013*cos(p.y*.177-p.x*.109));'+needle)
   else:code=code.replace(needle,'float e=art*(.019*sin(p.x*.143+p.y*.097)+.013*cos(p.y*.177-p.x*.109))+abs(UV.y*2-1)+')
  elif family=='HealingForecourt':code=code.replace('float2 a=float2(-4050,460)', 'r+=.014*sin(P.x*.143+P.y*.097)+.012*cos(P.y*.177-P.x*.109);float2 a=float2(-4050,460)')
  if code!=old:n.set_editor_property('code',code);changed.append({'before':old,'after':code})
 assert changed;L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);rows.append({'material':m.get_path_name(),'changes':changed})
(S/'GroundRefinement.json').write_text(json.dumps(rows,indent=2))
