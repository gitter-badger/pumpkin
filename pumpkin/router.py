import sys
import re

if sys.version < '3':
    from urlparse import parse_qs
else:
    from urllib.parse import parse_qs

"""
A simple router.
"""


class RouterException(Exception):
    pass


class Router(object):

    """Router object for request routing.
    """

    def __init__(self):
        self.rules = {}
        '''
        '/'
        '/hello'
        '/hello/pumpkin'
        '/hello/pumpkin/<int:id>'
        '''
        # caution!!!!
        # weird in python 3: get nothing to repeat error in python 3
        # http://stackoverflow.com/questions/3675144/regex-error-nothing-to-repeat
        self.url_pattern = re.compile(
            r'(?P<prefix>(/\w*)+)(?P<suffix><(?P<type>\w*)?:(?P<arg>\w*)>)?')

        # methods
        self.methods = {}
        self.methods.setdefault("GET", [])
        self.methods.setdefault("POST", [])
        self.methods.setdefault("DELETE", [])
        self.methods.setdefault("PUT", [])

    def register(self, path, fn, methods):
        if not callable(fn):
            raise RouterException("Router only accept callable object.")

        for m in methods:
            self.methods[m].append(fn)

        g = self.url_pattern.match(path)
        if not g:
            raise RouterException(
                "Router rules : %s can not be accepted." % path)
        p = g.group('prefix')
        if g.group('suffix'):
            assert g.group('type') == 'int', g.group('type')
            p += '(?P<args>\d+)'
            self.rules[(re.compile(p), g.group('arg'))] = fn
        else:
            self.rules[p] = fn

    def __call__(self, p, method='GET'):
        return self.get(p, mathod)

    def get(self, path, method='GET'):
        try:
            f, args = self._match_path(path)
        except TypeError:
            return None
        if not f:
            return None
        method = method.upper()
        if f not in self.methods.get(method):
            raise RouterException(
                "Request method %s not allowed in this app." % method)
        return (f, args)

    def _match_path(self, p):
        for k in self.rules:
            if isinstance(k, str):
                if k == p:
                    return self.rules[k], None
            elif isinstance(k[0], type(re.compile('dommy'))):
                _g = k[0].match(p)
                if _g:
                    return (self.rules[k], {k[1]: _g.group('args')})

    def url_for(self, fn):
        if not callable(object):
            raise RouterException(
                "router url_for method only accept callable object.")
        for k, v in self.rules.items():
            if v == fn:
                return k
        raise RouterException(
            "callable object doesn't matched any routing rule.")

    def all_callables(self):
        return self.rules.values()

