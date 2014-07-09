#!/usr/bin/python3

import os
import io
import sys
import git
import index
from lxml import etree

from parser import parseFile
from serializer import serializeRecipes

# hook is being executed inside the repository, so add the hooks
# directory to the path so that we can load our configuration from there
sys.path.append(os.getcwd())
import settings

def process( obj_id, target):
    """ get file from git, process, write to target folder

    Arguments:
    obj_id -- git object id of the file (as string)
    target -- target folder path (as string, with trailing slash)
    """
    stream = io.TextIOWrapper( git.blob_file_handle(obj_id), encoding='utf8')
    r = parseFile(stream)
    rec = serializeRecipes(r)
    rec.addprevious(etree.ProcessingInstruction('xml-stylesheet', 'type="text/xsl" href="' + settings.XSLT + '"'))
    et = etree.ElementTree(rec)
    et.write(target,xml_declaration=True,pretty_print=True,encoding='UTF-8')

def xml_filename(name):
    clean = name.rstrip('.rmd')
    return settings.TARGET + clean + '.xml'

def clean_output_dir():
    path = settings.TARGET

    for (_, _, filenames) in os.walk(settings.TARGET):
        for f in filenames:
            if f.split('.')[-1] == 'xml':
                os.remove(settings.TARGET + f)
    os.remove(settings.TARGET + 'index.html')

def main():
    os.umask(settings.UMASK)

    print('starting processing of all recipes')
    clean_output_dir()
    files = git.ls_tree('HEAD')

    # do a dry run to catch errors
    for f in files:
        file = ' '.join(f[3:])
        obj_id = f[2]

        if file.split('.')[-1] != 'rmd':
            continue

        r = process(obj_id,'/dev/null')

    # do a real run
    for f in files:
        file = f[3]
        obj_id = f[2]

        if file.split('.')[-1] != 'rmd':
            continue

        print('P {}'.format(file))
        process(obj_id, xml_filename(file))

    index.update_index(settings.TARGET)

    print('finished processing of commits')

if __name__ == '__main__':
    main()
