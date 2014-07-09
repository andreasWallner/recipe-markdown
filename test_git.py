import unittest
import tempfile
import utils
import subprocess
import os, io
import git

def _run_command(command, timeout=2000):
    environment = os.environ.copy()
    proc = subprocess.Popen(
        command,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        env = environment,
        )
    output = proc.communicate()

    if proc.returncode != 0:
        raise Exception('command failed {!r}'.format(command), output)

    return [ l.rstrip('\n') for l in output[0].decode('utf8').split('\n') ]

def _write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

class tests(unittest.TestCase, utils.TypeCheckMixin):
    def _setup_git(self):
        _run_command(['git', 'init'])
        _write_file('change', 'bar')
        _write_file('delete', 'bar')
        _run_command(['git', 'add', '.'])
        _run_command(['git', 'commit', '-m first'])

    def _second_commit(self):
        _write_file('new', 'bar')
        _write_file('change', 'foo')
        _write_file('with space', 'asdf')
        _write_file('utf8_ß', 'damn utf8')
        _write_file('"quote', 'content')
        _run_command(['git', 'rm', 'delete'])
        _run_command(['git', 'add', '.'])
        _run_command(['git', 'commit', '-m second'])

    def test_ls_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            with utils.ChangeDir(tmp):
                self._setup_git()
                self._second_commit()

                tree = git.ls_tree('HEAD')
                self.assertEqual(tree, result['tree'])

    def test_changed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            with utils.ChangeDir(tmp):
                self._setup_git()
                changes = git.changed_files('0000000000000000000000000000000000000000', 'HEAD')
                self.assertEqual(changes, result['first'])

                self._second_commit()
                changes = git.changed_files('HEAD^', 'HEAD')
                self.assertEqual(changes, result['second'])

    def test_blob_file_handle(self):
        with tempfile.TemporaryDirectory() as tmp:
            with utils.ChangeDir(tmp):
                self._setup_git()
                with git.blob_file_handle('ba0e162e1c47469e3fe4b393a8bf8c569f302116') as f:
                    self.assertType( f, io.BufferedReader)
                    content = f.readlines()
                    self.assertEqual(content, [b'bar'])

result = {
    'tree' : [
        ['100644', 'blob', '6b584e8ece562ebffc15d38808cd6b98fc3d97ea', '"quote'],
        ['100644', 'blob', '19102815663d23f8b75a47e7a01965dcdc96468c', 'change'],
        ['100644', 'blob', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', 'new'],
        ['100644', 'blob', 'b1af804585a1702ac00b132467d87d56e855324d', 'utf8_ß'],
        ['100644', 'blob', '5e40c0877058c504203932e5136051cf3cd3519b', 'with space'],
        ],
    'first' : [
        [':000000', '100644', '0000000000000000000000000000000000000000', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', 'A', 'change'],
        [':000000', '100644', '0000000000000000000000000000000000000000', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', 'A', 'delete'],
        ],
    'second' : [
        [':000000', '100644', '0000000000000000000000000000000000000000', '6b584e8ece562ebffc15d38808cd6b98fc3d97ea', 'A', '"quote'],
        [':100644', '100644', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', '19102815663d23f8b75a47e7a01965dcdc96468c', 'M', 'change'],
        [':100644', '000000', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', '0000000000000000000000000000000000000000', 'D', 'delete'],
        [':000000', '100644', '0000000000000000000000000000000000000000', 'ba0e162e1c47469e3fe4b393a8bf8c569f302116', 'A', 'new'],
        [':000000', '100644', '0000000000000000000000000000000000000000', 'b1af804585a1702ac00b132467d87d56e855324d', 'A', 'utf8_ß'],
        [':000000', '100644', '0000000000000000000000000000000000000000', '5e40c0877058c504203932e5136051cf3cd3519b', 'A', 'with space'],
        ],
    }

