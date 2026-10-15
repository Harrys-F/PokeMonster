import bpy,numpy as np,json,hashlib
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1'
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),link=False) as (a,b):b.scenes=['Hobbit_NPC_4K_Base_V1']
s=b.scenes[0];s.name='Hobbit_NPC_GameReady_Test_V1';bpy.context.window.scene=s
hp=next(o for o in s.objects if o.type=='MESH');hp.name='GRT_HighPoly_Reference';hp['role']='Unmodified complete artistic source; no rig'
m=hp.data;v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3);f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);f=f.reshape(-1,3)
uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3)
c=v[f].mean(1);head=c[:,2]>=1.105;torso=(c[:,2]>=.62)&(c[:,2]<1.105)&(np.abs(c[:,0])<=.36);rest=~(head|torso)
col=bpy.data.collections.new('GRT_LowPoly_Candidates');s.collection.children.link(col);ctx=bpy.data.collections.new('GRT_Untested_HighPoly_Context');s.collection.children.link(ctx)
metadata={}
for name,mask in [('HeadHair',head),('Torso',torso)]:
 idx=np.where(mask)[0];coords=v[f[idx]].reshape(-1,3);uniq,inv=np.unique(coords,axis=0,return_inverse=True);faces=inv.reshape(-1,3);mesh=bpy.data.meshes.new('GRT_'+name+'_Input');mesh.from_pydata(uniq,[],faces);mesh.update();o=bpy.data.objects.new('GRT_'+name,mesh);col.objects.link(o);o['role']='Bounded automatic retopology trial; not approved for animation';o['source_triangles']=len(idx)
 metadata[name]={'source_faces':len(idx),'source_unique_position_vertices':len(uniq),'selection':'Triangle centroid: z >= 1.105 m' if name=='HeadHair' else 'Triangle centroid: 0.62 <= z < 1.105 m and |x| <= 0.36 m; includes connected shoulder/collar/cape surface, not a garment separation','world_min':uniq.min(0).tolist(),'world_max':uniq.max(0).tolist()}
 np.savez_compressed(P/('Region_'+name+'.npz'),face_indices=idx)
idx=np.where(rest)[0];vertex_ids,inv=np.unique(f[idx],return_inverse=True);mesh=bpy.data.meshes.new('GRT_UnmodifiedContextMesh');mesh.from_pydata(v[vertex_ids],[],inv.reshape(-1,3));mesh.update();layer=mesh.uv_layers.new(name='UVMap');layer.data.foreach_set('uv',uv[idx].ravel());mesh.normals_split_custom_set(norm[idx].reshape(-1,3));mesh.materials.append(m.materials[0]);o=bpy.data.objects.new('GRT_UnmodifiedContext',mesh);ctx.objects.link(o);o['role']='Unoptimized context outside the two bounded test regions';o.hide_render=True
metadata['Context']={'triangles':len(idx),'vertices':len(vertex_ids),'not_optimized':True};metadata['complete_source']={'vertices':len(v),'triangles':len(f),'geometry_hash':hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest(),'uv_hash':hashlib.sha256(uv.tobytes()).hexdigest(),'normal_hash':hashlib.sha256(norm.tobytes()).hexdigest()}
for o in col.objects:o.hide_render=True
s.render.resolution_x=1100;s.render.resolution_y=1100;s.cycles.samples=24
(P/'RegionAnalysis.json').write_text(json.dumps(metadata,indent=2));bpy.data.libraries.write(str(B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'),{s},fake_user=True)
print(json.dumps(metadata,indent=2))
