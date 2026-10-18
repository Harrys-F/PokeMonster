"""Same input/capture review, with AA obtained solely from the saved map blendable."""
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();source=(R/'Tools/VisualV2TAAIntegrationV1/StartMotion.py').read_text().replace("w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1'","w.get_name()=='Dev_TestMap_VisualV2'");old="unreal.SystemLibrary.execute_console_command(w,'r.AntiAliasingMethod '+str(j['aa']));";assert old in source;source=source.replace(old,"")
exec(compile(source,'actual_map_motion_without_aa_console_override','exec'),globals())
