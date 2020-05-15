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
if php_class_exists("ParagonIE_Sodium_Core_ChaCha20_Ctx", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_ChaCha20_Ctx
#//
class ParagonIE_Sodium_Core_ChaCha20_Ctx(ParagonIE_Sodium_Core_Util):
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
    #// @throws TypeError
    #//
    def __init__(self, key="", iv="", counter=""):
        
        if self.strlen(key) != 32:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("ChaCha20 expects a 256-bit key."))
        # end if
        if self.strlen(iv) != 8:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("ChaCha20 expects a 64-bit nonce."))
        # end if
        self.container = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        #// "expand 32-byte k" as per ChaCha20 spec
        self.container[0] = 1634760805
        self.container[1] = 857760878
        self.container[2] = 2036477234
        self.container[3] = 1797285236
        self.container[4] = self.load_4(self.substr(key, 0, 4))
        self.container[5] = self.load_4(self.substr(key, 4, 4))
        self.container[6] = self.load_4(self.substr(key, 8, 4))
        self.container[7] = self.load_4(self.substr(key, 12, 4))
        self.container[8] = self.load_4(self.substr(key, 16, 4))
        self.container[9] = self.load_4(self.substr(key, 20, 4))
        self.container[10] = self.load_4(self.substr(key, 24, 4))
        self.container[11] = self.load_4(self.substr(key, 28, 4))
        if php_empty(lambda : counter):
            self.container[12] = 0
            self.container[13] = 0
        else:
            self.container[12] = self.load_4(self.substr(counter, 0, 4))
            self.container[13] = self.load_4(self.substr(counter, 4, 4))
        # end if
        self.container[14] = self.load_4(self.substr(iv, 0, 4))
        self.container[15] = self.load_4(self.substr(iv, 4, 4))
    # end def __init__
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @param int $value
    #// @return void
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetset(self, offset=None, value=None):
        
        if (not php_is_int(offset)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        if (not php_is_int(value)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer"))
        # end if
        self.container[offset] = value
    # end def offsetset
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $offset
    #// @return bool
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
    #// @return mixed|null
    #// @psalm-suppress MixedArrayOffset
    #//
    def offsetget(self, offset=None):
        
        return self.container[offset] if (php_isset(lambda : self.container[offset])) else None
    # end def offsetget
# end class ParagonIE_Sodium_Core_ChaCha20_Ctx
