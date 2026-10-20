"""Authored compound fern fronds: curved rachis, folded pinnae and varied growth. No alpha cards."""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2WorldArtV7';dst=A/'Source/Westland_Ferns.blend';assert not dst.exists();dst.parent.mkdir(exist_ok=True);(A/'Exports').mkdir(exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mat=bpy.data.materials.new('Westland_PaintedFern');mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');vc=mat.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='Col';mat.node_tree.links.new(vc.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.9
catalog=[]
for variant,fronds in [('A',7),('B',9)]:
 rng=random.Random(20261020+(variant=='B'));vs=[];fs=[];uv=[];cols=[]
 def vtx(p,t,c,col):vs.append(tuple(p));uv.append((c,t));cols.append((*col,1));return len(vs)-1
 for f in range(fronds):
  angle=f*math.tau/fronds+rng.uniform(-.22,.22);dr=Vector((math.cos(angle),math.sin(angle),0));side=Vector((-dr.y,dr.x,0));radius=rng.uniform(.55,.80);height=rng.uniform(.52,.83)
  def centre(t):return dr*radius*(.16*t+.84*t*t)+Vector((0,0,height*math.sin(t*math.pi*.78)))+side*.025*math.sin(t*math.pi)*math.sin(angle*2)
  rows=[]
  for j in range(19):
   t=j/18;c=centre(t);rad=.005*(1-.86*t);row=[]
   for k in range(5):
    a=k*math.tau/5;row.append(vtx(c+side*(rad*math.cos(a))+Vector((0,0,rad*math.sin(a))),t,k/5,(.035,.085,.018)))
   rows.append(row)
  for r1,r2 in zip(rows,rows[1:]):
   for k in range(5):fs.append((r1[k],r1[(k+1)%5],r2[(k+1)%5],r2[k]))
  fs.append(tuple(reversed(rows[0])));fs.append(tuple(rows[-1]))
  for j in range(12):
   t=.14+j*.065;base=centre(t);length=(.145*math.sin(t*math.pi)**.85+.025)*rng.uniform(.9,1.08);width=length*.18
   for sg in [-1,1]:
    direction=(side*sg+dr*.30+Vector((0,0,.10-.2*t))).normalized();cross=Vector((-direction.y,direction.x,0));shade=rng.uniform(.85,1.14);col=(.038*shade,.11*shade,.025*shade);start=vtx(base,t,.5,col);leafrows=[]
    for k in range(1,5):
     u=k/5;ctr=base+direction*length*u+Vector((0,0,.022*math.sin(u*math.pi)-.025*u*u));span=width*math.sin(u*math.pi)**.7;row=[]
     for q in [-1,0,1]:
      c=tuple(x*(1.11 if q==0 else 1) for x in col);row.append(vtx(ctr+cross*span*q+Vector((0,0,.006*(1-abs(q))*math.sin(u*math.pi))),u,(q+1)/2,c))
     leafrows.append(row)
    tip=vtx(base+direction*length+Vector((0,0,-.025)),1,.5,col)
    fs.extend([(start,leafrows[0][0],leafrows[0][1]),(start,leafrows[0][1],leafrows[0][2])])
    for a,b in zip(leafrows,leafrows[1:]):
     for k in range(2):fs.append((a[k],b[k],b[k+1],a[k+1]))
    fs.extend([(leafrows[-1][0],tip,leafrows[-1][1]),(leafrows[-1][1],tip,leafrows[-1][2])])
 m=bpy.data.meshes.new('WA7_Fern_'+variant);m.from_pydata(vs,[],fs);m.update();m.materials.append(mat);o=bpy.data.objects.new('WA7_Fern_'+variant,m);s.collection.objects.link(o)
 # Match the existing original asset footprint/height; existing instance positions and scales stay valid.
 old=json.loads((R/'Saved/ArtPassV3/FernAudit.json').read_text())['meshes']['SM_WLA_Fern_'+variant];mn=Vector(tuple(min(v.co[i] for v in m.vertices) for i in range(3)));mx=Vector(tuple(max(v.co[i] for v in m.vertices) for i in range(3)));ext=[(old['max'][i]-old['min'][i])/100 for i in range(3)]
 for v in m.vertices:
  for i in range(3):v.co[i]=(v.co[i]-mn[i])/(mx[i]-mn[i])*ext[i]+old['min'][i]/100
 layer=m.uv_layers.new(name='UVMap');color=m.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for f in m.polygons:
  f.use_smooth=True
  for li in f.loop_indices:vi=m.loops[li].vertex_index;layer.data[li].uv=uv[vi];color.data[li].color=cols[vi]
 bm=bmesh.new();bm.from_mesh(m);assert not [f for f in bm.faces if f.calc_area()<1e-12];bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();m.calc_loop_triangles();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_WA7_Fern_'+variant+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,bake_anim=False,mesh_smooth_type='FACE');catalog.append({'variant':variant,'object':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'fronds':fronds,'pinnae':fronds*24,'dimensions_m':list(o.dimensions),'source_asset_replaced_only_in_VisualV2':old['path']});o.location.x=0 if variant=='A' else 2.0
bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.wm.open_mainfile(filepath=str(dst));assert len([o for o in bpy.data.objects if o.type=='MESH'])==2;(A/'FernRefinement.json').write_text(json.dumps({'source':str(dst.relative_to(R)),'reopened':True,'meshes':catalog,'no_alpha_cards':True},indent=2));print('FERN_SOURCE_REOPENED',json.dumps(catalog))
