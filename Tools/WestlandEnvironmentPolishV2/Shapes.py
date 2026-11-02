"""Bounded edits to the existing terrain/river; protected routes/pads and water habitats stay fixed."""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import WestlandRegionLayout as L
pathgrid={}
for _,ps,w in L.PATHS:
 for e,n in L.sample(ps,spacing=2):pathgrid.setdefault((int(e//10),int(n//10)),[]).append((e,n,w))
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def route_distance(e,n):
 return min([math.hypot(e-u,n-v)-w*.5 for gx in range(int(e//10)-2,int(e//10)+3)for gy in range(int(n//10)-2,int(n//10)+3)for u,v,w in pathgrid.get((gx,gy),[])]or[999])
def protection(e,n):
 w=smooth(4.5,13,route_distance(e,n))
 for pe,pn,pz,hx,hy in L.PAD:
  d=math.hypot(max(0,abs(e-pe)-hx),max(0,abs(n-pn)-hy));w*=smooth(4,15,d)
 return w

def water_fade(n):
 # Preserve bridge seats, waterfall reach and all three existing short fish zones.
 w=1
 for center,inside,outside in [(-50,12,23),(-235,13,25),(175,22,35),(-130,24,37),(25,24,37),(125,24,37)]:w*=smooth(inside,outside,abs(n-center))
 return w

def center(n):return L.river(n)+.45*math.sin(n/19)*water_fade(n)
def halfwidth(n):return(7+.9*math.sin(n/19))*.5*(1+water_fade(n)*(.11*math.sin(n/31)+.06*math.sin(n/13)))
def delta(e,n,z):
 w=protection(e,n)
 if w<.00001:return 0
 dist=abs(e-L.river(n));channel=smooth(5,15,dist)
 # Natural small undulations; the village, routes and original plateau tops are protected.
 h=(1.05*math.sin(e/27)*math.cos(n/39)+.48*math.sin((e+n)/14)+.27*math.cos((e-2*n)/11))*w*channel
 old=10*math.exp(-(((e+310)/75)**4+((n-205)/80)**4))+18*math.exp(-(((e+45)/88)**4+((n-235)/60)**4))+12*math.exp(-(((e-230)/120)**4+((n-205)/90)**4))
 new=10*math.exp(-(((e+310)/83)**2+((n-205)/86)**2))+18*math.exp(-(((e+45)/95)**2+((n-235)/72)**2))+12*math.exp(-(((e-230)/130)**2+((n-205)/99)**2))
 h+=max(-2.6,min(2.6,(new-old)*.5))*w*channel
 ridge=L.backdrop_ridge(e,n);h+=ridge*(-.18+.11*math.sin(e/37+n/51)+.06*math.cos(e/63-n/31))*w
 # Visible shoreline remains continuous; asymmetric, less uniform banks outside protected reaches.
 wf=water_fade(n)*w;d=abs(e-center(n));bank=(1-smooth(5.5,13,d))*smooth(3.7,5.2,d)
 h+=wf*bank*(.24*math.sin(n/12)+.16*math.cos(n/7+(1 if e>center(n)else 0)))
 h-=wf*(1-smooth(1.8,3.4,d))*(.12+.10*(.5+.5*math.sin(n/24)))
 return h

def bank_height(e,n,z):
 # The old upper river plane could stand above the surrounding lowland.
 # Add a bounded, smooth containment bank, outside the unchanged fish corridor.
 d=abs(e-center(n));w=protection(e,n)*smooth(3.9,6.2,d)*(1-smooth(8,20,d))
 return z+(max(z,L.water(n)+.25)-z)*w
