"""Only crop/label genuine matched QHD screenshots. No painted or generated content."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[2];D=R/'Saved/AnimationCorrectionsV61/AlignedAB05';out=R/'Saved/AnimationCorrectionsV61/DetailsFinal';out.mkdir(exist_ok=False);receipt=[]
for name,box in [('PlayerWalk',(1130,590,1450,940)),('PlayerRun',(1130,590,1450,940)),('GlurakRear',(1000,170,1560,620))]:
 pieces=[]
 for label in ['Before','After']:
  p=D/(name+label+'00000.png');im=Image.open(p);assert im.size==(2560,1440);crop=im.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2),Image.Resampling.NEAREST);canvas=Image.new('RGB',(crop.width,crop.height+40),(24,24,24));canvas.paste(crop,(0,40));ImageDraw.Draw(canvas).text((12,12),'V6'if label=='Before'else'V6.1',fill='white');pieces.append(canvas)
 sheet=Image.new('RGB',(sum(x.width for x in pieces),pieces[0].height),(24,24,24));sheet.paste(pieces[0],(0,0));sheet.paste(pieces[1],(pieces[0].width,0));sheet.save(out/(name+'Comparison.png'));receipt.append(dict(name=name,sources=[str((D/(name+x+'00000.png')).relative_to(R))for x in ['Before','After']],crop_pixels=box,scale=2,method='nearest-neighbor magnification only; no generated details'))
(out/'Receipt.json').write_text(json.dumps(receipt,indent=2))
