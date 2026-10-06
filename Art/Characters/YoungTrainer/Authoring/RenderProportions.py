"""Read-only native orthographic gray/silhouette review of V1 and V2.
No animation, material editing, rig editing or file saves.
"""
import bpy,math
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
OUT=ROOT.parents[2]/'Saved/YoungTrainerProportions/Review';OUT.mkdir(parents=True,exist_ok=True)
views=[('Front',0,0),('FrontRight',-45,0),('Right',-90,0),('BackRight',-135,0),('Back',180,0),('BackLeft',135,0),('Left',90,0),('FrontLeft',45,0),('GameFront',0,40),('GameBack',180,40),('GameReferenceFront',0,30),('GameReferenceBack',180,30)]
for version,file in [('V1','YoungTrainer_Reference_V1.blend'),('V2','YoungTrainer_Proportions_V2.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Source'/file));scene=bpy.data.scenes['YoungTrainer_Reference_V1']
 if bpy.context.window:bpy.context.window.scene=scene
 scene.render.engine='BLENDER_WORKBENCH';scene.render.film_transparent=True
 scene.render.resolution_x=640;scene.render.resolution_y=800;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
 scene.display.shading.light='STUDIO';scene.display.shading.color_type='SINGLE';scene.display.shading.single_color=(.52,.52,.52)
 scene.display.shading.show_shadows=False;scene.display.shading.show_cavity=False;scene.display.shading.show_specular_highlight=False
 camera=bpy.data.objects['YT_ReviewFront'];scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=1.60
 for name,az,elev in views:
  a=math.radians(az);e=math.radians(elev);target=Vector((0,0,.7));camera.location=target+Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*4
  camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(version+'_Gray_'+name+'.png'))
  bpy.ops.render.render(write_still=True,scene=scene.name);print('GRAY_REVIEW',version,name,flush=True)
  if version=='V2':
   scene.display.shading.light='FLAT';scene.display.shading.single_color=(0,0,0);scene.render.filepath=str(OUT/(version+'_Silhouette_'+name+'.png'));bpy.ops.render.render(write_still=True,scene=scene.name)
   scene.display.shading.light='STUDIO';scene.display.shading.single_color=(.52,.52,.52)
 print('VERSION_RENDERED',version,flush=True)
print('PROPORTION_REVIEW_COMPLETE',flush=True)
