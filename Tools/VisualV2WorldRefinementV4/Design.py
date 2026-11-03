"""Shared authoring coordinates and protected existing routes, never runtime gameplay code."""
import math,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];paths=json.loads((R/'Tools/VisualV2FabAssetTrialV1/ExistingPaths.json').read_text());segments=[(a,b)for p in paths.values()for a,b in zip(p,p[1:])]
def sat(x):return min(1,max(0,x))
def smooth(x):x=sat(x);return x*x*(3-2*x)
def seg(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=sat(((x-a[0])*dx+(y-a[1])*dy)/max(1,dx*dx+dy*dy));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def pd(x,y):return min(seg(x,y,a,b)for a,b in segments)
def forest(x,y):return max(sat(1-((x-cx)/rx)**2-((y-cy)/ry)**2)for cx,cy,rx,ry in [(-4900,1700,1400,1350),(-2700,2300,1450,750),(1500,1400,1250,1450),(1850,-750,800,1000)])
def pondr(x,y):return math.hypot((x-720)/900,(y+1800)/650)
def shore(a):return .969+.016*math.sin(3*a+.6)+.011*math.sin(7*a-1.2)
def oldheight(x,y):return max(h*(1-smooth((math.hypot(x-cx,y-cy)/r-.45)/.55))for cx,cy,h,r in[(-1120,620,20,350),(-900,800,40,350),(-620,1010,60,450),(-5500,-2750,42,380),(2300,2400,65,400),(2300,-2800,38,370)])
pads=[(-3100,500,780,760),(-2750,-1020,650,500),(1080,900,460,470)]
functional=[]
p=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4/SceneBefore.json'
if p.exists():
 for a in json.loads(p.read_text())['actors'].values():
  if a['class'].startswith('/Script/PokeMonster.')and'Visual'not in a['class']and'Building'not in a['class']:functional.append(a['transform'][0][:2])
def delta(x,y):
 mask=smooth((pd(x,y)-165)/440)
 for cx,cy,rx,ry in pads:mask*=smooth((math.sqrt(((x-cx)/rx)**2+((y-cy)/ry)**2)-1)/.48)
 for cx,cy in functional:mask*=smooth((math.hypot(x-cx,y-cy)-135)/230)
 water=min(seg(x,y,(-910,-320),(1100,-320)),seg(x,y,(720,-320),(720,-680)));mask*=smooth((water-190)/260)*smooth((pondr(x,y)-1.13)/.28)
 hills=[(-5400,1950,145,1000,950),(-5000,-2550,100,1100,650),(-2200,2450,175,1150,650),(1950,1750,185,1100,1100),(2250,-800,125,750,1050),(2300,-2700,145,850,700),(-920,1100,90,850,700)]
 base=max(h*math.exp(-2.4*(((x-cx)/rx)**2+((y-cy)/ry)**2))for cx,cy,h,rx,ry in hills)
 return mask*(base*(.87+.13*math.sin(x*.0017+y*.0023))+7*(1+math.sin(x*.010+math.sin(y*.006)))*(.6+.4*math.sin(y*.008)))
def height(x,y):return oldheight(x,y)+delta(x,y)
def bed(x,y,oldz):
 r=pondr(x,y)
 if r<1.16:
  a=math.atan2((y+1800)/650,(x-720)/900);rr=r/shore(a);deep=-420*(1-smooth((rr-.64)/.35));lip=7*math.exp(-((rr-1.035)/.048)**2)*( .6+.4*math.sin(a*5)**2);return deep+lip
 return oldz+delta(x,y)
