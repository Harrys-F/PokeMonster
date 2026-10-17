import bpy,numpy as np,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');I=R/'Art/Characters/NPCs/IntegrationV1';rows=json.loads((I/'Characters.json').read_text());arg=sys.argv[sys.argv.index('--')+1:];cfg=next(x for x in rows if x['id']==arg[0]);C=R/'Art/Characters/NPCs'/cfg['id']
assert not C.exists(), 'Existing character folder must be reviewed, not overwritten'
for d in ['Source','Exports','Textures','Previews']:(C/d).mkdir(parents=True,exist_ok=True)
# This script is exclusively a separate factory-startup Blender process, never user's live scene.
assert bpy.app.background
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.name=cfg['id']+'_Source_V1';s.unit_settings.system=next(x.identifier for x in bpy.types.UnitSettings.bl_rna.properties['system'].enum_items if x.identifier=='METRIC');s.unit_settings.scale_length=1
path=R/'Art/Characters/NPCs/Incoming'/(cfg['input_stem']+'.glb');bpy.ops.import_scene.gltf(filepath=str(path));meshes=[o for o in s.objects if o.type=='MESH'];assert meshes
hp=bpy.data.collections.new('HIGH_POLY_REFERENCE');s.collection.children.link(hp)
# Bake importer transforms into new working data only. Original Incoming GLB stays untouched.
for k,o in enumerate(meshes):
 o.name=cfg['id']+'_HP_'+str(k);o.data.transform(o.matrix_world);o.matrix_world.identity()
 for c in list(o.users_collection):c.objects.unlink(o)
 hp.objects.link(o)
co=[]
for o in meshes:
 a=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',a);co.append(a.reshape(-1,3))
positions=np.concatenate(co);mn=positions.min(axis=0);mx=positions.max(axis=0);height=float(mx[2]-mn[2]);factor=cfg['review_height_m']/height;center=(mn+mx)/2
for o in meshes:
 o.location=(-float(center[0])*factor,-float(center[1])*factor,-float(mn[2])*factor);o.scale=(factor,)*3
 o['input_original']=str(path);o['source_geometry_unchanged']=True
# Validate edges from Blender's edge/loop relationship without welding UV seams.
audit=[]
for o in meshes:
 m=o.data;m.calc_loop_triangles();counts=np.zeros(len(m.edges),np.int32);ei=np.empty(len(m.loops),np.int32);m.loops.foreach_get('edge_index',ei);np.add.at(counts,ei,1)
 coords=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);vi=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',vi)
 area=np.empty(len(m.polygons),np.float32);m.polygons.foreach_get('area',area)
 # Connected indexed vertex components. A compiled numpy propagation union approach is avoided here: source seams are kept.
 audit.append({'object':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'polygons':len(m.polygons),'raw_boundary_edges':int((counts==1).sum()),'edges_more_than_two_faces':int((counts>2).sum()),'loose_edges':int((counts==0).sum()),'zero_area_polygons':int((area<1e-16).sum()),'nonfinite_coordinates':int((~np.isfinite(coords)).sum()),'uv_layers':[u.name for u in m.uv_layers],'geometry_hash':hashlib.sha256(coords.tobytes()+vi.tobytes()).hexdigest(),'component_audit':'Deferred exact connectivity/island audit; raw seam edges must not be treated as holes.','self_intersections':'Not exhaustively tested; visual review required'})
images=[]
for im in list(bpy.data.images):
 if im.source=='FILE' and im.users:
  im.name=cfg['id']+'_'+im.name
  if not im.packed_file:im.pack()
  # Preserve exact embedded texture bytes, no conversion or invented 4K label.
  if im.packed_file:
   ext='.png' if bytes(im.packed_file.data)[:8]==b'\x89PNG\r\n\x1a\n' else '.jpg'
   dest=C/'Textures'/(im.name.replace('/','_')+ext);dest.write_bytes(bytes(im.packed_file.data));im.filepath=str(dest)
   for pf in im.packed_files:pf.filepath=im.filepath
  images.append({'name':im.name,'size':list(im.size),'packed':bool(im.packed_file),'colorspace':im.colorspace_settings.name,'external_path':im.filepath})
for m in bpy.data.materials:
 if m.users:m.name=cfg['id']+'_'+m.name
review=bpy.data.collections.new('REVIEW');s.collection.children.link(review)
world=bpy.data.worlds.new(cfg['id']+'_Studio');world.use_nodes=True;next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.12,.14,.16,1);next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value=.45;s.world=world
h=cfg['review_height_m']
for name,loc,power,size in [('Key',(-2,-3,4),500,3),('Fill',(3,-2,2.3),280,3),('Rim',(0,3,3),440,2.5)]:
 data=bpy.data.lights.new(cfg['id']+'_'+name,'AREA');data.energy=power*(h/1.8)**2;data.shape='DISK';data.size=size*h/1.8;o=bpy.data.objects.new(data.name,data);review.objects.link(o);o.location=Vector(loc)*h/1.8;o.rotation_euler=(Vector((0,0,h*.55))-o.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new(cfg['id']+'_ReviewCamera');cam=bpy.data.objects.new(data.name,data);review.objects.link(cam);s.camera=cam;data.type=next(x.identifier for x in bpy.types.Camera.bl_rna.properties['type'].enum_items if x.identifier=='ORTHO');data.ortho_scale=h*1.35
try:s.render.engine='CYCLES'
except TypeError as e:raise RuntimeError(str(e))
s.cycles.samples=8;s.cycles.use_denoising=True;s.cycles.device='CPU';s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=2;s.render.image_settings.file_format='PNG'
s.render.filepath=str(C/'Previews/01_Front.png');cam.location=(0,-h*3,h*.5);cam.rotation_euler=(Vector((0,0,h*.5))-cam.location).to_track_quat('-Z','Y').to_euler()
# Source is a protected independent inspection master, not claimed to be rigged or runtime-ready.
s['status']='Imported highpoly reference; rig/optimization not approved';s['original_height_m']=height;s['review_height_m']=h
f=C/'Source'/(cfg['id']+'_NPC_Source_V1.blend');assert not f.exists();bpy.ops.wm.save_as_mainfile(filepath=str(f))
report={'id':cfg['id'],'input':str(path),'source_blend':str(f),'original_height_m':height,'review_height_m':h,'uniform_object_scale':factor,'front_assumption':'Negative Blender Y, pending visual check','mesh_audit':audit,'textures':images,'rigs':len([o for o in s.objects if o.type=='ARMATURE']),'actions':len(bpy.data.actions),'rendered_views':[]}
(I/(cfg['id']+'_SourceAudit.json')).write_text(json.dumps(report,indent=2))
for name,loc in [('01_Front',(0,-3,.5)),('02_Right',(3,0,.5)),('03_ThreeQuarter',(2,-3,1.05))]:
 cam.data.type='ORTHO';cam.data.ortho_scale=max(h*1.16,float(mx[0]-mn[0])*factor*1.12);s.render.resolution_x=900;s.render.resolution_y=900;cam.location=Vector(loc)*h;cam.rotation_euler=(Vector((0,0,h*.5))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(C/'Previews'/(name+'.png'));bpy.ops.render.render(write_still=True);report['rendered_views'].append(s.render.filepath);(I/(cfg['id']+'_SourceAudit.json')).write_text(json.dumps(report,indent=2));print('VIEW_DONE',cfg['id'],name,flush=True)
print('SOURCE_DONE',cfg['id'],flush=True)
