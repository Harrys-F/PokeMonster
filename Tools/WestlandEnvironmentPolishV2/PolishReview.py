"""Correct the visible regular bed pattern and use the existing mottled moss-rock surface."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world()and W.get_name()=='Dev_WestlandRegion';ML=unreal.MaterialEditingLibrary;rows=[]
for key in ['Grass','PathBlend']:
 m=unreal.load_asset('/Game/Environment/WestlandEnvironmentPolishV2/Materials/M_WEP_'+key)
 for node in ML.get_material_expressions(m):
  if not isinstance(node,unreal.MaterialExpressionCustom):continue
  code=node.get_editor_property('code')
  if 'float wetBed='not in code:continue
  a=code.index('float wetBed=');b=code.index('if(Mode<.5)return g;',a);code=code[:a]+'''float wetBed=1-smoothstep(2.8,4.8,abs(en.x-river));g=lerp(g,d*float3(.54,.61,.58),wetBed*.92);'''+code[b:]
  code=code.replace('pow((en.x-252)/100,4)','pow(abs((en.x-252)/100),4)').replace('pow((en.y-170)/126,4)','pow(abs((en.y-170)/126),4)').replace('pow((en.x+365)/38,4)','pow(abs((en.x+365)/38),4)').replace('pow((en.y-95)/160,4)','pow(abs((en.y-95)/160),4)');node.set_editor_property('code',code)
 ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);rows.append(m.get_path_name())
rock=unreal.load_asset('/Game/Environment/VisualV2EnvironmentV3/Materials/MI_EQ3_MossStoneInstanced');assert rock
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if a.get_actor_label().startswith('WEP_Boulders_'):a.modify();a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent).set_material(0,rock)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'ReviewPolish.json').write_text(json.dumps(dict(materials=rows,bed='existing painted soil and actual pebble meshes; regular dot shader removed',rocks=rock.get_path_name()),indent=2))
