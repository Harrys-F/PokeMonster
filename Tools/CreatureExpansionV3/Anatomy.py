"""Hand-fitted landmarks from actual orthogonal Meshy intake views; metres, front -Y."""
SPECS={
 'Pikachu':dict(dex=25,height=.4,origin_offset=(-.070,0,0),family='Biped',walk=.13,run=.28,pelvis=(0,-.025,.105),chest=(0,-.025,.185),neck=(0,-.035,.235),head=(0,-.035,.300),hip=(.052,-.025,.105),knee=(.060,-.040,.055),ankle=(.060,-.040,.012),toe=(.060,-.070,.010),shoulder=(.065,-.025,.187),elbow=(.105,-.027,.185),hand=(.145,-.032,.181),tip=(.157,-.04,.18)),
 'Myrapla':dict(dex=43,height=.5,family='Biped',walk=.10,run=.21,pelvis=(0,-.025,.075),chest=(0,-.025,.17),neck=(0,-.025,.23),head=(0,-.025,.26),hip=(.060,-.025,.075),knee=(.069,-.042,.040),ankle=(.073,-.044,.014),toe=(.073,-.078,.012)),
 'Enton':dict(dex=54,height=.8,family='Biped',walk=.21,run=.42,pelvis=(0,-.04,.20),chest=(0,-.04,.40),neck=(0,-.04,.53),head=(0,-.06,.69),hip=(.115,-.03,.20),knee=(.130,-.11,.11),ankle=(.135,-.10,.025),toe=(.135,-.22,.014),shoulder=(.14,-.03,.46),elbow=(.245,-.025,.45),hand=(.365,-.04,.45),tip=(.43,-.06,.45)),
 'Machomei':dict(dex=68,height=1.6,family='Biped',walk=.42,run=.78,pelvis=(0,-.015,.75),chest=(0,-.015,1.15),neck=(0,-.03,1.33),head=(0,-.035,1.48),hip=(.22,-.01,.75),knee=(.275,-.13,.40),ankle=(.30,-.08,.075),toe=(.30,-.25,.03),shoulder=(.28,-.015,1.20),elbow=(.56,-.04,1.14),hand=(.77,-.10,1.09),tip=(.89,-.15,1.08)),
 'Nebulak':dict(dex=92,height=1.3,family='Floating',walk=.32,run=.65,pelvis=(0,-.025,.50),chest=(0,-.025,.64),neck=(0,-.025,.76),head=(0,-.025,.88)),
 'Gengar':dict(dex=94,height=1.5,family='Biped',walk=.30,run=.62,pelvis=(0,-.10,.43),chest=(0,-.10,.76),neck=(0,-.20,.94),head=(0,-.24,1.17),hip=(.29,-.10,.43),knee=(.38,-.26,.24),ankle=(.42,-.25,.065),toe=(.42,-.44,.035),shoulder=(.40,-.13,.70),elbow=(.54,-.30,.58),hand=(.62,-.47,.50),tip=(.68,-.58,.45)),
 'Glurak':dict(dex=6,height=1.7,origin_offset=(0,-.25,0),family='Winged',walk=.36,run=.74,pelvis=(0,-.13,.45),chest=(0,-.13,.85),neck=(0,-.20,1.16),head=(0,-.27,1.54),hip=(.30,-.08,.45),knee=(.38,-.26,.25),ankle=(.38,-.25,.075),toe=(.38,-.43,.035),shoulder=(.26,-.14,.96),elbow=(.52,-.18,.94),hand=(.70,-.25,.91),tip=(.80,-.30,.88))}
def layout(name):
 s=SPECS[name];bones={'root':((0,0,0),(0,0,.04*s['height']),None)};chains=[]
 def b(n,h,t,parent):bones[n]=(h,t,parent)
 b('pelvis',s['pelvis'],s['chest'],'root');b('chest',s['chest'],s['neck'],'pelvis');b('head',s['neck'],s['head'],'chest')
 if 'hip'in s:
  for side,sign in [('L',1),('R',-1)]:
   def p(key):x,y,z=s[key];return(sign*x,y,z)
   b('thigh_'+side,p('hip'),p('knee'),'pelvis');b('shin_'+side,p('knee'),p('ankle'),'thigh_'+side);b('foot_'+side,p('ankle'),p('toe'),'shin_'+side);chains.append(dict(id=side,upper='thigh_'+side,lower='shin_'+side,foot='foot_'+side,pole=-1,phase=0 if side=='L'else .5))
   if 'shoulder'in s:
    for n,a,c,par in [('upperarm','shoulder','elbow','chest'),('forearm','elbow','hand','upperarm_'+side),('hand','hand','tip','forearm_'+side)]:b(n+'_'+side,p(a),p(c),par)
 if name=='Pikachu':
  b('tail_base',(0,.045,.075),(.075,.065,.10),'pelvis');b('tail_mid',(.075,.065,.10),(.10,.075,.20),'tail_base');b('tail_tip',(.10,.075,.20),(.20,.075,.26),'tail_mid')
  for side,sg in [('L',1),('R',-1)]:b('ear_'+side,(sg*.055,-.025,.28),(sg*.115,-.020,.365),'head')
 if name=='Myrapla':
  for side,sg in [('L',1),('R',-1)]:
   for row,y in enumerate([-.06,.07]):b('leaf_'+side+str(row),(sg*.025,y,.23),(sg*.21,y,.39),'head')
  b('leaf_centre',(0,0,.23),(0,.06,.48),'head')
 if name=='Enton':b('tail_base',(0,.13,.12),(0,.28,.17),'pelvis')
 if name=='Machomei':
  for side,sg in [('L',1),('R',-1)]:
   b('lower_upperarm_'+side,(sg*.25,.06,1.03),(sg*.47,.02,.85),'chest');b('lower_forearm_'+side,(sg*.47,.02,.85),(sg*.68,-.10,.77),'lower_upperarm_'+side);b('lower_hand_'+side,(sg*.68,-.10,.77),(sg*.79,-.16,.75),'lower_forearm_'+side)
 if name=='Nebulak':
  for i in range(8):
   import math
   angle=i*math.tau/8;x,z=math.sin(angle),math.cos(angle);b('gas_'+str(i),(x*.31,.045,.64+z*.31),(x*.52,.07,.64+z*.48),'pelvis')
 if name=='Gengar':
  b('tail_base',(0,.10,.28),(0,.40,.20),'pelvis');b('tail_tip',(0,.40,.20),(0,.85,.18),'tail_base')
 if name=='Glurak':
  b('tail_base',(0,.12,.36),(-.44,.50,.25),'pelvis');b('tail_mid',(-.44,.50,.25),(-.98,.88,.31),'tail_base');b('tail_tip',(-.98,.88,.31),(-1.38,1.04,.58),'tail_mid')
  b('flame_tip',(-1.38,1.04,.58),(-1.38,1.04,.78),'tail_tip')
  for side,sg in [('L',1),('R',-1)]:
   b('wing_base_'+side,(sg*.20,.08,1.03),(sg*.67,.12,1.53),'chest');b('wing_tip_'+side,(sg*.67,.12,1.53),(sg*1.52,.16,.96),'wing_base_'+side)
 return bones,chains
