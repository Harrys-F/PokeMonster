exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
body=bpy.data.objects['HNV2_Body'];skin=body.data.materials[0]
if not globals().get('KEEP_DETAILS',False):archive([o for o in list(C['HOBBIT_FACE'].objects)]+list(C['HOBBIT_HAIR'].objects))
# Preserve the old lower torso/joint cage; replace only head, hands and feet locally.
bm=bmesh.new();bm.from_mesh(body.data)
for point,normal in [((0,0,1.047),(0,0,1)),((.622,0,0),(1,0,0)),((-.622,0,0),(-1,0,0)),((0,0,.091),(0,0,-1))]:
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=point,plane_no=normal,clear_outer=True)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.to_mesh(body.data);bm.free()
V=[tuple(v.co) for v in body.data.vertices];F=[list(p.vertices) for p in body.data.polygons]
bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table();bm.verts.index_update();boundary=[e for e in bm.edges if e.is_boundary];groups=[];seen=set()
for e in boundary:
 if e in seen:continue
 todo=[e];seen.add(e);verts=set()
 while todo:
  edge=todo.pop();verts.update(v.index for v in edge.verts)
  for v in edge.verts:
   for other in v.link_edges:
    if other.is_boundary and other not in seen:seen.add(other);todo.append(other)
 groups.append(list(verts))
bm.free();assert len(groups)==5,[len(x) for x in groups]
def ring(points):
 a=[]
 for p in points:a.append(len(V));V.append(tuple(p))
 return a

def bridge(a,b):
 assert len(a)==len(b)
 for j in range(len(a)):F.append([a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]])

def cap(a):F.append(list(reversed(a)))
def mean(ids):return sum((Vector(V[i]) for i in ids),Vector())/len(ids)
head=next(g for g in groups if mean(g).z>1);head.sort(key=lambda i:math.atan2(V[i][1],V[i][0]));angles=[math.atan2(V[i][1],V[i][0]) for i in head]
# Adult jaw, narrower lower cheeks, recessed orbit, sculpted nose and smile creases.
profiles=[(1.047,.050,.044,0),(1.056,.050,.048,-.003),(1.066,.060,.057,-.008),(1.078,.078,.066,-.006),(1.090,.092,.073,-.002),(1.108,.101,.080,.001),(1.128,.109,.087,.006),(1.148,.113,.090,.008),(1.168,.112,.090,.008),(1.187,.110,.089,.009),(1.205,.107,.087,.010),(1.224,.106,.083,.013),(1.245,.101,.079,.015),(1.263,.089,.071,.015),(1.278,.062,.051,.016),(1.288,.006,.005,.016)]
def interp(z):
 for a,b in zip(profiles,profiles[1:]):
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);return [a[i]*(1-t)+b[i]*t for i in range(1,4)]
 return profiles[-1][1:]
def gauss(x,z,cx,cz,wx,wz):return math.exp(-((x-cx)/wx)**2-((z-cz)/wz)**2)
def sculpt_face(x,y,z):
 # Only anterior skin is affected; rear skull remains a smooth adult cranial volume.
 front=max(0.,min(1.,(-y-.003)/.055));d=0.
 for sign in [-1,1]:
  d+=.013*gauss(x,z,sign*.043,1.184,.023,.013) # orbit recess
  d-=.006*gauss(x,z,sign*.045,1.203,.030,.010) # brow ridge
  d-=.007*gauss(x,z,sign*.066,1.160,.028,.017) # cheekbone plane
  d+=.004*gauss(x,z,sign*.066,1.131,.025,.018) # leaner lower cheek
  d+=.0019*gauss(x,z,sign*(.029+.16*(1.145-z)),1.131,.004,.019) # smile fold
 d-=.015*gauss(x,z,0,1.176,.012,.026) # nasal bridge
 d-=.026*gauss(x,z,0,1.156,.016,.012) # soft tip
 for sign in [-1,1]:d-=.008*gauss(x,z,sign*.015,1.151,.009,.007)
 d-=.006*gauss(x,z,0,1.115,.034,.009) # lip support
 d-=.007*gauss(x,z,0,1.087,.050,.013) # mature chin
 return y+d*front
prev=head
for z in [1.052]+[1.057+i*(1.288-1.057)/47 for i in range(48)]:
 rx,ry,cy=interp(z);rr=[]
 for a in angles:
  x=rx*math.cos(a);y=cy+ry*math.sin(a);rr.append((x,sculpt_face(x,y,z),z))
 nxt=ring(rr);bridge(prev,nxt);prev=nxt
cap(prev)
hand_meta=[]
for sign,side in [(1,'L'),(-1,'R')]:
 g=next(g for g in groups if mean(g).x*sign>.6);cz=mean(g).z;g.sort(key=lambda i:math.atan2(V[i][2]-cz,V[i][1]));aa=[math.atan2(V[i][2]-cz,V[i][1]) for i in g];prev=g
 for x,ry,rz,cy,dz in [(.630,.029,.021,0,0),(.645,.034,.020,-.003,-.001),(.661,.041,.019,-.004,-.001),(.682,.044,.019,-.004,-.002),(.700,.043,.017,-.002,-.003),(.710,.036,.014,0,-.003)]:
  nxt=ring([(sign*x,cy+ry*math.cos(a),cz+dz+rz*math.sin(a)) for a in aa]);bridge(prev,nxt);prev=nxt
 cap(prev);hand_meta.append((sign,side,cz))
for sign,side in [(1,'L'),(-1,'R')]:
 g=next(g for g in groups if mean(g).z<.12 and mean(g).x*sign>0);cx=abs(mean(g).x);g.sort(key=lambda i:math.atan2(V[i][1],V[i][0]-sign*cx));aa=[math.atan2(V[i][1],V[i][0]-sign*cx) for i in g];prev=g
 for z,rx,ry,cy in [(.086,.037,.044,0),(.076,.043,.067,-.004),(.062,.058,.097,-.017),(.045,.068,.119,-.031),(.027,.068,.125,-.036),(.010,.061,.123,-.038),(.002,.054,.115,-.037),(0,.051,.109,-.037)]:
  nxt=ring([(sign*cx+rx*math.cos(a),cy+ry*math.sin(a),z) for a in aa]);bridge(prev,nxt);prev=nxt
 cap(prev)
me=bpy.data.meshes.new('HNV2_AdultAnatomy');me.from_pydata(V,[],F);me.update();me.materials.append(skin);body.data=me
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));print('Pre-union manifold',sum(not e.is_manifold for e in bm.edges));bm.to_mesh(me);bm.free()
# Full fingers with palm webs, knuckle rings, bent fingertip profiles and a distinct thumb.
for sign,side,cz in hand_meta:
 for i,(yy,length,r) in enumerate([(-.032,.067,.010),(-.010,.081,.0105),(.014,.071,.0098),(.035,.053,.0084)]):
  pts=[(sign*(.690+length*t),yy-.002*math.sin(math.pi*t),cz-.003-.003*math.sin(math.pi*t)) for t in [0,.08,.20,.35,.49,.57,.72,.84,.94,1]]
  radius=lambda t,r=r:r*(.15+.85*math.sin(math.pi*(.10+.82*t))**.45)*(1+.10*math.exp(-((t-.48)/.08)**2))
  body_union(tube('WorkFinger_'+side+'_'+str(i+1),pts,radius,'MODEL_WORK',skin,12,flatten=.88))
 pts=[(sign*(.652+.058*t),-.024-.055*t,cz-.006-.009*t) for t in [0,.12,.28,.46,.58,.75,.9,1]]
 body_union(tube('WorkThumb_'+side,pts,lambda t:.013*(.16+.84*math.sin(math.pi*(.13+.75*t))**.55),'MODEL_WORK',skin,12,flatten=.9))
 # Toes have a low plantar pad, graduated length, and metatarsal support.
 cx=.1121
 for i,(xx,ty,r) in enumerate([(-.044,-.230,.0185),(-.020,-.238,.016),(.004,-.231,.0145),(.026,-.218,.0128),(.046,-.199,.0108)]):
  pts=[(sign*(cx+xx),-.121+(ty+.121)*t,.025-.006*t+.003*math.sin(math.pi*t)) for t in [0,.12,.3,.45,.6,.77,.91,1]]
  body_union(tube('WorkToe_'+side+'_'+str(i+1),pts,lambda t,r=r:r*(.17+.83*math.sin(math.pi*(.12+.77*t))**.45),'MODEL_WORK',skin,12,flatten=.82))
 # Outer ears are part of the skin; their rim/folds are refined at the face stage.
 ear=sphere('WorkEar_'+side,(sign*.113,.010,1.167),(.023,.026,.041),'MODEL_WORK',skin,20,14)
 for v in ear.data.vertices:
  if v.co.z>0:v.co.x+=sign*.004*(v.co.z/.041)**2
 body_union(ear)
# Four grooves per foot separate the distal toes but preserve the common forefoot.
for sign in [1,-1]:
 for i,x in enumerate([.080,.104,.127,.148]):
  bpy.ops.mesh.primitive_cube_add(size=1,location=(sign*x,-.207,.027));o=bpy.context.object;o.name='HNV2_WorkToeGap'
  for col in list(o.users_collection):col.objects.unlink(o)
  C['MODEL_WORK'].objects.link(o);o.scale=(.003,.085,.09);active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  b=o.modifiers.new('SoftToeWeb','BEVEL');b.width=.001;b.segments=2;apply(o,b)
  m=body.modifiers.new('ToeSeparation','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=o;apply(body,m);bpy.data.objects.remove(o,do_unlink=True)
# Restrained calf/forearm definition and exact body symmetry, without global subdivision.
for v in body.data.vertices:
 p=v.co;ax=abs(p.x)
 if .46<ax<.61 and .88<p.z<.98:
  p.y-=.0015*math.exp(-((ax-.525)/.055)**2)*math.exp(-((p.z-.922)/.02)**2)
 if .10<p.z<.27 and ax<.22:p.y-=.0018*math.exp(-((p.z-.16)/.07)**2)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(1,0,0),clear_inner=True);bm.to_mesh(body.data);bm.free();mi=body.modifiers.new('ExactAdultBodySymmetry','MIRROR');mi.use_mirror_merge=True;mi.merge_threshold=1e-5;apply(body,mi)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
body.data.materials.clear();body.data.materials.append(skin)
for p in body.data.polygons:p.material_index=0;p.use_smooth=True
body['five_fingers_per_hand']=True;body['five_toes_per_foot']=True;body['rig_ready']=False;body['local_topology']='retained torso/limb rings, new head rows, palm/knuckle and ankle/toe support; unions require local retopology before high deformation'
(BASE/'Review/V2/AnatomyStage.json').write_text(json.dumps({'boundary_counts_before_reconstruction':[len(g) for g in groups],'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons),'finger_endpoints_per_hand':5,'toe_endpoints_per_foot':5},indent=2))
save_stage('01_AnatomyCorrected' if globals().get('KEEP_DETAILS',False) else '01_Anatomy')
print('Adult anatomy stage complete',len(body.data.vertices),len(body.data.polygons))
