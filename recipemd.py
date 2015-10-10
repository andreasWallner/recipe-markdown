#!/usr/bin/python

import sys
import argparse
import serializer.json as js
import serializer.xml as xs

from parser import parseFile

class BarAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        didfoo = getattr(namespace, first_action.dest, first_action.default)
        if didfoo == first_action.default:
            parser.error("foo before bar!")
        else:
            setattr(namespace, self.dest, values)

def main():
    parser = argparse.ArgumentParser(description='Work with recipe markdown files')
    parser.add_argument('-i', metavar='mdfile', type=argparse.FileType('r'), help='name of the markdown file to process, default: use stdin', default=sys.stdin)
    parser.add_argument('-o', metavar='output', type=argparse.FileType('wb'), help='name of the output file, default: use stdout', default=sys.stdout.buffer)
    parser.add_argument('-t', metavar='outtype', choices=['xml', 'json'], help='output type to generate (xml, json), default: xml', default='xml')
    parser.add_argument('--xslt', metavar='xslt', help='xslt to reference in PI of generated XMLs, ignored if outtype is not "xml"', default=None)
    args = parser.parse_args()

    recipes = parseFile(args.i)

    if args.t == 'xml':
        xs.dump(args.o, recipes, args.xslt)
    else:
        js.dump(args.o, recipes)

if __name__ == '__main__':
    main()
