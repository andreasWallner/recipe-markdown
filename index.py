import os
from lxml import etree

def extension(filename):
    s = filename.split('.')
    if len(s) > 1:
        return s[-1]
    else:
        return ''

def append_recipes(body,path,f):
    xml = etree.parse(path + f)
    recipes = xml.xpath('//recipe')

    for r in recipes:
        title = r.xpath('//title')[0].text
        print(title)

        a = etree.SubElement(body,'a')
        a.attrib['href'] = f
        a.text = title

def update_index(path):
    root = etree.Element('html')
    body = etree.SubElement(root, 'body')
    
    for f in os.listdir(path):
        if extension(f) == 'xml':
            append_recipes(body,path,f)

    tree = etree.ElementTree(root)
    tree.write(path+'index.html',pretty_print=True,encoding='UTF-8')
