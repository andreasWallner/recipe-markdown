import unittest
from utils import *

class XmlTestMixinTest(unittest.TestCase):
    def setUp(self):
        class Mock(XmlTestMixin):
            pass
        self.m = Mock()

    def test_match(self):
        # we can skip a bit of stuff here since we are testing a
        # class that will be a mixin to unittest anyhow
        # it therefore raises the right exceptions etc.

        self.m.assertXmlEqual('<root />', '<root />')
        self.m.assertXmlEqual('<root></root>', '<root />')
        self.m.assertXmlEqual('<root foo="x" />', '<root foo="x" />')
        self.m.assertXmlEqual('<r f="a" b="b" />', '<r f="a" b="b" />')
        self.m.assertXmlEqual('<r f="a" b="b" />', '<r b="b" f="a" />')

        self.m.assertXmlEqual('<root foo="x" />', '<root foo="..." />')
        self.m.assertXmlEqual('<r><n /></r>', '<r><n /></r>')
        self.m.assertXmlEqual('<r><n /></r>', '<r>...</r>')

    def test_nomatch(self):
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<r />', '<b />')
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<a /><b />', '<b /><a />')
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<r foo="x" />', '<r foo="b" />')
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<r foo="x" />', '<r bar="x" />')
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<r foo="x" />', '<r bar="..." />')
        self.assertRaises(AssertionError, self.m.assertXmlEqual, '<r><s>a</s><s>b</s></r>', '<r><s>...</s>')

    def test_message(self):
        with self.assertRaises(AssertionError) as context:
            self.m.assertXmlEqual('<r />', '<b />')
        self.assertEqual(context.exception.args[0], 'Expected:\n  <b></b>\n\nGot:\n  <r></r>\n\nDiff:\n  <b (got: r)></b (got: r)>\n')
