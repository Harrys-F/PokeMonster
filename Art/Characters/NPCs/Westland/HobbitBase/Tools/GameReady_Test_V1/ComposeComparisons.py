import bpy,array,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1/Previews';q=[]
for prefix in ['01_FaceFront','02_FaceThreeQuarter','03_FaceProfile','04_HairFront','05_HairSide','06_HairBack','07_Torso','08_HeadClay','09_HeadWire','10_TorsoClay','11_TorsoWire','12_2_5D','13_EyeMouthWire','14_VestDetail']:
 paths=[P/(prefix+'_'+suffix+'.png') for suffix in ['A_HP','B_TriangleControl']];ims=[bpy.data.images.load(str(p),check_existing=False) for p in paths];w,h=ims[0].size;assert all(tuple(im.size)==(w,h) for im in ims);dest=array.array('f',[0])*(w*2*h*4)
 for col,im in enumerate(ims):
  pix=array.array('f',[0])*(w*h*4);im.pixels.foreach_get(pix)
  for row in range(h):dest[(row*w*2+col*w)*4:(row*w*2+(col+1)*w)*4]=pix[row*w*4:(row+1)*w*4]
 out=P/(prefix+'_A_vs_B.png');im=bpy.data.images.new(out.stem,width=w*2,height=h,alpha=True);im.pixels.foreach_set(dest);im.filepath_raw=str(out);im.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');im.save();q.append({'path':str(out),'left':'A complete unchanged Highpoly','right':'B rejected triangle control with baked materials; untested regions retained at Highpoly'});
 for p in ims+[im]:bpy.data.images.remove(p)
(B/'Review/GameReady_Test_V1/ComparisonPages.json').write_text(json.dumps(q,indent=2));print('COMPARISON_PAGES_CREATED',flush=True)
