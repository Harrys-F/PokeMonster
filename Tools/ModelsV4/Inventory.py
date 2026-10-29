"""Actual AssetRegistry inventory, read-only for assets/maps; no name-based claim of playability."""
import unreal,json,struct
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/ModelsV4';reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.search_all_assets(True)
play=unreal.PokeMonsterCreatureSpeciesData.get_registered_playable_species();pids={s.get_path_name()for s in play};rows=[]
for a in reg.get_assets_by_path('/Game/Data/Creatures',True):
 s=a.get_asset()
 if not isinstance(s,unreal.PokeMonsterCreatureSpeciesData):continue
 p=s.get_visuals().presentation;m=p.mesh if p else None
 rows.append(dict(name=str(s.get_display_name()),id=str(s.get_internal_id()),dex=s.get_pokedex_number(),asset=s.get_path_name(),playable=s.get_path_name()in pids,presentation=p.get_path_name()if p else None,mesh=m.get_path_name()if m else None,skeleton=m.skeleton.get_path_name()if m and m.skeleton else None,reference_cm=p.reference_size_cm if p else None,ground_offset=p.ground_offset_cm if p else None,walk_speed=p.walk_speed if p else None,run_speed=p.run_speed if p else None,clips={str(k):{'asset':v.get_path_name(),'seconds':v.get_play_length(),'skeleton':v.get_editor_property('skeleton').get_path_name()}for k,v in p.clips.items()}if p else {},validation=list(p.get_validation_errors())if p else ['no presentation'],overworld=s.overworld.export_text(),learnset=[e.export_text()for e in s.level_up_moves],routes=[e.export_text()for e in s.get_evolutions()]))
assets=[]
for a in reg.get_assets_by_path('/Game/Characters/Creatures',True):
 assets.append({'asset':str(a.package_name),'class':str(a.asset_class_path.asset_name),'tags':{str(k):str(v)for k,v in a.get_editor_property('tags_and_values').items()}if False else {}})
sources=[]
for p in sorted((R/'Art').rglob('*')):
 if p.is_symlink()or not p.is_file()or p.suffix.lower()not in ['.blend','.fbx','.glb','.gltf','.obj','.usd','.usdz']:continue
 row={'path':str(p.relative_to(R)),'bytes':p.stat().st_size}
 if p.suffix.lower()=='.glb':
  with p.open('rb')as f:
   magic,version,total=struct.unpack('<III',f.read(12));n,t=struct.unpack('<II',f.read(8));doc=json.loads(f.read(n))
  row.update(meshes=len(doc.get('meshes',[])),materials=len(doc.get('materials',[])),textures=len(doc.get('textures',[])),skins=len(doc.get('skins',[])),animations=len(doc.get('animations',[])),triangles=sum(doc['accessors'][pr['indices']]['count']//3 for m in doc.get('meshes',[])for pr in m['primitives']if 'indices'in pr),generator=doc.get('asset',{}).get('generator'))
 sources.append(row)
result={'species':sorted(rows,key=lambda x:x['dex']),'playable_count':len(play),'creature_assets':assets,'sources':sources,'all_assets_named_raichu':[str(a.package_name)for a in reg.get_all_assets()if 'raichu'in str(a.package_name).lower()]}
(D/'Inventory.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print('MODELS_V4_INVENTORY',len(rows),len(play),len(assets),len(sources),'Raichu',result['all_assets_named_raichu'])
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
