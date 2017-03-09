import warnings
import os
from doctest import Example
from lxml.doctestcompare import LXMLOutputChecker
from functools import wraps

class XmlTestMixin(object):
    """ mixin to test xml for equality
    Uses lxml's doctestcompare facilities to compare XMLs that are serialized
    to strings.  Since it has no knowledge of the document structure is ensures
    the most basic guarantees that XML makes. Tags are treated as being ordered
    whereas attributes are being treated as unordered. Whitespace (except in
    text nodes) is ignored.

    Usage:
        class TextFixture(unittest.TestCase, XmlTestMixin):
            pass
    """
        
    def assertXmlEqual(self, got, want):
        """ fail if the two objects are not equal XML serializations
        In case of a failure, both serializations are pretty printed
        with differences marked.
        There is not check well-formedness or against any schema, only
        slightly intelligent matching of the tested string to the reference
        string.

        '...' can be used as a wildcard instead of nodes or attribute values.

        Wildcard Examples:
            <foo>...</foo>
            <foo bar="..." />

        Arguments:
            got -- string to check, as unicode string
            want -- reference string, as unicode string

        Usage Example:
            self.assertXmlEqual(etree.tounicode(...), reference)
        """
        checker = LXMLOutputChecker()
        if not checker.check_output(want, got, 0):
            message = checker.output_difference(Example("", want), got, 0)
            raise AssertionError(message)

class RealEqualMixin(object):
    """ methods to check comparison operators """
    def assertRealEqual(self, a, b, msg=None):
        """ checks the == and != operators, also check symmetry """
        self.assertTrue( a == b, '{!r} == {!r}'.format(a, b))
        self.assertTrue( b == a, '{!r} == {!r}'.format(b, a))
        self.assertFalse( a != b, '{!r} != {!r}'.format(a, b))
        self.assertFalse( b != a, '{!r} != {!r}'.format(b, a))

    def assertRealNotEqual(self, a, b, msg=None):
        """ checks the == and != operators, also check symmetry """
        self.assertTrue( a != b, '{!r} != {!r}'.format(a, b))
        self.assertTrue( b != a, '{!r} != {!r}'.format(b, a))
        self.assertFalse( a == b, '{!r} == {!r}'.format(a, b))
        self.assertFalse( b == a, '{!r} == {!r}'.format(b, a))

class TypeCheckMixin(object):
    def assertType(self, obj, t):
        """ fail if obj is not of type t """
        if not isinstance(obj, t):
            raise AssertionError('{!r} is not of type {}'.format(obj, t))

def extension(filename):
    """ returns the extension when given a filename

    will return None if there is no extension

    >>> extension('foo.bar')
    'bar'
    >>> extension('foo')
    None
    """
    s = filename.split('.')
    if len(s) > 1:
        return s[-1]
    else:
        return None

def Trace(f):
    @wraps(f)
    def dec_f(*args, **kwargs):
        print('entering ' +  f.__name__)
        print('  args: ' + str(args))
        print('  kwargs: ' + str(kwargs))
        result = f(*args, **kwargs)
        print('  returns {}'.format(str(result)))
        print('exiting ' +  f.__name__)
        return result
    return dec_f

class ChangeDir(object):
    """ changes the current working directoy
    best used with a context manager:

        with ChangeDir('/some/where'):
            ....

    after exiting the context, the current working
    directory is restored to its prior state.

    One can also call cleanup() to restore the
    working directory manually
    """
    def __init__(self, path):
        self._oldPath = os.getcwd()
        os.chdir(path)

    def __enter__(self):
        return self

    def __exit__(self, exit, value, exc):
        self.cleanup()

    def __del__(self):
        self.cleanup(_warn = True)

    def cleanup(self, _warn = False):
        """ call to cleanup manually """
        if self._oldPath is not None:
            os.chdir(self._oldPath)
            self._oldPath = None
            if _warn:
                warnings.warn('Implicit cleanup of {!r}'.format(self), ResourceWarning, stacklevel=2)
