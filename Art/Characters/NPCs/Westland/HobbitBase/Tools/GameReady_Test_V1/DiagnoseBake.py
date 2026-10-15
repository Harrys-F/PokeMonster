import bpy,numpy as np,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s;q={}
for name in ['HeadHair','Torso']:
 m=s.objects['GRT_'+name].data;uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2);cross=(uv[:,1,0]-uv[:,0,0])*(uv[:,2,1]-uv[:,0,1])-(uv[:,1,1]-uv[:,0,1])*(uv[:,2,0]-uv[:,0,0]);norm=np.empty(len(m.polygons)*3,np.float32);m.polygons.foreach_get('normal',norm)
 q[name]={'layers':[{'name':l.name,'active_render':l.active_render} for l in m.uv_layers],'uv_area_sum':float(np.abs(cross).sum()*.5),'zero_uv_faces':int(np.count_nonzero(abs(cross)<1e-12)),'uv_min':float(abs(cross).min()),'uv_area_p95':float(np.percentile(abs(cross),95)*.5),'zero_face_normals':int(np.count_nonzero(np.linalg.norm(norm.reshape(-1,3),axis=1)<.9)),'use_smooth':sum(p.use_smooth for p in m.polygons)}
q['bake_use_cage']=s.render.bake.use_cage;q['bake_selected_to_active']=s.render.bake.use_selected_to_active
(P/'BakeDiagnosis.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
