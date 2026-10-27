"""Exact route-distance acceleration, not a baked/approximated color or reduced quality.

A balanced AABB tree skips only segments whose lower distance bound exceeds an
already measured segment distance. A coarse seed only supplies an upper bound.
The original segment-distance expression, source coordinates and earliest-index
tie rule are preserved. Conservative bbox padding/relative slack avoids an
unsafe floating-point prune. Only generated shader flow changes.
"""
import re,math,random,statistics
PAT=r's=sd\(p,float2\(([-\d.]+),([-\d.]+)\),float2\(([-\d.]+),([-\d.]+)\)\);if\(s<d\)\{d=s;base=([-\d.]+);\}'
def distance(p,s):
 ax,ay,bx,by,_=s;vx=bx-ax;vy=by-ay;t=max(0.,min(1.,((p[0]-ax)*vx+(p[1]-ay)*vy)/(vx*vx+vy*vy)))
 return math.hypot(p[0]-ax-vx*t,p[1]-ay-vy*t)
def accelerate(code):
 lines=re.findall(PAT,code);segs=[tuple(map(float,x))for x in lines];assert len(segs)>=50
 old=re.search(r'float2 nearest\(float2 p\)\{.*?return float2\(d,base\);\}',code,re.S);assert old and len(re.findall(PAT,old.group()))==len(segs)
 def build(ids):
  box=(min(min(segs[i][0],segs[i][2])for i in ids)-.001,min(min(segs[i][1],segs[i][3])for i in ids)-.001,max(max(segs[i][0],segs[i][2])for i in ids)+.001,max(max(segs[i][1],segs[i][3])for i in ids)+.001)
  n={'box':box,'ids':ids}
  if len(ids)>4:
   axis=0 if box[2]-box[0]>=box[3]-box[1]else 1;ordered=sorted(ids,key=lambda i:(segs[i][axis]+segs[i][axis+2])/2);k=len(ids)//2;n['children']=[build(ordered[:k]),build(ordered[k:])]
  return n
 tree=build(list(range(len(segs))));xs=[-6500,-4000,-1500,1000,3500];ys=[-4500,-2250,0,2250,4500];seeds=[[min(range(len(segs)),key=lambda i:distance(((xs[x]+xs[x+1])/2,(ys[y]+ys[y+1])/2),segs[i]))for x in range(4)]for y in range(4)]
 def update(i):
  a,b,c,d,w=lines[i]
  return f's=sd(p,float2({a},{b}),float2({c},{d}));if(s<d||(s==d&&first!=2147483647&&{i}<first)){{d=s;base={w};first={i};}}'
 def seed_choice(lo,hi,axis,other=None):
  if hi-lo==1:
   if axis==0:return seed_choice(0,4,1,lo)
   return update(seeds[lo][other])+'\n'
  mid=(lo+hi)//2;split=(xs if axis==0 else ys)[mid];channel='x'if axis==0 else'y'
  return f'[branch] if(p.{channel}<{split:.6f}){{\n'+seed_choice(lo,mid,axis,other)+'}else{\n'+seed_choice(mid,hi,axis,other)+'}\n'
 counter=[0]
 def emit(n):
  ident=counter[0];counter[0]+=1;a,b,c,d=n['box'];s=f'float2 b{ident}=max(max(float2({a:.6f},{b:.6f})-p,p-float2({c:.6f},{d:.6f})),0);\n[branch] if(dot(b{ident},b{ident})<=d*d+max(.01,d*d*.00001)){{\n'
  if'children'in n:s+=''.join(emit(k)for k in n['children'])
  else:s+='\n'.join(update(i)for i in sorted(n['ids']))+'\n'
  return s+'}\n'
 replacement='float2 nearest(float2 p){\n// PV1 exact AABB acceleration; original earliest-segment ties retained.\nfloat d=100000;float base=120;float s;int first=2147483647;\n'+seed_choice(0,4,0)+emit(tree)+'return float2(d,base);}'
 def fast(p):
  x=sum(p[0]>=v for v in xs[1:4]);y=sum(p[1]>=v for v in ys[1:4]);best=[100000.,120.,2147483647];evaluated=[0]
  def visit_segment(i):
   evaluated[0]+=1;s=distance(p,segs[i])
   if s<best[0]or(s==best[0]and best[2]!=2147483647 and i<best[2]):best[:]=[s,segs[i][4],i]
  def visit(n):
   a,b,c,d=n['box'];dx=max(a-p[0],p[0]-c,0);dy=max(b-p[1],p[1]-d,0)
   if dx*dx+dy*dy>best[0]*best[0]+max(.01,best[0]*best[0]*.00001):return
   if'children'in n:
    for child in n['children']:visit(child)
   else:
    for i in sorted(n['ids']):visit_segment(i)
  visit_segment(seeds[y][x]);visit(tree);return best,evaluated[0]
 rng=random.Random(74283);points=[(rng.uniform(-8000,4500),rng.uniform(-6000,6000))for _ in range(4000)]+[(s[i],s[i+1])for s in segs for i in [0,2]]+[(rng.uniform(-1e6,1e6),rng.uniform(-1e6,1e6))for _ in range(50)];counts=[]
 for p in points:
  expected=(100000.,2147483647,120.)
  for i,seg in enumerate(segs):
   v=distance(p,seg)
   if v<expected[0]:expected=(v,i,seg[4])
  got,n=fast(p)
  assert got[0]==expected[0]and got[1]==expected[2],(p,expected,got);counts.append(n)
 new=code[:old.start()]+replacement+code[old.end():]
 assert code[:old.start()]==new[:old.start()]and code[old.end():]==new[old.start()+len(replacement):]
 return new,{'segments':len(segs),'bbox_nodes':counter[0],'test_points':len(points),'max_distance_error':0,'width_mismatches':0,'distance_evaluations_mean':statistics.mean(counts),'distance_evaluations_max':max(counts),'original_code_chars':len(code),'candidate_code_chars':len(new),'no_texture_or_lod_change':True}
