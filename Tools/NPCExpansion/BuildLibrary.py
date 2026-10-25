"""Individual NPC rig/clip preparation from existing working sources. Incoming stays immutable.
Run Blender --background --threads 3 --python ... -- <technical-ID>.
No runtime reduction, retopology, texture repainting, or automatic changes to originals.
"""
import bpy,bmesh,json,math,sys,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
R=Path('/Users/harry/Developer/PokeMonster');N=R/'Art/Characters/NPCs';key=sys.argv[sys.argv.index('--')+1]
a=next(x for x in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()) if x['id']==key);
if a.get('simple'):
 import runpy
 runpy.run_path(str(R/'Tools/NPCExpansion/BuildHealerLibrary.py'),run_name='__main__');raise SystemExit()
id=a['id'];C=N/id if id!='HobbitBase' else N/'Westland/HobbitBase';E=C/'Exports/Library';E.mkdir(parents=True,exist_ok=True);O=R/'Saved/ProjectRefinement/NPCExpansion/AnimationViews'/id;O.mkdir(parents=True,exist_ok=True)
dst=C/'Source'/(id+'_NPCLibrary.blend');assert not dst.exists(),dst
bpy.context.preferences.filepaths.save_version=0
if a.get('existing'):
 bpy.ops.wm.open_mainfile(filepath=str(N/a['existing']),load_ui=False);obj=bpy.data.objects[a['mesh']];rig=bpy.data.objects[a['rig']];rig.animation_data.action=None
 # Discard only in-memory other diagnostic/high-poly objects, never source files.
 for x in list(bpy.data.objects):
  if x not in (obj,rig):bpy.data.objects.remove(x,do_unlink=True)
 obj.hide_set(False);obj.hide_render=False
else:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(C/'Exports'/('SM_'+id+'_Reference_V1.fbx')));obj=next(x for x in bpy.data.objects if x.type=='MESH');rig=None
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.fps=30
obj.name=id+'_LibraryMesh'
# Actual source UV/material topology preserved byte-for-byte after bind-space normalization.
if not rig:
 bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 # Weld exact import seam duplicates only in the working rig, preserving loop UV data.
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(obj.data);bm.free()
 d=bpy.data.armatures.new(id+'_LibrarySkeleton');rig=bpy.data.objects.new(id+'_LibraryRig',d);s.collection.objects.link(rig);obj.select_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');bones={}
 def bone(n,h,t,p=None):
  b=d.edit_bones.new(n);b.head=h;b.tail=t
  if p:b.parent=bones[p]
  bones[n]=b
 bone('root',(0,0,0),(0,0,.10));bone('pelvis',(0,0,a['hip']),(0,0,a['hip']+.12),'root');bone('spine',(0,0,a['hip']+.12),(0,0,a['shoulder']-.15),'pelvis');bone('chest',(0,0,a['shoulder']-.15),(0,0,a['neck']),'spine');bone('neck',(0,0,a['neck']),(0,0,a['head']),'chest');bone('head',(0,0,a['head']),(0,0,a['height']-.01),'neck')
 for side,sg in [('l',1),('r',-1)]:
  bone('clavicle_'+side,(sg*.03,0,a['shoulder']),(sg*a['sx'],0,a['shoulder']),'chest');bone('upperarm_'+side,(sg*a['sx'],0,a['shoulder']),(sg*a['ex'],0,a['shoulder']),'clavicle_'+side);bone('lowerarm_'+side,(sg*a['ex'],0,a['shoulder']),(sg*a['wx'],0,a['shoulder']),'upperarm_'+side);bone('hand_'+side,(sg*a['wx'],0,a['shoulder']),(sg*a['hx'],-.01,a['shoulder']),'lowerarm_'+side)
  bone('thigh_'+side,(sg*a['fx'],0,a['hip']),(sg*a['fx'],-.01,a['knee']),'pelvis');bone('shin_'+side,(sg*a['fx'],-.01,a['knee']),(sg*a['fx'],0,a['ankle']),'thigh_'+side);bone('foot_'+side,(sg*a['fx'],0,a['ankle']),(sg*a['fx'],-a['height']*.08,.04),'shin_'+side)
  if a.get('sleeves'):
   for part,x,parent in [('upper',a['ex']*.8,'upperarm_'),('fore',(a['wx']+a['ex'])/2,'lowerarm_')]:
    bone('drape_'+part+'_'+side,(sg*x,0,a['shoulder']-.07),(sg*x,0,a['shoulder']-.40),parent+side);bones['drape_'+part+'_'+side].use_inherit_rotation=False
 bone('cape_upper',(0,.13,a['shoulder']-.02),(0,.16,a['hip']),'chest');bone('cape_lower',(0,.16,a['hip']),(0,.18,.18),'cape_upper');bone('bag',(.20,-.12,a['hip']),(.20,-.12,a['hip']-.18),'pelvis')
 if a.get('beard'):bone('beard',(0,-.13,a['head']),(0,-.19,a['shoulder']-.18),'head')
 bpy.ops.object.mode_set(mode='OBJECT');groups={n:obj.vertex_groups.new(name=n) for n in bones}
 def sm(lo,hi,x):t=max(0,min(1,(x-lo)/(hi-lo)));return t*t*(3-2*t)
 for v in obj.data.vertices:
  x,y,z=v.co;ax=abs(x);side='l' if x>0 else 'r';arm=sm(a['sx']*.76,a['sx']+ .06,ax)
  if a.get('rooted') and z<a['hip']:w={'root':1}
  elif a.get('beard') and y<-.13 and ax<a['sx']*.57 and a['shoulder']-.20<z<a['head']+.03:w={'beard':1}
  elif z>a['head']-.01 and ax<a['sx']*.95:w={'head':1}
  elif a.get('sleeves') and arm>0 and z>a['shoulder']-.60 and z<a['shoulder']-.08:
   t=sm(a['ex']-.06,a['ex']+.05,ax);w={'chest':1-arm,'drape_upper_'+side:(1-t)*arm,'drape_fore_'+side:t*arm}
  elif arm>0 and z>a['shoulder']-.18:
   if ax<a['wx']-.08:t=sm(a['ex']-.07,a['ex']+.06,ax);ww={'upperarm_'+side:1-t,'lowerarm_'+side:t}
   else:t=sm(a['wx']-.05,a['wx']+.03,ax);ww={'lowerarm_'+side:1-t,'hand_'+side:t}
   w={'chest':1-arm};w.update({n:q*arm for n,q in ww.items()})
  elif a.get('cape') and y>.09 and .12<z<a['shoulder']-.09:
   t=sm(a['hip']*.60,a['shoulder']*.90,z);w={'cape_upper':t,'cape_lower':1-t}
  elif z>a['neck']-.03:t=sm(a['neck']-.03,a['head'],z);w={'neck':1-t,'head':t}
  elif z>a['hip']-.02:t=sm(a['hip']+.10,a['shoulder']-.16,z);w={'spine':1-t,'chest':t}
  elif z>a['knee']*.65:
   t=sm(a['knee']-.05,a['knee']+.07,z);w={'shin_'+side:1-t,'thigh_'+side:t}
   # A robe remains cloth, never a pair of independently stretching trousers.
   if a['robe']:
    q=.45 if not a.get('rigid_armor') else .18;w={n:v*q for n,v in w.items()};w['pelvis']=1-q
  else:
   t=sm(a['ankle'],a['ankle']+.08,z);w={'foot_'+side:1-t,'shin_'+side:t}
  total=sum(max(q,0) for q in w.values())
  for n,q in w.items():
   if q>1e-6:groups[n].add([v.index],q/total,'REPLACE')
 obj.parent=rig;m=obj.modifiers.new('Individual NPC skinning','ARMATURE');m.object=rig
# Resolve source materials without changing images. Pack only referenced texture images.
for im in bpy.data.images:
 if im.source=='FILE' and im.users:
  old=Path(bpy.path.abspath(im.filepath));candidates=[old,C/'Textures'/old.name,C/'Textures/MeshyBaseV2'/old.name]
  p=next((x for x in candidates if x.is_file()),None)
  if p:im.filepath=str(p);im.reload();im.pack()
  else:assert im.packed_file,(id,im.name,im.filepath)
import runpy
runpy.run_path(str(R/'Tools/NPCExpansion/Materials.py'))['apply'](id,obj,C)
for m in obj.modifiers:
 if m.type=='ARMATURE':m.use_deform_preserve_volume=False
rig.name=a['rig'] if a.get('reuse_mesh') else id+'_LibraryRig';rig.animation_data_create();rig.animation_data.action=None;rig.data.pose_position='POSE';pb=rig.pose.bones
for p in pb:p.rotation_mode='QUATERNION'
def fingerprint():
 co=np.empty(len(obj.data.vertices)*3,np.float32);obj.data.vertices.foreach_get('co',co)
 uv=np.empty(len(obj.data.loops)*2,np.float32);obj.data.uv_layers.active.data.foreach_get('uv',uv)
 return dict(geometry=hashlib.sha256(co.tobytes()).hexdigest(),uv=hashlib.sha256(uv.tobytes()).hexdigest())
identity=fingerprint()
def rot(n,axis,ang):
 if n not in pb:return
 q=rig.data.bones[n].matrix_local.to_quaternion();pb[n].rotation_quaternion=(q.inverted()@Quaternion(axis,ang)@q)@pb[n].rotation_quaternion
def solve(side,target,pitch):
 bpy.context.view_layer.update();hip=pb['thigh_'+side].head.copy();b1=rig.data.bones['thigh_'+side];b2=rig.data.bones['shin_'+side];l1,l2=b1.length,b2.length;v=target-hip;d=min(v.length,l1+l2-.0001);u=v.normalized();target=hip+u*d;c=(l1*l1-l2*l2+d*d)/(2*d);pole=Vector((0,-1,0));k=hip+u*c+(pole-u*pole.dot(u)).normalized()*math.sqrt(max(0,l1*l1-c*c));toe=target+Quaternion((1,0,0),pitch)@(rig.data.bones['foot_'+side].tail_local-rig.data.bones['foot_'+side].head_local)
 for name,head,tail in [('thigh_'+side,hip,k),('shin_'+side,k,target),('foot_'+side,target,toe)]:
  b=rig.data.bones[name];q=(b.tail_local-b.head_local).rotation_difference(tail-head);pb[name].matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()@b.matrix_local.to_3x3().to_4x4();bpy.context.view_layer.update()
 return list(target)
def smooth(t):return t*t*t*(10+t*(-15+6*t))
clips=[('Idle',3.),('Talk',3.),('Greet',2.4),('TurnLeft',1.2),('TurnRight',1.2)]
if a['walk']>0:clips += [('Walk',1.0 if a['robe'] else .90)]
if a['run']>0:clips += [('Run',.68)]
audit=[];footids={side:[v.index for v in obj.data.vertices if v.co.z<a['ankle']*1.15 and (v.co.x>0)==(side=='l')] for side in ['l','r']}
for kind,duration in clips:
 count=round(duration*30)+1;act=bpy.data.actions.new('A_'+id+'_'+kind+'_Library');act.use_fake_user=True;rig.animation_data.action=None;contacts=[];minfloor=100;maxwidth=0
 for frame in range(1,count+1):
  s.frame_set(frame);t=(frame-1)/(count-1);ph=2*math.pi*t;moving=kind in ('Walk','Run');running=kind=='Run';turn=kind.startswith('Turn');speed=a['run'] if running else a['walk'];stride=speed*.01*duration/4 if moving else 0
  for p in pb:p.location=(0,0,0);p.rotation_quaternion=Quaternion();p.scale=(1,1,1)
  # Bone-local Y of pelvis is world Z. Avoid V3's excessive 7.8-cm crouch.
  pb['pelvis'].location=(a['height']*.003*math.sin(ph) if moving else 0,-a['height']*.012+(a['height']*.002*math.cos(2*ph) if moving else 0),0)
  if a.get('rooted'):pb['pelvis'].location=(0,0,0)
  rot('chest',(1,0,0),(.025 if running else .008)+.003*math.sin(ph));rot('chest',(0,0,1),-.025*math.sin(ph) if moving else .002*math.sin(ph));rot('head',(0,0,1),.022*math.sin(ph) if kind=='Talk' else .002*math.sin(ph))
  for side,sg in [('l',1),('r',-1)]:
   u=(t+(0 if sg==1 else .5))%1;stance=u<.5;forward=lift=pitch=0
   if moving:
    if stance:forward=stride-4*stride*u
    else:
     v=(u-.5)*2;forward=-stride-2*stride*v+4*stride*smooth(v);lift=a['height']*(.045 if running else .023)*math.sin(math.pi*v)**2;pitch=-.09*math.sin(math.pi*v)
   elif turn:lift=a['height']*.009*max(0,math.sin(2*math.pi*u))**2
   base=rig.data.bones['foot_'+side].head_local.copy();base.y-=forward;base.z+=lift+.002
   if not a.get('rooted'):ankle=solve(side,base,pitch)
   else:ankle=list(base)
   swing=(.23 if running else .11)*math.cos(ph+(0 if sg==1 else math.pi)) if moving else .003*math.sin(ph)
   down=62 if a.get('sleeves') else 70
   if a.get('rooted'):down=8
   rot('upperarm_'+side,(0,1,0),sg*math.radians(down));rot('upperarm_'+side,(1,0,0),swing);rot('lowerarm_'+side,(0,1,0),sg*math.radians(9 if not running else 24))
   if kind in ('Greet','Talk') and side=='l':
    envelope=math.sin(math.pi*t)**2
    rot('upperarm_l',(0,1,0),-math.radians(28 if kind=='Greet' else 5)*envelope);rot('lowerarm_l',(1,0,0),-(.65 if kind=='Greet' else .14)*envelope);rot('hand_l',(0,0,1),.11*math.sin(ph*2)*envelope if kind=='Greet' else 0)
   if a.get('sleeves'):
    # Exporter bakes no-inherit orientation into ordinary per-bone local transforms.
    for part in ['upper','fore']:pb['drape_'+part+'_'+side].rotation_quaternion=Quaternion()
   contacts.append({'frame':frame,'side':side,'stance':stance if moving or turn else True,'ankle_m':ankle})
  for n in ['cape_upper','cape_lower','cape_l','cape_r']:rot(n,(1,0,0),-.015-(.012 if moving else .003)*math.sin(2*ph-.6))
  rot('bag',(1,0,0),.012*math.sin(ph-.4) if moving else 0);rot('beard',(1,0,0),.004*math.sin(ph-.5))
  bpy.context.view_layer.update()
  # Evaluate real weighted geometry throughout sampled phase, never just a rig gizmo.
  if frame==1 or frame==count or (frame-1)%max(1,round((count-1)/8))==0:
   ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);assert np.isfinite(co).all(),(id,kind,frame);minfloor=min(minfloor,float(co[:,2].min()));maxwidth=max(maxwidth,float(np.ptp(co[:,0])));ev.to_mesh_clear()
  rig.animation_data.action=act
  for p in pb:p.keyframe_insert(data_path='location',frame=frame,group=p.name);p.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=p.name)
  rig.animation_data.action=None
 for layer in act.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for curve in bag.fcurves:
     for k in curve.keyframe_points:k.interpolation='LINEAR'
 audit.append({'role':kind,'name':act.name,'frames':count,'duration':duration,'minimum_surface_z_m':minfloor,'maximum_width_m':maxwidth,'contacts':contacts,'authored_speed_cm_s':speed if moving else 0})
 print('CLIP_COMPLETE',id,kind,minfloor,flush=True)
assert identity==fingerprint();s['technical_id']=id;s['original_appearance']='Original source geometry, UVs and textures retained';s['world_height_m']=a['height'];s['walk_speed_cm_s']=a['walk'];s['run_speed_cm_s']=a['run'];s['limitations']=a.get('limitation','No finger/facial animation or cloth simulation; authored ground clips require visual review.')
for o in s.objects:o.select_set(False)
obj.hide_set(False);obj.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
rig.animation_data.action=bpy.data.actions['A_'+id+'_Idle_Library'];s.frame_start=1;s.frame_end=91;s.frame_set(1)
# Save only reusable runtime mesh/rig/actions; packed textures, no high-poly duplicated reference.
bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(E/('SK_'+id+'_Library.fbx')),bake_anim=False,**kw);rig.data.pose_position='POSE'
for row in audit:
 rig.animation_data.action=bpy.data.actions[row['name']];s.frame_start=1;s.frame_end=row['frames'];s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(E/(row['name']+'.fbx')),bake_anim=True,**dict(kw,object_types={'ARMATURE'}))
report={'id':id,'source':a.get('existing',str((C/'Exports'/('SM_'+id+'_Reference_V1.fbx')).relative_to(N))),'blend':str(dst.relative_to(R)),'bones':len(rig.data.bones),'vertices':len(obj.data.vertices),'triangles':sum(len(p.vertices)-2 for p in obj.data.polygons),'geometry_and_uv_unchanged_during_animation_authoring':identity==fingerprint(),'fingerprints':identity,'clips':audit,'limitations':s['limitations'],'config':a};(O/'Audit.json').write_text(json.dumps(report,indent=2))
# Small diagnostic renders are local only, not evidence of an Unreal integration.
s.world=bpy.data.worlds.new('RigInspection');s.world.color=(.17,.17,.17)
for loc,power in [((-3,-4,5),650),((3,-1,4),500),((0,3,4),450)]:
 d=bpy.data.lights.new('RigInspection','AREA');d.energy=power;d.size=4;v=bpy.data.objects.new('RigInspection',d);s.collection.objects.link(v);v.location=Vector(loc)*max(1,a['height']/2);v.rotation_euler=(Vector((0,0,a['height']*.5))-v.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('RigInspection');cam=bpy.data.objects.new('RigInspection',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=a['height']*1.25;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3;s.render.resolution_x=600;s.render.resolution_y=750;s.render.resolution_percentage=100
for kind,frame,label in [('Idle',1,'Idle'),('Greet',37,'Greet')]+([('Walk',9,'Walk')] if a['walk']>0 else []):
 rig.animation_data.action=bpy.data.actions['A_'+id+'_'+kind+'_Library'];s.frame_set(frame);cam.location=(a['height']*1.5,-a['height']*3,a['height']*.75);cam.rotation_euler=(Vector((0,0,a['height']*.5))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(label+'.png'));bpy.ops.render.render(write_still=True)
print('NPC_LIBRARY_COMPLETE',id,flush=True)
