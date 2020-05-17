#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_Curve25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Curve25519
#// 
#// Implements Curve25519 core functions
#// 
#// Based on the ref10 curve25519 code provided by libsodium
#// 
#// @ref https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c
#//
class ParagonIE_Sodium_Core_Curve25519(ParagonIE_Sodium_Core_Curve25519_H):
    #// 
    #// Get a field element of size 10 with a value of 0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_0(self):
        
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    # end def fe_0
    #// 
    #// Get a field element of size 10 with a value of 1
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_1(self):
        
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    # end def fe_1
    #// 
    #// Add two field elements.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def fe_add(self, f_=None, g_=None):
        
        
        #// @var array<int, int> $arr
        arr_ = Array()
        i_ = 0
        while i_ < 10:
            
            arr_[i_] = php_int(f_[i_] + g_[i_])
            i_ += 1
        # end while
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(arr_)
    # end def fe_add
    #// 
    #// Constant-time conditional move.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fe_cmov(self, f_=None, g_=None, b_=0):
        
        
        #// @var array<int, int> $h
        h_ = Array()
        b_ *= -1
        i_ = 0
        while i_ < 10:
            
            #// @var int $x
            x_ = f_[i_] ^ g_[i_] & b_
            h_[i_] = php_int(php_int(f_[i_]) ^ x_)
            i_ += 1
        # end while
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(h_)
    # end def fe_cmov
    #// 
    #// Create a copy of a field element.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def fe_frombytes(self, s_=None):
        
        
        if self.strlen(s_) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Expected a 32-byte string."))
        # end if
        #// @var int $h0
        h0_ = self.load_4(s_)
        #// @var int $h1
        h1_ = self.load_3(self.substr(s_, 4, 3)) << 6
        #// @var int $h2
        h2_ = self.load_3(self.substr(s_, 7, 3)) << 5
        #// @var int $h3
        h3_ = self.load_3(self.substr(s_, 10, 3)) << 3
        #// @var int $h4
        h4_ = self.load_3(self.substr(s_, 13, 3)) << 2
        #// @var int $h5
        h5_ = self.load_4(self.substr(s_, 16, 4))
        #// @var int $h6
        h6_ = self.load_3(self.substr(s_, 20, 3)) << 7
        #// @var int $h7
        h7_ = self.load_3(self.substr(s_, 23, 3)) << 5
        #// @var int $h8
        h8_ = self.load_3(self.substr(s_, 26, 3)) << 4
        #// @var int $h9
        h9_ = self.load_3(self.substr(s_, 29, 3)) & 8388607 << 2
        #// @var int $carry9
        carry9_ = h9_ + 1 << 24 >> 25
        h0_ += self.mul(carry9_, 19, 5)
        h9_ -= carry9_ << 25
        #// @var int $carry1
        carry1_ = h1_ + 1 << 24 >> 25
        h2_ += carry1_
        h1_ -= carry1_ << 25
        #// @var int $carry3
        carry3_ = h3_ + 1 << 24 >> 25
        h4_ += carry3_
        h3_ -= carry3_ << 25
        #// @var int $carry5
        carry5_ = h5_ + 1 << 24 >> 25
        h6_ += carry5_
        h5_ -= carry5_ << 25
        #// @var int $carry7
        carry7_ = h7_ + 1 << 24 >> 25
        h8_ += carry7_
        h7_ -= carry7_ << 25
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        #// @var int $carry2
        carry2_ = h2_ + 1 << 25 >> 26
        h3_ += carry2_
        h2_ -= carry2_ << 26
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry6
        carry6_ = h6_ + 1 << 25 >> 26
        h7_ += carry6_
        h6_ -= carry6_ << 26
        #// @var int $carry8
        carry8_ = h8_ + 1 << 25 >> 26
        h9_ += carry8_
        h8_ -= carry8_ << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0_), php_int(h1_), php_int(h2_), php_int(h3_), php_int(h4_), php_int(h5_), php_int(h6_), php_int(h7_), php_int(h8_), php_int(h9_)))
    # end def fe_frombytes
    #// 
    #// Convert a field element to a byte string.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $h
    #// @return string
    #//
    @classmethod
    def fe_tobytes(self, h_=None):
        
        
        #// @var int $h0
        h0_ = php_int(h_[0])
        #// @var int $h1
        h1_ = php_int(h_[1])
        #// @var int $h2
        h2_ = php_int(h_[2])
        #// @var int $h3
        h3_ = php_int(h_[3])
        #// @var int $h4
        h4_ = php_int(h_[4])
        #// @var int $h5
        h5_ = php_int(h_[5])
        #// @var int $h6
        h6_ = php_int(h_[6])
        #// @var int $h7
        h7_ = php_int(h_[7])
        #// @var int $h8
        h8_ = php_int(h_[8])
        #// @var int $h9
        h9_ = php_int(h_[9])
        #// @var int $q
        q_ = self.mul(h9_, 19, 5) + 1 << 24 >> 25
        #// @var int $q
        q_ = h0_ + q_ >> 26
        #// @var int $q
        q_ = h1_ + q_ >> 25
        #// @var int $q
        q_ = h2_ + q_ >> 26
        #// @var int $q
        q_ = h3_ + q_ >> 25
        #// @var int $q
        q_ = h4_ + q_ >> 26
        #// @var int $q
        q_ = h5_ + q_ >> 25
        #// @var int $q
        q_ = h6_ + q_ >> 26
        #// @var int $q
        q_ = h7_ + q_ >> 25
        #// @var int $q
        q_ = h8_ + q_ >> 26
        #// @var int $q
        q_ = h9_ + q_ >> 25
        h0_ += self.mul(q_, 19, 5)
        #// @var int $carry0
        carry0_ = h0_ >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        #// @var int $carry1
        carry1_ = h1_ >> 25
        h2_ += carry1_
        h1_ -= carry1_ << 25
        #// @var int $carry2
        carry2_ = h2_ >> 26
        h3_ += carry2_
        h2_ -= carry2_ << 26
        #// @var int $carry3
        carry3_ = h3_ >> 25
        h4_ += carry3_
        h3_ -= carry3_ << 25
        #// @var int $carry4
        carry4_ = h4_ >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry5
        carry5_ = h5_ >> 25
        h6_ += carry5_
        h5_ -= carry5_ << 25
        #// @var int $carry6
        carry6_ = h6_ >> 26
        h7_ += carry6_
        h6_ -= carry6_ << 26
        #// @var int $carry7
        carry7_ = h7_ >> 25
        h8_ += carry7_
        h7_ -= carry7_ << 25
        #// @var int $carry8
        carry8_ = h8_ >> 26
        h9_ += carry8_
        h8_ -= carry8_ << 26
        #// @var int $carry9
        carry9_ = h9_ >> 25
        h9_ -= carry9_ << 25
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
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
        #// @var string $zero
        #// @var string $str
        str_ = self.fe_tobytes(f_)
        return (not self.verify_32(str_, php_str(zero_)))
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_mul(self, f_=None, g_=None):
        
        
        #// @var int $f0
        f0_ = f_[0]
        #// @var int $f1
        f1_ = f_[1]
        #// @var int $f2
        f2_ = f_[2]
        #// @var int $f3
        f3_ = f_[3]
        #// @var int $f4
        f4_ = f_[4]
        #// @var int $f5
        f5_ = f_[5]
        #// @var int $f6
        f6_ = f_[6]
        #// @var int $f7
        f7_ = f_[7]
        #// @var int $f8
        f8_ = f_[8]
        #// @var int $f9
        f9_ = f_[9]
        #// @var int $g0
        g0_ = g_[0]
        #// @var int $g1
        g1_ = g_[1]
        #// @var int $g2
        g2_ = g_[2]
        #// @var int $g3
        g3_ = g_[3]
        #// @var int $g4
        g4_ = g_[4]
        #// @var int $g5
        g5_ = g_[5]
        #// @var int $g6
        g6_ = g_[6]
        #// @var int $g7
        g7_ = g_[7]
        #// @var int $g8
        g8_ = g_[8]
        #// @var int $g9
        g9_ = g_[9]
        g1_19_ = self.mul(g1_, 19, 5)
        g2_19_ = self.mul(g2_, 19, 5)
        g3_19_ = self.mul(g3_, 19, 5)
        g4_19_ = self.mul(g4_, 19, 5)
        g5_19_ = self.mul(g5_, 19, 5)
        g6_19_ = self.mul(g6_, 19, 5)
        g7_19_ = self.mul(g7_, 19, 5)
        g8_19_ = self.mul(g8_, 19, 5)
        g9_19_ = self.mul(g9_, 19, 5)
        #// @var int $f1_2
        f1_2_ = f1_ << 1
        #// @var int $f3_2
        f3_2_ = f3_ << 1
        #// @var int $f5_2
        f5_2_ = f5_ << 1
        #// @var int $f7_2
        f7_2_ = f7_ << 1
        #// @var int $f9_2
        f9_2_ = f9_ << 1
        f0g0_ = self.mul(f0_, g0_, 26)
        f0g1_ = self.mul(f0_, g1_, 25)
        f0g2_ = self.mul(f0_, g2_, 26)
        f0g3_ = self.mul(f0_, g3_, 25)
        f0g4_ = self.mul(f0_, g4_, 26)
        f0g5_ = self.mul(f0_, g5_, 25)
        f0g6_ = self.mul(f0_, g6_, 26)
        f0g7_ = self.mul(f0_, g7_, 25)
        f0g8_ = self.mul(f0_, g8_, 26)
        f0g9_ = self.mul(f0_, g9_, 26)
        f1g0_ = self.mul(f1_, g0_, 26)
        f1g1_2_ = self.mul(f1_2_, g1_, 25)
        f1g2_ = self.mul(f1_, g2_, 26)
        f1g3_2_ = self.mul(f1_2_, g3_, 25)
        f1g4_ = self.mul(f1_, g4_, 26)
        f1g5_2_ = self.mul(f1_2_, g5_, 25)
        f1g6_ = self.mul(f1_, g6_, 26)
        f1g7_2_ = self.mul(f1_2_, g7_, 25)
        f1g8_ = self.mul(f1_, g8_, 26)
        f1g9_38_ = self.mul(g9_19_, f1_2_, 26)
        f2g0_ = self.mul(f2_, g0_, 26)
        f2g1_ = self.mul(f2_, g1_, 25)
        f2g2_ = self.mul(f2_, g2_, 26)
        f2g3_ = self.mul(f2_, g3_, 25)
        f2g4_ = self.mul(f2_, g4_, 26)
        f2g5_ = self.mul(f2_, g5_, 25)
        f2g6_ = self.mul(f2_, g6_, 26)
        f2g7_ = self.mul(f2_, g7_, 25)
        f2g8_19_ = self.mul(g8_19_, f2_, 26)
        f2g9_19_ = self.mul(g9_19_, f2_, 26)
        f3g0_ = self.mul(f3_, g0_, 26)
        f3g1_2_ = self.mul(f3_2_, g1_, 25)
        f3g2_ = self.mul(f3_, g2_, 26)
        f3g3_2_ = self.mul(f3_2_, g3_, 25)
        f3g4_ = self.mul(f3_, g4_, 26)
        f3g5_2_ = self.mul(f3_2_, g5_, 25)
        f3g6_ = self.mul(f3_, g6_, 26)
        f3g7_38_ = self.mul(g7_19_, f3_2_, 26)
        f3g8_19_ = self.mul(g8_19_, f3_, 25)
        f3g9_38_ = self.mul(g9_19_, f3_2_, 26)
        f4g0_ = self.mul(f4_, g0_, 26)
        f4g1_ = self.mul(f4_, g1_, 25)
        f4g2_ = self.mul(f4_, g2_, 26)
        f4g3_ = self.mul(f4_, g3_, 25)
        f4g4_ = self.mul(f4_, g4_, 26)
        f4g5_ = self.mul(f4_, g5_, 25)
        f4g6_19_ = self.mul(g6_19_, f4_, 26)
        f4g7_19_ = self.mul(g7_19_, f4_, 26)
        f4g8_19_ = self.mul(g8_19_, f4_, 26)
        f4g9_19_ = self.mul(g9_19_, f4_, 26)
        f5g0_ = self.mul(f5_, g0_, 26)
        f5g1_2_ = self.mul(f5_2_, g1_, 25)
        f5g2_ = self.mul(f5_, g2_, 26)
        f5g3_2_ = self.mul(f5_2_, g3_, 25)
        f5g4_ = self.mul(f5_, g4_, 26)
        f5g5_38_ = self.mul(g5_19_, f5_2_, 26)
        f5g6_19_ = self.mul(g6_19_, f5_, 25)
        f5g7_38_ = self.mul(g7_19_, f5_2_, 26)
        f5g8_19_ = self.mul(g8_19_, f5_, 25)
        f5g9_38_ = self.mul(g9_19_, f5_2_, 26)
        f6g0_ = self.mul(f6_, g0_, 26)
        f6g1_ = self.mul(f6_, g1_, 25)
        f6g2_ = self.mul(f6_, g2_, 26)
        f6g3_ = self.mul(f6_, g3_, 25)
        f6g4_19_ = self.mul(g4_19_, f6_, 26)
        f6g5_19_ = self.mul(g5_19_, f6_, 26)
        f6g6_19_ = self.mul(g6_19_, f6_, 26)
        f6g7_19_ = self.mul(g7_19_, f6_, 26)
        f6g8_19_ = self.mul(g8_19_, f6_, 26)
        f6g9_19_ = self.mul(g9_19_, f6_, 26)
        f7g0_ = self.mul(f7_, g0_, 26)
        f7g1_2_ = self.mul(f7_2_, g1_, 25)
        f7g2_ = self.mul(f7_, g2_, 26)
        f7g3_38_ = self.mul(g3_19_, f7_2_, 26)
        f7g4_19_ = self.mul(g4_19_, f7_, 26)
        f7g5_38_ = self.mul(g5_19_, f7_2_, 26)
        f7g6_19_ = self.mul(g6_19_, f7_, 25)
        f7g7_38_ = self.mul(g7_19_, f7_2_, 26)
        f7g8_19_ = self.mul(g8_19_, f7_, 25)
        f7g9_38_ = self.mul(g9_19_, f7_2_, 26)
        f8g0_ = self.mul(f8_, g0_, 26)
        f8g1_ = self.mul(f8_, g1_, 25)
        f8g2_19_ = self.mul(g2_19_, f8_, 26)
        f8g3_19_ = self.mul(g3_19_, f8_, 26)
        f8g4_19_ = self.mul(g4_19_, f8_, 26)
        f8g5_19_ = self.mul(g5_19_, f8_, 26)
        f8g6_19_ = self.mul(g6_19_, f8_, 26)
        f8g7_19_ = self.mul(g7_19_, f8_, 26)
        f8g8_19_ = self.mul(g8_19_, f8_, 26)
        f8g9_19_ = self.mul(g9_19_, f8_, 26)
        f9g0_ = self.mul(f9_, g0_, 26)
        f9g1_38_ = self.mul(g1_19_, f9_2_, 26)
        f9g2_19_ = self.mul(g2_19_, f9_, 25)
        f9g3_38_ = self.mul(g3_19_, f9_2_, 26)
        f9g4_19_ = self.mul(g4_19_, f9_, 25)
        f9g5_38_ = self.mul(g5_19_, f9_2_, 26)
        f9g6_19_ = self.mul(g6_19_, f9_, 25)
        f9g7_38_ = self.mul(g7_19_, f9_2_, 26)
        f9g8_19_ = self.mul(g8_19_, f9_, 25)
        f9g9_38_ = self.mul(g9_19_, f9_2_, 26)
        h0_ = f0g0_ + f1g9_38_ + f2g8_19_ + f3g7_38_ + f4g6_19_ + f5g5_38_ + f6g4_19_ + f7g3_38_ + f8g2_19_ + f9g1_38_
        h1_ = f0g1_ + f1g0_ + f2g9_19_ + f3g8_19_ + f4g7_19_ + f5g6_19_ + f6g5_19_ + f7g4_19_ + f8g3_19_ + f9g2_19_
        h2_ = f0g2_ + f1g1_2_ + f2g0_ + f3g9_38_ + f4g8_19_ + f5g7_38_ + f6g6_19_ + f7g5_38_ + f8g4_19_ + f9g3_38_
        h3_ = f0g3_ + f1g2_ + f2g1_ + f3g0_ + f4g9_19_ + f5g8_19_ + f6g7_19_ + f7g6_19_ + f8g5_19_ + f9g4_19_
        h4_ = f0g4_ + f1g3_2_ + f2g2_ + f3g1_2_ + f4g0_ + f5g9_38_ + f6g8_19_ + f7g7_38_ + f8g6_19_ + f9g5_38_
        h5_ = f0g5_ + f1g4_ + f2g3_ + f3g2_ + f4g1_ + f5g0_ + f6g9_19_ + f7g8_19_ + f8g7_19_ + f9g6_19_
        h6_ = f0g6_ + f1g5_2_ + f2g4_ + f3g3_2_ + f4g2_ + f5g1_2_ + f6g0_ + f7g9_38_ + f8g8_19_ + f9g7_38_
        h7_ = f0g7_ + f1g6_ + f2g5_ + f3g4_ + f4g3_ + f5g2_ + f6g1_ + f7g0_ + f8g9_19_ + f9g8_19_
        h8_ = f0g8_ + f1g7_2_ + f2g6_ + f3g5_2_ + f4g4_ + f5g3_2_ + f6g2_ + f7g1_2_ + f8g0_ + f9g9_38_
        h9_ = f0g9_ + f1g8_ + f2g7_ + f3g6_ + f4g5_ + f5g4_ + f6g3_ + f7g2_ + f8g1_ + f9g0_
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry1
        carry1_ = h1_ + 1 << 24 >> 25
        h2_ += carry1_
        h1_ -= carry1_ << 25
        #// @var int $carry5
        carry5_ = h5_ + 1 << 24 >> 25
        h6_ += carry5_
        h5_ -= carry5_ << 25
        #// @var int $carry2
        carry2_ = h2_ + 1 << 25 >> 26
        h3_ += carry2_
        h2_ -= carry2_ << 26
        #// @var int $carry6
        carry6_ = h6_ + 1 << 25 >> 26
        h7_ += carry6_
        h6_ -= carry6_ << 26
        #// @var int $carry3
        carry3_ = h3_ + 1 << 24 >> 25
        h4_ += carry3_
        h3_ -= carry3_ << 25
        #// @var int $carry7
        carry7_ = h7_ + 1 << 24 >> 25
        h8_ += carry7_
        h7_ -= carry7_ << 25
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry8
        carry8_ = h8_ + 1 << 25 >> 26
        h9_ += carry8_
        h8_ -= carry8_ << 26
        #// @var int $carry9
        carry9_ = h9_ + 1 << 24 >> 25
        h0_ += self.mul(carry9_, 19, 5)
        h9_ -= carry9_ << 25
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0_), php_int(h1_), php_int(h2_), php_int(h3_), php_int(h4_), php_int(h5_), php_int(h6_), php_int(h7_), php_int(h8_), php_int(h9_)))
    # end def fe_mul
    #// 
    #// Get the negative values for each piece of the field element.
    #// 
    #// h = -f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fe_neg(self, f_=None):
        
        
        h_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        i_ = 0
        while i_ < 10:
            
            h_[i_] = -f_[i_]
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_sq(self, f_=None):
        
        
        f0_ = php_int(f_[0])
        f1_ = php_int(f_[1])
        f2_ = php_int(f_[2])
        f3_ = php_int(f_[3])
        f4_ = php_int(f_[4])
        f5_ = php_int(f_[5])
        f6_ = php_int(f_[6])
        f7_ = php_int(f_[7])
        f8_ = php_int(f_[8])
        f9_ = php_int(f_[9])
        #// @var int $f0_2
        f0_2_ = f0_ << 1
        #// @var int $f1_2
        f1_2_ = f1_ << 1
        #// @var int $f2_2
        f2_2_ = f2_ << 1
        #// @var int $f3_2
        f3_2_ = f3_ << 1
        #// @var int $f4_2
        f4_2_ = f4_ << 1
        #// @var int $f5_2
        f5_2_ = f5_ << 1
        #// @var int $f6_2
        f6_2_ = f6_ << 1
        #// @var int $f7_2
        f7_2_ = f7_ << 1
        f5_38_ = self.mul(f5_, 38, 6)
        f6_19_ = self.mul(f6_, 19, 5)
        f7_38_ = self.mul(f7_, 38, 6)
        f8_19_ = self.mul(f8_, 19, 5)
        f9_38_ = self.mul(f9_, 38, 6)
        f0f0_ = self.mul(f0_, f0_, 25)
        f0f1_2_ = self.mul(f0_2_, f1_, 24)
        f0f2_2_ = self.mul(f0_2_, f2_, 25)
        f0f3_2_ = self.mul(f0_2_, f3_, 24)
        f0f4_2_ = self.mul(f0_2_, f4_, 25)
        f0f5_2_ = self.mul(f0_2_, f5_, 25)
        f0f6_2_ = self.mul(f0_2_, f6_, 25)
        f0f7_2_ = self.mul(f0_2_, f7_, 24)
        f0f8_2_ = self.mul(f0_2_, f8_, 25)
        f0f9_2_ = self.mul(f0_2_, f9_, 25)
        f1f1_2_ = self.mul(f1_2_, f1_, 24)
        f1f2_2_ = self.mul(f1_2_, f2_, 25)
        f1f3_4_ = self.mul(f1_2_, f3_2_, 25)
        f1f4_2_ = self.mul(f1_2_, f4_, 25)
        f1f5_4_ = self.mul(f1_2_, f5_2_, 26)
        f1f6_2_ = self.mul(f1_2_, f6_, 25)
        f1f7_4_ = self.mul(f1_2_, f7_2_, 25)
        f1f8_2_ = self.mul(f1_2_, f8_, 25)
        f1f9_76_ = self.mul(f9_38_, f1_2_, 25)
        f2f2_ = self.mul(f2_, f2_, 25)
        f2f3_2_ = self.mul(f2_2_, f3_, 24)
        f2f4_2_ = self.mul(f2_2_, f4_, 25)
        f2f5_2_ = self.mul(f2_2_, f5_, 25)
        f2f6_2_ = self.mul(f2_2_, f6_, 25)
        f2f7_2_ = self.mul(f2_2_, f7_, 24)
        f2f8_38_ = self.mul(f8_19_, f2_2_, 26)
        f2f9_38_ = self.mul(f9_38_, f2_, 25)
        f3f3_2_ = self.mul(f3_2_, f3_, 24)
        f3f4_2_ = self.mul(f3_2_, f4_, 25)
        f3f5_4_ = self.mul(f3_2_, f5_2_, 26)
        f3f6_2_ = self.mul(f3_2_, f6_, 25)
        f3f7_76_ = self.mul(f7_38_, f3_2_, 25)
        f3f8_38_ = self.mul(f8_19_, f3_2_, 25)
        f3f9_76_ = self.mul(f9_38_, f3_2_, 25)
        f4f4_ = self.mul(f4_, f4_, 25)
        f4f5_2_ = self.mul(f4_2_, f5_, 25)
        f4f6_38_ = self.mul(f6_19_, f4_2_, 26)
        f4f7_38_ = self.mul(f7_38_, f4_, 25)
        f4f8_38_ = self.mul(f8_19_, f4_2_, 26)
        f4f9_38_ = self.mul(f9_38_, f4_, 25)
        f5f5_38_ = self.mul(f5_38_, f5_, 25)
        f5f6_38_ = self.mul(f6_19_, f5_2_, 26)
        f5f7_76_ = self.mul(f7_38_, f5_2_, 26)
        f5f8_38_ = self.mul(f8_19_, f5_2_, 26)
        f5f9_76_ = self.mul(f9_38_, f5_2_, 26)
        f6f6_19_ = self.mul(f6_19_, f6_, 25)
        f6f7_38_ = self.mul(f7_38_, f6_, 25)
        f6f8_38_ = self.mul(f8_19_, f6_2_, 26)
        f6f9_38_ = self.mul(f9_38_, f6_, 25)
        f7f7_38_ = self.mul(f7_38_, f7_, 24)
        f7f8_38_ = self.mul(f8_19_, f7_2_, 25)
        f7f9_76_ = self.mul(f9_38_, f7_2_, 25)
        f8f8_19_ = self.mul(f8_19_, f8_, 25)
        f8f9_38_ = self.mul(f9_38_, f8_, 25)
        f9f9_38_ = self.mul(f9_38_, f9_, 25)
        h0_ = f0f0_ + f1f9_76_ + f2f8_38_ + f3f7_76_ + f4f6_38_ + f5f5_38_
        h1_ = f0f1_2_ + f2f9_38_ + f3f8_38_ + f4f7_38_ + f5f6_38_
        h2_ = f0f2_2_ + f1f1_2_ + f3f9_76_ + f4f8_38_ + f5f7_76_ + f6f6_19_
        h3_ = f0f3_2_ + f1f2_2_ + f4f9_38_ + f5f8_38_ + f6f7_38_
        h4_ = f0f4_2_ + f1f3_4_ + f2f2_ + f5f9_76_ + f6f8_38_ + f7f7_38_
        h5_ = f0f5_2_ + f1f4_2_ + f2f3_2_ + f6f9_38_ + f7f8_38_
        h6_ = f0f6_2_ + f1f5_4_ + f2f4_2_ + f3f3_2_ + f7f9_76_ + f8f8_19_
        h7_ = f0f7_2_ + f1f6_2_ + f2f5_2_ + f3f4_2_ + f8f9_38_
        h8_ = f0f8_2_ + f1f7_4_ + f2f6_2_ + f3f5_4_ + f4f4_ + f9f9_38_
        h9_ = f0f9_2_ + f1f8_2_ + f2f7_2_ + f3f6_2_ + f4f5_2_
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry1
        carry1_ = h1_ + 1 << 24 >> 25
        h2_ += carry1_
        h1_ -= carry1_ << 25
        #// @var int $carry5
        carry5_ = h5_ + 1 << 24 >> 25
        h6_ += carry5_
        h5_ -= carry5_ << 25
        #// @var int $carry2
        carry2_ = h2_ + 1 << 25 >> 26
        h3_ += carry2_
        h2_ -= carry2_ << 26
        #// @var int $carry6
        carry6_ = h6_ + 1 << 25 >> 26
        h7_ += carry6_
        h6_ -= carry6_ << 26
        #// @var int $carry3
        carry3_ = h3_ + 1 << 24 >> 25
        h4_ += carry3_
        h3_ -= carry3_ << 25
        #// @var int $carry7
        carry7_ = h7_ + 1 << 24 >> 25
        h8_ += carry7_
        h7_ -= carry7_ << 25
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry8
        carry8_ = h8_ + 1 << 25 >> 26
        h9_ += carry8_
        h8_ -= carry8_ << 26
        #// @var int $carry9
        carry9_ = h9_ + 1 << 24 >> 25
        h0_ += self.mul(carry9_, 19, 5)
        h9_ -= carry9_ << 25
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0_), php_int(h1_), php_int(h2_), php_int(h3_), php_int(h4_), php_int(h5_), php_int(h6_), php_int(h7_), php_int(h8_), php_int(h9_)))
    # end def fe_sq
    #// 
    #// Square and double a field element
    #// 
    #// h = 2 * f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_sq2(self, f_=None):
        
        
        f0_ = php_int(f_[0])
        f1_ = php_int(f_[1])
        f2_ = php_int(f_[2])
        f3_ = php_int(f_[3])
        f4_ = php_int(f_[4])
        f5_ = php_int(f_[5])
        f6_ = php_int(f_[6])
        f7_ = php_int(f_[7])
        f8_ = php_int(f_[8])
        f9_ = php_int(f_[9])
        #// @var int $f0_2
        f0_2_ = f0_ << 1
        #// @var int $f1_2
        f1_2_ = f1_ << 1
        #// @var int $f2_2
        f2_2_ = f2_ << 1
        #// @var int $f3_2
        f3_2_ = f3_ << 1
        #// @var int $f4_2
        f4_2_ = f4_ << 1
        #// @var int $f5_2
        f5_2_ = f5_ << 1
        #// @var int $f6_2
        f6_2_ = f6_ << 1
        #// @var int $f7_2
        f7_2_ = f7_ << 1
        f5_38_ = self.mul(f5_, 38, 6)
        #// 1.959375*2^30
        f6_19_ = self.mul(f6_, 19, 5)
        #// 1.959375*2^30
        f7_38_ = self.mul(f7_, 38, 6)
        #// 1.959375*2^30
        f8_19_ = self.mul(f8_, 19, 5)
        #// 1.959375*2^30
        f9_38_ = self.mul(f9_, 38, 6)
        #// 1.959375*2^30
        f0f0_ = self.mul(f0_, f0_, 24)
        f0f1_2_ = self.mul(f0_2_, f1_, 24)
        f0f2_2_ = self.mul(f0_2_, f2_, 24)
        f0f3_2_ = self.mul(f0_2_, f3_, 24)
        f0f4_2_ = self.mul(f0_2_, f4_, 24)
        f0f5_2_ = self.mul(f0_2_, f5_, 24)
        f0f6_2_ = self.mul(f0_2_, f6_, 24)
        f0f7_2_ = self.mul(f0_2_, f7_, 24)
        f0f8_2_ = self.mul(f0_2_, f8_, 24)
        f0f9_2_ = self.mul(f0_2_, f9_, 24)
        f1f1_2_ = self.mul(f1_2_, f1_, 24)
        f1f2_2_ = self.mul(f1_2_, f2_, 24)
        f1f3_4_ = self.mul(f1_2_, f3_2_, 24)
        f1f4_2_ = self.mul(f1_2_, f4_, 24)
        f1f5_4_ = self.mul(f1_2_, f5_2_, 24)
        f1f6_2_ = self.mul(f1_2_, f6_, 24)
        f1f7_4_ = self.mul(f1_2_, f7_2_, 24)
        f1f8_2_ = self.mul(f1_2_, f8_, 24)
        f1f9_76_ = self.mul(f9_38_, f1_2_, 24)
        f2f2_ = self.mul(f2_, f2_, 24)
        f2f3_2_ = self.mul(f2_2_, f3_, 24)
        f2f4_2_ = self.mul(f2_2_, f4_, 24)
        f2f5_2_ = self.mul(f2_2_, f5_, 24)
        f2f6_2_ = self.mul(f2_2_, f6_, 24)
        f2f7_2_ = self.mul(f2_2_, f7_, 24)
        f2f8_38_ = self.mul(f8_19_, f2_2_, 25)
        f2f9_38_ = self.mul(f9_38_, f2_, 24)
        f3f3_2_ = self.mul(f3_2_, f3_, 24)
        f3f4_2_ = self.mul(f3_2_, f4_, 24)
        f3f5_4_ = self.mul(f3_2_, f5_2_, 24)
        f3f6_2_ = self.mul(f3_2_, f6_, 24)
        f3f7_76_ = self.mul(f7_38_, f3_2_, 24)
        f3f8_38_ = self.mul(f8_19_, f3_2_, 24)
        f3f9_76_ = self.mul(f9_38_, f3_2_, 24)
        f4f4_ = self.mul(f4_, f4_, 24)
        f4f5_2_ = self.mul(f4_2_, f5_, 24)
        f4f6_38_ = self.mul(f6_19_, f4_2_, 25)
        f4f7_38_ = self.mul(f7_38_, f4_, 24)
        f4f8_38_ = self.mul(f8_19_, f4_2_, 25)
        f4f9_38_ = self.mul(f9_38_, f4_, 24)
        f5f5_38_ = self.mul(f5_38_, f5_, 24)
        f5f6_38_ = self.mul(f6_19_, f5_2_, 24)
        f5f7_76_ = self.mul(f7_38_, f5_2_, 24)
        f5f8_38_ = self.mul(f8_19_, f5_2_, 24)
        f5f9_76_ = self.mul(f9_38_, f5_2_, 24)
        f6f6_19_ = self.mul(f6_19_, f6_, 24)
        f6f7_38_ = self.mul(f7_38_, f6_, 24)
        f6f8_38_ = self.mul(f8_19_, f6_2_, 25)
        f6f9_38_ = self.mul(f9_38_, f6_, 24)
        f7f7_38_ = self.mul(f7_38_, f7_, 24)
        f7f8_38_ = self.mul(f8_19_, f7_2_, 24)
        f7f9_76_ = self.mul(f9_38_, f7_2_, 24)
        f8f8_19_ = self.mul(f8_19_, f8_, 24)
        f8f9_38_ = self.mul(f9_38_, f8_, 24)
        f9f9_38_ = self.mul(f9_38_, f9_, 24)
        #// @var int $h0
        h0_ = php_int(f0f0_ + f1f9_76_ + f2f8_38_ + f3f7_76_ + f4f6_38_ + f5f5_38_) << 1
        #// @var int $h1
        h1_ = php_int(f0f1_2_ + f2f9_38_ + f3f8_38_ + f4f7_38_ + f5f6_38_) << 1
        #// @var int $h2
        h2_ = php_int(f0f2_2_ + f1f1_2_ + f3f9_76_ + f4f8_38_ + f5f7_76_ + f6f6_19_) << 1
        #// @var int $h3
        h3_ = php_int(f0f3_2_ + f1f2_2_ + f4f9_38_ + f5f8_38_ + f6f7_38_) << 1
        #// @var int $h4
        h4_ = php_int(f0f4_2_ + f1f3_4_ + f2f2_ + f5f9_76_ + f6f8_38_ + f7f7_38_) << 1
        #// @var int $h5
        h5_ = php_int(f0f5_2_ + f1f4_2_ + f2f3_2_ + f6f9_38_ + f7f8_38_) << 1
        #// @var int $h6
        h6_ = php_int(f0f6_2_ + f1f5_4_ + f2f4_2_ + f3f3_2_ + f7f9_76_ + f8f8_19_) << 1
        #// @var int $h7
        h7_ = php_int(f0f7_2_ + f1f6_2_ + f2f5_2_ + f3f4_2_ + f8f9_38_) << 1
        #// @var int $h8
        h8_ = php_int(f0f8_2_ + f1f7_4_ + f2f6_2_ + f3f5_4_ + f4f4_ + f9f9_38_) << 1
        #// @var int $h9
        h9_ = php_int(f0f9_2_ + f1f8_2_ + f2f7_2_ + f3f6_2_ + f4f5_2_) << 1
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry1
        carry1_ = h1_ + 1 << 24 >> 25
        h2_ += carry1_
        h1_ -= carry1_ << 25
        #// @var int $carry5
        carry5_ = h5_ + 1 << 24 >> 25
        h6_ += carry5_
        h5_ -= carry5_ << 25
        #// @var int $carry2
        carry2_ = h2_ + 1 << 25 >> 26
        h3_ += carry2_
        h2_ -= carry2_ << 26
        #// @var int $carry6
        carry6_ = h6_ + 1 << 25 >> 26
        h7_ += carry6_
        h6_ -= carry6_ << 26
        #// @var int $carry3
        carry3_ = h3_ + 1 << 24 >> 25
        h4_ += carry3_
        h3_ -= carry3_ << 25
        #// @var int $carry7
        carry7_ = h7_ + 1 << 24 >> 25
        h8_ += carry7_
        h7_ -= carry7_ << 25
        #// @var int $carry4
        carry4_ = h4_ + 1 << 25 >> 26
        h5_ += carry4_
        h4_ -= carry4_ << 26
        #// @var int $carry8
        carry8_ = h8_ + 1 << 25 >> 26
        h9_ += carry8_
        h8_ -= carry8_ << 26
        #// @var int $carry9
        carry9_ = h9_ + 1 << 24 >> 25
        h0_ += self.mul(carry9_, 19, 5)
        h9_ -= carry9_ << 25
        #// @var int $carry0
        carry0_ = h0_ + 1 << 25 >> 26
        h1_ += carry0_
        h0_ -= carry0_ << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0_), php_int(h1_), php_int(h2_), php_int(h3_), php_int(h4_), php_int(h5_), php_int(h6_), php_int(h7_), php_int(h8_), php_int(h9_)))
    # end def fe_sq2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $Z
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $z
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def fe_sub(self, f_=None, g_=None):
        
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(f_[0] - g_[0]), php_int(f_[1] - g_[1]), php_int(f_[2] - g_[2]), php_int(f_[3] - g_[3]), php_int(f_[4] - g_[4]), php_int(f_[5] - g_[5]), php_int(f_[6] - g_[6]), php_int(f_[7] - g_[7]), php_int(f_[8] - g_[8]), php_int(f_[9] - g_[9])))
    # end def fe_sub
    #// 
    #// Add two group elements.
    #// 
    #// r = p + q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_add(self, p_=None, q_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
        #// @var int $i
        i_ = 0
        while i_ < 256:
            
            r_[i_] = php_int(1 & self.chrtoint(a_[php_int(i_ >> 3)]) >> i_ & 7)
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_frombytes_negate_vartime(self, s_=None):
        
        
        d_ = None
        if (not d_):
            d_ = ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.d)
        # end if
        #// # fe_frombytes(h->Y,s);
        #// # fe_1(h->Z);
        h_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3(self.fe_0(), self.fe_frombytes(s_), self.fe_1()))
        #// # fe_sq(u,h->Y);
        #// # fe_mul(v,u,d);
        #// # fe_sub(u,u,h->Z);       /* u = y^2-1
        #// # fe_add(v,v,h->Z);       /* v = dy^2+1
        u_ = self.fe_sq(h_.Y)
        #// @var ParagonIE_Sodium_Core_Curve25519_Fe $d
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
            h_.X = self.fe_mul(h_.X, ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.sqrtm1))
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p1p1_to_p2(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2())
        r_.X = self.fe_mul(p_.X, p_.T)
        r_.Y = self.fe_mul(p_.Y, p_.Z)
        r_.Z = self.fe_mul(p_.Z, p_.T)
        return r_
    # end def ge_p1p1_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_p1p1_to_p3(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3())
        r_.X = self.fe_mul(p_.X, p_.T)
        r_.Y = self.fe_mul(p_.Y, p_.Z)
        r_.Z = self.fe_mul(p_.Z, p_.T)
        r_.T = self.fe_mul(p_.X, p_.Y)
        return r_
    # end def ge_p1p1_to_p3
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p2_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2(self.fe_0(), self.fe_1(), self.fe_1()))
    # end def ge_p2_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P2 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_p2_dbl(self, p_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_p3_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3(self.fe_0(), self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_p3_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Cached
    #//
    @classmethod
    def ge_p3_to_cached(self, p_=None):
        
        
        d2_ = None
        if d2_ == None:
            d2_ = ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.d2)
        # end if
        #// @var ParagonIE_Sodium_Core_Curve25519_Fe $d2
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Cached())
        r_.YplusX = self.fe_add(p_.Y, p_.X)
        r_.YminusX = self.fe_sub(p_.Y, p_.X)
        r_.Z = self.fe_copy(p_.Z)
        r_.T2d = self.fe_mul(p_.T, d2_)
        return r_
    # end def ge_p3_to_cached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p3_to_p2(self, p_=None):
        
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2(p_.X, p_.Y, p_.Z))
    # end def ge_p3_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $h
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_p3_dbl(self, p_=None):
        
        
        q_ = self.ge_p3_to_p2(p_)
        return self.ge_p2_dbl(q_)
    # end def ge_p3_dbl
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #//
    @classmethod
    def ge_precomp_0(self):
        
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_precomp_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $b
    #// @param int $c
    #// @return int
    #//
    @classmethod
    def equal(self, b_=None, c_=None):
        
        
        return php_int(b_ ^ c_ - 1 & 4294967295 >> 31)
    # end def equal
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int|string $char
    #// @return int (1 = yes, 0 = no)
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def negative(self, char_=None):
        
        
        if php_is_int(char_):
            return 1 if char_ < 0 else 0
        # end if
        x_ = self.chrtoint(self.substr(char_, 0, 1))
        return php_int(x_ >> 63)
    # end def negative
    #// 
    #// Conditional move
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $t
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $u
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #//
    @classmethod
    def cmov(self, t_=None, u_=None, b_=None):
        
        
        if (not php_is_int(b_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer."))
        # end if
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_cmov(t_.yplusx, u_.yplusx, b_), self.fe_cmov(t_.yminusx, u_.yminusx, b_), self.fe_cmov(t_.xy2d, u_.xy2d, b_)))
    # end def cmov
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $pos
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def ge_select(self, pos_=0, b_=0):
        
        
        base_ = None
        if base_ == None:
            base_ = Array()
            #// @var int $i
            for i_,bas_ in self.base:
                j_ = 0
                while j_ < 8:
                    
                    base_[i_][j_] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas_[j_][0]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas_[j_][1]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas_[j_][2])))
                    j_ += 1
                # end while
            # end for
        # end if
        #// @var array<int, array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Precomp>> $base
        if (not php_is_int(pos_)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Position must be an integer"))
        # end if
        if pos_ < 0 or pos_ > 31:
            raise php_new_class("RangeException", lambda : RangeException("Position is out of range [0, 31]"))
        # end if
        #// @var int $bnegative
        bnegative_ = self.negative(b_)
        #// @var int $babs
        babs_ = b_ - -bnegative_ & b_ << 1
        t_ = self.ge_precomp_0()
        i_ = 0
        while i_ < 8:
            
            t_ = self.cmov(t_, base_[pos_][i_], self.equal(babs_, i_ + 1))
            i_ += 1
        # end while
        minusT_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_copy(t_.yminusx), self.fe_copy(t_.yplusx), self.fe_neg(t_.xy2d)))
        return self.cmov(t_, minusT_, bnegative_)
    # end def ge_select
    #// 
    #// Subtract two group elements.
    #// 
    #// r = p - q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_sub(self, p_=None, q_=None):
        
        
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P2 $h
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
    #// @param string $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #//
    @classmethod
    def ge_double_scalarmult_vartime(self, a_=None, A_=None, b_=None):
        
        
        #// @var array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Cached> $Ai
        Ai_ = Array()
        Bi_ = Array()
        if (not Bi_):
            i_ = 0
            while i_ < 8:
                
                Bi_[i_] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i_][0]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i_][1]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i_][2])))
                i_ += 1
            # end while
        # end if
        i_ = 0
        while i_ < 8:
            
            Ai_[i_] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Cached(self.fe_0(), self.fe_0(), self.fe_0(), self.fe_0()))
            i_ += 1
        # end while
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
            #// # if (bslide[i] > 0) {
            if bslide_[i_] > 0:
                #// @var int $index
                index_ = php_int(floor(bslide_[i_] / 2))
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_madd(&t,&u,&Bi[bslide[i]/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                t_ = self.ge_madd(t_, u_, Bi_[index_])
                pass
            elif bslide_[i_] < 0:
                #// @var int $index
                index_ = php_int(floor(-bslide_[i_] / 2))
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_msub(&t,&u,&Bi[(-bslide[i])/2]);
                u_ = self.ge_p1p1_to_p3(t_)
                t_ = self.ge_msub(t_, u_, Bi_[index_])
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def ge_scalarmult_base(self, a_=None):
        
        
        #// @var array<int, int> $e
        e_ = Array()
        r_ = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @throws TypeError
    #//
    @classmethod
    def sc_muladd(self, a_=None, b_=None, c_=None):
        
        
        #// @var int $a0
        a0_ = 2097151 & self.load_3(self.substr(a_, 0, 3))
        #// @var int $a1
        a1_ = 2097151 & self.load_4(self.substr(a_, 2, 4)) >> 5
        #// @var int $a2
        a2_ = 2097151 & self.load_3(self.substr(a_, 5, 3)) >> 2
        #// @var int $a3
        a3_ = 2097151 & self.load_4(self.substr(a_, 7, 4)) >> 7
        #// @var int $a4
        a4_ = 2097151 & self.load_4(self.substr(a_, 10, 4)) >> 4
        #// @var int $a5
        a5_ = 2097151 & self.load_3(self.substr(a_, 13, 3)) >> 1
        #// @var int $a6
        a6_ = 2097151 & self.load_4(self.substr(a_, 15, 4)) >> 6
        #// @var int $a7
        a7_ = 2097151 & self.load_3(self.substr(a_, 18, 3)) >> 3
        #// @var int $a8
        a8_ = 2097151 & self.load_3(self.substr(a_, 21, 3))
        #// @var int $a9
        a9_ = 2097151 & self.load_4(self.substr(a_, 23, 4)) >> 5
        #// @var int $a10
        a10_ = 2097151 & self.load_3(self.substr(a_, 26, 3)) >> 2
        #// @var int $a11
        a11_ = self.load_4(self.substr(a_, 28, 4)) >> 7
        #// @var int $b0
        b0_ = 2097151 & self.load_3(self.substr(b_, 0, 3))
        #// @var int $b1
        b1_ = 2097151 & self.load_4(self.substr(b_, 2, 4)) >> 5
        #// @var int $b2
        b2_ = 2097151 & self.load_3(self.substr(b_, 5, 3)) >> 2
        #// @var int $b3
        b3_ = 2097151 & self.load_4(self.substr(b_, 7, 4)) >> 7
        #// @var int $b4
        b4_ = 2097151 & self.load_4(self.substr(b_, 10, 4)) >> 4
        #// @var int $b5
        b5_ = 2097151 & self.load_3(self.substr(b_, 13, 3)) >> 1
        #// @var int $b6
        b6_ = 2097151 & self.load_4(self.substr(b_, 15, 4)) >> 6
        #// @var int $b7
        b7_ = 2097151 & self.load_3(self.substr(b_, 18, 3)) >> 3
        #// @var int $b8
        b8_ = 2097151 & self.load_3(self.substr(b_, 21, 3))
        #// @var int $b9
        b9_ = 2097151 & self.load_4(self.substr(b_, 23, 4)) >> 5
        #// @var int $b10
        b10_ = 2097151 & self.load_3(self.substr(b_, 26, 3)) >> 2
        #// @var int $b11
        b11_ = self.load_4(self.substr(b_, 28, 4)) >> 7
        #// @var int $c0
        c0_ = 2097151 & self.load_3(self.substr(c_, 0, 3))
        #// @var int $c1
        c1_ = 2097151 & self.load_4(self.substr(c_, 2, 4)) >> 5
        #// @var int $c2
        c2_ = 2097151 & self.load_3(self.substr(c_, 5, 3)) >> 2
        #// @var int $c3
        c3_ = 2097151 & self.load_4(self.substr(c_, 7, 4)) >> 7
        #// @var int $c4
        c4_ = 2097151 & self.load_4(self.substr(c_, 10, 4)) >> 4
        #// @var int $c5
        c5_ = 2097151 & self.load_3(self.substr(c_, 13, 3)) >> 1
        #// @var int $c6
        c6_ = 2097151 & self.load_4(self.substr(c_, 15, 4)) >> 6
        #// @var int $c7
        c7_ = 2097151 & self.load_3(self.substr(c_, 18, 3)) >> 3
        #// @var int $c8
        c8_ = 2097151 & self.load_3(self.substr(c_, 21, 3))
        #// @var int $c9
        c9_ = 2097151 & self.load_4(self.substr(c_, 23, 4)) >> 5
        #// @var int $c10
        c10_ = 2097151 & self.load_3(self.substr(c_, 26, 3)) >> 2
        #// @var int $c11
        c11_ = self.load_4(self.substr(c_, 28, 4)) >> 7
        #// Can't really avoid the pyramid here:
        s0_ = c0_ + self.mul(a0_, b0_, 24)
        s1_ = c1_ + self.mul(a0_, b1_, 24) + self.mul(a1_, b0_, 24)
        s2_ = c2_ + self.mul(a0_, b2_, 24) + self.mul(a1_, b1_, 24) + self.mul(a2_, b0_, 24)
        s3_ = c3_ + self.mul(a0_, b3_, 24) + self.mul(a1_, b2_, 24) + self.mul(a2_, b1_, 24) + self.mul(a3_, b0_, 24)
        s4_ = c4_ + self.mul(a0_, b4_, 24) + self.mul(a1_, b3_, 24) + self.mul(a2_, b2_, 24) + self.mul(a3_, b1_, 24) + self.mul(a4_, b0_, 24)
        s5_ = c5_ + self.mul(a0_, b5_, 24) + self.mul(a1_, b4_, 24) + self.mul(a2_, b3_, 24) + self.mul(a3_, b2_, 24) + self.mul(a4_, b1_, 24) + self.mul(a5_, b0_, 24)
        s6_ = c6_ + self.mul(a0_, b6_, 24) + self.mul(a1_, b5_, 24) + self.mul(a2_, b4_, 24) + self.mul(a3_, b3_, 24) + self.mul(a4_, b2_, 24) + self.mul(a5_, b1_, 24) + self.mul(a6_, b0_, 24)
        s7_ = c7_ + self.mul(a0_, b7_, 24) + self.mul(a1_, b6_, 24) + self.mul(a2_, b5_, 24) + self.mul(a3_, b4_, 24) + self.mul(a4_, b3_, 24) + self.mul(a5_, b2_, 24) + self.mul(a6_, b1_, 24) + self.mul(a7_, b0_, 24)
        s8_ = c8_ + self.mul(a0_, b8_, 24) + self.mul(a1_, b7_, 24) + self.mul(a2_, b6_, 24) + self.mul(a3_, b5_, 24) + self.mul(a4_, b4_, 24) + self.mul(a5_, b3_, 24) + self.mul(a6_, b2_, 24) + self.mul(a7_, b1_, 24) + self.mul(a8_, b0_, 24)
        s9_ = c9_ + self.mul(a0_, b9_, 24) + self.mul(a1_, b8_, 24) + self.mul(a2_, b7_, 24) + self.mul(a3_, b6_, 24) + self.mul(a4_, b5_, 24) + self.mul(a5_, b4_, 24) + self.mul(a6_, b3_, 24) + self.mul(a7_, b2_, 24) + self.mul(a8_, b1_, 24) + self.mul(a9_, b0_, 24)
        s10_ = c10_ + self.mul(a0_, b10_, 24) + self.mul(a1_, b9_, 24) + self.mul(a2_, b8_, 24) + self.mul(a3_, b7_, 24) + self.mul(a4_, b6_, 24) + self.mul(a5_, b5_, 24) + self.mul(a6_, b4_, 24) + self.mul(a7_, b3_, 24) + self.mul(a8_, b2_, 24) + self.mul(a9_, b1_, 24) + self.mul(a10_, b0_, 24)
        s11_ = c11_ + self.mul(a0_, b11_, 24) + self.mul(a1_, b10_, 24) + self.mul(a2_, b9_, 24) + self.mul(a3_, b8_, 24) + self.mul(a4_, b7_, 24) + self.mul(a5_, b6_, 24) + self.mul(a6_, b5_, 24) + self.mul(a7_, b4_, 24) + self.mul(a8_, b3_, 24) + self.mul(a9_, b2_, 24) + self.mul(a10_, b1_, 24) + self.mul(a11_, b0_, 24)
        s12_ = self.mul(a1_, b11_, 24) + self.mul(a2_, b10_, 24) + self.mul(a3_, b9_, 24) + self.mul(a4_, b8_, 24) + self.mul(a5_, b7_, 24) + self.mul(a6_, b6_, 24) + self.mul(a7_, b5_, 24) + self.mul(a8_, b4_, 24) + self.mul(a9_, b3_, 24) + self.mul(a10_, b2_, 24) + self.mul(a11_, b1_, 24)
        s13_ = self.mul(a2_, b11_, 24) + self.mul(a3_, b10_, 24) + self.mul(a4_, b9_, 24) + self.mul(a5_, b8_, 24) + self.mul(a6_, b7_, 24) + self.mul(a7_, b6_, 24) + self.mul(a8_, b5_, 24) + self.mul(a9_, b4_, 24) + self.mul(a10_, b3_, 24) + self.mul(a11_, b2_, 24)
        s14_ = self.mul(a3_, b11_, 24) + self.mul(a4_, b10_, 24) + self.mul(a5_, b9_, 24) + self.mul(a6_, b8_, 24) + self.mul(a7_, b7_, 24) + self.mul(a8_, b6_, 24) + self.mul(a9_, b5_, 24) + self.mul(a10_, b4_, 24) + self.mul(a11_, b3_, 24)
        s15_ = self.mul(a4_, b11_, 24) + self.mul(a5_, b10_, 24) + self.mul(a6_, b9_, 24) + self.mul(a7_, b8_, 24) + self.mul(a8_, b7_, 24) + self.mul(a9_, b6_, 24) + self.mul(a10_, b5_, 24) + self.mul(a11_, b4_, 24)
        s16_ = self.mul(a5_, b11_, 24) + self.mul(a6_, b10_, 24) + self.mul(a7_, b9_, 24) + self.mul(a8_, b8_, 24) + self.mul(a9_, b7_, 24) + self.mul(a10_, b6_, 24) + self.mul(a11_, b5_, 24)
        s17_ = self.mul(a6_, b11_, 24) + self.mul(a7_, b10_, 24) + self.mul(a8_, b9_, 24) + self.mul(a9_, b8_, 24) + self.mul(a10_, b7_, 24) + self.mul(a11_, b6_, 24)
        s18_ = self.mul(a7_, b11_, 24) + self.mul(a8_, b10_, 24) + self.mul(a9_, b9_, 24) + self.mul(a10_, b8_, 24) + self.mul(a11_, b7_, 24)
        s19_ = self.mul(a8_, b11_, 24) + self.mul(a9_, b10_, 24) + self.mul(a10_, b9_, 24) + self.mul(a11_, b8_, 24)
        s20_ = self.mul(a9_, b11_, 24) + self.mul(a10_, b10_, 24) + self.mul(a11_, b9_, 24)
        s21_ = self.mul(a10_, b11_, 24) + self.mul(a11_, b10_, 24)
        s22_ = self.mul(a11_, b11_, 24)
        s23_ = 0
        #// @var int $carry0
        carry0_ = s0_ + 1 << 20 >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry2
        carry2_ = s2_ + 1 << 20 >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry4
        carry4_ = s4_ + 1 << 20 >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry6
        carry6_ = s6_ + 1 << 20 >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry8
        carry8_ = s8_ + 1 << 20 >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry10
        carry10_ = s10_ + 1 << 20 >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry12
        carry12_ = s12_ + 1 << 20 >> 21
        s13_ += carry12_
        s12_ -= carry12_ << 21
        #// @var int $carry14
        carry14_ = s14_ + 1 << 20 >> 21
        s15_ += carry14_
        s14_ -= carry14_ << 21
        #// @var int $carry16
        carry16_ = s16_ + 1 << 20 >> 21
        s17_ += carry16_
        s16_ -= carry16_ << 21
        #// @var int $carry18
        carry18_ = s18_ + 1 << 20 >> 21
        s19_ += carry18_
        s18_ -= carry18_ << 21
        #// @var int $carry20
        carry20_ = s20_ + 1 << 20 >> 21
        s21_ += carry20_
        s20_ -= carry20_ << 21
        #// @var int $carry22
        carry22_ = s22_ + 1 << 20 >> 21
        s23_ += carry22_
        s22_ -= carry22_ << 21
        #// @var int $carry1
        carry1_ = s1_ + 1 << 20 >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry3
        carry3_ = s3_ + 1 << 20 >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry5
        carry5_ = s5_ + 1 << 20 >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry7
        carry7_ = s7_ + 1 << 20 >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry9
        carry9_ = s9_ + 1 << 20 >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry11
        carry11_ = s11_ + 1 << 20 >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        #// @var int $carry13
        carry13_ = s13_ + 1 << 20 >> 21
        s14_ += carry13_
        s13_ -= carry13_ << 21
        #// @var int $carry15
        carry15_ = s15_ + 1 << 20 >> 21
        s16_ += carry15_
        s15_ -= carry15_ << 21
        #// @var int $carry17
        carry17_ = s17_ + 1 << 20 >> 21
        s18_ += carry17_
        s17_ -= carry17_ << 21
        #// @var int $carry19
        carry19_ = s19_ + 1 << 20 >> 21
        s20_ += carry19_
        s19_ -= carry19_ << 21
        #// @var int $carry21
        carry21_ = s21_ + 1 << 20 >> 21
        s22_ += carry21_
        s21_ -= carry21_ << 21
        s11_ += self.mul(s23_, 666643, 20)
        s12_ += self.mul(s23_, 470296, 19)
        s13_ += self.mul(s23_, 654183, 20)
        s14_ -= self.mul(s23_, 997805, 20)
        s15_ += self.mul(s23_, 136657, 18)
        s16_ -= self.mul(s23_, 683901, 20)
        s10_ += self.mul(s22_, 666643, 20)
        s11_ += self.mul(s22_, 470296, 19)
        s12_ += self.mul(s22_, 654183, 20)
        s13_ -= self.mul(s22_, 997805, 20)
        s14_ += self.mul(s22_, 136657, 18)
        s15_ -= self.mul(s22_, 683901, 20)
        s9_ += self.mul(s21_, 666643, 20)
        s10_ += self.mul(s21_, 470296, 19)
        s11_ += self.mul(s21_, 654183, 20)
        s12_ -= self.mul(s21_, 997805, 20)
        s13_ += self.mul(s21_, 136657, 18)
        s14_ -= self.mul(s21_, 683901, 20)
        s8_ += self.mul(s20_, 666643, 20)
        s9_ += self.mul(s20_, 470296, 19)
        s10_ += self.mul(s20_, 654183, 20)
        s11_ -= self.mul(s20_, 997805, 20)
        s12_ += self.mul(s20_, 136657, 18)
        s13_ -= self.mul(s20_, 683901, 20)
        s7_ += self.mul(s19_, 666643, 20)
        s8_ += self.mul(s19_, 470296, 19)
        s9_ += self.mul(s19_, 654183, 20)
        s10_ -= self.mul(s19_, 997805, 20)
        s11_ += self.mul(s19_, 136657, 18)
        s12_ -= self.mul(s19_, 683901, 20)
        s6_ += self.mul(s18_, 666643, 20)
        s7_ += self.mul(s18_, 470296, 19)
        s8_ += self.mul(s18_, 654183, 20)
        s9_ -= self.mul(s18_, 997805, 20)
        s10_ += self.mul(s18_, 136657, 18)
        s11_ -= self.mul(s18_, 683901, 20)
        #// @var int $carry6
        carry6_ = s6_ + 1 << 20 >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry8
        carry8_ = s8_ + 1 << 20 >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry10
        carry10_ = s10_ + 1 << 20 >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry12
        carry12_ = s12_ + 1 << 20 >> 21
        s13_ += carry12_
        s12_ -= carry12_ << 21
        #// @var int $carry14
        carry14_ = s14_ + 1 << 20 >> 21
        s15_ += carry14_
        s14_ -= carry14_ << 21
        #// @var int $carry16
        carry16_ = s16_ + 1 << 20 >> 21
        s17_ += carry16_
        s16_ -= carry16_ << 21
        #// @var int $carry7
        carry7_ = s7_ + 1 << 20 >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry9
        carry9_ = s9_ + 1 << 20 >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry11
        carry11_ = s11_ + 1 << 20 >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        #// @var int $carry13
        carry13_ = s13_ + 1 << 20 >> 21
        s14_ += carry13_
        s13_ -= carry13_ << 21
        #// @var int $carry15
        carry15_ = s15_ + 1 << 20 >> 21
        s16_ += carry15_
        s15_ -= carry15_ << 21
        s5_ += self.mul(s17_, 666643, 20)
        s6_ += self.mul(s17_, 470296, 19)
        s7_ += self.mul(s17_, 654183, 20)
        s8_ -= self.mul(s17_, 997805, 20)
        s9_ += self.mul(s17_, 136657, 18)
        s10_ -= self.mul(s17_, 683901, 20)
        s4_ += self.mul(s16_, 666643, 20)
        s5_ += self.mul(s16_, 470296, 19)
        s6_ += self.mul(s16_, 654183, 20)
        s7_ -= self.mul(s16_, 997805, 20)
        s8_ += self.mul(s16_, 136657, 18)
        s9_ -= self.mul(s16_, 683901, 20)
        s3_ += self.mul(s15_, 666643, 20)
        s4_ += self.mul(s15_, 470296, 19)
        s5_ += self.mul(s15_, 654183, 20)
        s6_ -= self.mul(s15_, 997805, 20)
        s7_ += self.mul(s15_, 136657, 18)
        s8_ -= self.mul(s15_, 683901, 20)
        s2_ += self.mul(s14_, 666643, 20)
        s3_ += self.mul(s14_, 470296, 19)
        s4_ += self.mul(s14_, 654183, 20)
        s5_ -= self.mul(s14_, 997805, 20)
        s6_ += self.mul(s14_, 136657, 18)
        s7_ -= self.mul(s14_, 683901, 20)
        s1_ += self.mul(s13_, 666643, 20)
        s2_ += self.mul(s13_, 470296, 19)
        s3_ += self.mul(s13_, 654183, 20)
        s4_ -= self.mul(s13_, 997805, 20)
        s5_ += self.mul(s13_, 136657, 18)
        s6_ -= self.mul(s13_, 683901, 20)
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        s12_ = 0
        #// @var int $carry0
        carry0_ = s0_ + 1 << 20 >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry2
        carry2_ = s2_ + 1 << 20 >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry4
        carry4_ = s4_ + 1 << 20 >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry6
        carry6_ = s6_ + 1 << 20 >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry8
        carry8_ = s8_ + 1 << 20 >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry10
        carry10_ = s10_ + 1 << 20 >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry1
        carry1_ = s1_ + 1 << 20 >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry3
        carry3_ = s3_ + 1 << 20 >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry5
        carry5_ = s5_ + 1 << 20 >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry7
        carry7_ = s7_ + 1 << 20 >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry9
        carry9_ = s9_ + 1 << 20 >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry11
        carry11_ = s11_ + 1 << 20 >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        s12_ = 0
        #// @var int $carry0
        carry0_ = s0_ >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry1
        carry1_ = s1_ >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry2
        carry2_ = s2_ >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry3
        carry3_ = s3_ >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry4
        carry4_ = s4_ >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry5
        carry5_ = s5_ >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry6
        carry6_ = s6_ >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry7
        carry7_ = s7_ >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry8
        carry8_ = s8_ >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry9
        carry9_ = s9_ >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry10
        carry10_ = s10_ >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry11
        carry11_ = s11_ >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        #// @var int $carry0
        carry0_ = s0_ >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry1
        carry1_ = s1_ >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry2
        carry2_ = s2_ >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry3
        carry3_ = s3_ >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry4
        carry4_ = s4_ >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry5
        carry5_ = s5_ >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry6
        carry6_ = s6_ >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry7
        carry7_ = s7_ >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry8
        carry8_ = s8_ >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry9
        carry9_ = s9_ >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry10
        carry10_ = s10_ >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// 
        #// @var array<int, int>
        #//
        arr_ = Array(php_int(255 & s0_ >> 0), php_int(255 & s0_ >> 8), php_int(255 & s0_ >> 16 | s1_ << 5), php_int(255 & s1_ >> 3), php_int(255 & s1_ >> 11), php_int(255 & s1_ >> 19 | s2_ << 2), php_int(255 & s2_ >> 6), php_int(255 & s2_ >> 14 | s3_ << 7), php_int(255 & s3_ >> 1), php_int(255 & s3_ >> 9), php_int(255 & s3_ >> 17 | s4_ << 4), php_int(255 & s4_ >> 4), php_int(255 & s4_ >> 12), php_int(255 & s4_ >> 20 | s5_ << 1), php_int(255 & s5_ >> 7), php_int(255 & s5_ >> 15 | s6_ << 6), php_int(255 & s6_ >> 2), php_int(255 & s6_ >> 10), php_int(255 & s6_ >> 18 | s7_ << 3), php_int(255 & s7_ >> 5), php_int(255 & s7_ >> 13), php_int(255 & s8_ >> 0), php_int(255 & s8_ >> 8), php_int(255 & s8_ >> 16 | s9_ << 5), php_int(255 & s9_ >> 3), php_int(255 & s9_ >> 11), php_int(255 & s9_ >> 19 | s10_ << 2), php_int(255 & s10_ >> 6), php_int(255 & s10_ >> 14 | s11_ << 7), php_int(255 & s11_ >> 1), php_int(255 & s11_ >> 9), 255 & s11_ >> 17)
        return self.intarraytostring(arr_)
    # end def sc_muladd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def sc_reduce(self, s_=None):
        
        
        #// @var int $s0
        s0_ = 2097151 & self.load_3(self.substr(s_, 0, 3))
        #// @var int $s1
        s1_ = 2097151 & self.load_4(self.substr(s_, 2, 4)) >> 5
        #// @var int $s2
        s2_ = 2097151 & self.load_3(self.substr(s_, 5, 3)) >> 2
        #// @var int $s3
        s3_ = 2097151 & self.load_4(self.substr(s_, 7, 4)) >> 7
        #// @var int $s4
        s4_ = 2097151 & self.load_4(self.substr(s_, 10, 4)) >> 4
        #// @var int $s5
        s5_ = 2097151 & self.load_3(self.substr(s_, 13, 3)) >> 1
        #// @var int $s6
        s6_ = 2097151 & self.load_4(self.substr(s_, 15, 4)) >> 6
        #// @var int $s7
        s7_ = 2097151 & self.load_3(self.substr(s_, 18, 4)) >> 3
        #// @var int $s8
        s8_ = 2097151 & self.load_3(self.substr(s_, 21, 3))
        #// @var int $s9
        s9_ = 2097151 & self.load_4(self.substr(s_, 23, 4)) >> 5
        #// @var int $s10
        s10_ = 2097151 & self.load_3(self.substr(s_, 26, 3)) >> 2
        #// @var int $s11
        s11_ = 2097151 & self.load_4(self.substr(s_, 28, 4)) >> 7
        #// @var int $s12
        s12_ = 2097151 & self.load_4(self.substr(s_, 31, 4)) >> 4
        #// @var int $s13
        s13_ = 2097151 & self.load_3(self.substr(s_, 34, 3)) >> 1
        #// @var int $s14
        s14_ = 2097151 & self.load_4(self.substr(s_, 36, 4)) >> 6
        #// @var int $s15
        s15_ = 2097151 & self.load_3(self.substr(s_, 39, 4)) >> 3
        #// @var int $s16
        s16_ = 2097151 & self.load_3(self.substr(s_, 42, 3))
        #// @var int $s17
        s17_ = 2097151 & self.load_4(self.substr(s_, 44, 4)) >> 5
        #// @var int $s18
        s18_ = 2097151 & self.load_3(self.substr(s_, 47, 3)) >> 2
        #// @var int $s19
        s19_ = 2097151 & self.load_4(self.substr(s_, 49, 4)) >> 7
        #// @var int $s20
        s20_ = 2097151 & self.load_4(self.substr(s_, 52, 4)) >> 4
        #// @var int $s21
        s21_ = 2097151 & self.load_3(self.substr(s_, 55, 3)) >> 1
        #// @var int $s22
        s22_ = 2097151 & self.load_4(self.substr(s_, 57, 4)) >> 6
        #// @var int $s23
        s23_ = self.load_4(self.substr(s_, 60, 4)) >> 3
        s11_ += self.mul(s23_, 666643, 20)
        s12_ += self.mul(s23_, 470296, 19)
        s13_ += self.mul(s23_, 654183, 20)
        s14_ -= self.mul(s23_, 997805, 20)
        s15_ += self.mul(s23_, 136657, 18)
        s16_ -= self.mul(s23_, 683901, 20)
        s10_ += self.mul(s22_, 666643, 20)
        s11_ += self.mul(s22_, 470296, 19)
        s12_ += self.mul(s22_, 654183, 20)
        s13_ -= self.mul(s22_, 997805, 20)
        s14_ += self.mul(s22_, 136657, 18)
        s15_ -= self.mul(s22_, 683901, 20)
        s9_ += self.mul(s21_, 666643, 20)
        s10_ += self.mul(s21_, 470296, 19)
        s11_ += self.mul(s21_, 654183, 20)
        s12_ -= self.mul(s21_, 997805, 20)
        s13_ += self.mul(s21_, 136657, 18)
        s14_ -= self.mul(s21_, 683901, 20)
        s8_ += self.mul(s20_, 666643, 20)
        s9_ += self.mul(s20_, 470296, 19)
        s10_ += self.mul(s20_, 654183, 20)
        s11_ -= self.mul(s20_, 997805, 20)
        s12_ += self.mul(s20_, 136657, 18)
        s13_ -= self.mul(s20_, 683901, 20)
        s7_ += self.mul(s19_, 666643, 20)
        s8_ += self.mul(s19_, 470296, 19)
        s9_ += self.mul(s19_, 654183, 20)
        s10_ -= self.mul(s19_, 997805, 20)
        s11_ += self.mul(s19_, 136657, 18)
        s12_ -= self.mul(s19_, 683901, 20)
        s6_ += self.mul(s18_, 666643, 20)
        s7_ += self.mul(s18_, 470296, 19)
        s8_ += self.mul(s18_, 654183, 20)
        s9_ -= self.mul(s18_, 997805, 20)
        s10_ += self.mul(s18_, 136657, 18)
        s11_ -= self.mul(s18_, 683901, 20)
        #// @var int $carry6
        carry6_ = s6_ + 1 << 20 >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry8
        carry8_ = s8_ + 1 << 20 >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry10
        carry10_ = s10_ + 1 << 20 >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry12
        carry12_ = s12_ + 1 << 20 >> 21
        s13_ += carry12_
        s12_ -= carry12_ << 21
        #// @var int $carry14
        carry14_ = s14_ + 1 << 20 >> 21
        s15_ += carry14_
        s14_ -= carry14_ << 21
        #// @var int $carry16
        carry16_ = s16_ + 1 << 20 >> 21
        s17_ += carry16_
        s16_ -= carry16_ << 21
        #// @var int $carry7
        carry7_ = s7_ + 1 << 20 >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry9
        carry9_ = s9_ + 1 << 20 >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry11
        carry11_ = s11_ + 1 << 20 >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        #// @var int $carry13
        carry13_ = s13_ + 1 << 20 >> 21
        s14_ += carry13_
        s13_ -= carry13_ << 21
        #// @var int $carry15
        carry15_ = s15_ + 1 << 20 >> 21
        s16_ += carry15_
        s15_ -= carry15_ << 21
        s5_ += self.mul(s17_, 666643, 20)
        s6_ += self.mul(s17_, 470296, 19)
        s7_ += self.mul(s17_, 654183, 20)
        s8_ -= self.mul(s17_, 997805, 20)
        s9_ += self.mul(s17_, 136657, 18)
        s10_ -= self.mul(s17_, 683901, 20)
        s4_ += self.mul(s16_, 666643, 20)
        s5_ += self.mul(s16_, 470296, 19)
        s6_ += self.mul(s16_, 654183, 20)
        s7_ -= self.mul(s16_, 997805, 20)
        s8_ += self.mul(s16_, 136657, 18)
        s9_ -= self.mul(s16_, 683901, 20)
        s3_ += self.mul(s15_, 666643, 20)
        s4_ += self.mul(s15_, 470296, 19)
        s5_ += self.mul(s15_, 654183, 20)
        s6_ -= self.mul(s15_, 997805, 20)
        s7_ += self.mul(s15_, 136657, 18)
        s8_ -= self.mul(s15_, 683901, 20)
        s2_ += self.mul(s14_, 666643, 20)
        s3_ += self.mul(s14_, 470296, 19)
        s4_ += self.mul(s14_, 654183, 20)
        s5_ -= self.mul(s14_, 997805, 20)
        s6_ += self.mul(s14_, 136657, 18)
        s7_ -= self.mul(s14_, 683901, 20)
        s1_ += self.mul(s13_, 666643, 20)
        s2_ += self.mul(s13_, 470296, 19)
        s3_ += self.mul(s13_, 654183, 20)
        s4_ -= self.mul(s13_, 997805, 20)
        s5_ += self.mul(s13_, 136657, 18)
        s6_ -= self.mul(s13_, 683901, 20)
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        s12_ = 0
        #// @var int $carry0
        carry0_ = s0_ + 1 << 20 >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry2
        carry2_ = s2_ + 1 << 20 >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry4
        carry4_ = s4_ + 1 << 20 >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry6
        carry6_ = s6_ + 1 << 20 >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry8
        carry8_ = s8_ + 1 << 20 >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry10
        carry10_ = s10_ + 1 << 20 >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry1
        carry1_ = s1_ + 1 << 20 >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry3
        carry3_ = s3_ + 1 << 20 >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry5
        carry5_ = s5_ + 1 << 20 >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry7
        carry7_ = s7_ + 1 << 20 >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry9
        carry9_ = s9_ + 1 << 20 >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry11
        carry11_ = s11_ + 1 << 20 >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        s12_ = 0
        #// @var int $carry0
        carry0_ = s0_ >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry1
        carry1_ = s1_ >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry2
        carry2_ = s2_ >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry3
        carry3_ = s3_ >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry4
        carry4_ = s4_ >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry5
        carry5_ = s5_ >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry6
        carry6_ = s6_ >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry7
        carry7_ = s7_ >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry8
        carry8_ = s8_ >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry9
        carry9_ = s9_ >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry10
        carry10_ = s10_ >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// @var int $carry11
        carry11_ = s11_ >> 21
        s12_ += carry11_
        s11_ -= carry11_ << 21
        s0_ += self.mul(s12_, 666643, 20)
        s1_ += self.mul(s12_, 470296, 19)
        s2_ += self.mul(s12_, 654183, 20)
        s3_ -= self.mul(s12_, 997805, 20)
        s4_ += self.mul(s12_, 136657, 18)
        s5_ -= self.mul(s12_, 683901, 20)
        #// @var int $carry0
        carry0_ = s0_ >> 21
        s1_ += carry0_
        s0_ -= carry0_ << 21
        #// @var int $carry1
        carry1_ = s1_ >> 21
        s2_ += carry1_
        s1_ -= carry1_ << 21
        #// @var int $carry2
        carry2_ = s2_ >> 21
        s3_ += carry2_
        s2_ -= carry2_ << 21
        #// @var int $carry3
        carry3_ = s3_ >> 21
        s4_ += carry3_
        s3_ -= carry3_ << 21
        #// @var int $carry4
        carry4_ = s4_ >> 21
        s5_ += carry4_
        s4_ -= carry4_ << 21
        #// @var int $carry5
        carry5_ = s5_ >> 21
        s6_ += carry5_
        s5_ -= carry5_ << 21
        #// @var int $carry6
        carry6_ = s6_ >> 21
        s7_ += carry6_
        s6_ -= carry6_ << 21
        #// @var int $carry7
        carry7_ = s7_ >> 21
        s8_ += carry7_
        s7_ -= carry7_ << 21
        #// @var int $carry8
        carry8_ = s8_ >> 21
        s9_ += carry8_
        s8_ -= carry8_ << 21
        #// @var int $carry9
        carry9_ = s9_ >> 21
        s10_ += carry9_
        s9_ -= carry9_ << 21
        #// @var int $carry10
        carry10_ = s10_ >> 21
        s11_ += carry10_
        s10_ -= carry10_ << 21
        #// 
        #// @var array<int, int>
        #//
        arr_ = Array(php_int(s0_ >> 0), php_int(s0_ >> 8), php_int(s0_ >> 16 | s1_ << 5), php_int(s1_ >> 3), php_int(s1_ >> 11), php_int(s1_ >> 19 | s2_ << 2), php_int(s2_ >> 6), php_int(s2_ >> 14 | s3_ << 7), php_int(s3_ >> 1), php_int(s3_ >> 9), php_int(s3_ >> 17 | s4_ << 4), php_int(s4_ >> 4), php_int(s4_ >> 12), php_int(s4_ >> 20 | s5_ << 1), php_int(s5_ >> 7), php_int(s5_ >> 15 | s6_ << 6), php_int(s6_ >> 2), php_int(s6_ >> 10), php_int(s6_ >> 18 | s7_ << 3), php_int(s7_ >> 5), php_int(s7_ >> 13), php_int(s8_ >> 0), php_int(s8_ >> 8), php_int(s8_ >> 16 | s9_ << 5), php_int(s9_ >> 3), php_int(s9_ >> 11), php_int(s9_ >> 19 | s10_ << 2), php_int(s10_ >> 6), php_int(s10_ >> 14 | s11_ << 7), php_int(s11_ >> 1), php_int(s11_ >> 9), php_int(s11_) >> 17)
        return self.intarraytostring(arr_)
    # end def sc_reduce
    #// 
    #// multiply by the order of the main subgroup l = 2^252+27742317777372353535851937790883648493
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_mul_l(self, A_=None):
        
        
        #// @var array<int, int> $aslide
        aslide_ = Array(13, 0, 0, 0, 0, -1, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 3, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        #// @var array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Cached> $Ai size 8
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
# end class ParagonIE_Sodium_Core_Curve25519
