#!/usr/bin/python3

import os
import io
import sys
import git
from lxml import etree

from parser import parseFile
from serializer import serializeRecipes

TARGET='/var/www/localhost/htdocs/uhu01/recipes/'
XSLT='recipe2html.xslt'

def process( obj_id, target):
    stream = io.TextIOWrapper( git.blob_file_handle(obj_id), encoding='utf8')
    r = parseFile(stream)
    et = serializeRecipes(r)
    et.addprevious(etree.ProcessingInstruction('xml-stylesheet', 'type="text/xsl" href="' + XSLT + '"'))
    e = etree.ElementTree(serializeRecipes(r))
    e.write(target,xml_declaration=True,pretty_print=True,encoding='UTF-8')

def update_index():
    # very ugly index
    root = etree.Element('html')
    body = etree.SubElement(root,'body')
    
    for f in os.listdir(TARGET):
        print(f)

(ref,old,new) = sys.argv[1:4]

print('starting processing of commit')

cf = git.changed_files(old,new)

# do a dry run to catch errors
for f in cf:
    action = f[4]
    file = ' '.join(f[5:])
    obj_id = f[3]
    if action == 'M' or action == 'A' or action == 'C':
        r = process(git.blob_file_handle(obj_id),'/dev/null')

# do a real run
for c in cf:
   action = c[4]
   file = ' '.join(c[5:])
   obj_id = c[3]
   if action == 'D':
      print('D {}'.format(file))
      try:
         os.remove(TARGET + c[1] + '.xml')
      except FileNotFoundError:
         pass

   elif action == 'M' or action == 'A' or action == 'C':
      print('C {}'.format(file))
      process( git.blob_file_handle(obj_id), TARGET + file + '.xml')

   else:
      print('unknown git status {} of <{}>'.format(action,file), file=sys.stderr)

update_index()

print('finished processing of commits')

exit(1)

