#!/bin/env python3

"""Migrate old recipe markdown files by changing a few special characters."""

import re
import argparse

replacements = {
    '*': '-',
    '#': '*',
    '-': '#',
}

def repl(m):
    return m.group(1) + replacements[m.group(2)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='+', type=argparse.FileType('r'), help='files to convert')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse the replacements')
    args = parser.parse_args()
    if args.reverse:
        global replacements
        replacements = {v: k for k, v in replacements.items()}

    for f in args.file:
        contents = f.read()
        contents = re.sub('^(\s*)([-#\*])', repl, contents, flags=re.MULTILINE)
        f.close()
        with open(f.name, 'w') as out:
            out.write(contents)
        print(f.name, 'updated')

if __name__ == '__main__':
    main()

