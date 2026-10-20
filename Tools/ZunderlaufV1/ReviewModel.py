import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Zunderlauf/Source/Zunderlauf_V1.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.render.resolution_x=1024;s.render.resolution_y=1024;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('ReviewWorld');s.world.use_nodes=True;bg=s.world.node_tree.nodes.new('ShaderNodeBackground');wo=s.world.node_tree.nodes.new('ShaderNodeOutputWorld');s.world.node_tree.links.new(bg.outputs[0],wo.inputs[0]);bg.inputs[0].default_value=(.18,.21,.25,1);bg.inputs[1].default_value=.45
for name,loc,power,size in [('Key',(-1,-1,1.6),35,1.1),('Fill',(1,-.5,.8),15,.9),('Rim',(0,1,1.3),35,.6)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.3))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Review');o=bpy.data.objects.new('Review',d);s.collection.objects.link(o);s.camera=o;d.type='ORTHO';d.ortho_scale=.85
out=R/'Saved/ZunderlaufV1/ModelReview';out.mkdir(parents=True,exist_ok=True)
for name,loc in [('Front',(0,-2,.6)),('Quarter',(1,-2,.9)),('Side',(2,0,.6)),('Back',(0,2,.8))]:
 o.location=loc;o.rotation_euler=(Vector((0,.05,.33))-o.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
