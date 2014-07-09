import os
import io
import subprocess

def ls_tree(treeish):
    # return all file names and object ids of the given treeish
    git_call = ['git', 'ls-tree', '-r', treeish]

    environ = os.environ.copy()
    proc = subprocess.Popen(
        git_call,
        stdout = subprocess.PIPE,
        env = environ,
        )
    output = proc.communicate()

    if proc.returncode != 0:
        print('git process failed ({})'.format(proc.returncode))
        exit(1)

    result = []
    for l in output[0].decode('utf8').rstrip('\n').split('\n'):
        s = l.rstrip('\n').split()
        name = _unscramble_name(s[3:])

        line = s[:3] + [name]
        result.append(line)

    return result

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

    # elements [5:] will contain the name after the split,
    # we have to piece that stuff back together
    result = []
    for l in output[0].decode('utf8').rstrip('\n').split('\n'):
        s = l.rstrip('\n').split()
        name = _unscramble_name(s[5:])

        line = s[:5] + [name]
        result.append(line)

    return result

def blob_file_handle(obj_id):
    environ = os.environ.copy()
    proc = subprocess.Popen(
        ['git', 'cat-file', 'blob', obj_id],
        stdout=subprocess.PIPE,
        env=environ,
        )
    proc.wait(1000)
    return proc.stdout

import codecs
def _unscramble_name(nameparts):
    name = ' '.join(nameparts)
    # no special chars
    if '\\' not in name:
        return name

    if name[0] == '"':
        name = name.strip('"')

    return codecs.escape_decode(name)[0].decode()

