// Reuse authored V4 earth; color only, without changing any light or shadow values.
float3 v6Earth=Texture2DSample(W6Earth,W6EarthSampler,(p+v6Warp*.6)/226.0+float2(.19,.43)).rgb*.66+Texture2DSample(W6Earth,W6EarthSampler,(float2(p.y,-p.x)-v6Warp*.45)/357.0+float2(.61,.27)).rgb*.34;
float v6FootWear=1-smoothstep(24,v6Half-12,v6Dist);
float3 v6ForestSoil=lerp(v6Earth*float3(.78,.73,.62),waForest*float3(.74,.77,.64),.13+.17*(1-v6FootWear));
float3 v6MeadowSoil=v6Earth*float3(.90,.83,.71);
float3 v6BankSoil=lerp(v6Earth*float3(.84,.80,.70),waBank*float3(.78,.78,.69),.24);
float3 v6PathColor=lerp(v6MeadowSoil,v6ForestSoil,v6F);v6PathColor=lerp(v6PathColor,v6BankSoil,v6R);
v6PathColor*=1+.045*v6Noise+.035*v6FootWear;
float v6MossPatch=.5+.24*sin(p.x*.006+cos(p.y*.008))+.22*cos(p.y*.011-p.x*.002);
float v6Clearing=(1-smoothstep(.35,1,length((p-float2(-3210,2190))/float2(220,160))))+.65*(1-smoothstep(.30,1,length((p-float2(-2905,1495))/float2(160,115))));
float3 v6ForestSurface=waForest*lerp(float3(.79,.82,.69),float3(.71,.87,.66),saturate(v6MossPatch));
v6ForestSurface=lerp(v6ForestSurface,v6Earth*float3(.78,.76,.65),saturate(v6Clearing)*.36);
g=lerp(g,v6ForestSurface,v6F*.76);
g*=1+v6M*.045*(sin(p.x*.004+p.y*.002)*cos(p.y*.006));
g=lerp(g,waBank*float3(.75,.77,.69)*(1+.045*v6Noise),v6BankMask*.87);
g=lerp(g,v6PathColor,v6Scope*v6Coverage);
