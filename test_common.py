import unittest
import tempfile
import utils
import os
from os import path
from common import *

class tests(unittest.TestCase):
    def test_xml_filename(self):
        self.assertEqual(xml_filename('foo.rmd', 'foo/bar'), 'foo/bar/foo.xml')
        self.assertEqual(xml_filename('bar.rmd', 'foo/bar/'), 'foo/bar/bar.xml')
        self.assertEqual(xml_filename('baz.rmd', '/root/'), '/root/baz.xml')
        self.assertRaises(Exception, xml_filename, ('blub.xml', ''))

    def test_clean_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            with utils.ChangeDir(tmp):
                open('should_delete.xml', 'w').close()
                open('should_not_xml', 'w').close()

            clean_output_dir(tmp)

            files = [f for f in os.listdir(tmp) if path.isfile(path.join(tmp, f))]
            self.assertEqual(files, ['should_not_xml'])