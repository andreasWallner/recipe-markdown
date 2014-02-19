import os
import utils
from lxml import etree

def append_recipes(body, path, f):
    """ insert recipe information into a page

    can not handle files that are not in the webroot by itself
    this has to be done on the index page (via pointing the
    browser at another basedir)

    Arguments:
    body -- etree.Element where the information should be put into
    path -- path to the file
    file -- filename (will also be placed into the link
    """
    xml = etree.parse(path + f)
    recipes = xml.xpath('//recipe')

    for r in recipes:
        title = r.xpath('//title')[0].text

        a = etree.SubElement(body,'a')
        a.attrib['href'] = f
        a.text = title

def update_index(path):
    """ write index.html in/for path """
    root = etree.Element('html')
    body = etree.SubElement(root, 'body')
    
    for f in os.listdir(path):
        if utils.extension(f) == 'xml':
            append_recipes(body, path, f)

    tree = etree.ElementTree(root)
    tree.write(path+'index.html',pretty_print=True,encoding='UTF-8')
