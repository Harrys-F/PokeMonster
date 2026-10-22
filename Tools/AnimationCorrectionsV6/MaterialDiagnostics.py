import bpy,numpy as np,json
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[2];out={}
for n in ['Nebulak','Glurak']:
 bpy.ops.wm.open_mainfile(filepath=str(R/f'Art/Characters/Creatures/{n}/Source/{n}_MotionV5.blend'));o=bpy.data.objects[n+'_Body'];im=next(x for x in o.data.materials[0].node_tree.nodes if x.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;pix=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);r=[]
 for p in o.data.polygons:
  uv=sum((o.data.uv_layers.active.data[i].uv for i in p.loop_indices),Vector((0,0)))/len(p.loop_indices);rgb=pix[int((uv.y%1)*(im.size[1]-1)),int((uv.x%1)*(im.size[0]-1)),:3];c=sum((o.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
  if n=='Nebulak'and p.material_index==1 and abs(c.x)<.42 and .15<c.z<.86:r.append((list(c),rgb.tolist()))
 out[n]=dict(image=im.name,image_size=list(im.size),transparent_core_examples=r[::max(1,len(r)//35)],count=len(r))
(R/'Saved/AnimationCorrectionsV6/MaterialAudit.json').write_text(json.dumps(out,indent=2))
