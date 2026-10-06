"""Reference likeness pass on our 04 checkpoint, before UV and FK preparation.
Broad swept curls replace the regular stacked oval locks. No scene outside our
new character scene is touched; this script is intentionally stage-specific.
"""
import bpy, math, random
from mathutils import Vector
from pathlib import Path
ROOT=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
assert Path(bpy.data.filepath).name=='04_ReferenceRefined.blend'
scene=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=scene
coll=bpy.data.collections['YT_Character'];root=bpy.data.objects['YT_CharacterRoot']
rng=random.Random(904)
for ob in list(coll.objects):
 if ob.get('part')=='Hair':bpy.data.objects.remove(ob,do_unlink=True)
def mesh(name,vs,fs,uv,color='Hair'):
 data=bpy.data.meshes.new('YT_'+name);data.from_pydata(vs,[],fs);data.update()
 ob=bpy.data.objects.new('YT_'+name,data);coll.objects.link(ob);ob.parent=root
 ob['part']='Hair';ob['rig_mode']='head';ob['palette']=color
 ob.data.materials.append(bpy.data.materials['YT_'+color])
 layer=data.uv_layers.new(name='UVMap')
 for p in data.polygons:
  p.use_smooth=True
  for li in p.loop_indices:layer.data[li].uv=uv[data.loops[li].vertex_index]
 return ob
def lock(name,centers,normals,widths,depths,color='Hair',groove=False):
 vs=[];fs=[];uv=[];ns=12
 for i,c in enumerate(centers):
  tangent=(centers[min(i+1,len(centers)-1)]-centers[max(i-1,0)]).normalized()
  normal=normals[i];u=tangent.cross(normal).normalized();v=u.cross(tangent).normalized()
  for j in range(ns):
   a=math.tau*j/ns
   # Two soft longitudinal valleys; silhouette remains one readable hair mass.
   crease=1-.10*max(0,math.cos(3*a))
   vs.append(tuple(c+u*widths[i]*math.cos(a)+v*depths[i]*math.sin(a)*crease));uv.append((j/ns,i/(len(centers)-1)))
 for i in range(len(centers)-1):
  for j in range(ns):fs.append((i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j))
 for idx,rev in [(0,True),(len(centers)-1,False)]:
  k=len(vs);vs.append(tuple(centers[idx]));uv.append((.5,idx/(len(centers)-1)))
  for j in range(ns):
   a=idx*ns+j;b=idx*ns+(j+1)%ns;fs.append((k,b,a) if rev else (k,a,b))
 ob=mesh(name,vs,fs,uv,color)
 if groove:
  d=bpy.data.curves.new('YT_'+name+'_Ridge','CURVE');d.dimensions='3D';d.bevel_depth=.0012;d.bevel_resolution=1;d.use_fill_caps=True
  sp=d.splines.new('POLY');sp.points.add(len(centers)-3)
  for i,p in enumerate(sp.points):
   k=i+1;p.co=(*(centers[k]+normals[k]*(depths[k]*.96)),1)
  ro=bpy.data.objects.new('YT_'+name+'_Ridge',d);coll.objects.link(ro);ro.parent=root;ro['part']='Hair';ro['palette']='HairLight';ro['rig_mode']='head';d.materials.append(bpy.data.materials['YT_HairLight'])
 return ob
# Closed organic scalp envelope, independently editable before the final join.
vs=[];uv=[];fs=[];nr=14;ns=36
for i in range(nr):
 p=.012+(2.03-.012)*i/(nr-1)
 for j in range(ns):
  a=math.tau*j/ns
  # Lower cap only behind/at temples; keep the portrait forehead open.
  theta=min(p,1.25+.79*min(1,abs((a+math.pi)%math.tau-math.pi)/1.1))
  ripple=1+.023*math.sin(a*7+theta*3)+.017*math.cos(a*11-theta*5)
  vs.append((.159*math.sin(theta)*math.sin(a)*ripple,.025-.142*math.sin(theta)*math.cos(a)*ripple,1.238+.145*math.cos(theta)))
  uv.append((j/ns,i/(nr-1)))
for i in range(nr-1):
 for j in range(ns):fs.append((i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j))
for idx,rev in [(0,True),(nr-1,False)]:
 k=len(vs);vs.append((0,.025,1.238+.145*math.cos(.012 if idx==0 else 2.03)));uv.append((.5,idx/(nr-1)))
 for j in range(ns):fs.append((k,idx*ns+(j+1)%ns,idx*ns+j) if rev else (k,idx*ns+j,idx*ns+(j+1)%ns))
mesh('HairEnvelope',vs,fs,uv)
def surface(theta,a):
 p=Vector((.168*math.sin(theta)*math.sin(a),.022-.151*math.sin(theta)*math.cos(a),1.239+.143*math.cos(theta)))
 n=Vector((p.x/.168**2,(p.y-.022)/.151**2,(p.z-1.239)/.143**2)).normalized()
 return p,n
# Offset golden-angle distribution avoids visible horizontal rows.
for i in range(40):
 a=i*2.399963229728653+rng.uniform(-.18,.18)
 theta=math.acos(1-(i+.7)/41*1.31)
 aa=abs((a+math.pi)%math.tau-math.pi)
 if theta>1.13 and aa<1.05:continue
 centers=[];normals=[];widths=[];depths=[]
 slope=rng.uniform(.22,.44);curl=rng.uniform(.3,.72)*(-1 if i%3==0 else 1);width=rng.uniform(.024,.038);depth=rng.uniform(.012,.020)
 for k in range(18):
  t=k/17;th=theta+slope*t-.10*math.sin(t*math.tau);az=a+curl*math.sin(t*math.pi*1.25)
  p,n=surface(th,az);p+=n*(.002+.008*math.sin(t*math.pi))
  shape=max(.025,math.sin(math.pi*(.11+.885*t))**.75)
  centers.append(p);normals.append(n);widths.append(width*shape);depths.append(depth*shape)
 lock('SweptCurl_%02d'%i,centers,normals,widths,depths,'HairLight' if i%9==0 else 'Hair',i%3==0)
# Varied framing locks flow across the forehead rather than parallel hooks.
for i,(x,endx,endz) in enumerate([(-.133,-.143,1.238),(-.096,-.111,1.242),(-.052,-.080,1.251),(-.007,-.025,1.253),(.039,.007,1.260),(.088,.066,1.266),(.129,.133,1.248)]):
 centers=[];normals=[];widths=[];depths=[]
 for k in range(20):
  t=k/19;px=x+(endx-x)*t+.014*math.sin(t*math.pi*1.3)
  z=1.342+(endz-1.342)*t+.012*math.sin(t*math.pi)
  y=-.113-.036*math.sin(t*math.pi*.65)
  centers.append(Vector((px,y,z)));normals.append(Vector((0,-1,.2)).normalized())
  widths.append(.025*(1-t)**.6+.0018);depths.append(.0105*(1-t)**.65+.0014)
 lock('FramingCurl_%02d'%i,centers,normals,widths,depths,'HairLight' if i==2 else 'Hair',i in [1,4])
# Broad nape locks cover the rear cranium without hiding the neck scarf.
for i,a in enumerate([1.65,2.27,2.92,3.56,4.20,4.80]):
 centers=[];normals=[];widths=[];depths=[]
 for k in range(18):
  t=k/17;p,n=surface(1.68+.68*t,a+.18*math.sin(t*math.pi*1.5))
  shape=max(.035,math.sin(math.pi*(.08+.916*t))**.62)
  centers.append(p+n*.006);normals.append(n);widths.append(.040*shape);depths.append(.021*shape)
 lock('NapeLock_%02d'%i,centers,normals,widths,depths,'Hair',i in [1,4])
for ob in coll.objects:
 if ob.get('part')!='Hair':continue
 if ob.type=='MESH':
  for v in ob.data.vertices:v.co.x*=1.07;v.co.y=.025+(v.co.y-.025)*1.08
 elif ob.type=='CURVE':
  for sp in ob.data.splines:
   for p in sp.points:p.co.x*=1.07;p.co.y=.025+(p.co.y-.025)*1.08
# Warm large irises with restrained highlights; smaller, less angular nose.
head=bpy.data.objects['YT_Head'];bpy.context.view_layer.objects.active=head
bpy.ops.object.select_all(action='DESELECT');head.select_set(True)
sub=head.modifiers.new('Soft portrait quad loops','SUBSURF');sub.levels=1;sub.render_levels=1
bpy.ops.object.modifier_apply(modifier=sub.name);head.select_set(False)
for v in head.data.vertices:
 if v.co.y<-.025:
  r=min(((v.co.x-side*.064)/.052)**2+((v.co.z-1.211)/.033)**2 for side in [-1,1])
  v.co.y+=.017*math.exp(-r*1.5)
for side in [-1,1]:
 s='L' if side==1 else 'R';x=side*.064
 # Use angular latitude spacing for true oval silhouettes, not pointed lofts.
 for n,cz,rz,seg,nr in [('Iris',1.211,.025,24,10),('Pupil',1.212,.0165,20,8),('EyeCatch',1.224,.006,12,6),('EyeCatchSmall',1.202,.0025,10,4)]:
  ob=bpy.data.objects['YT_'+n+'_'+s]
  for v in ob.data.vertices:
   if v.index<(nr+1)*seg:v.co.z=cz-rz*math.cos(math.pi*(v.index//seg)/nr)
 white=bpy.data.objects['YT_EyeWhite_'+s]
 for v in white.data.vertices:v.co.y=-.143 if v.index==0 else (-.136 if v.index==33 else -.139)
 for n,factor in [('Iris',1.27),('Pupil',1.28)]:
  ob=bpy.data.objects['YT_'+n+'_'+s]
  for v in ob.data.vertices:v.co.x=x+(v.co.x-x)*factor;v.co.y-=.010
 for n in ['EyeCatch','EyeCatchSmall']:
  for v in bpy.data.objects['YT_'+n+'_'+s].data.vertices:v.co.y-=.010
 for name,cy in [('UpperLid',-.141),('LowerLid',-.141)]:
  ob=bpy.data.objects['YT_'+name+'_'+s]
  for sp in ob.data.splines:
   for p in sp.points:p.co.y=cy-(.004*max(0,(p.co.z-1.211)/.029) if name=='UpperLid' else 0)
 nose=bpy.data.objects['YT_Nose']
for v in nose.data.vertices:
 v.co.x*=.82;v.co.y=-.132+(v.co.y+.132)*.7;v.co.z=1.18+(v.co.z-1.18)*.7
for n,delta in [('Smile',.025),('LowerLip',.025)]:
 ob=bpy.data.objects['YT_'+n]
 for sp in ob.data.splines:
  for p in sp.points:p.co.z+=delta;p.co.y-=.012
# Footwear seams stay low contrast; add no further microgeometry.
scene['likeness_pass']='Irregular swept hair locks, enlarged warm irises, shorter nose and raised smile.'
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/Stages/05_LikenessPolish.blend'),check_existing=False)
print('LIKELINESS_POLISH_SAVED',len([o for o in coll.objects if o.type in ['MESH','CURVE']]))
