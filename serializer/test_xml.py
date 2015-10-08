import unittest
from .xml import serialize
from pieces import *
from utils import XmlTestMixin

class serializeTests(unittest.TestCase, XmlTestMixin):
    def test_ingredient_all(self):
        i = Ingredient('name', 'amount', 'unit')
        e = etree.Element('root')
        serialize(i, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['ingredient']['amount'])

    def test_ingredient_nounit(self):
        i = Ingredient('name', 'amount', None)
        e = etree.Element('root')
        serialize(i, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['ingredient']['nounit'])

    def test_ingredient_noamount(self):
        i = Ingredient('name', None, None)
        e = etree.Element('root')
        serialize(i, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['ingredient']['noamount'])
    def test_step(self):
        s = Step('text')
        e = etree.Element('root')
        serialize(s, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['step'])

    def test_note(self):
        n = Note('text')
        e = etree.Element('root')
        serialize(n, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['note'])

    def test_waitphase(self):
        h = WaitPhase('text')
        e = etree.Element('root')
        serialize(h, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['waitphase'])

    def test_part(self):
        p = Part('text')
        e = etree.Element('root')
        serialize(p, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['part'])

    def test_phase(self):
        i = Ingredient('name',None,None)
        s1 = Step('step1')
        s2 = Step('step2')
        p = Phase([i],[s1,s2])
        e = etree.Element('root')
        serialize(p, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['phase'])

    def test_recipe(self):
        p = Phase()
        r = Recipe(
            'title',
            'size',
            'de',
            'source',
            'author',
            'description',
            [p],
            ['k1', 'k2'],
            ['img1.jpg', 'img2.jpg'],
            )
        e = etree.Element('root')
        serialize(r, e)

        self.assertXmlEqual(etree.tounicode(e), serialization['recipe'])
    
serialization = {
    'ingredient' : {
        'amount' : '<root><ingredient><name>name</name><amount>amount</amount><unit>unit</unit></ingredient></root>',
        'nounit' : '<root><ingredient><name>name</name><amount>amount</amount></ingredient></root>',
        'noamount' : '<root><ingredient><name>name</name></ingredient></root>',
    },
    'step' : '<root><step>text</step></root>',
    'note' : '<root><note>text</note></root>',
    'waitphase' : '<root><waitphase>text</waitphase></root>',
    'part' : '<root><part>text</part></root>',
    'phase': '<root><phase><ingredient>...</ingredient><step>step1</step><step>step2</step></phase></root>',
    'recipe': """<root>
                   <recipe>
                     <meta>
                       <title>title</title>
                       <size>size</size>
                       <lang>de</lang>
                       <source>source</source>
                       <author>author</author>
                       <description>
                         <p>description</p>
                       </description>
                       <keywords>
                         <keyword>k1</keyword>
                         <keyword>k2</keyword>
                       </keywords>
                       <images>
                         <img>img1.jpg</img>
                        <img>img2.jpg</img>
                       </images>
                     </meta>
                     <instructions>
                       <phase />
                     </instructions>
                   </recipe>
                 </root>""",
}
