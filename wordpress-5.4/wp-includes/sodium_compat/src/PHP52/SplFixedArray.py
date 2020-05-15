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
if php_class_exists("SplFixedArray"):
    sys.exit(-1)
# end if
#// 
#// The SplFixedArray class provides the main functionalities of array. The
#// main differences between a SplFixedArray and a normal PHP array is that
#// the SplFixedArray is of fixed length and allows only integers within
#// the range as indexes. The advantage is that it allows a faster array
#// implementation.
#//
class SplFixedArray(Countable):
    internalArray = Array()
    size = 0
    #// 
    #// SplFixedArray constructor.
    #// @param int $size
    #//
    def __init__(self, size=0):
        
        self.size = size
        self.internalArray = Array()
    # end def __init__
    #// 
    #// @return int
    #//
    def count(self):
        
        return php_count(self.internalArray)
    # end def count
    #// 
    #// @return array
    #//
    def toarray(self):
        
        ksort(self.internalArray)
        return self.internalArray
    # end def toarray
    #// 
    #// @param array $array
    #// @param bool $save_indexes
    #// @return SplFixedArray
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fromarray(self, array=None, save_indexes=True):
        global self
        self = php_new_class("SplFixedArray", lambda : SplFixedArray(php_count(array)))
        if save_indexes:
            for key,value in array:
                self[int(key)] = value
            # end for
        else:
            i = 0
            for value in php_array_values(array):
                self[i] = value
                i += 1
            # end for
        # end if
        return self
    # end def fromarray
    #// 
    #// @return int
    #//
    def getsize(self):
        
        return self.size
    # end def getsize
    #// 
    #// @param int $size
    #// @return bool
    #//
    def setsize(self, size=None):
        
        self.size = size
        return True
    # end def setsize
    #// 
    #// @param string|int $index
    #// @return bool
    #//
    def offsetexists(self, index=None):
        
        return php_array_key_exists(int(index), self.internalArray)
    # end def offsetexists
    #// 
    #// @param string|int $index
    #// @return mixed
    #//
    def offsetget(self, index=None):
        
        return self.internalArray[int(index)]
    # end def offsetget
    #// 
    #// @param string|int $index
    #// @param mixed $newval
    #// @psalm-suppress MixedAssignment
    #//
    def offsetset(self, index=None, newval=None):
        
        self.internalArray[int(index)] = newval
    # end def offsetset
    #// 
    #// @param string|int $index
    #//
    def offsetunset(self, index=None):
        
        self.internalArray[int(index)] = None
    # end def offsetunset
    #// 
    #// Rewind iterator back to the start
    #// @link https://php.net/manual/en/splfixedarray.rewind.php
    #// @return void
    #// @since 5.3.0
    #//
    def rewind(self):
        
        reset(self.internalArray)
    # end def rewind
    #// 
    #// Return current array entry
    #// @link https://php.net/manual/en/splfixedarray.current.php
    #// @return mixed The current element value.
    #// @since 5.3.0
    #//
    def current(self):
        
        return current(self.internalArray)
    # end def current
    #// 
    #// Return current array index
    #// @return int The current array index.
    #//
    def key(self):
        
        return key(self.internalArray)
    # end def key
    #// 
    #// @return void
    #//
    def next(self):
        
        next(self.internalArray)
    # end def next
    #// 
    #// Check whether the array contains more elements
    #// @link https://php.net/manual/en/splfixedarray.valid.php
    #// @return bool true if the array contains any more elements, false otherwise.
    #//
    def valid(self):
        
        if php_empty(lambda : self.internalArray):
            return False
        # end if
        result = next(self.internalArray) != False
        php_prev(self.internalArray)
        return result
    # end def valid
    #// 
    #// Do nothing.
    #//
    def __wakeup(self):
        
        pass
    # end def __wakeup
# end class SplFixedArray
