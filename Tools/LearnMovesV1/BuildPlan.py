"""Reproduce this bounded binding plan from pinned Crystal move rows and existing verified learnlists."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[2]
source=R/'Saved/MoveEffectsV4/Resume/Reference/data_moves_moves.asm';assert hashlib.sha256(source.read_bytes()).hexdigest()=='50cd7c03a51a3228e96af6b61a1f77e9173fc2118017eb3752d5ce055d3be39d'
D={'GUST':('Gust','Windstoß'), 'WHIRLWIND':('Whirlwind','Wirbelwind'),'THRASH':('Thrash','Fuchtler'),'TWINEEDLE':('Twineedle','Duonadel'),'PIN_MISSILE':('PinMissile','Nadelrakete'),'SUPERSONIC':('Supersonic','Superschall'),'PSYBEAM':('Psybeam','Psystrahl'),'HYPER_BEAM':('HyperBeam','Hyperstrahl'),'DRILL_PECK':('DrillPeck','Bohrschnabel'),'MIRROR_MOVE':('MirrorMove','Spiegeltrick'),'SPLASH':('Splash','Platscher'),'FLAIL':('Flail','Dreschflegel'),'SAFEGUARD':('Safeguard','Bodyguard'),'PURSUIT':('Pursuit','Verfolgung'),'TWISTER':('Twister','Windhose')}
def c(kind,**kw):return dict(kind=kind,**kw)
fx={'TWINEEDLE':[c('MULTI_HIT',min_hits=2,max_hits=2,hit_weights=[1]),c('PRIMARY_STATUS',status='POISON',chance_percent=20,secondary=True,immune_types=['POISON'])], 'PIN_MISSILE':[c('MULTI_HIT',hit_weights=[3,3,1,1])], 'THRASH':[c('RAMPAGE',min_turns=2,max_turns=3)], 'SUPERSONIC':[c('CONFUSION',min_turns=2,max_turns=5)],'PSYBEAM':[c('CONFUSION',min_turns=2,max_turns=5,secondary=True,chance_percent=10)],'TWISTER':[c('FLINCH',secondary=True,chance_percent=20),c('AIRBORNE_BONUS',amount=2)],'GUST':[c('AIRBORNE_BONUS',amount=2)],'HYPER_BEAM':[c('RECHARGE')],'MIRROR_MOVE':[c('COPY_LAST_MOVE')],'SPLASH':[c('NO_EFFECT',self=True)],'FLAIL':[c('LOW_HP_POWER')],'SAFEGUARD':[c('SAFEGUARD',self=True,min_turns=5,max_turns=5)],'PURSUIT':[c('SWITCH_PUNISH',amount=2)],'WHIRLWIND':[c('FORCE_SWITCH')]}
rows=[];original_id=0
for line in source.read_text().splitlines():
 m=re.match(r'\s*move\s+(\w+),\s*(\w+),\s*(\d+),\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+)',line)
 if not m:continue
 original_id+=1
 if m[1]not in D:continue
 token,effect,power,typ,acc,pp,chance=m.groups();typ=typ.replace('_TYPE','');status=int(power)==0
 rows.append(dict(original_id=original_id,token=token,id=D[token][0],name=D[token][1],path='/Game/Data/Moves/LearnMovesV1/DA_'+D[token][0],type=typ,category='STATUS'if status else'SPECIAL'if typ in ['FIRE','WATER','GRASS','ELECTRIC','ICE','PSYCHIC','DRAGON','DARK']else'PHYSICAL',power=int(power),accuracy=int(acc),max_pp=int(pp),priority=-1 if token=='WHIRLWIND'else 0,never_miss=token in ['SPLASH','SAFEGUARD'],components=fx.get(token,[]),crystal_effect=effect,crystal_chance=int(chance)))
assert len(rows)==15
species=json.loads((R/'Tools/BiomeTestV1/SpeciesV11.json').read_text());bindings=[]
for name,data in species.items():
 for level,token in data['crystal_moves']:
  if token in D:bindings.append(dict(species=name,level=level,token=token,id=D[token][0]))
assert len(bindings)==16
refs={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in(R/'Saved/ProjectRefinement/LearnMovesV1/Reference').glob('*')}
plan=dict(source_commit='5c877ef55197039c9676e8e3eec6d254b1c40fe8',source_url='https://github.com/pret/pokecrystal/blob/5c877ef55197039c9676e8e3eec6d254b1c40fe8/data/moves/moves.asm',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),mechanism_sources_sha256=refs,rows=rows,bindings=bindings)
(R/'Tools/LearnMovesV1/Plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');print(len(rows),'moves',len(bindings),'bindings')
