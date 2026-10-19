"""Compose and measure actual Unreal captures. Never changes their light/color/content."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2ShadowQualityV8';O=Path('/Users/harry/Documents/Codex/PokeMonster_ShadowQuality_V8_2026-10-19');D=O/'Comparisons';D.mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24);manifest=[];measure=[]
for mode in ['PIE','Standalone']:
 dirs={v:S/'Photos'/(mode+'_'+v) for v in ['A','B','C']}
 if not all((d/'Result.json').exists() for d in dirs.values()):continue
 metadata={v:{r['name']:r for r in json.loads((d/'Result.json').read_text())} for v,d in dirs.items()}
 for name,a in metadata['A'].items():
  images=[];paths=[]
  for variant in ['A','B','C']:
   row=metadata[variant][name]
   for key in ['player','camera','camera_rotation_rpy']:assert max(abs(x-y) for x,y in zip(a[key],row[key]))<.02,(mode,name,key)
   assert row['viewport']==[2560,1440] and row['fov']==35 and row['percentage']==row['screen_percentage_cvar']==row['secondary_percentage_cvar']==100 and row['dynamic_resolution_mode']==0
   path=next(dirs[variant].glob(name+'*.png'));im=Image.open(path).convert('RGB');assert im.size==(2560,1440);images.append(im);paths.append(path)
  board=Image.new('RGB',(3840,766),(22,25,22));draw=ImageDraw.Draw(board)
  for i,(im,label) in enumerate(zip(images,['A – Original','B – Ziel ca. 25 % heller','C – Ziel ca. 50 % heller'])):
   board.paste(im.resize((1280,720),Image.Resampling.LANCZOS),(i*1280,46));draw.text((i*1280+15,10),label+' | '+name,fill='white',font=font)
  dest=D/(mode+'_'+name+'_ABC.jpg');board.save(dest,quality=95)
  manifest.append({'mode':mode,'view':name,'comparison':str(dest),'originals':[{ 'variant':v,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for v,p in zip(['A','B','C'],paths)]})
  crops={}
  if name=='Wald':crops={'BodenUndFigur':(1040,620,1700,1030)}
  if name=='Spielfigur':crops={'Figurenkontakt':(1040,650,1470,930)}
  if name=='Gebaeudeschatten':crops={'FassadeUndBoden':(1300,180,2250,740)}
  for key,box in crops.items():
   width=box[2]-box[0];height=box[3]-box[1];detail=Image.new('RGB',(width*3,height+46),(22,25,22));dr=ImageDraw.Draw(detail)
   for i,im in enumerate(images):detail.paste(im.crop(box),(i*width,46));dr.text((i*width+10,10),['A – Original','B – Versuch','C – Versuch'][i],fill='white',font=font)
   detail.save(D/(mode+'_'+key+'_Detail_ABC.jpg'),quality=97)
  arr=[np.asarray(im,dtype=np.float64)/255 for im in images];luma=[x@np.array([.2126,.7152,.0722]) for x in arr]
  rois={}
  if name=='Wald':rois={'forest_floor_calibration':(1400,770,1650,940),'sunlit_path_control':(1000,1150,1300,1350)}
  if name=='Innenraum':rois={'interior_floor_control':(700,1000,1050,1250)}
  # Project the capsule ground point using the recorded unchanged perspective camera.
  roll,pitch,yaw=a['camera_rotation_rpy'];pitch,yaw=map(math.radians,[pitch,yaw]);f=np.array([math.cos(pitch)*math.cos(yaw),math.cos(pitch)*math.sin(yaw),math.sin(pitch)]);right=np.array([-math.sin(yaw),math.cos(yaw),0]);up=np.cross(f,right);foot=np.array(a['player'])-np.array([0,0,48]);rel=foot-np.array(a['camera']);z=float(rel@f);sx=1280+float(rel@right)/z/math.tan(math.radians(17.5))*1280;sy=720-float(rel@up)/z/math.tan(math.radians(17.5))*1280
  if name in ['Wald','Spielfigur']:rois['projected_foot_contact_control']=(round(sx)-10,round(sy)-2,round(sx)+10,round(sy)+12)
  for key,(x0,y0,x1,y1) in rois.items():
   means=[float(x[y0:y1,x0:x1].mean()) for x in luma];measure.append({'mode':mode,'view':name,'region':key,'pixel_rectangle':[x0,y0,x1,y1],'mean_display_code_luma_A_B_C':means,'relative_percent_B_C':[(means[i]/means[0]-1)*100 for i in [1,2]],'not_physical_shadow_factor_or_exact_perceptual_percent':True})
(D/'Manifest.json').write_text(json.dumps(manifest,indent=2));(O/'ImageMeasurements.json').write_text(json.dumps(measure,indent=2));print(json.dumps({'matched_ABC_views':len(manifest),'measurements':measure},indent=2))
