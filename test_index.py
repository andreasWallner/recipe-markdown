import index
import unittest

class JinjaIndexTests(unittest.TestCase):
    def test_default(self):
        index.update_index_jinja('/home/alarm/coding/test/recipes/')
