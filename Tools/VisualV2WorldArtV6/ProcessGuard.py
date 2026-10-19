"""Recognize actual editor executables, never a shell command mentioning their path."""
import subprocess,time

def editor_pids():
 rows=subprocess.run(['ps','-axo','pid=,comm='],check=True,capture_output=True,text=True).stdout.splitlines()
 return [int(row.strip().split(None,1)[0]) for row in rows if len(row.strip().split(None,1))==2 and row.strip().split(None,1)[1].endswith('/Contents/MacOS/UnrealEditor')]

def wait_closed(seconds=90):
 start=time.monotonic()
 while editor_pids():
  assert time.monotonic()-start<seconds,'Existing editor is still running; never terminate it automatically'
  time.sleep(.5)
if __name__=='__main__':wait_closed();print('No active Unreal editor/game process',flush=True)
