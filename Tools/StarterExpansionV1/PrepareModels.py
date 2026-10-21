"""Fit independent biped/quadruped rigs to the actual Meshy surfaces. No remeshing."""
import bpy,json,hashlib,struct,math,sys
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2]
SPECS=[('Schiggy','Shiggy.glb',.5,'8353b766fc36d90d3c7a8905e82ae9c407a974959dcab6cac629c5127446a127'),('Bisasam','Bisasam.glb',.7,'01ee8bc064635aeaaed2b356e1c87e0a9d0ab819fa6285d86cfbe0460466306d')]
def smooth(a,b,x):t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
def blend(a,b,t):return {k:a.get(k,0)*(1-t)+b.get(k,0)*t for k in a.keys()|b.keys()}
def chainweight(p,chain):
 ds=[]
 for name,a,b in chain:
  a,b=Vector(a),Vector(b);u=max(0.,min(1.,(p-a).dot(b-a)/(b-a).length_squared));ds.append(((p-a-u*(b-a)).length,name))
 ds.sort();closest=ds[:2];w={n:1/max(d,.012)**3 for d,n in closest};total=sum(w.values());return {n:v/total for n,v in w.items()}
for name,file,height,digest in SPECS:
 A=R/'Art/Characters/Creatures'/name;out=A/'Source'/(name+'_Meshy_V1.blend');assert not out.exists();source=R/'Art/Characters/Creatures/Incoming'/file;raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==digest
 for folder in ['Source','Textures/MeshyV1','Exports/MeshyV1']: (A/folder).mkdir(parents=True,exist_ok=True)
 length,kind=struct.unpack_from('<II',raw,12);doc=json.loads(raw[20:20+length]);start=20+length+8
 for i,tex in enumerate(['BaseColor','MetallicRoughness','Normal']):
  v=doc['bufferViews'][doc['images'][i]['bufferView']];p=A/'Textures/MeshyV1'/(name+'_'+tex+'.jpg');assert not p.exists();p.write_bytes(raw[start+v.get('byteOffset',0):start+v.get('byteOffset',0)+v['byteLength']])
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.gltf(filepath=str(source));ref=next(o for o in bpy.context.scene.objects if o.type=='MESH');ref.name=name+'_UNMODIFIED_GLB';m=ref.data;m.calc_loop_triangles();points=[ref.matrix_world@v.co for v in m.vertices];mn=Vector(tuple(min(p[i]for p in points)for i in range(3)));mx=Vector(tuple(max(p[i]for p in points)for i in range(3)));origin=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=height/(mx.z-mn.z);points=[(p-origin)*scale for p in points]
 refcol=bpy.data.collections.new('UNMODIFIED_HIGH_REFERENCE');bpy.context.scene.collection.children.link(refcol)
 for c in list(ref.users_collection):c.objects.unlink(ref)
 refcol.objects.link(ref);refcol.hide_viewport=True;refcol.hide_render=True
 work=bpy.data.collections.new(name.upper()+'_ANIMATION_MASTER');bpy.context.scene.collection.children.link(work);body=ref.copy();body.data=ref.data.copy();body.name=name+'_Body';body.matrix_world=Matrix.Identity(4);work.objects.link(body)
 for v,p in zip(body.data.vertices,points):v.co=p
 body.data.update();arm=bpy.data.armatures.new(name+'_Rig');rig=bpy.data.objects.new(name+'_Rig',arm);work.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);rig.show_in_front=True;bpy.ops.object.mode_set(mode='EDIT');bones={}
 def bone(n,h,t,parent=None):
  b=arm.edit_bones.new(n);b.head=h;b.tail=t
  if parent:b.parent=arm.edit_bones[parent]
  bones[n]=(tuple(h),tuple(t),parent)
 sys.path.insert(0,str(Path(__file__).parent));from RigLayout import layout;positions,chains=layout(name)
 for n,(h,t,parent)in positions.items():bone(n,h,t,parent)
 bpy.ops.object.mode_set(mode='OBJECT')
 for n in bones:body.vertex_groups.new(name=n)
 from AutomaticSkin import assign_heat;weight_audit=assign_heat(body,rig)
 body.parent=rig;mod=body.modifiers.new('Anatomically fitted skin','ARMATURE');mod.object=rig;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.fps=30
 for im in bpy.data.images:
  if im.type=='IMAGE':im.pack()
 body.data.calc_loop_triangles();error=max((v.co-p).length for v,p in zip(body.data.vertices,points));assert error<1e-7;assert len(body.data.polygons)==len(m.polygons)
 audit={'species':name,'source':str(source.relative_to(R)),'source_sha256':digest,'height_m':height,'scale':scale,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'meshes':1,'materials':len(m.materials),'packed_images':[{'name':im.name,'size':list(im.size)}for im in bpy.data.images],'bones':bones,'leg_chains':chains,'rig_family':'Biped'if name=='Schiggy'else'Quadruped','rest_position_error_m':error,'faces_added_or_removed':0,'uv_original':True,'walk_speed_m_s':.26 if name=='Schiggy'else .32,'run_speed_m_s':.50 if name=='Schiggy'else .72,'weights':weight_audit}
 (A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out));assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('STARTER_SOURCE_PREPARED',name,flush=True)
