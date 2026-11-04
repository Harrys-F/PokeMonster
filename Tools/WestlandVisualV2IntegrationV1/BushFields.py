"""Four existing-habitat V5 fields and a few safe boundary shrub clusters; same global rules."""
import unreal,runpy,json,math,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/Common.py')));assert not(D/'BushFields.json').exists();zones={str(a.zone_id):a for a in actors.values()if isinstance(a,unreal.PokeMonsterHabitatZone)};paths=[(L.sample(p,spacing=2),w)for _,p,w in L.PATHS]+[(L.sample(p['points_m'],spacing=2),p['width_m'])for p in json.loads((R/'Art/World/WestlandRegion/WestlandRegion_Access.json').read_text())];terrain=[a for n,a in actors.items()if n.startswith('WR_Terrain_')];ignore=[a for a in actors.values()if a not in terrain];fields=[];boundaries=[];mesh='/Game/StyleHex_Studio/Free_Packs/FREE_Stylized_Grass_Flowers_Foliage/Meshes/SM_Fol_Bush_1';material=ROOT+'/Materials/MI_WI_FieldShrubs';large=group('BoundaryShrubs',mesh,[material],False,7000)
def road(e,n):return min(math.hypot(e-x,n-y)-w*.5 for ps,w in paths for x,y in ps)
def safe(e,n,margin):
 if road(e,n)<margin:return False
 if abs(e-L.river(n))<10+margin:return False
 for b in L.buildings():
  if math.hypot(e-b['place'][0],n-b['place'][1])<max(b['size'])/2+margin+4:return False
 for a in actors.values():
  if isinstance(a,(unreal.PokeMonsterNPC,unreal.PokeMonsterRestPoint,unreal.PokeMonsterWorldItem)):
   x,y=L.en(a.get_actor_location().x,a.get_actor_location().y)
   if math.hypot(e-x,n-y)<margin+4:return False
 return True
def ground(e,n):
 x,y,_=L.world(e,n);hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,16000),unreal.Vector(x,y,-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit,(e,n);z=float(re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text())[1]);return unreal.Vector(x,y,z)
def plant(c,e,n,h):
 b=c.static_mesh.get_bounding_box();scale=h/(b.max.z-b.min.z);t=unreal.Transform(rotation=unreal.Rotator(yaw=rng.uniform(-180,180)),scale=unreal.Vector(scale,scale,scale));offset=unreal.MathLibrary.transform_location(t,unreal.Vector((b.min.x+b.max.x)*.5,(b.min.y+b.max.y)*.5,b.min.z));t.translation=ground(e,n)-offset;c.add_instance(t,True)
for k,(name,e,n)in enumerate([('Westland_Hofwiese',-288,-181),('Westland_Wildwiesen',145,25),('Westland_Waldrand',178,65),('Westland_Waldruinen',239,175)]):
 assert safe(e,n,4.5),(name,'Protected route/mission too near');zone=zones[name];p=ground(e,n);c=group('BushField_'+name,mesh,[material],False,7000);ext=unreal.Vector(260,180,180)
 for sx in [-1,1]:
  for sy in [-1,1]:
   local=unreal.MathLibrary.inverse_transform_location(zone.bounds.get_world_transform(),p+unreal.Vector(sx*ext.x,sy*ext.y,0));ze=zone.bounds.get_unscaled_box_extent();assert abs(local.x)<ze.x and abs(local.y)<ze.y,(name,'Outside existing habitat')
 for i in range(-3,4):
  for j in range(-2,3):plant(c,e+i*.52+rng.uniform(-.1,.1),n+j*.52+rng.uniform(-.1,.1),rng.uniform(48,66))
 a=own('Encounter_'+name,unreal.PokeMonsterWildEncounterZone,p+unreal.Vector(0,0,100));a.set_editor_property('distance_based_bush_encounters',True);a.set_editor_property('habitat_zone_id',name);a.set_editor_property('encounter_id','Westland.Bush.'+name);a.set_editor_property('seed',260411+k*73);a.get_component_by_class(unreal.BoxComponent).set_box_extent(ext,True)
 for comp in a.get_components_by_class(unreal.StaticMeshComponent)+a.get_components_by_class(unreal.TextRenderComponent):comp.set_visibility(False);comp.set_hidden_in_game(True)
 fields.append(dict(actor=a.get_actor_label(),habitat=name,center=p.to_tuple(),en=[e,n],extent=ext.to_tuple(),plants=c.get_instance_count(),road_clearance_m=road(e,n)))
 # Boundary bushes sit beyond the field, never on a route or a functional target.
 for i in range(4):
  be=e+7.5+i*.95;bn=n+6.0+.35*math.sin(i)
  if not safe(be,bn,2):continue
  p=ground(be,bn);h=rng.uniform(150,185);plant(large,be,bn,h);coll=own('BoundaryCollision_'+str(k)+'_'+str(i),location=p+unreal.Vector(0,0,h*.44));cap=component(coll,unreal.CapsuleComponent);cap.set_capsule_size(57,h*.44,True);cap.set_collision_profile_name('BlockAll');cap.set_editor_property('generate_overlap_events',False);boundaries.append(dict(actor=coll.get_actor_label(),center=p.to_tuple(),radius=57,height=h,road_clearance_m=road(be,bn)))
assert len(fields)==4;finish('BushFields.json',dict(fields=fields,boundaries=boundaries,global_chance_cooldown_population_rules_unchanged=True,new_wild_species=False))
