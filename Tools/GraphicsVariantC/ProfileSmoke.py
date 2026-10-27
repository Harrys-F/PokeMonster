"""Profile switching only; caller owns an isolated PIE session."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GraphicsVariantC';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and unreal._perf1_isolated
U=unreal.GameUserSettings.get_game_user_settings();C=unreal.SystemLibrary;checks=[]
for profile,percent in [(None,75),('100',100),('C',75)]:
 if profile:C.execute_console_command(W,'pm.Graphics '+profile)
 assert C.get_console_variable_float_value('r.ScreenPercentage')==percent
 assert (U.get_screen_resolution().x,U.get_screen_resolution().y)==(2560,1440)
 for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading','Landscape']:assert C.get_console_variable_int_value('sg.'+n+'Quality')==2
 checks.append({'profile':profile or 'unforced default','percentage':percent})
(D/(json.loads((D/'StateRequest.json').read_text())['label']+'-Smoke.json')).write_text(json.dumps({'passed':True,'checks':checks},indent=2))
