import unittest
from io import StringIO
from parser import *

class parseIngredientTest(unittest.TestCase):
    def test_normal(self):
        i = parseIngredient('\t # 25g butter   \n')
        self.assertEqual(i, Ingredient('butter', '25', 'g'))

    def test_nospaces(self):
        i = parseIngredient('#25g butter')
        self.assertEqual(i, Ingredient('butter', '25', 'g'))

    def test_fraction(self):
        i = parseIngredient('#1/2g butter')
        self.assertEqual(i, Ingredient('butter', '1/2', 'g'))

    def test_mixed(self):
        i = parseIngredient('# 1 1/2g butter')
        self.assertEqual(i, Ingredient('butter', '1 1/2', 'g'))

    def test_real(self):
        i = parseIngredient('# 0.5g butter')
        self.assertEqual(i, Ingredient('butter', '0.5', 'g'))

    def test_nounit(self):
        i = parseIngredient('# 4 eggs')
        self.assertEqual(i, Ingredient('eggs', '4', None))

    def test_noamount(self):
        i = parseIngredient('\t #diced onion   \n')
        self.assertEqual(i, Ingredient('diced onion', None, None))

class parseMetaTest(unittest.TestCase):
    def test_title(self):
        r = Recipe()
        m = parseMeta('\t ! title: my title   \n', r)
        self.assertEqual(r, Recipe('my title'))

    def test_nospace_title(self):
        r = Recipe()
        m = parseMeta('!title:my title', r)
        self.assertEqual(r, Recipe('my title'))
    
    def test_size(self):
        r = Recipe()
        m = parseMeta('! size: for 4 people', r)
        self.assertEqual(r, Recipe(None, 'for 4 people'))

    def test_source(self):
        r = Recipe()
        m = parseMeta('! source: internet', r)
        self.assertEqual(r, Recipe(None, None, 'internet'))

    def test_author(self):
        r = Recipe()
        m = parseMeta('! author: myself', r)
        self.assertEqual(r, Recipe(None, None, None, 'myself'))

    def test_unkown(self):
        with self.assertRaises(Exception) as context:
            parseMeta('! unknown: foo', None)
        self.assertEqual(context.exception.args[0], 'invalid metadata key')

    def test_invalid(self):
        with self.assertRaises(Exception) as context:
            parseMeta('! not the excepted', None)
        self.assertEqual(context.exception.args[0], 'invalid metadata line')

class parseFileTest(unittest.TestCase):
    def test_simple(self):
        r = parseFile(StringIO(test_input['simple']))
        self.assertEqual(r, test_result['simple'])

    def test_multiphase(self):
        r = parseFile(StringIO(test_input['multiphase']))
        self.assertEqual(r, test_result['multiphase'])

    def test_multi_recipe(self):
        r = parseFile(StringIO(test_input['multi_recipe']))
        self.assertEqual(r, test_result['multi_recipe'])

    def test_meta_error(self):
        with self.assertRaises(RecipeParseError) as context:
            parseFile(StringIO(test_input['meta_error']))

        self.assertEqual(context.exception.line, '! unknown: foo')
        self.assertEqual(context.exception.line_nr, 2)
        self.assertIsNotNone(context.exception.__cause__)
        self.assertEqual(context.exception.__cause__.args[0], 'invalid metadata key')

test_input = {
    'simple' : """
        ! title: the title
        # 25g butter
        * eat butter   """,
    'multiphase' : """
        # 25g butter
        * eat butter
        + lie down a bit
        # 100g meat
        * eat meat""",
    'multi_recipe' : """
        ! title: rec 1
        # something
        ! title: rec 2
        """,
    'meta_error' : """
        ! unknown: foo""",
    }

test_result = {
    'simple' : [
        Recipe(
            'the title',
            None,
            None,
            None,
            [
                Phase(
                    [
                        Ingredient('butter', '25', 'g'),
                        ],
                    [
                        Step('eat butter'),
                        ]
                    )
                ]
            )
        ],
    'multiphase' : [
        Recipe(
            None,
            None,
            None,
            None,
            [
                Phase(
                    [
                        Ingredient('butter', '25', 'g'),
                        ],
                    [
                        Step('eat butter')
                        ]
                    ),
                WaitPhase('lie down a bit'),
                Phase(
                    [
                        Ingredient('meat', '100', 'g')
                        ],
                    [
                        Step('eat meat')
                        ]
                    )
                ]
            )
        ],
    'multi_recipe' : [
        Recipe(
            'rec 1',
            None,
            None,
            None,
            [
                Phase(
                    [
                        Ingredient('something', None, None)
                        ],
                    )
                ]
            ),
        Recipe(
            'rec 2'
            )
        ],
    }
