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
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519_Fe", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519_Fe
#// 
#// This represents a Field Element
#//
class ParagonIE_Sodium_Core32_Curve25519_Fe():
    container = Array()
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
    def fromarray(self, array=None, save_indexes=None):
        
        count = php_count(array)
        if save_indexes:
            keys = php_array_keys(array)
        else:
            keys = range(0, count - 1)
        # end if
        array = php_array_values(array)
        obj = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        if save_indexes:
            i = 0
            while i < count:
                
                array[i].overflow = 0
                obj.offsetset(keys[i], array[i])
                i += 1
            # end while
        else:
            i = 0
            while i < count:
                
                array[i].overflow = 0
                obj.offsetset(i, array[i])
                i += 1
            # end while
        # end if
        return obj
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
    def fromintarray(self, array=None, save_indexes=None):
        
        count = php_count(array)
        if save_indexes:
            keys = php_array_keys(array)
        else:
            keys = range(0, count - 1)
        # end if
        array = php_array_values(array)
        set = Array()
        #// @var int $i
        #// @var int $v
        for i,v in array:
            set[i] = ParagonIE_Sodium_Core32_Int32.fromint(v)
        # end for
        obj = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        if save_indexes:
            i = 0
            while i < count:
                
                set[i].overflow = 0
                obj.offsetset(keys[i], set[i])
                i += 1
            # end while
        else:
            i = 0
            while i < count:
                
                set[i].overflow = 0
                obj.offsetset(i, set[i])
                i += 1
            # end while
        # end if
        return obj
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
    def offsetset(self, offset=None, value=None):
        
        if (not type(value).__name__ == "ParagonIE_Sodium_Core32_Int32"):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an instance of ParagonIE_Sodium_Core32_Int32"))
        # end if
        if php_is_null(offset):
            self.container[-1] = value
        else:
            ParagonIE_Sodium_Core32_Util.declarescalartype(offset, "int", 1)
            self.container[int(offset)] = value
        # end if
    # end def offsetset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return bool
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetexists(self, offset=None):
        
        return (php_isset(lambda : self.container[offset]))
    # end def offsetexists
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetunset(self, offset=None):
        
        self.container[offset] = None
    # end def offsetunset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param mixed $offset
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset=None):
        
        if (not (php_isset(lambda : self.container[offset]))):
            self.container[int(offset)] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        # end if
        #// @var ParagonIE_Sodium_Core32_Int32 $get
        get = self.container[offset]
        return get
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
        c = Array(int(self.container[0].toint()), int(self.container[1].toint()), int(self.container[2].toint()), int(self.container[3].toint()), int(self.container[4].toint()), int(self.container[5].toint()), int(self.container[6].toint()), int(self.container[7].toint()), int(self.container[8].toint()), int(self.container[9].toint()))
        return Array(php_implode(", ", c))
    # end def __debuginfo
# end class ParagonIE_Sodium_Core32_Curve25519_Fe
