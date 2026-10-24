"""Biome sandbox coordinates in centimetres: u screen-right, v screen-up; existing yaw -45 camera."""
import math
C=math.sqrt(.5)
EXTENT=5200
CENTERS={'Wiese':(-2700,2700),'Wasser':(2700,2700),'Felsen':(-2700,-2700),'Wald':(2700,-2700)}
ROUTES=[[(0,0),(-2700,2700),(-3700,3700)],[(0,0),(1600,1600),(1900,2800),(1900,3650),(2700,4100),(3800,4100)],[(0,0),(-1100,-1100),(-1200,-1800),(-2200,-1800),(-2800,-1800)],[(-1200,-1800),(-1200,-2850),(-2700,-2850),(-2700,-4200)],[(0,0),(1500,-1500),(2800,-2800),(3000,-2800),(3000,-3500)]]
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
  pond=-125*smooth((1.13-q)/.43)
  channel=-100*smooth((245-abs(u-stream(u,v)))/180) if v>3000 else 0
  h=min(h,pond,channel)
 # Actual 3m rock table, steep edges and one generous approach slope.
 if u<-500 and v<-500:
  edge=max(abs(u+2800)-720,abs(v+1800)-570)
  hill=300*(1-smooth(edge/180))
  ramp=300*smooth((-1200-u)/850)*(1-smooth((abs(v+1800)-210)/110)) if -2140<u<-1200 else 0
  h=max(h,hill,ramp)
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
 bank=1-smooth((abs(height(u,v)+20)-15)/60) if u>1000 and v>900 else 0
 return (path*(1-bank*.65),forest,rock*.80,bank*.72)
