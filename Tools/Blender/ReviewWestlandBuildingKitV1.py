"""Reopen the explicitly saved source; validate modules and render without saving."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];ART=ROOT/'Art/Architecture/Westland';OUT=ROOT/'Saved/WestlandKitV1'
assert bpy.app.background and Path(bpy.data.filepath)==ART/'Source/WestlandBuildingKit_V1.blend'
kit=json.loads((ART/'WestlandBuildingKit_V1.json').read_text());layout=json.loads((ART/'Buildings/WL_Cottage_V1.json').read_text())
assert not any(x.library for x in bpy.data.objects) and not any(x.library for x in bpy.data.materials)
for m in kit['modules']:
 o=bpy.data.objects[m['mesh']];assert tuple(o.scale)==(1,1,1) and Vector(o.rotation_euler).length<.0001 and o.location.length<.0001
 assert o.data.materials and all(o.data.materials)
 bm=bmesh.new();bm.from_mesh(o.data);nm=sum(not e.is_manifold for e in bm.edges);bm.free();assert nm==0,(m['name'],nm)
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=1280;scene.render.resolution_y=960;scene.render.resolution_percentage=100
scene.world.use_nodes=True;bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.5,.6,.7,1);bg.inputs['Strength'].default_value=.7
for n,p,power,size in [('Key',(-10,12,15),1800,10),('Fill',(7,-4,10),900,8)]:
 data=bpy.data.lights.new(n,'AREA');data.energy=power;data.shape='DISK';data.size=size
 o=bpy.data.objects.new(n,data);scene.collection.objects.link(o);o.location=p;o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
c=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));scene.collection.objects.link(c);scene.camera=c;c.data.angle=math.radians(35)
bpy.ops.mesh.primitive_plane_add(size=40,location=(0,0,-.20));ground=bpy.context.object;mat=bpy.data.materials.new('ReviewGround');mat.diffuse_color=(.24,.30,.18,1);ground.data.materials.append(mat)
def shot(name,pos,target,cutaway=False):
 for p in layout['placements']:bpy.data.objects[p['label']].hide_render=cutaway and p['cutaway']
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
shot('Blender_Exterior',(-12,12,16),(0,0,1.6));shot('Blender_Rear',(12,-12,12),(0,0,1.8));shot('Blender_Interior',(-10,10,14),(0,0,.3),True)
(OUT/'BlenderValidation.json').write_text(json.dumps({'reopened':True,'source':str(bpy.data.filepath),'modules':len(kit['modules']),'manifold':True,'origins_applied':True,'materials_complete':True,'external_library_links':0,'placements':len(layout['placements']),'source_not_resaved':True},indent=2)+'\n')
print('WESTLAND_SOURCE_REOPEN_VALIDATED')
