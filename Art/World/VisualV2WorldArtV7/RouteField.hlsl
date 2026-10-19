struct W6Route {
float sd(float2 p,float2 a,float2 b){float2 v=b-a;return length(p-a-v*saturate(dot(p-a,v)/dot(v,v)));}
float2 nearest(float2 p){float d=100000;float base=120;float s;
s=sd(p,float2(-760.00000,-1410.00000),float2(-760.00000,-1110.00000));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-760.00000,-1110.00000),float2(-782.14844,-879.83398));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-782.14844,-879.83398),float2(-761.61133,-748.74268));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-761.61133,-748.74268),float2(-727.56836,-671.85303));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-727.56836,-671.85303),float2(-688.38257,-630.65552));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-688.38257,-630.65552),float2(-643.67188,-606.32812));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-643.67188,-606.32812),float2(-420.00000,-532.43164));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-420.00000,-532.43164),float2(-378.75000,-524.37500));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-378.75000,-524.37500),float2(-362.18750,-513.04688));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-362.18750,-513.04688),float2(-350.00000,-480.00000));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-350.00000,-480.00000),float2(-347.94922,-450.16602));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-347.94922,-450.16602),float2(-367.99561,-293.68286));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-367.99561,-293.68286),float2(-371.09375,-223.35938));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-371.09375,-223.35938),float2(-358.89893,-165.07690));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-358.89893,-165.07690),float2(-338.31055,-137.26562));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-338.31055,-137.26562),float2(-307.54883,-117.18750));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-307.54883,-117.18750),float2(-268.89648,-102.73438));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-268.89648,-102.73438),float2(-60.15625,-57.03125));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-60.15625,-57.03125),float2(16.05469,-18.39844));if(s<d){d=s;base=122.0;}
s=sd(p,float2(16.05469,-18.39844),float2(83.94531,32.30469));if(s<d){d=s;base=122.0;}
s=sd(p,float2(83.94531,32.30469),float2(224.70215,157.24121));if(s<d){d=s;base=122.0;}
s=sd(p,float2(224.70215,157.24121),float2(680.46875,538.12500));if(s<d){d=s;base=122.0;}
s=sd(p,float2(680.46875,538.12500),float2(730.00000,600.00000));if(s<d){d=s;base=122.0;}
s=sd(p,float2(730.00000,600.00000),float2(750.28809,649.82666));if(s<d){d=s;base=122.0;}
s=sd(p,float2(750.28809,649.82666),float2(760.65918,722.14111));if(s<d){d=s;base=122.0;}
s=sd(p,float2(760.65918,722.14111),float2(760.00000,850.00000));if(s<d){d=s;base=122.0;}
s=sd(p,float2(-760.00000,-1370.00000),float2(-880.00000,-1410.00000));if(s<d){d=s;base=59.0;}
s=sd(p,float2(-880.00000,-1410.00000),float2(-1000.00000,-1430.00000));if(s<d){d=s;base=59.0;}
s=sd(p,float2(-760.00000,-1410.00000),float2(-873.48511,-1617.74414));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-873.48511,-1617.74414),float2(-945.59570,-1733.43750));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-945.59570,-1733.43750),float2(-1003.98438,-1806.56250));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1003.98438,-1806.56250),float2(-1071.78711,-1870.46875));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1071.78711,-1870.46875),float2(-1150.00000,-1920.00000));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1150.00000,-1920.00000),float2(-1289.18213,-1976.29028));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1289.18213,-1976.29028),float2(-1452.05078,-2021.57227));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1452.05078,-2021.57227),float2(-1633.46436,-2053.27515));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1633.46436,-2053.27515),float2(-1828.28125,-2068.82812));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-1828.28125,-2068.82812),float2(-2031.35986,-2065.66040));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-2031.35986,-2065.66040),float2(-2322.23511,-2032.58545));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-2322.23511,-2032.58545),float2(-2566.55273,-1989.74609));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-2566.55273,-1989.74609),float2(-2818.12134,-1928.71338));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-2818.12134,-1928.71338),float2(-2982.53784,-1876.55029));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-2982.53784,-1876.55029),float2(-3213.23242,-1779.04297));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3213.23242,-1779.04297),float2(-3350.00000,-1700.00000));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3350.00000,-1700.00000),float2(-3477.34375,-1606.65039));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3477.34375,-1606.65039),float2(-3661.76758,-1439.80103));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3661.76758,-1439.80103),float2(-3776.90430,-1314.87183));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3776.90430,-1314.87183),float2(-3932.03125,-1114.11133));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3932.03125,-1114.11133),float2(-4059.03320,-905.92407));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4059.03320,-905.92407),float2(-4124.16992,-767.79175));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4124.16992,-767.79175),float2(-4171.04492,-630.23071));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4171.04492,-630.23071),float2(-4199.65820,-477.94800));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4199.65820,-477.94800),float2(-4213.28125,-231.39648));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4213.28125,-231.39648),float2(-4198.77930,14.93530));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4198.77930,14.93530),float2(-4177.39258,166.82739));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4177.39258,166.82739),float2(-4149.36523,300.31128));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4149.36523,300.31128),float2(-4117.04102,408.06274));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4117.04102,408.06274),float2(-4080.19409,483.42896));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4080.19409,483.42896),float2(-4026.95923,528.16772));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4026.95923,528.16772),float2(-3994.92188,541.01562));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3994.92188,541.01562),float2(-3923.48633,551.51367));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3923.48633,551.51367),float2(-3808.36792,540.80200));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3808.36792,540.80200),float2(-3641.65039,503.66211));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-3641.65039,503.66211),float2(-3600.00000,500.00000));if(s<d){d=s;base=127.0;}
s=sd(p,float2(-4100.00000,450.00000),float2(-4284.79004,1051.06201));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4284.79004,1051.06201),float2(-4319.40918,1213.63525));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4319.40918,1213.63525),float2(-4333.91113,1365.17334));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4333.91113,1365.17334),float2(-4331.05469,1433.69141));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4331.05469,1433.69141),float2(-4320.09277,1495.71533));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4320.09277,1495.71533),float2(-4300.00000,1550.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4300.00000,1550.00000),float2(-4270.73364,1598.73657));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4270.73364,1598.73657),float2(-4233.44727,1644.97070));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4233.44727,1644.97070),float2(-4137.89062,1730.07812));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4137.89062,1730.07812),float2(-4081.15845,1769.02466));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-4081.15845,1769.02466),float2(-3953.63159,1839.88647));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3953.63159,1839.88647),float2(-3812.48169,1901.61743));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3812.48169,1901.61743),float2(-3663.86108,1954.51050));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3663.86108,1954.51050),float2(-3513.92212,1998.85864));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3513.92212,1998.85864),float2(-3300.00000,2050.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3300.00000,2050.00000),float2(-3158.64258,2075.05859));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3158.64258,2075.05859),float2(-3006.64062,2093.28125));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3006.64062,2093.28125),float2(-2848.97461,2103.61328));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2848.97461,2103.61328),float2(-2690.62500,2105.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2690.62500,2105.00000),float2(-2536.57227,2096.38672));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2536.57227,2096.38672),float2(-2391.79688,2076.71875));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2391.79688,2076.71875),float2(-2261.27930,2044.94141));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2261.27930,2044.94141),float2(-2202.92358,2024.18213));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2202.92358,2024.18213),float2(-2102.09961,1970.91553));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2102.09961,1970.91553),float2(-2058.20312,1935.99609));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2058.20312,1935.99609),float2(-2018.01758,1895.93018));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-2018.01758,1895.93018),float2(-1947.60742,1803.11279));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1947.60742,1803.11279),float2(-1888.52539,1697.97119));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1888.52539,1697.97119),float2(-1838.42773,1586.01318));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1838.42773,1586.01318),float2(-1624.92676,1032.40845));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1624.92676,1032.40845),float2(-1587.01660,900.52856));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1587.01660,900.52856),float2(-1562.70020,765.01587));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1562.70020,765.01587),float2(-1550.00000,650.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1550.00000,650.00000),float2(-1545.19897,520.65796));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1545.19897,520.65796),float2(-1577.41211,-4.54102));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1577.41211,-4.54102),float2(-1579.63013,-238.88184));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1579.63013,-238.88184),float2(-1558.65356,-916.46851));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1558.65356,-916.46851),float2(-1560.04883,-1521.47461));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1560.04883,-1521.47461),float2(-1548.20923,-1699.58862));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1548.20923,-1699.58862),float2(-1531.60034,-1793.16040));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1531.60034,-1793.16040),float2(-1520.00000,-1830.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1520.00000,-1830.00000),float2(-1487.01172,-1883.97461));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1487.01172,-1883.97461),float2(-1465.76416,-1902.62329));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1465.76416,-1902.62329),float2(-1416.32568,-1926.13647));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1416.32568,-1926.13647),float2(-1332.50000,-1935.62500));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-1332.50000,-1935.62500),float2(-1150.00000,-1920.00000));if(s<d){d=s;base=112.0;}
s=sd(p,float2(-3350.00000,-1700.00000),float2(-3325.49805,-1364.06616));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3325.49805,-1364.06616),float2(-3310.00000,-1290.00000));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3310.00000,-1290.00000),float2(-3277.73438,-1206.32812));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3277.73438,-1206.32812),float2(-3213.07617,-1095.32227));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3213.07617,-1095.32227),float2(-3140.81299,-1012.58423));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3140.81299,-1012.58423),float2(-3121.91162,-1003.28979));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3121.91162,-1003.28979),float2(-3093.33984,-1000.22461));if(s<d){d=s;base=115.0;}
s=sd(p,float2(-3093.33984,-1000.22461),float2(-3020.00000,-1020.00000));if(s<d){d=s;base=115.0;}
return float2(d,base);}
};
float2 v6p=P.xy;
float2 v6Warp=float2(24*sin(v6p.y*.013+sin(v6p.x*.004)),19*cos(v6p.x*.011+cos(v6p.y*.006)));
float v6Noise=sin(v6p.x*.007+sin(v6p.y*.009))*cos(v6p.y*.005-v6p.x*.003);
float v6F=(1-smoothstep(.70,1,length((v6p-float2(-3400,1810))/float2(1080,640))+.035*v6Noise))*smoothstep(1220,1390,v6p.y);
float v6M=1-smoothstep(.70,1,length((v6p-float2(-2320,-1960))/float2(800,570))+.045*v6Noise);
float v6R=1-smoothstep(.70,1,length((v6p-float2(-250,-320))/float2(950,480))+.035*v6Noise);
float v6J=1-smoothstep(.65,1,length((v6p-float2(-1310,-1850))/float2(400,300))+.035*v6Noise);
float v6BridgeProtected=1-(1-smoothstep(85,115,abs(v6p.x+350)))*(1-smoothstep(120,155,abs(v6p.y+320)));
float v7Heal=smoothstep(-4700,-4400,v6p.x)*(1-smoothstep(-3800,-3520,v6p.x))*smoothstep(-800,-480,v6p.y)*(1-smoothstep(1000,1230,v6p.y));
float v7World=smoothstep(-5650,-5350,v6p.x)*(1-smoothstep(1750,2150,v6p.x))*smoothstep(-2850,-2600,v6p.y)*(1-smoothstep(2600,2900,v6p.y));
float v7West=1-smoothstep(.45,1,length((v6p-float2(-4400,1420))/float2(600,1000)));
float v7East=1-smoothstep(.55,1,length((v6p-float2(-1640,1070))/float2(700,1580)));
float v7Archive=1-smoothstep(.5,1,length((v6p-float2(750,700))/float2(900,750)));
v6F=max(v6F,max(v7West,v7East)*v7World*(1-v7Heal));
v6F=max(v6F,v7Archive*.72);
v6M=max(v6M,v7World*(1-v6F)*(1-v7Heal));
float v6Scope=max(max(v6F,v6M),max(v6R,v6J))*v6BridgeProtected;
float v6Dist=100000;float v6Half=120;
if(v6Scope>.00001){W6Route route;float2 field=route.nearest(v6p);v6Dist=field.x;v6Half=field.y;}
v6Half+=(15*v6Noise+6*sin(v6p.x*.013-v6p.y*.007))*saturate(v6Half/112.0);
v6Half+=29*(1-smoothstep(45,250,length((v6p-float2(-1220,-1895))*float2(1,1.25))));
float v6EdgeNoise=4*sin(v6p.x*.077+sin(v6p.y*.05))+3*cos(v6p.y*.113-v6p.x*.027);
float v6Coverage=1-smoothstep(v6Half-10,v6Half+17,v6Dist+v6EdgeNoise);
W6Route v7Water;
float v6WetDist=min(v7Water.sd(v6p,float2(-910,-320),float2(1100,-320))-66,min(v7Water.sd(v6p,float2(720,-320),float2(720,-680))-64,(length((v6p-float2(720,-720))/float2(264,190))-1)*185));
float v7R=smoothstep(-30,0,v6WetDist)*(1-smoothstep(180,245,v6WetDist))*v7World;
v6R=max(v6R,v7R);
float v6Shore=13*sin(v6p.x*.017+sin(v6p.x*.005))+12*cos(v6p.x*.033);
float v6BankMask=v6R*smoothstep(2,18,v6WetDist)*(1-smoothstep(72+v6Shore,153+v6Shore,v6WetDist));
float v6Cove=max(1-smoothstep(.40,1,length((v6p-float2(-790,-203))/float2(145,72))),max(1-smoothstep(.40,1,length((v6p-float2(-50,-449))/float2(150,80))),1-smoothstep(.40,1,length((v6p-float2(300,-199))/float2(145,78)))));
v6BankMask=max(v6BankMask,v6Cove*v6R*smoothstep(8,20,v6WetDist))*v6BridgeProtected;
