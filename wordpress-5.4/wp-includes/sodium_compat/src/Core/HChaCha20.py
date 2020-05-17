#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def hchacha20(self, in_="", key_="", c_=None):
        if c_ is None:
            c_ = None
        # end if
        
        ctx_ = Array()
        if c_ == None:
            ctx_[0] = 1634760805
            ctx_[1] = 857760878
            ctx_[2] = 2036477234
            ctx_[3] = 1797285236
        else:
            ctx_[0] = self.load_4(self.substr(c_, 0, 4))
            ctx_[1] = self.load_4(self.substr(c_, 4, 4))
            ctx_[2] = self.load_4(self.substr(c_, 8, 4))
            ctx_[3] = self.load_4(self.substr(c_, 12, 4))
        # end if
        ctx_[4] = self.load_4(self.substr(key_, 0, 4))
        ctx_[5] = self.load_4(self.substr(key_, 4, 4))
        ctx_[6] = self.load_4(self.substr(key_, 8, 4))
        ctx_[7] = self.load_4(self.substr(key_, 12, 4))
        ctx_[8] = self.load_4(self.substr(key_, 16, 4))
        ctx_[9] = self.load_4(self.substr(key_, 20, 4))
        ctx_[10] = self.load_4(self.substr(key_, 24, 4))
        ctx_[11] = self.load_4(self.substr(key_, 28, 4))
        ctx_[12] = self.load_4(self.substr(in_, 0, 4))
        ctx_[13] = self.load_4(self.substr(in_, 4, 4))
        ctx_[14] = self.load_4(self.substr(in_, 8, 4))
        ctx_[15] = self.load_4(self.substr(in_, 12, 4))
        return self.hchacha20bytes(ctx_)
    # end def hchacha20
    #// 
    #// @param array $ctx
    #// @return string
    #// @throws TypeError
    #//
    def hchacha20bytes(self, ctx_=None):
        
        
        x0_ = php_int(ctx_[0])
        x1_ = php_int(ctx_[1])
        x2_ = php_int(ctx_[2])
        x3_ = php_int(ctx_[3])
        x4_ = php_int(ctx_[4])
        x5_ = php_int(ctx_[5])
        x6_ = php_int(ctx_[6])
        x7_ = php_int(ctx_[7])
        x8_ = php_int(ctx_[8])
        x9_ = php_int(ctx_[9])
        x10_ = php_int(ctx_[10])
        x11_ = php_int(ctx_[11])
        x12_ = php_int(ctx_[12])
        x13_ = php_int(ctx_[13])
        x14_ = php_int(ctx_[14])
        x15_ = php_int(ctx_[15])
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
        return self.store32_le(php_int(x0_ & 4294967295)) + self.store32_le(php_int(x1_ & 4294967295)) + self.store32_le(php_int(x2_ & 4294967295)) + self.store32_le(php_int(x3_ & 4294967295)) + self.store32_le(php_int(x12_ & 4294967295)) + self.store32_le(php_int(x13_ & 4294967295)) + self.store32_le(php_int(x14_ & 4294967295)) + self.store32_le(php_int(x15_ & 4294967295))
    # end def hchacha20bytes
# end class ParagonIE_Sodium_Core_HChaCha20
