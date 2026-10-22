"""One-time reviewed V6 adoption; change only four visuals and two overworld speed overrides."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/AnimationCorrectionsV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();baseline=json.loads((O/'UnrealBaseline.json').read_text());rows=[];pending=[]
for name in ['Glurak','Nebulak','Machomei','Myrapla']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);old=s.get_visuals().presentation;new=unreal.load_asset('/Game/Characters/Creatures/'+name+'/AnimationV6/DA_'+name+'_Presentation_V6');assert old.get_path_name()==baseline[name]['profile'];assert not new.get_validation_errors();assert unreal.PokeMonsterCreaturePolishLibrary.have_matching_reference_skeleton(new.mesh,old.mesh);assert new.reference_size_cm==old.reference_size_cm and new.walk_speed==old.walk_speed and new.run_speed==old.run_speed and new.ground_offset_cm==old.ground_offset_cm;pending.append((s,new))
for name in ['Pikachu','Schiggy']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);o=s.overworld;assert o.walk_speed_override==baseline[name]['walk_override']==0 and o.run_speed_override==baseline[name]['run_override']==0
for s,new in pending:
 identity=str(s.get_internal_id());v=s.get_visuals();v.set_editor_property('presentation',new);s.set_editor_property('visuals',v);assert str(s.get_internal_id())==identity;assert unreal.EditorAssetLibrary.save_loaded_asset(s,False);rows.append(dict(species=identity,changed='visual presentation only',profile=new.get_path_name()))
for name in ['Pikachu','Schiggy']:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);o=s.overworld;p=s.get_visuals().presentation;o.set_editor_property('walk_speed_override',p.walk_speed*1.15);o.set_editor_property('run_speed_override',p.run_speed*1.15);s.set_editor_property('overworld',o);assert unreal.EditorAssetLibrary.save_loaded_asset(s,False);rows.append(dict(species=name,changed='overworld walk/run overrides only',walk=o.walk_speed_override,run=o.run_speed_override,authored_walk_unchanged=p.walk_speed,authored_run_unchanged=p.run_speed))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(O/'Adoption.json').write_text(json.dumps(rows,indent=2))
