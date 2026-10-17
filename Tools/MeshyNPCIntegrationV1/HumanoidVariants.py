import bpy,bmesh,numpy as np,json,math
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');I=R/'Art/Characters/NPCs/IntegrationV1';C=Path(bpy.data.filepath).parent.parent;id=C.name;s=bpy.context.scene
# Per-model landmarks chosen from actual front/profile renders, not a globally scaled human rig.
configs={
 'WhiteHairedWarrior':dict(h=1.85,hip=.91,knee=.47,ankle=.11,shoulder=1.43,neck=1.53,head=1.61,sx=.25,ex=.54,wx=.80,hx=.92,fx=.12,arm_floor=1.23),
 'ElvenArcher':dict(h=1.95,hip=.98,knee=.52,ankle=.105,shoulder=1.49,neck=1.60,head=1.68,sx=.255,ex=.565,wx=.835,hx=.97,fx=.12,arm_floor=1.24),
 'DwarfWarrior':dict(h=1.32,hip=.59,knee=.32,ankle=.085,shoulder=1.01,neck=1.04,head=1.13,sx=.23,ex=.43,wx=.59,hx=.69,fx=.12,arm_floor=.86)}
a=configs[id];hp=next(o for o in s.objects if o.type=='MESH');obj=hp.copy();obj.data=hp.data.copy();obj.name=id+'_Runtime';col=bpy.data.collections.new('RUNTIME_CANDIDATE');s.collection.children.link(col);col.objects.link(obj);obj.data.transform(obj.matrix_world);obj.matrix_world.identity();hp.hide_set(True);hp.hide_render=True
for o in s.objects:o.select_set(False)
obj.select_set(True);bpy.context.view_layer.objects.active=obj
bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(obj.data);bm.free();mod=obj.modifiers.new('Runtime reduction trial','DECIMATE');mod.ratio=90000/len(obj.data.polygons);mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
with bpy.data.libraries.load(str(R/'Art/Characters/NPCs/Ranger/Source/Ranger_NPC_V1.blend'),link=False) as (src,d):
 d.objects=['Ranger_Pilot_Rig'];d.actions=['A_Ranger_Idle_Pilot','A_Ranger_Gesture_Pilot']
rig=d.objects[0];rig.name=id+'_Rig';rig.data.name=id+'_Skeleton';col.objects.link(rig);obj.select_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig;rig.animation_data.action=None;bpy.ops.object.mode_set(mode='EDIT');b=rig.data.edit_bones
coords={'root':((0,0,0),(0,0,.12)),'pelvis':((0,0,a['hip']),(0,0,a['hip']+.13)),'spine':((0,0,a['hip']+.13),(0,0,a['shoulder']-.17)),'chest':((0,0,a['shoulder']-.17),(0,0,a['neck'])),'neck':((0,0,a['neck']),(0,0,a['head'])),'head':((0,0,a['head']),(0,0,a['h']-.02)),'cape_upper':((0,.10,a['shoulder']),(0,.15,a['hip'])),'cape_lower':((0,.15,a['hip']),(0,.17,.20)),'bag':((.20,-.10,a['hip']),(.20,-.10,a['hip']-.20)),'back_sword':((-.16,.14,a['shoulder']-.08),(-.20,.14,a['h']-.1))}
for side,sg in [('l',1),('r',-1)]:
 coords.update({'clavicle_'+side:((sg*.035,0,a['shoulder']),(sg*a['sx'],0,a['shoulder'])),'upperarm_'+side:((sg*a['sx'],0,a['shoulder']),(sg*a['ex'],0,a['shoulder'])),'lowerarm_'+side:((sg*a['ex'],0,a['shoulder']),(sg*a['wx'],-.005,a['shoulder'])),'hand_'+side:((sg*a['wx'],-.005,a['shoulder']),(sg*a['hx'],-.02,a['shoulder']-.005)),'thigh_'+side:((sg*.115,0,a['hip']),(sg*a['fx'],-.01,a['knee'])),'shin_'+side:((sg*a['fx'],-.01,a['knee']),(sg*a['fx'],0,a['ankle'])),'foot_'+side:((sg*a['fx'],0,a['ankle']),(sg*a['fx'],-.16,.05))})
for n,(h,t) in coords.items():b[n].head=h;b[n].tail=t
if id=='DwarfWarrior':
 v=b.new('beard');v.head=(0,-.15,1.12);v.tail=(0,-.20,.83);v.parent=b['head']
bpy.ops.object.mode_set(mode='OBJECT');groups={n:obj.vertex_groups.new(name=n) for n in rig.data.bones.keys()}
def smooth(lo,hi,x):
 t=max(0,min(1,(x-lo)/(hi-lo)));return t*t*(3-2*t)
for v in obj.data.vertices:
 x,y,z=v.co;ax=abs(x);side='l' if x>0 else 'r';strength=smooth(a['sx']*.75,a['sx']+ .045,ax)
 if id=='DwarfWarrior' and ax<.14 and y<-.12 and .78<z<1.18:w={'beard':1}
 elif id in ['WhiteHairedWarrior','ElvenArcher'] and y>.10 and ax>.17 and z>a['shoulder']-.08:w={'back_sword':1}
 elif z>a['head']-.015 and ax<.24:w={'head':1}
 elif ax>a['sx']*.75 and z>a['arm_floor']:
  if ax<a['wx']-.1:t=smooth(a['ex']-.06,a['ex']+.06,ax);arm={'upperarm_'+side:1-t,'lowerarm_'+side:t}
  else:t=smooth(a['wx']-.04,a['wx']+.025,ax);arm={'lowerarm_'+side:1-t,'hand_'+side:t}
  w={'chest':1-strength};w.update({n:q*strength for n,q in arm.items()})
 elif id=='ElvenArcher' and y>.055 and .24<z<a['shoulder']-.04:t=smooth(a['hip']*.6,a['shoulder']*.89,z);w={'cape_upper':t,'cape_lower':1-t}
 elif z>a['neck']-.04:t=smooth(a['neck']-.04,a['head'],z);w={'neck':1-t,'head':t}
 elif z>a['hip']-.03:t=smooth(a['hip']+.12,a['shoulder']-.12,z);w={'spine':1-t,'chest':t}
 elif z>a['knee']*.65:t=smooth(a['knee']-.06,a['knee']+.07,z);w={'shin_'+side:1-t,'thigh_'+side:t}
 else:t=smooth(a['ankle'],a['ankle']+.09,z);w={'foot_'+side:1-t,'shin_'+side:t}
 total=sum(w.values())
 for n,q in w.items():
  if q>1e-5:groups[n].add([v.index],q/total,'REPLACE')
obj.parent=rig;mod=obj.modifiers.new('Adapted humanoid deformation','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True;s.render.fps=30
idle,talk=d.actions;idle.use_fake_user=True;talk.use_fake_user=True;idle.name='A_'+id+'_Idle_V1';talk.name='A_'+id+'_Talk_V1';rig.animation_data.action=idle;s.frame_start=1;s.frame_end=91;s.frame_set(1)
path=C/'Source'/(id+'_NPC_V1.blend');assert not path.exists();s['status']='Stationary rig candidate, requires visual review';bpy.ops.wm.save_as_mainfile(filepath=str(path))
for o in s.objects:o.select_set(False)
obj.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
kw=dict(use_selection=True,object_types={'MESH','ARMATURE'},global_scale=1.,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',add_leaf_bones=False,use_armature_deform_only=True,mesh_smooth_type='FACE',use_mesh_modifiers=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_simplify_factor=0.,bake_anim_step=1.,path_mode='AUTO')
rig.data.pose_position='REST';bpy.ops.export_scene.fbx(filepath=str(C/'Exports'/('SK_'+id+'_NPC_V1.fbx')),bake_anim=False,**kw);rig.data.pose_position='POSE'
for clip,end in [(idle,91),(talk,61)]:
 rig.animation_data.action=clip;s.frame_start=1;s.frame_end=end;s.frame_set(1);bpy.ops.export_scene.fbx(filepath=str(C/'Exports'/(clip.name+'.fbx')),bake_anim=True,**kw)
audit={'id':id,'rig_bones':len(rig.data.bones),'triangles':len(obj.data.polygons),'vertices':len(obj.data.vertices),'per_model_landmarks':a,'compatible_core':'Naming/hierarchy reused from separately validated Ranger; own bone positions, weights, skeleton and clips. No player data changed.','status':'Needs visual inspection; not integrated','walk':'No moving NPC role, not authored','renders':[],'clips':[]}
for clip,end,label in [(idle,91,'05_Rig_Idle'),(talk,61,'06_Rig_Talk')]:
 rig.animation_data.action=clip;floor=100;outer=0
 for frame in range(1,end+1):
  s.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get();em=obj.evaluated_get(dg);m=em.to_mesh();co=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',co);co=co.reshape(-1,3);floor=min(floor,float(co[:,2].min()));outer=max(outer,float(np.abs(co[:,0]).max()));em.to_mesh_clear()
 audit['clips'].append({'name':clip.name,'frames_checked':end,'minimum_surface_z_m':floor,'max_half_width_m':outer})
 s.frame_set(1 if clip==idle else 31);s.camera.location=(a['h']*1.5,-a['h']*2.5,a['h']*1.15);s.camera.rotation_euler=(Vector((0,0,a['h']*.5))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=a['h']*1.25;s.render.filepath=str(C/'Previews'/(label+'.png'));bpy.ops.render.render(write_still=True);audit['renders'].append(s.render.filepath)
(I/(id+'_RigAudit.json')).write_text(json.dumps(audit,indent=2));print('HUMANOID_DONE',id,flush=True)
