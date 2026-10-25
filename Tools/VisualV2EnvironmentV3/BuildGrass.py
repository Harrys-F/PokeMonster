"""Deterministic curved, opaque grass blades in metres; reusable source, no texture cards."""
import bpy,math,random,json
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');A=R/'Art/World/VisualV2EnvironmentV3';A.mkdir(parents=True,exist_ok=True);(A/'Exports').mkdir(exist_ok=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
mat=bpy.data.materials.new('Grass_VertexPalette');mat.diffuse_color=(.19,.29,.06,1)
rows=[]
for variant,count,height,radius in [('Short',28,.18,.20),('Meadow',37,.29,.29),('Woodland',31,.35,.25)]:
 rng=random.Random(251003+count);vs=[];faces=[];colors=[];uv=[]
 for blade in range(count):
  angle=rng.uniform(0,math.tau);r=radius*math.sqrt(rng.random());x=math.cos(angle)*r;y=math.sin(angle)*r;h=height*rng.uniform(.50,1.12);direction=angle+rng.uniform(-.7,.7);dx,dy=math.cos(direction),math.sin(direction);wx,wy=-dy,dx;width=rng.uniform(.012,.027);lean=rng.uniform(.18,.65)*h;start=len(vs);tone=rng.uniform(.78,1.18)
  for k in range(5):
   t=k/4;cx=x+dx*lean*t*t;cy=y+dy*lean*t*t;z=h*(t-.13*t*t*t);w=width*(1-t)**.72
   for side in [-1,0,1]:
    vs.append((cx+wx*w*side,cy+wy*w*side,z+(1-abs(side))*.004*math.sin(math.pi*t)));uv.append(((side+1)/2,t));colors.append((tone*(.105+.11*t),tone*(.18+.15*t),tone*(.035+.035*t),1))
  for k in range(4):
   for side in range(2):
    a=start+k*3+side;b=a+1;c=a+3;d=c+1;faces.extend([(a,b,d),(a,d,c)])
 mesh=bpy.data.meshes.new('Grass_'+variant);mesh.from_pydata(vs,[],faces);mesh.update();obj=bpy.data.objects.new('SM_EQ3_Grass'+variant,mesh);bpy.context.collection.objects.link(obj);mesh.materials.append(mat);attr=mesh.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='CORNER');layer=mesh.uv_layers.new(name='UVMap')
 for poly in mesh.polygons:
  poly.use_smooth=True
  for loop in poly.loop_indices:
   vi=mesh.loops[loop].vertex_index;attr.data[loop].color=colors[vi];layer.data[loop].uv=uv[vi]
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 out=A/'Exports'/(obj.name+'.fbx');assert not out.exists();bpy.ops.export_scene.fbx(filepath=str(out),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',mesh_smooth_type='FACE',bake_anim=False)
 rows.append({'mesh':obj.name,'triangles':len(faces),'vertices':len(vs),'height_cm':max(v[2]for v in vs)*100,'blade_count':count})
source=A/'VisualV2_Grass.blend';assert not source.exists();bpy.ops.wm.save_as_mainfile(filepath=str(source));(A/'GrassGeometry.json').write_text(json.dumps(rows,indent=2));print(rows)
