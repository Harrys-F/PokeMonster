"""Isolate decal raster cost: identical shadow-disabled components, with/without blob drawing.
All changes are runtime-only in the existing GPU test map. No timing includes ProfileGPU.
"""
import unreal,json,time,csv
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2AASoftShadowsV1';P=R/'Saved/EnvironmentPerfV2';j=json.loads((O/'Request.json').read_text());label=j['label'];mode=j['mode']
w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2GPUBottleneckV1' and unreal.GameplayStatics.get_player_pawn(w,0))
plan=O/(label+'.tsv');assert not plan.exists()
rows=[]
for rep in range(3):
 for hidden in ([False,True] if rep%2==0 else [True,False]):rows.append(['Wald','SoftAA:C',rep+(10 if hidden else 0),2560,1440,2,100])
rows.extend([['Wald','SoftAA:C',90,2560,1440,2,100],['Wald','SoftAA:C',91,2560,1440,2,100],['Wald','SoftAA:A',99,2560,1440,2,100]])
plan.write_text(label+'\t'+mode+'\t5\t4\n'+'\n'.join('\t'.join(map(str,r)) for r in rows)+'\n')
before={n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in ['r.ProfileGPU.ShowUI','r.ProfileGPU.ShowLeafEvents','r.ProfileGPU.ThresholdPercent']}
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Run "'+str(plan)+'"');current=-1;stage=time.monotonic();profile=False;proof=[]
def tick(dt):
 global current,stage,profile
 if (P/(label+'_Done.txt')).exists():
  for n,v in before.items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(v))
  unreal.unregister_slate_post_tick_callback(unreal._vas_cost);(O/(label+'_Proof.json')).write_text(json.dumps(proof,indent=2));return
 f=P/(label+'_Segments.csv');index=len(list(csv.DictReader(f.open()))) if f.exists() else 0
 if index!=current:
  current=index;stage=time.monotonic();profile=False
  if current>=len(rows):return
  rep=rows[current][2];hide=10<=rep<20 or rep==91
  owners={c.get_owner() for c in unreal.ObjectIterator(unreal.DecalComponent) if c.get_world()==w and c.get_decal_material() and '/VisualV2AASoftShadowsV1/' in c.get_decal_material().get_path_name()}
  for a in owners:a.set_actor_hidden_in_game(hide)
  proof.append({'segment':index,'repeat':rep,'hidden':hide,'owners':len(owners),'time':time.time()});(O/(label+'_Proof.json')).write_text(json.dumps(proof,indent=2))
 if current<len(rows) and rows[current][2] in [90,91] and not profile and time.monotonic()-stage>2:
  profile=True;unreal.log('VAS_GPU_PROFILE_BEGIN '+label+' '+str(rows[current][2]))
  for cmd in ['r.ProfileGPU.ShowUI 0','r.ProfileGPU.ShowLeafEvents 1','r.ProfileGPU.ThresholdPercent 0.01','ProfileGPU']:unreal.SystemLibrary.execute_console_command(w,cmd)
unreal._vas_cost=unreal.register_slate_post_tick_callback(tick)
