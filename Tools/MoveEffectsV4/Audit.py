"""Join immutable GS metadata with a read-only actual Unreal inventory; no inferred effect support."""
from pathlib import Path
import json,argparse
args=argparse.ArgumentParser();args.add_argument("--inventory",default="Saved/MoveEffectsV4/AssetsBefore.json");args.add_argument("--output",required=True);options=args.parse_args()
R=Path(__file__).resolve().parents[2];ref=json.loads((R/'Tools/CreatureProgressionV1/Gen2Reference.json').read_text());assets=json.loads((R/options.inventory).read_text());byid={m['id']:m for m in assets};rows=[]
for m in ref['moves']:
 ident=''.join(x.title()for x in m['identifier'].split('-'));asset=byid.get(ident)
 rows.append(dict(id=ident,pokeapi_id=int(m['id']),name=m['german_name'],type_id=int(m['type_id']),category=m['damage_class_id'],power=int(m['power'])if m['power']else None,accuracy=int(m['accuracy'])if m['accuracy']else None,max_pp=int(m['pp']),priority=int(m['priority']),metadata_effect_id=int(m['effect_id']),effect_chance=int(m['effect_chance'])if m['effect_chance']else None,asset=asset,baseline_supported=bool(asset),missing_effect=''if asset else m['unavailable_reason'],source_commit=ref['source_commit'],rule_note='GS numeric metadata; effect_id is not proof of GS semantics. Project keeps per-move categories and simplified damage.'))
for m in assets:
 if not any(x['id']==m['id']for x in rows):rows.append(dict(id=m['id'],name=m['name'],asset=m,baseline_supported=True,rule_note='Historical project fixture, not a canonical learnset move.'))
out=dict(source_commit=ref['source_commit'],canonical_moves=len(ref['moves']),canonical_supported=sum(x['runtime_supported']for x in ref['moves']),baseline_unavailable=sum(not x['runtime_supported']for x in ref['moves']),actual_assets=len(assets),unique_missing_metadata_effect_ids=len(set(x['effect_id']for x in ref['moves']if not x['runtime_supported'])),rows=rows)
p=(R/options.output).resolve();assert p.is_relative_to(R/'Saved') or p.is_relative_to(R/'Docs');assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items()if k!='rows'})
