"""Reopen the saved source, audit UV/tangent basis, and render actual geometry.
Review-only camera, light, backdrop live in an unsaved temporary scene.
"""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV3'
assert Path(bpy.data.filepath).name=='WestlandAssetLibrary_V3.blend'
data=json.loads((A/'ArtQualityV3.json').read_text());rows=[]
for a in data['assets']:
 o=bpy.data.objects[a['object']];m=o.data;m.calc_loop_triangles();m.calc_tangents(uvmap='UV0');uv=m.uv_layers.active.data
 bad_uv=0
 for t in m.loop_triangles:
  x,y,z=[uv[i].uv for i in t.loops];bad_uv+=abs((y.x-x.x)*(z.y-x.y)-(y.y-x.y)*(z.x-x.x))<1e-10
 bad_n=sum(n.vector.length<.99 for n in m.corner_normals);bad_t=sum(l.tangent.length<.99 or l.bitangent.length<.99 for l in m.loops);bad_a=sum(t.area<1e-9 for t in m.loop_triangles)
 assert bad_uv==bad_n==bad_t==bad_a==0,(a['object'],bad_uv,bad_n,bad_t,bad_a)
 assert tuple(o.scale)==(1,1,1) and min(v.co.z for v in m.vertices)>=-1e-5 and len(m.materials)==2
 hulls=[]
 for name in a['collision_objects']:
  hull=bpy.data.objects[name];z=[(hull.matrix_world@v.co).z for v in hull.data.vertices];assert min(z)>=-1e-5 and max(z)>4;hulls.append({'object':name,'dimensions_m':list(hull.dimensions),'ground_z_m':min(z),'top_z_m':max(z)})
 rows.append({'object':a['object'],'triangles':len(m.loop_triangles),'bad_uvs':bad_uv,'bad_normals':bad_n,'bad_tangents_binormals':bad_t,'degenerate_triangles':bad_a,'dimensions_m':list(o.dimensions),'collision_hulls':hulls})
(O/'SourceReopenAudit.json').write_text(json.dumps({'source':bpy.data.filepath,'reopened':True,'resaved':False,'meshes':rows},indent=2))
if '--audit-only' in sys.argv:print('V3_REOPEN_AUDIT_PASS');raise SystemExit
s=bpy.data.scenes.new('Temporary_V3_Review');bpy.context.window.scene=s;s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX'
s.world=bpy.data.worlds.new('Temporary_ReviewWorld');s.world.use_nodes=True;bg=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs[0].default_value=(.48,.57,.69,1);bg.inputs[1].default_value=.7
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
bpy.ops.object.light_add(type='SUN');sun=bpy.context.object;sun.rotation_euler=(.4,-.35,-.5);sun.data.energy=2.0;sun.data.angle=.3
bpy.ops.mesh.primitive_plane_add(size=70,location=(0,0,-.025));ma=bpy.data.materials.new('Temporary_Ground');ma.diffuse_color=(.16,.23,.10,1);bpy.context.object.data.materials.append(ma)
for a in data['assets']:
 orig=bpy.data.objects[a['object']];o=bpy.data.objects.new('Temporary_asset',orig.data);s.collection.objects.link(o)
 target=Vector((0,0,a['dimensions_m'][2]*.45));cam.data.ortho_scale=max(a['dimensions_m'])*1.3+.15;cam.location=target+Vector((0,-math.cos(math.radians(55))*25,math.sin(math.radians(55))*25));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(O/('Blender_'+a['object']+'.png'));bpy.ops.render.render(write_still=True);bpy.data.objects.remove(o,do_unlink=True)
print('V3_SOURCE_REVIEW_RENDERED')
