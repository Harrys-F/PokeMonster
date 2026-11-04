"""Five matched final room views after the small visual floor connector."""
from pathlib import Path
import unreal
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()if E else None
if not W:W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0))
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if a.get_actor_label()=='WVI_Healer_VestibuleFloor');c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and c.get_instance_count()==1 and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;assert c.is_visible()
R=Path(unreal.Paths.project_dir()).resolve();source=R/'Tools/WestlandVisualV2IntegrationV1/Views.py';s=source.read_text().replace('def run():',"cases[:]=[c for c in cases if c[0].startswith('Heilhaus')]\ndef run():");exec(compile(s,str(source),'exec'),{'__name__':'__main__'})
