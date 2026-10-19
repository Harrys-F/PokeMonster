"""Authored lathed ceramics, curved joinery and botanical worksets; no original model replaced."""
import bpy,math,json,bmesh,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'Art/HealingHouse';dst=A/'Source/HealingHouse_ApothecaryDetails.blend';assert not dst.exists();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mat=bpy.data.materials.new('HH_HandcraftedSurface');mat.use_nodes=True;n=mat.node_tree.nodes;p=n.get('Principled BSDF');v=n.new('ShaderNodeVertexColor');v.layer_name='Col';mat.node_tree.links.new(v.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.74
rng=random.Random(20261019);parts=[]
def mesh(name,vs,fs,color):
 m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(name,m);s.collection.objects.link(o);m.materials.append(mat);c=m.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for f in m.polygons:
  f.use_smooth=True
  for li in f.loop_indices:c.data[li].color=(*[v*rng.uniform(.94,1.06) for v in color],1)
 parts.append(o);return o
wood=(.19,.075,.025);sage=(.075,.18,.105);cream=(.63,.49,.29);blue=(.035,.13,.16);cork=(.24,.13,.055)
def lathe(name,profile,pos,color,N=24):
 vs=[];fs=[]
 for r,z in profile:
  for i in range(N):
   a=math.tau*i/N;vs.append((pos[0]+r*math.cos(a),pos[1]+r*math.sin(a),pos[2]+z))
 for j in range(len(profile)-1):
  for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 fs.extend([tuple(range(N-1,-1,-1)),tuple((len(profile)-1)*N+i for i in range(N))]);return mesh(name,vs,fs,color)
def box(name,pos,size,col,bevel=.007):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);c=o.data.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER')
 for d in c.data:d.color=(*col,1)
 mod=o.modifiers.new('Worn rounded edge','BEVEL');mod.width=bevel;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name);parts.append(o);return o
def leaf(pos,a,L,W,color):
 dr=Vector((math.cos(a),math.sin(a),.6));side=Vector((-math.sin(a),math.cos(a),0));vs=[]
 for j in range(7):
  t=j/6;ctr=Vector(pos)+dr*L*t+Vector((0,0,.018*math.sin(t*math.pi)))
  for k in [-1,0,1]:vs.append(tuple(ctr+side*W*math.sin(t*math.pi)*k+Vector((0,0,.006*(1-abs(k))*math.sin(t*math.pi)))))
 fs=[(j*3+k,(j+1)*3+k,(j+1)*3+k+1,j*3+k+1) for j in range(6) for k in range(2)];mesh('Medicinal leaf',vs,fs,color)
def finish(name):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
 # Preserve world-origin authored placement and use angle-based island UVs; no texture dependencies.
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False) if hasattr(bpy.ops.mesh,'normals_make_consistent') else None
 bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.025);bpy.ops.object.mode_set(mode='OBJECT');o.data.calc_loop_triangles()
 bpy.ops.export_scene.fbx(filepath=str(A/'Exports'/('SM_HH_'+name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False)
 data={'name':name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'dimensions_m':list(o.dimensions),'material_slots':len(o.data.materials)};parts=[];return data
out=[]
box('tray', (0,0,.014),(.46,.29,.028),wood)
for y in [-.145,.145]:box('tray lip',(0,y,.035),(.48,.018,.07),wood)
for x in [-.235,.235]:box('tray handle',(x,0,.037),(.018,.29,.074),wood)
for i,(x,y,h,col) in enumerate([(-.13,.045,.22,blue),(.0,.06,.17,sage),(.12,.055,.25,cream)]):
 r=.043 if i!=1 else .05
 lathe('glazed remedy jar',[(r*.75,0),(r,.012),(r,h*.57),(r*.66,h*.73),(r*.39,h*.81),(r*.39,h*.96),(r*.48,h*.97),(r*.48,h),(r*.31,h),(r*.31,h*.88)],(x,y,.03),col)
 lathe('cork',[(r*.34,0),(r*.39,.008),(r*.36,.029)],(x,y,.03+h),cork,N=16)
 box('paper label',(x,y-r-.001,.03+h*.35),(.045,.002,.045),cream,.001)
lathe('small ceramic bowl',[(.04,0),(.061,.015),(.077,.05),(.074,.055),(.066,.05),(.051,.019),(.025,.009)],(.085,-.075,.03),sage)
for i in range(9):leaf((.075,-.075,.065),rng.random()*math.tau,.07,.017,sage)
out.append(finish('HerbalRemedyTray'))
lathe('thick stone mortar',[(.065,0),(.083,.015),(.105,.115),(.10,.13),(.084,.13),(.072,.047),(.035,.029)],(0,0,0),(.24,.25,.20))
p=lathe('wood pestle',[(.015,0),(.022,.03),(.02,.07),(.011,.20),(.018,.23),(.014,.24)],(0,0,0),wood,N=16)
p.rotation_euler=(0,.72,.2);p.location=(.015,0,.06)
for i in range(12):leaf((rng.uniform(-.04,.04),rng.uniform(-.04,.04),.05),rng.random()*math.tau,.06,.015,sage)
out.append(finish('HerbalMortar'))
# Curved 45cm porch brace, an extruded hand-cut profile, not an intersection of cubes.
outline=[(0,0),(.07,0),(.07,.28),(.09,.33),(.14,.37),(.23,.40),(.39,.40),(.45,.40),(.45,.47),(0,.47)]
vs=[(x,y,z) for y in [-.035,.035] for x,z in outline];N=len(outline);fs=[tuple(range(N-1,-1,-1)),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
o=mesh('curved solid oak brace',vs,fs,wood);bpy.context.view_layer.objects.active=o;o.select_set(True);mod=o.modifiers.new('softened joinery','BEVEL');mod.width=.008;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
out.append(finish('PorchCorbel'))
for i,o in enumerate(bpy.data.objects):o.location.x=i*.8
bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.wm.open_mainfile(filepath=str(dst));assert len([o for o in bpy.data.objects if o.type=='MESH'])==3
(A/'ApothecaryDetails.json').write_text(json.dumps({'source':str(dst.relative_to(R)),'assets':out,'units':'metres','reopened':True,'rig':False},indent=2));print('APOTHECARY_REOPEN_OK',json.dumps(out))
