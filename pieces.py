from errors import *
from lxml import etree

class Ingredient(object):
    def __init__( self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

        if amount is None and unit is not None or amount is not None and unit is None:
            raise RecipeParseError('ingredient with amount must have amount and unit')

    def serialize(self,element):
        i = etree.SubElement( element, 'ingredient')
        etree.SubElement( i, 'name').text = self.name
        if self.amount is not None:
            etree.SubElement( i, 'amount').text = self.amount
            etree.SubElement( i, 'unit').text = self.unit

    def __repr__(self):
        return 'Ingredient( {}, {}, {})'.format(self.name, self.amount, self.unit)

class Step(object):
    def __init__( self, text):
        self.text = text

    def serialize(self, element):
        e = etree.SubElement( element, 'step').text = self.text

    def __repr__(self):
        return 'Step({})'.format(self.text)

class Hint(object):
    def __init__( self, text):
        self.text = text

    def serialize(self, element):
        etree.SubElement( element, 'hint').text = self.text

    def __repr__(self):
        return 'Step({})'.format(self.text)

class Phase(object):
    def __init__( self, ingredients = None, steps = None):
        if ingredients is None:
            ingredients = []
        if steps is None:
            steps = []

        self.ingredients = ingredients
        self.steps = steps

    def serialize(self, element):
        p = etree.SubElement( element, 'phase')
        for x in self.ingredients:
            x.serialize(p)
        for x in self.steps:
            x.serialize(p)

    def __repr__(self):
        return 'Phase({},{})'.format(
            str(self.ingredients),
            str(self.steps),
            )

class Recipe(object):
    def __init__(self, title = None, size = None, source = None, author = None, phases = None):
        if phases == None:
            phases = []

        self.title = title
        self.size = size
        self.source = source
        self.author = author
        self.phases = phases

    def serialize(self, element):
        r = etree.SubElement( element, 'recipe')
        m = etree.SubElement( r, 'meta')
        i = etree.SubElement( r, 'instructions')

        if self.title is not None:
            etree.SubElement( m, 'title').text = self.title
        if self.size is not None:
            etree.SubElement( m, 'size').text = self.size
        if self.source is not None:
            etree.SubElement( m, 'source').text = self.source
        if self.author is not None:
            etree.SubElement( m, 'author').text = self.author

        for p in self.phases:
            p.serialize(i)

    def __repr__(self):
        return 'Recipe({},{},{},{},{})'.format(
            self.title, self.size, self.source, self.author, str(self.phases))
