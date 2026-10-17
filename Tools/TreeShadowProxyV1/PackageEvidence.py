# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
from pathlib import Path
import json,shutil,zipfile,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];O=R/'Saved/TreeShadowProxyV1';N=R/'Saved/EnvironmentPerfV2';D=R/'Art/World/TreeShadowProxyV1/Review';E=D/'Evidence';E.mkdir(exist_ok=True)
for name in ['SceneBefore.json','MapCopy.json','ImportPlace.json','Refinement.json','CollisionFix.json','MapValidation.json','RuntimeAudit.json','BarkDistance.json','Preservation.json','AutomationSummary.json','AutomationExit.json','EditorBeforeTests.json','GitBefore.txt','Head.txt']:
 p=O/name
 if p.exists():shutil.copy2(p,E/name)
shutil.copy2(O/'Automation/index.json',E/'Automation_index.json')
log=(O/'EditorRestart.log').read_text(errors='replace');checks=[s for s in log.splitlines() if 'MapCheck:' in s or 'TREE_SHADOW_MAP' in s];(E/'MapCheck.txt').write_text('\n'.join(checks)+'\n')
with zipfile.ZipFile(E/'RawMeasurements.zip','w',zipfile.ZIP_DEFLATED) as z:
 for i in range(1,7):
  label='TreeShadowProxyV1_C'+str(i)
  for p in list(N.glob(label+'_*'))+list(O.glob(label+'*'))+list((R/'Saved/Profiling/CSV').glob('ENV2_'+label+'_*.csv')):
   if p.is_file():z.write(p,str(p.relative_to(R/'Saved')))
 for name in ['Thermal.jsonl','Crash_MaterialQualitySwitch.log','EditorRestart.log','Automation.log','BeforeFiles.json','RuntimeAudit.json','BarkCoordinates.json']:
  p=O/name
  if p.exists():z.write(p,'TreeShadowProxyV1/'+name)
walk=sorted(O.glob('Walk_*.png'));assert len(walk)>=20
selected=walk[-18::3];images=[];contact=Image.new('RGB',(1440,864),(24,24,24));draw=ImageDraw.Draw(contact)
for i,p in enumerate(selected):
 out=D/('WalkReview_'+str(i+1).zfill(2)+'.png');shutil.copy2(p,out);im=Image.open(p).convert('RGB');im.thumbnail((480,400));x=i%3*480;y=i//3*432;contact.paste(im,(x,y));draw.text((x+8,y+407),p.stem,fill='white')
contact.save(D/'WalkContact.jpg',quality=92)
for p in walk:
 im=Image.open(p).convert('RGB');im.thumbnail((960,540));images.append(im)
images[0].save(D/'WalkSequence.gif',save_all=True,append_images=images[1:],duration=2000,loop=0,optimize=True)
(D/'WalkSequence.json').write_text(json.dumps({'source_images':[str(p.relative_to(R)) for p in walk],'capture_interval_seconds':2,'playback_duration_ms':2000,'synthetic':False,'note':'Sampled genuine Unreal walking frames; not a continuous video and not a high-frequency flicker test.'},indent=2))
manifest=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='EvidenceManifest.json'];(D/'EvidenceManifest.json').write_text(json.dumps(manifest,indent=2));print(len(manifest),'evidence files',round(sum(x['bytes'] for x in manifest)/1024**2,2),'MiB')
