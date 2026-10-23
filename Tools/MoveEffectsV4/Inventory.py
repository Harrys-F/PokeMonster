"""Read-only move-asset inventory for Audit.py. No asset or map writes."""
import unreal,json,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();assert R==Path('/Users/harry/Developer/PokeMonster');O=R/'Saved/MoveEffectsV4';O.mkdir(exist_ok=True);rows=[]
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
for path in sorted(unreal.EditorAssetLibrary.list_assets('/Game/Data/Moves',recursive=True,include_folder=False)):
 m=unreal.load_asset(path)
 if not isinstance(m,unreal.PokeMonsterMoveData):continue
 rows.append(dict(path=m.get_path_name(),id=str(m.internal_id),name=str(m.display_name),type=str(m.type),category=str(m.category),power=m.base_power,accuracy=m.accuracy,pp=m.max_pp,priority=m.priority,effect=str(m.effect.effect_id),chance=m.effect.chance_percent,description=str(m.effect.description),components=[dict(kind=str(c.kind),self=c.get_editor_property('self'),secondary=c.secondary,stat=str(c.stat),stages=c.stages,status=str(c.status),chance=c.chance_percent)for c in m.effects]))
assert len({x['id']for x in rows})==len(rows)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
p=O/('Inventory_'+str(time.time_ns())+'.json');assert not p.exists();p.write_text(json.dumps(rows,ensure_ascii=False,indent=2));unreal.log('MOVE_EFFECTS_V4_INVENTORY '+str(p))
