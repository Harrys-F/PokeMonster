"""Bounded review through Unreal's proven Shot/SaveImageByExtension path.
No framebuffer-format, rendering-quality, camera or production settings change.
"""
import unreal,time,csv,json
from pathlib import Path
class ScreenshotReview:
 def __init__(self,world,directory,game_time):
  self.world=world;self.directory=Path(directory);root=Path(unreal.Paths.project_dir()).resolve()/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';assert self.directory.resolve().is_relative_to(root);self.directory.mkdir(exist_ok=False);self.started=game_time;self.last=-1.;self.frames=[];self.pending=None;self.active=True;self.done=False;self.csv_path=self.directory/'Frames.csv';self.csv_path.write_text('frame,game_seconds,wall_seconds,width,height,file\n')
 def dimensions(self,p):
  data=p.read_bytes();assert data[:2]==b'\xff\xd8','Not an actual JPEG';i=2
  while i+9<len(data):
   if data[i]!=255:i+=1;continue
   marker=data[i+1];i+=2
   if marker in [0xD8,0xD9]or marker==0:continue
   n=int.from_bytes(data[i:i+2],'big')
   if marker in [0xC0,0xC1,0xC2]:return int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')
   i+=n
  raise AssertionError('JPEG has no dimensions')
 def stop(self):self.active=False
 def tick(self,game_time):
  if self.done:return
  if self.pending:
   item=self.pending;p=self.directory/item['file']
   if p.exists():
    assert p.stat().st_size>90000,'Blank/invalid screenshot rejected';w,h=self.dimensions(p);assert (w,h)==(2560,1440),(w,h);item.update(width=w,height=h);item.pop('requested_wall');self.frames.append(item);self.pending=None
    with self.csv_path.open('a',newline='')as f:csv.DictWriter(f,fieldnames=['frame','game_seconds','wall_seconds','width','height','file']).writerow(item)
   else:assert time.monotonic()-item['requested_wall']<12,'Screenshot request did not complete';return
  if not self.active:
   (self.directory/'Metrics.json').write_text(json.dumps({'frames':len(self.frames),'first_game_time':self.started,'pipeline':'Unreal Shot JPEG, existing screenshot save path','requested_game_interval':1/15,'rendering_overrides':False,'blank_size_guard':90000},indent=2));(self.directory/'Complete.txt').write_text(str(len(self.frames)));self.done=True;return
  if game_time-self.last<1/15-1.e-6:return
  if len(self.frames)>=1200:self.active=False;return
  if self.last<0:self.started=game_time
  index=len(self.frames);name='Frame_'+str(index).zfill(5)+'.jpg';self.pending={'frame':index,'game_seconds':game_time-self.started,'wall_seconds':time.monotonic(),'file':name,'requested_wall':time.monotonic()};self.last=game_time
  unreal.SystemLibrary.execute_console_command(self.world,'Shot filename="'+str(self.directory/name)+'" -nosuffix')
