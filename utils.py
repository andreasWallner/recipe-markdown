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
