"""One ordinary PIE session, existing test script, and RAM-only user-save protection."""
from pathlib import Path
import json,sys,time,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GameplayPraxisV1';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
kind,label=sys.argv[1:3];assert label.isalnum();O=D/label;O.mkdir(exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();req={'kind':kind,'label':label};replacements=[]
if kind=='controller':
 root=D/'Controller';root.mkdir(exist_ok=True);(root/'SwitchProRequest.json').write_text(json.dumps({'label':label}));req['source']='Tools/SwitchProControllerV1/Probe.py';replacements=[["O=R/'Saved/ProjectRefinement'","O=R/'Saved/ProjectRefinement/GameplayPraxisV1/Controller'"]];out=root/(label+'.json')
elif kind in ['battle','progression','wild','group']:
 old={'battle':'BattleSystemV3','progression':'CreatureProgressionV1','wild':'WildEncountersV2','group':'WildEncountersV2'}[kind];root=D/kind;root.mkdir(exist_ok=True);data={'label':label,'mode':'PIE'}
 if kind=='wild':data.update(species=sys.argv[3],temperament=sys.argv[4],outcome=sys.argv[5],approach_side='west')
 (root/('Request.json'if kind in ['wild','group']else'ReviewRequest.json')).write_text(json.dumps(data));req['source']='Tools/'+old+('/ReviewEncounter.py'if kind=='wild'else'/ReviewGroup.py'if kind=='group'else'/Review.py');replacements=[['Saved/'+old,'Saved/ProjectRefinement/GameplayPraxisV1/'+kind]];out=root/label/'Result.json'
 if kind in ['wild','group']:(root/label).mkdir(exist_ok=False)
elif kind=='themes':
 root=D/'Themes';root.mkdir(exist_ok=True);(root/'ReviewRequest.json').write_text(json.dumps({'label':label,'mode':'PIE'}));req['source']='Tools/BattleViewV2/Review.py';replacements=[['Saved/BattleViewV2','Saved/ProjectRefinement/GameplayPraxisV1/Themes']];out=root/label/'Result.json'
elif kind=='npc':
 req['source']='Tools/NPCExpansion/ExistingInteractionsPIE.py';replacements=[['Saved/ProjectRefinement/NPCExpansion','Saved/ProjectRefinement/GameplayPraxisV1/'+label]];out=O/'ExistingInteractions.json'
elif kind=='evolution':
 root=D/'Evolution';root.mkdir(exist_ok=True);(root/'ManualReviewRequest.json').write_text(json.dumps({'label':label}));(root/label).mkdir(exist_ok=False);req['source']='Tools/GlutexoEvolutionV2/ReviewManualEvolution.py';replacements=[['Saved/GlutexoEvolutionV2','Saved/ProjectRefinement/GameplayPraxisV1/Evolution']];out=root/label/'Result.json'
elif kind=='follower':req['source']='Tools/GameplayPraxisV1/Follower.py';out=O/'Result.json'
elif kind=='repertoire':req['source']='Tools/GameplayPraxisV1/Repertoire.py';out=O/'Result.json'
elif kind=='movement':req['source']='Tools/GameplayPraxisV1/Movement.py';out=O/'Motion/Result.json'
elif kind=='collision':req['source']='Tools/GameplayPraxisV1/Collision.py';out=O/'Result.json'
elif kind=='e2e':req['source']='Tools/GameplayPraxisV1/EndToEnd.py';out=O/'Footrun/Result.json'
else:raise ValueError(kind)
req['replacements']=replacements;req['result']=str(out.relative_to(R));(D/'Request.json').write_text(json.dumps(req,indent=2));job('script','Tools/GameplayPraxisV1/Prepare.py');job('start_pie');job('script','Tools/GameplayPraxisV1/Guard.py')
guard_start=time.monotonic()
while not(O/'Guard.json').exists():
 if(O/'GuardFailure.json').exists()or time.monotonic()-guard_start>12:
  failure=(O/'GuardFailure.json').read_text()if(O/'GuardFailure.json').exists()else'Guard timeout'
  (O/'InitializationFailure.json').write_text(failure);job('script','Tools/GameplayPraxisV1/Teardown.py');job('stop_pie');raise RuntimeError(failure)
 time.sleep(.1)

if kind=='evolution':
 # The legacy evolution test requires the existing default auto-offer path, after RAM protection.
 job('script','Tools/GameplayPraxisV1/EnableEvolution.py')
try:job('script','Tools/GameplayPraxisV1/Legacy.py')
except Exception as error:
 (O/'InitializationFailure.json').write_text(json.dumps({'error':str(error),'kind':kind},indent=2));job('script','Tools/GameplayPraxisV1/Teardown.py');job('stop_pie');assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha;raise
start=time.monotonic();last=''
while not out.exists():
 assert time.monotonic()-start<1000,'Timeout: retain RAM-protected session for inspection'
 time.sleep(2)
 for path in [out.parent/'Progress.json',out.parent/(label+'_Progress.json')]:
  if path.exists():
   now=path.read_text()
   if now!=last:v=json.loads(now);print(v.get('step',v.get('last',str(v)[:160]))if isinstance(v,dict)else v[-1].get('name'),flush=True);last=now
r=json.loads(out.read_text());job('script','Tools/GameplayPraxisV1/Teardown.py');job('stop_pie');assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha,'Stop: user save differs; never restore blindly'
(O/'Run.json').write_text(json.dumps({'kind':kind,'source':req['source'],'result':req['result'],'passed':r['passed'],'save_unchanged':True,'save_copied_or_renamed':False,'normal_pie_start_stop':True},indent=2));assert r['passed'],r.get('error');print('PRAXIS_PIE_PASS',kind,label,flush=True)
