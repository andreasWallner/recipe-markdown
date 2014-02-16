import unittest
from errors import *
from pieces import *
from lxml import etree
from utils import XmlTestMixin

class IngredientTest(unittest.TestCase, XmlTestMixin):
    def test_init(self):
        i = Ingredient('name','amount','unit')
        self.assertEqual(i.name, 'name')
        self.assertEqual(i.amount, 'amount')
        self.assertEqual(i.unit, 'unit')

    def test_init_fail(self):
        with self.assertRaises(RecipeParseError) as context:
            i = Ingredient('name','amount',None)
        with self.assertRaises(RecipeParseError) as context:
            i = Ingredient('name',None,'unit')

    def test_serialize(self):
        i = Ingredient('name','amount','unit')
        e = etree.Element('root')
        i.serialize(e)

        self.assertXmlEqual(etree.tounicode(e),serialization['ingredient']['amount'])

    def test_serialize_noamount(self):
        i = Ingredient('name',None,None)
        e = etree.Element('root')
        i.serialize(e)

        self.assertXmlEqual(etree.tounicode(e),serialization['ingredient']['noamount'])

    def test_repr(self):
        i = Ingredient('name','amount','unit')
        self.assertEqual(repr(i),"Ingredient('name', 'amount', 'unit')")

    def test_repr_noamount(self):
        i = Ingredient('name',None,None)
        self.assertEqual(repr(i),"Ingredient('name', None, None)")

class StepTest(unittest.TestCase, XmlTestMixin):
    def test_init(self):
        s = Step('text')
        self.assertEqual(s.text, 'text')

    def test_serialize(self):
        s = Step('text')
        e = etree.Element('root')
        s.serialize(e)

        self.assertXmlEqual(etree.tounicode(e), serialization['step'])

    def test_repr(self):
        s = Step('text')
        self.assertEqual(repr(s),"Step('text')")

class HintTest(unittest.TestCase,XmlTestMixin):
    def test_init(self):
        h = Hint('text')
        self.assertEqual(h.text, 'text')

    def test_serialize(self):
        h = Hint('text')
        e = etree.Element('root')
        h.serialize(e)

        self.assertXmlEqual(etree.tounicode(e), serialization['hint'])

    def test_repr(self):
        h = Hint('text')
        self.assertEqual(repr(h),"Hint('text')")

class PhaseTest(unittest.TestCase,XmlTestMixin):
    def test_init(self):
        p = Phase()
        self.assertEqual(p.ingredients,[])
        self.assertEqual(p.steps,[])

        i = Ingredient('name',None,None)
        s = Step('text')
        p = Phase([i],[s])
        self.assertEqual(p.ingredients, [i])
        self.assertEqual(p.steps, [s])

    def test_serialize(self):
        i = Ingredient('name',None,None)
        s1 = Step('step1')
        s2 = Step('step2')
        p = Phase([i],[s1,s2])
        e = etree.Element('root')
        p.serialize(e)

        self.assertXmlEqual(etree.tounicode(e), serialization['phase'])

class RecipeTest(unittest.TestCase,XmlTestMixin):
    def test_init(self):
        r = Recipe('title', 'size', 'source', 'author')
        self.assertEqual(r.title, 'title')
        self.assertEqual(r.size, 'size')
        self.assertEqual(r.source, 'source')
        self.assertEqual(r.author, 'author')
        self.assertEqual(r.phases, [])

        p = Phase()
        r = Recipe(None, None, None, None, [p])
        self.assertEqual(r.title, None)
        self.assertEqual(r.size, None)
        self.assertEqual(r.source, None)
        self.assertEqual(r.author, None)
        self.assertEqual(r.phases, [p])

    def test_serialize(self):
        p = Phase()
        r = Recipe('title', 'size', 'source', 'author', [p])
        e = etree.Element('root')
        r.serialize(e)

        self.assertXmlEqual(etree.tounicode(e), serialization['recipe'])
    
    def test_repr(self):
        r = Recipe('title', 'size', 'source', 'author')
        self.assertEqual(repr(r), "Recipe('title', 'size', 'source', 'author', [])")
        

if __name__ == '__main__':
    unittest.main()

serialization = {
    'ingredient' : {
        'amount' : '<root><ingredient><name>name</name><amount>amount</amount><unit>unit</unit></ingredient></root>',
        'noamount' : '<root><ingredient><name>name</name></ingredient></root>',
    },
    'step' : '<root><step>text</step></root>',
    'hint' : '<root><hint>text</hint></root>',
    'phase': '<root><phase><ingredient>...</ingredient><step>step1</step><step>step2</step></phase></root>',
    'recipe': """<root>
                   <recipe>
                     <meta>
                       <title>title</title>
                       <size>size</size>
                       <source>source</source>
                       <author>author</author>
                     </meta>
                     <instructions>
                       <phase />
                     </instructions>
                   </recipe>
                 </root>""",
}
