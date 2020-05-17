#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_XSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_XSalsa20
#//
class ParagonIE_Sodium_Core32_XSalsa20(ParagonIE_Sodium_Core32_HSalsa20):
    #// 
    #// Expand a key and nonce into an xsalsa20 keystream.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $len
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def xsalsa20(self, len_=None, nonce_=None, key_=None):
        
        
        ret_ = self.salsa20(len_, self.substr(nonce_, 16, 8), self.hsalsa20(nonce_, key_))
        return ret_
    # end def xsalsa20
    #// 
    #// Encrypt a string with XSalsa20. Doesn't provide integrity.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $message
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def xsalsa20_xor(self, message_=None, nonce_=None, key_=None):
        
        
        return self.xorstrings(message_, self.xsalsa20(self.strlen(message_), nonce_, key_))
    # end def xsalsa20_xor
# end class ParagonIE_Sodium_Core32_XSalsa20
