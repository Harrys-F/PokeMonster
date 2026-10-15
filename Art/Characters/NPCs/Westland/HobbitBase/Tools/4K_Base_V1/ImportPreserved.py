import bpy,json,math
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase')
S=bpy.data.scenes.new('Hobbit_NPC_4K_Base_V1');bpy.context.window.scene=S
S.unit_settings.system=next(i.identifier for i in bpy.types.UnitSettings.bl_rna.properties['system'].enum_items if i.identifier=='METRIC');S.unit_settings.scale_length=1
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(B/'Incoming/4K_Base_V1/Meshy_Hobbit.glb'))
model=[o for o in bpy.data.objects if o not in before];meshes=[o for o in model if o.type=='MESH']
col=bpy.data.collections.new('H4K_Original_Import');S.collection.children.link(col)
for o in model:
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
 o['source_GLΒ']='Meshy_Hobbit.glb';o['preserved_import']=True
points=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box];lo=Vector([min(v[i] for v in points) for i in range(3)]);hi=Vector([max(v[i] for v in points) for i in range(3)]);h=hi.z-lo.z;center=(lo+hi)/2
imgs=set()
for o in meshes:
 for m in o.data.materials:
  if m and m.use_nodes:
   for n in m.node_tree.nodes:
    if n.type=='TEX_IMAGE' and n.image:imgs.add(n.image)
for im in imgs:
 if not im.packed_file:im.pack()
 if not im.filepath:im.filepath='//../Textures/4K_Base_V1/'+im.name+'.jpg'
 for pf in im.packed_files:pf.filepath=im.filepath
studio=bpy.data.collections.new('H4K_Review_Studio');S.collection.children.link(studio)
world=bpy.data.worlds.new('H4K_StudioWorld');world.use_nodes=True;S.world=world
bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(.19,.215,.25,1);bg.inputs['Strength'].default_value=.35
camd=bpy.data.cameras.new('H4K_ReviewCamera');cam=bpy.data.objects.new('H4K_ReviewCamera',camd);studio.objects.link(cam);S.camera=cam
camd.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO');camd.ortho_scale=max(h,(hi.x-lo.x))*1.25;camd.clip_start=max(.0001,h*.001);camd.clip_end=h*100
cam.location=center+Vector((0,-h*4,0));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
for name,offset,energy,size in [('Key',(-2,-3,3),180,2),('Fill',(2,-1,1.8),100,2.2),('Rim',(1,2,2.6),160,1.6)]:
 d=bpy.data.lights.new('H4K_'+name,next(i.identifier for i in bpy.types.Light.bl_rna.properties['type'].enum_items if i.identifier=='AREA'));d.energy=energy*h*h;d.shape=next(i.identifier for i in bpy.types.AreaLight.bl_rna.properties['shape'].enum_items if i.identifier=='DISK');d.size=size*h
 o=bpy.data.objects.new(d.name,d);studio.objects.link(o);o.location=center+Vector(offset)*h;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
try:S.render.engine='CYCLES'
except TypeError as e:print(e);raise
S.cycles.samples=20;S.cycles.use_denoising=True;S.render.resolution_x=1100;S.render.resolution_y=1100;S.render.resolution_percentage=100
S.render.image_settings.file_format=next(i.identifier for i in bpy.types.ImageFormatSettings.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG')
S.render.filepath=str(B/'Review/4K_Base_V1/Previews/01_Front.png');S.render.film_transparent=False
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  a.spaces.active.region_3d.view_location=center;a.spaces.active.region_3d.view_distance=h*2
stats={'scene':S.name,'objects':[{'name':o.name,'type':o.type,'matrix_world':[list(row) for row in o.matrix_world]} for o in model], 'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'edges':len(o.data.edges),'polygons':len(o.data.polygons),'uv_layers':[l.name for l in o.data.uv_layers],'custom_normals':o.data.has_custom_normals} for o in meshes],'world_min':list(lo),'world_max':list(hi),'height_m':h,'dimensions_m':list(hi-lo),'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file),'colorspace':im.colorspace_settings.name,'filepath':im.filepath} for im in imgs]}
(B/'Review/4K_Base_V1/ImportResult.json').write_text(json.dumps(stats,indent=2))
bpy.data.libraries.write(str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),{S},fake_user=True)
print(json.dumps(stats,indent=2))
