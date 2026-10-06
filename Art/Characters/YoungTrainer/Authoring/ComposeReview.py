"""Arrange unmodified native Blender renders into review contact sheets.
Use the bundled workspace Python/Pillow; no installation or AI artwork.
"""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parents[2]/'Saved/YoungTrainerV1/Review'
order=['Front','FrontRight','Right','BackRight','Back','BackLeft','Left','FrontLeft']
for group in ['Turnaround','Elevated']:
 canvas=Image.new('RGB',(1600,1080),(27,34,31));draw=ImageDraw.Draw(canvas)
 for i,n in enumerate(order):
  im=Image.open(OUT/f'{group}_{n}.png').convert('RGB');im.thumbnail((400,500))
  x=(i%4)*400+(400-im.width)//2;y=(i//4)*540
  canvas.paste(im,(x,y));draw.text(((i%4)*400+18,y+509),n,fill=(227,215,185))
 canvas.save(OUT/f'{group}_ContactSheet.jpg',quality=93)
canvas=Image.new('RGB',(1280,850),(27,34,31))
for i,n in enumerate(['Probe_Stride','Probe_Interact']):
 im=Image.open(OUT/f'{n}.png').convert('RGB');canvas.paste(im,(i*640,0))
 ImageDraw.Draw(canvas).text((i*640+15,815),n,fill=(227,215,185))
canvas.save(OUT/'Deformation_ContactSheet.jpg',quality=93)
print('Three native-render contact sheets written:',OUT)
