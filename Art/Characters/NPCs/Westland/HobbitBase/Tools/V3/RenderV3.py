import bpy,math,json,os
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_Base_V3_Body'];bpy.context.window.scene=s;cam=s.camera;P=BASE/'Review/V3/Previews'
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=40;s.cycles.use_denoising=True;s.render.image_settings.file_format='PNG';s.render.resolution_percentage=100
views=[('01_Front',(0,-4,.641),(0,0,.641),1.76,1200,1200),('02_Back',(0,4,.641),(0,0,.641),1.76,1200,1200),('03_Side_Left',(-4,0,.641),(0,0,.641),1.44,1200,1200),('04_Side_Right',(4,0,.641),(0,0,.641),1.44,1200,1200),('05_ThreeQuarter',(2.5,-4,1.8),(0,0,.64),1.78,1200,1200),('06_Face_Front',(0,-2,1.17),(0,-.005,1.17),.31,1400,1400),('07_Face_ThreeQuarter',(.8,-1.6,1.23),(0,0,1.169),.32,1400,1400),('08_Face_Profile',(2,0,1.17),(0,0,1.17),.32,1400,1400),('09_Hands',(.96,-.68,1.47),(.680,-.013,1.004),.26,1400,1400),('10_Feet',(.48,-1.0,.68),(0,-.058,.084),.50,1400,1400),('11_Camera25D',(2.3,-2.3,4.03),(0,0,.64),1.70,1400,1400),('12_Compare_V2_V3',(0,-4,.65),(0,0,.65),3.70,1800,1000)]
mode=os.environ.get('HOBBIT_V3_RENDER','ALL')
if mode=='CHECK':views=[views[i] for i in [4,5,7,8,9]];s.cycles.samples=24
paths=[]
for name,loc,target,size,x,y in views:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size;s.render.resolution_x=x;s.render.resolution_y=y
 if name.startswith('12_'):
  # Own V2 is loaded only in this disposable rendering process, never in V3.
  source=BASE/'Source/Hobbit_NPC_Base_V2.blend'
  with bpy.data.libraries.load(str(source),link=False) as (data,to):
   to.objects=[n for n in data.objects if n=='HNV2_Body' or (n.startswith('HNV2_') and any(n.startswith('HNV2_'+p) for p in ['Eye_','Iris_','Pupil_','UpperLid_','LowerLid_','SculptedBrow_','EarHelix_','EarInnerFold_','Nostril_','UpperLipSurface','LowerLipSurface','MouthSeam']))]
  for ob in to.objects:
   if ob is not None:s.collection.objects.link(ob);ob.location.x-=.91
  neutral=bpy.data.materials.new('ReviewOnly_IdenticalSkin');neutral.use_nodes=True;ns=next(n for n in neutral.node_tree.nodes if n.type=='BSDF_PRINCIPLED');ns.inputs['Base Color'].default_value=(.45,.265,.185,1);ns.inputs['Roughness'].default_value=.72;ns.inputs['Specular IOR Level'].default_value=.20
  for ob in [s.objects['HNV3_Body']]+[q for q in to.objects if q is not None and (q.name=='HNV2_Body' or any(q.name.startswith('HNV2_'+p) for p in ['EarHelix_','EarInnerFold_','UpperLid_','LowerLid_']))]:
   for slot in ob.material_slots:slot.material=neutral
  for ob in [s.objects['HNV3_Body'],s.objects['HNV3_Eyeball_L'],s.objects['HNV3_Eyeball_R']]:ob.location.x+=.91
  for label,xx in [('V2 – Haut / Gesicht',-.91),('V3 – neues Basismesh',.91)]:
   data=bpy.data.curves.new(label,'FONT');data.body=label;data.align_x='CENTER';data.size=.080;ob=bpy.data.objects.new(label,data);s.collection.objects.link(ob);ob.location=(xx,-.30,1.40);ob.rotation_euler=(math.pi/2,0,0)
 s.render.filepath=str(P/('Hobbit_V3_'+name+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath)
(BASE/'Review/V3'/('CheckPreviews.json' if mode=='CHECK' else 'PreviewPaths.json')).write_text(json.dumps({'images':paths,'rendered_from_saved_source':bpy.data.filepath,'source_saved_by_renderer':False,'comparison_V2_only_disposable_process':True},indent=2))
print('Rendered V3',len(paths),'views')
