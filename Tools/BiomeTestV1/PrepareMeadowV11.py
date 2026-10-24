"""Anatomical rigs on five inspected original GLBs. No remeshing, UV edits, recolouring or GLB writes."""
import bpy, json, hashlib, struct, sys, math
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
R=Path(__file__).resolve().parents[2]
name=sys.argv[sys.argv.index('--')+1]
assert name in ['Raupy','Hornliu','Smettbo','Bibor','Habitak']
spec=json.loads((R/'Tools/BiomeTestV1/SpeciesV11.json').read_text())[name]
A=R/'Art/Characters/Creatures'/name;dest=A/'Source'/(name+'_Meshy_V1.blend')
assert not dest.exists() or ('--revise-own' in sys.argv and str(dest.relative_to(R)) not in json.loads((R/'Saved/BiomeTestV11/Before.json').read_text())['hashes'])
source=R/'Art/Characters/Creatures/Incoming'/(name+'.glb');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
intake=json.loads((R/'Saved/BiomeTestV11/Intake'/(name+'.json')).read_text());assert digest==intake['sha256']
for folder in ['Source','Textures/MeshyV1','Exports/MeshyV1']:(A/folder).mkdir(parents=True,exist_ok=True)
n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);offset=20+n+8;material=g['materials'][0]
for typ,idx in [('BaseColor',material['pbrMetallicRoughness']['baseColorTexture']['index']),('MetallicRoughness',material['pbrMetallicRoughness']['metallicRoughnessTexture']['index']),('Normal',material['normalTexture']['index'])]:
 image=g['images'][g['textures'][idx]['source']];assert image['mimeType']=='image/jpeg';v=g['bufferViews'][image['bufferView']];data=raw[offset+v.get('byteOffset',0):offset+v.get('byteOffset',0)+v['byteLength']];p=A/'Textures/MeshyV1'/(name+'_'+typ+'.jpg');assert not p.exists() or p.read_bytes()==data
 if not p.exists():p.write_bytes(data)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1;ref=meshes[0];points=[ref.matrix_world@v.co for v in ref.data.vertices]
mn=Vector(tuple(min(p[k]for p in points)for k in range(3)));mx=Vector(tuple(max(p[k]for p in points)for k in range(3)));origin=Vector((0,(mn.y+mx.y)/2,mn.z));h=spec['height']/100;scale=h/(mx.z-mn.z)
ref.name=name+'_UNMODIFIED_GLB';col=bpy.data.collections.new('UNMODIFIED_HIGH_REFERENCE');bpy.context.scene.collection.children.link(col)
for c in list(ref.users_collection):c.objects.unlink(ref)
col.objects.link(ref);col.hide_viewport=True;col.hide_render=True
body=ref.copy();body.data=ref.data.copy();body.name=name+'_Body';body.matrix_world=Matrix.Identity(4);bpy.context.scene.collection.objects.link(body)
for v,p in zip(body.data.vertices,points):v.co=(p-origin)*scale
body.data.update();bones={'root':((0,0,0),(0,0,.04),None)}
def bone(n,a,b,parent='root'):bones[n]=(tuple((Vector(a)-origin)*scale),tuple((Vector(b)-origin)*scale),parent)
if name in ['Raupy','Hornliu']:
 path=[(0,-.11,-.025),(0,-.035,-.19),(0,.07,-.34),(0,.21,-.35),(0,.33,-.23),(0,.38,-.05)]
 for i,(a,b)in enumerate(zip(path,path[1:])):bone('segment_'+str(i),a,b,'root'if i==0 else 'segment_'+str(i-1))
 bone('head',(0,-.10,.10),(0,-.24,.32))
elif name in ['Smettbo','Bibor']:
 bone('body',(0,0,-.14 if name=='Smettbo'else .10),(0,-.04,-.02 if name=='Smettbo'else-.10))
 bone('head',(0,-.06,-.02 if name=='Smettbo'else .24),(0,-.20,.04 if name=='Smettbo'else .24),'body')
 bone('abdomen',(0,.01,-.12),(0,.05,-.32),'body')
 for side,sg in [('L',1),('R',-1)]:
  z=-.05 if name=='Smettbo'else .14
  bone('wing_upper_'+side,(sg*.06,.07,z),(sg*.38,.10,.32 if name=='Smettbo'else .42),'body')
  bone('wing_lower_'+side,(sg*.06,.08,z),(sg*.28,.15,-.24 if name=='Smettbo'else .06),'body')
  bone('wing_tip_'+side,(sg*.29,.10,.23),(sg*.44,.10,.30),'wing_upper_'+side)
  bone('arm_'+side,(sg*.08,-.05,.13 if name=='Bibor'else-.12),(sg*.28,-.20,-.08 if name=='Bibor'else-.24),'body')
  bone('leg_'+side,(sg*.07,.02,-.16),(sg*.30,.07,-.43),'abdomen')
else:
 bone('body',(0,0,-.10),(0,-.02,.10));bone('head',(0,-.02,.12),(0,-.07,.24),'body');bone('tail',(0,.055,-.03),(0,.145,-.26),'body')
 for side,sg in [('L',1),('R',-1)]:
  bone('wing_'+side,(sg*.09,.005,.075),(sg*.29,.015,.07),'body');bone('wing_tip_'+side,(sg*.29,.015,.07),(sg*.47,.025,.055),'wing_'+side)
  bone('thigh_'+side,(sg*.055,.01,-.12),(sg*.06,-.02,-.20),'body');bone('shin_'+side,(sg*.06,-.02,-.20),(sg*.06,.0,-.275),'thigh_'+side);bone('foot_'+side,(sg*.06,.0,-.275),(sg*.06,-.10,-.29),'shin_'+side)
arm=bpy.data.armatures.new(name+'_Rig');rig=bpy.data.objects.new(name+'_Rig',arm);bpy.context.scene.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for n,(a,b,parent)in bones.items():
 eb=arm.edit_bones.new(n);eb.head=a;eb.tail=b
 if parent:eb.parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
for n in bones:
 if n!='root':body.vertex_groups.new(name=n)
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def nearest(p,names):
 d=[]
 for n in names:
  a=Vector(bones[n][0]);v=Vector(bones[n][1])-a;t=max(0,min(1,(p-a).dot(v)/v.length_squared));d.append(((p-a-v*t).length,n))
 d.sort();w={n:1/max(.006,x)**4 for x,n in d[:2]};total=sum(w.values());return{k:v/total for k,v in w.items()}
def mix(a,b,t):return{k:a.get(k,0)*(1-t)+b.get(k,0)*t for k in a.keys()|b.keys()}
for v in body.data.vertices:
 rawp=v.co/scale+origin;x,y,z=rawp;side='L'if x>=0 else'R'
 if name in ['Raupy','Hornliu']:
  w=nearest(v.co,[n for n in bones if n.startswith('segment_')]);w=mix(w,{'head':1},smooth(.02,.13,z))
 elif name=='Smettbo':
  w={'head':1}if y<-.035 and z>-.12 else nearest(v.co,['body','abdomen'])
  if y>.0 and abs(x)>.075:
   n='wing_upper_'+side if z>-.02 else 'wing_lower_'+side;wing={n:1}
   if n.startswith('wing_upper'):wing=mix(wing,{'wing_tip_'+side:1},smooth(.28,.40,abs(x))*.55)
   w=mix(w,wing,smooth(.075,.13,abs(x)))
  elif z<-.22:w=nearest(v.co,['arm_'+side,'leg_'+side,'abdomen'])
 elif name=='Bibor':
  w={'head':1}if y<-.04 and z>.14 else nearest(v.co,['body','abdomen'])
  if y>.025 and abs(x)>.075 and z>.025:w={'wing_upper_'+side if z>.20 else'wing_lower_'+side:1}
  elif abs(x)>.12 and y<.02:w={'arm_'+side:1}if z>-.15 else{'leg_'+side:1}
  elif abs(x)>.14 and z<-.12:w={'leg_'+side:1}
 else:
  w={'head':1}if z>.13 and abs(x)<.13 else{'body':1}
  if abs(x)>.085:
   wing=mix({'wing_'+side:1},{'wing_tip_'+side:1},smooth(.25,.34,abs(x)));w=mix(w,wing,smooth(.085,.14,abs(x)))
  if y>.065 and z<.01 and abs(x)<.14:w={'tail':1}
  elif z<-.155 and abs(x)<.13:w=nearest(v.co,['thigh_'+side,'shin_'+side,'foot_'+side])
 total=sum(w.values())
 for n,a in w.items():
  if a>1e-8:body.vertex_groups[n].add([v.index],a/total,'REPLACE')
assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in body.data.vertices)
body.parent=rig;mod=body.modifiers.new('Original geometry anatomical skin','ARMATURE');mod.object=rig
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.fps=30
for image in bpy.data.images:
 if image.type=='IMAGE':image.pack()
rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};records={};roles=[('Idle',2.4),('Walk',1.2 if name in ['Raupy','Hornliu']else .6),('Run',.8 if name in ['Raupy','Hornliu']else .4),('Attack',.9),('Hit',.5),('Faint',1.2),('Happy',1.6)]
if name=='Habitak':roles +=[('Takeoff',1.6),('Hover',.8),('Land',1.4)]
def set_world(n,m):
 parent=bones[n][2];parent_delta=posed[parent]@rest[parent].inverted()if parent else Matrix.Identity(4);rig.pose.bones[n].matrix_basis=rest[n].inverted()@parent_delta.inverted()@m;posed[n]=m
def orient_segment(n,a,b):
 original=Vector(bones[n][1])-Vector(bones[n][0]);rot=original.rotation_difference(b-a)@rest[n].to_quaternion();set_world(n,Matrix.LocRotScale(a,rot,Vector((1,1,1))))
def bird_ik(t,fast):
 stride=(.30*.4 if fast else .18*.6)
 for side,phase in [('L',t%1),('R',(t+.5)%1)]:
  hip=(posed['body']@rest['body'].inverted())@Vector(bones['thigh_'+side][0]);ankle=Vector(bones['foot_'+side][0]);swing=phase>=.60
  y=(-stride*.30+stride*phase)if not swing else(stride*.30-stride*.60*smooth(.60,1,phase));ankle.y+=y
  if swing:ankle.z+=(.026 if fast else .018)*math.sin(math.pi*(phase-.60)/.40)
  l1=(Vector(bones['thigh_'+side][1])-Vector(bones['thigh_'+side][0])).length;l2=(Vector(bones['shin_'+side][1])-Vector(bones['shin_'+side][0])).length;v=ankle-hip;distance=min(v.length,l1+l2-.00001);axis=v.normalized();bend=Vector((0,-1,0));bend=(bend-axis*bend.dot(axis)).normalized();a=(l1*l1-l2*l2+distance*distance)/(2*distance);knee=hip+axis*a+bend*math.sqrt(max(0,l1*l1-a*a));ankle=hip+axis*distance
  orient_segment('thigh_'+side,hip,knee);orient_segment('shin_'+side,knee,ankle);m=rest['foot_'+side].copy();m.translation=ankle;set_world('foot_'+side,m)
for role,duration in roles:
 action=bpy.data.actions.new(name+'_'+role);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;frames=round(duration*30);mins=[]
 for frame in range(frames+1):
  s.frame_set(frame+1);t=frame/frames;wave=math.sin(math.tau*t);pulse=math.sin(math.pi*t)**2;rotations={};root=Matrix.Identity(4)
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  if name in ['Raupy','Hornliu']:
   for i in range(5):rotations['segment_'+str(i)]=((1,0,0),(.015 if role=='Idle'else .07)*math.sin(math.tau*t-i*.8))
   rotations['head']=((0,0,1),.025*wave)
  elif name in ['Smettbo','Bibor']:
   cycles=2 if role in ['Idle','Walk','Run']else 3;beat=math.tau*t*cycles
   for side,sg in [('L',1),('R',-1)]:
    for part,phase in [('upper',0),('lower',.6)]:rotations['wing_'+part+'_'+side]=((0,0,1),sg*((.48+.42*math.sin(beat+phase))if name=='Smettbo'else(.27+.23*math.sin(beat+phase))))
    rotations['wing_tip_'+side]=((0,0,1),sg*.12*math.sin(beat-.5));rotations['leg_'+side]=((1,0,0),.06*math.sin(math.tau*t+.6*sg));rotations['arm_'+side]=((0,0,1),sg*.045*wave)
   rotations['body']=((1,0,0),.02*wave);rotations['head']=((0,0,1),.02*wave)
  else:
   flight=role in ['Takeoff','Hover','Land'];blend=smooth(0,.28,t)if role=='Takeoff'else 1-smooth(.70,1,t)if role=='Land'else 1 if role=='Hover'else 0
   for side,sg in [('L',1),('R',-1)]:
    rotations['wing_'+side]=((0,0,1),sg*.06*(1-blend));rotations['wing_tip_'+side]=((0,0,1),sg*.10*(1-blend))
   rotations['head']=((0,0,1),.035*wave);rotations['tail']=((1,0,0),.06*wave)
   root=Matrix.Translation((0,0,-.005*wave*wave if role in ['Walk','Run']else 0))
  if role=='Attack':root=Matrix.Translation((0,-h*.10*pulse,0))@Quaternion((1,0,0),.13*pulse).to_matrix().to_4x4()
  elif role=='Hit':root=Quaternion((0,0,1),.07*wave).to_matrix().to_4x4()
  elif role=='Faint':root=Quaternion((0,1,0),math.radians(70)*smooth(0,1,t)).to_matrix().to_4x4()
  elif role=='Happy':root=Matrix.Translation((0,0,h*.06*pulse))
  posed={};set_world('root',root@rest['root'])
  for n,(a,b,parent)in bones.items():
   if n=='root':continue
   inherit=posed[parent]@rest[parent].inverted();pivot=Vector(a);axis,angle=rotations.get(n,((1,0,0),0));m=Matrix.Translation(pivot)@Quaternion(axis,angle).to_matrix().to_4x4()@Matrix.Translation(-pivot)@rest[n]
   if name=='Habitak'and n.startswith('wing_'):
    sg=1 if n.endswith('_L')else-1;fold=1.2 if n.startswith('wing_tip_')else .8;flap=sg*(fold*(1-blend)+(.10+.60*math.sin(math.tau*t*(3 if role=='Takeoff'else 2)))*blend)if flight else sg*(fold+.035*math.sin(math.tau*t))
    m=Matrix.Translation(pivot)@Quaternion((0,1,0),flap).to_matrix().to_4x4()@Matrix.Translation(-pivot)@m
   set_world(n,inherit@m)
  if name=='Habitak'and role in ['Walk','Run']:bird_ik(t,role=='Run')
  bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();low=min(v.co.z for v in me.vertices);ev.to_mesh_clear();mins.append(low)
  if low<0:m=posed['root'].copy();m.translation.z-=low;set_world('root',m);bpy.context.view_layer.update()
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for k in curve.keyframe_points:k.interpolation='LINEAR'
 s.frame_start=1;s.frame_end=frames+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig;p=A/'Exports/MeshyV1'/(name+'_'+role+'.fbx');assert not p.exists()or '--revise-own'in sys.argv
 bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'ARMATURE','MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE')
 records[role]={'duration_s':duration,'frames':frames+1,'minimum_deformed_z_m_before_clearance':min(mins)};print('MEADOW_CLIP',name,role,flush=True)
rig.animation_data.action=bpy.data.actions[name+'_Idle'];s.frame_start=1;s.frame_end=73;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(dest))
walk,run=(.08,.14)if name in ['Raupy','Hornliu']else(.18,.30)if name=='Habitak'else(.40,.75)
audit=dict(species=name,source=str(source.relative_to(R)),source_sha256=digest,rig_family='Serpentine'if name in ['Raupy','Hornliu']else'Winged',catalog_size_cm=spec['height'],size_basis='original neutral mesh height including original appendages; uniform scale only',scale=scale,actual_height_cm=h*100,bones=bones,walk_speed_m_s=walk,run_speed_m_s=run,height_m=h,triangles=intake['meshes'][0]['triangles'],vertices=intake['meshes'][0]['vertices'],geometry_unchanged=True,uv_original=True,unweighted_vertices=0,clips=records)
(A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(records,indent=2));assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('MEADOW_SOURCE_READY',name,flush=True)
