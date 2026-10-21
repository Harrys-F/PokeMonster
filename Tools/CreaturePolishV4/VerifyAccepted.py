"""Read-only normalized structural map comparison and exact accepted links."""
import unreal,json,re,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePolishV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();sys.path.insert(0,str(R/'Tools/CreatureExpansionV3'));from MapState import snapshot
before=json.loads((O/'MapBefore.json').read_text());after=json.loads(json.dumps(snapshot(unreal.get_editor_subsystem(unreal.EditorActorSubsystem))));assert set(before)==set(after);
for data in [before,after]:
 for actor in data.values():
  for component in actor['components']:
   if 'color' in component:component['color']={k:int(v)for k,v in re.findall(r'([rgba]): (-?\d+)',component['color'])}
changes=[dict(actor=a['name'],before=before[key],after=a)for key,a in after.items()if a!=before[key]];(O/'MapAfter.json').write_text(json.dumps(after,indent=2));(O/'MapDifferences.json').write_text(json.dumps(changes,indent=2));assert len(changes)==1 and changes[0]['actor']=='VS_SoftSkyFill',[(c['actor'])for c in changes];b=changes[0]['before'];a=changes[0]['after'];assert len(b['components'])==len(a['components'])
for bc,ac in zip(b['components'],a['components']):
 for k in set(bc)|set(ac):
  if k=='intensity' and 'LightComponent'in ac['class']:assert abs(bc[k]-.65)<.001 and ac[k]==1.
  else:assert bc.get(k)==ac.get(k),k
rows=[]
for x in json.loads((O/'ImportedCandidates.json').read_text())['models']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+x['species']);assert s.visuals.presentation.get_path_name()==x['profile'];assert not s.visuals.presentation.get_validation_errors();assert str(s.get_internal_id())==x['species'];rows.append(dict(species=x['species'],stable_id=str(s.get_internal_id()),old=x['original_profile'],new=x['profile']))
(O/'Accepted.json').write_text(json.dumps(dict(species_links=rows,map_changes=changes,only_map_change='VS_SoftSkyFill intensity .65 to 1.0',normalization='JSON round-trip makes original list and current tuple coordinates comparable'),indent=2));unreal.log('POLISH_ACCEPTED_STRUCTURAL_CHECK_PASS')
