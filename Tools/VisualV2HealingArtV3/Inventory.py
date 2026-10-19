"""Read-only current cube, exterior plant and ground inventory."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();A=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
cube=next((a for a in A if a.get_actor_label()=='V2_House_HH_V3_SupplyCrate'),None);needle=cube.get_name() if cube else None;cubedata=None;refs=[];plants=[];ground=[]
for a in A:
 for p in a.get_class().properties() if hasattr(a.get_class(),'properties') else []:pass
 # Export the reflected actor text, which includes serialized references and components.
 try:
  task=unreal.AssetExportTask();task.object=a;task.exporter=unreal.ObjectExporterT3D();task.filename=str(S/'ActorProbe.t3d');task.automated=True;task.prompt=False;task.replace_identical=True
  unreal.Exporter.run_asset_export_task(task);raw=(S/'ActorProbe.t3d').read_bytes();txt=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8')
  if cube and a!=cube and (needle in txt or cube.get_path_name() in txt):refs.append({'actor':a.get_actor_label(),'path':a.get_path_name(),'text':txt})
 except Exception:raise
 label=a.get_actor_label();c=a.get_component_by_class(unreal.StaticMeshComponent)
 if not c:continue
 row={'name':a.get_name(),'label':label,'class':a.get_class().get_path_name(),'path':a.get_path_name(),'location':a.get_actor_location().to_tuple(),'scale':a.get_actor_scale3d().to_tuple(),'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'materials':[c.get_material(i).get_path_name() if c.get_material(i) else None for i in range(c.get_num_materials())],'collision':str(c.get_collision_enabled()),'shadow':c.cast_shadow,'tags':[str(x) for x in a.tags]}
 if a==cube:cubedata=row
 if label.startswith('V2_House') and any(x in label.lower() for x in ['plant','herb','pot','flower']):plants.append(row)
 if label in ['V2_Ground','V2_House_Forecourt','V2_Path_VillageLoop','V2_Path_NorthLoop','V2_House_HH_Q2_OrganicApproach']:ground.append(row)
(S/'Inventory.json').write_text(json.dumps({'cube':cubedata,'serialized_actor_referencers':refs,'plants':plants,'ground':ground,'serialized_actor_count_checked':len(A)},indent=2))
# Native engine reference search is supplementary to serialized map/source checks.
if cube:unreal.SystemLibrary.execute_console_command(w,'obj refs name='+cube.get_path_name()+' shortest')
