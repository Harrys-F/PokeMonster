exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];skin=body.data.materials[0]
# Orbital patches become actual connected skin, not separate glasses-like pieces.
for side in ['L','R']:
 o=bpy.data.objects['HNV2_OrbitalSkin_'+side]
 for m in list(o.modifiers):apply(o,m)
 body_union(o)
bm=bmesh.new();bm.from_mesh(body.data)
selected=[]
for v in bm.verts:
 x,y,z=v.co;d=((abs(x)-.043)/.033)**2+((z-1.184)/.025)**2
 if y<-.02 and .28<d<1.4:selected.append(v)
for _ in range(12):bmesh.ops.smooth_vert(bm,verts=selected,factor=.22,use_axis_x=True,use_axis_y=True,use_axis_z=True)
# Blend the palm/finger roots; retain the distinct phalange and fingertip rings.
hands=[v for v in bm.verts if .666<abs(v.co.x)<.721 and .904<v.co.z<.958]
for _ in range(7):bmesh.ops.smooth_vert(bm,verts=hands,factor=.18,use_axis_x=True,use_axis_y=True,use_axis_z=True)
for v in hands:
 x,y,z=v.co
 if z>.937:
  swell=max(math.exp(-((abs(x)-.707)/.013)**2-((y-yy)/.009)**2) for yy in [-.032,-.010,.014,.035])
  v.co.z+=.0015*swell
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(1,0,0),clear_inner=True);bm.to_mesh(body.data);bm.free();mi=body.modifiers.new('FinalBodySymmetry','MIRROR');mi.use_mirror_merge=True;mi.merge_threshold=1e-6;apply(body,mi)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));print('Final connected skin nonmanifold',sum(not e.is_manifold for e in bm.edges));bm.to_mesh(body.data);bm.free()
body.data.materials.clear();body.data.materials.append(skin)
for p in body.data.polygons:p.use_smooth=True;p.material_index=0
attribute=body.data.color_attributes.get('HNV2_SkinTint') or body.data.color_attributes.new(name='HNV2_SkinTint',type='FLOAT_COLOR',domain='POINT')
for v in body.data.vertices:
 x,y,z=v.co;pink=0.
 if y<0 and z>1.07:pink=max(math.exp(-((abs(x)-.065)/.030)**2-((z-1.157)/.022)**2),.7*math.exp(-(x/.020)**2-((z-1.156)/.016)**2))*.05
 attribute.data[v.index].color=(.47+pink,.245-pink*.12,.145-pink*.10,1)
# Fit nails to the actual curved skin rather than leaving pale elliptical stickers.
bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());nails=bpy.data.objects['HNV2_FingerAndToeNails'];inv=nails.matrix_world.inverted();fitted=0
for v in nails.data.vertices:
 p=nails.matrix_world@v.co;top=1.02 if p.z>.5 else .14;hit=bvh.ray_cast(Vector((p.x,p.y,top)),Vector((0,0,-1)),.25 if top>1 else .15)[0]
 if hit:
  p.z=hit.z+.00007+min(.00022,max(0,p.z-hit.z))*.30;v.co=inv@p;fitted+=1
mat=bpy.data.materials['HNV2_NaturalNails'];p=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(.43,.23,.14,1);p.inputs['Roughness'].default_value=.43
save_stage('08_OrbitalAndHands');bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V2.blend'),{scene});print(json.dumps({'fitted_nail_vertices':fitted,'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons)}))
