"""Fit actual incoming fish, preserving original vertices, UVs and textures. No source GLB writes."""
import bpy,json,hashlib,struct,sys,math
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];name=sys.argv[sys.argv.index('--')+1];assert name in ['Karpador','Garados']
A=R/'Art/Characters/Creatures'/name;dest=A/'Source'/(name+'_Meshy_V1.blend');assert not dest.exists() or ('--revise-own' in sys.argv and str(dest.relative_to(R)) not in json.loads((R/'Saved/BiomeTestV11/Before.json').read_text())['hashes'])
source=R/'Art/Characters/Creatures/Incoming'/(name+'.glb');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest();intake=json.loads((R/'Saved/BiomeTestV11/Intake'/(name+'.json')).read_text());assert digest==intake['sha256']
for folder in ['Source','Textures/MeshyV1','Exports/MeshyV1']:(A/folder).mkdir(parents=True,exist_ok=True)
n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);data_start=20+n+8;mat=g['materials'][0]
for typ,idx in [('BaseColor',mat['pbrMetallicRoughness']['baseColorTexture']['index']),('MetallicRoughness',mat['pbrMetallicRoughness']['metallicRoughnessTexture']['index']),('Normal',mat['normalTexture']['index'])]:
 im=g['images'][g['textures'][idx]['source']];assert im['mimeType']=='image/jpeg';v=g['bufferViews'][im['bufferView']];b=raw[data_start+v.get('byteOffset',0):data_start+v.get('byteOffset',0)+v['byteLength']];p=A/'Textures/MeshyV1'/(name+'_'+typ+'.jpg');assert not p.exists() or p.read_bytes()==b
 if not p.exists():p.write_bytes(b)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.gltf(filepath=str(source));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1;ref=meshes[0];points=[ref.matrix_world@v.co for v in ref.data.vertices];mn=Vector(tuple(min(p[i]for p in points)for i in range(3)));mx=Vector(tuple(max(p[i]for p in points)for i in range(3)));origin=Vector((0,(mn.y+mx.y)/2,mn.z))
# Garados' published 6.5 m is measured along the serpentine body axis, not vertically stretching the coil.
raw_path=[(0,-.32,.22),(0,-.18,.28),(0,-.04,.25),(0,-.01,.06),(0,-.025,-.12),(0,.09,-.22),(0,.22,-.16),(0,.28,-.02),(0,.37,-.06),(0,.41,-.19),(0,.40,-.34),(0,.44,-.42)]
axis_length=sum((Vector(b)-Vector(a)).length for a,b in zip(raw_path,raw_path[1:]));scale=.9/(mx.z-mn.z)if name=='Karpador'else 6.5/axis_length
ref.name=name+'_UNMODIFIED_GLB';col=bpy.data.collections.new('UNMODIFIED_HIGH_REFERENCE');bpy.context.scene.collection.children.link(col)
for c in list(ref.users_collection):c.objects.unlink(ref)
col.objects.link(ref);col.hide_viewport=True;col.hide_render=True
body=ref.copy();body.data=ref.data.copy();body.name=name+'_Body';body.matrix_world=Matrix.Identity(4);bpy.context.scene.collection.objects.link(body)
for v,p in zip(body.data.vertices,points):v.co=(p-origin)*scale
body.data.update();bones={}
def bone(n,a,b,p):bones[n]=(tuple(a),tuple(b),p)
bone('root',(0,0,0),(0,0,.04),None)
if name=='Karpador':
 h=.9
 bone('body',(0,0,h*.47),(0,-h*.08,h*.48),'root');bone('head',(0,-h*.08,h*.48),(0,-h*.33,h*.48),'body')
 for n,a,b,p in [('tail_base',(0,.11,.43),(0,.24,.43),'body'),('tail_mid',(0,.24,.43),(0,.34,.46),'tail_base'),('tail_tip',(0,.34,.46),(0,.43,.49),'tail_mid'),('dorsal',(0,0,.63),(0,.03,.84),'body'),('ventral',(0,.04,.28),(0,.10,.10),'body')]:bone(n,a,b,p)
 for side,sg in [('L',1),('R',-1)]:bone('fin_'+side,(sg*.15,-.01,.41),(sg*.35,.07,.38),'body')
else:
 path=[(Vector(p)-origin)*scale for p in raw_path]
 bone('head',path[1],path[0],'root')
 for i,(a,b)in enumerate(zip(path[1:],path[2:])):bone('body_'+str(i),a,b,'root'if i==0 else'body_'+str(i-1))
arm=bpy.data.armatures.new(name+'_Rig');rig=bpy.data.objects.new(name+'_Rig',arm);bpy.context.scene.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for n,(a,b,parent)in bones.items():
 x=arm.edit_bones.new(n);x.head=a;x.tail=b
 if parent:x.parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
for n in bones:
 if n!='root':body.vertex_groups.new(name=n)
def near(p,candidates):
 out=[]
 for n in candidates:
  a=Vector(bones[n][0]);d=Vector(bones[n][1])-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));out.append(((p-a-t*d).length,n))
 out.sort();out=out[:2];weights=[(n,1/max(.008,d)**4)for d,n in out];total=sum(w for n,w in weights);return{n:w/total for n,w in weights}
def smooth(a,b,v):t=max(0,min(1,(v-a)/(b-a)));return t*t*(3-2*t)
for v in body.data.vertices:
 x,y,z=v.co
 if name=='Karpador':
  w=near(v.co,['body','head'])
  if y>.12:
   t=smooth(.12,.21,y);tail=near(v.co,['tail_base','tail_mid','tail_tip']);w={n:w.get(n,0)*(1-t)+tail.get(n,0)*t for n in w.keys()|tail.keys()}
  if z>.65:w={'dorsal':1}
  elif z<.25 and y>-.10:w={'ventral':1}
  elif abs(x)>.17 and .30<z<.54 and -.10<y<.18:
   t=smooth(.17,.25,abs(x));n='fin_L'if x>0 else'fin_R';w={k:a*(1-t)for k,a in w.items()};w[n]=t
 else:
  rawp=v.co/scale+origin
  w={'head':1}if rawp.y<-.19 and rawp.z>.03 else near(v.co,[n for n in bones if n.startswith('body_')])
 total=sum(w.values())
 for n,a in w.items():
  if a>1e-8:body.vertex_groups[n].add([v.index],a/total,'REPLACE')
assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in body.data.vertices)
body.parent=rig;mod=body.modifiers.new('Aquatic anatomical skin','ARMATURE');mod.object=rig
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.fps=30
for im in bpy.data.images:
 if im.type=='IMAGE':im.pack()
rest={p.name:p.bone.matrix_local.copy()for p in rig.pose.bones};records={}
for role,duration in [('Idle',2.4),('Walk',1.2),('Run',.8),('Attack',.9),('Hit',.5),('Faint',1.2),('Happy',1.6)]:
 action=bpy.data.actions.new(name+'_'+role);action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;frames=round(duration*30);mins=[]
 for frame in range(frames+1):
  s.frame_set(frame+1);t=frame/frames;wave=math.sin(math.tau*t);pulse=math.sin(math.pi*t)**2
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
  root=rig.pose.bones['root']
  if name=='Karpador':
   for i,n in enumerate(['tail_base','tail_mid','tail_tip']):rig.pose.bones[n].rotation_quaternion=Quaternion((0,0,1),(.055 if role=='Idle'else .14)*math.sin(math.tau*t-i*.65))
   for side,sg in [('L',1),('R',-1)]:rig.pose.bones['fin_'+side].rotation_quaternion=Quaternion((0,1,0),sg*(.12+.24*math.sin(math.tau*t+.3*sg)))
   rig.pose.bones['dorsal'].rotation_quaternion=Quaternion((0,1,0),.045*wave);rig.pose.bones['ventral'].rotation_quaternion=Quaternion((0,1,0),.06*wave)
  else:
   for i in range(len(path)-2):
    p=rig.pose.bones['body_'+str(i)];p.rotation_quaternion=Quaternion((0,0,1),(.018 if role=='Idle'else .045)*math.sin(math.tau*t-i*.60))@Quaternion((1,0,0),.012*math.sin(math.tau*t-i*.65+.5))
   rig.pose.bones['head'].rotation_quaternion=Quaternion((0,0,1),.015*wave)
  if role=='Attack':root.matrix=Matrix.Translation((0,-.12*scale*pulse,0))@rest['root']
  elif role=='Hit':root.matrix=Quaternion((0,0,1),.065*wave).to_matrix().to_4x4()@rest['root']
  elif role=='Faint':root.matrix=Quaternion((0,1,0),math.radians(65)*(t*t*(3-2*t))).to_matrix().to_4x4()@rest['root']
  elif role=='Happy':root.matrix=Matrix.Translation((0,0,.025*scale*math.sin(math.pi*t)**2))@rest['root']
  bpy.context.view_layer.update();ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();low=min(v.co.z for v in me.vertices);ev.to_mesh_clear()
  if low<0:
   m=root.matrix.copy();m.translation.z-=low;root.matrix=m;bpy.context.view_layer.update()
  mins.append(low)
  for p in rig.pose.bones:
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=frame+1,group=p.name)
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for k in curve.keyframe_points:k.interpolation='LINEAR'
 s.frame_start=1;s.frame_end=frames+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);body.select_set(True);bpy.context.view_layer.objects.active=rig
 p=A/'Exports/MeshyV1'/(name+'_'+role+'.fbx');assert not p.exists() or ('--revise-own' in sys.argv and str(p.relative_to(R)) not in json.loads((R/'Saved/BiomeTestV11/Before.json').read_text())['hashes']);bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'ARMATURE','MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE')
 records[role]={'duration_s':duration,'frames':frames+1,'minimum_deformed_z_m':min(mins)};print('AQUATIC_CLIP',name,role,flush=True)
rig.animation_data.action=bpy.data.actions[name+'_Idle'];s.frame_start=1;s.frame_end=73;s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(dest))
audit=dict(species=name,source=str(source.relative_to(R)),source_sha256=digest,rig_family='Aquatic'if name=='Karpador'else'Serpentine',catalog_size_cm=90 if name=='Karpador'else 650,size_basis='neutral_height'if name=='Karpador'else'hand_fitted_body_axis_length',scale=scale,actual_height_cm=(mx.z-mn.z)*scale*100,bones=bones,walk_speed_m_s=.35 if name=='Karpador'else .70,run_speed_m_s=.70 if name=='Karpador'else 1.25,height_m=(mx.z-mn.z)*scale,triangles=intake['meshes'][0]['triangles'],vertices=intake['meshes'][0]['vertices'],geometry_unchanged=True,uv_original=True,unweighted_vertices=0,clips=records)
(A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));(A/'MeshyV1_AnimationAudit.json').write_text(json.dumps(records,indent=2));assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('AQUATIC_READY',name,audit['actual_height_cm'],flush=True)
