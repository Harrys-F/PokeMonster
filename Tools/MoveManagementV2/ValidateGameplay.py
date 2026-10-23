"""Validate every full-route receipt, including the supplementary observer the legacy runner omits."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/GlumandaV11/Acceptance'/label
read=lambda n:json.loads((O/n).read_text())
foot,observer,companion,save=map(read,['FootTest.json','CreatureGameplay.json','CompanionResult.json','SaveRestored.json'])
checks={'foot_passed':foot.get('passed')is True,'all_103_steps':len(foot['steps'])==103,'no_test_teleports':foot.get('no_test_teleports')is True,'classic_observer_passed':observer.get('passed')is True,'companion_no_recorded_issues':not companion['issues'],'save_restored':save.get('restored')is True}
result={'label':label,'checks':checks,'passed':all(checks.values()),'observer_error':observer.get('error'),'distance_m':foot['distance_m'],'max_speed_cm_s':foot['max_speed_cm_s'],'note':'No companion visual samples is not positive visual proof; use the separate controller/companion probe.'}
print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed']else 1)
