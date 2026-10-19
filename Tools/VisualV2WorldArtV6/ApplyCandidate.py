"""V6 changes four material bindings and transforms in the 16 explicitly visual V5 groups. No new actor."""
import unreal,json,sys,copy,math,random,ast
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV6';A=R/'Art/World/VisualV2WorldArtV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not (S/'CandidateScene.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(x):
 x=copy.deepcopy(x)
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return x
before=canon(scene(w));assert before==canon(json.loads((S/'BeforeScene.json').read_text()));actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};prepared=json.loads((S/'Prepared.json').read_text());materials={r['key']:r for r in prepared['materials']};bindings=[]
for label,key in [('V2_Ground','Ground'),('V2_Path_Main','MainPath'),('V2_Path_NorthLoop','NorthPath'),('V2_Path_VillageLoop','NorthPath')]:
 a=actors[label];row=materials[key];assert a.static_mesh_component.get_material(0).get_path_name()==row['old'];a.static_mesh_component.set_material(0,unreal.load_asset(row['new']));bindings.append({'name':a.get_name(),'label':label,'old':row['old'],'new':row['new']})
module=ast.parse((R/'Tools/ModernizeDevTestMapVisualV2.py').read_text());paths=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
def spline(points):
 pts=[]
 for i in range(len(points)-1):
  p0,p1,p2,p3=[points[max(0,min(len(points)-1,j))] for j in (i-1,i,i+1,i+2)]
  for j in range(16):
   t=j/16;pts.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t**3) for k in [0,1]))
 return pts+[points[-1]]
curves={k:spline(p) for k,p in paths.items()};edges=[(a,b) for pts in curves.values() for a,b in zip(pts,pts[1:])];linear=[(a,b) for pts in paths.values() for a,b in zip(pts,pts[1:])]+[((-1550,650),(-1900,530)),((-2100,-2060),(-1770,-1550))]
def project(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));q=(a[0]+t*dx,a[1]+t*dy);return math.hypot(x-q[0],y-q[1]),q

def distance(x,y,lines=edges):return min(project(x,y,a,b)[0] for a,b in lines)
def inside(biome,x,y):
 if biome=='Wald':return ((x+3400)/1010)**2+((y-1810)/570)**2<.94 and y>1280
 if biome=='Wiese':return ((x+2320)/740)**2+((y+1960)/510)**2<.94
 return ((x+250)/875)**2+((y+320)/420)**2<.94
protected=[a.get_actor_location() for a in actors.values() if 'PokeMonster' in a.get_class().get_name() and not a.get_actor_label().startswith('V2_House_')]
pockets={
 'Wald':[(-3940,1650,125,75),(-3660,1550,145,80),(-2810,1580,130,70),(-2650,1800,95,105),(-3800,2230,160,70),(-2920,2250,110,65)],
 'Wiese':[(-2760,-2160,150,85),(-2340,-2250,160,100),(-1930,-2190,100,65),(-2740,-1750,140,100),(-2180,-1600,140,70),(-1740,-1810,75,75)]}
weights={
 ('Wald','FernA'):[3,4,6,2,1,1],('Wald','FernB'):[1,3,5,2,1,2],('Wald','Shrub'):[3,1,4,3,1,1],('Wald','Grass'):[3,3,2,1,2,1],('Wald','Moss'):[4,2,4,2,1,1],
 ('Wiese','Grass'):[4,5,1,2,3,1],('Wiese','Clover'):[5,4,1,1,3,1],('Wiese','Flowers'):[5,1,1,1,5,0],('Wiese','Herbs'):[3,3,1,2,3,0],('Wiese','Pebbles'):[2,2,2,1,1,1]}
rng=random.Random(6191026);oldgroups=json.loads((R/'Art/World/VisualV2WorldArtV5/Scope.json').read_text())['new_groups'];rows=[]
base={'FernA':.48,'FernB':.46,'Shrub':.20,'Grass':1,'Moss':1,'Clover':.90,'Flowers':.78,'Herbs':.75,'Pebbles':.43,'Reeds':.83,'Fern':.37,'BankStone':.13}
rad={'FernA':38,'FernB':37,'Shrub':34,'Grass':23,'Moss':24,'Clover':20,'Flowers':25,'Herbs':24,'Pebbles':10,'Reeds':23,'Fern':30,'BankStone':24}
for old in oldgroups:
 biome,key=old['biome'],old['family'];a=actors[old['label']];assert a.get_name()==old['name'] and 'WorldArtV5' in [str(t) for t in a.tags];c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c and c.static_mesh.get_path_name().split('.')[0]==old['mesh'] and c.get_instance_count()==len(old['instances']);assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.cast_shadow
 if key=='Roots':continue
 count=c.get_instance_count();placed=[];radius=rad[key];area_edges=[(u,v) for u,v in edges if inside(biome,(u[0]+v[0])/2,(u[1]+v[1])/2)]
 for attempt in range(60000):
  if len(placed)==count:break
  edge_growth=key in ['Grass','Moss','Clover','Pebbles'] and rng.random()<.31 and biome!='Flussufer'
  if edge_growth and area_edges:
   u,v=rng.choice(area_edges);t=rng.random();x=u[0]+t*(v[0]-u[0]);y=u[1]+t*(v[1]-u[1]);dx=v[0]-u[0];dy=v[1]-u[1];length=math.hypot(dx,dy);offset=rng.uniform(110,158)*rng.choice([-1,1]);x-=dy/length*offset;y+=dx/length*offset
  elif biome=='Flussufer':
   centers=[(-885,1,30),(-710,-1,45),(-80,1,35),(70,-1,42),(365,1,42),(440,-1,32)];cx,side,spread=rng.choices(centers,weights=[5,2,4,1,3,1])[0];x=rng.gauss(cx,spread);waterdist=rng.uniform(88,126) if key in ['Reeds','Pebbles','BankStone'] else rng.uniform(125,205);y=-320+side*waterdist
   if -535<x<-165:continue
  else:
   px,py,sx,sy=rng.choices(pockets[biome],weights=weights.get((biome,key),[1]*6))[0];x=rng.gauss(px,sx);y=rng.gauss(py,sy)
  if not inside(biome,x,y):continue
  if biome=='Wald' and ((((x+3210)/220)**2+((y-2190)/160)**2<1) or (((x+3420)/165)**2+((y-1490)/100)**2<1)):continue
  if biome=='Wiese' and ((x+2380)/185)**2+((y+1820)/150)**2<1:continue
  clearance=132 if key=='Grass' else 110 if key in ['Moss','Clover'] else 92 if key=='Pebbles' else 165 if key in ['FernA','FernB','Fern','Shrub'] else 143
  if distance(x,y)<clearance or distance(x,y,linear)<90:continue
  if any(math.hypot(x-p.x,y-p.y)<165+radius for p in protected):continue
  sep=16 if key in ['Moss','Clover','Grass','Pebbles'] else 26
  if any(math.hypot(x-p['location_cm'][0],y-p['location_cm'][1])<sep for p in placed):continue
  sc=base[key]*rng.uniform(.68,1.27);sz=sc*rng.uniform(.65,1.35)
  if key=='Grass':sz=sc*rng.uniform(.45,1.36)
  if key in ['Pebbles','BankStone']:sz=sc*rng.uniform(.38,.58)
  z=-.15 if key in ['Pebbles','BankStone'] else .45;yaw=rng.uniform(0,360);scale=unreal.Vector(sc*rng.uniform(.82,1.16),sc,sz);rotation=unreal.Rotator(yaw=yaw,pitch=rng.uniform(-5,5) if key in ['Pebbles','BankStone'] else 0);t=unreal.Transform(location=unreal.Vector(x,y,z),rotation=rotation,scale=scale);placed.append({'location_cm':[x,y,z],'rotation_rpy':rotation.to_tuple(),'scale':scale.to_tuple(),'distance_to_existing_path_center_cm':distance(x,y),'world_transform':t})
 assert len(placed)==count,(biome,key,len(placed),count)
 for i,row in enumerate(placed):assert c.update_instance_transform(i,row.pop('world_transform'),True,i==count-1,True)
 rows.append({'name':a.get_name(),'label':a.get_actor_label(),'biome':biome,'family':key,'mesh':old['mesh'],'instance_count':count,'instances':placed})
after=canon(scene(w));assert set(after['actors'])==set(before['actors']) and after['world_settings']==before['world_settings'];bindingnames={x['name'] for x in bindings};groupnames={x['name'] for x in rows}
for name,old in before['actors'].items():
 actual=copy.deepcopy(after['actors'][name])
 if name in bindingnames:
  for u,v in zip(old['components'],actual['components']):v['materials']=u['materials']
 if name in groupnames:
  for u,v in zip(old['components'],actual['components']):
   if 'instances' in u:v['instances']=u['instances']
 assert actual==old,('Unexpected protected change',name)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();result={'material_bindings':bindings,'regrouped_groups':rows,'group_count':len(rows),'regrouped_instances':sum(x['instance_count'] for x in rows),'roots_unchanged':8,'new_actors':0,'deleted_actors':0,'new_meshes':0,'new_textures':0,'unchanged_existing_actors':len(before['actors'])-len(bindingnames)-len(groupnames),'existing_geometry_collision_navigation_lights_gameplay_unchanged':True};(A/'Scope.json').write_text(json.dumps(result,indent=2));(S/'Delta.json').write_text(json.dumps(result,indent=2));(S/'CandidateScene.json').write_text(json.dumps(scene(w),indent=2));unreal.log('WA6_CANDIDATE_APPLIED_NOT_SAVED')
