import bpy, numpy as np, json, hashlib, math
from pathlib import Path
from mathutils import Vector
B=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Art/Characters/NPCs/Westland/HobbitBase');P=B/'Review/Retopo_V2';O=B/'Source/Hobbit_NPC_Retopo_V2.blend'
assert not O.exists(), 'Do not overwrite an existing V2'
with bpy.data.libraries.load(str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),link=False) as (a,d):
 assert 'Hobbit_NPC_4K_Base_V1' in a.scenes
 d.scenes=['Hobbit_NPC_4K_Base_V1']
s=d.scenes[0];s.name='Hobbit_NPC_Retopo_V2';bpy.context.window.scene=s
old_children=list(s.collection.children)
collections={}
for name in ('HIGH_POLY_REFERENCE','RETOPO_BODY','RETOPO_HEAD','RETOPO_HAIR','RETOPO_CLOTHING','RETOPO_ACCESSORIES','BAKING','REVIEW'):
 c=bpy.data.collections.new(name);s.collection.children.link(c);collections[name]=c
hp=next(o for o in s.objects if o.type=='MESH');assert len([o for o in s.objects if o.type=='MESH'])==1
for o in list(s.objects):
 for c in list(o.users_collection):c.objects.unlink(o)
 collections['HIGH_POLY_REFERENCE' if o==hp else 'REVIEW'].objects.link(o)
for c in old_children:s.collection.children.unlink(c)
hp.name='RTV2_HP_REFERENCE_UNMODIFIED';hp.data.name='RTV2_HP_OriginalGeometry';hp.hide_select=True
hp['provenance']='Appended only from Hobbit_NPC_4K_Base_V1.blend; no geometry/UV/material edits'
hp['semantic_modules']=False
m=hp.data
v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3)
f=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',f);tri=f.reshape(-1,3)
uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers.active.data.foreach_get('uv',uv)
nm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',nm)
cohash=hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest();assert cohash=='80243ef20dff1efd193ca3c7b978ae5e428d4a38e0b7151842fc70047c2f0e77'
cent=v[tri].mean(axis=1)
regions={
 'head_hair_neck_candidate':cent[:,2]>=1.075,
 'front_face_candidate':(np.abs(cent[:,0])<.115)&(cent[:,1]<-.025)&(cent[:,2]>1.075)&(cent[:,2]<1.275),
 'upper_hair_candidate':cent[:,2]>=1.28,
 'torso_clothing_candidate':(np.abs(cent[:,0])<.36)&(cent[:,2]>=.62)&(cent[:,2]<1.075),
 'back_cape_candidate':(cent[:,1]>.04)&(cent[:,2]>.26)&(cent[:,2]<1.08)}
rows=[]
for label,mask in regions.items():
 ids=np.unique(tri[mask]);p=v[ids];rows.append({'label':label,'triangles':int(mask.sum()),'vertices_referenced':len(ids),'bounds_m':[p.min(axis=0).tolist(),p.max(axis=0).tolist()],'warning':'Overlapping spatial diagnostic candidate, NOT a semantic module or reliable cutting boundary.'})
mat=hp.data.materials[0];images=[]
for n in mat.node_tree.nodes:
 if n.type=='TEX_IMAGE' and n.image:
  im=n.image;images.append({'size':list(im.size),'colorspace':im.colorspace_settings.name,'packed':bool(im.packed_file),'sha256':hashlib.sha256(bytes(im.packed_file.data)).hexdigest() if im.packed_file else None})
# No generated head or failed V1 proxy: zero-face scaffold deliberately waits for manual loops.
mesh=bpy.data.meshes.new('RTV2_Head_EmptyScaffold');target=bpy.data.objects.new('RTV2_Head_MANUAL_RETOPO_REQUIRED',mesh);collections['RETOPO_HEAD'].objects.link(target)
mirror=target.modifiers.new('01_Mirror_X_START_CAGE_ONLY','MIRROR');mirror.use_clip=True;mirror.use_mirror_merge=True;mirror.merge_threshold=.0001
sw=target.modifiers.new('02_Surface_Conform_CHECK_HAIR_CONTACTS','SHRINKWRAP');sw.target=hp
sw.wrap_method=next(i.identifier for i in bpy.types.ShrinkwrapModifier.bl_rna.properties['wrap_method'].enum_items if i.identifier=='NEAREST_SURFACEPOINT');sw.offset=.0005
sw.show_in_editmode=True;target.show_in_front=True;target.color=(.04,.65,.3,1)
target['status']='Empty manual modeling scaffold; NOT a retopologized head; no eye/mouth loops yet'
target['projection_warning']='Nearest-surface can hit bangs/ears/cloth. Disable per area or use a manually validated projection target; never Apply blindly.'
rt=bpy.data.materials.new('RTV2_Retopo_Green');rt.use_nodes=True;bs=next(n for n in rt.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.035,.45,.18,1);bs.inputs['Roughness'].default_value=.85;rt.diffuse_color=(.04,.65,.3,1);mesh.materials.append(rt)
t=s.tool_settings;t.use_snap=True
snap=[i.identifier for i in bpy.types.ToolSettings.bl_rna.properties['snap_elements'].enum_items];t.snap_elements={next(x for x in snap if x=='FACE')}
for key,value in [('use_snap_project',True),('use_snap_to_nonedit',True),('use_snap_to_selectable',False),('use_snap_align_rotation',False)]:
 if hasattr(t,key):setattr(t,key,value)
t.snap_target=next(i.identifier for i in bpy.types.ToolSettings.bl_rna.properties['snap_target'].enum_items if i.identifier=='CLOSEST')
s.unit_settings.system=next(i.identifier for i in bpy.types.UnitSettings.bl_rna.properties['system'].enum_items if i.identifier=='METRIC');s.unit_settings.scale_length=1
s.render.filepath=str(P/'Previews/ManualWorkspace_Render.png');s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.cycles.samples=12;s.cycles.use_denoising=True;s.render.threads_mode=next(i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['threads_mode'].enum_items if i.identifier=='FIXED');s.render.threads=3
views=[('Front',(0,-2,1.205),(0,0,1.205),.43),('Right',(2,0,1.205),(0,0,1.205),.43),('Left',(-2,0,1.205),(0,0,1.205),.43),('ThreeQuarter',(1.25,-2,1.32),(0,0,1.205),.46),('2_5D_Close',(2.5,-2.5,4.9),(0,0,.7),1.82)]
cams=[]
for name,loc,aim,size in views:
 data=bpy.data.cameras.new('RTV2_'+name);cam=bpy.data.objects.new('RTV2_Camera_'+name,data);collections['REVIEW'].objects.link(cam)
 data.type=next(i.identifier for i in bpy.types.Camera.bl_rna.properties['type'].enum_items if i.identifier=='ORTHO');data.ortho_scale=size;cam.location=loc;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cams.append(cam)
s.camera=cams[0]
for o in s.objects:
 if o.type in ('LIGHT','CAMERA'):o.hide_set(True)
# hide_set affects viewport only, lights/cameras remain available for renders.
for o in s.objects:
 if o.select_get():o.select_set(False)
target.select_set(True);s.view_layers[0].objects.active=target
s['retopology_status']='MANUAL_WORKSPACE_ONLY_NO_VALID_HEAD_PILOT';s['animation_ready']=False;s['baked_target_materials']=False
s['orientation']='Front = negative Y, height = Z, symmetry = X'
readme=bpy.data.texts.new('RTV2_START_HERE')
readme.write('Manual retopology workspace; NOT finished head topology.\nSource locked and unchanged. Empty target with Mirror X + Shrinkwrap 0.5 mm.\nFront is -Y (NumPad1). Camera checks are in REVIEW.\nRead Review/Retopo_V2/MANUELLE_RETOPO_ANLEITUNG.md before editing.\nNo failed triangle mesh loaded. No UVs or bakes for the new target.\nNearest-surface projection may hit bangs. Check in profile before every extension.\nMirror is a start tool only: the source has asymmetric hair/face details.\n')
# A real dedicated workspace; do not replace user's previous screens/scenes.
try:
 bpy.ops.workspace.duplicate();bpy.context.workspace.name='Hobbit Retopo V2'
except Exception as e:print('WORKSPACE_DUPLICATE_WARNING',repr(e))
from mathutils import Quaternion
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  space=area.spaces.active;space.region_3d.view_rotation=Quaternion((1,0,0),math.pi/2);space.region_3d.view_perspective='ORTHO';space.region_3d.view_location=(0,0,1.205);space.region_3d.view_distance=.7
  space.clip_start=.001;space.clip_end=100;space.shading.color_type='MATERIAL';space.overlay.show_floor=False;space.overlay.show_axis_x=False;space.overlay.show_axis_y=False;space.overlay.show_text=True
info={'source':str(B/'Source/Hobbit_NPC_4K_Base_V1.blend'),'target':str(O),'status':s['retopology_status'],'vertices':len(m.vertices),'edges':len(m.edges),'triangles':len(m.polygons),'materials':len(m.materials),'uv_layers':[u.name for u in m.uv_layers],'geometry_hash':cohash,'uv_hash':hashlib.sha256(uv.tobytes()).hexdigest(),'normal_hash':hashlib.sha256(nm.tobytes()).hexdigest(),'bounds_m':[v.min(axis=0).tolist(),v.max(axis=0).tolist()],'images':images,'spatial_candidates':rows,'target_geometry':{'vertices':0,'faces':0,'triangles':0,'eye_loops':0,'mouth_loops':0},'collections':list(collections),'snap':{'enabled':t.use_snap,'elements':list(t.snap_elements),'project_individual':getattr(t,'use_snap_project',None)},'modifiers':[{'name':a.name,'type':a.type} for a in target.modifiers],'cameras':[o.name for o in cams]}
(P/'WorkspaceAudit.json').write_text(json.dumps(info,indent=2))
bpy.data.libraries.write(str(O),{s,readme},fake_user=True)
print(json.dumps(info,indent=2))
