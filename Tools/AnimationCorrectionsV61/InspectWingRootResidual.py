"""Read-only distinction between true outer residuals and visible dark inner edges."""
import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Glurak/Source/Glurak_AnimationCorrections_V61.blend'));b=bpy.data.objects['Glurak_Body'];bv=BVHTree.FromPolygons([v.co for v in b.data.vertices],[tuple(p.vertices)for p in b.data.polygons],all_triangles=True);attr=b.data.color_attributes['PolishV4'];im=next(n for n in b.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].links[0].from_node.image;pix=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);uv=b.data.uv_layers.active;rows=[]
for p in b.data.polygons:
 c=sum((b.data.vertices[i].co for i in p.vertices),Vector())/3
 if not(p.material_index==0 and .035<abs(c.x)<.67 and .65<c.z<1.52 and .02<c.y<.5 and attr.data[p.loop_start].color[0]<.5):continue
 t=sum((uv.data[i].uv for i in p.loop_indices),Vector((0,0)))/3;r,g,blue=pix[int(t.y*(im.size[1]-1)),int(t.x*(im.size[0]-1)),:3]
 if not(g>r*1.3 and blue>r*1.3):continue
 direction=Vector((0,-1,-.8)).normalized();top=bv.ray_cast(c-direction*3,direction,4)[2]==p.index
 if top:rows.append(dict(face=p.index,center=list(c),normal=list(p.normal),rgb=[float(r),float(g),float(blue)],front=bv.ray_cast(Vector((c.x,-2,c.z)),Vector((0,1,0)),4)[2]==p.index,back=bv.ray_cast(Vector((c.x,2,c.z)),Vector((0,-1,0)),4)[2]==p.index))
(R/'Saved/AnimationCorrectionsV61/GlurakResidualDiagnosis.json').write_text(json.dumps(rows,indent=2));print('Top-back visible dark root faces',len(rows),'outward normal',sum(x['normal'][1]>.05 for x in rows),flush=True)
