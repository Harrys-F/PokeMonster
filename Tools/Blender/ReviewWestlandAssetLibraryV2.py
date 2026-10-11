"""Read-only reopen/audit plus per-asset art renders; never saves the source."""
import bpy,json,math,bmesh,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV2';assert Path(bpy.data.filepath).name=='WestlandAssetLibrary_V2.blend'
data=json.loads((A/'Assets.json').read_text());assets=[a for a in data['assets'] if a.get('art_status')=='V2_review_pending'];assert len(assets)==20
rows=[]
for a in assets:
 o=bpy.data.objects[a['object']];m=o.data;m.calc_tangents(uvmap='UV0');m.calc_loop_triangles();uv=m.uv_layers.active.data
 baduv=0
 for t in m.loop_triangles:
  x,y,z=[uv[i].uv for i in t.loops];det=abs((y.x-x.x)*(z.y-x.y)-(y.y-x.y)*(z.x-x.x));baduv+=det<1e-10
 badn=sum(x.vector.length<.99 for x in m.corner_normals);badt=sum(l.tangent.length<.99 or l.bitangent.length<.99 for l in m.loops);badarea=sum(t.area<1e-9 for t in m.loop_triangles)
 assert badn==badt==badarea==baduv==0,(a['id'],badn,badt,badarea,baduv)
 assert all(m.materials) and min(v.co.z for v in m.vertices)>=-1e-5 and tuple(o.scale)==(1,1,1)
 if 'Runestone' in a['id']:
  bm=bmesh.new();bm.from_mesh(m);assert all(not e.is_boundary for e in bm.edges) and bm.calc_volume(signed=True)>0;bm.free()
 rows.append({'id':a['id'],'triangles':len(m.loop_triangles),'bad_uvs':baduv,'bad_normals':badn,'bad_tangent_or_binormal':badt,'degenerate_triangles':badarea})
(O/'SourceReopenAudit.json').write_text(json.dumps({'source':bpy.data.filepath,'reopened':True,'source_not_resaved':True,'meshes':rows},indent=2))
if '--audit-only' in sys.argv:print('REOPEN_AUDIT_PASS',len(rows));raise SystemExit
s=bpy.data.scenes.new('Temporary_ArtReview');bpy.context.window.scene=s;s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('Temporary_ReviewWorld');s.world.use_nodes=True;next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.42,.52,.62,1);next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value=.50
s.view_settings.view_transform='AgX'
bpy.ops.object.camera_add();camera=bpy.context.object;s.camera=camera;camera.data.type='ORTHO'
bpy.ops.object.light_add(type='SUN');sun=bpy.context.object;sun.rotation_euler=(.4,-.4,-.5);sun.data.energy=2;sun.data.angle=.25
bpy.ops.mesh.primitive_plane_add(size=80,location=(0,0,-.02));floor=bpy.context.object;ma=bpy.data.materials.new('Temporary_Ground');ma.diffuse_color=(.21,.26,.15,1);floor.data.materials.append(ma)
for a in assets:
 if '--runes' in sys.argv and a['id'].split('_')[1]!='Runestone':continue
 if '--trees' in sys.argv and a['id'].split('_')[1] not in ('OakAncient','OakYoung','Birch','FruitTree'):continue
 if '--surfaces' in sys.argv and a['id'].split('_')[1] not in ('Stump','Root','Runestone','Column'):continue
 orig=bpy.data.objects[a['object']];o=bpy.data.objects.new('Temporary_asset',orig.data);s.collection.objects.link(o)
 size=a['dimensions_m'];target=Vector((0,0,size[2]*.46));camera.data.ortho_scale=max(size)*1.38+.12;camera.location=target+Vector((8,-12,16));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/('Blender_'+a['id']+'.png'));bpy.ops.render.render(write_still=True);bpy.data.objects.remove(o,do_unlink=True)
print('RENDERED_AUDITED_20')
