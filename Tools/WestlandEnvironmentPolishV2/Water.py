"""Map-local physically lit Single Layer Water derivative; no global rendering changes."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';ROOT='/Game/Environment/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not(D/'Water.json').exists();ML=unreal.MaterialEditingLibrary;q=ROOT+'/Materials/M_WEP_FlowingRiver';assert not unreal.EditorAssetLibrary.does_asset_exist(q);m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/WestlandVisualUpgradeV1/Materials/M_WVU_River',q);assert m
m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_SINGLE_LAYER_WATER);m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_OPAQUE);m.set_editor_property('two_sided',True)
for prop in [unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialProperty.MP_OPACITY,unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialProperty.MP_SPECULAR]:
 n=ML.get_material_property_input_node(m,prop)
 if n:ML.delete_material_expression(m,n)
def scalar(x,prop):
 n=ML.create_material_expression(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',x);assert ML.connect_material_property(n,'',prop)
def vector(col):
 n=ML.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);n.set_editor_property('constant',unreal.LinearColor(*col,1));return n
assert ML.connect_material_property(vector((.009,.023,.018)),'',unreal.MaterialProperty.MP_BASE_COLOR);scalar(.08,unreal.MaterialProperty.MP_OPACITY);scalar(.18,unreal.MaterialProperty.MP_ROUGHNESS);scalar(.5,unreal.MaterialProperty.MP_SPECULAR)
sl=ML.create_material_expression(m,unreal.MaterialExpressionSingleLayerWaterMaterialOutput)
for pin,col in [('ScatteringCoefficients',(.00035,.0008,.00055)),('AbsorptionCoefficients',(.0045,.0019,.0011)),('ColorScaleBehindWater',(.92,.98,.94))]:assert ML.connect_material_expressions(vector(col),'',sl,pin),pin
n=ML.create_material_expression(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',.35);assert ML.connect_material_expressions(n,'',sl,'PhaseG')
ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);a=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()if a.get_actor_label()=='WR_WindingRiver');a.modify();a.static_mesh_component.set_material(0,m);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'Water.json').write_text(json.dumps(dict(material=m.get_path_name(),model=str(m.get_editor_property('shading_model')),opacity=.08,roughness=.18,hardware_path='SingleLayerWater; validate actual Metal compile/runtime, not just project configuration',original_retained=True),indent=2))
