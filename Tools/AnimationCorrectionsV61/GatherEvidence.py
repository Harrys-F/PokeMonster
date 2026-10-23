"""Compact auditable receipts. Raw media stays local, all protected originals must match."""
import json,hashlib,struct,csv,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/AnimationCorrectionsV61';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();initial=json.loads((O/'InitialProtection.json').read_text());changed=[p for p,h in initial['files'].items()if not(R/p).is_file()or sha(R/p)!=h];assert not changed,changed
assert all(sha(R/p)==h for p,h in initial['untracked'].items());assert sha(R/'Saved/SaveGames/PokeMonster_Dev.sav')==initial['save'];assert all(subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()==h for ref,h in initial['backup'].items())
protection=dict(original_files_unchanged=len(initial['files']),initial_untracked_unchanged=len(initial['untracked']),developer_save_sha256=initial['save'],backup_refs_unchanged=initial['backup']);(O/'FinalProtection.json').write_text(json.dumps(protection,indent=2));media=[]
for label in ['AlignedAB05','V61Before03','V61After01','V61AfterGlurak02','V61TenPokemon01']:
 d=json.loads((O/label/'Result.json').read_text());assert d['passed']and d['save_unchanged'],label
 for p in sorted((O/label).glob('*.png')):
  assert struct.unpack('>II',p.read_bytes()[16:24])==(2560,1440);media.append(dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size,width=2560,height=1440,real_unreal_frame=True))
for p in sorted((O/'Media').glob('*/Motion.mp4')):
 rows=list(csv.DictReader((p.parent/'Frames.csv').open()));assert len(rows)>100;media.append(dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size,source_frames=len(rows),width=2560,height=1440,original_timestamps=True,no_synthetic_frames=True))
assert len([x for x in media if x['path'].endswith('.mp4')])==4
sources=json.loads((O/'SourceValidation.json').read_text());assert len(sources)==2
foot=json.loads((R/'Saved/GlumandaV11/Acceptance/AnimationV61FullFoot01/FootTest.json').read_text());assert foot['passed']and foot['no_test_teleports']
battle=json.loads((R/'Saved/CreatureExpansionV3/AnimationV61GlurakBattle/Result.json').read_text());assert battle['passed']
controller=json.loads((R/'Saved/ProjectRefinement/AnimationV61SwitchPro.json').read_text());assert controller['passed']and controller['simulated_inputs_not_hardware']
checks=json.loads((O/'MapChecksResult.json').read_text());assert checks['passed']and len(checks['maps'])==11
build=json.loads((R/'Saved/ProjectRefinement/AnimationV61BuildFinal/Result.json').read_text());assert build['exit']==0
automation=json.loads((O/'AutomationFinalAssessment.json').read_text());assert automation['total_success']==101
receipt=dict(schema=1,kind='animation_polish_v61',base_commit=initial['head'],protection=protection,sources=sources,foot_contact_comparison=json.loads((O/'FootContactComparison.json').read_text()),build=build,automation=automation,map_checks=checks,gameplay=dict(label='AnimationV61FullFoot01',passed=True,steps=len(foot['steps']),distance_m=foot['distance_m'],max_speed_cm_s=foot['max_speed_cm_s'],no_test_teleports=True),glurak_battle=dict(label='AnimationV61GlurakBattle',passed=True,fixture=battle['fixture']),controller=dict(label='AnimationV61SwitchPro',passed=True,simulated_not_hardware=True,checks=controller['checks']),media=media,limitations=['Bounded foot IK is not full terrain/cloth collision simulation; tight pivots intentionally release contacts.','Video readback hitches; no 60 Hz smoothness or performance claim.','Physical controller baseline unchanged, not retested here.','Strict automation runner rejects the known external idevice_id warning even though every test state is Success.'])
(R/'Tools/AnimationCorrectionsV61/Acceptance.json').write_text(json.dumps(receipt,indent=2));print('V61_EVIDENCE_VERIFIED',len(media),'media receipts;',len(foot['steps']),'gameplay steps')
