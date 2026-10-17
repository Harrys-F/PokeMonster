# V5 optional evidence gate: no gameplay/build validation is skipped here.
import sys as _evidence_sys
from pathlib import Path as _EvidencePath
_evidence_root = next(p for p in _EvidencePath(__file__).resolve().parents if (p/'PokeMonster.uproject').is_file())
_evidence_sys.path.insert(0, str(_evidence_root/'Tools/DevelopmentEvidence'))
from evidence import review_preflight as _review_preflight
_review_preflight(__file__)
"""Layouts of genuine QHD captures; no generated scene pixels. Originals remain untouched."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];D=R/'Art/World/EnvironmentPerfV3/Review';S=D/'Screenshots';C=D/'Comparisons';C.mkdir(exist_ok=False)
try:font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',42)
except OSError:font=ImageFont.load_default()
def find(pattern):
 p=list(S.glob(pattern));assert len(p)==1,(pattern,p);return p[0]
pairs=[('Wald_V2_vs_LOD1_verworfen_QHD.png','Baseline_EnvironmentPerfV2_QHD_01_Wald_*.png','CandidatesQHD_09_Wald_*.png','V2 – unveraendert','Baum-LOD-Test – verworfen'),('Dorf_V1_vs_V3_QHD.png','Baseline_EnvironmentPerfV1_QHD_00_Dorf_*.png','Baseline_EnvironmentPerfV3_QHD_00_Dorf_*.png','V1 – Screen Probe Gather','V3 = V2 – Irradiance Field erhalten'),('Wald_V2_vs_final_V3_QHD.png','Baseline_EnvironmentPerfV2_QHD_01_Wald_*.png','Baseline_EnvironmentPerfV3_QHD_01_Wald_*.png','V2 – Referenz','V3 – Endstand ohne neue LOD-Eingriffe')]
records=[]
for name,pa,pb,ta,tb in pairs:
 a,b=find(pa),find(pb);ia,ib=Image.open(a).convert('RGB'),Image.open(b).convert('RGB');assert ia.size==ib.size==(2560,1440)
 canvas=Image.new('RGB',(5120,1536),(26,29,28));canvas.paste(ia,(0,96));canvas.paste(ib,(2560,96));draw=ImageDraw.Draw(canvas);draw.text((35,25),ta,font=font,fill=(240,235,220));draw.text((2595,25),tb,font=font,fill=(240,235,220));canvas.save(C/name)
 records.append({'output':str((C/name).relative_to(R)),'sources':[str(a.relative_to(R)),str(b.relative_to(R))],'source_dimensions':[2560,1440],'operation':'Side-by-side originals, no scaling; captions above images; no generated scene pixels'})
# Native pixel crops make the discarded contour change inspectable.
a,b=find('Baseline_EnvironmentPerfV2_QHD_01_Wald_*.png'),find('CandidatesQHD_09_Wald_*.png');box=(160,240,860,840);ia,ib=Image.open(a).crop(box),Image.open(b).crop(box);canvas=Image.new('RGB',(1400,680),(26,29,28));canvas.paste(ia,(0,80));canvas.paste(ib,(700,80));draw=ImageDraw.Draw(canvas);draw.text((20,15),'V2 – Stamm/Laub',font=font,fill='white');draw.text((720,15),'LOD-Test – verworfen',font=font,fill='white');canvas.save(C/'Wald_Contour_Detail_Originalpixels.png');records.append({'output':str((C/'Wald_Contour_Detail_Originalpixels.png').relative_to(R)),'sources':[str(a.relative_to(R)),str(b.relative_to(R))],'crop':box,'operation':'Native-pixel crops; no scaling'})
(D/'Comparisons.json').write_text(json.dumps(records,indent=2));print('Comparison layouts',len(records))
