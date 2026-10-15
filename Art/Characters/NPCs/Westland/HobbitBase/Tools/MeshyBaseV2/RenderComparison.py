import bpy,json,math
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s;cam=s.camera;body=s.objects['HNM2_Body'];rig=s.objects['HNM2_Rig'];original=body.data.materials[0]
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_MeshyBase_V1.blend'),link=False) as (a,b):b.objects=['HNM1_Body','HNM1_Rig']
oldbody,oldrig=b.objects
for ob in b.objects:s.collection.objects.link(ob);ob.hide_render=True
oldbody.parent=oldrig
for m in oldbody.modifiers:
 if m.type=='ARMATURE':m.object=oldrig
for ob in [rig,oldrig]:ob.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST')
clay=bpy.data.materials.new('Review_Clay');clay.use_nodes=True;pr=next(n for n in clay.node_tree.nodes if n.type=='BSDF_PRINCIPLED');pr.inputs['Base Color'].default_value=(.45,.42,.37,1);pr.inputs['Roughness'].default_value=.8
wire=clay.copy();nt=wire.node_tree;pr=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');w=nt.nodes.new('ShaderNodeWireframe');w.use_pixel_size=True;w.inputs['Size'].default_value=.6;mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.5,.48,.43,1);mix.inputs[2].default_value=(.025,.025,.025,1);nt.links.new(w.outputs[0],mix.inputs[0]);nt.links.new(mix.outputs[0],pr.inputs['Base Color'])
cam.data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO')
s.cycles.samples=24;s.render.resolution_x=1100;s.render.resolution_y=1100;paths=[]
views=[('Front',(0,-4,.7),(0,0,.7),1.78),('Back',(0,4,.7),(0,0,.7),1.78),('Left',(-4,0,.7),(0,0,.7),1.60),('Right',(4,0,.7),(0,0,.7),1.60),('ThreeQuarter',(2.6,-4,1.65),(0,0,.7),1.9),('Forearm',(.55,-1.5,1.05),(.49,-.02,1.025),.65),('Cape',(0,2,.68),(0,.10,.68),.84),('Feet',(.55,-1.3,.35),(0,-.06,.07),.55)]
for name,loc,target,size in views:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size
 modes=[('V1','Textured'),('V2','Textured')] if name in ['Front','Back','Forearm','Cape'] else [('V2','Textured')]
 if name in ['Front','Forearm','Cape']:modes += [('V2','Clay'),('V2','Wire')]
 for version,mode in modes:
  oldbody.hide_render=version!='V1';body.hide_render=version!='V2';body.data.materials[0]={'Textured':original,'Clay':clay,'Wire':wire}[mode]
  s.render.filepath=str(B/'Review/MeshyBaseV2/Previews'/('Compare_'+name+'_'+version+'_'+mode+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('COMPARE_DONE',name,version,mode,flush=True)
(B/'Review/MeshyBaseV2/ComparisonPreviews.json').write_text(json.dumps(paths,indent=2))
