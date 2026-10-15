exec(compile(open('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase/Tools/V2/Common.py').read(),'Common.py','exec'))
from mathutils.bvhtree import BVHTree
body=bpy.data.objects['HNV2_Body'];old=bpy.data.objects['HNV2_Waistcoat'];archive([old])
source=(BASE/'Tools/BuildHobbitBase.py').read_text();exec(source[source.index('V=[];F=[];zones=[]'):source.index("body=objmesh('HNB_Body'")]);f=.9844347990514335*.9984350818434603;V=[tuple(Vector(v)*f) for v in V]
fs=[face for face,z in zip(F,zones) if z=='torso' and min(V[i][2] for i in face)>=.685 and max(V[i][2] for i in face)<=1.006]
used=sorted({i for face in fs for i in face});ids={old:i for i,old in enumerate(used)}
mat=bpy.data.materials['HNV2_WalnutWool'];edge=bpy.data.materials['HNV2_WoolBinding'];leather=bpy.data.materials['HNV2_BrownLeather']
o=mesh('Waistcoat',[V[i] for i in used],[[ids[i] for i in face] for face in fs],'HOBBIT_CLOTHING',[mat]);su=o.modifiers.new('TailoredJointCage','SUBSURF');su.levels=1;su.render_levels=1;apply(o,su)
# Use the retained anatomical shoulder holes, avoiding arbitrary patch deletion.
bpy.context.view_layer.update()
for v in o.data.vertices:
 v.co+=v.normal*.025
 x,y,z=v.co
 if .72<z<.89:v.co+=v.normal*(.0018*math.sin(x*26+z*15)*math.exp(-((z-.80)/.09)**2))
def gap(z):
 p=[(.68,.032),(.76,.047),(.85,.067),(.945,.095),(1.005,.070)]
 for a,b in zip(p,p[1:]):
  if a[0]<=z<=b[0]:return a[1]+(b[1]-a[1])*(z-a[0])/(b[0]-a[0])
 return p[-1][1]
bm=bmesh.new();bm.from_mesh(o.data);remove=[]
for face in bm.faces:
 c=face.calc_center_median()
 if c.y<-.020 and abs(c.x)<gap(c.z):remove.append(face)
bmesh.ops.delete(bm,geom=remove,context='FACES');loose=[v for v in bm.verts if not v.link_faces]
if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
# Smooth only the front opening's boundary to remove a staircase edge.
for _ in range(2):
 updates={}
 for v in bm.verts:
  es=[e for e in v.link_edges if e.is_boundary]
  if len(es)==2 and v.co.y<-.02:
   avg=sum((e.other_vert(v).co for e in es),Vector())/2;updates[v]=v.co.lerp(avg,.35)
 for v,co in updates.items():v.co=co
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Actual skin-clearance on the final surface, before adding only a thin lining.
bpy.context.view_layer.update();bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
for iteration in range(3):
 for v in o.data.vertices:
  h,n,index,d=bvh.find_nearest(v.co);signed=(v.co-h).dot(n)
  if signed<.019:v.co+=n*(.019-signed)
# Bind every actual garment boundary; meshes remain exchangeable as one waistcoat object.
bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();bm.verts.index_update();edges=[e for e in bm.edges if e.is_boundary];done=set();loops=[]
for e in edges:
 if e in done:continue
 path=[e.verts[0]];curr=e.verts[0];edge=e
 while edge not in done:
  done.add(edge);curr=edge.other_vert(curr);path.append(curr);nxt=[x for x in curr.link_edges if x.is_boundary and x not in done]
  if not nxt:break
  edge=nxt[0]
 loops.append([tuple(v.co) for v in path])
bm.free();parts=[o]
for i,pts in enumerate(loops):parts.append(tube('TailoredVestBinding_'+str(i),pts,.00115,'HOBBIT_CLOTHING',edge if False else bpy.data.materials['HNV2_WoolBinding'],8))
so=o.modifiers.new('TailoredWoolThickness','SOLIDIFY');so.thickness=.0024;so.offset=-1;apply(o,so)
bpy.context.view_layer.update();vbh=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get())
for i,(z,x) in enumerate([(.746,.066),(.812,.087),(.879,.107)]):
 hit=vbh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)),1)[0]
 if hit:parts.append(sphere('TailoredVestButton_'+str(i),(x,hit.y-.002,z),(.0030,.0014,.0030),'HOBBIT_CLOTHING',leather,16,10))
o=join(parts,'Waistcoat')
# Make the surrounding orbital skin blend into the cheek plane without an outer rim.
for side in ['L','R']:
 oeye=bpy.data.objects['HNV2_OrbitalSkin_'+side];N=64;K=6
 for v in oeye.data.vertices:
  k=v.index//N
  if k==K-1:
   hit=bvh.ray_cast(Vector((v.co.x,-.5,v.co.z)),Vector((0,1,0)),1)[0]
   if hit:v.co.y=hit.y-.00003
 for mod in oeye.modifiers:
  if mod.type=='SOLIDIFY':mod.thickness=.00025;mod.offset=-1
scene['active_version']='V2';scene['production_ready']=False;scene['height_includes_hair']=True;scene['runtime_variant']='not created or imported; separate future retopology/LOD and material bake'
save_stage('06_TailoredVest');bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V2.blend'),{scene});print('Waistcoat rebuilt on the original anatomical shoulder cage',len(o.data.vertices),'boundary bindings',len(loops))
