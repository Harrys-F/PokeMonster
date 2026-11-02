"""Map-only woodland soil and visible gravel bed; existing painted textures and paths remain."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';ROOT='/Game/Environment/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();assert not(D/'Ground.json').exists();ML=unreal.MaterialEditingLibrary;bindings=[]
for key in ['Grass','PathBlend']:
 src='/Game/Environment/WestlandVisualUpgradeV1/Materials/M_WVU_'+key;q=ROOT+'/Materials/M_WEP_'+key;assert not unreal.EditorAssetLibrary.does_asset_exist(q);m=unreal.EditorAssetLibrary.duplicate_asset(src,q);assert m
 for node in ML.get_material_expressions(m):
  if not isinstance(node,unreal.MaterialExpressionCustom):continue
  code=node.get_editor_property('code')
  if 'float forest=Texture2DSample'not in code:continue
  needle='float shore=1-smoothstep(3.4,8.2,abs(en.x-river));';assert needle in code
  code=code.replace(needle,needle+'\nfloat eastWood=exp(-(pow((en.x-252)/100,4)+pow((en.y-170)/126,4)));float westWood=.75*exp(-(pow((en.x+365)/38,4)+pow((en.y-95)/160,4)));forest=max(forest,max(eastWood,westWood)*.88);')
  needle='if(Mode<.5)return g;';assert needle in code
  code=code.replace(needle,'''float wetBed=1-smoothstep(2.8,4.8,abs(en.x-river));float2 pc=frac(en*6.5);float stone=1-smoothstep(.21,.42,length((pc-.5)*float2(1,1.35)));float grain=.5+.5*sin(en.x*9+sin(en.y*7));float3 gravel=lerp(float3(.16,.14,.095),float3(.38,.36,.24),stone)*(.86+grain*.2);g=lerp(g,gravel,wetBed*.9);if(Mode<.5)return g;''');node.set_editor_property('code',code)
 ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
 for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   for i in range(c.get_num_materials()):
    old=c.get_material(i)
    if old and old.get_path_name().split('.')[0]==src:a.modify();c.set_material(i,m);bindings.append(dict(actor=a.get_actor_label(),slot=i,source=src,derived=q))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'Ground.json').write_text(json.dumps(bindings,indent=2))
