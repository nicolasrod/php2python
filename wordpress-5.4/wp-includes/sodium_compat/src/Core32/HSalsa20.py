#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_HSalsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_HSalsa20
#//
class ParagonIE_Sodium_Core32_HSalsa20(ParagonIE_Sodium_Core32_Salsa20):
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
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def hsalsa20(self, in_=None, k_=None, c_=None):
        
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int32 $x0
        #// @var ParagonIE_Sodium_Core32_Int32 $x1
        #// @var ParagonIE_Sodium_Core32_Int32 $x2
        #// @var ParagonIE_Sodium_Core32_Int32 $x3
        #// @var ParagonIE_Sodium_Core32_Int32 $x4
        #// @var ParagonIE_Sodium_Core32_Int32 $x5
        #// @var ParagonIE_Sodium_Core32_Int32 $x6
        #// @var ParagonIE_Sodium_Core32_Int32 $x7
        #// @var ParagonIE_Sodium_Core32_Int32 $x8
        #// @var ParagonIE_Sodium_Core32_Int32 $x9
        #// @var ParagonIE_Sodium_Core32_Int32 $x10
        #// @var ParagonIE_Sodium_Core32_Int32 $x11
        #// @var ParagonIE_Sodium_Core32_Int32 $x12
        #// @var ParagonIE_Sodium_Core32_Int32 $x13
        #// @var ParagonIE_Sodium_Core32_Int32 $x14
        #// @var ParagonIE_Sodium_Core32_Int32 $x15
        #// @var ParagonIE_Sodium_Core32_Int32 $j0
        #// @var ParagonIE_Sodium_Core32_Int32 $j1
        #// @var ParagonIE_Sodium_Core32_Int32 $j2
        #// @var ParagonIE_Sodium_Core32_Int32 $j3
        #// @var ParagonIE_Sodium_Core32_Int32 $j4
        #// @var ParagonIE_Sodium_Core32_Int32 $j5
        #// @var ParagonIE_Sodium_Core32_Int32 $j6
        #// @var ParagonIE_Sodium_Core32_Int32 $j7
        #// @var ParagonIE_Sodium_Core32_Int32 $j8
        #// @var ParagonIE_Sodium_Core32_Int32 $j9
        #// @var ParagonIE_Sodium_Core32_Int32 $j10
        #// @var ParagonIE_Sodium_Core32_Int32 $j11
        #// @var ParagonIE_Sodium_Core32_Int32 $j12
        #// @var ParagonIE_Sodium_Core32_Int32 $j13
        #// @var ParagonIE_Sodium_Core32_Int32 $j14
        #// @var ParagonIE_Sodium_Core32_Int32 $j15
        #//
        if self.strlen(k_) < 32:
            raise php_new_class("RangeException", lambda : RangeException("Key must be 32 bytes long"))
        # end if
        if c_ == None:
            x0_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
            x5_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
            x10_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
            x15_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        else:
            x0_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 0, 4))
            x5_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 4, 4))
            x10_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 8, 4))
            x15_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c_, 12, 4))
        # end if
        x1_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 0, 4))
        x2_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 4, 4))
        x3_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 8, 4))
        x4_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 12, 4))
        x6_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 0, 4))
        x7_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 4, 4))
        x8_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 8, 4))
        x9_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 12, 4))
        x11_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 16, 4))
        x12_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 20, 4))
        x13_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 24, 4))
        x14_ = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k_, 28, 4))
        i_ = self.ROUNDS
        while i_ > 0:
            
            x4_ = x4_.xorint32(x0_.addint32(x12_).rotateleft(7))
            x8_ = x8_.xorint32(x4_.addint32(x0_).rotateleft(9))
            x12_ = x12_.xorint32(x8_.addint32(x4_).rotateleft(13))
            x0_ = x0_.xorint32(x12_.addint32(x8_).rotateleft(18))
            x9_ = x9_.xorint32(x5_.addint32(x1_).rotateleft(7))
            x13_ = x13_.xorint32(x9_.addint32(x5_).rotateleft(9))
            x1_ = x1_.xorint32(x13_.addint32(x9_).rotateleft(13))
            x5_ = x5_.xorint32(x1_.addint32(x13_).rotateleft(18))
            x14_ = x14_.xorint32(x10_.addint32(x6_).rotateleft(7))
            x2_ = x2_.xorint32(x14_.addint32(x10_).rotateleft(9))
            x6_ = x6_.xorint32(x2_.addint32(x14_).rotateleft(13))
            x10_ = x10_.xorint32(x6_.addint32(x2_).rotateleft(18))
            x3_ = x3_.xorint32(x15_.addint32(x11_).rotateleft(7))
            x7_ = x7_.xorint32(x3_.addint32(x15_).rotateleft(9))
            x11_ = x11_.xorint32(x7_.addint32(x3_).rotateleft(13))
            x15_ = x15_.xorint32(x11_.addint32(x7_).rotateleft(18))
            x1_ = x1_.xorint32(x0_.addint32(x3_).rotateleft(7))
            x2_ = x2_.xorint32(x1_.addint32(x0_).rotateleft(9))
            x3_ = x3_.xorint32(x2_.addint32(x1_).rotateleft(13))
            x0_ = x0_.xorint32(x3_.addint32(x2_).rotateleft(18))
            x6_ = x6_.xorint32(x5_.addint32(x4_).rotateleft(7))
            x7_ = x7_.xorint32(x6_.addint32(x5_).rotateleft(9))
            x4_ = x4_.xorint32(x7_.addint32(x6_).rotateleft(13))
            x5_ = x5_.xorint32(x4_.addint32(x7_).rotateleft(18))
            x11_ = x11_.xorint32(x10_.addint32(x9_).rotateleft(7))
            x8_ = x8_.xorint32(x11_.addint32(x10_).rotateleft(9))
            x9_ = x9_.xorint32(x8_.addint32(x11_).rotateleft(13))
            x10_ = x10_.xorint32(x9_.addint32(x8_).rotateleft(18))
            x12_ = x12_.xorint32(x15_.addint32(x14_).rotateleft(7))
            x13_ = x13_.xorint32(x12_.addint32(x15_).rotateleft(9))
            x14_ = x14_.xorint32(x13_.addint32(x12_).rotateleft(13))
            x15_ = x15_.xorint32(x14_.addint32(x13_).rotateleft(18))
            i_ -= 2
        # end while
        return x0_.toreversestring() + x5_.toreversestring() + x10_.toreversestring() + x15_.toreversestring() + x6_.toreversestring() + x7_.toreversestring() + x8_.toreversestring() + x9_.toreversestring()
    # end def hsalsa20
# end class ParagonIE_Sodium_Core32_HSalsa20
