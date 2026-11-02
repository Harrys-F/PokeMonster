"""Real regional foot route at pm.Speed 3, using the existing input/tour machinery."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandIntegrationV1/FootTour.py';text=source.read_text().replace('WestlandIntegrationV1','WestlandVisualUpgradeV1');assert 'assert cm.max_walk_speed in [210,315]'in text;text=text.replace('assert cm.max_walk_speed in [210,315]','assert cm.max_walk_speed in [630,945]');text=text.replace('Software Shift input, no speed override','Software Shift input with pm.Speed 3; no other speed override');text=text.replace("if not error:\n  pc.toggle_main_menu()","if not error:\n  unreal.SystemLibrary.execute_console_command(w,'pm.Speed 1',pc);assert p.get_test_speed_factor()==1\n  pc.toggle_main_menu()")
ns={'__name__':'__main__'};exec(compile(text,str(source),'exec'),ns)
# Replace only the QA route, before the first callback; production movement/AI/collision stay live.
route=ns['route'];route.clear();L=ns['L'];path=ns['path'];shot=ns['shot'];action=ns['action'];close=ns['close']
path('Guide',[(-300,-220),(-299,-217.1)]);close('Guide_approach',unreal.Vector(*L.world(-299,-217.1)));action('interact','Wanderer','WR_NPC_0');action('dialogue','Original_Wanderer_dialogue');action('menu','Inventory');action('sprint_on','Shift_at_factor3');path('Dorf_Wiese',L.MAIN[:13]);shot('Dorf_Wiese');path('Wald',L.MAIN[12:18]);shot('Waldruinen');path('Waldpfad',L.PATHS[4][1]);path('Wiese_Rueckweg',[(180,25),(125,10),(75,-25)]);path('Ufer',L.PATHS[5][1][:3]);shot('Flussufer')
unreal.SystemLibrary.execute_console_command(ns['w'],'pm.Speed 3',ns['pc']);assert ns['p'].get_test_speed_factor()==3
