"""New Glurak source: welded-surface wing skin, anatomical mirrored flaps and ground-hover clips."""
import bpy,json,math,hashlib,heapq,numpy as np
from mathutils import Vector,Quaternion,Matrix
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Glurak';source=A/'Source/Glurak_MotionV5.blend';assert not source.exists();original=A/'Source/Glurak_PolishV4.blend';digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=digest(original);bpy.ops.wm.open_mainfile(filepath=str(original));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;body=bpy.data.objects['Glurak_Body'];rig=bpy.data.objects['Glurak_Rig'];pb=rig.pose.bones;co=np.array([tuple(v.co)for v in body.data.vertices]);uv=[tuple(v.uv)for v in body.data.uv_layers.active.data];edges=np.array([e.vertices[:]for e in body.data.edges]);lengths=np.linalg.norm(co[edges[:,0]]-co[edges[:,1]],axis=1);names=[g.name for g in body.vertex_groups];weights=np.zeros((len(co),len(names)))
for v in body.data.vertices:
 for g in v.groups:weights[v.index,g.group]=g.weight
_,inv=np.unique(np.rint(co/1e-5).astype(np.int64),axis=0,return_inverse=True);N=int(inv.max())+1;pos=np.zeros((N,3));count=np.bincount(inv);np.add.at(pos,inv,co);pos/=count[:,None];ends=np.unique(np.sort(inv[edges],axis=1),axis=0);ends=ends[ends[:,0]!=ends[:,1]];adj=[[]for _ in range(N)]
for a,b in ends:
 l=float(np.linalg.norm(pos[a]-pos[b]));adj[a].append((int(b),l));adj[b].append((int(a),l))
mask=np.zeros(len(co));attr=body.data.color_attributes['PolishV4']
for i,l in enumerate(body.data.loops):mask[l.vertex_index]=max(mask[l.vertex_index],attr.data[i].color[0])
wing_seeds=np.unique(inv[(mask>.5)&(abs(co[:,0])>.25)&(co[:,2]>.65)]);protected=(abs(pos[:,0])<.19)|(pos[:,2]<.60)|(pos[:,1]>.48)|((pos[:,1]<-.24)&(abs(pos[:,0])<.90)&(pos[:,2]<1.1))|((pos[:,1]<-.075)&(abs(pos[:,0])<.36)&(pos[:,2]>1.1));body_seeds=np.flatnonzero(protected)
def distances(seeds):
 d=np.full(N,np.inf);heap=[]
 for i in seeds:d[i]=0;heap.append((0.,int(i)))
 heapq.heapify(heap)
 while heap:
  v,i=heapq.heappop(heap)
  if v!=d[i]:continue
  for j,l in adj[i]:
   if v+l<d[j]:d[j]=v+l;heapq.heappush(heap,(v+l,j))
 return d
dw=distances(wing_seeds);db=distances(body_seeds);field=np.nan_to_num(db-dw,nan=-1,posinf=1,neginf=-1);t=np.clip(field/.13,0,1);t=t*t*(3-2*t);t[protected]=0
def ramp(a,b,x):
 q=np.clip((x-a)/(b-a),0,1);return q*q*(3-2*q)
front=-.12-.22*ramp(1.0,1.2,pos[:,2]);geometry=ramp(.24,.52,abs(pos[:,0]))*np.clip((pos[:,1]-front+.05)/.05,0,1)*ramp(.60,.80,pos[:,2])*(1-ramp(.38,.50,pos[:,1]));t=np.maximum(t,geometry);t[protected]=0
t=np.minimum(t,ramp(.22,.64,abs(pos[:,0])))
W=np.zeros((N,len(names)));np.add.at(W,inv,weights);W/=count[:,None];wi=[i for i,n in enumerate(names)if n.startswith('wing_')];affected=(t>1e-5)|(W[:,wi].sum(1)>.001);new=W.copy()
for i in np.flatnonzero(affected):
 base=W[i].copy();base[wi]=0
 if t[i]>.001:base[:]=0;base[names.index('chest')]=1
 if base.sum()<1e-7:base[names.index('chest')]=1
 base/=base.sum();side='L'if pos[i,0]>0 else'R';wing=np.zeros(len(names));tip=np.clip((abs(pos[i,0])-.95)/.65,0,1)*.28;wing[names.index('wing_base_'+side)]=1-tip;wing[names.index('wing_tip_'+side)]=tip;new[i]=base*(1-t[i])+wing*t[i]
# The continuous geometric field must not be diluted by unrelated old hand weights.
order=np.argsort(new,axis=1)[:,-4:];top=np.zeros_like(new,dtype=bool);np.put_along_axis(top,order,True,axis=1);new*=top;new/=new.sum(1)[:,None];changed=[]
for v in body.data.vertices:
 if not affected[inv[v.index]]:continue
 for g in body.vertex_groups:g.remove([v.index])
 for k in order[inv[v.index]]:
  if new[inv[v.index],k]>1e-8:body.vertex_groups[int(k)].add([v.index],float(new[inv[v.index],k]),'REPLACE')
 changed.append(v.index)
def smooth(a,b,x):
 u=max(0,min(1,(x-a)/(b-a)));return u*u*(3-2*u)
def rotate(n,axis,angle):
 rest=pb[n].bone.matrix_local.to_quaternion();pb[n].rotation_quaternion=rest.inverted()@Quaternion(axis,angle)@rest
cache={};original_actions={}
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']:
 old=bpy.data.actions['Glurak_'+role];original_actions[role]=old;rig.animation_data.action=old;lo,hi=map(int,old.frame_range);cache[role]={}
 for f in range(lo,hi+1):s.frame_set(f);cache[role][f]={b.name:(b.location.copy(),b.rotation_quaternion.copy(),b.scale.copy())for b in pb}
 old.name='REF_Glurak_'+role;old.use_fake_user=True
created={}
for role in ['Idle','Walk','Run','Attack','Hit','Faint','Happy','Takeoff','Hover','Land']:
 count={'Takeoff':49,'Hover':37,'Land':43}.get(role,max(cache[role])if role in cache else 61);a=bpy.data.actions.new('Glurak_'+role+'_MotionV5');a.use_fake_user=True;rig.animation_data.action=a;created[role]=a
 for f in range(1,count+1):
  u=(f-1)/(count-1);phase=math.tau*u;refrole=role if role in cache else'Idle';ref=cache[refrole][1+round(u*(max(cache[refrole])-1))];s.frame_set(f)
  for b in pb:b.location,b.rotation_quaternion,b.scale=ref[b.name]
  flying=smooth(.18,.85,u)if role=='Takeoff'else 1-smooth(.1,.82,u)if role=='Land'else 1. if role=='Hover'else 0.
  amp={'Idle':.035,'Walk':.055,'Run':.085,'Attack':.20,'Hit':.035,'Faint':.012,'Happy':.12,'Takeoff':.38,'Hover':.36,'Land':.30}[role]
  wave=math.sin(phase)+.16*math.sin(phase*2)
  if role=='Takeoff':wave=math.sin(phase*2.0)*smooth(.05,.3,u);amp*=smooth(.02,.3,u)
  if role=='Land':amp*=1-smooth(.55,1,u)
  for side,sign in [('L',1),('R',-1)]:
   rotate('wing_base_'+side,(0,1,0),sign*(-.025+amp*wave));rotate('wing_tip_'+side,(0,1,0),sign*(.035*math.sin(phase-.4)if flying else .012*math.sin(phase-.3)))
   # Retain established body/leg/tail motion; no unverified flight-leg retargeting.
  for b in pb:
   for prop in ['location','rotation_quaternion','scale']:b.keyframe_insert(data_path=prop,frame=f,group=b.name)
 for layer in a.layers:
  for strip in layer.strips:
   for cb in strip.channelbags:
    for curve in cb.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
# All original vertices and UVs remain exactly the same.
assert np.array_equal(co,np.array([tuple(v.co)for v in body.data.vertices]));assert uv==[tuple(v.uv)for v in body.data.uv_layers.active.data]
metrics={};wing_edges=(t[inv[edges[:,0]]]> .3)&(t[inv[edges[:,1]]]> .3)
for role,a in created.items():
 rig.animation_data.action=a;lo,hi=map(int,a.frame_range);zs=[];growth=[];worst=None;lowest=None
 for f in range(lo,hi+1):
  s.frame_set(f);ob=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh();pts=np.array([tuple(v.co)for v in m.vertices]);zs.append(float(pts[:,2].min()));g=np.linalg.norm(pts[edges[:,0]]-pts[edges[:,1]],axis=1)-lengths;growth.append(float(g[wing_edges].max()));ix=np.flatnonzero(wing_edges)[np.argmax(g[wing_edges])];low=int(np.argmin(pts[:,2]));
  if worst is None or growth[-1]>worst['growth_m']:worst=dict(frame=f,growth_m=growth[-1],edge=[dict(vertex=int(j),rest=co[j].tolist(),field=float(t[inv[j]]),wing_distance=float(dw[inv[j]]),body_distance=float(db[inv[j]]),weights={body.vertex_groups[z.group].name:z.weight for z in body.data.vertices[j].groups})for j in edges[ix]])
  if lowest is None or pts[low,2]<lowest['z']:lowest=dict(frame=f,z=float(pts[low,2]),vertex=low,rest=co[low].tolist(),field=float(t[inv[low]]))
  ob.to_mesh_clear()
 metrics[role]=dict(minimum_z_cm=min(zs)*100,maximum_wing_edge_growth_cm=max(growth)*100,frames=hi-lo+1,worst=worst,lowest=lowest);print(role,metrics[role],flush=True)
(R/'Saved/MotionRefinementV5/GlurakCandidateAudit.json').write_text(json.dumps(metrics,indent=2));assert max(x['maximum_wing_edge_growth_cm']for x in metrics.values())<6.,'Wing deformation failed; not saved'
rig.animation_data.action=created['Idle'];s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(source));assert digest(original)==before
(A/'MotionV5_Audit.json').write_text(json.dumps(dict(source=str(source.relative_to(R)),source_sha256=digest(source),original_sha256=before,original_geometry_uvs_preserved=True,changed_weight_vertices=len(changed),wing_seeds=len(wing_seeds),virtual_welded_vertices=N,metrics=metrics,actions={k:v.name for k,v in created.items()}),indent=2));print('GLURAK_MOTION_SOURCE_SAVED',flush=True)
