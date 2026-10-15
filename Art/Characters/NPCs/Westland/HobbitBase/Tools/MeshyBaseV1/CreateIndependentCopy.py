import bpy,json,math
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');OUT=BASE/'Source/Hobbit_NPC_MeshyBase_V1.blend'
assert not OUT.exists(),'Never replace an existing NPC copy'
s=bpy.data.scenes['Hobbit_Meshy_Inspection_Temporary'];s.name='Hobbit_NPC_MeshyBase_V1';bpy.context.window.scene=s
# This appended source scene is private; the original live player scenes stay intact.
objects=list(s.objects);old_to_new={o:o for o in objects};old_data={o:o.data for o in objects};data_copies={};materials={};images={};nodegroups={}
def copy_group(group):
 if group in nodegroups:return nodegroups[group]
 new=group.copy();new.name='HNM1_'+group.name;nodegroups[group]=new;remap_nodes(new);return new
def remap_nodes(tree):
 for n in tree.nodes:
  if n.type=='TEX_IMAGE' and n.image:
   old=n.image
   if old not in images:
    im=old.copy();im.name='HNM1_'+old.name;im.pack();images[old]=im
   n.image=images[old]
  if n.type=='GROUP' and n.node_tree:n.node_tree=copy_group(n.node_tree)
for o in objects:
 o.name='HNM1_'+('Body' if o.type=='MESH' else 'Rig' if o.type=='ARMATURE' else o.type.title())
 if o.data:
  original=o.data
  if original not in data_copies:data_copies[original]=original.copy();data_copies[original].name='HNM1_'+original.name
  o.data=data_copies[original]
 if o.type=='MESH':
  for slot in o.material_slots:
   if slot.material:
    old=slot.material
    if old not in materials:
     m=old.copy();m.name='HNM1_'+old.name
     if m.node_tree:remap_nodes(m.node_tree)
     materials[old]=m
    slot.material=materials[old]
for o in objects:
 if o.parent:o.parent=old_to_new.get(o.parent,o.parent)
 for m in o.modifiers:
  if hasattr(m,'object') and m.object:m.object=old_to_new.get(m.object,m.object)
 for c in list(o.constraints)+[c for p in o.pose.bones for c in p.constraints] if o.type=='ARMATURE' else list(o.constraints):
  if hasattr(c,'target') and c.target:c.target=old_to_new.get(c.target,c.target)
arm=next(o for o in objects if o.type=='ARMATURE');body=next(o for o in objects if o.type=='MESH')
source_run=arm.animation_data.action
with bpy.data.libraries.load('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend',link=False) as (a,b):b.actions=['A_Player_Meshy_Idle_V2','A_Player_Meshy_Walk_V2']
actions=[]
for original,label in [(b.actions[0],'Idle_V2'),(b.actions[1],'Walk_V2'),(source_run,'Run_V1')]:
 act=original.copy();act.name='HNM1_'+label;act.use_fake_user=True;actions.append(act)
arm.animation_data_clear();arm.animation_data_create();arm.animation_data.action=actions[0]
if len(actions[0].slots):arm.animation_data.action_slot=actions[0].slots[0]
arm.data.pose_position=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='REST')
s.frame_start=1;s.frame_end=181;s.render.fps=60;s.frame_set(1)
model=bpy.data.collections.new('HNM1_MODEL_RIG');studio=bpy.data.collections.new('HNM1_REVIEW_STUDIO');s.collection.children.link(model);s.collection.children.link(studio)
for o in objects:
 for c in list(o.users_collection):c.objects.unlink(o)
 (model if o.type in {'MESH','ARMATURE'} else studio).objects.link(o)
# No model modification: only independent studio data for review.
s.world=s.world.copy() if s.world else bpy.data.worlds.new('HNM1_ReviewWorld');s.world.name='HNM1_ReviewWorld';s.world.use_nodes=True
bg=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(.17,.19,.22,1);bg.inputs['Strength'].default_value=.30
cam=next(o for o in objects if o.type=='CAMERA');s.camera=cam
light=next(o for o in objects if o.type=='LIGHT');light.hide_render=True
for name,loc,power,size in [('Key',(-2,-3,3),240,3),('Fill',(2,-1,2.3),130,2.5),('Rim',(0,2,3),200,2.5)]:
 dat=bpy.data.lights.new('HNM1_'+name,next(i.identifier for i in bpy.types.Light.bl_rna.properties['type'].enum_items if i.identifier=='AREA'));dat.energy=power;dat.shape=next(i.identifier for i in bpy.types.AreaLight.bl_rna.properties['shape'].enum_items if i.identifier=='DISK');dat.size=size
 ob=bpy.data.objects.new(dat.name,dat);studio.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,0,.7))-ob.location).to_track_quat('-Z','Y').to_euler()
s['copied_sources']='Player_Meshy_Sprint_V1.blend: mesh, rig, material, textures, run; AnimationQuality_V2.blend: idle, walk'
s['scope']='Unmodified independent copy at original 1.40m; intended NPC target 1.32m requires subsequent approval'
s['npc_target_height_m']=1.32
try:s.render.engine='CYCLES'
except TypeError:raise
s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True
s.render.image_settings.file_format=next(i.identifier for i in bpy.types.ImageFormatSettings.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG')
s.render.resolution_x=1200;s.render.resolution_y=1200;s.render.resolution_percentage=100
# Explicitly serialize all independent actions, including inactive idle/walk/run.
owned={s,*actions,*images.values(),*materials.values(),*nodegroups.values()}
bpy.data.libraries.write(str(OUT),owned,fake_user=True)
info={'source_mesh_rig':'Art/Characters/YoungTrainer/Source/Player_Meshy_Sprint_V1.blend','source_idle_walk':'Art/Characters/YoungTrainer/Source/Player_Meshy_AnimationQuality_V2.blend','file':str(OUT),'mesh':body.name,'rig':arm.name,'copied_actions':[a.name for a in actions],'independent_object_data':all(o.data!=old_data[o] for o in objects),'independent_materials':all(a!=b for a,b in materials.items()),'independent_images':all(a!=b for a,b in images.items()),'packed_images':[{ 'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in images.values()],'external_libraries':[d.name for d in owned if d.library],'vertices':len(body.data.vertices),'faces':len(body.data.polygons),'bones':len(arm.data.bones),'reference_height_m':max(v.co.z for v in body.data.vertices)-min(v.co.z for v in body.data.vertices),'no_geometry_or_weight_edits':True}
(BASE/'Review/MeshyBaseV1/CopyAudit.json').write_text(json.dumps(info,indent=2));print(json.dumps(info,indent=2))
