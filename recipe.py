#!/usr/bin/python

import sys
import argparse
from lxml import etree

from parser import parseFile
from serializer import serializeRecipes

#from IPython.core import ultratb
#sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)

def main():
    parser = argparse.ArgumentParser(description='Work with recipe markdown files')
    parser.add_argument('-i', metavar='mdfile', type=argparse.FileType('r'), help='name of the markdown file to process', default=sys.stdin)
    parser.add_argument('-o', metavar='output', type=argparse.FileType('wb'), help='name of the output file', default=sys.stdout.buffer)
    args = parser.parse_args()

    r = parseFile(args.i)
    e = etree.ElementTree(serializeRecipes(r))
    e.write(args.o, xml_declaration=True, pretty_print=True, encoding='UTF-8')

if __name__ == '__main__':
    main()
