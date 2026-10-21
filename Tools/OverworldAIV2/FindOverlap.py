"""Read-only candidate search for overlapping canopy cores; does not move any actor."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();sun=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DirectionalLight)if a.get_component_by_class(unreal.DirectionalLightComponent).cast_shadows);d=-sun.get_actor_forward_vector();trees=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and '/Trees/'in c.static_mesh.get_path_name():
   center,ext,r=unreal.SystemLibrary.get_component_bounds(c);trees.append((a.get_name(),center,ext))
def hit(x,y,center,e):
 size=e*2;cc=unreal.Vector(center.x,center.y,center.z-e.z+size.z*.76);rad=unreal.Vector(size.x*.31,size.y*.31,size.z*.19);q=[(x-cc.x)/rad.x,(y-cc.y)/rad.y,(85-cc.z)/rad.z];v=[d.x/rad.x,d.y/rad.y,d.z/rad.z];t=max(0,-sum(a*b for a,b in zip(q,v))/sum(a*a for a in v));return math.sqrt(sum((a+t*b)**2 for a,b in zip(q,v)))<.7
rows=[]
for x in range(-2100,-800,50):
 for y in range(-1200,1200,50):
  hits=[n for n,c,e in trees if hit(x,y,c,e)]
  if len(hits)>=2:rows.append({'point':[x,y],'trees':hits})
(R/'Saved/OverworldAIV2/OverlapCandidates.json').write_text(json.dumps(rows,indent=2))
