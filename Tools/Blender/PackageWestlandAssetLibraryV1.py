"""Package this task's newly authored library only; retain original generated checkpoint."""
import bpy,bmesh,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibrary';source=A/'Source/WestlandAssetLibrary_V1.blend';assert Path(bpy.data.filepath)==source
checkpoint=O/'WestlandAssetLibrary_BeforePackaging.blend'
if not checkpoint.exists():shutil.copy2(source,checkpoint)
s=bpy.context.scene;s.name='WestlandAssetLibrary_Review';edit=bpy.data.scenes.get('WestlandAssetLibrary_Source') or bpy.data.scenes.new('WestlandAssetLibrary_Source');edit.unit_settings.system='METRIC';edit.unit_settings.scale_length=1
manifest=json.loads((A/'Assets.json').read_text());cleanup=[]
for a in manifest['assets']:
 c=bpy.data.collections[a['id']];c.hide_viewport=False;c.hide_render=False
 if c.name not in edit.collection.children:edit.collection.children.link(c)
 if c.name in s.collection.children:s.collection.children.unlink(c)
 o=bpy.data.objects[a['object']]
 if a['id']=='WLA_Herb_B':
  for i,k in enumerate(['LeafDark','LeafLight','Leaf']):o.data.materials[i]=bpy.data.materials['WLA_'+k]
 if a['id']=='WLA_Wildflowers_A':
  for i,k in enumerate(['LeafDark','LeafLight','FlowerBlue','FlowerCream','Leaf']):o.data.materials[i]=bpy.data.materials['WLA_'+k]
 a['materials']=[m.name for m in o.data.materials]
 if a['id'].startswith(('WLA_Bush','WLA_Birch')) and not o.get('WLA_leaf_scale_polished'):
  factor=.48 if 'Bush' in a['id'] else .70;adj={v.index:set() for v in o.data.vertices}
  for edge in o.data.edges:
   v0,v1=edge.vertices;adj[v0].add(v1);adj[v1].add(v0)
  todo=set(adj)
  while todo:
   root=todo.pop();group={root};stack=[root]
   while stack:
    for v in adj[stack.pop()]:
     if v in todo:todo.remove(v);group.add(v);stack.append(v)
   fs=[f for f in o.data.polygons if f.vertices[0] in group]
   if len(group)<=24 and fs and all(o.data.materials[f.material_index].name.startswith('WLA_Leaf') for f in fs):
    uv=o.data.uv_layers.active;loops=[li for f in fs for li in f.loop_indices];li=min(loops,key=lambda i:uv.data[i].uv.x);base=o.data.vertices[o.data.loops[li].vertex_index].co.copy()
    for v in group:o.data.vertices[v].co=base+(o.data.vertices[v].co-base)*factor
  o['WLA_leaf_scale_polished']=factor
 before=len(o.data.vertices);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-9],context='FACES');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();o.data.calc_loop_triangles()
 uv=o.data.uv_layers.active;bad=set()
 for t in o.data.loop_triangles:
  p0,p1,p2=[uv.data[i].uv for i in t.loops];det=(p1.x-p0.x)*(p2.y-p0.y)-(p2.x-p0.x)*(p1.y-p0.y)
  if abs(det)<1e-10:bad.add(t.polygon_index)
 for i in bad:
  f=o.data.polygons[i];axis=max(range(3),key=lambda k:abs(f.normal[k]));x,y=((1,2),(0,2),(0,1))[axis]
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[x],v[y])
 o['WLA_uv_cap_faces_fixed']=o.get('WLA_uv_cap_faces_fixed',0)+len(bad);a['uv_cap_faces_fixed']=o['WLA_uv_cap_faces_fixed']
 a['triangles']=len(o.data.loop_triangles);a['dimensions_m']=[round(max(v.co[i] for v in o.data.vertices)-min(v.co[i] for v in o.data.vertices),5) for i in range(3)];cleanup.append({'id':a['id'],'vertices_before':before,'vertices_after':len(o.data.vertices),'triangles':a['triangles']})
 assert all((o.data.vertices[t.vertices[1]].co-o.data.vertices[t.vertices[0]].co).cross(o.data.vertices[t.vertices[2]].co-o.data.vertices[t.vertices[0]].co).length>1e-10 for t in o.data.loop_triangles),a['id']
 o['WLA_art_status']=a.get('art_status','review pending');o['WLA_human_approval']=False
 o.asset_mark();o.asset_data.author='PokeMonster / Westland';o.asset_data.description=a['family']+'; metres; ground pivot; '+a['provenance']
 if a['family'] not in [t.name for t in o.asset_data.tags]:o.asset_data.tags.new(a['family'])
 for key,val in [('WLA_dimensions_m',a['dimensions_m']),('WLA_collision',a['collision']),('WLA_triangles',a['triangles'])]:o[key]=val
for im in bpy.data.images:
 if im.source=='FILE':
  path=Path(bpy.path.abspath(im.filepath));assert path.exists(),path
  im.pack();im.filepath=bpy.path.relpath(str(path),start=str(source.parent))
(A/'Assets.json').write_text(json.dumps(manifest,indent=2)+'\n');(O/'MeshCleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(source));print('WLA_PACKAGED_SOURCE',len(edit.collection.children))
