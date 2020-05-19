#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Fe", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Fe
#// 
#// This represents a Field Element
#//
class ParagonIE_Sodium_Core32_Curve25519_Fe(ArrayAccess):
    #// 
    #// @var array<int, ParagonIE_Sodium_Core32_Int32>
    #//
    container = Array()
    #// 
    #// @var int
    #//
    size = 10
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, ParagonIE_Sodium_Core32_Int32> $array
    #// @param bool $save_indexes
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromarray(self, array_=None, save_indexes_=None):
        if save_indexes_ is None:
            save_indexes_ = None
        # end if
        
        count_ = php_count(array_)
        if save_indexes_:
            keys_ = php_array_keys(array_)
        else:
            keys_ = range(0, count_ - 1)
        # end if
        array_ = php_array_values(array_)
        obj_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        if save_indexes_:
            i_ = 0
            while i_ < count_:
                
                array_[i_].overflow = 0
                obj_.offsetset(keys_[i_], array_[i_])
                i_ += 1
            # end while
        else:
            i_ = 0
            while i_ < count_:
                
                array_[i_].overflow = 0
                obj_.offsetset(i_, array_[i_])
                i_ += 1
            # end while
        # end if
        return obj_
    # end def fromarray
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, int> $array
    #// @param bool $save_indexes
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromintarray(self, array_=None, save_indexes_=None):
        if save_indexes_ is None:
            save_indexes_ = None
        # end if
        
        count_ = php_count(array_)
        if save_indexes_:
            keys_ = php_array_keys(array_)
        else:
            keys_ = range(0, count_ - 1)
        # end if
        array_ = php_array_values(array_)
        set_ = Array()
        #// @var int $i
        #// @var int $v
        for i_,v_ in array_.items():
            set_[i_] = ParagonIE_Sodium_Core32_Int32.fromint(v_)
        # end for
        obj_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        if save_indexes_:
            i_ = 0
            while i_ < count_:
                
                set_[i_].overflow = 0
                obj_.offsetset(keys_[i_], set_[i_])
                i_ += 1
            # end while
        else:
            i_ = 0
            while i_ < count_:
                
                set_[i_].overflow = 0
                obj_.offsetset(i_, set_[i_])
                i_ += 1
            # end while
        # end if
        return obj_
    # end def fromintarray
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @param mixed $value
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def offsetset(self, offset_=None, value_=None):
        
        
        if (not type(value_).__name__ == "ParagonIE_Sodium_Core32_Int32"):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an instance of ParagonIE_Sodium_Core32_Int32"))
        # end if
        if php_is_null(offset_):
            self.container[-1] = value_
        else:
            ParagonIE_Sodium_Core32_Util.declarescalartype(offset_, "int", 1)
            self.container[php_int(offset_)] = value_
        # end if
    # end def offsetset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return bool
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetexists(self, offset_=None):
        
        
        return (php_isset(lambda : self.container[offset_]))
    # end def offsetexists
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetunset(self, offset_=None):
        
        
        self.container[offset_] = None
    # end def offsetunset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset_=None):
        
        
        if (not (php_isset(lambda : self.container[offset_]))):
            self.container[php_int(offset_)] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        # end if
        #// @var ParagonIE_Sodium_Core32_Int32 $get
        get_ = self.container[offset_]
        return get_
    # end def offsetget
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return array
    #//
    def __debuginfo(self):
        
        
        if php_empty(lambda : self.container):
            return Array()
        # end if
        c_ = Array(php_int(self.container[0].toint()), php_int(self.container[1].toint()), php_int(self.container[2].toint()), php_int(self.container[3].toint()), php_int(self.container[4].toint()), php_int(self.container[5].toint()), php_int(self.container[6].toint()), php_int(self.container[7].toint()), php_int(self.container[8].toint()), php_int(self.container[9].toint()))
        return Array(php_implode(", ", c_))
    # end def __debuginfo
# end class ParagonIE_Sodium_Core32_Curve25519_Fe
