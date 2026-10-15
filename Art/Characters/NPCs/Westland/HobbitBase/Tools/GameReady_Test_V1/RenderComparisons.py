import bpy,json,sys
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1/Previews';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s;cam=s.camera;hp=s.objects['GRT_HighPoly_Reference'];low=[s.objects['GRT_HeadHair'],s.objects['GRT_Torso']];context=s.objects['GRT_UnmodifiedContext']
clay=bpy.data.materials.new('GRT_Review_Clay');clay.use_nodes=True;pr=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');pr.inputs['Base Color'].default_value=(.42,.39,.35,1);pr.inputs['Roughness'].default_value=.78
wire=clay.copy();pr=next(n for n in wire.node_tree.nodes if n.type=='BSDF_PRINCIPLED');w=wire.node_tree.nodes.new('ShaderNodeWireframe');w.use_pixel_size=True;w.inputs['Size'].default_value=.65;mix=wire.node_tree.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.55,.5,.44,1);mix.inputs[2].default_value=(.012,.015,.018,1);wire.node_tree.links.new(w.outputs[0],mix.inputs[0]);wire.node_tree.links.new(mix.outputs[0],pr.inputs['Base Color'])
cam.data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO');s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100
# Background-process-only device choice; no preferences or master saved.
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 types=[i.identifier for i in prefs.bl_rna.properties['compute_device_type'].enum_items]
 if 'METAL' in types:
  prefs.compute_device_type=next(i for i in types if i=='METAL');prefs.get_devices()
  available=[d for d in prefs.devices if d.type=='METAL']
  if available:
   for d in prefs.devices:d.use=d.type=='METAL'
   s.cycles.device=next(i.identifier for i in s.cycles.bl_rna.properties['device'].enum_items if i.identifier=='GPU')
 print('REVIEW_RENDER_DEVICE',s.cycles.device,[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
except Exception as err:print('GPU_UNAVAILABLE_USING_CPU',str(err),flush=True)
views=[('01_FaceFront',(0,-2,1.20),(0,-.04,1.20),.285,'texture'),('02_FaceThreeQuarter',(.7,-1.6,1.32),(0,-.04,1.20),.30,'texture'),('03_FaceProfile',(2,-.045,1.20),(0,-.045,1.20),.38,'texture'),('04_HairFront',(0,-2,1.245),(0,-.015,1.245),.43,'texture'),('05_HairSide',(-2,0,1.245),(0,0,1.245),.43,'texture'),('06_HairBack',(0,2,1.245),(0,.015,1.245),.43,'texture'),('07_Torso',(.25,-2,.89),(0,0,.86),.89,'texture'),('08_HeadClay',(0,-2,1.245),(0,-.015,1.245),.43,'clay'),('09_HeadWire',(0,-2,1.245),(0,-.015,1.245),.43,'wire'),('10_TorsoClay',(.25,-2,.89),(0,0,.86),.89,'clay'),('11_TorsoWire',(.25,-2,.89),(0,0,.86),.89,'wire'),('12_2_5D',(2.5,-2.5,4.9),(0,0,.7),1.82,'texture'),('13_EyeMouthWire',(0,-2,1.18),(0,-.07,1.18),.23,'wire'),('14_VestDetail',(.25,-2,.82),(0,-.11,.82),.42,'texture')]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];selected=set(args);records=[]
for name,loc,target,size,mode in views:
 if selected and name not in selected:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;s.view_layers[0].material_override={'clay':clay,'wire':wire}.get(mode)
 for version in ['A_HP','B_TriangleControl']:
  hp.hide_render=version!='A_HP';context.hide_render=version=='A_HP'
  for o in low:o.hide_render=version=='A_HP'
  s.render.filepath=str(P/(name+'_'+version+'.png'));bpy.ops.render.render(write_still=True);records.append({'path':s.render.filepath,'view':name,'version':version,'mode':mode,'camera_location':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':size});print('COMPARE_DONE',name,version,flush=True)
meta=B/'Review/GameReady_Test_V1/RenderSettings.json'
if selected and meta.exists():
 previous=json.loads(meta.read_text()); paths={r['path'] for r in records};records=[r for r in previous if r['path'] not in paths]+records
meta.write_text(json.dumps(records,indent=2))
# Deliberately no save: only temporary camera positions and material overrides.
