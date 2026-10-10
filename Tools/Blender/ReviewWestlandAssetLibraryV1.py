"""Read-only reopen, per-mesh geometry/UV/material audit and actual rendered review."""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/World/WestlandAssetLibrary';OUT=ROOT/'Saved/WestlandAssetLibrary';hero='HeroReview' in bpy.data.filepath;manifest=json.loads((ART/('Heroes.json' if hero else 'Assets.json')).read_text());s=bpy.context.scene
assert bpy.app.background and Path(bpy.data.filepath).exists()
for o in bpy.data.objects:
 if o.name.startswith('Review_'):o.hide_render=True
for c in s.collection.children:
 if c.name.startswith('WLA_'):c.hide_render=True;c.hide_viewport=False
s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=800;s.render.resolution_y=800;s.render.resolution_percentage=100
s.world.use_nodes=True;n=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');n.inputs['Color'].default_value=(.45,.55,.65,1);n.inputs['Strength'].default_value=.45
for o in bpy.data.objects:
 if o.type=='LIGHT':o.data.energy=2000;o.location=(4,-6,12);o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='SUN',location=(0,0,10));bpy.context.object.data.energy=1.2;bpy.context.object.data.angle=.25;bpy.context.object.rotation_euler=(.3,-.4,-.3)
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,-.015));floor=bpy.context.object;mat=bpy.data.materials.new('TemporaryReviewFloor');mat.use_nodes=True;bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.17,.22,.12,1);bs.inputs['Roughness'].default_value=1;floor.data.materials.append(mat)
cam=s.camera;audit=[]
chosen=[a['id'] for a in manifest['assets']] if hero else ['WLA_Birch_A','WLA_FruitTree_A','WLA_Bush_A','WLA_Cart_A','WLA_Barrel_A','WLA_Crate_A','WLA_Haybale_A','WLA_WallRemnant_A','WLA_Stump_A','WLA_Signpost_A','WLA_Woodpile_A','WLA_Column_A','WLA_Grass_A','WLA_Herb_A','WLA_Wildflowers_A','WLA_Root_A','WLA_Fence_A','WLA_SmallStones_A']
for a in manifest['assets']:
 o=bpy.data.objects[a['object']];assert o.type=='MESH' and all(o.data.materials) and o.data.uv_layers and all(abs(v-1)<1e-5 for v in o.scale)
 assert not o.library and not o.data.library
 bm=bmesh.new();bm.from_mesh(o.data);boundary=sum(e.is_boundary for e in bm.edges);loose=sum(not v.link_faces for v in bm.verts);deg=sum(f.calc_area()<1e-9 for f in bm.faces);bm.free();assert loose==0 and deg==0,(a['id'],loose,deg)
 assert min(v.co.z for v in o.data.vertices)>=-.00001
 audit.append({'id':a['id'],'triangles':a['triangles'],'boundary_edges':boundary,'loose_vertices':loose,'degenerate_faces':deg,'material_slots':len(o.data.materials),'uv_layers':len(o.data.uv_layers),'collision_bodies':len(a['collision_objects']),'reopened':True})
 if '--plants' in sys.argv and a['id'] not in ['WLA_Herb_B','WLA_Wildflowers_A']:continue
 if '--plants' in sys.argv:chosen.append(a['id'])
 if '--audit-only' in sys.argv or (a['id'] not in ['WLA_Bush_A','WLA_Birch_A'] if '--refined' in sys.argv else a['id'] not in chosen):continue
 c=bpy.data.collections[a['id']];
 if c.name not in s.collection.children:s.collection.children.link(c)
 c.hide_viewport=False;c.hide_render=False
 for name in a['collision_objects']:bpy.data.objects[name].hide_render=True
 size=a['dimensions_m'];target=Vector((0,0,size[2]*.42));cam.data.type='ORTHO';cam.data.ortho_scale=max(size)*1.34+.12;cam.location=target+Vector((8,-12,17));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(OUT/('Blender_'+a['id']+'.png'));bpy.ops.render.render(write_still=True);c.hide_render=True
for im in bpy.data.images:
 if im.source=='FILE':assert Path(bpy.path.abspath(im.filepath)).exists(),im.filepath
(OUT/('HeroSourceAudit.json' if hero else 'SourceAudit.json')).write_text(json.dumps({'source':bpy.data.filepath,'reopened':True,'source_not_resaved':True,'meshes':audit,'external_textures_valid':True},indent=2)+'\n');print('WLA_REOPEN_AUDIT_PASSED',len(audit))
