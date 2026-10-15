import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V2'];bpy.context.window.scene=s
P=BASE/'Review/V2/Previews';P.mkdir(exist_ok=True,parents=True);cam=s.camera
# Only temporary preview-camera settings; the saved source is never changed here.
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
views=[('Hobbit_V2_Front',(0,-4,.66),(0,0,.66),'ORTHO',1.72,1200,1200),('Hobbit_V2_Back',(0,4,.66),(0,0,.66),'ORTHO',1.72,1200,1200),('Hobbit_V2_Side_Left',(-4,0,.66),(0,0,.66),'ORTHO',1.47,1200,1200),('Hobbit_V2_Side_Right',(4,0,.66),(0,0,.66),'ORTHO',1.47,1200,1200),('Hobbit_V2_ThreeQuarter',(2.7,-4,1.9),(0,0,.67),'ORTHO',1.70,1200,1200),('Hobbit_V2_Camera_25D_Detail',(2.3,-2.3,4.05),(0,0,.67),'ORTHO',1.68,1200,1200),('Hobbit_V2_Camera_25D_2850cm',(12.953,-12.953,22.492),(0,0,.66),'PERSP',0,1600,900),('Hobbit_V2_FaceHair_Detail',(.48,-1.8,1.44),(0,-.005,1.183),'ORTHO',.36,1400,1400),('Hobbit_V2_Hands_Detail',(1.16,-.75,1.52),(.695,-.007,.934),'ORTHO',.265,1400,1400),('Hobbit_V2_Feet_Detail',(.55,-1.0,.65),(0,-.076,.08),'ORTHO',.48,1400,1400),('Hobbit_V2_Clothing_Detail',(.8,-2,1.3),(0,-.02,.79),'ORTHO',1.06,1400,1400),('Hobbit_V2_25D_Readability',(1.8,-1.8,3.78),(0,0,.67),'ORTHO',1.42,1400,1400)]
mode=os.environ.get('HOBBIT_V2_RENDER','ALL')
if mode=='CHECK':views=[views[0],views[7],views[4]]
paths=[]
for name,loc,target,kind,size,x,y in views:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=kind
 if size:cam.data.ortho_scale=size
 else:cam.data.lens=36/(2*math.tan(math.radians(35)/2));cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
 s.render.resolution_x=x;s.render.resolution_y=y;s.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath)
(BASE/'Review/V2'/('Preview_Check.json' if mode=='CHECK' else 'PreviewPaths.json')).write_text(json.dumps({'images':paths,'source_saved_during_render':False},indent=2))
print('V2 render complete',len(paths))
