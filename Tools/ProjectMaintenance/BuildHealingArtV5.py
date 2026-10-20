"""Own upholstered chair/cushion meshes, using the existing authoring helpers; no old source is modified."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
helper=(R/'Tools/ProjectMaintenance/BuildHealingArtV4.py').read_text().split('# Irregular, physically bevelled')[0].replace('HealingHouse_ArtV4.blend','HealingHouse_ArtV5.blend').replace("'SM_HH4_'","'SM_HH5_'")
exec(compile(helper,'existing_prop_authoring_helpers','exec'),globals())
def pillow(loc,w,d,h,col):
 N=18;M=14;vs=[];fs=[]
 for sign in [1,-1]:
  for j in range(M+1):
   v=j/M*2-1
   for i in range(N+1):
    u=i/N*2-1;x=u*w*.5*(1-.14*abs(v)**8);y=v*d*.5*(1-.14*abs(u)**8);bulge=max(0,(1-u*u)*(1-v*v))**.38
    pinch=sum(math.exp(-((u-k)**2+v*v)/.018)for k in [-.46,.46])*.018
    z=(h*.16+(h*.38)*bulge-pinch+ .002*math.sin(u*28+v*19)*(1-bulge))*sign
    vs.append((loc[0]+x,loc[1]+y,loc[2]+z))
 side=(N+1)*(M+1)
 for k in range(2):
  for j in range(M):
   for i in range(N):
    q=k*side+j*(N+1)+i;f=(q,q+1,q+N+2,q+N+1);fs.append(f if k==0 else f[::-1])
 border=list(range(N+1))+[j*(N+1)+N for j in range(1,M+1)]+[M*(N+1)+i for i in range(N-1,-1,-1)]+[j*(N+1)for j in range(M-1,0,-1)]
 for j,a in enumerate(border):b=border[(j+1)%len(border)];fs.append((a,a+side,b+side,b))
 o=mesh('tufted linen cushion',vs,fs,col)
 for f in o.data.polygons:f.use_smooth=True
 # Actual piping around the seam, rather than an emissive drawn line.
 pts=[(vs[i][0],vs[i][1],loc[2])for i in border[::2]];pts.append(pts[0]);tube('linen seam',pts,[.0038]*len(pts),(.45,.39,.24),6)
 return o
pillow((0,0,.065),.48,.36,.12,(.24,.32,.18));cushion=finish('LinenCushion')
# A single reading chair, sized for 140-cm characters: seat 43 cm, total height 103 cm.
for x in [-.285,.285]:
 for y in [-.25,.25]:tube('turned chair leg',[(x*1.05,y*1.06,0),(x,y,.12),(x,y,.37)],[.035,.026,.034],wood,12)
for y in [-.27,.27]:box('seat apron',(0,y,.365),(.65,.045,.105),wood)
for x in [-.305,.305]:box('seat apron',(x,0,.365),(.045,.56,.105),wood)
pillow((0,0,.455),.59,.54,.13,(.22,.30,.16))
for x in [-.31,.31]:
 tube('carved back post',[(x,-.265,.36),(x,-.30,.68),(x*.97,-.34,1.02)],[.03,.033,.035],wood,12)
 tube('curved arm rail',[(x,-.30,.69),(x,-.10,.66),(x,.24,.63)],[.03,.043,.035],edge,12)
 tube('arm support',[(x,.22,.40),(x,.23,.63)],[.023,.025],wood,10)
for z in [.58,.80,1.0]:tube('curved back rail',[(-.30,-.34,z),(0,-.37,z+.015),(.30,-.34,z)],[.027,.03,.027],edge,10)
for x in [-.22,-.11,0,.11,.22]:tube('back spindle',[(x,-.33,.54),(x,-.355,.80),(x,-.35,.99)],[.013,.016,.013],wood,8)
o=pillow((0,0,0),.51,.38,.10,(.27,.34,.19));start=parts.index(o)
# Piping follows the cushion in this local rotation.
for o in parts[start:]:
 for v in o.data.vertices:
  x,y,z=v.co;v.co=(x,-.30-z,.75+y)
chair=finish('ReadingChair')
# One bound book stack, usable on existing side tables and shelves.
for i,(angle,col) in enumerate([(-.11,(.18,.26,.16)),(.08,(.32,.17,.085)),(-.035,(.31,.30,.18))]):
 z=.055+i*.07;o=box('cream page block',(0,0,z),(.25,.18,.052),(.64,.57,.40),.003);o.rotation_euler.z=angle
 for dz in [-.03,.03]:o=box('clothbound cover',(0,0,z+dz),(.27,.20,.008),col,.003);o.rotation_euler.z=angle
 o=box('rounded book spine',(-.135,0,z),(.012,.20,.065),col,.006);o.rotation_euler.z=angle
books=finish('HerbalBooks')
# Organised source scene; exports above remain origin-centered.
for i,o in enumerate([cushion,chair,books]):o.location.x=i*1.1
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False)
assert len([o for o in bpy.context.scene.objects if o.type=='MESH'])==3
(A/'ArtV5_Props.json').write_text(json.dumps({'source':str(dst.relative_to(R)),'units':'m','assets':assets,'reopened':True,'only_new_sources':True},indent=2));print('ART_V5_PROPS_REOPENED')
