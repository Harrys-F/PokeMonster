"""V5 map-only presentation, route clearance and shared bush encounter volumes.
Uses existing assets. Refuses duplicate application or unrelated dirty assets.
"""
import unreal,json,math,random,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();actors={a.get_actor_label():a for a in A.get_all_level_actors()};assert not any(n.startswith('GEV5_')for n in actors),'Already authored; inspect instead of duplicating';rng=random.Random(51103);out=dict(npcs=[],sprites=[],moves=[],groups=[],fields=[],barriers=[],healer={});SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
# V4 terrain is unchanged. Its exact authoring height formula avoids tracing roofs/foliage.
geo=runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Design.py'));height=geo['height'];seg=geo['seg'];sat=geo['sat'];paths=json.loads((R/'Tools/VisualV2EnvironmentPolishV2/PathMaskSource.json').read_text());segments=[(name,a,b,paths['halfwidths_cm'][name])for name,p in paths['paths'].items()for a,b in zip(p,p[1:])]
# Door approaches remain the same lines as the current game; include actual interaction pads.
pads=[(-750,-600,145),(-1050,-1260,135),(-920,-1080,125),(-700,-1330,95),(820,680,100),(-3550,500,170),(-3020,-1020,145),(-2250,-1200,100)]
def nearest(x,y):
 rows=[]
 for n,a,b,w in segments:
  dx=b[0]-a[0];dy=b[1]-a[1];t=sat(((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy));px=a[0]+dx*t;py=a[1]+dy*t;rows.append((math.hypot(x-px,y-py)-w,px,py,dx,dy,w,n))
 return min(rows)
def clear(x,y,r=0,margin=25):
 if not(-5780+r<x<2780-r and -3030+r<y<3030-r):return False
 if nearest(x,y)[0]<r+margin:return False
 if any(math.hypot(x-cx,y-cy)<pr+r for cx,cy,pr in pads):return False
 if any(abs(x-cx)<rx+r and abs(y-cy)<ry+r for cx,cy,rx,ry in [(-3100,500,570,620),(-2750,-1020,420,370),(1080,900,350,400)]):return False
 if math.hypot((x-720)/1000,(y+1800)/740)<1.04:return False
 if -1080<x<1290 and abs(y+320)<185+r:return False
 return True

def own(a,label):a.set_actor_label('GEV5_'+label);a.set_folder_path('VisualV2/GameplayEnvironmentV5');a.tags=['VisualV2GameplayEnvironmentV5'];return a

def component(a,cls):
 h,err=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=cls,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,err;return c

def group(label,mesh,materials=None):
 a=own(A.spawn_actor_from_class(unreal.Actor,unreal.Vector()),label);c=component(a,unreal.HierarchicalInstancedStaticMeshComponent);c.set_collision_profile_name('NoCollision');c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(False)
 if materials:
  for i,m in enumerate(materials):c.set_material(i,m)
 c.set_static_mesh(mesh);out['groups'].append(dict(label=a.get_actor_label(),mesh=mesh.get_path_name(),count=0));return c

def plant(c,x,y,h,yaw=None):
 b=c.static_mesh.get_bounding_box();s=h/(b.max.z-b.min.z);rot=unreal.Rotator(yaw=rng.uniform(-180,180)if yaw is None else yaw);off=unreal.MathLibrary.transform_location(unreal.Transform(rotation=rot,scale=unreal.Vector(s,s,s)),unreal.Vector((b.min.x+b.max.x)*.5,(b.min.y+b.max.y)*.5,b.min.z));t=unreal.Transform(location=unreal.Vector(x,y,height(x,y)-.6)-off,rotation=rot,scale=unreal.Vector(s,s,s));c.add_instance(t,True);return t
# Reuse existing canonical profiles. Keep source XY, rotation, trainer/dialogue/quest identity.
for label,profile in [('Slice_Waldhueterin_Liora','ElvenArcher'),('Slice_Archivarin_Abzweig','ElvenScholar')]:
 source=actors[label];p=source.get_actor_location();data=unreal.load_asset('/Game/Characters/NPCs/Library/Profiles/DA_NPC_'+profile);assert data and not data.get_validation_errors();cap=source.get_component_by_class(unreal.CapsuleComponent);half=data.reference_height_cm*.5;cap.set_capsule_half_height(half,True);source.set_actor_location(unreal.Vector(p.x,p.y,height(p.x,p.y)+half),False,False);v=own(A.spawn_actor_from_class(unreal.PokeMonsterNPCVisualActor,unreal.Vector(p.x,p.y,height(p.x,p.y)+.5),unreal.Rotator(yaw=-90)),label+'_3D');v.source_actor=source;assert v.apply_presentation(data);v.attach_to_actor(source,unreal.Name(),unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,False);v.refresh_presentation();out['npcs'].append(dict(source=label,profile=data.get_path_name(),xy=[p.x,p.y],height=data.reference_height_cm,idle=data.idle.get_path_name()))
# Existing functional stones keep their interactions, IDs and collision; only sprite presentation changes.
stone=unreal.load_asset('/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_3');stonegroups=[]
for label,h in [('Slice_Ruhepunkt',55),('Slice_Ziel_Alter_Archivstein',95)]:
 source=actors[label];p=source.get_actor_location();c=group(label+'_Stone',stone);plant(c,p.x,p.y,h,45);sprite=source.get_component_by_class(unreal.PaperSpriteComponent);sprite.set_visibility(False);sprite.set_hidden_in_game(True);out['sprites'].append(dict(source=label,replacement=stone.get_path_name(),height=h))
# Clearance checks use mesh bounds in transformed world coordinates, not actor pivots.
# Tall crowns are not ground obstacles; their existing trunks/colliders are audited separately.
for a in list(actors.values()):
 name=a.get_actor_label()
 if a.hidden or a.get_class().get_path_name().startswith('/Script/PokeMonster.')or name.startswith(('V2_House_','WR4_','WOV3_Bridge')):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m or not c.is_visible()or c.hidden_in_game:continue
  kind=m.get_path_name().lower();eligible=any(k in kind for k in ['grass','flower','fern','bush','shrub','stump','small_rock'])
  if not eligible:continue
  b=m.get_bounding_box();n=c.get_instance_count()if isinstance(c,unreal.InstancedStaticMeshComponent)else 1
  for i in range(n):
   t=c.get_instance_transform(i,True)if isinstance(c,unreal.InstancedStaticMeshComponent)else c.get_world_transform();center=unreal.MathLibrary.transform_location(t,(b.min+b.max)*.5);size=b.max-b.min;s=t.scale3d
   # Circumscribed footprint also covers nonzero mesh-origin offsets and arbitrary yaw.
   radius=.5*math.hypot(size.x*s.x,size.y*s.y);x,y=center.x,center.y
   if x>3500 or clear(x,y,radius,10):continue
   # Decorative foreground on a bank/inside garden is deliberately retained unless touching a path or pad.
   if nearest(x,y)[0]>radius+15 and not any(math.hypot(x-cx,y-cy)<pr+radius for cx,cy,pr in pads):continue
   near=nearest(x,y);best=None
   for j in range(100):
    if j<60:
     sign=1 if j%2 else -1;dx,dy=near[3],near[4];ln=math.hypot(dx,dy);dist=near[5]+radius+45+(j//2)*9;nx=near[1]+sign*(-dy/ln)*dist+rng.uniform(-55,55);ny=near[2]+sign*(dx/ln)*dist+rng.uniform(-55,55)
    else:nx=x+rng.uniform(-700,700);ny=y+rng.uniform(-700,700)
    if clear(nx,ny,radius,25):best=(nx,ny);break
   if best is None:out['moves'].append(dict(actor=name,index=i,unresolved=True));continue
   nx,ny=best;old=t.translation.to_tuple();t.translation+=unreal.Vector(nx-x,ny-y,height(nx,ny)-height(x,y))
   if isinstance(c,unreal.InstancedStaticMeshComponent):c.update_instance_transform(i,t,True,True,True)
   else:a.set_actor_location(a.get_actor_location()+t.translation-unreal.Vector(*old),False,False)
   out['moves'].append(dict(actor=name,index=i,from_position=old,to_position=t.translation.to_tuple(),radius=radius))
# Connected meadow drifts, not a uniform grid; five colors reuse the successful V3 flower variants.
floweractors={color:actors['WOV3_Flowers_'+color].get_component_by_class(unreal.InstancedStaticMeshComponent)for color in ['Blue','Violet','Red','Cream','Yellow']};flowers={k:group('Meadow_'+k,c.static_mesh,[c.get_material(i)for i in range(c.get_num_materials())])for k,c in floweractors.items()}
patches=[(-4900,-2300,720,430,560),(-5200,-1550,440,330,220),(-3750,-2400,570,370,330),(-2500,-2600,480,300,240),(-5100,750,420,300,180),(-3300,2600,480,270,180),(-1950,2570,440,230,160),(1700,2300,470,380,220),(2100,-700,360,380,180)]
colors=list(flowers)
for cx,cy,rx,ry,count in patches:
 for i in range(count):
  angle=rng.random()*math.tau;r=math.sqrt(rng.random());x=cx+rx*r*math.cos(angle);y=cy+ry*r*math.sin(angle)
  if not clear(x,y,27,20):continue
  # Related colors cluster gently; red/white/yellow accents remain present in all meadows.
  dominant=int((math.sin(x*.008)+math.cos(y*.009)+2)*1.1)%5;color=colors[dominant]if rng.random()<.62 else rng.choice(colors);plant(flowers[color],x,y,rng.uniform(24,43))
# Four modest walk-through patches wholly inside existing land habitats, well away from roads/doors.
fields=[('WestMeadow',-4950,-2100,300,220),('WestForest',-4880,1430,270,210),('ForestEdge',-2300,1400,160,160),('NorthGlade',-2250,2620,250,145)]
shrubsource=actors['FAT_FabShrubs'].get_component_by_class(unreal.InstancedStaticMeshComponent);bushmesh=shrubsource.static_mesh;materials=[shrubsource.get_material(i)for i in range(shrubsource.get_num_materials())]
for ix,(zone,cx,cy,rx,ry)in enumerate(fields):
 assert clear(cx,cy,math.hypot(rx,ry)+40,0),(zone,'field too close to route')
 c=group('BushField_'+zone,bushmesh,materials)
 for x in range(int(cx-rx+35),int(cx+rx-25),67):
  for y in range(int(cy-ry+35),int(cy+ry-25),67):plant(c,x+rng.uniform(-19,19),y+rng.uniform(-19,19),rng.uniform(48,66))
 z=own(A.spawn_actor_from_class(unreal.PokeMonsterWildEncounterZone,unreal.Vector(cx,cy,height(cx,cy)+100)),'Encounter_'+zone);z.set_editor_property('distance_based_bush_encounters',True);z.set_editor_property('habitat_zone_id',zone);z.set_editor_property('seed',260511+ix*73);z.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(rx,ry,180),True);z.get_component_by_class(unreal.StaticMeshComponent).set_visibility(False);z.get_component_by_class(unreal.StaticMeshComponent).set_hidden_in_game(True);z.get_component_by_class(unreal.TextRenderComponent).set_visibility(False);z.get_component_by_class(unreal.TextRenderComponent).set_hidden_in_game(True);out['fields'].append(dict(actor=z.get_actor_label(),habitat=zone,center=[cx,cy],extent=[rx,ry],seed=z.get_editor_property('seed')))
# Short, irregular clusters guide routes without forming a map-edge wall. One capsule per shrub.
barriers=[(-5400,550,25,5),(-2900,1770,80,4),(1750,850,25,4),(1900,-480,100,4),(-3600,-2750,10,4)]
large=group('BoundaryShrubs',bushmesh,materials)
for k,(cx,cy,yaw,count)in enumerate(barriers):
 for i in range(count):
  x=cx+(i-(count-1)/2)*100*math.cos(math.radians(yaw))+rng.uniform(-20,20);y=cy+(i-(count-1)/2)*100*math.sin(math.radians(yaw))+rng.uniform(-20,20)
  if not clear(x,y,95,40):continue
  h=rng.uniform(145,185);plant(large,x,y,h);a=own(A.spawn_actor_from_class(unreal.Actor,unreal.Vector(x,y,height(x,y)+h*.44)),'BoundaryCollision_'+str(k)+'_'+str(i));cap=component(a,unreal.CapsuleComponent);cap.set_capsule_size(57,h*.44,True);cap.set_collision_profile_name('BlockAll');cap.set_editor_property('generate_overlap_events',False);out['barriers'].append(dict(actor=a.get_actor_label(),center=[x,y],radius=57,height=h))
cut=actors['V2_House_HouseCutaway'];removed=[a for a in cut.occluding_actors if a and a.get_actor_location().x>15000];cut.occluding_actors=[a for a in cut.occluding_actors if a and a not in removed];cut.set_editor_property('stable_doorway_transition',True);cut.doorway_landing_distance=150.;cut.set_editor_property('constrain_third_person_to_room',True);cut.interior_camera_boundary_margin=85.
for a in removed:
 a.set_actor_hidden_in_game(False)
 for c in a.get_components_by_class(unreal.PrimitiveComponent):c.set_visibility(True);c.set_hidden_in_game(False);c.set_custom_primitive_data_float(0,0.)
out['healer']=dict(removed_remote_occluders=[a.get_actor_label()for a in removed],landing_cm=150,camera_margin_cm=85,exterior_camera_unchanged=True)
for row in out['groups']:
 a=next(a for a in A.get_all_level_actors()if a.get_actor_label()==row['label']);row['count']=a.get_component_by_class(unreal.InstancedStaticMeshComponent).get_instance_count()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'Author.json').write_text(json.dumps(out,indent=2));print({k:len(v)if isinstance(v,list)else v for k,v in out.items()})
