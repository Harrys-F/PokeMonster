import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_4K_Base_V1'];bpy.context.window.scene=s;cam=s.camera;o=next(o for o in s.objects if o.type=='MESH');p=B/'Review/4K_Base_V1/Previews'
clay=bpy.data.materials.new('ReviewOnly_Clay');clay.use_nodes=True;bs=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.42,.39,.35,1);bs.inputs['Roughness'].default_value=.78
wire=clay.copy();bs=next(n for n in wire.node_tree.nodes if n.type=='BSDF_PRINCIPLED');n=wire.node_tree.nodes.new('ShaderNodeWireframe');n.use_pixel_size=True;n.inputs['Size'].default_value=.55;mix=wire.node_tree.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.55,.5,.44,1);mix.inputs[2].default_value=(.012,.015,.018,1);wire.node_tree.links.new(n.outputs[0],mix.inputs[0]);wire.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1100;s.render.resolution_percentage=100
# Model points unchanged, all cameras are review-only.
views=[('01_Front',(0,-4,.7),(0,0,.7),1.8,'textured'),('02_Back',(0,4,.7),(0,0,.7),1.8,'textured'),('03_Left',(-4,0,.7),(0,0,.7),1.7,'textured'),('04_Right',(4,0,.7),(0,0,.7),1.7,'textured'),('05_ThreeQuarter',(2.6,-4,1.5),(0,0,.7),1.88,'textured'),('06_2_5D_Close',(2.5,-2.5,4.9),(0,0,.7),1.82,'textured'),('07_Face_Hair',(0,-2,1.245),(0,-.015,1.245),.39,'textured'),('08_Hands',(.64,-1.4,1.45),(.59,-.025,1.04),.38,'textured'),('09_Feet',(.45,-1.6,.58),(0,-.045,.085),.65,'textured'),('10_Clothing',(.5,-2,.93),(0,0,.68),1.02,'textured'),('11_Face_Clay',(0,-2,1.245),(0,-.015,1.245),.39,'clay'),('12_Face_Wire',(0,-2,1.245),(0,-.015,1.245),.39,'wire'),('13_Body_Clay',(0,-4,.7),(0,0,.7),1.8,'clay'),('14_Hand_Clay',(.64,-1.4,1.45),(.59,-.025,1.04),.38,'clay'),('15_Feet_Clay',(.45,-1.6,.58),(0,-.045,.085),.65,'clay'),('16_Cape_Clay',(0,4,.7),(0,0,.7),1.8,'clay'),('17_Left_Clay',(-4,0,.7),(0,0,.7),1.7,'clay'),('19_Hand_R',(-.64,-1.4,1.45),(-.59,-.025,1.04),.38,'textured'),('20_Hand_Wire',(.64,-1.4,1.45),(.59,-.025,1.04),.38,'wire'),('21_Hand_L_Top',(.65,-.025,2.5),(.65,-.025,1.04),.27,'textured'),('22_Hand_R_Top',(-.65,-.025,2.5),(-.65,-.025,1.04),.27,'textured'),('18_2_5D_GameScale',(0,0,0),(0,0,.7),1.0,'game')]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];selected=set(args)
for name,loc,target,size,mode in views:
 if selected and name not in selected:continue
 s.view_layers[0].material_override={'clay':clay,'wire':wire}.get(mode)
 cam.data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier==('PERSP' if mode=='game' else 'ORTHO'))
 if mode=='game':
  cam.data.lens=36/(2*math.tan(math.radians(35)/2));cam.data.sensor_width=36;s.render.resolution_y=619;target=Vector((0,0,.83));loc=target+Vector((math.cos(math.radians(50))*28.5/math.sqrt(2),-math.cos(math.radians(50))*28.5/math.sqrt(2),math.sin(math.radians(50))*28.5))
 else:s.render.resolution_y=1100;cam.data.ortho_scale=size
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(p/(name+'.png'));bpy.ops.render.render(write_still=True);print('PREVIEW_DONE',name,flush=True)
# No saving: material overrides/camera changes are not written into master.
