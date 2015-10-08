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

class Note(object):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Note({!r})'.format(self.text)

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.text == other.text

    def __ne__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.text != other.text

class WaitPhase(object):
    def __init__(self, text = None):
        self.text = text

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

class Part(object):
    def __init__(self, text = None):
        self.text = text

    def __repr__(self):
        return 'Part({!r})'.format(self.text)

    def __eq__(self, other):
        if not isinstance(other, Part):
            return NotImplemented
        return self.text == other.text

    def __ne__(self, other):
        if not isinstance(other, Part):
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
    def __init__(self, title = None, size = None, lang = None, source = None, author = None, description = None, phases = None, keywords = None, images = None):
        if phases == None:
            phases = []
        if keywords == None:
            keywords = []
        if images == None:
            images = []

        self.title = title
        self.size = size
        self.lang = lang
        self.source = source
        self.author = author
        self.phases = phases
        if isinstance(description, str):
            self.description = [description]
        else:
            self.description = description
        self.keywords = keywords
        self.images = images

    def __repr__(self):
        return 'Recipe({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.title, self.size, self.lang, self.source, self.author, self.description, self.phases, self.keywords)

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented

        return (self.title == other.title
            and self.size == other.size
            and self.lang == other.lang
            and self.source == other.source
            and self.author == other.author
            and self.phases == other.phases
            and self.description == other.description
            and set(self.keywords) == set(other.keywords)
            and self.images == other.images)

    def __ne__(self, other):
        return not self == other
