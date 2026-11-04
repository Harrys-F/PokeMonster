"""Read current source room and actual target anchors/terrain; never save a package."""
import unreal,json,sys,re,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);assert not E.get_game_world();assert not(D/'MigrationInputs.json').exists()
def tr(t):
 r=t.rotation.rotator();return dict(location=t.translation.to_tuple(),rotation=dict(pitch=r.pitch,yaw=r.yaw,roll=r.roll),scale=t.scale3d.to_tuple())
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');W=E.get_editor_world();aa={a.get_actor_label():a for a in A.get_all_level_actors()};cut=aa['V2_House_HouseCutaway'];source=dict(door=tr(cut.relocated_door_threshold.get_world_transform()),room=[],groups=[],lights=[])
for name,a in aa.items():
 p=a.get_actor_location()
 if not(16000<p.x<17700):continue
 row=dict(label=name.removeprefix('V2_House_'),components=[])
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  row['components'].append(dict(name=c.get_name(),mesh=c.static_mesh.get_path_name()if c.static_mesh else None,materials=[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())],shadow=c.cast_shadow))
 source['room'].append(row)
 for c in a.get_components_by_class(unreal.LightComponent):
  source['lights'].append(dict(label=row['label'],component=c.get_name(),intensity=c.intensity,color=list(c.get_light_color().to_tuple()),shadow=c.cast_shadows,channels=str(c.lighting_channels)))
for name,a in aa.items():
 if not name.startswith('V6_Interior_'):continue
 for c in a.get_components_by_class(unreal.InstancedStaticMeshComponent):
  source['groups'].append(dict(label=name,mesh=c.static_mesh.get_path_name(),materials=[c.get_material(i).get_path_name()for i in range(c.get_num_materials())],instances=[tr(c.get_instance_transform(i,True))for i in range(c.get_instance_count())],shadow=c.cast_shadow))
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_WestlandRegion');W=E.get_editor_world();aa={a.get_actor_label():a for a in A.get_all_level_actors()};target=dict(door=tr(aa['HouseCutaway'].relocated_door_threshold.get_world_transform()));sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
ignore=[a for a in aa.values()if not a.get_actor_label().startswith('WR_Terrain_')]
def ground(e,n):
 x,y,_=L.world(e,n);hit=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,15000),unreal.Vector(x,y,-10000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert hit,(e,n);m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',hit.export_text());assert m;return x,y,float(m[1])
sites=[]
for name,e,n,te,tn in [('Dorf',-222,-47,-205,-42),('Wiese',150,13,180,25),('Waldweg',202,120,225,175),('Wald',247,250,265,264),('Fluss',L.river(-145)+10,-145,L.river(-145),-142)]:
 x,y,z=ground(e,n);tx,ty,_=L.world(te,tn);sites.append([name,x,y,z,math.degrees(math.atan2(ty-y,tx-x))])
door=target['door'];off=unreal.MathLibrary.rotate_angle_axis(unreal.Vector(400,0,0),door['rotation']['yaw'],unreal.Vector(0,0,1));q=unreal.Vector(*door['location'])+off;sites.append(['Heilhaus',q.x,q.y,1000,door['rotation']['yaw']+180]);target['sites']=sites
(D/'MigrationInputs.json').write_text(json.dumps(dict(source=source,target=target),indent=2));(R/'Tools/WestlandVisualV2IntegrationV1/Sites.json').write_text(json.dumps(sites,indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();print('Inputs',len(source['room']),len(source['groups']),len(source['lights']),len(sites))
