"""Fit approved V4 timber modules to the actual 16m regional span and original deck collider."""
import unreal,runpy,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/Common.py')));assert not(D/'Bridge.json').exists();bridge=actors['WR_Holzbruecke'];deck=actors['WR_Holzbruecke_Deck'].get_component_by_class(unreal.StaticMeshComponent);floor=deck.get_world_location().z+deck.get_world_scale().z*50;frame=bridge.get_actor_transform();z=floor-bridge.get_actor_location().z;mesh='/Game/Environment/Architecture/Westland/Meshes/Timber/SM_WL_HorizontalBeam2m';timber='/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Timber';stone='/Game/Environment/VisualV2WorldRefinementV4/Materials/M_WR4_Stone';boards=group('Bridge_DeckBoards',mesh,[timber],True);structure=group('Bridge_Structure',mesh,[timber],True);bearings=group('Bridge_Bearings','/Engine/BasicShapes/Cube',[stone],True)
def world(p):return unreal.MathLibrary.transform_location(frame,unreal.Vector(*p))
def beam(c,a,b,width,height=None):
 a=world(a);b=world(b);v=b-a;box=c.static_mesh.get_bounding_box();size=box.max-box.min;rot=unreal.MathLibrary.make_rot_from_yz(v,unreal.Vector(0,0,1));t=unreal.Transform(rotation=rot,scale=unreal.Vector(width/size.x,v.length()/size.y,(width if height is None else height)/size.z));t.translation=(a+b)*.5-unreal.MathLibrary.transform_location(t,(box.min+box.max)*.5);c.add_instance(t,True)
for i in range(76):
 x=-800+(i+.5)*1600/76;beam(boards,(x,-125,z-2.25),(x,125,z-2.25),1600/76-.4,4.5)
for y in [-90,90]:beam(structure,(-800,y,z-14.5),(800,y,z-14.5),18,20)
for y in [-132,132]:
 for x in [-775,-517,-258,0,258,517,775]:beam(structure,(x,y,z-4.5),(x,y,z+100),12)
 for h in [50,94]:beam(structure,(-782,y,z+h),(782,y,z+h),7,9)
 xs=[-775,-517,-258,0,258,517,775]
 for a,b in zip(xs,xs[1:]):beam(structure,(a,y,z+35),(b,y,z+89),6)
for x in [-775,775]:
 # Recessed regional bearings meet the original banks; no additional floor/collision layer.
 t=unreal.Transform(location=world((x,0,z-48)),rotation=frame.rotation.rotator(),scale=unreal.Vector(.65,3.0,.6));bearings.add_instance(t,True)
bridge.modify();bridge.get_component_by_class(unreal.StaticMeshComponent).set_visibility(False,False);deck.get_owner().modify();deck.set_visibility(False,False)
finish('Bridge.json',dict(original_bridge=bridge.get_actor_label(),original_collision=deck.get_owner().get_actor_label(),floor_world_z=floor,span_cm=1600,width_cm=250,planks=boards.get_instance_count(),original_colliders_retained=True,geometry_sources=[mesh,'/Engine/BasicShapes/Cube'],new_visual_collision=False))
