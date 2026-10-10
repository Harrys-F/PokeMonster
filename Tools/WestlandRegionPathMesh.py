"""Ground-conforming road geometry. Clip ribbons to native terrain triangles.
This avoids triangular terrain intersections without raising roads above the feet.
All coordinates are authoring metres; no engine/runtime dependency.
"""
import math
import WestlandRegionLayout as L

def terrain_height(e,n):
 e0=math.floor((e+500)/2)*2-500;n0=math.floor((n+400)/2)*2-400;u=(e-e0)/2;v=(n-n0)/2
 a=L.height(e0,n0);b=L.height(e0+2,n0);c=L.height(e0+2,n0+2);d=L.height(e0,n0+2)
 return a+(b-a)*u+(c-b)*v if v<=u else a+(c-d)*u+(d-a)*v

def elevation(e,n):
 if abs(n+50)<=2 and abs(e-L.river(-50))<=14:return -.020
 if abs(n+235)<=1.25 and abs(e-L.river(-235))<=8:return -.220
 return terrain_height(e,n)+.012

def cross(a,b,p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
def clip(poly,quad):
 for a,b in zip(quad,quad[1:]+quad[:1]):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   cp=cross(a,b,p);cq=cross(a,b,q);pi=cp>=-1e-8;qi=cq>=-1e-8
   if pi:out.append(p)
   if pi!=qi:
    t=cp/(cp-cq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  poly=out
  if len(poly)<3:return []
 return poly

def build(points,width):
 pts=L.sample(points,spacing=1);vs=[];uv=[];tri=[];count=len(pts)
 for i in range(count-1):
  a=pts[i];b=pts[i+1];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
  if length<1e-5:continue
  # Adjacent ribbon endpoints share their bisector, avoiding triangular gaps.
  edges=[]
  for j,p in [(i,a),(i+1,b)]:
   q=pts[max(0,j-1)];r=pts[min(count-1,j+1)];sx=r[0]-q[0];sy=r[1]-q[1];d=max(.001,math.hypot(sx,sy));w=width/2*(1+.035*math.sin(j*.17));edges.append(((p[0]-sy/d*w,p[1]+sx/d*w),(p[0]+sy/d*w,p[1]-sx/d*w)))
  quad=[edges[0][0],edges[0][1],edges[1][1],edges[1][0]]
  e0=math.floor((min(p[0] for p in quad)+500)/2)*2-500;e1=max(p[0] for p in quad);n0=math.floor((min(p[1] for p in quad)+400)/2)*2-400;n1=max(p[1] for p in quad)
  for ei in range(math.ceil((e1-e0)/2)):
   for ni in range(math.ceil((n1-n0)/2)):
    e=e0+ei*2;n=n0+ni*2;cell=[(e,n),(e,n+2),(e+2,n+2),(e+2,n)]
    for t in [(cell[0],cell[1],cell[2]),(cell[0],cell[2],cell[3])]:
     poly=clip(list(t),quad)
     if len(poly)<3:continue
     start=len(vs)
     for ee,nn in poly:
      vs.append(L.world(ee,nn,elevation(ee,nn)));along=max(0,min(1,((ee-a[0])*dx+(nn-a[1])*dy)/(length*length)));uu=(i+along)/(count-1);side=(-dy*(ee-a[0])+dx*(nn-a[1]))/length;uv.append((uu,max(0,min(1,.5-side/width))))
     for j in range(1,len(poly)-1):
      if abs(cross(poly[0],poly[j],poly[j+1]))>1e-8:tri.append((start,start+j,start+j+1))
 return vs,tri,uv
