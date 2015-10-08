import unittest
from errors import *
from pieces import *
from lxml import etree
from utils import XmlTestMixin, RealEqualMixin

class IngredientTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        i = Ingredient('name', 'amount', 'unit')
        self.assertEqual(i.name, 'name')
        self.assertEqual(i.amount, 'amount')
        self.assertEqual(i.unit, 'unit')
    
    def test_no_unit(self):
        i = Ingredient('name', '5', None)
        self.assertEqual(i.name, 'name')
        self.assertEqual(i.amount, '5')
        self.assertIsNone(i.unit)

    def test_init_fail(self):
        with self.assertRaises(RecipeParseError) as context:
            i = Ingredient(None, '5', 'g')
        with self.assertRaises(RecipeParseError) as context:
            i = Ingredient('name',None,'unit')

    def test_repr(self):
        i = Ingredient('name', 'amount', 'unit')
        self.assertEqual(repr(i), "Ingredient('name', 'amount', 'unit')")

    def test_repr_noamount(self):
        i = Ingredient('name', None, None)
        self.assertEqual(repr(i), "Ingredient('name', None, None)")

    def test_compare(self):
        self.assertRealEqual(Ingredient('n', None, None), Ingredient('n', None, None))
        self.assertRealEqual(Ingredient('n', 'a', 'u'), Ingredient('n', 'a', 'u'))

        self.assertRealNotEqual(Ingredient('n', None, None), Ingredient('m', None, None))
        self.assertRealNotEqual(Ingredient('n', 'a', 'u'), Ingredient('n', 'b', 'u'))
        self.assertRealNotEqual(Ingredient('n', 'a', 'u'), Ingredient('n', 'a', 'p'))

class StepTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        s = Step('text')
        self.assertEqual(s.text, 'text')

    def test_repr(self):
        s = Step('text')
        self.assertEqual(repr(s),"Step('text')")

    def test_compare(self):
        self.assertRealEqual(Step('foo'), Step('foo'))
        self.assertRealNotEqual(Step('foo'), Step('bar'))

class NoteTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        n = Note('text')
        self.assertEqual(n.text, 'text')

    def test_repr(self):
        n = Note('text')
        self.assertEqual(repr(n),"Note('text')")

    def test_compare(self):
        self.assertRealEqual(Note('foo'), Note('foo'))
        self.assertRealNotEqual(Note('foo'), Note('bar'))

class WaitPhaseTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        h = WaitPhase('text')
        self.assertEqual(h.text, 'text')

    def test_repr(self):
        h = WaitPhase('text')
        self.assertEqual(repr(h),"WaitPhase('text')")

    def test_compare(self):
        self.assertRealEqual(WaitPhase('foo'), WaitPhase('foo'))
        self.assertRealNotEqual(WaitPhase('foo'), WaitPhase('bar'))

class PartTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        p = Part('text')
        self.assertEqual(p.text, 'text')

    def test_repr(self):
        p = Part('text')
        self.assertEqual(repr(p),"Part('text')")

    def test_compare(self):
        self.assertRealEqual(Part('foo'), Part('foo'))
        self.assertRealNotEqual(Part('foo'), Part('bar'))

class PhaseTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        p = Phase()
        self.assertEqual(p.ingredients,[])
        self.assertEqual(p.steps,[])

        i = Ingredient('name',None,None)
        s = Step('text')
        p = Phase([i],[s])
        self.assertEqual(p.ingredients, [i])
        self.assertEqual(p.steps, [s])

    def test_compare(self):
        i1 = Ingredient('name',None,None)
        i2 = Ingredient('foo',None,None)
        s1 = Step('step1')
        s2 = Step('step2')
        
        self.assertRealEqual(Phase(), Phase())
        self.assertRealEqual(Phase([i1,i2]), Phase([i1,i2]))
        self.assertRealEqual(Phase(None, [s1,s2]), Phase(None, [s1,s2]))
        self.assertRealEqual(Phase([i1,i2],[s1,s2]), Phase([i1,i2],[s1,s2]))

        self.assertRealNotEqual(Phase([i1]), Phase())
        self.assertRealNotEqual(Phase(None, [s1]), Phase())
        self.assertRealNotEqual(Phase([i1]), Phase([i2]))
        self.assertRealNotEqual(Phase(None, [s1]), Phase(None, [s2]))
        
class RecipeTest(unittest.TestCase, XmlTestMixin, RealEqualMixin):
    def test_init(self):
        r = Recipe('title', 'size', 'de', 'source', 'author', 'description')
        self.assertEqual(r.title, 'title')
        self.assertEqual(r.size, 'size')
        self.assertEqual(r.lang, 'de')
        self.assertEqual(r.source, 'source')
        self.assertEqual(r.author, 'author')
        self.assertEqual(r.description, ['description'])
        self.assertEqual(r.phases, [])

        p = Phase()
        r = Recipe(None, None, None, None, None, None, [p])
        self.assertEqual(r.title, None)
        self.assertEqual(r.size, None)
        self.assertEqual(r.lang, None)
        self.assertEqual(r.source, None)
        self.assertEqual(r.author, None)
        self.assertEqual(r.description, None)
        self.assertEqual(r.phases, [p])

    def test_repr(self):
        r = Recipe('title', 'size', 'de', 'source', 'author', 'description')
        self.assertEqual(repr(r), "Recipe('title', 'size', 'de', 'source', 'author', ['description'], [], [])")

    def test_compare(self):
        i = Ingredient('foo', None, None)
        self.assertRealEqual(Recipe(), Recipe())
        self.assertRealEqual(Recipe('a', 'b', 'c', 'd', 'e', 'f', [Phase()], ['k']), Recipe('a', 'b', 'c', 'd', 'e', 'f', [Phase()], ['k']))
        self.assertRealEqual(Recipe(None, None, None, None, None, None, None, ['a', 'b']), Recipe(None, None, None, None, None, None, None, ['b', 'a']))
        
        self.assertRealNotEqual(Recipe('a'), Recipe('b'))
        self.assertRealNotEqual(Recipe(None, 'a'), Recipe())
        self.assertRealNotEqual(Recipe(None, 'a'), Recipe(None, 'b'))
        self.assertRealNotEqual(Recipe(None, None, 'a'), Recipe())
        self.assertRealNotEqual(Recipe(None, None, 'a'), Recipe(None, None, 'b'))
        self.assertRealNotEqual(Recipe(None, None, None, 'a'), Recipe())
        self.assertRealNotEqual(Recipe(None, None, None, 'a'), Recipe(None, None, None, 'b'))
        self.assertRealNotEqual(Recipe(None, None, None, None, 'a'), Recipe())
        self.assertRealNotEqual(Recipe(None, None, None, None, 'a'), Recipe(None, None, None, None, 'b'))
        self.assertRealNotEqual(Recipe(None, None, None, None, None, [Phase()]), Recipe())
        self.assertRealNotEqual(Recipe(None, None, None, None, None, [Phase()]), Recipe(None, None, None, None, None, [Phase([i])]))
        self.assertRealNotEqual(Recipe(None, None, None, None, None, None, ['a']), Recipe())
        self.assertRealNotEqual(Recipe(None, None, None, None, None, None, ['a']), Recipe(None, None, None, None, None, None, ['b']))
        self.assertRealNotEqual(Recipe(None, None, None, None, None, None, None, ['a']), Recipe(None, None, None, None, None, None, None, ['b']))

if __name__ == '__main__':
    unittest.main()

