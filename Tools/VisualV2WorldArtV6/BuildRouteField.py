from pathlib import Path
import ast,json,math
R=Path(__file__).resolve().parents[2];A=R/'Saved/VisualV2WorldArtV6/RouteFieldRebuild';A.mkdir(exist_ok=False)
# Rebuild into new local evidence only; never overwrite the authored input files.

module=ast.parse((R/'Tools/ModernizeDevTestMapVisualV2.py').read_text());paths=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
def dist(p,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def simplify(pts):
 if len(pts)<3:return pts
 errs=[dist(p,pts[0],pts[-1]) for p in pts[1:-1]];m=max(errs)
 if m<=4:return [pts[0],pts[-1]]
 i=1+errs.index(m);return simplify(pts[:i+1])[:-1]+simplify(pts[i:])
def spline(points):
 pts=[]
 for i in range(len(points)-1):
  p0,p1,p2,p3=[points[max(0,min(len(points)-1,j))] for j in (i-1,i,i+1,i+2)]
  for j in range(16):
   t=j/16;pts.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t**3) for k in [0,1]))
 return pts+[points[-1]]
boxes=[(-4650,-2050,1150,2550),(-3250,-900,-2650,-1350),(-1200,650,-950,180)]
def in_box(p):return any(a-100<p[0]<b+100 and c-100<p[1]<d+100 for a,b,c,d in boxes)
segments=[];audit=[]
for name,points in paths.items():
 full=spline(points);simple=simplify(full);edges=list(zip(simple,simple[1:]));err=max(min(dist(p,a,b) for a,b in edges) for p in full);assert err<=4.01
 selected=[(a,b) for a,b in edges if any(in_box((a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)) for t in [0,.25,.5,.75,1])]
 if name=='Wild':selected=[]
 segments += [{'route':name,'a':a,'b':b,'base_half_width_cm':{'Main':122,'VillageLoop':127,'NorthLoop':112}.get(name,115)} for a,b in selected]
 audit.append({'route':name,'original_mesh_samples':len(full),'distance_approx_max_error_cm':err,'selected_segments':len(selected)})
config={'source':'Tools/ModernizeDevTestMapVisualV2.py paths, actual 16-step Catmull-Rom ribbon sampling','geometry_collision_navigation_changes':False,'segments':segments,'sampling_audit':audit,'scope':{'Wald':[-3400,1810,1080,640],'Wiese':[-2320,-1960,800,570],'Flussufer':[-250,-320,950,480],'AngrenzendeKreuzung':[-1310,-1850,400,300]},'existing_group_policy':'Only 17 explicitly tagged WA5 groups; identical meshes/materials/counts, replace individual transforms. All other actors untouched.'}
(A/'RouteField.json').write_text(json.dumps(config,indent=2))
# Constant distance evaluation only within the bounded area. No runtime actor ticks or traces.
lines=['struct W6Route {','float sd(float2 p,float2 a,float2 b){float2 v=b-a;return length(p-a-v*saturate(dot(p-a,v)/dot(v,v)));}','float2 nearest(float2 p){float d=100000;float base=120;float s;']
for row in segments:
 a,b=row['a'],row['b'];lines.append(f's=sd(p,float2({a[0]:.5f},{a[1]:.5f}),float2({b[0]:.5f},{b[1]:.5f}));if(s<d){{d=s;base={row["base_half_width_cm"]:.1f};}}')
lines+=['return float2(d,base);}','};','''float2 v6p=P.xy;
float2 v6Warp=float2(24*sin(v6p.y*.013+sin(v6p.x*.004)),19*cos(v6p.x*.011+cos(v6p.y*.006)));
float v6Noise=sin(v6p.x*.007+sin(v6p.y*.009))*cos(v6p.y*.005-v6p.x*.003);
float v6F=(1-smoothstep(.70,1,length((v6p-float2(-3400,1810))/float2(1080,640))+.035*v6Noise))*smoothstep(1220,1390,v6p.y);
float v6M=1-smoothstep(.70,1,length((v6p-float2(-2320,-1960))/float2(800,570))+.045*v6Noise);
float v6R=1-smoothstep(.70,1,length((v6p-float2(-250,-320))/float2(950,480))+.035*v6Noise);
float v6J=1-smoothstep(.65,1,length((v6p-float2(-1310,-1850))/float2(400,300))+.035*v6Noise);
float v6BridgeProtected=1-(1-smoothstep(85,115,abs(v6p.x+350)))*(1-smoothstep(120,155,abs(v6p.y+320)));
float v6Scope=max(max(v6F,v6M),max(v6R,v6J))*v6BridgeProtected;
float v6Dist=100000;float v6Half=120;
if(v6Scope>.00001){W6Route route;float2 field=route.nearest(v6p);v6Dist=field.x;v6Half=field.y;}
v6Half+=15*v6Noise+6*sin(v6p.x*.013-v6p.y*.007);
v6Half+=29*(1-smoothstep(45,250,length((v6p-float2(-1220,-1895))*float2(1,1.25))));
float v6EdgeNoise=4*sin(v6p.x*.077+sin(v6p.y*.05))+3*cos(v6p.y*.113-v6p.x*.027);
float v6Coverage=1-smoothstep(v6Half-10,v6Half+17,v6Dist+v6EdgeNoise);
float v6WetDist=abs(v6p.y+320)-66;
float v6Shore=13*sin(v6p.x*.017+sin(v6p.x*.005))+12*cos(v6p.x*.033);
float v6BankMask=v6R*smoothstep(2,18,v6WetDist)*(1-smoothstep(72+v6Shore,153+v6Shore,v6WetDist));
float v6Cove=max(1-smoothstep(.40,1,length((v6p-float2(-790,-203))/float2(145,72))),max(1-smoothstep(.40,1,length((v6p-float2(-50,-449))/float2(150,80))),1-smoothstep(.40,1,length((v6p-float2(300,-199))/float2(145,78)))));
v6BankMask=max(v6BankMask,v6Cove*v6R*smoothstep(8,20,v6WetDist))*v6BridgeProtected;
''']
(A/'RouteField.hlsl').write_text('\n'.join(lines));print('Route field:',len(segments),'segments',audit)
