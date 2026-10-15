import bpy,array,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/4K_Base_V1/Previews';outputs=[]
def grid(names,out,cols):
 ims=[bpy.data.images.load(str(P/n),check_existing=False) for n in names];w,h=ims[0].size;assert all(tuple(im.size)==(w,h) for im in ims);rows=(len(ims)+cols-1)//cols;width=w*cols;height=h*rows;dest=array.array('f',[.04,.04,.04,1])*(width*height)
 for j,im in enumerate(ims):
  pix=array.array('f',[0.0])*(w*h*4);im.pixels.foreach_get(pix);col=j%cols;row=rows-1-j//cols
  for yy in range(h):dest[((row*h+yy)*width+col*w)*4:((row*h+yy)*width+(col+1)*w)*4]=pix[yy*w*4:(yy+1)*w*4]
 result=bpy.data.images.new(out,width=width,height=height,alpha=True);result.pixels.foreach_set(dest);result.filepath_raw=str(P/out);result.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');result.save();outputs.append({'path':result.filepath_raw,'layout_left_to_right_top_to_bottom':names})
 for im in ims:bpy.data.images.remove(im)
 bpy.data.images.remove(result)
grid(['01_Front.png','02_Back.png','03_Left.png','04_Right.png','05_ThreeQuarter.png','06_2_5D_Close.png'],'Review_Views.png',3)
grid(['07_Face_Hair.png','11_Face_Clay.png','12_Face_Wire.png'],'Review_Face_Textured_Clay_Wire.png',3)
grid(['08_Hands.png','19_Hand_R.png','14_Hand_Clay.png','20_Hand_Wire.png'],'Review_Hands.png',2)
grid(['09_Feet.png','15_Feet_Clay.png'],'Review_Feet.png',2)
(B/'Review/4K_Base_V1/PreviewPages.json').write_text(json.dumps(outputs,indent=2));print('REVIEW_PAGES_READY',flush=True)
