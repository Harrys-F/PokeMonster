"""Map-local healing-room refinement and two species speed assets. Never touches sources/outdoors."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';ROOT='/Game/Environment/VisualV2InteriorV6';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);ML=unreal.MaterialEditingLibrary;AT=unreal.AssetToolsHelpers.get_asset_tools()
assert W.get_name()=='Dev_TestMap_VisualV2'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not(D/'Authored.json').exists()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=scene(W);(D/'PreAuthorScene.json').write_text(json.dumps(before,indent=2));actors={a.get_actor_label():a for a in A.get_all_level_actors()};created=[];modified=[];assets=[]
assert all(p.get_path_name().startswith(ROOT+'/')for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
def material(name,code,rough=.83,emission=False):
 m=unreal.load_asset(ROOT+'/Materials/M_V6_'+name)or AT.create_asset('M_V6_'+name,ROOT+'/Materials',unreal.Material,unreal.MaterialFactoryNew());ML.delete_all_material_expressions(m);assets.append(m)
 p=ML.create_material_expression(m,unreal.MaterialExpressionWorldPosition,0,0);n=ML.create_material_expression(m,unreal.MaterialExpressionCustom,200,0);i=unreal.CustomInput();i.set_editor_property('input_name','P');n.set_editor_property('inputs',[i]);n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3);n.set_editor_property('code',code);assert ML.connect_material_expressions(p,'',n,'P');assert ML.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR)
 q=ML.create_material_expression(m,unreal.MaterialExpressionConstant,200,200);q.r=rough;ML.connect_material_property(q,'',unreal.MaterialProperty.MP_ROUGHNESS)
 if emission:ML.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 m.set_editor_property('used_with_instanced_static_meshes',True);ML.recompile_material(m);return m
plaster=material('LimePlaster','float b=sin(P.x*.018+sin(P.y*.023))*cos(P.z*.029);float f=sin(P.x*1.1+P.y*.87)*sin(P.z*1.31);return float3(.64,.51,.34)*(1+.045*b+.014*f);')
sage=material('SageLimewash','float b=sin(P.x*.025+P.y*.02)*cos(P.z*.033);return float3(.29,.36,.21)*(1+.045*b);')
glazing=material('FrostedWindow','float f=.92+.04*sin(P.z*.085)+.025*cos(P.x*.06+P.y*.07);return float3(.33,.39,.31)*f;',.42,True)
# Private opaque wood keeps the existing authored texture/normal coordinates; no cutaway or shared edits.
wood=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2WorldOverhaulV3/Materials/M_WOV_Timber',ROOT+'/Materials/M_V6_OakJoinery');assets.append(wood)
for n in ML.get_material_expressions(wood):
 if isinstance(n,unreal.MaterialExpressionCustom):
  c=n.get_editor_property('code')
  if 'float3(0.72,0.53,0.32)'in c:n.set_editor_property('code',c.replace('float3(0.72,0.53,0.32)','float3(.58,.36,.18)'))
ML.recompile_material(wood)
floor=unreal.EditorAssetLibrary.duplicate_asset('/Game/Environment/VisualV2WorldOverhaulV3/Materials/M_WOV_Timber',ROOT+'/Materials/M_V6_OakFloor');assets.append(floor)
for n in ML.get_material_expressions(floor):
 if isinstance(n,unreal.MaterialExpressionCustom):
  c=n.get_editor_property('code')
  if 'float3(0.72,0.53,0.32)'in c:n.set_editor_property('code',c.replace('float3(0.72,0.53,0.32)','float3(.85,.67,.43)'))
ML.recompile_material(floor)
# Restrict all rebinding to the existing relocated room, never a shared asset or outdoor actor.
for label,a in actors.items():
 if not 16000<a.get_actor_location().x<17700:continue
 changed=False
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.is_visible()or c.hidden_in_game:continue
  for i in range(c.get_num_materials()):
   old=c.get_material(i);name=old.get_name()if old else '';m=None
   if 'FrontWall'in label or 'DoorLintel'in label:m=plaster
   elif name in ['M_WOV_Plaster','M_HH_InteriorPlaster']:m=plaster
   elif name=='M_WOV_Timber':m=floor if '_Floor_'in label else wood
   if m:c.set_material(i,m);changed=True
 if changed:modified.append(label)
# Consolidated decorative architecture: one HISM per material. Existing gameplay collisions stay intact.
SUB=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);groups={}
def cube(key,m,pos,size,rotation=None):
 if key not in groups:
  a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('V6_Interior_'+key);a.tags=['VisualV2InteriorV6'];a.set_folder_path('VisualV2/InteriorV6');created.append(a.get_actor_label());h,r=SUB.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=SUB.k2_gather_subobject_data_for_instance(a)[0],new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True));c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h));assert c,r;c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));c.set_material(0,m);c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_editor_property('generate_overlap_events',False);c.set_cast_shadow(True);groups[key]=c
 groups[key].add_instance(unreal.Transform(location=unreal.Vector(*pos),rotation=rotation or unreal.Rotator(),scale=unreal.Vector(*(v/100 for v in size))),True)
# Ceiling sits above the fixed 1.72m eye; exposed lower beams join the existing upper wall plate.
cube('Ceiling',plaster,(16900,500,312),(1020,1220,20))
for x in [16425,16650,16900,17150,17375]:cube('OakFrame',wood,(x,500,290),(18,1180,24))
for y in [-75,500,1075]:cube('OakFrame',wood,(16900,y,298),(1000,16,18))
# Entry wall was bare rock; coherent oak studs, limewash panels and a stone plinth remain legible from behind.
for y in [10,300,700,990]:cube('OakFrame',wood,(16419,y,143),(13,15,286))
for y,w in [(155,480),(845,480)]:
 cube('OakFrame',wood,(16420,y,270),(15,w,18));cube('SageWainscot',sage,(16417,y,34),(5,w,65));cube('OakFrame',wood,(16422,y,69),(10,w,8))
# Short entry reveal conceals the remote-room void beyond the functioning transition threshold.
# The decorative door is well behind the exit threshold and has no gameplay collider.
cube('VestibuleDoor',wood,(16230,500,112),(12,185,224))
for y in [400,600]:cube('VestibuleWall',plaster,(16310,y,150),(180,18,300))
cube('VestibuleCeiling',wood,(16310,500,278),(180,215,18))
for y in [428,500,572]:cube('OakFrame',wood,(16239,y,110),(8,5,212))
for z in [22,190]:cube('OakFrame',wood,(16242,500,z),(10,178,12))
# Existing window apertures receive frosted glazing instead of revealing the unbuilt remote world.
for x in [16630,17210]:
 for y in [-102,1102]:
  cube('Glazing',glazing,(x,y,168),(100,4,130))
  for dx in [-48,0,48]:cube('OakFrame',wood,(x+dx,y+(8 if y<0 else -8),168),(5,8,132))
  cube('OakFrame',wood,(x,y+(8 if y<0 else -8),168),(100,8,5))
for y in [150,850]:
 cube('Glazing',glazing,(17402,y,178),(4,100,130))
 for dy in [-48,0,48]:cube('OakFrame',wood,(17394,y+dy,178),(8,5,132))
 cube('OakFrame',wood,(17394,y,178),(8,100,5))
# Reuse all existing lights, with warm lamps and restrained neutral-cool window light. No extra light actor.
lightrows=[]
for label,a in actors.items():
 if not 16000<a.get_actor_location().x<17700:continue
 for c in a.get_components_by_class(unreal.LightComponent):
  old=dict(intensity=c.intensity,color=str(c.light_color))
  color=unreal.LinearColor(.82,.89,1)if 'WindowLight'in label else unreal.LinearColor(1,.80,.59)
  c.set_light_color(color,True)
  if 'InteriorDiffuse'in label:
   c.set_light_color(unreal.LinearColor(1,.91,.78),True)
   # A single existing shadowless broad area light now supports the room as well as the hero.
   c.set_editor_property('lighting_channels',unreal.LightingChannels(channel0=True,channel1=True,channel2=False));c.set_intensity(1500)
  lightrows.append(dict(actor=label,before=old,after=dict(intensity=c.intensity,color=str(c.light_color))))
# Only these two existing species assets; animation reference stride and all clips remain unchanged.
for name,walk,run in [('Pikachu',42,56),('Karpador',56,61.25)]:
 s=unreal.load_asset('/Game/Data/Creatures/DA_'+name);o=s.get_editor_property('overworld');beforevalues=o.export_text();o.walk_speed_override=walk;o.run_speed_override=run
 if name=='Pikachu':o.minimum_travel=110;o.pause_minimum=.6;o.pause_maximum=1.8
 if name=='Karpador':
  behavior=o.behavior;behavior.walk_multiplier=1.0;o.behavior=behavior
 s.set_editor_property('overworld',o);assets.append(s);modified.append(dict(species=name,before=beforevalues,after=o.export_text()))
for a in assets:assert unreal.EditorAssetLibrary.save_loaded_asset(a,False)
assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_TestMap_VisualV2')
after=scene(W);(D/'SceneAfter.json').write_text(json.dumps(after,indent=2));(D/'Authored.json').write_text(json.dumps(dict(created=created,modified=modified,assets=[a.get_path_name()for a in assets],lights=lightrows,groups={k:v.get_instance_count()for k,v in groups.items()}),indent=2))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
