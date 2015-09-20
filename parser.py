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
    class WaitPhase: pass
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


def parseMeta(line, recipe):
    r = r'^\s*!?\s*([a-zA-Z]+)\s*:\s*(.*)'
    result = re.match( r, line)

    if result is None:
        key = 'desc'
        val = line.lstrip('! \t').rstrip(' \t\n')
    else:
        key = result.groups()[0]
        val = result.groups()[1].rstrip(' \t')

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
        if recipe.description == None:
            recipe.description = val
        else:
            recipe.description = recipe.description.strip() + ' ' + val
    elif key == 'keywords':
        kws = val.split(',')
        kws = [x.strip() for x in kws]
        recipe.keywords += kws
    else:
        raise Exception('invalid metadata key')

def parseWaitPhase(line, waitphase):
    line = line.lstrip(' \t+')
    line = line.rstrip(' \t\n')
    if waitphase.text is None:
        waitphase.text = line
    else:
        waitphase.text = waitphase.text + ' ' + line

def parseFile(stream):
    recipes = []

    phase = Phase()
    recipe = Recipe()
    waitphase = WaitPhase()

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

                if start == '+':
                    state = State.WaitPhase
                    continue

            if state == State.Meta:
                if not line:
                    state = State.FinishRecipe
                    continue

                if start == '#' or start == '*':
                    state = State.Ingredients
                    continue

                if start == '+':
                    state = State.WaitPhase
                    continue

                # also interpret as metadata if there is no '!'
                parseMeta( line, recipe)


            elif state == State.Ingredients:
                if start == '!' or start == '+' or not line:
                    state = State.FinishPhase
                    continue

                if start == '*':
                    state = State.Steps
                    continue
                
                if start == '#':
                    phase.ingredients.append(parseIngredient(line))

            elif state == State.Steps:
                if start == '!' or start == '#' or start == '+' or not line:
                    state = State.FinishPhase
                    continue

                if start == '*':
                    line = line.lstrip('* \t')
                    line = line.rstrip(' \t\n')
                    phase.steps.append(Step(line))

            elif state == State.WaitPhase:
                if start == '!' or start == '#' or start == '*' or not line:
                    recipe.phases.append(waitphase)
                    waitphase = WaitPhase()
                    if start == '!' or not line:
                        state = State.FinishRecipe
                    elif start == '#':
                        state = State.Ingredients
                    elif start == '*':
                        state = State.Steps
                    continue
                elif start == '+':
                    parseWaitPhase(line, waitphase)
           
            elif state == State.FinishPhase:
                recipe.phases.append(phase)
                phase = Phase()
                if start == '!' or not line:
                    state = State.FinishRecipe
                elif start == '#':
                    state = State.Ingredients
                elif start == '+':
                    state = State.WaitPhase
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
