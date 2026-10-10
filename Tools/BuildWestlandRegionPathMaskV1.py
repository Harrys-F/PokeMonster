"""Rasterize technical world-space path coverage; consistent blending at crossings.
Not illustrative texture generation: this grayscale field stores authored road footprints.
"""
from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
S=4;im=Image.new('L',(2000*S,1600*S),0);d=ImageDraw.Draw(im)
def xy(e,n):return ((e+500)*2*S,(400-n)*2*S)
paths=[{'points_m':p,'width_m':w} for _,p,w in L.PATHS]+json.loads((R/'Art/World/WestlandRegion/WestlandRegion_Access.json').read_text())
for p in paths:
 pts=[xy(*v) for v in L.sample(p['points_m'],spacing=.5)];width=round(p['width_m']*2*S*.86);d.line(pts,fill=255,width=width,joint='curve')
for e,n,rx,ry in [(-220,-35,17.5,15),(-301,-217,11,8.5),(145,-229,24,18)]:
 d.ellipse([xy(e-rx,n+ry),xy(e+rx,n-ry)],fill=255)
im=im.resize((2000,1600),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.6));o=R/'Art/World/WestlandRegion/Textures';o.mkdir(exist_ok=True);im.convert('RGB').save(o/'T_WR_PathCoverage.png')
