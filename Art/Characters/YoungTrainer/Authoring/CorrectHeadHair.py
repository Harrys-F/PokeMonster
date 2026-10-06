"""Head/face/hair only, from preserved Proportions V2. No rig or UV work."""
import bpy,bmesh,math,json,random
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/YoungTrainer')
assert Path(bpy.data.filepath).name=='YoungTrainer_Proportions_V2.blend'
scene=bpy.data.scenes['YoungTrainer_Reference_V1'];bpy.context.window.scene=scene
root=bpy.data.objects['YT_CharacterRoot'];old=bpy.data.collections['YT_Character']
archive=bpy.data.collections.new('YT_HeadHair_Source_V2');scene.collection.children.link(archive)
for name in ['YT_Head','YT_Eyes','YT_Face','YT_Hair']:
 o=bpy.data.objects[name];archive.objects.link(o);old.objects.unlink(o)
archive.hide_render=True;archive.hide_viewport=True
coll=bpy.data.collections.new('YT_HeadHair_V3');scene.collection.children.link(coll)
M={}
colors={'Skin':(.72,.43,.26,1),'SkinSoft':(.63,.32,.20,1),'Hair':(.055,.025,.013,1),
 'HairWarm':(.072,.033,.017,1),'HairDeep':(.039,.017,.010,1),'White':(.88,.84,.73,1),
 'Iris':(.21,.081,.023,1),'IrisWarm':(.30,.13,.037,1),'Pupil':(.008,.004,.002,1),
 'Glint':(.98,.95,.85,1),'Mouth':(.19,.066,.039,1),'Brow':(.045,.018,.009,1)}
for name,color in colors.items():
 m=bpy.data.materials.new('YT3_Preview_'+name);m.use_nodes=True;m.diffuse_color=color
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.68
 M[name]=m
def mesh(name,verts,faces,mat):
 data=bpy.data.meshes.new('YT3_'+name);data.from_pydata(verts,[],faces);data.update()
 bm=bmesh.new();bm.from_mesh(data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free()
 o=bpy.data.objects.new('YT3_'+name,data);coll.objects.link(o);o.parent=root;o.data.materials.append(M[mat])
 for p in data.polygons:p.use_smooth=True
 o['pass']='HeadHair V3, static modelling only; no new rig/weights/animation.'
 return o
def catmull(points,sub=5):
 ps=[Vector(p) for p in points];out=[]
 for i in range(len(ps)-1):
  a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)]
  for j in range(sub):
   t=j/sub;out.append((b*2+(-a+c)*t+(a*2-b*5+c*4-d)*t*t+(-a+b*3-c*3+d)*t*t*t)*.5)
 out.append(ps[-1]);return out
def tube(name,controls,widths,mat='Hair',depth=.72,sides=12,sub=5):
 ps=catmull(controls,sub);vs=[];fs=[];previous_tangent=None;previous_normal=None
 for i,p in enumerate(ps):
  tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
  radial=(p-Vector((0,.020,1.245))).normalized()
  if previous_normal is None:
   normal=(radial-tangent*radial.dot(tangent)).normalized()
   if normal.length<.01:normal=tangent.cross(Vector((0,1,0))).normalized()
  else:
   normal=previous_tangent.rotation_difference(tangent)@previous_normal
   normal=(normal-tangent*normal.dot(tangent)).normalized()
  previous_tangent=tangent;previous_normal=normal
  lateral=tangent.cross(normal).normalized()
  t=i/(len(ps)-1)*(len(widths)-1);j=min(len(widths)-2,int(t));w=widths[j]+(widths[j+1]-widths[j])*(t-j)
  for k in range(sides):
   a=math.tau*k/sides;vs.append(tuple(p+lateral*(math.cos(a)*w)+normal*(math.sin(a)*w*depth)))
 for i in range(len(ps)-1):
  for k in range(sides):fs.append((i*sides+k,i*sides+(k+1)%sides,(i+1)*sides+(k+1)%sides,(i+1)*sides+k))
 for idx,flip in [(0,True),(len(ps)-1,False)]:
  pole=len(vs);vs.append(tuple(ps[idx]))
  for k in range(sides):fs.append((pole,idx*sides+(k+1)%sides,idx*sides+k) if flip else (pole,idx*sides+k,idx*sides+(k+1)%sides))
 return mesh(name,vs,fs,mat)
def radius(z):
 t=max(-1,min(1,(z-1.198)/.134));return .145*math.sqrt(max(.001,1-t*t))*(1-.12*max(0,-t))
def surface(x,z):
 ry=.104*math.sqrt(max(.08,1-((z-1.20)/.153)**2))
 y=-.004-ry*math.sqrt(max(.04,1-(x/max(.015,radius(z)))**2))
 # Broad cheek volume, short small nose, no realistic nasal bridge.
 y-=.009*math.exp(-((abs(x)-.080)/.045)**2-((z-1.143)/.040)**2)
 y-=.020*math.exp(-(x/.013)**2-((z-1.146)/.012)**2)
 return y
def chart(u,v):
 x=.145*u*math.sqrt(1-v*v/2)*(1-.10*max(0,-v))
 z=1.198+.134*v*math.sqrt(1-u*u/2)
 return Vector((x,surface(x,z),z))
# Quad facial patch, explicit orbital/mouth annuli, and rounded rear skull.
NX=32;NZ=36;vs=[];fs=[];grid={}
for j in range(NZ+1):
 for i in range(NX+1):grid[i,j]=len(vs);vs.append(tuple(chart(-1+2*i/NX,-1+2*j/NZ)))
features=[('EyeR',4,14,12,22,-.056,1.187,.029,.030),
 ('EyeL',18,28,12,22,.056,1.187,.029,.030),('Mouth',13,19,4,8,0,1.111,.021,.0020)]
for j in range(NZ):
 for i in range(NX):
  if any(a<=i<b and c<=j<d for _,a,b,c,d,*rest in features):continue
  fs.append((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
loop_groups={}
for name,a,b,c,d,cx,cz,rx,rz in features:
 perimeter=([grid[i,c] for i in range(a,b)]+[grid[b,j] for j in range(c,d)]+
            [grid[i,d] for i in range(b,a,-1)]+[grid[a,j] for j in range(d,c,-1)])
 n=len(perimeter);previous=perimeter;loops=[]
 # Parameter follows the rectangular contour, retaining predictable quad flow.
 for size,rise in ([(1.18,1.15),(1.08,1.08),(1.025,1.025),(1.0,1.0)] if name.startswith('Eye') else [(1.08,5.0),(1.05,3.0),(1.025,1.6),(1.0,1.0)]):
  ids=[]
  for k,idx in enumerate(perimeter):
   p=Vector(vs[idx]);angle=math.atan2((p.z-cz)/(.036 if name.startswith('Eye') else .015),(p.x-cx)/(.040 if name.startswith('Eye') else .030))
   x=cx+rx*size*math.cos(angle);z=cz+rz*rise*math.sin(angle)
   if name.startswith('Eye'):
    z=cz+(z-cz)*(.55+.45*math.sin(angle)**2)
    if math.sin(angle)<0:z=cz+(z-cz)*.88
    z+=.0018*((x-cx)/(rx*size))*(1 if cx>0 else -1)
   else:z+=.002*(abs(x-cx)/(rx*size))**2
   ids.append(len(vs));vs.append((x,surface(x,z)-.0006,z))
  for k in range(n):fs.append((previous[k],previous[(k+1)%n],ids[(k+1)%n],ids[k]))
  loops.append(ids);previous=ids
 loop_groups[name]=loops
outer=([grid[i,0] for i in range(NX)]+[grid[NX,j] for j in range(NZ)]+
 [grid[i,NZ] for i in range(NX,0,-1)]+[grid[0,j] for j in range(NZ,0,-1)])
prev=outer
for ring in range(1,9):
 a=(math.pi/2)*ring/9;ids=[]
 for idx in outer:
  p=Vector(vs[idx]);ids.append(len(vs));vs.append((p.x*math.cos(a),.012+.120*math.sin(a),1.198+(p.z-1.198)*math.cos(a)))
 for k in range(len(ids)):fs.append((prev[k],prev[(k+1)%len(ids)],ids[(k+1)%len(ids)],ids[k]))
 prev=ids
pole=len(vs);vs.append((0,.132,1.198))
for k in range(len(prev)):fs.append((prev[k],prev[(k+1)%len(prev)],pole))
# Drop the unused grid interior of the reserved holes; never leave loose points.
used=sorted({v for f in fs for v in f});remap={v:i for i,v in enumerate(used)}
head=mesh('Head', [vs[i] for i in used], [tuple(remap[i] for i in f) for f in fs], 'Skin')
for name,loops in loop_groups.items():
 group=head.vertex_groups.new(name='Topology_'+name)
 group.add([remap[i] for loop in loops for i in loop],1,'REPLACE')
head['topology']='Continuous quad facial patch; 4 orbital and oral support loops; 3 intentional openings, rounded skull; no facial rig.'
head['facial_loops_json']=json.dumps({name:[len(ring) for ring in loops] for name,loops in loop_groups.items()})
sub=head.modifiers.new('Face smoothing preview','SUBSURF');sub.levels=1;sub.render_levels=1
def eye_shape(s,a,rx=.029,rz=.029):
 x=s*.056+rx*math.cos(a);z=1.187+rz*math.sin(a)*(.55+.45*math.sin(a)**2)*(1 if math.sin(a)>0 else .88)+.0018*math.cos(a)*s
 return x,z
def disc(name,cx,cz,rx,rz,mat,depth,bulge=0,segments=40,rings=6,eye=False):
 vs=[];fs=[]
 vs.append((cx,surface(cx,cz)-depth-bulge,cz))
 for j in range(1,rings+1):
  r=j/rings
  for k in range(segments):
   a=math.tau*k/segments;x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a)
   if eye:
    z=cz+(z-cz)*(.55+.45*math.sin(a)**2)
    if math.sin(a)<0:z=cz+(z-cz)*.88
    z+=.0018*r*math.cos(a)*(1 if cx>0 else -1)
   vs.append((x,surface(x,z)-depth-bulge*math.sqrt(max(0,1-r*r)),z))
 for k in range(segments):fs.append((0,1+k,1+(k+1)%segments))
 for j in range(rings-1):
  for k in range(segments):
   a=1+j*segments+k;b=1+j*segments+(k+1)%segments;c=1+(j+1)*segments+(k+1)%segments;d=1+(j+1)*segments+k;fs.append((a,b,c,d))
 return mesh(name,vs,fs,mat)
for s,label in [(-1,'R'),(1,'L')]:
 disc('EyeWhite_'+label,s*.056,1.187,.0294,.0303,'White',.0008,.004,eye=True)
 disc('Iris_'+label,s*.056,1.187,.0205,.0220,'Iris',.0055,.0015)
 disc('IrisWarm_'+label,s*.056,1.179,.012,.006,'IrisWarm',.0071,.0001,rings=3)
 disc('Pupil_'+label,s*.056,1.190,.0095,.014,'Pupil',.0078,.0003)
 disc('EyeGlint_'+label,s*.056-.007,1.200,.0045,.0050,'Glint',.009,.0002,rings=3)
 disc('EyeGlintSmall_'+label,s*.056+.006,1.178,.0018,.002,'Glint',.009,.0001,rings=2)
 upper=[];lower=[]
 for k in range(13):
  a=math.pi*k/12;x,z=eye_shape(s,a);upper.append((x,surface(x,z)-.0025,z))
  a=math.pi+math.pi*k/12;x,z=eye_shape(s,a);lower.append((x,surface(x,z)-.0018,z))
 tube('UpperLid_'+label,upper,[.0018,.0024,.0024,.0018],'Brow',.75,8,2)
 tube('LowerLid_'+label,lower,[.0016,.0022,.0022,.0016],'SkinSoft',.75,8,2)
 brow=[]
 for k in range(7):
  t=k/6;x=s*.056+(t-.5)*.057;z=1.227+.006*math.sin(t*math.pi)+s*(t-.5)*.002
  brow.append((x,surface(x,z)-.003,z))
 tube('Brow_'+label,brow,[.0028,.0045,.0045,.0025],'Brow',.65,10,3)
mouth=[]
for k in range(9):
 t=k/8;x=(t-.5)*.041;z=1.111+.002*(abs(t-.5)*2)**2;mouth.append((x,surface(x,z)-.0018,z))
tube('MouthLine',mouth,[.0011,.0016,.0016,.0010],'Mouth',.6,8,3)
disc('MouthCavity',0,1.112,.021,.0032,'Mouth',-.0004,0,rings=3)
# Existing ears only: a relative correction key; all non-ear body vertices remain identical.
body=bpy.data.objects['YT_Body'];current=body.data.shape_keys.key_blocks['Proportions_Silhouette_V2']
earkey=body.shape_key_add(name='HeadHair_V3_EarsOnly',from_mix=False);earkey.relative_key=current
ear_ids=[]
for v,d in zip(body.data.vertices,earkey.data):
 p=current.data[v.index].co.copy();groups={body.vertex_groups[g.group].name for g in v.groups if g.weight>.95}
 if 'head' in groups:
  s=1 if p.x>0 else -1;c=Vector((s*.145,.014,1.155));p=c+(p-c)*Vector((.80,.85,.80));p.z+=.011;ear_ids.append(v.index)
 d.co=p
earkey.value=1;slot=len(body.data.materials);body.data.materials.append(M['Skin'])
for p in body.data.polygons:
 if all(i in ear_ids for i in p.vertices):p.material_index=slot
body['head_pass_ear_vertices']=len(ear_ids)
# Hair cap: coverage around sides/back, cropped above eyes at the front.
vs=[];fs=[];N=48;K=18
vs.append((0,.018,1.366))
for j in range(1,K+1):
 for k in range(N):
  a=math.tau*k/N;front=max(0,math.cos(a));back=max(0,-math.cos(a));end=2.04-.86*front+.10*back;phi=end*j/K
  vs.append((.157*math.sin(a)*math.sin(phi),.018-.148*math.cos(a)*math.sin(phi),1.198+.168*math.cos(phi)))
for k in range(N):fs.append((0,1+k,1+(k+1)%N))
for j in range(K-1):
 for k in range(N):fs.append((1+j*N+k,1+j*N+(k+1)%N,1+(j+1)*N+(k+1)%N,1+(j+1)*N+k))
cap=mesh('HairFoundation',vs,fs,'HairDeep');cap['use']='Under-volume hides scalp gaps, not the final visible helmet.'
rng=random.Random(913);clumps=[]
# Irregular broad curls around side and back; no rows of tiny strands.
for band,(base_phi,count) in enumerate([(.78,9),(1.35,12),(1.80,14),(2.05,9)]):
 for k in range(count):
  a=math.tau*(k+.35*band)/count+rng.uniform(-.15,.15)
  if math.cos(a)>(.30 if band>=2 else .52):continue
  phi=base_phi+rng.uniform(-.20,.20)
  c=Vector((.166*math.sin(a)*math.sin(phi),.018-.151*math.cos(a)*math.sin(phi),1.220+.145*math.cos(phi)))
  normal=Vector((math.sin(a),-math.cos(a),.35*math.cos(phi))).normalized()
  tangent=Vector((math.cos(a),math.sin(a),rng.uniform(-.35,.35))).normalized();up=normal.cross(tangent).normalized()
  angle=rng.uniform(-.85,.85);tangent=(tangent*math.cos(angle)+up*math.sin(angle)).normalized();up=normal.cross(tangent).normalized()
  width=rng.uniform(.015,.020);rad=rng.uniform(.039,.046);controls=[]
  for j in range(7):
   t=j/6;ang=-.65+t*math.pi*.95;fall=1-.30*t
   controls.append(tuple(c+tangent*(math.cos(ang)*rad*fall)+up*(math.sin(ang)*rad*fall)+normal*(.008*math.sin(math.pi*t))))
  o=tube('Curl_%02d'%len(clumps),controls,[.012,width,.019,.010,.004,.0008],['Hair','HairWarm','HairDeep'][len(clumps)%3],.40,14,5);clumps.append(o)
# Major crown groups vary orientation/size and blend into the under-volume.
crowns=[(-.105,-.018,1.331,-.4),(-.050,-.048,1.354,.2),(.015,-.047,1.361,-.3),(.074,-.014,1.345,.4),
 (-.058,.079,1.339,-.5),(.025,.097,1.333,.5),(.105,.065,1.309,.2)]
for x,y,z,angle in crowns:
 controls=[(x-.036,y+.012,z-.015),(x-.026,y-.018,z+.014),(x+.010,y-.028,z+.020),
           (x+.030,y-.005,z+.008),(x+.012,y+.012,z-.007),(x-.002,y+.003,z+.002)]
 clumps.append(tube('CrownCurl_%02d'%len(clumps),controls,[.014,.024,.024,.014,.005,.0008],'HairWarm' if len(clumps)%3==0 else 'Hair',.40,14,6))
# Six sweeping asymmetric forehead curls. Their tips stay above the eyes.
fronts=[[(.059,-.065,1.341),(.025,-.115,1.330),(-.042,-.133,1.298),(-.102,-.123,1.270),(-.130,-.097,1.278),(-.105,-.083,1.293)],
 [(.111,-.051,1.324),(.079,-.105,1.313),(.035,-.128,1.273),(-.003,-.117,1.244),(-.026,-.091,1.259)],
 [(-.025,-.046,1.350),(-.076,-.111,1.324),(-.068,-.137,1.284),(-.026,-.129,1.260),(.008,-.102,1.279)],
 [(.121,-.044,1.303),(.151,-.101,1.281),(.152,-.108,1.252),(.126,-.076,1.233),(.108,-.054,1.250)],
 [(-.103,-.056,1.310),(-.149,-.110,1.285),(-.169,-.095,1.247),(-.150,-.061,1.226),(-.129,-.043,1.245)]]
for k,controls in enumerate(fronts):
 clumps.append(tube('ForeheadCurl_%02d'%k,controls,[.012,.028,.029,.020,.007,.0008],'HairWarm' if k in [1,4] else 'Hair',.32,16,6))
# Side whisker/temple curls soften the connection to ears and nape.
for s in [-1,1]:
 controls=[(s*.139,-.053,1.255),(s*.170,-.060,1.231),(s*.169,-.038,1.201),(s*.151,-.023,1.189),(s*.145,-.034,1.203)]
 clumps.append(tube('TempleCurl_'+str(s),controls,[.012,.024,.020,.008,.0008],'Hair',.35,14,5))
# Broad overlapping back sweeps cover the foundation and avoid a uniform curl grid.
for k,(x,z,s) in enumerate([(-.083,1.288,1),(.030,1.304,-1),(.103,1.257,-1),(-.045,1.237,-1),
 (.041,1.230,1),(-.090,1.202,1),(.067,1.183,-1),(0,1.176,1)]):
 y=.157 if z<1.28 else .136
 controls=[(x-s*.029,y-.008,z+.031),(x+s*.006,y+.003,z+.027),(x+s*.035,y+.007,z+.002),
           (x+s*.026,y+.006,z-.028),(x-s*.007,y+.012,z-.025),(x-s*.012,y+.004,z-.006)]
 clumps.append(tube('BackSweep_%02d'%k,controls,[.012,.021,.018,.010,.004,.0008],'HairWarm' if k in [1,5] else 'Hair',.35,14,6))
outline=[ [(-.123,.002,1.333),(-.168,-.010,1.352),(-.178,-.017,1.373),(-.153,-.028,1.366)],
 [(.043,.020,1.357),(.071,.030,1.389),(.101,.040,1.386),(.088,.058,1.367)],
 [(.140,.073,1.286),(.186,.083,1.310),(.193,.074,1.334),(.169,.058,1.327)],
 [(-.166,.098,1.245),(-.202,.110,1.270),(-.204,.102,1.298),(-.179,.081,1.287)],
 [(0,.159,1.184),(.029,.168,1.164),(.017,.173,1.145),(-.007,.153,1.155)]]
for k,controls in enumerate(outline):
 clumps.append(tube('SilhouetteCurl_%02d'%k,controls,[.009,.012,.008,.0008],'Hair',.40,12,6))
# Keep the already approved 1.40 m maximum, without rescaling body or head.
hair=[o for o in coll.objects if 'Curl' in o.name or o==cap]
for o in hair:
 for v in o.data.vertices:
  p=v.co
  if p.y<-.075 and abs(p.x)<.140:
   clearance=max(0,min(1,(1.320-p.z)/.095))*max(0,min(1,(.140-abs(p.x))/.030))
   p.y+=.026*clearance
   if 'ForeheadCurl' in o.name and p.z<1.225:p.z=1.225+(p.z-1.225)*.30
high=max(v.co.z for o in hair for v in o.data.vertices)
if abs(high-1.4)>1e-7:
 for o in hair:
  for v in o.data.vertices:
   if v.co.z>1.32:v.co.z=1.32+(v.co.z-1.32)*(.08/(high-1.32))
scene['head_pass']='V3 head/face/hair only; preview materials; source V2 archived; no rig edits.'
scene['head_pass_hair_groups']=len(clumps)
# Portrait supplementary reference, beside the model rather than misregistered on it.
refcoll=bpy.data.collections.new('REF_PORTRAIT');scene.collection.children.link(refcoll)
im=bpy.data.images.load(str(R/'Reference/HeadPass/Portrait.png'));im.pack();im.filepath='//../Reference/HeadPass/Portrait.png'
ob=bpy.data.objects.new('REF_CharacterPortrait',None);refcoll.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im
ob.empty_display_size=.68;ob.location=(.51,.15,1.17);ob.rotation_euler=Vector((0,-1,0)).to_track_quat('Z','Y').to_euler()
ob.color=(1,1,1,.45);ob.use_empty_image_alpha=True;ob.empty_image_depth='FRONT';ob.show_empty_image_perspective=False
ob.lock_location=(True,True,True);ob.lock_rotation=(True,True,True);ob.lock_scale=(True,True,True);ob.hide_select=True
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  sp=a.spaces.active;sp.shading.type='MATERIAL';sp.overlay.show_bones=False
  sp.region_3d.view_rotation=Vector((0,-1,0)).to_track_quat('Z','Y');sp.region_3d.view_location=(.14,0,1.17);sp.region_3d.view_distance=1.40;sp.region_3d.view_perspective='ORTHO'
bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=head
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/YoungTrainer_HeadHair_V3.blend'),check_existing=False)
print('HEAD_HAIR_V3_SAVED','new_meshes',len(coll.objects),'large_hair_groups',len(clumps),'facial_loops',head['facial_loops_json'])
