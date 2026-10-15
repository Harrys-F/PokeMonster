"""Original Blender-built Westland adult hobbit base. No imports, rig or animation."""
import bpy, bmesh, math, json
from mathutils import Vector
from pathlib import Path
BASE=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
assert not bpy.data.scenes.get('Hobbit_NPC_Base_V1'), 'Existing working scene must be inspected before rebuilding'
old_scene=bpy.context.scene
scene=bpy.data.scenes.new('Hobbit_NPC_Base_V1')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.0;scene.unit_settings.length_unit='METERS'
cols={}
for name in ['HOBBIT_BODY','HOBBIT_CLOTHING','HOBBIT_FACE','HOBBIT_HAIR','PREVIEW_STAGE','MODEL_WORK']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);cols[name]=c

def mat(name,c,rough=.7):
 m=bpy.data.materials.new('HNB_'+name);m.diffuse_color=(*c,1);m.use_nodes=True
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough
 return m
skin=mat('Skin',(0.54,.30,.18));linen=mat('Linen',(.66,.59,.44));vest=mat('Vest',(.14,.062,.024));pants=mat('Olive',(.18,.195,.085));leather=mat('Leather',(.075,.034,.015));brass=mat('Brass',(.36,.23,.075),.43);white=mat('Eyes',(.76,.71,.59),.4);iris=mat('Iris',(.095,.043,.015),.4);black=mat('Pupil',(.008,.006,.004),.3);lip=mat('Smile',(.24,.075,.048));hairmats=[mat('Hair_'+str(i),(.054+i*.009,.021+i*.004,.009+i*.002)) for i in range(4)]

def objmesh(name,verts,faces,col,material):
 me=bpy.data.meshes.new(name+'_Mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);cols[col].objects.link(o)
 if material:me.materials.append(material)
 bm=bmesh.new();bm.from_mesh(me);loose=[v for v in bm.verts if not v.link_edges]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 return o

def activate(o):
 for q in scene.objects:q.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o

def apply(o,m):activate(o);bpy.ops.object.modifier_apply(modifier=m.name)

def sphere(name,loc,scale,col,material,segments=20,rings=14):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
 o=bpy.context.object;o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 cols[col].objects.link(o);o.scale=scale;activate(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

V=[];F=[];zones=[]
def vert(v):V.append(v);return len(V)-1

def face(ids,zone):F.append(ids);zones.append(zone)
def ring(points):return [vert(tuple(p)) for p in points]
def bridge(a,b,zone):
 assert len(a)==len(b)
 for j in range(len(a)):face([a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]],zone)
def cap(a,zone):face(list(reversed(a)),zone)
N=32
sections=[(.58,.165,.095,0),(.65,.18,.11,-.012),(.70,.185,.135,-.02),(.78,.183,.145,-.027),(.86,.175,.12,-.012),(.90,.185,.105,0),(.925,.193,.098,0),(.95,.198,.092,0),(.975,.19,.082,0),(1.0,.165,.073,0),(1.023,.10,.062,0),(1.052,.05,.045,0),(1.075,.05,.045,0),(1.09,.075,.070,-.006),(1.105,.088,.077,-.014),(1.125,.102,.086,-.015),(1.155,.118,.091,-.004),(1.19,.123,.094,0),(1.225,.121,.092,0),(1.26,.108,.082,.003),(1.282,.085,.065,.005),(1.30,.035,.03,.006)]
rings=[]
for z,rx,ry,cy in sections:
 rings.append(ring([(rx*math.cos(j*math.tau/N),cy+ry*math.sin(j*math.tau/N),z) for j in range(N)]))
# True shoulder openings: the arms bridge these borders instead of overlapping pieces.
for i in range(len(rings)-1):
 for j in range(N):
  if 5<=i<9 and any((j-centre)%N in [29,30,31,0,1,2] for centre in [0,16]):continue
  face([rings[i][j],rings[i][(j+1)%N],rings[i+1][(j+1)%N],rings[i+1][j]],'torso' if i<11 else 'head')
cap(rings[-1],'head')
shoulder_borders={}
for sign,centre in [(1,0),(-1,16)]:
 js=[(centre+j)%N for j in range(-3,4)]
 border=[rings[5][j] for j in js]+[rings[i][js[-1]] for i in range(6,10)]+[rings[9][j] for j in js[-2::-1]]+[rings[i][js[0]] for i in range(8,5,-1)]
 assert len(border)==20
 border.sort(key=lambda idx:math.atan2(V[idx][2]-.95,V[idx][1]))
 shoulder_borders[sign]=border
 angles=[math.atan2(V[idx][2]-.95,V[idx][1]) for idx in border]
 prev=border
 for x,ry,rz in [(.225,.055,.058),(.27,.055,.058),(.33,.051,.052),(.405,.046,.047),(.428,.044,.046),(.45,.044,.045),(.48,.045,.043),(.56,.037,.035),(.615,.029,.027),(.64,.029,.025),(.665,.035,.023),(.69,.045,.024),(.715,.044,.022),(.742,.034,.019)]:
  rr=ring([(sign*x,ry*math.cos(a),.95+rz*math.sin(a)) for a in angles]);bridge(prev,rr,'arm' if x<.65 else 'hand');prev=rr
 cap(prev,'hand')
# A shared crotch seam splits the torso border into two connected leg sockets.
crotch=[vert((0,.050,.548)),vert((0,0,.53)),vert((0,-.050,.548))]
for sign in [1,-1]:
 arc=[rings[0][j%N] for j in (range(24,41) if sign==1 else range(8,25))]
 border=arc+(crotch if sign==1 else list(reversed(crotch)))
 angles=[math.atan2(V[idx][1],V[idx][0]-sign*.105) for idx in border];order=sorted(range(20),key=lambda j:angles[j]);border=[border[j] for j in order];angles=[angles[j] for j in order];prev=border
 for z,cx,rx,ry,cy in [(.52,.105,.079,.083,0),(.48,.105,.080,.084,0),(.40,.107,.071,.075,0),(.325,.11,.06,.06,0),(.305,.11,.058,.057,-.003),(.28,.112,.057,.055,0),(.245,.114,.061,.058,.005),(.19,.114,.054,.055,.005),(.125,.114,.038,.041,.003),(.105,.114,.036,.040,0),(.080,.114,.052,.081,-.015),(.055,.114,.074,.126,-.04),(.022,.114,.071,.13,-.045),(0,.114,.06,.11,-.039)]:
  rr=ring([(sign*cx+rx*math.cos(a),cy+ry*math.sin(a),z) for a in angles]);bridge(prev,rr,'leg' if z>.105 else 'foot');prev=rr
 cap(prev,'foot')
body=objmesh('HNB_Body',V,F,'HOBBIT_BODY',skin)
# Store the authored joint-ring cage separately as a mesh datablock for future retopology.
body['anatomy']='one head, one torso, two arms/hands/legs/feet; five digits per hand and foot'
body['pose']='T-pose; arms straight on shoulder axis; no rig'
body['joint_loops']='shoulder sockets, elbow support rings, wrists, pelvis, knees, ankles'
# Garments derive from the same surface, with clear separate object boundaries.
def garment(name,condition,material,offset):
 fs=[f for f,z in zip(F,zones) if condition(f,z)]
 used=sorted({i for f in fs for i in f});ids={old:i for i,old in enumerate(used)}
 o=objmesh(name,[V[i] for i in used],[[ids[i] for i in f] for f in fs],'HOBBIT_CLOTHING',material)
 # A small normal offset avoids intersections without changing the anatomy.
 o.data.update()
 for v in o.data.vertices:v.co+=v.normal*offset
 s=o.modifiers.new('GarmentSurface','SUBSURF');s.levels=1;s.render_levels=1
 so=o.modifiers.new('FabricThickness','SOLIDIFY');so.thickness=.003;so.offset=0
 return o
shirt=garment('HNB_Shirt',lambda f,z:z in ['torso','arm'],linen,.011)
waistcoat=garment('HNB_Waistcoat',lambda f,z:z=='torso' and min(V[i][2] for i in f)>=.70 and not all(V[i][1]<-.05 and abs(V[i][0])<.045 for i in f),vest,.024)
# Loose breeches use a dedicated continuous waist/crotch/leg shell.
vp=[];fp=[]
for z,rx,ry,cy in [(.72,.199,.15,-.02),(.665,.195,.129,-.012),(.59,.185,.118,0)]:
 vp.extend([(rx*math.cos(j*math.tau/32),cy+ry*math.sin(j*math.tau/32),z) for j in range(32)])
for k in range(2):
 for j in range(32):fp.append([k*32+j,k*32+(j+1)%32,(k+1)*32+(j+1)%32,(k+1)*32+j])
ci=[]
for y in [.06,0,-.06]:ci.append(len(vp));vp.append((0,y,.54))
for sign in [1,-1]:
 border=[64+j%32 for j in (range(24,41) if sign==1 else range(8,25))]+(ci if sign==1 else list(reversed(ci)))
 aa=[math.atan2(vp[i][1],vp[i][0]-sign*.106) for i in border];ix=sorted(range(20),key=lambda j:aa[j]);border=[border[i] for i in ix];aa=[aa[i] for i in ix];prev=border
 for z,rx,ry in [(.515,.099,.1),(.445,.103,.105),(.365,.094,.096),(.325,.082,.077),(.295,.069,.067),(.283,.066,.063)]:
  rr=[]
  for a in aa:rr.append(len(vp));vp.append((sign*.11+rx*math.cos(a),ry*math.sin(a),z))
  for j in range(20):fp.append([prev[j],prev[(j+1)%20],rr[(j+1)%20],rr[j]])
  prev=rr
breeches=objmesh('HNB_Breeches',vp,fp,'HOBBIT_CLOTHING',pants);su=breeches.modifiers.new('BreechesSurface','SUBSURF');su.levels=1;su.render_levels=1;so=breeches.modifiers.new('FabricThickness','SOLIDIFY');so.thickness=.003
# Anatomical fingers/toes are merged into the skin body, not extra limbs.
def capsule(name,start,end,r):
 a=Vector(start);b=Vector(end);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
 if u.length<.1:u=d.cross(Vector((0,1,0)))
 u.normalize();v=d.cross(u);points=[];faces=[]
 for t,s in [(0,.16),(.10,.74),(.24,1),(.72,.97),(.90,.7),(1,.12)]:
  c=a.lerp(b,t)
  for j in range(12):points.append(tuple(c+r*s*(math.cos(j*math.tau/12)*u+math.sin(j*math.tau/12)*v)))
 for i in range(5):
  for j in range(12):faces.append([i*12+j,i*12+(j+1)%12,(i+1)*12+(j+1)%12,(i+1)*12+j])
 faces.extend([list(reversed(list(range(12)))),list(range(60,72))]);return objmesh(name,points,faces,'MODEL_WORK',skin)
def unite(o):
 m=body.modifiers.new('AnatomicalUnion','BOOLEAN');m.operation='UNION';m.solver='EXACT';m.object=o;apply(body,m);bpy.data.objects.remove(o,do_unlink=True)
for sign,side in [(1,'L'),(-1,'R')]:
 for i,(yy,length,rr) in enumerate([(-.032,.060,.011),(-.011,.078,.012),(.013,.07,.011),(.034,.053,.0095)]):unite(capsule('HNB_Finger_'+side+'_'+str(i+1),(sign*.720,yy,.95),(sign*(.731+length),yy,.946),rr))
 unite(capsule('HNB_Thumb_'+side,(sign*.681,-.029,.95),(sign*.739,-.063,.94),.014))
 for i,(xx,ty,rr) in enumerate([(-.048,-.238,.019),(-.022,-.246,.017),(.003,-.237,.015),(.026,-.225,.013),(.047,-.208,.012)]):
  unite(capsule('HNB_Toe_'+side+'_'+str(i+1),(sign*(.114+xx),-.127,.043),(sign*(.114+xx),ty,.042),rr))
for sign,side in [(1,'L'),(-1,'R')]:unite(sphere('HNB_Ear_'+side,(sign*.123,.003,1.184),(.022,.025,.037),'MODEL_WORK',skin,16,12))
unite(sphere('HNB_Nose',(0,-.092,1.172),(.023,.023,.026),'MODEL_WORK',skin,16,12))
# Apply one surface subdivision after the anatomy merges; no automated rigging.
su=body.modifiers.new('BodySurface','SUBSURF');su.levels=1;su.render_levels=1;apply(body,su)
# Final recalc and numeric manifold check, not a claim of finished facial retopology.
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
for p in body.data.polygons:p.use_smooth=True
BASE.joinpath('Review','BodyStage.json').write_text(json.dumps({'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons),'scene':scene.name,'next':'face, hair, belt and calibration'},indent=2))
# Preview studio is confined to its own collection and does not affect model dimensions.
world=bpy.data.worlds.new('HNB_PreviewWorld');scene.world=world;world.use_nodes=True
next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Color'].default_value=(.11,.13,.15,1)
next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.45
floor=objmesh('HNB_PreviewFloor',[(-12,-12,-.009),(12,-12,-.009),(12,12,-.009),(-12,12,-.009)],[(0,1,2,3)],'PREVIEW_STAGE',mat('Floor',(.19,.205,.19)))
for name,loc,power,size in [('Key',(-2.3,-3.5,4.2),420,3),('Fill',(2.8,-1.0,2.8),190,2.5),('Rim',(0,2.5,3.8),330,2)]:
 ld=bpy.data.lights.new('HNB_'+name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size;o=bpy.data.objects.new(ld.name,ld);cols['PREVIEW_STAGE'].objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.7))-o.location).to_track_quat('-Z','Y').to_euler()
cd=bpy.data.cameras.new('HNB_PreviewCamera');camera=bpy.data.objects.new(cd.name,cd);cols['PREVIEW_STAGE'].objects.link(camera);camera.location=(0,-4,.75);camera.rotation_euler=(Vector((0,0,.66))-camera.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=1.95;scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1024;scene.render.resolution_y=1024;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene['model_scope']='Original Blender geometry only; no imported or generated models; no rig/animation'
# Preserve the original live scene and its objects. Write only the new scene graph.
activate(body)
bpy.data.libraries.write(str(BASE/'Source/Hobbit_NPC_BodyStage_V1.blend'),{scene})
print(json.dumps({'scene':scene.name,'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons),'original_scene_untouched':old_scene.name,'objects':len(scene.objects)}))
