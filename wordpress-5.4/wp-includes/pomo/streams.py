#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// Classes, which help reading streams of data from files.
#// Based on the classes from Danilo Segan <danilo@kvota.net>
#// 
#// @version $Id: streams.php 1157 2015-11-20 04:30:11Z dd32 $
#// @package pomo
#// @subpackage streams
#//
if (not php_class_exists("POMO_Reader", False)):
    class POMO_Reader():
        endian = "little"
        _post = ""
        #// 
        #// PHP5 constructor.
        #//
        def __init__(self):
            
            self.is_overloaded = php_ini_get("mbstring.func_overload") & 2 != 0 and php_function_exists("mb_substr")
            self._pos = 0
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see POMO_Reader::__construct()
        #//
        def pomo_reader(self):
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__()
        # end def pomo_reader
        #// 
        #// Sets the endianness of the file.
        #// 
        #// @param string $endian Set the endianness of the file. Accepts 'big', or 'little'.
        #//
        def setendian(self, endian=None):
            
            #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
            self.endian = endian
        # end def setendian
        #// 
        #// Reads a 32bit Integer from the Stream
        #// 
        #// @return mixed The integer, corresponding to the next 32 bits from
        #// the stream of false if there are not enough bytes or on error
        #//
        def readint32(self):
            
            bytes = self.read(4)
            if 4 != self.strlen(bytes):
                return False
            # end if
            endian_letter = "N" if "big" == self.endian else "V"
            int = unpack(endian_letter, bytes)
            return reset(int)
        # end def readint32
        #// 
        #// Reads an array of 32-bit Integers from the Stream
        #// 
        #// @param integer $count How many elements should be read
        #// @return mixed Array of integers or false if there isn't
        #// enough data or on error
        #//
        def readint32array(self, count=None):
            
            bytes = self.read(4 * count)
            if 4 * count != self.strlen(bytes):
                return False
            # end if
            endian_letter = "N" if "big" == self.endian else "V"
            return unpack(endian_letter + count, bytes)
        # end def readint32array
        #// 
        #// @param string $string
        #// @param int    $start
        #// @param int    $length
        #// @return string
        #//
        def substr(self, string=None, start=None, length=None):
            
            if self.is_overloaded:
                return php_mb_substr(string, start, length, "ascii")
            else:
                return php_substr(string, start, length)
            # end if
        # end def substr
        #// 
        #// @param string $string
        #// @return int
        #//
        def strlen(self, string=None):
            
            if self.is_overloaded:
                return php_mb_strlen(string, "ascii")
            else:
                return php_strlen(string)
            # end if
        # end def strlen
        #// 
        #// @param string $string
        #// @param int    $chunk_size
        #// @return array
        #//
        def str_split(self, string=None, chunk_size=None):
            
            if (not php_function_exists("str_split")):
                length = self.strlen(string)
                out = Array()
                i = 0
                while i < length:
                    
                    out[-1] = self.substr(string, i, chunk_size)
                    i += chunk_size
                # end while
                return out
            else:
                return str_split(string, chunk_size)
            # end if
        # end def str_split
        #// 
        #// @return int
        #//
        def pos(self):
            
            return self._pos
        # end def pos
        #// 
        #// @return true
        #//
        def is_resource(self):
            
            return True
        # end def is_resource
        #// 
        #// @return true
        #//
        def close(self):
            
            return True
        # end def close
    # end class POMO_Reader
# end if
if (not php_class_exists("POMO_FileReader", False)):
    class POMO_FileReader(POMO_Reader):
        #// 
        #// @param string $filename
        #//
        def __init__(self, filename=None):
            
            super().__init__()
            self._f = fopen(filename, "rb")
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see POMO_FileReader::__construct()
        #//
        def pomo_filereader(self, filename=None):
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__(filename)
        # end def pomo_filereader
        #// 
        #// @param int $bytes
        #// @return string|false Returns read string, otherwise false.
        #//
        def read(self, bytes=None):
            
            return fread(self._f, bytes)
        # end def read
        #// 
        #// @param int $pos
        #// @return boolean
        #//
        def seekto(self, pos=None):
            
            if -1 == fseek(self._f, pos, SEEK_SET):
                return False
            # end if
            self._pos = pos
            return True
        # end def seekto
        #// 
        #// @return bool
        #//
        def is_resource(self):
            
            return is_resource(self._f)
        # end def is_resource
        #// 
        #// @return bool
        #//
        def feof(self):
            
            return php_feof(self._f)
        # end def feof
        #// 
        #// @return bool
        #//
        def close(self):
            
            return php_fclose(self._f)
        # end def close
        #// 
        #// @return string
        #//
        def read_all(self):
            
            all = ""
            while True:
                
                if not ((not self.feof())):
                    break
                # end if
                all += self.read(4096)
            # end while
            return all
        # end def read_all
    # end class POMO_FileReader
# end if
if (not php_class_exists("POMO_StringReader", False)):
    #// 
    #// Provides file-like methods for manipulating a string instead
    #// of a physical file.
    #//
    class POMO_StringReader(POMO_Reader):
        _str = ""
        #// 
        #// PHP5 constructor.
        #//
        def __init__(self, str=""):
            
            super().__init__()
            self._str = str
            self._pos = 0
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see POMO_StringReader::__construct()
        #//
        def pomo_stringreader(self, str=""):
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__(str)
        # end def pomo_stringreader
        #// 
        #// @param string $bytes
        #// @return string
        #//
        def read(self, bytes=None):
            
            data = self.substr(self._str, self._pos, bytes)
            self._pos += bytes
            if self.strlen(self._str) < self._pos:
                self._pos = self.strlen(self._str)
            # end if
            return data
        # end def read
        #// 
        #// @param int $pos
        #// @return int
        #//
        def seekto(self, pos=None):
            
            self._pos = pos
            if self.strlen(self._str) < self._pos:
                self._pos = self.strlen(self._str)
            # end if
            return self._pos
        # end def seekto
        #// 
        #// @return int
        #//
        def length(self):
            
            return self.strlen(self._str)
        # end def length
        #// 
        #// @return string
        #//
        def read_all(self):
            
            return self.substr(self._str, self._pos, self.strlen(self._str))
        # end def read_all
    # end class POMO_StringReader
# end if
if (not php_class_exists("POMO_CachedFileReader", False)):
    #// 
    #// Reads the contents of the file in the beginning.
    #//
    class POMO_CachedFileReader(POMO_StringReader):
        #// 
        #// PHP5 constructor.
        #//
        def __init__(self, filename=None):
            
            super().__init__()
            self._str = php_file_get_contents(filename)
            if False == self._str:
                return False
            # end if
            self._pos = 0
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see POMO_CachedFileReader::__construct()
        #//
        def pomo_cachedfilereader(self, filename=None):
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__(filename)
        # end def pomo_cachedfilereader
    # end class POMO_CachedFileReader
# end if
if (not php_class_exists("POMO_CachedIntFileReader", False)):
    #// 
    #// Reads the contents of the file in the beginning.
    #//
    class POMO_CachedIntFileReader(POMO_CachedFileReader):
        #// 
        #// PHP5 constructor.
        #//
        def __init__(self, filename=None):
            
            super().__init__(filename)
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.4.0 Use __construct() instead.
        #// 
        #// @see POMO_CachedIntFileReader::__construct()
        #//
        def pomo_cachedintfilereader(self, filename=None):
            
            _deprecated_constructor(self.class_, "5.4.0", static.class_)
            self.__init__(filename)
        # end def pomo_cachedintfilereader
    # end class POMO_CachedIntFileReader
# end if
