#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    #// 
    #// @var array<int, int>
    #//
    container = Array()
    #// 
    #// @var int
    #//
    size = 10
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, int> $array
    #// @param bool $save_indexes
    #// @return self
    #//
    @classmethod
    def fromarray(self, array_=None, save_indexes_=None):
        
        
        count_ = php_count(array_)
        if save_indexes_:
            keys_ = php_array_keys(array_)
        else:
            keys_ = range(0, count_ - 1)
        # end if
        array_ = php_array_values(array_)
        #// @var array<int, int> $keys
        obj_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        if save_indexes_:
            i_ = 0
            while i_ < count_:
                
                obj_.offsetset(keys_[i_], array_[i_])
                i_ += 1
            # end while
        else:
            i_ = 0
            while i_ < count_:
                
                obj_.offsetset(i_, array_[i_])
                i_ += 1
            # end while
        # end if
        return obj_
    # end def fromarray
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int|null $offset
    #// @param int $value
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetset(self, offset_=None, value_=None):
        
        
        if (not php_is_int(value_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        if is_null(offset_):
            self.container[-1] = value_
        else:
            self.container[offset_] = value_
        # end if
    # end def offsetset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return bool
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetexists(self, offset_=None):
        
        
        return (php_isset(lambda : self.container[offset_]))
    # end def offsetexists
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetunset(self, offset_=None):
        
        
        self.container[offset_] = None
    # end def offsetunset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return int
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset_=None):
        
        
        if (not (php_isset(lambda : self.container[offset_]))):
            self.container[offset_] = 0
        # end if
        return php_int(self.container[offset_])
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
