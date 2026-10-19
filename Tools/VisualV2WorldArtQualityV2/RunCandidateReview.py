from Control import R,O,job
import json,time,sys
mode=sys.argv[1];assert mode in ['Merged','V2'];label='Review_'+mode;assert not (O/'Photos'/label).exists();(O/'ReviewVariant.json').write_text(json.dumps({'mode':mode}));(O/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':2560,'height':1440,'percentage':100}));job('SetReviewVariant.py');time.sleep(4);job('Photos.py');start=time.monotonic()
while not (O/'Photos'/label/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<65
print('REVIEW PHOTOS COMPLETE',mode,flush=True)
