"""Own deterministic forest composition. Fab data is referenced, never copied or generated."""
from pathlib import Path
import random,math,json,struct,zlib
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/EuropeanBeechV1';A=R/'Art/World/EuropeanBeechV1';A.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
BOUNDS=(-7500,4500,3000,15000);CLEAR=(-400,8500,1100);SEED=117031
routes=[ [(-3300,2350),(-3300,2800),(-3300,3400),(-2800,4300),(-2400,5200),(-3600,6500),(-2600,7800),(-400,8500),(700,10000),(-700,11300),(-2800,11200),(-4400,10000),(-4700,8200),(-3900,6800),(-3600,6500)], [(-2800,11200),(-4200,12000),(-5500,12100)] ]
def smooth(points):
 out=[];ext=[points[0]]+points+[points[-1]]
 for i in range(1,len(ext)-2):
  p0,p1,p2,p3=ext[i-1:i+3];n=max(3,int(math.dist(p1,p2)/65))
  for j in range(n):
   t=j/n;out.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t)for k in [0,1]))
 out.append(points[-1]);return out
paths=[smooth(p)for p in routes];segments=[(a,b)for p in paths for a,b in zip(p,p[1:])]
def sd(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def road(x,y):return min(sd(x,y,a,b)for a,b in segments)
def zone(x,y):return 'Edge'if y<4900 else('West'if x<-2400 else'Inner')
rng=random.Random(SEED);objects=[];large=[]
def place(family,mesh,n,spacing,road_gap,scale=(.9,1.1),clear_gap=0,shadow=True):
 pts=[]
 for attempt in range(100000):
  if len(pts)==n:break
  x,y=rng.uniform(-7000,4000),rng.uniform(3550,14500)
  if family in ['Fern','Moss','Grass'] and rng.random()<.75:
   center=rng.choice([(-3400,5100),(-5100,9300),(-1800,12500),(1900,6200),(-400,8700),(-5900,12500)]);x,y=rng.gauss(center[0],650),rng.gauss(center[1],850)
  if not -7000<x<4000 or not 3550<y<14500:continue
  if road(x,y)<road_gap:continue
  if clear_gap and math.hypot(x-CLEAR[0],y-CLEAR[1])<clear_gap:continue
  if any(math.hypot(x-u,y-v)<spacing for u,v in pts):continue
  if family in ['Canopy','UnderTree']and any(math.hypot(x-u,y-v)<600 for u,v in large):continue
  if family not in ['Canopy','UnderTree']and any(math.hypot(x-u,y-v)<100 for u,v in large):continue
  sc=rng.uniform(*scale);row={'family':family,'mesh':mesh,'zone':zone(x,y),'position':[round(x,3),round(y,3),.2],'scale':[sc,sc,sc*rng.uniform(.96,1.04)],'yaw':rng.uniform(0,360),'shadow':shadow};objects.append(row);pts.append((x,y))
  if family in ['Canopy','UnderTree']:large.append((x,y))
 assert len(pts)==n,(family,mesh,len(pts),n)
F='/Game/Fab/EuropeanBeech/Geometry/SimpleWind/'
for i,n in [(1,4),(2,4),(4,26),(5,32),(6,40),(7,40),(8,45)]:place('Canopy'if i!=8 else'UnderTree',F+'SM_EuropeanBeech_Forest_'+str(i).zfill(2),n,550,410,clear_gap=1700 if i in [1,2]else 1100)
place('Canopy',F+'SM_EuropeanBeech_Field_01',3,1700,750,(.85,1.0),1800)
for i in [1,2,3,4]:place('Sapling',F+'SM_EuropeanBeech_Sapling_'+str(i).zfill(2),34,210,420,(.85,1.15),850)
for i in [1,2,3,4]:place('Seedling',F+'SM_EuropeanBeech_Seedling_'+str(i).zfill(2),55,110,230,(.85,1.15),650,False)
for suffix in ['A','B']:place('Fern','/Game/Environment/VisualV2WorldArtV7/Meshes/SM_WA7_Fern_'+suffix,400,65,190,(.75,1.15),0,False)
place('Moss','/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_MossCushion',260,65,180,(.7,1.25),0,False)
place('Grass','/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_GrassWoodland',850,55,185,(.6,1.05),0,False)
# Actual existing branches/stumps, concentrated away from the branch path in the deadwood pocket.
for i in range(28):
 x,y=rng.uniform(-6550,-4700),rng.uniform(11600,13500)
 if road(x,y)<260:continue
 objects.append({'family':'Deadwood','mesh':'/Game/Environment/HealingHouse/ArtV4/Meshes/SM_HH4_FallenBranch','zone':'Deadwood','position':[x,y,.2],'scale':[rng.uniform(1.5,3),rng.uniform(1.5,3),rng.uniform(1.2,1.8)],'yaw':rng.uniform(0,360),'shadow':True})
for i in range(9):objects.append({'family':'Stump','mesh':'/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Stump_'+('A'if i%2 else'B'),'zone':'Deadwood','position':[-6350+(i%3)*600,12500+(i//3)*480,.2],'scale':[.8,.8,.8],'yaw':rng.uniform(0,360),'shadow':True})
plan={'version':1,'seed':SEED,'bounds_cm':BOUNDS,'ground_top_cm':.2,'clearing_cm':CLEAR,'path_width_cm':280,'paths_cm':paths,'objects':objects,'no_spawns_npcs_quests':True}
(D/'Layout.json').write_text(json.dumps(plan,indent=2));(R/'Tools/EuropeanBeechV1/Layout.json').write_text(json.dumps(plan,indent=2))
# Numeric authoring mask: soft 2.8m path + clearing, no external image library required.
N=1024;buf=bytearray(N*N*3);step=12000/N
for path in paths:
 for x,y in path:
  px,py=(x-BOUNDS[0])/step,(y-BOUNDS[2])/step
  for yy in range(max(0,int(py-19)),min(N,int(py+20))):
   for xx in range(max(0,int(px-19)),min(N,int(px+20))):
    distance=math.hypot((xx+.5-px)*step,(yy+.5-py)*step);edge=140+9*math.sin(xx*.7+yy*.37);v=int(255*max(0,min(1,(edge+55-distance)/55)));index=(yy*N+xx)*3;buf[index]=max(buf[index],v)
for yy in range(N):
 for xx in range(N):
  x,y=BOUNDS[0]+(xx+.5)*step,BOUNDS[2]+(yy+.5)*step;v=int(255*max(0,min(1,(800-math.hypot(x-CLEAR[0],y-CLEAR[1]))/250)));buf[(yy*N+xx)*3+1]=v
raw=b''.join(b'\0'+bytes(buf[y*N*3:(y+1)*N*3])for y in range(N))
def chunk(t,v):return struct.pack('>I',len(v))+t+v+struct.pack('>I',zlib.crc32(t+v)&0xffffffff)
(A/'PathMask.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',N,N,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))
print('Own layout:',len(objects),'instances; paths',sum(len(p)for p in paths),'samples')
