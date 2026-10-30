"""Technical rig/weight/animation derivation of Harry's unchanged Meshy Garados. No new mesh topology."""
import bpy,json,math,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GaradosWaterV2';A=R/'Art/Characters/Creatures/Garados';source=A/'Source/Garados_Meshy_V1.blend';out=A/'Source/Garados_Water_V2.blend';revise='--revise-generated'in sys.argv;assert not out.exists()or revise;digest=hashlib.sha256(source.read_bytes()).hexdigest();original_hash=hashlib.sha256((R/'Art/Characters/Creatures/Incoming/Garados.glb').read_bytes()).hexdigest();assert original_hash=='ce0661729d56dfa628a3232f4296bd5ae3bd51a914f417e8e82426e33133f5b9'
bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;oldrig=bpy.data.objects['Garados_Rig'];original=bpy.data.objects['Garados_Body'];oldrig.animation_data.action=None
for p in oldrig.pose.bones:p.matrix_basis=Matrix.Identity(4)
pts=[oldrig.data.bones['body_'+str(i)].head_local.copy()for i in range(10)]+[oldrig.data.bones['body_9'].tail_local.copy()]
# Subdivide the actual fitted axis. No point, face, material or UV coordinate is generated/replaced.
path=[]
for a,b in zip(pts,pts[1:]):path.extend([a,(a+b)*.5])
path.append(pts[-1]);reference=bpy.data.collections.new('UNCHANGED_MESHY_WORK_REFERENCE');bpy.context.scene.collection.children.link(reference)
for o in [original,oldrig]:
 for c in list(o.users_collection):c.objects.unlink(o)
 reference.objects.link(o)
reference.hide_viewport=True;reference.hide_render=True
body=original.copy();body.data=original.data.copy();body.name='Garados_Water_Body';body.parent=None;body.modifiers.clear();body.vertex_groups.clear();bpy.context.scene.collection.objects.link(body)
arm=bpy.data.armatures.new('Garados_Water_Rig');rig=bpy.data.objects.new('Garados_Water_Rig',arm);bpy.context.scene.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def b(n,h,t,parent):
 x=arm.edit_bones.new(n);x.head=h;x.tail=t
 if parent:x.parent=arm.edit_bones[parent]
b('root',Vector(),Vector((0,0,.04)),None);b('head',path[0],oldrig.data.bones['head'].tail_local.copy(),'root')
for i,(h,t)in enumerate(zip(path,path[1:])):b('spine_'+str(i).zfill(2),h,t,'root'if i==0 else'spine_'+str(i-1).zfill(2))
bpy.ops.object.mode_set(mode='OBJECT');names=['spine_'+str(i).zfill(2)for i in range(20)];lengths=[rig.data.bones[n].length for n in names]
for n in ['head']+names:body.vertex_groups.new(name=n)
def ramp(a,b,x):
 t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
# Weld positions virtually for skin-space analysis; source faces and UV seams remain unchanged.
import numpy as np
co=np.array([list(v.co)for v in body.data.vertices]);_,inv=np.unique(np.rint(co/1e-6).astype(np.int64),axis=0,return_inverse=True);N=int(inv.max())+1;pos=np.zeros((N,3));counts=np.bincount(inv)
for v in body.data.vertices:pos[inv[v.index]]+=co[v.index]
pos/=counts[:,None];graph=[{}for _ in range(N)]
for e in body.data.edges:
 a,b=(int(inv[i])for i in e.vertices)
 if a!=b:graph[a][b]=graph[b][a]=float(np.linalg.norm(pos[a]-pos[b]))
sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from SmoothSkin import smooth
rest={b.name:b.matrix_local.copy()for b in rig.data.bones};s=bpy.context.scene;s.render.fps=30;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;export=A/'Exports/WaterV2';export.mkdir(exist_ok=True)
def setbone(n,h,d):
 old=rig.data.bones[n].tail_local-rig.data.bones[n].head_local;old_angle=math.atan2(old.z,old.y);angle=math.atan2(d.z,d.y);flat=Quaternion((1,0,0),angle-old_angle);yaw=math.atan2(-d.x,d.y)if n!='head'else math.atan2(d.x,-d.y);q=Quaternion((0,0,1),yaw)@flat;m=q.to_matrix().to_4x4()@rest[n];m.translation=h;rig.pose.bones[n].matrix=m;bpy.context.view_layer.update()
water_pitch=[0. for _ in range(20)]
def pose(phase,strength=1,observe=0,turn=0):
 for p in rig.pose.bones:p.matrix_basis=Matrix.Identity(4)
 # Forebody rises while the posterior body remains on its horizontal, submerged plane.
 angles=[water_pitch[i]+math.radians(-50*max(0.,1-i/8)**1.2)*observe for i in range(20)]
 basez=1.65;headz=basez-sum(L*math.sin(a)for L,a in zip(lengths,angles));pos=Vector((0,-sum(lengths)/2+.65,headz+.12));setbone('head',pos,Vector((.006*math.sin(phase),-1,.02*observe)))
 for i,(n,L)in enumerate(zip(names,lengths)):
  t=i/19;wave=strength*(.012+.17*t*t)*math.sin(phase-t*math.tau*1.25);bend=-turn*.48*t;pitch=angles[i]-(.025 if i<8 else 0);d=Vector((math.sin(wave+bend)*math.cos(pitch),math.cos(wave+bend)*math.cos(pitch),math.sin(pitch)));setbone(n,pos,d);pos+=d*L
# Continuous surface-based uncoiling. A harmonic longitudinal coordinate follows
# the connected original skin, so nearby S-folds do not steal one another's weights.
orig=np.zeros((N,3))
for v in original.data.vertices:orig[inv[v.index]]+=np.array(v.co)
orig/=counts[:,None];edge=np.array([(a,b)for a in range(N)for b in graph[a]if a<b]);ea,eb=edge.T;conduct=1/np.maximum(.002,np.linalg.norm(orig[ea]-orig[eb],axis=1));degree=np.bincount(ea,weights=conduct,minlength=N)+np.bincount(eb,weights=conduct,minlength=N)
fixed=(orig[:,1]<-1.15)|((orig[:,1]>.8)&(orig[:,2]<.12));bc=np.zeros(N);bc[(orig[:,1]>.8)&(orig[:,2]<.12)]=1.;free=~fixed
rhs=np.bincount(ea,weights=conduct*bc[eb],minlength=N)+np.bincount(eb,weights=conduct*bc[ea],minlength=N);rhs[fixed]=0

def multiply(v):
 result=degree*v-np.bincount(ea,weights=conduct*v[eb],minlength=N)-np.bincount(eb,weights=conduct*v[ea],minlength=N);result[fixed]=0;return result
u=np.zeros(N);res=rhs.copy();z=res/np.maximum(degree,1e-9);direction=z.copy();rz=np.dot(res,z)
for solve_iteration in range(4000):
 product=multiply(direction);alpha=rz/max(np.dot(direction,product),1e-20);u+=alpha*direction;res-=alpha*product
 if np.linalg.norm(res)<1e-6:break
 z=res/np.maximum(degree,1e-9);next_rz=np.dot(res,z);direction=z+next_rz/max(rz,1e-30)*direction;rz=next_rz
u+=bc;assert np.linalg.norm(res)<.01;print('WATER_LONGITUDINAL_FIELD',solve_iteration,float(np.linalg.norm(res)),flush=True)
# Disconnected original horns/fins remain original geometry and attach at their
# nearest anatomical base on the connected body, never across a nearby fold.
components=[];seen=set()
for j in range(N):
 if j in seen:continue
 cc=[];stack=[j];seen.add(j)
 while stack:
  k=stack.pop();cc.append(k)
  for n in graph[k]:
   if n not in seen:seen.add(n);stack.append(n)
 components.append(cc)
components.sort(key=len,reverse=True);main=np.array(components[0]);from mathutils.kdtree import KDTree
kd=KDTree(len(main))
for j in main:kd.insert(Vector(orig[j]),int(j))
kd.balance()
for cc in components[1:]:
 links=sorted((kd.find(Vector(orig[j]))[2],j,kd.find(Vector(orig[j]))[1])for j in cc);base=[k for _,j,k in links[:max(3,len(cc)//12)]];value=float(np.median(u[base]));u[cc]=value
# Fit ring centres from the lateral shell; fins and whiskers are not centreline samples.
levels=np.linspace(0,1,151);curve=[]
for value in levels:
 ids=main[np.argsort(abs(u[main]-value))[:100]];width=np.quantile(abs(orig[ids,0]),.8);ids=ids[abs(orig[ids,0])>=max(.02,width*.8)];curve.append(np.median(orig[ids],axis=0))
curve=np.array(curve);curve[:,0]=0
for axis in [1,2]:curve[:,axis]=np.convolve(np.pad(curve[:,axis],(3,3),mode='edge'),np.ones(7)/7,mode='valid')
head_point=np.array([0.,-1.05,3.0]);tail_point=np.mean(orig[main][orig[main,2]<.12],axis=0);head_level=float(np.median(u[np.argsort(np.linalg.norm(orig-head_point,axis=1))[:30]]));tail_level=float(np.median(u[main[np.argsort(np.linalg.norm(orig[main]-tail_point,axis=1))[:30]]]));print('FIELD_ENDPOINTS',head_level,tail_level,float(u.min()),float(u.max()),flush=True);assert tail_level>head_level+.2
keep=(levels>head_level)&(levels<tail_level);levels=np.r_[head_level,levels[keep],tail_level];curve=np.vstack([head_point,curve[keep],tail_point]);tangent=np.gradient(curve,axis=0);tangent/=np.maximum(np.linalg.norm(tangent,axis=1)[:,None],1e-8);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(curve,axis=0),axis=1))];arc*=sum(lengths)/arc[-1];head_y=-sum(lengths)/2+.65
old_head=oldrig.data.bones['head'].tail_local-oldrig.data.bones['head'].head_local;head_rotation=Quaternion((1,0,0),math.pi-math.atan2(old_head.z,old_head.y));new_head=Vector((0,head_y,1.77))
for v in body.data.vertices:
 j=inv[v.index];value=u[j];c=np.array([np.interp(value,levels,curve[:,axis])for axis in range(3)]);d=np.array([np.interp(value,levels,tangent[:,axis])for axis in range(3)]);d/=max(np.linalg.norm(d),1e-9);offset=orig[j]-c;along=float(np.dot(offset,d));radial=float(offset[2]*d[1]-offset[1]*d[2]);distance=float(np.interp(value,levels,arc));p=Vector((orig[j,0],head_y+distance+along,1.77-distance*.015+radial));h=head_rotation@(Vector(orig[j])-Vector(head_point))+new_head;blend=ramp(-1.15,-.9,orig[j,1]);v.co=h.lerp(p,blend)
body.modifiers.clear();rig.animation_data_clear();bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');pos=new_head.copy();arm.edit_bones['head'].head=pos;arm.edit_bones['head'].tail=pos+Vector((0,-.62,0))
for n,L in zip(names,lengths):arm.edit_bones[n].head=pos;arm.edit_bones[n].tail=pos+Vector((0,L,0));pos+=Vector((0,L,0))
bpy.ops.object.mode_set(mode='OBJECT');rest={b.name:b.matrix_local.copy()for b in rig.data.bones};centres_y=[(rig.data.bones[n].head_local.y+rig.data.bones[n].tail_local.y)*.5 for n in names]
for v in body.data.vertices:
 for g in body.vertex_groups:g.remove([v.index])
 head=1-ramp(head_y-.12,head_y+.15,v.co.y);w=[math.exp(-((v.co.y-y)/.19)**2)for y in centres_y];total=sum(w)
 for j,value in enumerate(w):
  value=value/max(total,1e-12)*(1-head)
  if value>1e-7:body.vertex_groups[names[j]].add([v.index],value,'REPLACE')
 if head>1e-7:body.vertex_groups['head'].add([v.index],head,'REPLACE')
weights=smooth(body,iterations=12);weights.pop('no_geometry_or_uv_changes',None);weights['original_faces_and_uvs_unchanged']=True;body.parent=rig;body.data.update();mod=body.modifiers.new('Water rest pose skin','ARMATURE');mod.object=rig
roles={'SwimIdle':(.20,0,0),'SwimSlow':(.5,0,0),'SwimNormal':(1.,0,0),'SwimFast':(1.4,0,0),'SwimTurnLeft':(1.,0,1),'SwimTurnRight':(1.,0,-1),'SwimObserve':(.22,1,0),'SwimAttack':(.3,1,0),'SwimHit':(.25,0,0),'SwimFaint':(.1,.2,0),'SwimHappy':(.4,.35,0)};audits={}
for role,(strength,observe,turn)in roles.items():
 action=bpy.data.actions.new('Garados_'+role+'_V2');action.use_fake_user=True;rig.animation_data_create();rig.animation_data.action=action;seconds=2.4 if role in ['SwimIdle','SwimObserve']else 1.6;frames=round(seconds*30)
 for f in range(frames+1):
  s.frame_set(f+1);phase=math.tau*f/frames;pose(phase,strength,observe,turn)
  pulse=math.sin(math.pi*f/frames)**2;root=rig.pose.bones['root']
  if role=='SwimAttack':root.matrix_basis=Matrix.Translation((0,-.25*pulse,0))
  elif role=='SwimHit':root.matrix_basis=Quaternion((0,0,1),.045*math.sin(phase)).to_matrix().to_4x4()
  elif role=='SwimFaint':
   progress=(f/frames)**2*(3-2*f/frames);pivot=Vector((0,0,1.7));root.matrix_basis=Matrix.Translation(pivot+Vector((0,0,-.06*progress)))@Quaternion((0,1,0),.24*progress).to_matrix().to_4x4()@Matrix.Translation(-pivot)
  elif role=='SwimHappy':root.matrix_basis=Matrix.Translation((0,0,.08*pulse))
  bpy.context.view_layer.update()
  for p in rig.pose.bones:
   p.rotation_mode='QUATERNION'
   for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=prop,frame=f+1,group=p.name)
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for k in curve.keyframe_points:k.interpolation='LINEAR'
 s.frame_start=1;s.frame_end=frames+1;s.frame_set(1);bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=str(export/('Garados_'+role+'_V2.fbx')),use_selection=True,object_types={'ARMATURE','MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0,mesh_smooth_type='FACE');audits[role]={'seconds':seconds,'frames':frames+1,'strength':strength,'observe':observe,'turn':turn};print('WATER_CLIP',role,flush=True)
rig.animation_data.action=bpy.data.actions['Garados_SwimNormal_V2'];s.frame_start=1;s.frame_end=49;s.frame_set(1)
for im in bpy.data.images:
 if im.type=='IMAGE':im.pack()
assert len(body.data.vertices)==len(original.data.vertices)and len(body.data.polygons)==len(original.data.polygons);assert all(list(p.vertices)==list(q.vertices)for p,q in zip(body.data.polygons,original.data.polygons));assert all((v.uv-w.uv).length<1e-8 for v,w in zip(body.data.uv_layers.active.data,original.data.uv_layers.active.data));assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;bpy.ops.wm.save_as_mainfile(filepath=str(out))
(A/'WaterV2_Audit.json').write_text(json.dumps({'original_glb':'Art/Characters/Creatures/Incoming/Garados.glb','original_glb_sha256':original_hash,'original_working_source_sha256':digest,'derived_source':str(out.relative_to(R)),'original_topology_faces_uvs_unchanged':True,'water_rest_pose':'Continuous surface-guided uncoiling of the original vertices; original working/source files unchanged','new_spine_segments':20,'bones':len(arm.bones),'body_axis_length_m':sum(lengths),'weight_smoothing':weights,'uncoiling':'Harmonic coordinate on connected original body; disconnected original fins/horns attached at nearest body base; original faces and UVs retained','longitudinal_solver_residual':float(np.linalg.norm(res)),'clips':audits,'land_and_battle_original_rig_animations_untouched':True},indent=2));print('WATER_SOURCE_READY',flush=True)
