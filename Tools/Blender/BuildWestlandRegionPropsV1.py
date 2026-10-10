"""Reusable region props only; independent Blender process preserves live character scene."""
import bpy,math,random
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'Art/World/WestlandRegion';D.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for n,c in [('Stone',(.39,.43,.36,1)),('Wood',(.27,.15,.065,1)),('Iron',(.16,.18,.16,1))]:
 m=bpy.data.materials.new('WR_'+n);m.diffuse_color=c;m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=c;m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.9
parts=[]
def cube(p,size,mat='Stone',rot=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);a=bpy.context.object;a.scale=size
 if rot:a.rotation_euler=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);a.data.materials.append(bpy.data.materials['WR_'+mat]);parts.append(a);return a
def join(name):
 bpy.ops.object.select_all(action='DESELECT')
 for a in parts:a.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();a=bpy.context.object;a.name=name
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');parts.clear();return a
# Bridges run local X; feet and railings are separate from terrain.
for kind,length,width in [('StoneBridge',28,4),('WoodBridge',16,2.5)]:
 mat='Stone' if kind.startswith('Stone') else 'Wood'
 for i in range(int(length/.5)):
  x=-length/2+i*.5+.25;cube((x,0,-.12),(.51,width,.24),mat)
 for side in (-1,1):
  for i in range(int(length/2)+1):cube((-length/2+i*2,side*(width/2+.06),.48),(.19,.19,.96),mat)
  cube((0,side*(width/2+.06),.77),(length,.14,.18),mat)
  if mat=='Stone':
   for i in range(18):
    t=math.pi*i/17;x=6.1*math.cos(t);z=-3+2.9*math.sin(t)
    cube((x,side*1.6,z),(.75,.5,.65),mat,(0,math.pi/2-t,0))
 join('WR_'+kind)
# 4 m waterwheel, local disk plane XZ; axle along Y.
for i in range(16):
 t=2*math.pi*i/16
 cube((2*math.cos(t),0,2+2*math.sin(t)),(.46,1.1,.18),'Wood',(0,-t,0))
for side in (-.43,.43):
 for i in range(32):
  t=2*math.pi*i/32;cube((1.87*math.cos(t),side,2+1.87*math.sin(t)),(.38,.14,.16),'Wood',(0,math.pi/2-t,0))
for i in range(8):
 t=2*math.pi*i/8;cube((.95*math.cos(t),0,2+.95*math.sin(t)),(2,.22,.16),'Wood',(0,-t,0))
cube((0,0,2),(.34,1.35,.34),'Iron');join('WR_Waterwheel')
for side in (-1,1):
 for i in range(5):cube((side*1.65,0,.27+i*.49),(.7,.8,.5))
for i in range(11):
 t=math.pi*i/10;cube((1.65*math.cos(t),0,2.25+1.65*math.sin(t)),(.52,.85,.52),rot=(0,math.pi/2-t,0))
join('WR_RuinArch')
for i in range(6):cube((.025*math.sin(i),0,.25+i*.48),(.65,.65,.49))
join('WR_RuinColumn')
for name,radius,depth in [('StandingStone',.65,3.3),('Crag',2.7,3.5)]:
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(0,0,depth/2));a=bpy.context.object
 rng=random.Random(26)
 for v in a.data.vertices:
  v.co.x*=radius*rng.uniform(.8,1.12);v.co.y*=radius*.72*rng.uniform(.8,1.12);v.co.z*=depth/2*rng.uniform(.9,1.05)
 a.name='WR_'+name;a.data.materials.append(bpy.data.materials['WR_Stone']);parts.append(a);join(a.name)
# Source review layout offsets apply ONLY in the review collection, not exported shapes.
assets=[a for a in bpy.data.objects if a.type=='MESH'];review=bpy.data.collections.new('REVIEW');bpy.context.scene.collection.children.link(review)
for i,a in enumerate(assets):
 c=a.copy();c.data=a.data;review.objects.link(c);c.location=(i%3*32,i//3*12,0);c.name='Review_'+a.name
 a.hide_render=True;a.hide_set(True)
bpy.ops.object.camera_add(location=(50,-58,56));cam=bpy.context.object
from mathutils import Vector
cam.rotation_euler=(Vector((30,13,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=105;bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(30,-10,48));bpy.context.object.data.energy=180000;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=50
bpy.ops.object.light_add(type='SUN',rotation=(.45,-.3,-.4));bpy.context.object.data.energy=2.5
bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1500;s.render.resolution_y=900;s.render.resolution_percentage=100;s.world.color=(.35,.4,.45)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'WestlandRegion_PropsV1.blend'));s.render.filepath=str(R/'Saved/WestlandRegion/BlenderPropsReview.png');bpy.ops.render.render(write_still=True)
