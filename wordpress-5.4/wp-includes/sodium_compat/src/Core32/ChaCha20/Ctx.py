#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_ChaCha20_Ctx", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_ChaCha20_Ctx
#//
class ParagonIE_Sodium_Core32_ChaCha20_Ctx(ParagonIE_Sodium_Core32_Util,ArrayAccess):
    #// 
    #// @var SplFixedArray internally, <int, ParagonIE_Sodium_Core32_Int32>
    #//
    container = Array()
    #// 
    #// ParagonIE_Sodium_Core_ChaCha20_Ctx constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $key     ChaCha20 key.
    #// @param string $iv      Initialization Vector (a.k.a. nonce).
    #// @param string $counter The initial counter value.
    #// Defaults to 8 0x00 bytes.
    #// @throws InvalidArgumentException
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def __init__(self, key_="", iv_="", counter_=""):
        
        
        if self.strlen(key_) != 32:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("ChaCha20 expects a 256-bit key."))
        # end if
        if self.strlen(iv_) != 8:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("ChaCha20 expects a 64-bit nonce."))
        # end if
        self.container = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        #// "expand 32-byte k" as per ChaCha20 spec
        self.container[0] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
        self.container[1] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
        self.container[2] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
        self.container[3] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        self.container[4] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 0, 4))
        self.container[5] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 4, 4))
        self.container[6] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 8, 4))
        self.container[7] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 12, 4))
        self.container[8] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 16, 4))
        self.container[9] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 20, 4))
        self.container[10] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 24, 4))
        self.container[11] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 28, 4))
        if php_empty(lambda : counter_):
            self.container[12] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
            self.container[13] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        else:
            self.container[12] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(counter_, 0, 4))
            self.container[13] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(counter_, 4, 4))
        # end if
        self.container[14] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(iv_, 0, 4))
        self.container[15] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(iv_, 4, 4))
    # end def __init__
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @param int|ParagonIE_Sodium_Core32_Int32 $value
    #// @return void
    #//
    def offsetset(self, offset_=None, value_=None):
        
        
        if (not php_is_int(offset_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        if type(value_).__name__ == "ParagonIE_Sodium_Core32_Int32":
            pass
        else:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        self.container[offset_] = value_
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
    #// @return mixed|null
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset_=None):
        
        
        return self.container[offset_] if (php_isset(lambda : self.container[offset_])) else None
    # end def offsetget
# end class ParagonIE_Sodium_Core32_ChaCha20_Ctx
