"""Explicit anatomical envelopes for disconnected Meshy surfaces. No topology changes."""
from mathutils import Vector
import math

def assign(body,rig,s,name):
 bones=rig.data.bones
 def dist(p,n):
  b=bones[n];a=b.head_local;t=b.tail_local-a;u=max(0.,min(1.,(p-a).dot(t)/t.length_squared));return(p-a-u*t).length
 def mix(weights):
  weights=sorted(weights.items(),key=lambda kv:-kv[1])[:4];total=sum(v for _,v in weights);assert total>0;return{n:v/total for n,v in weights}
 def near(p,names):return mix({n:1/max(dist(p,n),s['height']*.008)**4 for n in names})
 def smooth(a,b,x):t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
 body.vertex_groups.clear()
 for b in bones:
  if b.name!='root':body.vertex_groups.new(name=b.name)
 counts={};transitions=0
 for v in body.data.vertices:
  p=v.co;x,y,z=p;side='L'if x>0 else'R';h=s['height'];ch=s['chest'][2];neck=s['neck'][2];weights=near(p,['pelvis','chest','head'])
  if z>neck:weights={'head':1.}
  if 'hip'in s and z<(h*.11 if name=='Pikachu'else s['hip'][2]*1.12) and abs(x)>s['hip'][0]*.55:
   leg=near(p,['thigh_'+side,'shin_'+side,'foot_'+side]);f=smooth(s['hip'][0]*.55,s['hip'][0]*.95,abs(x))*(1-smooth(h*.05,h*.11,z)if name=='Pikachu'else 1-smooth(s['hip'][2]*.8,s['hip'][2]*1.12,z));weights={k:weights.get(k,0)*(1-f)+leg.get(k,0)*f for k in weights.keys()|leg.keys()}
  if 'shoulder'in s and ((name=='Machomei'and abs(x)>.30 and .67<z<1.35)or(name!='Machomei'and abs(x)>s['shoulder'][0]*.8 and z>s['hip'][2]*1.12 and abs(z-s['shoulder'][2])<h*(.065 if name=='Pikachu'else .10)and(name!='Pikachu'or(abs(x)>.095 and y<.025))and(name!='Gengar'or(abs(x)>.48 and y<-.25 and z<.72)))):
   candidates=['upperarm_'+side,'forearm_'+side,'hand_'+side]
   if name=='Machomei':candidates+=['lower_upperarm_'+side,'lower_forearm_'+side,'lower_hand_'+side]
   ar=near(p,candidates);f=smooth(.095,.145,abs(x))if name=='Pikachu'else smooth(s['shoulder'][0]*.80,s['shoulder'][0]*1.32,abs(x));weights={k:weights.get(k,0)*(1-f)+ar.get(k,0)*f for k in weights.keys()|ar.keys()}
  if name=='Pikachu':
   if z>.325 and abs(x)>.070:weights={'ear_'+side:1}
   if y>.075:
    f=smooth(.075,.095,y);weights={k:weights.get(k,0)*(1-f)+(f if k=='tail_tip'else 0) for k in weights.keys()|{'tail_tip'}}
  elif name=='Myrapla'and .050<z<=.235:weights={'head':1}
  elif name=='Myrapla'and z>.235:
   weights=near(p,[n for n in bones.keys()if n.startswith('leaf_')])
  elif name=='Enton'and y>.16 and z<.30:weights={'tail_base':1}
  elif name=='Nebulak':
   radial=((x/.39)**2+((z-.47)/.39)**2)**.5
   weights={'head':1}if radial<1.08 else near(p,[n for n in bones.keys()if n.startswith('gas_')])
  elif name=='Glurak':
   if x<-.90 and y>.80 and z>.40:weights={'flame_tip':1}
   elif (x<-.40 or y>.31)and z<.80:weights=near(p,['tail_base','tail_mid','tail_tip'])
   elif abs(x)>.31 and z>1.01:weights=near(p,['wing_base_'+side,'wing_tip_'+side])
  weights=mix(weights)
  for n,w in weights.items():body.vertex_groups[n].add([v.index],w,'REPLACE');counts[n]=counts.get(n,0)+1
 assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in body.data.vertices)
 return dict(method='explicit hand-fitted anatomical segment envelopes, maximum four normalized influences; pose inspection required',bone_heat='Pikachu original Bone Heat failed; incomplete weights rejected, not transferred',vertices_per_bone=counts,unweighted_vertices=0,original_geometry_unchanged=True)
