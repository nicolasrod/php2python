#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
class SplFixedArray(IteratorArrayAccessCountable):
    #// @var array<int, mixed>
    internalArray = Array()
    #// @var int $size
    size = 0
    #// 
    #// SplFixedArray constructor.
    #// @param int $size
    #//
    def __init__(self, size_=0):
        
        
        self.size = size_
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
    def fromarray(self, array_=None, save_indexes_=None):
        if save_indexes_ is None:
            save_indexes_ = True
        # end if
        
        self_ = php_new_class("SplFixedArray", lambda : SplFixedArray(php_count(array_)))
        if save_indexes_:
            for key_,value_ in array_:
                self_[php_int(key_)] = value_
            # end for
        else:
            i_ = 0
            for value_ in php_array_values(array_):
                self_[i_] = value_
                i_ += 1
            # end for
        # end if
        return self_
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
    def setsize(self, size_=None):
        
        
        self.size = size_
        return True
    # end def setsize
    #// 
    #// @param string|int $index
    #// @return bool
    #//
    def offsetexists(self, index_=None):
        
        
        return php_array_key_exists(php_int(index_), self.internalArray)
    # end def offsetexists
    #// 
    #// @param string|int $index
    #// @return mixed
    #//
    def offsetget(self, index_=None):
        
        
        return self.internalArray[php_int(index_)]
    # end def offsetget
    #// 
    #// @param string|int $index
    #// @param mixed $newval
    #// @psalm-suppress MixedAssignment
    #//
    def offsetset(self, index_=None, newval_=None):
        
        
        self.internalArray[php_int(index_)] = newval_
    # end def offsetset
    #// 
    #// @param string|int $index
    #//
    def offsetunset(self, index_=None):
        
        
        self.internalArray[php_int(index_)] = None
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
        result_ = next(self.internalArray) != False
        php_prev(self.internalArray)
        return result_
    # end def valid
    #// 
    #// Do nothing.
    #//
    def __wakeup(self):
        
        
        pass
    # end def __wakeup
# end class SplFixedArray
