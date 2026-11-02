"""Reuse proven fresh-process save/travel review in this task's own UserDir."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandIntegrationV1/RestartTravel.py';text=source.read_text().replace('WestlandIntegrationV1','WestlandVisualUpgradeV1').replace('NativeTour01','NativeTour02');text=text.replace("assert P.is_third_person_camera()", "assert P.get_test_speed_factor()==1;assert P.is_third_person_camera()")
exec(compile(text,str(source),'exec'),{'__name__':'__main__'})
