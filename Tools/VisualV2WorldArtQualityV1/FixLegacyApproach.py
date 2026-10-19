"""Fix confirmed legacy opaque path overlay at z=1.4cm above the 1cm forecourt.
Keep original source mesh/material and all transforms; only assign a private bounded variant.
"""
import unreal,json,sys,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;dst='/Game/Environment/VisualV2WorldArtV1/Materials/M_WAQ1_LegacyApproach';assert not unreal.EditorAssetLibrary.does_asset_exist(dst)
m=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend',dst);nodes=[x for x in unreal.ObjectIterator(unreal.MaterialExpression) if x.get_outer()==m];color=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionCustom));code=color.get_editor_property('code');area='smoothstep(-4620,-4510,p.x)*(1-smoothstep(-3670,-3560,p.x))*smoothstep(-720,-610,p.y)*(1-smoothstep(1080,1190,p.y))';code=code.replace('float2 p=P.xy;','float2 p=P.xy;float art='+area+';');needle='if(Mode<2.5)return lerp(g,d*(1-.08*(1-saturate(edge))),alpha*ends);';assert needle in code;color.set_editor_property('code',code.replace(needle,'if(Mode<2.5)return lerp(lerp(g,d*(1-.08*(1-saturate(edge))),alpha*ends),d,art);'))
m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('opacity_mask_clip_value',.333);mask=L.create_material_expression(m,unreal.MaterialExpressionCustom,400,650);mask.set_editor_property('desc','WAQ1 remove legacy opaque painted grass overlay locally');mask.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1);inputs=[]
for name in ['P','UV']:
 i=unreal.CustomInput();i.set_editor_property('input_name',name);inputs.append(i)
mask.set_editor_property('inputs',inputs);mask.set_editor_property('code','float2 p=P.xy;float art='+area+';float e=abs(UV.y*2-1)+sin(p.x*.027+sin(p.y*.04))*.035+sin(p.x*.073)*.018;float a=(1-smoothstep(.65,.99,e))*smoothstep(0,.035,UV.x)*(1-smoothstep(.965,1,UV.x));return lerp(1,a,art);')
pos=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionWorldPosition));uv=next(x for x in nodes if isinstance(x,unreal.MaterialExpressionTextureCoordinate));assert L.connect_material_expressions(pos,'',mask,'P');assert L.connect_material_expressions(uv,'',mask,'UV');d=L.create_material_expression(m,unreal.MaterialExpressionMaterialFunctionCall,650,650);d.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));assert L.connect_material_expressions(mask,'',d,'Alpha Threshold');assert L.connect_material_property(d,'',unreal.MaterialProperty.MP_OPACITY_MASK);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label()=='V2_House_HH_Q2_OrganicApproach');old=a.static_mesh_component.get_material(0).get_path_name();a.static_mesh_component.set_material(0,m)
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((S/'Dev_TestMap_VisualV2_Scene.json').read_text());after=scene(w);changed={k for k in before['actors'] if before['actors'][k]!=after['actors'].get(k)};expected={'V2_Ground','V2_House_Forecourt','V2_Path_VillageLoop','V2_Path_NorthLoop','V2_House_HH_Q2_OrganicApproach'};assert {before['actors'][k]['label'] for k in changed}==expected
for k in changed:
 b=copy.deepcopy(before['actors'][k]);v=copy.deepcopy(after['actors'][k])
 for row in [b,v]:
  for comp in row['components']:
   if 'materials' in comp:comp['materials']=[]
 assert b==v,k
assert before['world_settings']==after['world_settings'];assert len(after['actors'])==len(before['actors'])+6;assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2')
j=json.loads((S/'ArtChanges.json').read_text());j['material_changes'].append({'label':a.get_actor_label(),'old':old,'new':m.get_path_name()});j['new_materials'].append(m.get_path_name());j['existing_actors_changed_only_material_slots']=sorted(changed);j['confirmed_legacy_overlay']='V2_House_HH_Q2_OrganicApproach: opaque grass-painted ribbon at z=1.4 cm above forecourt top z=1 cm; own masked variant preserves original outside bounded region';(S/'ArtChanges.json').write_text(json.dumps(j,indent=2));(S/'AfterScene.json').write_text(json.dumps(after,indent=2))
