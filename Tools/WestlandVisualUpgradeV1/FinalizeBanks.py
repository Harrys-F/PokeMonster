"""Ground visual bank-rock clusters on their low-side support; geometry/collision unchanged."""
import unreal,json,math,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualUpgradeV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not(D/'BankSupportAudit.json').exists();actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();ignore=[a for a in actors if a.actor_has_tag('BiomePlayerWaterBarrier')]
def floor(x,y,z):
 h=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+4000),unreal.Vector(x,y,z-8000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE)
 if not h:return None
 m=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',h.export_text());return float(m[1])if m else None
a=next(a for a in actors if a.get_actor_label()=='WR_RockyContours');c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);b=c.static_mesh.get_bounding_box();rows=[];a.modify()
for i in range(c.get_instance_count()):
 t=c.get_instance_transform(i,True);p=t.translation;rx=(b.max.x-b.min.x)*t.scale3d.x*.32;ry=(b.max.y-b.min.y)*t.scale3d.y*.32
 support=[floor(p.x+dx,p.y+dy,p.z)for dx,dy in [(0,0),(rx,0),(-rx,0),(0,ry),(0,-ry)]];support=[v for v in support if v is not None];assert support;z=min(support)-b.min.z*t.scale3d.z-(b.max.z-b.min.z)*t.scale3d.z*.22;t.translation=unreal.Vector(p.x,p.y,z);c.update_instance_transform(i,t,True,i==c.get_instance_count()-1,True);rows.append(dict(instance=i,support_min_z=min(support),before_z=p.z,after_z=z,xy_unchanged=True))
m=unreal.load_asset('/Game/Environment/WestlandVisualUpgradeV1/Materials/M_WVU_River')
for n in unreal.MaterialEditingLibrary.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom):
  code=n.get_editor_property('code')
  if 'float opacity=lerp(.38,.72,deep)'in code:n.set_editor_property('code',code.replace('float3(.022,.080,.095)','float3(.024,.100,.121)').replace('float3(.009,.016,.015)','float3(.015,.025,.023)').replace('lerp(.38,.72,deep)','lerp(.38,.82,deep)'))
unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'BankSupportAudit.json').write_text(json.dumps(rows,indent=2))
