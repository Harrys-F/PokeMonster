"""Strict V5 contract: only approved floor/decor/material/understory changes; original gameplay and outside renderer preserved."""
import unreal,json,sys,copy,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV5';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene

def canonical(x):
 if isinstance(x,dict):
  y={k:canonical(v)for k,v in x.items()}
  if 'components'in y:y['components']=sorted([c for c in y['components'] if not(c['name']=='NPCStaticVisual' and c['props'].get('static_mesh')in[None,'None'])],key=lambda c:c['name'])
  return y
 if isinstance(x,list):return [canonical(v)for v in x]
 if isinstance(x,float)and x==0:return 0.0
 return x

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
I=json.loads((R/'Art/HealingHouse/ArtV5_Interior.json').read_text());P=json.loads((R/'Art/World/VisualV2WorldArtV7/ArtV5_Landscape.json').read_text());F=json.loads((R/'Art/HealingHouse/ArtV5_ReviewFinish.json').read_text());a=canonical(scene(w));live={x.get_name():x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};scoped=False;changed=[]
if (S/'BeforeScene.json').exists():
 b=canonical(json.loads((S/'BeforeScene.json').read_text()));assert a['world_settings']==b['world_settings'];removed={x['actor']for x in I['removed_stone_actors']+P['removed_fences']};added={x['actor']for x in I['new_actors']};assert set(b['actors'])-set(a['actors'])==removed and set(a['actors'])-set(b['actors'])==added
 binds={}
 for row in I['material_bindings']+P['bindings']+F['material_bindings']:binds.setdefault(row['actor'],[]).append(row)
 floors={x['actor']:x for x in I['floor_changes']};groups={}
 for row in P['groups']+F['group_adjustments']:
  assert row['actor'] not in groups;groups[row['actor']]=row
 for n,old in b['actors'].items():
  if n in removed:continue
  actual=a['actors'][n];after=copy.deepcopy(actual)
  if after==old:continue
  changed.append(old['label']);assert n in binds or n in floors or n in groups or old['label']=='V2_House_InteriorDiffuse',old['label']
  if n in floors:
   assert after['transform'][0]==old['transform'][0] and after['transform'][1]==old['transform'][1] and after['transform'][2]==[2.,2.,1.];after['transform'][2]=old['transform'][2]
  for c in after['components']:
   c0=next(x for x in old['components']if x['name']==c['name']);assert c.get('collision')==c0.get('collision')
   if n in floors:
    assert c['props'].get('static_mesh')=='/Engine/BasicShapes/Plane.Plane';c['props']['static_mesh']=c0['props']['static_mesh'];c['transform']=c0['transform']
   for row in binds.get(n,[]):
    if row['component']!=c['name']:continue
    assert c['materials'][row['slot']]==row['after'];c['materials'][row['slot']]=row['before']
   if n in groups and 'instances'in c:
    assert len(c['instances'])==len(c0['instances'])==groups[n]['count'];allowed={x['index']:x for x in groups[n]['changed_instances']}
    for index,(now,prev)in enumerate(zip(c['instances'],c0['instances'])):
     if now==prev:continue
     assert index in allowed,(n,index);row=allowed[index]
     for field,slot in [('position',0),('scale',2)]:assert max(abs(v-u)for v,u in zip(now[slot],row['after'][field]))<.001,(n,index,field)
     c['instances'][index]=prev
   if old['label']=='V2_House_InteriorDiffuse' and 'intensity'in c['props']:assert float(c['props']['intensity'])==1000.;c['props']['intensity']=c0['props']['intensity']
  if after!=old:(S/'ScopeDifference.json').write_text(json.dumps({'before':old,'normalized_after':after},indent=2))
  assert after==old,('UNAPPROVED_CHANGE',old['label'])
 scoped=True
assert not any(isinstance(c,unreal.StaticMeshComponent)and c.static_mesh and c.static_mesh.get_name()=='SM_HH4_FlagstoneApron' for obj in live.values()for c in obj.get_components_by_class(unreal.StaticMeshComponent))
h=next(x for x in live.values()if x.get_actor_label()=='V2_House_SilverLady_HealerVisual');assert h.visual.get_material(0).get_path_name()==I['original_silverlady_material'];assert h.visual.get_skeletal_mesh_asset().get_name()=='SK_WestlandHealer_ArtV4';assert h.source_actor.get_actor_location().to_tuple()==(17230.,420.,62.);assert h.visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
for row in I['new_actors']:
 obj=live[row['actor']];c=obj.static_mesh_component;assert not c.cast_shadow;channels=c.get_editor_property('lighting_channels');assert not channels.channel0 and channels.channel1;assert c.get_collision_enabled()==(unreal.CollisionEnabled.QUERY_AND_PHYSICS if row['collision']else unreal.CollisionEnabled.NO_COLLISION)
light=next(x for x in live.values()if x.get_actor_label()=='V2_House_InteriorDiffuse').get_component_by_class(unreal.RectLightComponent);assert light.source_width==1200 and light.source_height==1000 and light.indirect_lighting_intensity==0 and not light.cast_shadows
signature={'schema':1,'map':'/Game/Maps/Dev_TestMap_VisualV2','actors':{n:digest(o)for n,o in a['actors'].items()},'world_settings':a['world_settings']};path=R/'Tools/ProjectMaintenance/ArtV5Signatures.json'
if path.exists():assert json.loads(path.read_text())==signature,'V5 required scene signature differs'
else:assert scoped;path.write_text(json.dumps(signature,indent=2))
(S/'FinalScene.json').write_text(json.dumps(a,indent=2));(S/'ScopeValidation.json').write_text(json.dumps({'passed':True,'detailed_before_after':scoped,'changed_existing_labels':changed,'removed_actors':len(I['removed_stone_actors'])+len(P['removed_fences']),'new_actors':len(I['new_actors']),'original_silverlady_material':I['original_silverlady_material'],'stone_floor_instances':0,'gameplay_old_collisions_outside_lighting_shadow_camera_and_aa_preserved':True},indent=2));unreal.log('ART_V5_SCOPE_PASS')
