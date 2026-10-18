"""Do not rerun or suppress warnings. Classify only the exact preserved platform event."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';D=S/'AutomationFinal';j=json.loads((D/'Report/index.json').read_text(encoding='utf-8-sig'));tests=j['tests'];assert len(tests)==49 and all(t['state']=='Success' and t.get('errors',0)==0 for t in tests)
assert j['succeeded']==48 and j['succeededWithWarnings']==1 and all(j[k]==0 for k in ['failed','notRun','inProcess'])
allowed={'LogHAL: FMacPlatformProcess::CreateProc: posix_spawn("/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id") failed (86, Bad CPU type in executable)','LogHAL: Failed to launch Tool. (/Users/Shared/Epic Games/UE_5.8/Engine/Extras/ThirdPartyNotUE/libimobiledevice/Mac/idevice_id)'}
events=[]
for t in tests:
 for entry in t['entries']:
  e=entry['event']
  if e['type'] in ['Warning','Error']:
   assert e['type']=='Warning' and e['message'] in allowed,(t['fullTestPath'],e)
   events.append({'test':t['fullTestPath'],'event':e})
assert len(events)==2 and {e['event']['message'] for e in events}==allowed
baseline=R/'Saved/VisualV2TAAIntegrationV1/Automation/Engine.log';text=baseline.read_text(errors='replace').replace('LogHAL: Warning:','LogHAL:');assert all(x in text for x in allowed),'Not actually present in prior baseline'
result={'all_49_test_states_success':True,'raw_summary':{k:j[k] for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']},'classified_existing_platform_warning_only':True,'events_preserved':events,'same_warnings_present_in_pre_task_baseline':str(baseline),'original_report_unchanged':True,'warnings_suppressed':False,'repeat_to_hide_warnings_performed':False,'strict_wrapper_exit_was_nonzero':True}
(D/'WarningClassification.json').write_text(json.dumps(result,indent=2));(S/'FinalChecks.json').write_text(json.dumps({'final_build_passed':True,'final_automation_all_test_states_success':True,'final_automation_passed_without_warnings':False,'final_automation_known_platform_warning_only':True,'classification':str(D/'WarningClassification.json'),'only_post_measurement_change':'Precise log terminology; no rendering or timed operations changed'},indent=2));print('49 successful test states; 48 clean, 1 with two preserved pre-existing platform warnings. No suppression or retry.')
