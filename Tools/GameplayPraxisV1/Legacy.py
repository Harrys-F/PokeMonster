"""Reuse reviewed PIE scripts verbatim except explicit evidence destinations and test-only extensions."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';req=json.loads((D/'Request.json').read_text());source=R/req['source'];code=source.read_text()
for old,new in req.get('replacements',[]):
 assert old in code,(source,old);code=code.replace(old,new)
if req['kind']=='controller':
 # Additional context-overlap case uses the same key simulator and existing UMG.
 code=code.replace('def finish(error=None):', '''key('X overlapping-input page',X)
action('hold B while menu owns focus',lambda:command('pm.Input.Key '+B+' down'),.18)
action('overlap repeated X',lambda:command('pm.Input.Key '+X+' down repeat'),.12)
action('release overlapping X',lambda:command('pm.Input.Key '+X+' up'),.12)
check('Overlapping held B and repeat X keeps one menu and no encounter',lambda:pc.is_menu_open()and not enc.is_encounter_active())
key('A cancels selection while B held',A)
action('release held B',lambda:command('pm.Input.Key '+B+' up'),.15)
key('A closes overlapped menu',A)
check('Overlapping menu inputs restore world focus without duplicate action',lambda:not pc.is_menu_open()and not enc.is_encounter_active()and not p.is_overworld_input_locked())

def finish(error=None):''')
 code=code.replace("result['checks'].append(name)","result['checks'].append(name)\n  if name in ['X opens existing team menu','R reaches inventory','B opens dialogue without advancing twice','Bag selected through Dpad and B']:command('pm.CreatureReview.CaptureLiveUI Praxis'+label+str(len(result['checks'])))")
exec(compile(code,str(source),'exec'),globals())
