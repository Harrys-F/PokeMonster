import bpy,math,json,array
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s;rig=s.objects['HNM2_Rig'];body=s.objects['HNM2_Body'];cam=s.camera;P=B/'Review/MeshyBaseV2/Previews';F=B/'Review/MeshyBaseV2/AnimationFrames'
cam.data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO');cam.location=(2.4,-4,1.6);cam.rotation_euler=(Vector((0,0,.66))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.63
s.cycles.samples=12;s.render.resolution_x=512;s.render.resolution_y=512
rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='POSE')
allpaths=[]
for label in ['Idle_V2','Walk_V2','Run_V1']:
 act=bpy.data.actions['HNM2_'+label];rig.animation_data.action=act
 if act.slots:rig.animation_data.action_slot=act.slots[0]
 first,last=map(int,act.frame_range);frames=sorted(set(round(first+(last-first)*i/7) for i in range(8)));paths=[]
 for i,frame in enumerate(frames):
  s.frame_set(frame);bpy.context.view_layer.update();s.render.filepath=str(F/(label+'_frame_'+str(frame).zfill(3)+'.png'));bpy.ops.render.render(write_still=True);paths.append(s.render.filepath);print('ANIM_FRAME',label,frame,flush=True)
 # Native Blender bitmap contact sheet, preserving existing rendered pixels.
 atlas=bpy.data.images.new('Review_'+label+'_ContactSheet',width=2048,height=1024,alpha=True);dest=array.array('f',[0.0])*(2048*1024*4)
 for n,path in enumerate(paths):
  im=bpy.data.images.load(path,check_existing=False);src=array.array('f',[0.0])*(512*512*4);im.pixels.foreach_get(src);col=n%4;row=1-n//4
  for yy in range(512):
   di=((row*512+yy)*2048+col*512)*4;si=yy*512*4;dest[di:di+512*4]=src[si:si+512*4]
 atlas.pixels.foreach_set(dest);atlas.filepath_raw=str(P/('Sequence_'+label+'.png'));atlas.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');atlas.save();allpaths.append({'clip':label,'frames':frames,'frame_paths':paths,'sheet':atlas.filepath_raw,'sampling':'8 ordered samples across complete saved cycle, not real-time video'})
# Visible rig diagram generated from exact existing bone endpoints; review-only curves, not model parts.
rig.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST');body.hide_render=True
s.render.resolution_x=1400;s.render.resolution_y=1200;s.cycles.samples=20;cam.location=(2,-4,1.5);cam.rotation_euler=(Vector((0,0,.7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.8
mat=bpy.data.materials.new('Review_RigLines');mat.use_nodes=True;pr=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');pr.inputs['Base Color'].default_value=(.12,.55,.35,1);pr.inputs['Emission Color'].default_value=(.05,.25,.12,1);pr.inputs['Emission Strength'].default_value=.5
created=[]
for bone in rig.data.bones:
 dat=bpy.data.curves.new('ReviewBone_'+bone.name,'CURVE');dat.dimensions=next(i.identifier for i in bpy.types.Curve.bl_rna.properties['dimensions'].enum_items if i.identifier=='3D');dat.bevel_depth=.0035;dat.bevel_resolution=2;sp=dat.splines.new(next(i.identifier for i in bpy.types.Spline.bl_rna.properties['type'].enum_items if i.identifier=='POLY'));sp.points.add(1)
 for point,co in zip(sp.points,[bone.head_local,bone.tail_local]):point.co=(*co,1)
 ob=bpy.data.objects.new(dat.name,dat);s.collection.objects.link(ob);dat.materials.append(mat);created.append(ob)
 txt=bpy.data.curves.new('Label_'+bone.name,'FONT');txt.body=bone.name;txt.size=.022;txt.align_x='LEFT' if bone.head_local.x>=0 else 'RIGHT';ob=bpy.data.objects.new(txt.name,txt);s.collection.objects.link(ob);ob.location=(bone.head_local+bone.tail_local)*.5+Vector((.018 if bone.head_local.x>=0 else -.018,-.022,0));ob.rotation_euler=cam.rotation_euler;created.append(ob)
s.render.filepath=str(P/'Rig_Existing25Bones.png');bpy.ops.render.render(write_still=True)
for o in created:o.hide_render=True
# Uniform scale comparison, temporary instances only; no saved NPC variants.
copies=[]
for height,xx in [(1.2,-1.65),(1.32,0),(1.45,1.65)]:
 r=rig.copy();r.data=rig.data.copy();s.collection.objects.link(r);r.location=(xx,0,0);r.scale=(height/1.4,)*3
 ob=body.copy();ob.data=body.data;s.collection.objects.link(ob);ob.parent=r;ob.location=(0,0,0);ob.hide_render=False
 for m in ob.modifiers:
  if m.type=='ARMATURE':m.object=r
 txt=bpy.data.curves.new('ReviewSizeLabel','FONT');txt.body=str(height)+' m';txt.size=.13;txt.align_x='CENTER';t=bpy.data.objects.new(txt.name,txt);s.collection.objects.link(t);t.location=(xx,-.15,1.65);t.rotation_euler=(math.pi/2,0,0);copies.extend([r,ob,t])
cam.location=(0,-5,.72);cam.rotation_euler=(Vector((0,0,.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=5.1;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.filepath=str(P/'Scale_120_132_145.png');bpy.ops.render.render(write_still=True)
(B/'Review/MeshyBaseV2/AnimationPreviews.json').write_text(json.dumps({'sequences':allpaths,'rig_image':str(P/'Rig_Existing25Bones.png'),'scale_image':str(P/'Scale_120_132_145.png'),'source_saved':False,'debug_curves_and_size_instances_not_in_master':True},indent=2))
print('ANIMATION_AND_RIG_REVIEW_DONE',flush=True)
