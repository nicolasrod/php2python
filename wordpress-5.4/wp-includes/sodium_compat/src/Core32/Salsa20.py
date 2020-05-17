#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Salsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Salsa20
#//
class ParagonIE_Sodium_Core32_Salsa20(ParagonIE_Sodium_Core32_Util):
    ROUNDS = 20
    #// 
    #// Calculate an salsa20 hash of a single block
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
    def core_salsa20(self, in_=None, k_=None, c_=None):
        
        
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
        j0_ = copy.deepcopy(x0_)
        j1_ = copy.deepcopy(x1_)
        j2_ = copy.deepcopy(x2_)
        j3_ = copy.deepcopy(x3_)
        j4_ = copy.deepcopy(x4_)
        j5_ = copy.deepcopy(x5_)
        j6_ = copy.deepcopy(x6_)
        j7_ = copy.deepcopy(x7_)
        j8_ = copy.deepcopy(x8_)
        j9_ = copy.deepcopy(x9_)
        j10_ = copy.deepcopy(x10_)
        j11_ = copy.deepcopy(x11_)
        j12_ = copy.deepcopy(x12_)
        j13_ = copy.deepcopy(x13_)
        j14_ = copy.deepcopy(x14_)
        j15_ = copy.deepcopy(x15_)
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
        x0_ = x0_.addint32(j0_)
        x1_ = x1_.addint32(j1_)
        x2_ = x2_.addint32(j2_)
        x3_ = x3_.addint32(j3_)
        x4_ = x4_.addint32(j4_)
        x5_ = x5_.addint32(j5_)
        x6_ = x6_.addint32(j6_)
        x7_ = x7_.addint32(j7_)
        x8_ = x8_.addint32(j8_)
        x9_ = x9_.addint32(j9_)
        x10_ = x10_.addint32(j10_)
        x11_ = x11_.addint32(j11_)
        x12_ = x12_.addint32(j12_)
        x13_ = x13_.addint32(j13_)
        x14_ = x14_.addint32(j14_)
        x15_ = x15_.addint32(j15_)
        return x0_.toreversestring() + x1_.toreversestring() + x2_.toreversestring() + x3_.toreversestring() + x4_.toreversestring() + x5_.toreversestring() + x6_.toreversestring() + x7_.toreversestring() + x8_.toreversestring() + x9_.toreversestring() + x10_.toreversestring() + x11_.toreversestring() + x12_.toreversestring() + x13_.toreversestring() + x14_.toreversestring() + x15_.toreversestring()
    # end def core_salsa20
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
    def salsa20(self, len_=None, nonce_=None, key_=None):
        
        
        if self.strlen(key_) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Key must be 32 bytes long"))
        # end if
        kcopy_ = "" + key_
        in_ = self.substr(nonce_, 0, 8) + php_str_repeat(" ", 8)
        c_ = ""
        while True:
            
            if not (len_ >= 64):
                break
            # end if
            c_ += self.core_salsa20(in_, kcopy_, None)
            u_ = 1
            #// Internal counter.
            i_ = 8
            while i_ < 16:
                
                u_ += self.chrtoint(in_[i_])
                in_[i_] = self.inttochr(u_ & 255)
                u_ >>= 8
                i_ += 1
            # end while
            len_ -= 64
        # end while
        if len_ > 0:
            c_ += self.substr(self.core_salsa20(in_, kcopy_, None), 0, len_)
        # end if
        try: 
            ParagonIE_Sodium_Compat.memzero(kcopy_)
        except SodiumException as ex_:
            kcopy_ = None
        # end try
        return c_
    # end def salsa20
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $m
    #// @param string $n
    #// @param int $ic
    #// @param string $k
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def salsa20_xor_ic(self, m_=None, n_=None, ic_=None, k_=None):
        
        
        mlen_ = self.strlen(m_)
        if mlen_ < 1:
            return ""
        # end if
        kcopy_ = self.substr(k_, 0, 32)
        in_ = self.substr(n_, 0, 8)
        #// Initialize the counter
        in_ += ParagonIE_Sodium_Core32_Util.store64_le(ic_)
        c_ = ""
        while True:
            
            if not (mlen_ >= 64):
                break
            # end if
            block_ = self.core_salsa20(in_, kcopy_, None)
            c_ += self.xorstrings(self.substr(m_, 0, 64), self.substr(block_, 0, 64))
            u_ = 1
            i_ = 8
            while i_ < 16:
                
                u_ += self.chrtoint(in_[i_])
                in_[i_] = self.inttochr(u_ & 255)
                u_ >>= 8
                i_ += 1
            # end while
            mlen_ -= 64
            m_ = self.substr(m_, 64)
        # end while
        if mlen_:
            block_ = self.core_salsa20(in_, kcopy_, None)
            c_ += self.xorstrings(self.substr(m_, 0, mlen_), self.substr(block_, 0, mlen_))
        # end if
        try: 
            ParagonIE_Sodium_Compat.memzero(block_)
            ParagonIE_Sodium_Compat.memzero(kcopy_)
        except SodiumException as ex_:
            block_ = None
            kcopy_ = None
        # end try
        return c_
    # end def salsa20_xor_ic
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
    def salsa20_xor(self, message_=None, nonce_=None, key_=None):
        
        
        return self.xorstrings(message_, self.salsa20(self.strlen(message_), nonce_, key_))
    # end def salsa20_xor
# end class ParagonIE_Sodium_Core32_Salsa20
