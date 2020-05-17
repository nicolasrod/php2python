#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def hchacha20(self, in_="", key_="", c_=None):
        
        
        ctx_ = Array()
        if c_ == None:
            ctx_[0] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
            ctx_[1] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
            ctx_[2] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
            ctx_[3] = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        else:
            ctx_[0] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 0, 4))
            ctx_[1] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 4, 4))
            ctx_[2] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 8, 4))
            ctx_[3] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 12, 4))
        # end if
        ctx_[4] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 0, 4))
        ctx_[5] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 4, 4))
        ctx_[6] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 8, 4))
        ctx_[7] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 12, 4))
        ctx_[8] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 16, 4))
        ctx_[9] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 20, 4))
        ctx_[10] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 24, 4))
        ctx_[11] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(key_, 28, 4))
        ctx_[12] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 0, 4))
        ctx_[13] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 4, 4))
        ctx_[14] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 8, 4))
        ctx_[15] = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 12, 4))
        return self.hchacha20bytes(ctx_)
    # end def hchacha20
    #// 
    #// @param array $ctx
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def hchacha20bytes(self, ctx_=None):
        
        
        #// @var ParagonIE_Sodium_Core32_Int32 $x0
        x0_ = ctx_[0]
        #// @var ParagonIE_Sodium_Core32_Int32 $x1
        x1_ = ctx_[1]
        #// @var ParagonIE_Sodium_Core32_Int32 $x2
        x2_ = ctx_[2]
        #// @var ParagonIE_Sodium_Core32_Int32 $x3
        x3_ = ctx_[3]
        #// @var ParagonIE_Sodium_Core32_Int32 $x4
        x4_ = ctx_[4]
        #// @var ParagonIE_Sodium_Core32_Int32 $x5
        x5_ = ctx_[5]
        #// @var ParagonIE_Sodium_Core32_Int32 $x6
        x6_ = ctx_[6]
        #// @var ParagonIE_Sodium_Core32_Int32 $x7
        x7_ = ctx_[7]
        #// @var ParagonIE_Sodium_Core32_Int32 $x8
        x8_ = ctx_[8]
        #// @var ParagonIE_Sodium_Core32_Int32 $x9
        x9_ = ctx_[9]
        #// @var ParagonIE_Sodium_Core32_Int32 $x10
        x10_ = ctx_[10]
        #// @var ParagonIE_Sodium_Core32_Int32 $x11
        x11_ = ctx_[11]
        #// @var ParagonIE_Sodium_Core32_Int32 $x12
        x12_ = ctx_[12]
        #// @var ParagonIE_Sodium_Core32_Int32 $x13
        x13_ = ctx_[13]
        #// @var ParagonIE_Sodium_Core32_Int32 $x14
        x14_ = ctx_[14]
        #// @var ParagonIE_Sodium_Core32_Int32 $x15
        x15_ = ctx_[15]
        i_ = 0
        while i_ < 10:
            
            #// # QUARTERROUND( x0,  x4,  x8,  x12)
            x0_, x4_, x8_, x12_ = self.quarterround(x0_, x4_, x8_, x12_)
            #// # QUARTERROUND( x1,  x5,  x9,  x13)
            x1_, x5_, x9_, x13_ = self.quarterround(x1_, x5_, x9_, x13_)
            #// # QUARTERROUND( x2,  x6,  x10,  x14)
            x2_, x6_, x10_, x14_ = self.quarterround(x2_, x6_, x10_, x14_)
            #// # QUARTERROUND( x3,  x7,  x11,  x15)
            x3_, x7_, x11_, x15_ = self.quarterround(x3_, x7_, x11_, x15_)
            #// # QUARTERROUND( x0,  x5,  x10,  x15)
            x0_, x5_, x10_, x15_ = self.quarterround(x0_, x5_, x10_, x15_)
            #// # QUARTERROUND( x1,  x6,  x11,  x12)
            x1_, x6_, x11_, x12_ = self.quarterround(x1_, x6_, x11_, x12_)
            #// # QUARTERROUND( x2,  x7,  x8,  x13)
            x2_, x7_, x8_, x13_ = self.quarterround(x2_, x7_, x8_, x13_)
            #// # QUARTERROUND( x3,  x4,  x9,  x14)
            x3_, x4_, x9_, x14_ = self.quarterround(x3_, x4_, x9_, x14_)
            i_ += 1
        # end while
        return x0_.toreversestring() + x1_.toreversestring() + x2_.toreversestring() + x3_.toreversestring() + x12_.toreversestring() + x13_.toreversestring() + x14_.toreversestring() + x15_.toreversestring()
    # end def hchacha20bytes
# end class ParagonIE_Sodium_Core32_HChaCha20
