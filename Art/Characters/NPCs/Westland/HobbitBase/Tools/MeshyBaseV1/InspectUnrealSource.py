import sys,time,json
from pathlib import Path
sys.path.insert(0,'/Users/Shared/Epic Games/UE_5.8/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python')
import remote_execution as re
out=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Review/MeshyBaseV1/UnrealSourceAudit.json')
r=re.RemoteExecution();result={}
try:
 r.start()
 for _ in range(30):
  if r.remote_nodes:break
  time.sleep(.1)
 nodes=r.remote_nodes;result['nodes']=nodes
 nodes=[n for n in nodes if n.get('project_name')=='PokeMonster' or 'PokeMonster' in n.get('project_root','')]
 if len(nodes)==1:
  r.open_command_connection(nodes[0]['node_id'])
  code='''import unreal,json
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
audit={'project':unreal.Paths.project_dir(),'map':E.get_editor_world().get_path_name(),'dirty_maps_before':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content_before':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
base='/Game/Characters/YoungTrainer/MeshyV2/'
mesh=unreal.load_asset(base+'Meshes/SK_Player_Meshy_V2')
audit['mesh']=mesh.get_path_name();audit['skeleton']=mesh.skeleton.get_path_name()
try:audit['mesh_import_sources']=mesh.get_editor_property('asset_import_data').extract_filenames()
except Exception as ex:audit['import_source_error']=str(ex)
audit['animations']=[]
for name in ['A_Player_Meshy_Idle_V2','A_Player_Meshy_Walk_V2','A_Player_Meshy_Run_V1']:
 a=unreal.load_asset(base+'Animations/'+name)
 row={'asset':a.get_path_name(),'seconds':a.get_play_length(),'skeleton':a.get_editor_property('skeleton').get_path_name(),'root_motion':a.get_editor_property('enable_root_motion')}
 try:row['import_sources']=a.get_editor_property('asset_import_data').extract_filenames()
 except Exception as ex:row['import_source_error']=str(ex)
 audit['animations'].append(row)
audit['player_components']=[]
try:
 cls=unreal.load_class(None,'/Script/PokeMonster.PokeMonsterPlayerCharacter');cdo=unreal.get_default_object(cls)
 components=cdo.get_components_by_class(unreal.SkeletalMeshComponent)
 for comp in components:
  row={'component':comp.get_path_name(),'mesh':comp.get_editor_property('skeletal_mesh').get_path_name()}
  for prop in ['idle_animation','walk_animation','run_animation']:
   v=comp.get_editor_property(prop);row[prop]=v.get_path_name() if v else None
  audit['player_components'].append(row)
except Exception as ex:audit['component_error']=str(ex)
audit['pie_running']=bool(E.get_game_world())
audit['dirty_maps_after']=[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()];audit['dirty_content_after']=[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print(json.dumps(audit))'''
  response=r.run_command(code,exec_mode=re.MODE_EXEC_FILE);result['response']=response
 else:result['availability']='No unambiguous existing PokeMonster remote Python session; no settings changed.'
except Exception as e:result['error']=str(e)
finally:r.stop()
out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
