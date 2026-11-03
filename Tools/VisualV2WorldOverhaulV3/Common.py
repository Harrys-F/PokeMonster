import unreal,json,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';ROOT='/Game/Environment/VisualV2WorldOverhaulV3';ML=unreal.MaterialEditingLibrary;A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();actors={a.get_actor_label():a for a in A.get_all_level_actors()};SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups={};changes=[];rng=random.Random(2611033)
paths=json.loads((R/'Tools/VisualV2FabAssetTrialV1/ExistingPaths.json').read_text());segments=[(a,b)for p in paths.values()for a,b in zip(p,p[1:])]
def segment(x,y,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/max(1,dx*dx+dy*dy)));return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def pd(x,y):return min(segment(x,y,a,b)for a,b in segments)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
mounds=[(-1120,620,20,350),(-900,800,40,350),(-620,1010,60,450),(-5500,-2750,42,380),(2300,2400,65,400),(2300,-2800,38,370)]
def height(x,y):return max(h*(1-smooth((math.hypot(x-cx,y-cy)/r-.45)/.55))for cx,cy,h,r in mounds)
def forest(x,y):return max(max(0,1-((x-cx)/rx)**2-((y-cy)/ry)**2)for cx,cy,rx,ry in [(-4900,1700,1200,1250),(-2700,2300,1300,650),(1500,1400,1100,1350),(1850,-750,700,1000)])
def safe(x,y,margin=150):
 if not(-5750<x<2750 and -3000<y<2900)or pd(x,y)<margin:return False
 if ((x-720)/1040)**2+((y+1800)/790)**2<1:return False
 if min(segment(x,y,(-910,-320),(1100,-320)),segment(x,y,(720,-320),(720,-680)))<160:return False
 if ((x+3100)/710)**2+((y-500)/680)**2<1 or((x+2750)/620)**2+((y+1020)/430)**2<1 or((x-1080)/370)**2+((y-900)/360)**2<1:return False
 return not any(math.hypot(x-p.x,y-p.y)<100 for a in actors.values()if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterWorldItem,unreal.PokeMonsterRestPoint))for p in[a.get_actor_location()])
def group(key,path,mats=None,shadow=False,collision='NoCollision'):
 if key in groups:return groups[key]
 mesh=unreal.load_asset(path);assert mesh,path;a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WOV3_'+key);a.set_folder_path('VisualV2/WorldOverhaulV3');a.tags=['VisualV2WorldOverhaulV3'];h,r=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,r;c.set_static_mesh(mesh)
 if mats:
  for i,v in enumerate(mats):c.set_material(i,unreal.load_asset(v)if isinstance(v,str)else v)
 c.set_collision_profile_name(collision);c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_editor_property('affect_distance_field_lighting',shadow);c.set_cull_distances(6000,8000);groups[key]=c;return c
def put(c,x,y,h,yaw=None,z=None):
 b=c.static_mesh.get_bounding_box();s=h/max(1,b.max.z-b.min.z);p=height(x,y)if z is None else z;c.add_instance(unreal.Transform(location=unreal.Vector(x,y,p-b.min.z*s-.7),rotation=unreal.Rotator(yaw=rng.uniform(0,360)if yaw is None else yaw),scale=unreal.Vector(s,s,s)),True)
def save(name,extra=None):
 dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name().startswith(ROOT+'/')for p in dirty),[p.get_path_name()for p in dirty]
 for p in dirty:assert unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(p.get_path_name()),False)
 assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2');out=dict(changes=changes,groups=[dict(label='WOV3_'+k,count=c.get_instance_count(),mesh=c.static_mesh.get_path_name())for k,c in groups.items()]);out.update(extra or{});(D/name).write_text(json.dumps(out,indent=2))
