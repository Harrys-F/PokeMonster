"""One-time visual-only dressing of the editor-created Dev_TestMap_VisualV2 copy.
Original maps/assets never saved. Gameplay actors and original collision retained.
"""
import unreal,json,math,random
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';D='/Game/Environment/DevTestMapVisualV2';W='/Game/Environment/WestlandAssetLibrary';V=W+'/QualityV3';G='/Game/Environment/Westland/NaturalGroundV1'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);world=E.get_editor_world();assert world.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world()
A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(A.get_all_level_actors());assert not any(a.get_actor_label()=='V2_Ground' for a in actors),'Already dressed'
by={a.get_actor_label():a for a in actors};T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;rng=random.Random(121026);record={'new_actors':[],'retained_hidden':[],'replacements':[],'paths':[]}
def spawn(label,path,pos,yaw=0,scale=(1,1,1),collision=False,shadow=True):
 mesh=unreal.load_asset(path);assert mesh,path
 a=A.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos),unreal.Rotator(yaw=yaw));a.set_actor_label('V2_'+label);a.tags=['DevVisualV2'];a.set_folder_path('VisualV2/Environment');a.set_actor_scale3d(unreal.Vector(*scale));c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_cast_shadow(shadow);c.set_editor_property('ld_max_draw_distance',8500)
 record['new_actors'].append({'label':a.get_actor_label(),'mesh':path,'position_cm':pos,'scale':scale,'collision':collision});return a
def hide(a):
 for c in a.get_components_by_class(unreal.PrimitiveComponent):c.set_visibility(False)
 a.set_actor_hidden_in_game(True);record['retained_hidden'].append(a.get_actor_label())
def material(name):
 existing=unreal.load_asset(D+'/Materials/'+name)
 if existing:L.delete_all_material_expressions(existing);return existing
 return T.create_asset(name,D+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
def exp(m,cls,x=0,y=0):return L.create_material_expression(m,cls,x,y)
def wire(s,out,d,pin):assert L.connect_material_expressions(s,out,d,pin)
def const(m,v,prop):n=exp(m,unreal.MaterialExpressionConstant);n.r=v;L.connect_material_property(n,'',prop)
# Scoped crown reveal: spatially soft dither corridor along fixed camera-to-focus ray.
# No game tick, global material override, player access or collision mutation.
m=material('M_V2_CrownReveal');m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('two_sided',True);m.set_editor_property('opacity_mask_clip_value',.45)
tex=exp(m,unreal.MaterialExpressionTextureSampleParameter2D,-900,0);tex.texture=unreal.load_asset(V+'/Textures/T_WLA_FoliageGroups_V3');tex.set_editor_property('parameter_name','Paint')
vc=exp(m,unreal.MaterialExpressionVertexColor,-900,300);mul=exp(m,unreal.MaterialExpressionMultiply,-500,0);wire(tex,'RGB',mul,'A');wire(vc,'',mul,'B');L.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
p=exp(m,unreal.MaterialExpressionWorldPosition,-900,500);camera=exp(m,unreal.MaterialExpressionCameraPositionWS,-900,650);f=exp(m,unreal.MaterialExpressionCustom,-500,500);f.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1)
inputs=[]
for key in ('P','C'):
 n=unreal.CustomInput();n.set_editor_property('input_name',key);inputs.append(n)
f.set_editor_property('inputs',inputs);f.set_editor_property('code','float3 v=float3(0.4055798,-0.4055798,-0.819152)*2500; float t=dot(P-C,v)/dot(v,v); float d=length((P-C)-t*v); float corridor=(1-smoothstep(70,155,d))*smoothstep(.08,.18,t)*(1-smoothstep(.91,1.03,t)); return lerp(1,.08,corridor);');wire(p,'',f,'P');wire(camera,'',f,'C')
dither=exp(m,unreal.MaterialExpressionMaterialFunctionCall,-240,500);dither.set_material_function(unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA'));wire(f,'',dither,'Alpha Threshold');mask=exp(m,unreal.MaterialExpressionMultiply,0,500);wire(tex,'A',mask,'A');wire(dither,'',mask,'B');L.connect_material_property(mask,'',unreal.MaterialProperty.MP_OPACITY_MASK);const(m,.95,unreal.MaterialProperty.MP_ROUGHNESS);const(m,.05,unreal.MaterialProperty.MP_SPECULAR);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
# Retain all old environment actors as collision/fallback. Replace only visible props.
for a in actors:
 if a.get_actor_label().startswith('V2_House_'):continue
 if isinstance(a,unreal.PaperSpriteActor):
  c=a.get_component_by_class(unreal.PaperSpriteComponent);spr=c.get_sprite()
  if not spr:continue
  name=spr.get_name();pos=a.get_actor_location();sc=a.get_actor_scale3d()
  if name in ('S_Oak','S_Bush','S_Rock','S_Hut'):
   hide(a)
   if name=='S_Oak':
    tree=spawn('Tree_'+a.get_actor_label(),V+'/Meshes/Trees/SM_WLA_OakAncient_V3',(pos.x,pos.y,0),rng.uniform(0,360),(rng.uniform(.32,.45),)*3,False,True);tree.static_mesh_component.set_material(1,m)
   elif name=='S_Bush':spawn('Bush_'+a.get_actor_label(),V+'/Meshes/Vegetation/SM_WLA_WildBush_V3_'+rng.choice(['A','B']),(pos.x,pos.y,0),rng.uniform(0,360),(rng.uniform(.35,.65),)*3,False,False)
   elif name=='S_Rock':spawn('Stone_'+a.get_actor_label(),W+'/Meshes/Landscape/SM_WLA_Boulder_A',(pos.x,pos.y,0),rng.uniform(0,360),(rng.uniform(.12,.24),)*3,False,True)
for a in actors:
 name=a.get_actor_label()
 if name.startswith('V2_House_'):continue
 if isinstance(a,unreal.StaticMeshActor) and a.static_mesh_component.is_visible() and (name.startswith(('P2D_Wash','P2D_Surface','P2D_OrganicPath','EW_','Path_')) or name in ['SM_DevFloor','P2D_BackgroundGround','House_Body','House_Roof','House_Door']):hide(a)
# Painted grass family already uses multi-scale/macro variation from Quality V3.
floor=spawn('Ground','/Engine/BasicShapes/Cube',(-1500,0,-10),scale=(90,65,.2),collision=True,shadow=False);floor.static_mesh_component.set_material(0,unreal.load_asset(G+'/Materials/M_WL_NG_Grass'));floor.static_mesh_component.set_editor_property('ld_max_draw_distance',0)
# Existing expanded room's original collision is kept; independent safe underpinning.
f=spawn('InteriorUnderfloor','/Engine/BasicShapes/Cube',(16900,500,-10),scale=(18,15,.2),collision=True,shadow=False);f.static_mesh_component.set_material(0,unreal.load_asset(G+'/Materials/M_WL_NG_Earth'));f.static_mesh_component.set_editor_property('ld_max_draw_distance',0)
# New curved ribbons; each face oriented upwards, explicit UV/normal + Mikk tangents.
paths={
 'Main':[(-760,-1410),(-760,-1110),(-780,-850),(-700,-640),(-440,-540),(-350,-480),(-350,-150),(-20,-40),(240,170),(470,360),(730,600),(760,850)],
 'Wild':[(-760,-1370),(-880,-1410),(-1000,-1430)],
 'VillageLoop':[(-760,-1410),(-1150,-1920),(-2100,-2060),(-3350,-1700),(-4150,-700),(-4100,450),(-3600,500)],
 'NorthLoop':[(-4100,450),(-4300,1550),(-3300,2050),(-2150,2000),(-1700,1220),(-1550,650),(-1580,-100),(-1560,-860),(-1520,-1830),(-1150,-1920)]}
route_samples=[]
def pathmesh(name,points,width):
 pts=[]
 for i in range(len(points)-1):
  p0,p1,p2,p3=[points[max(0,min(len(points)-1,j))] for j in (i-1,i,i+1,i+2)]
  for j in range(16):
   t=j/16;pts.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t**3) for k in (0,1)))
 pts.append(points[-1]);route_samples.extend(pts);vs=[];uv=[];tris=[]
 for i,(x,y) in enumerate(pts):
  prev=pts[max(0,i-1)];nxt=pts[min(len(pts)-1,i+1)];dx=nxt[0]-prev[0];dy=nxt[1]-prev[1];length=max(.1,math.hypot(dx,dy));bw=width*(1+.07*math.sin(i*.42))
  for j in range(7):
   v=j/6;vs.append(unreal.Vector(x-dy/length*(2*v-1)*bw/2,y+dx/length*(2*v-1)*bw/2,1.35));uv.append(unreal.Vector2D(i/(len(pts)-1),v))
   if i and j:
    a=(i-1)*7+j-1;b=i*7+j-1
    for t in [unreal.IntVector(a,b,b+1),unreal.IntVector(a,b+1,a+1)]:
     if (vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).z<0:t=unreal.IntVector(t.x,t.z,t.y)
     if (vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).length()>.01:tris.append(t)
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.triangles=tris;buf.uv0=uv;buf.normals=[unreal.Vector(0,0,1) for _ in vs];dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf)
 opts=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opts.enable_collision=False;opts.enable_nanite=False;opts.enable_recompute_normals=False;opts.enable_recompute_tangents=True;mesh,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,D+'/Meshes/SM_V2_Path_'+name,opts);assert mesh
 mesh.set_material(0,unreal.load_asset(G+'/Materials/M_WL_NG_PathBlend'));unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);spawn('Path_'+name,mesh.get_path_name(),(0,0,0),shadow=False);record['paths'].append({'name':name,'points_cm':points,'width_cm':width,'triangles':len(tris)})
for name,points in paths.items():pathmesh(name,points,270 if name!='Wild' else 140)
# Village furniture and clear foreground. Existing NPC locations never moved.
for i,(name,x,y,yaw,sc) in enumerate([('Bench_A',-1770,-1550,120,1),('Cart_A',-2250,-1780,25,.8),('Barrel_A',-3860,930,10,1),('Crate_A',-3900,1030,40,1),('Signpost_A',-1240,-1760,135,.9)]):spawn('Village_'+str(i),W+'/Meshes/Village/SM_WLA_'+name,(x,y,0),yaw,(sc,)*3,False)
for i,(x,y,yaw) in enumerate([(-2550,-2230,5),(-2800,-2170,20),(-4520,-220,90),(-4520,40,90),(-1870,1980,0)]):spawn('Fence_'+str(i),W+'/Meshes/Village/SM_WLA_Fence_A',(x,y,0),yaw,collision=True)
# Ruins frame the existing archive goal rather than replacing its logic.
for i,(name,x,y,yaw,sc) in enumerate([('Column_A',1160,640,145,.8),('Column_B',700,1060,45,.65),('WallRemnant_A',1100,1110,45,.8),('Runestone_A',1080,760,135,.65)]):spawn('Archive_'+str(i),W+'/Meshes/Ruins/SM_WLA_'+name,(x,y,0),yaw,(sc,)*3,False)
for i,(x,y,sc) in enumerate([(-4650,900,.62),(-3880,1580,.60),(-2640,1670,.52),(-2060,650,.54),(-2380,-750,.50),(-2570,-1830,.46)]):
 a=spawn('ForestOak_'+str(i),V+'/Meshes/Trees/SM_WLA_OakAncient_V3',(x,y,0),rng.uniform(0,360),(sc,)*3,True);a.static_mesh_component.set_material(1,m)
for i,(x,y,sc) in enumerate([(-2600,-1320,.7),(-3760,-820,.6),(-2030,1220,.6),(-4780,1500,.75)]):spawn('Birch_'+str(i),W+'/Meshes/Trees/SM_WLA_Birch_A',(x,y,0),rng.uniform(0,360),(sc,)*3,True)
# HISM distribution in clusters, rejecting free paths, NPC approach and building footprint.
protected=[a.get_actor_location() for a in actors if 'PokeMonster' in a.get_class().get_name() and not a.get_actor_label().startswith('V2_House_')]
centres=[(-2200,-1400),(-3400,-850),(-4540,1120),(-3420,1700),(-2300,1350),(-1800,400),(200,-1020),(1200,-1100),(1250,1150),(-900,500)]
counts={}
for key,mesh,count,sc in [('Grass',W+'/Meshes/Vegetation/SM_WLA_Grass_A',180,1),('Fern',W+'/Meshes/Vegetation/SM_WLA_Fern_A',50,.7),('Flowers',W+'/Meshes/Vegetation/SM_WLA_Wildflowers_A',65,.8),('Herbs',W+'/Meshes/Vegetation/SM_WLA_Herb_A',55,.8),('Pebbles',G+'/Meshes/SM_WL_NG_PebbleCluster',65,.9),('BushA',V+'/Meshes/Vegetation/SM_WLA_WildBush_V3_A',32,.5),('BushB',V+'/Meshes/Vegetation/SM_WLA_WildBush_V3_B',30,.5)]:
 a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label('V2_Instanced_'+key);a.set_folder_path('VisualV2/Instancing');a.tags=['DevVisualV2'];sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(a)[0];params=unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True);handle,reason=sub.add_new_subobject(params);c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason;c.set_static_mesh(unreal.load_asset(mesh));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(4500,6500);n=0
 for _ in range(count*30):
  cx,cy=rng.choice(centres);x=rng.gauss(cx,280);y=rng.gauss(cy,240)
  if min(math.hypot(x-px,y-py) for px,py in route_samples)<190:continue
  if any(math.hypot(x-p.x,y-p.y)<180 for p in protected):continue
  if -3710<x<-2350 and -190<y<1200:continue
  if -930<x<1100 and -960<y<-170:continue
  scale=sc*rng.uniform(.65,1.25);c.add_instance(unreal.Transform(location=unreal.Vector(x,y,1),rotation=unreal.Rotator(yaw=rng.uniform(0,360)),scale=unreal.Vector(scale,scale,scale)),True);n+=1
  if n==count:break
 counts[key]=n
record['hism_counts']=counts
# Warm directional model, local exposure only: no global project settings.
lights=[a for a in actors if isinstance(a,unreal.DirectionalLight)]
for i,a in enumerate(lights):
 c=a.light_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_intensity(3.2 if i==0 else .25);c.set_light_color(unreal.LinearColor(1,.94,.84) if i==0 else unreal.LinearColor(.72,.82,1));c.set_cast_shadows(i==0)
 if i==0:a.set_actor_rotation(unreal.Rotator(pitch=-48,yaw=-100),False)
for a in actors:
 if isinstance(a,unreal.SkyLight):a.light_component.set_intensity(.65)
pp=A.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector());pp.set_actor_label('V2_OutdoorExposure');pp.set_editor_property('unbound',True);pp.set_editor_property('priority',-10);settings=pp.get_editor_property('settings')
for key,value in {'override_auto_exposure_bias':True,'auto_exposure_bias':-.55,'override_auto_exposure_min_brightness':True,'auto_exposure_min_brightness':1.,'override_auto_exposure_max_brightness':True,'auto_exposure_max_brightness':1.,'override_ambient_occlusion_intensity':True,'ambient_occlusion_intensity':.65}.items():settings.set_editor_property(key,value)
pp.set_editor_property('settings',settings)
# Match bridge wood to the same family without changing deck/rail collision.
wood=unreal.load_asset('/Game/Environment/HealingHouse/QualityV3/Materials/M_HH_Q3_Wood')
if not wood:wood=unreal.load_asset('/Game/Environment/HealingHouse/QualityV2/Materials/M_HH_Q2_Wood')
for a in actors:
 if a.get_actor_label().startswith('VS_Bridge') and isinstance(a,unreal.StaticMeshActor):a.static_mesh_component.set_material(0,wood)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Maps/Dev_TestMap_VisualV2')
(O/'Dressing.json').write_text(json.dumps(record,indent=2));unreal.SystemLibrary.execute_console_command(world,'MAP CHECK');unreal.log('DEV_VISUAL_V2_DRESSING_READY')
