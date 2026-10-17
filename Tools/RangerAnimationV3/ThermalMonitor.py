import ctypes,json,time,os,sys,subprocess
from pathlib import Path
ctypes.CDLL('/System/Library/Frameworks/Foundation.framework/Foundation');lib=ctypes.CDLL('/usr/lib/libobjc.A.dylib');lib.objc_getClass.argtypes=[ctypes.c_char_p];lib.objc_getClass.restype=ctypes.c_void_p;lib.sel_registerName.argtypes=[ctypes.c_char_p];lib.sel_registerName.restype=ctypes.c_void_p
send=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));scalar=ctypes.CFUNCTYPE(ctypes.c_long,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));obj=send(lib.objc_getClass(b'NSProcessInfo'),lib.sel_registerName(b'processInfo'))
p=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster/Saved/RangerAnimationV3');p.mkdir(exist_ok=True);tag='Repair' if '--repair' in sys.argv else '';stop=p/('StopThermal'+tag+'.txt')
with (p/('Thermal'+tag+'.jsonl')).open('a') as f:
 while not stop.exists():
  state=scalar(obj,lib.sel_registerName(b'thermalState'));f.write(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'thermal_state':state,'thermal_label':['nominal','fair','serious','critical'][state] if 0<=state<=3 else 'unknown','loadavg':os.getloadavg(),'power':subprocess.check_output(['pmset','-g','batt'],text=True).strip()})+'\n');f.flush()
  if '--once' in sys.argv:print(state);break
  time.sleep(10)
