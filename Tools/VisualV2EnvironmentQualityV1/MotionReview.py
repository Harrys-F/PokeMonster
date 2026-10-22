"""Short actual-camera motion-blur sequence; never counted as performance samples."""
import csv
import json
import time
import traceback
from pathlib import Path
import unreal

R = Path(unreal.Paths.project_dir()).resolve()
O = R / 'Saved/VisualV2EnvironmentQualityV1'
request = json.loads((O / 'MotionRequest.json').read_text())
condition = request['condition']
assert condition in ['Control', 'MotionBlurOff']
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world and 'Dev_TestMap_VisualV2EnvironmentQualityV1' in world.get_name()
player = unreal.GameplayStatics.get_player_pawn(world, 0)
controller = unreal.GameplayStatics.get_player_controller(world, 0)
subsystem = next(s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if s.get_world() == world)
move = next(a for a in unreal.ObjectIterator(unreal.InputAction) if a.get_outer() == player and a.get_name() == 'MoveAction')
label = 'VEQ1_MotionReview_' + condition
folder = O / 'Screenshots' / label
folder.mkdir(parents=True, exist_ok=False)
plan = O / (label + '.tsv')
assert not plan.exists()
plan.write_text(label + '\tPIE\t60\t1\nNPCWald\t' + condition + '\t1\t2560\t1440\t2\t100\n')
unreal.SystemLibrary.execute_console_command(world, 'pm.EnvPerf.Run ' + str(plan))
elapsed = 0.0
records = []
shot_index = 0


def inject(x, y):
    subsystem.inject_input_vector_for_action(move, unreal.Vector(x, y, 0), [], [])


def finish(error=None):
    inject(0, 0)
    unreal.unregister_slate_post_tick_callback(unreal._visualenv_motion)
    del unreal._visualenv_motion
    unreal.SystemLibrary.execute_console_command(world, 'pm.EnvPerf.Stop')
    (folder / 'Sequence.json').write_text(json.dumps({
        'condition': condition, 'error': error, 'frames': records,
        'purpose': 'Motion review only. Canonical initial placement by existing probe; not the no-teleport foot test.',
        'native_probe_cancelled_before_timing': True,
    }, indent=2))


def tick(dt):
    global elapsed, shot_index
    try:
        elapsed += dt
        # Hold still for settling, then walk out and back using real Enhanced Input.
        direction = 1 if 2 <= elapsed < 4 else -1 if 4 <= elapsed < 6 else 0
        inject(0, direction)
        if shot_index < 13 and elapsed >= 1 + .5 * shot_index:
            path = folder / (str(shot_index).zfill(2) + '.png')
            unreal.SystemLibrary.execute_console_command(world, 'Shot filename=' + str(path), controller)
            camera = controller.player_camera_manager
            records.append({'image': str(path), 'game_seconds': elapsed,
                            'player': player.get_actor_location().to_tuple(),
                            'velocity': player.get_velocity().to_tuple(),
                            'camera': camera.get_camera_location().to_tuple(),
                            'rotation': camera.get_camera_rotation().to_tuple(),
                            'viewport': list(controller.get_viewport_size())})
            shot_index += 1
        if elapsed > 7.4:
            finish()
    except Exception:
        finish(traceback.format_exc())


unreal._visualenv_motion = unreal.register_slate_post_tick_callback(tick)
