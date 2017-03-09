import json
import unittest
from io import BytesIO
from recipemd import pieces
import recipemd.serializer.json as js


class tests(unittest.TestCase):
    def test_dump(self):
        b = BytesIO()
        p = pieces.Phase()
        r = pieces.Recipe(
            'my title',
            'some size',
            'de',
            'some source',
            'some author',
            'long description',
            [p],
            ['kw1', 'kw2'],
            ['image.jpg'],
            )
        js.dump(b, [r])

        read = json.loads(b.getvalue().decode())
        
        self.assertEqual(
            [{
                'title' : 'my title',
                'size' : 'some size',
                'lang' : 'de',
                'source' : 'some source',
                'author' : 'some author',
                'description' : ['long description'],
                'phases' : [{
                    '_type' : 'phase',
                    'ingredients' : [],
                    'instructions' : [],
                    }],
                'keywords' : ['kw1', 'kw2'],
                'images' : ['image.jpg'],
                }],
            read)

class RecipeEncoderTests(unittest.TestCase):
    def test_serializeRecipe(self):
        p = pieces.Phase()
        wp = pieces.WaitPhase()
        pa = pieces.Part()

        r = pieces.Recipe(
            'my title',
            'some size',
            'de',
            'some source',
            'some author',
            'long description',
            [p, wp, pa],
            ['kw1', 'kw2'],
            ['image.jpg'],
            )
        result = js.RecipeEncoder().default(r)
        self.assertEqual(
            {
                'title' : 'my title',
                'size' : 'some size',
                'lang' : 'de',
                'source' : 'some source',
                'author' : 'some author',
                'description' : ['long description'],
                'phases' : [p, wp, pa],
                'keywords' : ['kw1', 'kw2'],
                'images' : ['image.jpg'],
                },
            result,
            )

    def test_serializePhase(self):
        i = [
            pieces.Ingredient('foo', None, None),
            pieces.Ingredient('bar', 1, 'unit'),
            ]
        s = [
            pieces.Step('step 1'),
            pieces.Step('step 2'),
            ]
        p = pieces.Phase(i, s)
        result = js.RecipeEncoder().default(p)
        self.assertEqual(
            {
                '_type' : 'phase',
                'ingredients' : i,
                'instructions' : s,
                },
            result,
            )
        
    def test_serializeWaitPhase(self):
        wp = pieces.WaitPhase('waitphase text')
        result = js.RecipeEncoder().default(wp)
        self.assertEqual(
            {
                '_type' : 'waitphase',
                'text' : 'waitphase text',
                },
            result,
            )

    def test_serializeStep(self):
        s = pieces.Step('my text')
        result = js.RecipeEncoder().default(s)
        self.assertEqual(
            {
                '_type' : 'step',
                'text' : 'my text'
                },
            result
            )

    def test_serializeNote(self):
        s = pieces.Note('some note')
        result = js.RecipeEncoder().default(s)
        self.assertEqual(
            {
                '_type' : 'note',
                'text' : 'some note',
                },
            result
            )

    def test_serializePart(self):
        s = pieces.Part('headline')
        result = js.RecipeEncoder().default(s)
        self.assertEqual(
            {
                '_type' : 'part',
                'text' : 'headline',
                },
            result
            )

    def test_serializeIngredient(self):
        i = pieces.Ingredient('na', 'am', 'un')
        result = js.RecipeEncoder().default(i)
        self.assertEqual(
            {
                'name' : 'na',
                'unit' : 'un',
                'amount' : 'am',
                },
            result,
            )
