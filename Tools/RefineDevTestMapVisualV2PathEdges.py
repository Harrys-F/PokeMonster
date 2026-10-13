"""Remove coplanar ribbon junction artifacts without touching collision or shared materials."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();o=r/'Saved/DevTestMapVisualV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not e.get_game_world()
m=unreal.load_asset('/Game/Environment/DevTestMapVisualV2/Materials/M_V2_PathBlend');l=unreal.MaterialEditingLibrary
expr=[x for x in unreal.ObjectIterator(unreal.MaterialExpressionCustom) if x.get_outer()==m]
color=next(x for x in expr if x.get_editor_property('output_type')==unreal.CustomMaterialOutputType.CMOT_FLOAT3)
code=color.get_editor_property('code');old='if(Mode<2.5)return lerp(g,d*(1-.08*(1-saturate(edge))),alpha*ends);';new='if(Mode<2.5)return d*(1-.08*(1-saturate(edge)));'
assert old in code or new in code; color.set_editor_property('code',code.replace(old,new))
m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('opacity_mask_clip_value',.333)
mask=next((x for x in expr if x.get_editor_property('desc')=='VisualV2 path edge opacity'),None)
if not mask:
 mask=l.create_material_expression(m,unreal.MaterialExpressionCustom,400,650);mask.set_editor_property('desc','VisualV2 path edge opacity');mask.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1)
 inputs=[]
 for n in ['P','UV']:
  i=unreal.CustomInput();i.set_editor_property('input_name',n);inputs.append(i)
 mask.set_editor_property('inputs',inputs);mask.set_editor_property('code','float irregular=sin(P.x*.027+sin(P.y*.04))*.035+sin(P.x*.073)*.018;float edge=abs(UV.y*2-1)+irregular;float a=1-smoothstep(.72,.99,edge);float ends=smoothstep(0,.018,UV.x)*(1-smoothstep(.982,1,UV.x));return a*ends;')
 pos=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionWorldPosition) if x.get_outer()==m);uv=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionTextureCoordinate) if x.get_outer()==m)
 assert l.connect_material_expressions(pos,'',mask,'P');assert l.connect_material_expressions(uv,'',mask,'UV')
 d=l.create_material_expression(m,unreal.MaterialExpressionMaterialFunctionCall,650,650);d.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));assert l.connect_material_expressions(mask,'',d,'Alpha Threshold');assert l.connect_material_property(d,'',unreal.MaterialProperty.MP_OPACITY_MASK)
l.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
paths=[]
for i,name in enumerate(['Main','Wild','VillageLoop','NorthLoop','Cottage']):
 a=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label()=='V2_Path_'+name)
 a.set_actor_location(unreal.Vector(0,0,.15+i*.15),False,False);paths.append({'label':a.get_actor_label(),'world_z_cm':1.5+i*.15,'collision':str(a.static_mesh_component.get_collision_enabled())})
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(o/'PathEdges.json').write_text(json.dumps({'cause':'Coplanar intersecting opaque grass-edge ribbons','solution':'Scoped masked/dithered earth ribbon edges; staggered visual heights; unchanged collision','paths':paths},indent=2))
