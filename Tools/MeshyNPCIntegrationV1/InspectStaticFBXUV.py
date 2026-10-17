import bpy,numpy as np,json
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');I=R/'Art/Characters/NPCs/IntegrationV1';out=[]
for id in ['SilverLady','TreeBeing','ElvenScholar','Wizard','DarkArmored','CrouchedCreature']:
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.ops.import_scene.fbx(filepath=str(R/'Art/Characters/NPCs'/id/'Exports'/('SM_'+id+'_Reference_V1.fbx')),use_anim=False)
 m=next(o.data for o in bpy.context.scene.objects if o.type=='MESH');m.calc_loop_triangles();ls=np.empty(len(m.loop_triangles)*3,np.int32);m.loop_triangles.foreach_get('loops',ls);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)[ls.reshape(-1,3)];a=uv[:,1]-uv[:,0];b=uv[:,2]-uv[:,0];det=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0]);out.append({'id':id,'triangles':len(m.loop_triangles),'UV_determinant_lt_1e_12':int((det<1e-12).sum()),'UV_determinant_lt_1e_8':int((det<1e-8).sum()),'nonfinite_uvs':int((~np.isfinite(uv)).sum()),'note':'Read-only exported derivative audit. No tangent warning suppressed.'});print('STATIC_FBX_UV',id,out[-1],flush=True)
(I/'StaticFBXUV.json').write_text(json.dumps(out,indent=2))
