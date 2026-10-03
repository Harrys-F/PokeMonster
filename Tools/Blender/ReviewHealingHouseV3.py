"""Background-only source finalization and architectural evidence renders.

The actual game-camera/PIE screenshots are separate, authoritative evidence.
Review lights/camera/ground belong only to this background process, never FBX.
"""
import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector

if not bpy.app.background:
    raise RuntimeError('Use background Blender; preserve the live scene.')
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'Art/HealingHouse'
SOURCE=ART/'Source/HealingHouse_V3.blend'
scene=bpy.data.scenes.get('HealingHouse_V3')
if not scene:
    with bpy.data.libraries.load(str(SOURCE),link=False) as (_,dst):
        dst.scenes=['HealingHouse_V3']
    scene=dst.scenes[0]
bpy.context.window.scene=scene
for other in list(bpy.data.scenes):
    if other!=scene: bpy.data.scenes.remove(other)
bpy.context.preferences.filepaths.save_version=0
# Read-only review process: source was already explicitly saved and reopened.

scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1440
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.world=bpy.data.worlds.new('V2_ReviewWorld')
scene.world.use_nodes=True
background=next(n for n in scene.world.node_tree.nodes if n.bl_idname=='ShaderNodeBackground')
background.inputs['Color'].default_value=(.48,.57,.65,1)
background.inputs['Strength'].default_value=.6

for name,location,energy,size in [('Key',(-10,-10,16),2200,9),('Fill',(8,-3,10),1200,8)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size
    light=bpy.data.objects.new(name,data);scene.collection.objects.link(light)
    light.location=location
    light.rotation_euler=(Vector((0,0,2))-light.location).to_track_quat('-Z','Y').to_euler()
groundmat=bpy.data.materials.new('ReviewGround');groundmat.diffuse_color=(.18,.24,.14,1)
bpy.ops.mesh.primitive_plane_add(size=50,location=(0,0,-.38))
bpy.context.object.data.materials.append(groundmat)
camera=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'))
scene.collection.objects.link(camera);scene.camera=camera
camera.data.type='PERSP';camera.data.angle=math.radians(35)
def shot(name,location,target,hide=()):
    for o in scene.objects:
        if o.name.startswith('HH_V2_'): o.hide_render=o.name.removeprefix('HH_V2_') in hide
    camera.location=location
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(ART/'Review/V3'/('Front' if '--' not in sys.argv else sys.argv[sys.argv.index('--')+1])/name)
    bpy.ops.render.render(write_still=True)
shot('Blender_Exterior.png',(-17,-18,18),(0,0,2.5))
shot('Blender_Porch.png',(-13,15,10),(-1,4,1.4))
shot('Blender_Interior.png',(-12,-12,16),(0,0,.6),
     ('Roof_Main','Roof_Trim','Roof_Entry','Roof_Porch','Gable_Front','Walls_Front',
      'Walls_CameraSide','Timber_Front','Timber_CameraSide','Stone_Front',
      'Stone_CameraSide','DoorFrame','DoorLeaf','Timber_Entry','Windows_Front',
      'Windows_CameraSide','Glass_Front','Glass_CameraSide','Windows_Loft',
      'Glass_Loft','Chimney','ChimneyCap','InteriorBeams_CameraSide'))
