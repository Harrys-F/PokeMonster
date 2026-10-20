"""Zunderlauf: authored continuous branch topology, original reference proportions, explicit gait rig.
No external mesh, remesh, purchased service or existing character is modified.
Blender 5.2; metres. Front=-Y, up=Z. The provisional body height is 0.66 m.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion
R=Path(__file__).resolve().parents[2]; A=R/'Art/Characters/Creatures/Zunderlauf'; S=R/'Saved/ZunderlaufV1'; out=A/'Source/Zunderlauf_V1.blend'
assert not out.exists() or "--revise" in sys.argv; bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene; scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.render.fps=30
collection=bpy.data.collections.new('ZUNDERLAUF_MASTER');scene.collection.children.link(collection)
materials={}
def mat(name,color,rough=.48):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;materials[name]=m;return m
skin=mat('Z_Skin',(.78,.17,.012));belly=mat('Z_Belly',(.67,.51,.255),.61);eyes=mat('Z_Eyes',(.006,.015,.022),.16);claw=mat('Z_Claws',(.46,.44,.36),.41);mouth=mat('Z_Mouth',(.11,.033,.013),.63)
# Object-coordinate scales, not baked studio light. Fine irregular pores/scales with broad colour variation.
n=skin.node_tree.nodes;l=skin.node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');vor=n.new('ShaderNodeTexVoronoi');vor.feature='DISTANCE_TO_EDGE';vor.inputs['Scale'].default_value=78;l.new(tc.outputs['Object'],vor.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.25;bump.inputs['Distance'].default_value=.00045;l.new(vor.outputs['Distance'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal']);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=22;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.64,.115,.006,1);ramp.color_ramp.elements[1].color=(.90,.23,.019,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
n=eyes.node_tree.nodes;v=n.new('ShaderNodeVertexColor');v.layer_name='Col';eyes.node_tree.links.new(v.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
parts=[]
def object_mesh(name,vs,fs,material,weights=None,colors=None):
 m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(name,m);collection.objects.link(o);m.materials.append(material)
 for p in m.polygons:p.use_smooth=True
 if weights:
  groups={k:o.vertex_groups.new(name=k)for k in sorted({k for w in weights for k in w})}
  for i,w in enumerate(weights):
   total=sum(w.values())
   for k,a in w.items():
    if a>1e-8:groups[k].add([i],a/total,'REPLACE')
 if colors:
  c=m.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
  for loop,d in zip(m.loops,c.data):d.color=(*colors[loop.vertex_index],1)
 parts.append(o);return o

def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def trunk_weights(z):
 h=smooth(.410,.473,z);ch=smooth(.26,.40,z)*(1-h);sp=smooth(.17,.30,z)*(1-h-ch);return {k:v for k,v in {'head':h,'chest':ch,'spine':sp,'pelvis':1-h-ch-sp}.items()if v>1e-7}
profile=[(.105,0,0),(.126,.074,.074),(.16,.128,.105),(.22,.16,.13),(.29,.145,.124),(.36,.115,.101),(.40,.094,.087),(.43,.092,.083),(.46,.14,.116),(.50,.171,.133),(.56,.166,.139),(.61,.139,.115),(.645,.082,.071),(.66,0,0)]
def radii(z):
 for i in range(len(profile)-1):
  if profile[i][0]<=z<=profile[i+1][0]:
   a,b=profile[i],profile[i+1];t=(z-a[0])/(b[0]-a[0]);result=[]
   for col in [1,2]:
    prev=profile[max(i-1,0)];nxt=profile[min(i+2,len(profile)-1)];m0=(b[col]-prev[col])/(b[0]-prev[0]);m1=(nxt[col]-a[col])/(nxt[0]-a[0]);dz=b[0]-a[0];result.append((2*t**3-3*t*t+1)*a[col]+(t**3-2*t*t+t)*m0*dz+(-2*t**3+3*t*t)*b[col]+(t**3-t*t)*m1*dz)
   return result
 return (0,0)
def surface_y(x,z):
 rx,ry=radii(z);front=-ry*math.sqrt(max(0,1-(x/max(rx,.001))**2));return front-.028*math.exp(-((z-.482)/.032)**2)*max(0,1-(x/.165)**4)
N=64;Z=[.111+(.654-.111)*i/71 for i in range(72)];vs=[];ws=[];fs=[]
for z in Z:
 rx,ry=radii(z)
 for j in range(N):
  th=j/N*math.tau;x=rx*math.sin(th);y=-ry*math.cos(th)
  if math.cos(th)>0:y-=.028*math.exp(-((z-.482)/.032)**2)*math.cos(th)**3
  vs.append((x,y,z));ws.append(trunk_weights(z))
holes=[]
def hole(z0,z1,j0,j1,key):
 k0=min(range(len(Z)),key=lambda k:abs(Z[k]-z0));k1=min(range(len(Z)),key=lambda k:abs(Z[k]-z1));holes.append((k0,k1,j0,j1,key));return holes[-1]
for side,j in [('L',16),('R',48)]:hole(.317,.386,j-4,j+4,'arm_'+side);hole(.143,.203,j-7,j+7,'leg_'+side)
hole(.188,.249,27,37,'tail')
for k in range(len(Z)-1):
 for j in range(N):
  if any(k0<=k<k1 and j0<=j<j1 for k0,k1,j0,j1,key in holes):continue
  fs.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
for end,z in [(0,.105),(len(Z)-1,.66)]:
 center=len(vs);vs.append((0,0,z));ws.append(trunk_weights(z))
 for j in range(N):
  face=(end*N+j,end*N+(j+1)%N,center);fs.append(face[::-1]if end==0 else face)
def branch(h,centers,radiiA,radiiB,labels):
 k0,k1,j0,j1,key=h;loop=[k0*N+j for j in range(j0,j1+1)]+[k*N+j1 for k in range(k0+1,k1+1)]+[k1*N+j for j in range(j1-1,j0-1,-1)]+[k*N+j0 for k in range(k1-1,k0,-1)];count=len(loop)
 # Preserve angular order of the rectangular body opening; parallel-transport the ring basis.
 c0=sum((Vector(vs[i])for i in loop),Vector())/count;tangent=(Vector(centers[0])-c0).normalized();u=(Vector(vs[loop[0]])-c0);u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u).normalized();angles=[math.atan2((Vector(vs[i])-c0).dot(v),(Vector(vs[i])-c0).dot(u))for i in loop];prev=loop
 for k,c in enumerate(centers):
  c=Vector(c);d=(Vector(centers[min(k+1,len(centers)-1)])-(c0 if k==0 else Vector(centers[k-1]))).normalized();u=(u-d*u.dot(d)).normalized();v=d.cross(u).normalized();ring=[]
  for a in angles:
   pos=c+u*math.cos(a)*radiiA[k]+v*math.sin(a)*radiiB[k]
   if key.startswith('leg') and k>=len(centers)-2:pos.z=max(.006,pos.z)
   ring.append(len(vs));vs.append(tuple(pos));ws.append(labels[k])
  for i in range(count):fs.append((prev[i],prev[(i+1)%count],ring[(i+1)%count],ring[i]))
  prev=ring
 center=len(vs);vs.append(tuple(Vector(centers[-1])));ws.append(labels[-1])
 for i in range(count):fs.append((prev[i],prev[(i+1)%count],center))
for h in holes:
 key=h[-1]
 if key.startswith('arm'):
  side=key[-1];s=1 if side=='L'else-1;branch(h,[(s*.155,-.004,.337),(s*.184,-.010,.302),(s*.208,-.020,.270),(s*.217,-.033,.246),(s*.217,-.043,.237)],[.037,.038,.031,.032,.023],[.036,.035,.029,.032,.018],[{'chest':.25,'upperarm_'+side:.75},{'upperarm_'+side:1},{'upperarm_'+side:.3,'forearm_'+side:.7},{'forearm_'+side:.3,'hand_'+side:.7},{'hand_'+side:1}])
 elif key.startswith('leg'):
  side=key[-1];s=1 if side=='L'else-1;branch(h,[(s*.125,.002,.164),(s*.132,-.003,.122),(s*.132,-.028,.077),(s*.132,-.057,.038),(s*.132,-.069,.018)],[.061,.059,.046,.060,.048],[.063,.057,.046,.087,.065],[{'pelvis':.3,'thigh_'+side:.7},{'thigh_'+side:.65,'shin_'+side:.35},{'shin_'+side:.8,'foot_'+side:.2},{'foot_'+side:1},{'foot_'+side:1}])
 else:
  cs=[(0,.145,.219),(.008,.20,.224),(.021,.267,.263),(.040,.335,.326),(.056,.397,.394),(.064,.438,.444)];branch(h,cs,[.063,.053,.042,.031,.020,.010],[.061,.052,.041,.030,.019,.010],[{'pelvis':.25,'tail_01':.75},{'tail_01':.65,'tail_02':.35},{'tail_02':.65,'tail_03':.35},{'tail_03':.65,'tail_04':.35},{'tail_04':1},{'tail_tip':1}])
body=object_mesh('Zunderlauf_Body',vs,fs,skin,ws)
# Remove only unused grid vertices inside deliberately cut branch openings, no remeshing.
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();body.data.update()
bpy.context.view_layer.objects.active=body;body.select_set(True);sub=body.modifiers.new('Curved branch surfaces','SUBSURF');sub.levels=1;bpy.ops.object.modifier_apply(modifier=sub.name)
# Fine curved mouth / lip and true little nostril recess surfaces, not flames or decals.
def tube(name,points,radius,material,bone):
 verts=[];faces=[];sides=8
 for i,p in enumerate(points):
  d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);d.normalize();u=d.cross(Vector((0,0,1)));u.normalize();v=d.cross(u)
  for j in range(sides):verts.append(tuple(Vector(p)+(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides))*radius))
 for i in range(len(points)-1):
  for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))]);return object_mesh(name,verts,faces,material,[{bone:1}for _ in verts])
points=[]
for i in range(49):
 x=-.124+i/48*.248;z=.478+.013*(abs(x)/.124)**3+.0015*math.cos(x/.124*math.pi*2);points.append((x,surface_y(x,z)-.001,z))
tube('Mouth_SmileGroove',points,.0015,mouth,'head');tube('LowerLip_Organic',[tuple(Vector(p)+Vector((0,.0003,-.0025)))for p in points],.0019,skin,'head')
# A continuous coloured belly belongs to the skin surface: no overlapping plate objects.
bs=skin.copy();bs.name='Z_SkinAndBelly';body.data.materials[0]=bs
bc=body.data.color_attributes.new(name='BellyTint',type='FLOAT_COLOR',domain='POINT')
widths=[(.126,.008),(.15,.076),(.20,.118),(.26,.124),(.32,.114),(.375,.091),(.41,.049),(.415,.008)]
for vert,attr in zip(body.data.vertices,bc.data):
 x,y,z=vert.co;w=0
 for (z0,w0),(z1,w1) in zip(widths,widths[1:]):
  if z0<=z<=z1:w=w0+(w1-w0)*(z-z0)/(z1-z0)
 mask=(1-smooth(w-.002,w+.002,abs(x))) if w and y<-.018 else 0
 c=[a*(1-mask)+b*mask for a,b in zip((.78,.17,.012),(.72,.55,.29))]
 # Shallow segmented creases within one continuous anatomical surface.
 crease=max(math.exp(-((z-zz)/.0022)**2)for zz in [.168,.255,.345])*mask
 if mask:vert.co.y+=.0015*crease
 attr.color=tuple(a*(1-.16*crease) for a in c)+(1,)
bn=bs.node_tree.nodes;bl=bs.node_tree.links;vc=bn.new('ShaderNodeVertexColor');vc.layer_name='BellyTint';mix=bn.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.12;bl.new(vc.outputs['Color'],mix.inputs[1]);bl.new(bn.get('Noise Texture').outputs['Fac'],mix.inputs[2]);bl.new(mix.outputs[0],bn.get('Principled BSDF').inputs['Base Color'])
# Embedded glossy eyes: crescent teal iris and dark large pupil; reflections are real studio/engine light.
for sign in [-1,1]:
 cx=sign*.084;cz=.551;v=[(cx,surface_y(cx,cz)-.030,cz)];colors=[(.003,.009,.012)];faces=[];nr=14;nt=48
 for k in range(1,nr+1):
  r=k/nr
  for j in range(nt):
   th=j/nt*math.tau;x=cx+math.cos(th)*.044*r;z=cz+math.sin(th)*.057*r;y=surface_y(x,z)-.004-.027*math.sqrt(max(0,1-r*r));v.append((x,y,z));pupil=smooth(.76,.98,r);ray=.85+.15*math.sin(th*27+r*32);colors.append(tuple((a*(1-pupil)+b*pupil)*ray for a,b in zip((.002,.007,.010),(.005,.21,.30))))
 for j in range(nt):faces.append((0,1+j,1+(j+1)%nt))
 for k in range(nr-1):
  for j in range(nt):a=1+k*nt+j;b=1+k*nt+(j+1)%nt;faces.append((a,a+nt,b+nt,b))
 object_mesh('Eye_'+str(sign),v,faces,eyes,[{'head':1}for _ in v],colors)
 for index,(zscale,rad)in enumerate([(1,.0021),(-1,.0014)]):
  pts=[]
  for j in range(25):
   th=(j/24*math.pi)*(1 if zscale==1 else -1);x=cx+math.cos(th)*.045;z=cz+math.sin(th)*.058;pts.append((x,surface_y(x,z)-.005,z))
  tube('Organic_Eyelid_'+str(sign)+'_'+str(index),pts,rad,skin,'head')
 for nsign in [-1,1]:pass
 x=sign*.026;z=.506;pts=[]
 for j in range(13):
  th=j/12*math.tau;xx=x+.003*math.cos(th);zz=z+.0017*math.sin(th);pts.append((xx,surface_y(xx,zz)-.0012,zz))
 tube('Nostril_'+str(sign),pts,.001,mouth,'head')
# Blunt three-toed claws; three little claws on each hand, matching primary reference.
def claw_mesh(loc,length,width,bone,forward):
 axis=Vector(forward).normalized();u=axis.cross(Vector((1,0,0))).normalized();v=axis.cross(u);verts=[];faces=[];N=12
 for k,(t,r)in enumerate([(0,.75),(.32,1),(.78,.63),(1,.06)]):
  for j in range(N):verts.append(tuple(Vector(loc)+axis*length*t+(u*math.cos(j*math.tau/N)+v*math.sin(j*math.tau/N))*width*r))
 for k in range(3):
  for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 faces.extend([tuple(range(N-1,-1,-1)),tuple(3*N+j for j in range(N))]);object_mesh('Claw',verts,faces,claw,[{bone:1}for _ in verts])
for side,sign in [('L',1),('R',-1)]:
 for i in range(3):
  claw_mesh((sign*.132+(i-1)*.031,-.126,.024),.030,.012,'foot_'+side,(0,-1,-.1));claw_mesh((sign*.217+(i-1)*.011,-.050,.232),.019,.0075,'hand_'+side,(sign*.10,-.4,-1))
# Join only the authored creature surfaces. Material partitions and weights remain explicit.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object;body.name='Zunderlauf';bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# Create useful UV islands without changing topology, shape or weights.
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(65),island_margin=.018);bpy.ops.object.mode_set(mode='OBJECT')
# Rig has real short-leg axes, all locomotion in local -Y. No player/humanoid skeleton forced onto it.
arm=bpy.data.armatures.new('Zunderlauf_Rig');rig=bpy.data.objects.new('Zunderlauf_Rig',arm);collection.objects.link(rig);bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');bones={}
def bone(name,head,tail,parent=None):
 b=arm.edit_bones.new(name);b.head=head;b.tail=tail
 if parent:b.parent=arm.edit_bones[parent]
 bones[name]=(Vector(head),Vector(tail));return b
bone('root',(0,0,0),(0,0,.08));bone('pelvis',(0,0,.20),(0,0,.28),'root');bone('spine',(0,0,.28),(0,0,.35),'pelvis');bone('chest',(0,0,.35),(0,0,.425),'spine');bone('head',(0,0,.425),(0,0,.635),'chest')
for side,sign in [('L',1),('R',-1)]:
 bone('upperarm_'+side,(sign*.130,0,.35),(sign*.203,-.016,.274),'chest');bone('forearm_'+side,(sign*.203,-.016,.274),(sign*.217,-.033,.246),'upperarm_'+side);bone('hand_'+side,(sign*.217,-.033,.246),(sign*.217,-.051,.226),'forearm_'+side)
 bone('thigh_'+side,(sign*.125,0,.193),(sign*.132,-.003,.117),'pelvis');bone('shin_'+side,(sign*.132,-.003,.117),(sign*.132,-.050,.047),'thigh_'+side);bone('foot_'+side,(sign*.132,-.050,.047),(sign*.132,-.129,.022),'shin_'+side)
tail=[(0,.105,.218),(.008,.20,.224),(.021,.267,.263),(.04,.335,.326),(.056,.397,.394),(.064,.438,.444)]
for i in range(4):bone('tail_0'+str(i+1),tail[i],tail[i+1],'pelvis'if i==0 else'tail_0'+str(i))
bone('tail_tip',tail[4],tail[5],'tail_04');bone('tail_socket',tail[5],(tail[5][0],tail[5][1],tail[5][2]+.02),'tail_tip');bpy.ops.object.mode_set(mode='OBJECT');mod=body.modifiers.new('Creature skin weights','ARMATURE');mod.object=rig;body.parent=rig
# Standalone opaque 3D fire silhouette; shader animation later, exclusively attached to tail_tip.
v=[];faces=[];N=16
for k in range(10):
 t=k/9;rad=max(.0001,.029*math.sin(math.pi*t)**.72*(1-.35*t))
 for j in range(N):
  a=j/N*math.tau;r=rad*(1+.17*math.sin(a*3+t*9));v.append((r*math.cos(a)+.012*t*t,r*math.sin(a),.105*t))
for k in range(9):
 for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
firemat=mat('Z_TailFlame',(.9,.22,.02),.8);p=firemat.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.28,.015,1);p.inputs['Emission Strength'].default_value=1.8
flame=object_mesh('TailFlame_Only',v,faces,firemat);flame.location=tail[-1]
# Rest-pose and static model are saved before clip generation by the next stage.
scene.frame_start=1;scene.frame_end=61;scene.frame_set(1);body.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(body.data);audit={'vertices':len(body.data.vertices),'triangles':len(body.data.loop_triangles),'polygons':len(body.data.polygons),'loose_vertices':sum(not v.link_faces for v in bm.verts),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'materials':len(body.data.materials),'bones':list(bones),'height_m':max(v.co.z for v in body.data.vertices)-min(v.co.z for v in body.data.vertices),'tail_tip_m':tail[-1],'provisional_body_height_target_m':.66};bm.free();assert audit['loose_vertices']==0 and audit['zero_area_faces']==0
bpy.ops.wm.save_as_mainfile(filepath=str(out));(A/'ModelAudit.json').write_text(json.dumps(audit,indent=2));print('ZUNDERLAUF_BODY_BUILT',audit['triangles'],audit['height_m'])
