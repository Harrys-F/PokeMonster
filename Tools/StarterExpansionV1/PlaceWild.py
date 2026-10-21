"""Add exactly two native visible encounters; preserve every pre-existing actor/component."""
import unreal,json,hashlib,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/StarterExpansionV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world()
def clean():return not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert clean() and not(O/'WildPlacement.json').exists()
def stable(value):return re.sub(r'0x[0-9a-fA-F]+','ADDRESS',str(value))
def snapshot():
 rows={}
 for a in A.get_all_level_actors():
  cs=[]
  for c in a.get_components_by_class(unreal.SceneComponent):
   d={'name':c.get_name(),'class':c.get_class().get_name(),'transform':stable(c.get_world_transform())}
   if isinstance(c,unreal.PrimitiveComponent):d.update(collision=str(c.get_collision_enabled()),profile=str(c.get_collision_profile_name()),shadow=c.cast_shadow)
   if isinstance(c,unreal.MeshComponent):d['materials']=[m.get_path_name()if m else None for m in c.get_materials()]
   if isinstance(c,unreal.StaticMeshComponent):d['mesh']=c.static_mesh.get_path_name()if c.static_mesh else None
   if isinstance(c,unreal.LightComponent):d.update(intensity=c.intensity,color=stable(c.light_color))
   cs.append(d)
  rows[a.get_path_name()]={'label':a.get_actor_label(),'class':a.get_class().get_name(),'transform':stable(a.get_actor_transform()),'tags':[str(t)for t in a.tags],'components':cs}
 return rows
before=snapshot();mapfile=R/'Content/Maps/Dev_TestMap_VisualV2.umap';oldhash=hashlib.sha256(mapfile.read_bytes()).hexdigest();rows=[]
for name,radius,hh,seed,points in [('Schiggy',30.,30.,7217,[(420,-1050),(650,-1050),(990,-850),(400,-800)]),('Bisasam',38.,38.,7218,[(-700,250),(-550,650),(-850,450),(150,900)])]:
 ident='Dev_'+name+'_Wild_01';assert all(str(a.get_editor_property('encounter_id'))!=ident for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor))
 species=unreal.load_asset('/Game/Data/Creatures/DA_'+name);profile=unreal.load_asset('/Game/Data/Encounters/DA_'+name+'_Wild');assert species and profile
 a=A.spawn_actor_from_class(unreal.PokeMonsterVisibleWildCreatureActor,unreal.Vector(points[0][0],points[0][1],hh));a.set_actor_label('Slice_Wild_'+name);body=a.get_component_by_class(unreal.CapsuleComponent);body.set_capsule_size(radius,hh,False);a.get_component_by_class(unreal.PaperSpriteComponent).set_relative_location(unreal.Vector(0,0,15-hh),False,False)
 for k,v in dict(profile=profile,visual_species=species,ambient_motion=True,encounter_id=ident,seed=seed).items():a.set_editor_property(k,v)
 movement=a.get_component_by_class(unreal.PokeMonsterCreatureRoamingComponent);chosen=None;attempts=[]
 for x,y in points:
  a.set_actor_location(unreal.Vector(x,y,hh),False,False);movement.configure(species,hh,radius,hh,None,seed);ground=movement.project_walkable(unreal.Vector(x,y,0));attempts.append({'xy':[x,y],'ground':str(ground)})
  if ground is not None:
   # UFUNCTION bool + FVector out is exposed as FVector or None.
   assert isinstance(ground,unreal.Vector),str(ground);chosen=ground;break
 assert chosen is not None,(name,attempts)
 a.set_actor_location(chosen+unreal.Vector(0,0,hh),False,False);rows.append({'species':name,'actor':a.get_path_name(),'id':ident,'location':a.get_actor_location().to_tuple(),'radius':radius,'half_height':hh,'attempts':attempts})
after=snapshot();assert len(after)==len(before)+2;diff={k:{'before':before[k],'after':after[k]}for k in before if before[k]!=after[k]};(O/'WildPlacementActorDiff.json').write_text(json.dumps(diff,indent=2));assert not diff,'Existing actor changed';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');assert clean();(O/'WildPlacement.json').write_text(json.dumps({'rows':rows,'existing_actor_count':len(before),'existing_actors_unchanged':True,'map_sha256_before':oldhash,'map_sha256_after':hashlib.sha256(mapfile.read_bytes()).hexdigest(),'existing_actor_snapshot':before},indent=2));unreal.log('STARTER_WILD_PLACEMENT_PASS')
