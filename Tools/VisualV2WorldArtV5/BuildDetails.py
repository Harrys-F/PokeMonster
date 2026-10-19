"""Only missing botanical forms: small clover/low moss and natural bank reeds.
Existing V4 grasses, Westland ferns, roots, shrubs and stones are reused separately.
"""
from pathlib import Path
import bpy,bmesh,math,random,json
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/World/VisualV2WorldArtV5';S=R/'Saved/VisualV2WorldArtV5';dst=A/'Source/Westland_ThreeBiomes_Details_V5.blend';assert bpy.app.background and not dst.exists();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats=[]
for name,col in [('Foliage',(.065,.13,.035,1)),('Seed',(.19,.12,.06,1))]:
 m=bpy.data.materials.new('WA5_'+name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.88;bs.inputs['Base Color'].default_value=col;vc=m.node_tree.nodes.new('ShaderNodeVertexColor');vc.layer_name='Col';m.node_tree.links.new(vc.outputs['Color'],bs.inputs['Base Color']);mats.append(m)
catalog={}
for index,family in enumerate(['CloverPatch','MossCushion','ReedTuft']):
 rng=random.Random(5319+index);vs=[];fs=[];cols=[];uvs=[];material=[]
 def vert(p,uv=(0,0),col=(1,1,1,1)):vs.append(tuple(p));uvs.append(uv);cols.append(col);return len(vs)-1
 def face(f,mat=0):fs.append(tuple(f));material.append(mat)
 def tube(points,radius,col,mat=0):
  rings=[]
  for i,p in enumerate(points):
   d=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=d.cross(Vector((0,1,0))).normalized();v=d.cross(u).normalized();r=radius*(1-.45*i/max(1,len(points)-1));rings.append([vert(p+r*(u*math.cos(j*math.tau/6)+v*math.sin(j*math.tau/6)),(j/6,i/max(1,len(points)-1)),col) for j in range(6)])
  for a,b in zip(rings,rings[1:]):
   for j in range(6):face((a[j],a[(j+1)%6],b[(j+1)%6],b[j]),mat)
  # Planar cap UVs are set per face below, not shared cylindrical zero-area UVs.
  face(tuple(reversed(rings[0])),mat);face(rings[-1],mat)
 def leaf(a,b,width,col,kind='blade'):
  d=b-a;side=d.cross(Vector((0,0,1)))
  if side.length<.001:side=Vector((1,0,0))
  side.normalize();normal=side.cross(d).normalized();start=vert(a,(.5,0),col);rows=[]
  for i in range(1,7):
   t=i/7;mid=a+d*t+normal*(math.sin(t*math.pi)*.009-.012*t*t);span=width*math.sin(t*math.pi)**(.56 if kind=='clover' else .9);span*=1+.10*math.cos(t*math.tau*2) if kind=='clover' else 1
   row=[]
   for j in range(5):
    u=(j-2)/2;row.append(vert(mid+side*u*span+normal*.008*(1-u*u)*math.sin(t*math.pi),(j/4,t),tuple(c*(1+.10*(1-abs(u))) for c in col[:3])+(1,)))
   rows.append(row)
  tip=vert(b,(.5,1),col)
  for j in range(4):face((start,rows[0][j],rows[0][j+1]))
  for row,nextrow in zip(rows,rows[1:]):
   for j in range(4):face((row[j],nextrow[j],nextrow[j+1],row[j+1]))
  for j in range(4):face((rows[-1][j],tip,rows[-1][j+1]))
 if family=='CloverPatch':
  for i in range(22):
   ang=rng.uniform(0,math.tau);r=rng.uniform(.01,.21);root=Vector((r*math.cos(ang),r*math.sin(ang),0));top=root+Vector((rng.uniform(-.018,.018),rng.uniform(-.018,.018),rng.uniform(.055,.13)));col=(.040*rng.uniform(.8,1.2),.12*rng.uniform(.85,1.15),.018,1);tube([root,top],.0015,col)
   for j in range(3):
    a=ang+j*math.tau/3;length=rng.uniform(.035,.058);leaf(top,top+Vector((math.cos(a)*length,math.sin(a)*length,.004)),length*.55,col,'clover')
 elif family=='MossCushion':
  for i in range(46):
   a=rng.random()*math.tau;r=rng.random()**.6*.29;root=Vector((math.cos(a)*r,math.sin(a)*r,.002));h=rng.uniform(.025,.065)*(1-.3*r/.29);col=(.047,.10*rng.uniform(.85,1.2),.016,1)
   for j in range(3):
    b=a+j*2.399;leaf(root,root+Vector((math.cos(b)*.045,math.sin(b)*.045,h)),.015,col)
 else:
  for i in range(13):
   a=i*2.399+rng.uniform(-.3,.3);r=rng.uniform(.025,.17);root=Vector((math.cos(a)*r,math.sin(a)*r,0));h=rng.uniform(.56,1.0);lean=Vector((math.cos(a)*rng.uniform(.05,.18),math.sin(a)*rng.uniform(.05,.18),0));points=[root+lean*(t*t)+Vector((0,0,h*t)) for t in [0,.2,.4,.6,.8,1]];col=(.065,.13*rng.uniform(.8,1.05),.035,1);tube(points,.0032,col)
   for j in [1,2,3,4]:
    ori=points[j];ang=a+j*2.1;length=rng.uniform(.17,.32)*(1-.07*j);leaf(ori,ori+Vector((math.cos(ang)*length,math.sin(ang)*length,length*.3)),.015+rng.random()*.01,col)
   if i%3==0:
    # Restrained bent seed head, modeled as a tapered spindle rather than a rigid floating capsule.
    p=points[-1];axis=Vector((lean.x*.2,lean.y*.2,.13));tube([p,p+axis*.25,p+axis*.65,p+axis],.014,(.12,.073,.027,1),1)
 me=bpy.data.meshes.new('WA5_'+family);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('WA5_'+family,me);s.collection.objects.link(o)
 for m in mats:me.materials.append(m)
 uv=me.uv_layers.new(name='UVMap');co=me.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for f,mat in zip(me.polygons,material):
  f.material_index=mat;f.use_smooth=True;axis=max(range(3),key=lambda i:abs(f.normal[i]));ab=[(1,2),(0,2),(0,1)][axis];cap=len(f.vertices)==6
  for li in f.loop_indices:
   vi=me.loops[li].vertex_index;v=me.vertices[vi].co;uv.data[li].uv=(v[ab[0]]*3,v[ab[1]]*3) if cap else uvs[vi];co.data[li].color=cols[vi]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.calc_loop_triangles();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_WA5_'+family+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False,path_mode='COPY')
 catalog[family]={'object':o.name,'vertices':len(me.vertices),'triangles':len(me.loop_triangles),'dimensions_m':[max(v.co[i] for v in me.vertices)-min(v.co[i] for v in me.vertices) for i in range(3)],'materials':[m.name for m in me.materials]};o.location.x=(index-1)*.9
world=bpy.data.worlds.new('Neutral botanical inspection');s.world=world;world.use_nodes=True;world.node_tree.nodes.get('Background').inputs[0].default_value=(.11,.12,.13,1)
for name,power,pos,size in [('Key',450,(1,-3,4),4),('Fill',300,(-2,0,3),3)]:
 l=bpy.data.lights.new(name,'AREA');l.energy=power;l.size=size;o=bpy.data.objects.new(name,l);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
c=bpy.data.cameras.new('Overview');o=bpy.data.objects.new('Overview',c);s.collection.objects.link(o);o.location=(1,-4,2.8);o.rotation_euler=(Vector((0,0,.35))-o.location).to_track_quat('-Z','Y').to_euler();c.type='ORTHO';c.ortho_scale=3.2;s.camera=o;s.render.resolution_x=1500;s.render.resolution_y=850;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(S/'BlenderDetails.png')
bpy.ops.wm.save_as_mainfile(filepath=str(dst));(A/'Details.json').write_text(json.dumps(catalog,indent=2));bpy.ops.wm.open_mainfile(filepath=str(dst));assert len([o for o in bpy.data.objects if o.type=='MESH'])==3;bpy.ops.render.render(write_still=True);print('WA5_SOURCE_REOPEN_OK',json.dumps(catalog))
