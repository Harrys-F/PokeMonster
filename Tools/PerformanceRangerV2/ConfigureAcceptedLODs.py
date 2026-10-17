import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2');s=unreal.load_asset('/Game/Characters/NPCs/RangerV2/DA_RangerV2_LODSettings');groups=list(s.get_editor_property('lod_groups'))[:2];assert len(groups)==2;s.set_editor_property('lod_groups',groups);unreal.EditorAssetLibrary.save_loaded_asset(s,False)
(P/'LODDecision.json').write_text(json.dumps({'accepted_candidate_triangles':[55000,24000],'rejected':{'triangles':10000,'reason':'Protected face survives, but collar/chest collapse creates visibly damaged cloth in close review. Retained only as rejected Blender/FBX evidence.'},'runtime_lod_count':2,'screen_sizes':[1.,.12],'hysteresis':.015,'no_automatic_baseline_release':True},indent=2))
