"""Bounded actual deformed-surface views. Still samples are not an optical motion approval."""
import bpy,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Raichu';D=R/'Saved/ProjectRefinement/ModelsV4/Blender/Motion';D.mkdir(parents=True,exist_ok=True);bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Raichu_V4.blend'));s=bpy.context.scene;rig=bpy.data.objects['Raichu_Rig'];s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=480;s.render.resolution_y=480;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('MotionReview');s.world.color=(.4,.4,.4)
for loc,power in [((2,-3,4),400),((-2,1,3),250)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=3;o.rotation_euler=(Vector((.15,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(1.8,-2.5,1.1));c=bpy.context.object;c.data.type='ORTHO';c.data.ortho_scale=1.5;c.rotation_euler=(Vector((.15,0,.4))-c.location).to_track_quat('-Z','Y').to_euler();s.camera=c
for name in (['Faint']if '--faint'in sys.argv else ['Walk','Run','Attack','Hit','Faint','Happy']):
 a=bpy.data.actions['Raichu_'+name];rig.animation_data.action=a;lo,hi=a.frame_range
 for k,t in enumerate([.0,.25,.5,.75,1.]):
  s.frame_set(round(lo+(hi-lo)*t));s.render.filepath=str(D/(name+'_'+str(k)+'.png'));bpy.ops.render.render(write_still=True)
print('MOTION_SURFACES_RENDERED')
