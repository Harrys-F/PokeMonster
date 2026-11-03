"""Own water only: reduce refractive high-frequency waves seen as far-shore stripes."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/MaterialHelpers.py')))
for name in ['Pond','Stream']:
 m=material(name);nodes=[n for n in ML.get_material_expressions(m)if isinstance(n,unreal.MaterialExpressionCustom)and 'return normalize(float3('in n.get_editor_property('code')];assert len(nodes)==1
 nodes[0].set_editor_property('code','float a=(P.x-T*18)*.035+sin(P.y*.023);float b=P.y*.043+P.x*.013+T*.29;return normalize(float3(.004*sin(a)+.002*cos(b),.006*cos(a*.7)+.003*sin(b),1));');finish(m)
save('WaterPolish.json',dict(rejected='Regular refractive ripple distortion along far pond shore',normal_amplitude_before=.025,normal_amplitude_after=.006,longer_waves=True))
