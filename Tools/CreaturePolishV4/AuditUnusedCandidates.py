"""Read-only dependency proof for this task's own rejected Glurak intermediates."""
import unreal,json,hashlib,subprocess
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
P='/Game/Characters/Creatures/Glurak/PolishV4/';assets=[P+'A_Glurak_'+v for v in ['Idle','Walk','Run','Attack','Hit','Faint','Happy']]+[P+'SK_Glurak_PolishV4_Skeleton'];registry=unreal.AssetRegistryHelpers.get_asset_registry();options=unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True,include_searchable_names=True,include_soft_management_references=True,include_hard_management_references=True);rows=[]
for a in assets:
 refs=[str(x)for x in registry.get_referencers(a,options)];external=[x for x in refs if x not in assets];assert not external,(a,external)
 f=R/('Content/'+a.removeprefix('/Game/')+'.uasset');assert f.is_file();rows.append(dict(path=str(f.relative_to(R)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,referencers=refs))
for v in ['Walk','Run','Attack','Hit','Faint','Happy']:
 f=R/('Art/Characters/Creatures/Glurak/Exports/PolishV4/Glurak_'+v+'.fbx');rows.append(dict(path=str(f.relative_to(R)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,reason='Rejected own candidate; final original clips reused, not in final export audit'))
initial=json.loads((R/'Saved/CreaturePolishV4/InitialState.json').read_text());assert not set(x['path']for x in rows)&set(initial['untracked']);assert not subprocess.check_output(['git','ls-files','--',*[x['path']for x in rows]],cwd=R).strip()
(R/'Saved/CreaturePolishV4/RejectedOwnCandidates.json').write_text(json.dumps(dict(files=rows,only_own_untracked=True,external_referencers=[]),indent=2));unreal.log('OWN_REJECTED_INPUTS_AUDIT_PASS')
