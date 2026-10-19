// Diagnostic shadow-like floor lift, NOT an exact VSM shadow-factor modification.
// Post-tonemap stage: the existing light, GI, exposure, TAA and bloom settings stay untouched.
float3 rgb=max(Color.rgb,0);float3 lum=float3(.2126,.7152,.0722);
float albedo=max(dot(Diffuse.rgb,lum),.025);float illumination=dot(rgb,lum)/albedo;
float darkMask=1-smoothstep(Low,High,illumination);
float floorMask=smoothstep(.68,.94,Normal.z)*(1-smoothstep(20,45,Position.z));
float exterior=1-smoothstep(2500,4000,Position.x);
float contact=1;
contact*=smoothstep(Contact0.w,Contact0.w+24,length(Position.xy-Contact0.xy));
contact*=smoothstep(Contact1.w,Contact1.w+24,length(Position.xy-Contact1.xy));
contact*=smoothstep(Contact2.w,Contact2.w+24,length(Position.xy-Contact2.xy));
contact*=smoothstep(Contact3.w,Contact3.w+24,length(Position.xy-Contact3.xy));
contact*=smoothstep(Contact4.w,Contact4.w+24,length(Position.xy-Contact4.xy));
contact*=smoothstep(Contact5.w,Contact5.w+24,length(Position.xy-Contact5.xy));
contact*=smoothstep(Contact6.w,Contact6.w+24,length(Position.xy-Contact6.xy));
contact*=smoothstep(Contact7.w,Contact7.w+24,length(Position.xy-Contact7.xy));
contact*=smoothstep(Contact8.w,Contact8.w+24,length(Position.xy-Contact8.xy));
contact*=smoothstep(Contact9.w,Contact9.w+24,length(Position.xy-Contact9.xy));
contact*=smoothstep(Contact10.w,Contact10.w+24,length(Position.xy-Contact10.xy));
contact*=smoothstep(Contact11.w,Contact11.w+24,length(Position.xy-Contact11.xy));
contact*=smoothstep(Contact12.w,Contact12.w+24,length(Position.xy-Contact12.xy));
contact*=smoothstep(Contact13.w,Contact13.w+24,length(Position.xy-Contact13.xy));
contact*=smoothstep(Contact14.w,Contact14.w+24,length(Position.xy-Contact14.xy));
contact*=smoothstep(Contact15.w,Contact15.w+24,length(Position.xy-Contact15.xy));

// Keep the foot of the two existing exterior buildings firmly grounded.
float2 h=abs(Position.xy-float2(-3140,500))-float2(460,650);
float dh=length(max(h,0))+min(max(h.x,h.y),0);
float2 c=abs(Position.xy-float2(-2750,-1020))-float2(300,300);
float dc=length(max(c,0))+min(max(c.x,c.y),0);
contact*=smoothstep(0,36,dh)*smoothstep(0,30,dc);
float aoGuard=smoothstep(.05,.20,AO.r);
float mask=darkMask*floorMask*exterior*contact;
if(Debug>2.5)return float3(darkMask,floorMask,contact);
if(Debug>1.5)return saturate(illumination/2).xxx;
if(Debug>.5)return mask.xxx;
return Color.rgb+rgb*Gain*mask;
