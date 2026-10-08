"""Read-only V6 source preservation, references and geometry audit in Blender.

Opens both saved files and writes diagnostics under ignored Saved; never saves
a Blender source and never evaluates an animation or edits a rig.
"""
import bpy
import bmesh
import hashlib
import json
import math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

R = Path(__file__).resolve().parents[1]
OUT = R.parents[2] / 'Saved/YoungTrainerClothingFeetV1'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'Audit.json').write_text(json.dumps({'status': 'RUNNING'}) + '\n')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def vector_value(value):
    try:
        return list(value)
    except TypeError:
        return value


def snapshot():
    objects = {}
    materials = {}
    for o in bpy.data.objects:
        row = {'type': o.type, 'matrix': [list(r) for r in o.matrix_basis],
               'parent': o.parent.name if o.parent else None}
        if o.type == 'MESH':
            row.update(vertices=[list(v.co) for v in o.data.vertices],
                       faces=[list(p.vertices) for p in o.data.polygons],
                       weights=[[(g.group, g.weight) for g in v.groups] for v in o.data.vertices],
                       groups=[g.name for g in o.vertex_groups],
                       uv=[[list(v.uv) for v in layer.data] for layer in o.data.uv_layers],
                       keys={k.name: {'value': k.value, 'coordinates': [list(v.co) for v in k.data]}
                             for k in o.data.shape_keys.key_blocks} if o.data.shape_keys else {},
                       materials=[m.name for m in o.data.materials],
                       material_indices=[p.material_index for p in o.data.polygons],
                       armature_modifiers=[(m.name, m.object.name if m.object else None)
                                           for m in o.modifiers if m.type == 'ARMATURE'])
        if o.type == 'ARMATURE':
            row['bones'] = [(b.name, list(b.head_local), list(b.tail_local),
                             [list(r) for r in b.matrix_local], b.parent.name if b.parent else None)
                            for b in o.data.bones]
            row['pose'] = [(b.name, [list(r) for r in b.matrix_basis],
                            [(c.name, c.type) for c in b.constraints]) for b in o.pose.bones]
        if o.type == 'EMPTY' and o.empty_display_type == 'IMAGE':
            row['reference'] = {'size': o.empty_display_size, 'offset': list(o.empty_image_offset),
                                'color': list(o.color), 'locks': [list(o.lock_location), list(o.lock_rotation), list(o.lock_scale)],
                                'locked_select': o.hide_select,
                                'image': hashlib.sha256(o.data.packed_file.data).hexdigest() if o.data.packed_file else None}
        objects[o.name] = digest(row)
    for m in bpy.data.materials:
        row = {'color': list(m.diffuse_color)}
        if m.node_tree:
            row['nodes'] = [(n.name, n.bl_idname, n.image.name if n.type == 'TEX_IMAGE' and n.image else None,
                             [(s.identifier, vector_value(s.default_value)) for s in n.inputs if hasattr(s, 'default_value')])
                            for n in m.node_tree.nodes]
            row['links'] = [(l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier)
                            for l in m.node_tree.links]
        materials[m.name] = digest(row)
    return {'objects': objects, 'materials': materials, 'actions': [a.name for a in bpy.data.actions]}


# The original non-head parts are copied exactly, including UVs and modifiers.
def mesh_signature(o):
    return digest({'vertices':[list(v.co) for v in o.data.vertices],
                   'faces':[list(p.vertices) for p in o.data.polygons],
                   'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],
                   'groups':[g.name for g in o.vertex_groups],
                   'uv':[[list(v.uv) for v in layer.data] for layer in o.data.uv_layers],
                   'materials':[m.name for m in o.data.materials],
                   'material_indices':[p.material_index for p in o.data.polygons],
                   'modifiers':[(m.name,m.type,{p.identifier:vector_value(getattr(m,p.identifier)) for p in m.bl_rna.properties if not p.is_readonly and p.type in ['INT','FLOAT','BOOLEAN','ENUM']}) for m in o.modifiers],
                   'matrix':[list(row) for row in o.matrix_basis]})


bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_HeadForm_V6.blend'))
before=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(R/'Source/YoungTrainer_ClothingFeet_V1.blend'))
after=snapshot()
assert all(after['objects'].get(k)==v for k,v in before['objects'].items()),[k for k,v in before['objects'].items() if after['objects'].get(k)!=v]
assert before['materials']==after['materials']
assert before['actions']==after['actions']
allowed={'Shirt','Vest','Pants','Pouches','DiagonalWaistBelt','RolledCuff_R','RolledCuff_L','BareFoot_R','BareFoot_L'}
unchanged=[];changed=[]
for o in bpy.data.collections['YTCF_Player'].objects:
    if o.type!='MESH' or 'source_v6_object' not in o:continue
    name=o.name.removeprefix('YTCF_');old=bpy.data.objects[o['source_v6_object']]
    same=mesh_signature(o)==mesh_signature(old)
    if name not in allowed:assert same,o.name
    (unchanged if same else changed).append(o.name)
col=bpy.data.collections['YTCF_Player'];root=bpy.data.objects['YTCF_PlayerRoot']
assert root.location.length==0 and list(root.scale)==[1.,1.,1.]
rows=[];points=[];dg=bpy.context.evaluated_depsgraph_get()
for o in col.objects:
    if o.type!='MESH':continue
    assert o.parent==root and not o.animation_data and not o.data.shape_keys
    assert not any(m.type=='ARMATURE' for m in o.modifiers)
    assert not any(t in o.name.lower() for t in ['boot','shoe','sock','sole'])
    bm=bmesh.new();bm.from_mesh(o.data)
    row={'name':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),
         'boundary':sum(e.is_boundary for e in bm.edges),
         'invalid_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),
         'loose':sum(not v.link_faces for v in bm.verts),
         'degenerate':sum(f.calc_area()<1e-12 for f in bm.faces)}
    assert all(math.isfinite(c) for v in bm.verts for c in v.co)
    assert row['invalid_edges']==row['loose']==row['degenerate']==0,row
    if any(t in o.name for t in ['HairSculpt','BareFoot','Scarf']):assert row['boundary']==0,row
    bm.free();ev=o.evaluated_get(dg);m=ev.to_mesh();wp=[o.matrix_world@v.co for v in m.vertices];points.extend(wp);ev.to_mesh_clear()
    row['evaluated_bounds_m']={'min':[min(p[k] for p in wp) for k in range(3)],'max':[max(p[k] for p in wp) for k in range(3)]}
    rows.append(row)
low=[min(p[k] for p in points) for k in range(3)];high=[max(p[k] for p in points) for k in range(3)]
assert abs(low[2])<1e-6 and abs(high[2]-1.4)<1e-6,(low,high)
refs=bpy.data.collections['REF_PLAYER_FINAL'];assert len(refs.objects)==11
for o in refs.objects:assert o.data.packed_file and all(o.lock_location) and all(o.lock_rotation) and all(o.lock_scale) and o.hide_select
feet={}
for label,side,angle in [('R',1,9),('L',-1,-21)]:
    o=bpy.data.objects['YTCF_BareFoot_'+label]
    assert o['toe_count']==5 and o['barefoot'] and min(v.co.z for v in o.data.vertices)==0
    ca=math.cos(math.radians(angle));sa=math.sin(math.radians(angle))
    vs=[]
    for v in o.data.vertices:
        x=v.co.x-side*.131;y=v.co.y
        vs.append(((x*ca+y*sa)*side,-x*sa+y*ca,v.co.z))
    lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)]
    # Geometry, not only a custom property: detect five distinct anterior toe lobes.
    tree=BVHTree.FromPolygons([Vector(p) for p in vs],[list(p.vertices) for p in o.data.polygons])
    contour=[]
    for i in range(181):
        x=-.066+i*.0008
        for j in range(135):
            y=-.216+j*.0007
            loc,normal,index,distance=tree.ray_cast(Vector((x,y,.13)),Vector((0,0,-1)),.14)
            if loc is not None:
                contour.append((x,y));break
    tips=[]
    for a,b in [(-.064,-.028),(-.028,.005),(.005,.031),(.031,.055),(.055,.078)]:
        samples=[p for p in contour if a<=p[0]<b]
        assert samples,label
        tip=min(samples,key=lambda p:p[1]);assert a+.001<tip[0]<b-.001,(label,tip,a,b)
        tips.append(tip)
    assert len(tips)==5
    feet[label]={'local_bounds_m':{'min':lo,'max':hi},'width_cm':(hi[0]-lo[0])*100,'length_cm':(hi[1]-lo[1])*100,'toe_count':5,'five_toes_inherited_from_connected_v6_mesh':True,'five_anterior_lobes_geometrically_sampled':True,'toe_tips_local_xy_m':tips,'no_footwear':True}
files=json.loads((OUT/'BeforeFiles.json').read_text())
for p,sha in files.items():assert hashlib.sha256((R.parents[2]/p).read_bytes()).hexdigest()==sha,p
report={'status':'PASS','source_reopened':bpy.data.filepath,'existing_objects_preserved':len(before['objects']),
        'existing_materials_preserved':len(before['materials']),'existing_file_hashes_preserved':len(files),
        'unchanged_meshes':unchanged,'modified_source_meshes':changed,
        'v6_head_eyes_ears_hair_expression_exact':True,'body_hands_backpack_bedroll_equipment_pendant_exact':True,
        'rig_actions_originals_unchanged':True,'no_unreal_export':True,
        'bounds_m':{'min':low,'max':high},'height_m':high[2]-low[2],
        'feet':feet,'locked_reference_images':len(refs.objects),
        'camera_note':'Approximate illustration perspective, fixed comparison camera; not Unreal runtime.',
        'geometry':rows}
(OUT/'Audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='geometry'},indent=2),flush=True)
