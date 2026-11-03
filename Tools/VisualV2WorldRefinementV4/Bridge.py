"""Bevelled existing timber modules, real bearings and connected rails; original deck collision retained."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/MaterialHelpers.py')));assert not(D/'Bridge.json').exists()
m=unreal.EditorAssetLibrary.duplicate_asset(material('Timber').get_path_name(),ROOT+'/Materials/M_WR4_BridgeDeck');assert m
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom):
  code=n.get_editor_property('code')
  if 'a.z>.55?P.xy'in code:n.set_editor_property('code',code.replace('a.z>.55?P.xy','a.z>.55?P.yx'))
finish(m)
path='/Game/Environment/Architecture/Westland/Meshes/Timber/SM_WL_HorizontalBeam2m';planks=group('BridgeDeckBoards',path,[m]);posts=group('BridgePosts',path,[material('Timber')]);rails=group('BridgeRails',path,[material('Timber')]);supports=group('BridgeBearings','/Engine/BasicShapes/Cube',[material('Stone')]);caps=group('BridgeCaps','/Engine/BasicShapes/Cube',[material('Timber')]);pegs=group('BridgePegs','/Engine/BasicShapes/Cylinder',[material('Iron')],False)
old=[]
for label,a in actors.items():
 if label.startswith('VS_BridgePlank'):
  c=a.static_mesh_component;p=a.get_actor_location();sz=a.get_actor_scale3d();a.modify();c.set_visibility(False,False);centred(planks,(p.x,p.y,21.75),(sz.y*100,sz.x*100,4.5),unreal.Rotator(yaw=90));old.append(label)
 elif label.startswith('VS_BridgePost'):
  c=a.static_mesh_component;p=a.get_actor_location();sz=a.get_actor_scale3d();a.modify();c.set_visibility(False,False);centred(posts,p.to_tuple(),(sz.x*100,sz.z*100,sz.y*100),unreal.MathLibrary.make_rot_from_y(unreal.Vector(0,0,1)));centred(caps,(p.x,p.y,p.z+sz.z*50+2),(12,12,4));old.append(label)
 elif label.startswith('VS_BridgeRail'):
  c=a.static_mesh_component;p=a.get_actor_location();sz=a.get_actor_scale3d();a.modify();c.set_visibility(False,False);centred(rails,p.to_tuple(),(sz.x*100,sz.y*100,sz.z*100));old.append(label)
 elif label.startswith(('WOV3_BridgeStringer','WOV3_BridgeBrace')):
  a.modify();a.static_mesh_component.set_visibility(False,False);old.append(label)
 elif label.startswith('WOV3_BridgeApproach'):
  a.modify();a.static_mesh_component.set_material(0,material('Timber'))
def beam(a,b,w=10,h=None):
 a=unreal.Vector(*a);b=unreal.Vector(*b);v=b-a;centred(rails,((a+b)*.5).to_tuple(),(w,v.length(),w if h is None else h),unreal.MathLibrary.make_rot_from_y(v))
for x in[-416,-284]:beam((x,-432,12),(x,-208,12),12,14)
for y in[-435,-205]:centred(supports,(-350,y,-3.5),(174,28,17))
for x in[-435.49,-264.51]:
 beam((x,-410,60),(x,-230,60),6,8)
 for ya,yb in[(-407.5,-320),(-232.5,-320)]:beam((x,ya,29),(x,yb,83),5.5,6.5)
 for y in[-407.5,-320,-232.5]:
  for z in[60,100]:centred(pegs,(x+(-5 if x<-350 else 5),y,z),(3,3,1.8),unreal.Rotator(pitch=90))
save('Bridge.json',dict(hidden_replaced_visuals=old,original_deck_and_rail_collision_preserved=True,deck_top_cm=24,water_cm=4.4,bearings_top_cm=5,stringer_bottom_cm=5,deck_width_cm=170,span_cm=210))
