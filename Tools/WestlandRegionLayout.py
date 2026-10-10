"""Region V1 authoring coordinates: east/north in metres, Unreal centimetres.
No runtime imports or gameplay logic. The saved JSON is the reviewable source layout.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP='/Game/Maps/Dev_WestlandRegion'
ASSETS='/Game/Environment/WestlandRegion'
TAG='WestlandRegionV1'
C=math.sqrt(.5)
def world(e,n,z=0):return ((e+n)*C*100,(e-n)*C*100,z*100)
def en(x,y):return ((x+y)*C/100,(x-y)*C/100)
def river(n):return 25+35*math.sin((n+70)/150)+200*max(0,(-n-80)/220)
def water(n):
 if 165<=n<174.5:return 3+.5*(n-165)/9.5
 if 174.5<=n<185:return 7.0
 pts=[(-420,-8),(-250,-6),(-80,-4),(80,-1),(165,3),(185,7),(300,12),(420,15)]
 for (a,h),(b,k) in zip(pts,pts[1:]):
  if a<=n<=b:return h+(k-h)*(n-a)/(b-a)
 return -8 if n<pts[0][0] else 15
PLACES={'Hof':(-300,-220),'Dorf':(-220,-35),'Heilhaus':(-310,205),'Steinkreis':(-45,235),'Wildwiesen':(150,5),'Waldruinen':(225,205),'Muehle':(145,-230),'Ausgang':(380,170),'Lichtung':(280,80),'Aussicht':(-155,265),'Uferfund':(river(-145)+12,-145)}
MAIN=[(-300,-220),(-315,-180),(-295,-140),(-275,-95),(-240,-60),(-220,-35),(-175,-10),(-130,-20),(-80,-55),(river(-50)-18,-50),(river(-50)+18,-50),(75,-25),(125,10),(180,25),(205,80),(200,125),(225,175),(225,205),(280,215),(325,190),(380,170)]
PATHS=[('Hauptroute',MAIN,3.6),('Heilhauszugang',[(-220,-35),(-265,10),(-300,60),(-310,100),(-325,155),(-310,190)],3.4),('Nordrunde',[(-310,190),(-275,230),(-215,240),(-155,265),(-95,255),(-45,235),(-55,165),(-90,105),(-120,40),(-130,-20)],2.4),('Muehlenrunde',[(125,10),(175,-35),(195,-100),(180,-165),(145,-210),(153,-220),(153,-240),(153,-235),(river(-235)+12,-235),(river(-235)+8,-235),(river(-235)-8,-235),(river(-235)-12,-235),(-35,-245),(-125,-255),(-225,-245),(-300,-220)],2.5),('Waldpfad',[(225,205),(280,170),(280,80),(235,50),(180,25)],2.1),('Uferpfad',[(75,-25),(65,-90),(river(-145)+12,-145),(river(-180)+15,-180),(145,-210)],2.1)]
PAD=[]
def backdrop_ridge(e,n):
 d=max(0,abs(e)-430,abs(n)-330)
 bank=min(1,max(0,(abs(e-river(n))-7)/9));bank=bank*bank*(3-2*bank)
 return d*d*.022*(.85+.15*math.sin(e/45+n/72))*bank
def height(e,n):
 h=.7*math.sin(e/65)*math.cos(n/52)+.35*math.sin((e+n)/29)
 h+=10*math.exp(-(((e+310)/75)**4+((n-205)/80)**4))
 h+=18*math.exp(-(((e+45)/88)**4+((n-235)/60)**4))
 h+=12*math.exp(-(((e-230)/120)**4+((n-205)/90)**4))
 # River valley is truly lower than surrounding terraces.
 dist=abs(e-river(n));t=max(0,1-dist/14);t=t*t*(3-2*t)
 h=h*(1-t)+(water(n)-.8)*t
 for pe,pn,pz,hx,hy in PAD:
  d=math.hypot(max(0,abs(e-pe)-hx),max(0,abs(n-pn)-hy));f=max(0,1-d/9);f=f*f*(3-2*f)
  if f:h=h*(1-f)+pz*f
 dist=abs(e-river(n));carve=max(0,min(1,(7-dist)/3.5));carve=carve*carve*(3-2*carve)
 h=h*(1-carve)+(water(n)-.8)*carve
 # Dedicated bank landings: bridge ends stay level; channel under its deck stays open.
 de=abs(e-river(-235));dn=abs(n+235)
 if 7.0<de<21 and dn<8:
  f=min(1,(de-7)/.8)*max(0,min(1,(21-de)/4))*max(0,min(1,(8-dn)/4))
  f=f*f*(3-2*f);h=h*(1-f)-.2*f
 return h+backdrop_ridge(e,n)

def sample(points,spacing=1.5):
 # Catmull-Rom, then linear resampling by arc length.
 a=[points[0]]+points+[points[-1]];curve=[]
 for i in range(1,len(a)-2):
  p0,p1,p2,p3=a[i-1:i+3]
  steps=max(4,math.ceil(math.dist(p1,p2)/2))
  for j in range(steps):
   t=j/steps;curve.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in (0,1)))
 curve.append(points[-1]);out=[curve[0]]
 for a,b in zip(curve,curve[1:]):
  steps=max(1,math.ceil(math.dist(a,b)/spacing));out.extend(tuple(a[k]+(b[k]-a[k])*j/steps for k in (0,1)) for j in range(1,steps+1))
 return out

def configure_pads():
 PAD.clear();PAD.extend([(-310,205,10,9,10),(-45,235,18,12,12),(225,205,12,14,16),(-300,-220,0,11,9),(-220,-35,0,18,15),(145,-230,-.2,10,9),(river(-235)-12,-235,-.2,4,3),(380,170,4,8,10)])
 for b in buildings():PAD.append((*b['place'],b['z'],b['size'][1]/2+3,b['size'][0]/2+3))
def buildings():
 return [dict(id=i,place=(e,n),size=(d,w),z=z,yaw=-45+o,kind=k) for i,e,n,d,w,z,o,k in [
 ('Spielerhaus',-312,-220,8,6,0,0,'home'),('Obstschuppen',-283,-205,4,6,0,-8,'home'),
 ('Birkenhaus',-270,-72,8,6,0,8,'home'),('Brunnenhaus',-245,-5,6,6,0,-12,'home'),('Kraeuterhof',-205,8,8,8,0,10,'home'),('Gartenhaus',-175,-15,6,6,0,-10,'home'),('Westhof',-275,-15,6,8,0,5,'home'),('Nordhaus',-240,40,8,6,0,-15,'home'),('Werkstatt',-185,-75,8,8,0,7,'home'),('Gasthaus',-205,-42,8,8,0,-5,'inn'),('Wassermuehle',145,-230,8,6,-.2,0,'mill')]]
configure_pads()
if __name__=='__main__':
 r=ROOT/'Art/World/WestlandRegion';r.mkdir(parents=True,exist_ok=True)
 pts=sample(MAIN);length=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))
 data={'version':1,'map':MAP,'region_m':[800,600],'backdrop_margin_m':100,'coordinate_basis':'E=screen right; N=screen up; world yaw -45 unchanged','places_m':PLACES,'paths':[{'id':i,'points_m':p,'width_m':w} for i,p,w in PATHS],'buildings':buildings(),'main_route_m':length,'theoretical_walk_seconds_at_210':length/2.1,'seed':5100926,'terrain':'separate 100 m mesh tiles, 2 m surface grid; native GeometryScript; no gameplay rewrite'}
 (r/'WestlandRegion_V1.json').write_text(json.dumps(data,indent=2));print(length,length/2.1)
