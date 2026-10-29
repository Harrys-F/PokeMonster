"""Authored Raichu candidate, Blender 5.2; no existing model is modified or reused as a disguise.
Metres; front -Y, Z up. Named surfaces, simple custom rig; source remains editable.
Run once into an absent namespace; --revise only for this task's own uncommitted candidate.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Raichu';D=R/'Saved/ProjectRefinement/ModelsV4';O=A/'Source/Raichu_V4.blend'
assert not O.exists()or '--revise'in sys.argv
for p in [O.parent,A/'Exports/V4',D/'Blender']:p.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1.;s.render.fps=30
mats={}
for name,color,rough in [('Coat',(.66,.215,.035),.52),('Cream',(.86,.73,.47),.6),('Brown',(.13,.052,.024),.51),('Gold',(.95,.62,.035),.48),('Eyes',(.008,.009,.012),.19),('Highlight',(.9,.94,.91),.27)]:
 m=bpy.data.materials.new('Raichu_'+name);m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;m.diffuse_color=(*color,1);mats[name]=m
parts=[];core=[]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def material(o,key):o.data.materials.clear();o.data.materials.append(mats[key]);return o
def weights(o,w):
 for name,value in w.items():o.vertex_groups.new(name=name).add(list(range(len(o.data.vertices))),value,'REPLACE')
def uv(name,c,scale,key,bone=None,body=False):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=c);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);material(o,key)
 for f in o.data.polygons:f.use_smooth=True
 (core if body else parts).append(o)
 if bone:weights(o,{bone:1})
 return o
def mesh(name,vs,fs,key,bone):
 data=bpy.data.meshes.new(name);data.from_pydata(vs,[],fs);data.update();o=bpy.data.objects.new(name,data);s.collection.objects.link(o);material(o,key);weights(o,{bone:1})
 for f in data.polygons:f.use_smooth=True
 parts.append(o);return o
def tube(name,points,radii,key,bones):
 vs=[];fs=[];N=12
 for i,c in enumerate(points):
  d=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u)
  for j in range(N):vs.append(tuple(Vector(c)+(u*math.cos(j*math.tau/N)+v*math.sin(j*math.tau/N))*radii[i]))
 for i in range(len(points)-1):
  for j in range(N):fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 fs += [tuple(range(N-1,-1,-1)),tuple((len(points)-1)*N+j for j in range(N))]
 o=mesh(name,vs,fs,key,bones[0]);o.vertex_groups.clear()
 for i in range(len(points)):
  bn=bones[min(i,len(bones)-1)]
  if bn not in o.vertex_groups:o.vertex_groups.new(name=bn)
  o.vertex_groups[bn].add(list(range(i*N,(i+1)*N)),1,'REPLACE')
 return o
# Connected organic core; union/remesh only the new authored surfaces, never an original asset.
uv('Pear shaped torso',(0,.022,.29),(.176,.132,.222),'Coat',body=True)
uv('Soft neck',(0,.006,.427),(.113,.106,.111),'Coat',body=True)
uv('Broad friendly head',(0,-.025,.53),(.163,.129,.145),'Coat',body=True)
uv('Soft muzzle',(0,-.116,.485),(.101,.054,.066),'Coat',body=True)
for sign in [-1,1]:
 uv('Haunch',(sign*.124,.015,.16),(.082,.082,.123),'Coat',body=True)
 uv('Upper forepaw',(sign*.166,-.013,.34),(.047,.046,.079),'Coat',body=True)
 uv('Forepaw wrist',(sign*.182,-.039,.29),(.039,.04,.044),'Coat',body=True)
bpy.ops.object.select_all(action='DESELECT')
for o in core:o.select_set(True)
bpy.context.view_layer.objects.active=core[0];bpy.ops.object.join();body=bpy.context.object;body.name='Raichu_OrganicCore'
rm=body.modifiers.new('Connected authored skin','REMESH');rm.mode='VOXEL';rm.voxel_size=.0045;rm.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rm.name)
sm=body.modifiers.new('Soft anatomical junctions','SMOOTH');sm.factor=.72;sm.iterations=4;bpy.ops.object.modifier_apply(modifier=sm.name)
dec=body.modifiers.new('Efficient curved surface','DECIMATE');dec.ratio=.55;bpy.ops.object.modifier_apply(modifier=dec.name)
for f in body.data.polygons:f.use_smooth=True
for bn in ['pelvis','chest','head','upperarm_L','forearm_L','upperarm_R','forearm_R','thigh_L','shin_L','thigh_R','shin_R']:body.vertex_groups.new(name=bn)
for vert in body.data.vertices:
 x,y,z=vert.co;side='L'if x>=0 else'R';arm=smooth(.118,.164,abs(x))*(1-smooth(.365,.415,z))*smooth(.235,.27,z);leg=smooth(.065,.11,abs(x))*(1-smooth(.19,.23,z));head=smooth(.406,.46,z);chest=smooth(.27,.40,z)*(1-head);w={'pelvis':(1-head-chest)*(1-arm)*(1-leg),'chest':chest*(1-arm),'head':head,'upperarm_'+side:arm*smooth(.285,.33,z),'forearm_'+side:arm*(1-smooth(.285,.33,z)),'thigh_'+side:leg*smooth(.10,.15,z),'shin_'+side:leg*(1-smooth(.10,.15,z))};total=sum(w.values())
 for bn,v in w.items():
  if v>1e-6:body.vertex_groups[bn].add([vert.index],v/total,'REPLACE')
parts.append(body)
# Belly patch follows the front ellipsoid, clean broad silhouette, not a separate bulging belly.
vs=[(0,-.112,.28)];fs=[];N=48;NR=12
for k in range(1,NR+1):
 r=k/NR
 for j in range(N):
  t=j/N*math.tau;x=.119*r*math.cos(t);z=.285+.157*r*math.sin(t);y=.022-.132*math.sqrt(max(.001,1-(x/.176)**2-((z-.29)/.222)**2))-.0012;vs.append((x,y,z))
for j in range(N):fs.append((0,1+j,1+(j+1)%N))
for k in range(NR-1):
 for j in range(N):a=1+k*N+j;b=1+k*N+(j+1)%N;fs.append((a,b,b+N,a+N))
belly=mesh('Cream belly',vs,fs,'Cream','pelvis')
# Expressive face, flush cheeks and eyes; no baked light or emissive body.
for sign in [-1,1]:
 uv('Golden cheek',(sign*.119,-.12,.486),(.037,.014,.031),'Gold','head')
 eye=uv('Eye',(sign*.066,-.145,.559),(.023,.010,.031),'Eyes','head')
 uv('Eye glint',(sign*.066-.005,-.154,.572),(.006,.0026,.008),'Highlight','head')
 uv('Small forepaw',(sign*.183,-.045,.276),(.039,.039,.036),'Brown','hand_'+('L'if sign>0 else'R'))
 uv('Long hind paw',(sign*.119,-.047,.033),(.061,.097,.030),'Brown','foot_'+('L'if sign>0 else'R'))
 for t in [-.018,.018]:tube('Toe fold',[(sign*.119+t,-.123,.035),(sign*.119+t,-.105,.052)], [.0011,.0011],'Coat',['foot_'+('L'if sign>0 else'R')]*2)
uv('Nose',(0,-.173,.523),(.012,.009,.008),'Brown','head')
tube('Quiet smile',[(-.037,-.158,.482),(-.02,-.170,.478),(0,-.174,.483),(.02,-.170,.478),(.037,-.158,.482)],[.0018]*5,'Brown',['head']*5)
# Raichu's broad swept ears: dark outer rim, golden interior, curved tip, closed thickness.
def catmull(values,steps=5):
 out=[]
 for i in range(len(values)-1):
  p0=Vector(values[max(0,i-1)]);p1=Vector(values[i]);p2=Vector(values[i+1]);p3=Vector(values[min(len(values)-1,i+2)])
  for j in range(steps):
   t=j/steps;out.append(tuple(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)))
 out.append(values[-1]);return out
for sign in [-1,1]:
 side='L'if sign>0 else'R';centers=[(.104,.607),(.157,.665),(.209,.721),(.263,.766),(.294,.791),(.314,.781),(.311,.757),(.297,.744)];widths=[.020,.036,.042,.037,.022,.013,.010,.003];curved=catmull([(x,z,w)for (x,z),w in zip(centers,widths)]);centers=[(x,z)for x,z,w in curved];widths=[w for x,z,w in curved];vs=[];fs=[]
 for i,((x,z),w)in enumerate(zip(centers,widths)):
  prev=Vector(centers[max(0,i-1)]);nxt=Vector(centers[min(len(centers)-1,i+1)]);d=(nxt-prev).normalized();per=Vector((-d.y,d.x))
  for dep in [-.014,.014]:
   for a in [-1,1]:vs.append((sign*(x+per.x*w*a),-.017+dep,z+per.y*w*a))
 for i in range(len(centers)-1):
  a=i*4;b=a+4
  fs += [(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,a+2+4,a+2),(a+1,a+3,b+3,b+1)]
 fs += [(0,2,3,1),tuple(4*(len(centers)-1)+j for j in [0,1,3,2])]
 ear=mesh('Swept outer ear '+side,vs,fs,'Brown','ear_'+side);be=ear.modifiers.new('Soft ear rim','BEVEL');be.width=.005;be.segments=3;bpy.context.view_layer.objects.active=ear;bpy.ops.object.select_all(action='DESELECT');ear.select_set(True);bpy.ops.object.modifier_apply(modifier=be.name)
 # Raised inset avoids z-fighting and remains attached to exactly the same ear bone.
 vs=[];fs=[]
 for i in range(1,len(centers)-1):
  x,z=centers[i];d=(Vector(centers[i+1])-Vector(centers[i-1])).normalized();per=Vector((-d.y,d.x));w=widths[i]*.63
  for a in [-1,1]:vs.append((sign*(x+per.x*w*a),-.0325,z+per.y*w*a))
 for i in range(len(vs)//2-1):fs.append((i*2,i*2+1,i*2+3,i*2+2))
 mesh('Golden inner ear '+side,vs,fs,'Gold','ear_'+side)
# Two characteristic back bands, following rear surface.
for zc,wid in [(.377,.095),(.320,.124)]:
 vs=[];fs=[]
 for k in range(3):
  z=zc+(k-1)*.012
  for j in range(25):x=wid*(j/12-1);y=.022+.132*math.sqrt(max(.001,1-(x/.176)**2-((z-.29)/.222)**2))+.0012;vs.append((x,y,z))
 for k in range(2):
  for j in range(24):a=k*25+j;fs.append((a,a+25,a+26,a+1))
 mesh('Brown back band',vs,fs,'Brown','chest'if zc>.35 else'pelvis')
tail=[(0,.145,.205),(.045,.224,.188),(.15,.29,.18),(.29,.30,.214),(.41,.27,.282),(.47,.22,.38)]
tube('Long thin tail',tail,[.012,.010,.008,.007,.006,.005],'Brown',['tail_01','tail_01','tail_02','tail_03','tail_04','tail_tip'])
# Closed, bevelled lightning end; distinct from Pikachu's short broad zigzag tail.
poly=[(.462,.375),(.468,.538),(.521,.511),(.529,.699),(.642,.648),(.566,.578),(.553,.481),(.507,.492),(.481,.37)];vs=[(x,.22+dy,z)for dy in [-.009,.009]for x,z in poly];N=len(poly);fs=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]+[(j,(j+1)%N,(j+1)%N+N,j+N)for j in range(N)]
bolt=mesh('Lightning tail end',vs,fs,'Gold','tail_tip');be=bolt.modifiers.new('Soft lightning edge','BEVEL');be.width=.006;be.segments=3;bpy.context.view_layer.objects.active=bolt;bpy.ops.object.select_all(action='DESELECT');bolt.select_set(True);bpy.ops.object.modifier_apply(modifier=be.name)
# One draw mesh with six compact material slots, no extra effect actors.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object;body.name='Raichu';bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(65),island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
arm=bpy.data.armatures.new('Raichu_Rig');rig=bpy.data.objects.new('Raichu_Rig',arm);s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(n,h,t,pa=None):
 b=arm.edit_bones.new(n);b.head=h;b.tail=t
 if pa:b.parent=arm.edit_bones[pa]
bone('root',(0,0,0),(0,0,.08));bone('pelvis',(0,.02,.19),(0,.02,.29),'root');bone('chest',(0,.02,.29),(0,0,.44),'pelvis');bone('head',(0,0,.44),(0,-.025,.61),'chest')
for sign,side in [(1,'L'),(-1,'R')]:
 bone('ear_'+side,(sign*.105,-.017,.612),(sign*.26,-.017,.76),'head')
 bone('upperarm_'+side,(sign*.14,0,.38),(sign*.18,-.024,.32),'chest');bone('forearm_'+side,(sign*.18,-.024,.32),(sign*.183,-.04,.285),'upperarm_'+side);bone('hand_'+side,(sign*.183,-.04,.285),(sign*.183,-.06,.26),'forearm_'+side)
 bone('thigh_'+side,(sign*.112,.01,.19),(sign*.123,-.024,.113),'pelvis');bone('shin_'+side,(sign*.123,-.024,.113),(sign*.119,-.045,.047),'thigh_'+side);bone('foot_'+side,(sign*.119,-.045,.047),(sign*.119,-.12,.035),'shin_'+side)
for i in range(4):bone('tail_0'+str(i+1),tail[i],tail[i+1],'pelvis'if i==0 else'tail_0'+str(i))
bone('tail_tip',tail[4],tail[5],'tail_04');bpy.ops.object.mode_set(mode='OBJECT');mod=body.modifiers.new('Raichu deform','ARMATURE');mod.object=rig;body.parent=rig
body['quality_status']='Authored candidate; technical and visual review required';body['source']='Authored in Blender by project tool; no external game files or downloads';body['target_height_m']=.8
s.frame_start=1;s.frame_end=61;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(O));body.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(body.data)
audit={'source':str(O.relative_to(R)),'vertices':len(body.data.vertices),'triangles':len(body.data.loop_triangles),'materials':len(body.data.materials),'bones':len(arm.bones),'height_m':max(v.co.z for v in body.data.vertices)-min(v.co.z for v in body.data.vertices),'loose_vertices':sum(not v.link_faces for v in bm.verts),'boundary_edges':sum(e.is_boundary for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'status':'candidate, visual approval outstanding'};bm.free();assert audit['zero_area_faces']==0 and audit['loose_vertices']==0
(A/'ModelAudit.json').write_text(json.dumps(audit,indent=2));print('RAICHU_AUTHORED',audit)
