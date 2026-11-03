"""All exterior surfaces plus bounded rear/side carpentry; footprints/colliders/doors retained."""
import unreal,runpy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/MaterialHelpers.py')));assert not(D/'Architecture.json').exists()
m=new('Glass');n=custom(m,'return float3(.075,.11,.095);',{});ML.connect_material_property(n,'',unreal.MaterialProperty.MP_BASE_COLOR);n=custom(m,'return float3(.052,.032,.009);',{});ML.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);scalar(m,.23,unreal.MaterialProperty.MP_ROUGHNESS);scalar(m,.75,unreal.MaterialProperty.MP_SPECULAR);finish(m)
m=unreal.EditorAssetLibrary.duplicate_asset(material('Timber').get_path_name(),ROOT+'/Materials/M_WR4_ShutterGreen');assert m
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom)and'return T*float3'in n.get_editor_property('code'):n.set_editor_property('code','float g=dot(T,float3(.299,.587,.114));return lerp(T*.43,g*float3(.26,.48,.27),.76);')
finish(m)
inv=json.loads((D/'Inventory.json').read_text());outside={r['label']for r in inv['rows']if any(-6000<t['position'][0]<3000 and-3250<t['position'][1]<3250 for t in r['instances'])};swap={'M_WOV_Timber':'Timber','M_WOV_Stone':'Stone','M_WOV_Plaster':'Plaster','M_WOV_Roof':'Roof','M_WOV_Cobbles':'Paving'}
for label,a in actors.items():
 if label not in outside or not label.startswith(('V2_House_','V2_Cottage_','V2_Village_','V2_Fence_','FAT_Garden','V2_Archive_')):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  for i in range(c.get_num_materials()):
   old=c.get_material(i)
   if not old:continue
   target=swap.get(old.get_name())
   if 'Glass'in old.get_name():target='Glass'
   if target:a.modify();c.set_material(i,material(target));changes.append(dict(label=label,slot=i,before=old.get_path_name(),after=target))
# Existing modules face outward along local -X; origin is just outside actual wall bounds.
wl='/Game/Environment/Architecture/Westland/Meshes/';hh='/Game/Environment/HealingHouse/Meshes/'
c=group('CottageRearWindows',wl+'Windows/SM_WL_WindowArch',[material('Glass'),material('Timber')]);
for y in [-820,-1220]:c.add_instance(unreal.Transform(location=unreal.Vector(-2439,y,90),rotation=unreal.Rotator(yaw=180)),True)
c=group('HealerRearWindows',hh+'SM_HH_V2_WindowModule_Arch',[material('Timber'),material('Stone'),material('Glass')])
for y in [280,720]:c.add_instance(unreal.Transform(location=unreal.Vector(-2634,y,90),rotation=unreal.Rotator(yaw=180)),True)
sh=group('WindowShutters','/Engine/BasicShapes/Cube',[material('ShutterGreen')])
for x,ys in [(-2429,[-820,-1220]),(-2623,[280,720])]:
 for y in ys:
  spread=82 if x<-2400 and x>-2500 else 103
  for side in [-1,1]:centred(sh,(x,y+side*spread,154),(6,40,132),unreal.Rotator(yaw=side*12))
beam=group('RearCarpentry',wl+'Timber/SM_WL_HorizontalBeam2m',[material('Timber')])
def between(c,a,b,width=10):
 a=unreal.Vector(*a);b=unreal.Vector(*b);v=b-a;centred(c,((a+b)*.5).to_tuple(),(width,v.length(),width),unreal.MathLibrary.make_rot_from_y(v))
for a,b in [((-2630,75,65),(-2630,195,240)),((-2630,925,65),(-2630,805,240)),((-2434,-1320,236),(-2434,-1268,286)),((-2434,-720,236),(-2434,-772,286)),((-2434,-1315,235),(-2434,-725,235))]:between(beam,a,b)
# A few existing decorative bushes close to the cottage door move into its garden edge.
moved=[]
for a in actors.values():
 if not a.get_actor_label().startswith(('FAT_','EP2_','V2_Bush')):continue
 for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
  if not c.static_mesh or not any(k in c.static_mesh.get_name().lower()for k in ['bush','shrub','hydrangea']):continue
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,True);p=t.translation
   if abs(p.x+3050)<160 and abs(p.y+1020)<190:
    a.modify();c.modify();t.translation=unreal.Vector(-3160-rng.uniform(0,60),-1500-rng.uniform(0,45),p.z);c.update_instance_transform(i,t,True,True,True);moved.append(dict(label=a.get_actor_label(),before=p.to_tuple(),after=t.translation.to_tuple()))
save('Architecture.json',dict(footprints_and_colliders_unchanged=True,new_windows=4,new_shutters=8,relocated_decorative_bushes=moved))
