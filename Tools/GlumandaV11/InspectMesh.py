"""Read-only Blender analysis of genuine boundaries after exact-position seam mapping."""
import bpy,bmesh,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/GlumandaV11';bpy.ops.wm.open_mainfile(filepath=str(R/'Art/Characters/Creatures/Zunderlauf/Source/Glumanda_Meshy_V1.blend'));body=bpy.data.objects['Glumanda_Meshy'];bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.verts.ensure_lookup_table();edges={e for e in bm.edges if e.is_boundary};rows=[]
while edges:
 start=next(iter(edges));component={start};stack=[start]
 while stack:
  e=stack.pop()
  for v in e.verts:
   for other in v.link_edges:
    if other.is_boundary and other not in component:component.add(other);stack.append(other)
 edges-=component;vs={v for e in component for v in e.verts};row={'edges':len(component),'vertices':len(vs),'perimeter_m':sum(e.calc_length()for e in component),'closed_loop':all(sum(e in component for e in v.link_edges)==2 for v in vs),'min':[min(v.co[i]for v in vs)for i in range(3)],'max':[max(v.co[i]for v in vs)for i in range(3)],'points':[list(v.co)for v in vs]};rows.append(row)
rows.sort(key=lambda x:x['perimeter_m']);(O/'BoundaryInspection.json').write_text(json.dumps(rows,indent=2));print(json.dumps([{k:v for k,v in x.items()if k!='points'}for x in rows],indent=2));bm.free()
