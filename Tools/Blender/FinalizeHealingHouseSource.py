"""Background Blender only: turn the scene-library export into a normal .blend.

Run with Blender -b Art/HealingHouse/Source/HealingHouse_V1.blend --python this_file.
This must not run in the user's live Blender session.
"""
import bpy
from pathlib import Path

if not bpy.app.background:
    raise RuntimeError('Use a separate background process to preserve the live scene.')
source = Path(__file__).resolve().parents[2] / 'Art/HealingHouse/Source/HealingHouse_V1.blend'
scene = bpy.data.scenes.get('HealingHouse_V1')
if not scene:
    with bpy.data.libraries.load(str(source), link=False) as (src, dst):
        dst.scenes = ['HealingHouse_V1']
    scene = dst.scenes[0]
bpy.context.window.scene = scene
for other in list(bpy.data.scenes):
    if other != scene: bpy.data.scenes.remove(other)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(source))
