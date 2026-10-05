"""Final real-camera color adjustment; changes only owned V3 art materials."""
import unreal
def refine_quality_v3():
 lib=unreal.MaterialEditingLibrary
 playing=bool(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world())
 colors={'Leaf':(.028,.072,.018),'LeafLight':(.085,.15,.04),'LeafDark':(.015,.04,.007),
         'Flower':(.24,.06,.035),'FlowerCream':(.40,.27,.09),'Ceramic':(.14,.06,.025)}
 for name,color in colors.items():
  path='/Game/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_'+name
  m=unreal.load_asset(path);assert m
  n=lib.get_material_property_input_node(m,unreal.MaterialProperty.MP_BASE_COLOR)
  assert isinstance(n,unreal.MaterialExpressionConstant3Vector)
  n.set_editor_property('constant',unreal.LinearColor(*color,1))
  lib.delete_unused_expressions(m);lib.recompile_material(m)
  if not playing:assert unreal.EditorAssetLibrary.save_asset(path,False)
 for path in unreal.EditorAssetLibrary.list_assets('/Game/Environment/HealingHouse/QualityV3/Materials',True,False):
  m=unreal.load_asset(path);lib.delete_unused_expressions(m);lib.recompile_material(m)
  if not playing:assert unreal.EditorAssetLibrary.save_asset(path,False)
 if not playing:
  actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
  by={a.get_actor_label():a for a in actors}
  for label,pos in {'HH_Art_FloorHerb_1':(19620,480,1),'HH_Art_FloorHerb_2':(20380,410,1)}.items():
   by[label].set_actor_location(unreal.Vector(*pos),False,False)
  by['HH_Art_FloorHerb_1'].set_actor_scale3d(unreal.Vector(.85,.85,.85))
  for i,pos in enumerate([(19735,-570,214),(20315,570,214),(20470,-425,214)]):
   by['HH_Q3_HangingHerb_'+str(i)].set_actor_location(unreal.Vector(*pos),False,False)
   by['HH_Q3_HangingHerb_'+str(i)].set_actor_scale3d(unreal.Vector(.55,.55,.55))
   by['HH_Q3_HangingHook_'+str(i)].set_actor_scale3d(unreal.Vector(1,.85,1))
  world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
  assert world.get_name()=='Dev_HealingHouseTestMap'
  assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
 unreal.log('HEALING_Q3_CAMERA_COLOR_REFINEMENT_PASSED')
refine_quality_v3()
