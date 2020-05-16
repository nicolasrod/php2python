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
if php_class_exists("ParagonIE_Sodium_Core_Curve25519_Fe", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Curve25519_Fe
#// 
#// This represents a Field Element
#//
class ParagonIE_Sodium_Core_Curve25519_Fe():
    container = Array()
    size = 10
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, int> $array
    #// @param bool $save_indexes
    #// @return self
    #//
    @classmethod
    def fromarray(self, array=None, save_indexes=None):
        
        count = php_count(array)
        if save_indexes:
            keys = php_array_keys(array)
        else:
            keys = range(0, count - 1)
        # end if
        array = php_array_values(array)
        #// @var array<int, int> $keys
        obj = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        if save_indexes:
            i = 0
            while i < count:
                
                obj.offsetset(keys[i], array[i])
                i += 1
            # end while
        else:
            i = 0
            while i < count:
                
                obj.offsetset(i, array[i])
                i += 1
            # end while
        # end if
        return obj
    # end def fromarray
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int|null $offset
    #// @param int $value
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetset(self, offset=None, value=None):
        
        if (not php_is_int(value)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        if is_null(offset):
            self.container[-1] = value
        else:
            self.container[offset] = value
        # end if
    # end def offsetset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return bool
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetexists(self, offset=None):
        
        return (php_isset(lambda : self.container[offset]))
    # end def offsetexists
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetunset(self, offset=None):
        
        self.container[offset] = None
    # end def offsetunset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return int
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset=None):
        
        if (not (php_isset(lambda : self.container[offset]))):
            self.container[offset] = 0
        # end if
        return php_int(self.container[offset])
    # end def offsetget
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return array
    #//
    def __debuginfo(self):
        
        return Array(php_implode(", ", self.container))
    # end def __debuginfo
# end class ParagonIE_Sodium_Core_Curve25519_Fe
