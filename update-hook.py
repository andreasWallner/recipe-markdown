#!/usr/bin/python3

import os
import io
import sys
import git
import index
from lxml import etree

from parser import parseFile
from serializer import serializeRecipes

TARGET='/var/www/localhost/htdocs/uhu01/recipes/'
XSLT='recipe2html.xslt'

def process( obj_id, target):
    stream = io.TextIOWrapper( git.blob_file_handle(obj_id), encoding='utf8')
    r = parseFile(stream)
    rec = serializeRecipes(r)
    rec.addprevious(etree.ProcessingInstruction('xml-stylesheet', 'type="text/xsl" href="' + XSLT + '"'))
    et = etree.ElementTree(rec)
    et.write(target,xml_declaration=True,pretty_print=True,encoding='UTF-8')

def cleanup_filename(name):
    parts = name.split('.')
    if parts[-1] == 'rmd':
        return '.'.join(parts[:-1])
    else:
        return name

def xml_filename(name):
    return TARGET + cleanup_filename(name) + '.xml'

(ref,old,new) = sys.argv[1:4]

print('starting processing of commit')

cf = git.changed_files(old,new)

# do a dry run to catch errors
for f in cf:
    action = f[4]
    file = ' '.join(f[5:])
    obj_id = f[3]
    if action == 'M' or action == 'A' or action == 'C':
        r = process(obj_id,'/dev/null')

# do a real run
for c in cf:
    action = c[4]
    file = ' '.join(c[5:])
    obj_id = c[3]
    if action == 'D':
        print('D {}'.format(file))
        try:
            os.remove(xml_filename(file))
        except FileNotFoundError:
            print('file to be removed, but could not be found'.format(file))

    elif action == 'M' or action == 'A' or action == 'C':
        print('C {}'.format(file))
        process(obj_id, xml_filename(file))

    else:
        print('unknown git status {} of <{}>'.format(action,file), file=sys.stderr)

index.update_index(TARGET)

print('finished processing of commits')

exit(1)

