"""Targeted candidate sources; exact original mesh/rest rig retained except listed core repair."""
import bpy,math,json,hashlib,sys,ast,subprocess,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];name=sys.argv[sys.argv.index('--')+1];assert name in ['Glurak','Nebulak','Machomei','Myrapla'];A=R/'Art/Characters/Creatures'/name;previous=A/'Source'/(name+('_MotionV5'if name in ['Glurak','Nebulak']else'_Meshy_V1')+'.blend');dest=A/'Source'/(name+'_AnimationCorrections_V6.blend');assert not dest.exists()or('--refine-unreleased'in sys.argv and subprocess.run(['git','ls-files','--error-unmatch',str(dest.relative_to(R))],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(previous);bpy.ops.wm.open_mainfile(filepath=str(previous));bpy.context.preferences.filepaths.save_version=0;rig=bpy.data.objects[name+'_Rig'];body=bpy.data.objects[name+'_Body'];scene=bpy.context.scene;pb=rig.pose.bones;co=[tuple(v.co)for v in body.data.vertices];uv=[tuple(v.uv)for v in body.data.uv_layers.active.data];rest={p.name:p.bone.matrix_local.copy()for p in pb};heads={p.name:p.bone.head_local.copy()for p in pb};tails={p.name:p.bone.tail_local.copy()for p in pb};changes={};old_materials=len(body.data.materials)
def rotate(n,axis,angle):
 q=pb[n].bone.matrix_local.to_quaternion();pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,angle)@q)@pb[n].rotation_quaternion
if name=='Glurak':
 from mathutils.bvhtree import BVHTree
 bv=BVHTree.FromPolygons([v.co for v in body.data.vertices],[tuple(p.vertices)for p in body.data.polygons],all_triangles=False)
 attr=body.data.color_attributes['PolishV4'];body.data.color_attributes.active_color=attr;rear_count=shared_count=0
 for poly in body.data.polygons:
  c=sum((body.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
  wing_weight=sum(sum(g.weight for g in body.data.vertices[i].groups if body.vertex_groups[g.group].name.startswith('wing_'))for i in poly.vertices)/len(poly.vertices)
  wing=poly.material_index==0 and abs(c.x)>.23 and c.z>.65 and c.y<.5 and wing_weight>.02
  rear=front=False
  if wing:
   rear=bv.ray_cast(Vector((c.x,2,c.z)),Vector((0,-1,0)),4)[2]==poly.index
   front=bv.ray_cast(Vector((c.x,-2,c.z)),Vector((0,1,0)),4)[2]==poly.index
  fixed=1. if rear and not front else 0.;shared=1. if rear and front else 0.;orientation=1. if poly.normal.y>0 else 0.
  for i in poly.loop_indices:attr.data[i].color=(fixed,shared,orientation,1)
  rear_count+=rear;shared_count+=rear and front
 changes.update(rear_faces=rear_count,two_sided_membrane_faces=shared_count,selection='Exact front/rear BVH ray visibility plus anatomical wing weights; shared faces use TwoSidedSign',no_texture_hue_threshold=True)
if name=='Nebulak':
 # Previous gas assignment was driven by any peripheral skin influence, cutting into the rigid sphere.
 restored=[]
 for poly in body.data.polygons:
  center=sum((body.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices);r2=(center.x/.415)**2+(center.y/.325)**2+((center.z-.475)/.415)**2
  if poly.material_index==1 and r2<1.055:
   poly.material_index=0;restored.append(poly.index)
 changes['core_faces_restored_opaque']=len(restored)
 # Small closed opaque backing inside original core; original facial surface remains in front.
 # This closes remaining transparency-connected openings without remeshing the Meshy face or its UVs.
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,radius=1);inner=bpy.context.object;inner.name='Nebulak_ClosedCore_V6'
 for v in inner.data.vertices:v.co=Vector((v.co.x*.385,v.co.y*.285,.475+v.co.z*.385))
 mat=bpy.data.materials.new('Nebulak_ClosedCore_V6');mat.diffuse_color=(.004,.003,.009,1);body.data.materials.append(mat);inner.data.materials.append(mat)
 for p in inner.data.polygons:p.use_smooth=True
 inner.vertex_groups.new(name='head').add(list(range(len(inner.data.vertices))),1.,'REPLACE');bpy.ops.object.select_all(action='DESELECT');body.select_set(True);inner.select_set(True);bpy.context.view_layer.objects.active=body;bpy.ops.object.join();changes['closed_inner_core_triangles']=40*46;changes['original_vertices_retained']=len(co)
# Cache exact old actions; preserve them as editable references.
roles=['Idle','Walk','Run','Attack','Hit','Faint','Happy']+(['Takeoff','Hover','Land']if name=='Glurak'else[]);cache={};created={}
for role in roles:
 key=name+'_'+role+('_MotionV5'if name=='Glurak'else'');a=bpy.data.actions[key];rig.animation_data.action=a;lo,hi=map(int,a.frame_range);cache[role]={}
 for f in range(lo,hi+1):
  scene.frame_set(f);cache[role][f]={b.name:(b.location.copy(),b.rotation_quaternion.copy(),b.scale.copy())for b in pb}
if name=='Machomei':
 h=1.6;chains=json.loads((A/'MeshyV1_ModelAudit.json').read_text())['leg_chains'];tree=ast.parse((R/'Tools/CreatureExpansionV3/AnimateSource.py').read_text())
 for node in tree.body:
  if isinstance(node,ast.FunctionDef)and node.name in ['orient','solve']:exec(ast.get_source_segment((R/'Tools/CreatureExpansionV3/AnimateSource.py').read_text(),node))
metrics={}
for role in roles:
 a=bpy.data.actions.new(name+'_'+role+'_V6');a.use_fake_user=True;rig.animation_data.action=a;created[role]=a;count=max(cache[role]);duration=(count-1)/scene.render.fps
 for f in range(1,count+1):
  scene.frame_set(f);u=(f-1)/(count-1);phase=math.tau*u
  for b in pb:b.location,b.rotation_quaternion,b.scale=cache[role][f][b.name]
  if name=='Glurak':
   amp={'Idle':.04,'Walk':.07,'Run':.11,'Attack':.24,'Hit':.035,'Faint':.015,'Happy':.13,'Takeoff':.40,'Hover':.40,'Land':.32}[role];flying=role in ['Takeoff','Hover','Land'];envelope=1.
   if role=='Takeoff':envelope=min(1.,u/.25)
   if role=='Land':envelope=1-max(0.,(u-.55)/.45)
   p=phase*(2 if role=='Takeoff'else 1);wave=math.sin(p)+.18*math.sin(2*p-.25)
   for side,sg in [('L',1),('R',-1)]:
    pb['wing_base_'+side].rotation_quaternion=Quaternion();pb['wing_tip_'+side].rotation_quaternion=Quaternion();rotate('wing_base_'+side,(0,1,0),sg*(-.025+amp*envelope*wave));rotate('wing_base_'+side,(0,0,1),sg*(.10 if not flying else .025));rotate('wing_tip_'+side,(0,1,0),sg*((.12 if flying else .032)*envelope*math.sin(p-.55)));rotate('wing_tip_'+side,(0,0,1),sg*(.12 if not flying else .02))
    if role!='Faint':
     arm='upperarm_'+side;pb[arm].rotation_quaternion=Quaternion();rotate(arm,(0,1,0),sg*.63);rotate(arm,(1,0,0),(.13 if role=='Walk'else .21 if role=='Run'else .04)*math.sin(phase+(0 if sg==1 else math.pi)));rotate('forearm_'+side,(0,1,0),sg*.12);rotate('forearm_'+side,(1,0,0),-.09+.04*math.sin(p-.5))
  elif name=='Machomei'and role!='Faint':
   moving=role in ['Walk','Run'];speed=.42 if role=='Walk'else .78 if role=='Run'else 0.;duty=.57 if role=='Walk'else .44
   m=pb['pelvis'].matrix.copy();m.translation.x+=.012*math.sin(phase)if moving else .003*math.sin(phase);pb['pelvis'].matrix=m;rotate('chest',(0,0,1),-.018*math.sin(phase));bpy.context.view_layer.update()
   for c in chains:
    target=heads[c['foot']].copy();target.x=.23 if c['id']=='L'else-.23
    if moving:
     v=(u+c['phase'])%1;travel=speed*duration*duty
     if v<duty:target.y+=travel*(v/duty-.5)
     else:
      t=(v-duty)/(1-duty);slope=(1-duty)/duty;hermite=(-2*t**3+3*t*t)-slope*((t**3-2*t*t+t)+(t**3-t*t));target.y+=travel*(.5-hermite);target.z+=.036*math.sin(math.pi*t)**2
    elif role in ['Attack','Hit','Happy']:target+=pb['root'].matrix.translation-rest['root'].translation
    solve(c,target)
   for side,sg in [('L',1),('R',-1)]:
    for prefix,lag,drop in [('',0,.22),('lower_',.85,.28)]:
     upper=prefix+'upperarm_'+side;fore=prefix+'forearm_'+side;a0=phase+(0 if sg==1 else math.pi)+lag;pb[upper].rotation_quaternion=Quaternion();pb[fore].rotation_quaternion=Quaternion();rotate(upper,(0,1,0),sg*drop);rotate(upper,(1,0,0),(.18 if role=='Walk'else .27 if role=='Run'else .015)*math.sin(a0));rotate(fore,(1,0,0),-.17-.09*math.sin(a0-.35));rotate(fore,(0,1,0),-sg*.08)
     if role=='Attack':
      pulse=math.sin(math.pi*max(0,min(1,(u-(.12 if prefix else 0))/.82)))**2;rotate(upper,(1,0,0),-.48*pulse);rotate(fore,(0,0,1),-sg*.22*pulse)
  elif name=='Myrapla':
   for i,b in enumerate([p for p in pb if p.name.startswith('leaf_')]):
    b.rotation_quaternion=Quaternion();amp={'Idle':.045,'Walk':.075,'Run':.115,'Attack':.09,'Hit':.04,'Faint':.02,'Happy':.10}[role];lag=i*.91;rotate(b.name,(1,0,0),amp*(math.sin(phase-lag)+.24*math.sin(phase*2+lag)));rotate(b.name,(0,1,0),amp*.52*math.sin(phase+lag+.5))
  for b in pb:
   for prop in ['location','rotation_quaternion','scale']:b.keyframe_insert(data_path=prop,frame=f,group=b.name)
 for layer in a.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for key in curve.keyframe_points:key.interpolation='LINEAR'
 lows=[];width=[]
 for f in range(1,count+1):
  scene.frame_set(f);ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();lows.append(min(v.co.z for v in me.vertices));ev.to_mesh_clear()
  if name=='Machomei':width.append(abs(pb['foot_L'].head.x-pb['foot_R'].head.x))
 metrics[role]=dict(duration=duration,min_z_cm=min(lows)*100,foot_width_cm=sum(width)/len(width)*100 if width else None)
 print(name,role,metrics[role],flush=True)
assert co==[tuple(v.co)for v in list(body.data.vertices)[:len(co)]];assert uv==[tuple(v.uv)for v in list(body.data.uv_layers.active.data)[:len(uv)]]
rig.animation_data.action=created['Idle'];scene.frame_start=1;scene.frame_end=max(cache['Idle']);scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert sha(previous)==before
(A/'AnimationCorrectionsV6_Audit.json').write_text(json.dumps(dict(source=str(dest.relative_to(R)),source_sha256=sha(dest),previous_sha256=before,changes=changes,original_geometry_uvs_preserved=True,metrics=metrics,actions={k:v.name for k,v in created.items()}),indent=2));print('V6_CREATURE_SOURCE_OK',name,changes,flush=True)
