import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
assert 'Hobbit_NPC_Base_V3_Body' not in bpy.data.scenes
s=bpy.data.scenes.new('Hobbit_NPC_Base_V3_Body');bpy.context.window.scene=s
s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
collections={}
for n in ['BODY','EYES','STUDIO']:
 c=bpy.data.collections.new('HNV3_'+n);s.collection.children.link(c);collections[n]=c
V=[];F=[];regions={};face_material=[]
def vert(p):V.append(tuple(p));return len(V)-1
def face(ids,mat=0):F.append(list(ids));face_material.append(mat)
def ring(points):return [vert(p) for p in points]
def bridge(a,b):
 assert len(a)==len(b),(len(a),len(b))
 for j in range(len(a)):face([a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]])
def fit(points,loop):
 # Choose orientation/phase by geometric distance, avoiding twisted joins.
 options=[];N=len(loop)
 for reverse in [False,True]:
  pp=list(reversed(points)) if reverse else list(points)
  for shift in range(N):
   q=pp[shift:]+pp[:shift]
   score=sum((Vector(V[i])-Vector(p)).length_squared for i,p in zip(loop,q))
   options.append((score,q))
 return min(options,key=lambda a:a[0])[1]
def rect_loop(grid,j0,j1,k0,k1,N):
 return [grid[k0][j%N] for j in range(j0,j1)]+[grid[k][j1%N] for k in range(k0,k1)]+[grid[k1][j%N] for j in range(j1,j0,-1)]+[grid[k][j0%N] for k in range(k1,k0,-1)]
def cap(loop,p):
 c=vert(p)
 for j in range(len(loop)):face([loop[j],loop[(j+1)%len(loop)],c])
def lerp_profile(profile,z):
 for k,(a,b) in enumerate(zip(profile,profile[1:])):
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);h=b[0]-a[0];out=[]
   for i in range(1,len(a)):
    aa=profile[max(0,k-1)];bb=profile[min(len(profile)-1,k+2)]
    ma=(b[i]-aa[i])/(b[0]-aa[0]);mb=(bb[i]-a[i])/(bb[0]-a[0])
    out.append((2*t**3-3*t*t+1)*a[i]+(t**3-2*t*t+t)*h*ma+(-2*t**3+3*t*t)*b[i]+(t**3-t*t)*h*mb)
   return tuple(out)
 return tuple(profile[0 if z<profile[0][0] else -1][1:])
def gaussian(x,z,cx,cz,rx,rz):return math.exp(-((x-cx)/rx)**2-((z-cz)/rz)**2)

# New torso cage: sections follow pelvis, belly, ribs, clavicles and neck.
N=48
zs=[.610,.640,.670,.700,.735,.770,.805,.840,.875,.900,.923,.945,.968,.990,1.014,1.038,1.046,1.051,1.055]
zs=sorted(zs+[(a+b)/2 for a,b in zip(zs,zs[1:]) if b<=.923])
profile=[(.610,.173,.125,.008),(.670,.190,.139,.004),(.735,.182,.147,-.012),(.805,.176,.143,-.010),(.875,.175,.123,-.003),(.945,.185,.112,0),(1.014,.135,.081,.003),(1.038,.065,.052,.006),(1.046,.052,.045,.008),(1.051,.049,.044,.009),(1.055,.049,.044,.010)]
torso=[]
for z in zs:
 rx,ry,cy=lerp_profile(profile,z);points=[]
 for j in range(N):
  a=math.tau*j/N;x=rx*math.sin(a);y=cy-ry*math.cos(a);front=max(0,math.cos(a))**6
  y-=front*.009*gaussian(abs(x),z,.079,.946,.075,.065)
  y+=front*.005*gaussian(x,z,0,.788,.016,.015)
  y+=front*.003*gaussian(abs(x),z,.073,1.018,.080,.010)
  if math.cos(a)<0:y-=.006*gaussian(x,z,0,.67,.018,.045)
  points.append((0 if abs(x)<1e-10 else x,y,z))
 torso.append(ring(points))
arm_holes=[(9,15,zs.index(.945),zs.index(1.038)),(33,39,zs.index(.945),zs.index(1.038))]
for k in range(len(zs)-1):
 for j in range(N):
  if any(j0<=j<j1 and k0<=k<k1 for j0,j1,k0,k1 in arm_holes):continue
  face([torso[k][j],torso[k][(j+1)%N],torso[k+1][(j+1)%N],torso[k+1][j]])
regions['torso_levels']=zs;regions['shoulder_holes']=arm_holes

def limb_from_loop(loop,sections,axis,sign=1):
 prev=loop;ordered=None
 for idx,section in enumerate(sections):
  if axis=='X':
   x,cy,cz,ry,rz=section;points=[(sign*x,cy+ry*math.cos(math.tau*j/len(loop)),cz+rz*math.sin(math.tau*j/len(loop))) for j in range(len(loop))]
  else:
   z,cx,cy,rx,ry=section;points=[(sign*(cx+rx*math.sin(math.tau*j/len(loop))),cy-ry*math.cos(math.tau*j/len(loop)),z) for j in range(len(loop))]
  # The same phase/order is propagated through every ring.
  if idx==0:
   ordered=fit(points,loop)
   mapping=[min(range(len(points)),key=lambda j:(Vector(p)-Vector(points[j])).length_squared) for p in ordered]
  points=[points[j] for j in mapping];curr=ring(points);bridge(prev,curr);prev=curr
 return prev

arm_sections=[(.220,0,1.003,.064,.055),(.245,-.002,1.003,.061,.053),(.280,-.003,1.003,.054,.049),(.315,-.002,1.003,.049,.044),(.350,0,1.003,.041,.038),(.375,.003,1.003,.035,.033),(.390,.005,1.003,.034,.033),(.405,.004,1.003,.037,.033),(.430,.002,1.003,.042,.036),(.462,0,1.003,.041,.032),(.493,-.001,1.003,.036,.029),(.525,-.001,1.003,.030,.026),(.557,0,1.003,.026,.022),(.585,0,1.003,.025,.020)]
arm_sections=sorted(arm_sections+[((a[0]+b[0])/2,*lerp_profile(arm_sections,(a[0]+b[0])/2)) for a,b in zip(arm_sections,arm_sections[1:])])
def finger(root,centers,sign,axis='X'):
 prev=root;mapping=None
 for k,(x,y,z,rad1,rad2) in enumerate(centers):
  if axis=='X':pp=[(sign*x,y+rad1*math.cos(math.tau*j/len(root)),z+rad2*math.sin(math.tau*j/len(root))) for j in range(len(root))]
  else:pp=[(sign*(x+rad1*math.cos(math.tau*j/len(root))),y,z+rad2*math.sin(math.tau*j/len(root))) for j in range(len(root))]
  if mapping is None:
   q=fit(pp,root);mapping=[min(range(len(pp)),key=lambda j:(Vector(p)-Vector(pp[j])).length_squared) for p in q]
  curr=ring([pp[j] for j in mapping]);bridge(prev,curr);prev=curr
 x,y,z,_,_=centers[-1];cap(prev,(sign*x+sign*.001 if axis=='X' else sign*x,y-.001 if axis=='Y' else y,z))
def hand(wrist,sign):
 # Palm: paired quad grids and side strips; finger/web connections share edges.
 xs=[.595,.605,.616,.627,.638,.649,.660,.671,.680];yy=[-.044+.088*j/8 for j in range(9)];top=[];bottom=[]
 for i,x in enumerate(xs):
  t=i/8;top.append([]);bottom.append([])
  for j,y in enumerate(yy):
   width=.73+.27*math.sin(t*math.pi/2);yc=y*width
   zt=1.003+.020-.003*t+.002*math.cos(y/.044*math.pi/2)*math.sin(t*math.pi)
   zb=1.003-.020+.004*t
   top[i].append(vert((sign*x,yc,zt)));bottom[i].append(vert((sign*x,yc,zb)))
 for i in range(8):
  for j in range(8):
   face([top[i][j],top[i+1][j],top[i+1][j+1],top[i][j+1]])
   face([bottom[i][j+1],bottom[i+1][j+1],bottom[i+1][j],bottom[i][j]])
 mids={}
 for edge,j in [('thumb',0),('little',8)]:
  mids[edge]=[vert(tuple((Vector(V[top[i][j]])+Vector(V[bottom[i][j]]))*.5)) for i in range(9)]
  for i in range(8):
   if edge=='thumb' and 2<=i<5:continue
   face([top[i][j],top[i+1][j],mids[edge][i+1],mids[edge][i]])
   face([mids[edge][i],mids[edge][i+1],bottom[i+1][j],bottom[i][j]])
 wr=top[0]+[mids['little'][0]]+list(reversed(bottom[0]))+[mids['thumb'][0]]
 assert len(wr)==len(wrist)
 # Match the wrist circle to the new palm's rectangular/rounded outline.
 options=[]
 for rr in [wr,list(reversed(wr))]:
  for k in range(len(rr)):
   q=rr[k:]+rr[:k];options.append((sum((Vector(V[a])-Vector(V[b])).length_squared for a,b in zip(wrist,q)),q))
 bridge(wrist,min(options,key=lambda x:x[0])[1])
 frontmid=[mids['thumb'][-1]]+[vert(tuple((Vector(V[top[-1][j]])+Vector(V[bottom[-1][j]]))*.5)) for j in range(1,8)]+[mids['little'][-1]]
 ends=[.756,.778,.767,.743]
 for f in range(4):
  j=f*2;root=[top[-1][j],top[-1][j+1],top[-1][j+2],frontmid[j+2],bottom[-1][j+2],bottom[-1][j+1],bottom[-1][j],frontmid[j]];cy=(yy[j]+yy[j+2])/2;end=ends[f]
  centers=[]
  for t,r in [(0,.0105),(.10,.0095),(.25,.0102),(.31,.0098),(.48,.0087),(.62,.0093),(.70,.0088),(.88,.0072),(1,.0039)]:
   centers.append((.689+(end-.689)*t,cy*(1+.065*t),1.002-.003*t,r,r*.88))
  finger(root,centers,sign)
 root=[top[2][0],top[3][0],top[4][0],top[5][0],mids['thumb'][5],bottom[5][0],bottom[4][0],bottom[3][0],bottom[2][0],mids['thumb'][2]]
 centers=[(.631,-.050,1.001,.016,.014),(.638,-.059,.998,.014,.013),(.651,-.072,.993,.012,.011),(.661,-.083,.991,.011,.010),(.673,-.096,.990,.009,.008),(.680,-.104,.990,.0045,.005)]
 # Thumb rings lie across its dominant Y axis; opposed to the finger plane.
 finger(root,centers,sign,'Y')

for sign,hole in [(1,arm_holes[0]),(-1,arm_holes[1])]:
 loop=rect_loop(torso,*hole,N);assert len(loop)==20;wr=limb_from_loop(loop,arm_sections,'X',sign);hand(wr,sign)

# Pelvis branches through a shared saddle of quads, not Boolean unions.
crotch=[vert((0,.125*(1-2*j/8),.610-.032*math.sin(math.pi*j/8))) for j in range(1,8)]
right_root=[torso[0][j] for j in range(25)]+crotch
left_root=[torso[0][j%48] for j in range(24,49)]+list(reversed(crotch))
leg_sections=[(.569,.106,.006,.075,.091),(.540,.107,.004,.078,.091),(.510,.109,0,.079,.085),(.474,.112,-.003,.074,.077),(.438,.112,-.006,.070,.071),(.405,.112,-.009,.061,.064),(.381,.112,-.012,.053,.061),(.367,.112,-.014,.052,.060),(.351,.112,-.014,.053,.060),(.330,.112,-.005,.057,.062),(.301,.112,.003,.060,.063),(.270,.112,.005,.058,.062),(.238,.112,.008,.052,.055),(.208,.112,.009,.044,.047),(.180,.112,.010,.036,.037),(.156,.112,.011,.031,.032),(.134,.112,.012,.030,.032)]
def foot(ankle,sign):
 # Foot longitudinal cage with real ankle opening and five shared-edge toe roots.
 ys=[.114,.101,.086,.068,.054,.046,.038,.030,.022,.014,.006,-.002,-.010,-.018,-.026,-.045,-.068,-.087,-.104,-.121,-.135]
 g=[]
 for k,y in enumerate(ys):
  if y>.07:rx=.054*math.sqrt(max(.05,(.124-y)/.054));height=.054+(.114-y)*.70
  elif y>-.03:rx=.054;height=.105
  elif y>-.10:rx=.060+(abs(y)-.03)*.20;height=.088-(abs(y)-.03)*.35
  else:rx=.078;height=.054
  p=[]
  # 10 top/10 bottom spans, two spans per side: 24 boundary vertices.
  for j in range(11):
   u=-1+2*j/10;z=height*(.24+.76*max(0,1-u*u)**.55);p.append((sign*(.112+rx*u),y,z))
  p.append((sign*(.112+rx),y,height*.10))
  for j in range(11):
   u=1-2*j/10;arch=.005*math.exp(-((y+.035)/.040)**2)*max(0,(1-u)/2)**1.7;p.append((sign*(.112+rx*.91*u),y,arch))
  p.append((sign*(.112-rx),y,height*.10));g.append(ring(p))
 for k in range(len(ys)-1):
  for j in range(24):
   if 2<=j<8 and 4<=k<14:continue
   face([g[k][j],g[k][(j+1)%24],g[k+1][(j+1)%24],g[k+1][j]])
 cap(g[0],(sign*.112,.118,.034))
 hole=rect_loop(g,2,8,4,14,24);assert len(hole)==32
 # Match the ankle to the opening; no hidden overlapping foot/leg solids.
 options=[]
 for rr in [hole,list(reversed(hole))]:
  for k in range(32):
   q=rr[k:]+rr[:k];options.append((sum((Vector(V[a])-Vector(V[b])).length_squared for a,b in zip(ankle,q)),q))
 bridge(ankle,min(options,key=lambda a:a[0])[1])
 top=g[-1][:11];bottom=list(reversed(g[-1][12:23]));mid=[g[-1][23]]+[vert(tuple((Vector(V[top[j]])+Vector(V[bottom[j]]))*.5)) for j in range(1,10)]+[g[-1][11]]
 lengths=[.054,.058,.048,.037,.026]
 for f in range(5):
  j=f*2;root=[top[j],top[j+1],top[j+2],mid[j+2],bottom[j+2],bottom[j+1],bottom[j],mid[j]];cx=.112+.078*(-1+2*(j+1)/10);end=-.144-lengths[f];centers=[]
  for t,r in [(0,.014),(.15,.0135),(.32,.0138),(.48,.0125),(.64,.013),(.82,.0115),(1,.0055)]:
   r*=1-.07*f;centers.append((cx*(1+.025*t),-.144+(end+.144)*t,.017-.001*t,r,r*.9))
  finger(root,centers,sign,'Y')
for sign,root in [(1,right_root),(-1,left_root)]:foot(limb_from_loop(root,leg_sections,'Z',sign),sign)

# Entirely new head topology. Anatomical fields shape this cage; openings are
# rebuilt with concentric quad loops for lids, lips and ear contours.
HEAD_START=len(V);N=96
def head_z(z):return 1.282+(z-1.282)*((1.282-1.055)/(1.282-1.090))
hz=[1.090,1.097,1.104,1.111,1.118,1.125,1.132,1.139,1.1425,1.14425,1.146,1.153,1.160,1.167,1.174,1.181,1.188,1.195,1.202,1.209,1.216,1.225,1.231,1.237,1.243,1.249,1.254,1.260,1.265,1.270,1.274,1.278,1.280,1.2812]
hp=[(1.09,.059,.052,.008),(1.111,.089,.070,.010),(1.139,.107,.084,.008),(1.167,.118,.091,.007),(1.195,.118,.101,.008),(1.225,.111,.104,.013),(1.249,.101,.094,.014),(1.270,.066,.068,.016),(1.278,.030,.035,.016),(1.282,0,0,.016)]
def headpoint(a,z):
 rx,ry,cy=lerp_profile(hp,z)
 if z>1.231:
  t=min(1,(z-1.231)/.014);t=t*t*(3-2*t);section=math.sqrt(max(0,1-((z-1.210)/.072)**2));rx=rx*(1-t)+.116*section*t;ry=ry*(1-t)+.106*section*t;cy=cy*(1-t)+.016*t
 x=rx*math.sin(a);y=cy-ry*math.cos(a);front=max(0,math.cos(a))**5
 # Adult planes: jaw, cheekbone, lower cheek, orbital hollow, brow, nose and chin.
 y-=front*(.009*gaussian(abs(x),z,.071,1.163,.032,.022)+.005*gaussian(abs(x),z,.060,1.134,.043,.025))
 y+=front*.010*gaussian(abs(x),z,.049,1.176,.024,.019)
 y-=front*.009*gaussian(abs(x),z,.050,1.199,.034,.010)
 y-=front*(.016*gaussian(x,z,0,1.179,.017,.037)+.027*gaussian(x,z,0,1.151,.026,.018)+.013*gaussian(abs(x),z,.021,1.146,.011,.011))
 y+=front*.008*gaussian(abs(x),z,.019,1.142,.005,.0035)
 y-=front*(.007*gaussian(x,z,0,1.112,.036,.013)+.009*gaussian(x,z,0,1.100,.039,.012))
 return (0 if abs(x)<1e-10 else x,y,z)
head=[ring([headpoint(math.tau*j/N,z) for j in range(N)]) for z in hz]
eye_holes=[(2,12,hz.index(1.160),hz.index(1.195)),(-12,-2,hz.index(1.160),hz.index(1.195))];mouth_hole=(-10,10,2,5);ear_holes=[(20,28,hz.index(1.139),hz.index(1.195)),(68,76,hz.index(1.139),hz.index(1.195))]
nose_holes=[(2,4,hz.index(1.139),hz.index(1.146)),(-4,-2,hz.index(1.139),hz.index(1.146))]
holes=eye_holes+[mouth_hole]+ear_holes+nose_holes
for k in range(len(hz)-1):
 for j in range(N):
  if any(any(q%N==j for q in range(j0,j1)) and k0<=k<k1 for j0,j1,k0,k1 in holes):continue
  face([head[k][j],head[k][(j+1)%N],head[k+1][(j+1)%N],head[k+1][j]])
for j in range(48):
 face([torso[-1][j],torso[-1][(j+1)%48],head[0][(2*j+2)%96],head[0][2*j+1]])
 face([torso[-1][j],head[0][2*j+1],head[0][2*j]])
cap(head[-1],(0,.016,1.282))

def surface_y(x,z):
 rx=lerp_profile(hp,z)[0];a=math.asin(max(-.999,min(.999,x/rx)));return headpoint(a,z)[1]
for sign,hole in [(1,eye_holes[0]),(-1,eye_holes[1])]:
 boundary=rect_loop(head,*hole,N);M=len(boundary);cx=sign*.049;cz=1.177;cy=surface_y(cx,cz)+.007;eye_r=.0165
 # Anatomical inner/outer canthi and curved eyelids around an actual eyeball.
 def eye_ring(scale,depth=0):
  pp=[]
  for j in range(M):
   a=math.tau*j/M;dx=.0158*scale*math.cos(a);dz=(.0064 if math.sin(a)>0 else .0048)*scale*math.sin(a)+.0012*dx/.0158
   x=cx+sign*dx;z=cz+dz;y=cy-math.sqrt(max(.000004,eye_r**2-dx*dx-dz*dz))-depth
   pp.append((x,y,z))
  return pp
 aperture=fit(eye_ring(1),boundary);mapping=[min(range(M),key=lambda j:(Vector(p)-Vector(eye_ring(1)[j])).length_squared) for p in aperture]
 prev=boundary
 for t in [.25,.50,.72,.86,1.0]:
  pp=[]
  for j,(b,p) in enumerate(zip(boundary,aperture)):
   point=Vector(V[b]).lerp(Vector(p),t);point.y-=.0020*math.sin(math.pi*t);pp.append(point)
  curr=ring(pp);bridge(prev,curr);prev=curr
 inner=ring([Vector(p)+Vector((0,.0022,0)) for p in aperture]);bridge(prev,inner)
 # Closed socket behind the eyeball. The visible aperture remains natural.
 back=ring([(cx+(p.x-cx)*.75,cy+.014,cz+(p.z-cz)*.75) for p in map(Vector,aperture)]);bridge(inner,back);cap(back,(cx,cy+.017,cz))
for sign,hole in [(1,ear_holes[0]),(-1,ear_holes[1])]:
 boundary=rect_loop(head,*hole,N);M=len(boundary);prev=boundary
 def ear_surface(y,z):
  rx,ry,cy=lerp_profile(hp,z);return rx*math.sqrt(max(.01,1-((y-cy)/ry)**2))
 target=[]
 for j in range(M):
  a=math.tau*j/M;y=.006+.019*math.cos(a)*(1+.08*math.sin(a));z=1.167+.0265*math.sin(a);target.append((sign*(ear_surface(y,z)+.0015),y,z))
 target=fit(target,boundary)
 for t in [.15,.40,.70,1.0]:
  pp=[]
  for b,p in zip(boundary,target):
   q=Vector(V[b]).lerp(Vector(p),t);q.x=sign*(ear_surface(q.y,q.z)+.0015*t*t);pp.append(q)
  curr=ring(pp);bridge(prev,curr);prev=curr
 for scale,lift in [(.85,.014),(.69,.011),(.53,.003),(.28,.002)]:
  pp=[]
  for p in target:
   y=.006+(p[1]-.006)*scale;z=1.167+(p[2]-1.167)*scale
   relief=0 if scale>.6 else .004*gaussian(y,z,.009,1.173,.005,.008)+.003*gaussian(y,z,-.003,1.158,.004,.005)
   pp.append((sign*(ear_surface(y,z)+lift+relief),y,z))
  curr=ring(pp);bridge(prev,curr);prev=curr
 cap(prev,(sign*(ear_surface(.004,1.163)+.003),.004,1.163))

darkverts=[]
for sign,hole in [(1,nose_holes[0]),(-1,nose_holes[1])]:
 boundary=rect_loop(head,*hole,N);M=len(boundary);cx=sign*.0205;cz=1.1425;pp=[]
 for j in range(M):
  a=math.tau*j/M;x=cx+sign*.0045*math.cos(a);z=cz+.0019*math.sin(a);pp.append((x,surface_y(x,z)+.0006,z))
 aperture=fit(pp,boundary);prev=boundary
 for t in [.30,.65,1.0]:
  curr=ring([Vector(V[b]).lerp(Vector(p),t) for b,p in zip(boundary,aperture)]);bridge(prev,curr);prev=curr
 inner=ring([(cx+(p[0]-cx)*.65,p[1]+.006,cz+(p[2]-cz)*.65) for p in aperture]);bridge(prev,inner);darkverts.extend(inner);begin=len(V);cap(inner,(cx,surface_y(cx,cz)+.008,cz));darkverts.extend(range(begin,len(V)))

boundary=rect_loop(head,*mouth_hole,N);M=len(boundary)
def lip_points(rx,rz,depth):
 pp=[]
 for j in range(M):
  a=math.tau*j/M;x=rx*math.cos(a);smile=.003*(abs(x)/rx)**1.8
  z=1.116+smile+rz*math.sin(a)
  if math.sin(a)>0:z-=.0008*math.exp(-(x/.007)**2)
  pp.append((x,surface_y(x,z)-depth,z))
 return pp
aperture=fit(lip_points(.040,.0035,.0018),boundary);mapping=[min(range(M),key=lambda j:(Vector(p)-Vector(lip_points(.040,.0035,.0018)[j])).length_squared) for p in aperture]
prev=boundary
for t in [.25,.5,.75,1.0]:
 curr=ring([Vector(V[b]).lerp(Vector(p),t)+Vector((0,-.0014*math.sin(t*math.pi),0)) for b,p in zip(boundary,aperture)]);bridge(prev,curr);prev=curr
for rx,rz,depth in [(.038,.0011,-.0001),(.035,.0006,-.0030)]:
 pp=lip_points(rx,rz,depth);curr=ring([pp[j] for j in mapping]);bridge(prev,curr);prev=curr
cap(prev,(0,surface_y(0,1.116)+.004,1.116))
for i in range(HEAD_START,len(V)):
 x,y,z=V[i];V[i]=(x,y,head_z(z))

me=bpy.data.meshes.new('HNV3_Body_QuadCage');me.from_pydata(V,[],F);me.update();o=bpy.data.objects.new('HNV3_Body',me);collections['BODY'].objects.link(o)
nostril_attr=me.attributes.new(name='NostrilInterior',type='FLOAT',domain='POINT')
for idx in darkverts:nostril_attr.data[idx].value=1
bm=bmesh.new();bm.from_mesh(me);unused=[v for v in bm.verts if not v.link_faces];bmesh.ops.delete(bm,geom=unused,context='VERTS')
# Enforce exact bilateral symmetry on the new cage, without Boolean geometry.
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(1,0,0),clear_inner=True)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
for q in s.objects:q.select_set(False)
o.select_set(True);bpy.context.view_layer.objects.active=o
mi=o.modifiers.new('BilateralBodyConstruction','MIRROR');mi.merge_threshold=1e-6;bpy.ops.object.modifier_apply(modifier=mi.name)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));nm=sum(not e.is_manifold for e in bm.edges);bm.to_mesh(me);bm.free()
for p in me.polygons:p.use_smooth=True
skin=bpy.data.materials.new('HNV3_NeutralSkin');skin.use_nodes=True;skin.diffuse_color=(.45,.265,.185,1)
p=next(n for n in skin.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.45,.265,.185,1);p.inputs['Roughness'].default_value=.68;p.inputs['Specular IOR Level'].default_value=.23;p.inputs['Subsurface Weight'].default_value=.045
attr=me.color_attributes.new(name='SkinRegions',type='FLOAT_COLOR',domain='POINT')
for v in me.vertices:
 x,y,z=v.co;red=0
 if z>1.055:z=1.282+(z-1.282)/((1.282-1.055)/(1.282-1.090))
 if y<0 and z>1.09:red=.020*max(gaussian(abs(x),z,.074,1.160,.032,.021),gaussian(x,z,0,1.151,.021,.015))
 col=(.45+red,.265-red*.30,.185-red*.18,1)
 if y<-.075 and 1.111<z<1.124 and abs(x)<.043:
  w=math.exp(-((z-(1.116+.005*(abs(x)/.04)**1.8))/.0028)**2)*.24
  col=tuple(col[i]*(1-w)+(.40,.18,.13,1)[i]*w for i in range(4))
 if me.attributes['NostrilInterior'].data[v.index].value>.5:col=(.052,.030,.021,1)
 attr.data[v.index].color=col
node=skin.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='SkinRegions';skin.node_tree.links.new(node.outputs['Color'],p.inputs['Base Color']);me.materials.append(skin)

# Separate anatomically seated eyeballs, no pasted discs or eye planes.
for sign,side in [(1,'L'),(-1,'R')]:
 bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=28,radius=.0165,location=(sign*.049,surface_y(sign*.049,1.177)+.007,head_z(1.177)));eye=bpy.context.object;eye.name='HNV3_Eyeball_'+side
 for c in list(eye.users_collection):c.objects.unlink(eye)
 collections['EYES'].objects.link(eye)
 colors=eye.data.color_attributes.new(name='EyeColor',type='FLOAT_COLOR',domain='POINT')
 for v in eye.data.vertices:
  x,y,z=v.co;r=math.sqrt(x*x+z*z)
  if y<0 and r<.0032:color=(.013,.010,.007,1)
  elif y<0 and r<.0066:
   mix=(r-.0032)/.0034;color=(.16+.07*mix,.073+.035*mix,.021+.018*mix,1)
  else:color=(.72,.69,.62,1)
  colors.data[v.index].color=color
 for pp in eye.data.polygons:pp.use_smooth=True
 em=bpy.data.materials.get('HNV3_Eyes')
 if not em:
  em=bpy.data.materials.new('HNV3_Eyes');em.use_nodes=True;ep=next(n for n in em.node_tree.nodes if n.type=='BSDF_PRINCIPLED');ep.inputs['Roughness'].default_value=.35;ep.inputs['Specular IOR Level'].default_value=.3;nd=em.node_tree.nodes.new('ShaderNodeVertexColor');nd.layer_name='EyeColor';em.node_tree.links.new(nd.outputs['Color'],ep.inputs['Base Color'])
 eye.data.materials.append(em)

def studio_object(name,typ,data):
 ob=bpy.data.objects.new(name,data);collections['STUDIO'].objects.link(ob);return ob
cam=studio_object('HNV3_ReviewCamera','CAMERA',bpy.data.cameras.new('HNV3_ReviewCamera'));cam.location=(2,-4,1.7);cam.rotation_euler=(Vector((0,0,.64))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.8;s.camera=cam
for name,loc,power,size in [('Key',(-2,-3,3.8),240,3),('Fill',(2,-1,2.4),100,2.6),('Rim',(0,2,3),180,2.5)]:
 d=bpy.data.lights.new('HNV3_'+name,'AREA');d.energy=power;d.shape='DISK';d.size=size;light=studio_object('HNV3_'+name,'LIGHT',d);light.location=loc;light.rotation_euler=(Vector((0,0,.8))-light.location).to_track_quat('-Z','Y').to_euler()
world=bpy.data.worlds.new('HNV3_StudioWorld');world.use_nodes=True;next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Color'].default_value=(.16,.18,.20,1);next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.35;s.world=world
floor_me=bpy.data.meshes.new('HNV3_Floor');floor_me.from_pydata([(-20,-20,-.001),(20,-20,-.001),(20,20,-.001),(-20,20,-.001)],[],[(0,1,2,3)]);floor=studio_object('HNV3_Floor','MESH',floor_me);fm=bpy.data.materials.new('HNV3_StudioGround');fm.use_nodes=True;next(n for n in fm.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].default_value=(.125,.14,.15,1);floor_me.materials.append(fm)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=1200;s.render.resolution_percentage=100
o['Construction']='New explicitly joined quad patches; no V1/V2 vertices, Boolean union, remesh or subdivision.';o['Planned_total_height_with_future_hair_m']=1.32;o['Current_skin_height_m']=1.282
(BASE/'Review/V3/Construction.json').write_text(json.dumps({'regions':regions,'new_body_vertices':len(me.vertices),'new_body_faces':len(me.polygons),'nonmanifold_edges':nm,'unused_construction_vertices_removed':len(unused),'hair_allowance_m':.038},indent=2))
stage=BASE/'Source/StagesV3/Hobbit_NPC_Base_V3_07_NoseEarContours.blend';assert not stage.exists();bpy.data.libraries.write(str(stage),{s});bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V3_Body.blend'),{s})
print(json.dumps({'body_vertices':len(me.vertices),'faces':len(me.polygons),'nonmanifold':nm,'height':max(v.co.z for v in me.vertices),'new_scene':s.name}))
