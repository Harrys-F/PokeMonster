"""Art revision of exactly twenty existing WLA meshes. Keep V1 source and 26 other meshes.
Metres, ground pivots, explicit triangle UVs; real branch/spray construction, no crown cores.
Run background with V1 open. Saves a sibling V2 blend, never saves the input source.
"""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];ART=R/'Art/World/WestlandAssetLibrary';O=R/'Saved/WestlandAssetLibraryV2';O.mkdir(exist_ok=True)
assert bpy.app.background and Path(bpy.data.filepath).name=='WestlandAssetLibrary_V1.blend'
TARGET=ART/'Source/WestlandAssetLibrary_V2.blend'
if TARGET.exists():
 import shutil
 backup=O/('WestlandAssetLibrary_V2_Working_'+str(len(list(O.glob('WestlandAssetLibrary_V2_Working_*.blend'))))+'.blend');shutil.copy2(TARGET,backup)
bpy.context.preferences.filepaths.save_version=0
scene=bpy.data.scenes['WestlandAssetLibrary_Source'];bpy.context.window.scene=scene
catalog=json.loads((ART/'Assets.json').read_text());rng=random.Random(70219)
keys=['OakAncient','OakYoung','Birch','FruitTree','Bush','Fern','Stump','Root','Column','Runestone']
selected=[a for a in catalog['assets'] if any(a['id'].startswith('WLA_'+k+'_') for k in keys)]
assert len(selected)==20
mats={m.name.removeprefix('WLA_'):m for m in bpy.data.materials if m.name.startswith('WLA_') and '.' not in m.name}
for key,tint in [('LeafOak',(.80,.89,.72)),('LeafBirch',(.83,.92,.77)),('LeafOrchard',(.86,.89,.71)),('LeafFern',(.72,.87,.71))]:
 m=mats['Leaf'].copy();m.name='WLA_'+key;mats[key]=m
 im=bpy.data.images.load(str(ART/'Textures'/('T_WLA_'+key+'_V2.png')),check_existing=True)
 for n in m.node_tree.nodes:
  if n.type=='TEX_IMAGE':n.image=im
  elif n.type=='MIX_RGB':n.inputs[2].default_value=(*tint,1)
 # Make vertex pigments visible in Blender as they are in Unreal's existing master.
 mix=next(n for n in m.node_tree.nodes if n.type=='MIX_RGB');bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');v=m.node_tree.nodes.new('ShaderNodeVertexColor');v.layer_name='PaintTint';mul=m.node_tree.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;m.node_tree.links.new(mix.outputs[0],mul.inputs[1]);m.node_tree.links.new(v.outputs['Color'],mul.inputs[2]);m.node_tree.links.new(mul.outputs[0],bs.inputs['Base Color'])
 catalog['materials'][key]={'color':list(tint),'texture':str((ART/'Textures'/('T_WLA_'+key+'_V2.png')).relative_to(R)),'two_sided':True,'vertex_color':True}
verts=[];faces=[];uvs=[];slots=[];face_mats=[];colors=[];active_leaf_scale=1.0
def surface(v,f,key,uv=None,pigment=(1,1,1,1)):
 off=len(verts);verts.extend([tuple(x) for x in v]);colors.extend([pigment]*len(v));uvs.extend(uv or [(p[0],p[2]) for p in v])
 if key not in slots:slots.append(key)
 faces.extend([tuple(off+i for i in x) for x in f]);face_mats.extend([slots.index(key)]*len(f))
def tube(points,radii,key='Bark',sides=10):
 pts=[Vector(p) for p in points];v=[];uv=[];f=[];arc=0
 for j,p in enumerate(pts):
  if j:arc+=(p-pts[j-1]).length
  d=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized();ref=Vector((0,0,1)) if abs(d.z)<.92 else Vector((0,1,0));x=d.cross(ref).normalized();y=d.cross(x).normalized()
  for i in range(sides+1):
   a=i/sides*math.tau;r=radii[j]*(1+.09*math.sin(a*5+j*.30));v.append(p+r*(x*math.cos(a)+y*math.sin(a)));uv.append((i/sides,arc*.65))
 for j in range(len(pts)-1):
  for i in range(sides):q=j*(sides+1)+i;f.extend([(q,q+1,q+sides+2),(q,q+sides+2,q+sides+1)])
 surface(v,f,key,uv)
 # Endcaps are separate, flat-shaded triangle fans, with planar UVs (no collinear cap UVs).
 for j,reverse in [(0,True),(len(pts)-1,False)]:
  vv=[pts[j]]+[Vector(v[j*(sides+1)+i]) for i in range(sides)];ff=[]
  for i in range(sides):ff.append((0,(i+1)%sides+1,i+1) if reverse else (0,i+1,(i+1)%sides+1))
  uu=[(.5,.5)]+[(.5+.5*math.cos(math.tau*i/sides),.5+.5*math.sin(math.tau*i/sides)) for i in range(sides)];surface(vv,ff,key,uu)
def blade(base,direction,length,width,key,lobed=False,pigment=(1,1,1,1)):
 length*=active_leaf_scale;width*=active_leaf_scale
 base=Vector(base);d=Vector(direction).normalized();x=d.cross(Vector((0,0,1)))
 if x.length<.1:x=Vector((1,0,0))
 x.normalize();up=x.cross(d).normalized();v=[base];uv=[(.5,.02)];f=[]
 # Unique base/tip: no collapsed row, no duplicate zero-area edge faces.
 for j in range(1,6):
  t=j/6;w=width*math.sin(math.pi*t)**.65*(1+.23*math.sin(t*math.pi*8) if lobed else 1)
  center=base+d*(length*t)+up*(length*.14*math.sin(math.pi*t))
  for k in (-1,0,1):v.append(center+x*w*k+up*(width*.13 if k==0 else 0));uv.append((.5+k*.47,t*.96+.02))
 f=[(0,1,2),(0,2,3)]
 for j in range(4):
  q=1+j*3
  f.extend([(q,q+3,q+4),(q,q+4,q+1),(q+1,q+4,q+5),(q+1,q+5,q+2)])
 v.append(base+d*length-up*(length*.04));uv.append((.5,.98));q=13;f.extend([(q,16,q+1),(q+1,16,q+2)])
 surface(v,f,key,uv,pigment)
def spray(center,size,key,phase=0,pendant=False):
 c=Vector(center)
 for j in range(3):
  a=phase+j*2.399+rng.uniform(-.20,.20);d=Vector((math.cos(a),math.sin(a),rng.uniform(-.30,.60)));reach=size*rng.uniform(.60,1)
  points=[c,c+d*reach*.45+Vector((0,0,size*.14)),c+d*reach]
  tube(points,[size*.017,size*.010,size*.003],'Birch' if key=='LeafBirch' else 'Bark',5)
  for k in range(1,3):
   p=points[0].lerp(points[-1],k/2.8);side=Vector((-d.y,d.x,.28));leaflen=size*rng.uniform(.52,.74);wide=leaflen*(.23 if key=='LeafBirch' else .30)
   for sign in (-1,1):
    out=d*.45+side*sign;out.z-=.42 if pendant else 0
    shade=rng.uniform(.77,1.04);blade(p,out,leaflen,wide,key,key=='LeafOak',(shade,shade,shade*.96,1))
  blade(points[-1],d+Vector((0,0,.14)),size*.63,size*.19,key,key=='LeafOak')
def tree(kind,variant):
 global active_leaf_scale
 active_leaf_scale={"OakAncient":.50,"OakYoung":.80,"Birch":.72,"FruitTree":.80}[kind]
 h={'OakAncient':11.7,'OakYoung':5.15,'Birch':9.0,'FruitTree':5.3}[kind];w={'OakAncient':4.25,'OakYoung':2.0,'Birch':1.65,'FruitTree':2.5}[kind];tr={'OakAncient':.57,'OakYoung':.22,'Birch':.15,'FruitTree':.25}[kind]
 key={'Birch':'LeafBirch','FruitTree':'LeafOrchard'}.get(kind,'LeafOak');bark='Birch' if kind=='Birch' else 'Bark';phase=variant*.77;lean=.32 if variant==0 else -.34
 trunk=[(0,0,0),(.05,-.02,h*.16),(lean,.09,h*.34),(lean*.5,.15,h*.53),(lean+.18,.02,h*.74),(lean+.12,.15,h*.87)]
 tube(trunk,[tr*1.5,tr,tr*.78,tr*.59,tr*.32,.02],bark,16)
 for j in range(5 if kind!='Birch' else 3):
  a=j*2.399+phase;d=Vector((math.cos(a),math.sin(a),0));tube([(0,0,.35),d*tr*1.2+Vector((0,0,.15)),d*tr*2.2+Vector((0,0,.045))],[tr*.40,tr*.20,.035],bark,10)
 count=9 if kind=='OakAncient' else 7
 for j in range(count):
  a=j*2.399+phase;d=Vector((math.cos(a),math.sin(a),0));z=h*(.48+.34*j/(count-1));r=w*(.90-.38*j/(count-1));base=Vector((lean*.65,.07,z-h*.18));mid=base+d*r*.58+Vector((0,0,h*.13));tip=base+d*r+Vector((0,0,h*(.16 if kind=='Birch' else .12)))
  tube([base,base+d*r*.19+Vector((0,0,h*.025)),mid,tip],[tr*.40,tr*.31,tr*.16,.014],bark,10)
  for k in range(4):
   angle=a+(k-1.5)*.56;side=Vector((math.cos(angle),math.sin(angle),0));p=mid.lerp(tip,k/4);end=p+side*w*.36+Vector((0,0,h*.035+rng.uniform(-.13,.13)))
   tube([p,p.lerp(end,.45)+Vector((0,0,.10)),end],[tr*.11,tr*.055,.007],bark,7)
   size=w*(.24 if kind!='Birch' else .31);spray(end,size,key,angle,kind=='Birch');spray(end-side*size*.55+Vector((0,0,size*.52)),size*.80,key,angle+.7,kind=='Birch')
  spray(tip,w*.26,key,a,kind=='Birch')
 for j in range(5):spray(Vector(trunk[-1])+Vector((math.cos(j*2.4)*w*.27,math.sin(j*2.4)*w*.27,-j*.10)),w*.27,key,j*2.4,kind=='Birch')
 if kind=='FruitTree':
  for j in range(16):
   a=j*2.4+phase;p=Vector((math.cos(a)*w*.75,math.sin(a)*w*.75,h*(.59+.17*(j%4)/3)));organic_stone(p,(.075,.072,.082),j,'Apple')
 active_leaf_scale=1.0
def bush(variant):
 for j in range(9):
  a=j*2.399+variant*.8;r=rng.uniform(.32,.66);tip=Vector((math.cos(a)*r,math.sin(a)*r,.65+rng.uniform(-.18,.30)));tube([(0,0,.04),tip*.50+Vector((0,0,.10)),tip],[.04,.022,.007],sides=7)
  spray(tip,.48,'LeafOrchard',a);spray(tip+Vector((-.12,.08,.17)),.38,'LeafOrchard',a+.6)
def fern(variant):
 for j in range(11):
  a=j*2.399+variant*.65;d=Vector((math.cos(a),math.sin(a),0));size=rng.uniform(.63,.88);pts=[]
  for k in range(17):t=k/16;pts.append(d*size*t+Vector((0,0,.04+size*.83*math.sin(t*2.15))))
  tube(pts,[.008*(1-k/20) for k in range(17)],'LeafFern',5)
  for k in range(2,16):
   t=k/16;side=Vector((-d.y,d.x,.08));ln=size*.23*math.sin(t*math.pi)**.8
   for sign in (-1,1):blade(pts[k],side*sign+d*.35,ln,ln*.15,'LeafFern',True,(.82+.16*t,.86+.10*t,.80+.12*t,1))
def stump(variant):
 sides=32;v=[];f=[];uu=[]
 for j in range(9):
  t=j/8
  for i in range(sides+1):
   a=i/sides*math.tau;r=.32+(.18*(1-t)**3)+.035*math.sin(a*5+variant)+.018*math.sin(a*11+t*3);z=.80*t+(t**4)*(.015*math.sin(a*5)+.008*math.cos(a*9));v.append((r*math.cos(a)+.05*t,r*math.sin(a),z));uu.append((i/sides,t*.70))
 for j in range(8):
  for i in range(sides):q=j*(sides+1)+i;f.extend([(q,q+1,q+sides+2),(q,q+sides+2,q+sides+1)])
 surface(v,f,'Bark',uu)
 # Uneven exposed end-grain, recessed growth rings, not a perfect cylinder cap.
 vv=[(.05,0,.798)]+[v[8*(sides+1)+i] for i in range(sides)];surface(vv,[(0,i+1,(i+1)%sides+1) for i in range(sides)],'Wood',[(.5,.5)]+[(.5+.45*math.cos(i/sides*math.tau),.5+.45*math.sin(i/sides*math.tau)) for i in range(sides)])
 for rr in (.10,.17,.24):
  ps=[(.05+(rr+.009*math.sin(i*.7))*math.cos(i*math.tau/40),(rr+.009*math.sin(i*.7))*math.sin(i*math.tau/40),.802) for i in range(41)];tube(ps,[.0028]*41,'Timber',4)
 for j in range(5):
  a=j*2.399+variant*.7;d=Vector((math.cos(a),math.sin(a),0));tube([d*.25+Vector((0,0,.27)),d*.45+Vector((0,0,.15)),d*.65+Vector((0,0,.06)),d*.82+Vector((0,0,.04))],[.16,.13,.08,.048],sides=10)
 # Small broken branch, rounded, not a star point.
 tube([(.26,0,.48),(.44,.03,.56),(.52,.08,.62)],[.09,.07,.045],sides=10)
def root(variant):
 ps=[(-.82,-.06,.08),(-.55,.03,.22),(-.1,.03,.31),(.30,-.12,.22),(.83,-.20,.09)]
 tube(ps,[.09,.13,.18,.13,.07],sides=12)
 for j in range(2):
  p=Vector(ps[1+j%3]);sgn=(-1)**j;end=p+Vector((.20,sgn*(.45+j*.07),-.18));tube([p,p.lerp(end,.45)+Vector((.02,0,.06)),end],[.10,.08,.042],sides=9)
def organic_stone(center,size,seed,key='MossStone'):
 # Rounded/chipped layered stone with multiple curvature bands and no primitive operator.
 v=[];f=[];uv=[];sides=20;levels=10
 for j in range(levels+1):
  t=j/levels;z=-1+2*t;radius=math.sqrt(max(.025,1-z*z));
  for i in range(sides+1):
   a=i/sides*math.tau;noise=1+.10*math.sin(a*3+seed)+.05*math.cos(a*7+z*4+seed);p=Vector((math.cos(a)*size[0]*radius*noise,math.sin(a)*size[1]*radius*noise,z*size[2]*(1+.035*math.cos(a*5+seed))))+Vector(center);v.append(p);uv.append((i/sides,t))
 for j in range(levels):
  for i in range(sides):q=j*(sides+1)+i;f.extend([(q,q+1,q+sides+2),(q,q+sides+2,q+sides+1)])
 surface(v,f,key,uv)
def column(variant):
 # Faceted weathered carved shaft with entasis/fluting, irregular broken rim and softened bases.
 sides=32;v=[];uu=[];f=[]
 for j in range(17):
  t=j/16
  for i in range(sides+1):
   a=i/sides*math.tau;r=.28+.035*math.sin(t*math.pi)-.016*math.cos(a*8)+.012*math.sin(a*3+t*9+variant);z=.19+1.65*t+t**8*(.10*math.sin(a*3+.8*variant)+.04*math.cos(a*7));v.append((r*math.cos(a)+.05*t*t,r*math.sin(a),z));uu.append((i/sides*1.1,t*1.7))
 for j in range(16):
  for i in range(sides):q=j*(sides+1)+i;f.extend([(q,q+1,q+sides+2),(q,q+sides+2,q+sides+1)])
 surface(v,f,'MossStone',uu)
 # Broken irregular exposed top. Circular fan with valid planar UVs.
 vv=[(.05,0,1.82)]+[v[16*(sides+1)+i] for i in range(sides)];surface(vv,[(0,i+1,(i+1)%sides+1) for i in range(sides)],'Stone',[(.5,.5)]+[(.5+.45*math.cos(i/sides*math.tau),.5+.45*math.sin(i/sides*math.tau)) for i in range(sides)])
 organic_stone((0,0,.10),(.48,.46,.11),variant+7)
 organic_stone((0,0,.22),(.38,.37,.065),variant+2)
def runestone(variant):
 # Structured worn monolith grid; engraved lines are recessed into the face, not added tubes.
 v=[];f=[];uv=[];nx=32;nz=48;width=.98;height=2.25;depth=.28
 segments=[((-.25,.62),(.22,1.32)),((.22,1.32),(-.16,1.77)),((-.16,1.77),(.18,1.96)),((-.16,1.77),(-.28,1.43)),((.22,1.32),(.30,.98))]
 def line_dist(x,z,a,b):
  p=Vector((x,z));a=Vector(a);b=Vector(b);t=max(0,min(1,(p-a).dot(b-a)/(b-a).length_squared));return (p-a-(b-a)*t).length
 for side in (-1,1):
  for j in range(nz+1):
   z=j/nz*height
   for i in range(nx+1):
    t=i/nx;x=(t-.5)*width*(.91+.07*math.sin(z*1.5)+.03*math.sin(z*8+variant));edge=abs(t-.5)*2;zv=z+(.035*math.sin(t*9+variant))*((z/height)**8);y=side*(depth+.022*math.sin(x*8+z*5)+.011*math.cos(z*13+x*11));dist=min(line_dist(x,z,a,b) for a,b in segments)
    if side==-1:y+=.062*math.exp(-(dist/.019)**2)*min(1,(1-edge)*10)
    y*=1-.15*edge**8;v.append((x,y,zv));uv.append((x*1.2,z*.8))
  off=0 if side==-1 else (nx+1)*(nz+1)
  for j in range(nz):
   for i in range(nx):q=off+j*(nx+1)+i;f.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)] if side==-1 else [(q,q+nx+2,q+1),(q,q+nx+1,q+nx+2)])
 surface(v,f,'MossStone',uv)
 # Rounded rim strips stitch front/back without coplanar UVs.
 n=(nx+1)*(nz+1)
 for indices in [[i for i in range(nx+1)],[nz*(nx+1)+i for i in range(nx+1)],[j*(nx+1) for j in range(nz+1)],[j*(nx+1)+nx for j in range(nz+1)]]:
  vv=[v[i] for i in indices]+[v[i+n] for i in indices];m=len(indices);ff=[]
  for k in range(m-1):ff.extend([(k,k+1,k+1+m),(k,k+1+m,k+m)])
  surface(vv,ff,'MossStone',[(k/(m-1),side) for side in (0,1) for k in range(m)])

audit=[]
for a in selected:
 verts=[];faces=[];uvs=[];slots=[];face_mats=[];colors=[];active_leaf_scale=1.0;rng.seed(70219+sum(map(ord,a['id'])))
 kind=a['id'].split('_')[1];variant=int(a['variant']=='B');old=bpy.data.objects[a['object']];collection=bpy.data.collections[a['id']]
 # Keep the object, collection, collision proxy, review references and all non-selected assets.
 if kind in ('OakAncient','OakYoung','Birch','FruitTree'):tree(kind,variant)
 else:globals()[kind.lower()](variant)
 if kind=='Root':verts=[(x,y,z*.52) for x,y,z in verts]
 if kind=='Runestone':
  for idx,(x,y,z) in enumerate(verts):
   if y<0:
    # Pigment settles in the actual engraved recess; no floating glyph geometry.
    dist=min((Vector((x,z))-Vector(a)).length if Vector(b)==Vector(a) else (Vector((x,z))-Vector(a)-(Vector(b)-Vector(a))*max(0,min(1,(Vector((x,z))-Vector(a)).dot(Vector(b)-Vector(a))/(Vector(b)-Vector(a)).length_squared))).length for a,b in [((-.25,.62),(.22,1.32)),((.22,1.32),(-.16,1.77)),((-.16,1.77),(.18,1.96)),((-.16,1.77),(-.28,1.43)),((.22,1.32),(.30,.98))])
    w=math.exp(-(dist/.029)**2);colors[idx]=(1-.40*w,1-.32*w,1-.39*w,1)
 mesh=bpy.data.meshes.new(a['object']+'_ArtV2');mesh.from_pydata(verts,[],faces);mesh.update();uv=mesh.uv_layers.new(name='UV0')
 for p,mat in zip(mesh.polygons,face_mats):
  p.material_index=mat;p.use_smooth=True
  for li in p.loop_indices:uv.data[li].uv=uvs[mesh.loops[li].vertex_index]
 for key in slots:mesh.materials.append(mats[key])
 paint=mesh.color_attributes.new(name='PaintTint',type='FLOAT_COLOR',domain='POINT')
 for i,c in enumerate(colors):paint.data[i].color=c
 mesh.color_attributes.active_color=paint
 # Every triangle gets a sound UV chart. Caps and rims can have a different projection.
 fixed=0
 for p in mesh.polygons:
  i,j,k=p.loop_indices;aa,bb,cc=[uv.data[x].uv for x in (i,j,k)];det=abs((bb.x-aa.x)*(cc.y-aa.y)-(bb.y-aa.y)*(cc.x-aa.x))
  if det<1e-8:
   axis=max(range(3),key=lambda q:abs(p.normal[q]));d,e=((1,2),(0,2),(0,1))[axis]
   for li in p.loop_indices:co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(co[d],co[e])
   fixed+=1
 bm=bmesh.new();bm.from_mesh(mesh)
 if kind=='Runestone':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update();mesh.calc_loop_triangles()
 z=min(v.co.z for v in mesh.vertices)
 for v in mesh.vertices:v.co.z-=z
 old.data=mesh;old['WLA_revision']='Art Quality V2';old['WLA_ArtStatus']='V2_review_pending';old['WLA_human_art_approval']=False
 mesh.calc_tangents(uvmap='UV0');badn=sum(x.vector.length<.99 for x in mesh.corner_normals);badt=sum(l.tangent.length<.99 or l.bitangent.length<.99 for l in mesh.loops);badarea=sum(t.area<1e-9 for t in mesh.loop_triangles)
 assert badn==badt==badarea==0,(a['id'],badn,badt,badarea)
 lo=[min(v.co[i] for v in mesh.vertices) for i in range(3)];hi=[max(v.co[i] for v in mesh.vertices) for i in range(3)]
 a.update({'dimensions_m':[hi[i]-lo[i] for i in range(3)],'triangles':len(mesh.loop_triangles),'materials':[m.name for m in mesh.materials],'provenance':'Art V2 revision of existing V1 asset; branch/leaf construction and surface revision','art_status':'V2_review_pending','status':'needs_visual_review','technical_status':'source_tangent_audit_passed'})
 a.pop('technical_caveat',None);audit.append({'id':a['id'],'triangles':a['triangles'],'normal_binormal_errors':0,'uv_repairs':fixed})
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:im.pack()
# Make the review scene active on reopen; export uses source scene explicitly.
bpy.context.window.scene=bpy.data.scenes['WestlandAssetLibrary_Review']
bpy.ops.wm.save_as_mainfile(filepath=str(TARGET));(ART/'Assets.json').write_text(json.dumps(catalog,indent=2)+'\n');(O/'SourceBuild.json').write_text(json.dumps(audit,indent=2)+'\n');print('WLA_V2_SOURCE_SAVED',len(audit))
