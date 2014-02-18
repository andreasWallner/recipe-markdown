import os
import io
import subprocess

def changed_files(old,new):
    environ = os.environ.copy()
    proc = subprocess.Popen(
        ['git', 'diff-tree', '--full-index', old, new],
        stdout=subprocess.PIPE,
        env=environ,
        )
    output = proc.communicate()

    if proc.returncode != 0:
        print('git process failed ({})'.format(proc.returncode))
        exit(1)

    return [ l.rstrip('\n').split() for l in output[0].decode('utf8').rstrip('\n').split('\n') ]

def blob_file_handle(obj_id):
    environ = os.environ.copy()
    proc = subprocess.Popen(
        ['git', 'cat-file', 'blob', obj_id],
        stdout=subprocess.PIPE,
        env=environ,
        )
    proc.wait(1000)
    return proc.stdout
