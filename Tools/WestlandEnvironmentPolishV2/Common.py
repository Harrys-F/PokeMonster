"""Existing-asset map-local authoring helpers; no runtime subsystem."""
import unreal,json,sys,math,random,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';ROOT='/Game/Environment/WestlandEnvironmentPolishV2';sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
actors={a.get_actor_label():a for a in A.get_all_level_actors()};SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);ML=unreal.MaterialEditingLibrary;barriers=[a for a in actors.values()if a.actor_has_tag('BiomePlayerWaterBarrier')];protected=[L.en(a.get_actor_location().x,a.get_actor_location().y)for a in actors.values()if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterRestPoint,unreal.PokeMonsterWorldItem))];pathgrid={};cache={};groups={};derivations=[]
for _,ps,width in L.PATHS:
 for e,n in L.sample(ps,spacing=2):pathgrid.setdefault((int(e//10),int(n//10)),[]).append((e,n,width))
def path_distance(e,n):
 near=[math.hypot(e-u,n-v)-w*.5 for gx in range(int(e//10)-2,int(e//10)+3)for gy in range(int(n//10)-2,int(n//10)+3)for u,v,w in pathgrid.get((gx,gy),[])];return min(near or[999])
def safe(e,n,margin=1):
 if not(-405<e<405 and -305<n<305)or path_distance(e,n)<margin:return False
 if abs(e-L.river(n))<7.5+margin:return False
 for b in L.buildings():
  if abs(e-b['place'][0])<b['size'][1]*.5+4+margin and abs(n-b['place'][1])<b['size'][0]*.5+4+margin:return False
 for name in ['Heilhaus','Steinkreis','Waldruinen','Ausgang','Lichtung']:
  u,v=L.PLACES[name]
  if math.hypot(e-u,n-v)<16+margin:return False
 return not any(math.hypot(e-u,n-v)<3.5+margin for u,v in protected)
def forest(e,n):
 east=math.exp(-(((e-252)/100)**4+((n-170)/126)**4));west=.75*math.exp(-(((e+365)/38)**4+((n-95)/160)**4));return max(east,west)
def ground(x,y,z):
 hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+6000),unreal.Vector(x,y,z-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,barriers,unreal.DrawDebugTrace.NONE)
 assert hit,(x,y,'missing terrain');m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());assert m;return float(m[1])
def mat(m):
 if isinstance(m,str):m=unreal.load_asset(m)
 p=m.get_path_name()
 if p in cache:return cache[p]
 out=m
 if isinstance(m,unreal.Material)and not m.get_editor_property('used_with_instanced_static_meshes'):
  name='M_WEP_Inst_'+m.get_name();q=ROOT+'/Materials/'+name;out=unreal.load_asset(q)if unreal.EditorAssetLibrary.does_asset_exist(q)else unreal.EditorAssetLibrary.duplicate_asset(p,q);out.set_editor_property('used_with_instanced_static_meshes',True);ML.recompile_material(out);assert unreal.EditorAssetLibrary.save_loaded_asset(out,False)
 elif isinstance(m,unreal.MaterialInstanceConstant):
  parent=mat(m.parent)
  if parent!=m.parent:
   q=ROOT+'/Materials/MI_WEP_Inst_'+m.get_name();out=unreal.load_asset(q)if unreal.EditorAssetLibrary.does_asset_exist(q)else unreal.EditorAssetLibrary.duplicate_asset(p,q);ML.set_material_instance_parent(out,parent);assert unreal.EditorAssetLibrary.save_loaded_asset(out,False)
 if out!=m:derivations.append(dict(source=p,derived=out.get_path_name()))
 cache[p]=out;return out

def group(label,mesh,materials=None,collision=False,shadow=False,cull=7000):
 if label in groups:return groups[label]
 assert 'WEP_'+label not in actors,'Never repeat completed authoring';mesh=unreal.load_asset(mesh)if isinstance(mesh,str)else mesh;assert mesh
 mats=[mat(m)for m in(materials or[x.material_interface for x in mesh.static_materials])];a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('WEP_'+label);a.tags=['WestlandEnvironmentPolishV2'];a.set_folder_path('WestlandRegion/EnvironmentPolishV2');handle,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason
 for i,m in enumerate(mats):c.set_material(i,m)
 c.set_static_mesh(mesh);c.set_collision_profile_name('BlockAll'if collision else'NoCollision');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_IGNORE);c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(shadow);c.set_editor_property('affect_distance_field_lighting',shadow);c.set_cull_distances(int(cull*.85),cull);groups[label]=c;return c

def put(c,e,n,height,yaw,scale=None):
 x,y,z=L.world(e,n,L.height(e,n));g=ground(x,y,z);b=c.static_mesh.get_bounding_box();sc=height/(b.max.z-b.min.z);s=scale or(sc,sc,sc);c.add_instance(unreal.Transform(location=unreal.Vector(x,y,g-b.min.z*s[2]-.8),rotation=unreal.Rotator(yaw=yaw),scale=unreal.Vector(*s)),True);return g

def save(name,extra=None):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Shared source auto-edit; never save originals';assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');data=dict(groups=[dict(label=k,instances=c.get_instance_count(),mesh=c.static_mesh.get_path_name(),materials=[c.get_material(i).get_path_name()for i in range(c.get_num_materials())],collision=str(c.get_collision_enabled()),shadow=c.cast_shadow)for k,c in groups.items()],derivations=derivations,extra=extra);(D/name).write_text(json.dumps(data,indent=2))
