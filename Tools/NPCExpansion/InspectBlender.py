"""Inspect existing runtime exports, not the multi-million-polygon Incoming originals."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path('/Users/harry/Developer/PokeMonster');O=R/'Saved/ProjectRefinement/NPCExpansion/SourceViews';O.mkdir(parents=True,exist_ok=True)
configs=json.loads((R/'Art/Characters/NPCs/IntegrationV1/Characters.json').read_text());rows=[]
for a in configs:
 id=a['id'];C=R/'Art/Characters/NPCs'/id;source=C/'Exports'/('SM_'+id+'_Reference_V1.fbx')
 if id=='Ranger':source=C/'Exports/SK_Ranger_NPC_V1.fbx'
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;bpy.ops.import_scene.fbx(filepath=str(source));s=bpy.context.scene
 models=[x for x in s.objects if x.type=='MESH'];assert len(models)==1;obj=models[0]
 for image in bpy.data.images:
  if image.source=='FILE' and image.users:
   p=C/'Textures'/Path(image.filepath.replace('\\','/')).name
   if p.is_file():image.filepath=str(p);image.reload()
 co=[obj.matrix_world@v.co for v in obj.data.vertices];lo=Vector(tuple(min(v[i] for v in co) for i in range(3)));hi=Vector(tuple(max(v[i] for v in co) for i in range(3)));h=hi.z-lo.z
 rows.append({'id':id,'source':str(source.relative_to(R)),'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons),'bounds':[list(lo),list(hi)],'armatures':len([x for x in s.objects if x.type=='ARMATURE']),'materials':[m.name if m else None for m in obj.data.materials]})
 s.world=bpy.data.worlds.new('InspectionWorld');s.world.color=(.16,.16,.16)
 for loc,power in [((-3,-4,5),700),((3,-1,3),450),((0,3,4),500)]:
  d=bpy.data.lights.new('Inspection','AREA');d.energy=power;d.size=4;v=bpy.data.objects.new('Inspection',d);s.collection.objects.link(v);v.location=Vector(loc)*max(1,h/2);v.rotation_euler=(Vector((0,0,h*.5))-v.location).to_track_quat('-Z','Y').to_euler()
 d=bpy.data.cameras.new('Inspection');c=bpy.data.objects.new('Inspection',d);s.collection.objects.link(c);s.camera=c;d.type='ORTHO';d.ortho_scale=max(h*1.2,hi.x-lo.x+ .1);s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3;s.render.resolution_x=560;s.render.resolution_y=650;s.render.resolution_percentage=100
 for label,loc in [('Front',(0,-h*3,h*.53)),('Side',(h*3,0,h*.53))]:
  c.location=loc;c.rotation_euler=(Vector((0,0,h*.5))-c.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(id+'_'+label+'.png'));bpy.ops.render.render(write_still=True)
 print('INSPECTED',id,flush=True)
(O/'Sources.json').write_text(json.dumps(rows,indent=2))
