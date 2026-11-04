"""Verify completed migration evidence without changing maps or saves."""
from pathlib import Path
import json,struct,re
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
labels=['PIEReview03','PIEProgression01','PIERoomFinal01','NativeBefore01','NativeAfter01','NativeFeatures02','NativeRestart01','NativeAccess03','NativeViewsBefore01','NativeViewsAfter01','NativeRoomFinal01','NativeRoomBenchmark01','NativeAfterFinal01']
rows=[]
for name in labels:
 r=load(D/name/'Result.json');assert r['passed'],(name,r.get('error'))
 if name.startswith('Native'):assert load(D/name/'ProcessExit.json')['returncode']==0
 rows.append(dict(label=name,passed=True))
assert load(D/'NativeTour01/Tour_review.json')['passed']and load(D/'NativeTour01/ProcessExit.json')['returncode']==0
q=load(D/'Automation05/Result.json');assert q['strict_wrapper_exit']==0 and q['engine_exit']==0 and q['summary']==dict(succeeded=339,succeededWithWarnings=0,failed=0,notRun=0,inProcess=0)
text=(D/'EditorGroundFinal01/Engine.log').read_text(errors='replace');checks=[]
for name,section in re.findall(r'VISUALV2_FAB_V1_MAPCHECK_BEGIN ([^\n]+)\n(.*?)VISUALV2_FAB_V1_MAPCHECK_END',text,re.S):
 matches=re.findall(r'MapCheck: Kartenprüfung abgeschlossen: (\d+) Fehler, (\d+) Warnung',section);assert len(matches)==1 and matches[0]==('0','0'),(name,matches);checks.append(dict(map=name,errors=0,warnings=0))
assert len(checks)==12;(D/'MapCheckResultsFinal.json').write_text(json.dumps(checks,indent=2))
photos=[]
for label in ['NativeViewsBefore01','NativeViewsAfter01','NativeRoomFinal01']:
 for p in(D/label).glob('*.png'):
  header=p.read_bytes()[:24];assert header[:8]==b'\x89PNG\r\n\x1a\n';size=struct.unpack('>II',header[16:24]);assert size==(2560,1440),(str(p),size);photos.append(str(p.relative_to(D)))
assert len(photos)==65;assert load(D/'ProtectionAudit.json')['passed'];assert load(D/'SceneAudit.json')['passed'];r=dict(passed=True,runtime_checks=rows,automation=q['summary'],strict_wrapper_exit=0,map_checks=len(checks),qhd_original_photos=len(photos),photos=photos,full_road_centerline_limitation='Existing Gartenhaus approach centerline intersects unchanged rear wall; no claim all eleven original centerlines passed')
(D/'EvidenceFinal.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items()if k not in ['photos','runtime_checks']},indent=2))
