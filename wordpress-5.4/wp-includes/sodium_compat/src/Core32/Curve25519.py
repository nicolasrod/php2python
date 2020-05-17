#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519
#// 
#// Implements Curve25519 core functions
#// 
#// Based on the ref10 curve25519 code provided by libsodium
#// 
#// @ref https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c
#//
class ParagonIE_Sodium_Core32_Curve25519(ParagonIE_Sodium_Core32_Curve25519_H):
    #// 
    #// Get a field element of size 10 with a value of 0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_0(self):
        
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())))
    # end def fe_0
    #// 
    #// Get a field element of size 10 with a value of 1
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_1(self):
        
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(1), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())))
    # end def fe_1
    #// 
    #// Add two field elements.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_add(self, f_=None, g_=None):
        
        
        arr_ = Array()
        i_ = 0
        while i_ < 10:
            
            arr_[i_] = f_[i_].addint32(g_[i_])
            i_ += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $arr
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(arr_)
    # end def fe_add
    #// 
    #// Constant-time conditional move.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_cmov(self, f_=None, g_=None, b_=0):
        
        
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h
        h_ = Array()
        i_ = 0
        while i_ < 10:
            
            if (not type(f_[i_]).__name__ == "ParagonIE_Sodium_Core32_Int32"):
                raise php_new_class("TypeError", lambda : TypeError("Expected Int32"))
            # end if
            if (not type(g_[i_]).__name__ == "ParagonIE_Sodium_Core32_Int32"):
                raise php_new_class("TypeError", lambda : TypeError("Expected Int32"))
            # end if
            h_[i_] = f_[i_].xorint32(f_[i_].xorint32(g_[i_]).mask(b_))
            i_ += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(h_)
    # end def fe_cmov
    #// 
    #// Create a copy of a field element.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    @classmethod
    def fe_copy(self, f_=None):
        
        
        h_ = copy.deepcopy(f_)
        return h_
    # end def fe_copy
    #// 
    #// Give: 32-byte string.
    #// Receive: A field element object to use for internal calculations.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws RangeException
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_frombytes(self, s_=None):
        
        
        if self.strlen(s_) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Expected a 32-byte string."))
        # end if
        #// @var ParagonIE_Sodium_Core32_Int32 $h0
        h0_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_4(s_))
        #// @var ParagonIE_Sodium_Core32_Int32 $h1
        h1_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 4, 3)) << 6)
        #// @var ParagonIE_Sodium_Core32_Int32 $h2
        h2_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 7, 3)) << 5)
        #// @var ParagonIE_Sodium_Core32_Int32 $h3
        h3_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 10, 3)) << 3)
        #// @var ParagonIE_Sodium_Core32_Int32 $h4
        h4_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 13, 3)) << 2)
        #// @var ParagonIE_Sodium_Core32_Int32 $h5
        h5_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_4(self.substr(s_, 16, 4)))
        #// @var ParagonIE_Sodium_Core32_Int32 $h6
        h6_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 20, 3)) << 7)
        #// @var ParagonIE_Sodium_Core32_Int32 $h7
        h7_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 23, 3)) << 5)
        #// @var ParagonIE_Sodium_Core32_Int32 $h8
        h8_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 26, 3)) << 4)
        #// @var ParagonIE_Sodium_Core32_Int32 $h9
        h9_ = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s_, 29, 3)) & 8388607 << 2)
        carry9_ = h9_.addint(1 << 24).shiftright(25)
        h0_ = h0_.addint32(carry9_.mulint(19, 5))
        h9_ = h9_.subint32(carry9_.shiftleft(25))
        carry1_ = h1_.addint(1 << 24).shiftright(25)
        h2_ = h2_.addint32(carry1_)
        h1_ = h1_.subint32(carry1_.shiftleft(25))
        carry3_ = h3_.addint(1 << 24).shiftright(25)
        h4_ = h4_.addint32(carry3_)
        h3_ = h3_.subint32(carry3_.shiftleft(25))
        carry5_ = h5_.addint(1 << 24).shiftright(25)
        h6_ = h6_.addint32(carry5_)
        h5_ = h5_.subint32(carry5_.shiftleft(25))
        carry7_ = h7_.addint(1 << 24).shiftright(25)
        h8_ = h8_.addint32(carry7_)
        h7_ = h7_.subint32(carry7_.shiftleft(25))
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint32(carry0_)
        h0_ = h0_.subint32(carry0_.shiftleft(26))
        carry2_ = h2_.addint(1 << 25).shiftright(26)
        h3_ = h3_.addint32(carry2_)
        h2_ = h2_.subint32(carry2_.shiftleft(26))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint32(carry4_)
        h4_ = h4_.subint32(carry4_.shiftleft(26))
        carry6_ = h6_.addint(1 << 25).shiftright(26)
        h7_ = h7_.addint32(carry6_)
        h6_ = h6_.subint32(carry6_.shiftleft(26))
        carry8_ = h8_.addint(1 << 25).shiftright(26)
        h9_ = h9_.addint32(carry8_)
        h8_ = h8_.subint32(carry8_.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0_, h1_, h2_, h3_, h4_, h5_, h6_, h7_, h8_, h9_))
    # end def fe_frombytes
    #// 
    #// Convert a field element to a byte string.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_tobytes(self, h_=None):
        
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64[] $f
        #// @var ParagonIE_Sodium_Core32_Int64 $q
        #//
        f_ = Array()
        i_ = 0
        while i_ < 10:
            
            f_[i_] = h_[i_].toint64()
            i_ += 1
        # end while
        q_ = f_[9].mulint(19, 5).addint(1 << 14).shiftright(25).addint64(f_[0]).shiftright(26).addint64(f_[1]).shiftright(25).addint64(f_[2]).shiftright(26).addint64(f_[3]).shiftright(25).addint64(f_[4]).shiftright(26).addint64(f_[5]).shiftright(25).addint64(f_[6]).shiftright(26).addint64(f_[7]).shiftright(25).addint64(f_[8]).shiftright(26).addint64(f_[9]).shiftright(25)
        f_[0] = f_[0].addint64(q_.mulint(19, 5))
        carry0_ = f_[0].shiftright(26)
        f_[1] = f_[1].addint64(carry0_)
        f_[0] = f_[0].subint64(carry0_.shiftleft(26))
        carry1_ = f_[1].shiftright(25)
        f_[2] = f_[2].addint64(carry1_)
        f_[1] = f_[1].subint64(carry1_.shiftleft(25))
        carry2_ = f_[2].shiftright(26)
        f_[3] = f_[3].addint64(carry2_)
        f_[2] = f_[2].subint64(carry2_.shiftleft(26))
        carry3_ = f_[3].shiftright(25)
        f_[4] = f_[4].addint64(carry3_)
        f_[3] = f_[3].subint64(carry3_.shiftleft(25))
        carry4_ = f_[4].shiftright(26)
        f_[5] = f_[5].addint64(carry4_)
        f_[4] = f_[4].subint64(carry4_.shiftleft(26))
        carry5_ = f_[5].shiftright(25)
        f_[6] = f_[6].addint64(carry5_)
        f_[5] = f_[5].subint64(carry5_.shiftleft(25))
        carry6_ = f_[6].shiftright(26)
        f_[7] = f_[7].addint64(carry6_)
        f_[6] = f_[6].subint64(carry6_.shiftleft(26))
        carry7_ = f_[7].shiftright(25)
        f_[8] = f_[8].addint64(carry7_)
        f_[7] = f_[7].subint64(carry7_.shiftleft(25))
        carry8_ = f_[8].shiftright(26)
        f_[9] = f_[9].addint64(carry8_)
        f_[8] = f_[8].subint64(carry8_.shiftleft(26))
        carry9_ = f_[9].shiftright(25)
        f_[9] = f_[9].subint64(carry9_.shiftleft(25))
        #// @var int $h0
        h0_ = f_[0].toint32().toint()
        #// @var int $h1
        h1_ = f_[1].toint32().toint()
        #// @var int $h2
        h2_ = f_[2].toint32().toint()
        #// @var int $h3
        h3_ = f_[3].toint32().toint()
        #// @var int $h4
        h4_ = f_[4].toint32().toint()
        #// @var int $h5
        h5_ = f_[5].toint32().toint()
        #// @var int $h6
        h6_ = f_[6].toint32().toint()
        #// @var int $h7
        h7_ = f_[7].toint32().toint()
        #// @var int $h8
        h8_ = f_[8].toint32().toint()
        #// @var int $h9
        h9_ = f_[9].toint32().toint()
        #// 
        #// @var array<int, int>
        #//
        s_ = Array(php_int(h0_ >> 0 & 255), php_int(h0_ >> 8 & 255), php_int(h0_ >> 16 & 255), php_int(h0_ >> 24 | h1_ << 2 & 255), php_int(h1_ >> 6 & 255), php_int(h1_ >> 14 & 255), php_int(h1_ >> 22 | h2_ << 3 & 255), php_int(h2_ >> 5 & 255), php_int(h2_ >> 13 & 255), php_int(h2_ >> 21 | h3_ << 5 & 255), php_int(h3_ >> 3 & 255), php_int(h3_ >> 11 & 255), php_int(h3_ >> 19 | h4_ << 6 & 255), php_int(h4_ >> 2 & 255), php_int(h4_ >> 10 & 255), php_int(h4_ >> 18 & 255), php_int(h5_ >> 0 & 255), php_int(h5_ >> 8 & 255), php_int(h5_ >> 16 & 255), php_int(h5_ >> 24 | h6_ << 1 & 255), php_int(h6_ >> 7 & 255), php_int(h6_ >> 15 & 255), php_int(h6_ >> 23 | h7_ << 3 & 255), php_int(h7_ >> 5 & 255), php_int(h7_ >> 13 & 255), php_int(h7_ >> 21 | h8_ << 4 & 255), php_int(h8_ >> 4 & 255), php_int(h8_ >> 12 & 255), php_int(h8_ >> 20 | h9_ << 6 & 255), php_int(h9_ >> 2 & 255), php_int(h9_ >> 10 & 255), php_int(h9_ >> 18 & 255))
        return self.intarraytostring(s_)
    # end def fe_tobytes
    #// 
    #// Is a field element negative? (1 = yes, 0 = no. Used in calculations.)
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_isnegative(self, f_=None):
        
        
        str_ = self.fe_tobytes(f_)
        return php_int(self.chrtoint(str_[0]) & 1)
    # end def fe_isnegative
    #// 
    #// Returns 0 if this field element results in all NUL bytes.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_isnonzero(self, f_=None):
        
        
        zero_ = None
        if zero_ == None:
            zero_ = php_str_repeat(" ", 32)
        # end if
        #// @var string $str
        str_ = self.fe_tobytes(f_)
        #// @var string $zero
        return (not self.verify_32(str_, zero_))
    # end def fe_isnonzero
    #// 
    #// Multiply two field elements
    #// 
    #// h = f * g
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @security Is multiplication a source of timing leaks? If so, can we do
    #// anything to prevent that from happening?
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_mul(self, f_=None, g_=None):
        
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int32[] $f
        #// @var ParagonIE_Sodium_Core32_Int32[] $g
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        #// @var ParagonIE_Sodium_Core32_Int64 $g0
        #// @var ParagonIE_Sodium_Core32_Int64 $g1
        #// @var ParagonIE_Sodium_Core32_Int64 $g2
        #// @var ParagonIE_Sodium_Core32_Int64 $g3
        #// @var ParagonIE_Sodium_Core32_Int64 $g4
        #// @var ParagonIE_Sodium_Core32_Int64 $g5
        #// @var ParagonIE_Sodium_Core32_Int64 $g6
        #// @var ParagonIE_Sodium_Core32_Int64 $g7
        #// @var ParagonIE_Sodium_Core32_Int64 $g8
        #// @var ParagonIE_Sodium_Core32_Int64 $g9
        #//
        f0_ = f_[0].toint64()
        f1_ = f_[1].toint64()
        f2_ = f_[2].toint64()
        f3_ = f_[3].toint64()
        f4_ = f_[4].toint64()
        f5_ = f_[5].toint64()
        f6_ = f_[6].toint64()
        f7_ = f_[7].toint64()
        f8_ = f_[8].toint64()
        f9_ = f_[9].toint64()
        g0_ = g_[0].toint64()
        g1_ = g_[1].toint64()
        g2_ = g_[2].toint64()
        g3_ = g_[3].toint64()
        g4_ = g_[4].toint64()
        g5_ = g_[5].toint64()
        g6_ = g_[6].toint64()
        g7_ = g_[7].toint64()
        g8_ = g_[8].toint64()
        g9_ = g_[9].toint64()
        g1_19_ = g1_.mulint(19, 5)
        #// 2^4 <= 19 <= 2^5, but we only want 5 bits
        g2_19_ = g2_.mulint(19, 5)
        g3_19_ = g3_.mulint(19, 5)
        g4_19_ = g4_.mulint(19, 5)
        g5_19_ = g5_.mulint(19, 5)
        g6_19_ = g6_.mulint(19, 5)
        g7_19_ = g7_.mulint(19, 5)
        g8_19_ = g8_.mulint(19, 5)
        g9_19_ = g9_.mulint(19, 5)
        #// @var ParagonIE_Sodium_Core32_Int64 $f1_2
        f1_2_ = f1_.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f3_2
        f3_2_ = f3_.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f5_2
        f5_2_ = f5_.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f7_2
        f7_2_ = f7_.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f9_2
        f9_2_ = f9_.shiftleft(1)
        f0g0_ = f0_.mulint64(g0_, 27)
        f0g1_ = f0_.mulint64(g1_, 27)
        f0g2_ = f0_.mulint64(g2_, 27)
        f0g3_ = f0_.mulint64(g3_, 27)
        f0g4_ = f0_.mulint64(g4_, 27)
        f0g5_ = f0_.mulint64(g5_, 27)
        f0g6_ = f0_.mulint64(g6_, 27)
        f0g7_ = f0_.mulint64(g7_, 27)
        f0g8_ = f0_.mulint64(g8_, 27)
        f0g9_ = f0_.mulint64(g9_, 27)
        f1g0_ = f1_.mulint64(g0_, 27)
        f1g1_2_ = f1_2_.mulint64(g1_, 27)
        f1g2_ = f1_.mulint64(g2_, 27)
        f1g3_2_ = f1_2_.mulint64(g3_, 27)
        f1g4_ = f1_.mulint64(g4_, 30)
        f1g5_2_ = f1_2_.mulint64(g5_, 30)
        f1g6_ = f1_.mulint64(g6_, 30)
        f1g7_2_ = f1_2_.mulint64(g7_, 30)
        f1g8_ = f1_.mulint64(g8_, 30)
        f1g9_38_ = g9_19_.mulint64(f1_2_, 30)
        f2g0_ = f2_.mulint64(g0_, 30)
        f2g1_ = f2_.mulint64(g1_, 29)
        f2g2_ = f2_.mulint64(g2_, 30)
        f2g3_ = f2_.mulint64(g3_, 29)
        f2g4_ = f2_.mulint64(g4_, 30)
        f2g5_ = f2_.mulint64(g5_, 29)
        f2g6_ = f2_.mulint64(g6_, 30)
        f2g7_ = f2_.mulint64(g7_, 29)
        f2g8_19_ = g8_19_.mulint64(f2_, 30)
        f2g9_19_ = g9_19_.mulint64(f2_, 30)
        f3g0_ = f3_.mulint64(g0_, 30)
        f3g1_2_ = f3_2_.mulint64(g1_, 30)
        f3g2_ = f3_.mulint64(g2_, 30)
        f3g3_2_ = f3_2_.mulint64(g3_, 30)
        f3g4_ = f3_.mulint64(g4_, 30)
        f3g5_2_ = f3_2_.mulint64(g5_, 30)
        f3g6_ = f3_.mulint64(g6_, 30)
        f3g7_38_ = g7_19_.mulint64(f3_2_, 30)
        f3g8_19_ = g8_19_.mulint64(f3_, 30)
        f3g9_38_ = g9_19_.mulint64(f3_2_, 30)
        f4g0_ = f4_.mulint64(g0_, 30)
        f4g1_ = f4_.mulint64(g1_, 30)
        f4g2_ = f4_.mulint64(g2_, 30)
        f4g3_ = f4_.mulint64(g3_, 30)
        f4g4_ = f4_.mulint64(g4_, 30)
        f4g5_ = f4_.mulint64(g5_, 30)
        f4g6_19_ = g6_19_.mulint64(f4_, 30)
        f4g7_19_ = g7_19_.mulint64(f4_, 30)
        f4g8_19_ = g8_19_.mulint64(f4_, 30)
        f4g9_19_ = g9_19_.mulint64(f4_, 30)
        f5g0_ = f5_.mulint64(g0_, 30)
        f5g1_2_ = f5_2_.mulint64(g1_, 30)
        f5g2_ = f5_.mulint64(g2_, 30)
        f5g3_2_ = f5_2_.mulint64(g3_, 30)
        f5g4_ = f5_.mulint64(g4_, 30)
        f5g5_38_ = g5_19_.mulint64(f5_2_, 30)
        f5g6_19_ = g6_19_.mulint64(f5_, 30)
        f5g7_38_ = g7_19_.mulint64(f5_2_, 30)
        f5g8_19_ = g8_19_.mulint64(f5_, 30)
        f5g9_38_ = g9_19_.mulint64(f5_2_, 30)
        f6g0_ = f6_.mulint64(g0_, 30)
        f6g1_ = f6_.mulint64(g1_, 30)
        f6g2_ = f6_.mulint64(g2_, 30)
        f6g3_ = f6_.mulint64(g3_, 30)
        f6g4_19_ = g4_19_.mulint64(f6_, 30)
        f6g5_19_ = g5_19_.mulint64(f6_, 30)
        f6g6_19_ = g6_19_.mulint64(f6_, 30)
        f6g7_19_ = g7_19_.mulint64(f6_, 30)
        f6g8_19_ = g8_19_.mulint64(f6_, 30)
        f6g9_19_ = g9_19_.mulint64(f6_, 30)
        f7g0_ = f7_.mulint64(g0_, 30)
        f7g1_2_ = g1_.mulint64(f7_2_, 30)
        f7g2_ = f7_.mulint64(g2_, 30)
        f7g3_38_ = g3_19_.mulint64(f7_2_, 30)
        f7g4_19_ = g4_19_.mulint64(f7_, 30)
        f7g5_38_ = g5_19_.mulint64(f7_2_, 30)
        f7g6_19_ = g6_19_.mulint64(f7_, 30)
        f7g7_38_ = g7_19_.mulint64(f7_2_, 30)
        f7g8_19_ = g8_19_.mulint64(f7_, 30)
        f7g9_38_ = g9_19_.mulint64(f7_2_, 30)
        f8g0_ = f8_.mulint64(g0_, 30)
        f8g1_ = f8_.mulint64(g1_, 29)
        f8g2_19_ = g2_19_.mulint64(f8_, 30)
        f8g3_19_ = g3_19_.mulint64(f8_, 30)
        f8g4_19_ = g4_19_.mulint64(f8_, 30)
        f8g5_19_ = g5_19_.mulint64(f8_, 30)
        f8g6_19_ = g6_19_.mulint64(f8_, 30)
        f8g7_19_ = g7_19_.mulint64(f8_, 30)
        f8g8_19_ = g8_19_.mulint64(f8_, 30)
        f8g9_19_ = g9_19_.mulint64(f8_, 30)
        f9g0_ = f9_.mulint64(g0_, 30)
        f9g1_38_ = g1_19_.mulint64(f9_2_, 30)
        f9g2_19_ = g2_19_.mulint64(f9_, 30)
        f9g3_38_ = g3_19_.mulint64(f9_2_, 30)
        f9g4_19_ = g4_19_.mulint64(f9_, 30)
        f9g5_38_ = g5_19_.mulint64(f9_2_, 30)
        f9g6_19_ = g6_19_.mulint64(f9_, 30)
        f9g7_38_ = g7_19_.mulint64(f9_2_, 30)
        f9g8_19_ = g8_19_.mulint64(f9_, 30)
        f9g9_38_ = g9_19_.mulint64(f9_2_, 30)
        #// $h0 = $f0g0 + $f1g9_38 + $f2g8_19 + $f3g7_38 + $f4g6_19 + $f5g5_38 + $f6g4_19 + $f7g3_38 + $f8g2_19 + $f9g1_38;
        h0_ = f0g0_.addint64(f1g9_38_).addint64(f2g8_19_).addint64(f3g7_38_).addint64(f4g6_19_).addint64(f5g5_38_).addint64(f6g4_19_).addint64(f7g3_38_).addint64(f8g2_19_).addint64(f9g1_38_)
        #// $h1 = $f0g1 + $f1g0    + $f2g9_19 + $f3g8_19 + $f4g7_19 + $f5g6_19 + $f6g5_19 + $f7g4_19 + $f8g3_19 + $f9g2_19;
        h1_ = f0g1_.addint64(f1g0_).addint64(f2g9_19_).addint64(f3g8_19_).addint64(f4g7_19_).addint64(f5g6_19_).addint64(f6g5_19_).addint64(f7g4_19_).addint64(f8g3_19_).addint64(f9g2_19_)
        #// $h2 = $f0g2 + $f1g1_2  + $f2g0    + $f3g9_38 + $f4g8_19 + $f5g7_38 + $f6g6_19 + $f7g5_38 + $f8g4_19 + $f9g3_38;
        h2_ = f0g2_.addint64(f1g1_2_).addint64(f2g0_).addint64(f3g9_38_).addint64(f4g8_19_).addint64(f5g7_38_).addint64(f6g6_19_).addint64(f7g5_38_).addint64(f8g4_19_).addint64(f9g3_38_)
        #// $h3 = $f0g3 + $f1g2    + $f2g1    + $f3g0    + $f4g9_19 + $f5g8_19 + $f6g7_19 + $f7g6_19 + $f8g5_19 + $f9g4_19;
        h3_ = f0g3_.addint64(f1g2_).addint64(f2g1_).addint64(f3g0_).addint64(f4g9_19_).addint64(f5g8_19_).addint64(f6g7_19_).addint64(f7g6_19_).addint64(f8g5_19_).addint64(f9g4_19_)
        #// $h4 = $f0g4 + $f1g3_2  + $f2g2    + $f3g1_2  + $f4g0    + $f5g9_38 + $f6g8_19 + $f7g7_38 + $f8g6_19 + $f9g5_38;
        h4_ = f0g4_.addint64(f1g3_2_).addint64(f2g2_).addint64(f3g1_2_).addint64(f4g0_).addint64(f5g9_38_).addint64(f6g8_19_).addint64(f7g7_38_).addint64(f8g6_19_).addint64(f9g5_38_)
        #// $h5 = $f0g5 + $f1g4    + $f2g3    + $f3g2    + $f4g1    + $f5g0    + $f6g9_19 + $f7g8_19 + $f8g7_19 + $f9g6_19;
        h5_ = f0g5_.addint64(f1g4_).addint64(f2g3_).addint64(f3g2_).addint64(f4g1_).addint64(f5g0_).addint64(f6g9_19_).addint64(f7g8_19_).addint64(f8g7_19_).addint64(f9g6_19_)
        #// $h6 = $f0g6 + $f1g5_2  + $f2g4    + $f3g3_2  + $f4g2    + $f5g1_2  + $f6g0    + $f7g9_38 + $f8g8_19 + $f9g7_38;
        h6_ = f0g6_.addint64(f1g5_2_).addint64(f2g4_).addint64(f3g3_2_).addint64(f4g2_).addint64(f5g1_2_).addint64(f6g0_).addint64(f7g9_38_).addint64(f8g8_19_).addint64(f9g7_38_)
        #// $h7 = $f0g7 + $f1g6    + $f2g5    + $f3g4    + $f4g3    + $f5g2    + $f6g1    + $f7g0    + $f8g9_19 + $f9g8_19;
        h7_ = f0g7_.addint64(f1g6_).addint64(f2g5_).addint64(f3g4_).addint64(f4g3_).addint64(f5g2_).addint64(f6g1_).addint64(f7g0_).addint64(f8g9_19_).addint64(f9g8_19_)
        #// $h8 = $f0g8 + $f1g7_2  + $f2g6    + $f3g5_2  + $f4g4    + $f5g3_2  + $f6g2    + $f7g1_2  + $f8g0    + $f9g9_38;
        h8_ = f0g8_.addint64(f1g7_2_).addint64(f2g6_).addint64(f3g5_2_).addint64(f4g4_).addint64(f5g3_2_).addint64(f6g2_).addint64(f7g1_2_).addint64(f8g0_).addint64(f9g9_38_)
        #// $h9 = $f0g9 + $f1g8    + $f2g7    + $f3g6    + $f4g5    + $f5g4    + $f6g3    + $f7g2    + $f8g1    + $f9g0   ;
        h9_ = f0g9_.addint64(f1g8_).addint64(f2g7_).addint64(f3g6_).addint64(f4g5_).addint64(f5g4_).addint64(f6g3_).addint64(f7g2_).addint64(f8g1_).addint64(f9g0_)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #// @var ParagonIE_Sodium_Core32_Int64 $carry0
        #// @var ParagonIE_Sodium_Core32_Int64 $carry1
        #// @var ParagonIE_Sodium_Core32_Int64 $carry2
        #// @var ParagonIE_Sodium_Core32_Int64 $carry3
        #// @var ParagonIE_Sodium_Core32_Int64 $carry4
        #// @var ParagonIE_Sodium_Core32_Int64 $carry5
        #// @var ParagonIE_Sodium_Core32_Int64 $carry6
        #// @var ParagonIE_Sodium_Core32_Int64 $carry7
        #// @var ParagonIE_Sodium_Core32_Int64 $carry8
        #// @var ParagonIE_Sodium_Core32_Int64 $carry9
        #//
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry1_ = h1_.addint(1 << 24).shiftright(25)
        h2_ = h2_.addint64(carry1_)
        h1_ = h1_.subint64(carry1_.shiftleft(25))
        carry5_ = h5_.addint(1 << 24).shiftright(25)
        h6_ = h6_.addint64(carry5_)
        h5_ = h5_.subint64(carry5_.shiftleft(25))
        carry2_ = h2_.addint(1 << 25).shiftright(26)
        h3_ = h3_.addint64(carry2_)
        h2_ = h2_.subint64(carry2_.shiftleft(26))
        carry6_ = h6_.addint(1 << 25).shiftright(26)
        h7_ = h7_.addint64(carry6_)
        h6_ = h6_.subint64(carry6_.shiftleft(26))
        carry3_ = h3_.addint(1 << 24).shiftright(25)
        h4_ = h4_.addint64(carry3_)
        h3_ = h3_.subint64(carry3_.shiftleft(25))
        carry7_ = h7_.addint(1 << 24).shiftright(25)
        h8_ = h8_.addint64(carry7_)
        h7_ = h7_.subint64(carry7_.shiftleft(25))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry8_ = h8_.addint(1 << 25).shiftright(26)
        h9_ = h9_.addint64(carry8_)
        h8_ = h8_.subint64(carry8_.shiftleft(26))
        carry9_ = h9_.addint(1 << 24).shiftright(25)
        h0_ = h0_.addint64(carry9_.mulint(19, 5))
        h9_ = h9_.subint64(carry9_.shiftleft(25))
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0_.toint32(), h1_.toint32(), h2_.toint32(), h3_.toint32(), h4_.toint32(), h5_.toint32(), h6_.toint32(), h7_.toint32(), h8_.toint32(), h9_.toint32()))
    # end def fe_mul
    #// 
    #// Get the negative values for each piece of the field element.
    #// 
    #// h = -f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_neg(self, f_=None):
        
        
        h_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        i_ = 0
        while i_ < 10:
            
            h_[i_] = h_[i_].subint32(f_[i_])
            i_ += 1
        # end while
        return h_
    # end def fe_neg
    #// 
    #// Square a field element
    #// 
    #// h = f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_sq(self, f_=None):
        
        
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        f0_ = f_[0].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        f1_ = f_[1].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        f2_ = f_[2].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        f3_ = f_[3].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        f4_ = f_[4].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        f5_ = f_[5].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        f6_ = f_[6].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        f7_ = f_[7].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        f8_ = f_[8].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        f9_ = f_[9].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f0_2
        f0_2_ = f0_.shiftleft(1)
        f1_2_ = f1_.shiftleft(1)
        f2_2_ = f2_.shiftleft(1)
        f3_2_ = f3_.shiftleft(1)
        f4_2_ = f4_.shiftleft(1)
        f5_2_ = f5_.shiftleft(1)
        f6_2_ = f6_.shiftleft(1)
        f7_2_ = f7_.shiftleft(1)
        f5_38_ = f5_.mulint(38, 6)
        f6_19_ = f6_.mulint(19, 5)
        f7_38_ = f7_.mulint(38, 6)
        f8_19_ = f8_.mulint(19, 5)
        f9_38_ = f9_.mulint(38, 6)
        #// @var ParagonIE_Sodium_Core32_Int64 $f0f0
        f0f0_ = f0_.mulint64(f0_, 28)
        f0f1_2_ = f0_2_.mulint64(f1_, 28)
        f0f2_2_ = f0_2_.mulint64(f2_, 28)
        f0f3_2_ = f0_2_.mulint64(f3_, 28)
        f0f4_2_ = f0_2_.mulint64(f4_, 28)
        f0f5_2_ = f0_2_.mulint64(f5_, 28)
        f0f6_2_ = f0_2_.mulint64(f6_, 28)
        f0f7_2_ = f0_2_.mulint64(f7_, 28)
        f0f8_2_ = f0_2_.mulint64(f8_, 28)
        f0f9_2_ = f0_2_.mulint64(f9_, 28)
        f1f1_2_ = f1_2_.mulint64(f1_, 28)
        f1f2_2_ = f1_2_.mulint64(f2_, 28)
        f1f3_4_ = f1_2_.mulint64(f3_2_, 28)
        f1f4_2_ = f1_2_.mulint64(f4_, 28)
        f1f5_4_ = f1_2_.mulint64(f5_2_, 30)
        f1f6_2_ = f1_2_.mulint64(f6_, 28)
        f1f7_4_ = f1_2_.mulint64(f7_2_, 28)
        f1f8_2_ = f1_2_.mulint64(f8_, 28)
        f1f9_76_ = f9_38_.mulint64(f1_2_, 30)
        f2f2_ = f2_.mulint64(f2_, 28)
        f2f3_2_ = f2_2_.mulint64(f3_, 28)
        f2f4_2_ = f2_2_.mulint64(f4_, 28)
        f2f5_2_ = f2_2_.mulint64(f5_, 28)
        f2f6_2_ = f2_2_.mulint64(f6_, 28)
        f2f7_2_ = f2_2_.mulint64(f7_, 28)
        f2f8_38_ = f8_19_.mulint64(f2_2_, 30)
        f2f9_38_ = f9_38_.mulint64(f2_, 30)
        f3f3_2_ = f3_2_.mulint64(f3_, 28)
        f3f4_2_ = f3_2_.mulint64(f4_, 28)
        f3f5_4_ = f3_2_.mulint64(f5_2_, 30)
        f3f6_2_ = f3_2_.mulint64(f6_, 28)
        f3f7_76_ = f7_38_.mulint64(f3_2_, 30)
        f3f8_38_ = f8_19_.mulint64(f3_2_, 30)
        f3f9_76_ = f9_38_.mulint64(f3_2_, 30)
        f4f4_ = f4_.mulint64(f4_, 28)
        f4f5_2_ = f4_2_.mulint64(f5_, 28)
        f4f6_38_ = f6_19_.mulint64(f4_2_, 30)
        f4f7_38_ = f7_38_.mulint64(f4_, 30)
        f4f8_38_ = f8_19_.mulint64(f4_2_, 30)
        f4f9_38_ = f9_38_.mulint64(f4_, 30)
        f5f5_38_ = f5_38_.mulint64(f5_, 30)
        f5f6_38_ = f6_19_.mulint64(f5_2_, 30)
        f5f7_76_ = f7_38_.mulint64(f5_2_, 30)
        f5f8_38_ = f8_19_.mulint64(f5_2_, 30)
        f5f9_76_ = f9_38_.mulint64(f5_2_, 30)
        f6f6_19_ = f6_19_.mulint64(f6_, 30)
        f6f7_38_ = f7_38_.mulint64(f6_, 30)
        f6f8_38_ = f8_19_.mulint64(f6_2_, 30)
        f6f9_38_ = f9_38_.mulint64(f6_, 30)
        f7f7_38_ = f7_38_.mulint64(f7_, 28)
        f7f8_38_ = f8_19_.mulint64(f7_2_, 30)
        f7f9_76_ = f9_38_.mulint64(f7_2_, 30)
        f8f8_19_ = f8_19_.mulint64(f8_, 30)
        f8f9_38_ = f9_38_.mulint64(f8_, 30)
        f9f9_38_ = f9_38_.mulint64(f9_, 28)
        h0_ = f0f0_.addint64(f1f9_76_).addint64(f2f8_38_).addint64(f3f7_76_).addint64(f4f6_38_).addint64(f5f5_38_)
        h1_ = f0f1_2_.addint64(f2f9_38_).addint64(f3f8_38_).addint64(f4f7_38_).addint64(f5f6_38_)
        h2_ = f0f2_2_.addint64(f1f1_2_).addint64(f3f9_76_).addint64(f4f8_38_).addint64(f5f7_76_).addint64(f6f6_19_)
        h3_ = f0f3_2_.addint64(f1f2_2_).addint64(f4f9_38_).addint64(f5f8_38_).addint64(f6f7_38_)
        h4_ = f0f4_2_.addint64(f1f3_4_).addint64(f2f2_).addint64(f5f9_76_).addint64(f6f8_38_).addint64(f7f7_38_)
        h5_ = f0f5_2_.addint64(f1f4_2_).addint64(f2f3_2_).addint64(f6f9_38_).addint64(f7f8_38_)
        h6_ = f0f6_2_.addint64(f1f5_4_).addint64(f2f4_2_).addint64(f3f3_2_).addint64(f7f9_76_).addint64(f8f8_19_)
        h7_ = f0f7_2_.addint64(f1f6_2_).addint64(f2f5_2_).addint64(f3f4_2_).addint64(f8f9_38_)
        h8_ = f0f8_2_.addint64(f1f7_4_).addint64(f2f6_2_).addint64(f3f5_4_).addint64(f4f4_).addint64(f9f9_38_)
        h9_ = f0f9_2_.addint64(f1f8_2_).addint64(f2f7_2_).addint64(f3f6_2_).addint64(f4f5_2_)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #//
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry1_ = h1_.addint(1 << 24).shiftright(25)
        h2_ = h2_.addint64(carry1_)
        h1_ = h1_.subint64(carry1_.shiftleft(25))
        carry5_ = h5_.addint(1 << 24).shiftright(25)
        h6_ = h6_.addint64(carry5_)
        h5_ = h5_.subint64(carry5_.shiftleft(25))
        carry2_ = h2_.addint(1 << 25).shiftright(26)
        h3_ = h3_.addint64(carry2_)
        h2_ = h2_.subint64(carry2_.shiftleft(26))
        carry6_ = h6_.addint(1 << 25).shiftright(26)
        h7_ = h7_.addint64(carry6_)
        h6_ = h6_.subint64(carry6_.shiftleft(26))
        carry3_ = h3_.addint(1 << 24).shiftright(25)
        h4_ = h4_.addint64(carry3_)
        h3_ = h3_.subint64(carry3_.shiftleft(25))
        carry7_ = h7_.addint(1 << 24).shiftright(25)
        h8_ = h8_.addint64(carry7_)
        h7_ = h7_.subint64(carry7_.shiftleft(25))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry8_ = h8_.addint(1 << 25).shiftright(26)
        h9_ = h9_.addint64(carry8_)
        h8_ = h8_.subint64(carry8_.shiftleft(26))
        carry9_ = h9_.addint(1 << 24).shiftright(25)
        h0_ = h0_.addint64(carry9_.mulint(19, 5))
        h9_ = h9_.subint64(carry9_.shiftleft(25))
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0_.toint32(), h1_.toint32(), h2_.toint32(), h3_.toint32(), h4_.toint32(), h5_.toint32(), h6_.toint32(), h7_.toint32(), h8_.toint32(), h9_.toint32()))
    # end def fe_sq
    #// 
    #// Square and double a field element
    #// 
    #// h = 2 * f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_sq2(self, f_=None):
        
        
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        f0_ = f_[0].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        f1_ = f_[1].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        f2_ = f_[2].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        f3_ = f_[3].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        f4_ = f_[4].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        f5_ = f_[5].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        f6_ = f_[6].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        f7_ = f_[7].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        f8_ = f_[8].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        f9_ = f_[9].toint64()
        f0_2_ = f0_.shiftleft(1)
        f1_2_ = f1_.shiftleft(1)
        f2_2_ = f2_.shiftleft(1)
        f3_2_ = f3_.shiftleft(1)
        f4_2_ = f4_.shiftleft(1)
        f5_2_ = f5_.shiftleft(1)
        f6_2_ = f6_.shiftleft(1)
        f7_2_ = f7_.shiftleft(1)
        f5_38_ = f5_.mulint(38, 6)
        #// 1.959375*2^30
        f6_19_ = f6_.mulint(19, 5)
        #// 1.959375*2^30
        f7_38_ = f7_.mulint(38, 6)
        #// 1.959375*2^30
        f8_19_ = f8_.mulint(19, 5)
        #// 1.959375*2^30
        f9_38_ = f9_.mulint(38, 6)
        #// 1.959375*2^30
        f0f0_ = f0_.mulint64(f0_, 28)
        f0f1_2_ = f0_2_.mulint64(f1_, 28)
        f0f2_2_ = f0_2_.mulint64(f2_, 28)
        f0f3_2_ = f0_2_.mulint64(f3_, 28)
        f0f4_2_ = f0_2_.mulint64(f4_, 28)
        f0f5_2_ = f0_2_.mulint64(f5_, 28)
        f0f6_2_ = f0_2_.mulint64(f6_, 28)
        f0f7_2_ = f0_2_.mulint64(f7_, 28)
        f0f8_2_ = f0_2_.mulint64(f8_, 28)
        f0f9_2_ = f0_2_.mulint64(f9_, 28)
        f1f1_2_ = f1_2_.mulint64(f1_, 28)
        f1f2_2_ = f1_2_.mulint64(f2_, 28)
        f1f3_4_ = f1_2_.mulint64(f3_2_, 29)
        f1f4_2_ = f1_2_.mulint64(f4_, 28)
        f1f5_4_ = f1_2_.mulint64(f5_2_, 29)
        f1f6_2_ = f1_2_.mulint64(f6_, 28)
        f1f7_4_ = f1_2_.mulint64(f7_2_, 29)
        f1f8_2_ = f1_2_.mulint64(f8_, 28)
        f1f9_76_ = f9_38_.mulint64(f1_2_, 29)
        f2f2_ = f2_.mulint64(f2_, 28)
        f2f3_2_ = f2_2_.mulint64(f3_, 28)
        f2f4_2_ = f2_2_.mulint64(f4_, 28)
        f2f5_2_ = f2_2_.mulint64(f5_, 28)
        f2f6_2_ = f2_2_.mulint64(f6_, 28)
        f2f7_2_ = f2_2_.mulint64(f7_, 28)
        f2f8_38_ = f8_19_.mulint64(f2_2_, 29)
        f2f9_38_ = f9_38_.mulint64(f2_, 29)
        f3f3_2_ = f3_2_.mulint64(f3_, 28)
        f3f4_2_ = f3_2_.mulint64(f4_, 28)
        f3f5_4_ = f3_2_.mulint64(f5_2_, 28)
        f3f6_2_ = f3_2_.mulint64(f6_, 28)
        f3f7_76_ = f7_38_.mulint64(f3_2_, 29)
        f3f8_38_ = f8_19_.mulint64(f3_2_, 29)
        f3f9_76_ = f9_38_.mulint64(f3_2_, 29)
        f4f4_ = f4_.mulint64(f4_, 28)
        f4f5_2_ = f4_2_.mulint64(f5_, 28)
        f4f6_38_ = f6_19_.mulint64(f4_2_, 29)
        f4f7_38_ = f7_38_.mulint64(f4_, 29)
        f4f8_38_ = f8_19_.mulint64(f4_2_, 29)
        f4f9_38_ = f9_38_.mulint64(f4_, 29)
        f5f5_38_ = f5_38_.mulint64(f5_, 29)
        f5f6_38_ = f6_19_.mulint64(f5_2_, 29)
        f5f7_76_ = f7_38_.mulint64(f5_2_, 29)
        f5f8_38_ = f8_19_.mulint64(f5_2_, 29)
        f5f9_76_ = f9_38_.mulint64(f5_2_, 29)
        f6f6_19_ = f6_19_.mulint64(f6_, 29)
        f6f7_38_ = f7_38_.mulint64(f6_, 29)
        f6f8_38_ = f8_19_.mulint64(f6_2_, 29)
        f6f9_38_ = f9_38_.mulint64(f6_, 29)
        f7f7_38_ = f7_38_.mulint64(f7_, 29)
        f7f8_38_ = f8_19_.mulint64(f7_2_, 29)
        f7f9_76_ = f9_38_.mulint64(f7_2_, 29)
        f8f8_19_ = f8_19_.mulint64(f8_, 29)
        f8f9_38_ = f9_38_.mulint64(f8_, 29)
        f9f9_38_ = f9_38_.mulint64(f9_, 29)
        h0_ = f0f0_.addint64(f1f9_76_).addint64(f2f8_38_).addint64(f3f7_76_).addint64(f4f6_38_).addint64(f5f5_38_)
        h1_ = f0f1_2_.addint64(f2f9_38_).addint64(f3f8_38_).addint64(f4f7_38_).addint64(f5f6_38_)
        h2_ = f0f2_2_.addint64(f1f1_2_).addint64(f3f9_76_).addint64(f4f8_38_).addint64(f5f7_76_).addint64(f6f6_19_)
        h3_ = f0f3_2_.addint64(f1f2_2_).addint64(f4f9_38_).addint64(f5f8_38_).addint64(f6f7_38_)
        h4_ = f0f4_2_.addint64(f1f3_4_).addint64(f2f2_).addint64(f5f9_76_).addint64(f6f8_38_).addint64(f7f7_38_)
        h5_ = f0f5_2_.addint64(f1f4_2_).addint64(f2f3_2_).addint64(f6f9_38_).addint64(f7f8_38_)
        h6_ = f0f6_2_.addint64(f1f5_4_).addint64(f2f4_2_).addint64(f3f3_2_).addint64(f7f9_76_).addint64(f8f8_19_)
        h7_ = f0f7_2_.addint64(f1f6_2_).addint64(f2f5_2_).addint64(f3f4_2_).addint64(f8f9_38_)
        h8_ = f0f8_2_.addint64(f1f7_4_).addint64(f2f6_2_).addint64(f3f5_4_).addint64(f4f4_).addint64(f9f9_38_)
        h9_ = f0f9_2_.addint64(f1f8_2_).addint64(f2f7_2_).addint64(f3f6_2_).addint64(f4f5_2_)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #//
        h0_ = h0_.shiftleft(1)
        h1_ = h1_.shiftleft(1)
        h2_ = h2_.shiftleft(1)
        h3_ = h3_.shiftleft(1)
        h4_ = h4_.shiftleft(1)
        h5_ = h5_.shiftleft(1)
        h6_ = h6_.shiftleft(1)
        h7_ = h7_.shiftleft(1)
        h8_ = h8_.shiftleft(1)
        h9_ = h9_.shiftleft(1)
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry1_ = h1_.addint(1 << 24).shiftright(25)
        h2_ = h2_.addint64(carry1_)
        h1_ = h1_.subint64(carry1_.shiftleft(25))
        carry5_ = h5_.addint(1 << 24).shiftright(25)
        h6_ = h6_.addint64(carry5_)
        h5_ = h5_.subint64(carry5_.shiftleft(25))
        carry2_ = h2_.addint(1 << 25).shiftright(26)
        h3_ = h3_.addint64(carry2_)
        h2_ = h2_.subint64(carry2_.shiftleft(26))
        carry6_ = h6_.addint(1 << 25).shiftright(26)
        h7_ = h7_.addint64(carry6_)
        h6_ = h6_.subint64(carry6_.shiftleft(26))
        carry3_ = h3_.addint(1 << 24).shiftright(25)
        h4_ = h4_.addint64(carry3_)
        h3_ = h3_.subint64(carry3_.shiftleft(25))
        carry7_ = h7_.addint(1 << 24).shiftright(25)
        h8_ = h8_.addint64(carry7_)
        h7_ = h7_.subint64(carry7_.shiftleft(25))
        carry4_ = h4_.addint(1 << 25).shiftright(26)
        h5_ = h5_.addint64(carry4_)
        h4_ = h4_.subint64(carry4_.shiftleft(26))
        carry8_ = h8_.addint(1 << 25).shiftright(26)
        h9_ = h9_.addint64(carry8_)
        h8_ = h8_.subint64(carry8_.shiftleft(26))
        carry9_ = h9_.addint(1 << 24).shiftright(25)
        h0_ = h0_.addint64(carry9_.mulint(19, 5))
        h9_ = h9_.subint64(carry9_.shiftleft(25))
        carry0_ = h0_.addint(1 << 25).shiftright(26)
        h1_ = h1_.addint64(carry0_)
        h0_ = h0_.subint64(carry0_.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0_.toint32(), h1_.toint32(), h2_.toint32(), h3_.toint32(), h4_.toint32(), h5_.toint32(), h6_.toint32(), h7_.toint32(), h8_.toint32(), h9_.toint32()))
    # end def fe_sq2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $Z
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_invert(self, Z_=None):
        
        
        z_ = copy.deepcopy(Z_)
        t0_ = self.fe_sq(z_)
        t1_ = self.fe_sq(t0_)
        t1_ = self.fe_sq(t1_)
        t1_ = self.fe_mul(z_, t1_)
        t0_ = self.fe_mul(t0_, t1_)
        t2_ = self.fe_sq(t0_)
        t1_ = self.fe_mul(t1_, t2_)
        t2_ = self.fe_sq(t1_)
        i_ = 1
        while i_ < 5:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        t1_ = self.fe_mul(t2_, t1_)
        t2_ = self.fe_sq(t1_)
        i_ = 1
        while i_ < 10:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        t2_ = self.fe_mul(t2_, t1_)
        t3_ = self.fe_sq(t2_)
        i_ = 1
        while i_ < 20:
            
            t3_ = self.fe_sq(t3_)
            i_ += 1
        # end while
        t2_ = self.fe_mul(t3_, t2_)
        t2_ = self.fe_sq(t2_)
        i_ = 1
        while i_ < 10:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        t1_ = self.fe_mul(t2_, t1_)
        t2_ = self.fe_sq(t1_)
        i_ = 1
        while i_ < 50:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        t2_ = self.fe_mul(t2_, t1_)
        t3_ = self.fe_sq(t2_)
        i_ = 1
        while i_ < 100:
            
            t3_ = self.fe_sq(t3_)
            i_ += 1
        # end while
        t2_ = self.fe_mul(t3_, t2_)
        t2_ = self.fe_sq(t2_)
        i_ = 1
        while i_ < 50:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        t1_ = self.fe_mul(t2_, t1_)
        t1_ = self.fe_sq(t1_)
        i_ = 1
        while i_ < 5:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        return self.fe_mul(t1_, t0_)
    # end def fe_invert
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref https://github.com/jedisct1/libsodium/blob/68564326e1e9dc57ef03746f85734232d20ca6fb/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c#L1054-L1106
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $z
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_pow22523(self, z_=None):
        
        
        #// # fe_sq(t0, z);
        #// # fe_sq(t1, t0);
        #// # fe_sq(t1, t1);
        #// # fe_mul(t1, z, t1);
        #// # fe_mul(t0, t0, t1);
        #// # fe_sq(t0, t0);
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0_ = self.fe_sq(z_)
        t1_ = self.fe_sq(t0_)
        t1_ = self.fe_sq(t1_)
        t1_ = self.fe_mul(z_, t1_)
        t0_ = self.fe_mul(t0_, t1_)
        t0_ = self.fe_sq(t0_)
        t0_ = self.fe_mul(t1_, t0_)
        t1_ = self.fe_sq(t0_)
        #// # for (i = 1; i < 5; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i_ = 1
        while i_ < 5:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0_ = self.fe_mul(t1_, t0_)
        t1_ = self.fe_sq(t0_)
        #// # for (i = 1; i < 10; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i_ = 1
        while i_ < 10:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        #// # fe_mul(t1, t1, t0);
        #// # fe_sq(t2, t1);
        t1_ = self.fe_mul(t1_, t0_)
        t2_ = self.fe_sq(t1_)
        #// # for (i = 1; i < 20; ++i) {
        #// #     fe_sq(t2, t2);
        #// # }
        i_ = 1
        while i_ < 20:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        #// # fe_mul(t1, t2, t1);
        #// # fe_sq(t1, t1);
        t1_ = self.fe_mul(t2_, t1_)
        t1_ = self.fe_sq(t1_)
        #// # for (i = 1; i < 10; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i_ = 1
        while i_ < 10:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0_ = self.fe_mul(t1_, t0_)
        t1_ = self.fe_sq(t0_)
        #// # for (i = 1; i < 50; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i_ = 1
        while i_ < 50:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        #// # fe_mul(t1, t1, t0);
        #// # fe_sq(t2, t1);
        t1_ = self.fe_mul(t1_, t0_)
        t2_ = self.fe_sq(t1_)
        #// # for (i = 1; i < 100; ++i) {
        #// #     fe_sq(t2, t2);
        #// # }
        i_ = 1
        while i_ < 100:
            
            t2_ = self.fe_sq(t2_)
            i_ += 1
        # end while
        #// # fe_mul(t1, t2, t1);
        #// # fe_sq(t1, t1);
        t1_ = self.fe_mul(t2_, t1_)
        t1_ = self.fe_sq(t1_)
        #// # for (i = 1; i < 50; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i_ = 1
        while i_ < 50:
            
            t1_ = self.fe_sq(t1_)
            i_ += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t0, t0);
        #// # fe_sq(t0, t0);
        #// # fe_mul(out, t0, z);
        t0_ = self.fe_mul(t1_, t0_)
        t0_ = self.fe_sq(t0_)
        t0_ = self.fe_sq(t0_)
        return self.fe_mul(t0_, z_)
    # end def fe_pow22523
    #// 
    #// Subtract two field elements.
    #// 
    #// h = f - g
    #// 
    #// Preconditions:
    #// |f| bounded by 1.1*2^25,1.1*2^24,1.1*2^25,1.1*2^24,etc.
    #// |g| bounded by 1.1*2^25,1.1*2^24,1.1*2^25,1.1*2^24,etc.
    #// 
    #// Postconditions:
    #// |h| bounded by 1.1*2^26,1.1*2^25,1.1*2^26,1.1*2^25,etc.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #// @psalm-suppress MixedTypeCoercion
    #//
    @classmethod
    def fe_sub(self, f_=None, g_=None):
        
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(f_[0].subint32(g_[0]), f_[1].subint32(g_[1]), f_[2].subint32(g_[2]), f_[3].subint32(g_[3]), f_[4].subint32(g_[4]), f_[5].subint32(g_[5]), f_[6].subint32(g_[6]), f_[7].subint32(g_[7]), f_[8].subint32(g_[8]), f_[9].subint32(g_[9])))
    # end def fe_sub
    #// 
    #// Add two group elements.
    #// 
    #// r = p + q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_add(self, p_=None, q_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r_.X = self.fe_add(p_.Y, p_.X)
        r_.Y = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_mul(r_.X, q_.YplusX)
        r_.Y = self.fe_mul(r_.Y, q_.YminusX)
        r_.T = self.fe_mul(q_.T2d, p_.T)
        r_.X = self.fe_mul(p_.Z, q_.Z)
        t0_ = self.fe_add(r_.X, r_.X)
        r_.X = self.fe_sub(r_.Z, r_.Y)
        r_.Y = self.fe_add(r_.Z, r_.Y)
        r_.Z = self.fe_add(t0_, r_.T)
        r_.T = self.fe_sub(t0_, r_.T)
        return r_
    # end def ge_add
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref https://github.com/jedisct1/libsodium/blob/157c4a80c13b117608aeae12178b2d38825f9f8f/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c#L1185-L1215
    #// @param string $a
    #// @return array<int, mixed>
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def slide(self, a_=None):
        
        
        if self.strlen(a_) < 256:
            if self.strlen(a_) < 16:
                a_ = php_str_pad(a_, 256, "0", STR_PAD_RIGHT)
            # end if
        # end if
        #// @var array<int, int> $r
        r_ = Array()
        i_ = 0
        while i_ < 256:
            
            r_[i_] = php_int(1 & self.chrtoint(a_[i_ >> 3]) >> i_ & 7)
            i_ += 1
        # end while
        i_ = 0
        while i_ < 256:
            
            if r_[i_]:
                b_ = 1
                while b_ <= 6 and i_ + b_ < 256:
                    
                    if r_[i_ + b_]:
                        if r_[i_] + r_[i_ + b_] << b_ <= 15:
                            r_[i_] += r_[i_ + b_] << b_
                            r_[i_ + b_] = 0
                        elif r_[i_] - r_[i_ + b_] << b_ >= -15:
                            r_[i_] -= r_[i_ + b_] << b_
                            k_ = i_ + b_
                            while k_ < 256:
                                
                                if (not r_[k_]):
                                    r_[k_] = 1
                                    break
                                # end if
                                r_[k_] = 0
                                k_ += 1
                            # end while
                        else:
                            break
                        # end if
                    # end if
                    b_ += 1
                # end while
            # end if
            i_ += 1
        # end while
        return r_
    # end def slide
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_frombytes_negate_vartime(self, s_=None):
        
        
        d_ = None
        if (not d_):
            #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d
            d_ = ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.d[0]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[1]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[2]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[3]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[4]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[5]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[6]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[7]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[8]), ParagonIE_Sodium_Core32_Int32.fromint(self.d[9])))
        # end if
        #// # fe_frombytes(h->Y,s);
        #// # fe_1(h->Z);
        h_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3(self.fe_0(), self.fe_frombytes(s_), self.fe_1()))
        #// # fe_sq(u,h->Y);
        #// # fe_mul(v,u,d);
        #// # fe_sub(u,u,h->Z);       /* u = y^2-1
        #// # fe_add(v,v,h->Z);       /* v = dy^2+1
        u_ = self.fe_sq(h_.Y)
        #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d
        v_ = self.fe_mul(u_, d_)
        u_ = self.fe_sub(u_, h_.Z)
        #// u =  y^2 - 1
        v_ = self.fe_add(v_, h_.Z)
        #// v = dy^2 + 1
        #// # fe_sq(v3,v);
        #// # fe_mul(v3,v3,v);        /* v3 = v^3
        #// # fe_sq(h->X,v3);
        #// # fe_mul(h->X,h->X,v);
        #// # fe_mul(h->X,h->X,u);    /* x = uv^7
        v3_ = self.fe_sq(v_)
        v3_ = self.fe_mul(v3_, v_)
        #// v3 = v^3
        h_.X = self.fe_sq(v3_)
        h_.X = self.fe_mul(h_.X, v_)
        h_.X = self.fe_mul(h_.X, u_)
        #// x = uv^7
        #// # fe_pow22523(h->X,h->X); /* x = (uv^7)^((q-5)/8)
        #// # fe_mul(h->X,h->X,v3);
        #// # fe_mul(h->X,h->X,u);    /* x = uv^3(uv^7)^((q-5)/8)
        h_.X = self.fe_pow22523(h_.X)
        #// x = (uv^7)^((q-5)/8)
        h_.X = self.fe_mul(h_.X, v3_)
        h_.X = self.fe_mul(h_.X, u_)
        #// x = uv^3(uv^7)^((q-5)/8)
        #// # fe_sq(vxx,h->X);
        #// # fe_mul(vxx,vxx,v);
        #// # fe_sub(check,vxx,u);    /* vx^2-u
        vxx_ = self.fe_sq(h_.X)
        vxx_ = self.fe_mul(vxx_, v_)
        check_ = self.fe_sub(vxx_, u_)
        #// vx^2 - u
        #// # if (fe_isnonzero(check)) {
        #// #     fe_add(check,vxx,u);  /* vx^2+u
        #// #     if (fe_isnonzero(check)) {
        #// #         return -1;
        #// #     }
        #// #     fe_mul(h->X,h->X,sqrtm1);
        #// # }
        if self.fe_isnonzero(check_):
            check_ = self.fe_add(vxx_, u_)
            #// vx^2 + u
            if self.fe_isnonzero(check_):
                raise php_new_class("RangeException", lambda : RangeException("Internal check failed."))
            # end if
            h_.X = self.fe_mul(h_.X, ParagonIE_Sodium_Core32_Curve25519_Fe.fromintarray(self.sqrtm1))
        # end if
        #// # if (fe_isnegative(h->X) == (s[31] >> 7)) {
        #// #     fe_neg(h->X,h->X);
        #// # }
        i_ = self.chrtoint(s_[31])
        if self.fe_isnegative(h_.X) == i_ >> 7:
            h_.X = self.fe_neg(h_.X)
        # end if
        #// # fe_mul(h->T,h->X,h->Y);
        h_.T = self.fe_mul(h_.X, h_.Y)
        return h_
    # end def ge_frombytes_negate_vartime
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_madd(self, R_=None, p_=None, q_=None):
        
        
        r_ = copy.deepcopy(R_)
        r_.X = self.fe_add(p_.Y, p_.X)
        r_.Y = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_mul(r_.X, q_.yplusx)
        r_.Y = self.fe_mul(r_.Y, q_.yminusx)
        r_.T = self.fe_mul(q_.xy2d, p_.T)
        t0_ = self.fe_add(copy.deepcopy(p_.Z), copy.deepcopy(p_.Z))
        r_.X = self.fe_sub(r_.Z, r_.Y)
        r_.Y = self.fe_add(r_.Z, r_.Y)
        r_.Z = self.fe_add(t0_, r_.T)
        r_.T = self.fe_sub(t0_, r_.T)
        return r_
    # end def ge_madd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_msub(self, R_=None, p_=None, q_=None):
        
        
        r_ = copy.deepcopy(R_)
        r_.X = self.fe_add(p_.Y, p_.X)
        r_.Y = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_mul(r_.X, q_.yminusx)
        r_.Y = self.fe_mul(r_.Y, q_.yplusx)
        r_.T = self.fe_mul(q_.xy2d, p_.T)
        t0_ = self.fe_add(p_.Z, p_.Z)
        r_.X = self.fe_sub(r_.Z, r_.Y)
        r_.Y = self.fe_add(r_.Z, r_.Y)
        r_.Z = self.fe_sub(t0_, r_.T)
        r_.T = self.fe_add(t0_, r_.T)
        return r_
    # end def ge_msub
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p1p1_to_p2(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2())
        r_.X = self.fe_mul(p_.X, p_.T)
        r_.Y = self.fe_mul(p_.Y, p_.Z)
        r_.Z = self.fe_mul(p_.Z, p_.T)
        return r_
    # end def ge_p1p1_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p1p1_to_p3(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3())
        r_.X = self.fe_mul(p_.X, p_.T)
        r_.Y = self.fe_mul(p_.Y, p_.Z)
        r_.Z = self.fe_mul(p_.Z, p_.T)
        r_.T = self.fe_mul(p_.X, p_.Y)
        return r_
    # end def ge_p1p1_to_p3
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p2_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2(self.fe_0(), self.fe_1(), self.fe_1()))
    # end def ge_p2_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p2_dbl(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r_.X = self.fe_sq(p_.X)
        r_.Z = self.fe_sq(p_.Y)
        r_.T = self.fe_sq2(p_.Z)
        r_.Y = self.fe_add(p_.X, p_.Y)
        t0_ = self.fe_sq(r_.Y)
        r_.Y = self.fe_add(r_.Z, r_.X)
        r_.Z = self.fe_sub(r_.Z, r_.X)
        r_.X = self.fe_sub(t0_, r_.Y)
        r_.T = self.fe_sub(r_.T, r_.Z)
        return r_
    # end def ge_p2_dbl
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3(self.fe_0(), self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_p3_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Cached
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_to_cached(self, p_=None):
        
        
        d2_ = None
        if d2_ == None:
            d2_ = ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.d2[0]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[1]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[2]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[3]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[4]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[5]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[6]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[7]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[8]), ParagonIE_Sodium_Core32_Int32.fromint(self.d2[9])))
        # end if
        #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d2
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Cached())
        r_.YplusX = self.fe_add(p_.Y, p_.X)
        r_.YminusX = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_copy(p_.Z)
        r_.T2d = self.fe_mul(p_.T, d2_)
        return r_
    # end def ge_p3_to_cached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p3_to_p2(self, p_=None):
        
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2(p_.X, p_.Y, p_.Z))
    # end def ge_p3_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_tobytes(self, h_=None):
        
        
        recip_ = self.fe_invert(h_.Z)
        x_ = self.fe_mul(h_.X, recip_)
        y_ = self.fe_mul(h_.Y, recip_)
        s_ = self.fe_tobytes(y_)
        s_[31] = self.inttochr(self.chrtoint(s_[31]) ^ self.fe_isnegative(x_) << 7)
        return s_
    # end def ge_p3_tobytes
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_dbl(self, p_=None):
        
        
        q_ = self.ge_p3_to_p2(p_)
        return self.ge_p2_dbl(q_)
    # end def ge_p3_dbl
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_precomp_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_precomp_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $b
    #// @param int $c
    #// @return int
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def equal(self, b_=None, c_=None):
        
        
        return php_int(b_ ^ c_ - 1 & 4294967295 >> 31)
    # end def equal
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string|int $char
    #// @return int (1 = yes, 0 = no)
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def negative(self, char_=None):
        
        
        if php_is_int(char_):
            return 1 if char_ < 0 else 0
        # end if
        #// @var string $char
        #// @var int $x
        x_ = self.chrtoint(self.substr(char_, 0, 1))
        return php_int(x_ >> 31)
    # end def negative
    #// 
    #// Conditional move
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $t
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $u
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def cmov(self, t_=None, u_=None, b_=None):
        
        
        if (not php_is_int(b_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer."))
        # end if
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_cmov(t_.yplusx, u_.yplusx, b_), self.fe_cmov(t_.yminusx, u_.yminusx, b_), self.fe_cmov(t_.xy2d, u_.xy2d, b_)))
    # end def cmov
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $pos
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayOffset
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def ge_select(self, pos_=0, b_=0):
        
        
        base_ = None
        if base_ == None:
            base_ = Array()
            for i_,bas_ in self.base:
                j_ = 0
                while j_ < 8:
                    
                    base_[i_][j_] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][0][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][1][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas_[j_][2][9])))))
                    j_ += 1
                # end while
            # end for
        # end if
        if (not php_is_int(pos_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Position must be an integer"))
        # end if
        if pos_ < 0 or pos_ > 31:
            raise php_new_class("RangeException", lambda : RangeException("Position is out of range [0, 31]"))
        # end if
        bnegative_ = self.negative(b_)
        #// @var int $babs
        babs_ = b_ - -bnegative_ & b_ << 1
        t_ = self.ge_precomp_0()
        i_ = 0
        while i_ < 8:
            
            t_ = self.cmov(t_, base_[pos_][i_], self.equal(babs_, i_ + 1))
            i_ += 1
        # end while
        minusT_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_copy(t_.yminusx), self.fe_copy(t_.yplusx), self.fe_neg(t_.xy2d)))
        return self.cmov(t_, minusT_, -bnegative_)
    # end def ge_select
    #// 
    #// Subtract two group elements.
    #// 
    #// r = p - q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_sub(self, p_=None, q_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r_.X = self.fe_add(p_.Y, p_.X)
        r_.Y = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_mul(r_.X, q_.YminusX)
        r_.Y = self.fe_mul(r_.Y, q_.YplusX)
        r_.T = self.fe_mul(q_.T2d, p_.T)
        r_.X = self.fe_mul(p_.Z, q_.Z)
        t0_ = self.fe_add(r_.X, r_.X)
        r_.X = self.fe_sub(r_.Z, r_.Y)
        r_.Y = self.fe_add(r_.Z, r_.Y)
        r_.Z = self.fe_sub(t0_, r_.T)
        r_.T = self.fe_add(t0_, r_.T)
        return r_
    # end def ge_sub
    #// 
    #// Convert a group element to a byte string.
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_tobytes(self, h_=None):
        
        
        recip_ = self.fe_invert(h_.Z)
        x_ = self.fe_mul(h_.X, recip_)
        y_ = self.fe_mul(h_.Y, recip_)
        s_ = self.fe_tobytes(y_)
        s_[31] = self.inttochr(self.chrtoint(s_[31]) ^ self.fe_isnegative(x_) << 7)
        return s_
    # end def ge_tobytes
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
    #// @param string $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    @classmethod
    def ge_double_scalarmult_vartime(self, a_=None, A_=None, b_=None):
        
        
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai
        Ai_ = Array()
        Bi_ = Array()
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp> $Bi
        if (not Bi_):
            i_ = 0
            while i_ < 8:
                
                Bi_[i_] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][0][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][1][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i_][2][9])))))
                i_ += 1
            # end while
        # end if
        i_ = 0
        while i_ < 8:
            
            Ai_[i_] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Cached(self.fe_0(), self.fe_0(), self.fe_0(), self.fe_0()))
            i_ += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai
        #// # slide(aslide,a);
        #// # slide(bslide,b);
        #// @var array<int, int> $aslide
        aslide_ = self.slide(a_)
        #// @var array<int, int> $bslide
        bslide_ = self.slide(b_)
        #// # ge_p3_to_cached(&Ai[0],A);
        #// # ge_p3_dbl(&t,A); ge_p1p1_to_p3(&A2,&t);
        Ai_[0] = self.ge_p3_to_cached(A_)
        t_ = self.ge_p3_dbl(A_)
        A2_ = self.ge_p1p1_to_p3(t_)
        #// # ge_add(&t,&A2,&Ai[0]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[1],&u);
        #// # ge_add(&t,&A2,&Ai[1]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[2],&u);
        #// # ge_add(&t,&A2,&Ai[2]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[3],&u);
        #// # ge_add(&t,&A2,&Ai[3]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[4],&u);
        #// # ge_add(&t,&A2,&Ai[4]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[5],&u);
        #// # ge_add(&t,&A2,&Ai[5]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[6],&u);
        #// # ge_add(&t,&A2,&Ai[6]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[7],&u);
        i_ = 0
        while i_ < 7:
            
            t_ = self.ge_add(A2_, Ai_[i_])
            u_ = self.ge_p1p1_to_p3(t_)
            Ai_[i_ + 1] = self.ge_p3_to_cached(u_)
            i_ += 1
        # end while
        #// # ge_p2_0(r);
        r_ = self.ge_p2_0()
        #// # for (i = 255;i >= 0;--i) {
        #// #     if (aslide[i] || bslide[i]) break;
        #// # }
        i_ = 255
        while i_ >= 0:
            
            if aslide_[i_] or bslide_[i_]:
                break
            # end if
            i_ -= 1
        # end while
        #// # for (;i >= 0;--i) {
        while i_ >= 0:
            
            #// # ge_p2_dbl(&t,r);
            t_ = self.ge_p2_dbl(r_)
            #// # if (aslide[i] > 0) {
            if aslide_[i_] > 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_add(&t,&u,&Ai[aslide[i]/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                t_ = self.ge_add(u_, Ai_[php_int(floor(aslide_[i_] / 2))])
                pass
            elif aslide_[i_] < 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_sub(&t,&u,&Ai[(-aslide[i])/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                t_ = self.ge_sub(u_, Ai_[php_int(floor(-aslide_[i_] / 2))])
            # end if
            #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp> $Bi
            #// # if (bslide[i] > 0) {
            if bslide_[i_] > 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_madd(&t,&u,&Bi[bslide[i]/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                #// @var int $index
                index_ = php_int(floor(bslide_[i_] / 2))
                #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $thisB
                thisB_ = Bi_[index_]
                t_ = self.ge_madd(t_, u_, thisB_)
                pass
            elif bslide_[i_] < 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_msub(&t,&u,&Bi[(-bslide[i])/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                #// @var int $index
                index_ = php_int(floor(-bslide_[i_] / 2))
                #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $thisB
                thisB_ = Bi_[index_]
                t_ = self.ge_msub(t_, u_, thisB_)
            # end if
            #// # ge_p1p1_to_p2(r,&t);
            r_ = self.ge_p1p1_to_p2(t_)
            i_ -= 1
        # end while
        return r_
    # end def ge_double_scalarmult_vartime
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_scalarmult_base(self, a_=None):
        
        
        #// @var array<int, int> $e
        e_ = Array()
        r_ = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        i_ = 0
        while i_ < 32:
            
            #// @var int $dbl
            dbl_ = php_int(i_) << 1
            e_[dbl_] = php_int(self.chrtoint(a_[i_])) & 15
            e_[dbl_ + 1] = php_int(self.chrtoint(a_[i_]) >> 4) & 15
            i_ += 1
        # end while
        #// @var int $carry
        carry_ = 0
        i_ = 0
        while i_ < 63:
            
            e_[i_] += carry_
            #// @var int $carry
            carry_ = e_[i_] + 8
            #// @var int $carry
            carry_ >>= 4
            e_[i_] -= carry_ << 4
            i_ += 1
        # end while
        #// @var array<int, int> $e
        e_[63] += php_int(carry_)
        h_ = self.ge_p3_0()
        i_ = 1
        while i_ < 64:
            
            t_ = self.ge_select(php_int(floor(i_ / 2)), php_int(e_[i_]))
            r_ = self.ge_madd(r_, h_, t_)
            h_ = self.ge_p1p1_to_p3(r_)
            i_ += 2
        # end while
        r_ = self.ge_p3_dbl(h_)
        s_ = self.ge_p1p1_to_p2(r_)
        r_ = self.ge_p2_dbl(s_)
        s_ = self.ge_p1p1_to_p2(r_)
        r_ = self.ge_p2_dbl(s_)
        s_ = self.ge_p1p1_to_p2(r_)
        r_ = self.ge_p2_dbl(s_)
        h_ = self.ge_p1p1_to_p3(r_)
        i_ = 0
        while i_ < 64:
            
            t_ = self.ge_select(i_ >> 1, php_int(e_[i_]))
            r_ = self.ge_madd(r_, h_, t_)
            h_ = self.ge_p1p1_to_p3(r_)
            i_ += 2
        # end while
        return h_
    # end def ge_scalarmult_base
    #// 
    #// Calculates (ab + c) mod l
    #// where l = 2^252 + 27742317777372353535851937790883648493
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param string $b
    #// @param string $c
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sc_muladd(self, a_=None, b_=None, c_=None):
        
        
        a0_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 0, 3)))
        a1_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a_, 2, 4)) >> 5)
        a2_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 5, 3)) >> 2)
        a3_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a_, 7, 4)) >> 7)
        a4_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a_, 10, 4)) >> 4)
        a5_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 13, 3)) >> 1)
        a6_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a_, 15, 4)) >> 6)
        a7_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 18, 3)) >> 3)
        a8_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 21, 3)))
        a9_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a_, 23, 4)) >> 5)
        a10_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a_, 26, 3)) >> 2)
        a11_ = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(a_, 28, 4)) >> 7)
        b0_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 0, 3)))
        b1_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b_, 2, 4)) >> 5)
        b2_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 5, 3)) >> 2)
        b3_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b_, 7, 4)) >> 7)
        b4_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b_, 10, 4)) >> 4)
        b5_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 13, 3)) >> 1)
        b6_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b_, 15, 4)) >> 6)
        b7_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 18, 3)) >> 3)
        b8_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 21, 3)))
        b9_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b_, 23, 4)) >> 5)
        b10_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b_, 26, 3)) >> 2)
        b11_ = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(b_, 28, 4)) >> 7)
        c0_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 0, 3)))
        c1_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c_, 2, 4)) >> 5)
        c2_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 5, 3)) >> 2)
        c3_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c_, 7, 4)) >> 7)
        c4_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c_, 10, 4)) >> 4)
        c5_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 13, 3)) >> 1)
        c6_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c_, 15, 4)) >> 6)
        c7_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 18, 3)) >> 3)
        c8_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 21, 3)))
        c9_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c_, 23, 4)) >> 5)
        c10_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c_, 26, 3)) >> 2)
        c11_ = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(c_, 28, 4)) >> 7)
        #// Can't really avoid the pyramid here:
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $s0
        #// @var ParagonIE_Sodium_Core32_Int64 $s1
        #// @var ParagonIE_Sodium_Core32_Int64 $s2
        #// @var ParagonIE_Sodium_Core32_Int64 $s3
        #// @var ParagonIE_Sodium_Core32_Int64 $s4
        #// @var ParagonIE_Sodium_Core32_Int64 $s5
        #// @var ParagonIE_Sodium_Core32_Int64 $s6
        #// @var ParagonIE_Sodium_Core32_Int64 $s7
        #// @var ParagonIE_Sodium_Core32_Int64 $s8
        #// @var ParagonIE_Sodium_Core32_Int64 $s9
        #// @var ParagonIE_Sodium_Core32_Int64 $s10
        #// @var ParagonIE_Sodium_Core32_Int64 $s11
        #// @var ParagonIE_Sodium_Core32_Int64 $s12
        #// @var ParagonIE_Sodium_Core32_Int64 $s13
        #// @var ParagonIE_Sodium_Core32_Int64 $s14
        #// @var ParagonIE_Sodium_Core32_Int64 $s15
        #// @var ParagonIE_Sodium_Core32_Int64 $s16
        #// @var ParagonIE_Sodium_Core32_Int64 $s17
        #// @var ParagonIE_Sodium_Core32_Int64 $s18
        #// @var ParagonIE_Sodium_Core32_Int64 $s19
        #// @var ParagonIE_Sodium_Core32_Int64 $s20
        #// @var ParagonIE_Sodium_Core32_Int64 $s21
        #// @var ParagonIE_Sodium_Core32_Int64 $s22
        #// @var ParagonIE_Sodium_Core32_Int64 $s23
        #//
        s0_ = c0_.addint64(a0_.mulint64(b0_, 24))
        s1_ = c1_.addint64(a0_.mulint64(b1_, 24)).addint64(a1_.mulint64(b0_, 24))
        s2_ = c2_.addint64(a0_.mulint64(b2_, 24)).addint64(a1_.mulint64(b1_, 24)).addint64(a2_.mulint64(b0_, 24))
        s3_ = c3_.addint64(a0_.mulint64(b3_, 24)).addint64(a1_.mulint64(b2_, 24)).addint64(a2_.mulint64(b1_, 24)).addint64(a3_.mulint64(b0_, 24))
        s4_ = c4_.addint64(a0_.mulint64(b4_, 24)).addint64(a1_.mulint64(b3_, 24)).addint64(a2_.mulint64(b2_, 24)).addint64(a3_.mulint64(b1_, 24)).addint64(a4_.mulint64(b0_, 24))
        s5_ = c5_.addint64(a0_.mulint64(b5_, 24)).addint64(a1_.mulint64(b4_, 24)).addint64(a2_.mulint64(b3_, 24)).addint64(a3_.mulint64(b2_, 24)).addint64(a4_.mulint64(b1_, 24)).addint64(a5_.mulint64(b0_, 24))
        s6_ = c6_.addint64(a0_.mulint64(b6_, 24)).addint64(a1_.mulint64(b5_, 24)).addint64(a2_.mulint64(b4_, 24)).addint64(a3_.mulint64(b3_, 24)).addint64(a4_.mulint64(b2_, 24)).addint64(a5_.mulint64(b1_, 24)).addint64(a6_.mulint64(b0_, 24))
        s7_ = c7_.addint64(a0_.mulint64(b7_, 24)).addint64(a1_.mulint64(b6_, 24)).addint64(a2_.mulint64(b5_, 24)).addint64(a3_.mulint64(b4_, 24)).addint64(a4_.mulint64(b3_, 24)).addint64(a5_.mulint64(b2_, 24)).addint64(a6_.mulint64(b1_, 24)).addint64(a7_.mulint64(b0_, 24))
        s8_ = c8_.addint64(a0_.mulint64(b8_, 24)).addint64(a1_.mulint64(b7_, 24)).addint64(a2_.mulint64(b6_, 24)).addint64(a3_.mulint64(b5_, 24)).addint64(a4_.mulint64(b4_, 24)).addint64(a5_.mulint64(b3_, 24)).addint64(a6_.mulint64(b2_, 24)).addint64(a7_.mulint64(b1_, 24)).addint64(a8_.mulint64(b0_, 24))
        s9_ = c9_.addint64(a0_.mulint64(b9_, 24)).addint64(a1_.mulint64(b8_, 24)).addint64(a2_.mulint64(b7_, 24)).addint64(a3_.mulint64(b6_, 24)).addint64(a4_.mulint64(b5_, 24)).addint64(a5_.mulint64(b4_, 24)).addint64(a6_.mulint64(b3_, 24)).addint64(a7_.mulint64(b2_, 24)).addint64(a8_.mulint64(b1_, 24)).addint64(a9_.mulint64(b0_, 24))
        s10_ = c10_.addint64(a0_.mulint64(b10_, 24)).addint64(a1_.mulint64(b9_, 24)).addint64(a2_.mulint64(b8_, 24)).addint64(a3_.mulint64(b7_, 24)).addint64(a4_.mulint64(b6_, 24)).addint64(a5_.mulint64(b5_, 24)).addint64(a6_.mulint64(b4_, 24)).addint64(a7_.mulint64(b3_, 24)).addint64(a8_.mulint64(b2_, 24)).addint64(a9_.mulint64(b1_, 24)).addint64(a10_.mulint64(b0_, 24))
        s11_ = c11_.addint64(a0_.mulint64(b11_, 24)).addint64(a1_.mulint64(b10_, 24)).addint64(a2_.mulint64(b9_, 24)).addint64(a3_.mulint64(b8_, 24)).addint64(a4_.mulint64(b7_, 24)).addint64(a5_.mulint64(b6_, 24)).addint64(a6_.mulint64(b5_, 24)).addint64(a7_.mulint64(b4_, 24)).addint64(a8_.mulint64(b3_, 24)).addint64(a9_.mulint64(b2_, 24)).addint64(a10_.mulint64(b1_, 24)).addint64(a11_.mulint64(b0_, 24))
        s12_ = a1_.mulint64(b11_, 24).addint64(a2_.mulint64(b10_, 24)).addint64(a3_.mulint64(b9_, 24)).addint64(a4_.mulint64(b8_, 24)).addint64(a5_.mulint64(b7_, 24)).addint64(a6_.mulint64(b6_, 24)).addint64(a7_.mulint64(b5_, 24)).addint64(a8_.mulint64(b4_, 24)).addint64(a9_.mulint64(b3_, 24)).addint64(a10_.mulint64(b2_, 24)).addint64(a11_.mulint64(b1_, 24))
        s13_ = a2_.mulint64(b11_, 24).addint64(a3_.mulint64(b10_, 24)).addint64(a4_.mulint64(b9_, 24)).addint64(a5_.mulint64(b8_, 24)).addint64(a6_.mulint64(b7_, 24)).addint64(a7_.mulint64(b6_, 24)).addint64(a8_.mulint64(b5_, 24)).addint64(a9_.mulint64(b4_, 24)).addint64(a10_.mulint64(b3_, 24)).addint64(a11_.mulint64(b2_, 24))
        s14_ = a3_.mulint64(b11_, 24).addint64(a4_.mulint64(b10_, 24)).addint64(a5_.mulint64(b9_, 24)).addint64(a6_.mulint64(b8_, 24)).addint64(a7_.mulint64(b7_, 24)).addint64(a8_.mulint64(b6_, 24)).addint64(a9_.mulint64(b5_, 24)).addint64(a10_.mulint64(b4_, 24)).addint64(a11_.mulint64(b3_, 24))
        s15_ = a4_.mulint64(b11_, 24).addint64(a5_.mulint64(b10_, 24)).addint64(a6_.mulint64(b9_, 24)).addint64(a7_.mulint64(b8_, 24)).addint64(a8_.mulint64(b7_, 24)).addint64(a9_.mulint64(b6_, 24)).addint64(a10_.mulint64(b5_, 24)).addint64(a11_.mulint64(b4_, 24))
        s16_ = a5_.mulint64(b11_, 24).addint64(a6_.mulint64(b10_, 24)).addint64(a7_.mulint64(b9_, 24)).addint64(a8_.mulint64(b8_, 24)).addint64(a9_.mulint64(b7_, 24)).addint64(a10_.mulint64(b6_, 24)).addint64(a11_.mulint64(b5_, 24))
        s17_ = a6_.mulint64(b11_, 24).addint64(a7_.mulint64(b10_, 24)).addint64(a8_.mulint64(b9_, 24)).addint64(a9_.mulint64(b8_, 24)).addint64(a10_.mulint64(b7_, 24)).addint64(a11_.mulint64(b6_, 24))
        s18_ = a7_.mulint64(b11_, 24).addint64(a8_.mulint64(b10_, 24)).addint64(a9_.mulint64(b9_, 24)).addint64(a10_.mulint64(b8_, 24)).addint64(a11_.mulint64(b7_, 24))
        s19_ = a8_.mulint64(b11_, 24).addint64(a9_.mulint64(b10_, 24)).addint64(a10_.mulint64(b9_, 24)).addint64(a11_.mulint64(b8_, 24))
        s20_ = a9_.mulint64(b11_, 24).addint64(a10_.mulint64(b10_, 24)).addint64(a11_.mulint64(b9_, 24))
        s21_ = a10_.mulint64(b11_, 24).addint64(a11_.mulint64(b10_, 24))
        s22_ = a11_.mulint64(b11_, 24)
        s23_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0_ = s0_.addint(1 << 20).shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry2_ = s2_.addint(1 << 20).shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry4_ = s4_.addint(1 << 20).shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry6_ = s6_.addint(1 << 20).shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry8_ = s8_.addint(1 << 20).shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry10_ = s10_.addint(1 << 20).shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry12_ = s12_.addint(1 << 20).shiftright(21)
        s13_ = s13_.addint64(carry12_)
        s12_ = s12_.subint64(carry12_.shiftleft(21))
        carry14_ = s14_.addint(1 << 20).shiftright(21)
        s15_ = s15_.addint64(carry14_)
        s14_ = s14_.subint64(carry14_.shiftleft(21))
        carry16_ = s16_.addint(1 << 20).shiftright(21)
        s17_ = s17_.addint64(carry16_)
        s16_ = s16_.subint64(carry16_.shiftleft(21))
        carry18_ = s18_.addint(1 << 20).shiftright(21)
        s19_ = s19_.addint64(carry18_)
        s18_ = s18_.subint64(carry18_.shiftleft(21))
        carry20_ = s20_.addint(1 << 20).shiftright(21)
        s21_ = s21_.addint64(carry20_)
        s20_ = s20_.subint64(carry20_.shiftleft(21))
        carry22_ = s22_.addint(1 << 20).shiftright(21)
        s23_ = s23_.addint64(carry22_)
        s22_ = s22_.subint64(carry22_.shiftleft(21))
        carry1_ = s1_.addint(1 << 20).shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry3_ = s3_.addint(1 << 20).shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry5_ = s5_.addint(1 << 20).shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry7_ = s7_.addint(1 << 20).shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry9_ = s9_.addint(1 << 20).shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry11_ = s11_.addint(1 << 20).shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        carry13_ = s13_.addint(1 << 20).shiftright(21)
        s14_ = s14_.addint64(carry13_)
        s13_ = s13_.subint64(carry13_.shiftleft(21))
        carry15_ = s15_.addint(1 << 20).shiftright(21)
        s16_ = s16_.addint64(carry15_)
        s15_ = s15_.subint64(carry15_.shiftleft(21))
        carry17_ = s17_.addint(1 << 20).shiftright(21)
        s18_ = s18_.addint64(carry17_)
        s17_ = s17_.subint64(carry17_.shiftleft(21))
        carry19_ = s19_.addint(1 << 20).shiftright(21)
        s20_ = s20_.addint64(carry19_)
        s19_ = s19_.subint64(carry19_.shiftleft(21))
        carry21_ = s21_.addint(1 << 20).shiftright(21)
        s22_ = s22_.addint64(carry21_)
        s21_ = s21_.subint64(carry21_.shiftleft(21))
        s11_ = s11_.addint64(s23_.mulint(666643, 20))
        s12_ = s12_.addint64(s23_.mulint(470296, 19))
        s13_ = s13_.addint64(s23_.mulint(654183, 20))
        s14_ = s14_.subint64(s23_.mulint(997805, 20))
        s15_ = s15_.addint64(s23_.mulint(136657, 18))
        s16_ = s16_.subint64(s23_.mulint(683901, 20))
        s10_ = s10_.addint64(s22_.mulint(666643, 20))
        s11_ = s11_.addint64(s22_.mulint(470296, 19))
        s12_ = s12_.addint64(s22_.mulint(654183, 20))
        s13_ = s13_.subint64(s22_.mulint(997805, 20))
        s14_ = s14_.addint64(s22_.mulint(136657, 18))
        s15_ = s15_.subint64(s22_.mulint(683901, 20))
        s9_ = s9_.addint64(s21_.mulint(666643, 20))
        s10_ = s10_.addint64(s21_.mulint(470296, 19))
        s11_ = s11_.addint64(s21_.mulint(654183, 20))
        s12_ = s12_.subint64(s21_.mulint(997805, 20))
        s13_ = s13_.addint64(s21_.mulint(136657, 18))
        s14_ = s14_.subint64(s21_.mulint(683901, 20))
        s8_ = s8_.addint64(s20_.mulint(666643, 20))
        s9_ = s9_.addint64(s20_.mulint(470296, 19))
        s10_ = s10_.addint64(s20_.mulint(654183, 20))
        s11_ = s11_.subint64(s20_.mulint(997805, 20))
        s12_ = s12_.addint64(s20_.mulint(136657, 18))
        s13_ = s13_.subint64(s20_.mulint(683901, 20))
        s7_ = s7_.addint64(s19_.mulint(666643, 20))
        s8_ = s8_.addint64(s19_.mulint(470296, 19))
        s9_ = s9_.addint64(s19_.mulint(654183, 20))
        s10_ = s10_.subint64(s19_.mulint(997805, 20))
        s11_ = s11_.addint64(s19_.mulint(136657, 18))
        s12_ = s12_.subint64(s19_.mulint(683901, 20))
        s6_ = s6_.addint64(s18_.mulint(666643, 20))
        s7_ = s7_.addint64(s18_.mulint(470296, 19))
        s8_ = s8_.addint64(s18_.mulint(654183, 20))
        s9_ = s9_.subint64(s18_.mulint(997805, 20))
        s10_ = s10_.addint64(s18_.mulint(136657, 18))
        s11_ = s11_.subint64(s18_.mulint(683901, 20))
        carry6_ = s6_.addint(1 << 20).shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry8_ = s8_.addint(1 << 20).shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry10_ = s10_.addint(1 << 20).shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry12_ = s12_.addint(1 << 20).shiftright(21)
        s13_ = s13_.addint64(carry12_)
        s12_ = s12_.subint64(carry12_.shiftleft(21))
        carry14_ = s14_.addint(1 << 20).shiftright(21)
        s15_ = s15_.addint64(carry14_)
        s14_ = s14_.subint64(carry14_.shiftleft(21))
        carry16_ = s16_.addint(1 << 20).shiftright(21)
        s17_ = s17_.addint64(carry16_)
        s16_ = s16_.subint64(carry16_.shiftleft(21))
        carry7_ = s7_.addint(1 << 20).shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry9_ = s9_.addint(1 << 20).shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry11_ = s11_.addint(1 << 20).shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        carry13_ = s13_.addint(1 << 20).shiftright(21)
        s14_ = s14_.addint64(carry13_)
        s13_ = s13_.subint64(carry13_.shiftleft(21))
        carry15_ = s15_.addint(1 << 20).shiftright(21)
        s16_ = s16_.addint64(carry15_)
        s15_ = s15_.subint64(carry15_.shiftleft(21))
        s5_ = s5_.addint64(s17_.mulint(666643, 20))
        s6_ = s6_.addint64(s17_.mulint(470296, 19))
        s7_ = s7_.addint64(s17_.mulint(654183, 20))
        s8_ = s8_.subint64(s17_.mulint(997805, 20))
        s9_ = s9_.addint64(s17_.mulint(136657, 18))
        s10_ = s10_.subint64(s17_.mulint(683901, 20))
        s4_ = s4_.addint64(s16_.mulint(666643, 20))
        s5_ = s5_.addint64(s16_.mulint(470296, 19))
        s6_ = s6_.addint64(s16_.mulint(654183, 20))
        s7_ = s7_.subint64(s16_.mulint(997805, 20))
        s8_ = s8_.addint64(s16_.mulint(136657, 18))
        s9_ = s9_.subint64(s16_.mulint(683901, 20))
        s3_ = s3_.addint64(s15_.mulint(666643, 20))
        s4_ = s4_.addint64(s15_.mulint(470296, 19))
        s5_ = s5_.addint64(s15_.mulint(654183, 20))
        s6_ = s6_.subint64(s15_.mulint(997805, 20))
        s7_ = s7_.addint64(s15_.mulint(136657, 18))
        s8_ = s8_.subint64(s15_.mulint(683901, 20))
        s2_ = s2_.addint64(s14_.mulint(666643, 20))
        s3_ = s3_.addint64(s14_.mulint(470296, 19))
        s4_ = s4_.addint64(s14_.mulint(654183, 20))
        s5_ = s5_.subint64(s14_.mulint(997805, 20))
        s6_ = s6_.addint64(s14_.mulint(136657, 18))
        s7_ = s7_.subint64(s14_.mulint(683901, 20))
        s1_ = s1_.addint64(s13_.mulint(666643, 20))
        s2_ = s2_.addint64(s13_.mulint(470296, 19))
        s3_ = s3_.addint64(s13_.mulint(654183, 20))
        s4_ = s4_.subint64(s13_.mulint(997805, 20))
        s5_ = s5_.addint64(s13_.mulint(136657, 18))
        s6_ = s6_.subint64(s13_.mulint(683901, 20))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        s12_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0_ = s0_.addint(1 << 20).shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry2_ = s2_.addint(1 << 20).shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry4_ = s4_.addint(1 << 20).shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry6_ = s6_.addint(1 << 20).shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry8_ = s8_.addint(1 << 20).shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry10_ = s10_.addint(1 << 20).shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry1_ = s1_.addint(1 << 20).shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry3_ = s3_.addint(1 << 20).shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry5_ = s5_.addint(1 << 20).shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry7_ = s7_.addint(1 << 20).shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry9_ = s9_.addint(1 << 20).shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry11_ = s11_.addint(1 << 20).shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        s12_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0_ = s0_.shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry1_ = s1_.shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry2_ = s2_.shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry3_ = s3_.shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry4_ = s4_.shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry5_ = s5_.shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry6_ = s6_.shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry7_ = s7_.shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry8_ = s8_.shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry9_ = s9_.shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry10_ = s10_.shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry11_ = s11_.shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        carry0_ = s0_.shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry1_ = s1_.shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry2_ = s2_.shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry3_ = s3_.shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry4_ = s4_.shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry5_ = s5_.shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry6_ = s6_.shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry7_ = s7_.shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry8_ = s10_.shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry9_ = s9_.shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry10_ = s10_.shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        S0_ = s0_.toint()
        S1_ = s1_.toint()
        S2_ = s2_.toint()
        S3_ = s3_.toint()
        S4_ = s4_.toint()
        S5_ = s5_.toint()
        S6_ = s6_.toint()
        S7_ = s7_.toint()
        S8_ = s8_.toint()
        S9_ = s9_.toint()
        S10_ = s10_.toint()
        S11_ = s11_.toint()
        #// 
        #// @var array<int, int>
        #//
        arr_ = Array(php_int(255 & S0_ >> 0), php_int(255 & S0_ >> 8), php_int(255 & S0_ >> 16 | S1_ << 5), php_int(255 & S1_ >> 3), php_int(255 & S1_ >> 11), php_int(255 & S1_ >> 19 | S2_ << 2), php_int(255 & S2_ >> 6), php_int(255 & S2_ >> 14 | S3_ << 7), php_int(255 & S3_ >> 1), php_int(255 & S3_ >> 9), php_int(255 & S3_ >> 17 | S4_ << 4), php_int(255 & S4_ >> 4), php_int(255 & S4_ >> 12), php_int(255 & S4_ >> 20 | S5_ << 1), php_int(255 & S5_ >> 7), php_int(255 & S5_ >> 15 | S6_ << 6), php_int(255 & S6_ >> 2), php_int(255 & S6_ >> 10), php_int(255 & S6_ >> 18 | S7_ << 3), php_int(255 & S7_ >> 5), php_int(255 & S7_ >> 13), php_int(255 & S8_ >> 0), php_int(255 & S8_ >> 8), php_int(255 & S8_ >> 16 | S9_ << 5), php_int(255 & S9_ >> 3), php_int(255 & S9_ >> 11), php_int(255 & S9_ >> 19 | S10_ << 2), php_int(255 & S10_ >> 6), php_int(255 & S10_ >> 14 | S11_ << 7), php_int(255 & S11_ >> 1), php_int(255 & S11_ >> 9), php_int(255 & S11_ >> 17))
        return self.intarraytostring(arr_)
    # end def sc_muladd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sc_reduce(self, s_=None):
        
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $s0
        #// @var ParagonIE_Sodium_Core32_Int64 $s1
        #// @var ParagonIE_Sodium_Core32_Int64 $s2
        #// @var ParagonIE_Sodium_Core32_Int64 $s3
        #// @var ParagonIE_Sodium_Core32_Int64 $s4
        #// @var ParagonIE_Sodium_Core32_Int64 $s5
        #// @var ParagonIE_Sodium_Core32_Int64 $s6
        #// @var ParagonIE_Sodium_Core32_Int64 $s7
        #// @var ParagonIE_Sodium_Core32_Int64 $s8
        #// @var ParagonIE_Sodium_Core32_Int64 $s9
        #// @var ParagonIE_Sodium_Core32_Int64 $s10
        #// @var ParagonIE_Sodium_Core32_Int64 $s11
        #// @var ParagonIE_Sodium_Core32_Int64 $s12
        #// @var ParagonIE_Sodium_Core32_Int64 $s13
        #// @var ParagonIE_Sodium_Core32_Int64 $s14
        #// @var ParagonIE_Sodium_Core32_Int64 $s15
        #// @var ParagonIE_Sodium_Core32_Int64 $s16
        #// @var ParagonIE_Sodium_Core32_Int64 $s17
        #// @var ParagonIE_Sodium_Core32_Int64 $s18
        #// @var ParagonIE_Sodium_Core32_Int64 $s19
        #// @var ParagonIE_Sodium_Core32_Int64 $s20
        #// @var ParagonIE_Sodium_Core32_Int64 $s21
        #// @var ParagonIE_Sodium_Core32_Int64 $s22
        #// @var ParagonIE_Sodium_Core32_Int64 $s23
        #//
        s0_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 0, 3)))
        s1_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 2, 4)) >> 5)
        s2_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 5, 3)) >> 2)
        s3_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 7, 4)) >> 7)
        s4_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 10, 4)) >> 4)
        s5_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 13, 3)) >> 1)
        s6_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 15, 4)) >> 6)
        s7_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 18, 4)) >> 3)
        s8_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 21, 3)))
        s9_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 23, 4)) >> 5)
        s10_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 26, 3)) >> 2)
        s11_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 28, 4)) >> 7)
        s12_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 31, 4)) >> 4)
        s13_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 34, 3)) >> 1)
        s14_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 36, 4)) >> 6)
        s15_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 39, 4)) >> 3)
        s16_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 42, 3)))
        s17_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 44, 4)) >> 5)
        s18_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 47, 3)) >> 2)
        s19_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 49, 4)) >> 7)
        s20_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 52, 4)) >> 4)
        s21_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s_, 55, 3)) >> 1)
        s22_ = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s_, 57, 4)) >> 6)
        s23_ = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(s_, 60, 4)) >> 3)
        s11_ = s11_.addint64(s23_.mulint(666643, 20))
        s12_ = s12_.addint64(s23_.mulint(470296, 19))
        s13_ = s13_.addint64(s23_.mulint(654183, 20))
        s14_ = s14_.subint64(s23_.mulint(997805, 20))
        s15_ = s15_.addint64(s23_.mulint(136657, 18))
        s16_ = s16_.subint64(s23_.mulint(683901, 20))
        s10_ = s10_.addint64(s22_.mulint(666643, 20))
        s11_ = s11_.addint64(s22_.mulint(470296, 19))
        s12_ = s12_.addint64(s22_.mulint(654183, 20))
        s13_ = s13_.subint64(s22_.mulint(997805, 20))
        s14_ = s14_.addint64(s22_.mulint(136657, 18))
        s15_ = s15_.subint64(s22_.mulint(683901, 20))
        s9_ = s9_.addint64(s21_.mulint(666643, 20))
        s10_ = s10_.addint64(s21_.mulint(470296, 19))
        s11_ = s11_.addint64(s21_.mulint(654183, 20))
        s12_ = s12_.subint64(s21_.mulint(997805, 20))
        s13_ = s13_.addint64(s21_.mulint(136657, 18))
        s14_ = s14_.subint64(s21_.mulint(683901, 20))
        s8_ = s8_.addint64(s20_.mulint(666643, 20))
        s9_ = s9_.addint64(s20_.mulint(470296, 19))
        s10_ = s10_.addint64(s20_.mulint(654183, 20))
        s11_ = s11_.subint64(s20_.mulint(997805, 20))
        s12_ = s12_.addint64(s20_.mulint(136657, 18))
        s13_ = s13_.subint64(s20_.mulint(683901, 20))
        s7_ = s7_.addint64(s19_.mulint(666643, 20))
        s8_ = s8_.addint64(s19_.mulint(470296, 19))
        s9_ = s9_.addint64(s19_.mulint(654183, 20))
        s10_ = s10_.subint64(s19_.mulint(997805, 20))
        s11_ = s11_.addint64(s19_.mulint(136657, 18))
        s12_ = s12_.subint64(s19_.mulint(683901, 20))
        s6_ = s6_.addint64(s18_.mulint(666643, 20))
        s7_ = s7_.addint64(s18_.mulint(470296, 19))
        s8_ = s8_.addint64(s18_.mulint(654183, 20))
        s9_ = s9_.subint64(s18_.mulint(997805, 20))
        s10_ = s10_.addint64(s18_.mulint(136657, 18))
        s11_ = s11_.subint64(s18_.mulint(683901, 20))
        carry6_ = s6_.addint(1 << 20).shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry8_ = s8_.addint(1 << 20).shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry10_ = s10_.addint(1 << 20).shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry12_ = s12_.addint(1 << 20).shiftright(21)
        s13_ = s13_.addint64(carry12_)
        s12_ = s12_.subint64(carry12_.shiftleft(21))
        carry14_ = s14_.addint(1 << 20).shiftright(21)
        s15_ = s15_.addint64(carry14_)
        s14_ = s14_.subint64(carry14_.shiftleft(21))
        carry16_ = s16_.addint(1 << 20).shiftright(21)
        s17_ = s17_.addint64(carry16_)
        s16_ = s16_.subint64(carry16_.shiftleft(21))
        carry7_ = s7_.addint(1 << 20).shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry9_ = s9_.addint(1 << 20).shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry11_ = s11_.addint(1 << 20).shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        carry13_ = s13_.addint(1 << 20).shiftright(21)
        s14_ = s14_.addint64(carry13_)
        s13_ = s13_.subint64(carry13_.shiftleft(21))
        carry15_ = s15_.addint(1 << 20).shiftright(21)
        s16_ = s16_.addint64(carry15_)
        s15_ = s15_.subint64(carry15_.shiftleft(21))
        s5_ = s5_.addint64(s17_.mulint(666643, 20))
        s6_ = s6_.addint64(s17_.mulint(470296, 19))
        s7_ = s7_.addint64(s17_.mulint(654183, 20))
        s8_ = s8_.subint64(s17_.mulint(997805, 20))
        s9_ = s9_.addint64(s17_.mulint(136657, 18))
        s10_ = s10_.subint64(s17_.mulint(683901, 20))
        s4_ = s4_.addint64(s16_.mulint(666643, 20))
        s5_ = s5_.addint64(s16_.mulint(470296, 19))
        s6_ = s6_.addint64(s16_.mulint(654183, 20))
        s7_ = s7_.subint64(s16_.mulint(997805, 20))
        s8_ = s8_.addint64(s16_.mulint(136657, 18))
        s9_ = s9_.subint64(s16_.mulint(683901, 20))
        s3_ = s3_.addint64(s15_.mulint(666643, 20))
        s4_ = s4_.addint64(s15_.mulint(470296, 19))
        s5_ = s5_.addint64(s15_.mulint(654183, 20))
        s6_ = s6_.subint64(s15_.mulint(997805, 20))
        s7_ = s7_.addint64(s15_.mulint(136657, 18))
        s8_ = s8_.subint64(s15_.mulint(683901, 20))
        s2_ = s2_.addint64(s14_.mulint(666643, 20))
        s3_ = s3_.addint64(s14_.mulint(470296, 19))
        s4_ = s4_.addint64(s14_.mulint(654183, 20))
        s5_ = s5_.subint64(s14_.mulint(997805, 20))
        s6_ = s6_.addint64(s14_.mulint(136657, 18))
        s7_ = s7_.subint64(s14_.mulint(683901, 20))
        s1_ = s1_.addint64(s13_.mulint(666643, 20))
        s2_ = s2_.addint64(s13_.mulint(470296, 19))
        s3_ = s3_.addint64(s13_.mulint(654183, 20))
        s4_ = s4_.subint64(s13_.mulint(997805, 20))
        s5_ = s5_.addint64(s13_.mulint(136657, 18))
        s6_ = s6_.subint64(s13_.mulint(683901, 20))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        s12_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0_ = s0_.addint(1 << 20).shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry2_ = s2_.addint(1 << 20).shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry4_ = s4_.addint(1 << 20).shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry6_ = s6_.addint(1 << 20).shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry8_ = s8_.addint(1 << 20).shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry10_ = s10_.addint(1 << 20).shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry1_ = s1_.addint(1 << 20).shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry3_ = s3_.addint(1 << 20).shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry5_ = s5_.addint(1 << 20).shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry7_ = s7_.addint(1 << 20).shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry9_ = s9_.addint(1 << 20).shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry11_ = s11_.addint(1 << 20).shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        s12_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0_ = s0_.shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry1_ = s1_.shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry2_ = s2_.shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry3_ = s3_.shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry4_ = s4_.shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry5_ = s5_.shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry6_ = s6_.shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry7_ = s7_.shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry8_ = s8_.shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry9_ = s9_.shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry10_ = s10_.shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        carry11_ = s11_.shiftright(21)
        s12_ = s12_.addint64(carry11_)
        s11_ = s11_.subint64(carry11_.shiftleft(21))
        s0_ = s0_.addint64(s12_.mulint(666643, 20))
        s1_ = s1_.addint64(s12_.mulint(470296, 19))
        s2_ = s2_.addint64(s12_.mulint(654183, 20))
        s3_ = s3_.subint64(s12_.mulint(997805, 20))
        s4_ = s4_.addint64(s12_.mulint(136657, 18))
        s5_ = s5_.subint64(s12_.mulint(683901, 20))
        carry0_ = s0_.shiftright(21)
        s1_ = s1_.addint64(carry0_)
        s0_ = s0_.subint64(carry0_.shiftleft(21))
        carry1_ = s1_.shiftright(21)
        s2_ = s2_.addint64(carry1_)
        s1_ = s1_.subint64(carry1_.shiftleft(21))
        carry2_ = s2_.shiftright(21)
        s3_ = s3_.addint64(carry2_)
        s2_ = s2_.subint64(carry2_.shiftleft(21))
        carry3_ = s3_.shiftright(21)
        s4_ = s4_.addint64(carry3_)
        s3_ = s3_.subint64(carry3_.shiftleft(21))
        carry4_ = s4_.shiftright(21)
        s5_ = s5_.addint64(carry4_)
        s4_ = s4_.subint64(carry4_.shiftleft(21))
        carry5_ = s5_.shiftright(21)
        s6_ = s6_.addint64(carry5_)
        s5_ = s5_.subint64(carry5_.shiftleft(21))
        carry6_ = s6_.shiftright(21)
        s7_ = s7_.addint64(carry6_)
        s6_ = s6_.subint64(carry6_.shiftleft(21))
        carry7_ = s7_.shiftright(21)
        s8_ = s8_.addint64(carry7_)
        s7_ = s7_.subint64(carry7_.shiftleft(21))
        carry8_ = s8_.shiftright(21)
        s9_ = s9_.addint64(carry8_)
        s8_ = s8_.subint64(carry8_.shiftleft(21))
        carry9_ = s9_.shiftright(21)
        s10_ = s10_.addint64(carry9_)
        s9_ = s9_.subint64(carry9_.shiftleft(21))
        carry10_ = s10_.shiftright(21)
        s11_ = s11_.addint64(carry10_)
        s10_ = s10_.subint64(carry10_.shiftleft(21))
        S0_ = s0_.toint32().toint()
        S1_ = s1_.toint32().toint()
        S2_ = s2_.toint32().toint()
        S3_ = s3_.toint32().toint()
        S4_ = s4_.toint32().toint()
        S5_ = s5_.toint32().toint()
        S6_ = s6_.toint32().toint()
        S7_ = s7_.toint32().toint()
        S8_ = s8_.toint32().toint()
        S9_ = s9_.toint32().toint()
        S10_ = s10_.toint32().toint()
        S11_ = s11_.toint32().toint()
        #// 
        #// @var array<int, int>
        #//
        arr_ = Array(php_int(S0_ >> 0), php_int(S0_ >> 8), php_int(S0_ >> 16 | S1_ << 5), php_int(S1_ >> 3), php_int(S1_ >> 11), php_int(S1_ >> 19 | S2_ << 2), php_int(S2_ >> 6), php_int(S2_ >> 14 | S3_ << 7), php_int(S3_ >> 1), php_int(S3_ >> 9), php_int(S3_ >> 17 | S4_ << 4), php_int(S4_ >> 4), php_int(S4_ >> 12), php_int(S4_ >> 20 | S5_ << 1), php_int(S5_ >> 7), php_int(S5_ >> 15 | S6_ << 6), php_int(S6_ >> 2), php_int(S6_ >> 10), php_int(S6_ >> 18 | S7_ << 3), php_int(S7_ >> 5), php_int(S7_ >> 13), php_int(S8_ >> 0), php_int(S8_ >> 8), php_int(S8_ >> 16 | S9_ << 5), php_int(S9_ >> 3), php_int(S9_ >> 11), php_int(S9_ >> 19 | S10_ << 2), php_int(S10_ >> 6), php_int(S10_ >> 14 | S11_ << 7), php_int(S11_ >> 1), php_int(S11_ >> 9), php_int(S11_) >> 17)
        return self.intarraytostring(arr_)
    # end def sc_reduce
    #// 
    #// multiply by the order of the main subgroup l = 2^252+27742317777372353535851937790883648493
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_mul_l(self, A_=None):
        
        
        #// @var array<int, int> $aslide
        aslide_ = Array(13, 0, 0, 0, 0, -1, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 3, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai size 8
        Ai_ = Array()
        #// # ge_p3_to_cached(&Ai[0], A);
        Ai_[0] = self.ge_p3_to_cached(A_)
        #// # ge_p3_dbl(&t, A);
        t_ = self.ge_p3_dbl(A_)
        #// # ge_p1p1_to_p3(&A2, &t);
        A2_ = self.ge_p1p1_to_p3(t_)
        i_ = 1
        while i_ < 8:
            
            #// # ge_add(&t, &A2, &Ai[0]);
            t_ = self.ge_add(A2_, Ai_[i_ - 1])
            #// # ge_p1p1_to_p3(&u, &t);
            u_ = self.ge_p1p1_to_p3(t_)
            #// # ge_p3_to_cached(&Ai[i], &u);
            Ai_[i_] = self.ge_p3_to_cached(u_)
            i_ += 1
        # end while
        r_ = self.ge_p3_0()
        i_ = 252
        while i_ >= 0:
            
            t_ = self.ge_p3_dbl(r_)
            if aslide_[i_] > 0:
                #// # ge_p1p1_to_p3(&u, &t);
                u_ = self.ge_p1p1_to_p3(t_)
                #// # ge_add(&t, &u, &Ai[aslide[i] / 2]);
                t_ = self.ge_add(u_, Ai_[php_int(aslide_[i_] / 2)])
            elif aslide_[i_] < 0:
                #// # ge_p1p1_to_p3(&u, &t);
                u_ = self.ge_p1p1_to_p3(t_)
                #// # ge_sub(&t, &u, &Ai[(-aslide[i]) / 2]);
                t_ = self.ge_sub(u_, Ai_[php_int(-aslide_[i_] / 2)])
            # end if
            i_ -= 1
        # end while
        #// # ge_p1p1_to_p3(r, &t);
        return self.ge_p1p1_to_p3(t_)
    # end def ge_mul_l
# end class ParagonIE_Sodium_Core32_Curve25519
