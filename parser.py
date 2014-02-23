import re
from pieces import *
from errors import *
from utils import *
from lxml import etree

class State:
    class Waiting: pass
    class Meta: pass
    class Ingredients: pass
    class Steps: pass
    class FinishPhase: pass
    class FinishRecipe: pass

def parseIngredient(line):
    r = r'^\s*#\s*([0-9/\.]+(?:\s+[0-9/]+)?)([a-zA-Z]+)?\s+(.*)'
    result = re.match( r, line)

    if result is None:
        line = line.lstrip('# \t')
        line = line.rstrip(' \t\n')
        return Ingredient( line, None, None)

    return Ingredient(
        result.groups()[2].rstrip(),
        result.groups()[0],
        result.groups()[1],
        )


def parseMeta(line,recipe):
    r = r'^\s*!\s*([a-zA-Z]+)\s*:\s*(.*)'
    result = re.match( r, line)

    if result is None:
        raise Exception('invalid metadata line')

    key = result.groups()[0]
    val = result.groups()[1].rstrip(' \t')

    if key == 'title':
        recipe.title = val
    elif key == 'size':
        recipe.size = val
    elif key == 'source':
        recipe.source = val
    elif key == 'author':
        recipe.author = val
    else:
        raise Exception('invalid metadata key')

def parseFile(stream):
    recipes = []

    phase = Phase()
    recipe = Recipe()

    state = State.Waiting

    line = ''
    line_nr = 0

    try:
        while True:
            line = line.lstrip(' \t')
            if len(line) > 0:
                start = line[0]
            else:
                start = ''

            if state == State.Waiting:
                if start == '!':
                    state = State.Meta
                    continue
                
                if start == '#':
                    state = State.Ingredients
                    continue

                if start == '*':
                    state = State.Steps
                    continue

            if state == State.Meta:
                if not line:
                    state = State.FinishRecipe
                    continue

                if start == '#' or start == '*':
                    state = State.Ingredients
                    continue

                if start == '!':
                    parseMeta( line, recipe)


            elif state == State.Ingredients:
                if start == '!' or not line:
                    state = State.FinishPhase
                    continue

                if start == '*':
                    state = State.Steps
                    continue

                if start == '#':
                    phase.ingredients.append(parseIngredient(line))

            elif state == State.Steps:
                if start == '!' or start == '#' or not line:
                    state = State.FinishPhase
                    continue

                if start == '*':
                    line = line.lstrip('* \t')
                    line = line.rstrip(' \t\n')
                    phase.steps.append(Step(line))
           
            elif state == State.FinishPhase:
                recipe.phases.append(phase)
                phase = Phase()
                if start == '!' or not line:
                    state = State.FinishRecipe
                elif start == '#':
                    state = State.Ingredients
                continue

            elif state == State.FinishRecipe:
                recipes.append(recipe)
                recipe = Recipe()
                state = State.Waiting
                continue

            line = stream.readline()
            if not line and state == State.Waiting:
                break
            else:
                line_nr += 1

    except Exception as e:
        line = line.rstrip('\n')
        raise RecipeParseError(line, line_nr) from e

    return recipes
