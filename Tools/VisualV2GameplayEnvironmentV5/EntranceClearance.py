"""Supplemental V5 pass: relocate only existing ground-level house grass off routes; retain plants and original assets."""
import unreal,json,math,random,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();actors={a.get_actor_label():a for a in A.get_all_level_actors()};rng=random.Random(51103);out=dict(npcs=[],sprites=[],moves=[],groups=[],fields=[],barriers=[],healer={});SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
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
for a in list(actors.values()):
 name=a.get_actor_label()
 if a.hidden or not name.startswith('V2_House_'):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  m=c.static_mesh
  if not m or not c.is_visible()or c.hidden_in_game:continue
  kind=m.get_path_name().lower();eligible='grass'in kind
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
   out['moves'].append(dict(actor=name,component=c.get_name(),index=i,from_position=old,to_position=t.translation.to_tuple(),radius=radius))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');(D/'EntranceClearance.json').write_text(json.dumps(out['moves'],indent=2));print('Ground-level entrance grass relocated',len(out['moves']))
