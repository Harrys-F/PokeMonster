"""Local visual refinement after actual game-camera review; only owned V4 graphs."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';L=unreal.MaterialEditingLibrary;assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
for family in ['HealingMeadow','HealingPath','HealingForecourt','LegacyApproach']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV4/Materials/M_HA4_'+family)
 for n in L.get_material_expressions(m):
  if not isinstance(n,unreal.MaterialExpressionCustom):continue
  code=n.get_editor_property('code');old=code
  code=code.replace('smoothstep(-4620,-4510,p.x)','smoothstep(-4620,-4380,p.x+38*sin(p.y*.013+sin(p.x*.007)))').replace('(1-smoothstep(-3670,-3560,p.x))','(1-smoothstep(-3790,-3560,p.x+28*sin(p.y*.019)))').replace('smoothstep(-720,-610,p.y)','smoothstep(-720,-480,p.y+35*sin(p.x*.014))').replace('(1-smoothstep(1080,1190,p.y))','(1-smoothstep(940,1190,p.y+30*cos(p.x*.017)))')
  # Keep a dominant readable texture; use a smaller rotated contribution to interrupt repetition.
  code=code.replace('float3 g2=lerp(Texture2DSample(GTex,GTexSampler,c).rgb,Texture2DSample(NewGrass,NewGrassSampler,painted/255.0+float2(.13,.27)).rgb,localPaint);','float3 g2=lerp(Texture2DSample(GTex,GTexSampler,c).rgb,Texture2DSample(NewGrass,NewGrassSampler,float2(painted.y,-painted.x)/417.0+float2(.37,.11)).rgb,localPaint);')
  n.set_editor_property('code',code);rows.append({'family':family,'before':old,'after':code})
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Ivy has thin wall-facing surfaces. Use a dedicated controlled leaf tint, preserving the cutaway mask.
D='/Game/Environment/VisualV2HealingArtV4';p=D+'/Materials/M_HA4_Ivy';assert not unreal.EditorAssetLibrary.does_asset_exist(p);m=unreal.EditorAssetLibrary.duplicate_asset(D+'/Materials/M_HA4_Foliage',p)
c=L.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,0,0);c.set_editor_property('constant',unreal.LinearColor(.045,.105,.022,1));assert L.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR);L.delete_unused_expressions(m);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
for name in ['IvySprigA','IvySprigB']:
 mesh=unreal.load_asset(D+'/Meshes/SM_HA4_'+name);mesh.set_material(0,m);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
(S/'Refinements.json').write_text(json.dumps(rows,indent=2));manifest=json.loads((R/'Art/World/VisualV2HealingArtV4/AssetManifest.json').read_text());manifest['assets'].append(p);(R/'Art/World/VisualV2HealingArtV4/AssetManifest.json').write_text(json.dumps(manifest,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
# Reimport/material authoring can mark the level dirty; no out-of-scope scene changes are saved.
sys=__import__('sys');sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
current=scene(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world());expected=json.loads((S/'CandidateScene.json').read_text());oldnames={r['name'] for r in json.loads((S/'Delta.json').read_text())['changed'] if 'Ivy_' in r['label']}
for value in [current,expected]:
 for name,row in value['actors'].items():
  row['components'].sort(key=lambda c:c['name'])
  if name in oldnames:
   for comp in row['components']:
    if 'materials' in comp:comp['materials']=[p+'.M_HA4_Ivy']
assert current==expected,'Unexpected scene change';(S/'CandidateScene.json').write_text(json.dumps(current,indent=2));unreal.log('HA4_REVIEW_REFINEMENT_COMPLETE')
