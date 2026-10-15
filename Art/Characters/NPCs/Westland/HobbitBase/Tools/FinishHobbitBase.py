"""Finish the scoped Blender body with a simple adult face, curls and belt."""
import bpy,math,json,bmesh
from pathlib import Path
from mathutils import Vector
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
scene=bpy.data.scenes['Hobbit_NPC_Base_V1'];bpy.context.window.scene=scene
cols={c.name:c for c in scene.collection.children};body=bpy.data.objects['HNB_Body'];skin=bpy.data.materials['HNB_Skin'];hairmats=[bpy.data.materials['HNB_Hair_'+str(i)] for i in range(4)]
assert not bpy.data.objects.get('HNB_HairCore'), 'Finish stage has already run; inspect before editing'

def mesh(name,v,f,col,material):
 me=bpy.data.meshes.new(name+'_Mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);cols[col].objects.link(o);me.materials.append(material)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 return o

def activate(o):
 for q in scene.objects:q.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o

def ellipsoid(name,loc,size,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=14,location=loc);o=bpy.context.object;o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 cols['HOBBIT_FACE'].objects.link(o);o.scale=size;activate(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def tube(name,points,radius,material,col='HOBBIT_FACE',sides=8):
 v=[];f=[];points=[Vector(p) for p in points]
 for i,p in enumerate(points):
  d=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.1:u=d.cross(Vector((0,1,0)))
  u.normalize();vv=d.cross(u);r=radius*(.65+.35*math.sin(math.pi*i/(len(points)-1)))
  for j in range(sides):v.append(tuple(p+r*(u*math.cos(j*math.tau/sides)+vv*math.sin(j*math.tau/sides))))
 for i in range(len(points)-1):
  for j in range(sides):f.append([i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j])
 f.extend([list(reversed(list(range(sides)))),list(range((len(points)-1)*sides,len(points)*sides))]);return mesh(name,v,f,col,material)
for sign,side in [(1,'L'),(-1,'R')]:
 ellipsoid('HNB_Eye_'+side,(sign*.049,-.083,1.195),(.019,.010,.012),bpy.data.materials['HNB_Eyes'])
 ellipsoid('HNB_Iris_'+side,(sign*.049,-.0930,1.195),(.0082,.0015,.0082),bpy.data.materials['HNB_Iris'])
 ellipsoid('HNB_Pupil_'+side,(sign*.049,-.0943,1.195),(.0044,.0007,.0047),bpy.data.materials['HNB_Pupil'])
 # Eyelids partly cover the eye to avoid an oversized, childlike expression.
 pts=[]
 for i in range(13):
  a=math.pi*i/12;x=.049+.019*math.cos(a);pts.append((sign*x,-.089+(.005*abs(x-.049)/.019),1.195+.0115*math.sin(a)))
 tube('HNB_UpperLid_'+side,pts,.0018,skin)
 pts=[(sign*x,-.083- .007*math.sin(math.pi*t),1.216+.006*math.sin(math.pi*t)) for t,x in [(i/12,.029+.043*i/12) for i in range(13)]]
 tube('HNB_Brow_'+side,pts,.0036,hairmats[0])
smile=[]
for i in range(21):
 t=i/20;x=(t-.5)*.060;smile.append((x,-.095+.008*(x/.03)**2,1.144+.006*(x/.03)**2))
tube('HNB_GentleSmile',smile,.0018,bpy.data.materials['HNB_Smile'])
# An irregular cap plus curved locks, not sphere-clump hair. Exact mirrored pairs.
v=[];f=[];N=64;K=18
for k in range(K+1):
 t=k/K
 for j in range(N):
  phi=math.tau*j/N;s=math.sin(phi);max_theta=1.70+.48*max(0,s)-.42*max(0,-s);theta=(.025+.975*t)*max_theta
  wave=1+.023*math.cos(4*phi)*math.sin(theta)**2+.017*math.cos(2*phi)*math.sin(5*theta)
  v.append((.136*math.cos(phi)*math.sin(theta)*wave,.004+.110*math.sin(phi)*math.sin(theta)*wave,1.195+.137*math.cos(theta)*wave))
for k in range(K):
 for j in range(N):f.append([k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j])
f.append(list(reversed(list(range(N)))))
core=mesh('HNB_HairCore',v,f,'HOBBIT_HAIR',hairmats[1]);so=core.modifiers.new('HairCapThickness','SOLIDIFY');so.thickness=.004;so.offset=-1
locks=[]
for row,theta in enumerate([.32,.62,.92,1.22,1.52,1.85]):
 for j,phi in enumerate([-.95,-.48,0,.48,.95,1.32]):
  max_theta=1.70+.48*max(0,math.sin(phi))-.42*max(0,-math.sin(phi))
  if theta>max_theta-.10:continue
  n=Vector((math.cos(phi)*math.sin(theta),math.sin(phi)*math.sin(theta),math.cos(theta))).normalized();c=Vector((.139*n.x,.004+.114*n.y,1.195+.141*n.z));u=Vector((-math.sin(phi),math.cos(phi),0));vv=n.cross(u).normalized()
  pts=[];radius=.014+.003*((row+j)%3)
  for i in range(25):
   t=i/24;a=math.tau*1.1*t+(j+row)*.3;rr=radius*(.35+.65*math.sin(math.pi*t));p=c+rr*(math.cos(a)*u+math.sin(a)*vv)+n*(.003+.002*math.sin(2*a));pts.append(tuple(p))
  for sign,side in [(1,'L'),(-1,'R')]:locks.append(tube('HNB_Curl_'+side+'_'+str(row)+'_'+str(j),[(sign*x,y,z) for x,y,z in pts],.0055,hairmats[(row+j)%4],'HOBBIT_HAIR',8))
# A few forehead locks form a softer, less regular hairline.
for j in range(3):
 pts=[]
 for i in range(20):
  t=i/19;x=.018+j*.034+.013*math.sin(t*math.tau);y=-.090-.018*math.sin(math.pi*t);z=1.29-.060*t+.008*math.sin(t*math.tau);pts.append((x,y,z))
 for sign,side in [(1,'L'),(-1,'R')]:locks.append(tube('HNB_Fringe_'+side+'_'+str(j),[(sign*x,y,z) for x,y,z in pts],.0065,hairmats[j+1],'HOBBIT_HAIR',8))
# Consolidate strands into one editable hair object with a small shared material family.
for o in scene.objects:o.select_set(False)
for o in locks:o.select_set(True)
bpy.context.view_layer.objects.active=locks[0];bpy.ops.object.join();locks[0].name='HNB_CurlyHairLocks'
# Belt: a genuine small band with thickness, rather than a painted torso stripe.
v=[];f=[];N=64
for z,rx,ry in [(.696,.212,.173),(.731,.212,.173),(.696,.207,.168),(.731,.207,.168)]:
 for j in range(N):v.append((rx*math.cos(j*math.tau/N),-.021+ry*math.sin(j*math.tau/N),z))
for a,b in [(0,1),(1,3),(3,2),(2,0)]:
 for j in range(N):f.append([a*N+j,a*N+(j+1)%N,b*N+(j+1)%N,b*N+j])
belt=mesh('HNB_Belt',v,f,'HOBBIT_CLOTHING',bpy.data.materials['HNB_Leather'])
# A simple rectangular buckle assembled as one mesh.
v=[];f=[]
for cx,cz,sx,sz in [(-.019,.7135,.006,.040),(.019,.7135,.006,.040),(0,.7305,.037,.006),(0,.6965,.037,.006),(0,.7135,.003,.032)]:
 start=len(v)
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:v.append((cx+x*sx/2,-.198+y*.003,cz+z*sz/2))
 f.extend([[start+i for i in ff] for ff in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]])
buckle=mesh('HNB_Buckle',v,f,'HOBBIT_CLOTHING',bpy.data.materials['HNB_Brass']);be=buckle.modifiers.new('SoftBuckleEdges','BEVEL');be.width=.001;be.segments=2
# Calibration includes evaluated clothes/hair; soles are the actual bottom of the body.
model_cols=[cols[k] for k in ['HOBBIT_BODY','HOBBIT_CLOTHING','HOBBIT_FACE','HOBBIT_HAIR']]
model=[o for c in model_cols for o in c.objects]
dg=bpy.context.evaluated_depsgraph_get()
def extents():
 z=[]
 for o in model:
  e=o.evaluated_get(dg);me=e.to_mesh();z.extend((e.matrix_world@v.co).z for v in me.vertices);e.to_mesh_clear()
 return min(z),max(z)
lo,hi=extents();factor=1.32/(hi-lo)
for o in model:
 for v in o.data.vertices:v.co=(o.matrix_world@v.co-Vector((0,0,lo)))*factor
 o.matrix_world.identity()
 # Length-based modifiers must scale with the calibrated anatomy too.
 for m in o.modifiers:
  if m.type=='SOLIDIFY':m.thickness*=factor
  elif m.type=='BEVEL':m.width*=factor
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();lo2,hi2=extents()
# Tiny evaluated modifier differences are corrected without altering the pose.
for _ in range(3):
 if abs((hi2-lo2)-1.32)<1e-7 and abs(lo2)<1e-7:break
 fix=1.32/(hi2-lo2)
 for o in model:
  for v in o.data.vertices:v.co=(v.co-Vector((0,0,lo2)))*fix
  for m in o.modifiers:
   if m.type=='SOLIDIFY':m.thickness*=fix
   elif m.type=='BEVEL':m.width*=fix
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();lo2,hi2=extents()
body['height_m']=1.32;body['variant_height_range_m']=[1.20,1.45];body['toes_per_foot']=5;body['fingers_per_hand']=5;body['side_count']=2
scene['height_definition']='Visible geometry: foot sole to uppermost hair curl, evaluated in metres'
scene['calibrated_height_m']=hi2-lo2
scene['future_work']='No rig, skin weights, walk/run or Unreal export in NPC base stage; joint deformation tests pending'
activate(body)
for a in scene.screen.areas if hasattr(scene,'screen') else []:pass
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.region_3d.view_location=(0,0,.66);area.spaces.active.region_3d.view_distance=2.7
bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_Base_V1.blend'),{scene})
(BASE/'Review/Calibration.json').write_text(json.dumps({'height_m':hi2-lo2,'sole_z_m':lo2,'top_z_m':hi2,'calibration_factor':factor,'model_objects':[o.name for o in model],'blender_version':bpy.app.version_string,'no_armatures':not any(o.type=='ARMATURE' for o in scene.objects),'actions_in_scene':sum(bool(o.animation_data and o.animation_data.action) for o in scene.objects)},indent=2))
print(json.dumps({'saved':str(BASE/'Source/Hobbit_NPC_Base_V1.blend'),'height_m':hi2-lo2,'sole_z_m':lo2,'top_z_m':hi2,'model_objects':len(model)}))
