# coding: utf8

import io
import os
import os.path
import cgi
import sys
import re
import inspect
import mysql.connector
import hashlib

from datetime import datetime
from urllib.parse import urlparse

__DIR__ = os.getcwd()
_HEADERS = {}
_HEADERS_PRINTED = False
_AUTOLOAD_FN = None

_PHP_INI_FILE = {
        "max_execution_time": "36000",
        "memory_limit": "6000000",
        "allow_url_fopen": "False", 
        "safe_mode": "True",
        "upload_tmp_dir": "/tmp",
        "open_basedir": "", 
        "disable_functions": "",
        "upload_max_filesize": "1000000000", 
        "post_max_size": "1000000000",
        "sendmail_path": "",
        "sendmail_from": "", 
        "zlib.output_compression": "False",
        "output_handler": "",
        "error_reporting": "",
        "error_log": "",
        "user_agent": "",
        "disable_classes": "", 
        "register_globals": "False"
        }

def php_empty(var_):
    if callable(var_):
        try:
            var_ = var_()
        except:
            return True
    if var_ is None:
        return True
    if type(var_).__name__ == "Array" or isinstance(var_, str):
        return len(var_) == 0
    return False

def php_get_locals(locals_, *args):
    return [locals_[x] for x in args]

def fix_ext(fname):
    filename, ext = os.path.splitext(fname)

    if ext.lower().strip() == ".php":
        return f"{filename}.py"
    return fname

def php_include_file(fname, redirect=False):
    global __DIR__
    
    filename = fix_ext(fname)
    
    with open(filename) as src:
        code = compile(src.read().replace("\x00", ""), filename, "exec")

    old_dir = __DIR__
    __DIR__ = os.path.dirname(os.path.realpath(filename))

    try:
        if redirect:
            f = io.StringIO()
            with redirect_stdout(f):
                exec(code, globals(), globals())
            return f.getvalue()
    
        exec(code, globals(), globals())
    except SystemExit as e:
        if e.code != -1:
            raise e
    finally:
        __DIR__ = old_dir

# -----------------------------------------------------------------------------------
# PHP globals

class Array():
    def __init__(self, *items):
        self.data = {}
        self.pos = None
        self.keys = None
        self.push(*items)

    def push(self, *items):
        for item in items:
            if hasattr(item, "items"):
                for k, v in item.items():
                    self.data.update(item.items())
            elif isinstance(item, list):
                for v in item:
                    self.data[self.get_next_idx()] = v
            else:
                self.data[self.get_next_idx()] = item

    def __getitem__(self, k):
        if not k in self.data:
            self.data[k] = Array()
        return self.data[k]

    def __setitem__(self, k, v=None):
        if v is None:
            self.data[self.get_next_idx()] = k
        else:
            if k == -1:
                k = self.get_next_idx()
            self.data[k] = v

    def get_next_idx(self):
        return max([-1] + [x for x in self.data if isinstance(x, int)]) + 1

    def extend(self, arr):
        if isinstance(arr, Array) or isinstance(arr, dict):
            for k, v in arr.items():
                if isinstance(k, int):
                    self.data[self.get_next_idx()] = v
                else:
                    self.data[k] = v
        elif isinstance(arr, list):
            for v in arr:
                self.data[self.get_next_idx()] = v
        else:
            self.data[self.get_next_idx()] = arr

    update = extend

    def __iter__(self):
        yield from self.data.values()

    def items(self):
        return self.data.items()

    def get_keys(self):
        return list(self.data.keys())

    def has_key(self, k):
        return k in self.data

    def values(self):
        return list(self.data.values())

    def __len__(self):
        return len(self.data.items())

    def shift(self):
        self.reset()
        k = list(self.data.keys())[0]
        rval = self.data.pop(k)
        newarr = Array()
        newarr.append(self.data)
        self.data = {}
        self.push(newarr)
        return rval

    def append(self, d, _preserve=False):
        for k, v in d.items():
            self.data[k if (not isinstance(k, int) or _preserve) else self.get_next_idx()] = v

    def slice(self, start_=0, end_=None):
        items = list(self.data.items())
        if start_ < 0:
            start_ = len(items) + start_
            end_ = start_ + end_
        return Array(dict(items[start_:end_]))

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

    def pop(self):
        return self.data.popitem()[1]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)


class HandleObj:
    pass

# =============================================================0

PHP_OS = sys.platform

PHP_GLOBALS = Array(globals())
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
PHP_SERVER["PHP_SELF"] = os.path.realpath(__file__)
PHP_SAPI = ""

PHP_POST = PHP_REQUEST
PHP_ENV = PHP_SERVER

PHP_VERSION_ID = 73000

# -----------------------------------------------------------------------------------
# PHP constants

PHP_URL_SCHEME = "scheme"
PHP_URL_USER = "user"
PHP_URL_PASS = "pass"
PHP_URL_HOST = "host"
PHP_URL_PORT = "port"
PHP_URL_PATH = "path"
PHP_URL_QUERY = "query"
PHP_URL_FRAGMENT = "fragment"

INI_USER=1
INI_PERDIR=2
INI_SYSTEM=4
INI_ALL=7 

ENT_NOQUOTES = 1
E_ALL = 1
E_DEPRECATED = 1
E_STRICT = 1
E_NOTICE = 1
E_CORE_ERROR = 1
E_CORE_WARNING = 1
E_COMPILE_ERROR = 1
E_ERROR = 1
E_WARNING = 1
E_PARSE = 1
E_USER_ERROR = 1
E_USER_WARNING = 1 
E_RECOVERABLE_ERROR = 1

CASE_LOWER = 1 
CASE_UPPER = 2 

STR_PAD_RIGHT = 1
E_USER_NOTICE = 1
PHP_BINARY_READ = 1
SODIUM_CRYPTO_GENERICHASH_BYTES = 1
SSH2_TERM_UNIT_CHARS = 1
STREAM_CLIENT_CONNECT = 1
MCRYPT_DEV_URANDOM = 1
IDNA_DEFAULT = 1
INTL_IDNA_VARIANT_UTS46 = 1
M_E = 1
PHP_QUERY_RFC1738 = 1
DEBUG_BACKTRACE_PROVIDE_OBJECT = 1
PHP_INT_MAX = 1
EXTR_OVERWRITE = 1
FTP_BINARY = 1
HTML_SPECIALCHARS = 1
ENT_COMPAT = 1
ENT_HTML401 = 2
FILTER_DEFAULT = 1
FILEINFO_NONE = 1
SEEK_SET = 1
CURLVERSION_NOW = 1 
COUNT_NORMAL = 1 
SORT_STRING = 1
SORT_REGULAR = 2
SORT_REGULAR = 2
ZLIB_ENCODING_RAW = 1
FORCE_GZIP = 1
PHP_OUTPUT_HANDLER_STDFLAGS = 1
PKCS7_DETACHED = 1
OPENSSL_PKCS1_PADDING = 1
OPENSSL_ALGO_SHA1 = 1
PATHINFO_DIRNAME = 1
PATHINFO_BASENAME = 2
PATHINFO_EXTENSION = 3
PATHINFO_FILENAME = 4
INFO_ALL = 1
PREG_PATTERN_ORDER = 1
PHP_ROUND_HALF_UP = 1
SCANDIR_SORT_ASCENDING = 1

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

def php_new_class(klass, ctr):
    if not klass in globals():
        php_call_user_func(_AUTOLOAD_FN, klass)

    return ctr()

def php_isset(v):
    try:
        val_ = v()
        return not php_empty(val_)
    except:
        return False

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
        if len([x.lower().strip() == "content-type" for x in _HEADERS.keys()]) == 0:
            print("Content-Type: text/html")
        
        for k, v in _HEADERS.items():
            # TODO: sanitize headers!
            print(f"{k}: {v}")  

        print()

        _HEADERS_PRINTED = True

    print(*args, end=" ")

def _post(v, l, n):
    if v in l:
        yield l[v]
        l[v] += n
    else:
        yield globals()[v]
        globals()[v] += n

def _pre(v, l, n):
    if v in l:
        l[v] += n
        return l[v]
    else:
        globals()[v] += n
        return globals()[v]

def php_preinc(v, l, n=1):
    return _pre(v, l, n)

def php_predec(v, l, n=1):
    return _pre(v, l, -n)

def php_postinc(v, l, n=1):
    yield from _post(v, l, n)

def php_postdec(v, l, n=1):
    yield from _post(v, l, -n)

def gmdate(x):
    return x

date = gmdate

def php_php_addcslashes(_str, _charlist="\\'\!\0"):
    return _str #@@ TODO:

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
    >>> array2 = Array({"b": "green"}, "yellow", "red")
    >>> php_array_diff(array1, array2)
    {1: 'blue'}
    """
    cmp = []
    for item in args:
        cmp.extend(item.values())
        
    return Array(dict([(k, v) for k, v in _arr.items() if v not in cmp]))

def php_array_diff_assoc(_array1, _array2, *args):
    pass

def php_array_diff_key(_array1, _array2, *args):
    pass

def php_array_fill(_start_index, _num, _value):
    pass

def php_array_fill_keys(_keys, _value):
    pass

def php_array_filter(_array, _callback=None, _flag=0):
    """
    function odd($var)
    return $var & 1;
function even($var)
    return !($var & 1);

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
        return Array(dict([(k, v) for k, v in _array.items() if php_to_bool(v)]))
    else:
        if callable(_callback):
            return Array(dict([(k, v) for k, v in _array.items() if _callback(v)]))
        else:
            return Array(dict([(k, v) for k, v in _array.items() 
                        if php_call_user_func(_callback, v)]))

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
    pass

def php_array_intersect(_array1, _array2, *args):
    pass

def php_array_intersect_assoc(_array1, _array2, *args):
    pass

def php_array_intersect_key(_array1, _array2, *args):
    pass

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

def php_array_map(_callback, _array1, *args):
    pass

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
    pass

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
    _array.push(*args)

def php_array_rand(_array, _num=1):
    pass

def php_array_reduce(_array, _callback, _initial=None, _carry=None, _item=None):
    pass

def php_array_replace_recursive(_array1, *args):
    pass

def php_array_reverse(_array, _preserve_keys=False):
    pass

def php_array_search(_needle, _haystack, _strict=False):
    pass

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

def php_array_slice(_array, _offset, _length=None, _preserve_keys=False):
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
    out = Array()
    out.append(_array.slice(_offset, _length), _preserve_keys)
    return out 

def php_array_splice(_input, _offset, _length=None, _replacement=[]):
    pass

def php_array_sum(_array):
    pass

def php_array_unique(_array, _sort_flags=SORT_STRING):
    pass

def php_array_unshift(_array, *args):
    pass

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

def php_array_walk(_array, _callback, _userdata=None):
    pass

def php_arsort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_asort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_assert(_assertion, _description):
    pass

def php_base64_decode(_data, _strict=False):
    pass

def php_base64_encode(_data):
    pass

def php_base_convert(_number, _frombase, _tobase):
    pass

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

def php_bin2hex(_str):
    return _str #@

def php_bindec(_binary_string):
    return _str #@

def php_call_user_func(_fn, *args):
    if callable(_fn):
        return _fn(*args)

    if _fn.find(".") != -1:
        *klass, method = _fn.split(".")
        klass = "_".join(klass)
        fn = globals()[klass]
        return getattr(fn, method)(*args)
    else:
        fn = globals()[_fn]
    return fn(*args)

def php_call_user_func_array(_callback, _param_arr):
    pass

def php_ceil(_value):
    return _value #@

import functools

def true_if_no_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            return True
        except:
            return False
    return wrapper

@true_if_no_exception
def php_chdir(_directory):
    """
    >>> php_chdir("/Users/nico")
    True
    >>> php_chdir("/Users/Idonotexists")
    False
    """
    os.chdir(_directory)

def php_checkdate(_month, _day, _year):
    pass

def php_chgrp(_filename, _group):
    pass

def php_chmod(_filename, _mode):
    pass

def php_chown(_filename, _user):
    pass

def php_chr(_bytevalue):
    pass

def php_chunk_split(_body, _chunklen=76, _end="\r\n"):
    pass

def php_class_exists(_class_name, _autoload=True):
    return _class_name in globals() #@

def php_clearstatcache(_clear_realpath_cache=False, _filename=None):
    pass

def php_closedir(dh):
    dh = None

def php_compact(_varname1, *args):
    pass

def php_constant(_name):
    pass

def php_copy(_source, _dest, _context):
    pass

COUNT_NORMAL = 1
COUNT_RECURSIVE = 2

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

    if item is None: return 0
    if isinstance(item, bool): return 1
    if _mode == COUNT_NORMAL: 
        return len(item)

    cnt = 0
    for k, v in item.items():
        if isinstance(k, str):
            cnt += 1
        cnt += php_count(v) if isinstance(v, Array) else 1
    return cnt

def php_count_chars(_string, _mode=0):
    pass

def php_crc32(_str):
    pass

def php_crypt(_str, _salt):
    pass

def php_ctype_alnum(_text):
    pass

def php_ctype_digit(_text):
    pass

def php_curl_close(_ch):
    pass

def php_curl_errno(_ch):
    pass

def php_curl_error(_ch):
    pass

def php_curl_exec(_ch):
    pass

def php_curl_getinfo(_ch, _opt):
    pass

def php_curl_init(_url=None):
    pass

def php_curl_multi_add_handle(_mh, _ch):
    pass

def php_curl_multi_close(_mh):
    pass

def php_curl_multi_exec(_mh, _still_running):
    pass

def php_curl_multi_info_read(_mh, _msgs_in_queue=None):
    pass

def php_curl_multi_init():
    pass

def php_curl_multi_remove_handle(_mh, _ch):
    pass

def php_curl_setopt(_ch, _option, _value):
    pass

def php_curl_version(_age=CURLVERSION_NOW):
    pass

def php_current(_array):
    pass

def php_date(_format, _timestamp=None):
    pass

def php_date_default_timezone_get():
    pass

def php_date_default_timezone_set(_timezone_identifier):
    pass

def php_debug_backtrace(_options=DEBUG_BACKTRACE_PROVIDE_OBJECT, _limit=0):
    pass

def php_decbin(_number):
    pass

def php_dechex(_number):
    pass

def php_decoct(_number):
    pass

def php_dir(_directory, _context):
    pass

def php_dirname(_path, _levels=1):
    return os.path.dirname(_path)

def php_disk_free_space(_directory):
    pass

def php_dl(_library):
    pass

def php_each(_array):
    pass

def php_end(_array):
    pass

def php_error_get_last():
    pass

def php_error_log(_message, _message_type=0, _destination=None, _extra_headers=None):
    pass

def php_error_reporting(_level):
    pass

def php_escapeshellarg(_arg):
    pass

def php_escapeshellcmd(_command):
    pass

def php_exec(_command, _output, _return_var):
    pass

def php_exif_imagetype(_filename):
    pass

def php_exif_read_data(_stream, _sections=None, _arrays=False, _thumbnail=False):
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

def php_extract(_array, _flags=EXTR_OVERWRITE, _prefix=None):
    pass

def php_fastcgi_finish_request():
    pass

def php_fclose(_handle):
    _handle.close()

def php_feof(_handle):
    pass

def php_fflush(_handle):
    pass

def php_fgets(_handle, _length):
    pass

def php_file(_filename, _flags=0, _context=None):
    pass

def php_fileatime(_filename):
    pass

def php_file_exists(_filename):
    return os.path.exists(fix_ext(_filename))

def php_file_get_contents(_filename, _use_include_path=False, _context=None, _offset=0, _maxlen=None):
    with open(_filename, "r") as f:
        return f.read()

def php_filegroup(_filename):
    pass

def php_filemtime(_filename):
    pass

def php_fileowner(_filename):
    pass

def php_fileperms(_filename):
    pass

def php_file_put_contents(_filename, _data, _flags=0, _context=None):
    pass

def php_filesize(_filename):
    pass

def php_filter_var(_variable, _filter=FILTER_DEFAULT, _options=None):
    pass

def php_finfo_close(_finfo):
    pass

def php_finfo_file(_finfo, _file_name, _options=FILEINFO_NONE, _context=None):
    pass

def php_finfo_open(_options=FILEINFO_NONE, _magic_file=""):
    pass

def php_floatval(_var):
    pass

def php_flock(_handle, _operation, _wouldblock):
    pass

def php_floor(_value):
    pass

def php_flush():
    pass

def php_fopen(_filename, _mode, _use_include_path=False, _context=None):
    pass

def php_fread(_handle, _length):
    pass

def php_fseek(_handle, _offset, _whence=SEEK_SET):
    pass

def php_fsockopen(_hostname, _port=-1, _errno=None, _errstr=None, _timeout=None):
    pass

def php_fstat(_handle):
    pass

def php_ftell(_handle):
    pass

def php_ftp_chdir(_ftp_stream, _directory):
    pass

def php_ftp_chmod(_ftp_stream, _mode, _filename):
    pass

def php_ftp_close(_ftp_stream):
    pass

def php_ftp_connect(_host, _port=21, _timeout=90):
    pass

def php_ftp_delete(_ftp_stream, _path):
    pass

def php_ftp_fget(_ftp_stream, _handle, _remote_file, _mode=FTP_BINARY, _resumepos=0):
    pass

def php_ftp_fput(_ftp_stream, _remote_file, _handle, _mode=FTP_BINARY, _startpos=0):
    pass

def php_ftp_get_option(_ftp_stream, _option):
    pass

def php_ftp_login(_ftp_stream, _username, _password):
    pass

def php_ftp_mdtm(_ftp_stream, _remote_file):
    pass

def php_ftp_mkdir(_ftp_stream, _directory):
    pass

def php_ftp_nlist(_ftp_stream, _directory):
    pass

def php_ftp_pasv(_ftp_stream, _pasv):
    pass

def php_ftp_pwd(_ftp_stream):
    pass

def php_ftp_rawlist(_ftp_stream, _directory, _recursive=False):
    pass

def php_ftp_rename(_ftp_stream, _oldname, _newname):
    pass

def php_ftp_rmdir(_ftp_stream, _directory):
    pass

def php_ftp_set_option(_ftp_stream, _option, _value):
    pass

def php_ftp_site(_ftp_stream, _command):
    pass

def php_ftp_size(_ftp_stream, _remote_file):
    pass

def php_ftp_ssl_connect(_host, _port=21, _timeout=90):
    pass

def php_ftp_systype(_ftp_stream):
    pass

def php_ftruncate(_handle, _size):
    pass

def php_func_get_arg(_arg_num):
    pass

def php_func_get_args():
    pass

def php_func_num_args():
    pass

def php_function_exists(_function_name):
    return _function_name in globals() or f"php_{_function_name}" in globals()

def php_fwrite(_handle, _string, _length):
    pass

def php_gc_enabled():
    return True

def php_gd_info():
    pass

def php_get_class(_object):
    pass

def php_get_class_methods(_class_name):
    pass

def php_getcwd():
    return os.getcwd()

def php_getdate(_timestamp=None):
    pass

def php_get_defined_constants(_categorize=False):
    pass

def php_getenv(_varname, _local_only=False):
    return os.getenv(_varname)

def php_gethostbyaddr(_ip_address):
    pass

def php_gethostbyname(_hostname):
    pass

def php_gethostbynamel(_hostname):
    pass

def php_gethostname():
    pass

def php_get_html_translation_table(_table=HTML_SPECIALCHARS, _flags=ENT_COMPAT | ENT_HTML401, _encoding="UTF-8"):
    pass

def php_getimagesize(_filename, _imageinfo):
    pass

def php_get_magic_quotes_runtime():
    pass

def php_get_object_vars(_object):
    pass

def php_get_resource_type(_handle):
    pass

def php_gettype(_var):
    pass

def php_glob(_pattern, _flags=0):
    pass

def php_gmdate(_format, _timestamp=None):
    pass

def php_gmmktime(_hour=gmdate("H"), _minute=gmdate("i"), _second=gmdate("s"), _month=gmdate("n"), _day=gmdate("j"), _year=gmdate("Y"), _is_dst=-1):
    pass

def php_gzclose(_zp):
    pass

def php_gzdecode(_data, _length):
    pass

def php_gzdeflate(_data, _level=-1, _encoding=ZLIB_ENCODING_RAW):
    pass

def php_gzencode(_data, _level=-1, _encoding_mode=FORCE_GZIP):
    pass

def php_gzinflate(_data, _length=0):
    pass

def php_gzopen(_filename, _mode, _use_include_path=0):
    pass

def php_gzread(_zp, _length):
    pass

def php_gzuncompress(_data, _length=0):
    pass

def php_gzwrite(_zp, _string, _length):
    pass

def php_hash(_algo, _data, _raw_output=False):
    pass

def php_hash_algos():
    pass

def php_hash_equals(_known_string, _user_string):
    pass

def php_hash_file(_algo, _filename, _raw_output=False):
    pass

def php_hash_final(_context, _raw_output=False):
    pass

def php_hash_hmac(_algo, _data, _key, _raw_output=False):
    pass

def php_hash_init(_algo, _options=0, _key=None):
    pass

def php_hash_update(_context, _data):
    pass

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

def php_hexdec(_hex_string):
    pass

def php_htmlentities(_string, _flags=ENT_COMPAT | ENT_HTML401, _encoding="UTF-8", _double_encode=True):
    pass

def php_html_entity_decode(_string, _flags=ENT_COMPAT | ENT_HTML401, _encoding="UTF-8"):
    pass

def php_htmlspecialchars(_string, _flags=ENT_COMPAT | ENT_HTML401, _encoding="UTF-8", _double_encode=True):
    pass

def php_htmlspecialchars_decode(_string, _flags=ENT_COMPAT | ENT_HTML401):
    pass

def php_http_build_query(_query_data, _numeric_prefix, _arg_separator, _enc_type=PHP_QUERY_RFC1738):
    pass

def php_iconv(_in_charset, _out_charset, _str):
    pass

def php_iconv_mime_decode(_encoded_header, _mode=0, _charset="UTF-8"):
    pass

def php_idn_to_ascii(_domain, _options=IDNA_DEFAULT, _variant=INTL_IDNA_VARIANT_UTS46,
        _idna_info=None):
    pass

def php_ignore_user_abort(_value):
    pass

def php_imagealphablending(_image, _blendmode):
    pass

def php_imageantialias(_image, _enabled):
    pass

def php_imagecolorallocatealpha(_image, _red, _green, _blue, _alpha):
    pass

def php_imagecolorstotal(_image):
    pass

def php_imagecopy(_dst_im, _src_im, _dst_x, _dst_y, _src_x, _src_y, _src_w, _src_h):
    pass

def php_imagecopyresampled(_dst_image, _src_image, _dst_x, _dst_y, _src_x, _src_y, _dst_w, _dst_h, _src_w, _src_h):
    pass

def php_imagecreatefromgif(_filename):
    pass

def php_imagecreatefromjpeg(_filename):
    pass

def php_imagecreatefrompng(_filename):
    pass

def php_imagecreatefromstring(_image):
    pass

def php_imagecreatetruecolor(_width, _height):
    pass

def php_imagedestroy(_image):
    pass

def php_imagegif(_image, _to=None):
    pass

def php_imageistruecolor(_image):
    pass

def php_imagejpeg(_image, _to=None, _quality=-1):
    pass

def php_imagepng(_image, _to=None, _quality=-1, _filters=-1):
    pass

def php_imagerotate(_image, _angle, _bgd_color, _ignore_transparent=0):
    pass

def php_imagesavealpha(_image, _saveflag):
    pass

def php_imagesx(_image):
    pass

def php_imagesy(_image):
    pass

def php_imagetruecolortopalette(_image, _dither, _ncolors):
    pass

def php_imagetypes():
    pass

def php_image_type_to_mime_type(_imagetype):
    pass

def php_imap_rfc822_parse_adrlist(_address, _default_host):
    pass

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
    return _glue.join(_array.values())

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
    return _needle in _haystack 

def php_inet_ntop(_in_addr):
    pass

def php_inet_pton(_address):
    pass

def php_ini_get(_varname):
    return _PHP_INI_FILE.get(_varname, "")

def php_ini_get_all(_extension=None, _details=True):
    return _PHP_INI_FILE 

def php_ini_set(_varname, _newvalue):
    _PHP_INI_FILE[_varname] = _newvalue

def php_intval(_var, _base=10):
    return int(str(_var), _base)

def php_ip2long(_ip_address):
    pass

def php_iptcparse(_iptcblock):
    pass

def php_is_a(_object, _class_name, _allow_string=False):
    return type(_object).__name__ == _class_name  #@

def php_is_array(_var):
    return isinstance(_var, list)

def php_is_bool(_var):
    return isinstance(_var, bool)

def php_is_callable(_var, _syntax_only=False, _callable_name=None):
    return callable(_var)

def php_is_dir(_filename):
    return os.path.isdir(_filename)

def php_is_executable(_filename):
    pass

def php_is_file(_filename):
    return os.path.isfile(_filename)

def php_is_float(_var):
    return isinstance(_var, float)

def php_is_int(_var):
    return isinstance(_var, int)

def php_is_link(_filename):
    return os.path.islink(_filename)

def php_is_nan(_val):
    pass

def php_is_null(_var):
    return _var is None

def php_is_numeric(_var):
    return isinstance(_var, int) or isinstance(_var, float)

def php_is_object(_var):
    return isinstance(_var, type)

def php_is_readable(_filename):
    return True

def php_is_resource(_var):
    pass

def php_is_scalar(_var):
    pass

def php_is_string(_var):
    return isinstance(_var, str)

def php_is_subclass_of(_object, _class_name, _allow_string=True):
    pass

def php_is_uploaded_file(_filename):
    pass

def php_is_writable(_filename):
    return True

def php_json_decode(_json, _assoc=False, _depth=512, _options=0):
    return json.loads(_json)

def php_json_encode(_value, _options=0, _depth=512):
    return json.dumps(_value)

def php_json_last_error():
    pass

def php_json_last_error_msg():
    pass

def php_key(_array):
    pass

def php_krsort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_ksort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_libxml_clear_errors():
    pass

def php_libxml_disable_entity_loader(_disable=True):
    pass

def php_libxml_get_last_error():
    pass

def php_libxml_use_internal_errors(_use_errors=False):
    pass

def php_log(_arg, _base=M_E):
    pass

def php_log10(_arg):
    pass

def php_long2ip(_proper_address):
    pass

def php_ltrim(_str, _character_mask=None):
    return _str.lstrip()

def php_mail(_to, _subject, _message, _additional_headers, _additional_parameters):
    pass

def php_max(_values, _value1, *args):
    return max(_values, value1) #@

def php_mb_check_encoding(_var=None, _encoding="UTF-8"):
    pass

def php_mb_convert_encoding(_val, _to_encoding, _from_encoding="UTF-8"):
    pass

def php_mb_detect_encoding(_str, _encoding_list=None, _strict=False):
    pass

def php_mb_detect_order(_encoding_list=None):
    pass

def php_mb_get_info(_type="all"):
    pass

def php_mb_internal_encoding(_encoding="UTF-8"):
    pass

def php_mb_list_encodings():
    pass

def php_mb_stripos(_haystack, _needle, _offset=0, _encoding="UTF-8"):
    return _haystack.find(_needle) #@

def php_mb_strlen(_str, _encoding="UTF-8"):
    return len(_str)

def php_mb_strtolower(_str, _encoding="UTF-8"):
    return _str.lower()

def php_mb_substr(_str, _start, _length=0, _encoding="UTF-8"):
    return _str[_start:_start + _length]

def php_mcrypt_create_iv(_size, _source=MCRYPT_DEV_URANDOM):
    pass

def php_md5(_str, _raw_output=False):
    m = hashlib.md5()
    m.update(_str.encode("utf-8"))
    return m.hexdigest()

def php_md5_file(_filename, _raw_output=False):
    with open(_filename, encoding="utf-8") as f:
        return php_md5(f.read())

def php_method_exists(_object, _method_name):
    return hasattr(_object, _method_name) and callable(getattr(_object, _method_name))

def php_microtime(_get_as_float=False):
    return int(datetime.now().timestamp() * 1000)

def php_mime_content_type(_filename):
    pass

def php_min(_values, _value1, *args):
    return min(_values, _value1)

def php_mkdir(_pathname, _mode=0o777, _recursive=False, _context=None):
    pass

def php_mktime(_hour=date("H"), _minute=date("i"), _second=date("s"), _month=date("n"), _day=date("j"), _year=date("Y"), _is_dst=-1):
    pass

def php_move_uploaded_file(_filename, _destination):
    pass

def php_mt_rand(_min=None, _max=None):
    pass

def php_mysqli_real_connect(dbh_, host_, username_, passwd_, dbname_, port_=None, 
        socket_=None, flags_=None):
    try:
        dbh_[-1] = php_mysqli_connect(host_, username_, passwd_, dbname_) 
        return True
    except:
        return False

def php_mysqli_init():
    return Array()

def php_mysqli_connect(host, user, pwd, db):
    return mysql.connector.connect(host=host, user=user,passwd=pwd, database=db)

def php_mysql_client_encoding(_link_identifier=None):
    pass

def php_mysql_close(_link_identifier=None):
    pass

def php_mysql_ping(_link_identifier=None):
    pass

def php_mysql_set_charset(_charset, _link_identifier=None):
    pass

def php_natcasesort(_array):
    pass

def php_natsort(_array):
    pass

def php_next(_array):
    pass

def php_number_format(_number=None, _decimals=0, _dec_point=".", _thousands_sep=","):
    pass

def php_ob_clean():  pass
def php_ob_end_clean(): pass
def php_ob_end_flush(): pass
def php_ob_get_clean(): pass
def php_ob_get_contents(): pass
def php_ob_get_flush():  pass
def php_ob_get_length():   pass
def php_ob_get_level():  pass
def php_ob_start(_output_callback=None, _chunk_size=0, _flags=PHP_OUTPUT_HANDLER_STDFLAGS, _buffer=None, _phase=None): pass
def php_opcache_invalidate(_script, _force=False): pass

def php_opendir(_path, _context=None):
    dh = HandleObj()
    dh.path = _path
    dh.context = _context
    dh.files = os.listdir(_path)
    dh.pos = 0
    return dh

def php_openssl_decrypt(_data, _method, _key, _options=0, _iv="", _tag="", _aad=""):
    pass

def php_openssl_encrypt(_data, _method, _key, _options=0, _iv="", _tag=None, _aad="", _tag_length=16):
    pass

def php_openssl_error_string():
    pass

def php_openssl_get_cipher_methods(_aliases=False):
    pass

def php_openssl_get_md_methods(_aliases=False):
    pass

def php_openssl_pkcs7_sign(_infilename, _outfilename, _signcert, _privkey, _headers, _flags=PKCS7_DETACHED, _extracerts=None):
    pass

def php_openssl_pkey_free(_key):
    pass

def php_openssl_pkey_get_details(_key):
    pass

def php_openssl_pkey_get_private(_key, _passphrase=""):
    pass

def php_openssl_private_encrypt(_data, _crypted, _key, _padding=OPENSSL_PKCS1_PADDING):
    pass

def php_openssl_sign(_data, _signature, _priv_key_id, _signature_alg=OPENSSL_ALGO_SHA1):
    pass

def php_openssl_x509_parse(_x509cert, _shortnames=True):
    pass

def php_ord(_string):
    return ord(_string)

def php_pack(_format, *args):
    pass

def php_parse_str(_encoded_string, _result):
    pass

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

def php_pathinfo(_path, _options=PATHINFO_DIRNAME | PATHINFO_BASENAME | PATHINFO_EXTENSION | PATHINFO_FILENAME):
    pass

def php_pclose(_handle):
    pass

def php_phpinfo(_what=INFO_ALL):
    pass

def php_php_sapi_name(): return ""

def php_php_uname(_mode="a"):
    pass

def php_phpversion(_extension=None): return "php/7.3"

def php_popen(_command, _mode):
    pass

def php_posix_getgrgid(_gid):
    pass

def php_posix_getpwuid(_uid):
    pass

def php_pow(_base, _exp):
    pass

def _get_pattern(p):
    sep = p[0]
    last = p.rfind(sep)
    return p[1:last]

def php_preg_match(_pattern, _subject, _matches=None, _flags=0, _offset=0):
    return re.match(_get_pattern(_pattern), _subject)

def php_preg_match_all(_pattern, _subject, _matches, _flags=PREG_PATTERN_ORDER, _offset=0):
    pass

def php_preg_quote(_str, _delimiter=None):
    pass

def php_preg_replace(_pattern, _replacement, _subject, _limit=0, _count=None):
    assert _count is None
    return re.sub(_get_pattern(_pattern), _replacement, _subject, _limit)

def php_preg_replace_callback(_pattern, _callback, _subject, _limit=-1, _count=None, _matches=None):
    pass

def php_preg_split(_pattern, _subject, _limit=-1, _flags=0):
    return re.split(_get_pattern(_pattern), _subject)

def php_prev(_array):
    assert isinstance(_array, Array)
    return _array.prev()

def php_end(_array):
    assert isinstance(_array, Array)
    return _array.end()

def php_printf(_format, *args):
    pass

def php_print_r(_expression, _return=False):
    pass

def php_property_exists(_class, _property):
    pass

def php_quoted_printable_decode(_str):
    pass

def php_quoted_printable_encode(_str):
    pass

def php_rand(_min=None, _max=None):
    pass

def php_random_bytes(_length):
    pass

def php_random_int(_min, _max):
    pass

def php_range(_start, _end, _step=1):
    pass

def php_rawurldecode(_str):
    pass

def php_rawurlencode(_str):
    pass

def php_readdir(dh):
    try:
        fname = dh.files[dh.pos]
        dh.pos += 1
        return fname
    except:
        return False

def php_readfile(_filename, _use_include_path=False, _context=None):
    pass

def php_realpath(_path):
    return os.path.realpath(_path)

def php_register_shutdown_function(_callback, *args):
    pass

def php_rename(_oldname, _newname, _context):
    pass

def php_reset(_array):
    pass

def php_restore_error_handler():
    pass

def php_rewind(_handle):
    pass

def php_rmdir(_dirname, _context):
    pass

def php_round(_val, _precision=0, _mode=PHP_ROUND_HALF_UP):
    pass

def php_rsort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_rtrim(_str, _character_mask=None):
    return _str.rstrip()

def php_scandir(_directory, _sorting_order=SCANDIR_SORT_ASCENDING, _context=None):
    pass

def php_serialize(_value):
    pass

def php_setcookie(_name, _value="", _expires=0, _path="", _domain="", _secure=False, _httponly=False):
    pass

def php_set_error_handler(_error_handler, _error_types=None, _errno=None, _errstr=None, _errfile=None, _errline=None, _errcontext=None):
    pass

def php_setlocale(_category, _locale, *args):
    pass

def php_set_magic_quotes_runtime(_new_setting):
    pass

def php_set_time_limit(_seconds):
    pass

def php_settype(_var, _type):
    pass

def php_sha1(_str, _raw_output=False):
    pass

def php_sha1_file(_filename, _raw_output=False):
    pass

def php_shell_exec(_cmd):
    pass

def php_shuffle(_array):
    pass

def php_simplexml_import_dom(_node, _class_name="SimpleXMLElement"):
    pass

def php_simplexml_load_string(_data, _class_name="SimpleXMLElement", _options=0, _ns="", _is_prefix=False):
    pass

def php_sleep(_seconds):
    pass

def php_socket_accept(_socket):
    pass

def php_socket_bind(_socket, _address, _port=0):
    pass

def php_socket_close(_socket):
    pass

def php_socket_connect(_socket, _address, _port=0):
    pass

def php_socket_create(_domain, _type, _protocol):
    pass

def php_socket_getsockname(_socket, _addr, _port):
    pass

def php_socket_last_error(_socket):
    pass

def php_socket_listen(_socket, _backlog=0):
    pass

def php_socket_read(_socket, _length, _type=PHP_BINARY_READ):
    pass

def php_socket_set_option(_socket, _level, _optname, _optval):
    pass

def php_socket_strerror(_errno):
    pass

def php_socket_write(_socket, _buffer, _length=0):
    pass

def php_sodium_bin2hex(_bin):
    pass

def php_sodium_compare(_buf1, _buf2):
    pass

def php_sodium_crypto_aead_aes256gcm_is_available():
    pass

def php_sodium_crypto_aead_chacha20poly1305_decrypt(_ciphertext, _ad, _nonce, _key):
    pass

def php_sodium_crypto_aead_chacha20poly1305_encrypt(_msg, _ad, _nonce, _key):
    pass

def php_sodium_crypto_aead_chacha20poly1305_ietf_decrypt(_ciphertext, _ad, _nonce, _key):
    pass

def php_sodium_crypto_aead_chacha20poly1305_ietf_encrypt(_msg, _ad, _nonce, _key):
    pass

def php_sodium_crypto_aead_xchacha20poly1305_ietf_decrypt(_ciphertext, _ad, _nonce, _key):
    pass

def php_sodium_crypto_aead_xchacha20poly1305_ietf_encrypt(_msg, _ad, _nonce, _key):
    pass

def php_sodium_crypto_auth(_msg, _key):
    pass

def php_sodium_crypto_auth_verify(_signature, _msg, _key):
    pass

def php_sodium_crypto_box(_msg, _nonce, _key):
    pass

def php_sodium_crypto_box_keypair():
    pass

def php_sodium_crypto_box_keypair_from_secretkey_and_publickey(_secret_key, _public_key):
    pass

def php_sodium_crypto_box_open(_ciphertext, _nonce, _key):
    pass

def php_sodium_crypto_box_publickey(_key):
    pass

def php_sodium_crypto_box_publickey_from_secretkey(_key):
    pass

def php_sodium_crypto_box_seal(_msg, _key):
    pass

def php_sodium_crypto_box_seal_open(_ciphertext, _key):
    pass

def php_sodium_crypto_box_secretkey(_key):
    pass

def php_sodium_crypto_box_seed_keypair(_key):
    pass

def php_sodium_crypto_generichash(_msg, _key, _length=SODIUM_CRYPTO_GENERICHASH_BYTES):
    pass

def php_sodium_crypto_generichash_final(_state, _length=SODIUM_CRYPTO_GENERICHASH_BYTES):
    pass

def php_sodium_crypto_generichash_init(_key, _length=SODIUM_CRYPTO_GENERICHASH_BYTES):
    pass

def php_sodium_crypto_generichash_update(_state, _msg):
    pass

def php_sodium_crypto_pwhash(_length, _password, _salt, _opslimit, _memlimit, _alg):
    pass

def php_sodium_crypto_pwhash_scryptsalsa208sha256(_length, _password, _salt, _opslimit, _memlimit):
    pass

def php_sodium_crypto_pwhash_scryptsalsa208sha256_str(_password, _opslimit, _memlimit):
    pass

def php_sodium_crypto_pwhash_scryptsalsa208sha256_str_verify(_hash, _password):
    pass

def php_sodium_crypto_pwhash_str(_password, _opslimit, _memlimit):
    pass

def php_sodium_crypto_pwhash_str_verify(_hash, _password):
    pass

def php_sodium_crypto_scalarmult(_n, _p):
    pass

def php_sodium_crypto_secretbox(_string, _nonce, _key):
    pass

def php_sodium_crypto_secretbox_open(_ciphertext, _nonce, _key):
    pass

def php_sodium_crypto_shorthash(_msg, _key):
    pass

def php_sodium_crypto_sign(_msg, _secret_key):
    pass

def php_sodium_crypto_sign_detached(_msg, _secretkey):
    pass

def php_sodium_crypto_sign_ed25519_pk_to_curve25519(_key):
    pass

def php_sodium_crypto_sign_ed25519_sk_to_curve25519(_key):
    pass

def php_sodium_crypto_sign_keypair():
    pass

def php_sodium_crypto_sign_keypair_from_secretkey_and_publickey(_secret_key, _public_key):
    pass

def php_sodium_crypto_sign_open(_string, _public_key):
    pass

def php_sodium_crypto_sign_publickey(_keypair):
    pass

def php_sodium_crypto_sign_publickey_from_secretkey(_key):
    pass

def php_sodium_crypto_sign_secretkey(_key):
    pass

def php_sodium_crypto_sign_seed_keypair(_key):
    pass

def php_sodium_crypto_sign_verify_detached(_signature, _msg, _public_key):
    pass

def php_sodium_crypto_stream(_length, _nonce, _key):
    pass

def php_sodium_crypto_stream_xor(_msg, _nonce, _key):
    pass

def php_sodium_hex2bin(_hex, _ignore):
    pass

def php_sodium_increment(_val):
    pass

def php_sodium_memcmp(_buf1, _buf2):
    pass

def php_sodium_memzero(_buf):
    pass

def php_sodium_pad(_unpadded, _length):
    pass

def php_sodium_unpad(_padded, _length):
    pass

def php_sort(_array, _sort_flags=SORT_REGULAR):
    pass

def php_spl_autoload_unregister(_fn, _throw=True, _prepend=False):
    global _AUTOLOAD_FN

    _AUTOLOAD_FN = None

def php_spl_autoload_register(_fn, _throw=True, _prepend=False):
    global _AUTOLOAD_FN

    if isinstance(_fn, str):
        _AUTOLOAD_FN = _fn
    elif type(_fn).__name__ == "Array":
        _AUTOLOAD_FN = ".".join(_fn.get_list())
    else:
        assert False, "Closure not yet supported!"

def php_spl_object_hash(_obj):
    pass

def php_sprintf(_format, *args):
    return _format % args

def php_sscanf(_str, _format, *args):
    pass

def php_ssh2_auth_password(_session, _username, _password):
    pass

def php_ssh2_auth_pubkey_file(_session, _username, _pubkeyfile, _privkeyfile, _passphrase):
    pass

def php_ssh2_connect(_host, _port=22, _methods=None, _callbacks=None):
    pass

def php_ssh2_exec(_session, _command, _pty, _env, _width=80, _height=25, _width_height_type=SSH2_TERM_UNIT_CHARS):
    pass

def php_ssh2_sftp(_session):
    pass

def php_ssh2_sftp_mkdir(_sftp, _dirname, _mode=0o777, _recursive=False):
    pass

def php_ssh2_sftp_realpath(_sftp, _filename):
    pass

def php_ssh2_sftp_rename(_sftp, _from, _to):
    pass

def php_ssh2_sftp_rmdir(_sftp, _dirname):
    pass

def php_ssh2_sftp_unlink(_sftp, _filename):
    pass

def php_stat(_filename):
    pass

def php_strcasecmp(_str1, _str2):
    pass

def php_strcmp(_str1, _str2):
    pass

def php_strcspn(_subject, _mask, _start, _length):
    pass

def php_stream_context_create(_options, _params):
    pass

def php_stream_context_get_options(_stream_or_context):
    pass

def php_stream_context_set_option(_stream_or_context, *args):
    pass

def php_stream_get_contents(_handle, _maxlength=-1, _offset=-1):
    pass

def php_stream_get_meta_data(_stream):
    pass

def php_stream_get_wrappers():
    pass

def php_stream_set_blocking(_stream, _mode):
    pass

def php_stream_set_chunk_size(_fp, _chunk_size):
    pass

def php_stream_set_read_buffer(_stream, _buffer):
    pass

def php_stream_set_timeout(_stream, _seconds, _microseconds=0):
    pass

def php_stream_socket_client(_remote_socket, _errno, _errstr, _timeout=None, _flags=STREAM_CLIENT_CONNECT, _context=None):
    pass

def php_stream_socket_enable_crypto(_stream, _enable, _crypto_type, _session_stream):
    pass

def php_strftime(_format, _timestamp=None):
    pass

def php_stripcslashes(_str):
    return _str 

def php_stripos(_haystack, _needle, _offset=0):
    return _haystack.find(_needle)

def php_stripslashes(_str):
    return _str

def php_strip_tags(_str, _allowable_tags):
    return _str

def php_str_ireplace(_search, _replace, _subject, _count):
    return _subject.replace(_seach, _replace)

def php_stristr(_haystack, _needle, _before_needle=False):
    return _haystack.find(_needle)

def php_strlen(_string):
    return len(_string)

def php_strnatcasecmp(_str1, _str2):
    pass

def php_strncmp(_str1, _str2, _len):
    pass

def php_str_pad(_input, _pad_length, _pad_string=" ", _pad_type=STR_PAD_RIGHT):
    return _input

def php_strpbrk(_haystack, _char_list):
    pass

def php_strpos(_haystack, _needle, _offset=0):
    pos = _haystack.find(_needle)
    if pos == -1:
        return False
    return pos

def php_strrchr(_haystack, _needle):
    pass

def php_str_repeat(_input, _multiplier):
    return _input * _multiplier

def php_str_replace(_search, _replace, _subject, _count=0):
    if not isinstance(_search, Array):
        return _subject.replace(_search, _replace)
    else:
        for sr, rp in zip(_search, _replace):
            _subject = _subject.replace(sr, rp)
        return _subject

def php_strrev(_string):
    return _string[::-1]

def php_strripos(_haystack, _needle, _offset=0):
    return _haystack.find(_needle)

def php_strrpos(_haystack, _needle, _offset=0):
    return _haystack.find(_needle)

def php_str_split(_string, _split_length=1):
    pass

def php_strspn(_subject, _mask, _start, _length):
    pass

def php_strstr(_haystack, _needle, _before_needle=False):
    pos = _haystack.find(_needle)

    if pos == -1:
        return _haystack

    if _before_needle:
        return _haystack[:pos]
    else:
        return _haystack[pos:]

def php_strtok(*args):
    pass

def php_strtolower(_string): return _string.lower()
def php_strtoupper(_string): return _string.upper()

def php_strtotime(_time, _now=None):
    pass

def php_strtr(_str, *args):
    return _str

def php_strval(_var):
    return _var

def php_substr(_string, _start, _length=None):
    if _length is None:
       return _string[_start:]
    return _string[_start:_start + _length]

def php_substr_count(_haystack, _needle, _offset=0, _length=None):
    return _haystack.count(_needle)

def php_substr_replace(_string, _replacement, _start, _length):
    return _string

def php_sys_get_temp_dir():
    import tempfile
    return tempfile.gettempdir()

def php_tempnam(_dir, _prefix):
    import tempfile
    fh, fpath = tempfile.mkstemp(prefix=_prefix, dir=_dir)
    fh.close()
    return fpath

def php_time():
    pass

def php_token_get_all(_source, _flags=0):
    pass

def php_touch(_filename, _time=None, _atime=None):
    pass

def php_trigger_error(_error_msg, _error_type=E_USER_NOTICE):
    pass

def php_trim(_str, _character_mask=" \t\n\r\0\x0B"):
    return _str.strip()

def php_uasort(_array, _value_compare_func):
    pass

def php_ucfirst(_str):
    pass

def php_ucwords(_str, _delimiters=" \t\r\n\f\v"):
    pass

def php_uksort(_array, _key_compare_func, _a, _b):
    pass

def php_umask(_mask=None):
    pass

def php_uniqid(_prefix="", _more_entropy=False):
    pass

def php_unlink(_filename, _context):
    pass

def php_unpack(_format, _data, _offset=0):
    pass

def php_unserialize(_str, _options):
    pass

def php_urldecode(_str):
    pass

def php_urlencode(_str):
    pass

def php_usort(_array, _value_compare_func, _a, _b):
    pass

def php_utf8_decode(_data):
    pass

def php_utf8_encode(_data):
    pass

def php_var_export(_expression, _return=False):
    pass

def php_version_compare(_version1, _version2, _operator=None):
    pass

def php_vsprintf(_format, _args):
    pass

def php_wordwrap(_str, _width=75, _break="\n", _cut=False):
    pass

def php_xdiff_string_diff(_old_data, _new_data, _context=3, _minimal=False):
    pass

def php_xml_error_string(_code):
    pass

def php_xml_get_current_byte_index(_parser):
    pass

def php_xml_get_current_column_number(_parser):
    pass

def php_xml_get_current_line_number(_parser):
    pass

def php_xml_get_error_code(_parser):
    pass

def php_xml_parse(_parser, _data, _is_final=False):
    pass

def php_xml_parse_into_struct(_parser, _data, _values, _index):
    pass

def php_xml_parser_create(_encoding):
    pass

def php_xml_parser_create_ns(_encoding, _separator=":"):
    pass

def php_xml_parser_free(_parser):
    pass

def php_xml_parser_set_option(_parser, _option, _value):
    pass

def php_xml_set_character_data_handler(_parser, _handler):
    pass

def php_xml_set_default_handler(_parser, _handler):
    pass

def php_xml_set_element_handler(_parser, _start_element_handler, _end_element_handler):
    pass

def php_xml_set_end_namespace_decl_handler(_parser, _handler):
    pass

def php_xml_set_object(_parser, _object):
    pass

def php_xml_set_start_namespace_decl_handler(_parser, _handler):
    pass

def php_zend_version():
    return "1.0"

def php_session_name(name):
    pass

def php_session_set_cookie_params(p1,p2,p3,p4,p5):
    pass

def php_session_start():
    pass

# ========================================================================================

def stream_get_transports():
    return Array("tcp", "udp", "unix", "udg", "ssl", "tls", "tlsv1.0", "tlsv1.1", "tlsv1.2")

defs = locals().copy()
PHP_FUNCTIONS = [k[4:] for k, v in defs.items() if callable(v) and k.startswith("php_")]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
