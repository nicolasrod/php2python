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
if php_class_exists("ParagonIE_Sodium_Core32_HChaCha20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_HChaCha20
#//
class ParagonIE_Sodium_Core32_HChaCha20(ParagonIE_Sodium_Core32_ChaCha20):
    #// 
    #// @param string $in
    #// @param string $key
    #// @param string|null $c
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def hchacha20(self, in_="", key="", c=None):
        
        ctx = Array()
        if c == None:
            ctx[0] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
            ctx[1] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
            ctx[2] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
            ctx[3] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        else:
            ctx[0] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 0, 4))
            ctx[1] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 4, 4))
            ctx[2] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 8, 4))
            ctx[3] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 12, 4))
        # end if
        ctx[4] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 0, 4))
        ctx[5] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 4, 4))
        ctx[6] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 8, 4))
        ctx[7] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 12, 4))
        ctx[8] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 16, 4))
        ctx[9] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 20, 4))
        ctx[10] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 24, 4))
        ctx[11] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key, 28, 4))
        ctx[12] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 0, 4))
        ctx[13] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 4, 4))
        ctx[14] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 8, 4))
        ctx[15] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 12, 4))
        return self.hchacha20bytes(ctx)
    # end def hchacha20
    #// 
    #// @param array $ctx
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def hchacha20bytes(self, ctx=None):
        
        #// @var ParagonIE_Sodium_Core32_Int32 $x0
        x0 = ctx[0]
        #// @var ParagonIE_Sodium_Core32_Int32 $x1
        x1 = ctx[1]
        #// @var ParagonIE_Sodium_Core32_Int32 $x2
        x2 = ctx[2]
        #// @var ParagonIE_Sodium_Core32_Int32 $x3
        x3 = ctx[3]
        #// @var ParagonIE_Sodium_Core32_Int32 $x4
        x4 = ctx[4]
        #// @var ParagonIE_Sodium_Core32_Int32 $x5
        x5 = ctx[5]
        #// @var ParagonIE_Sodium_Core32_Int32 $x6
        x6 = ctx[6]
        #// @var ParagonIE_Sodium_Core32_Int32 $x7
        x7 = ctx[7]
        #// @var ParagonIE_Sodium_Core32_Int32 $x8
        x8 = ctx[8]
        #// @var ParagonIE_Sodium_Core32_Int32 $x9
        x9 = ctx[9]
        #// @var ParagonIE_Sodium_Core32_Int32 $x10
        x10 = ctx[10]
        #// @var ParagonIE_Sodium_Core32_Int32 $x11
        x11 = ctx[11]
        #// @var ParagonIE_Sodium_Core32_Int32 $x12
        x12 = ctx[12]
        #// @var ParagonIE_Sodium_Core32_Int32 $x13
        x13 = ctx[13]
        #// @var ParagonIE_Sodium_Core32_Int32 $x14
        x14 = ctx[14]
        #// @var ParagonIE_Sodium_Core32_Int32 $x15
        x15 = ctx[15]
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
        return x0.toreversestring() + x1.toreversestring() + x2.toreversestring() + x3.toreversestring() + x12.toreversestring() + x13.toreversestring() + x14.toreversestring() + x15.toreversestring()
    # end def hchacha20bytes
# end class ParagonIE_Sodium_Core32_HChaCha20
