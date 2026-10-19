"""Only repair the diagnosed moved image path; retain geometry, UVs and materials."""
import bpy,json,hashlib,array,subprocess
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');O=R/'Saved/ProjectMigration'
targets=['Art/World/TreeShadowProxyV1/Source/OakAncient_ShadowProxy_V1.blend','Art/World/WestlandAssetLibrary/Source/WestlandAssetLibrary_V3.blend']
texture=R/'Art/World/WestlandAssetLibrary/Textures/T_WLA_FoliageGroups_V3.png'
old='/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/World/WestlandAssetLibrary/Textures/T_WLA_FoliageGroups_V3.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected=subprocess.check_output(['git','show','HEAD:'+str(texture.relative_to(R))],cwd=R)
if expected.startswith(b'version https://git-lfs.github.com/spec/v1'):
 assert 'oid sha256:'+sha(texture) in expected.decode()
else:assert expected==texture.read_bytes()
def values(data,prop,width,typecode='f'):
 a=array.array(typecode,[0])*(len(data)*width);data.foreach_get(prop,a);return hashlib.sha256(a.tobytes()).hexdigest()
def state():
 meshes={}
 for m in bpy.data.meshes:
  attrs={}
  for a in m.attributes:
   spec={'INT32_2D':('value',2,'i'),'FLOAT':('value',1,'f'),'INT':('value',1,'i'),'BOOLEAN':('value',1,'b'),'FLOAT_VECTOR':('vector',3,'f'),'FLOAT2':('vector',2,'f'),'FLOAT_COLOR':('color',4,'f'),'BYTE_COLOR':('color',4,'f')}.get(a.data_type)
   if spec:attrs[a.name]=(a.domain,a.data_type,values(a.data,*spec))
   else:raise RuntimeError('Unverified attribute type '+a.data_type)
  meshes[m.name]={'vertices':values(m.vertices,'co',3),'edges':values(m.edges,'vertices',2,'i'),'loop_vertices':values(m.loops,'vertex_index',1,'i'),'polygon_sizes':values(m.polygons,'loop_total',1,'i'),'polygon_materials':values(m.polygons,'material_index',1,'i'),'attributes':attrs,'materials':[x.name if x else None for x in m.materials]}
 materials={}
 for m in bpy.data.materials:
  nodes=[]
  if m.use_nodes:
   for n in m.node_tree.nodes:
    inputs=[]
    for s in n.inputs:
     if hasattr(s,'default_value'):
      v=s.default_value
      if not isinstance(v,(str,float,int,bool)):
       try:v=list(v)
       except TypeError:v=str(v)
      inputs.append((s.identifier,v))
    nodes.append((n.name,n.bl_idname,inputs,n.image.name if n.bl_idname=='ShaderNodeTexImage' and n.image else None))
   links=sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links)
  else:links=[]
  materials[m.name]={'nodes':nodes,'links':links,'diffuse_color':list(m.diffuse_color)}
 return json.dumps({'meshes':meshes,'materials':materials,'objects':{o.name:{'type':o.type,'matrix':[list(row) for row in o.matrix_world],'data':o.data.name if o.data else None,'modifiers':[(x.name,x.type) for x in o.modifiers]} for o in bpy.data.objects}},sort_keys=True)
results=[]
bpy.context.preferences.filepaths.save_version=0
for rel in targets:
 p=R/rel;before_sha=sha(p);assert bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)=={'FINISHED'}
 bpy.context.view_layer.update();before=state();retained=[]
 for category in ['meshes','materials']:
  for block in getattr(bpy.data,category):
   if block.users==0 and not block.use_fake_user:block.use_fake_user=True;retained.append({'category':category,'name':block.name})
 images=[i for i in bpy.data.images if i.filepath==old];assert len(images)==1
 i=images[0];assert not i.packed_file
 i.filepath=bpy.path.relpath(str(texture),start=str(p.parent));i.reload();bpy.context.view_layer.update();newpath=i.filepath
 assert state()==before,'Content changed before save'
 bpy.context.preferences.filepaths.save_version=0
 assert bpy.ops.wm.save_as_mainfile(filepath=str(p),check_existing=False,compress=True,relative_remap=False)=={'FINISHED'}
 assert bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)=={'FINISHED'}
 bpy.context.view_layer.update();after=state()
 (O/(p.stem+'_BeforeFingerprint.json')).write_text(before)
 (O/(p.stem+'_AfterFingerprint.json')).write_text(after)
 if after!=before:
  pointer=subprocess.check_output(['git','show','HEAD:'+rel],cwd=R,text=True);oid=next(x.split(':',1)[1] for x in pointer.splitlines() if x.startswith('oid sha256:'));original=R/'.git/lfs/objects'/oid[:2]/oid[2:4]/oid
  assert sha(original)==oid;p.write_bytes(original.read_bytes());assert sha(p)==before_sha
  raise RuntimeError('Fingerprint differs; original source automatically restored; inspect fingerprint JSONs')
 fixed=bpy.data.images.get(i.name) if False else next(x for x in bpy.data.images if x.filepath==newpath)
 assert Path(bpy.path.abspath(fixed.filepath)).resolve()==texture and not fixed.packed_file
 results.append({'file':rel,'before_sha256':before_sha,'after_sha256':sha(p),'old_path':old,'new_relative_path':newpath,'texture_sha256':sha(texture),'geometry_uv_materials_objects_fingerprint':hashlib.sha256(before.encode()).hexdigest(),'content_fingerprint_unchanged':True,'reopened':True,'additional_backup_created':False,'previously_unused_datablocks_retained':retained})
 (O/'BlenderPathRepairs.json').write_text(json.dumps(results,indent=2));print('REPAIRED_TEXTURE_PATH_ONLY',rel,flush=True)
