import bpy,math,json
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V1'];bpy.context.window.scene=s;ob=s.objects['HNM1_Body'];cam=s.camera;original=ob.data.materials[0]
clay=bpy.data.materials.new('ReviewOnly_Clay');clay.use_nodes=True;p=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.45,.42,.37,1);p.inputs['Roughness'].default_value=.8
wire=clay.copy();wire.name='ReviewOnly_Wire';nt=wire.node_tree;p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');w=nt.nodes.new('ShaderNodeWireframe');w.use_pixel_size=True;w.inputs['Size'].default_value=.75;mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.50,.48,.43,1);mix.inputs[2].default_value=(.035,.035,.035,1);nt.links.new(w.outputs[0],mix.inputs[0]);nt.links.new(mix.outputs[0],p.inputs['Base Color'])
s.cycles.samples=20;s.render.resolution_x=1000;s.render.resolution_y=1000
paths=[]
for view,loc,target,size in [('Front',(0,-4,.7),(0,0,.7),1.78),('Forearm',(.55,-1.5,1.05),(.49,-.02,1.025),.44),('Cape',(.10,2,.68),(0,.10,.68),.84)]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size
 for mode,mat in [('Textured',original),('Clay',clay),('Wire',wire)]:
  ob.data.materials[0]=mat;s.render.filepath=str(B/'Review/MeshyBaseV2/Previews'/('Diagnostic_V1_'+view+'_'+mode+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('DIAGNOSTIC_RENDER',view,mode,flush=True)
(B/'Review/MeshyBaseV2/DiagnosticPreviews.json').write_text(json.dumps(paths,indent=2))
