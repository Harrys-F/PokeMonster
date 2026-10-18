"""No save: compare both editor worlds to the protected central scene signature."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
reference=json.loads((O/'SourceScene.json').read_text());results=[]
for package in ['/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1','/Game/Maps/Dev_TestMap_VisualV2']:
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 assert unreal.EditorLoadingAndSavingUtils.load_map(package)
 current=scene(e.get_editor_world());normalized=json.dumps(current,sort_keys=True).replace('Dev_TestMap_VisualV2GPUBottleneckV1','Dev_TestMap_VisualV2')
 assert normalized==json.dumps(reference,sort_keys=True),package
 unreal.SystemLibrary.execute_console_command(e.get_editor_world(),'MAP CHECK')
 results.append({'package':package,'scene_identical':True,'actors':len(current['actors'])})
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1')
(O/'FinalMapAudit.json').write_text(json.dumps({'maps':results,'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]},indent=2))

# Validate finished PIE data before spending time on native measurement. No timing is active here.
import subprocess
# Export only the trace table-of-contents while the editor is idle, never during timings.
external=Path.home()/'Documents/Codex/PokeMonster_VisualV2_GPU_Bottleneck_V1_2026-10-17'
trace=external/'MetalSystemTrace.trace'
if trace.exists() and (external/'MetalSystemTrace_Result.json').exists() and json.loads((external/'MetalSystemTrace_Result.json').read_text()).get('complete') and not (external/'MetalTOC.xml').exists():
 with (external/'MetalTOC_Export.log').open('w') as f:
  exported=subprocess.run(['xcrun','xctrace','export','--input',str(trace),'--toc','--output',str(external/'MetalTOC.xml')],stdout=f,stderr=subprocess.STDOUT,timeout=60)
 (external/'MetalTOC_ExportResult.json').write_text(json.dumps({'exit':exported.returncode}))
analysis_label='FinalAnalysis' if (R/'Saved/EnvironmentPerfV2/VGB1_Final_Standalone_Base_8_Done.txt').exists() else 'PreNativeAnalysis'
with (O/(analysis_label+'.log')).open('w') as f:result=subprocess.run(['/usr/bin/python3',str(R/'Tools/VisualV2GPUBottleneckV1/Analyze.py')],stdout=f,stderr=subprocess.STDOUT)
assert result.returncode==0, 'Finished PIE measurements failed validation; inspect PreNativeAnalysis.log'
(O/(analysis_label+'.json')).write_text(json.dumps({'exit':result.returncode,'validated_before_native':analysis_label=='PreNativeAnalysis'},indent=2))
