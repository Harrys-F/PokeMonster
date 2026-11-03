"""Reduce diagnosed repeated bright wave bands; preserve surface geometry and masks."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert not(D/'WaterPolish.json').exists()
for name in ['Pond','Stream']:
 m=unreal.load_asset(ROOT+'/Materials/M_WOV_'+name)
 for n in ML.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code')
  if '(P.x-T*18)'in code:n.set_editor_property('code','float2 q=P.xy*.045;float a=q.x-T*.7+1.3*sin(q.y*.67+T*.13);float b=q.y*1.21+q.x*.46+T*.5+sin(q.x*.87);float amp=.65+.35*sin(P.x*.009+P.y*.013);return normalize(float3((sin(a)*.035+cos(b)*.012)*amp,(cos(a+b*.4)*.028+sin(b)*.012)*amp,1));')
  elif 'float4(col,wet'in code:n.set_editor_property('code',code.replace('wave*.010','wave*.004').replace('float3(.018,.031,.029)*glint','float3(.006,.010,.009)*glint'))
 ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
(D/'WaterPolish.json').write_text(json.dumps(dict(reason='Large repeated bright bands in genuine pond capture',preserved=['geometry','depth','surface_count','shore_masks','shading_models','collisions'],normal_amplitude='0.035/0.028 plus 0.012 irregular secondary waves',base_glint_reduced=True),indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
