import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/MeshyGlumandaV1';bpy.ops.wm.open_mainfile(filepath=str(A/'Source/Glumanda_Meshy_V1.blend'));s=bpy.context.scene;s.world=bpy.data.worlds.new('ReviewWorld');s.world.color=(.18,.18,.18);s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100
for loc,energy in [((1,-2,3),180),((-2,-1,2),100),((1,2,2),200)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=energy;o.data.size=3;o.rotation_euler=(Vector((0,0,.3))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(1,-2,.9));c=bpy.context.object;c.rotation_euler=(Vector((0,0,.3))-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=.85;s.camera=c;rig=bpy.data.objects['Glumanda_Meshy_Rig']
for name,frame in [('Idle',1),('Walk',5),('Run',5),('Faint',25)]:
 rig.animation_data.action=bpy.data.actions['Glumanda_'+name];s.frame_set(frame);s.render.filepath=str(O/('Rig_'+name+'.png'));bpy.ops.render.render(write_still=True)
