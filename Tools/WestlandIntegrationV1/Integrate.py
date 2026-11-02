"""One guarded authoring pass on the existing region. Original geometry/assets/dialogues are retained."""
import unreal,json,sys,re,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
D=R/'Saved/ProjectRefinement/WestlandIntegrationV1';Q=json.loads((R/'Tools/WestlandIntegrationV1/Layout.json').read_text());E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert E.get_editor_world().get_name()=='Dev_WestlandRegion'
assert hashlib.sha256((R/'Content/Maps/Dev_WestlandRegion.umap').read_bytes()).hexdigest()==json.loads((D/'Baseline.json').read_text())['westland']['sha256'],'Original map changed; inspect before authoring'
W=E.get_editor_world();actors=list(A.get_all_level_actors());by={a.get_actor_label():a for a in actors};TAG='WestlandIntegrationV1';assert not any(a.actor_has_tag(TAG)for a in actors),'Already integrated; inspect saved map instead of duplicating'
audit={'npcs':[],'zones':[],'pickups':[],'terrain_visibility':[],'water_barriers':[]}
def tag(a):a.tags=list(a.tags)+[TAG];a.set_folder_path('WestlandRegion/IntegrationV1')
def spawn(cls,label,p,rot=unreal.Rotator()):
 a=A.spawn_actor_from_class(cls,unreal.Vector(*p),rot);assert a;a.set_actor_label(label);tag(a);return a
def floor(x,y,z=0,ignore=None):
 h=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+900),unreal.Vector(x,y,z-2000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore or [],unreal.DrawDebugTrace.NONE)
 if not h:return None
 m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',h.export_text());return float(m[1])if m else None
# Existing region terrain deliberately ignored Visibility in the old art proof.
# The shared creature/surface planner needs this query channel, without changing Pawn collision or geometry.
terrain=[a for a in actors if a.get_actor_label().startswith('WR_Terrain_')];assert len(terrain)==80
for a in terrain:
 c=a.get_component_by_class(unreal.StaticMeshComponent);a.modify();c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK);audit['terrain_visibility'].append(a.get_name())
for a in actors:
 if a.get_actor_label()=='HH_Expanded_Floor':
  a.modify();a.get_component_by_class(unreal.StaticMeshComponent).set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK);audit['terrain_visibility'].append(a.get_name())
barriers=[a for a in actors if a.get_actor_label().startswith('WR_RiverBarrier_')]
for a in barriers:
 a.modify();a.tags=list(a.tags)+['BiomePlayerWaterBarrier'];audit['water_barriers'].append(a.get_name())
# Appearance only, attached to the original interaction actor. No duplicate dialogue/heal actors.
for row in Q['npc_presentations']:
 source=by[row['label']];profile=unreal.load_asset('/Game/Characters/NPCs/Library/Profiles/DA_NPC_'+row['profile']);assert profile and not profile.get_validation_errors()
 before={'name':source.get_name(),'position':list(source.get_actor_location().to_tuple()),'dialogue':str(source.get_editor_property('dialogue'))if isinstance(source,unreal.PokeMonsterNPC)else None,'display_name':str(source.display_name)}
 p=source.get_actor_location();body=source.get_component_by_class(unreal.CapsuleComponent);ground=floor(p.x,p.y,p.z,[source]);assert ground is not None,(row['label'],'No floor')
 half=row['height_cm']*.5;source.modify();body.set_capsule_size(34 if isinstance(source,unreal.PokeMonsterNPC)else 48,half,True);source.set_actor_location(unreal.Vector(p.x,p.y,ground+half+2),False,False)
 visual=spawn(unreal.PokeMonsterNPCVisualActor,'WR_Visual_'+row['label'],(p.x,p.y,ground+.4),source.get_actor_rotation());visual.source_actor=source;assert visual.apply_presentation(profile);scale=row['height_cm']/profile.reference_height_cm;visual.set_actor_scale3d(unreal.Vector(scale,scale,scale))
 visual.shadowless_interior_presentation=isinstance(source,unreal.PokeMonsterRestPoint)and by['HouseCutaway'].get_editor_property('use_shadowless_interior_lighting');visual.refresh_presentation();visual.attach_to_actor(source,'',unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,unreal.AttachmentRule.KEEP_WORLD,False)
 # The old fixed-size sprite labels should not float above a now differently sized capsule.
 for c in source.get_components_by_class(unreal.TextRenderComponent):
  if c.get_name()=='NameLabel':c.set_relative_location(unreal.Vector(0,0,half+22),False,False)
 if isinstance(source,unreal.PokeMonsterRestPoint):
  for c in source.get_components_by_class(unreal.StaticMeshComponent):c.set_visibility(False,True)
 assert str(source.display_name)==before['display_name']
 if isinstance(source,unreal.PokeMonsterNPC):assert str(source.dialogue)==before['dialogue']
 audit['npcs'].append({**row,'source_before':before,'source_after':source.get_actor_location().to_tuple(),'visual':visual.get_name(),'ground_z':ground,'capsule_half_height':half,'idle':visual.idle_animation.get_path_name(),'mesh':visual.visual.skeletal_mesh_asset.get_path_name()})
# Existing sun is retained. Only missing shadowless fill is added, using the existing day/night contract.
sun=next(a for a in actors if isinstance(a,unreal.DirectionalLight));sun.modify();sun.tags=list(sun.tags)+['PokeMonsterSun'];sun.light_component.set_editor_property('cast_shadows',True);sun.light_component.set_editor_property('light_source_angle',3.5);sun.light_component.set_editor_property('forward_shading_priority',1)
fill=spawn(unreal.DirectionalLight,'WR_SoftSkyFill',(0,0,600),unreal.Rotator(pitch=-65,yaw=35));fill.tags=list(fill.tags)+['PokeMonsterSkyFill'];fill.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);fill.light_component.set_editor_property('cast_shadows',False);fill.light_component.set_intensity(1.8)
# Reuse the current native TAA-only blendable, without replacing regional exposure/tonemapping.
pp=by['WR_OutdoorExposure'];settings=pp.settings;old=settings.export_text();assert not settings.weighted_blendables.array;pp.modify();blend=unreal.new_object(unreal.PokeMonsterTemporalAABlendable,outer=pp,name='Westland_TAA');weighted=settings.weighted_blendables;weighted.array=[unreal.WeightedBlendable(weight=1,object=blend)];settings.weighted_blendables=weighted;pp.settings=settings
check=unreal.PostProcessSettings();check.import_text(pp.settings.export_text());weighted=check.weighted_blendables;weighted.array=[];check.weighted_blendables=weighted;assert check.export_text()==old,'Non-AA postprocess changed'
# Authored zones are consumed by the existing world subsystem. Global species/caps/rhythms remain unchanged.
for row in Q['land_zones']:
 e,n=row['east_m'],row['north_m'];x,y,_=L.world(e,n);ground=floor(x,y,L.height(e,n)*100);assert ground is not None,row['id']
 z=spawn(unreal.PokeMonsterHabitatZone,'WR_Habitat_'+row['id'],(x,y,ground),unreal.Rotator(yaw=45));z.zone_id=row['id'];z.habitat_type=row['type'];z.habitat_name=row['id'];z.maximum_population=row['maximum'];z.coverage_priority=30;z.bounds.set_box_extent(unreal.Vector(*row['extent_cm']));z.water_surface_z=L.water(n)*100
 audit['zones'].append({**row,'position':z.get_actor_location().to_tuple(),'water_surface_z':z.water_surface_z,'medium':'Land'})
for n in Q['water_sections_north_m']:
 e=L.river(n);x,y,surface=L.world(e,n,L.water(n));bed=floor(x,y,surface,barriers);assert bed is not None and surface-bed>=45,(n,'Insufficient existing river depth',bed,surface)
 z=spawn(unreal.PokeMonsterHabitatZone,'WR_Habitat_River_'+str(n),(x,y,surface),unreal.Rotator(yaw=-45));z.zone_id='Westland_River_'+str(n);z.habitat_type='Water';z.habitat_name='Westland Fluss';z.maximum_population=1;z.coverage_priority=30;z.medium=unreal.PokeMonsterBiomeMedium.WATER_ONLY;z.water_surface_z=surface;z.bounds.set_box_extent(unreal.Vector(Q['water_half_length_cm'],Q['water_half_width_cm'],300));z.travel_points=[unreal.Vector(v,0,0)for v in [-320,-200,-80,80,200,320]]
 audit['zones'].append({'id':str(z.zone_id),'type':'Water','position':z.get_actor_location().to_tuple(),'extent_cm':z.bounds.get_unscaled_box_extent().to_tuple(),'medium':'WaterOnly','surface_z':surface,'bed_z':bed,'measured_depth_cm':surface-bed,'Garados_excluded_by_width_and_draft':True})
# A small number of ordinary existing item finds; no new item types or quest/story text.
for label,e,n,item,qty in [('HofFund',-302,-215,'PokeBall',2),('DorfFund',-223,-31,'TestHealingItem',1),('UferFund',L.river(-145)+12,-145,'GreatBall',1)]:
 x,y,_=L.world(e,n);ground=floor(x,y,L.height(e,n)*100);assert ground is not None
 a=spawn(unreal.PokeMonsterWorldItem,'WR_Pickup_'+label,(x,y,ground+1));a.set_editor_property('pickup_id','Pickup.Westland.IntegrationV1.'+label);a.set_editor_property('item',unreal.load_asset('/Game/Data/Items/DA_'+item));assert a.item;a.set_editor_property('quantity',qty);audit['pickups'].append({'label':a.get_actor_label(),'id':str(a.pickup_id),'position':a.get_actor_location().to_tuple(),'item':str(a.item),'quantity':qty})
assert len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PlayerStart))==1
assert len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterNPC))==3
assert len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterRestPoint))==1
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'No shared assets may be changed'
assert unreal.EditorLoadingAndSavingUtils.save_map(W,Q['map'])
(D/'IntegrationAudit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False));unreal.log('WESTLAND_INTEGRATION_SAVED '+str(len(audit['zones']))+' zones / 4 visuals / 3 finds')
