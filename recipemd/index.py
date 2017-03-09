import os
import json
from lxml import etree
from operator import itemgetter
from recipemd import utils

try:
    from jinja2 import Environment, FileSystemLoader
    update_index = lambda p: update_index_jinja(p)
except ImportError:
    import html
    update_index = lambda p: update_index_simple(p)

def _extract_data(path, f):
    recipes = []
    abspath = os.path.join(path, f)
    xml = etree.parse(abspath)
    for r in xml.xpath('//recipe'):
        meta = {'filename' : f}
        for m in r.xpath('meta/*'):
            meta[m.tag] = m.text

        recipes.append(meta)
    return recipes

def _collect_data(path):
    recs = []
    for f in os.listdir(path):
        # encoding dance to deal with surrogate characters from listdir
        f = f.encode('utf-8', 'surrogateescape').decode('utf-8')
        if utils.extension(f) == 'xml':
            for r in _extract_data(path, f):
                recs.append(r)
    recs = sorted(recs, key=itemgetter('title'))
    return recs

def update_index_jinja(path):
    recs = _collect_data(path)

    env = Environment(loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')))
    template = env.get_template('index.jinja')

    # specify encoding explicitly, since the shell that git spawns us in does
    # not have a locale set, so open() would default to ANSI_X3.4-1968
    template.stream(recipes=recs).dump(path + 'index.html', encoding='utf-8')

def update_json(path):
    """ write index.json in/for path """
    recs = _collect_data(path)

    with open(path + '/metadata.json', 'w') as fp:
        json.dump(recs, fp, indent=2)

def _append_recipes(body, path, f):
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

        a = etree.SubElement(body, 'a')
        a.attrib['href'] = html.escape(f).replace(' ', '%20')
        a.text = html.escape(title)
        etree.SubElement(body, 'br')

def update_index_simple(path):
    """ write index.html in/for path """
    
    root = etree.Element('html')
    head = etree.SubElement(root, 'head')
    title = etree.SubElement(head, 'title')
    title.text = 'Recipes'
    meta = etree.SubElement(head, 'meta')
    meta.attrib['http-equiv'] = "Content-Type"
    meta.attrib['content'] = "text/html;charset=utf-8"
    body = etree.SubElement(root, 'body')
    
    for f in os.listdir(path):
        # encoding dance to deal with surrogate characters from listdir
        f = f.encode('utf-8', 'surrogateescape').decode('utf-8')
        if utils.extension(f) == 'xml':
            _append_recipes(body, path, f)

    with open(path + 'index.html', 'wb') as f:
        f.write(b'<!DOCTYPE HTML>')
        etree.ElementTree(root).write(f, encoding='utf-8')

