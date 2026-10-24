"""One scoped upgrade of the existing Biome map. No other map, original material or species is saved."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1'
O=R/'Saved/BiomeTestV11/WaterMapUpgrade.json';assert not O.exists();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
for n in ['Karpador','Garados']:assert (R/'Saved/BiomeTestV11'/('Import'+n+'.json')).exists()
assert(R/'Saved/BiomeTestV11/ImportSchiggySwim.json').exists()
actors=list(ES.get_all_level_actors());habitats={a.habitat_name:a for a in actors if isinstance(a,unreal.PokeMonsterBiomeHabitat)}
def spec(name,u,v,centre,override=None):
 q=unreal.PokeMonsterBiomeSpecimen();q.set_editor_property('species',unreal.load_asset('/Game/Data/Creatures/DA_'+name));q.set_editor_property('local_position',unreal.Vector(u-centre[0],-(v-centre[1]),L.height(u,v)));q.set_editor_property('seed',57129 if name=='Karpador'else 57130);q.set_editor_property('bWaterDiagnostic',False)
 if override:q.set_editor_property('presentation_override',unreal.load_asset(override))
 return q
def configure(a,name,centre,half,points,species,draft,radius,override=None):
 a.set_actor_location(unreal.Vector(*L.world(*centre)),False,True);a.set_actor_rotation(unreal.Rotator(yaw=45),False);a.set_actor_label('Biome_Habitat_'+name);a.set_editor_property('habitat_name',name);a.set_editor_property('medium',unreal.PokeMonsterBiomeMedium.WATER_ONLY);a.bounds.set_box_extent(unreal.Vector(*half,600));a.set_editor_property('water_draft_cm',draft);a.set_editor_property('clearance_radius_cm',radius);a.set_editor_property('minimum_depth_cm',draft+10);a.set_editor_property('specimens',[spec(species,*points[0],centre,override)]);a.set_editor_property('travel_points',[unreal.Vector(u-centre[0],-(v-centre[1]),0)for u,v in points]);a.tags=['BiomeTestV1'];a.set_folder_path('BiomeV1/Habitats')
configure(habitats['NurWasser_Diagnose'],'Karpador',(3830,2850),(225,300),[(3800,2780),(3860,3000),(3740,2700)],'Karpador',43,38)
a=ES.spawn_actor_from_class(unreal.PokeMonsterBiomeHabitat,unreal.Vector(),unreal.Rotator(yaw=45));configure(a,'Garados',(3120,2810),(590,450),[(3050,2750),(3230,2950),(3300,2700)],'Garados',180,205)
sh=habitats['SchiggyUfer'];arr=list(sh.specimens);assert len(arr)==1;arr[0].set_editor_property('presentation_override',unreal.load_asset('/Game/Characters/Creatures/Schiggy/BiomeV11/DA_Schiggy_SwimPresentation'));sh.set_editor_property('specimens',arr)
# Add only newly required deep-water player blockers; the original barriers remain.
existing=set()
for a in actors:
 if a.actor_has_tag('BiomePlayerWaterBarrier'):
  p=a.get_actor_location();u,v=L.local(p.x,p.y);existing.add((round(u),round(v)))
SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);added=[]
for u in range(1900,4401,120):
 for v in range(1800,5200,120):
  if L.height(u,v)>-48 or abs(v-4100)<230 or(u,v)in existing:continue
  a=ES.spawn_actor_from_class(unreal.Actor,unreal.Vector(*L.world(u,v,75)),unreal.Rotator(yaw=45));a.set_actor_label('Biome_V11_WaterBarrier_'+str(len(added)));a.set_folder_path('BiomeV1/Collision');a.tags=['BiomeTestV1','BiomePlayerWaterBarrier'];root=SUB.k2_gather_subobject_data_for_instance(a)[0];h,reason=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.BoxComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,reason;c.set_box_extent(unreal.Vector(62,62,125));c.set_collision_profile_name('BlockAll');c.set_hidden_in_game(True);added.append(a.get_actor_label())
for a in actors:
 if a.get_actor_label()=='Biome_WaterDiagnosticLabel':a.text_render.set_text('Karpador und Garados\nEigene Schwimm-Rigs')
 if isinstance(a,unreal.DirectionalLight):
  # Resolve the existing forward-translucency priority warning, without changing any light value.
  a.light_component.set_editor_property('forward_shading_priority',1 if a.get_actor_label()=='Biome_DirectionalLight_Dev'else 0)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'map':'/Game/Maps/Dev_BiomeTestMap_V1','new_species':['Karpador','Garados'],'water_depth_cm':400,'schiggy_swim_override_only':True,'additional_player_water_barriers':added,'light_values_unchanged_priority_resolved':True,'other_maps_saved':False},indent=2))
