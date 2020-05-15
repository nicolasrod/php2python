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
if php_class_exists("ParagonIE_Sodium_Core_XSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_XSalsa20
#//
class ParagonIE_Sodium_Core_XSalsa20(ParagonIE_Sodium_Core_HSalsa20):
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
    def xsalsa20(self, len=None, nonce=None, key=None):
        
        ret = self.salsa20(len, self.substr(nonce, 16, 8), self.hsalsa20(nonce, key))
        return ret
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
    def xsalsa20_xor(self, message=None, nonce=None, key=None):
        
        return self.xorstrings(message, self.xsalsa20(self.strlen(message), nonce, key))
    # end def xsalsa20_xor
# end class ParagonIE_Sodium_Core_XSalsa20
