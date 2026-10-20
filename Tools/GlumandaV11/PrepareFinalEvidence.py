"""Contact sheets from verified real captures only. Local Saved output, never imported art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,shutil
R=Path(__file__).resolve().parents[2];O=R/'Saved/GlumandaV11/Evidence';O.mkdir(exist_ok=True);S=R/'Saved/GlumandaV11/SightAccepted';j=json.loads((S/'Result.json').read_text());assert j['passed']and math.dist(j['rows'][0]['camera'],j['rows'][1]['camera'])<.001
out=Image.new('RGB',(2560,754),'#19251f');d=ImageDraw.Draw(out)
for i,(prefix,label)in enumerate([('A_Original','A: vorher, Radien 55 / 110 cm'),('B_DoubleDiameter','B: nachher, Radien 110 / 220 cm')]):
 files=list(S.glob(prefix+'*.png'));assert len(files)==1;im=Image.open(files[0]);assert im.size==(2560,1440);out.paste(im.resize((1280,720)),(i*1280,34));d.text((i*1280+14,10),label+' - echte QHD-Spielkamera',fill='white')
out.save(O/'Sichtkreis_Vergleich.png')
for name,source in [('ClassicBattle_Unreal.png','ClassicIdleFinal'),('WorldBattle_Unreal.png','WorldBattle01')]:
 p=R/'Saved/GlumandaV11/LiveUI'/source/'ActualSlateViewport.png';assert p.exists();im=Image.open(p);assert im.size==(2027,1140);shutil.copyfile(p,O/name)
(O/'FinalEvidenceMethod.json').write_text(json.dumps({'battle':'actual Slate viewport screenshot, 2027 x 1140, not QHD','sight':'two actual 2560 x 1440 framebuffer shots with identical cameras; contact sheet downscaled 50 percent','concept_images_used_as_evidence':False},indent=2));print('REAL_EVIDENCE_PREPARED')
