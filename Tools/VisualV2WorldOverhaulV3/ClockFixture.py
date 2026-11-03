"""Bounded clock fixture in a newly captured isolated test save; normal loader applies it.
No protected Python properties, C++ changes, user slots or parallel clock. The
existing V11 GVAS SecondsOfDay double is replaced once, with strict tag guards.
"""
from pathlib import Path
import unreal,struct,json,hashlib

def set_hour(world,controller,save_subsystem,hour):
 root=Path(unreal.Paths.project_dir()).resolve()/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';storage=Path(unreal.Paths.project_saved_dir()).resolve();assert storage.is_relative_to(root)and world.get_name()=='Dev_TestMap_VisualV2'and 0<=hour<24
 if not controller.is_menu_open():controller.toggle_main_menu()
 assert controller.is_menu_open()and save_subsystem.save_current_game()
 slot=storage/'SaveGames/PokeMonster_Dev.sav';assert slot.is_file();clock=next(c for c in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if c.get_outer()==unreal.GameplayStatics.get_game_instance(world));assert clock.is_clock_paused()
 old=clock.get_time().seconds_of_day;raw=slot.read_bytes();assert raw[:4]==b'GVAS';tag=b'SecondsOfDay\0';assert raw.count(tag)==1;at=raw.index(tag);assert b'DoubleProperty\0'in raw[at:at+60]and b'PokeMonsterWorldTime\0'in raw[max(0,at-120):at]
 encoded=struct.pack('<d',old);assert raw.count(encoded)==1;value=raw.index(encoded);assert at<value<at+100;assert raw[value+8:value+17]==struct.pack('<i',5)+b'None\0';replacement=struct.pack('<d',float(hour*3600));changed=raw[:value]+replacement+raw[value+8:];assert len(changed)==len(raw);slot.write_bytes(changed)
 evidence=root/'ClockFixtureTransactions.jsonl'
 with evidence.open('a')as f:f.write(json.dumps(dict(slot=str(slot),field='PokeMonsterWorldTime.SecondsOfDay',offset=value,before=old,after=hour*3600,only_eight_serialized_bytes_replaced=True))+'\n')
 assert save_subsystem.load_game()
