import bpy,numpy as np,json,shutil
from pathlib import Path
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/GameReady_Test_V1';archive=P/'FirstBakeFailure';archive.mkdir(exist_ok=False);s=bpy.data.scenes['Hobbit_NPC_GameReady_Test_V1'];bpy.context.window.scene=s
for p in (B/'Textures/GameReady_Test_V1').glob('*.png'):shutil.copy2(p,archive/p.name)
for p in (P/'Previews').glob('*B_TriangleControl.png'):shutil.copy2(p,archive/p.name)
for p in ['BakeTrial.json','TechnicalAudit.json','BakeDiagnosis.json']:
 if (P/p).exists():shutil.copy2(P/p,archive/p)
q={}
for name in ['HeadHair','Torso']:
 o=s.objects['GRT_'+name]
 for obj in s.objects:obj.select_set(False)
 o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.mode_set(mode=next(i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items if i.identifier=='EDIT'));bpy.ops.mesh.select_all(action=next(i.identifier for i in bpy.ops.mesh.select_all.get_rna_type().properties['action'].enum_items if i.identifier=='SELECT'))
 margin=next(i.identifier for i in bpy.ops.uv.smart_project.get_rna_type().properties['margin_method'].enum_items if i.identifier=='FRACTION');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=4/2048,margin_method=margin,area_weight=.4,scale_to_bounds=True)
 bpy.ops.object.mode_set(mode=next(i.identifier for i in bpy.ops.object.mode_set.get_rna_type().properties['mode'].enum_items if i.identifier=='OBJECT'))
 uv=np.empty(len(o.data.loops)*2,np.float32);o.data.uv_layers.active.data.foreach_get('uv',uv);u=uv.reshape(-1,3,2);cross=(u[:,1,0]-u[:,0,0])*(u[:,2,1]-u[:,0,1])-(u[:,1,1]-u[:,0,1])*(u[:,2,0]-u[:,0,0]);q[name]={'angle_limit_rad':1.15,'margin_method':margin,'margin_uv':4/2048,'area_weight':.4,'scale_to_bounds':True,'uv_area_sum':float(np.abs(cross).sum()*.5)}
 for mat in list(o.data.materials):
  o.data.materials.clear()
  if mat.users==0:bpy.data.materials.remove(mat)
for im in list(bpy.data.images):
 if im.name.startswith('GRT_') and im.users==0:bpy.data.images.remove(im)
(P/'FixedUV.json').write_text(json.dumps(q,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(B/'Source/Hobbit_NPC_GameReady_Test_V1.blend'));print(json.dumps(q,indent=2),flush=True)
