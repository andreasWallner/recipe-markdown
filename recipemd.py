#!/usr/bin/python

import sys
import argparse
import serializer.json as js
import serializer.xml as xs

from parser import parseFile

def main():
    parser = argparse.ArgumentParser(description='Work with recipe markdown files')
    parser.add_argument('-i', metavar='mdfile', type=argparse.FileType('r'), help='name of the markdown file to process', default=sys.stdin)
    parser.add_argument('-o', metavar='output', type=argparse.FileType('wb'), help='name of the output file', default=sys.stdout.buffer)
    parser.add_argument('-t', metavar='outtype', choices=['xml', 'json'], help='output type to generate (xml, json)', default='xml')
    args = parser.parse_args()

    recipes = parseFile(args.i)

    if args.t == 'xml':
        xs.dump(args.o, recipes)
    else:
        js.dump(args.o, recipes)

if __name__ == '__main__':
    main()
