"""Joint positions in metres fitted to measured source landmarks, Blender forward -Y."""
def layout(name):
 bones={'root':((0,0,0),(0,0,.04),None)};chains=[]
 def b(n,h,t,p):bones[n]=(h,t,p)
 if name=='Schiggy':
  b('pelvis',(0,-.03,.145),(0,-.03,.205),'root');b('spine',(0,-.03,.205),(0,-.03,.265),'pelvis');b('chest',(0,-.03,.265),(0,-.075,.320),'spine');b('head',(0,-.095,.320),(0,-.10,.47),'chest');b('shell',(0,.040,.12),(0,.050,.29),'chest')
  for side,sign in [('L',1),('R',-1)]:
   a=(sign*.09,-.085,.290);e=(sign*.145,-.130,.265);w=(sign*.190,-.155,.247);t=(sign*.204,-.175,.235);b('upperarm_'+side,a,e,'chest');b('forearm_'+side,e,w,'upperarm_'+side);b('hand_'+side,w,t,'forearm_'+side)
   hip=(sign*.100,-.030,.145);knee=(sign*.120,-.085,.085);ankle=(sign*.118,-.075,.022);toe=(sign*.118,-.12,.012);b('thigh_'+side,hip,knee,'pelvis');b('shin_'+side,knee,ankle,'thigh_'+side);b('foot_'+side,ankle,toe,'shin_'+side);chains.append(dict(id=side,upper='thigh_'+side,lower='shin_'+side,foot='foot_'+side,pole=-1,phase=0 if side=='L'else .5))
  b('tail_base',(0,.065,.07),(.08,.135,.07),'pelvis');b('tail_tip',(.08,.135,.07),(.16,.175,.12),'tail_base')
 else:
  assert name=='Bisasam';b('pelvis',(0,.13,.205),(0,.05,.225),'root');b('spine',(0,.05,.225),(0,-.06,.235),'pelvis');b('chest',(0,-.06,.235),(0,-.165,.26),'spine');b('head',(0,-.165,.26),(0,-.295,.28),'chest');b('bulb',(0,.085,.33),(0,.13,.65),'spine')
  for side,sign in [('L',1),('R',-1)]:
   for limb,parent,pole,phase,a,k,f,t in [('front','chest',1,0 if side=='L'else .5,(sign*.155,-.175,.19),(sign*.180,-.145,.105),(sign*.187,-.217,.025),(sign*.187,-.26,.012)),('hind','pelvis',-1,.5 if side=='L'else 0,(sign*.205,.165,.19),(sign*.230,.095,.105),(sign*.241,.118,.025),(sign*.241,.075,.012))]:
    pre=limb+'_'+side;b(pre+'_upper',a,k,parent);b(pre+'_lower',k,f,pre+'_upper');b(pre+'_foot',f,t,pre+'_lower');chains.append(dict(id=pre,upper=pre+'_upper',lower=pre+'_lower',foot=pre+'_foot',pole=pole,phase=phase))
 return bones,chains
