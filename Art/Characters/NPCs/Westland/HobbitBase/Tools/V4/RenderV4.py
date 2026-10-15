import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_V4_HeadSculpt'];bpy.context.window.scene=s;cam=s.camera;P=BASE/'Review/V4/Previews'
v4=[o for o in s.objects if o.type=='MESH' and ('HNV4_Body' in o.name or 'HNV4_Eyeball' in o.name)];v3=[o for o in s.objects if o.name.startswith('REF_V3_')]
original_locations={o:o.location.copy() for o in v4+v3}
for o in v4+v3:o.hide_set(False)
s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_percentage=100
views=[('01_V3_Head_Front','V3',(0,-2,1.17),(0,-.005,1.17),.31,1100,1100),('02_V4_Head_Front','V4',(0,-2,1.17),(0,-.005,1.17),.31,1100,1100),('03_V3_Head_Profile','V3',(2,0,1.17),(0,0,1.17),.32,1100,1100),('04_V4_Head_Profile','V4',(2,0,1.17),(0,0,1.17),.32,1100,1100),('05_V3_Head_ThreeQuarter','V3',(.8,-1.6,1.23),(0,0,1.169),.32,1100,1100),('06_V4_Head_ThreeQuarter','V4',(.8,-1.6,1.23),(0,0,1.169),.32,1100,1100),('07_Compare_V3_V4','BOTH',(0,-2,1.18),(0,0,1.18),.72,1800,1000),('08_V4_Body_Front','V4',(0,-4,.641),(0,0,.641),1.76,1200,1200),('09_V4_Body_Camera25D','V4',(2.3,-2.3,4.03),(0,0,.64),1.70,1200,1200)]
if os.environ.get('V4_CHECK')=='1':views=[views[1],views[3],views[6]];s.cycles.samples=24
paths=[]
for name,version,loc,target,size,w,h in views:
 for o in v3:o.hide_render=version=='V4';o.location=original_locations[o]+Vector((-.185 if version=='BOTH' else 0,0,0))
 for o in v4:o.hide_render=version=='V3';o.location=original_locations[o]+Vector((.185 if version=='BOTH' else 0,0,0))
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;s.render.resolution_x=w;s.render.resolution_y=h
 s.render.filepath=str(P/('Hobbit_V4_'+name+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('RENDER_DONE',name,flush=True)
(BASE/'Review/V4/PreviewPaths.json').write_text(json.dumps({'images':paths,'source':bpy.data.filepath,'saved_by_renderer':False,'comparison_left':'V3','comparison_right':'V4','lighting_identical':True},indent=2))
