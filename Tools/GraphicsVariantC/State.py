"""Read effective profile before any benchmark can override settings."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GraphicsVariantC';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world();assert W
GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);U=unreal.GameUserSettings.get_game_user_settings();q=json.loads((D/'StateRequest.json').read_text());p=D/(q['label']+'.json');assert not p.exists()
cv=['r.ScreenPercentage','r.TemporalAA.Upsampling','r.DynamicRes.OperationMode','r.SecondaryScreenPercentage.GameViewport','r.Editor.Viewport.OverridePIEScreenPercentage','r.VSync','t.MaxFPS']+['sg.'+n+'Quality'for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading','Landscape']]
res=U.get_screen_resolution()
r={'world':W.get_path_name(),'settings_resolution':(res.x,res.y),'settings_quality':U.get_overall_scalability_level(),'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in cv},'wall':time.time()};assert r['settings_resolution']==(2560,1440);assert r['cvars']['r.ScreenPercentage']==q.get('percentage',75);assert all(v==2 for n,v in r['cvars'].items()if n.startswith('sg.'));assert r['cvars']['r.TemporalAA.Upsampling']==1 and r['cvars']['r.DynamicRes.OperationMode']==0;p.write_text(json.dumps(r,indent=2));unreal.SystemLibrary.execute_console_command(W,'pm.Graphics status',PC)
