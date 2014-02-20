import os
import io
import subprocess

def changed_files(old,new):
    # if old is before the first commit, it will be all zeros, which is invalid
    # therefore just make it blank
    git_call = ['git', 'diff-tree', '--full-index', '--root', '--no-commit-id', old, new]
    if len(old.strip('0')) == 0: 
        del git_call[-2]

    environ = os.environ.copy()
    proc = subprocess.Popen(
        git_call,
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
