#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_ChaCha20_IetfCtx", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_ChaCha20_IetfCtx
#//
class ParagonIE_Sodium_Core_ChaCha20_IetfCtx(ParagonIE_Sodium_Core_ChaCha20_Ctx):
    #// 
    #// ParagonIE_Sodium_Core_ChaCha20_IetfCtx constructor.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $key     ChaCha20 key.
    #// @param string $iv      Initialization Vector (a.k.a. nonce).
    #// @param string $counter The initial counter value.
    #// Defaults to 4 0x00 bytes.
    #// @throws InvalidArgumentException
    #// @throws TypeError
    #//
    def __init__(self, key_="", iv_="", counter_=""):
        
        
        if self.strlen(iv_) != 12:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("ChaCha20 expects a 96-bit nonce in IETF mode."))
        # end if
        super().__init__(key_, self.substr(iv_, 0, 8), counter_)
        if (not php_empty(lambda : counter_)):
            self.container[12] = self.load_4(self.substr(counter_, 0, 4))
        # end if
        self.container[13] = self.load_4(self.substr(iv_, 0, 4))
        self.container[14] = self.load_4(self.substr(iv_, 4, 4))
        self.container[15] = self.load_4(self.substr(iv_, 8, 4))
    # end def __init__
# end class ParagonIE_Sodium_Core_ChaCha20_IetfCtx
