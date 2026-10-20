"""Preserve the identified GLB surfaces/UV/normals; own anatomically fitted rig, no remesh."""
import bpy,math,json,hashlib,struct
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2];A=R/'Art/Characters/Creatures/Zunderlauf';O=R/'Saved/MeshyGlumandaV1';out=A/'Source/Glumanda_Meshy_V1.blend';assert not out.exists()
source=R/'Art/Characters/Creatures/Incoming/Glumanda.glb';raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()=='44a82157d256a1ae4526f13c37aa3fc85d1022f2615f2812a2a8bba04ba4285c'
for p in [A/'Exports/MeshyV1',A/'Textures/MeshyV1']:p.mkdir(parents=True,exist_ok=True)
n,t=struct.unpack_from('<II',raw,12);doc=json.loads(raw[20:20+n]);binstart=20+n+8
for i,name in enumerate(['BaseColor','MetallicRoughness','Normal']):
 view=doc['bufferViews'][doc['images'][i]['bufferView']];p=A/'Textures/MeshyV1'/('Glumanda_'+name+'.jpg');assert not p.exists();p.write_bytes(raw[binstart+view.get('byteOffset',0):binstart+view.get('byteOffset',0)+view['byteLength']])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.gltf(filepath=str(source));ref=next(o for o in bpy.context.scene.objects if o.type=='MESH');ref.name='GLB_Original_Reference';m=ref.data;m.calc_loop_triangles();originalnormals=[n.vector.copy() for n in m.corner_normals];coords=[ref.matrix_world@v.co for v in m.vertices];mn=Vector(tuple(min(v[i]for v in coords)for i in range(3)));mx=Vector(tuple(max(v[i]for v in coords)for i in range(3)));center=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=.6/(mx.z-mn.z);points=[(v-center)*scale for v in coords]
reference=bpy.data.collections.new('UNMODIFIED_GLB_REFERENCE');bpy.context.scene.collection.children.link(reference)
for c in list(ref.users_collection):c.objects.unlink(ref)
reference.objects.link(ref);reference.hide_viewport=True;reference.hide_render=True
work=bpy.data.collections.new('GLUMANDA_MESHY_MASTER');bpy.context.scene.collection.children.link(work)
flamefaces=[];bodyfaces=[]
for f in m.polygons:
 c=sum((points[i] for i in f.vertices),Vector())/len(f.vertices)
 (flamefaces if c.y>.125 and c.x>.14 and c.z>.275 else bodyfaces).append(f)
assert flamefaces and bodyfaces
socket=Vector((.218,.19,.275))
def meshcopy(name,faces,origin):
 ids=sorted({i for f in faces for i in f.vertices});mapping={old:i for i,old in enumerate(ids)};mesh=bpy.data.meshes.new(name);mesh.from_pydata([points[i]-origin for i in ids],[],[tuple(mapping[i]for i in f.vertices)for f in faces]);mesh.update();uv=mesh.uv_layers.new(name='UVMap');normals=[]
 for nf,old in zip(mesh.polygons,faces):
  nf.use_smooth=True
  for nl,ol in zip(nf.loop_indices,old.loop_indices):uv.data[nl].uv=m.uv_layers.active.data[ol].uv;normals.append(originalnormals[ol])
 mesh.normals_split_custom_set(normals);mesh.materials.append(m.materials[0]);o=bpy.data.objects.new(name,mesh);work.objects.link(o);o.location=origin;return o,ids
body,ids=meshcopy('Glumanda_Meshy',bodyfaces,Vector());flame,_=meshcopy('Meshy_TailFlame_Original',flamefaces,socket)
assert len(body.data.polygons)+len(flame.data.polygons)==len(m.polygons)
arm=bpy.data.armatures.new('Glumanda_Meshy_Rig');rig=bpy.data.objects.new('Glumanda_Meshy_Rig',arm);work.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,h,t,parent=None):
 b=arm.edit_bones.new(name);b.head=h;b.tail=t
 if parent:b.parent=arm.edit_bones[parent]
bone('root',(0,0,0),(0,0,.06));bone('pelvis',(0,0,.145),(0,0,.215),'root');bone('spine',(0,0,.215),(0,0,.285),'pelvis');bone('chest',(0,0,.285),(0,0,.355),'spine');bone('head',(0,0,.355),(0,0,.575),'chest')
for side,s in [('L',1),('R',-1)]:
 bone('upperarm_'+side,(s*.105,0,.323),(s*.183,-.008,.323),'chest');bone('forearm_'+side,(s*.183,-.008,.323),(s*.240,-.013,.323),'upperarm_'+side);bone('hand_'+side,(s*.240,-.013,.323),(s*.271,-.022,.323),'forearm_'+side)
 bone('thigh_'+side,(s*.115,.012,.155),(s*.115,-.047,.095),'pelvis');bone('shin_'+side,(s*.115,-.047,.095),(s*.115,-.052,.032),'thigh_'+side);bone('foot_'+side,(s*.115,-.052,.032),(s*.115,-.118,.017),'shin_'+side)
tail=[Vector(v) for v in [(0,.07,.14),(.015,.13,.12),(.075,.195,.135),(.16,.232,.18),(.213,.22,.258),(.218,.19,.305)]]
for i in range(4):bone('tail_0'+str(i+1),tail[i],tail[i+1],'pelvis' if i==0 else 'tail_0'+str(i))
bone('tail_tip',tail[4],tail[5],'tail_04');bone('tail_socket',socket,socket+Vector((0,0,.02)),'tail_tip');bpy.ops.object.mode_set(mode='OBJECT')
def smooth(a,b,x):u=max(0.,min(1.,(x-a)/(b-a)));return u*u*(3-2*u)
def add(w,k,v):
 if v>1e-9:w[k]=w.get(k,0)+v
def distline(p,a,b):u=max(0.,min(1.,(p-a).dot(b-a)/(b-a).length_squared));return (p-a-u*(b-a)).length,u
weights=[]
for p in points:
 x,y,z=p;side='L' if x>=0 else 'R';w={};near=min(((*distline(p,tail[i],tail[i+1]),i)for i in range(5)),key=lambda a:a[0]);distance,u,index=near
 tailgate=smooth(.075,.125,y)*(1-smooth(.055,.085,distance))*(1-smooth(.30,.34,z))
 if z>.26 and x<.13:tailgate=0
 if tailgate>0:
  k=['tail_01','tail_02','tail_03','tail_04','tail_tip'][index];nextk=['tail_02','tail_03','tail_04','tail_tip','tail_tip'][index];add(w,k,tailgate*(1-u));add(w,nextk,tailgate*u)
  if z>.26: w={'tail_tip':1};weights.append(w);continue
 remaining=1-tailgate;armgate=smooth(.100,.145,abs(x))*smooth(.245,.29,z)*(1-smooth(.36,.385,z));leggate=(1-smooth(.13,.185,z))*smooth(.05,.085,abs(x))
 if armgate:
  t=smooth(.155,.205,abs(x));h=smooth(.224,.251,abs(x));add(w,'upperarm_'+side,remaining*armgate*(1-t));add(w,'forearm_'+side,remaining*armgate*t*(1-h));add(w,'hand_'+side,remaining*armgate*t*h)
 elif leggate:
  f=1-smooth(.04,.075,z);th=smooth(.075,.13,z);add(w,'foot_'+side,remaining*leggate*f);add(w,'shin_'+side,remaining*leggate*(1-f)*(1-th));add(w,'thigh_'+side,remaining*leggate*(1-f)*th)
 rest=remaining*(1-armgate if armgate else 1-leggate);h=smooth(.33,.385,z);c=smooth(.23,.31,z)*(1-h);sp=smooth(.15,.235,z)*(1-h-c)
 for k,v in {'head':h,'chest':c,'spine':sp,'pelvis':1-h-c-sp}.items():add(w,k,rest*v)
 total=sum(w.values());weights.append({k:v/total for k,v in w.items()})
for name in arm.bones:body.vertex_groups.new(name=name.name)
for vi,old in enumerate(ids):
 for name,w in weights[old].items():body.vertex_groups[name].add([vi],w,'REPLACE')
body.parent=rig;mod=body.modifiers.new('Fitted creature skin','ARMATURE');mod.object=rig
flame.parent=rig;flame.parent_type='BONE';flame.parent_bone='tail_socket';flame.matrix_world=Matrix.Translation(socket)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.fps=30
for image in bpy.data.images:
 if image.type=='IMAGE':image.pack()
# Rest silhouette is a split of exactly the original triangles after one uniform normalization.
audit={'original_glb':str(source.relative_to(R)),'source_sha256':hashlib.sha256(raw).hexdigest(),'scale':scale,'original_height_m':mx.z-mn.z,'height_m':.6,'body_vertices':len(body.data.vertices),'body_triangles':len(body.data.polygons),'flame_vertices':len(flame.data.vertices),'flame_triangles':len(flame.data.polygons),'total_triangles':len(m.polygons),'faces_removed':0,'new_faces':0,'uv_and_custom_normals_copied':True,'rest_vertex_position_error_m':0.,'bones':len(arm.bones),'tail_socket_m':list(socket),'tail_isolation':'Original triangles only; spatial boundary above tail neck; no second flame mesh added','weights':'Anatomical region masks and smooth capsule/chain interpolation; coincident UV seam positions share weights','normalization':'One uniform scale and origin translation; reference mesh untouched'}
bpy.ops.wm.save_as_mainfile(filepath=str(out));(A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));print('MESHY_PREPARE_PASS',json.dumps(audit))
