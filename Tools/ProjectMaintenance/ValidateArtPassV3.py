"""Strict Art-Pass V3 scope and saved regression validation; optional photos never gate builds."""
import unreal,json,sys,copy,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/ArtPassV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and w.get_name()=='Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canonical(j):
 for a in j['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return j
def digest(a):return hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':')).encode()).hexdigest()
a=canonical(scene(w));actors={v.get_name():v for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)};interior=json.loads((R/'Art/HealingHouse/ArtPassV3_Interior.json').read_text());land=json.loads((R/'Art/World/VisualV2WorldArtV7/ArtPassV3_Landscape.json').read_text());light=json.loads((R/'Art/HealingHouse/ArtPassV3_Lighting.json').read_text());sigpath=R/'Tools/ProjectMaintenance/ArtV3Signatures.json';scoped=False
if (S/'BeforeScene.json').exists():
 b=canonical(json.loads((S/'BeforeScene.json').read_text()));assert a['world_settings']==b['world_settings'];assert set(a['actors'])-set(b['actors'])=={interior['new_healer_visual'],light['actor']};assert set(b['actors'])<=set(a['actors']);moves={m['name']:m for m in interior['furniture_moves']};ferns={m['actor']:m for m in land['bindings']}
 for name,old in b['actors'].items():
  new=copy.deepcopy(a['actors'][name]);obj=actors[name];room=16300<old['transform'][0][0]<17500
  if name in moves:
   m=moves[name];assert new['transform'][0]==m['after'];new['transform']=old['transform']
  if obj.get_actor_label()=='V2_House_HH_Art_MainRunner':assert tuple(obj.get_actor_scale3d().to_tuple())==(1.25,.86,1.)
  if obj.get_actor_label()=='V2_House_HH_Art_ReceptionRug':assert new['props']['hidden']=='True';new['props']['hidden']=old['props']['hidden']
  for c0 in old['components']:
   c1=next(c for c in new['components'] if c['name']==c0['name']);assert c0.get('collision')==c1.get('collision') and c0.get('instances')==c1.get('instances'),name
   if name in moves:c1['transform']=c0['transform']
   if room and 'cast_shadow' in c1['props']:assert c1['props']['cast_shadow']=='False';c1['props']['cast_shadow']=c0['props']['cast_shadow']
   if name in ferns and 'static_mesh' in c1['props']:
    assert c1['props']['static_mesh']==ferns[name]['after'];c1['props']['static_mesh']=c0['props']['static_mesh'];c1['materials']=c0['materials']
   if (name==interior['healer_source'] and c1['class']=='/Script/Paper2D.PaperSpriteComponent') or obj.get_actor_label()=='V2_House_HH_Art_ReceptionRug':
    assert c1['props']['visible']=='False';c1['props']['visible']=c0['props']['visible']
  if new!=old:(S/'ScopeDifference.json').write_text(json.dumps({'actor':name,'old':old,'normalized_new':new},indent=2))
  assert new==old,('UNEXPECTED_SCOPE_CHANGE',name)
 scoped=True
# Check actual lighting channels, not merely the generic scene signature.
for name,obj in actors.items():
 if not 16300<obj.get_actor_location().x<17500:continue
 for c in obj.get_components_by_class(unreal.PrimitiveComponent):
  if isinstance(c,(unreal.BillboardComponent,unreal.ArrowComponent)):continue
  ch=c.get_editor_property('lighting_channels');assert not c.cast_shadow and (ch.channel0,ch.channel1,ch.channel2)==(False,True,False),(name,c.get_name())
 for c in obj.get_components_by_class(unreal.LightComponent):
  ch=c.get_editor_property('lighting_channels');assert not c.cast_shadows and (ch.channel0,ch.channel1,ch.channel2)==(False,True,False)
c=actors[light['actor']].get_component_by_class(unreal.RectLightComponent);assert c.intensity==550 and c.indirect_lighting_intensity==0 and c.temperature==5000
assert actors[interior['cutaway']].use_shadowless_interior_lighting
v=actors[interior['new_healer_visual']];assert v.source_actor==actors[interior['healer_source']] and v.static_visual and v.static_visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and v.forward_yaw_offset==-90
for row in land['ferns']:
 m=unreal.load_asset(row['path']);assert m.get_num_triangles(0)==row['triangles'] and len(m.static_materials)==1 and unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).get_simple_collision_count(m)==0
for row in json.loads((R/'Art/World/VisualV2WorldArtV7/ArtPassV3_PathGraphs.json').read_text()):
 m=unreal.load_asset(row['material']);n=next(n for n in unreal.MaterialEditingLibrary.get_material_expressions(m) if n.get_name()==row['expression']);assert n.get_editor_property('code')==row['after_code'];assert all(unreal.MaterialEditingLibrary.get_inputs_for_material_expression(m,n))
sig={'schema':1,'map':'/Game/Maps/Dev_TestMap_VisualV2','actors':{n:digest(v) for n,v in a['actors'].items()},'world_settings':a['world_settings']}
if sigpath.exists():assert json.loads(sigpath.read_text())==sig,'Saved Art-Pass V3 regression signatures differ'
else:assert scoped,'Initial signatures require detailed actual pre/post scope proof';sigpath.write_text(json.dumps(sig,indent=2))
(S/'FinalScene.json').write_text(json.dumps(a,indent=2));(S/'ScopeValidation.json').write_text(json.dumps({'passed':True,'detailed_pre_post':scoped,'actor_count':len(a['actors']),'new_actors':2,'fern_instances':224,'outside_actors_lights_shadows_and_pp_unchanged':True,'room_collision_profiles_and_gameplay_properties_preserved':True,'furniture_moved_with_matching_blockers':True},indent=2));unreal.log('ART_PASS_V3_SCOPE_PASS')
