"""Read final scene invariants and original actor identities; no asset/map writes."""
import unreal,json,sys,collections
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((D/'Dev_WestlandRegion_Before.json').read_text());after=scene(W);assert set(before['actors'])<=set(after['actors']);assert before['world_settings']==after['world_settings'];changed=[];instanced=[];allowed_props={'HouseCutaway','WR_Visual_HouseHealer'}
for key,row in before['actors'].items():
 now=after['actors'][key];assert row['class']==now['class']and row['transform']==now['transform'],(row['label'],'original actor moved/replaced')
 if row['props']!=now['props']:assert row['label']in allowed_props,(row['label'],'unexpected actor properties',row['props'],now['props'])
 prior={c['name']:c for c in row['components']};current={c['name']:c for c in now['components']};assert set(prior)==set(current),(row['label'],'source component removed/added')
 for name,c in prior.items():
  v=current[name];assert c['transform']==v['transform'],(row['label'],name,'original component transform');assert c.get('collision')==v.get('collision'),(row['label'],name,'collision changed')
  if c.get('instances')!=v.get('instances'):assert row['label'].startswith('WEP_Wildflowers_');instanced.append(row['label'])
 if row!=now:changed.append(row['label'])
actors={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)};classes=collections.Counter(a.get_class().get_name()for a in actors.values());assert classes['PokeMonsterBuildingCutaway']==12 and classes['PokeMonsterNPC']==3 and classes['PokeMonsterNPCVisualActor']==4 and classes['PokeMonsterRestPoint']==1 and classes['PokeMonsterHabitatZone']==16 and classes['PokeMonsterWildEncounterZone']==4
for a in actors.values():
 if isinstance(a,unreal.PokeMonsterNPCVisualActor):assert a.source_actor and a.idle_animation and a.visual.skeletal_mesh_asset and a.visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
cut=actors['HouseCutaway'];assert cut.get_editor_property('stable_doorway_transition')and cut.get_editor_property('constrain_third_person_to_room')and cut.get_editor_property('use_shadowless_interior_lighting');walls=[a for n,a in actors.items()if n.startswith(('HH_Expanded_RearWall','HH_Expanded_SideWall','HH_Expanded_FrontWall'))];assert len(walls)==18 and all(a not in cut.occluding_actors and not a.hidden for a in walls)
for a in actors.values():
 assert not a.get_actor_label().startswith(('V6_Interior_','PokemonTestGround','TestGround_'))
 for c in a.get_components_by_class(unreal.StaticMeshComponent):assert not c.static_mesh or '/ModelIntakeV6/'not in c.static_mesh.get_path_name()
# Every current source-bound model keeps its original source identity and display/dialogue data.
for row in json.loads((D/'Inventory.json').read_text())['Dev_WestlandRegion_functional']:
 if row['class_name']not in ['PokeMonsterNPC','PokeMonsterRestPoint']:continue
 a=actors[row['label']]
 for k in ['display_name','dialogue','checkpoint_id']:
  if k in row['properties']:
   v=a.get_editor_property(k);assert (v.get_path_name()if isinstance(v,unreal.Object)else str(v))==row['properties'][k],(row['label'],k)
healer=json.loads((D/'Healer.json').read_text());healer['groups']=[dict(name=n,instances=a.get_component_by_class(unreal.InstancedStaticMeshComponent).get_instance_count())for n,a in actors.items()if n.startswith('WVI_Healer_V6_Interior_')];assert len(healer['groups'])==7;(D/'Healer.json').write_text(json.dumps(healer,indent=2));(D/'Dev_WestlandRegion_After.json').write_text(json.dumps(after,indent=2));(D/'SceneAudit.json').write_text(json.dumps(dict(passed=True,original_actors=len(before['actors']),current_actors=len(after['actors']),all_original_transforms_and_collisions_retained=True,changed=changed,instance_groups_with_targeted_variation=sorted(set(instanced)),classes=dict(classes),wall_count=len(walls),test_ground_not_copied=True,npc_identities_retained=True),indent=2));print('WESTLAND_VI_AUDIT_OK',len(before['actors']),len(after['actors']),len(changed))
