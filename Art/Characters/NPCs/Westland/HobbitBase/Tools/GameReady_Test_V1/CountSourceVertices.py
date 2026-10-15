import bpy,numpy as np,json
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';m=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'].objects['GRT_HighPoly_Reference'].data;f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3);q={}
for name in ['HeadHair','Torso']:
 idx=np.load(P/('Region_'+name+'.npz'))['face_indices'];q[name]={'source_vertex_ids':len(np.unique(f[idx])),'source_triangles':len(idx)}
(P/'SourceVertexCounts.json').write_text(json.dumps(q,indent=2));print(q)
