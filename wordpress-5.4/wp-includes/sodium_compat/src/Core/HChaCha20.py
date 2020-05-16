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
if php_class_exists("ParagonIE_Sodium_Core_HChaCha20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_HChaCha20
#//
class ParagonIE_Sodium_Core_HChaCha20(ParagonIE_Sodium_Core_ChaCha20):
    #// 
    #// @param string $in
    #// @param string $key
    #// @param string|null $c
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def hchacha20(self, in_="", key="", c=None):
        
        ctx = Array()
        if c == None:
            ctx[0] = 1634760805
            ctx[1] = 857760878
            ctx[2] = 2036477234
            ctx[3] = 1797285236
        else:
            ctx[0] = self.load_4(self.substr(c, 0, 4))
            ctx[1] = self.load_4(self.substr(c, 4, 4))
            ctx[2] = self.load_4(self.substr(c, 8, 4))
            ctx[3] = self.load_4(self.substr(c, 12, 4))
        # end if
        ctx[4] = self.load_4(self.substr(key, 0, 4))
        ctx[5] = self.load_4(self.substr(key, 4, 4))
        ctx[6] = self.load_4(self.substr(key, 8, 4))
        ctx[7] = self.load_4(self.substr(key, 12, 4))
        ctx[8] = self.load_4(self.substr(key, 16, 4))
        ctx[9] = self.load_4(self.substr(key, 20, 4))
        ctx[10] = self.load_4(self.substr(key, 24, 4))
        ctx[11] = self.load_4(self.substr(key, 28, 4))
        ctx[12] = self.load_4(self.substr(in_, 0, 4))
        ctx[13] = self.load_4(self.substr(in_, 4, 4))
        ctx[14] = self.load_4(self.substr(in_, 8, 4))
        ctx[15] = self.load_4(self.substr(in_, 12, 4))
        return self.hchacha20bytes(ctx)
    # end def hchacha20
    #// 
    #// @param array $ctx
    #// @return string
    #// @throws TypeError
    #//
    def hchacha20bytes(self, ctx=None):
        
        x0 = php_int(ctx[0])
        x1 = php_int(ctx[1])
        x2 = php_int(ctx[2])
        x3 = php_int(ctx[3])
        x4 = php_int(ctx[4])
        x5 = php_int(ctx[5])
        x6 = php_int(ctx[6])
        x7 = php_int(ctx[7])
        x8 = php_int(ctx[8])
        x9 = php_int(ctx[9])
        x10 = php_int(ctx[10])
        x11 = php_int(ctx[11])
        x12 = php_int(ctx[12])
        x13 = php_int(ctx[13])
        x14 = php_int(ctx[14])
        x15 = php_int(ctx[15])
        i = 0
        while i < 10:
            
            #// # QUARTERROUND( x0,  x4,  x8,  x12)
            x0, x4, x8, x12 = self.quarterround(x0, x4, x8, x12)
            #// # QUARTERROUND( x1,  x5,  x9,  x13)
            x1, x5, x9, x13 = self.quarterround(x1, x5, x9, x13)
            #// # QUARTERROUND( x2,  x6,  x10,  x14)
            x2, x6, x10, x14 = self.quarterround(x2, x6, x10, x14)
            #// # QUARTERROUND( x3,  x7,  x11,  x15)
            x3, x7, x11, x15 = self.quarterround(x3, x7, x11, x15)
            #// # QUARTERROUND( x0,  x5,  x10,  x15)
            x0, x5, x10, x15 = self.quarterround(x0, x5, x10, x15)
            #// # QUARTERROUND( x1,  x6,  x11,  x12)
            x1, x6, x11, x12 = self.quarterround(x1, x6, x11, x12)
            #// # QUARTERROUND( x2,  x7,  x8,  x13)
            x2, x7, x8, x13 = self.quarterround(x2, x7, x8, x13)
            #// # QUARTERROUND( x3,  x4,  x9,  x14)
            x3, x4, x9, x14 = self.quarterround(x3, x4, x9, x14)
            i += 1
        # end while
        return self.store32_le(php_int(x0 & 4294967295)) + self.store32_le(php_int(x1 & 4294967295)) + self.store32_le(php_int(x2 & 4294967295)) + self.store32_le(php_int(x3 & 4294967295)) + self.store32_le(php_int(x12 & 4294967295)) + self.store32_le(php_int(x13 & 4294967295)) + self.store32_le(php_int(x14 & 4294967295)) + self.store32_le(php_int(x15 & 4294967295))
    # end def hchacha20bytes
# end class ParagonIE_Sodium_Core_HChaCha20
