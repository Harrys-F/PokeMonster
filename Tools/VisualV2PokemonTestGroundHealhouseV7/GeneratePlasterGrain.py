"""Owned, seamless numeric surface micro-normal. No photographs/models or original edits."""
from pathlib import Path
import math,random,struct,zlib
R=Path(__file__).resolve().parents[2];O=R/'Art/World/VisualV2InteriorV7/Generated/PlasterGrainNormal.png';O.parent.mkdir(parents=True,exist_ok=True);assert not O.exists();N=512;rng=random.Random(731570);layers=[]
for size,weight in [(4,.08),(8,.12),(16,.28),(32,.32),(64,.2)]:layers.append((size,weight,[[rng.uniform(-1,1)for _ in range(size)]for _ in range(size)]))
def smooth(t):return t*t*(3-2*t)
height=[]
for y in range(N):
 row=[]
 for x in range(N):
  value=0
  for size,weight,grid in layers:
   fx=x*size/N;fy=y*size/N;i=int(fx);j=int(fy);u=smooth(fx-i);v=smooth(fy-j);a=grid[j%size][i%size]*(1-u)+grid[j%size][(i+1)%size]*u;b=grid[(j+1)%size][i%size]*(1-u)+grid[(j+1)%size][(i+1)%size]*u;value+=weight*(a*(1-v)+b*v)
  row.append(value)
 height.append(row)
raw=bytearray()
for y in range(N):
 raw.append(0)
 for x in range(N):
  dx=(height[y][(x+1)%N]-height[y][(x-1)%N])*2.4;dy=(height[(y+1)%N][x]-height[(y-1)%N][x])*2.4;l=math.sqrt(dx*dx+dy*dy+1);raw.extend([round((-dx/l*.5+.5)*255),round((-dy/l*.5+.5)*255),round((1/l*.5+.5)*255)])
def chunk(k,d):return struct.pack('>I',len(d))+k+d+struct.pack('>I',zlib.crc32(k+d)&0xffffffff)
O.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',N,N,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''));print(O)
