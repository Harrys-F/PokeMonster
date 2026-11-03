"""Irregular whole-map compositions; no spawn/AI edits and no source models modified."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert not(D/'Vegetation.json').exists()
assert not any(k.startswith('WOV3_Grass_')for k in actors),'Vegetation already exists; do not rerun'
# Tone down the previously overbright Fab shrubs through a private parent graph.
old=unreal.load_asset('/Game/Environment/VisualV2FabAssetTrialV1/Materials/MI_FAT_Shrubs');master=unreal.EditorAssetLibrary.duplicate_asset(old.parent.get_path_name(),ROOT+'/Materials/M_WOV_ShrubMaster');assert master;src=ML.get_material_property_input_node(master,unreal.MaterialProperty.MP_BASE_COLOR);pin=ML.get_material_property_input_node_output_name(master,unreal.MaterialProperty.MP_BASE_COLOR);assert src;n=ML.create_material_expression(master,unreal.MaterialExpressionCustom);n.set_editor_property('code','float g=dot(C,float3(.299,.587,.114));float leaf=saturate((C.g-max(C.r,C.b)) * 6);return lerp(C,g*float3(.55,.80,.39),leaf*.62)*.88;');n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3);i=unreal.CustomInput();i.set_editor_property('input_name','C');n.set_editor_property('inputs',[i]);assert ML.connect_material_expressions(src,pin,n,'C');assert ML.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR);ML.recompile_material(master);assert unreal.EditorAssetLibrary.save_loaded_asset(master,False);mi=unreal.EditorAssetLibrary.duplicate_asset(old.get_path_name(),ROOT+'/Materials/MI_WOV_Shrubs');ML.set_material_instance_parent(mi,master);assert unreal.EditorAssetLibrary.save_loaded_asset(mi,False)
a=actors['FAT_FabShrubs'];a.modify();c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);c.set_material(0,mi)
for j in range(c.get_instance_count()):
 t=c.get_instance_transform(j,True);b=c.static_mesh.get_bounding_box();oldz=t.translation.z+b.min.z*t.scale3d.z;t.scale3d=t.scale3d*.8;t.translation=unreal.Vector(t.translation.x,t.translation.y,oldz-b.min.z*t.scale3d.z);c.update_instance_transform(j,t,True,j==c.get_instance_count()-1,True)
changes.append(dict(actor=a.get_name(),label=a.get_actor_label(),kind='own subdued leaf material and 20 percent smaller shrubs, preserve all instances'))
# Nine composition zones cover the existing main world, not only six showcases.
sections=[('SW',-4550,-2450,1000,450),('SC',-1900,-2250,1150,650),('SE',2150,-2000,550,800),('MW',-5050,-150,450,900),('MC',-2100,200,650,700),('ME',1750,-50,700,750),('NW',-4800,1900,950,750),('NC',-2550,2350,1200,400),('NE',1650,2000,950,700)]
flower=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Meshes/Vegetation/SM_WLA_Wildflowers_A');pal=['Cream','Yellow','Blue','Violet','Red','Pink'];placed={}
for key,cx,cy,rx,ry in sections:
 count=0
 for j in range(480):
  x=cx+rng.uniform(-rx,rx);y=cy+rng.uniform(-ry,ry)
  if not safe(x,y):continue
  island=math.sin(x*.008+math.sin(y*.003))*math.cos(y*.006)
  if island<-.2:continue
  f=forest(x,y)
  if f>.35 and j%5<2:
   var='A'if j%2 else'B';c=group('Ferns'+var,'/Game/Fab/VisualV2TrialLocal/Plants/SM_FAT_Fern'+var);h=rng.uniform(32,62)
  elif j%4==0:
   color=pal[(j//9+len(key))%len(pal)];ms=[s.material_interface for s in flower.static_materials];ms[1]=ROOT+'/Materials/MI_WOV_Flower_'+color;ms[2]=ROOT+'/Materials/MI_WOV_Flower_'+('Cream'if j%2 else'Yellow');c=group('Flowers_'+color,flower.get_path_name(),ms);h=rng.uniform(28,53)
  else:
   var='Woodland'if f>.35 else('Short'if j%3 else'Meadow');c=group('Grass_'+var,'/Game/Environment/VisualV2EnvironmentV3/Meshes/SM_EQ3_Grass'+var);h=rng.uniform(19,35)if var=='Short'else rng.uniform(25,44)
  put(c,x,y,h);count+=1
 placed[key]=count
# Several existing tree species in small uneven groups; paths and camera corridors stay free.
for j,(cx,cy)in enumerate([(-5450,2450),(-5100,2200),(-4400,2500),(-3750,2700),(-2500,2700),(-1450,2450),(1900,2450),(2400,1900),(2300,900),(2400,-500),(2300,-1000),(-5550,900)]):
 if not safe(cx,cy,390):continue
 name=['Birch_A','Birch_B','OakYoung_B','FruitTree_A'][j%4];path='/Game/Environment/WestlandAssetLibrary/Meshes/Trees/SM_WLA_'+name;c=group('Trees_'+name,path,shadow=True);put(c,cx,cy,rng.uniform(430,620));col=group('TreeTrunkCollision','/Engine/BasicShapes/Cylinder',shadow=False,collision='BlockAll');t=unreal.Transform(location=unreal.Vector(cx,cy,height(cx,cy)+90),scale=unreal.Vector(.32,.32,1.8));col.add_instance(t,True);col.set_visibility(False);col.set_hidden_in_game(True)
# Sparse path shoulders, kept out of walkable centres; real existing centimetre pebbles.
for j in range(200):
 a,b=segments[j%len(segments)];t=rng.random();dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy);side=rng.choice([-1,1]);d=rng.uniform(155,215);x=a[0]+t*dx-side*dy/ln*d;y=a[1]+t*dy+side*dx/ln*d
 if not safe(x,y,140):continue
 c=group('PathPebbles'+str(j%3+1),'/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_'+str(j%3+1));put(c,x,y,rng.uniform(4,10))
# Water-bank composition, all along both banks and around the whole pond.
for j in range(270):
 if j<150:x=rng.uniform(-940,1130);y=-320+rng.choice([-1,1])*rng.uniform(85,135)
 else:
  angle=rng.uniform(0,math.tau);x=720+math.cos(angle)*rng.uniform(925,1000);y=-1800+math.sin(angle)*rng.uniform(675,730)
 if -540<x<-170 and abs(y+320)<220:continue
 c=group('BankSmallStone'+str(j%5+1),'/Game/RockEnv_Pack/Meshes/Small_Rocks/SM_Small_Rock_'+str(j%5+1));put(c,x,y,rng.uniform(4,12),z=0)
 if j%3==0:
  c=group('BankPratia','/Game/Fab/VisualV2TrialLocal/PolishV2/Pratia/SM_EP2_PratiaA');put(c,x,y,rng.uniform(8,13),z=0)
# Rounded embedded outcrops frame hills and the eastern margin, no random grey boulder carpet.
for j,(cx,cy)in enumerate([(-1130,1350),(-900,1450),(-620,1400),(2100,2500),(2350,2100),(2400,-2700),(-5450,-2750)]):
 if not safe(cx,cy,230):continue
 path='/Game/Fab/VisualV2TrialLocal/Rocks/SM_SimpleRock_'+['03A','11A','17A'][j%3]+'_Collision';c=group('EmbeddedRock'+str(j%3),path,shadow=True,collision='BlockAll');put(c,cx,cy,rng.uniform(65,125),z=height(cx,cy)-10)
save('Vegetation.json',dict(section_instances=placed,no_spawn_rule_changes=True))
