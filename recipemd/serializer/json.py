import json
from recipemd import pieces


def dump(f, content):
    f.write(json.dumps(content, indent=2, cls=RecipeEncoder).encode())

class RecipeEncoder(json.JSONEncoder):
    def default(self, o):
        calls = {
            pieces.Recipe : self.serializeRecipe,
            pieces.Phase : self.serializePhase,
            pieces.WaitPhase : self.serializeWaitPhase,
            pieces.Part : self.serializePart,
            pieces.Step : self.serializeStep,
            pieces.Note : self.serializeNote,
            pieces.Ingredient : self.serializeIngredient,
        }

        if type(o) in calls:
            return calls[type(o)](o)

        return json.JSONEncoder.default(self, o)

    def serializeRecipe(self, o):
        serial = {}

        keys = [
            'title',
            'size',
            'lang',
            'source',
            'author',
            'description',
            'keywords',
            'images',
            'phases',
            ]
        for k in keys:
            serial[k] = getattr(o, k)
        return serial

    def serializePhase(self, o):
        return {
            '_type' : 'phase',
            'ingredients' : o.ingredients,
            'instructions' : o.steps,
            }

    def serializeWaitPhase(self, o):
        return {
            '_type' : 'waitphase',
            'text' : o.text,
            }

    def serializePart(self, o):
        return {
            '_type' : 'part',
            'text' : o.text,
            }

    def serializeStep(self, o):
        return {
            '_type' : 'step',
            'text' : o.text,
            }

    def serializeNote(self, o):
        return {
            '_type' : 'note',
            'text' : o.text,
            }

    def serializeIngredient(self, o):
        return {
            'name' : o.name,
            'amount' : o.amount,
            'unit' : o.unit
            }
