"""Required V4 actor signatures and explicit gameplay/camera/collision scope; no media prerequisite."""
import unreal,json,sys,hashlib,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def numeric_zero(v):
 if isinstance(v,dict):return {k:numeric_zero(x) for k,x in v.items()}
 if isinstance(v,list):return [numeric_zero(x) for x in v]
 if isinstance(v,float) and v==0:return 0.0
 return v
def canonical(j):
 for a in j['actors'].values():
  a['components']=[c for c in a['components'] if not (c['name']=='NPCStaticVisual' and c['props'].get('static_mesh') in [None,'None'])]
  a['components'].sort(key=lambda c:c['name'])
 return numeric_zero(j)
def digest(a):return hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':')).encode()).hexdigest()
a=canonical(scene(w));actors={a.get_name():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};I=json.loads((R/'Art/HealingHouse/ArtV4_Interior.json').read_text());P=json.loads((R/'Art/World/VisualV2WorldArtV7/ArtV4_Landscape.json').read_text());H=json.loads((R/'Art/Characters/NPCs/SilverLady/ArtV4_Unreal.json').read_text());sig=R/'Tools/ProjectMaintenance/ArtV4Signatures.json';scoped=False;changed=[]
if (S/'BeforeScene.json').exists():
 b=canonical(json.loads((S/'BeforeScene.json').read_text()));assert a['world_settings']==b['world_settings'];expected=set(I['new_actors'])|{g['actor'] for g in P['groups']}|set(P['fences']);assert set(a['actors'])-set(b['actors'])==expected and set(b['actors'])<=set(a['actors'])
 moves={x['name']:x for x in json.loads((R/'Art/HealingHouse/ArtV4_FurnitureMoves.json').read_text())};bindings={x['actor'] for x in I['material_bindings']};rugnames={'V2_House_HH_Art_MainRunner','V2_House_HH_Art_WaitingRug'}
 for n,before in b['actors'].items():
  after=copy.deepcopy(a['actors'][n]);label=before['label']
  if after==before:continue
  changed.append(label);assert (n in bindings or n in moves or label in rugnames or label in ['V2_House_HH_Art_BannerReception','V2_House_InteriorDiffuse','V2_House_SilverLady_HealerVisual']),('UNEXPECTED_ACTOR_CHANGE',label)
  if label in rugnames:after['transform']=before['transform']
  if n in moves:assert after['transform'][0]==moves[n]['after'];after['transform']=before['transform']
  if label=='V2_House_SilverLady_HealerVisual':
   assert after['props']['source_actor']==before['props']['source_actor'];after['transform']=before['transform'];after['props']['idle_animation']=before['props']['idle_animation'];after['components']=[c for c in after['components'] if c['name']!='NPCStaticVisual'];before=copy.deepcopy(before);before['components']=[c for c in before['components'] if c['name']!='NPCStaticVisual']
  if label=='V2_House_HH_Art_BannerReception':assert after['props']['hidden']=='True';after['props']['hidden']=before['props']['hidden']
  for c0 in before['components']:
   c=next(c for c in after['components'] if c['name']==c0['name']);assert c.get('collision')==c0.get('collision') and c.get('instances')==c0.get('instances'),label
   if label in rugnames or n in moves or label=='V2_House_SilverLady_HealerVisual':c['transform']=c0['transform']
   if n in bindings or label in rugnames or label=='V2_House_SilverLady_HealerVisual':
    if 'materials'in c:c['materials']=c0['materials']
    for k in ['static_mesh','skeletal_mesh_asset']:
     if k in c0['props']:c['props'][k]=c0['props'][k]
   if label in rugnames:
    c['transform']=c0['transform']
   if label in ['V2_House_HH_Art_BannerReception','V2_House_SilverLady_HealerVisual']:c['props']['visible']=c0['props']['visible']
   if label=='V2_House_InteriorDiffuse' and 'intensity'in c['props']:c['props']['intensity']=c0['props']['intensity']
  if after!=before:(S/'ScopeDifference.json').write_text(json.dumps({'label':label,'before':before,'normalized_after':after},indent=2))
  assert after==before,('NON_VISUAL_CHANGE',label)
 scoped=True
for row in json.loads((R/'Art/HealingHouse/ArtV4_HearthPlacement.json').read_text()):assert actors[row['actor']].get_actor_location().to_tuple()==tuple(row['position'])
v=actors[H['actor']];assert v.source_actor.get_actor_location().to_tuple()==(17230.,420.,62.) and v.idle_animation and abs(v.idle_animation.get_play_length()-4)<.05;assert v.visual.get_skeletal_mesh_asset().get_path_name()==H['mesh'] and v.visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
for g in P['groups']:
 c=actors[g['actor']].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c.get_instance_count()==g['count'] and not c.cast_shadow and c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
for n in I['new_actors']:
 obj=actors[n]
 for c in obj.get_components_by_class(unreal.PrimitiveComponent):
  ch=c.get_editor_property('lighting_channels');assert not c.cast_shadow and not ch.channel0 and ch.channel1
  expected=unreal.CollisionEnabled.QUERY_AND_PHYSICS if any(obj.get_actor_label().startswith('ArtV4_'+k+'_') for k in ['Hearth','RemedyCabinet']) else unreal.CollisionEnabled.NO_COLLISION;assert c.get_collision_enabled()==expected
for row in json.loads((R/'Art/World/VisualV2WorldArtV7/ArtV4_PathGraphs.json').read_text()):
 m=unreal.load_asset(row['material']);n=next(n for n in unreal.MaterialEditingLibrary.get_material_expressions(m) if n.get_name()==row['expression']);assert n.get_editor_property('code')==row['after']
result={'schema':1,'map':'/Game/Maps/Dev_TestMap_VisualV2','actors':{n:digest(o) for n,o in a['actors'].items()},'world_settings':a['world_settings']}
if sig.exists():assert json.loads(sig.read_text())==result,'Required V4 signatures differ'
else:assert scoped;sig.write_text(json.dumps(result,indent=2))
(S/'FinalScene.json').write_text(json.dumps(a,indent=2));(S/'ScopeValidation.json').write_text(json.dumps({'passed':True,'detailed_before_after':scoped,'changed_existing_labels':changed,'new_actors':len(I['new_actors'])+len(P['groups'])+len(P['fences']),'new_landscape_instances':P['new_instances'],'existing_gameplay_camera_route_collisions_and_exterior_lights_preserved':True},indent=2));unreal.log('ART_V4_SCOPE_PASS')
