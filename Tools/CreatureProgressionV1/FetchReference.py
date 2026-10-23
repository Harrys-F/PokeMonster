"""Cache and pin public PokeAPI tabular metadata; never download ROMs or visual assets."""
from pathlib import Path
import csv,hashlib,io,json,subprocess,urllib.request
R=Path(__file__).resolve().parents[2];O=R/'Saved/CreatureProgressionV1/Reference';O.mkdir(exist_ok=True)
sha=subprocess.check_output(['git','ls-remote','https://github.com/PokeAPI/pokeapi.git','refs/heads/master'],text=True).split()[0]
files=['pokemon_moves','moves','move_changelog','move_names','pokemon_species','pokemon_evolution','version_groups','pokemon'];tables={};sources=[]
for n in files:
 p=O/(sha+'_'+n+'.csv');url='https://raw.githubusercontent.com/PokeAPI/pokeapi/'+sha+'/data/v2/csv/'+n+'.csv'
 if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=120).read())
 b=p.read_bytes();tables[n]=list(csv.DictReader(io.StringIO(b.decode())));sources.append(dict(url=url,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
# Gold/Silver, not modern move values or an arbitrary union of generations.
vg=next(x for x in tables['version_groups'] if x['identifier']=='gold-silver');assert vg['id']=='3'
names={x['move_id']:x['name'] for x in tables['move_names'] if x['local_language_id']=='6'}
moves={x['id']:dict(x) for x in tables['moves']};chosen=[1,4,6,7,25,43,54,68,92,94]
sp={int(x['id']):x for x in tables['pokemon_species']};out=[];ids=set()
for dex in chosen:
 rows=[dict(level=int(x['level']),move_id=int(x['move_id']),order=int(x['order'] or 0)) for x in tables['pokemon_moves'] if int(x['pokemon_id'])==dex and x['version_group_id']=='3' and x['pokemon_move_method_id']=='1']
 rows.sort(key=lambda x:(x['level'],x['order'],x['move_id']));ids.update(x['move_id'] for x in rows)
 out.append(dict(dex=dex,species=sp[dex]['identifier'],growth_rate_id=int(sp[dex]['growth_rate_id']),learnset=rows,evolutions=[x for x in tables['pokemon_evolution'] if sp[int(x['evolved_species_id'])]['evolves_from_species_id']==str(dex)]))
selected=[]
for mid in sorted(ids):
 m=moves[str(mid)];applied=[]
 # Each changelog row is the value BEFORE the named version group. Earliest future
 # change wins independently per field; null means unchanged, not missing power.
 for change in sorted([x for x in tables['move_changelog'] if x['move_id']==str(mid) and int(x['changed_in_version_group_id'])>3],key=lambda x:int(x['changed_in_version_group_id']),reverse=True):
  for k,v in change.items():
   if k not in ['move_id','changed_in_version_group_id'] and v!='':m[k]=v
  applied.append(change)
 m['runtime_supported']=m['identifier'] in {'scratch','growl','ember','tackle','tail-whip','bubble','withdraw','water-gun','leech-seed','vine-whip','quick-attack','absorb','leer','seismic-toss','night-shade','wing-attack','flamethrower','slam','hydro-pump'}
 m['unavailable_reason']='' if m['runtime_supported'] else 'Spezialwirkung im vorhandenen Kampfsystem noch nicht vollständig implementiert'
 m['german_name']=names[str(mid)];m['past_changes']=applied;selected.append(m)
result=dict(source_commit=sha,version_group='gold-silver',version_group_id=3,sources=sources,species=out,moves=selected,note='Public metadata, not extracted ROM content. Move effects require separate implementation review; evolution method is contemporary metadata and requires project/Gen2 validation.')
p=R/'Tools/CreatureProgressionV1/Gen2Reference.json';assert not p.exists(),'Never overwrite a reviewed reference';p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('REFERENCE',sha,len(out),'species',len(selected),'moves')
for s in out:print(s['dex'],s['species'],[(x['level'],moves[str(x['move_id'])]['identifier']) for x in s['learnset']])
