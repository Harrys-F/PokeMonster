"""Keep engine warnings visible; distinguish test failures from the known external iOS helper."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];label=sys.argv[1];p=R/'Saved/ProjectRefinement'/label/'Report/index.json';d=json.loads(p.read_text(encoding='utf-8-sig'));events=[]
for t in d['tests']:
 if t['warnings']or t['errors']:events.append(dict(test=t['fullTestPath'],state=t['state'],warnings=t['warnings'],errors=t['errors'],entries=t['entries']))
assert d['failed']==0 and d['notRun']==0 and d['inProcess']==0
assert all(t['state']=='Success'and t['errors']==0 for t in d['tests'])
unknown=[e for t in events for e in t['entries']if e['event']['type']=='Warning'and'idevice_id'not in e['event']['message']];assert not unknown,unknown
out=dict(total_success=d['succeeded']+d['succeededWithWarnings'],success_clean=d['succeeded'],success_with_external_warning=d['succeededWithWarnings'],strict_runner_rejected_external_warning=d['succeededWithWarnings']>0,external_events=events,source=str(p.relative_to(R)),note='No warnings suppressed. This assessment does not relabel the strict ProjectQA result as clean.')
(R/'Saved/AnimationCorrectionsV61/AutomationFinalAssessment.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k!='external_events'},indent=2))
