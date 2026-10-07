"""Read-only Blender review renders and camera registration; never saves source."""
import bpy,math,json,os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer');OUT=R.parents[2]/'Saved/YoungTrainerHeadFormV5/Review';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V5.blend'));s=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=s
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=64;s.render.film_transparent=True;s.render.resolution_x=600;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
cam=bpy.data.objects['YT5_FormReview_Front'];s.camera=cam;cam.data.type='ORTHO';cam.data.sensor_fit='VERTICAL';cam.data.ortho_scale=1.62
for o in bpy.data.collections['YT_ReviewOnly'].objects:
 if o.type=='LIGHT':o.hide_render=True
for name,power,loc,size,color in [('V5_ReviewKey',180,(-2,-3,4),2.4,(1,.90,.79)),('V5_ReviewFill',125,(2,-2,2.5),2.5,(.80,.87,1)),('V5_ReviewRim',130,(0,3,3),2.0,(1,.90,.80))]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.7))-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.size=size;d.color=color

def aim(az,elev,center=(0,0,.70),distance=4):
 a=math.radians(az);e=math.radians(elev);c=Vector(center);cam.location=c+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*distance;cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
views=[('Front',0),('FrontRight',-45),('Right',-90),('BackRight',-135),('Back',180),('BackLeft',135),('Left',90),('FrontLeft',45)]
registration={}
for name,az in ([] if os.getenv('YT5_HEAD_ONLY') else views):
 aim(az,0);s.render.filepath=str(OUT/('V5_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name)
 lo=world_to_camera_view(s,cam,Vector((0,0,0)));hi=world_to_camera_view(s,cam,Vector((0,0,1.4)));registration[name]={'sole_y_px':(1-lo.y)*900,'crown_y_px':(1-hi.y)*900,'axis_x_px':lo.x*600,'m_per_px':1.4/((hi.y-lo.y)*900)};print('VIEW',name,flush=True)
# Actual Blender RIGHT orthographic (+X) matches the sheet's LEFT profile.
registration['RightOrtho']=registration.get('Left',{});s.render.filepath=str(OUT/'V5_RightOrtho.png');aim(90,0)
if not os.getenv('YT5_HEAD_ONLY'):bpy.ops.render.render(write_still=True,scene=s.name)
cam.data.type='PERSP';cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.lens=36/(2*math.tan(math.radians(35)/2))
for name,az,elev,dist in ([] if os.getenv('YT5_HEAD_ONLY') else [('GamePerspective',-45,35,3.4),('GameFront',0,35,3.4),('GameBack',180,35,3.4)]):
 aim(az,elev,distance=dist);s.render.filepath=str(OUT/('V5_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name);print('GAME',name,flush=True)
# All eight elevated views use the same inspection camera, not an Unreal runtime camera.
for name,az in ([] if os.getenv('YT5_HEAD_ONLY') else views):
 aim(az,35,distance=3.4);s.render.filepath=str(OUT/('V5_Game_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name);print('GAME_DIRECTION',name,flush=True)
cam.data.type='ORTHO';cam.data.ortho_scale=.45;s.render.resolution_x=700;s.render.resolution_y=700
for name,az in [('HeadFront',0),('HeadQuarter',-45),('HeadRight',90),('HeadBack',180)]:
 aim(az,0,(0,.02,1.21));s.render.filepath=str(OUT/('V5_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=s.name);print('HEAD',name,flush=True)
cam.data.ortho_scale=.52;s.render.resolution_x=900;s.render.resolution_y=600;aim(-30,40,(0,-.05,.11));s.render.filepath=str(OUT/'V5_BareFeet.png')
if not os.getenv('YT5_HEAD_ONLY'):bpy.ops.render.render(write_still=True,scene=s.name)
(OUT/('HeadRegistration.json' if os.getenv('YT5_HEAD_ONLY') else 'Registration.json')).write_text(json.dumps(registration,indent=2)+'\n');print('V5_REVIEW_COMPLETE',flush=True)
