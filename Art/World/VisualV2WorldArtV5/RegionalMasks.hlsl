float waNoise=sin(p.x*.009+sin(p.y*.007))*cos(p.y*.012-p.x*.003);
float waF=(1-smoothstep(.68,1.0,length((p-float2(-3400,1810))/float2(1080,640))+.045*waNoise))*smoothstep(1220,1390,p.y);
float waM=1-smoothstep(.68,1.0,length((p-float2(-2320,-1960))/float2(800,570))+.065*waNoise);
float waRiverRegion=1-smoothstep(.68,1.0,length((p-float2(-250,-320))/float2(950,480))+.045*waNoise);
float waDistance=abs(p.y+320)-66;float waU=waRiverRegion*smoothstep(-5,18,waDistance)*(1-smoothstep(85,205,waDistance));
float waClear=1-.24*(1-smoothstep(.45,1,length((p-float2(-3210,2190))/float2(220,160))));
