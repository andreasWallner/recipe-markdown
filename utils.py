from functools import wraps

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
