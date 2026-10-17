import bpy,json,numpy as np
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV3/Data';s=bpy.context.scene;r=s.objects['Ranger_Pilot_Rig'];r.data.pose_position='REST';s.frame_set(1);a={'reopened':bpy.data.filepath,'bones':len(r.data.bones),'actions':[(x.name,x.frame_range[:]) for x in bpy.data.actions],'meshes':[],'clips':[]}
for n in ['Ranger_V2_LOD0','Ranger_V2_LOD1']:
 o=s.objects[n];m=o.data;m.calc_loop_triangles();co=np.array([v.co[:] for v in m.vertices]);weights=np.array([sum(g.weight for g in v.groups) for v in m.vertices]);a['meshes'].append({'name':n,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'height_m':float(co[:,2].max()-co[:,2].min()),'min_z_m':float(co[:,2].min()),'uv_layers':[x.name for x in m.uv_layers],'material_slots':len(m.materials),'weights_min':float(weights.min()),'weights_max':float(weights.max()),'nonfinite_coordinates':int((~np.isfinite(co)).sum())})
r.data.pose_position='POSE'
for kind,count in [('Idle',181),('Walk',49),('Talk',181),('TurnLeft',61),('TurnRight',61)]:
 r.animation_data.action=bpy.data.actions['A_Ranger_'+kind+'_AQV3'];floors={n:100 for n in ['Ranger_V2_LOD0','Ranger_V2_LOD1']};maxspan=0
 for f in range(1,count+1):
  s.frame_set(f)
  for n in floors:
   o=s.objects[n];o.hide_set(False);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();co=np.array([v.co[:] for v in m.vertices]);assert np.isfinite(co).all();floors[n]=min(floors[n],float(co[:,2].min()));maxspan=max(maxspan,float(np.ptp(co[:,0])));ev.to_mesh_clear()
 a['clips'].append({'clip':kind,'frames_evaluated':count,'minimum_z_m':floors,'maximum_surface_width_m':maxspan})
a['textures']=[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)} for im in bpy.data.images if im.users and im.source=='FILE'];(O/'BlenderReopened.json').write_text(json.dumps(a,indent=2));print('REOPEN_AND_CYCLE_AUDIT_OK',flush=True)
