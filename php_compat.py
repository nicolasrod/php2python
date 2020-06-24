# coding: utf8

"""
PHP Compatibility Layer
=======================
Run its doctests by executing:

$ python3 -m doctest php_compat.py
"""
import atexit
import base64
import cgi
import functools
import hashlib
import hmac
import inspect
import io
import itertools
import json
import mysql.connector
import os
import os.path
import random
import re
import sys
import tempfile
import uuid

from collections import namedtuple
from contextlib import redirect_stdout
from datetime import datetime
from goto import with_goto
from packaging import version
from urllib.parse import urlparse
import subprocess
import html

def php_yield(var_):
    try:
        yield from var_
    except:
        yield var_


def php_empty(var_):
    """
    >>> expected_array_got_string = 'somestring'
    >>> php_empty(expected_array_got_string)
    False
    >>> php_empty(expected_array_got_string[0])
    False
    >>> print(len(Array()))
    0
    >>> print(len(Array()) == 0)
    True
    >>> php_empty(Array())
    True
    """
    # if var_ is a lambda, evaluate it
    if callable(var_):
        try:
            var_ = var_()
        except:
            return True

    if var_ is None:
        return True
    if isinstance(var_, bool) and not var_:
        return True
    if isinstance(var_, str) and (var_ == "" or var_ == "0"):
        return True
    if (isinstance(var_, int) or isinstance(var_, float)) and var_ == 0:
        return True
    if isinstance(var_, Array):
        return len(var_) == 0
    if not php_isset(var_):
        return False
    return False


def php_get_locals(locals_, *args):
    return [locals_[x] for x in args]


def fix_ext(fname):
    filename, ext = os.path.splitext(fname)

    if ext.lower().strip() == ".php":
        return f"{filename}.py"
    return fname


def php_no_error(fn):
    try:
        return fn()
    except:
        pass


def php_set_include_retval(val):
    globals()["__php_include_return_value__"] = val


def php_get_include_retval():
    return globals()["__php_include_return_value__"]


def php_include_file(fname, once=True, redirect=False):
    global __DIR__
    global __FILE__

    old_dir = __DIR__
    old_file = __FILE__

    filename = fix_ext(fname)

    if fname.startswith('/'):  # absolute path
        __FILE__ = os.path.realpath(filename)
    else:
        __FILE__ = os.path.join(__DIR__, filename)

    __DIR__ = os.path.dirname(__FILE__)

    if __FILE__ in _PHP_INCLUDES and once:
        return None

    _PHP_INCLUDES[__FILE__] = True

    print(">>> IMPORTING:", __FILE__)
    with open(__FILE__) as src:
        code = compile(src.read().replace("\x00", ""), filename, "exec")

    try:
        if redirect:
            f = io.StringIO()
            with redirect_stdout(f):
                exec(code, globals(), globals())
            return f.getvalue()

        php_set_include_retval(None)
        exec(code, globals(), globals())
        return php_get_include_retval()
    except SystemExit as e:
        if e.code != -1:
            raise e
    finally:
        __DIR__ = old_dir
        __FILE__ = old_file

# -----------------------------------------------------------------------------------
# PHP globals


class Resource:
    pass


class Traversable:
    pass


class Iterator:
    pass


class IteratorAggregate:
    pass


class IteratorArrayAccess:
    pass


class Throwable:
    pass


class ArrayAccess:
    pass


class Serializable:
    pass


class Closure:
    pass


class Generator:
    pass


class WeakReference:
    pass


class Array():
    def __init__(self, *items, _preserve=False):
        self.data = {}
        self.reset()

        for item in items:
            self.extend(item, _preserve=_preserve)

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, k):
        if isinstance(k, (int, str)):
            return self.data.get(k, Array())
        else:
            return list(self.data.items())[k.start:k.stop:k.step]

    def get(self, k, def_):
        if self.has_key(k):
            return self.__getitem__(k)
        return def_

    def __setitem__(self, k, v=None):
        if v is None:
            self.data[self.get_next_idx()] = k
        else:
            self.data[self.get_next_idx() if k == -1 else k] = v

    def extend(self, arr, _preserve=False):
        if isinstance(arr, Array) or isinstance(arr, dict):
            pass  # we're ready for it!
        elif isinstance(arr, list) or isinstance(arr, tuple):
            arr = dict(enumerate(arr))
        else:
            # single value!
            arr = dict([(self.get_next_idx(), arr)])

        for k, v in arr.items():
            self.data[k if (not isinstance(k, int) or _preserve
                            ) else self.get_next_idx()] = v

    def get_next_idx(self):
        return max([-1] + [x for x in self.data if isinstance(x, int)]) + 1

    def __iter__(self):
        ks = self.data.keys()
        if len([True for x in ks if isinstance(x, int)]) != len(ks):
            yield from self.data.items()
        else:
            yield from self.data.values()

    def items(self):
        return self.data.copy().items()

    def get_keys(self):
        return list(self.data.copy().keys())

    def has_key(self, k):
        return k in self.data

    def values(self):
        return list(self.data.copy().values())

    def __len__(self):
        return len(self.data.items())

    def pop(self):
        return self.data.popitem()[1]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def shift(self):
        first_key = list(self.data.keys())[0]
        first_val = self.data.pop(first_key)

        self.set(Array(self.data))
        self.reset()
        return first_val

    def set(self, data, preserve=False, clean=True):
        if clean:
            self.data = {}
        self.extend(data, preserve)

    def slice(self, start_=0, end_=None, _preserve=False):
        items = list(self.data.items())
        if start_ < 0:
            start_ = len(items) + start_
            end_ = start_ + end_
        return Array(dict(items[start_:end_]), _preserve=_preserve)

    def key(self):
        if self.pos is None:
            return False
        return self.iter[self.pos][0]

    def current(self):
        if self.pos is None:
            self.iter = list(self.data.items())
            self.pos = 0

        try:
            return self.iter[self.pos][1]
        except:
            self.reset()
            return False

    def next(self):
        self.pos += 1
        return self.current()

    def prev(self):
        self.pos -= 1
        return self.current()

    def end(self):
        if self.pos is None:
            return

        self.pos = len(self.iter)
        return self.current()

    def reset(self):
        self.pos = None
        self.iter = None


# =============================================================0
# Load "PHP" INI file


_src = os.path.dirname(os.getenv('PHP2PY_COMPAT', __file__))

with open(os.path.join(_src, 'php_compat.ini'), 'r') as f:
    data = f.read()
    _ini_json = json.loads(data)

_PHP_INI_FILE = Array(_ini_json)
_PHP_INI_FILE_DETAILS = Array(dict(
    [(k, Array({'global_value': v, 'local_value': v, 'access': 7}))
     for k, v in _ini_json.items()]))



# =============================================================0

__FILE__ = os.path.realpath(__file__)
__DIR__ = os.path.dirname(__FILE__)

# TODO: probably use PHP_GLOBALS as a proxy objects and not get the reference to globals at this point

PHP_OS = sys.platform
PHP_GLOBALS = globals()
PHP_REQUEST = Array(cgi.FieldStorage())
PHP_SERVER = Array(os.environ)
PHP_COOKIE = Array()
PHP_FILES = Array()
PHP_SESSION = Array()
PHP_SERVER["SCRIPT_NAME"] = os.path.realpath(__file__)
PHP_SERVER["SCRIPT_FILENAME"] = os.path.realpath(__file__)
PHP_SERVER["HTTP_HOST"] = "localhost"
PHP_SERVER["SERVER_SOFTWARE"] = "localhost"
PHP_SERVER["REQUEST_URI"] = "/"
PHP_SERVER["SERVER_PORT"] = "80"
PHP_SERVER["HTTP_ACCEPT_ENCODING"] = "*"
PHP_SERVER["PHP_SELF"] = __FILE__
PHP_SAPI = ""
PHP_POST = PHP_REQUEST
PHP_ENV = PHP_SERVER
PHP_VERSION_ID = 73000

_PHP_INCLUDES = {}
_HEADERS = {}
_HEADERS_PRINTED = False
_AUTOLOAD_FN = []
_PHP_SESSION_INFO = Array({
    'name': 'PHPSESSID', 
    'id': None, 
    'path': None, 
    'domain': None, 
    'secure': False, 
    'httponly': False
})


# -----------------------------------------------------------------------------------
# PHP constants


def _Id(l=[0]):
    l[0] += 1
    return l[0]


CASE_LOWER = _Id()
CASE_UPPER = _Id()
COUNT_NORMAL = _Id()
COUNT_RECURSIVE = _Id()
CURLVERSION_NOW = _Id()
DEBUG_BACKTRACE_PROVIDE_OBJECT = _Id()
E_ALL = _Id()
E_COMPILE_ERROR = _Id()
E_CORE_ERROR = _Id()
E_CORE_WARNING = _Id()
E_DEPRECATED = _Id()
E_ERROR = _Id()
E_NOTICE = _Id()
E_PARSE = _Id()
E_RECOVERABLE_ERROR = _Id()
E_STRICT = _Id()
E_USER_ERROR = _Id()
E_USER_NOTICE = _Id()
E_USER_WARNING = _Id()
E_WARNING = _Id()
ENT_COMPAT = _Id()
ENT_HTML401 = _Id()
ENT_NOQUOTES = _Id()
ENT_QUOTES = _Id()
ENT_IGNORE = _Id()
ENT_SUBSTITUTE = _Id()
ENT_DISALLOWED = _Id()
ENT_HTML401 = _Id()
ENT_XML1 = _Id()
ENT_XHTML = _Id()
ENT_HTML5 = _Id()
EXTR_OVERWRITE = _Id()
FILEINFO_NONE = _Id()
FILTER_DEFAULT = _Id()
FORCE_GZIP = _Id()
FTP_BINARY = _Id()
HTML_SPECIALCHARS = _Id()
IDNA_DEFAULT = _Id()
INFO_ALL = _Id()
INI_ALL = _Id()
INI_PERDIR = _Id()
INI_SYSTEM = _Id()
INI_USER = _Id()
INTL_IDNA_VARIANT_UTS46 = _Id()
M_E = _Id()
MCRYPT_DEV_URANDOM = _Id()
OPENSSL_ALGO_SHA1 = _Id()
OPENSSL_PKCS1_PADDING = _Id()
PATHINFO_BASENAME = _Id()
PATHINFO_DIRNAME = _Id()
PATHINFO_EXTENSION = _Id()
PATHINFO_FILENAME = _Id()
PHP_BINARY_READ = _Id()
PHP_INT_MAX = _Id()
PHP_OUTPUT_HANDLER_STDFLAGS = _Id()
PHP_QUERY_RFC1738 = _Id()
PHP_ROUND_HALF_UP = _Id()
PHP_URL_FRAGMENT = _Id()
PHP_URL_HOST = _Id()
PHP_URL_PASS = _Id()
PHP_URL_PATH = _Id()
PHP_URL_PORT = _Id()
PHP_URL_QUERY = _Id()
PHP_URL_SCHEME = _Id()
PHP_URL_USER = _Id()
PKCS7_DETACHED = _Id()
PREG_PATTERN_ORDER = _Id()
SCANDIR_SORT_ASCENDING = _Id()
SEEK_SET = _Id()
SODIUM_CRYPTO_GENERICHASH_BYTES = _Id()
SORT_REGULAR = _Id()
SORT_STRING = _Id()
SORT_NUMERIC = _Id()
SSH2_TERM_UNIT_CHARS = _Id()
STR_PAD_RIGHT = _Id()
STR_PAD_LEFT = _Id()
STR_PAD_BOTH = _Id()
STREAM_CLIENT_CONNECT = _Id()
ZLIB_ENCODING_RAW = _Id()

JSON_ERROR_NONE = _Id()
JSON_ERROR_DEPTH = _Id()
JSON_ERROR_STATE_MISMATCH = _Id()
JSON_ERROR_CTRL_CHAR = _Id()
JSON_ERROR_SYNTAX = _Id()
JSON_ERROR_UTF8 = _Id()
JSON_ERROR_RECURSION = _Id()
JSON_ERROR_INF_OR_NAN = _Id()
JSON_ERROR_UNSUPPORTED_TYPE = _Id()
JSON_ERROR_INVALID_PROPERTY_NAME = _Id()
JSON_ERROR_UTF16 = _Id()

# --------------------------------------------------------------------------------------------
# @@ Patch compile-time transformations


def to_python(fn, args):
    if f"php_{fn}" in globals():
        return globals()[f"php_{fn}"](*args)
    return f"""{fn}({",".join(args)})"""


# --------------------------------------------------------------------------------------------
# Implementing PHP Switch/Case in Python
# Source: https://stuff.mit.edu/afs/athena/software/su2_v5.0/bin/SU2/util/switch.py


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


# --------------------------------------------------------------------------------------------


def php_new_class(klass, ctr):
    if not klass in globals():
        for alfn in _AUTOLOAD_FN:
            php_call_user_func(alfn, klass)
    return ctr()


def php_isset(v):
    try:
        v = v() if callable(v) else v

        # TODO: check if we can use php_empty() instead
        if isinstance(v, Array) and len(v) == 0:
            return False
        return not v is None
    except:
        return False


def php_check_if_defined(*args):
    for k in args:
        if k not in globals():
            globals()[k] = Array()


def php_define(k, v):
    globals()[k] = v


def php_defined(k):
    return k in globals()


def php_exit(_value=1):
    php_print()
    sys.exit(_value)


def php_print(*args):
    global _HEADERS_PRINTED

    if not _HEADERS_PRINTED:
        if len([x.lower().strip() == "content-type"
                for x in _HEADERS.keys()]) == 0:
            print("Content-Type: text/html")

        for k, v in _HEADERS.items():
            # TODO: sanitize headers!
            print(f"{k}: {v}")

        print()
        _HEADERS_PRINTED = True

    print(*args, end=" ")


def php_array_change_key_case(_array, _case=CASE_LOWER):
    """
    >>> input_array = Array({"FirSt": 1, "SecOnd": 4})
    >>> input_array
    {'FirSt': 1, 'SecOnd': 4}

    >>> php_array_change_key_case(input_array, CASE_UPPER)
    {'FIRST': 1, 'SECOND': 4}
    """
    out = Array()
    for k, v in _array.items():
        if isinstance(k, str):
            k = k.lower() if _case == CASE_LOWER else k.upper()
        out[k] = v
    return out


def php_array_column(_input, _column_key, _index_key=None):
    """
    >>> records = Array([ \
            Array({'id': 2135, 'first_name': 'John', 'last_name': 'Doe'}), \
            Array({'id': 3245, 'first_name': 'Sally', 'last_name': 'Smith'}), \
            Array({'id': 5342, 'first_name': 'Jane', 'last_name': 'Jones'}), \
            Array({'id': 5623, 'first_name': 'Peter', 'last_name': 'Doe'})])
    >>> php_array_column(records, 'first_name')
    {0: 'John', 1: 'Sally', 2: 'Jane', 3: 'Peter'}

    >>> php_array_column(records, 'last_name', 'id')
    {2135: 'Doe', 3245: 'Smith', 5342: 'Jones', 5623: 'Doe'}

    # TODO: columns as class property name:
    # https://www.php.net/manual/en/function.array-column.php
    """
    out = Array()
    for arr in _input:
        idx = -1 if _index_key is None else arr[_index_key]
        out[idx] = arr[_column_key]
    return out


def php_array_combine(_keys, _values):
    """
    >>> a = Array('green', 'red', 'yellow')
    >>> b = Array('avocado', 'apple', 'banana')
    >>> php_array_combine(a, b)
    {'green': 'avocado', 'red': 'apple', 'yellow': 'banana'}
    """
    return Array(dict(zip(_keys.values(), _values.values())))


def php_array_count_values(_array):
    """
    >>> php_array_count_values(Array(1, "hello", 1, "world", "hello"))
    {1: 2, 'hello': 2, 'world': 1}
    """
    cnt = {}
    for v in _array.values():
        if not v in cnt:
            cnt[v] = 1
        else:
            cnt[v] += 1
    return cnt


def php_array_diff(_arr, *args):
    """
    >>> array1 = Array({"a": "green"}, "red", "blue", "red")
    >>> array1
    {'a': 'green', 0: 'red', 1: 'blue', 2: 'red'}
    >>> array2 = Array({"b": "green"}, "yellow", "red")
    >>> array2
    {'b': 'green', 0: 'yellow', 1: 'red'}
    >>> php_array_diff(array1, array2)
    {1: 'blue'}
    """
    cmp = list(itertools.chain.from_iterable([x.values() for x in args]))
    return Array(dict([(k, v) for k, v in _arr.items() if v not in cmp]),
                 _preserve=True)


def php_array_diff_assoc(_array1, *args):
    """
    >>> array1 = Array({"a": "green", "b": "brown", "c": "blue"}, "red")
    >>> array2 = Array({"a": "green"}, "yellow")
    >>> php_array_diff_assoc(array1, array2)
    {'b': 'brown', 'c': 'blue', 0: 'red'}
    """
    cmp = list(itertools.chain.from_iterable([x.items() for x in args]))
    return Array(dict([(k, v) for k, v in _array1.items()
                       if (k, v) not in cmp]),
                 _preserve=True)


def php_array_diff_key(_array1, *args):
    """
    >>> array1 = Array({"a": "green"}, "red", "blue", "red")
    >>> array1
    {'a': 'green', 0: 'red', 1: 'blue', 2: 'red'}
    >>> array2 = Array({"b": "green"}, "yellow", "red")
    >>> array2
    {'b': 'green', 0: 'yellow', 1: 'red'}
    >>> php_array_diff_key(array1, array2)
    {'a': 'green', 2: 'red'}
    """
    cmp = list(itertools.chain.from_iterable([x.get_keys() for x in args]))
    return Array(dict([(k, v) for k, v in _array1.items() if k not in cmp]),
                 _preserve=True)


def php_array_fill_keys(_keys, _value):
    """
    >>> ks = Array('foo', 5, 10, 'bar')
    >>> php_array_fill_keys(ks, 'banana')
    {'foo': 'banana', 5: 'banana', 10: 'banana', 'bar': 'banana'}
    """
    return Array(dict([(k, _value) for k in _keys.values()]), _preserve=True)


def php_array_filter(_array, _callback=None, _flag=0):
    """
    >>> array1 = Array({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
    >>> array2 = Array(6, 7, 8, 9, 10, 11, 12)
    >>> php_array_filter(array1, lambda n: n % 2 != 0)
    {'a': 1, 'c': 3, 'e': 5}
    >>> php_array_filter(array2, lambda n: n % 2 == 0)
    {0: 6, 2: 8, 4: 10, 6: 12}

    >>> entry = Array({0: 'foo', 1: False, 2: -1, 3: None, 4: '', 5: '0', 6: 0})
    >>> php_array_filter(entry)
    {0: 'foo', 2: -1}
    """
    if _callback is None:
        return Array(dict([(k, v) for k, v in _array.items()
                           if php_to_bool(v)]),
                     _preserve=True)
    else:
        if callable(_callback):
            return Array(dict([(k, v) for k, v in _array.items()
                               if _callback(v)]),
                         _preserve=True)
        else:
            return Array(dict([(k, v) for k, v in _array.items()
                               if php_call_user_func(_callback, v)]),
                         _preserve=True)


def php_to_bool(v):
    if v is None:
        return False

    if isinstance(v, bool):
        return v

    if isinstance(v, int) or isinstance(v, float):
        return abs(v) != 0

    if isinstance(v, str):
        return not (v == "" or v == "0")

    if isinstance(v, Array) or isinstance(v, list):
        return len(v) != 0

    if isinstance(v, dict):
        return len(v.items()) != 0
    return False


def php_array_flip(_array):
    """
    >>> input = Array("oranges", "apples", "pears")
    >>> php_array_flip(input)
    {'oranges': 0, 'apples': 1, 'pears': 2}
    """
    return Array(dict(zip(_array.values(), _array.get_keys())), _preserve=True)


def php_array_intersect(_array1, *args):
    """
    >>> array1 = Array({"a": "green"}, "red", "blue")
    >>> array2 = Array({"b": "green"}, "yellow", "red")
    >>> php_array_intersect(array1, array2)
    {'a': 'green', 0: 'red'}

    >>> array1 = Array(2, 4, 6, 8, 10, 12)
    >>> array2 = Array(1, 2, 3, 4, 5, 6)
    >>> php_array_intersect(array1, array2)
    {0: 2, 1: 4, 2: 6}
    >>> php_array_intersect(array2, array1)
    {1: 2, 3: 4, 5: 6}
    """
    cmp = list(itertools.chain.from_iterable([x.values() for x in args]))
    return Array(dict([(k, v) for k, v in _array1.items() if v in cmp]),
                 _preserve=True)


def php_array_intersect_assoc(_array1, *args):
    """
    >>> array1 = Array({"a": "green", "b": "brown", "c": "blue"}, "red")
    >>> array2 = Array({"a": "green", "b": "yellow"}, "blue", "red")
    >>> php_array_intersect_assoc(array1, array2)
    {'a': 'green'}
    """
    cmp = list(itertools.chain.from_iterable([x.items() for x in args]))
    return Array(dict([(k, v) for k, v in _array1.items() if (k, v) in cmp]),
                 _preserve=True)


def php_array_intersect_key(_array1, *args):
    """
    >>> array1 = Array({"a": "green"}, "red", "blue", "red")
    >>> array1
    {'a': 'green', 0: 'red', 1: 'blue', 2: 'red'}
    >>> array2 = Array({"b": "green"}, "yellow", "red")
    >>> array2
    {'b': 'green', 0: 'yellow', 1: 'red'}
    >>> php_array_intersect_key(array1, array2)
    {0: 'red', 1: 'blue'}
    >>> array1 = Array({'blue': 1, 'red': 2, 'green': 3, 'purple': 4})
    >>> array2 = Array({'green': 5, 'blue': 6, 'yellow': 7, 'cyan': 8})
    >>> php_array_intersect_key(array1, array2)
    {'blue': 1, 'green': 3}
    """
    cmp = list(itertools.chain.from_iterable([x.get_keys() for x in args]))
    return Array(dict([(k, v) for k, v in _array1.items() if k in cmp]),
                 _preserve=True)


def php_array_key_exists(_key, _array):
    """
    >>> php_array_key_exists('first', Array({'first': 1, 'second': 4}))
    True

    >>> php_array_key_exists('first', Array({'first': None, 'second': 4}))
    True
    """
    return _array.has_key(_key)


def php_array_keys(_array, _search=None, _strict=False):
    """
    >>> php_array_keys(Array({0: 100}, {'color': 'red'}))
    {0: 0, 1: 'color'}

    >>> php_array_keys(Array("blue", "red", "green", "blue", "blue"), "blue")
    {0: 0, 1: 3, 2: 4}

    >>> php_array_keys(Array({'color': Array('blue', 'red', 'green'), \
            'size': Array('small', 'medium', 'large')}))
    {0: 'color', 1: 'size'}
    """
    if php_empty(_array):
        return Array()

    if _search is None:
        return Array(_array.get_keys())
    else:
        return Array([k for k, v in _array.items() if v == _search])


def php_array_map(fn, _array1, *args):
    """
    >>> a = Array(1, 2, 3, 4, 5)
    >>> php_array_map(lambda n: n * n * n, a)
    {0: 1, 1: 8, 2: 27, 3: 64, 4: 125}

    >>> a = Array(1, 2, 3, 4, 5)
    >>> b = Array('uno', 'dos', 'tres', 'cuatro', 'cinco')
    >>> php_array_map(lambda n, m: f"#{n} is {m}", a, b)
    {0: '#1 is uno', 1: '#2 is dos', 2: '#3 is tres', 3: '#4 is cuatro', 4: '#5 is cinco'}
    >>> php_array_map(lambda n, m: {n: m}, a, b)
    {0: {1: 'uno'}, 1: {2: 'dos'}, 2: {3: 'tres'}, 3: {4: 'cuatro'}, 4: {5: 'cinco'}}


    >>> a = Array(1, 2, 3, 4, 5)
    >>> b = Array('one', 'two', 'three', 'four', 'five')
    >>> c = Array('uno', 'dos', 'tres', 'cuatro', 'cinco')
    >>> php_array_map(None, a, b, c)
    {0: {0: 1, 1: 'one', 2: 'uno'}, 1: {0: 2, 1: 'two', 2: 'dos'}, 2: {0: 3, 1: 'three', 2: 'tres'}, 3: {0: 4, 1: 'four', 2: 'cuatro'}, 4: {0: 5, 1: 'five', 2: 'cinco'}}

    >>> array = Array(1, 2, 3)
    >>> php_array_map(None, array)
    {0: 1, 1: 2, 2: 3}
    """

    if not callable(fn):
        fn = lambda *a: Array(a) if len(a) > 1 else a[0]

    out = Array()
    for idx, kv in enumerate(_array1.items()):
        params = [x[idx] for x in args]
        out[kv[0]] = fn(kv[1], *params)
    return out


def php_array_merge(*args):
    """
    >>> array1 = Array({"color": "red"}, 2, 4)
    >>> array1
    {'color': 'red', 0: 2, 1: 4}

    >>> array2 = Array("a", "b", {"color": "green", "shape": "trapezoid"}, 4)
    >>> array2
    {0: 'a', 1: 'b', 'color': 'green', 'shape': 'trapezoid', 2: 4}

    >>> php_array_merge(array1, array2)
    {'color': 'green', 0: 2, 1: 4, 2: 'a', 3: 'b', 'shape': 'trapezoid', 4: 4}

    >>> array1 = Array()
    >>> array2 = Array({1: "data"})
    >>> php_array_merge(array1, array2)
    {0: 'data'}

    >>> beginning = 'foo'
    >>> end = Array({1: 'bar'})
    >>> php_array_merge(beginning, end)
    {0: 'foo', 1: 'bar'}
    """
    if len(args) == 0:
        return args

    out = Array()
    for arr in args:
        out.extend(arr)
    return out


def php_array_merge_recursive(*args):
    """
    >>> ar1 = Array({"color": Array({"favorite": "red"})}, 5)
    >>> ar2 = Array(10, {"color": Array({"favorite": "green"}, "blue")})
    >>> php_array_merge_recursive(ar1, ar2)
    >>> a = "{'color': {'favorite': {0: 'red', 1: 'green'}, 'blue'}, 0: 5, 1: 10}"
    """
    out = Array()
    for i in args:
        out.extend(i)
    # @@ TODO! implement function!


def php_array_pop(_array):
    """
    >>> stack = Array("orange", "banana", "apple", "raspberry")
    >>> php_array_pop(stack)
    'raspberry'
    >>> stack
    {0: 'orange', 1: 'banana', 2: 'apple'}
    """
    assert isinstance(_array, Array)
    return _array.pop()


def php_array_push(_array, *args):
    """
    >>> stack = Array("orange", "banana")
    >>> php_array_push(stack, "apple", "raspberry")
    >>> stack
    {0: 'orange', 1: 'banana', 2: 'apple', 3: 'raspberry'}
    """
    assert isinstance(_array, Array)
    _array.extend(args, _preserve=False)


def php_array_rand(_array, _num=1):
    """
    >>> input = Array("Neo", "Morpheus", "Trinity", "Cypher", "Tank")
    >>> a = php_array_rand(input, 2)
    >>> len(a) == 2
    True
    """
    out = Array()

    for i in range(_num):
        out.extend(_array[random.randrange(len(_array))])
    return out


def php_array_search(_needle, _haystack, _strict=False):
    """
    >>> array = Array({0: 'blue', 1: 'red', 2: 'green', 3: 'red'})
    >>> php_array_search('green', array)
    2
    >>> php_array_search('red', array)
    1
    >>> php_array_search('purple', array)
    False
    """
    if not _needle in _haystack.values():
        return False
    for k, v in _haystack.items():
        if v == _needle:
            return k
    return False  # should never reach this!


def php_array_shift(_array):
    """
    >>> stack = Array("orange", "banana", "apple", "raspberry")
    >>> php_array_shift(stack)
    'orange'
    >>> stack
    {0: 'banana', 1: 'apple', 2: 'raspberry'}
    """
    assert isinstance(_array, Array)
    return _array.shift()


def php_array_slice(_array, _offset, _length=None, _preserve=False):
    """
    >>> input = Array("a", "b", "c", "d", "e")
    >>> php_array_slice(input, 2)
    {0: 'c', 1: 'd', 2: 'e'}
    >>> php_array_slice(input, -2, 1)
    {0: 'd'}
    >>> php_array_slice(input, 0, 3)
    {0: 'a', 1: 'b', 2: 'c'}
    >>> php_array_slice(input, 2, -1)
    {0: 'c', 1: 'd'}
    >>> php_array_slice(input, 2, -1, True)
    {2: 'c', 3: 'd'}
    """
    assert isinstance(_array, Array)
    out = Array(_array.slice(_offset, _length, _preserve=_preserve),
                _preserve=_preserve)
    return out


def php_array_values(_array):
    """
    >>> array = Array({"size": "XL", "color": "gold"})
    >>> php_array_values(array)
    {0: 'XL', 1: 'gold'}
    """
    try:
        return Array(_array.values())
    except:
        return Array()


def php_base64_decode(_data, _strict=False):
    """
    >>> php_base64_decode('VGhpcyBpcyBhbiBlbmNvZGVkIHN0cmluZw==')
    'This is an encoded string'
    """
    return base64.b64decode(_data.encode('ascii')).decode('ascii')


def php_base64_encode(_data):
    """
    >>> php_base64_encode('This is an encoded string')
    'VGhpcyBpcyBhbiBlbmNvZGVkIHN0cmluZw=='
    """
    return base64.b64encode(_data.encode('ascii')).decode('ascii')


def php_basename(_path, _suffix=None):
    """
    >>> php_basename("/etc/sudoers.d", ".d")
    'sudoers'
    >>> php_basename("/etc/sudoers.d")
    'sudoers.d'
    >>> php_basename("/etc/passwd")
    'passwd'
    >>> php_basename("/etc/")
    'etc'
    >>> php_basename(".")
    '.'
    >>> php_basename("/")
    ''
    """
    if _path.endswith("/"):
        _path = _path[:-1]

    if not _suffix is None:
        pos = _path.rfind(_suffix)

        if pos != -1:
            _path = _path[:pos]
    return os.path.basename(_path)


def php_call_user_func(_fn, *args):
    if callable(_fn):
        return _fn(*args)

    if isinstance(_fn, Array):
        if not isinstance(_fn[0], str):
            fn = _fn[0]
            for it in _fn[1:]:
                fn = getattr(fn, it[1])
            return fn(*args)
        _fn = ".".join(_fn)

    if _fn.find(".") != -1:
        *klass, method = _fn.split(".")
        klass = "_".join(klass)
        fn = globals()[klass]
        return getattr(fn, method)(*args)
    else:
        fn = globals()[_fn]

    return fn(*args)


def php_chdir(_directory):
    """
    >>> php_chdir("/Users/nico")
    True
    >>> php_chdir("/Users/Idonotexists")
    False
    """
    try:
        os.chdir(_directory)
        return True
    except:
        return False


def php_class_exists(_class_name, _autoload=True):
    return _class_name in globals()  # @


def php_closedir(dh):
    dh = None


def php_count(item, _mode=COUNT_NORMAL):
    """
    >>> php_count(Array({0: 1, 1: 3, 2: 5}))
    3

    >>> php_count(Array({0: 7, 5: 9, 10: 11}))
    3

    >>> php_count(None)
    0

    >>> php_count(False)
    1

    >>> food = Array({'fruits': Array('orange', 'lemon', 'apple'), \
                'veggie': Array('carrot', 'collard', 'pea')})

    >>> php_count(food)
    2

    >>> php_count(food, COUNT_RECURSIVE);
    8
    """

    if item is None:
        return 0
    if isinstance(item, bool):
        return 1
    if _mode == COUNT_NORMAL:
        return len(item)

    cnt = 0
    for k, v in item.items():
        if isinstance(k, str):
            cnt += 1
        cnt += php_count(v) if isinstance(v, Array) else 1
    return cnt


def php_dirname(_path, _levels=1):
    """
    >>> php_dirname("/etc/passwd")
    '/etc'
    >>> php_dirname("/etc/")
    '/'
    >>> php_dirname(".")
    '.'
    >>> php_dirname("/usr/local/lib", 2)
    '/usr'
    """
    if _path == ".":
        return "."

    if _path.endswith("/"):
        _path = _path[:-1]

    parts = _path.split("/")

    if len(parts) == 1:
        return "/"

    rs = "/".join(parts[:len(parts) - _levels])
    if rs == "":
        return "/"
    return rs


def php_dl(_library):
    raise Exception("[-] The function *dl()* cannot be used in Python!")


def php_end(_array):
    """
    >>> a = Array(1, 2, 3, 4, 5)
    >>> php_end(a)
    5
    >>> a = Array({'fruit': 'orange', 'color': 'blue'})
    >>> php_end(a)
    'blue'
    """
    return _array.end()


def php_error_log(_message,
                  _message_type=0,
                  _destination=None,
                  _extra_headers=None):
    pass


def php_error_reporting(_level):
    pass


def php_explode(_delimiter, _string, _limit=-1):
    """
    >>> pizza = "piece1 piece2 piece3 piece4 piece5 piece6"
    >>> pieces = php_explode(" ", pizza)
    >>> pieces[0]
    'piece1'
    >>> pieces[1]
    'piece2'

    >>> data = "foo:*:1023:1000::/home/foo:/bin/sh"
    >>> user, pass_, uid, gid, gecos, home, shell = php_explode(":", data)
    >>> user
    'foo'
    >>> pass_
    '*'

    >>> php_explode(',', "hello")
    {0: 'hello'}
    >>> php_explode(',', "hello,there")
    {0: 'hello', 1: 'there'}
    >>> php_explode(',', ',')
    {0: '', 1: ''}
    """
    return Array(_string.split(_delimiter, _limit))


def php_extension_loaded(_name):
    enabled = ["mysqli", "dom", "mbstring"]
    return _name.lower().strip() in enabled


def php_fclose(_handle):
    _handle.close()


def php_feof(_handle):
    oldpos = _handle.tell()
    _handle.seek(0, 2)
    is_eof = oldpos == _handle.tell()
    _handle.seek(oldpos, 0)
    return is_eof


def php_fflush(_handle):
    _handle.flush()


def php_fgets(_handle, _length=None):
    return _handle.read(_length)


def php_file_exists(_filename):
    return os.path.exists(fix_ext(_filename))


def php_file_get_contents(_filename,
                          _use_include_path=False,
                          _context=None,
                          _offset=0,
                          _maxlen=None):
    # TODO: finish this!
    with open(_filename, "r") as f:
        return f.read()


def php_function_exists(_function_name):
    return _function_name in globals() or f"php_{_function_name}" in globals()


def php_gc_enabled():
    return True


def php_getcwd():
    return os.getcwd()


def php_getenv(_varname, _local_only=False):
    return os.getenv(_varname)


def php_header(_header, _replace=True, _http_response_code=None):
    assert _replace == True

    k, *v = _header.split(":")
    v = ":".join(v).strip()

    if k.lower() == "location":
        if v.endswith(".php"):
            v = v[:-4] + ".py"

    _HEADERS[k] = v


def php_header_remove(_name):
    if _name in _HEADERS:
        del _HEADERS[_name]


def php_headers_sent(_file=None, _line=None):
    return _HEADERS_PRINTED


def php_implode(*args):
    """
    >>> array = Array('lastname', 'email', 'phone')
    >>> php_implode(",", array)
    'lastname,email,phone'

    >>> php_implode('hello', Array())
    ''
    """
    if len(args) == 1:
        assert isinstance(args, list)
        return "".join(args)

    assert len(args) == 2
    assert (isinstance(args[0], str) and isinstance(args[1], Array)) or \
        (isinstance(args[1], str) and isinstance(args[0], Array))

    _glue = args[0] if isinstance(args[0], str) else args[1]
    _array = args[1] if isinstance(args[1], Array) else args[0]
    return _glue.join([str(x) for x in _array.values()])


def php_in_array(_needle, _haystack, _strict=False):
    """
    >>> os = Array("Mac", "NT", "Irix", "Linux")
    >>> php_in_array("Irix", os)
    True
    >>> php_in_array("mac", os)
    False

    >>> a = Array('1.10', 12.4, 1.13)
    >>> php_in_array('12.4', a, True)
    False
    >>> php_in_array('12.4', a)
    True
    >>> php_in_array(1.13, a, True)
    True
    """

    if not _strict:
        return str(_needle) in [str(x) for x in _haystack.values()]
    return _needle in _haystack


def php_ini_get(_varname):
    return _PHP_INI_FILE.get(_varname, "")


def php_ini_get_all(_extension=None, _details=True):
    if _details:
        return _PHP_INI_FILE_DETAILS
    return _PHP_INI_FILE


def php_ini_set(_varname, _newvalue):
    _PHP_INI_FILE[_varname] = _newvalue


def php_intval(_var, _base=10):
    return int(str(_var), _base)


def php_is_a(_object, _class_name, _allow_string=False):
    return type(_object).__name__ == _class_name  # @


def php_is_array(_var):
    return isinstance(_var, Array)


def php_is_bool(_var):
    return isinstance(_var, bool)


def php_is_callable(_var, _syntax_only=False, _callable_name=None):
    if isinstance(_var, str):
        try:
            _var = globals()[_var]
        except:
            return False
    return callable(_var)


def php_is_dir(_filename):
    return os.path.isdir(_filename)


def php_is_file(_filename):
    return os.path.isfile(_filename)


def php_is_float(_var):
    return isinstance(_var, float)


def php_is_int(_var):
    return isinstance(_var, int)


def php_is_link(_filename):
    return os.path.islink(_filename)


def php_is_null(_var):
    return _var is None


def php_is_numeric(_var):
    return isinstance(_var, int) or isinstance(_var, float)


def php_is_resource(_var):
    return isinstance(_var, Resource)


def php_is_object(_var):
    return isinstance(_var, type)


def php_is_readable(_filename):
    return os.access(_filename, os.R_OK)


def php_is_string(_var):
    return isinstance(_var, str)


def php_is_writable(_filename):
    return os.access(_filename, os.W_OK)


def php_json_decode(_json, _assoc=False, _depth=512, _options=0):
    """
    >>> php_json_decode('{"a":1,"b":2,"c":3,"d":4,"e":5}')
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    >>> php_json_decode("{ 'bar': 'baz' }")

    """
    try:
        data = json.loads(_json)
        php_json_last_error.value = None
        return data
    except json.JSONDecodeError as err:
        php_json_last_error.value = err
        return None


def php_json_encode(_value, _options=0, _depth=512):
    """
    >>> php_json_encode({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
    '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
    >>> php_json_encode(Array({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}))
    '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'
    """
    try:
        data = json.dumps(_value.data if isinstance(_value, Array) else _value)
        php_json_last_error.value = None
        return data
    except json.JSONDecodeError as err:
        php_json_last_error.value = err
        return False

# TODO: Convert JSON errors to PHP constants


def php_json_last_error():
    if hasattr(php_json_last_error, 'value'):
        return php_json_last_error.value
    return JSON_ERROR_NONE


def php_ltrim(_str, _character_mask=None):
    return _str.lstrip()


def php_max(_values, *args):
    """
    >> php_max(2, 3, 1, 6, 7)
    7
    >> php_max(Array(2, 4, 5))
    5

    >> php_max(0, 'hello')
    0
    >> php_max('hello', 0)
    0

    # TODO: finish implementing this!
    php_max('hello', -1) => 'hello'

    // With multiple arrays of different lengths, max returns the longest
    $val = max(array(2, 2, 2), array(1, 1, 1, 1)); // array(1, 1, 1, 1)
    // Multiple arrays of the same length are compared from left to right
    // so in our example: 2 == 2, but 5 > 4
    $val = max(array(2, 4, 8), array(2, 5, 1)); // array(2, 5, 1)

    // If both an array and non-array are given, the array will be returned
    // as comparisons treat arrays as greater than any other value
    $val = max('string', array(2, 5, 7), 42);   // array(2, 5, 7)

    // If one argument is None or a boolean, it will be compared against
    // other values using the rule FALSE < TRUE regardless of the other types involved
    // In the below example, -10 is treated as TRUE in the comparison
    $val = max(-10, FALSE); // -10

    // 0, on the other hand, is treated as FALSE, so is "lower than" TRUE
    $val = max(0, TRUE); // TRUE
    """
    if isinstance(_values, Array):
        if len(_values) == 0:
            return False
        return max(_values)
    #print(">>>>",tuple([_values, args]), type(_values).__name__)
    #print(args, type(args).__name__)
    return max(tuple([_values, args]))


def php_mb_stripos(_haystack, _needle, _offset=0, _encoding="UTF-8"):
    return _haystack.find(_needle)  # TODO: check!


def php_mb_strlen(_str, _encoding="UTF-8"):
    return len(_str)


def php_mb_strtolower(_str, _encoding="UTF-8"):
    return _str.lower()


def php_mb_substr(_str, _start, _length=0, _encoding="UTF-8"):
    return _str[_start:_start + _length]


def php_md5(_str, _raw_output=False):
    m = hashlib.md5()
    m.update(_str.encode("utf-8"))
    return m.hexdigest()


def php_md5_file(_filename, _raw_output=False):
    with open(_filename, encoding="utf-8") as f:
        return php_md5(f.read())


def php_method_exists(_object, _method_name):
    return hasattr(_object, _method_name) and callable(
        getattr(_object, _method_name))


def php_microtime(_get_as_float=False):
    return int(datetime.now().timestamp() * 1000)


def php_min(_values, _value1, *args):
    return min(_values, _value1)


def php_mysqli_real_connect(dbh_,
                            host_,
                            username_,
                            passwd_,
                            dbname_,
                            port_=None,
                            socket_=None,
                            flags_=None):
    try:
        dbh_.cnx = php_mysqli_connect(host_, username_, passwd_, dbname_)
        dbh_.connect_errno = 0

        return True
    except:
        return False


def php_mysqli_init():
    dbh = Resource()
    for it in ['affected_rows', 'connect_errno', 'connect_error', 'errno', 'error_list', 'error', 'field_count',
               'client_info', 'client_version', 'host_info', 'protocol_version', 'server_info', 'server_version',
               'info', 'insert_id', 'sqlstate', 'thread_id', 'warning_count']:
        setattr(dbh, it, None)
    return dbh


def php_mysqli_connect(host, user, pwd, db):
    return mysql.connector.connect(host=host,
                                   user=user,
                                   passwd=pwd,
                                   database=db)


def php_opendir(_path, _context=None):
    dh = Resource()
    dh.path = _path
    dh.context = _context
    dh.files = os.listdir(_path)
    dh.pos = 0
    return dh


def php_ord(_string):
    return ord(_string)


def php_parse_url(_url, _component=-1):
    o = urlparse(_url)
    parts = {
        "scheme": o.scheme,
        "host": o.hostname,
        "port": o.port,
        "user": o.username,
        "pass": o.password,
        "path": o.path,
        "query": o.query,
        "fragment": o.fragment
    }

    if _component == -1:
        return parts

    return parts.get(_component, None)


def php_php_sapi_name():
    return ""


def php_phpversion(_extension=None):
    return "7.4.5"


def _get_pattern(p):
    sep = p[0]
    last = p.rfind(sep)
    return p[1:last]


def php_preg_match(_pattern, _subject, _matches=None, _flags=0, _offset=0):
    if _subject is None:
        return None
    return re.match(_get_pattern(_pattern), _subject)


def php_preg_replace(_pattern, _replacement, _subject, _limit=0, _count=None):
    assert _count is None
    return re.sub(_get_pattern(_pattern), _replacement, _subject, _limit)


def php_preg_split(_pattern, _subject, _limit=-1, _flags=0):
    return re.split(_get_pattern(_pattern), _subject)


def php_prev(_array):
    assert isinstance(_array, Array)
    return _array.prev()


def php_end(_array):
    assert isinstance(_array, Array)
    return _array.end()


def php_readdir(dh):
    try:
        fname = dh.files[dh.pos]
        dh.pos += 1
        return fname
    except:
        return False


def php_realpath(_path):
    return os.path.realpath(_path)


def php_rtrim(_str, _character_mask=None):
    return _str.rstrip()


def php_spl_autoload_unregister(_fn, _throw=True, _prepend=False):
    global _AUTOLOAD_FN

    for fn in _AUTOLOAD_FN:
        if fn == _fn:
            del _AUTOLOAD_FN[fn]
            break


def php_spl_autoload_register(_fn, _throw=True, _prepend=False):
    global _AUTOLOAD_FN

    if isinstance(_fn, str):
        _AUTOLOAD_FN.append(_fn)
    elif type(_fn).__name__ == "Array":
        _AUTOLOAD_FN.append(".".join(_fn.get_list()))
    elif callable(_fn):
        _AUTOLOAD_FN.append(_fn)
    else:
        assert False, "[-] Invalid type for autoload function!"


def php_sprintf(_format, *args):
    """
    >>> num = 5
    >>> location = 'tree'
    >>> php_sprintf('There are %d monkeys in the %s', num, location)
    'There are 5 monkeys in the tree'
    >>> php_sprintf('The %2$s contains %1$d monkeys', num, location)
    'The tree contains 5 monkeys'
    >>> php_sprintf('''%'.9d''', 123)
    '......123'
    >>> php_sprintf('''%'09d''', 123)
    '000000123'
    >>> php_sprintf('The %2$s contains %1$04d monkeys', num, location)
    'The tree contains 0005 monkeys'
    >>> money = 68.75 + 54.35
    >>> php_sprintf('%01.2f', money)
    '123.10'
    """

    def _fix(m):
        n = m.group('argnum') or ''
        w = m.group('width') or ''
        f = m.group('flags') or ''
        fc = m.group('fillchar') or ' '
        fc = fc[1:]

        p = m.group('precision') or ''
        s = m.group('spec') or ''
        if len(p) > 0:
            p = '.' + p
        sign = ''
        align = ''

        if f == '-':
            align = '<'
        else:
            sign = f

        if fc != '' and align == '':
            align = '>'

        fspec = f'{fc}{align}{sign}{w}{p}{s}'
        if len(fspec) > 0:
            fspec = ':' + fspec

        if len(n) > 0:
            n = str(int(n) - 1)
        if s == 's':  #  if string is specified, convert to string!
            return f'{{{n}!s{fspec}}}'
        return f'{{{n}{fspec}}}'

    _format = re.sub(
        '%(?P<argnum>\d+)?\$?(?P<flags>[-+0])?(?P<fillchar>\'[\w\.])?(?P<width>\d+)?\.?(?P<precision>\d+)?(?P<spec>[%bcdeEfFgGosuxX])', _fix, _format)

    return _format.format(*args)


def php_vsprintf(fmt, args):
    return php_sprintf(fmt, *args)


def php_stripos(_haystack, _needle, _offset=0):
    return _haystack.find(_needle)


def php_str_ireplace(_search, _replace, _subject, _count):
    assert False
    return _subject.replace(_search, _replace)


def php_stristr(_haystack, _needle, _before_needle=False):
    assert False
    return _haystack.find(_needle)


def php_strlen(_string):
    return len(_string)


def php_str_pad(_input, _pad_length, _pad_char=' ', _pad_type=STR_PAD_RIGHT):
    """
    """
    if len(_input) <= _pad_length:
        return _input

    if _pad_type == STR_PAD_RIGHT:
        return _input.ljust(_pad_length, _pad_char)
    elif _pad_type == STR_PAD_LEFT:
        return _input.rjust(_pad_length, _pad_char)
    return _input.center(_pad_length, _pad_char)


def php_strpos(_haystack, _needle, _offset=0):
    """
    >>> php_strpos('abc', 'a');
    0
    >>> newstring = 'abcdef abcdef'
    >>> php_strpos(newstring, 'a', 1)
    7
    """
    pos = _haystack.find(_needle, _offset)
    if pos == -1:
        return False
    return pos


def php_str_repeat(_input, _multiplier):
    """
    >>> php_str_repeat('*', 10)
    '**********'
    >>> php_str_repeat('xyz', 3)
    'xyzxyzxyz'
    >>> php_str_repeat('xyz', 0)
    ''
    """
    return _input * _multiplier


def php_str_replace(_search, _replace, _subject, _count=None):
    """
    >>> php_str_replace("%body%", "black", "<body text='%body%'>")
    "<body text='black'>"

    >>> vowels = Array("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
    >>> php_str_replace(vowels, "", "Hello World of PHP")
    'Hll Wrld f PHP'

    >>> phrase  = "You should eat fruits, vegetables, and fiber every day."
    >>> healthy = Array("fruits", "vegetables", "fiber")
    >>> yummy   = Array("pizza", "beer", "ice cream")
    >>> php_str_replace(healthy, yummy, phrase)
    'You should eat pizza, beer, and ice cream every day.'
    """
    assert _count is None or isinstance(
        _count, Array), '_count parameter should be an Array!'

    if _count is not None:
        _count[0] = len(list(re.findall(_search, _subject)))

    if not isinstance(_search, Array):
        return _subject.replace(_search, _replace)

    if isinstance(_replace, Array):
        for sr, rp in zip(_search, _replace):
            _subject = _subject.replace(sr, rp)
        return _subject
    else:
        for sr in _search:
            _subject = _subject.replace(sr, _replace)
        return _subject


def php_strrev(_string):
    """
    >>> php_strrev('Hello world!')
    '!dlrow olleH'
    """
    return _string[::-1]


def php_strripos(_haystack, _needle, _offset=0):
    """
    >>> php_strripos('ababcd', 'aB')
    2
    >>> php_strripos('ababcd', 'axx')
    False
    """
    pos = _haystack.lower().rfind(_needle.lower(), _offset)

    if pos == -1:
        return False
    return pos


def php_strrpos(_haystack, _needle, _offset=0):
    assert False
    return _haystack.find(_needle)


def php_strstr(_haystack, _needle, _before_needle=False):
    assert False
    pos = _haystack.find(_needle)

    if pos == -1:
        return _haystack

    if _before_needle:
        return _haystack[:pos]
    else:
        return _haystack[pos:]


def php_strtolower(_string):
    assert isinstance(_string, str)
    return _string.lower()


def php_strtoupper(_string):
    assert isinstance(_string, str)
    return _string.upper()


def php_strtr(_str, *args):
    assert False
    return _str


def php_strval(_var):
    """
    >>> php_strval(True)
    '1'
    >>> php_strval(False)
    ''
    >>> php_strval(Array(1, 2, 3))
    'Array'
    >>> php_strval(12.4)
    '12.4'
    >>> php_strval(None)
    ''
    """
    if isinstance(_var, bool):
        return '1' if _var else ''
    if isinstance(_var, Array):
        return 'Array'
    if _var is None:
        return ''
    return str(_var)


def php_substr(_string, _start, _length=None):
    """
    >>> php_substr("abcdef", -1)
    'f'
    >>> php_substr("abcdef", -2)
    'ef'
    >>> php_substr("abcdef", -3, 1)
    'd'
    >>> php_substr("abcdef", 0, -1)
    'abcde'
    >>> php_substr("abcdef", 2, -1);
    'cde'
    >>> php_substr("abcdef", 4, -4);
    False
    >>> php_substr("abcdef", -3, -1);
    'de'
    >>> php_substr('a', 2)
    False
    """
    if not isinstance(_string, str):
        return False

    if _string == "":
        return False

    if _length is None:
        if _start > len(_string):
            return False
        return _string[_start:]

    if _start < 0 and _length > 0:
        _length = _start + _length
    r = _string[_start:_length]

    if r == "":
        return False
    return r


def php_substr_count(_haystack, _needle, _offset=0, _length=None):
    """
    >>> text = 'This is a test'
    >>> php_strlen(text)
    14
    >>> php_substr_count(text, 'is')
    2
    >>> php_substr_count(text, 'is', 3)
    1
    >>> php_substr_count(text, 'is', 3, 3)
    0
    >>> php_substr_count(text, 'is', 5, 10)
    1
    >>> php_substr_count('gcdgcdgcd', 'gcdgcd')
    1
    """
    if _length is None:
        _length = len(_haystack)
    return _haystack.count(_needle, _offset, _offset + _length)


def php_substr_replace(_string, _replacement, _start, _length):
    assert False
    return _string


def php_sys_get_temp_dir():
    return tempfile.gettempdir()


def php_tempnam(_dir, _prefix):
    fh, fpath = tempfile.mkstemp(prefix=_prefix, dir=_dir)
    fh.close()
    return fpath


def php_trim(_str, _character_mask=" \t\n\r\0\x0B"):
    """
    >>> a = r"  \ttesting \t    "
    >>> php_trim(a)
    'testing'
    """

    start = 0
    end_ = len(_str) - 1
    chars = [x for x in _character_mask]

    while True:
        if _str[start] in chars:
            start += 1
            continue
        break

    while True:
        if _str[end_] in chars:
            end_ -= 1
            continue
        end_ += 1
        break

    return _str[start:end_]


def php_zend_version():
    return "3.4.0"


def stream_get_transports():
    return Array("tcp", "udp", "unix", "udg", "ssl", "tls", "tlsv1.0",
                 "tlsv1.1", "tlsv1.2")


def php_version_compare(_v1, _v2, _operator=None):
    """
    php_version_compare('1', '1.0') => -1 got: 0
    php_version_compare('1.0', '1.0.0') =>  -1 got: 0

    >>> php_version_compare('1.0', '1.1')
    -1
    >>> php_version_compare('1.0.0', '1.0.00')
    0
    >>> php_version_compare('7.3', '7.3.5')
    -1
    >>> php_version_compare('2', '1.19')
    1
    """

    v1 = version.parse(_v1)
    v2 = version.parse(_v2)

    if _operator is None:
        if v1 == v2:
            return 0

        if v1 < v2:
            return -1

        if v1 > v2:
            return 1

    _operator = _operator.lower().strip()

    if _operator in ['<', 'lt']:
        return v1 < v2

    if _operator in ['<=', 'le']:
        return v1 <= v2

    if _operator in ['>', 'gt']:
        return v1 > v2

    if _operator in ['>=', 'ge']:
        return v1 >= v2

    if _operator in ['=', '==', 'eq']:
        return v1 == v2

    if _operator in ['!=', '<>', 'ne']:
        return v1 != v2

    assert False, 'should not reach this code!'


def php_func_get_arg(_arg_num):
    parent = _get_caller_data()
    varname = parent.args_name[_arg_num]
    return parent.locals[varname]


def php_func_get_args():
    parent = _get_caller_data()
    return parent.args_name


def php_func_num_args():
    parent = _get_caller_data()
    return parent.num_args


def _get_caller_data():

    frame = inspect.currentframe().f_back.f_back
    fcode = frame.f_code
    CallerInfo = namedtuple(
        'CallerInfo', 'name, num_args, args_name, locals, globals')
    return CallerInfo(name=fcode.co_name,
                      num_args=fcode.co_argcount,
                      args_name=Array(fcode.co_varnames[:fcode.co_argcount]),
                      locals=Array(frame.f_locals),
                      globals=Array(frame.f_globals))


def php_register_shutdown_function(_callback, *args):

    if callable(_callback):
        atexit.register(_callback)
        return

    if isinstance(_callback, str):
        fn = globals()[_callback]
        atexit.register(fn)
        return

    if isinstance(_callback, Array):
        # parts of a static method!
        # print(type(_callback).__name__)
        # print(_callback)
        """
$scheduler->registerShutdownEvent(array($scheduler, 'dynamicTest'));
// try with a static call:
$scheduler->registerShutdownEvent('scheduler::staticTest');
        """
        return  # TODO: finish this!

    assert False, 'wrong turn!'


def php_date_default_timezone_get():
    pass


def php_date_default_timezone_set(_timezone_identifier):
    pass


def php_strncmp(s1, s2, l):
    """
    >>> php_strncmp('phpaaa', 'php', 6)
    1
    >>> php_strncmp('aapaaa', 'php', 6)
    -1
    >>> php_strncmp('abcdef', 'abcdaa', 3)
    0
    """
    _s1 = s1[:l]
    _s2 = s2[:l]

    if _s1 < _s2:
        return -1

    if _s1 > _s2:
        return 1

    return 0


def php_bool(v):
    pass


def php_float(v):
    return float(v)


def php_int(v, base=10):
    """
    >>> php_int(42)
    42
    >>> php_int(4.2)
    4
    >>> php_int('42')
    42
    >>> php_int('+42')
    42
    >>> php_int('-42')
    -42
    >>> php_int('042')
    42
    >>> php_int(0x1A)
    26
    >>> php_int(42000000)
    42000000
    >>> php_int(42, 8)
    42
    >>> php_int('42', 8)
    34
    >>> php_int(Array())
    0
    >>> php_int(Array('foo', 'bar'))
    1
    >>> php_int(False)
    0
    >>> php_int(True)
    1

    php_int(042) => 34
    php_int('1e10'); => 1
    # TODO: handle overflow!
    php_int(420000000000000000000) => 0
    php_int('420000000000000000000') => 2147483647
    """
    if isinstance(v, bool):
        return 1 if v else 0
    if isinstance(v, Array):
        return 0 if len(v) == 0 else 1

    if base != 10:
        if not isinstance(v, str):
            return int(v)
        return int(v, base)

    try:
        return int(v)
    except:
        return int(''.join([x for x in str(v) if not x.isalpha()]))


def php_str(v):
    return str(v)


def php_random_int():
    assert False, "Not Implemented!"


def php_sodium_crypto_box():
    assert False, "Not Implemented!"


def php_compact(*names):
    """
    >>> city = 'San Francisco'
    >>> state = 'CA'
    >>> event = 'SIGGRAPH'
    >>> location_vars = Array('city', 'state')
    >>> php_compact('event', location_vars)
    {'event': 'SIGGRAPH', 'city': 'San Francisco', 'state': 'CA'}
    """

    def _item(x):
        if isinstance(x, (Array, dict)):
            return x.values()
        return [x]

    caller = inspect.stack()[1][0]  # caller of compact()
    vars = {}
    arr = list(itertools.chain.from_iterable([_item(x) for x in names]))
    for n in arr:
        k = n[:-1] if n.endswith('_') else n
        if n in caller.f_locals:
            vars[k] = caller.f_locals[n]
        elif n in caller.f_globals:
            vars[k] = caller.f_globals[n]
    return vars


def _execdb(db, sql, all=True, with_data=True):
    r = db.cnx.cursor()
    r.execute(sql)
    data = None
    if with_data:
        data = r.fetchall() if all else r.fetchone()
    r.close()
    return data


def _check_db_is_connected(dbh):
    assert hasattr(
        dbh, 'cnx') and dbh.cnx is not None, 'Not connected to database!'


def php_mysqli_ping(dbh):
    try:
        php_mysqli_get_server_info()
        return True
    except:
        return False


mysqli_ping = php_mysqli_ping


def php_mysqli_error(dbh):
    return 'Some error!' if dbh.connect_errno != 0 else ''


mysqli_error = php_mysqli_error


def php_mysqli_get_server_info(dbh):
    _check_db_is_connected(dbh)

    dbh.server_info = _execdb(dbh, 'SELECT VERSION()', False)[0]
    return dbh.server_info


class MySQLResult(Traversable):
    def __init__(self, cursor):
        self.cursor = cursor
        self.current_field = None
        self.field_count = None
        # array $lengths;

    @property
    def num_rows(self):
        # count!
        return 1

    # data_seek ( int $offset ) : bool
    # fetch_all ([ int $resulttype = MYSQLI_NUM ] ) : mixed
    # fetch_array ([ int $resulttype = MYSQLI_BOTH ] ) : mixed
    # fetch_assoc ( void ) : array
    # fetch_field_direct ( int $fieldnr ) : object
    # fetch_field ( void ) : object
    # fetch_fields ( void ) : array
    # fetch_object ([ string $class_name = "stdClass" [, array $params ]] ) : object
    # fetch_row ( void ) : mixed
    # field_seek ( int $fieldnr ) : bool
    # free ( void ) : void


def php_mysqli_query(dbh, sql):
    """
    Returns FALSE on failure. For successful SELECT, SHOW, DESCRIBE or EXPLAIN queries mysqli_query() will return a mysqli_result object. For other successful queries mysqli_query() will return TRUE.
    """
    _check_db_is_connected(dbh)
    
    try:
        cursor = dbh.cnx.cursor()
        cursor.execute(sql)
        return MySQLResult(cursor)
    except:
        return False


def php_mysqli_fetch_array(r):
    return r.cursor.fetchone()


def php_mysqli_select_db(dbh, db):
    _check_db_is_connected(dbh)
    _execdb(dbh, f'USE {db}', with_data=False)
    return True


def php_mysqli_free_result(r):
    assert isinstance(r, MySQLResult)
    r.cursor.close()


def php_is_scalar(v):
    if v is None:
        return False
    return isinstance(v, (int, float, str, bool))


def preg_match_all(pattern, subject, matches, flags=None, offset=0):
    """
    string $pattern , string $subject [, array &$matches [, int $flags = PREG_PATTERN_ORDER [, int $offset = 0 ]]] ) : int
    string $pattern , string $subject [, array &$matches [, int $flags = PREG_PATTERN_ORDER [, int $offset = 0 ]]] ) : int
    """
    assert isinstance(matches, Array), 'parameter matches must be an Array!'

    m = re.findall(pattern, subject)

    for it in m:
        matches[-1] = it

    return len(m)


def php_array_walk(arr, fn, user_data=None):
    if not php_is_array(arr):
        arr = Array(arr)

    for k, v in arr.items():
        if user_data:
            php_call_user_func(fn, v, user_data)
        else:
            php_call_user_func(fn, v)


def php_mysqli_real_escape_string(dbh, s):
    return dbh.cnx._cmysql.escape_string(s).decode('utf-8')


def php_uniqid(prefix=None, more_entropy=False):
    data = str(uuid.uuid4()).replace('-', '')

    if prefix is None:
        return data[:13]

    if more_entropy:
        return data[:23]

    return data


def php_hash_hmac_algos():
    return Array('md5', 'sha1')


def php_hash_hmac(algo, data, key, raw_output_=None, *_args_):
    if raw_output_ is None:
        raw_output_ = False

    m = hmac.new(key.encode('ascii'), digestmod=getattr(
        hashlib, algo.lower().strip()))
    m.update(data.encode('ascii'))

    if raw_output_:
        return m.digest()

    data = m.hexdigest()
    return data


def php_shell_exec(_cmd):
    """
    >>> php_shell_exec('true')
    ''
    >>> php_shell_exec('echo 42')
    '42'
    >>> php_shell_exec('false')
    False
    """
    out = Array()
    code = Array()
    php_exec(_cmd, out, code, shell=True)
    if int(code[0]) != 0:
        return False

    return "\n".join(out.values())


def php_exec(cmd, out=None, exitcode=None, shell=False):
    proc = subprocess.run(cmd, check=False, text=True,
                          shell=shell, stdout=subprocess.PIPE)
    lines = proc.stdout.strip().split('\n')

    if isinstance(out, Array):
        for it in lines:
            out[-1] = it

    if exitcode is not None:
        assert isinstance(
            exitcode, Array), 'exitcode should be an array in Python! FIX THIS!'
        exitcode[-1] = proc.returncode

    return lines[-1]


def php_ksort(arr, flags=None):
    """
    >>> fruits = Array({'d': 'lemon', "a": "orange", "b": "banana", "c": "apple"})
    >>> php_ksort(fruits)
    True
    >>> fruits
    {'a': 'orange', 'b': 'banana', 'c': 'apple', 'd': 'lemon'}
    """
    tmp = Array()
    for it in sorted(arr.get_keys()):
        tmp[it] = arr[it]
        del arr[it]

    for k, v in tmp.items():
        arr[k] = v
    return True


def php_debug_backtrace(*args):
    return Array()


def php_join(s, arr):
    return s.join(arr)


def php_array_reverse(_array, _preserve_keys=False):
    return _array  # TODO: Fix!


def php_htmlspecialchars(s, *args):
    """
    >>> php_htmlspecialchars("<a href='test'>Test</a>", ENT_QUOTES)
    '&lt;a href=&#x27;test&#x27;&gt;Test&lt;/a&gt;'
    """
    return html.escape(s, quote=True)


def php_printf(fmt, *args):
    php_print(php_sprintf(fmt, *args))


def php_preg_replace_callback(pattern, callback, subject, limit=-1, count=None):
    """
    >>> s = 'This is a Test String!'
    >>> php_preg_replace_callback('\\s', lambda m: 'X', s)
    'ThisXisXaXTestXString!'

    TODO: limit and count parameters!
    """
    return re.sub(pattern, lambda m: php_call_user_func(callback, m), subject)

fullpath = os.path.realpath

def php_session_name(name=None):
    global _PHP_SESSION_INFO

    old_name = _PHP_SESSION_INFO['name']    

    if name is not None:
        assert not _HEADERS_PRINTED, 'Headers already sent! cannot change them at this point'
        _PHP_SESSION_INFO['name'] = name
    return old_name
session_name = php_session_name

def php_session_start(*args):
    global _PHP_SESSION_INFO

    if not _PHP_SESSION_INFO['id']:
        _PHP_SESSION_INFO['id'] = php_uniqid()

    # TODO: create or restore session here!

    # TODO: add lifetime to the cookie => _PHP_SESSION_INFO['lifetime'] = lifetime

    tmp = []
        
    if _PHP_SESSION_INFO["path"]:
        tmp.append(f'Path={_PHP_SESSION_INFO["path"]}')

    if _PHP_SESSION_INFO["domain"]:
        tmp.append(f'Domain={_PHP_SESSION_INFO["domain"]}')

    if _PHP_SESSION_INFO["secure"]:
        tmp.append(f'Secure')

    if _PHP_SESSION_INFO["httponly"]:
        tmp.append(f'httponly')
    
    _HEADERS['Set-Cookie'] = f'{_PHP_SESSION_INFO["name"]}={";".join(tmp)}'
session_start = php_session_start


def php_session_set_cookie_params(lifetime, _path=None, domain=None, secure=False, httponly=False):
    if php_is_array(lifetime):
        path = lifetime.get('path', None)
        domain = lifetime.get('domain', None)
        secure = lifetime.get('secure', False)
        httponly = lifetime.get('httponly', False)
        lifetime = lifetime.get('lifetime', 600)


    _PHP_SESSION_INFO['lifetime'] = lifetime

    if _path:
        _PHP_SESSION_INFO['path'] = _path

    if domain:
        _PHP_SESSION_INFO['domain'] = domain 

    if secure:
        _PHP_SESSION_INFO['secure'] = secure

    if httponly:
        _PHP_SESSION_INFO['httponly'] = httponly
    return True
session_set_cookie_params = php_session_set_cookie_params

def php_unset(fn_del):
    try:
        fn_del()
    except:
        pass

# ========================================================================================


defs = locals().copy()
PHP_FUNCTIONS = [
    k[4:] for k, v in defs.items() if callable(v) and k.startswith("php_")
]
