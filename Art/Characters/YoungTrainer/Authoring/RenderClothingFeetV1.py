"""Read-only identical-camera V6 / ClothingFeet renders; no source saves.

YT_CF_QUICK=1 makes Front, Game Front and a foot close-up for each version.
Default renders every requested orthographic, quarter and elevated view.
"""
import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];O=R.parents[2]/'Saved/YoungTrainerClothingFeetV1/Review';O.mkdir(exist_ok=True,parents=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_ClothingFeet_V1.blend'))
s=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=s
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=64;s.render.film_transparent=True
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
for o in bpy.data.collections['YT_ReviewOnly'].objects:
 if o.type=='LIGHT':o.hide_render=True
for name,power,loc,size,color in [('CF_ReviewKey',180,(-2,-3,4),2.4,(1,.90,.79)),('CF_ReviewFill',125,(2,-2,2.5),2.5,(.80,.87,1)),('CF_ReviewRim',130,(0,3,3),2,(1,.90,.80))]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.7))-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.size=size;d.color=color
cam=s.camera

def aim(az,elev,center=(0,0,.70),distance=4):
 a=math.radians(az);e=math.radians(elev);c=Vector(center);cam.location=c+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*distance;cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()

def render(prefix,name):
 s.render.filepath=str(O/(prefix+'_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name);print('VIEW',prefix,name,flush=True)
quick=bool(os.getenv('YT_CF_QUICK'));close_only=bool(os.getenv('YT_CF_CLOSE_ONLY'));registrations={}
allviews=[('Front',0),('FrontRight',-45),('Right',-90),('BackRight',-135),('Back',180),('BackLeft',135),('Left',90),('FrontLeft',45)]
for prefix,col in [('V6','YT6_Player'),('CF1','YTCF_Player')]:
 if os.getenv('YT_CF_VERSION') and prefix!=os.getenv('YT_CF_VERSION'):continue
 for name in ['YT6_Player','YTCF_Player']:
  bpy.data.collections[name].hide_render=name!=col;bpy.data.collections[name].hide_viewport=name!=col
 bpy.context.view_layer.update()
 cam.data.type='ORTHO';cam.data.sensor_fit='VERTICAL';cam.data.ortho_scale=1.62;s.render.resolution_x=600;s.render.resolution_y=900
 for name,az in ([] if close_only else allviews[:1] if quick else allviews+[('RightOrtho',90)]):
  aim(az,0);render(prefix,name)
  lo=world_to_camera_view(s,cam,Vector((0,0,0)));hi=world_to_camera_view(s,cam,Vector((0,0,1.4)))
  registrations[name]={'sole_y_px':(1-lo.y)*900,'crown_y_px':(1-hi.y)*900,'axis_x_px':lo.x*600,'m_per_px':1.4/((hi.y-lo.y)*900)}
 cam.data.type='PERSP';cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.lens=36/(2*math.tan(math.radians(35)/2))
 for name,az in ([] if close_only else allviews[:1] if quick else allviews):
  aim(az,35,distance=3.4);render(prefix,'Game_'+name)
 # Both feet and ankle/cuff transitions, using one unchanged camera across versions.
 cam.data.type='ORTHO';cam.data.sensor_fit='HORIZONTAL';cam.data.ortho_scale=.64;s.render.resolution_x=1000;s.render.resolution_y=760
 aim(-20,48,(0,-.060,.085));render(prefix,'BareFeet')
 if not quick:
  flags={o:o.hide_render for o in bpy.data.collections[col].objects if o.type=='MESH'}
  for o in flags:o.hide_render='BareFoot_' not in o.name
  bpy.context.view_layer.update();aim(0,90,(0,-.060,.080));render(prefix,'FeetTop')
  for o,flag in flags.items():o.hide_render=flag
  bpy.context.view_layer.update()
  cam.data.sensor_fit='VERTICAL';cam.data.ortho_scale=.74;s.render.resolution_x=850;s.render.resolution_y=850
  aim(-35,0,(0,-.025,.82));render(prefix,'ClothingClose')
if not close_only:(O/'Registration.json').write_text(json.dumps(registrations,indent=2)+'\n')
print('CLOTHING_FEET_REVIEW_COMPLETE',flush=True)
