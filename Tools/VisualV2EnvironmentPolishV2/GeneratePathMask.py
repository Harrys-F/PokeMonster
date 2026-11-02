"""Regenerate only our own mask from recorded existing routes, never alter a map."""
from pathlib import Path
import json,math,struct,zlib
R=Path(__file__).resolve().parents[2];T=Path(__file__).parent;D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';D.mkdir(exist_ok=True);c=json.loads((T/'PathMaskSource.json').read_text());N=c['size'];xmin,ymin,xmax,ymax=c['world_bounds'];sx=xmax-xmin;sy=ymax-ymin;pixels=bytearray(N*N)
for key,ps in c['paths'].items():
 width=c['halfwidths_cm'][key]
 for a,b in zip(ps,ps[1:]):
  lo=[max(0,int((min(a[0],b[0])-width-45-xmin)/sx*N)),max(0,int((min(a[1],b[1])-width-45-ymin)/sy*N))];hi=[min(N-1,int((max(a[0],b[0])+width+45-xmin)/sx*N)),min(N-1,int((max(a[1],b[1])+width+45-ymin)/sy*N))];dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy
  for j in range(lo[1],hi[1]+1):
   y=(j+.5)/N*sy+ymin
   for i in range(lo[0],hi[0]+1):
    x=(i+.5)/N*sx+xmin;t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/den));d=math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);noise=6*math.sin(x*.033+math.sin(y*.017))+4*math.sin(y*.073);w=max(0,min(1,(width+noise+24-d)/42));v=round(255*w*w*(3-2*w));k=j*N+i;pixels[k]=max(pixels[k],v)
raw=b''.join(b'\0'+pixels[j*N:(j+1)*N]for j in range(N))
def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
p=D/'PathMask.png';p.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',N,N,8,0,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''));print(p)
