#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Poly1305", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Poly1305
#//
class ParagonIE_Sodium_Core32_Poly1305(ParagonIE_Sodium_Core32_Util):
    BLOCK_SIZE = 16
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $m
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def onetimeauth(self, m_=None, key_=None):
        
        
        if self.strlen(key_) < 32:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Key must be 32 bytes long."))
        # end if
        state_ = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(self.substr(key_, 0, 32)))
        return state_.update(m_).finish()
    # end def onetimeauth
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $mac
    #// @param string $m
    #// @param string $key
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def onetimeauth_verify(self, mac_=None, m_=None, key_=None):
        
        
        if self.strlen(key_) < 32:
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Key must be 32 bytes long."))
        # end if
        state_ = php_new_class("ParagonIE_Sodium_Core32_Poly1305_State", lambda : ParagonIE_Sodium_Core32_Poly1305_State(self.substr(key_, 0, 32)))
        calc_ = state_.update(m_).finish()
        return self.verify_16(calc_, mac_)
    # end def onetimeauth_verify
# end class ParagonIE_Sodium_Core32_Poly1305
