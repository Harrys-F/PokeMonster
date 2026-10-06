"""Read-only native head and game-distance review. Saves images, never a blend."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=R.parents[2]/'Saved/YoungTrainerHeadPass/Review';OUT.mkdir(parents=True,exist_ok=True)
views=[('Front',0),('FrontRight',-45),('Right',-90),('BackRight',-135),('Back',180),('BackLeft',135),('Left',90),('FrontLeft',45)]
def aim(cam,az,elev,center,distance):
 a=math.radians(az);e=math.radians(elev);c=Vector(center)
 cam.location=c+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*distance
 cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
for version,file in [('V2','YoungTrainer_Proportions_V2.blend'),('V3','YoungTrainer_HeadHair_V3.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(R/'Source'/file));s=bpy.data.scenes['YoungTrainer_Reference_V1']
 if bpy.context.window:bpy.context.window.scene=s
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=64;s.render.film_transparent=True
 s.render.resolution_x=600;s.render.resolution_y=600;s.render.resolution_percentage=100
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
 cam=bpy.data.objects['YT_ReviewFront'];s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.46
 # Review studio only, identical between V2 and V3, never saved into either file.
 for name in ['YT_Key','YT_Fill','YT_Rim']:
  if name in bpy.data.objects:bpy.data.objects[name].hide_render=True
 for o in bpy.data.collections['YT_ReviewOnly'].objects:
  if o.type=='LIGHT':o.hide_render=True
 for name,position,power,size,color in [('HeadReviewKey',(-1,-1.5,2.7),65,1.3,(1,.90,.80)),('HeadReviewFill',(1.2,-1.0,1.6),35,1.5,(.80,.88,1)),('HeadReviewRim',(0,1.2,2),55,1.0,(1,.9,.79))]:
  d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=position
  o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.size=size;d.color=color
 for name,az in (views if version=='V3' else views[:2]):
  aim(cam,az,0,(0,.025,1.208),3);s.render.filepath=str(OUT/(version+'_Head_'+name+'.png'))
  bpy.ops.render.render(write_still=True,scene=s.name);print('HEAD',version,name,flush=True)
 if version=='V3':
  for name,az in views:
   aim(cam,az,55,(0,0,.70),25);cam.data.type='PERSP';cam.data.sensor_width=36;cam.data.lens=36/(2*math.tan(math.radians(35)/2));cam.data.sensor_fit='HORIZONTAL'
   s.render.resolution_x=1280;s.render.resolution_y=720;s.render.filepath=str(OUT/('V3_Game25m_'+name+'.png'))
   bpy.ops.render.render(write_still=True,scene=s.name);print('GAME_25M',name,flush=True)
  cam.data.type='ORTHO';cam.data.ortho_scale=1.60;s.render.resolution_x=640;s.render.resolution_y=800
  for name,az,elev in [('Front',0,0),('ThreeQuarter',-45,10),('GameFront',0,55),('GameQuarter',-45,55),('GameBack',180,55)]:
   aim(cam,az,elev,(0,0,.7),4);s.render.filepath=str(OUT/('V3_Full_'+name+'.png'))
   bpy.ops.render.render(write_still=True,scene=s.name);print('FULL',name,flush=True)
print('HEAD_HAIR_REVIEW_COMPLETE',flush=True)
