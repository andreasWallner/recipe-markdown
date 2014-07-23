import unittest
import tempfile
import utils
import subprocess
import os, io
import git
import inspect

_current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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
    def _setup_target_git(self, target, outdir):
        with utils.ChangeDir(target):
            _run_command(['git', 'init', '--bare'])
            os.symlink(_current_dir + '/update-hook.py', 'hooks/update')
            _write_file('hooks/settings.py', settings.format(outdir))

    def _setup_source_git(self, source, target):
        with utils.ChangeDir(source):
            _run_command(['git', 'init'])
            _run_command(['git', 'remote', 'add', 'target', target])
            _run_command(['git', 'config', 'push.default', 'simple'])
    
    def test_all(self):
        with tempfile.TemporaryDirectory() as source:
            with tempfile.TemporaryDirectory() as target:
                with tempfile.TemporaryDirectory() as outdir:
                    self._setup_target_git(target, outdir)
                    self._setup_source_git(source, target)
                
                    self._real_test_all(source, target, outdir)

    def _real_test_all(self, source, target, outdir):
        # for now we'll just be happy that the files are there
        with utils.ChangeDir(source):
            _write_file('ignore.foo', 'foobar')
            _write_file('add.rmd', add_text)
            _run_command(['git', 'add', '.'])
            _run_command(['git', 'commit', '-m', 'add step'])
            _run_command(['git', 'push', 'target', 'master'])

        with utils.ChangeDir(outdir):
            self.assertTrue(os.path.isfile('add.xml'), 'Xml has not been generated')
            self.assertTrue(os.path.isfile('index.html'), 'Index has not been generated')

            os.remove('add.xml')
            os.remove('index.html')

        with utils.ChangeDir(source):
            _write_file('add.rmd', change_text)
            _run_command(['git', 'commit', '-am', 'change step'])
            _run_command(['git', 'push', 'target', 'master'])

        with utils.ChangeDir(outdir):
            self.assertTrue(os.path.isfile('add.xml'), 'Xml has not been generated')
            self.assertTrue(os.path.isfile('index.html'), 'Index has not been generated')

            os.remove('index.html')

        with utils.ChangeDir(source):
            _run_command(['git', 'rm', 'add.rmd'])
            _run_command(['git', 'commit', '-m', 'delete step'])
            _run_command(['git', 'push', 'target', 'master'])

        with utils.ChangeDir(outdir):
            self.assertFalse(os.path.isfile('add.xml'), 'Xml has not been deleted')
            self.assertTrue(os.path.isfile('index.html'), 'Index has not been generated')


settings = """
TARGET="{}/"
XSLT="recipe2html.xslt"
UMASK=0o022
"""

add_text = """
!title: Test

# Ingredient
* Step
"""

change_text = """
!title: Change Test

# Ingredient
* Step
"""

