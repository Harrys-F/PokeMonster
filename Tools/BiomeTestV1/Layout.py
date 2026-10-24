"""Biome sandbox coordinates in centimetres: u screen-right, v screen-up; existing yaw -45 camera."""
import math
C=math.sqrt(.5)
EXTENT=5200
CENTERS={'Wiese':(-2700,2700),'Wasser':(2700,2700),'Felsen':(-2700,-2700),'Wald':(2700,-2700)}
# Explicit walkable switchbacks, ~90 m run for a 15 m rise. Screen-space route, not a new navigation system.
PLATEAU_APPROACH=[(-900,-1000,0),(-1080,-2100,210),(-950,-3300,420),(-1050,-4400,630),(-1700,-4400,750),(-1750,-2750,1040),(-1700,-1100,1330),(-2450,-1100,1500),(-2900,-1800,1500)]
CAVE_ROUTE=[(-900,-1000),(-650,-2000),(-650,-4750),(-2900,-4750),(-2900,-3750),(-2900,-3450)]
ROUTES=[[(0,0),(-2700,2700),(-3700,3700)],[(0,0),(1600,1600),(1900,2800),(1900,3650),(2700,4100),(3800,4100)],[(0,0)]+[(u,v)for u,v,z in PLATEAU_APPROACH],CAVE_ROUTE,[(0,0),(1500,-1500),(2800,-2800),(3000,-2800),(3000,-3500)]]
def world(u,v,z=0):return ((u+v)*C,(u-v)*C,z)
def local(x,y):return ((x+y)*C,(x-y)*C)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def sd(u,v,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((u-a[0])*dx+(v-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(u-a[0]-t*dx,v-a[1]-t*dy)
def path_distance(u,v):return min(sd(u,v,a,b)for path in ROUTES for a,b in zip(path,path[1:]))
def stream(u,v):return 3280+110*math.sin((v-3000)/850)
def height(u,v):
 h=3*math.sin(u/450)*math.sin(v/530)
 # Pond and stream have a real continuous lowered bed; water is at -20cm.
 if u>800 and v>700:
  q=math.hypot((u-3200)/1000,(v-2850)/760)
  pond=-125*smooth((1.13-q)/.43)-275*smooth((.78-q)/.25)
  channel=-100*smooth((245-abs(u-stream(u,v)))/180) if v>3000 else 0
  h=min(h,pond,channel)
 # Fifteen-metre rocky table with an explicitly graded approach; cliff edges remain impassable.
 if u<-500 and v<-500:
  edge=max(abs(u+3000)-850,abs(v+2250)-1050)
  h=max(h,1500*(1-smooth(edge/330)))
  candidates=[]
  for a,b in zip(PLATEAU_APPROACH,PLATEAU_APPROACH[1:]):
   dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((u-a[0])*dx+(v-a[1])*dy)/(dx*dx+dy*dy)))
   candidates.append((math.hypot(u-a[0]-t*dx,v-a[1]-t*dy),a[2]+(b[2]-a[2])*t))
  d,z=min(candidates);w=1-smooth((d-145)/125)
  h=h*(1-w)+z*w
  # Open approach pocket at the real cliff foot; the existing masked doorway relocates inside.
  pocket=(1-smooth((abs(u+2900)-230)/100))*(1-smooth((v+3330)/110))
  h*=1-pocket
 # Raised frame only beyond the explorable surface; visible rocks/hedges mark the limit.
 border=max(abs(u),abs(v))-4920
 if border>0:h+=80*smooth(border/280)
 return h

def vertex_colour(u,v):
 noise=16*math.sin(u/105)*math.sin(v/83)+11*math.sin((u+v)/180)
 path=1-smooth((path_distance(u,v)-(138+noise))/95)
 path=max(path,1-smooth((math.hypot(u,v)-400)/120))
 forest=smooth((u-600)/750)*smooth((-v-600)/750)
 rock=smooth((-u-600)/750)*smooth((-v-600)/750)
 bank=0
 if u>1000 and v>900:
  q=math.hypot((u-3200)/1000,(v-2850)/760)
  bank=max(1-smooth((q-1.07)/.18),1-smooth((abs(u-stream(u,v))-190)/120)if v>3000 else 0)
 return (path*(1-bank*.65),forest,rock*.80,bank*.72)
