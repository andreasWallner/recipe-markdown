import unittest
from errors import *

class RecipeParseErrorTest(unittest.TestCase):
    def test_init(self):
        r = RecipeParseError('the line', 45)
        self.assertEqual(r.line, 'the line')
        self.assertEqual(r.line_nr, 45)
        self.assertEqual(str(r), "Error: on line #45 ('the line'): invalid")

    def test_chaining(self):
        with self.assertRaises(RecipeParseError) as context:
            try:
                raise Exception('foo')
            except Exception as e:
                raise RecipeParseError('the line', 45) from e
        self.assertEqual(context.exception.line, 'the line')
        self.assertEqual(context.exception.line_nr, 45)
        self.assertIsInstance(context.exception.__cause__, Exception)
        self.assertEqual(context.exception.__cause__.args[0], 'foo')
        self.assertEqual(
            str(context.exception),
            "Error: on line #45 ('the line'):\nfoo"
            )
