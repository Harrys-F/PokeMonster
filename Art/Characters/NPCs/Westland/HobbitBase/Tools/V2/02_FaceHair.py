exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];skin=body.data.materials[0];dg=bpy.context.evaluated_depsgraph_get();bvh=BVHTree.FromObject(body,dg)
def face_y(x,z,margin=.001):
 hit=bvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1.)[0]
 assert hit is not None,(x,z)
 return hit.y-margin
skin_node=next(n for n in skin.node_tree.nodes if n.type=='BSDF_PRINCIPLED');skin_node.inputs['Base Color'].default_value=(.47,.245,.145,1);skin_node.inputs['Roughness'].default_value=.6
if 'Subsurface Weight' in skin_node.inputs:skin_node.inputs['Subsurface Weight'].default_value=.065;skin_node.inputs['Subsurface Scale'].default_value=.008
# A subtle authored skin tint emphasizes cheeks/nose without bitmap textures.
a=body.data.color_attributes.new(name='HNV2_SkinTint',type='FLOAT_COLOR',domain='POINT')
for v in body.data.vertices:
 x,y,z=v.co;pink=0.
 if y<0 and z>1.07:
  pink=max(math.exp(-((abs(x)-.065)/.030)**2-((z-1.157)/.022)**2),.7*math.exp(-(x/.020)**2-((z-1.156)/.016)**2))*.05
 a.data[v.index].color=(.47+pink,.245-pink*.12,.145-pink*.10,1)
nt=skin.node_tree;attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='HNV2_SkinTint';nt.links.new(attr.outputs['Color'],skin_node.inputs['Base Color'])
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=430;noise.inputs['Detail'].default_value=2
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.065;bump.inputs['Distance'].default_value=.00012;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],skin_node.inputs['Normal'])
# Detail skin uses the same base tint but no absent vertex attribute.
skindetail=material('FaceSkin',(.48,.255,.155),.6);eyewhite=material('Sclera',(.49,.455,.37),.28);irism=material('HazelIris',(.073,.034,.014),.27);pupil=material('DeepPupil',(.004,.002,.001),.24)
lip=material('MutedLips',(.31,.118,.079),.59);mouth=material('MouthLine',(.12,.038,.024),.76);earm=material('EarWarmth',(.405,.187,.116),.74);nailmat=material('NaturalNails',(.50,.30,.20),.42)
hairm=[material('CurlBrown_'+str(i),(.032+i*.008,.010+i*.0035,.0045+i*.0018),.53) for i in range(4)]
for m in hairm:
 n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=125;n.inputs['Detail'].default_value=2
 b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.08;b.inputs['Distance'].default_value=.0003;m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],next(q for q in m.node_tree.nodes if q.type=='BSDF_PRINCIPLED').inputs['Normal'])
faceparts=[]
for sign,side in [(1,'L'),(-1,'R')]:
 cx=sign*.043;cy=-.070;cz=1.184
 sphere('Eye_'+side,(cx,cy,cz),(.019,.014,.0095),'HOBBIT_FACE',eyewhite,32,20)
 # Curved small iris discs face the same forward direction; not divergent button eyes.
 sphere('Iris_'+side,(cx-sign*.0003,cy-.0141,cz),(.006,.0011,.0063),'HOBBIT_FACE',irism,24,16)
 sphere('Pupil_'+side,(cx-sign*.0003,cy-.01505,cz),(.0029,.00045,.0036),'HOBBIT_FACE',pupil,20,12)
 for upper in [True,False]:
  pts=[]
  for j in range(25):
   t=j/24;x=cx+sign*.019*math.cos(math.pi*t);z=cz+(.0088 if upper else -.0069)*math.sin(math.pi*t)
   r2=((x-cx)/.019)**2+((z-cz)/.0095)**2;y=cy-.014*math.sqrt(max(0,1-r2))-.0007
   y=min(y,face_y(x,z,.0004));pts.append((x,y,z))
  tube(('UpperLid_' if upper else 'LowerLid_')+side,pts,lambda t:(.0017 if upper else .0012)*(.45+.55*math.sin(math.pi*t)),'HOBBIT_FACE',skindetail,10)
 pts=[]
 for j in range(18):
  t=j/17;x=sign*(.026+.042*t);z=1.203+.004*math.sin(math.pi*t)-.0015*t;pts.append((x,face_y(x,z,.0014),z))
 tube('SculptedBrow_'+side,pts,lambda t:.0034*(.25+.75*math.sin(math.pi*(.12+.81*t))),'HOBBIT_FACE',hairm[0],8,flatten=.43)
 # A soft eyelid crease belongs to the orbital plane, not a painted black outline.
 pts=[]
 for j in range(16):
  t=j/15;x=sign*(.025+.036*t);z=1.197+.0035*math.sin(math.pi*t);pts.append((x,face_y(x,z,.00035),z))
 tube('OrbitalFold_'+side,pts,lambda t:.0007*math.sin(math.pi*(.05+.9*t)),'HOBBIT_FACE',skindetail,6)
 # Helix and antihelix follow the actual integrated ear surface.
 pts=[]
 for j in range(33):
  t=j/32;aa=-.7+math.tau*.88*t;y=.010+.020*math.cos(aa);z=1.167+.034*math.sin(aa)
  hit=bvh.ray_cast(Vector((sign*.3,y,z)),Vector((-sign,0,0)),.4)[0]
  pts.append((hit.x+sign*.001 if hit else sign*.13,y,z))
 tube('EarHelix_'+side,pts,.0019,'HOBBIT_FACE',skindetail,8)
 pts=[]
 for j in range(17):
  t=j/16;y=.004+.009*math.sin(t*math.pi);z=1.145+.031*t;hit=bvh.ray_cast(Vector((sign*.3,y,z)),Vector((-sign,0,0)),.4)[0]
  pts.append((hit.x+sign*.0007,y,z))
 tube('EarInnerFold_'+side,pts,lambda t:.0015*(.5+.5*math.sin(math.pi*t)),'HOBBIT_FACE',earm,8)
# Sculpted lips and restrained nasolabial corners, no sphere nose or drawn-on broad smile.
for name,dz,mat,r in [('UpperLip',.0018,lip,.0014),('LowerLip',-.0018,lip,.0021),('MouthSeam',0,mouth,.00055)]:
 pts=[]
 for j in range(33):
  t=j/32;x=(t-.5)*.063;z=1.115+.0045*(abs(x)/.0315)**1.8+dz
  if name=='UpperLip':z+=.0012*math.sin(abs(x)/.0315*math.pi*1.3)
  pts.append((x,face_y(x,z,.0008),z))
 tube(name,pts,lambda t,r=r:r*(.2+.8*math.sin(math.pi*t)),'HOBBIT_FACE',mat,10,flatten=.75)
for sign,side in [(1,'L'),(-1,'R')]:
 pts=[]
 for j in range(13):
  t=j/12;x=sign*(.010+.009*t);z=1.148+.0014*math.sin(math.pi*t);pts.append((x,face_y(x,z,.0003),z))
 tube('Nostril_'+side,pts,lambda t:.00065*math.sin(math.pi*(.07+.86*t)),'HOBBIT_FACE',mouth,6)
# Individually modeled nails and subtle knuckle arcs. Skin remains one closed body.
nails=[];hairfeet=[]
for sign,side in [(1,'L'),(-1,'R')]:
 for i,(yy,endx) in enumerate([(-.032,.757),(-.010,.771),(.014,.763),(.035,.740)]):
  hit=bvh.ray_cast(Vector((sign*endx,yy,1.03)),Vector((0,0,-1)),.2)[0]
  if hit:nails.append(sphere('HandNail_'+side+'_'+str(i),(sign*endx,yy,hit.z+.0003),(.0065,.0054,.0006),'HOBBIT_FACE',nailmat,16,8))
 hit=bvh.ray_cast(Vector((sign*.702,-.069,1.03)),Vector((0,0,-1)),.2)[0]
 if hit:nails.append(sphere('ThumbNail_'+side,(sign*.702,-.069,hit.z+.0003),(.0058,.0052,.0006),'HOBBIT_FACE',nailmat,16,8))
 for i,(xx,yy,r) in enumerate([(.068,-.214,.010),(.092,-.220,.0085),(.116,-.215,.0078),(.138,-.204,.0065),(.158,-.189,.0055)]):
  hit=bvh.ray_cast(Vector((sign*xx,yy,.14)),Vector((0,0,-1)),.14)[0]
  if hit:nails.append(sphere('ToeNail_'+side+'_'+str(i),(sign*xx,yy,hit.z+.0003),(r,.010 if i<2 else .007,.0006),'HOBBIT_FACE',nailmat,16,8))
 rng=random.Random(927)
 for j in range(22):
  x=.112+rng.uniform(-.039,.039);y=rng.uniform(-.126,-.067);hit=bvh.ray_cast(Vector((sign*x,y,.14)),Vector((0,0,-1)),.14)[0]
  if not hit:continue
  length=rng.uniform(.007,.013);pts=[tuple(hit+Vector((sign*.002*t,-length*t,.001+.004*math.sin(math.pi*t)))) for t in [0,.2,.4,.6,.8,1]]
  hairfeet.append(tube('FootHair_'+side+'_'+str(j),pts,lambda t:.00045*(1-.8*t),'HOBBIT_HAIR',hairm[0],5))
if nails:join(nails,'FingerAndToeNails')
if hairfeet:join(hairfeet,'FootHair')
# A varied sculpted mass of thick curled locks replaces the exposed cap and sparse worms.
vv=[];ff=[];N=64;K=18
for k in range(K+1):
 t=k/K
 for j in range(N):
  ph=math.tau*j/N;mx=1.87+.23*max(0,math.sin(ph))-.48*max(0,-math.sin(ph));th=.018+t*(mx-.018)
  wave=1+.022*math.cos(4*ph)*math.sin(th)**2
  vv.append((.129*math.cos(ph)*math.sin(th)*wave,.012+.103*math.sin(ph)*math.sin(th)*wave,1.205+.109*math.cos(th)))
for k in range(K):
 for j in range(N):ff.append([k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j])
ff.append(list(reversed(range(N))));core=mesh('HairUnderMass',vv,ff,'HOBBIT_HAIR',[hairm[0]]);so=core.modifiers.new('HairShellThickness','SOLIDIFY');so.thickness=.003;so.offset=-1
rng=random.Random(2418);locks=[]
def curl(name,theta,phi,width,length,phase):
 # Thick flattened tear-drop sweep, with an outward hooked tip and small broad flutes.
 points=[];normals=[];K=14;S=10
 for i in range(K):
  t=i/(K-1);th=theta+length*(t-.5);ph=phi+.10*math.sin(math.pi*t+phase)+.08*t
  n=Vector((math.cos(ph)*math.sin(th),math.sin(ph)*math.sin(th),math.cos(th))).normalized()
  p=Vector((.134*n.x,.012+.111*n.y,1.205+.114*n.z))
  p+=n*(.007*math.sin(math.pi*t)-.003*(1-t));p+=Vector((-math.sin(ph),math.cos(ph),0))*(.010*math.sin(math.pi*t)*math.sin(phase+t*math.tau*.8))
  points.append(p);normals.append(n)
 vs=[];fs=[]
 for i,p in enumerate(points):
  t=i/(K-1);d=(points[min(K-1,i+1)]-points[max(0,i-1)]).normalized();u=normals[i].cross(d).normalized();v=d.cross(u).normalized();w=width*(.20+.80*math.sin(math.pi*(.10+.86*t)))
  for j in range(S):
   a=math.tau*j/S;flute=1+.08*math.cos(3*a+phase)
   vs.append(tuple(p+u*(w*math.cos(a)*flute)+v*(w*.58*math.sin(a)*flute)))
 for i in range(K-1):
  for j in range(S):fs.append([i*S+j,i*S+(j+1)%S,(i+1)*S+(j+1)%S,(i+1)*S+j])
 fs.extend([list(reversed(range(S))),list(range((K-1)*S,K*S))]);o=mesh(name,vs,fs,'HOBBIT_HAIR',[hairm[rng.randrange(4)]]);return o
for k in range(56):
 theta=.17+(k+.5)/56*1.84;phi=-math.pi/2+((k*.61803398875)%1)*math.pi
 mx=1.87+.23*max(0,math.sin(phi))-.48*max(0,-math.sin(phi))
 if theta>mx-.08:continue
 width=rng.uniform(.012,.022);length=rng.uniform(.30,.51);phase=rng.uniform(-math.pi,math.pi)
 o=curl('Curl_L_'+str(k),theta,phi,width,length,phase);locks.append(o)
 # Hair and facial expression remain symmetric; variations are distributed, not uniform beads.
 copy=o.copy();copy.data=o.data.copy();C['HOBBIT_HAIR'].objects.link(copy);copy.name='HNV2_Curl_R_'+str(k)
 for v in copy.data.vertices:v.co.x=-v.co.x
 bm=bmesh.new();bm.from_mesh(copy.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(copy.data);bm.free();locks.append(copy)
# Dedicated layered forehead hooks frame the adult brow without covering the eyes.
for sign,side in [(1,'L'),(-1,'R')]:
 for j in range(3):
  pts=[]
  for i in range(17):
   t=i/16;x=sign*(.020+j*.027+.012*math.sin(math.pi*t));y=-.078-.024*math.sin(math.pi*t);z=1.277-.064*t+.006*math.sin(t*math.tau)
   pts.append((x,y,z))
  locks.append(tube('ForeheadHook_'+side+'_'+str(j),pts,lambda t:.0095*(.2+.8*math.sin(math.pi*(.12+.83*t))),'HOBBIT_HAIR',hairm[j+1],10,flatten=.70))
locks=join(locks,'SculptedCurls')
# Only hair is calibrated. Body, sole, clothing and T-pose dimensions are not globally scaled.
activehair=[core,locks];bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();top=max((o.matrix_world@v.co).z for o in activehair for v in o.evaluated_get(dg).data.vertices)
anchor=1.14;factor=(1.32-anchor)/(top-anchor)
for o in activehair:
 for v in o.data.vertices:v.co.z=anchor+(v.co.z-anchor)*factor
scene['hair_height_factor']=factor;scene['calibrated_height_m']=1.32
save_stage('02_FaceHair');print(json.dumps({'hair_factor':factor,'new_hair_vertices':len(locks.data.vertices),'nail_count_before_join':len(nails),'no_rig':True}))
