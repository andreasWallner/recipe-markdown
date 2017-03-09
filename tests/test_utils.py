import unittest
from recipemd.utils import *


class XmlTestMixinTest(unittest.TestCase, XmlTestMixin):
    def test_match(self):
        # we can skip a bit of stuff here since we are testing a
        # class that will be a mixin to unittest anyhow
        # it therefore raises the right exceptions etc.

        self.assertXmlEqual('<root />', '<root />')
        self.assertXmlEqual('<root></root>', '<root />')
        self.assertXmlEqual('<root foo="x" />', '<root foo="x" />')
        self.assertXmlEqual('<r f="a" b="b" />', '<r f="a" b="b" />')
        self.assertXmlEqual('<r f="a" b="b" />', '<r b="b" f="a" />')

        self.assertXmlEqual('<root foo="x" />', '<root foo="..." />')
        self.assertXmlEqual('<r><n /></r>', '<r><n /></r>')
        self.assertXmlEqual('<r><n /></r>', '<r>...</r>')

    def test_nomatch(self):
        eq = self.assertXmlEqual
        self.assertRaises(AssertionError, eq, '<r />', '<b />')
        self.assertRaises(AssertionError, eq, '<a /><b />', '<b /><a />')
        self.assertRaises(AssertionError, eq, '<r foo="x" />', '<r foo="b" />')
        self.assertRaises(AssertionError, eq, '<r foo="x" />', '<r bar="x" />')
        self.assertRaises(AssertionError, eq, '<r foo="x" />', '<r bar="..." />')
        self.assertRaises(AssertionError, eq, '<r><s>a</s><s>b</s></r>', '<r><s>...</s>')

    def test_message(self):
        with self.assertRaises(AssertionError) as context:
            self.assertXmlEqual('<r />', '<b />')
        self.assertEqual(context.exception.args[0], 'Expected:\n  <b></b>\n\nGot:\n  <r></r>\n\nDiff:\n  <b (got: r)></b (got: r)>\n')

class extensionTest(unittest.TestCase):
    def test_normal(self):
        x = extension('foo.rmd')
        self.assertEqual(x, 'rmd')

    def test_noext(self):
        x = extension('foo')
        self.assertIsNone(x)

    def test_multiple(self):
        x = extension('foo.rmd.xml')
        self.assertEqual(x, 'xml')

class ChangeDirTest(unittest.TestCase):
    def setUp(self):
        # TODO make test work on windows too
        self.testdir = '/tmp'

    def test_normal(self):
        old = os.getcwd()
        with ChangeDir(self.testdir):
            self.assertEqual(os.getcwd(), self.testdir)
        self.assertEqual(os.getcwd(), old)

    def test_manual(self):
        old = os.getcwd()
        c = ChangeDir(self.testdir)
        self.assertEqual(os.getcwd(), self.testdir)

        c.cleanup()
        self.assertEqual(os.getcwd(), old)

    def test_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            c = ChangeDir(self.testdir)
            del c
            
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, ResourceWarning))
            self.assertIn('Implicit cleanup of <recipemd.utils.ChangeDir object at', str(w[-1].message))
