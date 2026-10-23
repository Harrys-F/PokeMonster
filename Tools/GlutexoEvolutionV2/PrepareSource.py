"""Prepare ONE explicitly named source. Keep GLB topology, UVs, original reference and packed images."""
import bpy,json,hashlib,struct,sys
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent));from Anatomy import SPECS,layout;sys.path.append(str(R/"Tools/CreatureExpansionV3"))
name=sys.argv[sys.argv.index('--')+1];s=SPECS[name];A=R/'Art/Characters/Creatures'/name;out=A/'Source'/(name+'_Meshy_V1.blend');assert not out.exists()or '--revise-generated'in sys.argv;source=R/'Art/Characters/Creatures/Incoming'/(name+'.glb');raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest();intake=json.loads((R/'Saved/GlutexoEvolutionV2/Intake'/(name+'.json')).read_text());assert digest==intake['sha256']
for folder in ['Source','Textures/MeshyV1','Exports/MeshyV1']:(A/folder).mkdir(parents=True,exist_ok=True)
length,kind=struct.unpack_from('<II',raw,12);doc=json.loads(raw[20:20+length]);start=20+length+8;assert len(doc['images'])==3
for i,typ in enumerate(['BaseColor','MetallicRoughness','Normal']):
 im=doc['images'][i];assert im['mimeType']=='image/jpeg';v=doc['bufferViews'][im['bufferView']];p=A/'Textures/MeshyV1'/(name+'_'+typ+'.jpg');payload=raw[start+v.get('byteOffset',0):start+v.get('byteOffset',0)+v['byteLength']];assert not p.exists()or p.read_bytes()==payload;
 if not p.exists():p.write_bytes(payload)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.gltf(filepath=str(source));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1;ref=meshes[0];ref.name=name+'_UNMODIFIED_GLB';m=ref.data;m.calc_loop_triangles();points=[ref.matrix_world@v.co for v in m.vertices];mn=Vector(tuple(min(p[i]for p in points)for i in range(3)));mx=Vector(tuple(max(p[i]for p in points)for i in range(3)));origin=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z));scale=s['height']/(mx.z-mn.z);origin+=Vector(s.get('origin_offset',(0,0,0)))/scale;points=[(p-origin)*scale for p in points]
refcol=bpy.data.collections.new('UNMODIFIED_HIGH_REFERENCE');bpy.context.scene.collection.children.link(refcol)
for c in list(ref.users_collection):c.objects.unlink(ref)
refcol.objects.link(ref);refcol.hide_viewport=True;refcol.hide_render=True
work=bpy.data.collections.new(name.upper()+'_ANIMATION_MASTER');bpy.context.scene.collection.children.link(work);body=ref.copy();body.data=ref.data.copy();body.name=name+'_Body';body.matrix_world=Matrix.Identity(4);work.objects.link(body)
for v,p in zip(body.data.vertices,points):v.co=p
body.data.update();arm=bpy.data.armatures.new(name+'_Rig');rig=bpy.data.objects.new(name+'_Rig',arm);work.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);rig.show_in_front=True;bpy.ops.object.mode_set(mode='EDIT');bones,chains=layout(name)
for n,(h,t,parent)in bones.items():
 b=arm.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');from SkinEnvelopes import assign
if name in ['Enton','Machomei','Gengar','Glutexo']:
 for b in rig.data.bones:b.use_deform=b.name!='root'and not b.name.startswith(('tail_','ear_','leaf_','gas_','wing_'))
 sys.path.insert(0,str(R/'Tools/StarterExpansionV1'));from AutomaticSkin import assign_heat;weights=assign_heat(body,rig)
 for b in rig.data.bones:
  b.use_deform=b.name!='root'
  if b.name!='root'and not body.vertex_groups.get(b.name):body.vertex_groups.new(name=b.name)
else:weights=assign(body,rig,s,name)
if name=='Gengar':
 for v in body.data.vertices:
  if v.co.y>.20 and v.co.z<.75:
   t=max(0.,min(1.,(v.co.y-.20)/.20));t=t*t*(3-2*t);current={body.vertex_groups[g.group].name:g.weight*(1-t)for g in v.groups};current['tail_base']=current.get('tail_base',0)+t
   for group in body.vertex_groups:group.remove([v.index])
   total=sum(current.values())
   for group,value in current.items():
    if value>1e-7:body.vertex_groups[group].add([v.index],value/total,'REPLACE')
# Anatomical tail envelopes are separate from leg/body envelopes. Original geometry is retained.
for v in body.data.vertices:
 x,y,z=v.co
 if y>.045 and (z<.38 or x<-.25):
  candidates=['tail_base','tail_mid','tail_tip']
  if x<-.30 and y>.18 and z>.65:candidates=['flame_tip']
  def distance(n):
   b=rig.data.bones[n];d=b.tail_local-b.head_local;u=max(0.,min(1.,(v.co-b.head_local).dot(d)/d.length_squared));return (v.co-b.head_local-d*u).length
  values={n:1/max(.012,distance(n))**4 for n in candidates};total=sum(values.values())
  for g in body.vertex_groups:g.remove([v.index])
  for n,w in values.items():body.vertex_groups[n].add([v.index],w/total,'REPLACE')
from SmoothSkin import smooth
weights['smoothing']=smooth(body)
if name=='Glutexo':
 flame=body.data.materials[0].copy();flame.name='Glutexo_OriginalTailFlame';body.data.materials.append(flame);flame_faces=[]
 for polygon in body.data.polygons:
  centre=sum((body.data.vertices[i].co for i in polygon.vertices),Vector())/len(polygon.vertices)
  if centre.x<-.30 and centre.y>.18 and centre.z>.65:polygon.material_index=1;flame_faces.append(polygon.index)
 assert len(flame_faces)>20,flame_faces
 weights['original_flame_faces']=len(flame_faces)
 bsdf=next(n for n in flame.node_tree.nodes if n.type=='BSDF_PRINCIPLED');base=bsdf.inputs['Base Color'];bsdf.inputs['Emission Strength'].default_value=.35
 if base.is_linked:flame.node_tree.links.new(base.links[0].from_socket,bsdf.inputs['Emission Color'])

# Exact sole lock and rigid flat lightning tail. No geometry edits.
def assign(v,w):
 for g in body.vertex_groups:g.remove([v.index])
 total=sum(w.values());assert total>0
 for n,a in w.items():
  if a>1e-7:body.vertex_groups[n].add([v.index],a/total,'REPLACE')
locked=0
for v in body.data.vertices:
 x,y,z=v.co
 if x<-.30 and y>.18 and z>.65:assign(v,{'flame_tip':1})
 if chains and z<s['ankle'][2]*.8 and abs(x)>s['height']*.04:
  assign(v,{'foot_L'if x>0 else'foot_R':1});locked+=1
 if name=='Nebulak':
  # Facial sphere is rigid; smoke's existing sculpted volume gets only subtle peripheral deformation.
  radial=((x/.39)**2+((z-.47)/.39)**2)**.5
  if radial<.90:assign(v,{'head':1})
body.parent=rig;mod=body.modifiers.new('Anatomically fitted skin','ARMATURE');mod.object=rig;scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.render.fps=30
for im in bpy.data.images:
 if im.type=='IMAGE':im.pack()
assert max((v.co-p).length for v,p in zip(body.data.vertices,points))<1e-7;assert len(body.data.polygons)==len(m.polygons)
audit=dict(species=name,source=str(source.relative_to(R)),source_sha256=digest,height_m=s['height'],size_basis='standing_height',size_measurement='complete neutral model including ears/leaves/gas silhouette; no runtime actor rescaling',front='-Y',anatomical_origin_offset_m=s.get('origin_offset',(0,0,0)),scale=scale,vertices=len(m.vertices),triangles=len(m.loop_triangles),materials=len(body.data.materials),bones=bones,leg_chains=chains,rig_family=s['family'],walk_speed_m_s=s['walk'],run_speed_m_s=s['run'],geometry_unchanged=True,uv_original=True,weights=weights,sole_vertices_locked=locked,notes=['Original source appearance preserved; no remesh or decimation.'])
(A/'MeshyV1_ModelAudit.json').write_text(json.dumps(audit,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out));assert hashlib.sha256(source.read_bytes()).hexdigest()==digest;print('SOURCE_PREPARED',name,len(bones),flush=True)
