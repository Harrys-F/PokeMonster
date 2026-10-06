"""Native Blender review renders; never save changes to the source .blend.
Run background on the finished source. Rendered cameras are authoring previews,
not proof of imported/animated Unreal behaviour.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=ROOT.parents[2]/'Saved/YoungTrainerV1/Review';OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.data.scenes['YoungTrainer_Reference_V1']
if bpy.context.window:bpy.context.window.scene=scene
review=bpy.data.collections['YT_ReviewOnly'];arm=bpy.data.objects['YT_Rig']
for b in arm.pose.bones:b.rotation_mode='XYZ';b.rotation_euler=(0,0,0)
# Temporary studio ground only, no runtime/environment asset.
d=bpy.data.meshes.new('ReviewGround');d.from_pydata([(-200,-200,-.001),(200,-200,-.001),(200,200,-.001),(-200,200,-.001)],[],[(0,1,2,3)])
floor=bpy.data.objects.new('YT_RenderGround',d);review.objects.link(floor)
m=bpy.data.materials.new('YT_ReviewGroundMat');m.use_nodes=True
p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.043,.053,.049,1);p.inputs['Roughness'].default_value=1;d.materials.append(m)
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.render.resolution_percentage=100;scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=640;scene.render.resolution_y=800
scene.render.image_settings.color_mode='RGBA'
camera=bpy.data.objects['YT_ReviewFront'];scene.camera=camera
camera.data.type='ORTHO';camera.data.ortho_scale=1.63
records=[]
def render(name,az=0,elev=0,target=(0,0,.70),distance=4,ortho=1.63,rx=640,ry=800,perspective=False):
 a=math.radians(az);e=math.radians(elev);t=Vector(target)
 camera.location=t+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*distance
 camera.rotation_euler=(t-camera.location).to_track_quat('-Z','Y').to_euler()
 camera.data.type='PERSP' if perspective else 'ORTHO';camera.data.ortho_scale=ortho
 if perspective:camera.data.angle=math.radians(35);camera.data.clip_end=500
 scene.render.resolution_x=rx;scene.render.resolution_y=ry;scene.render.filepath=str(OUT/(name+'.png'))
 bpy.ops.render.render(write_still=True,scene=scene.name)
 records.append({'image':name+'.png','azimuth_deg':az,'elevation_deg':elev,'distance_m':distance,'projection':camera.data.type,'fov_horizontal_deg':35 if perspective else None,'ortho_vertical_m':ortho if not perspective else None})
 print('REVIEW_RENDERED',name,flush=True)
for az,name in [(0,'Front'),(45,'FrontRight'),(90,'Right'),(135,'BackRight'),(180,'Back'),(225,'BackLeft'),(270,'Left'),(315,'FrontLeft')]:render('Turnaround_'+name,az,0)
render('Portrait',0,4,target=(0,-.035,1.235),distance=2,ortho=.46,rx=800,ry=800)
for az,name in [(0,'Front'),(45,'FrontRight'),(90,'Right'),(135,'BackRight'),(180,'Back'),(225,'BackLeft'),(270,'Left'),(315,'FrontLeft')]:render('Elevated_'+name,az,40,ortho=1.65,rx=600,ry=720)
render('GameCamera_25m_Front',0,55,distance=25,perspective=True,rx=1920,ry=1080)
render('GameCamera_25m_Back',180,55,distance=25,perspective=True,rx=1920,ry=1080)
for name,angles in [('Stride',{'upperarm.L':(20,0,0),'upperarm.R':(-20,0,0),'thigh.L':(14,0,0),'thigh.R':(-14,0,0),'shin.R':(-16,0,0)}),('Interact',{'upperarm.L':(-18,0,0),'forearm.L':(-35,0,0),'head':(0,20,0)})]:
 for b in arm.pose.bones:b.rotation_euler=(0,0,0)
 for n,r in angles.items():arm.pose.bones[n].rotation_euler=[math.radians(x) for x in r]
 bpy.context.view_layer.update();render('Probe_'+name,35,20)
for b in arm.pose.bones:b.rotation_euler=(0,0,0)
bpy.context.view_layer.update()
(OUT/'Cameras.json').write_text(json.dumps(records,indent=2)+'\n')
print('REVIEW_COMPLETE',len(records),flush=True)
