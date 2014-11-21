from errors import *
from lxml import etree

class Ingredient(object):
    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit
        
        if name is None:
            raise RecipeParseError('ingredient must not have None as a name')
        if amount is None and unit is not None:
            raise RecipeParseError('ingredient with unit must have amount')

    def serialize(self, element):
        i = etree.SubElement( element, 'ingredient')
        etree.SubElement( i, 'name').text = self.name
        if self.amount is not None:
            etree.SubElement( i, 'amount').text = self.amount
        if self.unit is not None:
            etree.SubElement( i, 'unit').text = self.unit

    def __repr__(self):
        return 'Ingredient({!r}, {!r}, {!r})'.format(self.name, self.amount, self.unit)

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented

        return (self.name == other.name
            and self.amount == other.amount
            and self.unit == other.unit)

    def __ne__(self, other):
        return not self == other

class Step(object):
    def __init__(self, text):
        self.text = text

    def serialize(self, element):
        e = etree.SubElement(element, 'step').text = self.text

    def __repr__(self):
        return 'Step({!r})'.format(self.text)

    def __eq__(self, other):
        if not isinstance(other, Step):
            return NotImplemented
        return self.text == other.text

    def __ne__(self, other):
        if not isinstance(other, Step):
            return NotImplemented
        return self.text != other.text

class WaitPhase(object):
    def __init__(self, text = None):
        self.text = text

    def serialize(self, element):
        etree.SubElement(element, 'waitphase').text = self.text

    def __repr__(self):
        return 'WaitPhase({!r})'.format(self.text)

    def __eq__(self, other):
        if not isinstance(other, WaitPhase):
            return NotImplemented
        return self.text == other.text

    def __ne__(self, other):
        if not isinstance(other, WaitPhase):
            return NotImplemented
        return self.text != other.text

class Phase(object):
    def __init__(self, ingredients = None, steps = None):
        if ingredients is None:
            ingredients = []
        if steps is None:
            steps = []

        self.ingredients = ingredients
        self.steps = steps

    def serialize(self, element):
        p = etree.SubElement(element, 'phase')
        for x in self.ingredients:
            x.serialize(p)
        for x in self.steps:
            x.serialize(p)

    def __repr__(self):
        return 'Phase({!r},{!r})'.format(self.ingredients, self.steps)

    def __eq__(self, other):
        if not isinstance(other, Phase):
            return NotImplemented

        return (self.ingredients == other.ingredients
            and self.steps == other.steps)

    def __ne__(self, other):
        return not self == other

class Recipe(object):
    def __init__(self, title = None, size = None, lang = None, source = None, author = None, description = None, phases = None, keywords = None):
        if phases == None:
            phases = []
        if keywords == None:
            keywords = []

        self.title = title
        self.size = size
        self.lang = lang
        self.source = source
        self.author = author
        self.phases = phases
        self.description = description
        self.keywords = keywords

    def serialize(self, element):
        r = etree.SubElement(element, 'recipe')
        m = etree.SubElement(r, 'meta')
        i = etree.SubElement(r, 'instructions')

        if self.title is not None:
            etree.SubElement(m, 'title').text = self.title
        if self.size is not None:
            etree.SubElement(m, 'size').text = self.size
        if self.lang is not None:
            etree.SubElement(m, 'lang').text = self.lang
        if self.source is not None:
            etree.SubElement(m, 'source').text = self.source
        if self.author is not None:
            etree.SubElement(m, 'author').text = self.author
        if self.description is not None:
            etree.SubElement(m, 'description').text = self.description
        if self.keywords:
            kwe = etree.SubElement(m, 'keywords')
            for kw in self.keywords:
                etree.SubElement(kwe, 'keyword').text = kw

        for p in self.phases:
            p.serialize(i)

    def __repr__(self):
        return 'Recipe({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.title, self.size, self.lang, self.source, self.author, self.description, self.phases)

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented

        return (self.title == other.title
            and self.size == other.size
            and self.lang == other.lang
            and self.source == other.source
            and self.author == other.author
            and self.phases == other.phases
            and self.description == other.description)

    def __ne__(self, other):
        return not self == other
