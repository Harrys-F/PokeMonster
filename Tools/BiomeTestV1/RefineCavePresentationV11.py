"""Narrow correction of actual reviewed overexposure and masonry-like cliff repetition; biome assets only."""
import unreal,json,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);ES=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world()and w.get_name()=='Dev_BiomeTestMap_V1';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
O=R/'Saved/BiomeTestV11/CavePresentationCorrection.json';assert not O.exists();by={a.get_actor_label():a for a in ES.get_all_level_actors()};rows=[]
for i,lm in enumerate([1200,650,750]):
 c=by['Biome_CaveLocalLight_V11_'+str(i)].get_editor_property('light_component');rows.append({'light':i,'intensity_before':c.intensity,'units_before':str(c.get_editor_property('intensity_units')),'lumens_after':lm});c.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);c.set_intensity(lm)
cut=by['Biome_CaveInterior_V11'];cut.set_editor_property('interior_camera_distance',4550.)
# Retain mossy rock walls; use existing earth material on the cave floor instead of bright huge stone slabs.
ground=unreal.load_asset('/Game/Environment/BiomeTestV1/Materials/M_BiomeGround');by['Biome_CaveFloor_V11'].static_mesh_component.set_material(0,ground)
L=unreal.MaterialEditingLibrary;custom=next(n for n in L.get_material_expressions(ground)if isinstance(n,unreal.MaterialExpressionCustom));code=custom.get_editor_property('code');assert 'Texture2DSample(S,SSampler,P.xy/240.0).rgb'in code and 'float strata'not in code
ci=unreal.CustomInput();ci.set_editor_property('input_name','N');custom.set_editor_property('inputs',list(custom.get_editor_property('inputs'))+[ci]);n=L.create_material_expression(ground,unreal.MaterialExpressionPixelNormalWS);assert L.connect_material_expressions(n,'',custom,'N')
code=code.replace('float3 s=Texture2DSample(S,SSampler,P.xy/240.0).rgb;',"""// World-space painterly rock stratum: no XY-only brick projection on vertical cliffs.
float3 q=P*.014;
float grain=saturate(.5+.21*sin(q.x+sin(q.z*1.31))+.17*sin(q.y*1.43-q.z*.83)+.09*sin(q.x*3.7+q.y*2.1+q.z*2.9));
float strata=pow(saturate(.5+.5*sin(P.z*.073+1.6*sin(P.x*.009)+sin(P.y*.011))),5);
float3 s=lerp(float3(.21,.18,.135),float3(.43,.385,.30),grain)*(1-.17*strata);
s*=.94+.06*sin(P.x*.17+sin(P.y*.19)+P.z*.13);""")
code=code.replace('saturate(V.r));','saturate(V.r)*smoothstep(.62,.92,abs(N.z)));');custom.set_editor_property('code',code);L.recompile_material(ground);assert unreal.EditorAssetLibrary.save_loaded_asset(ground,False)
# Two irregular edge pockets give depth while the tested central and side routes remain clear.
rng=random.Random(68241);created=[];C=math.sqrt(.5)
def room(x,y,z=0):return unreal.Vector(25000+C*(x+y),C*(-x+y),z)
for pocket,(cx,cy)in enumerate([(620,-540),(-550,620)]):
 for j in range(5):
  x=cx+rng.uniform(-100,90);y=cy+rng.uniform(-75,75);a=ES.spawn_actor_from_class(unreal.StaticMeshActor,room(x,y),unreal.Rotator(yaw=rng.uniform(0,360)));a.set_actor_label('Biome_CavePocket_V11_'+str(pocket)+'_'+str(j));a.set_folder_path('BiomeV11/CaveAndPlateau');a.tags=['BiomeTestV1','BiomeV11'];c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_'+('A'if j%2 else'B')));a.set_actor_scale3d(unreal.Vector(rng.uniform(.25,.48),rng.uniform(.25,.42),rng.uniform(.35,.9)));c.set_collision_profile_name('BlockAll');c.set_lighting_channels(False,True,False);c.set_cast_shadow(False);created.append(a.get_actor_label())
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages());assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_BiomeTestMap_V1')
O.write_text(json.dumps({'confirmed_overexposure':rows,'camera_distance_cm':4550,'ground_material':ground.get_path_name(),'cliff_fix':'world-space procedural rock strata only in existing rocky vertex mask; slope suppresses dirt on steep cliff faces','edge_pockets':created,'exterior_lights_changed':False,'original_materials_changed':False},indent=2))
