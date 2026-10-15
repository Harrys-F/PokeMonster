import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');s=bpy.data.scenes['Hobbit_NPC_MeshyBase_V2_Cleanup'];bpy.context.window.scene=s;rig=s.objects['HNM2_Rig'];ob=s.objects['HNM2_Body'];me=ob.data
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_MeshyBase_V1.blend'),link=False) as (a,b):b.scenes=['Hobbit_NPC_MeshyBase_V1'];b.actions=['HNM1_Idle_V2','HNM1_Walk_V2','HNM1_Run_V1']
oldscene=b.scenes[0];oldscene.name='Disposable_V1_AnimationComparison';oldrig=oldscene.objects['HNM1_Rig'];oldob=oldscene.objects['HNM1_Body']
# Link only comparison objects in this disposable process so both dependency graphs evaluate.
for o in [oldrig,oldob]:s.collection.objects.link(o);o.hide_render=True
oldob.parent=oldrig
for m in oldob.modifiers:
 if m.type=='ARMATURE':m.object=oldrig
pose=next(i.identifier for i in bpy.types.Armature.bl_rna.properties['pose_position'].enum_items if i.identifier=='POSE')
rig.data.pose_position=pose;oldrig.data.pose_position=pose
origids=[d.value for d in me.attributes['V1_OriginalVertexID'].data]
def signature(arm):return [(b.name,b.parent.name if b.parent else None,list(b.head_local),list(b.tail_local),b.use_deform,list(map(list,b.matrix_local))) for b in arm.data.bones]
def ahash(a):
 h=hashlib.sha256()
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for c in bag.fcurves:
     h.update(repr((c.data_path,c.array_index,[(tuple(k.co),k.interpolation,tuple(k.handle_left),tuple(k.handle_right)) for k in c.keyframe_points])).encode())
 return h.hexdigest()
originalacts=dict(zip(['Idle_V2','Walk_V2','Run_V1'],b.actions))
ids={side:[v.index for v in me.vertices if v.co.z<.085 and ((v.co.x>0)==(side=='l'))] for side in ['l','r']}
reference={side:min(ix,key=lambda i:(me.vertices[i].co-Vector((.16 if side=='l' else -.16,-.04,0))).length_squared) for side,ix in ids.items()}
variants=[];maxdeform=0
for height in [1.4,1.2,1.32,1.45]:
 factor=height/1.4;rig.scale=(factor,)*3;variant={'height_m':height,'scale':factor,'clips':[]}
 for label,speed in [('Idle_V2',0),('Walk_V2',2.1),('Run_V1',3.15)]:
  act=bpy.data.actions['HNM2_'+label];rig.animation_data.action=act;oldrig.animation_data.action=act
  if act.slots:rig.animation_data.action_slot=act.slots[0];oldrig.animation_data.action_slot=act.slots[0]
  start,end=map(int,act.frame_range);samples=[]
  for frame in range(start,end+1):
   s.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();eo=ob.evaluated_get(dg);em=eo.to_mesh();world=[eo.matrix_world@v.co for v in em.vertices]
   row={'frame':frame,'sole_min_m':{side:min(world[i].z for i in ix) for side,ix in ids.items()},'root_translation_m':list(rig.matrix_world@rig.pose.bones['root'].matrix.translation),'finite':all(all(math.isfinite(x) for x in p) for p in world),'reference_sole_points':{side:list(world[ix]) for side,ix in reference.items()}}
   if height==1.4:
    eold=oldob.evaluated_get(dg);mold=eold.to_mesh();delta=max((em.vertices[i].co-mold.vertices[j].co).length for i,j in enumerate(origids));maxdeform=max(maxdeform,delta);row['max_old_new_vertex_delta_m']=delta;eold.to_mesh_clear()
   eo.to_mesh_clear();samples.append(row)
  duration=(end-start)/60;sliding={}
  if speed:
   for side in ['l','r']:
    selected=[row for row in samples if ((row['frame']-start)/(end-start)<(.5 if label=='Walk_V2' else .42))] if side=='l' else [row for row in samples if .5<=((row['frame']-start)/(end-start))<(.5+(.5 if label=='Walk_V2' else .42))]
    yy=[row['reference_sole_points'][side][1]-speed*factor*(row['frame']-start)/60 for row in selected]
    xx=[row['reference_sole_points'][side][0] for row in selected]
    sliding[side]={'virtual_ground_drift_y_cm':(max(yy)-min(yy))*100,'lateral_drift_cm':(max(xx)-min(xx))*100,'assumed_constant_speed_cm_s':speed*factor*100,'contact_phase_assumed':'authored first 50% walk / 42% run, opposite leg +0.5 cycle; fixed source sole vertex, no terrain/blend simulation'}
  variant['clips'].append({'name':act.name,'keyframes_unchanged':ahash(act)==ahash(originalacts[label]),'duration_s':duration,'samples':samples,'min_sole_m':min(v for row in samples for v in row['sole_min_m'].values()),'root_max_m':max(Vector(row['root_translation_m']).length for row in samples),'foot_sliding_estimate':sliding})
 variants.append(variant);print('VARIANT_AUDITED',height,flush=True)
uvsame=all(tuple(a.uv)==tuple(b.uv) for u,v in zip(me.uv_layers,oldob.data.uv_layers) for a,b in zip(u.data,v.data))
normaldiff=max((a.vector-b.vector).length for a,b in zip(me.corner_normals,oldob.data.corner_normals))
result={'source':bpy.data.filepath,'saved_source_modified':False,'rig_signature_identical':signature(rig)==signature(oldrig),'animations_identical':all(c['keyframes_unchanged'] for v in variants for c in v['clips']),'original_uv_corners_identical':uvsame,'corner_normal_max_vector_difference':normaldiff,'max_V1_V2_deformed_vertex_difference_m_all_243_frames':maxdeform,'variants':variants,'full_frame_samples':sum(len(c['samples']) for v in variants for c in v['clips']),'limitations':'Bone-based in-place clips; no runtime spring, terrain IK, acceleration, interpolation-between-saved-frame self-collision or Unreal import tested.'}
(B/'Review/MeshyBaseV2/AnimationAudit.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='variants'});assert result['rig_signature_identical'];assert result['animations_identical'];assert uvsame;assert maxdeform<1e-7;assert all(row['finite'] for v in variants for c in v['clips'] for row in c['samples'])
