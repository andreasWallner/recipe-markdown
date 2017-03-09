from lxml import etree
from recipemd import pieces


def dump(f, content, xslt = None):
    root = etree.Element('root')
    for r in content:
        serialize(r, root)
    if xslt is not None:
        root.addprevious(
            etree.ProcessingInstruction(
                'xml-stylesheet',
                'type="text/xsl" href="' + xslt + '"',
                ))
    et = etree.ElementTree(root)
    et.write(f, xml_declaration=True, pretty_print=True, encoding='UTF-8')

def serializeRecipes(recipes):
    e = etree.Element('root')
    for r in recipes:
        serialize(r, e)
    return e

def serialize(piece, element):
    calls = {
        pieces.Recipe : serializeRecipe,
        pieces.Phase : serializePhase,
        pieces.WaitPhase : serializeWaitPhase,
        pieces.Part : serializePart,
        pieces.Step : serializeStep,
        pieces.Note : serializeNote,
        pieces.Ingredient : serializeIngredient,
    }
    if type(piece) in calls:
        calls[type(piece)](piece, element)
    else:
       raise TypeError('could not serialize unknown type "' + type(piece) + '"')

def serializeIngredient(ingredient, element):
    i = etree.SubElement( element, 'ingredient')
    etree.SubElement( i, 'name').text = ingredient.name
    if ingredient.amount is not None:
        etree.SubElement( i, 'amount').text = ingredient.amount
    if ingredient.unit is not None:
        etree.SubElement( i, 'unit').text = ingredient.unit

def serializeStep(step, element):
    e = etree.SubElement(element, 'step').text = step.text

def serializeNote(note, element):
    e = etree.SubElement(element, 'note').text = note.text

def serializeWaitPhase(wp, element):
    etree.SubElement(element, 'waitphase').text = wp.text

def serializePart(part, element):
    etree.SubElement(element, 'part').text = part.text

def serializePhase(phase, element):
    p = etree.SubElement(element, 'phase')
    for x in phase.ingredients:
        serialize(x, p)
    for x in phase.steps:
        serialize(x, p)

def serializeRecipe(recipe, element):
    r = etree.SubElement(element, 'recipe')
    m = etree.SubElement(r, 'meta')
    i = etree.SubElement(r, 'instructions')

    if recipe.title is not None:
        etree.SubElement(m, 'title').text = recipe.title
    if recipe.size is not None:
        etree.SubElement(m, 'size').text = recipe.size
    if recipe.lang is not None:
        etree.SubElement(m, 'lang').text = recipe.lang
    if recipe.source is not None:
        etree.SubElement(m, 'source').text = recipe.source
    if recipe.author is not None:
        etree.SubElement(m, 'author').text = recipe.author
    if recipe.description is not None:
        desc = etree.SubElement(m, 'description')
        for p in recipe.description:
            etree.SubElement(desc, 'p').text = p
    if recipe.keywords:
        kwe = etree.SubElement(m, 'keywords')
        for kw in recipe.keywords:
            etree.SubElement(kwe, 'keyword').text = kw
    if recipe.images:
        imge = etree.SubElement(m, 'images')
        for img in recipe.images:
            etree.SubElement(imge, 'img').text = img

    for p in recipe.phases:
        serialize(p, i)
