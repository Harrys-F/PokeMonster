import bpy,array,json,math
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/MeshyBaseV2/Previews';outputs=[]
def page(names,out):
 ims=[bpy.data.images.load(str(P/n),check_existing=False) for n in names];w,h=ims[0].size;assert all(list(im.size)==[w,h] for im in ims);dest=array.array('f',[0.0])*(w*len(ims)*h*4);width=w*len(ims)
 for col,im in enumerate(ims):
  pix=array.array('f',[0.0])*(w*h*4);im.pixels.foreach_get(pix)
  for yy in range(h):dest[(yy*width+col*w)*4:(yy*width+(col+1)*w)*4]=pix[yy*w*4:(yy+1)*w*4]
 result=bpy.data.images.new(out,width=width,height=h,alpha=True);result.pixels.foreach_set(dest);result.filepath_raw=str(P/out);result.file_format=next(i.identifier for i in bpy.types.Image.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG');result.save();outputs.append(result.filepath_raw)
 if len(ims)==2 and 'BeforeAfter' in out:
  a=array.array('f',[0.0])*(w*h*4);b=array.array('f',[0.0])*(w*h*4);ims[0].pixels.foreach_get(a);ims[1].pixels.foreach_get(b);vals=[abs(x-y) for i,(x,y) in enumerate(zip(a,b)) if i%4!=3];return {'mean_abs_rgb_difference':sum(vals)/len(vals),'max_abs_rgb_difference':max(vals),'pixels_not_geometry_metric':True,'left':'V1','right':'V2'}
metrics={}
for view in ['Front','Back']:
 metrics[view]=page(['Compare_'+view+'_V1_Textured.png','Compare_'+view+'_V2_Textured.png'],'BeforeAfter_'+view+'.png')
page(['Compare_Cape_V2_Textured.png','Compare_Cape_V2_Clay.png','Compare_Cape_V2_Wire.png'],'Diagnosis_Cape_Textured_Clay_Wire.png')
page(['Compare_Forearm_V2_Textured.png','Compare_Forearm_V2_Clay.png','Compare_Forearm_V2_Wire.png'],'Diagnosis_Arm_Textured_Clay_Wire.png')
(B/'Review/MeshyBaseV2/VisualComparison.json').write_text(json.dumps({'pages':outputs,'pixel_comparisons':metrics,'interpretation':'Noise, normal encoding and tangent recalculation can create tiny pixel differences. Artist judgement plus exact surface/deformation verification remain required.'},indent=2));print(metrics)
