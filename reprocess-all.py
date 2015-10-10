#!/usr/bin/env python3

import os
import sys
import git
import index
import argparse
import utils
from lxml import etree

import common

# hook is being executed inside the repository, so add the hooks
# directory to the path so that we can load our configuration from there
sys.path.append(os.getcwd())
settingsAvailable = False
try:
  import settings
  settingsAvailable = True
except ImportError:
  pass

def reprocess(target, source, umask = None):
  target = os.path.abspath(target)
  with utils.ChangeDir(source):
    if umask is not None:
      os.umask(umask)

    print('starting processing of all recipes')
    common.clean_output_dir(target)
    files = git.ls_tree('HEAD')

    # do a dry run to catch errors
    for f in files:
      file = ' '.join(f[3:])
      obj_id = f[2]

      if file.split('.')[-1] != 'rmd':
        continue

      r = common.process(obj_id, '/dev/null')

    # do a real run
    for f in files:
      file = f[3]
      obj_id = f[2]

      if file.split('.')[-1] != 'rmd':
        continue

      print('P {}'.format(file))
      common.process(obj_id, common.xml_filename(file, target))

    print('finished processing of files')

def main():
  defaultTarget = '.'
  defaultUmask = 0o022
  if settingsAvailable:
    defaultTarget = settings.TARGET
    defaultUmask = settings.UMASK

  parser = argparse.ArgumentParser(description='Work with recipe markdown files')
  parser.add_argument('-s', metavar='source', help='source of data', default='.')
  parser.add_argument('-t', metavar='target', help='target for processed outputs', default=defaultTarget)
  parser.add_argument('-i', help='do not reprocess, build index', default=None, action='store_true')
  parser.add_argument('-j', help='do not reprocess, build metadata json', default=None, action='store_true')
  args = parser.parse_args()

  if args.t is None:
    print('no target specified via command line or config file')
    return 1

  if args.i is None and args.j is None:
    reprocess(args.t, args.s, defaultUmask)

  target = args.t + '/'
  if args.i or args.i is None:
    print('building html index')
    index.update_index(target)

  if args.j or args.j is None:
    print('building json index')
    index.update_json(target)

  return 0

if __name__ == '__main__':
    sys.exit(main())
