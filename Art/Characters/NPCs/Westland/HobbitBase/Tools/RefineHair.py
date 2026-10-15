import bpy,math,json,random,bmesh
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');scene=bpy.data.scenes['Hobbit_NPC_Base_V1'];bpy.context.window.scene=scene
cal=json.loads((BASE/'Review/Calibration.json').read_text());scale=cal['calibration_factor'];o=bpy.data.objects['HNB_CurlyHairLocks'];v=[];f=[];mi=[];rng=random.Random(711)
def tube(pts,r,material):
 start=len(v);pts=[Vector(p)*scale for p in pts];r*=scale;S=8
 for i,p in enumerate(pts):
  d=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.1:u=d.cross(Vector((0,1,0)))
  u.normalize();vv=d.cross(u);rr=r*(.5+.5*math.sin(math.pi*i/(len(pts)-1)))
  for j in range(S):v.append(tuple(p+rr*(math.cos(j*math.tau/S)*u+math.sin(j*math.tau/S)*vv)))
 for i in range(len(pts)-1):
  for j in range(S):f.append([start+i*S+j,start+i*S+(j+1)%S,start+(i+1)*S+(j+1)%S,start+(i+1)*S+j]);mi.append(material)
 f.append([start+j for j in reversed(range(S))]);mi.append(material);f.append([start+(len(pts)-1)*S+j for j in range(S)]);mi.append(material)
for row,th in enumerate([.30,.59,.89,1.19,1.49,1.82]):
 for j,ph in enumerate([-.98,-.48,.03,.5,.98,1.31]):
  theta=th+rng.uniform(-.055,.055);phi=ph+rng.uniform(-.075,.075);max_theta=1.70+.48*max(0,math.sin(phi))-.42*max(0,-math.sin(phi))
  if theta>max_theta-.09:continue
  n=Vector((math.cos(phi)*math.sin(theta),math.sin(phi)*math.sin(theta),math.cos(theta))).normalized();c=Vector((.135*n.x,.004+.111*n.y,1.195+.137*n.z));u=Vector((-math.sin(phi),math.cos(phi),0));vv=n.cross(u).normalized();phase=rng.uniform(-math.pi,math.pi);radius=rng.uniform(.010,.016);pts=[]
  for i in range(22):
   t=i/21;a=phase+math.tau*(.62+.06*((row+j)%3))*t;rr=radius*(.4+.6*math.sin(math.pi*t));p=c+rr*(math.cos(a)*u+math.sin(a)*vv)+n*(-.002+.007*math.sin(math.pi*t));pts.append(tuple(p))
  radius_tube=rng.uniform(.0064,.0071)
  for sign in [1,-1]:tube([(sign*x,y,z) for x,y,z in pts],radius_tube,(row+j)%4)
for j in range(3):
 pts=[]
 for i in range(20):
  t=i/19;x=.018+j*.034+.011*math.sin(t*math.tau);pts.append((x,-.088-.010*math.sin(math.pi*t),1.29-.060*t+.007*math.sin(t*math.tau)))
 for sign in [1,-1]:tube([(sign*x,y,z) for x,y,z in pts],.0070,j+1)
me=bpy.data.meshes.new('HNB_CurlyHairLocks_Refined');me.from_pydata(v,[],f);me.update();o.data=me
for i in range(4):me.materials.append(bpy.data.materials['HNB_Hair_'+str(i)])
for p,idx in zip(me.polygons,mi):p.material_index=idx;p.use_smooth=True
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
model=[o for c in scene.collection.children if c.name in ['HOBBIT_BODY','HOBBIT_CLOTHING','HOBBIT_FACE','HOBBIT_HAIR'] for o in c.objects]
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
def limits():
 z=[]
 for o in model:
  e=o.evaluated_get(dg);m=e.to_mesh();z.extend((e.matrix_world@p.co).z for p in m.vertices);e.to_mesh_clear()
 return min(z),max(z)
lo,hi=limits();fix=1.32/(hi-lo)
for o in model:
 for p in o.data.vertices:p.co=(p.co-Vector((0,0,lo)))*fix
 for mod in o.modifiers:
  if mod.type=='SOLIDIFY':mod.thickness*=fix
  elif mod.type=='BEVEL':mod.width*=fix
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();lo,hi=limits();scene['calibrated_height_m']=hi-lo
cal.update(height_m=hi-lo,sole_z_m=lo,top_z_m=hi,hair_refinement_scale=fix);(BASE/'Review/Calibration.json').write_text(json.dumps(cal,indent=2))
bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V1.blend'),{scene})
print(json.dumps({'height_m':hi-lo,'hair_vertices':len(me.vertices),'source_saved':True}))
