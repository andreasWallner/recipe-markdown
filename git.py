import os
import io
import subprocess

def changed_files(old,new):
   environ = os.environ.copy()
   proc = subprocess.Popen(['git','diff-tree','--full-index',old,new], stdout=subprocess.PIPE, env=environ)
   proc.wait(1000)

   if proc.returncode != 0:
      print('git process failed ({})'.format(proc.returncode))
      exit(1)

   return [ l.decode('utf8').strip('\n').split() for l in proc.stdout ]

def blob_file_handle(obj_id):
    environ = os.environ.copy()
    proc = subprocess.Popen(['git','cat-file','blob',obj_id], stdout=subprocess.PIPE, env=environ)
    proc.wait(1000)
    return proc.stdout
