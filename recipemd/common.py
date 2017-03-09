import os
import io
import os.path
from recipemd.parser import parseFile
from recipemd import git
from recipemd.serializer.xml import dump


def process(obj_id, target, xslt = None):
  """ get file from git, process, write to target folder

  Arguments:
  obj_id -- git object id of the file (as string)
  target -- target folder path (as string, with trailing slash)
  xslt   -- xslt file path if xml-stylesheet PI should be included,
            no PI will be included if null (which is default)
  """
  stream = io.TextIOWrapper(git.blob_file_handle(obj_id), encoding='utf8')
  r = parseFile(stream)
  dump(target, r, xslt)

def xml_filename(name, path):
  if not name.endswith('.rmd'):
    raise Exception('Invalid file extension for recipe ({})'.format(name))
  clean = name[0:-4] + '.xml'
  return os.path.join(path, clean)

def clean_output_dir(path):
  """ remove xml files and index.html from path """

  for (_, _, filenames) in os.walk(path):
    for f in filenames:
      if f.split('.')[-1] == 'xml':
        os.remove(os.path.join(path, f))
  try:
    os.remove(path + '/index.html')
  except FileNotFoundError:
    pass
