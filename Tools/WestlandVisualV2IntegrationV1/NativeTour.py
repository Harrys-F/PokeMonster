"""Full existing regional circuit; factor3 outside, regular speed at the pre-existing relocated doorway."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandIntegrationV1/FootTour.py';text=source.read_text().replace('WestlandIntegrationV1','WestlandVisualV2IntegrationV1');assert 'assert cm.max_walk_speed in [210,315]'in text;text=text.replace('assert cm.max_walk_speed in [210,315]','assert cm.max_walk_speed in [210*p.get_test_speed_factor(),315*p.get_test_speed_factor()]');text=text.replace('Software Shift input, no speed override','Software Shift input; pm.Speed3 outside, pm.Speed1 at the existing relocated doorway')
text=text.replace("if not error:\n  pc.toggle_main_menu()","if not error:\n  unreal.SystemLibrary.execute_console_command(w,'pm.Speed 1',pc);assert p.get_test_speed_factor()==1\n  pc.toggle_main_menu()")
text=text.replace("if kind in ['walk','close']:","if kind=='test_speed':\n   inject(0,0);unreal.SystemLibrary.execute_console_command(w,'pm.Speed '+str(target),pc);state['checks'].append({'check':label,'factor':p.get_test_speed_factor()});done()\n  elif kind in ['walk','close']:")
text=text.replace('if cut.is_viewer_relocated()==entering:','if cut.is_viewer_relocated()==entering and (p.get_actor_location()-door(cut,0,entering)).length()<1000:')
text=text.replace('inject(0,0);unreal.SystemLibrary.execute_console_command(w,\'pm.Input.Key LeftShift up\',pc);', 'inject(0,0);unreal.SystemLibrary.execute_console_command(w,\'csvprofile stop\',pc);unreal.SystemLibrary.execute_console_command(w,\'pm.Input.Key LeftShift up\',pc);')
text=text.replace("else:(OUT/'TourProgress.json').write_text(json.dumps(state,indent=2))","elif now-state.get('last_progress',0)>1:state['last_progress']=now;(OUT/'TourProgress.json').write_text(json.dumps(state,indent=2))")
ns={'__name__':'__main__'};exec(compile(text,str(source),'exec'),ns);route=ns['route']
i=next(i for i,r in enumerate(route)if r[1]=='Healing_front');route.insert(i,('test_speed','Regular speed at relocated door',1));i=next(i for i,r in enumerate(route)if r[1]=='Exterior_clear_door');route.insert(i+1,('test_speed','Restore outside test speed',3));unreal.SystemLibrary.execute_console_command(ns['w'],'pm.Speed 3',ns['pc']);assert ns['p'].get_test_speed_factor()==3

# Reuse all six existing regional route definitions, plus safe access to the two
# branches missing from the older circuit. Actual input only; no teleport.
route[:]=[r for r in route if r[0]!='shot']
ns['state']['screenshots']=[]
# Sample complete Waldpfad/eastern Muehlenrunde from the existing layout at the
# appropriate connected route end, rather than inventing new paths.

L=ns['L'];side=[]
for name,points in [('Muehlenrunde_East',L.PATHS[3][1][:5])]:
 for e,n in L.sample(points+list(reversed(points[:-1])),spacing=4):side.append(('walk',name,L.world(e,n)[:2]))
i=next(i for i,r in enumerate(route)if r[1]=='Meadow_front');route[i:i]=side
side=[];points=L.PATHS[4][1]
for e,n in L.sample(points+list(reversed(points[:-1])),spacing=4):side.append(('walk','Waldpfad_Full',L.world(e,n)[:2]))
i=next(i for i,r in enumerate(route)if r[1]=='Exit');route[i:i]=side
# CSV captures only the moving native session; no screenshots or video in this tour.
ns['state']['benchmark_note']='Full input-driven regional circuit, live clock/AI, dialogues/house transitions retained; no video or screenshots'
for command in ['pm.EnvPerf2.Viewport 2560 1440','r.GPUCsvStatsEnabled 1','r.VSync 0','t.MaxFPS 0','csvprofile start']:
 unreal.SystemLibrary.execute_console_command(ns['w'],command,ns['pc'])
