"""Accept only reviewed presentation links and the single verified exterior fill intensity."""
import unreal,json,re,hashlib,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePolishV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();initial=json.loads((O/'InitialState.json').read_text());mapfile=R/'Content/Maps/Dev_TestMap_VisualV2.umap';assert hashlib.sha256(mapfile.read_bytes()).hexdigest()==initial['original_files'][str(mapfile.relative_to(R))];rows=[]
for x in json.loads((O/'ImportedCandidates.json').read_text())['models']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+x['species']);profile=unreal.load_asset(x['profile']);assert not profile.get_validation_errors();v=s.visuals;assert v.presentation.get_path_name()==x['original_profile'];old_id=str(s.get_internal_id());v.set_editor_property('presentation',profile);s.set_editor_property('visuals',v);assert str(s.get_internal_id())==old_id;assert unreal.EditorAssetLibrary.save_loaded_asset(s,False);rows.append(dict(species=x['species'],stable_id=old_id,old=x['original_profile'],new=profile.get_path_name()))
world=E.get_editor_world();assert 'Dev_TestMap_VisualV2' in world.get_name();light=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.DirectionalLight)if a.get_actor_label()=='VS_SoftSkyFill').get_component_by_class(unreal.DirectionalLightComponent);assert not light.cast_shadows and abs(light.intensity-.65)<.001;light.set_intensity(1.0);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from MapState import snapshot
before=json.loads((O/'MapBefore.json').read_text());after=json.loads(json.dumps(snapshot(unreal.get_editor_subsystem(unreal.EditorActorSubsystem))));
for data in [before,after]:
 for actor in data.values():
  for component in actor['components']:
   if 'color' in component:component['color']={k:int(v)for k,v in re.findall(r'([rgba]): (-?\d+)',component['color'])}
changes=[]
for key,a in after.items():
 if a!=before.get(key):changes.append(dict(actor=a['name'],before=before.get(key),after=a))
assert len(changes)==1 and changes[0]['actor']=='VS_SoftSkyFill',changes
b=changes[0]['before'];a=changes[0]['after'];assert len(b['components'])==len(a['components'])
for bc,ac in zip(b['components'],a['components']):
 for k in set(bc)|set(ac):
  if k=='intensity' and 'LightComponent'in ac['class']:assert abs(bc[k]-.65)<.001 and ac[k]==1.
  else:assert bc.get(k)==ac.get(k),(k,bc,ac)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_TestMap_VisualV2');assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(O/'Accepted.json').write_text(json.dumps(dict(species_links=rows,map_changes=changes,source='FillComparisonFixed; six exact camera pairs; sun/Lumen/TAA/visibility settings untouched'),indent=2));unreal.log('POLISH_V4_ACCEPTED_REVIEWED_CANDIDATES')
