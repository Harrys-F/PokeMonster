"""New named species only. Reuse the tested importer; never overwrite an existing species/profile."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/BiomeTestV11';request=json.loads((O/'ImportRequest.json').read_text());name=request['species'];specs=json.loads((R/'Tools/BiomeTestV1/SpeciesV11.json').read_text());spec=specs[name]
code=(R/'Tools/CreatureExpansionV3/ImportOne.py').read_text().split('MOVE_SPECS=')[0]
code=code.replace("O=R/'Saved/CreatureExpansionV3'","O=R/'Saved/BiomeTestV11'").replace("R/'Tools/CreatureExpansionV3/Species.json'","R/'Tools/BiomeTestV1/SpeciesV11.json'")
needle="  assert not profile.get_validation_errors(),list(profile.get_validation_errors());save(profile,P);"
assert needle in code
code=code.replace(needle,"  if name in ['Karpador','Garados']:\n   profile.set_editor_property('swim_idle_clip',clips[unreal.PokeMonsterCreatureClip.IDLE]);profile.set_editor_property('swim_clip',clips[unreal.PokeMonsterCreatureClip.WALK]);profile.set_editor_property('swim_reference_speed',walk)\n"+needle)
code=code.replace("   if species=='Schiggy'and typ=='BaseColor':","   if typ=='BaseColor':a.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_DEFAULT)\n   if species=='Schiggy'and typ=='BaseColor':")
exec(compile(code,'ExistingSingleSpeciesVisualImporter','exec'))
plan=json.loads((R/'Tools/MoveEffectsV4/CrystalMovePlan.json').read_text());by_symbol={r['identifier'].replace('-','_').upper():r for r in plan['rows']};by_symbol['POISONPOWDER']=by_symbol['POISON_POWDER']
entries=[];missing=[]
for level,symbol in spec['crystal_moves']:
 row=by_symbol.get(symbol)
 if row:
  m=unreal.load_asset(row['path']);assert m;entries.append(unreal.PokeMonsterLevelMove(level=level,move=m))
 else:
  entries.append(unreal.PokeMonsterLevelMove(level=level,unavailable_move_name=symbol,unavailable_reason='Verified Crystal learnset; this move is not yet bound in the existing move catalogue.'));missing.append({'level':level,'symbol':symbol})
profile=unreal.load_asset(rows[0]['profile']);s=data('DA_'+name,'/Game/Data/Creatures',unreal.PokeMonsterCreatureSpeciesData)
settings=unreal.PokeMonsterCreatureOverworldSettings();settings.set_editor_property('body_radius',float(spec['radius']));settings.set_editor_property('roam_radius',750.);settings.set_editor_property('maximum_active_distance',2200.);behavior=settings.get_editor_property('behavior');behavior.set_editor_property('temperament',getattr(unreal.PokeMonsterOverworldTemperament,spec['behavior']));settings.set_editor_property('behavior',behavior)
for k,v in dict(internal_id=name,display_name=name,pokedex_number=spec['dex'],base_capture_rate=spec['capture'],primary_type=getattr(unreal.PokeMonsterCreatureType,spec['types'][0]),secondary_type=getattr(unreal.PokeMonsterCreatureType,spec['types'][1]),base_stats=unreal.PokeMonsterCreatureBaseStats(**dict(zip(['hp','attack','defense','special_attack','special_defense','speed'],spec['stats']))),gender=unreal.PokeMonsterGenderData(system=unreal.PokeMonsterGenderSystem.MIXED,female_ratio=spec['female']),starting_level=spec['level'],growth_rate=getattr(unreal.PokeMonsterGrowthRate,spec['growth']),base_experience_yield=spec['xp'],visuals=unreal.PokeMonsterCreatureVisuals(presentation=profile),overworld=settings,level_up_moves=entries).items():s.set_editor_property(k,v)
save(s,'/Game/Data');wild=data('DA_'+name+'_Wild','/Game/Data/Encounters',unreal.PokeMonsterEncounterProfile);wild.set_editor_property('entries',[unreal.PokeMonsterWildEncounterEntry(species=s,min_level=spec['level'],max_level=spec['level'],weight=1)]);save(wild,'/Game/Data')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(O/('Import'+name+'.json')).write_text(json.dumps({'species':name,'assets':created,'profile':profile.get_path_name(),'missing_move_bindings':missing,'originals_unchanged':True,'maps_saved':False},indent=2));unreal.log('BIOME_SPECIES_V11_IMPORTED '+name)
