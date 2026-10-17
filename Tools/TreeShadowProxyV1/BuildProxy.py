"""Background Blender only. Source scene is read; only new experiment outputs saved."""
import bpy,math,json,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/'Art/World/TreeShadowProxyV1';A.mkdir(parents=True,exist_ok=True)
for d in ['Source','Exports','Review']:(A/d).mkdir(exist_ok=True)
target=A/'Source/OakAncient_ShadowProxy_V1.blend';assert not target.exists()
assert bpy.app.background
source=bpy.data.objects['SM_WLA_OakAncient_V3'];assert source.type=='MESH'
scene=bpy.data.scenes.new('TreeShadowProxyV1');bpy.context.window.scene=scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
col=bpy.data.collections.new('SHADOW_ONLY_OPAQUE');scene.collection.children.link(col)
# Keep the source bark exactly, including its grounded roots and branch silhouettes.
mesh=source.data.copy();obj=bpy.data.objects.new('SM_TSP_OakAncient_Bark',mesh);col.objects.link(obj)
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index!=0],context='FACES');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001);bm.to_mesh(mesh);bm.free()
mat=bpy.data.materials.new('M_TSP_OpaqueShadow');mat.diffuse_color=(.2,.23,.16,1);mesh.materials.clear();mesh.materials.append(mat)
for f in mesh.polygons:f.material_index=0
# Solid irregular crown volume with three large through-openings. No transparency.
curve=bpy.data.curves.new('IrregularCrown_ThreeLargeGaps','CURVE');curve.dimensions='2D';curve.resolution_u=1;curve.fill_mode='BOTH';curve.extrude=.70;curve.bevel_depth=0
def loop(points):
 s=curve.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,0,1)
 s.use_cyclic_u=True
outer=[]
for i in range(56):
 a=i/56*math.tau;r=1+.105*math.sin(3*a+.4)+.055*math.sin(7*a-.7)+.025*math.sin(11*a)
 outer.append((-.25+5.45*math.cos(a)*r,-.2+4.25*math.sin(a)*r))
loop(outer)
for cx,cy,rx,ry,phase in [(-1.1,.0,.78,.93,.2),(2.4,-.65,.83,.64,.7),(-2.35,1.85,.62,.60,1.1)]:
 points=[]
 for i in reversed(range(12)):
  a=i/12*math.tau;r=1+.1*math.sin(3*a+phase);points.append((cx+rx*r*math.cos(a),cy+ry*r*math.sin(a)))
 loop(points)
crown=bpy.data.objects.new('SM_TSP_OakAncient_Crown',curve);col.objects.link(crown);bpy.context.view_layer.objects.active=crown;crown.select_set(True);bpy.ops.object.convert(target='MESH');crown=bpy.context.object
for v in crown.data.vertices:
 x,y,z=v.co;rad=min(1,((x+.25)/6)**2+((y+.2)/4.8)**2);v.co.z=5.4+(z+9.0+.75*(1-rad)-9.5)*.12
crown.data.materials.append(mat)
objects=[obj,crown];audit=[]
for o in objects:
 for x in bpy.context.selected_objects:x.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 # Valid uncollapsed UVs for importer tangents, opaque shadow shader does not sample them.
 if not o.data.uv_layers:o.data.uv_layers.new(name='UV0')
 uv=o.data.uv_layers.active;uv.name="UV0"
 for p in o.data.polygons:
  for li in p.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v.x*.08+.5,v.y*.08+.5+v.z*.03)
 o.data.calc_loop_triangles();o.data.calc_tangents(uvmap='UV0')
 bm=bmesh.new();bm.from_mesh(o.data);non=sum(not e.is_manifold for e in bm.edges);bm.free()
 audit.append({'object':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'non_manifold_edges':non,'dimensions_m':list(o.dimensions)})
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',use_mesh_modifiers=True,mesh_smooth_type='FACE',use_tspace=True,bake_anim=False,add_leaf_bones=False)
# Pack no old images: new scene only needs the one opaque shader.
for s in list(bpy.data.scenes):
 if s!=scene:bpy.data.scenes.remove(s)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(target))
(A/'Review/Geometry.json').write_text(json.dumps({'source':'Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V3.blend','crown_gaps':3,'opaque':True,'objects':audit},indent=2));print('PROXY_SAVED',audit)
