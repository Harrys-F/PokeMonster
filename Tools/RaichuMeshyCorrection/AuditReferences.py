"""Read actual Unreal package dependencies before/after replacing the unwanted model."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/RaichuMeshyCorrection';reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.search_all_assets(True);old='/Game/Characters/Creatures/Raichu/V4';options=unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True,include_searchable_names=True,include_soft_management_references=True,include_hard_management_references=True);rows=[]
for a in reg.get_assets_by_path(old,True):
 name=str(a.package_name);refs=sorted(str(x)for x in reg.get_referencers(name,options));rows.append({'package':name,'class':str(a.asset_class_path.asset_name),'referencers':refs,'external_referencers':[x for x in refs if not x.startswith(old+'/')]})
s=unreal.load_asset('/Game/Data/Creatures/DA_Raichu');p=s.get_visuals().presentation;result={'old_assets':rows,'old_asset_count':len(rows),'active_species':s.get_path_name(),'active_presentation':p.get_path_name()if p else None,'active_mesh':p.mesh.get_path_name()if p and p.mesh else None,'registered_species':[str(s.get_internal_id())for s in unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species()]}
expected=[old+'/DA_Raichu_Presentation',old+'/Meshes/SK_Raichu_V4',old+'/Meshes/SK_Raichu_V4_Skeleton']+[old+'/Animations/A_Raichu_'+n for n in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']]+[old+'/Materials/M_Raichu_'+n for n in ['Brown','Coat','Cream','Eyes','Gold','Highlight']]
result['old_package_referencers']={n:sorted(str(x)for x in (reg.get_referencers(n,options)or []))for n in expected}
if not rows:assert not any(result['old_package_referencers'].values()),result['old_package_referencers']
name=('ReferencesBeforeRemoval.json'if (D/'ReferencesBefore.json').exists()else'ReferencesBefore.json')if rows else'ReferencesAfter.json';(D/name).write_text(json.dumps(result,indent=2));print('RAICHU_REFERENCE_AUDIT',len(rows),'old assets; external',[(x['package'],x['external_referencers'])for x in rows if x['external_referencers']])
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
