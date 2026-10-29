"""Actual Blender source renders, not generated illustrations."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Raichu';D=R/'Saved/ProjectRefinement/ModelsV4/Blender';D.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Raichu_V4.blend'));s=bpy.context.scene
s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('RaichuReviewWorld');s.world.color=(.25,.25,.25);world=s.world;world.use_nodes=True;next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.3,.3,.3,1)
s.view_settings.view_transform='AgX'
for loc,power,size in [((2,-3,4),320,3),((-2,-1,2),180,2),((1,3,3),350,2)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,.4))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();c=bpy.context.object;s.camera=c;c.data.type='ORTHO';c.data.ortho_scale=1.18
for name,loc in [('Front',(.15,-2,.65)),('Back',(0,2,.65)),('Left',(-2,0,.65)),('Right',(2,0,.65)),('GameAngle',(1.8,-2.1,2.5))]:
 c.location=loc;c.rotation_euler=(Vector((.12,0,.41))-c.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(D/(name+'.png'));bpy.ops.render.render(write_still=True)
print('SOURCE_RENDERS_DONE')
