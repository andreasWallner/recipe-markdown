import re
from pieces import *
from errors import *
from utils import *
from lxml import etree

class State:
    class Meta: pass
    class Ingredients: pass
    class Steps: pass
    class FinishPhase: pass
    class FinishRecipe: pass

def parseIngredient(line):
    r = r'#\s*([0-9/]+(?:\s[0-9/]+)*)\s*([a-zA-Z]+)\s+(.*)'
    result = re.match( r, line)

    if result is not None:
        return Ingredient( result.groups()[2], result.groups()[1], result.groups()[0])

    return Ingredient( line.lstrip('# \t'), None, None)

def parseMeta(line,recipe):
    r = r'!\s*([a-zA-Z]+)\s*:\s*(.*)'
    result = re.match( r, line)

    if result is None:
        raise RecipeParseError('invalid meta data line', line)

    mn = result.groups()[0]
    if mn == 'title':
        recipe.title = result.groups()[1]
    elif mn == 'size':
        recipe.size = result.groups()[1]
    elif mn == 'source':
        recipe.size = result.groups()[1]
    elif mn == 'author':
        recipe.size = result.groups()[1]
    else:
        raise Exception('invalid meta data key', line)

def parseFile(stream):
    recipes = []

    phase = Phase()
    recipe = Recipe()

    state = State.Meta

    line = ''

    while True:
        if len(line) > 0:
            start = line[0]
        else:
            start = ''

        if state == State.Meta:
            if start == '!':
                parseMeta( line, recipe)
            if start == '#' or start == '*':
                state = State.Ingredients
                continue

        elif state == State.Ingredients:
            if start == '!':
                state = State.FinishRecipe
                continue
            if start == '*':
                state = State.Steps
                continue
            if start == '#':
                phase.ingredients.append(parseIngredient(line))

        elif state == State.Steps:
            if start == '!':
                state = State.FinishRecipe
                continue
            if start == '#':
                state = State.FinishPhase
                continue
            if start == '*':
                phase.steps.append(Step(line.lstrip('* \t')))
        
        elif state == State.FinishPhase:
            recipe.phases.append(phase)
            phase = Phase()
            state = State.Ingredients

        elif state == State.FinishRecipe:
            recipes.append(recipe)
            recipe = Recipe()
            state = State.Meta

        line = stream.readline()
        if line == '':
            if state != State.Meta:
                recipes.append(recipe)
            break
        line = line.strip(' \t\n')

    return recipes
