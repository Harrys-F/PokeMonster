"""Glutexo landmarks fitted to the read-only front/side/back intake; metres, front -Y."""
import runpy
from pathlib import Path
shared=runpy.run_path(str(Path(__file__).parents[1]/'CreatureExpansionV3/Anatomy.py'))
SPECS=dict(shared['SPECS'])
SPECS['Glutexo']=dict(dex=5,height=1.1,family='Biped',walk=.30,run=.60,pelvis=(0,-.12,.32),chest=(0,-.12,.58),neck=(0,-.13,.76),head=(0,-.14,.96),hip=(.14,-.10,.31),knee=(.17,-.17,.18),ankle=(.17,-.16,.035),toe=(.17,-.27,.025),shoulder=(.17,-.12,.64),elbow=(.35,-.12,.64),hand=(.49,-.12,.64),tip=(.565,-.12,.64))
def layout(name):
 assert name=='Glutexo'
 shared['SPECS'][name]=SPECS[name]
 bones,chains=shared['layout'](name)
 bones.update(tail_base=((0,.03,.22),(-.27,.22,.18),'pelvis'),tail_mid=((- .27,.22,.18),(-.40,.31,.43),'tail_base'),tail_tip=((- .40,.31,.43),(-.40,.31,.68),'tail_mid'),flame_tip=((- .40,.31,.68),(-.40,.31,.92),'tail_tip'))
 return bones,chains
