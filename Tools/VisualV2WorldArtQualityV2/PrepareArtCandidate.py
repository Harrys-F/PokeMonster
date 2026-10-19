"""Prepare private bounded materials and a deterministic 175-instance layout. No map mutation."""
import unreal,json,math,random,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not (S/'ArtCandidate.json').exists();D='/Game/Environment/VisualV2WorldArtV2/Materials';L=unreal.MaterialEditingLibrary;materials=[]
area='smoothstep(-4620,-4510,p.x)*(1-smoothstep(-3670,-3560,p.x))*smoothstep(-720,-610,p.y)*(1-smoothstep(1080,1190,p.y))'
for name in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 src='/Game/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_'+name;dst=D+'/M_WAQ2_'+name;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);m=unreal.EditorAssetLibrary.duplicate_asset(src,dst);color=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if x.get_outer()==m and x.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3);code=color.get_editor_property('code');needle='float2 p=P.xy;';assert needle in code
 prefix='float localPaint='+area+';float2 painted=p+localPaint*float2(24*sin(p.y*.008+sin(p.x*.0037)),21*cos(p.x*.009+sin(p.y*.0041)));'
 code=code.replace(needle,needle+prefix).replace('float2 a=p/190.0;','float2 a=painted/190.0;').replace('float2(p.x*.809-p.y*.588,p.x*.588+p.y*.809)/271.0','float2(painted.x*.809-painted.y*.588,painted.x*.588+painted.y*.809)/271.0').replace('float2(p.y,-p.x)/413.0','float2(painted.y,-painted.x)/413.0').replace('DTexSampler,p/220.0','DTexSampler,painted/220.0').replace('float2(p.x*.6+p.y*.8,-p.x*.8+p.y*.6)/337.0','float2(painted.x*.6+painted.y*.8,-painted.x*.8+painted.y*.6)/337.0')
 # Same texture fetch count, local coordinate dephasing only. Preserve all edge-mask expressions.
 color.set_editor_property('code',code);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);materials.append({'old':src+'.M_WAQ1_'+name,'new':m.get_path_name()})
inv=json.loads((R/'Art/World/VisualV2WorldArtV2/BaselineInstances.json').read_text());rng=random.Random(19102602)
# Variable-size, asymmetric botanical pockets. Explicit gaps in between remain unplanted.
pockets=[(-4430,-350,56,120,3.0),(-3910,-320,45,58,.8),(-4410,95,35,45,.4),(-3870,95,56,95,2.7),(-4440,320,32,48,.35),(-4335,815,72,78,3.6),(-4205,1030,40,35,.7),(-3860,905,78,52,2.2),(-3710,1000,28,36,.4)]
route=[((-4150,-720),(-4100,450)),((-4100,450),(-3600,500)),((-4100,450),(-4300,1190))];pots=[(-3640,325,50),(-3650,775,50),(-3780,90,60),(-4200,70,85),(-3800,45,85),(-4020,950,90)]
def dist(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def safe(x,y,rad):
 return -4510<x<-3630 and -610<y<1080 and not(x>-3800 and 300<y<720) and min(dist(x,y,a,b) for a,b in route)>155+rad and all(math.hypot(x-px,y-py)>rr+rad*.5 for px,py,rr in pots)
new=[];allpoints=[]
for group in inv['groups']:
 key=group['label'].removeprefix('WAQ1_');rad={'GrassSmall':14,'GrassMedium':26,'MeadowHerbs':24,'Flowers':24,'Fern':36,'Pebbles':10}[key];points=[];counts={str(i):0 for i in range(len(pockets))}
 for i,old in enumerate(group['transforms']):
  tf=unreal.Transform();tf.import_text(old)
  for attempt in range(10000):
   weights=[p[4] for p in pockets]
   if key=='Fern':weights=[.8,.1,0,1.0,0,4,.1,.4,0]
   elif key=='Flowers':weights=[2.2,.2,0,1.5,0,.6,.2,2.0,.1]
   elif key=='Pebbles':weights=[1,1,1,1,.5,.7,.5,.7,.5]
   k=rng.choices(range(len(pockets)),weights=weights)[0];cx,cy,sx,sy,_=pockets[k];x=rng.gauss(cx,sx);y=rng.gauss(cy,sy)
   if not safe(x,y,rad):continue
   if any(math.hypot(x-p[0],y-p[1])<rad*.75 for p in points):continue
   break
  else:raise RuntimeError('No valid placement '+key)
  tf.translation=unreal.Vector(x,y,tf.translation.z);tf.rotation=unreal.Rotator(yaw=rng.uniform(0,360)).quaternion();points.append([x,y]);allpoints.append((x,y));counts[str(k)]+=1
  new.append({'actor':group['actor'],'label':group['label'],'index':i,'transform':tf.export_text()})
 group['pocket_counts']=counts
assert len(new)==175
(S/'ArtCandidate.json').write_text(json.dumps({'materials':materials,'placements':new,'pockets':pockets,'family_counts':{g['label']:g['count'] for g in inv['groups']},'pocket_counts':{g['label']:g['pocket_counts'] for g in inv['groups']},'bounding_region_cm':[-4620,-3560,-720,1190],'unchanged_total_instances':175,'topfpflanzen_unchanged':True},indent=2));unreal.log('WAQ2_BOUNDED_ART_CANDIDATE_READY')
