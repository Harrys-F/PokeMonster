"""Only three private V6 materials; all V4/V5 meshes, textures and materials remain unchanged."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV6';A=R/'Art/World/VisualV2WorldArtV6';D='/Game/Environment/VisualV2WorldArtV6';L=unreal.MaterialEditingLibrary
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not (S/'Prepared.json').exists()
assert all(p.get_path_name().startswith(D+'/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
marker=S/'AssetWorkSession.json'
# Do not overwrite existing work in a fresh checkout. Only resume our explicitly
# owned unfinished session; all shared V4/V5 assets are read-only sources.
if marker.exists():assert json.loads(marker.read_text())['private_root']==D
else:assert not unreal.EditorAssetLibrary.does_directory_exist(D)
allowed={D+'/Materials/M_WA6_'+k for k in ['Ground','NorthPath','MainPath']}
if unreal.EditorAssetLibrary.does_directory_exist(D):
 assert {p.split('.')[0] for p in unreal.EditorAssetLibrary.list_assets(D,True,False)}<=allowed
marker.write_text(json.dumps({'private_root':D,'baseline':'8725ca992b8832701da61621799b34cf21f936ff'}))
common=(A/'RouteField.hlsl').read_text();rows=[]
for key in ['Ground','NorthPath','MainPath']:
 src='/Game/Environment/VisualV2WorldArtV5/Materials/M_WA5_'+key;dst=D+'/Materials/M_WA6_'+key;m=unreal.load_asset(dst) if unreal.EditorAssetLibrary.does_asset_exist(dst) else unreal.EditorAssetLibrary.duplicate_asset(src,dst);assert m
 expressions=L.get_material_expressions(m);color=next(n for n in expressions if isinstance(n,unreal.MaterialExpressionCustom) and n.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3);source_nodes=unreal.MaterialEditingLibrary.get_material_expressions(unreal.load_asset(src));source_codes={n.get_name():n.get_editor_property('code') for n in source_nodes if isinstance(n,unreal.MaterialExpressionCustom)};old=source_codes[color.get_name()];code=old;assert code.count('float2 p=P.xy;')==1;code=code.replace('float2 p=P.xy;','float2 p=P.xy;'+common,1)
 arg=unreal.CustomInput();arg.set_editor_property('input_name','W6Earth');color.set_editor_property('inputs',[i for i in color.get_editor_property('inputs') if str(i.get_editor_property('input_name'))!='W6Earth']+[arg]);texture=next((n for n in expressions if isinstance(n,unreal.MaterialExpressionTextureObjectParameter) and str(n.get_editor_property('parameter_name'))=='W6Earth'),None) or L.create_material_expression(m,unreal.MaterialExpressionTextureObjectParameter,-1400,1900);texture.set_editor_property('parameter_name','W6Earth');texture.set_editor_property('texture',unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Textures/T_HA4_Earth'));assert L.connect_material_expressions(texture,'',color,'W6Earth')
 for a,b in [('p/155.0','(p+v6Warp)/169.0'),('waTurn/267.0','(waTurn+float2(17*sin(p.x*.013),14*cos(p.y*.017)))/281.0'),('p/240.0','(p+v6Warp*.85)/240.0'),('waTurn/391.0','(waTurn-v6Warp*.53)/391.0'),('p/170.0','(p+v6Warp*.35)/170.0')]:assert a in code;code=code.replace(a,b)
 needle='float waDistance=abs(p.y+320)-66;float waU=waRiverRegion*smoothstep(-5,18,waDistance)*(1-smoothstep(85,205,waDistance));';assert needle in code;code=code.replace(needle,needle+'waU=lerp(waU,v6BankMask,v6R*v6BridgeProtected);')
 needle='if(Mode<.5)return g;';assert needle in code
 insert=(A/'SurfaceColor.hlsl').read_text();code=code.replace(needle,insert+'\n'+needle)
 needle='if(Mode<1.5)return d;';assert needle in code;code=code.replace(needle,'d=lerp(d,v6PathColor,v6Scope);'+needle)
 needle='if(Mode<2.5)return d*(1-.08*(1-saturate(edge)));'
 if key!='Ground':
  assert needle in code;code=code.replace(needle,'if(Mode<2.5)return lerp(d*(1-.08*(1-saturate(edge))),v6PathColor,v6Scope);')
 color.set_editor_property('code',code);assert all(L.get_inputs_for_material_expression(m,color));alpha_changes=[]
 for n in expressions:
  if not isinstance(n,unreal.MaterialExpressionCustom) or n==color:continue
  before=source_codes[n.get_name()]
  if 'return a*ends;' not in before:continue
  # World-distance coverage changes only visible road shoulders, not the collision or mesh.
  after=before.replace('return a*ends;','float v6OriginalAlpha=a*ends;'+common+'return lerp(v6OriginalAlpha,v6Coverage,v6Scope);');n.set_editor_property('code',after);alpha_changes.append({'node':n.get_name(),'before':before,'after':after})
 assert len(alpha_changes)==(0 if key=='Ground' else 1);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);rows.append({'key':key,'old':unreal.load_asset(src).get_path_name(),'new':m.get_path_name(),'color_before':old,'color_after':code,'opacity':alpha_changes})
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();result={'materials':rows,'new_meshes':0,'new_textures':0,'existing_geometry_collision_unchanged':True};(S/'Prepared.json').write_text(json.dumps(result,indent=2));(A/'AssetManifest.json').write_text(json.dumps(result,indent=2));unreal.log('WA6_PRIVATE_MATERIALS_READY')
