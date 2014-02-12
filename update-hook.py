#!/usr/bin/python3

import os
import sys
import subprocess
from lxml import etree

from parser import parseFile
from serializer import serializeRecipes

TARGET='/var/www/localhost/htdocs/uhu01/recipes/'

def process( objid, target):
    environ = os.environ.copy()
    proc = subprocess.Popen(['git','cat-file','blob',objid], stdout=subprocess.PIPE, env=environ)
    proc.wait(1000)
    r = parseFile(proc.stdout)
    e = etree.ElementTree(serializeRecipes(r))
    e.write(target,xml_declaration=True,pretty_print=True,encoding='UTF-8')

def changed_files(old,new):
   environ = os.environ.copy()
   proc = subprocess.Popen(['git','diff-tree','--full-index',old,new], stdout=subprocess.PIPE, env=environ)
   proc.wait(1000)

   if proc.returncode != 0:
      print('git process failed ({})'.format(proc.returncode))
      exit(1)

   return [ l.decode('utf8').strip('\n').split() for l in proc.stdout ]

(ref,old,new) = sys.argv[1:4]

print('starting processing of commit')

cf = changed_files(old,new)

# do a dry run to catch errors
for f in cf:
    action = f[4]
    file = f[5]
    objid = f[3]
    if f[0] == 'M' or f[0] == 'A' or f[0] == 'C':
        r = process(f[1],'/dev/null')

# do a real run
for c in cf:
   action = c[4]
   file = c[5]
   objid = c[3]
   if action == 'D':
      print('D {}'.format(file))
      try:
         os.remove(TARGET + c[1] + '.xml')
      except FileNotFoundError:
         pass
   elif action == 'M' or action == 'A' or action == 'C':
      print('C {}'.format(file))
      process( objid, TARGET + file + '.xml')
   else:
      print('unknown git status {} of <{}>'.format(action,file), file=sys.stderr)
#updateList()

print('finished processing of commits')

exit(1)

