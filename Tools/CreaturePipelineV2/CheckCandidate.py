"""Read-only candidate acceptance check via Saved/CreaturePipelineV2/CandidateRequest.json.
Checks exactly one existing presentation, never assigns it to species or saves assets.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/CreaturePipelineV2';request=json.loads((O/'CandidateRequest.json').read_text());E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
s=unreal.load_asset(request['species_asset']);d=unreal.load_asset(request['presentation_asset'])
assert isinstance(s,unreal.PokeMonsterCreatureSpeciesData) and isinstance(d,unreal.PokeMonsterCreaturePresentationData)
assert 'CreatureSpecies:'+str(s.get_internal_id())==request['expected_primary_asset_id'],'Never change stable species identity for a visual exchange'
errors=list(d.get_validation_errors());clips=d.get_editor_property('clips');roles=set(clips.keys())
# Runtime supports intentionally idle-only previews; complete creatures require all seven roles.
required={getattr(unreal.PokeMonsterCreatureClip,n) for n in ['IDLE','WALK','RUN','ATTACK','HIT','FAINT','HAPPY']}
if request.get('require_all_seven',True) and not required.issubset(roles):errors.append('Complete creature requires seven explicit animation roles')
result={'species':s.get_path_name(),'presentation':d.get_path_name(),'expected_primary_asset_id':request['expected_primary_asset_id'],'errors':errors,'passed':not errors,'changed_species_binding':False,'saved_assets':False}
(O/'CandidateValidation.json').write_text(json.dumps(result,indent=2));assert not errors,errors;unreal.log('CREATURE_PIPELINE_V2_CANDIDATE_PASS')
