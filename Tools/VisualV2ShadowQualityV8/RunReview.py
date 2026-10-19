import json,time,sys
from Control import O,job
variant,label,gain,debug=sys.argv[1:5];views=sys.argv[5:];assert variant in ['A','B','C'];gain=float(gain);debug=float(debug)
req={'variant':variant,'gain':gain,'debug':debug,'low':.40,'high':1.20};(O/'VariantRequest.json').write_text(json.dumps(req));job('RuntimeVariant.py');time.sleep(3)
(O/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':2560,'height':1440,'percentage':100,'quality':1,'variant':req,'views':views}));job('Photos.py');start=time.monotonic()
while not (O/'Photos'/label/'Result.json').exists():
 time.sleep(1);assert time.monotonic()-start<150
print('REVIEW COMPLETE',label,flush=True)
