"""Local caps on two diagnosed gaps. Original geometry, UVs, weights and inputs stay intact."""
import bpy, bmesh, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
R = Path(__file__).resolve().parents[2]
A = R/'Art/Characters/Creatures/Schiggy'
source = A/'Source/Schiggy_Meshy_V1.blend'
out = A/'Source/Schiggy_Surface_V2.blend'
fbx = A/'Exports/SurfaceV2/Schiggy_Surface.fbx'
assert (not out.exists() and not fbx.exists()) or '--revise-generated' in sys.argv
sha = hashlib.sha256(source.read_bytes()).hexdigest()
assert sha == '370643ec5faf226874940278c5b998df610db8ac216acc13de85e1d93fa9fca5'
bpy.ops.wm.open_mainfile(filepath=str(source))
bpy.context.preferences.filepaths.save_version = 0
body = bpy.data.objects['Schiggy_Body']; rig = bpy.data.objects['Schiggy_Rig']; mesh = body.data
positions = [tuple(v.co) for v in mesh.vertices]
faces = [tuple(f.vertices) for f in mesh.polygons]
uvs = [tuple(x.uv) for x in mesh.uv_layers.active.data]
normals = [tuple(n.vector) for n in mesh.corner_normals]
weights = [[(g.group,g.weight) for g in v.groups] for v in mesh.vertices]
# Weld only a temporary helper to identify actual cyclic boundary order across UV splits.
helper = bmesh.new(); helper.from_mesh(mesh)
bmesh.ops.remove_doubles(helper, verts=list(helper.verts), dist=1e-6)
helper.normal_update(); remaining = {e for e in helper.edges if e.is_boundary}
nonmanifold_before = sum(not e.is_manifold for e in helper.edges)
anchors = [Vector((.0649640709,-.1837011129,.3876796365)), Vector((.0850872695,-.1626667082,.3818017542))]
loops = []
while remaining:
    first = remaining.pop(); edges = {first}; todo = [first]
    while todo:
        for v in todo.pop().verts:
            for e in v.link_edges:
                if e in remaining: remaining.remove(e); edges.add(e); todo.append(e)
    vertices = {v for e in edges for v in e.verts}
    center = sum((v.co for v in vertices), Vector())/len(vertices)
    if min((center-a).length for a in anchors) > .0001: continue
    assert len(edges) in (4,5) and all(sum(e in edges for e in v.link_edges)==2 for v in vertices)
    start = min(vertices,key=lambda v:tuple(v.co)); ordered = [start]; previous = None; current = start
    while True:
        choices = [e.other_vert(current) for e in current.link_edges if e in edges and e.other_vert(current)!=previous]
        nxt = min(choices,key=lambda v:tuple(v.co))
        if nxt == start: break
        assert nxt not in ordered
        ordered.append(nxt); previous,current=current,nxt
    assert len(ordered)==len(vertices)
    edge = next(e for e in ordered[0].link_edges if ordered[1] in e.verts)
    # Reverse the adjacent face's edge direction; cap winding must be consistent.
    lf = next(l for l in edge.link_faces[0].loops if l.edge==edge)
    if lf.vert == ordered[0]: ordered.reverse()
    loops.append({'center':list(center),'points':[v.co.copy() for v in ordered]})
assert len(loops)==2
bm = bmesh.new(); bm.from_mesh(mesh); bm.verts.ensure_lookup_table(); uv = bm.loops.layers.uv.active
oldfaces = set(bm.faces)
for hole in loops:
    verts = [min(bm.verts,key=lambda v:(v.co-p).length_squared) for p in hole['points']]
    assert all((v.co-p).length<1e-6 for v,p in zip(verts,hole['points']))
    # A center fan avoids connecting opposite atlas/shell vertices across existing diagonals.
    center=bm.verts.new(sum((v.co for v in verts),Vector())/len(verts))
    deform=bm.verts.layers.deform.active
    averages={}
    for v in verts:
        for group,weight in v[deform].items(): averages[group]=averages.get(group,0)+weight/len(verts)
    total=sum(averages.values())
    for group,weight in averages.items(): center[deform][group]=weight/total
    for i,v in enumerate(verts):
        face=bm.faces.new([v,verts[(i+1)%len(verts)],center]);face.smooth=True;face.material_index=1
        for l in face.loops:l[uv].uv=(l.vert.co.x*10,l.vert.co.z*10)
assert len(bm.faces)-len(faces)==9
assert all(f.calc_area()>1e-10 for f in bm.faces if f not in oldfaces)
bm.to_mesh(mesh); bm.free(); mesh.update()
assert positions == [tuple(v.co) for v in mesh.vertices[:len(positions)]]
assert faces == [tuple(f.vertices) for f in mesh.polygons[:len(faces)]]
assert uvs == [tuple(x.uv) for x in mesh.uv_layers.active.data[:len(uvs)]]
assert weights == [[(g.group,g.weight) for g in v.groups] for v in mesh.vertices[:len(weights)]]
# Verify closure, not just an opaque picture: exactly the nine target boundary edges disappear.
verify=bmesh.new(); verify.from_mesh(mesh); bmesh.ops.remove_doubles(verify,verts=list(verify.verts),dist=1e-6)
nonmanifold_after=sum(not e.is_manifold for e in verify.edges)
assert nonmanifold_after==nonmanifold_before-9,(nonmanifold_before,nonmanifold_after)
verify.free(); helper.free()
newnormals=list(normals)
for loop in mesh.loops[len(normals):]:
    co=mesh.vertices[loop.vertex_index].co
    choices=[Vector(normals[l.index]) for l in mesh.loops[:len(normals)] if (mesh.vertices[l.vertex_index].co-co).length<1e-6]
    if not choices:
        nearby=sorted(mesh.loops[:len(normals)],key=lambda l:(mesh.vertices[l.vertex_index].co-co).length_squared)[:12]
        choices=[Vector(normals[l.index])for l in nearby]
    newnormals.append(tuple((sum(choices,Vector())/len(choices)).normalized()))
mesh.normals_split_custom_set(newnormals)
shader=next(n for n in body.data.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
base=shader.inputs['Base Color'].links[0].from_node.image
width,height=base.size; pixels=list(base.pixels)
def color(uv):
    x=max(0,min(width-1,int(uv.x*width))); y=max(0,min(height-1,int(uv.y*height)))
    raw=pixels[(y*width+x)*4:(y*width+x)*4+3]
    return Vector(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in raw)
centroid_uv={}
for face in mesh.polygons[:len(faces)]:
    centeruv=sum((mesh.uv_layers.active.data[li].uv for li in face.loop_indices),Vector((0,0)))/len(face.loop_indices)
    for li in face.loop_indices:centroid_uv[li]=mesh.uv_layers.active.data[li].uv*.25+centeruv*.75
layer=mesh.color_attributes.new(name='SurfaceRepairColor',type='FLOAT_COLOR',domain='CORNER')
for c in layer.data: c.color=(1,1,1,.65)
mat=bpy.data.materials.new('Schiggy_LocalSurfaceCaps'); mat.use_nodes=True
shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
node=mat.node_tree.nodes.new('ShaderNodeVertexColor'); node.layer_name='SurfaceRepairColor'
mat.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
mat.node_tree.links.new(node.outputs['Alpha'],shader.inputs['Roughness'])
body.data.materials.append(mat)
for face in mesh.polygons[len(faces):]:
    face.material_index=1
    for li in face.loop_indices:
        co=mesh.vertices[mesh.loops[li].vertex_index].co
        choices=[color(centroid_uv[l.index]) for l in mesh.loops[:len(uvs)] if (mesh.vertices[l.vertex_index].co-co).length<1e-6]
        if not choices:
            nearby=sorted(mesh.loops[:len(uvs)],key=lambda l:(mesh.vertices[l.vertex_index].co-co).length_squared)[:12]
            choices=[color(centroid_uv[l.index])for l in nearby]
        rgb=sum(choices,Vector())/len(choices); layer.data[li].color=(*rgb,.65)
rig.animation_data.action=bpy.data.actions['Schiggy_Idle']; bpy.context.scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active=rig
fbx.parent.mkdir(exist_ok=True)
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'ARMATURE','MESH'},global_scale=1,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE',colors_type='LINEAR',path_mode='AUTO')
bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=str(out)); bpy.ops.wm.open_mainfile(filepath=str(out))
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
result={'original':str(source.relative_to(R)),'original_sha256':sha,'source':str(out.relative_to(R)),'export':str(fbx.relative_to(R)), 'patches':[{'center':h['center'],'boundary_edges':len(h['points'])}for h in loops], 'original_vertices_faces_uv_weights_preserved':True,'triangles_before':len(faces),'triangles_after':21282,'added_vertices':2,'nonmanifold_before':nonmanifold_before,'nonmanifold_after':nonmanifold_after,'cap_material_only_new_faces':True,'cap_triangle_count':9,'reopened':True}
(A/'SurfaceV2_Audit.json').write_text(json.dumps(result,indent=2))
print('SCHIGGY_LOCAL_CAPS_PASS',result,flush=True)
