#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_HSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_HSalsa20
#//
class ParagonIE_Sodium_Core_HSalsa20(ParagonIE_Sodium_Core_Salsa20):
    #// 
    #// Calculate an hsalsa20 hash of a single block
    #// 
    #// HSalsa20 doesn't have a counter and will never be used for more than
    #// one block (used to derive a subkey for xsalsa20).
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $in
    #// @param string $k
    #// @param string|null $c
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def hsalsa20(self, in_=None, k_=None, c_=None):
        if c_ is None:
            c_ = None
        # end if
        
        if c_ == None:
            x0_ = 1634760805
            x5_ = 857760878
            x10_ = 2036477234
            x15_ = 1797285236
        else:
            x0_ = self.load_4(self.substr(c_, 0, 4))
            x5_ = self.load_4(self.substr(c_, 4, 4))
            x10_ = self.load_4(self.substr(c_, 8, 4))
            x15_ = self.load_4(self.substr(c_, 12, 4))
        # end if
        x1_ = self.load_4(self.substr(k_, 0, 4))
        x2_ = self.load_4(self.substr(k_, 4, 4))
        x3_ = self.load_4(self.substr(k_, 8, 4))
        x4_ = self.load_4(self.substr(k_, 12, 4))
        x11_ = self.load_4(self.substr(k_, 16, 4))
        x12_ = self.load_4(self.substr(k_, 20, 4))
        x13_ = self.load_4(self.substr(k_, 24, 4))
        x14_ = self.load_4(self.substr(k_, 28, 4))
        x6_ = self.load_4(self.substr(in_, 0, 4))
        x7_ = self.load_4(self.substr(in_, 4, 4))
        x8_ = self.load_4(self.substr(in_, 8, 4))
        x9_ = self.load_4(self.substr(in_, 12, 4))
        i_ = self.ROUNDS
        while i_ > 0:
            
            x4_ ^= self.rotate(x0_ + x12_, 7)
            x8_ ^= self.rotate(x4_ + x0_, 9)
            x12_ ^= self.rotate(x8_ + x4_, 13)
            x0_ ^= self.rotate(x12_ + x8_, 18)
            x9_ ^= self.rotate(x5_ + x1_, 7)
            x13_ ^= self.rotate(x9_ + x5_, 9)
            x1_ ^= self.rotate(x13_ + x9_, 13)
            x5_ ^= self.rotate(x1_ + x13_, 18)
            x14_ ^= self.rotate(x10_ + x6_, 7)
            x2_ ^= self.rotate(x14_ + x10_, 9)
            x6_ ^= self.rotate(x2_ + x14_, 13)
            x10_ ^= self.rotate(x6_ + x2_, 18)
            x3_ ^= self.rotate(x15_ + x11_, 7)
            x7_ ^= self.rotate(x3_ + x15_, 9)
            x11_ ^= self.rotate(x7_ + x3_, 13)
            x15_ ^= self.rotate(x11_ + x7_, 18)
            x1_ ^= self.rotate(x0_ + x3_, 7)
            x2_ ^= self.rotate(x1_ + x0_, 9)
            x3_ ^= self.rotate(x2_ + x1_, 13)
            x0_ ^= self.rotate(x3_ + x2_, 18)
            x6_ ^= self.rotate(x5_ + x4_, 7)
            x7_ ^= self.rotate(x6_ + x5_, 9)
            x4_ ^= self.rotate(x7_ + x6_, 13)
            x5_ ^= self.rotate(x4_ + x7_, 18)
            x11_ ^= self.rotate(x10_ + x9_, 7)
            x8_ ^= self.rotate(x11_ + x10_, 9)
            x9_ ^= self.rotate(x8_ + x11_, 13)
            x10_ ^= self.rotate(x9_ + x8_, 18)
            x12_ ^= self.rotate(x15_ + x14_, 7)
            x13_ ^= self.rotate(x12_ + x15_, 9)
            x14_ ^= self.rotate(x13_ + x12_, 13)
            x15_ ^= self.rotate(x14_ + x13_, 18)
            i_ -= 2
        # end while
        return self.store32_le(x0_) + self.store32_le(x5_) + self.store32_le(x10_) + self.store32_le(x15_) + self.store32_le(x6_) + self.store32_le(x7_) + self.store32_le(x8_) + self.store32_le(x9_)
    # end def hsalsa20
# end class ParagonIE_Sodium_Core_HSalsa20
