"""V4 reference correction on a new version, preserving source meshes and rig.
No new weights, animation, final UVs/textures or runtime export.
"""
import bpy,bmesh,math,json,random
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
s=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=s
assert 'YT4_Player' not in bpy.data.collections
assert Path(bpy.data.filepath).name in ['YoungTrainer_BarefootReference_V4.blend','08_BeforeBarefootReferenceRework_20261007.blend']
C=bpy.data.collections.new('YT4_Player');s.collection.children.link(C)
root=bpy.data.objects.new('YT4_PlayerRoot',None);C.objects.link(root);root['height_m']=1.4
M={}
for name,color in {'Skin':(.72,.43,.26,1),'Hair':(.050,.021,.011,1),'HairWarm':(.060,.026,.014,1),'HairDeep':(.038,.014,.008,1),'Scarf':(.33,.048,.030,1),'ScarfLight':(.39,.062,.037,1),'ScarfDeep':(.24,.030,.019,1),'Cream':(.80,.70,.50,1),'Leather':(.16,.071,.028,1)}.items():
 m=bpy.data.materials.new('YT4_Preview_'+name);m.use_nodes=True;m.diffuse_color=color
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.72;M[name]=m

def mesh(name,vs,fs,mat,smooth=True):
 d=bpy.data.meshes.new('YT4_'+name);d.from_pydata(vs,[],fs);d.update()
 bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
 o=bpy.data.objects.new('YT4_'+name,d);C.objects.link(o);o.parent=root
 if mat:d.materials.append(M[mat])
 for p in d.polygons:p.use_smooth=smooth
 o['stage']='V4 barefoot-reference static modelling; no skinning'
 return o

def clamp(x):return max(0,min(1,x))
def lerp(x,rows):
 if x<=rows[0][0]:return rows[0][1]+x-rows[0][0]
 if x>=rows[-1][0]:return rows[-1][1]+x-rows[-1][0]
 for (a,b),(c,d) in zip(rows,rows[1:]):
  if a<=x<=c:return b+(d-b)*(x-a)/(c-a)

def mixed(o):
 if not o.data.shape_keys:return [v.co.copy() for v in o.data.vertices]
 ks=o.data.shape_keys.key_blocks;out=[v.co.copy() for v in ks[0].data]
 for k in list(ks)[1:]:
  if k.value:
   for i,p in enumerate(k.data):out[i]+=(p.co-k.relative_key.data[i].co)*k.value
 return out

def duplicate(o,points,mapper=None):
 new=o.copy();new.data=o.data.copy();new.name='YT4_'+o.name.removeprefix('YT_').removeprefix('YT3_');C.objects.link(new)
 new.parent=root;new.matrix_parent_inverse.identity();new.matrix_basis.identity()
 if new.data.shape_keys:new.shape_key_clear()
 for mod in list(new.modifiers):
  if mod.type=='ARMATURE':new.modifiers.remove(mod)
 new.animation_data_clear();new.data.animation_data_clear()
 for v,p in zip(new.data.vertices,points):v.co=mapper(p.copy(),v.index) if mapper else p
 for poly in new.data.polygons:poly.use_smooth=True
 new['stage']='V4 static copy; source mesh and rig preserved in hidden source collection'
 return new
oldarm=[Vector((.130,0,1.020)),Vector((.227,0,.803)),Vector((.290,0,.650))]
newarm=[Vector((.127,0,.971)),Vector((.182,0,.715)),Vector((.223,-.012,.590))]
def arm(p):
 side=1 if p.x>=0 else -1;q=Vector((abs(p.x),p.y,p.z));choices=[]
 for i in range(2):
  v=oldarm[i+1]-oldarm[i];t=clamp((q-oldarm[i]).dot(v)/v.length_squared);choices.append(((q-oldarm[i]-v*t).length_squared,i,t))
 _,i,t=min(choices);v=oldarm[i+1]-oldarm[i];w=newarm[i+1]-newarm[i]
 offset=v.rotation_difference(w)@(q-oldarm[i]-v*t)
 offset*=Vector((.94,1.07,1.00));result=newarm[i]+w*t+offset;result.x*=side;return result

def torso(p,part):
 x,y,z=p;f=lerp(z,[(.55,.96),(.72,.93),(.95,.90),(1.06,.91)])
 zz=lerp(z,[(.555,.476),(.602,.510),(.728,.694),(.82,.784),(.918,.877),(1.035,.980),(1.065,1.024)])
 yy=y*(1+.04*math.sin((z-.65)*7));xx=x*f
 if part=='Vest':
  flare=1+.52*(1-clamp((z-.555)/.20))
  xx*=flare
  yy-=.070*(1-clamp((z-.60)/.13))*clamp(-y/.065)
  yy-=.012*max(0,-y/.10)*math.sin(math.pi*clamp((z-.55)/.5));zz+=.017*math.sin(x*15)*(1-clamp((z-.55)/.20))
  zz+=.018*(1-clamp((z-.555)/.10))*max(0,1-abs(x)/.09)
  zz-=.040*(1-clamp((z-.60)/.12))
 return Vector((xx,yy,zz))
def headmap(p):
 x,y,z=p;face=y<-.035
 if face:
  # Soften lower jaw without inflating the full head into a sphere.
  f=.935-.045*math.exp(-((z-1.095)/.042)**2);x*=f
  y+=.009*math.exp(-(p.x/.015)**2-((z-1.146)/.015)**2)
 else:x*=.95
 zz=lerp(z,[(1.064,1.029),(1.187,1.153),(1.332,1.307)])
 return Vector((x,.010+(y-.010)*.96,zz))
# Preserve the original component layout and textures; change static geometry only.
for o in list(bpy.data.collections['YT_Character'].objects):
 if o.type!='MESH' or o.name in ['YT_Boots','YT_Socks','YT_Scarf','YT_Hands']:continue
 ps=mixed(o);part=o.get('part');centers={}
 if part in ['Shirt','Body']:
  bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();seen=set()
  for v in bm.verts:
   if v.index in seen:continue
   stack=[v];ids=[];seen.add(v.index)
   while stack:
    cur=stack.pop();ids.append(cur.index)
    for edge in cur.link_edges:
     n=edge.other_vert(cur)
     if n.index not in seen:seen.add(n.index);stack.append(n)
   center=sum((ps[k] for k in ids),Vector())/len(ids)
   for k in ids:centers[k]=center
  bm.free()
 def mapping(p,i,part=part,o=o):
  x,y,z=p;side=1 if x>=0 else -1
  if part=='Hands':return Vector((side*.242,-.016,.540))+(p-Vector((side*.312,-.004,.609)))*Vector((.95,1.10,1.03))
  if part=='Wristbands':return arm(p)
  if part=='Body':
   groups={o.vertex_groups[g.group].name for g in o.data.vertices[i].groups if g.weight>.95}
   if 'head' in groups:
    # Cup the preserved broad ear volume without adding fine cartilage details.
    radial=((abs(x)-.153)/.033)**2+((z-1.165)/.044)**2
    if y<.007:p.y+=.014*math.exp(-radial*2)
    return headmap(p)
   if abs(centers[i].x)>.15:return arm(p)
   return Vector((x*.92,y*.98,lerp(z,[(1.037,.979),(1.062,1.023),(1.088,1.048)])))
  if part=='Shirt':
   if abs(centers[i].x)>.15:
    q=arm(p);t=clamp((.98-q.z)/.28)
    axis=newarm[0].lerp(newarm[1],t);dx=abs(q.x)-axis.x
    q.x=side*(axis.x+dx*(1+.12*math.sin(t*math.pi)))
    q.x+=side*.012*math.sin(t*math.pi*2.1);q.y+=.010*math.sin(t*math.pi*2.8)
    q.y+=.007*math.cos(math.atan2(dx,q.y)*3+t*8)*math.sin(t*math.pi)
    q.y*=1+.18*math.sin(t*math.pi);return q
   q=torso(p,part)
   if z<.65 and y<-.045:q.z+=.045*(1-clamp((z-.555)/.09))*max(0,1-abs(x)/.038)
   return q
  if part=='Vest':return torso(p,part)
  if part=='Pants':
   zz=lerp(z,[(.274,.188),(.32,.235),(.412,.352),(.466,.409),(.535,.487),(.61,.590),(.733,.702)])
   center=side*lerp(z,[(.274,.123),(.41,.119),(.54,.104),(.733,.078)])
   f=lerp(z,[(.274,.91),(.35,.96),(.412,1.02),(.54,.99),(.733,.95)])
   x=center+(x-center)*f;y*=1.05
   a=math.atan2((x-center)/.10,-y/.10);g=math.exp(-((zz-.34)/.08)**2)
   radial=1+(.13 if side<0 else .10)*math.sin(3*a+zz*10+side*.7)*g
   radial+=.08*math.exp(-((zz-.25)/.045)**2)*math.sin(2*a+side)
   x=center+(x-center)*radial
   y*=radial
   y-=.018*math.exp(-((zz-.31)/.06)**2)
   x+=side*.010*math.exp(-((zz-.32)/.09)**2)
   y+=.006*math.sin(z*38+side*1.3)*clamp((z-.3)/.12)*clamp((.63-z)/.1)
   zz+=.007*math.sin((x-center)*30+side)*clamp((.70-z)/.2)
   return Vector((x,y,zz))
  if part=='Belt':return Vector((x*.96,y*.99,z-.055))
  if part=='Pouches':
   size=.90 if side<0 else 1.04
   return Vector((side*.175+(x-side*.188)*size,y-.030+(-.012 if side<0 else .003),.682+(z-.738)*(1.0 if side<0 else 1.12)+(-.018 if side<0 else .006)))
  if part=='Harness':return torso(p,'Shirt')
  if part=='Pendant':return Vector((x*.78,y*1.02,lerp(z,[(.830,.784),(.865,.815),(1.051,1.004)])))
  if part=='Backpack':
   xx=x*.94;zz=.536+(z-.601)*1.01
   yy=.084+(y-.082)*1.43+.024*math.sin(math.pi*clamp((zz-.536)/.442))*max(0,1-(x/.22)**2)
   xx*=1+.04*math.sin(math.pi*clamp((zz-.536)/.442))
   yy+=.006*math.sin(x*20+zz*9)*clamp((y-.18)/.08)
   zz-=.007*math.exp(-(x/.11)**2)*clamp((zz-.96)/.04)
   return Vector((xx,yy,zz))
  if part=='Bedroll':
   dz=.010*max(0,1-(x/.22)**2)
   return Vector((x*1.01,.21+(y-.143)*.98,.887+(z-.950)*1.13-dz))
  if part=='Equipment':
   if i>=28:return Vector((.230,.195,.615))+(p-Vector((.225,.040,.635)))*1.25
   return Vector((x*.94,.284+(y-.216),z+.005))
  return p
 new=duplicate(o,ps,mapping)
 if part=='Vest':
  # Decorative edge strips are archived with the source; they are not silhouette geometry.
  bm=bmesh.new();bm.from_mesh(new.data);bm.verts.ensure_lookup_table()
  bmesh.ops.delete(bm,geom=[v for v in bm.verts if 432<=v.index<654 or 1176<=v.index<1398],context='VERTS');bm.to_mesh(new.data);bm.free()
 if part=='Backpack':
  for i in list(range(284,380))+list(range(452,548)):new.data.vertices[i].co.y-=.030
 if part=='Belt':
  # Keep the existing buckle on the new sloping belt; archive the old belt untouched.
  points=[new.data.vertices[i].co.copy() for i in range(66,90)];center=sum(points,Vector())/len(points)
  for i in range(66,90):
   q=new.data.vertices[i].co-center;a=math.radians(-14)
   new.data.vertices[i].co=(q.x*math.cos(a)-q.z*math.sin(a),-.134+q.y,.701+q.x*math.sin(a)+q.z*math.cos(a))
  bm=bmesh.new();bm.from_mesh(new.data);bm.verts.ensure_lookup_table()
  bmesh.ops.delete(bm,geom=[v for v in bm.verts if not 66<=v.index<90],context='VERTS');bm.to_mesh(new.data);bm.free()
 if part=='Pants':
  bm=bmesh.new();bm.from_mesh(new.data);bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=2,use_grid_fill=True)
  for v in bm.verts:
   x,y,z=v.co;side=1 if x>=0 else -1;center=side*.123
   if .215<z<.48:
    a=math.atan2((x-center)/.10,-y/.12);amplitude=0.0
    for height,width,depth,shift in [(.25,.013,.013,.024),(.32,.017,.011,-.027),(.405,.018,.008,.025)]:
     bend=height+shift*math.sin(a+side*.8)
     amplitude-=depth*math.exp(-((z-bend)/width)**2)*(.55+.45*math.sin(a*1.5+side)**2)
    r=math.hypot(x-center,y)
    if r>.035:v.co.x+=(x-center)/r*amplitude;v.co.y+=y/r*amplitude
  bm.to_mesh(new.data);bm.free();new.data.update()
 if part in ['Body','Hands']:
  new.data.materials.clear();new.data.materials.append(M['Skin'])
  for poly in new.data.polygons:poly.material_index=0
 if part in ['Body','Hands','Shirt','Pants','Vest']:
  mod=new.modifiers.new('Soft form preview','SUBSURF');mod.levels=1;mod.render_levels=1
 if part=='Backpack':
  bm=bmesh.new();bm.from_mesh(new.data)
  bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=3,use_grid_fill=True)
  for v in bm.verts:
   x,y,z=v.co
   f=math.sin(math.pi*clamp((z-.55)/.40))*max(0,1-(x/.215)**2)
   v.co.y+=.025*f*clamp((y-.13)/.10)
   v.co.z-=.012*max(0,1-(x/.14)**2)*clamp((y-.24)/.05)*clamp((z-.85)/.08)
  bm.to_mesh(new.data);bm.free();new.data.update()
 if part in ['Pouches','Backpack']:
  mod=new.modifiers.new('Soft leather corner preview','BEVEL');mod.width=.011 if part=='Backpack' else .009;mod.segments=4
  if part=='Backpack':
   mod=new.modifiers.new('Supple pack form preview','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=1;mod.render_levels=1
   mod=new.modifiers.new('Leather volume smoothing','SMOOTH');mod.factor=.55;mod.iterations=8
 if part=='Hands':
  bpy.ops.object.select_all(action='DESELECT');new.select_set(True);bpy.context.view_layer.objects.active=new
  new.modifiers.clear();mod=new.modifiers.new('Unified soft hand form','REMESH');mod.mode='VOXEL';mod.voxel_size=.0017;mod.use_smooth_shade=True
  bpy.ops.object.modifier_apply(modifier=mod.name)
  mod=new.modifiers.new('Hand smoothing','SMOOTH');mod.factor=.3;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
# Head retains its facial loops; reshape eyes and orbital loops consistently.
for o in list(bpy.data.collections['YT_HeadHair_V3'].objects):
 if 'Hair' in o.name or 'Curl' in o.name or 'Sweep' in o.name:continue
 ps=mixed(o);eye='Eye' in o.name or 'Iris' in o.name or 'Pupil' in o.name or 'Glint' in o.name or 'Lid' in o.name
 eye_ids=set();mouth_ids=set()
 if o.name=='YT3_Head':
  for v in o.data.vertices:
   if any(o.vertex_groups[g.group].name in ['Topology_EyeL','Topology_EyeR'] for g in v.groups):eye_ids.add(v.index)
   if any(o.vertex_groups[g.group].name=='Topology_Mouth' for g in v.groups):mouth_ids.add(v.index)
 def mapping(p,i,o=o,eye=eye,eye_ids=eye_ids,mouth_ids=mouth_ids):
  if eye or i in eye_ids:
   cx=.056 if p.x>0 else -.056
   iris='Iris' in o.name or 'Pupil' in o.name or 'Glint' in o.name
   p.x=cx+(p.x-cx)*(1.28 if iris else 1.08)
   p.z=1.187+(p.z-1.187)*(1.20 if iris else 1.16)
  if 'Mouth' in o.name or i in mouth_ids:
   p.z+=.0035*(abs(p.x)/.026)**1.5
  return headmap(p)
 new=duplicate(o,ps,mapping)
 if o.name=='YT3_Head':new.data.materials.clear();new.data.materials.append(M['Skin'])
# One connected sculpted hair envelope: lobes and flowing ridges share topology.
rng=random.Random(1793);lobes=[]
for j,(phi,n) in enumerate([(.48,7),(.95,11),(1.45,13),(1.95,13),(2.25,9)]):
 for k in range(n):
  a=math.tau*(k+.27*j)/n+rng.uniform(-.13,.13)
  if phi>1.70 and math.cos(a)>.40:continue
  lobes.append((a,phi+rng.uniform(-.12,.12),rng.uniform(.009,.014),rng.uniform(.24,.34),rng.uniform(.22,.32),rng.uniform(-1,1)))
N=144;K=64;vs=[(0,.021,1.40)];fs=[]
for j in range(1,K+1):
 t=j/K
 for k in range(N):
  a=math.tau*k/N;front=max(0,math.cos(a));back=max(0,-math.cos(a))
  end=2.30-.44*front+.15*back+.12*math.sin(3*a+.65)*front+.055*math.cos(5*a)*front
  phi=end*t;push=0
  for aa,pp,amp,sa,sp,sw in lobes:
   da=(a-aa+math.pi)%math.tau-math.pi;dp=phi-pp;u=da/sa;v=dp/sp;dist=u*u+v*v
   if dist<9:
    flow=v+.45*math.sin(u*1.7+sw);ridge=.62+.38*math.cos(flow*2.5)
    push+=amp*math.exp(-dist*1.3)*ridge
  rx=.161+push;ry=.143+push*.95;rz=.142+push*.45
  x=rx*math.sin(a)*math.sin(phi);y=.021-ry*math.cos(a)*math.sin(phi);z=1.245+rz*math.cos(phi)
  if back and z<1.21:y+=.027*back*clamp((1.21-z)/.08)
  if front and abs(x)<.14 and z<1.235:y+=.030*front*clamp((1.235-z)/.06)
  # Broad asymmetric curl tips through envelope, no tubular ornament pieces.
  wave=.005*math.sin(a*7+phi*3.5)*math.sin(phi)
  x+=wave*math.sin(a);y-=wave*math.cos(a)
  vs.append((x,y,z))
for k in range(N):fs.append((0,1+k,1+(k+1)%N))
for j in range(K-1):
 for k in range(N):fs.append((1+j*N+k,1+j*N+(k+1)%N,1+(j+1)*N+(k+1)%N,1+(j+1)*N+k))
pole=len(vs);vs.append((0,.02,1.15))
for k in range(N):fs.append((pole,1+(K-1)*N+(k+1)%N,1+(K-1)*N+k))
hair=mesh('HairContinuousVolume',vs,fs,'Hair');hair.data.materials.append(M['HairWarm']);hair.data.materials.append(M['HairDeep'])
hair['connected_lobe_fields']=len(lobes);hair['no_separate_tubular_locks']=True
mod=hair.modifiers.new('Hair volume smoothing','SUBSURF');mod.levels=1;mod.render_levels=1
# Broad closed leaf-like curl pads, not round tubes. Roots intersect the shared mass.
def catmull(points,sub=6):
 ps=[Vector(p) for p in points];out=[]
 for i in range(len(ps)-1):
  a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)]
  for j in range(sub):
   t=j/sub;out.append((b*2+(-a+c)*t+(a*2-b*5+c*4-d)*t*t+(-a+b*3-c*3+d)*t*t*t)*.5)
 out.append(ps[-1]);return out
def curlpad(name,controls,width=.04,mat='Hair'):
 ps=catmull(controls);vs=[];fs=[];B=10;oldnormal=None
 for i,p in enumerate(ps):
  t=i/(len(ps)-1);tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized();normal=(p-Vector((0,.020,1.24))).normalized()
  normal=(normal-tangent*normal.dot(tangent)).normalized();lateral=tangent.cross(normal).normalized()
  w=width*(.20+.85*math.sin(math.pi*t))*(1-.85*t*t)
  for surface in [0,1]:
   for j in range(B+1):
    u=-1+2*j/B;h=(.0075*(1-u*u)*math.sin(math.pi*t) if surface==0 else -.007)
    # A broad folded crest gives each curl readable direction.
    h+=.003*math.cos((u+.30)*math.pi)*math.sin(math.pi*t)
    vs.append(tuple(p+lateral*w*u+normal*h))
 stride=2*(B+1)
 for i in range(len(ps)-1):
  for q in [0,1]:
   for j in range(B):a=i*stride+q*(B+1)+j;fs.append((a,a+1,a+stride+1,a+stride))
  for j in [0,B]:a=i*stride+j;fs.append((a,a+B+1,a+stride+B+1,a+stride))
 for i in [0,len(ps)-1]:
  for j in range(B):a=i*stride+j;fs.append((a,a+1,a+B+2,a+B+1))
 return mesh(name,vs,fs,mat)
hairpads=[]
for band,(phi,n) in enumerate([(.40,8),(.85,11),(1.30,13),(1.75,14),(2.15,10)]):
 for k in range(n):
  a=math.tau*(k+.25*band)/n+rng.uniform(-.16,.16)
  twist=rng.uniform(.35,.80);length=rng.uniform(.30,.53);width=rng.uniform(.022,.034)
  if phi>1.7 and math.cos(a)>.38:continue
  controls=[]
  for j in range(5):
   t=j/4;aa=a+twist*math.sin(math.pi*t)+.20*t;pp=phi-length*.50+length*t-.12*math.sin(t*math.tau)
   rr=.004 if j==0 else (.012 if j==4 else .016)
   p=Vector(((.162+rr)*math.sin(aa)*math.sin(pp),.021-(.145+rr)*math.cos(aa)*math.sin(pp),1.245+(.149+rr*.5)*math.cos(pp)))
   if math.cos(aa)<0 and p.z<1.21:p.y+=.022*clamp((1.21-p.z)/.08)
   controls.append(tuple(p))
  hairpads.append(curlpad('HairGroup_%02d'%len(hairpads),controls,width,'HairWarm' if len(hairpads)%4==0 else 'Hair'))
frontpaths=[[(.092,-.019,1.369),(.062,-.106,1.339),(.035,-.157,1.273),(.023,-.129,1.203),(.009,-.108,1.171)],
 [(-.055,-.044,1.369),(-.094,-.132,1.332),(-.081,-.167,1.281),(-.030,-.147,1.244),(-.006,-.133,1.262)],
 [(.129,-.035,1.329),(.155,-.112,1.295),(.157,-.128,1.250),(.123,-.108,1.228),(.112,-.088,1.246)]]
for i,p in enumerate(frontpaths):hairpads.append(curlpad('ForeheadGroup_'+str(i),p,.044,'HairWarm' if i==0 else 'Hair'))
# Uneven side curls stay close to the shared volume; no four repeated horn tips.
for side in [-1,1]:
 for j,(z,y) in enumerate([(1.35,-.018),(1.28,-.085),(1.23,-.003),(1.205,.071),(1.31,.117)]):
  dz=.010*(1 if j%2 else -1);xx=.145 if j<2 else .155
  p=[(side*(xx-.018),y,z+.011),(side*(xx+.018),y-.014,z-.016),
     (side*(xx+.030),y-.009,z-.020+dz),(side*(xx+.030),y+.006,z-.002+dz),
     (side*(xx+.013),y+.009,z+.008+dz)]
  hairpads.append(curlpad('OutlineCurl_'+str(side)+'_'+str(j),p,.018 if j%2 else .021))
# Three broad top sweeps establish the asymmetrical crown, not uniformly spiked tips.
for j,p in enumerate([
 [(-.083,.01,1.33),(-.071,-.005,1.373),(-.015,-.015,1.414),(.041,-.007,1.423),(.066,.012,1.396)],
 [(.055,.066,1.333),(.105,.034,1.371),(.127,.012,1.398),(.109,-.015,1.410),(.081,-.022,1.396)],
 [(-.113,.083,1.313),(-.147,.055,1.346),(-.153,.026,1.375),(-.135,.010,1.389),(-.113,.025,1.372)]]):
 hairpads.append(curlpad('CrownSweep_'+str(j),p,.030 if j==0 else .022))
allhair=[hair]+hairpads;high=max(v.co.z for o in allhair for v in o.data.vertices)
for o in allhair:
 for v in o.data.vertices:
  if o.name.startswith(('YT4_HairGroup','YT4_OutlineCurl')) and v.co.y<-.055 and .027<abs(v.co.x)<.117 and v.co.z<1.225:
   v.co.z=1.225+(v.co.z-1.225)*.12
  if v.co.z>1.28:v.co.z=1.28+(v.co.z-1.28)*(.12/(high-1.28))
  if v.co.y>.02 and v.co.z<1.21:
   v.co.z-=.064*clamp((1.21-v.co.z)/.088)*clamp((v.co.y-.02)/.050)
hair['broad_curl_groups']=len(hairpads)
# Cloth bands: closed folded ribbons, deliberately broad and flattened.
def cloth(name,centers,widths,thickness,mat):
 vs=[];fs=[];m=8
 for i,(cx,cy,cz) in enumerate(centers):
  width=widths[i] if isinstance(widths,list) else widths
  for front in [0,1]:
   for j in range(m+1):
    u=-1+2*j/m;vs.append((cx+u*width,cy+(front-.5)*thickness+.007*math.sin(math.pi*u),cz-.012*u*u+.004*math.cos(u*math.tau)))
 stride=2*(m+1)
 for i in range(len(centers)-1):
  for q in [0,1]:
   for j in range(m):a=i*stride+q*(m+1)+j;fs.append((a,a+1,a+stride+1,a+stride))
  for j in [0,m]:
   a=i*stride+j;fs.append((a,a+m+1,a+stride+m+1,a+stride))
 for i in [0,len(centers)-1]:
  for j in range(m):a=i*stride+j;fs.append((a,a+1,a+m+2,a+m+1))
 return mesh(name,vs,fs,mat)
for layer in range(3):
 vs=[];fs=[];A=80;B=6
 for backface in [0,1]:
  for i in range(A):
   a=math.tau*i/A;front=max(0,math.cos(a));height=.052+.012*front
   for j in range(B+1):
    v=j/B;z=1.047-layer*.024+(v-.5)*height-(.030+layer*.022)*front+.014*math.sin(a+layer*.95)
    z+=.012*math.sin(a*2+layer*.7)*math.sin(math.pi*v)
    r=.011*math.sin(v*math.pi)+.003*math.sin(v*math.pi*2)+.005*math.sin(a*3+layer)+.005*math.cos(a-layer*.7)*math.sin(math.pi*v)
    x=(.073+layer*.015+r+(backface-.5)*.012)*math.sin(a);y=.005-(.066+layer*.024+r+(backface-.5)*.012)*math.cos(a)
    vs.append((x,y,z))
 stride=A*(B+1)
 for q in [0,1]:
  for i in range(A):
   for j in range(B):a=q*stride+i*(B+1)+j;b=q*stride+((i+1)%A)*(B+1)+j;fs.append((a,b,b+1,a+1))
 for i in range(A):
  for j in [0,B]:a=i*(B+1)+j;b=((i+1)%A)*(B+1)+j;fs.append((a,b,b+stride,a+stride))
 scarf_layer=mesh('ScarfLayer'+str(layer),vs,fs,['ScarfLight','Scarf','ScarfDeep'][layer])
cloth('ScarfFrontFold',[(-.022,-.130,.989),(-.010,-.142,.956),(.008,-.145,.927),(.030,-.137,.905),(.040,-.126,.891)],[.087,.087,.062,.034,.008],.012,'Scarf')
cloth('ScarfSideTail',[(.073,-.040,1.037),(.114,-.053,1.014),(.157,-.052,.986),(.180,-.041,.956),(.195,-.019,.941)],[.037,.035,.034,.027,.008],.010,'ScarfLight')
for ob in C.objects:
 if ob.name.startswith('YT4_Scarf'):
  mod=ob.modifiers.new('Soft cloth edge preview','SUBSURF');mod.levels=1;mod.render_levels=1
# Merge only the new scarf folds into one soft cloth volume; preserve the source scarf.
scarf_parts=[o for o in C.objects if o.name.startswith('YT4_Scarf')]
bpy.ops.object.select_all(action='DESELECT')
for o in scarf_parts:o.select_set(True);o.modifiers.clear()
bpy.context.view_layer.objects.active=scarf_parts[0];bpy.ops.object.join();scarf=scarf_parts[0];scarf.name='YT4_ScarfWrappedVolume'
mod=scarf.modifiers.new('Unified overlapping scarf folds','REMESH');mod.mode='VOXEL';mod.voxel_size=.002;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=scarf.modifiers.new('Soft fold smoothing','SMOOTH');mod.factor=.30;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
bm=bmesh.new();bm.from_mesh(scarf.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(scarf.data);bm.free()
# One simple preview color keeps polygon-based material transfers from imitating faceting.
scarf.data.materials.clear();scarf.data.materials.append(M['Scarf'])
for p in scarf.data.polygons:p.use_smooth=True;p.material_index=0
mod=scarf.modifiers.new('Cloth surface smoothing preview','SUBSURF');mod.levels=1;mod.render_levels=1
scarf['source_preserved']=True;scarf['broad_fold_pass']=True
# Readable sloping waist belt, following the torso rather than a thin straight line.
vs=[];fs=[];A=80
for row in range(4):
 for i in range(A):
  a=math.tau*i/A;x=(.163+(.006 if row>=2 else 0))*math.sin(a);y=-(.115+(.006 if row>=2 else 0))*math.cos(a)
  z=.701-.041*math.sin(a)+(-.023 if row%2==0 else .023);vs.append((x,y,z))
for i in range(A):
 n=(i+1)%A
 for row,nextrow in [(0,1),(1,3),(3,2),(2,0)]:fs.append((row*A+i,row*A+n,nextrow*A+n,nextrow*A+i))
mesh('DiagonalWaistBelt',vs,fs,'Leather')
# Bare foot volume, instep/arch, heel and five independently identifiable toe lobes.
def ellipsoid(name,c,scale,mat='Skin',segments=28,rings=16):
 vs=[(c[0],c[1],c[2]+scale[2])];fs=[]
 for j in range(1,rings):
  p=math.pi*j/rings
  for k in range(segments):
   a=math.tau*k/segments;vs.append((c[0]+scale[0]*math.sin(p)*math.cos(a),c[1]+scale[1]*math.sin(p)*math.sin(a),c[2]+scale[2]*math.cos(p)))
 bottom=len(vs);vs.append((c[0],c[1],c[2]-scale[2]))
 for k in range(segments):fs.append((0,1+k,1+(k+1)%segments))
 for j in range(rings-2):
  for k in range(segments):a=1+j*segments+k;b=1+j*segments+(k+1)%segments;fs.append((a,b,b+segments,a+segments))
 for k in range(segments):fs.append((bottom,1+(rings-2)*segments+(k+1)%segments,1+(rings-2)*segments+k))
 return mesh(name,vs,fs,mat)
# Human hand layout: four fingers across the palm and a separate angled thumb.
for side,label in [(1,'R'),(-1,'L')]:
 parts=[ellipsoid('Palm_'+label,(side*.248,-.016,.551),(.030,.016,.041))]
 for i,(dx,length,radius) in enumerate([(-.021,.051,.0095),(-.006,.060,.010),(.010,.057,.0095),(.024,.045,.0085)]):
  x=side*(.248+dx);rootz=.526
  parts.append(ellipsoid('Finger'+str(i+1)+'_'+label,(x,-.020,rootz-length*.5),(radius,.011,length*.5+.009),segments=20,rings=14))
 parts.append(ellipsoid('Thumb_'+label,(side*.214,-.026,.544),(.014,.012,.030),segments=20,rings=14))
 bpy.ops.object.select_all(action='DESELECT')
 for ob in parts:ob.select_set(True)
 ob=parts[0];bpy.context.view_layer.objects.active=ob;bpy.ops.object.join();ob.name='YT4_Hand_'+label
 mod=ob.modifiers.new('Unified human hand','REMESH');mod.mode='VOXEL';mod.voxel_size=.0013;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=ob.modifiers.new('Gentle hand smoothing','SMOOTH');mod.factor=.3;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 ob['finger_count']=5;ob['finger_layout']='four distal fingers and medial thumb; no rig or weights'
# Soft irregular rolled cuffs around each forearm; no fine seams.
for side,label in [(1,'R'),(-1,'L')]:
 center=Vector((side*.190,-.002,.714));axis=Vector((side*.041,-.012,-.125)).normalized();right=axis.cross(Vector((0,1,0))).normalized();depth=axis.cross(right).normalized()
 vs=[];fs=[];N=40
 rows=[(-.024,.050),(-.016,.065),(.008,.068),(.026,.058),(.019,.047),(-.018,.044)]
 for height,radius in rows:
  for i in range(N):
   a=math.tau*i/N;r=radius*(1+.035*math.sin(3*a+side));vs.append(tuple(center+axis*height+right*(r*math.cos(a))+depth*(r*math.sin(a))))
 for row in range(len(rows)):
  nxt=(row+1)%len(rows)
  for i in range(N):fs.append((row*N+i,row*N+(i+1)%N,nxt*N+(i+1)%N,nxt*N+i))
 cuff=mesh('RolledCuff_'+label,vs,fs,'Cream');mod=cuff.modifiers.new('Soft cuff preview','SUBSURF');mod.levels=1;mod.render_levels=1
for side,label in [(1,'R'),(-1,'L')]:
 pieces=[];vs=[];fs=[];segments=36
 rows=[(.079,.008,.004,.022,.032),(.069,.005,.027,.004,.061),(.042,0,.042,0,.078),(-.005,0,.041,.011,.092),(-.070,0,.051,.015,.070),(-.125,0,.061,0,.061),(-.154,0,.055,.004,.047)]
 for y,x,rx,base,top in rows:
  for k in range(segments):
   a=math.tau*k/segments;xx=x+rx*math.cos(a);z=(top+base)/2+(top-base)/2*math.sin(a)
   # Medial arch raised locally, plantar contact retained at heel and ball.
   z+=.006*math.exp(-((y+.025)/.048)**2)*max(0,-math.cos(a))
   vs.append((xx,y,z))
 for j in range(len(rows)-1):
  for k in range(segments):fs.append((j*segments+k,j*segments+(k+1)%segments,(j+1)*segments+(k+1)%segments,(j+1)*segments+k))
 for j in [0,len(rows)-1]:
  center=len(vs);y,x,rx,base,top=rows[j];vs.append((x,y,(top+base)/2))
  for k in range(segments):fs.append((center,j*segments+k,j*segments+(k+1)%segments))
 base=mesh('FootMain_'+label,vs,fs,'Skin');pieces.append(base)
 for i,(x,y,rx,ry,rz) in enumerate([(-.043,-.168,.020,.035,.023),(-.009,-.174,.014,.033,.021),(.018,-.165,.013,.031,.020),(.042,-.155,.012,.027,.018),(.061,-.143,.011,.023,.016)]):
  pieces.append(ellipsoid('Toe'+str(i+1)+'_'+label,(x,y,.026),(rx,ry,rz)))
 # Skin lower leg joins the foot and runs beneath the trouser cuff.
 ankle=ellipsoid('Ankle_'+label,(0,.014,.123),(.043,.041,.095))
 for v in ankle.data.vertices:
  f=lerp(v.co.z,[(.028,1.),(.070,.85),(.120,.80),(.175,1.03),(.218,1.08)])
  v.co.x*=f;v.co.y=.014+(v.co.y-.014)*f
 pieces.append(ankle)
 pieces.append(ellipsoid('RoundedHeel_'+label,(.003,.030,.031),(.035,.038,.028)))
 bpy.ops.object.select_all(action='DESELECT')
 for o in pieces:o.select_set(True)
 bpy.context.view_layer.objects.active=base;bpy.ops.object.join();base.name='YT4_BareFoot_'+label
 remesh=base.modifiers.new('Unified foot form','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0023;remesh.use_smooth_shade=True
 bpy.ops.object.modifier_apply(modifier=remesh.name)
 smooth=base.modifiers.new('Gentle foot smoothing','SMOOTH');smooth.factor=.35;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
 localmin=min(v.co.z for v in base.data.vertices);angle=side*math.radians(10 if side>0 else 28)
 for v in base.data.vertices:
  x,y,z=v.co;x*=side
  v.co=(side*.131+x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),max(0,z-localmin))
 for p in base.data.polygons:p.use_smooth=True
 base['toe_count']=5;base['barefoot']=True;base['sole_z']=0.;base['toe_order_medial_to_lateral']='Big, second, third, fourth, fifth'
# Source components remain recoverable, but none are part of the active player.
for name in ['YT_Character','YT_HeadHair_V3','REF_CHARACTER','REF_PORTRAIT']:
 old=bpy.data.collections[name];old.hide_render=True;old.hide_viewport=True
# Only the new reference sheet is active, at one locked common pixel scale.
refs=bpy.data.collections.new('REF_PLAYER_FINAL');s.collection.children.link(refs)
align=json.loads((R/'Reference/BarefootFinal/Alignment.json').read_text());scale=align['scale_m_per_pixel']
for row in align['views']:
 image=bpy.data.images.load(str(R/'Reference/BarefootFinal'/row['file']));image.pack();image.filepath='//../Reference/BarefootFinal/'+row['file']
 ob=bpy.data.objects.new('REF_FINAL_'+row['name'],None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=image
 w,h=image.size;l,t,rr,b=row['crop'];ob.empty_display_size=max(w,h)*scale
 ob.empty_image_offset=(-(row['axis_global']-l)/w,-(b-align['sole_pixel_global'])/h)
 n=Vector(row['normal']).normalized();ob.rotation_euler=n.to_track_quat('Z','Y').to_euler();ob.location=n*.40
 ob.color=(1,1,1,.40);ob.use_empty_image_alpha=True;ob.empty_image_depth='FRONT';ob.empty_image_side='FRONT';ob.show_empty_image_perspective=False;ob.show_empty_image_orthographic=True;ob.show_empty_image_only_axis_aligned=True
 ob.lock_location=(True,True,True);ob.lock_rotation=(True,True,True);ob.lock_scale=(True,True,True);ob.hide_select=True;ob['scale_m_per_pixel']=scale;ob['ground_z']=0.;ob['authoritative_reference']='BarefootFinal'
for name,loc,size in [('Portrait',(.75,.3,1.0),.9),('BareFeetDetail',(.67,.3,.16),.55),('GameDirections',(-.80,.3,.7),.8)]:
 im=bpy.data.images.load(str(R/'Reference/BarefootFinal'/(name+'.png')));im.pack();im.filepath='//../Reference/BarefootFinal/'+name+'.png'
 ob=bpy.data.objects.new('REF_FINAL_'+name,None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.empty_display_size=size;ob.location=loc;ob.rotation_euler=Vector((0,-1,0)).to_track_quat('Z','Y').to_euler();ob.color=(1,1,1,.45);ob.use_empty_image_alpha=True;ob.empty_image_depth='FRONT';ob.show_empty_image_perspective=False;ob.hide_select=True;ob.lock_location=ob.lock_rotation=ob.lock_scale=(True,True,True)
s['active_character_reference']='BarefootFinal/Player_Barefoot_Turnaround.png';s['correction_pass']='V4 likeness and silhouette only; static meshes; rig and source preserved'
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  sp=a.spaces.active;sp.shading.type='MATERIAL';sp.overlay.show_bones=False;sp.region_3d.view_rotation=Vector((0,-1,0)).to_track_quat('Z','Y');sp.region_3d.view_location=(0,0,.70);sp.region_3d.view_distance=2.15;sp.region_3d.view_perspective='ORTHO'
bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=hair;bpy.context.view_layer.update()
path=R/'Source/YoungTrainer_BarefootReference_V4.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),check_existing=False)
print('V4_SAVED',len(C.objects),'active objects','hair_lobes',len(lobes),'toe_counts',[bpy.data.objects['YT4_BareFoot_'+l]['toe_count'] for l in ['L','R']])
