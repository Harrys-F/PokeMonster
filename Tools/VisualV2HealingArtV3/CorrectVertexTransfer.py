"""FBX stores sRGB vertex colours; decode to linear albedo rather than reducing scene lighting."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';L=unreal.MaterialEditingLibrary;E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();proof=[]
decode='float3 a=lerp(C/12.92,pow(max((C+.055)/1.055,0),2.4),step(.04045,C));'
for family in ['Foliage','Blossom']:
 m=unreal.load_asset('/Game/Environment/VisualV2HealingArtV3/Materials/M_HA3_'+family);n=next(n for n in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if n.get_outer()==m);before=n.get_editor_property('code');after=decode+('float vein=exp(-abs(UV.x-.5)*95)*sin(UV.y*3.14159);float minor=(1-smoothstep(.03,.07,abs(frac(UV.y*7+abs(UV.x-.5)*2.3)-.5)))*sin(UV.y*3.14159);return a*(1+.16*vein+.045*minor);' if family=='Foliage' else 'return a;');n.set_editor_property('code',after);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);proof.append({'material':m.get_path_name(),'before':before,'after':after,'cause':'FBX sRGB-coded vertex colours read as raw linear values; measured render-data palette versus Blender/FBX roundtrip'})
(S/'VertexTransferCorrection.json').write_text(json.dumps(proof,indent=2));unreal.log('HA3_VERTEX_COLOUR_TRANSFER_CORRECTED')
