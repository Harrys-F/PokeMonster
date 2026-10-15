exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];skindetail=bpy.data.materials['HNV2_FaceSkin'];eyewhite=bpy.data.materials['HNV2_Sclera'];iris=bpy.data.materials['HNV2_HazelIris'];pupil=bpy.data.materials['HNV2_DeepPupil'];mouthmat=bpy.data.materials['HNV2_MouthLine'];lipmat=bpy.data.materials['HNV2_MutedLips'];nailmat=bpy.data.materials['HNV2_NaturalNails']
# Smooth the ankle section into the old calf, instead of leaving a cuff-like step.
for v in body.data.vertices:
 x,y,z=v.co
 if .076<z<.125:
  cx=.1121 if x>0 else -.1121;aa=math.atan2(y,x-cx)
  profile=[(.076,.043,.061),(.086,.039,.048),(.098,.037,.043),(.113,.040,.046),(.125,.043,.049)]
  for a,b in zip(profile,profile[1:]):
   if a[0]<=z<=b[0]:
    t=(z-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);rx=a[1]*(1-t)+b[1]*t;ry=a[2]*(1-t)+b[2]*t;v.co.x=cx+rx*math.cos(aa);v.co.y=ry*math.sin(aa);break
bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
def fy(x,z,offset=.0003):
 hit=bvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)[0]
 assert hit is not None
 return hit.y-offset
# Replace the full visible oval by an anatomical almond aperture in a skin socket.
old=[]
for o in list(C['HOBBIT_FACE'].objects):
 if any(o.name.startswith('HNV2_'+p) for p in ['Eye_','Iris_','Pupil_','UpperLid_','LowerLid_','OrbitalFold_','UpperLip','LowerLip','MouthSeam','FingerAndToeNails']):old.append(o)
archive(old)
for sign,side in [(1,'L'),(-1,'R')]:
 cx=sign*.043;cz=1.184;cy=-.0635;rx=.017;rz=.0095;ry=.011
 sphere('Eye_'+side,(cx,cy,cz),(rx,ry,rz),'HOBBIT_FACE',eyewhite,28,18)
 sphere('Iris_'+side,(cx-sign*.00025,cy-ry-.0003,cz),(.0052,.0008,.0058),'HOBBIT_FACE',iris,24,16)
 sphere('Pupil_'+side,(cx-sign*.00025,cy-ry-.0010,cz),(.0025,.0003,.0034),'HOBBIT_FACE',pupil,20,12)
 vs=[];fs=[];N=64;K=6
 for k in range(K):
  u=k/(K-1);ease=u*u*(3-2*u)
  for j in range(N):
   aa=math.tau*j/N;dx=.0146*math.cos(aa);dz=(.0058 if math.sin(aa)>0 else .0047)*math.sin(aa)
   ix=cx+dx;iz=cz+dz;iy=cy-ry*math.sqrt(max(0,1-(dx/rx)**2-(dz/rz)**2))-.0004
   iy=min(iy,fy(ix,iz,.0001))
   ox=cx+.027*math.cos(aa);oz=cz+(.018 if math.sin(aa)>0 else .016)*math.sin(aa);oy=fy(ox,oz,.00018)
   p=Vector((ix,iy,iz)).lerp(Vector((ox,oy,oz)),ease);p.y-=.0012*math.sin(math.pi*u);vs.append(tuple(p))
 for k in range(K-1):
  for j in range(N):fs.append([k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j])
 o=mesh('OrbitalSkin_'+side,vs,fs,'HOBBIT_FACE',[skindetail]);so=o.modifiers.new('EyelidSkinThickness','SOLIDIFY');so.thickness=.0008;so.offset=1
 for upper in [True,False]:
  pts=[]
  for i in range(25):
   a=math.pi*i/24;dx=.0146*math.cos(a);dz=(.0058 if upper else -.0047)*math.sin(a);y=cy-ry*math.sqrt(max(0,1-(dx/rx)**2-(dz/rz)**2))-.0005;y=min(y,fy(cx+sign*dx,cz+dz,.00015));pts.append((cx+sign*dx,y,cz+dz))
  tube(('UpperLid_' if upper else 'LowerLid_')+side,pts,lambda t:(.00135 if upper else .0009)*(.35+.65*math.sin(math.pi*t)),'HOBBIT_FACE',skindetail,8)
# Broad, shallow lip surfaces replace the three obvious tubing lines.
for name,upper in [('UpperLipSurface',True),('LowerLipSurface',False)]:
 vs=[];fs=[];N=33;K=5
 for k in range(K):
  u=k/(K-1)
  for j in range(N):
   t=j/(N-1);x=(t-.5)*.059;width=(.0022 if upper else .0030)*math.sin(math.pi*t);z=1.115+.0040*(abs(x)/.0295)**1.8+(width*u if upper else -width*u)
   if upper:z+=.0007*math.sin(abs(x)/.0295*math.pi*1.3)*u
   y=fy(x,z,.00015)-.0010*math.sin(math.pi*u)*math.sin(math.pi*t);vs.append((x,y,z))
 for k in range(K-1):
  for j in range(N-1):fs.append([k*N+j,k*N+j+1,(k+1)*N+j+1,(k+1)*N+j])
 o=mesh(name,vs,fs,'HOBBIT_FACE',[lipmat]);so=o.modifiers.new('LipSkinThickness','SOLIDIFY');so.thickness=.0003
pts=[]
for i in range(33):
 t=i/32;x=(t-.5)*.059;z=1.115+.0040*(abs(x)/.0295)**1.8;pts.append((x,fy(x,z,.00045),z))
tube('MouthSeam',pts,lambda t:.00035*(.1+.9*math.sin(math.pi*t)),'HOBBIT_FACE',mouthmat,6)
# Nails are refitted to the corrected (now closed) anatomical skin.
nails=[]
for sign,side in [(1,'L'),(-1,'R')]:
 for i,(yy,endx) in enumerate([(-.032,.752),(-.010,.765),(.014,.758),(.035,.736),(-.069,.703)]):
  hit=bvh.ray_cast(Vector((sign*endx,yy,1.02)),Vector((0,0,-1)),.2)[0]
  assert hit is not None,(side,i)
  nails.append(sphere('NailFinger_'+side+'_'+str(i),(sign*endx,yy,hit.z+.00015),(.006,.0048,.00045),'HOBBIT_FACE',nailmat,16,8))
 for i,(xx,yy,r) in enumerate([(.068,-.211,.009),(.092,-.216,.0077),(.116,-.210,.007),(.138,-.199,.006),(.158,-.179,.005)]):
  hit=bvh.ray_cast(Vector((sign*xx,yy,.14)),Vector((0,0,-1)),.14)[0]
  assert hit is not None,(side,i)
  nails.append(sphere('NailToe_'+side+'_'+str(i),(sign*xx,yy,hit.z+.00015),(r,.008 if i<2 else .006,.00045),'HOBBIT_FACE',nailmat,16,8))
join(nails,'FingerAndToeNails')
# Rebuild curls with rotation-minimizing frames and buried, tapered roots/tips.
archive([bpy.data.objects['HNV2_SculptedCurls']]);rng=random.Random(9413);hm=[bpy.data.materials['HNV2_CurlBrown_'+str(i)] for i in range(4)];locks=[]
for m in hm:
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Roughness'].default_value=.72;p.inputs['Specular IOR Level'].default_value=.22
 # UV across the lock, V along its flow: fine longitudinal striations, no bitmap.
 nt=m.node_tree;tex=nt.nodes.new('ShaderNodeTexCoord');wave=nt.nodes.new('ShaderNodeTexWave');directions=[i.identifier for i in wave.bl_rna.properties['bands_direction'].enum_items]
 if 'X' in directions:wave.bands_direction='X'
 wave.inputs['Scale'].default_value=5.;wave.inputs['Distortion'].default_value=.7;wave.inputs['Detail'].default_value=1.5;nt.links.new(tex.outputs['UV'],wave.inputs['Vector'])
 b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.12;b.inputs['Distance'].default_value=.00018;nt.links.new(wave.outputs['Color'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],p.inputs['Normal'])
def curl(name,th,ph,width,length,phase):
 K=16;S=10;pts=[];ns=[]
 for i in range(K):
  t=i/(K-1);theta=th+length*(t-.5);phi=ph+.13*math.sin(math.pi*t+phase)+.10*t;n=Vector((math.cos(phi)*math.sin(theta),math.sin(phi)*math.sin(theta),math.cos(theta))).normalized();u=Vector((-math.sin(phi),math.cos(phi),0))
  p=Vector((.131*n.x,.012+.108*n.y,1.205+.112*n.z));p+=n*(.010*math.sin(math.pi*t)-.007*(1-t)**2-.004*t**5)
  p+=u*(.011*math.sin(math.pi*t)*math.sin(phase+math.tau*t*.75));pts.append(p);ns.append(n)
 v=[];f=[];lastd=None;frameu=None
 for i,p in enumerate(pts):
  t=i/(K-1);d=(pts[min(K-1,i+1)]-pts[max(0,i-1)]).normalized()
  if lastd is None:frameu=ns[i].cross(d).normalized()
  else:frameu=lastd.rotation_difference(d)@frameu;frameu=(frameu-d*frameu.dot(d)).normalized()
  framev=d.cross(frameu).normalized();lastd=d;w=width*(.06+.94*math.sin(math.pi*t)**.65)
  for j in range(S):
   a=math.tau*j/S;flute=1+.035*math.cos(3*a+phase);v.append(tuple(p+frameu*(w*math.cos(a)*flute)+framev*(w*.50*math.sin(a)*flute)))
 for i in range(K-1):
  for j in range(S):f.append([i*S+j,i*S+(j+1)%S,(i+1)*S+(j+1)%S,(i+1)*S+j])
 f.extend([list(reversed(range(S))),list(range((K-1)*S,K*S))]);o=mesh(name,v,f,'HOBBIT_HAIR',[hm[rng.randrange(4)]]);uv=o.data.uv_layers.new(name='CurlFlowUV')
 for poly in o.data.polygons:
  js=[o.data.loops[k].vertex_index%S for k in poly.loop_indices];wrap=0 in js and S-1 in js
  for k in poly.loop_indices:
   idx=o.data.loops[k].vertex_index;j=idx%S;uv.data[k].uv=((1 if wrap and j==0 else j/S),idx//S/(K-1))
 return o
for i in range(70):
 th=.10+(i+.5)/70*1.85;ph=-math.pi/2+((i*.61803398875)%1)*math.pi;mx=1.87+.23*max(0,math.sin(ph))-.48*max(0,-math.sin(ph))
 if th>mx-.08:continue
 o=curl('FlowCurl_L_'+str(i),th,ph,rng.uniform(.0095,.0165),rng.uniform(.35,.54),rng.uniform(-math.pi,math.pi));locks.append(o);mirror=o.copy();mirror.data=o.data.copy();C['HOBBIT_HAIR'].objects.link(mirror);mirror.name='HNV2_FlowCurl_R_'+str(i)
 for v in mirror.data.vertices:v.co.x=-v.co.x
 bm=bmesh.new();bm.from_mesh(mirror.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mirror.data);bm.free();locks.append(mirror)
for sign,side in [(1,'L'),(-1,'R')]:
 for i,(th,ph) in enumerate([(1.12,-1.34),(1.20,-1.06),(1.24,-.70)]):
  o=curl('Fringe_'+side+'_'+str(i),th,ph,.011,.47,1.1+i*.8)
  if sign<0:
   for v in o.data.vertices:v.co.x=-v.co.x
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  locks.append(o)
locks=join(locks,'SculptedCurls');core=bpy.data.objects['HNV2_HairUnderMass'];bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();top=max((o.matrix_world@v.co).z for o in [core,locks] for v in o.evaluated_get(dg).data.vertices);factor=(1.32-1.14)/(top-1.14)
for o in [core,locks]:
 for v in o.data.vertices:v.co.z=1.14+(v.co.z-1.14)*factor
save_stage('04_FaceHairRefined');print(json.dumps({'nails':len(nails),'curl_vertices':len(locks.data.vertices),'hair_z_calibration':factor}))
