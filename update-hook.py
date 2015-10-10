#!/usr/bin/python3

import os
import io
import sys
import git
import index

import common

# hook is being executed inside the repository, so add the hooks
# directory to the path so that we can load our configuration from there
sys.path.append(os.path.join(os.getcwd(), 'hooks'))
import settings

def main():
    os.umask(settings.UMASK)
    (ref,old,new) = sys.argv[1:4]

    print('starting processing of commit')

    cf = git.changed_files(old,new)

    # do a dry run to catch errors
    for f in cf:
        action = f[4]
        file = f[5]
        obj_id = f[3]
        
        if file.split('.')[-1] != settings.EXTENSION:
            continue

        if action == 'M' or action == 'A' or action == 'C':
            r = common.process(obj_id,'/dev/null')

    # do a real run
    for c in cf:
        action = c[4]
        file = c[5]
        obj_id = c[3]
        
        if file.split('.')[-1] != settings.EXTENSION:
            continue

        filename = common.xml_filename(file, settings.TARGET)

        if action == 'D':
            print('D {}'.format(file))
            try:
                os.remove(filename)
            except FileNotFoundError:
                print('file to be removed, but could not be found'.format(file))

        elif action == 'M' or action == 'A' or action == 'C':
            print('C {}'.format(file))
            common.process(obj_id, filename)

        else:
            print('unknown git status {} of <{}>'.format(action, file), file=sys.stderr)

    index.update_index(settings.TARGET)
    index.update_json(settings.TARGET)

    print('finished processing of commits')

if __name__ == '__main__':
    main()
