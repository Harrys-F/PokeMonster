"""Reconstruct approved before visuals only in an owned disposable runtime world."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2'
def prepare(world):
 assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
 before=json.loads((D/'SceneBefore.json').read_text())['actors'];audit=json.loads((D/'GeometryAudit.json').read_text());auth=json.loads((D/'Authored.json').read_text());bank=json.loads((D/'BankViewCorrection.json').read_text());current={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor)};temp=[];restore=[]
 def transform(v):return unreal.Transform(location=unreal.Vector(*v[0]),rotation=unreal.Quat(*v[1]).rotator(),scale=unreal.Vector(*v[2]))
 bank_ids={x['name']for x in bank};ids={x['name']for x in auth['removed']}|bank_ids;sprites={x['name']:x for x in audit['sprites']if x['name']in {z['name']for z in auth['replaced_sprites']}}
 for name in sorted(ids|set(sprites)):
  row=before[name];tr=transform(row['transform'])
  if name in sprites:
   path=sprites[name]['sprite']
   if not path:continue
   a=unreal.get_default_object(unreal.GameplayStatics).call_method('BeginDeferredActorSpawnFromClass',(world,unreal.PaperSpriteActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));unreal.get_default_object(unreal.GameplayStatics).call_method('FinishSpawningActor',(a,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));c=a.render_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_sprite(unreal.load_asset(path))
  else:
   cr=next(c for c in row['components']if c['props'].get('static_mesh'));a=unreal.get_default_object(unreal.GameplayStatics).call_method('BeginDeferredActorSpawnFromClass',(world,unreal.StaticMeshActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));unreal.get_default_object(unreal.GameplayStatics).call_method('FinishSpawningActor',(a,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));c=a.static_mesh_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);assert c.set_static_mesh(unreal.load_asset(cr['props']['static_mesh']))
  c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_cast_shadow(row['components'][0]['props'].get('cast_shadow')=='True')
  original=row['components'][0]
  for i,path in enumerate(original.get('materials',[])):
   if path:c.set_material(i,unreal.load_asset(path))
  c.set_visibility(True);c.set_hidden_in_game(False);c.set_mobility(unreal.ComponentMobility.STATIC);assert math.dist(a.get_actor_location().to_tuple(),row['transform'][0])<.01;assert math.dist(a.get_actor_scale3d().to_tuple(),row['transform'][2])<.001;a.set_actor_hidden_in_game(True);temp.append(a)
  if name not in sprites:assert c.static_mesh.get_path_name()==cr['props']['static_mesh']
 for x in bank:restore.append(current[before[x['name']]['label']])
 ground=current['V2_Ground'];old=unreal.load_asset(next(c for c in before[next(n for n,r in before.items()if r['label']=='V2_Ground')]['components']if c.get('materials'))['materials'][0]);new=ground.static_mesh_component.get_material(0);groups=[a for a in current.values()if a.actor_has_tag('VisualV2EnvironmentPolishV2')]
 def apply(variant):
  assert variant in ['Before','After'];after=variant=='After';ground.static_mesh_component.set_material(0,new if after else old)
  for a in groups:a.set_actor_hidden_in_game(not after)
  for a in temp:a.set_actor_hidden_in_game(after)
  for a in restore:a.set_actor_hidden_in_game(not after)
  assert all(a.get_editor_property('hidden')==after for a in temp)and all(a.get_editor_property('hidden')==(not after)for a in groups+restore)
  with(D/'RuntimeReferenceChecks.jsonl').open('a')as f:f.write(json.dumps(dict(variant=variant,stationary_reference_actors=len(temp),new_groups=len(groups),original_bank_actors=len(restore),ground_material=ground.static_mesh_component.get_material(0).get_path_name(),visibility_verified=True))+'\n')
 return apply
