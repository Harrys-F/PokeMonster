"""Own numeric material masks/micro-normal data; no generated scenery or external image alteration."""
from pathlib import Path
import runpy,math,struct,zlib,json
R=Path(__file__).resolve().parents[2];globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py')));O=R/'Art/World/VisualV2WorldRefinementV4/Generated';O.mkdir(parents=True,exist_ok=True)
def png(path,n,channels,pixels):
 def ch(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
 raw=b''.join(b'\0'+pixels[j*n*channels:(j+1)*n*channels]for j in range(n));path.write_bytes(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>2I5B',n,n,8,6 if channels==4 else 2,0,0,0))+ch(b'IDAT',zlib.compress(raw,6))+ch(b'IEND',b''))
n=1024;p=bytearray(n*n*4);c=json.loads((R/'Tools/VisualV2EnvironmentPolishV2/PathMaskSource.json').read_text())
for j in range(n):
 y=-3250+(j+.5)*6500/n
 for i in range(n):
  x=-6000+(i+.5)*9000/n;road=0
  for key,ps in c['paths'].items():
   d=min(seg(x,y,a,b)for a,b in zip(ps,ps[1:]));width=c['halfwidths_cm'][key];noise=6*math.sin(x*.033+math.sin(y*.017))+4*math.sin(y*.073);road=max(road,smooth((width+noise+24-d)/42))
  r=pondr(x,y);ang=math.atan2((y+1800)/650,(x-720)/900);water=min(seg(x,y,(-910,-320),(1100,-320)),seg(x,y,(720,-320),(720,-680)));wet=max(1-smooth((water-65)/100),1-smooth(abs(r-shore(ang))/.14));macro=sat(.5+.22*math.sin(x*.0019+math.sin(y*.0027))+.16*math.cos(y*.0041+x*.0007));k=(j*n+i)*4;p[k:k+4]=bytes(round(sat(v)*255)for v in[road,forest(x,y)*.88,wet*.7,macro])
png(O/'GroundWeights.png',n,4,p)
n=512;p=bytearray(n*n*3)
for j in range(n):
 for i in range(n):
  dx=.035*math.sin(i*.17+math.sin(j*.29))+.016*math.sin(i*1.31+j*.47);dy=.035*math.cos(j*.21+math.sin(i*.23))+.016*math.sin(j*1.43+i*.61);k=(j*n+i)*3;p[k:k+3]=bytes([round((dx*.5+.5)*255),round((dy*.5+.5)*255),255])
png(O/'PlasterMicroNormal.png',n,3,p);print('Generated own numeric mask and micro-normal sources',O)
