from lxml import etree

def serializeRecipes(recipes):
    e = etree.Element('root')
    for r in recipes:
        r.serialize(e)
    return e
