import re
from pieces import *
from errors import *
from utils import *
from lxml import etree


class Line:
    """Holds the type and contents of a line, e.g. an ingredient or an instruction.

    In case that word wrapping was used in the original markup, one Line class can
    actually hold the contents of multiple lines in the source code belonging to the
    same ingredient, instruction etc.
    """
    class Empty: pass
    class Plain: pass
    class Comment: pass
    class Command: pass
    class Part: pass
    class Ingredient: pass
    class Step: pass
    class Note: pass
    class WaitPhase: pass

    startCharacters = (
        ("'", Comment),
        ('!', Command),
        ('#', Part),
        ('*', Ingredient),
        ('--', Note), # notes have to be parsed before steps!
        ('-', Step),
        ('+', WaitPhase),
    )

    def __init__(self, lineType = None, lineNo = None, contents = None):
        self.lineType = lineType
        self.lineNo = lineNo
        self.contents = contents

    def __repr__(self):
        return 'Line({!r}, {!r}, {!r})'.format(self.lineType, self.lineNo, self.contents)

    @property
    def contents(self):
        if isinstance(self._contents, str):
            return self._contents
        else:
            return ' '.join(self._contents)

    @contents.setter
    def contents(self, contents):
        self._contents = contents

    def append(self, contents):
        if isinstance(self._contents, str):
            self._contents = [self._contents, contents]
        else:
            self._contents.append(contents)

def preprocessLines(stream):
    """Generator that joins word wrapped lines back together and parses the type of the line,
    e.g. ingredient or step. Yields instances of the Line class.
    """
    currentLine = None
    for lineNo, rawLine in enumerate(stream, 1):
        lineType = None
        contents = rawLine.strip()
        for c, t in Line.startCharacters:
            if contents.startswith(c):
                lineType = t
                contents = contents[len(c):].lstrip()
                break

        if lineType == None:
            if len(contents) == 0:
                if currentLine:
                    yield currentLine
                    currentLine = None
                yield Line(Line.Empty, lineNo, '')
            elif currentLine:
                currentLine.append(contents)
            else:
                lineType = Line.Plain

        if lineType != None:
            if currentLine:
                yield currentLine
            currentLine = Line(lineType, lineNo, contents)
    if currentLine:
        yield currentLine

def parseIngredient(line):
    r = r'^(.+)\[(.*)\](.+)'
    result = re.match(r, line)

    if result is None:
        r = r'^\s*([0-9/\.]+(?:\s+[0-9/]+)?)([a-zA-Z]+)?\s+(.*)'
        result = re.match( r, line)

    if result is None:
        return Ingredient(line, None, None)

    name = result.group(3).strip()
    amount = result.group(1).strip()
    unit = result.group(2)
    if isinstance(unit, str):
        unit = unit.strip()
    if not unit:
        unit = None
    return Ingredient(name, amount, unit)

def splitCommand(line):
    r = r'^\s*([a-zA-Z]+)\s*:\s*(.*)'
    result = re.match(r, line)
    if result:
        key = result.groups()[0]
        val = result.groups()[1]
        return key, val
    return None, None

def parseMeta(key, val, recipe):
    if key == 'title':
        recipe.title = val
    elif key == 'size':
        recipe.size = val
    elif key == 'lang':
        recipe.lang = val
    elif key == 'source':
        recipe.source = val
    elif key == 'author':
        recipe.author = val
    elif key == 'desc':
        if recipe.description is None:
            recipe.description = [val]
        else:
            recipe.description.append(val)
    elif key == 'keywords':
        kws = val.split(',')
        kws = [x.strip() for x in kws]
        recipe.keywords += kws
    elif key == 'img':
        recipe.images.append(val)
    else:
        raise Exception('invalid metadata key')

def parseFile(stream):
    recipes = []
    line = Line()
    try:
        recipe = None
        phase = None
        meta = False
        for line in preprocessLines(stream):
            if line.lineType == Line.Command:
                key, value = splitCommand(line.contents)
                if recipe and key == 'title':
                    recipe = None
                if not recipe:
                    if key != 'title':
                        raise Exception('recipes must start with a title')
                    recipe = Recipe()
                    recipes.append(recipe)
                    meta = True
                if meta:
                    parseMeta(key, value, recipe)
                else:
                    raise Exception('commands are not yet used (metadata must appear at the beginning of the recipe)')

            elif line.lineType == Line.Plain:
                if len(recipe.phases):
                    raise Exception('plain lines are only allowed for description at the beginning of the recipe')
                parseMeta('desc', line.contents, recipe)

            elif line.lineType == Line.Part:
                if not recipe:
                    raise Exception('part occurred outside of recipe')
                meta = False
                phase = None
                part = Part(line.contents)
                recipe.phases.append(part)

            elif line.lineType == Line.Ingredient:
                if not recipe:
                    raise Exception('ingredient outside of recipe')
                meta = False
                if not phase or len(phase.steps):
                    phase = Phase()
                    recipe.phases.append(phase)
                phase.ingredients.append(parseIngredient(line.contents))

            elif line.lineType == Line.Step:
                if not recipe:
                    raise Exception('step outside of recipe')
                meta = False
                if not phase:
                    phase = Phase()
                    recipe.phases.append(phase)
                phase.steps.append(Step(line.contents))

            elif line.lineType == Line.Note:
                if not recipe:
                    raise Exception('note occurred outside of recipe')
                meta = False
                if not phase:
                    phase = Phase()
                    recipe.phases.append(phase)
                phase.steps.append(Note(line.contents))

            elif line.lineType == Line.WaitPhase:
                if not recipe:
                    raise Exception('Wait phase occurred outside of recipe')
                meta = False
                phase = None
                waitphase = WaitPhase(line.contents)
                recipe.phases.append(waitphase)

            elif line.lineType == Line.Empty:
                meta = False # to allow progress images at the beginning of the recipe
                if phase:
                    phase = None
            elif line.lineType != Line.Comment:
                raise Exception('invalid line type')

    except Exception as e:
        raise RecipeParseError(line.contents, line.lineNo) from e

    return recipes
