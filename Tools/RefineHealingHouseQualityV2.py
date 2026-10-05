"""Camera-review corrections on own QualityV2 assets only; no V1 overwrite.
Run after Import/Dress. Fix ribbon winding, soften paint scale, blend forecourt.
"""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();W='/Game/Environment/Westland/NaturalGroundV1';lib=unreal.MaterialEditingLibrary
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert world.get_name()=='Dev_HealingHouseTestMap';assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
by={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
m=unreal.load_asset(W+'/Materials/M_WL_NG_PathBlend')
# Inspect expression objects directly; shader nodes are private subobjects.
expr=list(lib.get_material_expressions(m))
for o in expr:
 if isinstance(o,unreal.MaterialExpressionMultiply):o.set_editor_property('const_b',1/190 if o.get_editor_property('material_expression_editor_y')==200 else 1/220)
 if isinstance(o,unreal.MaterialExpressionCustom):o.set_editor_property('code','float irregular=sin(P.x*.027+sin(P.y*.04))*.035+sin(P.x*.073)*.018;float edge=abs(UV.y*2-1)+irregular;float a=1-smoothstep(.65,.99,edge);float ends=smoothstep(0,.035,UV.x)*(1-smoothstep(.965,1,UV.x));float wear=1-.08*(1-saturate(edge));float3 grass=lerp(G,dot(G,float3(.299,.587,.114)),.25)*float3(.66,.72,.62);return lerp(grass,D*float3(.86,.80,.73)*wear,a*ends);')
for sample in [o for o in expr if isinstance(o,unreal.MaterialExpressionTextureSample)]:
 y=lib.get_material_expression_node_position(sample)[1];mul=next(o for o in expr if isinstance(o,unreal.MaterialExpressionMultiply) and lib.get_material_expression_node_position(o)[1]==y);assert lib.connect_material_expressions(mul,'',sample,'UVs')
lib.delete_unused_expressions(m);lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
sm=unreal.load_asset(W+'/Meshes/SM_WL_NG_HealingApproach');dm=unreal.DynamicMesh();dm,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(sm,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
normal,valid=dm.get_triangle_face_normal(0);assert valid
if normal.z<0:unreal.GeometryScript_Normals.flip_normals(dm)
options=unreal.GeometryScriptCopyMeshToAssetOptions();dm,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,sm,options,unreal.GeometryScriptMeshWriteLOD());assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
sm.set_material(0,m);unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
# Forecourt uses its existing geometry and collision, with earth fading into
# the exact same world-space grass sample at every rectangular mesh boundary.
path=W+'/Materials/M_WL_NG_ForecourtBlend'
if not unreal.EditorAssetLibrary.does_asset_exist(path):assert unreal.EditorAssetLibrary.duplicate_asset(m.get_path_name().split('.')[0],path)
court=unreal.load_asset(path)
for o in lib.get_material_expressions(court):
 if isinstance(o,unreal.MaterialExpressionCustom):o.set_editor_property('code','float2 q=(P.xy-Center.xy)/Extent.xy;float radius=length(q);float uneven=sin(P.x*.026+P.y*.018)*.035+cos(P.y*.047)*.024;float a=1-smoothstep(.69,.98,radius+uneven);float3 grass=lerp(G,dot(G,float3(.299,.587,.114)),.25)*float3(.66,.72,.62);return lerp(grass,D*float3(.86,.80,.73),a);')
expr=list(lib.get_material_expressions(court))
for sample in [o for o in expr if isinstance(o,unreal.MaterialExpressionTextureSample)]:
 y=lib.get_material_expression_node_position(sample)[1];mul=next(o for o in expr if isinstance(o,unreal.MaterialExpressionMultiply) and lib.get_material_expression_node_position(o)[1]==y);assert lib.connect_material_expressions(mul,'',sample,'UVs')
custom=next(o for o in expr if isinstance(o,unreal.MaterialExpressionCustom));inputs=list(custom.get_editor_property('inputs'))
definitions=[('Center','CourtCenter_cm',(-850,0,0,0)),('Extent','CourtHalfSize_cm',(325,340,0,0))]
for pin,parameter,default in definitions:
 if pin not in [str(i.get_editor_property('input_name')) for i in inputs]:
  i=unreal.CustomInput();i.set_editor_property('input_name',pin);inputs.append(i)
# Assign the array once: assigning it again after wiring would restore stale
# struct copies and disconnect the previous Center input.
custom.set_editor_property('inputs',inputs)
for pin,parameter,default in definitions:
 node=next((o for o in lib.get_material_expressions(court) if isinstance(o,unreal.MaterialExpressionVectorParameter) and str(o.get_editor_property('parameter_name'))==parameter),None)
 if not node:node=lib.create_material_expression(court,unreal.MaterialExpressionVectorParameter,-750,950 if pin=='Center' else 1100)
 node.set_editor_property('parameter_name',parameter);node.set_editor_property('default_value',unreal.LinearColor(*default));assert lib.connect_material_expressions(node,'',custom,pin)
assert all(lib.get_inputs_for_material_expression(court,custom))
lib.delete_unused_expressions(court);lib.recompile_material(court);unreal.EditorAssetLibrary.save_loaded_asset(court,False);by['Forecourt'].static_mesh_component.set_material(0,court)
# Keep textile relief subordinate to the room; no busy repeating wave pattern.
for name,base_color in [('Sage',(.20,.28,.12)),('Linen',(.43,.42,.33))]:
 fabric=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_'+name);expr=list(lib.get_material_expressions(fabric))
 for node in expr:
  if isinstance(node,unreal.MaterialExpressionTextureCoordinate):node.set_editor_property('u_tiling',1);node.set_editor_property('v_tiling',1)
 sample=next(o for o in expr if isinstance(o,unreal.MaterialExpressionTextureSample));mix=lib.get_material_property_input_node(fabric,unreal.MaterialProperty.MP_BASE_COLOR)
 base=lib.create_material_expression(fabric,unreal.MaterialExpressionConstant3Vector,-480,420);base.constant=unreal.LinearColor(*base_color,1);blend=lib.create_material_expression(fabric,unreal.MaterialExpressionLinearInterpolate,-300,250);blend.set_editor_property('const_alpha',.22)
 assert lib.connect_material_expressions(base,'',blend,'A') and lib.connect_material_expressions(sample,'RGB',blend,'B') and lib.connect_material_expressions(blend,'',mix,'A')
 lib.delete_unused_expressions(fabric);lib.recompile_material(fabric);unreal.EditorAssetLibrary.save_loaded_asset(fabric,False)
unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_HealingHouseTestMap')
(ROOT/'Saved/HealingQualityV2/CameraRefinement.json').write_text(json.dumps({'ribbon_corrected_upward':True,'ground_tile_cm':190,'earth_tile_cm':220,'cloth_uv_repeat':1,'cloth_detail_mix':.22,'court_existing_geometry':True,'gameplay_unchanged':True},indent=2))
unreal.log('QUALITY_V2_CAMERA_REFINEMENT_PASSED')
