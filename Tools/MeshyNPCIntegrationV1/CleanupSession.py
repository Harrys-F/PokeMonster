import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();I=r/'Art/Characters/NPCs/IntegrationV1';out={}
for n in ['_npc_review','_npc_perf','_npc_cost']:
 if hasattr(unreal,n):unreal.unregister_slate_post_tick_callback(getattr(unreal,n));delattr(unreal,n);out[n]='removed'
if hasattr(unreal,'_npcintegration_queue'):unreal.unregister_slate_post_tick_callback(unreal._npcintegration_queue);del unreal._npcintegration_queue;out['queue']='removed'
# No global editor/project configuration is saved.
(I/'SessionCleanup.json').write_text(json.dumps(out,indent=2))
