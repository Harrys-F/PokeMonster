"""Reopen each rig-only source, append its clip to the unchanged reference, inspect and render."""
import bpy,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];label=sys.argv[sys.argv.index('--')+1]if'--'in sys.argv else'SprintValidation';assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;O.mkdir(exist_ok=False);rows=[]
for species,rig_name,body_name,height in [('Zunderlauf','Glumanda_Meshy_Rig','Glumanda_Meshy',.6),('Schiggy','Schiggy_Rig','Schiggy_Body',.5),('Bisasam','Bisasam_Rig','Bisasam_Body',.7)]:
 A=R/'Art/Characters/Creatures'/species;audit=json.loads((A/'OverworldSprint_AnimationAudit.json').read_text());source=R/audit['reference_source'];library=R/audit['rig_action_source'];sha=hashlib.sha256(library.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(library));assert len(bpy.data.actions)==1;assert len([o for o in bpy.data.objects if o.type=='ARMATURE'])==1;assert not any(o.type=='MESH'for o in bpy.data.objects);assert bpy.context.scene.render.fps==60
 bpy.ops.wm.open_mainfile(filepath=str(source))
 with bpy.data.libraries.load(str(library),link=False)as(data,loaded):loaded.actions=[species+'_OverworldSprint']
 rig=bpy.data.objects[rig_name];body=bpy.data.objects[body_name];rig.animation_data.action=loaded.actions[0];s=bpy.context.scene;s.render.fps=60;s.world=bpy.data.worlds.new('SprintInspectionWorld');s.world.color=(.18,.18,.18);s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=850;s.render.resolution_y=850;s.render.resolution_percentage=100
 for loc,power,size in [((1,-2,3),220,3),((-2,-1,2),140,2),((1,2,2),220,2)]:
  bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,height/2))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=height*1.75;cam.location=(1,-2,height*1.15);cam.rotation_euler=(Vector((0,0,height/2))-cam.location).to_track_quat('-Z','Y').to_euler()
 for frame in [4,10,16]:s.frame_set(frame);s.render.filepath=str(O/(species+'_'+str(frame)+'.png'));bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==audit['reference_source_sha256'];assert hashlib.sha256(library.read_bytes()).hexdigest()==sha
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(R/audit['fbx']));assert len(bpy.data.actions)==1;assert len([o for o in bpy.data.objects if o.type=='ARMATURE'])==1;rows.append({'species':species,'reference_unchanged':True,'reopened_rig_source':True,'fbx_reimported':True,'stance_error_m':audit['stance_increment_error_max_m'],'minimum_mesh_z_m':audit['mesh_min_z_m']})
(O/'Result.json').write_text(json.dumps({'passed':True,'rows':rows},indent=2))
